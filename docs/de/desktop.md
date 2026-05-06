> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code Desktop verwenden

> Nutzen Sie Claude Code Desktop optimal: parallele Sitzungen mit Git-Isolation, Drag-and-Drop-Pane-Layout, integriertes Terminal und Datei-Editor, Seitenchats, Computernutzung, Dispatch-Sitzungen von Ihrem Telefon, visuelle Diff-Überprüfung, App-Vorschau, PR-Überwachung, Konnektoren und Unternehmenskonfiguration.

Die Claude Desktop-App hat drei Registerkarten: **Chat** für Gespräche, **Cowork** für [Dispatch und längere agentengestützte Arbeiten](https://claude.com/product/cowork) und **Code** für Softwareentwicklung. Diese Seite ist die Referenz für die Registerkarte „Code".

<CardGroup cols={2}>
  <Card title="Download for macOS" icon="apple" href="https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs">
    Universal build for Intel and Apple Silicon
  </Card>

  <Card title="Download for Windows" icon="windows" href="https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code&utm_medium=docs">
    For x64 processors
  </Card>
</CardGroup>

For Windows ARM64, download the [ARM64 installer](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs). The desktop app is not available on Linux; use the [CLI](/en/quickstart) instead.

Nach der Installation starten Sie Claude, melden sich an und klicken auf die Registerkarte **Code**. Beim ersten Öffnen unter Windows benötigen Sie [Git für Windows](https://git-scm.com/downloads/win) installiert; starten Sie die App nach der Installation neu. Eine Anleitung für Ihre erste Sitzung finden Sie im [Leitfaden „Erste Schritte"](/de/desktop-quickstart).

In der Registerkarte „Code" ist jedes Gespräch eine **Sitzung**: Es hat seinen eigenen Chat-Verlauf, Projektordner und Code-Änderungen, unabhängig von jeder anderen Sitzung. Die Seitenleiste listet Ihre Sitzungen auf und ermöglicht es Ihnen, mehrere parallel auszuführen. Innerhalb einer Sitzung können Sie:

* [Diffs überprüfen und kommentieren](#review-changes-with-diff-view), dann [den resultierenden PR durch CI überwachen](#monitor-pull-request-status)
* [Ihre laufende App](#preview-your-app) in einem eingebetteten Browser in der Vorschau anzeigen, während Claude seine eigenen Änderungen überprüft
* [Panes anordnen](#arrange-your-workspace) für Chat, Diff, Vorschau, Terminal und Datei-Editor nebeneinander
* Eine [Seitenfrage](#ask-a-side-question-without-derailing-the-session) stellen, die den Kontext der Sitzung nutzt, ohne sie zu beeinträchtigen
* [Externe Tools verbinden](#connect-external-tools) wie GitHub, Slack und Linear
* Claude [Apps öffnen und Ihren Bildschirm steuern lassen](#let-claude-use-your-computer)
* Auf Ihrem Computer, in der [Cloud](#run-long-running-tasks-remotely) oder über [SSH](#ssh-sessions) ausführen

Für [geplante wiederkehrende Arbeiten](/de/desktop-scheduled-tasks), [Tastaturkürzel](#keyboard-shortcuts) oder [Aufgaben von Ihrem Telefon senden](#sessions-from-dispatch) siehe die verlinkten Seiten und Abschnitte. Wenn Sie bereits die Terminal-basierte CLI verwenden, siehe den [CLI-Vergleich](#coming-from-the-cli) für das, was übertragen wird.

## Sitzung starten

Bevor Sie Ihre erste Nachricht senden, konfigurieren Sie vier Dinge im Eingabebereich:

* **Umgebung**: Wählen Sie, wo Claude ausgeführt wird. Wählen Sie **Lokal** für Ihren Computer, **Remote** für von Anthropic gehostete Cloud-Sitzungen oder eine [**SSH-Verbindung**](#ssh-sessions) für einen von Ihnen verwalteten Remote-Computer. Siehe [Umgebungskonfiguration](#environment-configuration).
* **Projektordner**: Wählen Sie den Ordner oder das Repository aus, in dem Claude arbeitet. Für Remote-Sitzungen können Sie [mehrere Repositories](#run-long-running-tasks-remotely) hinzufügen.
* **Modell**: Wählen Sie ein [Modell](/de/model-config#available-models) aus dem Dropdown neben der Schaltfläche „Senden". Sie können dies während der Sitzung ändern.
* **Berechtigungsmodus**: Wählen Sie, wie viel Autonomie Claude aus dem [Moduswahlschalter](#choose-a-permission-mode) hat. Sie können dies während der Sitzung ändern.

Geben Sie Ihre Aufgabe ein und drücken Sie **Eingabe**, um zu starten. Jede Sitzung verfolgt ihren eigenen Kontext und Änderungen unabhängig.

## Arbeiten mit Code

Geben Sie Claude den richtigen Kontext, kontrollieren Sie, wie viel es eigenständig tut, und überprüfen Sie, was es geändert hat.

### Verwenden Sie das Eingabefeld

Geben Sie ein, was Claude tun soll, und drücken Sie **Eingabe**, um zu senden. Claude liest Ihre Projektdateien, nimmt Änderungen vor und führt Befehle basierend auf Ihrem [Berechtigungsmodus](#choose-a-permission-mode) aus. Sie können Claude jederzeit unterbrechen: Klicken Sie auf die Stoppschaltfläche oder geben Sie Ihre Korrektur ein und drücken Sie **Eingabe**. Claude stoppt, was es tut, und passt sich basierend auf Ihrer Eingabe an.

Die Schaltfläche **+** neben dem Eingabefeld gibt Ihnen Zugriff auf Dateianhänge, [Skills](#use-skills), [Konnektoren](#connect-external-tools) und [Plugins](#install-plugins).

### Fügen Sie Dateien und Kontext zu Eingaben hinzu

Das Eingabefeld unterstützt zwei Möglichkeiten, um externen Kontext einzubinden:

* **@mention-Dateien**: Geben Sie `@` gefolgt von einem Dateinamen ein, um eine Datei zum Gesprächskontext hinzuzufügen. Claude kann diese Datei dann lesen und referenzieren. @mention ist nicht in Remote-Sitzungen verfügbar.
* **Dateien anhängen**: Hängen Sie Bilder, PDFs und andere Dateien an Ihre Eingabe an, indem Sie die Schaltfläche „Anhängen" verwenden, oder ziehen Sie Dateien direkt in die Eingabe. Dies ist nützlich zum Teilen von Screenshots von Fehlern, Design-Mockups oder Referenzdokumenten.

### Wählen Sie einen Berechtigungsmodus

Berechtigungsmodi kontrollieren, wie viel Autonomie Claude während einer Sitzung hat: ob es vor dem Bearbeiten von Dateien, dem Ausführen von Befehlen oder beidem fragt. Sie können Modi jederzeit mit dem Moduswahlschalter neben der Schaltfläche „Senden" wechseln. Beginnen Sie mit „Berechtigungen erfragen", um genau zu sehen, was Claude tut, und wechseln Sie dann zu „Bearbeitungen automatisch akzeptieren" oder „Plan Mode", wenn Sie sich wohler fühlen.

| Modus                                     | Einstellungsschlüssel | Verhalten                                                                                                                                                                                                                                                                                                                                |
| ----------------------------------------- | --------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Berechtigungen erfragen**               | `default`             | Claude fragt vor dem Bearbeiten von Dateien oder dem Ausführen von Befehlen. Sie sehen einen Diff und können jede Änderung akzeptieren oder ablehnen. Empfohlen für neue Benutzer.                                                                                                                                                       |
| **Bearbeitungen automatisch akzeptieren** | `acceptEdits`         | Claude akzeptiert Dateibearbeitungen automatisch und häufige Dateisystem-Befehle wie `mkdir`, `touch` und `mv`, fragt aber immer noch vor dem Ausführen anderer Terminal-Befehle. Verwenden Sie dies, wenn Sie Dateiänderungen vertrauen und schnellere Iterationen wünschen.                                                            |
| **Plan Mode**                             | `plan`                | Claude liest Dateien und führt Befehle aus, um zu erkunden, schlägt dann einen Plan vor, ohne Ihren Quellcode zu bearbeiten. Gut für komplexe Aufgaben, bei denen Sie den Ansatz zuerst überprüfen möchten.                                                                                                                              |
| **Auto**                                  | `auto`                | Claude führt alle Aktionen mit Hintergrund-Sicherheitsprüfungen aus, die die Ausrichtung mit Ihrer Anfrage überprüfen. Reduziert Berechtigungsaufforderungen bei Beibehaltung der Überwachung. Aktivieren Sie in Ihren Einstellungen → Claude Code. Siehe [Verfügbarkeitsanforderungen](#auto-mode-availability) unten.                  |
| **Berechtigungen umgehen**                | `bypassPermissions`   | Claude läuft ohne Berechtigungsaufforderungen, äquivalent zu `--dangerously-skip-permissions` in der CLI. Aktivieren Sie dies in Ihren Einstellungen → Claude Code unter „Bypass-Berechtigungsmodus zulassen". Verwenden Sie dies nur in sandboxierten Containern oder VMs. Enterprise-Administratoren können diese Option deaktivieren. |

Der Berechtigungsmodus `dontAsk` ist nur in der [CLI](/de/permission-modes#allow-only-pre-approved-tools-with-dontask-mode) verfügbar.

<span id="auto-mode-availability" />

Auto Mode ist eine Forschungsvorschau, die auf Max-, Team-, Enterprise- und API-Plänen verfügbar ist. Es ist nicht auf Pro-Plänen oder bei Drittanbieter-Providern verfügbar. Auf Team-, Enterprise- und API-Plänen ist Claude Sonnet 4.6, Opus 4.6 oder Opus 4.7 erforderlich. Auf Max-Plänen ist Claude Opus 4.7 erforderlich.

<Tip title="Best Practice">
  Beginnen Sie komplexe Aufgaben im Plan Mode, damit Claude einen Ansatz abbildet, bevor Änderungen vorgenommen werden. Sobald Sie den Plan genehmigen, wechseln Sie zu 'Bearbeitungen automatisch akzeptieren" oder „Berechtigungen erfragen", um ihn auszuführen. Siehe [Zuerst erkunden, dann planen, dann codieren](/de/best-practices#explore-first-then-plan-then-code) für mehr zu diesem Workflow.
</Tip>

Remote-Sitzungen unterstützen „Bearbeitungen automatisch akzeptieren" und „Plan Mode". „Berechtigungen erfragen" ist nicht verfügbar, da Remote-Sitzungen Dateibearbeitungen standardmäßig automatisch akzeptieren, und „Berechtigungen umgehen" ist nicht verfügbar, da die Remote-Umgebung bereits sandboxed ist.

Enterprise-Administratoren können einschränken, welche Berechtigungsmodi verfügbar sind. Siehe [Unternehmenskonfiguration](#enterprise-configuration) für Details.

### Vorschau Ihrer App

Claude kann einen Dev-Server starten und einen eingebetteten Browser öffnen, um seine Änderungen zu überprüfen. Dies funktioniert sowohl für Frontend-Web-Apps als auch für Backend-Server: Claude kann API-Endpunkte testen, Server-Protokolle anzeigen und Probleme, die er findet, iterieren. In den meisten Fällen startet Claude den Server automatisch nach dem Bearbeiten von Projektdateien. Sie können Claude auch jederzeit bitten, eine Vorschau anzuzeigen. Standardmäßig [überprüft Claude automatisch](#auto-verify-changes) Änderungen nach jeder Bearbeitung.

Das Vorschau-Pane kann auch statische HTML-Dateien, PDFs, Bilder und Videos aus Ihrem Projekt öffnen. Klicken Sie auf einen HTML-, PDF-, Bild- oder Videopfad im Chat, um ihn in der Vorschau zu öffnen.

Aus dem Vorschau-Pane können Sie:

* Direkt im eingebetteten Browser mit Ihrer laufenden App interagieren
* Beobachten, wie Claude seine eigenen Änderungen automatisch überprüft: Es macht Screenshots, inspiziert das DOM, klickt auf Elemente, füllt Formulare aus und behebt Probleme, die es findet
* Server aus dem Dropdown **Vorschau** in der Sitzungs-Symbolleiste starten oder stoppen
* Cookies und lokalen Speicher über Server-Neustarts hinweg beibehalten, indem Sie **Sitzungen beibehalten** im Dropdown auswählen, damit Sie sich während der Entwicklung nicht erneut anmelden müssen
* Die Server-Konfiguration bearbeiten oder alle Server auf einmal stoppen

Claude erstellt die anfängliche Server-Konfiguration basierend auf Ihrem Projekt. Wenn Ihre App einen benutzerdefinierten Dev-Befehl verwendet, bearbeiten Sie `.claude/launch.json`, um Ihr Setup zu entsprechen. Siehe [Vorschau-Server konfigurieren](#configure-preview-servers) für die vollständige Referenz.

Um gespeicherte Sitzungsdaten zu löschen, schalten Sie **Vorschau-Sitzungen beibehalten** in Einstellungen → Claude Code aus. Um die Vorschau vollständig zu deaktivieren, schalten Sie **Vorschau** in Einstellungen → Claude Code aus.

### Überprüfen Sie Änderungen mit der Diff-Ansicht

Nachdem Claude Änderungen an Ihrem Code vorgenommen hat, können Sie mit der Diff-Ansicht Änderungen dateiweise überprüfen, bevor Sie einen Pull Request erstellen.

Wenn Claude Dateien ändert, wird ein Diff-Statistik-Indikator angezeigt, der die Anzahl der hinzugefügten und entfernten Zeilen anzeigt, z. B. `+12 -1`. Klicken Sie auf diesen Indikator, um den Diff-Viewer zu öffnen, der eine Dateiliste auf der linken Seite und die Änderungen für jede Datei auf der rechten Seite anzeigt.

Um Kommentare zu bestimmten Zeilen hinzuzufügen, klicken Sie auf eine beliebige Zeile im Diff, um ein Kommentarfeld zu öffnen. Geben Sie Ihr Feedback ein und drücken Sie **Eingabe**, um den Kommentar hinzuzufügen. Nach dem Hinzufügen von Kommentaren zu mehreren Zeilen senden Sie alle Kommentare auf einmal:

* **macOS**: drücken Sie **Cmd+Eingabe**
* **Windows**: drücken Sie **Strg+Eingabe**

Claude liest Ihre Kommentare und nimmt die angeforderten Änderungen vor, die als neuer Diff angezeigt werden, den Sie überprüfen können.

### Überprüfen Sie Ihren Code

Klicken Sie in der Diff-Ansicht auf **Code überprüfen** in der oberen rechten Symbolleiste, um Claude zu bitten, die Änderungen vor dem Commit zu bewerten. Claude untersucht die aktuellen Diffs und hinterlässt Kommentare direkt in der Diff-Ansicht. Sie können auf jeden Kommentar antworten oder Claude bitten, zu überarbeiten.

Die Überprüfung konzentriert sich auf hochwertige Probleme: Kompilierungsfehler, definitive Logikfehler, Sicherheitslücken und offensichtliche Fehler. Sie kennzeichnet keine Stil-, Formatierungs-, bereits vorhandenen Probleme oder etwas, das ein Linter erfassen würde.

### Überwachen Sie den Pull-Request-Status

Nachdem Sie einen Pull Request öffnen, wird eine CI-Statusleiste in der Sitzung angezeigt. Claude Code verwendet die GitHub CLI, um Prüfergebnisse abzurufen und Fehler anzuzeigen.

* **Automatische Fehlerbehebung**: Wenn aktiviert, versucht Claude automatisch, fehlgeschlagene CI-Prüfungen zu beheben, indem die Fehlerausgabe gelesen und iteriert wird.
* **Automatisches Merge**: Wenn aktiviert, führt Claude den PR zusammen, sobald alle Prüfungen bestanden sind. Die Merge-Methode ist Squash. Das automatische Merge muss [in Ihren GitHub-Repository-Einstellungen aktiviert sein](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository), damit dies funktioniert.

Verwenden Sie die Umschalter **Automatische Fehlerbehebung** und **Automatisches Merge** in der CI-Statusleiste, um eine der beiden Optionen zu aktivieren. Claude Code sendet auch eine Desktop-Benachrichtigung, wenn CI abgeschlossen ist. Um die Sitzung automatisch zu archivieren, sobald der PR zusammengeführt oder geschlossen wird, schalten Sie [Auto-Archivieren](#work-in-parallel-with-sessions) in Einstellungen → Claude Code ein.

<Note>
  Die PR-Überwachung erfordert, dass die [GitHub CLI (`gh`)](https://cli.github.com/) auf Ihrem Computer installiert und authentifiziert ist. Wenn `gh` nicht installiert ist, fordert Desktop Sie auf, es beim ersten Versuch, einen PR zu erstellen, zu installieren.
</Note>

## Anordnen Ihres Arbeitsbereichs

Die Code-Registerkarte ist um Panes aufgebaut, die Sie in jedem Layout anordnen können: Chat, Diff, Vorschau, Terminal, Datei, Plan, Aufgaben und Subagent. Ziehen Sie ein Pane an seiner Kopfzeile, um es zu verschieben, oder ziehen Sie eine Pane-Kante, um es zu vergrößern. Drücken Sie **Cmd+\\** auf macOS oder **Ctrl+\\** auf Windows, um das fokussierte Pane zu schließen. Öffnen Sie zusätzliche Panes aus dem Menü **Ansichten** in der Sitzungs-Symbolleiste.

<Note>
  Das Pane-Layout, Terminal, Datei-Editor und Ansichtsmodi in diesem Abschnitt erfordern Claude Desktop v1.2581.0 oder später. Öffnen Sie **Claude → Nach Updates suchen** auf macOS oder **Hilfe → Nach Updates suchen** auf Windows, um zu aktualisieren.
</Note>

### Führen Sie Befehle im Terminal aus

Das integrierte Terminal ermöglicht es Ihnen, Befehle neben Ihrer Sitzung auszuführen, ohne zu einer anderen App zu wechseln. Öffnen Sie es aus dem Menü **Ansichten** oder drücken Sie **Ctrl+\`** auf macOS oder Windows. Das Terminal öffnet sich im Arbeitsverzeichnis Ihrer Sitzung und teilt die gleiche Umgebung wie Claude, sodass Befehle wie `npm test` oder `git status` die gleichen Dateien sehen, die Claude bearbeitet. Das Terminal ist nur in lokalen Sitzungen verfügbar.

### Öffnen und bearbeiten Sie Dateien

Klicken Sie auf einen Dateipfad im Chat oder Diff-Viewer, um ihn im Datei-Pane zu öffnen. HTML-, PDF-, Bild- und Videopfade öffnen sich stattdessen im [Vorschau-Pane](#preview-your-app). Nehmen Sie Spot-Bearbeitungen vor und klicken Sie auf **Speichern**, um sie zurückzuschreiben. Wenn sich die Datei auf der Festplatte geändert hat, seit Sie sie geöffnet haben, warnt Sie das Pane und lässt Sie überschreiben oder verwerfen. Klicken Sie auf **Verwerfen**, um Ihre Bearbeitungen rückgängig zu machen, oder klicken Sie auf den Pfad in der Pane-Kopfzeile, um den absoluten Pfad zu kopieren.

Das Datei-Pane ist in lokalen und SSH-Sitzungen verfügbar. Für Remote-Sitzungen bitten Sie Claude, die Änderung vorzunehmen.

### Öffnen Sie Dateien in anderen Apps

Klicken Sie mit der rechten Maustaste auf einen Dateipfad im Chat, Diff-Viewer oder Datei-Pane, um ein Kontextmenü zu öffnen:

* **Als Kontext anhängen**: Fügen Sie die Datei zu Ihrer nächsten Eingabe hinzu
* **Öffnen in**: Öffnen Sie die Datei in einem installierten Editor wie VS Code, Cursor oder Zed
* **Im Finder anzeigen** auf macOS, **Im Explorer anzeigen** auf Windows: Öffnen Sie den enthaltenden Ordner
* **Pfad kopieren**: Kopieren Sie den absoluten Pfad in Ihre Zwischenablage

### Wechseln Sie Ansichtsmodi

Ansichtsmodi kontrollieren, wie viel Detail im Chat-Transkript angezeigt wird. Wechseln Sie Modi aus dem Dropdown **Transkript-Ansicht** neben der Schaltfläche „Senden", oder drücken Sie **Ctrl+O** auf macOS oder Windows, um durch sie zu zyklisieren.

| Modus               | Was es anzeigt                                                                               |
| ------------------- | -------------------------------------------------------------------------------------------- |
| **Normal**          | Tool-Aufrufe in Zusammenfassungen zusammengefasst, mit vollständigen Text-Antworten          |
| **Ausführlich**     | Jeden Tool-Aufruf, jede Datei-Leseoperation und jeden Zwischenschritt, den Claude unternimmt |
| **Zusammenfassung** | Nur Claudes endgültige Antworten und die Änderungen, die er vorgenommen hat                  |

Verwenden Sie „Ausführlich", wenn Sie debuggen, warum Claude eine bestimmte Aktion unternommen hat. Verwenden Sie „Zusammenfassung", wenn Sie mehrere Sitzungen ausführen und Ergebnisse schnell scannen möchten.

### Tastaturkürzel

Drücken Sie **Cmd+/** auf macOS oder **Ctrl+/** auf Windows, um alle im Code-Tab verfügbaren Kürzel zu sehen. Unter Windows verwenden Sie **Ctrl** anstelle von **Cmd** für die folgenden Kürzel. Sitzungs-Zyklisierung, Terminal-Umschalter und Ansichtsmodus-Umschalter verwenden **Ctrl** auf jeder Plattform.

| Kürzel                                | Aktion                                  |
| ------------------------------------- | --------------------------------------- |
| `Cmd` `/`                             | Tastaturkürzel anzeigen                 |
| `Cmd` `N`                             | Neue Sitzung                            |
| `Cmd` `W`                             | Sitzung schließen                       |
| `Ctrl` `Tab` / `Ctrl` `Shift` `Tab`   | Nächste oder vorherige Sitzung          |
| `Cmd` `Shift` `]` / `Cmd` `Shift` `[` | Nächste oder vorherige Sitzung          |
| `Esc`                                 | Claudes Antwort stoppen                 |
| `Cmd` `Shift` `D`                     | Diff-Pane umschalten                    |
| `Cmd` `Shift` `P`                     | Vorschau-Pane umschalten                |
| `Cmd` `Shift` `S`                     | Element in Vorschau auswählen           |
| `Ctrl` `` ` ``                        | Terminal-Pane umschalten                |
| `Cmd` `\`                             | Fokussiertes Pane schließen             |
| `Cmd` `;`                             | Seitenchat öffnen                       |
| `Ctrl` `O`                            | Ansichtsmodi zyklisieren                |
| `Cmd` `Shift` `M`                     | Berechtigungsmodus-Menü öffnen          |
| `Cmd` `Shift` `I`                     | Modell-Menü öffnen                      |
| `Cmd` `Shift` `E`                     | Aufwand-Menü öffnen                     |
| `1`–`9`                               | Element in einem offenen Menü auswählen |

Diese Kürzel gelten nur für den Code-Tab. Die Terminal-basierten [Kürzel des interaktiven Modus](/de/interactive-mode#keyboard-shortcuts), wie `Shift+Tab` zum Zyklisieren von Modi, gelten nicht in Desktop.

### Überprüfen Sie die Nutzung

Klicken Sie auf den Nutzungsring neben dem Modell-Wahlschalter, um Ihre aktuelle Kontextfenster-Nutzung und Ihre Plan-Nutzung für den Zeitraum zu sehen. Die Kontext-Nutzung ist pro Sitzung; die Plan-Nutzung wird über alle Ihre Claude-Code-Oberflächen hinweg geteilt.

## Lassen Sie Claude Ihren Computer verwenden

Computernutzung ermöglicht es Claude, Ihre Apps zu öffnen, Ihren Bildschirm zu steuern und direkt auf Ihrem Computer zu arbeiten, wie Sie es tun würden. Bitten Sie Claude, eine native App im mobilen Simulator zu testen, mit einem Desktop-Tool zu interagieren, das keine CLI hat, oder etwas zu automatisieren, das nur über eine GUI funktioniert.

<Note>
  Computernutzung ist eine Forschungsvorschau auf macOS und Windows, die einen Pro- oder Max-Plan erfordert. Sie ist nicht für Team- oder Enterprise-Pläne verfügbar. Die Claude Desktop-App muss ausgeführt werden.
</Note>

Computernutzung ist standardmäßig deaktiviert. [Aktivieren Sie sie in Einstellungen](#enable-computer-use), bevor Claude Ihren Bildschirm steuern kann. Auf macOS müssen Sie auch Barrierefreiheits- und Bildschirmaufzeichnungsberechtigungen gewähren.

<Warning>
  Im Gegensatz zum [sandboxierten Bash-Tool](/de/sandboxing) läuft Computernutzung auf Ihrem tatsächlichen Desktop mit Zugriff auf das, was Sie genehmigen. Claude überprüft jede Aktion und kennzeichnet potenzielle Prompt-Injection von Bildschirminhalten, aber die Vertrauensgrenze ist unterschiedlich. Siehe den [Sicherheitsleitfaden für Computernutzung](https://support.claude.com/en/articles/14128542) für Best Practices.
</Warning>

### Wann Computernutzung anwendbar ist

Claude hat mehrere Möglichkeiten, mit einer App oder einem Dienst zu interagieren, und Computernutzung ist die breiteste und langsamste. Es versucht zuerst das präziseste Tool:

* Wenn Sie einen [Konnektor](#connect-external-tools) für einen Dienst haben, verwendet Claude den Konnektor.
* Wenn die Aufgabe ein Shell-Befehl ist, verwendet Claude Bash.
* Wenn die Aufgabe Browser-Arbeit ist und Sie [Claude in Chrome](/de/chrome) eingerichtet haben, verwendet Claude das.
* Wenn keine dieser Optionen zutrifft, verwendet Claude Computernutzung.

Die [Pro-App-Zugriffsstufen](#app-permissions) verstärken dies: Browser sind auf Nur-Ansicht begrenzt, und Terminals und IDEs auf Nur-Klick, was Claude zum dedizierten Tool lenkt, auch wenn Computernutzung aktiv ist. Bildschirmsteuerung ist für Dinge reserviert, die nichts anderes erreichen kann, wie native Apps, Hardware-Steuerfelder, mobile Simulatoren oder proprietäre Tools ohne API.

### Aktivieren Sie Computernutzung

Computernutzung ist standardmäßig deaktiviert. Wenn Sie Claude bitten, etwas zu tun, das es benötigt, während es deaktiviert ist, teilt Claude Ihnen mit, dass es die Aufgabe tun könnte, wenn Sie Computernutzung in Einstellungen aktivieren.

<Steps>
  <Step title="Aktualisieren Sie die Desktop-App">
    Stellen Sie sicher, dass Sie die neueste Version von Claude Desktop haben. Laden Sie herunter oder aktualisieren Sie unter [claude.com/download](https://claude.com/download), und starten Sie die App neu.
  </Step>

  <Step title="Schalten Sie den Umschalter ein">
    Gehen Sie in der Desktop-App zu **Einstellungen > Allgemein** (unter **Desktop-App**). Suchen Sie den Umschalter **Computernutzung** und schalten Sie ihn ein. Unter Windows wird der Umschalter sofort wirksam und das Setup ist abgeschlossen. Auf macOS fahren Sie mit dem nächsten Schritt fort.

    Wenn Sie den Umschalter nicht sehen, bestätigen Sie, dass Sie macOS oder Windows mit einem Pro- oder Max-Plan verwenden, und aktualisieren und starten Sie die App neu.
  </Step>

  <Step title="Gewähren Sie macOS-Berechtigungen">
    Auf macOS müssen Sie zwei Systemberechtigungen gewähren, bevor der Umschalter wirksam wird:

    * **Barrierefreiheit**: ermöglicht Claude, zu klicken, zu tippen und zu scrollen
    * **Bildschirmaufzeichnung**: ermöglicht Claude, zu sehen, was auf Ihrem Bildschirm ist

    Die Einstellungsseite zeigt den aktuellen Status jeder Berechtigung. Wenn eine verweigert wird, klicken Sie auf das Badge, um den relevanten Systemeinstellungsbereich zu öffnen.
  </Step>
</Steps>

### App-Berechtigungen

Wenn Claude eine App zum ersten Mal verwenden muss, wird eine Eingabeaufforderung in Ihrer Sitzung angezeigt. Klicken Sie auf **Für diese Sitzung zulassen** oder **Ablehnen**. Genehmigungen gelten für die aktuelle Sitzung oder 30 Minuten in [Dispatch-generierten Sitzungen](#sessions-from-dispatch).

Die Eingabeaufforderung zeigt auch, welche Kontrollebene Claude für diese App erhält. Diese Stufen sind nach App-Kategorie festgelegt und können nicht geändert werden:

| Stufe                  | Was Claude tun kann                                                        | Gilt für                    |
| :--------------------- | :------------------------------------------------------------------------- | :-------------------------- |
| Nur Ansicht            | Die App in Screenshots sehen                                               | Browser, Handelsplattformen |
| Nur Klick              | Klicken und scrollen, aber nicht tippen oder Tastenkombinationen verwenden | Terminals, IDEs             |
| Vollständige Kontrolle | Klicken, tippen, ziehen und Tastenkombinationen verwenden                  | Alles andere                |

Apps mit großer Reichweite wie Terminals, Finder oder Datei-Explorer und Systemeinstellungen oder Einstellungen zeigen eine zusätzliche Warnung in der Eingabeaufforderung, damit Sie wissen, was das Genehmigen gewährt.

Sie können zwei Einstellungen in **Einstellungen > Allgemein** (unter **Desktop-App**) konfigurieren:

* **Abgelehnte Apps**: Fügen Sie Apps hier hinzu, um sie ohne Aufforderung abzulehnen. Claude kann eine abgelehnte App indirekt durch Aktionen in einer zulässigen App beeinflussen, kann aber nicht direkt mit der abgelehnen App interagieren.
* **Apps anzeigen, wenn Claude fertig ist**: Während Claude arbeitet, werden Ihre anderen Fenster ausgeblendet, damit es nur mit der genehmigten App interagiert. Wenn Claude fertig ist, werden ausgeblendete Fenster wiederhergestellt, es sei denn, Sie deaktivieren diese Einstellung.

## Verwalten Sie Sitzungen

Jede Sitzung ist ein unabhängiges Gespräch mit eigenem Kontext und Änderungen. Sie können mehrere Sitzungen parallel ausführen, Arbeit in die Cloud senden oder Dispatch Sitzungen von Ihrem Telefon aus starten lassen.

### Arbeiten Sie parallel mit Sitzungen

Klicken Sie auf **+ Neue Sitzung** in der Seitenleiste, oder drücken Sie **Cmd+N** auf macOS oder **Ctrl+N** auf Windows, um an mehreren Aufgaben parallel zu arbeiten. Drücken Sie **Ctrl+Tab** und **Ctrl+Shift+Tab**, um durch Sitzungen in der Seitenleiste zu zyklisieren. Für Git-Repositories erhält jede Sitzung ihre eigene isolierte Kopie Ihres Projekts mit [Git Worktrees](/de/worktrees), sodass Änderungen in einer Sitzung andere Sitzungen nicht beeinflussen, bis Sie sie committen.

Um zwei Sitzungen gleichzeitig anzuzeigen, halten Sie **Cmd** auf macOS oder **Ctrl** auf Windows gedrückt und klicken Sie auf eine Sitzung in der Seitenleiste. Die Sitzung wird in einem zweiten Bereich neben dem bereits geöffneten angezeigt. Während die Aufteilung aktiv ist, ersetzt das Klicken auf eine andere Sitzung in der Seitenleiste denjenigen Bereich, der den Fokus hat. Drücken Sie **Cmd+\\** auf macOS oder **Ctrl+\\** auf Windows, um den fokussierten Bereich zu schließen und zu einer einzelnen Sitzung zurückzukehren.

Worktrees werden standardmäßig in `<project-root>/.claude/worktrees/` gespeichert. Sie können dies in Einstellungen → Claude Code unter 'Worktree-Speicherort" in ein benutzerdefiniertes Verzeichnis ändern. Sie können auch ein Branch-Präfix festlegen, das jedem Worktree-Branch-Namen vorangestellt wird, was nützlich ist, um von Claude erstellte Branches organisiert zu halten. Um einen Worktree zu entfernen, wenn Sie fertig sind, fahren Sie mit der Maus über die Sitzung in der Seitenleiste und klicken Sie auf das Archiv-Symbol. Um Sitzungen automatisch zu archivieren, wenn ihr Pull Request zusammengeführt oder geschlossen wird, schalten Sie **Auto-Archivieren nach PR-Merge oder -Schließung** in Einstellungen → Claude Code ein. Auto-Archivieren gilt nur für lokale Sitzungen, die beendet wurden.

Um gitignorierte Dateien wie `.env` in neue Worktrees einzubeziehen, erstellen Sie eine [`.worktreeinclude`-Datei](/de/worktrees#copy-gitignored-files-into-worktrees) in Ihrem Projektstammverzeichnis.

<Note>
  Die Sitzungsisolation erfordert [Git](https://git-scm.com/downloads). Die meisten Macs enthalten Git standardmäßig. Führen Sie `git --version` im Terminal aus, um zu überprüfen. Unter Windows ist Git erforderlich, damit die Registerkarte „Code" funktioniert: [Laden Sie Git für Windows herunter](https://git-scm.com/downloads/win), installieren Sie es und starten Sie die App neu. Wenn Sie auf Git-Fehler stoßen, bitten Sie Claude im [Cowork-Tab](https://claude.com/product/cowork), Ihnen bei der Behebung Ihres Setups zu helfen.
</Note>

Verwenden Sie die Steuerelemente oben in der Seitenleiste, um Sitzungen nach Status, Projekt oder Umgebung zu filtern, und um Sitzungen nach Projekt zu gruppieren. Um eine Sitzung umzubenennen, klicken Sie auf den Sitzungstitel in der Symbolleiste oben in der aktiven Sitzung. Um die Kontext-Nutzung zu überprüfen, siehe [Überprüfen Sie die Nutzung](#check-usage). Wenn der Kontext voll wird, fasst Claude das Gespräch automatisch zusammen und arbeitet weiter. Sie können auch `/compact` eingeben, um die Zusammenfassung früher auszulösen und Kontextraum freizugeben. Siehe [das Kontextfenster](/de/how-claude-code-works#the-context-window) für Details, wie die Komprimierung funktioniert.

### Fragen Sie eine Seitenfrage, ohne die Sitzung zu entgleisen

Ein Seitenchat ermöglicht es Ihnen, Claude eine Frage zu stellen, die den Kontext Ihrer Sitzung nutzt, aber nichts zum Hauptgespräch hinzufügt. Verwenden Sie ihn, wenn Sie ein Stück Code verstehen, eine Annahme überprüfen oder eine Idee erkunden möchten, ohne die Sitzung vom Kurs abzubringen.

Drücken Sie **Cmd+;** auf macOS oder **Ctrl+;** auf Windows, um einen Seitenchat zu öffnen, oder geben Sie `/btw` im Eingabefeld ein. Der Seitenchat kann alles im Hauptthread bis zu diesem Punkt lesen. Wenn Sie fertig sind, schließen Sie den Seitenchat und setzen Sie die Hauptsitzung dort fort, wo Sie aufgehört haben. Seitenchats sind in lokalen und SSH-Sitzungen verfügbar.

### Beobachten Sie Hintergrund-Aufgaben

Das Aufgaben-Pane zeigt die Hintergrundarbeit, die in der aktuellen Sitzung läuft: Subagents, Hintergrund-Shell-Befehle und Workflows. Öffnen Sie es aus dem Menü **Ansichten** oder ziehen Sie es in Ihr Layout.

Klicken Sie auf einen beliebigen Eintrag, um seine Ausgabe im Subagent-Pane zu sehen oder ihn zu stoppen. Um zu sehen, was andere Sitzungen tun, verwenden Sie die [Seitenleiste](#work-in-parallel-with-sessions).

### Führen Sie lange laufende Aufgaben remote aus

Für große Refaktorierungen, Test-Suites, Migrationen oder andere lange laufende Aufgaben wählen Sie **Remote** statt **Lokal**, wenn Sie eine Sitzung starten. Remote-Sitzungen laufen auf Anthropics Cloud-Infrastruktur und werden fortgesetzt, auch wenn Sie die App schließen oder Ihren Computer herunterfahren. Überprüfen Sie jederzeit den Fortschritt oder lenken Sie Claude in eine andere Richtung. Sie können Remote-Sitzungen auch von [claude.ai/code](https://claude.ai/code) oder der Claude iOS-App aus überwachen.

Remote-Sitzungen unterstützen auch mehrere Repositories. Nach Auswahl einer Cloud-Umgebung klicken Sie auf die Schaltfläche **+** neben dem Repo-Pill, um zusätzliche Repositories zur Sitzung hinzuzufügen. Jedes Repo erhält seinen eigenen Branch-Wahlschalter. Dies ist nützlich für Aufgaben, die mehrere Codebases umfassen, z. B. das Aktualisieren einer gemeinsamen Bibliothek und ihrer Consumer.

Siehe [Claude Code im Web](/de/claude-code-on-the-web) für mehr darüber, wie Remote-Sitzungen funktionieren.

### Fortsetzen auf einer anderen Oberfläche

Das Menü **Fortsetzen in**, das über das VS Code-Symbol unten rechts in der Sitzungs-Symbolleiste zugänglich ist, ermöglicht es Ihnen, Ihre Sitzung auf eine andere Oberfläche zu verschieben:

* **Claude Code im Web**: sendet Ihre lokale Sitzung, um remote weiter zu laufen. Desktop pusht Ihren Branch, generiert eine Zusammenfassung des Gesprächs und erstellt eine neue Remote-Sitzung mit dem vollständigen Kontext. Sie können dann wählen, die lokale Sitzung zu archivieren oder zu behalten. Dies erfordert einen sauberen Arbeitsbaum und ist nicht für SSH-Sitzungen verfügbar.
* **Ihre IDE**: öffnet Ihr Projekt in einer unterstützten IDE im aktuellen Arbeitsverzeichnis.

### Sitzungen von Dispatch

[Dispatch](https://support.claude.com/en/articles/13947068) ist ein persistentes Gespräch mit Claude, das in der Registerkarte [Cowork](https://claude.com/product/cowork#dispatch-and-computer-use) lebt. Sie senden Dispatch eine Aufgabe, und es entscheidet, wie damit umzugehen ist.

Eine Aufgabe kann auf zwei Wegen als Code-Sitzung enden: Sie fragen direkt danach, z. B. „Öffnen Sie eine Claude Code-Sitzung und beheben Sie den Login-Fehler", oder Dispatch entscheidet, dass die Aufgabe Entwicklungsarbeit ist und startet eine von selbst. Aufgaben, die typischerweise zu Code führen, umfassen das Beheben von Fehlern, das Aktualisieren von Abhängigkeiten, das Ausführen von Tests oder das Öffnen von Pull Requests. Forschung, Dokumentbearbeitung und Tabellenkalkulationsarbeit bleiben in Cowork.

In jedem Fall wird die Code-Sitzung in der Seitenleiste der Registerkarte „Code" mit einem **Dispatch**-Badge angezeigt. Sie erhalten eine Push-Benachrichtigung auf Ihrem Telefon, wenn sie fertig ist oder Ihre Genehmigung benötigt.

Wenn Sie [Computernutzung](#let-claude-use-your-computer) aktiviert haben, können Dispatch-generierte Code-Sitzungen diese auch verwenden. App-Genehmigungen in diesen Sitzungen verfallen nach 30 Minuten und werden erneut angefordert, anstatt die gesamte Sitzung zu dauern wie bei regulären Code-Sitzungen.

Für Setup, Pairing und Dispatch-Einstellungen siehe den [Dispatch-Hilfeartikel](https://support.claude.com/en/articles/13947068). Dispatch erfordert einen Pro- oder Max-Plan und ist nicht für Team- oder Enterprise-Pläne verfügbar.

Dispatch ist eine von mehreren Möglichkeiten, mit Claude zu arbeiten, wenn Sie weg von Ihrem Terminal sind. Siehe [Plattformen und Integrationen](/de/platforms#work-when-you-are-away-from-your-terminal), um es mit Remote Control, Channels, Slack und geplanten Aufgaben zu vergleichen.

## Erweitern Sie Claude Code

Verbinden Sie externe Dienste, fügen Sie wiederverwendbare Workflows hinzu, passen Sie Claudes Verhalten an und konfigurieren Sie Vorschau-Server. Um Konnektoren, Skills und Plugins an einem Ort zu verwalten, klicken Sie auf **Anpassen** in der Seitenleiste.

### Verbinden Sie externe Tools

Für lokale und [SSH](#ssh-sessions)-Sitzungen klicken Sie auf die Schaltfläche **+** neben dem Eingabefeld und wählen Sie **Konnektoren**, um Integrationen wie Google Calendar, Slack, GitHub, Linear, Notion und mehr hinzuzufügen. Sie können Konnektoren vor oder während einer Sitzung hinzufügen. Die Schaltfläche **+** ist nicht in Remote-Sitzungen verfügbar, aber [Routinen](/de/routines) konfigurieren Konnektoren zum Zeitpunkt der Routine-Erstellung.

Um Konnektoren zu verwalten oder zu trennen, gehen Sie zu Einstellungen → Konnektoren in der Desktop-App oder wählen Sie **Konnektoren verwalten** aus dem Konnektoren-Menü im Eingabefeld.

Nach der Verbindung kann Claude Ihren Kalender lesen, Nachrichten senden, Probleme erstellen und direkt mit Ihren Tools interagieren. Sie können Claude fragen, welche Konnektoren in Ihrer Sitzung konfiguriert sind.

Konnektoren sind [MCP-Server](/de/mcp) mit einem grafischen Setup-Ablauf. Verwenden Sie sie für schnelle Integration mit unterstützten Diensten. Für Integrationen, die nicht in Konnektoren aufgelistet sind, fügen Sie MCP-Server manuell über [Einstellungsdateien](/de/mcp#installing-mcp-servers) hinzu. Sie können auch [benutzerdefinierte Konnektoren erstellen](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

### Verwenden Sie Skills

[Skills](/de/skills) erweitern, was Claude tun kann. Claude lädt sie automatisch, wenn relevant, oder Sie können eine direkt aufrufen: Geben Sie `/` im Eingabefeld ein oder klicken Sie auf die Schaltfläche **+** und wählen Sie **Slash-Befehle**, um zu sehen, was verfügbar ist. Dies umfasst [integrierte Befehle](/de/commands), Ihre [benutzerdefinierten Skills](/de/skills#create-your-first-skill), Projekt-Skills aus Ihrer Codebasis und Skills aus allen [installierten Plugins](/de/plugins). Wählen Sie einen aus und er wird im Eingabefeld hervorgehoben angezeigt. Geben Sie Ihre Aufgabe danach ein und senden Sie wie gewohnt.

### Installieren Sie Plugins

[Plugins](/de/plugins) sind wiederverwendbare Pakete, die Skills, Agents, hooks, MCP-Server und LSP-Konfigurationen zu Claude Code hinzufügen. Sie können Plugins aus der Desktop-App installieren, ohne das Terminal zu verwenden.

Für lokale und [SSH](#ssh-sessions)-Sitzungen klicken Sie auf die Schaltfläche **+** neben dem Eingabefeld und wählen Sie **Plugins**, um Ihre installierten Plugins und deren Skills zu sehen. Um ein Plugin hinzuzufügen, wählen Sie **Plugin hinzufügen** aus dem Untermenü, um den Plugin-Browser zu öffnen, der verfügbare Plugins aus Ihren konfigurierten [Marketplaces](/de/plugin-marketplaces) einschließlich des offiziellen Anthropic-Marketplace anzeigt. Wählen Sie **Plugins verwalten**, um Plugins zu aktivieren, zu deaktivieren oder zu deinstallieren.

Plugins können auf Ihr Benutzerkonto, ein bestimmtes Projekt oder nur lokal beschränkt sein. Wenn Ihre Organisation Plugins zentral verwaltet, sind diese Plugins in Desktop-Sitzungen auf die gleiche Weise verfügbar wie in der CLI. Plugins sind nicht für Remote-Sitzungen verfügbar. Für die vollständige Plugin-Referenz einschließlich der Erstellung eigener Plugins siehe [Plugins](/de/plugins).

### Konfigurieren Sie Vorschau-Server

Claude erkennt automatisch Ihr Dev-Server-Setup und speichert die Konfiguration in `.claude/launch.json` im Stammverzeichnis des Ordners, den Sie beim Starten der Sitzung ausgewählt haben. Die Vorschau verwendet diesen Ordner als Arbeitsverzeichnis. Wenn Sie also einen übergeordneten Ordner ausgewählt haben, werden Unterordner mit ihren eigenen Dev-Servern nicht automatisch erkannt. Um mit dem Server eines Unterordners zu arbeiten, starten Sie entweder eine Sitzung direkt in diesem Ordner oder fügen Sie eine Konfiguration manuell hinzu.

Um anzupassen, wie Ihr Server startet, z. B. um `yarn dev` statt `npm run dev` zu verwenden oder den Port zu ändern, bearbeiten Sie die Datei manuell oder klicken Sie auf **Konfiguration bearbeiten** im Dropdown „Vorschau", um sie in Ihrem Code-Editor zu öffnen. Die Datei unterstützt JSON mit Kommentaren.

```json theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

Sie können mehrere Konfigurationen definieren, um verschiedene Server aus demselben Projekt auszuführen, z. B. ein Frontend und eine API. Siehe die [Beispiele](#examples) unten.

#### Automatische Überprüfung von Änderungen

Wenn `autoVerify` aktiviert ist, überprüft Claude automatisch Code-Änderungen nach dem Bearbeiten von Dateien. Es macht Screenshots, prüft auf Fehler und bestätigt, dass Änderungen funktionieren, bevor es seine Antwort abschließt.

Die automatische Überprüfung ist standardmäßig aktiviert. Deaktivieren Sie sie pro Projekt, indem Sie `"autoVerify": false` zu `.claude/launch.json` hinzufügen, oder schalten Sie sie aus dem Dropdown **Vorschau** um.

```json theme={null}
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [...]
}
```

Wenn deaktiviert, sind Vorschau-Tools immer noch verfügbar und Sie können Claude jederzeit bitten, zu überprüfen. Die automatische Überprüfung macht es automatisch nach jeder Bearbeitung.

#### Konfigurationsfelder

Jeder Eintrag im Array `configurations` akzeptiert die folgenden Felder:

| Feld                | Typ       | Beschreibung                                                                                                                                                                                                                                                                                                    |
| ------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`              | string    | Ein eindeutiger Bezeichner für diesen Server                                                                                                                                                                                                                                                                    |
| `runtimeExecutable` | string    | Der auszuführende Befehl, z. B. `npm`, `yarn` oder `node`                                                                                                                                                                                                                                                       |
| `runtimeArgs`       | string\[] | An `runtimeExecutable` übergebene Argumente, z. B. `["run", "dev"]`                                                                                                                                                                                                                                             |
| `port`              | number    | Der Port, auf dem Ihr Server lauscht. Standardmäßig 3000                                                                                                                                                                                                                                                        |
| `cwd`               | string    | Arbeitsverzeichnis relativ zu Ihrem Projektstammverzeichnis. Standardmäßig das Projektstammverzeichnis. Verwenden Sie `${workspaceFolder}`, um das Projektstammverzeichnis explizit zu referenzieren                                                                                                            |
| `env`               | object    | Zusätzliche Umgebungsvariablen als Schlüssel-Wert-Paare, z. B. `{ "NODE_ENV": "development" }`. Legen Sie hier keine Geheimnisse ab, da diese Datei in Ihr Repo committed wird. Um Geheimnisse an Ihren Dev-Server zu übergeben, legen Sie sie stattdessen im [lokalen Umgebungs-Editor](#local-sessions) fest. |
| `autoPort`          | boolean   | Wie Port-Konflikte behandelt werden. Siehe unten                                                                                                                                                                                                                                                                |
| `program`           | string    | Ein mit `node` auszuführendes Skript. Siehe [wann `program` vs `runtimeExecutable` verwendet werden](#when-to-use-program-vs-runtimeexecutable)                                                                                                                                                                 |
| `args`              | string\[] | An `program` übergebene Argumente. Wird nur verwendet, wenn `program` gesetzt ist                                                                                                                                                                                                                               |

##### Wann `program` vs `runtimeExecutable` verwendet werden

Verwenden Sie `runtimeExecutable` mit `runtimeArgs`, um einen Dev-Server über einen Package Manager zu starten. Zum Beispiel `"runtimeExecutable": "npm"` mit `"runtimeArgs": ["run", "dev"]` führt `npm run dev` aus.

Verwenden Sie `program`, wenn Sie ein eigenständiges Skript haben, das Sie direkt mit `node` ausführen möchten. Zum Beispiel `"program": "server.js"` führt `node server.js` aus. Übergeben Sie zusätzliche Flags mit `args`.

#### Port-Konflikte

Das Feld `autoPort` kontrolliert, was passiert, wenn Ihr bevorzugter Port bereits verwendet wird:

* **`true`**: Claude findet und verwendet automatisch einen freien Port. Geeignet für die meisten Dev-Server.
* **`false`**: Claude schlägt mit einem Fehler fehl. Verwenden Sie dies, wenn Ihr Server einen bestimmten Port verwenden muss, z. B. für OAuth-Callbacks oder CORS-Allowlists.
* **Nicht gesetzt (Standard)**: Claude fragt, ob der Server diesen genauen Port benötigt, und speichert dann Ihre Antwort.

Wenn Claude einen anderen Port wählt, übergibt es den zugewiesenen Port an Ihren Server über die Umgebungsvariable `PORT`.

#### Beispiele

Diese Konfigurationen zeigen häufige Setups für verschiedene Projekttypen:

<Tabs>
  <Tab title="Next.js">
    Diese Konfiguration führt eine Next.js-App mit Yarn auf Port 3000 aus:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "web",
          "runtimeExecutable": "yarn",
          "runtimeArgs": ["dev"],
          "port": 3000
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Multiple servers">
    Für ein Monorepo mit einem Frontend und einem API-Server definieren Sie mehrere Konfigurationen. Das Frontend verwendet `autoPort: true`, sodass es einen freien Port wählt, wenn 3000 belegt ist, während der API-Server Port 8080 genau benötigt:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "frontend",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "dev"],
          "cwd": "apps/web",
          "port": 3000,
          "autoPort": true
        },
        {
          "name": "api",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "start"],
          "cwd": "server",
          "port": 8080,
          "env": { "NODE_ENV": "development" },
          "autoPort": false
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Node.js script">
    Um ein Node.js-Skript direkt auszuführen, statt einen Package-Manager-Befehl zu verwenden, verwenden Sie das Feld `program`:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "server",
          "program": "server.js",
          "args": ["--verbose"],
          "port": 4000
        }
      ]
    }
    ```
  </Tab>
</Tabs>

## Umgebungskonfiguration

Die Umgebung, die Sie beim [Starten einer Sitzung](#start-a-session) wählen, bestimmt, wo Claude ausgeführt wird und wie Sie sich verbinden:

* **Lokal**: läuft auf Ihrem Computer mit direktem Zugriff auf Ihre Dateien
* **Remote**: läuft auf Anthropics Cloud-Infrastruktur. Sitzungen werden fortgesetzt, auch wenn Sie die App schließen.
* **SSH**: läuft auf einem Remote-Computer, mit dem Sie sich über SSH verbinden, z. B. Ihre eigenen Server, Cloud-VMs oder Dev-Container

### Lokale Sitzungen

Die Desktop-App erbt nicht immer Ihre vollständige Shell-Umgebung. Auf macOS liest die App beim Starten aus dem Dock oder Finder Ihr Shell-Profil, z. B. `~/.zshrc` oder `~/.bashrc`, um `PATH` und einen festen Satz von Claude Code-Variablen zu extrahieren, aber andere Variablen, die Sie dort exportieren, werden nicht übernommen. Unter Windows erbt die App Benutzer- und Systemumgebungsvariablen, liest aber keine PowerShell-Profile.

Um Umgebungsvariablen für lokale Sitzungen und Dev-Server auf jeder Plattform festzulegen, öffnen Sie das Umgebungs-Dropdown im Eingabefeld, fahren Sie mit der Maus über **Lokal** und klicken Sie auf das Zahnrad-Symbol, um den lokalen Umgebungs-Editor zu öffnen. Variablen, die Sie hier speichern, werden verschlüsselt auf Ihrem Computer gespeichert und gelten für jede lokale Sitzung und jeden Vorschau-Server, den Sie starten. Sie können auch Variablen zum Schlüssel `env` in Ihrer Datei `~/.claude/settings.json` hinzufügen, obwohl diese nur Claude-Sitzungen erreichen und nicht Dev-Server. Siehe [Umgebungsvariablen](/de/env-vars) für die vollständige Liste der unterstützten Variablen.

[Erweitertes Denken](/de/model-config#extended-thinking) ist standardmäßig aktiviert, was die Leistung bei komplexen Denkaufgaben verbessert, aber zusätzliche Token verwendet. Um das Denken vollständig zu deaktivieren, setzen Sie `MAX_THINKING_TOKENS` auf `0` im lokalen Umgebungs-Editor. Bei Modellen mit [adaptiver Argumentation](/de/model-config#adjust-effort-level) wird jeder andere `MAX_THINKING_TOKENS`-Wert ignoriert, da adaptive Argumentation die Denktiefe steuert. Bei Opus 4.6 und Sonnet 4.6 setzen Sie `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` auf `1`, um ein festes Denk-Budget zu verwenden; Opus 4.7 verwendet immer adaptive Argumentation und hat keinen Modus mit festem Budget.

### Remote-Sitzungen

Remote-Sitzungen werden im Hintergrund fortgesetzt, auch wenn Sie die App schließen. Die Nutzung wird auf Ihre [Abonnementplanlimits](/de/costs) angerechnet, ohne separate Compute-Gebühren.

Sie können benutzerdefinierte Cloud-Umgebungen mit verschiedenen Netzwerkzugriffsstufen und Umgebungsvariablen erstellen. Wählen Sie das Umgebungs-Dropdown beim Starten einer Remote-Sitzung und wählen Sie **Umgebung hinzufügen**. Siehe [die Cloud-Umgebung](/de/claude-code-on-the-web#the-cloud-environment) für Details zur Konfiguration von Netzwerkzugriff und Umgebungsvariablen.

### SSH-Sitzungen

SSH-Sitzungen ermöglichen es Ihnen, Claude Code auf einem Remote-Computer auszuführen, während Sie die Desktop-App als Ihre Schnittstelle verwenden. Dies ist nützlich für die Arbeit mit Codebases, die auf Cloud-VMs, Dev-Containern oder Servern mit spezifischer Hardware oder Abhängigkeiten vorhanden sind.

Um eine SSH-Verbindung hinzuzufügen, klicken Sie auf das Umgebungs-Dropdown vor dem Starten einer Sitzung und wählen Sie **+ SSH-Verbindung hinzufügen**. Der Dialog fragt nach:

* **Name**: ein freundlicher Bezeichner für diese Verbindung
* **SSH-Host**: `user@hostname` oder ein in `~/.ssh/config` definierter Host
* **SSH-Port**: Standard ist 22, wenn leer gelassen, oder verwendet den Port aus Ihrer SSH-Konfiguration
* **Identity File**: Pfad zu Ihrem privaten Schlüssel, z. B. `~/.ssh/id_rsa`. Lassen Sie leer, um den Standardschlüssel oder Ihre SSH-Konfiguration zu verwenden.

Nach dem Hinzufügen wird die Verbindung im Umgebungs-Dropdown angezeigt. Wählen Sie sie aus, um eine Sitzung auf diesem Computer zu starten. Claude läuft auf dem Remote-Computer mit Zugriff auf seine Dateien und Tools.

Der Remote-Computer muss Linux oder macOS ausführen. Die Desktop-App installiert Claude Code auf dem Remote-Computer automatisch beim ersten Verbindungsaufbau. Nach der Verbindung unterstützen SSH-Sitzungen Berechtigungsmodi, Konnektoren, Plugins und MCP-Server.

#### SSH-Verbindungen für Ihr Team vorkonfigurieren

Administratoren können SSH-Verbindungen an Teammitglieder verteilen, indem sie `sshConfigs` zu einer [verwalteten Einstellungsdatei](/de/settings#settings-precedence) hinzufügen. Auf diese Weise definierte Verbindungen werden in der Umgebungs-Dropdown-Liste jedes Benutzers automatisch angezeigt und sind als verwaltet gekennzeichnet, sodass Benutzer sie auswählen, aber nicht bearbeiten oder löschen können.

Das folgende Beispiel konfiguriert eine einzelne Verbindung vor, die sich in `~/projects` auf dem Remote-Host öffnet:

```json theme={null}
{
  "sshConfigs": [
    {
      "id": "shared-dev-vm",
      "name": "Shared Dev VM",
      "sshHost": "user@dev.example.com",
      "sshPort": 22,
      "sshIdentityFile": "~/.ssh/id_ed25519",
      "startDirectory": "~/projects"
    }
  ]
}
```

Jeder Eintrag erfordert `id`, `name` und `sshHost`. Die Felder `sshPort`, `sshIdentityFile` und `startDirectory` sind optional. Benutzer können auch `sshConfigs` zu ihrer eigenen `~/.claude/settings.json` hinzufügen, wo Verbindungen, die über den Dialog hinzugefügt werden, gespeichert sind.

## Unternehmenskonfiguration

Organisationen in Team- oder Enterprise-Plänen können das Verhalten der Desktop-App durch Admin-Konsolen-Steuerelemente, verwaltete Einstellungsdateien und Geräteverwaltungsrichtlinien verwalten.

### Admin-Konsolen-Steuerelemente

Diese Einstellungen werden über die [Admin-Einstellungskonsole](https://claude.ai/admin-settings/claude-code) konfiguriert:

* **Code in der Desktop-App**: Kontrollieren Sie, ob Benutzer in Ihrer Organisation auf Claude Code in der Desktop-App zugreifen können
* **Code im Web**: Aktivieren oder deaktivieren Sie [Web-Sitzungen](/de/claude-code-on-the-web) für Ihre Organisation
* **Remote Control**: Aktivieren oder deaktivieren Sie [Remote Control](/de/remote-control) für Ihre Organisation
* **Bypass-Berechtigungsmodus deaktivieren**: Verhindern Sie, dass Benutzer in Ihrer Organisation den Bypass-Berechtigungsmodus aktivieren

### Verwaltete Einstellungen

Verwaltete Einstellungen überschreiben Projekt- und Benutzereinstellungen und gelten, wenn Desktop CLI-Sitzungen startet. Sie können diese Schlüssel in der [verwalteten Einstellungsdatei](/de/settings#settings-precedence) Ihrer Organisation oder remote über die Admin-Konsole festlegen.

| Schlüssel                                  | Beschreibung                                                                                                                                                                                                               |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `permissions.disableBypassPermissionsMode` | auf `"disable"` setzen, um Benutzer daran zu hindern, den Bypass-Berechtigungsmodus zu aktivieren.                                                                                                                         |
| `disableAutoMode`                          | auf `"disable"` setzen, um Benutzer daran zu hindern, den [Auto](/de/permission-modes#eliminate-prompts-with-auto-mode)-Modus zu aktivieren. Entfernt Auto aus dem Moduswahlschalter. Auch unter `permissions` akzeptiert. |
| `autoMode`                                 | passen Sie an, was der Auto-Modus-Klassifizierer über Ihre Organisation vertraut und blockiert. Siehe [Auto-Modus konfigurieren](/de/auto-mode-config).                                                                    |
| `sshConfigs`                               | vorkonfigurieren Sie [SSH-Verbindungen](#pre-configure-ssh-connections-for-your-team), die in der Umgebungs-Dropdown angezeigt werden. Benutzer können verwaltete Verbindungen nicht bearbeiten oder löschen.              |

Eine verwaltete Einstellungsdatei, die auf jedem Computer auf der Festplatte bereitgestellt wird, gilt für Desktop-Sitzungen. Verwaltete Einstellungen, die remote über die Admin-Konsole hochgeladen werden, erreichen derzeit nur CLI- und IDE-Sitzungen. Für Desktop-Bereitstellungen verteilen Sie die Datei daher über MDM oder verwenden Sie die [Admin-Konsolen-Steuerelemente](#admin-console-controls) oben.

`permissions.disableBypassPermissionsMode` und `disableAutoMode` funktionieren auch in Benutzer- und Projekteinstellungen, aber das Platzieren in verwalteten Einstellungen verhindert, dass Benutzer sie überschreiben. `autoMode` wird aus Benutzereinstellungen, `.claude/settings.local.json` und verwalteten Einstellungen gelesen, aber nicht aus der eingecheckten `.claude/settings.json`: ein geklontes Repo kann seine eigenen Klassifiziererregeln nicht injizieren. Für die vollständige Liste der verwalteten Einstellungen einschließlich `allowManagedPermissionRulesOnly` und `allowManagedHooksOnly` siehe [verwaltete Einstellungen](/de/permissions#managed-only-settings).

### Geräteverwaltungsrichtlinien

IT-Teams können die Desktop-App über MDM auf macOS oder Gruppenrichtlinie unter Windows verwalten. Verfügbare Richtlinien umfassen das Aktivieren oder Deaktivieren der Claude-Code-Funktion, das Steuern von Auto-Updates und das Festlegen einer benutzerdefinierten Bereitstellungs-URL.

* **macOS**: Konfigurieren Sie über die Präferenzdomäne `com.anthropic.Claude` mit Tools wie Jamf oder Kandji
* **Windows**: Konfigurieren Sie über die Registrierung unter `SOFTWARE\Policies\Claude`

### Authentifizierung und SSO

Enterprise-Organisationen können SSO für alle Benutzer verlangen. Siehe [Authentifizierung](/de/authentication) für Plan-Level-Details und [Einrichten von SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso) für SAML- und OIDC-Konfiguration.

### Datenbehandlung

Claude Code verarbeitet Ihren Code lokal in lokalen Sitzungen oder auf Anthropics Cloud-Infrastruktur in Remote-Sitzungen. Gespräche und Code-Kontext werden an Anthropics API zur Verarbeitung gesendet. Siehe [Datenbehandlung](/de/data-usage) für Details zu Datenspeicherung, Datenschutz und Compliance.

### Bereitstellung

Desktop kann über Enterprise-Bereitstellungstools verteilt werden:

* **macOS**: Verteilen Sie über MDM wie Jamf oder Kandji mit dem `.dmg`-Installer
* **Windows**: Stellen Sie über MSIX-Paket oder `.exe`-Installer bereit. Siehe [Claude Desktop für Windows bereitstellen](https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows) für Enterprise-Bereitstellungsoptionen einschließlich stiller Installation

Für Netzwerkkonfiguration wie Proxy-Einstellungen, Firewall-Allowlisting und LLM-Gateways siehe [Netzwerkkonfiguration](/de/network-config).

Für die vollständige Enterprise-Konfigurationsreferenz siehe das [Enterprise-Konfigurationshandbuch](https://support.claude.com/en/articles/12622667-enterprise-configuration).

## Kommen Sie von der CLI?

Wenn Sie bereits die Claude Code CLI verwenden, führt Desktop dieselbe zugrunde liegende Engine mit einer grafischen Benutzeroberfläche aus. Sie können beide gleichzeitig auf demselben Computer ausführen, sogar auf demselben Projekt. Jede behält separate Sitzungsverlauf, aber sie teilen Konfiguration und Projektgedächtnis über CLAUDE.md-Dateien.

Um eine CLI-Sitzung in Desktop zu verschieben, führen Sie `/desktop` im Terminal aus. Claude speichert Ihre Sitzung und öffnet sie in der Desktop-App, dann beendet die CLI. Dieser Befehl ist nur auf macOS und Windows verfügbar.

<Tip>
  Wann Desktop vs CLI verwendet werden: Verwenden Sie Desktop, wenn Sie parallele Sitzungen in einem Fenster verwalten, Panes nebeneinander anordnen oder Änderungen visuell überprüfen möchten. Verwenden Sie die CLI, wenn Sie Scripting, Automatisierung oder einen Terminal-Workflow bevorzugen.
</Tip>

### CLI-Flag-Äquivalente

Diese Tabelle zeigt das Desktop-App-Äquivalent für häufige CLI-Flags. Flags, die nicht aufgelistet sind, haben kein Desktop-Äquivalent, da sie für Scripting oder Automatisierung konzipiert sind.

| CLI                                     | Desktop-Äquivalent                                                                                                                                                                 |
| --------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--model sonnet`                        | Modell-Dropdown neben der Schaltfläche „Senden"                                                                                                                                    |
| `--resume`, `--continue`                | Klicken Sie auf eine Sitzung in der Seitenleiste                                                                                                                                   |
| `--permission-mode`                     | Moduswahlschalter neben der Schaltfläche „Senden"                                                                                                                                  |
| `--dangerously-skip-permissions`        | Bypass-Berechtigungsmodus. Aktivieren Sie in Einstellungen → Claude Code → „Bypass-Berechtigungsmodus zulassen". Enterprise-Administratoren können diese Einstellung deaktivieren. |
| `--add-dir`                             | Fügen Sie mehrere Repos mit der Schaltfläche **+** in Remote-Sitzungen hinzu                                                                                                       |
| `--allowedTools`, `--disallowedTools`   | Kein Pro-Sitzungs-Äquivalent. Berechtigungsregeln in [Einstellungsdateien](/de/settings) gelten weiterhin.                                                                         |
| `--verbose`                             | [Ausführliche Ansichtsmodus](#switch-view-modes) im Dropdown „Transkript-Ansicht"                                                                                                  |
| `--print`, `--output-format`            | Nicht verfügbar. Desktop ist nur interaktiv.                                                                                                                                       |
| `ANTHROPIC_MODEL` Umgebungsvariable     | Modell-Dropdown neben der Schaltfläche „Senden"                                                                                                                                    |
| `MAX_THINKING_TOKENS` Umgebungsvariable | Im lokalen Umgebungs-Editor festlegen. Siehe [Umgebungskonfiguration](#environment-configuration).                                                                                 |

### Gemeinsame Konfiguration

Desktop und CLI lesen dieselben Konfigurationsdateien, daher wird Ihr Setup übertragen:

* **[CLAUDE.md](/de/memory)** und `CLAUDE.local.md`-Dateien in Ihrem Projekt werden von beiden verwendet
* **[MCP-Server](/de/mcp)**, die in `~/.claude.json` oder `.mcp.json` konfiguriert sind, funktionieren in beiden
* **[Hooks](/de/hooks)** und **[Skills](/de/skills)**, die in Einstellungen definiert sind, gelten für beide
* **[Einstellungen](/de/settings)** in `~/.claude.json` und `~/.claude/settings.json` werden geteilt. Berechtigungsregeln, erlaubte Tools und andere Einstellungen in `settings.json` gelten für Desktop-Sitzungen.
* **Modelle**: Sonnet, Opus und Haiku sind in beiden verfügbar. Wählen Sie in Desktop das Modell aus dem Dropdown neben der Schaltfläche „Senden". Sie können das Modell während der Sitzung ändern.

<Note>
  **MCP-Server: Desktop-Chat-App vs Claude Code**: MCP-Server, die für die Claude Desktop-Chat-App in `claude_desktop_config.json` konfiguriert sind, sind separat von Claude Code und werden nicht auf der Registerkarte „Code" angezeigt. Um MCP-Server in Claude Code zu verwenden, konfigurieren Sie sie in `~/.claude.json` oder der `.mcp.json`-Datei Ihres Projekts. Siehe [MCP-Konfiguration](/de/mcp#installing-mcp-servers) für Details.
</Note>

### Funktionsvergleich

Diese Tabelle vergleicht Kernfunktionen zwischen CLI und Desktop. Für eine vollständige Liste der CLI-Flags siehe die [CLI-Referenz](/de/cli-reference).

| Funktion                                               | CLI                                                       | Desktop                                                                                                                                                                                                                                 |
| ------------------------------------------------------ | --------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Berechtigungsmodi                                      | Alle Modi einschließlich `dontAsk`                        | Berechtigungen erfragen, Bearbeitungen automatisch akzeptieren, Plan Mode, Auto und Bypass-Berechtigungen über Einstellungen                                                                                                            |
| `--dangerously-skip-permissions`                       | CLI-Flag                                                  | Bypass-Berechtigungsmodus. Aktivieren Sie in Einstellungen → Claude Code → „Bypass-Berechtigungsmodus zulassen"                                                                                                                         |
| [Drittanbieter-Provider](/de/third-party-integrations) | Bedrock, Vertex, Foundry                                  | Anthropics API standardmäßig. Enterprise-Bereitstellungen können Vertex AI und Gateway-Provider konfigurieren. Siehe das [Enterprise-Konfigurationshandbuch](https://support.claude.com/en/articles/12622667-enterprise-configuration). |
| [MCP-Server](/de/mcp)                                  | In Einstellungsdateien konfigurieren                      | Konnektoren-UI für lokale und SSH-Sitzungen oder Einstellungsdateien                                                                                                                                                                    |
| [Plugins](/de/plugins)                                 | `/plugin`-Befehl                                          | Plugin-Manager-UI                                                                                                                                                                                                                       |
| @mention-Dateien                                       | Textbasiert                                               | Mit Autovervollständigung; lokale und SSH-Sitzungen nur                                                                                                                                                                                 |
| Dateianhänge                                           | Nicht verfügbar                                           | Bilder, PDFs                                                                                                                                                                                                                            |
| Sitzungsisolation                                      | [`--worktree`](/de/cli-reference)-Flag                    | Automatische Worktrees                                                                                                                                                                                                                  |
| Mehrere Sitzungen                                      | Separate Terminals                                        | Seitenleisten-Tabs                                                                                                                                                                                                                      |
| Wiederkehrende Aufgaben                                | Cron-Jobs, CI-Pipelines                                   | [Geplante Aufgaben](/de/desktop-scheduled-tasks)                                                                                                                                                                                        |
| Computernutzung                                        | [Aktivieren über `/mcp`](/de/computer-use) auf macOS      | [App- und Bildschirmsteuerung](#let-claude-use-your-computer) auf macOS und Windows                                                                                                                                                     |
| Dispatch-Integration                                   | Nicht verfügbar                                           | [Dispatch-Sitzungen](#sessions-from-dispatch) in der Seitenleiste                                                                                                                                                                       |
| Scripting und Automatisierung                          | [`--print`](/de/cli-reference), [Agent SDK](/de/headless) | Nicht verfügbar                                                                                                                                                                                                                         |

### Was ist nicht in Desktop verfügbar

Die folgenden Funktionen sind nur in der CLI oder VS Code-Erweiterung verfügbar:

* **Drittanbieter-Provider**: Desktop verbindet sich mit Anthropics API standardmäßig. Enterprise-Bereitstellungen können Vertex AI und Gateway-Provider über [verwaltete Einstellungen](https://support.claude.com/en/articles/12622667-enterprise-configuration) konfigurieren. Für Bedrock oder Foundry verwenden Sie die [CLI](/de/quickstart).
* **Linux**: Die Desktop-App ist nur auf macOS und Windows verfügbar. Verwenden Sie unter Linux die [CLI](/de/quickstart).
* **Inline-Code-Vorschläge**: Desktop bietet keine Autovervollständigungs-ähnlichen Vorschläge. Es funktioniert durch Gesprächseingaben und explizite Code-Änderungen.
* **Agent-Teams**: Multi-Agent-Orchestrierung ist über die [CLI](/de/agent-teams) und [Agent SDK](/de/headless) verfügbar, nicht in Desktop.

## Fehlerbehebung

Die folgenden Abschnitte behandeln Probleme, die spezifisch für die Desktop-App sind. Für Runtime-API-Fehler, die im Chat angezeigt werden, wie `API Error: 500`, `529 Overloaded`, `429` oder `Prompt is too long`, siehe die [Fehlerreferenz](/de/errors). Diese Fehler und ihre Lösungen sind gleich über CLI, Desktop und Web.

### Überprüfen Sie Ihre Version

Um zu sehen, welche Version der Desktop-App Sie ausführen:

* **macOS**: Klicken Sie auf **Claude** in der Menüleiste und dann auf **Über Claude**
* **Windows**: Klicken Sie auf **Hilfe** und dann auf **Über**

Klicken Sie auf die Versionsnummer, um sie in Ihre Zwischenablage zu kopieren.

### 403 oder Authentifizierungsfehler auf der Registerkarte „Code"

Wenn Sie `Error 403: Forbidden` oder andere Authentifizierungsfehler bei der Verwendung der Registerkarte „Code" sehen:

1. Melden Sie sich aus dem App-Menü ab und wieder an. Dies ist die häufigste Lösung.
2. Überprüfen Sie, ob Sie ein aktives bezahltes Abonnement haben: Pro, Max, Team oder Enterprise.
3. Wenn die CLI funktioniert, aber Desktop nicht, beenden Sie die Desktop-App vollständig, nicht nur das Fenster schließen, und öffnen Sie sie dann erneut und melden Sie sich an.
4. Überprüfen Sie Ihre Internetverbindung und Proxy-Einstellungen.

### Leerer oder hängender Bildschirm beim Start

Wenn die App öffnet, aber einen leeren oder nicht reagierenden Bildschirm anzeigt:

1. Starten Sie die App neu.
2. Überprüfen Sie auf ausstehende Updates. Die App wird beim Start automatisch aktualisiert.
3. Überprüfen Sie unter Windows den Event Viewer auf Absturzprotokolle unter **Windows Logs → Application**.

### „Fehler beim Laden der Sitzung"

Wenn Sie `Failed to load session` sehen, existiert der ausgewählte Ordner möglicherweise nicht mehr, ein Git-Repository benötigt möglicherweise Git LFS, das nicht installiert ist, oder Dateiberechtigungen verhindern möglicherweise den Zugriff. Versuchen Sie, einen anderen Ordner auszuwählen oder die App neu zu starten.

### Sitzung findet installierte Tools nicht

Wenn Claude Tools wie `npm`, `node` oder andere CLI-Befehle nicht finden kann, überprüfen Sie, dass die Tools in Ihrem regulären Terminal funktionieren, überprüfen Sie, dass Ihr Shell-Profil PATH richtig einrichtet, und starten Sie die Desktop-App neu, um Umgebungsvariablen neu zu laden.

### Git- und Git LFS-Fehler

Unter Windows ist Git erforderlich, damit die Registerkarte „Code" lokale Sitzungen startet. Wenn Sie „Git is required" sehen, installieren Sie [Git für Windows](https://git-scm.com/downloads/win) und starten Sie die App neu.

Wenn Sie „Git LFS is required by this repository but is not installed" sehen, installieren Sie Git LFS von [git-lfs.com](https://git-lfs.com/), führen Sie `git lfs install` aus und starten Sie die App neu.

### MCP-Server funktionieren nicht unter Windows

Wenn MCP-Server-Umschalter nicht reagieren oder Server unter Windows keine Verbindung herstellen, überprüfen Sie, dass der Server in Ihren Einstellungen richtig konfiguriert ist, starten Sie die App neu, überprüfen Sie, dass der Server-Prozess im Task Manager läuft, und überprüfen Sie Server-Protokolle auf Verbindungsfehler.

### App wird nicht beendet

* **macOS**: drücken Sie Cmd+Q. Wenn die App nicht reagiert, verwenden Sie Force Quit mit Cmd+Option+Esc, wählen Sie Claude und klicken Sie auf Force Quit.
* **Windows**: verwenden Sie Task Manager mit Strg+Umschalt+Esc, um den Claude-Prozess zu beenden.

### Windows-spezifische Probleme

* **PATH nicht aktualisiert nach Installation**: Öffnen Sie ein neues Terminal-Fenster. PATH-Updates gelten nur für neue Terminal-Sitzungen.
* **Fehler bei gleichzeitiger Installation**: Wenn Sie einen Fehler über eine andere Installation sehen, die läuft, aber es gibt keine, versuchen Sie, das Installationsprogramm als Administrator auszuführen.

### „Branch existiert noch nicht" beim Öffnen in CLI

Remote-Sitzungen können Branches erstellen, die auf Ihrem lokalen Computer nicht existieren. Klicken Sie auf den Branch-Namen in der Sitzungs-Symbolleiste, um ihn zu kopieren, und rufen Sie ihn dann lokal ab:

```bash theme={null}
git fetch origin <branch-name>
git checkout <branch-name>
```

### Immer noch stecken?

* Suchen Sie oder melden Sie einen Fehler auf [GitHub Issues](https://github.com/anthropics/claude-code/issues)
* Besuchen Sie das [Claude Support Center](https://support.claude.com/)

Wenn Sie einen Fehler melden, geben Sie Ihre Desktop-App-Version, Ihr Betriebssystem, die genaue Fehlermeldung und relevante Protokolle an. Überprüfen Sie auf macOS Console.app. Überprüfen Sie unter Windows Event Viewer → Windows Logs → Application.
