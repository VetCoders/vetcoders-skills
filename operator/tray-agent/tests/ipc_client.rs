use std::time::Duration;

use tokio::io::{AsyncBufReadExt, AsyncWriteExt, BufReader};
use tokio::net::UnixListener;
use tray_agent::ipc_client::{
    IpcEvent, MuxAgentStatus, MuxControlCommand, MuxControlRequest, MuxControlResponse, MuxService,
};

#[tokio::test]
async fn subscribe_event_updates_status_channel() {
    let dir = tempfile::tempdir().expect("tempdir");
    let socket = dir.path().join("control.sock");
    let listener = UnixListener::bind(&socket).expect("bind");
    let status_rx = tray_agent::state::init_channels().expect("status channel");

    let server = tokio::spawn(async move {
        let (stream, _) = listener.accept().await.expect("accept");
        let (reader, mut writer) = stream.into_split();
        let mut lines = BufReader::new(reader).lines();
        let line = lines.next_line().await.expect("read").expect("line");
        let request: MuxControlRequest = serde_json::from_str(&line).expect("request");
        assert_eq!(request.command, MuxControlCommand::Subscribe);
        let response = MuxControlResponse::Event {
            event: IpcEvent::StateChange {
                status: MuxAgentStatus::Routing,
                services: vec![MuxService {
                    name: "memex".to_string(),
                    status: MuxAgentStatus::Routing,
                    queue_depth: 1,
                    queue_capacity: 10,
                    restart_count: 0,
                }],
            },
        };
        writer
            .write_all(serde_json::to_string(&response).unwrap().as_bytes())
            .await
            .unwrap();
        writer.write_all(b"\n").await.unwrap();
    });

    let client = tokio::spawn(tray_agent::ipc_client::subscribe_loop(socket));
    let status = tokio::task::spawn_blocking(move || {
        status_rx
            .recv_timeout(Duration::from_secs(2))
            .expect("status update")
    })
    .await
    .unwrap();

    assert_eq!(status, tray_agent::TrayStatus::Routing);
    server.await.unwrap();
    client.abort();
}
