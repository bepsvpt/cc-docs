> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code einrichten

> Installieren, authentifizieren und beginnen Sie mit der Verwendung von Claude Code auf Ihrem Entwicklungscomputer.

## Systemanforderungen

* **Betriebssystem**:
  * macOS 13.0+
  * Windows 10 1809+ oder Windows Server 2019+ ([siehe Setuphinweise](#platform-specific-setup))
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+ ([zusätzliche Abhängigkeiten erforderlich](#platform-specific-setup))
* **Hardware**: 4 GB+ RAM
* **Netzwerk**: Internetverbindung erforderlich (siehe [Netzwerkkonfiguration](/de/network-config#network-access-requirements))
* **Shell**: Funktioniert am besten in Bash oder Zsh
* **Standort**: [Von Anthropic unterstützte Länder](https://www.anthropic.com/supported-countries)

### Zusätzliche Abhängigkeiten

* **ripgrep**: Normalerweise in Claude Code enthalten. Falls die Suche fehlschlägt, siehe [Suche-Fehlerbehebung](/de/troubleshooting#search-and-discovery-issues).
* **[Node.js 18+](https://nodejs.org/en/download)**: Nur erforderlich für [veraltete npm-Installation](#npm-installation-deprecated)

## Installation

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell  theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

Nach Abschluss des Installationsvorgangs navigieren Sie zu Ihrem Projekt und starten Claude Code:

```bash  theme={null}
cd your-awesome-project
claude
```

Wenn während der Installation Probleme auftreten, konsultieren Sie das [Fehlerbehebungshandbuch](/de/troubleshooting).

<Tip>
  Führen Sie `claude doctor` nach der Installation aus, um Ihren Installationstyp und die Version zu überprüfen.
</Tip>

### Plattformspezifisches Setup

**Windows**: Führen Sie Claude Code nativ aus (erfordert [Git Bash](https://git-scm.com/downloads/win)) oder innerhalb von WSL. Sowohl WSL 1 als auch WSL 2 werden unterstützt, aber WSL 1 hat begrenzte Unterstützung und unterstützt keine Funktionen wie Bash-Tool-Sandboxing.

**Alpine Linux und andere musl/uClibc-basierte Distributionen**:

Das native Installationsprogramm auf Alpine und anderen musl/uClibc-basierten Distributionen erfordert `libgcc`, `libstdc++` und `ripgrep`. Installieren Sie diese mit dem Paketmanager Ihrer Distribution und setzen Sie dann `USE_BUILTIN_RIPGREP=0`.

Auf Alpine:

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

### Authentifizierung

#### Für Einzelpersonen

1. **Claude Pro oder Max Plan** (empfohlen): Abonnieren Sie Claude's [Pro oder Max Plan](https://claude.ai/pricing) für ein einheitliches Abonnement, das sowohl Claude Code als auch Claude im Web umfasst. Verwalten Sie Ihr Konto an einem Ort und melden Sie sich mit Ihrem Claude.ai-Konto an.
2. **Claude Console**: Verbinden Sie sich über die [Claude Console](https://console.anthropic.com) und schließen Sie den OAuth-Prozess ab. Erfordert aktive Abrechnung in der Anthropic Console. Ein „Claude Code"-Arbeitsbereich wird automatisch für Nutzungsverfolgung und Kostenverwaltung erstellt. Sie können keine API-Schlüssel für den Claude Code-Arbeitsbereich erstellen; er ist ausschließlich für die Claude Code-Nutzung vorgesehen.

#### Für Teams und Organisationen

1. **Claude for Teams oder Enterprise** (empfohlen): Abonnieren Sie [Claude for Teams](https://claude.com/pricing#team-&-enterprise) oder [Claude for Enterprise](https://anthropic.com/contact-sales) für zentrale Abrechnung, Teamverwaltung und Zugriff auf sowohl Claude Code als auch Claude im Web. Teammitglieder melden sich mit ihren Claude.ai-Konten an.
2. **Claude Console mit Team-Abrechnung**: Richten Sie eine gemeinsame [Claude Console](https://console.anthropic.com)-Organisation mit Team-Abrechnung ein. Laden Sie Teammitglieder ein und weisen Sie Rollen für die Nutzungsverfolgung zu.
3. **Cloud-Anbieter**: Konfigurieren Sie Claude Code für die Verwendung von [Amazon Bedrock, Google Vertex AI oder Microsoft Foundry](/de/third-party-integrations) für Bereitstellungen mit Ihrer vorhandenen Cloud-Infrastruktur.

### Installieren Sie eine bestimmte Version

Das native Installationsprogramm akzeptiert entweder eine spezifische Versionsnummer oder einen Release-Kanal (`latest` oder `stable`). Der Kanal, den Sie bei der Installation wählen, wird zu Ihrem Standard für automatische Updates. Weitere Informationen finden Sie unter [Release-Kanal konfigurieren](#configure-release-channel).

So installieren Sie die neueste Version (Standard):

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
  </Tab>
</Tabs>

So installieren Sie die stabile Version:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s stable
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
    ```
  </Tab>
</Tabs>

So installieren Sie eine bestimmte Versionsnummer:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 1.0.58 && del install.cmd
    ```
  </Tab>
</Tabs>

### Binäre Integrität und Code-Signierung

* SHA256-Checksummen für alle Plattformen werden in den Release-Manifesten veröffentlicht, die sich derzeit unter `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json` befinden (Beispiel: ersetzen Sie `{VERSION}` durch `2.0.30`)
* Signierte Binärdateien werden für die folgenden Plattformen verteilt:
  * macOS: Signiert von 'Anthropic PBC" und von Apple beglaubigt
  * Windows: Signiert von „Anthropic, PBC"

## NPM-Installation (veraltet)

Die NPM-Installation ist veraltet. Verwenden Sie die [native Installationsmethode](#installation), wenn möglich. Um eine vorhandene npm-Installation zu einer nativen zu migrieren, führen Sie `claude install` aus.

**Globale npm-Installation**

```sh  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  Verwenden Sie NICHT `sudo npm install -g`, da dies zu Berechtigungsproblemen und Sicherheitsrisiken führen kann.
  Wenn Sie auf Berechtigungsfehler stoßen, siehe [Fehlerbehebung bei Berechtigungsfehlern](/de/troubleshooting#command-not-found-claude-or-permission-errors) für empfohlene Lösungen.
</Warning>

## Windows-Setup

**Option 1: Claude Code innerhalb von WSL**

* Sowohl WSL 1 als auch WSL 2 werden unterstützt
* WSL 2 unterstützt [Sandboxing](/de/sandboxing) für erhöhte Sicherheit. WSL 1 unterstützt kein Sandboxing.

**Option 2: Claude Code auf nativem Windows mit Git Bash**

* Erfordert [Git für Windows](https://git-scm.com/downloads/win)
* Für tragbare Git-Installationen geben Sie den Pfad zu Ihrer `bash.exe` an:
  ```powershell  theme={null}
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Claude Code aktualisieren

### Automatische Updates

Claude Code aktualisiert sich automatisch, um sicherzustellen, dass Sie die neuesten Funktionen und Sicherheitspatches haben.

* **Update-Überprüfungen**: Werden beim Start und regelmäßig während der Ausführung durchgeführt
* **Update-Prozess**: Downloads und Installationen erfolgen automatisch im Hintergrund
* **Benachrichtigungen**: Sie sehen eine Benachrichtigung, wenn Updates installiert werden
* **Updates anwenden**: Updates werden beim nächsten Start von Claude Code wirksam

<Note>
  Homebrew- und WinGet-Installationen werden nicht automatisch aktualisiert. Verwenden Sie `brew upgrade claude-code` oder `winget upgrade Anthropic.ClaudeCode`, um manuell zu aktualisieren.

  **Bekanntes Problem:** Claude Code kann Sie über Updates benachrichtigen, bevor die neue Version in diesen Paketmanagern verfügbar ist. Wenn ein Upgrade fehlschlägt, warten Sie und versuchen Sie es später erneut.
</Note>

### Release-Kanal konfigurieren

Konfigurieren Sie, welchen Release-Kanal Claude Code für automatische Updates und `claude update` mit der Einstellung `autoUpdatesChannel` folgt:

* `"latest"` (Standard): Erhalten Sie neue Funktionen, sobald sie veröffentlicht werden
* `"stable"`: Verwenden Sie eine Version, die typischerweise etwa eine Woche alt ist und überspringen Sie Releases mit großen Regressionen

Konfigurieren Sie dies über `/config` → **Auto-update channel**, oder fügen Sie es zu Ihrer [settings.json-Datei](/de/settings) hinzu:

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Für Enterprise-Bereitstellungen können Sie einen konsistenten Release-Kanal in Ihrer Organisation mit [verwalteten Einstellungen](/de/settings#settings-files) erzwingen.

### Automatische Updates deaktivieren

Setzen Sie die Umgebungsvariable `DISABLE_AUTOUPDATER` in Ihrer Shell oder [settings.json-Datei](/de/settings):

```bash  theme={null}
export DISABLE_AUTOUPDATER=1
```

### Manuell aktualisieren

```bash  theme={null}
claude update
```

## Claude Code deinstallieren

Wenn Sie Claude Code deinstallieren müssen, folgen Sie den Anweisungen für Ihre Installationsmethode.

### Native Installation

Entfernen Sie die Claude Code-Binärdatei und Versionsdateien:

**macOS, Linux, WSL:**

```bash  theme={null}
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```

**Windows PowerShell:**

```powershell  theme={null}
Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
```

**Windows CMD:**

```batch  theme={null}
del "%USERPROFILE%\.local\bin\claude.exe"
rmdir /s /q "%USERPROFILE%\.local\share\claude"
```

### Homebrew-Installation

```bash  theme={null}
brew uninstall --cask claude-code
```

### WinGet-Installation

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### NPM-Installation

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Konfigurationsdateien bereinigen (optional)

<Warning>
  Das Entfernen von Konfigurationsdateien löscht alle Ihre Einstellungen, zulässigen Tools, MCP-Serverkonfigurationen und Sitzungsverlauf.
</Warning>

So entfernen Sie Claude Code-Einstellungen und zwischengespeicherte Daten:

**macOS, Linux, WSL:**

```bash  theme={null}
# Benutzereinstellungen und Status entfernen
rm -rf ~/.claude
rm ~/.claude.json

# Projektspezifische Einstellungen entfernen (führen Sie dies aus Ihrem Projektverzeichnis aus)
rm -rf .claude
rm -f .mcp.json
```

**Windows PowerShell:**

```powershell  theme={null}
# Benutzereinstellungen und Status entfernen
Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

# Projektspezifische Einstellungen entfernen (führen Sie dies aus Ihrem Projektverzeichnis aus)
Remove-Item -Path ".claude" -Recurse -Force
Remove-Item -Path ".mcp.json" -Force
```

**Windows CMD:**

```batch  theme={null}
REM Benutzereinstellungen und Status entfernen
rmdir /s /q "%USERPROFILE%\.claude"
del "%USERPROFILE%\.claude.json"

REM Projektspezifische Einstellungen entfernen (führen Sie dies aus Ihrem Projektverzeichnis aus)
rmdir /s /q ".claude"
del ".mcp.json"
```
