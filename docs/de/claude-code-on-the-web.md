> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code im Web

> Führen Sie Claude Code-Aufgaben asynchron auf sicherer Cloud-Infrastruktur aus

<Note>
  Claude Code im Web befindet sich derzeit in der Forschungsvorschau.
</Note>

## Was ist Claude Code im Web?

Claude Code im Web ermöglicht es Entwicklern, Claude Code aus der Claude-App zu starten. Dies ist perfekt für:

* **Fragen beantworten**: Fragen zur Code-Architektur und zur Implementierung von Funktionen stellen
* **Fehlerbehebung und Routineaufgaben**: Gut definierte Aufgaben, die keine häufige Steuerung erfordern
* **Parallele Arbeit**: Mehrere Fehlerbehebungen parallel durchführen
* **Repositories nicht auf Ihrem lokalen Computer**: Arbeiten Sie an Code, den Sie nicht lokal ausgecheckt haben
* **Backend-Änderungen**: Wo Claude Code Tests schreiben und dann Code schreiben kann, um diese Tests zu bestehen

Claude Code ist auch in der Claude-App für [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) und [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) verfügbar, um Aufgaben unterwegs zu starten und laufende Arbeiten zu überwachen.

Sie können [neue Aufgaben im Web von Ihrem Terminal aus starten](#from-terminal-to-web) mit `--remote`, oder [Web-Sitzungen zurück zu Ihrem Terminal teleportieren](#from-web-to-terminal), um lokal fortzufahren. Um die Web-Oberfläche zu verwenden, während Sie Claude Code auf Ihrem eigenen Computer statt auf Cloud-Infrastruktur ausführen, siehe [Remote Control](/de/remote-control).

## Wer kann Claude Code im Web nutzen?

Claude Code im Web ist in der Forschungsvorschau verfügbar für:

* **Pro-Benutzer**
* **Max-Benutzer**
* **Team-Benutzer**
* **Enterprise-Benutzer** mit Premium-Sitzen oder Chat + Claude Code-Sitzen

## Erste Schritte

Richten Sie Claude Code im Web über den Browser oder von Ihrem Terminal aus ein.

### Vom Browser

1. Besuchen Sie [claude.ai/code](https://claude.ai/code)
2. Verbinden Sie Ihr GitHub-Konto
3. Installieren Sie die Claude GitHub-App in Ihren Repositories
4. Wählen Sie Ihre Standardumgebung
5. Reichen Sie Ihre Coding-Aufgabe ein
6. Überprüfen Sie Änderungen in der Diff-Ansicht, iterieren Sie mit Kommentaren und erstellen Sie dann einen Pull Request

### Vom Terminal

Führen Sie `/web-setup` innerhalb von Claude Code aus, um GitHub mit Ihren lokalen `gh` CLI-Anmeldedaten zu verbinden. Der Befehl synchronisiert Ihr `gh auth token` mit Claude Code im Web, erstellt eine Standard-Cloud-Umgebung und öffnet claude.ai/code in Ihrem Browser, wenn er fertig ist.

Dieser Pfad erfordert, dass die `gh` CLI installiert und mit `gh auth login` authentifiziert ist. Wenn `gh` nicht verfügbar ist, öffnet `/web-setup` claude.ai/code, damit Sie GitHub stattdessen vom Browser aus verbinden können.

Ihre `gh`-Anmeldedaten geben Claude Zugriff zum Klonen und Pushen, sodass Sie die GitHub-App für grundlegende Sitzungen überspringen können. Installieren Sie die App später, wenn Sie [Auto-fix](#auto-fix-pull-requests) möchten, das die App verwendet, um PR-Webhooks zu empfangen.

<Note>
  Team- und Enterprise-Administratoren können das Terminal-Setup mit dem Quick web setup-Umschalter unter [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) deaktivieren.
</Note>

## Wie es funktioniert

Wenn Sie eine Aufgabe in Claude Code im Web starten:

1. **Repository-Klonen**: Ihr Repository wird auf eine von Anthropic verwaltete virtuelle Maschine geklont
2. **Umgebungssetup**: Claude bereitet eine sichere Cloud-Umgebung mit Ihrem Code vor und führt dann Ihr [Setup-Skript](#setup-scripts) aus, falls konfiguriert
3. **Netzwerkkonfiguration**: Der Internetzugriff wird basierend auf Ihren Einstellungen konfiguriert
4. **Aufgabenausführung**: Claude analysiert Code, nimmt Änderungen vor, führt Tests aus und überprüft seine Arbeit
5. **Fertigstellung**: Sie werden benachrichtigt, wenn die Aufgabe abgeschlossen ist, und können einen PR mit den Änderungen erstellen
6. **Ergebnisse**: Änderungen werden in einen Branch gepusht, bereit für die Pull Request-Erstellung

## Überprüfen Sie Änderungen mit der Diff-Ansicht

Die Diff-Ansicht zeigt Ihnen genau, was Claude geändert hat, bevor Sie einen Pull Request erstellen. Anstatt auf „PR erstellen" zu klicken, um Änderungen in GitHub zu überprüfen, sehen Sie den Diff direkt in der App und iterieren Sie mit Claude, bis die Änderungen bereit sind.

Wenn Claude Änderungen an Dateien vornimmt, wird ein Diff-Statistik-Indikator angezeigt, der die Anzahl der hinzugefügten und entfernten Zeilen anzeigt (z. B. `+12 -1`). Wählen Sie diesen Indikator, um den Diff-Viewer zu öffnen, der eine Dateiliste auf der linken Seite und die Änderungen für jede Datei auf der rechten Seite anzeigt.

Aus der Diff-Ansicht können Sie:

* Änderungen Datei für Datei überprüfen
* Kommentare zu bestimmten Änderungen hinterlassen, um Änderungen anzufordern
* Mit Claude basierend auf dem, was Sie sehen, weiter iterieren

Dies ermöglicht es Ihnen, Änderungen durch mehrere Runden von Feedback zu verfeinern, ohne Draft-PRs zu erstellen oder zu GitHub zu wechseln.

## Auto-fix Pull Requests

Claude kann einen Pull Request überwachen und automatisch auf CI-Fehler und Review-Kommentare reagieren. Claude abonniert GitHub-Aktivitäten auf dem PR, und wenn eine Überprüfung fehlschlägt oder ein Reviewer einen Kommentar hinterlässt, untersucht Claude das Problem und pusht eine Lösung, wenn eine klar ist.

<Note>
  Auto-fix erfordert, dass die Claude GitHub-App auf Ihrem Repository installiert ist. Falls noch nicht geschehen, installieren Sie sie von der [GitHub App-Seite](https://github.com/apps/claude) oder wenn Sie dazu während des [Setups](#getting-started) aufgefordert werden.
</Note>

Es gibt mehrere Möglichkeiten, Auto-fix zu aktivieren, je nachdem, woher der PR stammt und welches Gerät Sie verwenden:

* **PRs, die in Claude Code im Web erstellt wurden**: Öffnen Sie die CI-Statusleiste und wählen Sie **Auto-fix**
* **Von der Mobile-App**: Sagen Sie Claude, den PR zu auto-fixen, zum Beispiel „watch this PR and fix any CI failures or review comments"
* **Jeder vorhandene PR**: Fügen Sie die PR-URL in eine Sitzung ein und sagen Sie Claude, den PR zu auto-fixen

### Wie Claude auf PR-Aktivität reagiert

Wenn Auto-fix aktiv ist, empfängt Claude GitHub-Events für den PR, einschließlich neuer Review-Kommentare und CI-Check-Fehler. Für jedes Event untersucht Claude das Problem und entscheidet, wie vorgegangen wird:

* **Klare Fixes**: Wenn Claude sich einer Lösung sicher ist und sie nicht mit früheren Anweisungen in Konflikt steht, nimmt Claude die Änderung vor, pusht sie und erklärt, was getan wurde, in der Sitzung
* **Mehrdeutige Anfragen**: Wenn ein Reviewer-Kommentar auf mehrere Arten interpretiert werden könnte oder etwas architektonisch Bedeutsames betrifft, fragt Claude Sie, bevor er handelt
* **Doppelte oder keine Aktion erforderlich Events**: Wenn ein Event ein Duplikat ist oder keine Änderung erfordert, notiert Claude es in der Sitzung und fährt fort

Claude kann als Teil der Auflösung auf Review-Kommentar-Threads auf GitHub antworten. Diese Antworten werden mit Ihrem GitHub-Konto gepostet, sodass sie unter Ihrem Benutzernamen erscheinen, aber jede Antwort ist als von Claude Code stammend gekennzeichnet, damit Reviewer wissen, dass sie vom Agent geschrieben wurde und nicht direkt von Ihnen.

## Verschieben von Aufgaben zwischen Web und Terminal

Sie können neue Aufgaben im Web von Ihrem Terminal aus starten oder Web-Sitzungen in Ihr Terminal ziehen, um lokal fortzufahren. Web-Sitzungen bleiben bestehen, auch wenn Sie Ihren Laptop schließen, und Sie können sie von überall aus überwachen, einschließlich der Claude Mobile-App.

<Note>
  Die Sitzungsübergabe ist unidirektional: Sie können Web-Sitzungen in Ihr Terminal ziehen, aber Sie können keine vorhandene Terminal-Sitzung ins Web verschieben. Das Flag `--remote` erstellt eine *neue* Web-Sitzung für Ihr aktuelles Repository.
</Note>

### Vom Terminal zum Web

Starten Sie eine Web-Sitzung von der Befehlszeile mit dem Flag `--remote`:

```bash  theme={null}
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

Dies erstellt eine neue Web-Sitzung auf claude.ai. Die Aufgabe wird in der Cloud ausgeführt, während Sie lokal weiterarbeiten. Verwenden Sie `/tasks`, um den Fortschritt zu überprüfen, oder öffnen Sie die Sitzung auf claude.ai oder der Claude Mobile-App, um direkt zu interagieren. Von dort aus können Sie Claude steuern, Feedback geben oder Fragen beantworten, genau wie in jedem anderen Gespräch.

#### Tipps für Remote-Aufgaben

**Planen Sie lokal, führen Sie remote aus**: Für komplexe Aufgaben starten Sie Claude im Plan Mode, um den Ansatz zu besprechen, und senden Sie dann die Arbeit ins Web:

```bash  theme={null}
claude --permission-mode plan
```

Im Plan Mode kann Claude nur Dateien lesen und das Codebase erkunden. Sobald Sie mit dem Plan zufrieden sind, starten Sie eine Remote-Sitzung für autonome Ausführung:

```bash  theme={null}
claude --remote "Execute the migration plan in docs/migration-plan.md"
```

Dieses Muster gibt Ihnen Kontrolle über die Strategie, während Claude autonom in der Cloud ausgeführt wird.

**Führen Sie Aufgaben parallel aus**: Jeder `--remote`-Befehl erstellt seine eigene Web-Sitzung, die unabhängig ausgeführt wird. Sie können mehrere Aufgaben starten und sie werden alle gleichzeitig in separaten Sitzungen ausgeführt:

```bash  theme={null}
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

Überwachen Sie alle Sitzungen mit `/tasks`. Wenn eine Sitzung abgeschlossen ist, können Sie einen PR aus der Web-Oberfläche erstellen oder die [Sitzung teleportieren](#from-web-to-terminal), um im Terminal fortzufahren.

### Vom Web zum Terminal

Es gibt mehrere Möglichkeiten, eine Web-Sitzung in Ihr Terminal zu ziehen:

* **Mit `/teleport`**: Führen Sie innerhalb von Claude Code `/teleport` (oder `/tp`) aus, um eine interaktive Auswahl Ihrer Web-Sitzungen zu sehen. Wenn Sie nicht committete Änderungen haben, werden Sie aufgefordert, diese zuerst zu stashen.
* **Mit `--teleport`**: Führen Sie von der Befehlszeile `claude --teleport` für eine interaktive Sitzungsauswahl aus, oder `claude --teleport <session-id>`, um eine bestimmte Sitzung direkt fortzusetzen.
* **Von `/tasks`**: Führen Sie `/tasks` aus, um Ihre Hintergrund-Sitzungen zu sehen, drücken Sie dann `t`, um in eine zu teleportieren
* **Von der Web-Oberfläche**: Klicken Sie auf „Open in CLI", um einen Befehl zu kopieren, den Sie in Ihr Terminal einfügen können

Wenn Sie eine Sitzung teleportieren, überprüft Claude, dass Sie sich im richtigen Repository befinden, ruft den Branch aus der Remote-Sitzung ab und checkt ihn aus, und lädt die vollständige Gesprächshistorie in Ihr Terminal.

#### Anforderungen für das Teleportieren

Teleport überprüft diese Anforderungen, bevor eine Sitzung fortgesetzt wird. Wenn eine Anforderung nicht erfüllt ist, sehen Sie einen Fehler oder werden aufgefordert, das Problem zu beheben.

| Anforderung          | Details                                                                                                                                    |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| Sauberer Git-Status  | Ihr Arbeitsverzeichnis darf keine nicht committeten Änderungen haben. Teleport fordert Sie auf, Änderungen zu stashen, falls erforderlich. |
| Korrektes Repository | Sie müssen `--teleport` aus einem Checkout desselben Repositories ausführen, nicht aus einem Fork.                                         |
| Branch verfügbar     | Der Branch aus der Web-Sitzung muss in das Remote gepusht worden sein. Teleport ruft ihn automatisch ab und checkt ihn aus.                |
| Gleiches Konto       | Sie müssen sich bei demselben Claude.ai-Konto authentifizieren, das in der Web-Sitzung verwendet wurde.                                    |

### Sitzungen teilen

Um eine Sitzung zu teilen, schalten Sie ihre Sichtbarkeit gemäß den folgenden Kontotypen um. Danach teilen Sie den Sitzungslink wie gewohnt. Empfänger, die Ihre gemeinsame Sitzung öffnen, sehen den neuesten Status der Sitzung beim Laden, aber die Seite des Empfängers wird nicht in Echtzeit aktualisiert.

#### Teilen von einem Enterprise- oder Teams-Konto

Für Enterprise- und Teams-Konten sind die beiden Sichtbarkeitsoptionen **Privat** und **Team**. Die Team-Sichtbarkeit macht die Sitzung für andere Mitglieder Ihrer Claude.ai-Organisation sichtbar. Die Überprüfung des Repository-Zugriffs ist standardmäßig aktiviert, basierend auf dem GitHub-Konto, das mit dem Konto des Empfängers verbunden ist. Der Anzeigename Ihres Kontos ist für alle Empfänger mit Zugriff sichtbar. [Claude in Slack](/de/slack)-Sitzungen werden automatisch mit Team-Sichtbarkeit geteilt.

#### Teilen von einem Max- oder Pro-Konto

Für Max- und Pro-Konten sind die beiden Sichtbarkeitsoptionen **Privat** und **Öffentlich**. Die öffentliche Sichtbarkeit macht die Sitzung für jeden Benutzer sichtbar, der bei claude.ai angemeldet ist.

Überprüfen Sie Ihre Sitzung auf sensible Inhalte, bevor Sie sie teilen. Sitzungen können Code und Anmeldedaten aus privaten GitHub-Repositories enthalten. Die Überprüfung des Repository-Zugriffs ist standardmäßig nicht aktiviert.

Aktivieren Sie die Überprüfung des Repository-Zugriffs und/oder halten Sie Ihren Namen in Ihren gemeinsamen Sitzungen zurück, indem Sie zu Einstellungen > Claude Code > Freigabeeinstellungen gehen.

## Planen Sie wiederkehrende Aufgaben

Führen Sie Claude nach einem wiederkehrenden Zeitplan aus, um Arbeiten wie tägliche PR-Reviews, Abhängigkeitsprüfungen und CI-Fehleranalyse zu automatisieren. Siehe [Schedule tasks on the web](/de/web-scheduled-tasks) für den vollständigen Leitfaden.

## Verwalten von Sitzungen

### Archivieren von Sitzungen

Sie können Sitzungen archivieren, um Ihre Sitzungsliste organisiert zu halten. Archivierte Sitzungen sind in der Standard-Sitzungsliste ausgeblendet, können aber durch Filtern nach archivierten Sitzungen angezeigt werden.

Um eine Sitzung zu archivieren, bewegen Sie den Mauszeiger über die Sitzung in der Seitenleiste und klicken Sie auf das Archiv-Symbol.

### Löschen von Sitzungen

Das Löschen einer Sitzung entfernt die Sitzung und ihre Daten dauerhaft. Diese Aktion kann nicht rückgängig gemacht werden. Sie können eine Sitzung auf zwei Arten löschen:

* **Von der Seitenleiste**: Filtern Sie nach archivierten Sitzungen, bewegen Sie dann den Mauszeiger über die Sitzung, die Sie löschen möchten, und klicken Sie auf das Lösch-Symbol
* **Vom Sitzungsmenü**: Öffnen Sie eine Sitzung, klicken Sie auf das Dropdown-Menü neben dem Sitzungstitel und wählen Sie **Löschen**

Sie werden aufgefordert, vor dem Löschen einer Sitzung zu bestätigen.

## Cloud-Umgebung

### Standardimage

Wir erstellen und verwalten ein universelles Image mit vorinstallierten gängigen Toolchains und Sprachökosystemen. Dieses Image enthält:

* Beliebte Programmiersprachen und Laufzeiten
* Gängige Build-Tools und Paketmanager
* Test-Frameworks und Linter

#### Überprüfung verfügbarer Tools

Um zu sehen, was in Ihrer Umgebung vorinstalliert ist, bitten Sie Claude Code, Folgendes auszuführen:

```bash  theme={null}
check-tools
```

Dieser Befehl zeigt:

* Programmiersprachen und ihre Versionen
* Verfügbare Paketmanager
* Installierte Entwicklungstools

#### Sprachspezifische Setups

Das universelle Image enthält vorkonfigurierte Umgebungen für:

* **Python**: Python 3.x mit pip, poetry und gängigen wissenschaftlichen Bibliotheken
* **Node.js**: Neueste LTS-Versionen mit npm, yarn, pnpm und bun
* **Ruby**: Versionen 3.1.6, 3.2.6, 3.3.6 (Standard: 3.3.6) mit gem, bundler und rbenv für Versionsverwaltung
* **PHP**: Version 8.4.14
* **Java**: OpenJDK mit Maven und Gradle
* **Go**: Neueste stabile Version mit Modulunterstützung
* **Rust**: Rust-Toolchain mit cargo
* **C++**: GCC- und Clang-Compiler

#### Datenbanken

Das universelle Image enthält die folgenden Datenbanken:

* **PostgreSQL**: Version 16
* **Redis**: Version 7.0

### Umgebungskonfiguration

Wenn Sie eine Sitzung in Claude Code im Web starten, passiert folgendes im Hintergrund:

1. **Umgebungsvorbereitung**: Wir klonen Ihr Repository und führen alle konfigurierten [Setup-Skripte](#setup-scripts) aus. Das Repo wird mit dem Standard-Branch Ihres GitHub-Repos geklont. Wenn Sie einen bestimmten Branch auschecken möchten, können Sie dies in der Eingabeaufforderung angeben.

2. **Netzwerkkonfiguration**: Wir konfigurieren den Internetzugriff für den Agent. Der Internetzugriff ist standardmäßig begrenzt, aber Sie können die Umgebung so konfigurieren, dass sie keinen Internetzugriff oder vollständigen Internetzugriff hat, je nach Ihren Anforderungen.

3. **Claude Code-Ausführung**: Claude Code wird ausgeführt, um Ihre Aufgabe zu erfüllen, Code zu schreiben, Tests auszuführen und seine Arbeit zu überprüfen. Sie können Claude während der Sitzung über die Web-Oberfläche steuern und lenken. Claude respektiert den Kontext, den Sie in Ihrer `CLAUDE.md` definiert haben.

4. **Ergebnis**: Wenn Claude seine Arbeit abgeschlossen hat, pusht es den Branch zu Remote. Sie können einen PR für den Branch erstellen.

<Note>
  Claude arbeitet vollständig über das Terminal und die CLI-Tools, die in der Umgebung verfügbar sind. Es verwendet die vorinstallierten Tools im universellen Image und alle zusätzlichen Tools, die Sie über hooks oder Abhängigkeitsverwaltung installieren.
</Note>

**Um eine neue Umgebung hinzuzufügen:** Wählen Sie die aktuelle Umgebung, um die Umgebungsauswahl zu öffnen, und wählen Sie dann „Umgebung hinzufügen". Dies öffnet einen Dialog, in dem Sie den Umgebungsnamen, die Netzwerkzugriffsstufe, Umgebungsvariablen und ein [Setup-Skript](#setup-scripts) angeben können.

**Um eine vorhandene Umgebung zu aktualisieren:** Wählen Sie die aktuelle Umgebung, rechts neben dem Umgebungsnamen, und wählen Sie die Schaltfläche Einstellungen. Dies öffnet einen Dialog, in dem Sie den Umgebungsnamen, den Netzwerkzugriff, Umgebungsvariablen und das Setup-Skript aktualisieren können.

**Um Ihre Standardumgebung vom Terminal aus auszuwählen:** Wenn Sie mehrere Umgebungen konfiguriert haben, führen Sie `/remote-env` aus, um auszuwählen, welche verwendet werden soll, wenn Sie Web-Sitzungen von Ihrem Terminal mit `--remote` starten. Mit einer einzelnen Umgebung zeigt dieser Befehl Ihre aktuelle Konfiguration an.

<Note>
  Umgebungsvariablen müssen als Schlüssel-Wert-Paare im [`.env`-Format](https://www.dotenv.org/) angegeben werden. Zum Beispiel:

  ```text  theme={null}
  API_KEY=your_api_key
  DEBUG=true
  ```
</Note>

### Setup-Skripte

Ein Setup-Skript ist ein Bash-Skript, das ausgeführt wird, wenn eine neue Cloud-Sitzung startet, bevor Claude Code startet. Verwenden Sie Setup-Skripte, um Abhängigkeiten zu installieren, Tools zu konfigurieren oder alles vorzubereiten, das die Cloud-Umgebung benötigt und nicht im [Standardimage](#default-image) enthalten ist.

Skripte werden als Root auf Ubuntu 24.04 ausgeführt, daher funktionieren `apt install` und die meisten Sprachpaketmanager.

<Tip>
  Um zu überprüfen, was bereits installiert ist, bevor Sie es zu Ihrem Skript hinzufügen, bitten Sie Claude, `check-tools` in einer Cloud-Sitzung auszuführen.
</Tip>

Um ein Setup-Skript hinzuzufügen, öffnen Sie den Dialog Umgebungseinstellungen und geben Sie Ihr Skript in das Feld **Setup-Skript** ein.

Dieses Beispiel installiert die `gh` CLI, die nicht im Standardimage enthalten ist:

```bash  theme={null}
#!/bin/bash
apt update && apt install -y gh
```

Setup-Skripte werden nur beim Erstellen einer neuen Sitzung ausgeführt. Sie werden übersprungen, wenn eine vorhandene Sitzung fortgesetzt wird.

Wenn das Skript mit einem Nicht-Null-Wert beendet wird, schlägt die Sitzung fehl zu starten. Fügen Sie `|| true` an nicht kritische Befehle an, um zu vermeiden, dass die Sitzung bei einer fehlerhaften Installation blockiert wird.

<Note>
  Setup-Skripte, die Pakete installieren, benötigen Netzwerkzugriff, um Registries zu erreichen. Der Standard-Netzwerkzugriff ermöglicht Verbindungen zu [gängigen Paketregistries](#default-allowed-domains), einschließlich npm, PyPI, RubyGems und crates.io. Skripte schlagen fehl, Pakete zu installieren, wenn Ihre Umgebung Netzwerkzugriff deaktiviert hat.
</Note>

#### Setup-Skripte vs. SessionStart-Hooks

Verwenden Sie ein Setup-Skript, um Dinge zu installieren, die die Cloud benötigt, aber Ihr Laptop bereits hat, wie eine Sprachlaufzeit oder ein CLI-Tool. Verwenden Sie einen [SessionStart-Hook](/de/hooks#sessionstart) für Projekt-Setup, das überall ausgeführt werden sollte, Cloud und lokal, wie `npm install`.

Beide werden am Anfang einer Sitzung ausgeführt, aber sie gehören an verschiedene Orte:

|                 | Setup-Skripte                                      | SessionStart-Hooks                                                       |
| --------------- | -------------------------------------------------- | ------------------------------------------------------------------------ |
| Angehängt an    | Die Cloud-Umgebung                                 | Ihr Repository                                                           |
| Konfiguriert in | Cloud-Umgebungs-UI                                 | `.claude/settings.json` in Ihrem Repo                                    |
| Wird ausgeführt | Bevor Claude Code startet, nur bei neuen Sitzungen | Nach Claude Code startet, bei jeder Sitzung einschließlich fortgesetzter |
| Umfang          | Nur Cloud-Umgebungen                               | Sowohl lokal als auch Cloud                                              |

SessionStart-Hooks können auch in Ihrer Benutzer-Level-Datei `~/.claude/settings.json` lokal definiert werden, aber Benutzer-Level-Einstellungen werden nicht zu Cloud-Sitzungen übertragen. In der Cloud werden nur Hooks ausgeführt, die zum Repo committed sind.

### Abhängigkeitsverwaltung

Benutzerdefinierte Umgebungsimages und Snapshots werden noch nicht unterstützt. Verwenden Sie [Setup-Skripte](#setup-scripts), um Pakete zu installieren, wenn eine Sitzung startet, oder [SessionStart-Hooks](/de/hooks#sessionstart) für die Abhängigkeitsinstallation, die auch in lokalen Umgebungen ausgeführt werden sollte. SessionStart-Hooks haben [bekannte Einschränkungen](#dependency-management-limitations).

Um die automatische Abhängigkeitsinstallation mit einem Setup-Skript zu konfigurieren, öffnen Sie Ihre Umgebungseinstellungen und fügen Sie ein Skript hinzu:

```bash  theme={null}
#!/bin/bash
npm install
pip install -r requirements.txt
```

Alternativ können Sie SessionStart-Hooks in der Datei `.claude/settings.json` Ihres Repositories für die Abhängigkeitsinstallation verwenden, die auch in lokalen Umgebungen ausgeführt werden sollte:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

Erstellen Sie das entsprechende Skript unter `scripts/install_pkgs.sh`:

```bash  theme={null}
#!/bin/bash

# Only run in remote environments
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

Machen Sie es ausführbar: `chmod +x scripts/install_pkgs.sh`

#### Umgebungsvariablen beibehalten

SessionStart-Hooks können Umgebungsvariablen für nachfolgende Bash-Befehle beibehalten, indem sie in die Datei schreiben, die in der Umgebungsvariablen `CLAUDE_ENV_FILE` angegeben ist. Weitere Informationen finden Sie unter [SessionStart-Hooks](/de/hooks#sessionstart) in der Hooks-Referenz.

#### Abhängigkeitsverwaltung Einschränkungen

* **Hooks werden für alle Sitzungen ausgelöst**: SessionStart-Hooks werden in lokalen und Remote-Umgebungen ausgeführt. Es gibt keine Hook-Konfiguration, um einen Hook nur auf Remote-Sitzungen zu beschränken. Um die lokale Ausführung zu überspringen, überprüfen Sie die Umgebungsvariable `CLAUDE_CODE_REMOTE` in Ihrem Skript wie oben gezeigt.
* **Erfordert Netzwerkzugriff**: Installationsbefehle benötigen Netzwerkzugriff, um Paketregistries zu erreichen. Wenn Ihre Umgebung mit „Kein Internet"-Zugriff konfiguriert ist, schlagen diese Hooks fehl. Verwenden Sie „Begrenzt" (Standard) oder „Vollständig" Netzwerkzugriff. Die [Standard-Allowlist](#default-allowed-domains) enthält gängige Registries wie npm, PyPI, RubyGems und crates.io.
* **Proxy-Kompatibilität**: Der gesamte ausgehende Datenverkehr in Remote-Umgebungen läuft durch einen [Sicherheits-Proxy](#security-proxy). Einige Paketmanager funktionieren mit diesem Proxy nicht korrekt. Bun ist ein bekanntes Beispiel.
* **Wird bei jedem Sitzungsstart ausgeführt**: Hooks werden jedes Mal ausgeführt, wenn eine Sitzung startet oder fortgesetzt wird, was die Startup-Latenz erhöht. Halten Sie Installationsskripte schnell, indem Sie überprüfen, ob Abhängigkeiten bereits vorhanden sind, bevor Sie sie neu installieren.

## Netzwerkzugriff und Sicherheit

### Netzwerkrichtlinie

#### GitHub-Proxy

Aus Sicherheitsgründen werden alle GitHub-Operationen über einen dedizierten Proxy-Service durchgeführt, der alle Git-Interaktionen transparent verwaltet. Innerhalb der Sandbox authentifiziert sich der Git-Client mit einem benutzerdefinierten Scoped-Credential. Dieser Proxy:

* Verwaltet GitHub-Authentifizierung sicher - der Git-Client verwendet ein Scoped-Credential innerhalb der Sandbox, das der Proxy überprüft und in Ihr tatsächliches GitHub-Authentifizierungstoken übersetzt
* Beschränkt Git-Push-Operationen auf den aktuellen Arbeitsbranch aus Sicherheitsgründen
* Ermöglicht nahtloses Klonen, Abrufen und PR-Operationen bei Beibehaltung von Sicherheitsgrenzen

#### Sicherheits-Proxy

Umgebungen werden aus Sicherheits- und Missbrauchspräventionsgründen hinter einem HTTP/HTTPS-Netzwerk-Proxy ausgeführt. Der gesamte ausgehende Internetdatenverkehr läuft durch diesen Proxy, der Folgendes bietet:

* Schutz vor böswilligen Anfragen
* Ratenbegrenzung und Missbrauchsprävention
* Inhaltsfilterung für erhöhte Sicherheit

### Zugriffsstufen

Standardmäßig ist der Netzwerkzugriff auf [Allowlist-Domains](#default-allowed-domains) begrenzt.

Sie können benutzerdefinierten Netzwerkzugriff konfigurieren, einschließlich Deaktivierung des Netzwerkzugriffs.

### Standard-Allowlist-Domains

Bei Verwendung von „Begrenzt" Netzwerkzugriff sind die folgenden Domains standardmäßig zulässig:

#### Anthropic-Services

* api.anthropic.com
* statsig.anthropic.com
* platform.claude.com
* code.claude.com
* claude.ai

#### Versionskontrolle

* github.com
* [www.github.com](http://www.github.com)
* api.github.com
* npm.pkg.github.com
* raw\.githubusercontent.com
* pkg-npm.githubusercontent.com
* objects.githubusercontent.com
* codeload.github.com
* avatars.githubusercontent.com
* camo.githubusercontent.com
* gist.github.com
* gitlab.com
* [www.gitlab.com](http://www.gitlab.com)
* registry.gitlab.com
* bitbucket.org
* [www.bitbucket.org](http://www.bitbucket.org)
* api.bitbucket.org

#### Container-Registries

* registry-1.docker.io
* auth.docker.io
* index.docker.io
* hub.docker.com
* [www.docker.com](http://www.docker.com)
* production.cloudflare.docker.com
* download.docker.com
* gcr.io
* \*.gcr.io
* ghcr.io
* mcr.microsoft.com
* \*.data.mcr.microsoft.com
* public.ecr.aws

#### Cloud-Plattformen

* cloud.google.com
* accounts.google.com
* gcloud.google.com
* \*.googleapis.com
* storage.googleapis.com
* compute.googleapis.com
* container.googleapis.com
* azure.com
* portal.azure.com
* microsoft.com
* [www.microsoft.com](http://www.microsoft.com)
* \*.microsoftonline.com
* packages.microsoft.com
* dotnet.microsoft.com
* dot.net
* visualstudio.com
* dev.azure.com
* \*.amazonaws.com
* \*.api.aws
* oracle.com
* [www.oracle.com](http://www.oracle.com)
* java.com
* [www.java.com](http://www.java.com)
* java.net
* [www.java.net](http://www.java.net)
* download.oracle.com
* yum.oracle.com

#### Paketmanager - JavaScript/Node

* registry.npmjs.org
* [www.npmjs.com](http://www.npmjs.com)
* [www.npmjs.org](http://www.npmjs.org)
* npmjs.com
* npmjs.org
* yarnpkg.com
* registry.yarnpkg.com

#### Paketmanager - Python

* pypi.org
* [www.pypi.org](http://www.pypi.org)
* files.pythonhosted.org
* pythonhosted.org
* test.pypi.org
* pypi.python.org
* pypa.io
* [www.pypa.io](http://www.pypa.io)

#### Paketmanager - Ruby

* rubygems.org
* [www.rubygems.org](http://www.rubygems.org)
* api.rubygems.org
* index.rubygems.org
* ruby-lang.org
* [www.ruby-lang.org](http://www.ruby-lang.org)
* rubyforge.org
* [www.rubyforge.org](http://www.rubyforge.org)
* rubyonrails.org
* [www.rubyonrails.org](http://www.rubyonrails.org)
* rvm.io
* get.rvm.io

#### Paketmanager - Rust

* crates.io
* [www.crates.io](http://www.crates.io)
* index.crates.io
* static.crates.io
* rustup.rs
* static.rust-lang.org
* [www.rust-lang.org](http://www.rust-lang.org)

#### Paketmanager - Go

* proxy.golang.org
* sum.golang.org
* index.golang.org
* golang.org
* [www.golang.org](http://www.golang.org)
* goproxy.io
* pkg.go.dev

#### Paketmanager - JVM

* maven.org
* repo.maven.org
* central.maven.org
* repo1.maven.org
* jcenter.bintray.com
* gradle.org
* [www.gradle.org](http://www.gradle.org)
* services.gradle.org
* plugins.gradle.org
* kotlin.org
* [www.kotlin.org](http://www.kotlin.org)
* spring.io
* repo.spring.io

#### Paketmanager - Andere Sprachen

* packagist.org (PHP Composer)
* [www.packagist.org](http://www.packagist.org)
* repo.packagist.org
* nuget.org (.NET NuGet)
* [www.nuget.org](http://www.nuget.org)
* api.nuget.org
* pub.dev (Dart/Flutter)
* api.pub.dev
* hex.pm (Elixir/Erlang)
* [www.hex.pm](http://www.hex.pm)
* cpan.org (Perl CPAN)
* [www.cpan.org](http://www.cpan.org)
* metacpan.org
* [www.metacpan.org](http://www.metacpan.org)
* api.metacpan.org
* cocoapods.org (iOS/macOS)
* [www.cocoapods.org](http://www.cocoapods.org)
* cdn.cocoapods.org
* haskell.org
* [www.haskell.org](http://www.haskell.org)
* hackage.haskell.org
* swift.org
* [www.swift.org](http://www.swift.org)

#### Linux-Distributionen

* archive.ubuntu.com
* security.ubuntu.com
* ubuntu.com
* [www.ubuntu.com](http://www.ubuntu.com)
* \*.ubuntu.com
* ppa.launchpad.net
* launchpad.net
* [www.launchpad.net](http://www.launchpad.net)

#### Entwicklungstools & Plattformen

* dl.k8s.io (Kubernetes)
* pkgs.k8s.io
* k8s.io
* [www.k8s.io](http://www.k8s.io)
* releases.hashicorp.com (HashiCorp)
* apt.releases.hashicorp.com
* rpm.releases.hashicorp.com
* archive.releases.hashicorp.com
* hashicorp.com
* [www.hashicorp.com](http://www.hashicorp.com)
* repo.anaconda.com (Anaconda/Conda)
* conda.anaconda.org
* anaconda.org
* [www.anaconda.com](http://www.anaconda.com)
* anaconda.com
* continuum.io
* apache.org (Apache)
* [www.apache.org](http://www.apache.org)
* archive.apache.org
* downloads.apache.org
* eclipse.org (Eclipse)
* [www.eclipse.org](http://www.eclipse.org)
* download.eclipse.org
* nodejs.org (Node.js)
* [www.nodejs.org](http://www.nodejs.org)

#### Cloud-Services & Überwachung

* statsig.com
* [www.statsig.com](http://www.statsig.com)
* api.statsig.com
* sentry.io
* \*.sentry.io
* http-intake.logs.datadoghq.com
* \*.datadoghq.com
* \*.datadoghq.eu

#### Content Delivery & Mirrors

* sourceforge.net
* \*.sourceforge.net
* packagecloud.io
* \*.packagecloud.io

#### Schema & Konfiguration

* json-schema.org
* [www.json-schema.org](http://www.json-schema.org)
* json.schemastore.org
* [www.schemastore.org](http://www.schemastore.org)

#### Model Context Protocol

* \*.modelcontextprotocol.io

<Note>
  Domains, die mit `*` gekennzeichnet sind, zeigen Wildcard-Subdomain-Matching an. Zum Beispiel erlaubt `*.gcr.io` den Zugriff auf jede Subdomain von `gcr.io`.
</Note>

### Sicherheits-Best-Practices für benutzerdefinierten Netzwerkzugriff

1. **Prinzip der geringsten Berechtigung**: Aktivieren Sie nur den minimalen erforderlichen Netzwerkzugriff
2. **Regelmäßig überprüfen**: Überprüfen Sie zulässige Domains regelmäßig
3. **Verwenden Sie HTTPS**: Bevorzugen Sie immer HTTPS-Endpunkte gegenüber HTTP

## Sicherheit und Isolation

Claude Code im Web bietet starke Sicherheitsgarantien:

* **Isolierte virtuelle Maschinen**: Jede Sitzung wird in einer isolierten, von Anthropic verwalteten VM ausgeführt
* **Netzwerkzugriffskontrolle**: Der Netzwerkzugriff ist standardmäßig begrenzt und kann deaktiviert werden

<Note>
  Wenn Claude Code mit deaktiviertem Netzwerkzugriff ausgeführt wird, darf Claude Code mit der Anthropic API kommunizieren, was möglicherweise immer noch ermöglicht, dass Daten die isolierte Claude Code VM verlassen.
</Note>

* **Schutz von Anmeldedaten**: Sensible Anmeldedaten (wie Git-Anmeldedaten oder Signaturschlüssel) befinden sich niemals in der Sandbox mit Claude Code. Die Authentifizierung wird über einen sicheren Proxy mit Scoped-Credentials verwaltet
* **Sichere Analyse**: Code wird in isolierten VMs analysiert und geändert, bevor PRs erstellt werden

## Preisgestaltung und Ratenlimits

Claude Code im Web teilt Ratenlimits mit allen anderen Claude- und Claude Code-Nutzungen in Ihrem Konto. Das Ausführen mehrerer Aufgaben parallel verbraucht proportional mehr Ratenlimits.

## Einschränkungen

* **Repository-Authentifizierung**: Sie können Sitzungen nur vom Web zum lokalen Computer verschieben, wenn Sie sich bei demselben Konto authentifizieren
* **Plattformbeschränkungen**: Claude Code im Web funktioniert nur mit Code, der in GitHub gehostet wird. Selbstgehostete [GitHub Enterprise Server](/de/github-enterprise-server)-Instanzen werden für Teams- und Enterprise-Pläne unterstützt. GitLab und andere Nicht-GitHub-Repositories können nicht mit Cloud-Sitzungen verwendet werden

## Best Practices

1. **Automatisieren Sie das Umgebungssetup**: Verwenden Sie [Setup-Skripte](#setup-scripts), um Abhängigkeiten zu installieren und Tools zu konfigurieren, bevor Claude Code startet. Für fortgeschrittenere Szenarien konfigurieren Sie [SessionStart-Hooks](/de/hooks#sessionstart).
2. **Dokumentieren Sie Anforderungen**: Geben Sie Abhängigkeiten und Befehle klar in Ihrer `CLAUDE.md`-Datei an. Wenn Sie eine `AGENTS.md`-Datei haben, können Sie sie in Ihrer `CLAUDE.md` mit `@AGENTS.md` sourcing verwenden, um eine einzige Quelle der Wahrheit zu erhalten.

## Verwandte Ressourcen

* [Hooks-Konfiguration](/de/hooks)
* [Einstellungsreferenz](/de/settings)
* [Sicherheit](/de/security)
* [Datennutzung](/de/data-usage)
