use std::path::{Path, PathBuf};
use std::time::Duration;

use anyhow::{Context, Result};
use serde::{Deserialize, Serialize};
use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::net::UnixStream;
use tracing::{debug, warn};

use crate::menu;
use crate::state::update_tray_status;
use crate::types::TrayStatus;

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum ClientKind {
    Claude,
    Codex,
    Gemini,
    Cursor,
    Other(String),
}

impl ClientKind {
    pub fn label(&self) -> String {
        match self {
            Self::Claude => "Claude".to_string(),
            Self::Codex => "Codex".to_string(),
            Self::Gemini => "Gemini".to_string(),
            Self::Cursor => "Cursor".to_string(),
            Self::Other(value) => value.clone(),
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "kebab-case")]
pub enum MuxAgentStatus {
    Idle,
    Routing,
    Saturated,
    Restarting,
    Failed,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MuxService {
    pub name: String,
    pub status: MuxAgentStatus,
    pub queue_depth: usize,
    pub queue_capacity: usize,
    pub restart_count: u64,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ClientHealth {
    pub kind: ClientKind,
    pub ok: bool,
    pub detail: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ServerHealth {
    pub services: Vec<MuxService>,
    pub clients: Vec<ClientHealth>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct RouteSnapshot {
    pub routes: Vec<RouteEntry>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct RouteEntry {
    pub client: ClientKind,
    pub service: String,
    pub state: String,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DiagnosticsSnapshot {
    pub services: Vec<MuxService>,
    pub clients: Vec<ClientHealth>,
    pub restart_total: u64,
    pub notes: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "kebab-case")]
pub enum MuxControlCommand {
    Subscribe,
    GetStatus,
    RouteSnapshot,
    Diagnostics,
    RestartService { name: String },
    Verify { client_kind: ClientKind },
    Shutdown,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct MuxControlRequest {
    pub jsonrpc: String,
    pub id: u64,
    pub command: MuxControlCommand,
}

impl MuxControlRequest {
    pub fn new(id: u64, command: MuxControlCommand) -> Self {
        Self {
            jsonrpc: "2.0".to_string(),
            id,
            command,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "kebab-case")]
pub enum IpcEvent {
    StateChange {
        status: MuxAgentStatus,
        services: Vec<MuxService>,
    },
    ServerHealth(ServerHealth),
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "kebab-case")]
pub enum MuxControlResponse {
    Ack {
        id: Option<u64>,
        message: String,
    },
    Status {
        id: Option<u64>,
        health: ServerHealth,
    },
    RouteSnapshot {
        id: Option<u64>,
        snapshot: RouteSnapshot,
    },
    Diagnostics {
        id: Option<u64>,
        snapshot: DiagnosticsSnapshot,
    },
    Verify {
        id: Option<u64>,
        result: ClientHealth,
    },
    Event {
        event: IpcEvent,
    },
    Error {
        id: Option<u64>,
        message: String,
    },
}

pub fn default_socket_path() -> PathBuf {
    std::env::var_os("HOME")
        .map(PathBuf::from)
        .unwrap_or_else(|| PathBuf::from("."))
        .join(".rust-mux/ipc/control.sock")
}

pub async fn subscribe_loop(socket_path: PathBuf) {
    let mut attempt = 0u32;
    let mut backoff = Duration::from_secs(1);
    loop {
        match subscribe_once(&socket_path).await {
            Ok(()) => {
                attempt = 0;
                backoff = Duration::from_secs(1);
            }
            Err(error) => {
                attempt += 1;
                warn!("mux tray IPC subscribe failed attempt {attempt}/10: {error:#}");
                if attempt >= 10 {
                    let _ = update_tray_status(TrayStatus::Failed);
                    return;
                }
                tokio::time::sleep(backoff).await;
                backoff = (backoff * 2).min(Duration::from_secs(30));
            }
        }
    }
}

async fn subscribe_once(socket_path: &Path) -> Result<()> {
    let stream = UnixStream::connect(socket_path)
        .await
        .with_context(|| format!("connect {}", socket_path.display()))?;
    let (reader, mut writer) = stream.into_split();
    write_request(&mut writer, 1, &MuxControlCommand::Subscribe).await?;
    let mut lines = BufReader::new(reader).lines();
    while let Some(line) = lines.next_line().await? {
        let response: MuxControlResponse = serde_json::from_str(&line)?;
        if let MuxControlResponse::Event { event } = response {
            handle_event(event)?;
        } else {
            debug!("mux subscribe response: {response:?}");
        }
    }
    anyhow::bail!("mux IPC stream closed")
}

fn handle_event(event: IpcEvent) -> Result<()> {
    match event {
        IpcEvent::StateChange { status, services } => apply_services(status, &services),
        IpcEvent::ServerHealth(health) => {
            apply_services(aggregate_status(&health.services), &health.services)
        }
    }
}

fn apply_services(status: MuxAgentStatus, services: &[MuxService]) -> Result<()> {
    menu::refresh_service_count(services.len());
    update_tray_status(match aggregate_with_capacity(status, services) {
        MuxAgentStatus::Idle => TrayStatus::Idle,
        MuxAgentStatus::Routing => TrayStatus::Routing,
        MuxAgentStatus::Saturated => TrayStatus::Saturated,
        MuxAgentStatus::Restarting => TrayStatus::Restarting,
        MuxAgentStatus::Failed => TrayStatus::Failed,
    })
}

fn aggregate_status(services: &[MuxService]) -> MuxAgentStatus {
    if services.iter().any(|s| s.status == MuxAgentStatus::Failed) {
        MuxAgentStatus::Failed
    } else if services
        .iter()
        .any(|s| s.status == MuxAgentStatus::Restarting)
    {
        MuxAgentStatus::Restarting
    } else if services.iter().any(|s| {
        aggregate_with_capacity(s.status, std::slice::from_ref(s)) == MuxAgentStatus::Saturated
    }) {
        MuxAgentStatus::Saturated
    } else if services.iter().any(|s| s.status == MuxAgentStatus::Routing) {
        MuxAgentStatus::Routing
    } else {
        MuxAgentStatus::Idle
    }
}

fn aggregate_with_capacity(status: MuxAgentStatus, services: &[MuxService]) -> MuxAgentStatus {
    if status == MuxAgentStatus::Saturated
        || services
            .iter()
            .any(|s| s.queue_capacity > 0 && s.queue_depth * 100 >= s.queue_capacity * 80)
    {
        MuxAgentStatus::Saturated
    } else {
        status
    }
}

pub async fn send_command(
    socket_path: impl AsRef<Path>,
    command: &MuxControlCommand,
) -> Result<MuxControlResponse> {
    let mut stream = UnixStream::connect(socket_path.as_ref()).await?;
    write_request(&mut stream, 1, command).await?;
    let mut lines = BufReader::new(stream).lines();
    let Some(line) = lines.next_line().await? else {
        anyhow::bail!("mux IPC returned no response");
    };
    serde_json::from_str(&line).context("decode mux response")
}

async fn write_request<W>(writer: &mut W, id: u64, command: &MuxControlCommand) -> Result<()>
where
    W: AsyncWriteExt + Unpin,
{
    let encoded = serde_json::to_string(&MuxControlRequest::new(id, command.clone()))?;
    writer.write_all(encoded.as_bytes()).await?;
    writer.write_all(b"\n").await?;
    writer.flush().await?;
    Ok(())
}

pub async fn stop_mux_daemon(socket_path: &Path) -> Result<MuxControlResponse> {
    send_command(socket_path, &MuxControlCommand::Shutdown).await
}

pub async fn restart_service(socket_path: &Path, name: &str) -> Result<MuxControlResponse> {
    send_command(
        socket_path,
        &MuxControlCommand::RestartService {
            name: name.to_string(),
        },
    )
    .await
}

pub async fn verify_client(socket_path: &Path, client_kind: ClientKind) -> Result<String> {
    match send_command(socket_path, &MuxControlCommand::Verify { client_kind }).await? {
        MuxControlResponse::Verify { result, .. } => Ok(format!(
            "{}: {} ({})",
            result.kind.label(),
            if result.ok { "ok" } else { "drift" },
            result.detail
        )),
        MuxControlResponse::Error { message, .. } => anyhow::bail!(message),
        other => Ok(format!("{other:?}")),
    }
}

pub async fn route_snapshot(socket_path: PathBuf) -> Result<String> {
    match send_command(&socket_path, &MuxControlCommand::RouteSnapshot).await? {
        MuxControlResponse::RouteSnapshot { snapshot, .. } => {
            Ok(serde_json::to_string_pretty(&snapshot)?)
        }
        MuxControlResponse::Error { message, .. } => anyhow::bail!(message),
        other => Ok(format!("{other:?}")),
    }
}

pub async fn diagnostics(socket_path: PathBuf) -> Result<String> {
    match send_command(&socket_path, &MuxControlCommand::Diagnostics).await? {
        MuxControlResponse::Diagnostics { snapshot, .. } => {
            Ok(serde_json::to_string_pretty(&snapshot)?)
        }
        MuxControlResponse::Error { message, .. } => anyhow::bail!(message),
        other => Ok(format!("{other:?}")),
    }
}
