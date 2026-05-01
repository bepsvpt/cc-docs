> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# JetBrains IDEs

> Verwenden Sie Claude Code mit JetBrains IDEs einschließlich IntelliJ, PyCharm, WebStorm und mehr

Claude Code integriert sich mit JetBrains IDEs durch ein dediziertes Plugin und bietet Funktionen wie interaktive Diff-Anzeige, Freigabe von Auswahlkontext und mehr.

## Unterstützte IDEs

Das Claude Code Plugin funktioniert mit den meisten JetBrains IDEs, einschließlich:

* IntelliJ IDEA
* PyCharm
* Android Studio
* WebStorm
* PhpStorm
* GoLand

## Funktionen

* **Schnellstart**: Verwenden Sie `Cmd+Esc` (Mac) oder `Ctrl+Esc` (Windows/Linux), um Claude Code direkt aus Ihrem Editor zu öffnen, oder klicken Sie auf die Claude Code Schaltfläche in der Benutzeroberfläche
* **Diff-Anzeige**: Code-Änderungen können direkt im IDE Diff-Viewer anstelle des Terminals angezeigt werden
* **Auswahlkontext**: Die aktuelle Auswahl oder der aktuelle Tab in der IDE wird automatisch mit Claude Code geteilt
* **Dateireferenz-Verknüpfungen**: Verwenden Sie `Cmd+Option+K` (Mac) oder `Alt+Ctrl+K` (Linux/Windows), um Dateireferenzen wie `@src/auth.ts#L1-99` einzufügen
* **Diagnose-Freigabe**: Diagnosefehler aus der IDE, wie Lint- und Syntaxfehler, werden automatisch mit Claude geteilt, während Sie arbeiten

## Installation

### Marketplace-Installation

Suchen Sie das [Claude Code Plugin](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) im JetBrains Marketplace und installieren Sie es, dann starten Sie Ihre IDE neu.

Falls Sie Claude Code noch nicht installiert haben, lesen Sie den [Schnellstart-Leitfaden](/de/quickstart) für Installationsanweisungen.

<Note>
  Nach der Installation des Plugins müssen Sie Ihre IDE möglicherweise vollständig neu starten, damit es wirksam wird.
</Note>

## Verwendung

### Aus Ihrer IDE

Führen Sie `claude` aus dem integrierten Terminal Ihrer IDE aus, und alle Integrationsfunktionen sind aktiv.

### Aus externen Terminals

Verwenden Sie den `/ide` Befehl in einem beliebigen externen Terminal, um Claude Code mit Ihrer JetBrains IDE zu verbinden und alle Funktionen zu aktivieren:

```bash theme={null}
claude
```

```text theme={null}
/ide
```

Wenn Sie möchten, dass Claude Zugriff auf die gleichen Dateien wie Ihre IDE hat, starten Sie Claude Code aus dem gleichen Verzeichnis wie Ihr IDE-Projektstammverzeichnis.

## Konfiguration

### Claude Code Einstellungen

Konfigurieren Sie die IDE-Integration durch Claude Code Einstellungen:

1. Führen Sie `claude` aus
2. Geben Sie den `/config` Befehl ein
3. Stellen Sie das Diff-Tool auf `auto` ein, um Diffs in der IDE anzuzeigen, oder auf `terminal`, um sie im Terminal zu behalten

### Plugin-Einstellungen

Konfigurieren Sie das Claude Code Plugin, indem Sie zu **Einstellungen → Tools → Claude Code \[Beta]** gehen:

#### Allgemeine Einstellungen

* **Claude Befehl**: Geben Sie einen benutzerdefinierten Befehl an, um Claude auszuführen, zum Beispiel `claude`, `/usr/local/bin/claude` oder `npx @anthropic-ai/claude-code`
* **Benachrichtigung für Claude-Befehl nicht gefunden unterdrücken**: Überspringen Sie Benachrichtigungen über das Nichtfinden des Claude-Befehls
* **Option+Enter für mehrzeilige Eingabeaufforderungen aktivieren**: Nur auf macOS. Wenn aktiviert, fügt Option+Enter neue Zeilen in Claude Code Eingabeaufforderungen ein. Deaktivieren Sie dies, wenn die Option-Taste unerwartet erfasst wird. Erfordert einen Terminal-Neustart.
* **Automatische Updates aktivieren**: Automatisch nach Plugin-Updates suchen und diese installieren, angewendet beim Neustart

<Tip>
  Für WSL-Benutzer: Stellen Sie `wsl -d Ubuntu -- bash -lic "claude"` als Ihren Claude-Befehl ein (ersetzen Sie `Ubuntu` durch Ihren WSL-Distributionsnamen)
</Tip>

#### ESC-Taste Konfiguration

Wenn die ESC-Taste Claude Code Operationen in JetBrains Terminals nicht unterbricht:

1. Gehen Sie zu **Einstellungen → Tools → Terminal**
2. Entweder:
   * Deaktivieren Sie „Fokus mit Escape zum Editor verschieben", oder
   * Klicken Sie auf „Terminal-Tastenkombinationen konfigurieren" und löschen Sie die Verknüpfung „Fokus zum Editor wechseln"
3. Wenden Sie die Änderungen an

Dies ermöglicht es der ESC-Taste, Claude Code Operationen ordnungsgemäß zu unterbrechen.

## Spezielle Konfigurationen

### Remote-Entwicklung

<Warning>
  Bei Verwendung von JetBrains Remote Development müssen Sie das Plugin auf dem Remote-Host über **Einstellungen → Plugin (Host)** installieren.
</Warning>

Das Plugin muss auf dem Remote-Host installiert werden, nicht auf Ihrem lokalen Client-Computer.

### WSL-Konfiguration

Wenn Sie Claude Code auf WSL2 mit einer JetBrains IDE verwenden und „Keine verfügbaren IDEs erkannt" sehen, ist die Ursache normalerweise WSL2s NAT-Netzwerk oder die Windows Firewall, die die Verbindung zwischen WSL2 und der IDE blockiert, die auf dem Windows-Host ausgeführt wird. WSL1 verwendet das Netzwerk des Hosts direkt und ist nicht betroffen.

#### WSL2-Datenverkehr durch Windows Firewall zulassen

Dies ist die empfohlene Lösung, da sie Ihren vorhandenen WSL2-Netzwerkmodus beibehält.

<Steps>
  <Step title="Finden Sie Ihre WSL2 IP-Adresse">
    Führen Sie in Ihrer WSL-Shell Folgendes aus:

    ```bash theme={null}
    hostname -I
    ```

    Notieren Sie sich das Subnetz, zum Beispiel `172.21.123.45` befindet sich in `172.21.0.0/16`.
  </Step>

  <Step title="Erstellen Sie eine Firewall-Regel">
    Öffnen Sie PowerShell als Administrator und führen Sie Folgendes aus, passen Sie den IP-Bereich an Ihr Subnetz an:

    ```powershell theme={null}
    New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
    ```
  </Step>

  <Step title="Starten Sie Ihre IDE und Claude Code neu">
    Schließen Sie beide und öffnen Sie sie erneut, damit die neue Regel wirksam wird.
  </Step>
</Steps>

#### Wechseln Sie WSL2 zu gespiegeltem Netzwerk

Gespiegeltes Netzwerk erfordert Windows 11 22H2 oder später. Wenn Sie Windows 10 verwenden, verwenden Sie stattdessen die Firewall-Regel oben.

Fügen Sie dies zu `.wslconfig` in Ihrem Windows-Benutzerverzeichnis hinzu:

```ini theme={null}
[wsl2]
networkingMode=mirrored
```

Starten Sie dann WSL mit `wsl --shutdown` von PowerShell neu.

## Troubleshooting

### Plugin funktioniert nicht

Wenn das Plugin installiert ist, aber Claude Code Funktionen nicht in Ihrer IDE angezeigt werden:

* Stellen Sie sicher, dass Sie Claude Code aus dem Projektstammverzeichnis ausführen
* Überprüfen Sie, dass das JetBrains Plugin in den IDE-Einstellungen aktiviert ist
* Starten Sie die IDE vollständig neu (möglicherweise müssen Sie dies mehrmals tun)
* Stellen Sie für Remote Development sicher, dass das Plugin auf dem Remote-Host installiert ist

### IDE nicht erkannt

Wenn das Ausführen von `claude` 'Keine verfügbaren IDEs erkannt" anzeigt:

* Überprüfen Sie, dass das Plugin installiert und aktiviert ist
* Starten Sie die IDE vollständig neu
* Überprüfen Sie, dass Sie Claude Code aus dem integrierten Terminal ausführen
* Für WSL-Benutzer lesen Sie [WSL-Konfiguration](#wsl-konfiguration) oben

### Befehl nicht gefunden

Wenn das Klicken auf das Claude-Symbol „Befehl nicht gefunden" anzeigt:

1. Überprüfen Sie, dass Claude Code installiert ist, indem Sie `claude --version` in einem Terminal ausführen
2. Konfigurieren Sie den Claude-Befehlspfad in den Plugin-Einstellungen
3. Für WSL-Benutzer verwenden Sie das WSL-Befehlsformat, das im Konfigurationsabschnitt erwähnt wird

## Sicherheitsaspekte

Wenn Claude Code in einer JetBrains IDE mit aktivierten Auto-Edit-Berechtigungen ausgeführt wird, kann es möglicherweise IDE-Konfigurationsdateien ändern, die automatisch von Ihrer IDE ausgeführt werden können. Dies kann das Risiko der Ausführung von Claude Code im Auto-Edit-Modus erhöhen und es ermöglichen, Claude Code Berechtigungsaufforderungen für die Bash-Ausführung zu umgehen.

Bei der Ausführung in JetBrains IDEs sollten Sie Folgendes beachten:

* Verwenden Sie den manuellen Genehmigungsmodus für Bearbeitungen
* Achten Sie besonders darauf, dass Claude nur mit vertrauenswürdigen Eingabeaufforderungen verwendet wird
* Seien Sie sich bewusst, welche Dateien Claude Code ändern kann

Für Claude Code Installations- oder Anmeldeprobleme außerhalb der IDE lesen Sie [Troubleshoot installation and login](/de/troubleshoot-install).
