# Fundacja Agents OS

## Teza

Agents OS to nie jest worek narzędzi.
To model operacyjny dla agentów na poziomie własności.

Pytanie nie brzmi:

- czy mamy automatyzację przeglądarki
- czy mamy klikanie po pulpicie
- czy mamy percepcję ekranu

Prawdziwe pytanie brzmi:

- czy mamy płaszczyznę kontroli nad wykonaniem
- czy mamy prawdę o artefaktach
- czy mamy odzyskiwanie po częściowej awarii
- czy wiemy, który wykonawca powinien działać dalej i dlaczego

Jeżeli odpowiedź brzmi „tak”, mamy Agents OS.

## Związek z 'Ownership'

`vetcoders-ownership` to nie tylko prompt umiejętności.
To warstwa polityki, która decyduje, jak system bierze `odpowiedzialność` za wycinek produktu **end **.

W tym ujęciu:

Codex lub główny agent to mózg wykonawczy
Playwright to deterministyczny wykonawca interfejsu
osascript i cliclic to wykonawcy desktopowi
Anthropic Computer Use to wykonawca oparty na percepcji
laptop to host środowiska wykonawczego

Żadne z tych narzędzi samo w sobie nie jest systemem.
Razem, pod jednym modelem kontroli, mogą nim się stać.

Kluczowe Warstwy

1. Płaszczyzna Kontroli

Płaszczyzna kontroli odpowiada za:

stan zadań
ponawianie prób
zatrzymywanie i wznawianie
przekazywanie zadań
eskalacje
priorytetyzację
wybór wykonawcy

Bez tego narzędzia są tylko manualnymi pomocnikami.

2. Adaptery Wykonawcze

Adaptery wykonawcze realizują pracę na prawdziwych powierzchniach:

adaptery repozytorium i CLI
Playwright do deterministycznej automatyzacji przeglądarki
automatyzacja desktopowa przez osascript i cliclic
Computer Use do niedeterministycznej egzekucji opartej o ekran

Adapter wybierany jest na podstawie kształtu zadania, a nie przyzwyczajenia.

3. Warstwa Percepcji

System musi obserwować stan wieloma kanałami:

zrzuty DOM
zrzuty ekranu
logi
ślady wykonania
OCR lub rozumienie ekranu
lokalne wyjścia środowiska

Percepcja pozwala systemowi płynnie przechodzić z kontroli deterministycznej na rozmytą bez utraty prawdy.

4. Magistrala Artefaktów

Każde poważne uruchomienie powinno generować trwałe artefakty:

raporty
zrzuty ekranu
ślady
transkrypty
statusy meta
wyniki weryfikacji

Jeżeli stan istnieje tylko w przewiniętym terminalu, system nie jest na poziomie własności.

5. Warstwa Polityki

Warstwa polityki decyduje:

kiedy agent działa autonomicznie
kiedy eskaluje
kiedy preferuje automatyzację deterministyczną
kiedy przechodzi na kontrolę desktopową
kiedy używa Computer Use
co uznajemy za zakończone

To tutaj faktycznie żyje vetcoders-ownership.

Hierarchia Wykonania

Domyślna kolejność preferencji:

natywne sterowanie repozytorium i aplikacją
automatyzacja deterministyczna, np. Playwright
automatyzacja desktopowa, np. osascript i cliclic
kontrola percepcyjna, np. Anthropic Computer Use

Najpierw używaj najsilniejszej metody deterministycznej.
Kontrolę percepcyjną stosuj, gdy interfejs jest zbyt dynamiczny, ukryty, natywny lub chaotyczny dla selektorów deterministycznych.

Rola Aktualnego Stosu

Playwright

Playwright to nie jest „ta rzecz do przeglądarki”.
To deterministyczny sterownik UI.

Używaj go, gdy:

powierzchnia jest przeglądarkowa
selektory są wystarczająco stabilne
powtarzalność ma znaczenie
chcemy czystych śladów i zrzutów

osascript + cliclic

To aktuatory na poziomie pulpitu.

Używaj ich, gdy:

aplikacja jest natywna dla desktopu lub oparta o Tauri
przepływ przechodzi przez systemowe okna dialogowe lub zmiany fokusu
narzędzia przeglądarkowe nie mogą dosięgnąć powierzchni

Są użyteczne, ale kruche.
Nie powinny być domyślną płaszczyzną kontroli.

Anthropic Computer Use

To operator oparty na percepcji.

Używaj go, gdy:

powierzchnia nie jest niezawodnie osiągalna przez selektory
UI jest mocno wizualne lub stanowe
potrzebna jest pętla „zobacz i działaj” jak u człowieka

To nie jest pierwszy wybór do powtarzalnej automatyzacji.
To najlepsze narzędzie na ostatnią nieprzewidywalną milę.

Laptop

Laptop to nie tylko maszyna.
To host środowiska wykonawczego:

prawdziwy system operacyjny
prawdziwe okna
prawdziwy fokus
prawdziwe GPU i renderowanie
prawdziwa, widoczna dla użytkownika rzeczywistość

To ma znaczenie, bo własność wymaga prawdy środowiska, nie tylko statycznej poprawności.

Kryteria Własności

Agents OS jest na poziomie własności, gdy potrafi:

wybrać właściwego wykonawcę dla kolejnej akcji
zachować stan zadania przez ponowienia i restart
udowodnić przebieg za pomocą artefaktów
czysto odzyskać po częściowej awarii
eskalować tylko przy realnym rozgałęzieniu
zamknąć pętlę na prawdzie produktu, nie tylko na prawdzie kodu

Jeżeli mamy tylko narzędzia, mamy pomocników.
Jeżeli mamy stan, trasowanie, artefakty i odzyskiwanie, mamy system operacyjny.

Minimalne Drzewo Decyzyjne

Używaj Playwright, gdy powierzchnia jest osiągalna i stabilna.

Używaj automatyzacji desktopowej, gdy powierzchnia jest realna, ale nieadresowalna przez przeglądarkę.

Używaj Computer Use, gdy powierzchnia jest realna, ale nie da się jej niezawodnie zautomatyzować deterministycznie.

Eskaluj do człowieka tylko, gdy:

istnieje ukryta konsekwencja
granica zaufania lub poświadczenia blokuje postęp
stan środowiska jest niejednoznaczny nawet po zebraniu artefaktów

Wniosek Praktyczny

Stos:

Codex jako mózg wykonawczy
Playwright jako deterministyczna egzekucja UI
osascript i cliclic jako zapas na desktop
Anthropic Computer Use jako kontrola percepcyjna
lokalny laptop jako host środowiska wykonawczego

jest wystarczający, by stworzyć prawdziwy Agents OS.

Ale tylko, jeśli zostanie ujęty jako system kontroli, percepcji, polityki, artefaktów i odzyskiwania.

Bez tego pozostaje potężnym stosem narzędzi.


# Agents OS Foundation

## Thesis

Agents OS is not a bag of tools.
It is an ownership-grade operating model for agents.

The question is not:

- do we have browser automation
- do we have desktop clicks
- do we have screen perception

The real question is:

- do we have a control plane over execution
- do we have artifact truth
- do we have recovery after partial failure
- do we know which executor should act next and why

If that answer is yes, we have an Agents OS.

## Relationship To Ownership

`vetcoders-ownership` is not just a skill prompt.
It is the policy layer that decides how the system takes responsibility for a product slice end to end.

In this frame:

- Codex or the main agent is the executive brain
- Playwright is a deterministic UI executor
- `osascript` and `cliclic` are desktop executors
- Anthropic Computer Use is a perception-driven executor
- the laptop is the runtime host

None of those tools is the system.
Together, under one control model, they can become the system.

## Core Layers

### 1. Control Plane

The control plane owns:

- task state
- retries
- stop and resume
- handoffs
- escalation
- prioritization
- executor selection

Without this, tools are just manual helpers.

### 2. Execution Adapters

Execution adapters perform work against real surfaces:

- repo and CLI adapters
- Playwright for deterministic browser UI
- desktop automation via `osascript` and `cliclic`
- Computer Use for non-deterministic screen-driven execution

The adapter is chosen by task shape, not by habit.

### 3. Perception Layer

The system must be able to observe state through multiple channels:

- DOM snapshots
- screenshots
- logs
- traces
- OCR or screen understanding
- local runtime output

Perception is what lets the system route from deterministic control to fuzzy control without losing truth.

### 4. Artifact Bus

Every serious run should emit durable artifacts:

- reports
- screenshots
- traces
- transcripts
- meta status
- verification output

If state lives only in terminal scrollback, the system is not ownership-grade.

### 5. Policy Layer

The policy layer decides:

- when the agent acts autonomously
- when it escalates
- when to prefer deterministic automation
- when to fall back to desktop control
- when to use Computer Use
- what counts as done

This is where `vetcoders-ownership` actually lives.

## Execution Hierarchy

Default order of preference:

1. repo-native and app-native control
2. deterministic automation such as Playwright
3. desktop automation such as `osascript` and `cliclic`
4. perception-driven control such as Anthropic Computer Use

Use the strongest deterministic method first.
Use perception-driven control when the UI is too dynamic, hidden, native, or chaotic for deterministic selectors.

## Roles Of The Current Stack

### Playwright

Playwright is not "the browser thing".
It is the deterministic UI driver.

Use it when:

- the surface is browser-based
- selectors are stable enough
- repeatability matters
- we want clean traces and snapshots

### `osascript` + `cliclic`

These are desktop-level actuators.

Use them when:

- the app is desktop-native or Tauri-bound
- the flow crosses system dialogs or focus edges
- browser-native tools cannot reach the surface

They are useful but brittle.
They should not be the default control plane.

### Anthropic Computer Use

This is the perception-driven operator.

Use it when:

- the surface cannot be reliably addressed through selectors
- the UI is highly visual or stateful
- a human-like "see and act" loop is needed

It is not the first choice for repeatable automation.
It is the best tool for the last unpredictable mile.

### The Laptop

The laptop is not just a machine.
It is the host runtime:

- real OS
- real windows
- real focus
- real GPU and rendering
- real user-visible truth

That matters because ownership requires runtime truth, not only static correctness.

## Ownership-Grade Criteria

An Agents OS is ownership-grade when it can:

- choose the right executor for the next action
- preserve task state across retries and restarts
- prove what happened with artifacts
- recover cleanly from partial failure
- escalate only when the fork is real
- close the loop on product truth, not only code truth

If we only have tools, we have helpers.
If we have state, routing, artifacts, and recovery, we have an operating system.

## Minimal Decision Tree

Use Playwright when the surface is reachable and stable.

Use desktop automation when the surface is real but not browser-addressable.

Use Computer Use when the surface is real but not reliably automatable through deterministic control.

Escalate to the human only when:

- there is a hidden consequence
- a credential or trust boundary blocks progress
- the runtime state is ambiguous even after artifact collection

## Practical Conclusion

The stack of:

- Codex as the executive brain
- Playwright as deterministic UI execution
- `osascript` and `cliclic` as desktop fallback
- Anthropic Computer Use as perception-driven control
- a local laptop as the runtime host

is sufficient to form a real Agents OS.

But only if it is framed as a system of control, perception, policy, artifacts, and recovery.

Without that, it remains a powerful pile of tools.
