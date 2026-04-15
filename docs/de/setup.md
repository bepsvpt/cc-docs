> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Erweiterte Einrichtung

> Systemanforderungen, plattformspezifische Installation, Versionsverwaltung und Deinstallation für Claude Code.

Diese Seite behandelt Systemanforderungen, plattformspezifische Installationsdetails, Updates und Deinstallation. Eine geführte Anleitung für Ihre erste Sitzung finden Sie im [Schnellstart](/de/quickstart). Wenn Sie noch nie ein Terminal verwendet haben, siehe [Terminalanleitung](/de/terminal-guide).

## Systemanforderungen

Claude Code läuft auf den folgenden Plattformen und Konfigurationen:

* **Betriebssystem**:
  * macOS 13.0+
  * Windows 10 1809+ oder Windows Server 2019+
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+
* **Hardware**: 4 GB+ RAM
* **Netzwerk**: Internetverbindung erforderlich. Siehe [Netzwerkkonfiguration](/de/network-config#network-access-requirements).
* **Shell**: Bash, Zsh, PowerShell oder CMD. Unter Windows ist [Git für Windows](https://git-scm.com/downloads/win) erforderlich.
* **Standort**: [Von Anthropic unterstützte Länder](https://www.anthropic.com/supported-countries)

### Zusätzliche Abhängigkeiten

* **ripgrep**: normalerweise in Claude Code enthalten. Falls die Suche fehlschlägt, siehe [Suche-Fehlerbehebung](/de/troubleshooting#search-and-discovery-issues).

## Claude Code installieren

<Tip>
  Bevorzugen Sie eine grafische Benutzeroberfläche? Die [Desktop-App](/de/desktop-quickstart) ermöglicht es Ihnen, Claude Code ohne das Terminal zu verwenden. Laden Sie sie für [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) oder [Windows](https://claude.com/download?utm_source=claude_code\&utm_medium=docs) herunter.

  Neu im Terminal? Siehe die [Terminalanleitung](/de/terminal-guide) für Schritt-für-Schritt-Anweisungen.
</Tip>

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. If you see `'irm' is not recognized as an internal or external command`, you're in CMD, not PowerShell. Your prompt shows `PS C:\` when you're in PowerShell and `C:\` without the `PS` when you're in CMD.

    **Native Windows setups require [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it. WSL setups do not need it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash theme={null}
    brew install --cask claude-code
    ```

    Homebrew offers two casks. `claude-code` tracks the stable release channel, which is typically about a week behind and skips releases with major regressions. `claude-code@latest` tracks the latest channel and receives new versions as soon as they ship.

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` or `brew upgrade claude-code@latest`, depending on which cask you installed, to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

Nach Abschluss der Installation öffnen Sie ein Terminal in dem Projekt, an dem Sie arbeiten möchten, und starten Sie Claude Code:

```bash theme={null}
claude
```

Wenn während der Installation Probleme auftreten, siehe [Fehlerbehebungsanleitung](/de/troubleshooting).

### Einrichtung unter Windows

Claude Code unter Windows erfordert [Git für Windows](https://git-scm.com/downloads/win) oder WSL. Sie können `claude` von PowerShell, CMD oder Git Bash aus starten. Claude Code verwendet Git Bash intern, um Befehle auszuführen. Sie müssen PowerShell nicht als Administrator ausführen.

**Option 1: Natives Windows mit Git Bash**

Installieren Sie [Git für Windows](https://git-scm.com/downloads/win), und führen Sie dann den Installationsbefehl von PowerShell oder CMD aus.

Wenn Claude Code Ihre Git Bash-Installation nicht finden kann, legen Sie den Pfad in Ihrer [settings.json-Datei](/de/settings) fest:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

Claude Code kann auch PowerShell nativ unter Windows als Opt-in-Vorschau ausführen. Siehe [PowerShell-Tool](/de/tools-reference#powershell-tool) für Einrichtung und Einschränkungen.

**Option 2: WSL**

Sowohl WSL 1 als auch WSL 2 werden unterstützt. WSL 2 unterstützt [Sandboxing](/de/sandboxing) für erhöhte Sicherheit. WSL 1 unterstützt kein Sandboxing.

### Alpine Linux und musl-basierte Distributionen

Das native Installationsprogramm auf Alpine und anderen musl/uClibc-basierten Distributionen erfordert `libgcc`, `libstdc++` und `ripgrep`. Installieren Sie diese mit dem Paketmanager Ihrer Distribution, und setzen Sie dann `USE_BUILTIN_RIPGREP=0`.

Dieses Beispiel installiert die erforderlichen Pakete auf Alpine:

```bash theme={null}
apk add libgcc libstdc++ ripgrep
```

Setzen Sie dann `USE_BUILTIN_RIPGREP` auf `0` in Ihrer [`settings.json`](/de/settings#available-settings)-Datei:

```json theme={null}
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

## Installation überprüfen

Nach der Installation bestätigen Sie, dass Claude Code funktioniert:

```bash theme={null}
claude --version
```

Für eine detailliertere Überprüfung Ihrer Installation und Konfiguration führen Sie [`claude doctor`](/de/troubleshooting#get-more-help) aus:

```bash theme={null}
claude doctor
```

## Authentifizierung

Claude Code erfordert ein Pro-, Max-, Teams-, Enterprise- oder Console-Konto. Der kostenlose Claude.ai-Plan beinhaltet keinen Claude Code-Zugriff. Sie können Claude Code auch mit einem Drittanbieter-API-Provider wie [Amazon Bedrock](/de/amazon-bedrock), [Google Vertex AI](/de/google-vertex-ai) oder [Microsoft Foundry](/de/microsoft-foundry) verwenden.

Nach der Installation melden Sie sich an, indem Sie `claude` ausführen und den Browser-Aufforderungen folgen. Siehe [Authentifizierung](/de/authentication) für alle Kontotypen und Team-Setup-Optionen.

## Claude Code aktualisieren

Native Installationen werden automatisch im Hintergrund aktualisiert. Sie können [den Release-Kanal konfigurieren](#configure-release-channel), um zu steuern, ob Sie Updates sofort oder nach einem verzögerten stabilen Zeitplan erhalten, oder [Auto-Updates vollständig deaktivieren](#disable-auto-updates). Homebrew- und WinGet-Installationen erfordern manuelle Updates.

### Auto-Updates

Claude Code prüft beim Start und regelmäßig während der Ausführung auf Updates. Updates werden im Hintergrund heruntergeladen und installiert und treten beim nächsten Start von Claude Code in Kraft.

<Note>
  Homebrew- und WinGet-Installationen werden nicht automatisch aktualisiert. Verwenden Sie `brew upgrade claude-code` oder `winget upgrade Anthropic.ClaudeCode`, um manuell zu aktualisieren.

  **Bekanntes Problem:** Claude Code kann Sie über Updates benachrichtigen, bevor die neue Version in diesen Paketmanagern verfügbar ist. Wenn ein Upgrade fehlschlägt, warten Sie und versuchen Sie es später erneut.

  Homebrew behält alte Versionen nach Upgrades auf der Festplatte. Führen Sie regelmäßig `brew cleanup claude-code` aus, um Speicherplatz freizugeben.
</Note>

### Release-Kanal konfigurieren

Steuern Sie, welchem Release-Kanal Claude Code für Auto-Updates und `claude update` folgt, mit der Einstellung `autoUpdatesChannel`:

* `"latest"`, die Standardeinstellung: Erhalten Sie neue Funktionen, sobald sie veröffentlicht werden
* `"stable"`: Verwenden Sie eine Version, die normalerweise etwa eine Woche alt ist und überspringen Sie Releases mit großen Regressionen

Konfigurieren Sie dies über `/config` → **Auto-update channel**, oder fügen Sie es zu Ihrer [settings.json-Datei](/de/settings) hinzu:

```json theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Für Enterprise-Bereitstellungen können Sie einen konsistenten Release-Kanal in Ihrer Organisation mit [verwalteten Einstellungen](/de/permissions#managed-settings) erzwingen.

### Auto-Updates deaktivieren

Setzen Sie `DISABLE_AUTOUPDATER` auf `"1"` im `env`-Schlüssel Ihrer [`settings.json`](/de/settings#available-settings)-Datei:

```json theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

### Manuell aktualisieren

Um ein Update sofort anzuwenden, ohne auf die nächste Hintergrundprüfung zu warten, führen Sie aus:

```bash theme={null}
claude update
```

## Erweiterte Installationsoptionen

Diese Optionen sind für Versions-Pinning, Migration von npm und Überprüfung der Binärintegrität.

### Eine bestimmte Version installieren

Das native Installationsprogramm akzeptiert entweder eine bestimmte Versionsnummer oder einen Release-Kanal (`latest` oder `stable`). Der Kanal, den Sie bei der Installation wählen, wird zu Ihrem Standard für Auto-Updates. Siehe [Release-Kanal konfigurieren](#configure-release-channel) für weitere Informationen.

So installieren Sie die neueste Version (Standard):

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
  </Tab>
</Tabs>

So installieren Sie die stabile Version:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s stable
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
    ```
  </Tab>
</Tabs>

So installieren Sie eine bestimmte Versionsnummer:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 2.1.89
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 2.1.89 && del install.cmd
    ```
  </Tab>
</Tabs>

### Veraltete npm-Installation

Die npm-Installation ist veraltet. Das native Installationsprogramm ist schneller, erfordert keine Abhängigkeiten und wird automatisch im Hintergrund aktualisiert. Verwenden Sie die [native Installationsmethode](#install-claude-code), wenn möglich.

#### Von npm zu nativ migrieren

Wenn Sie Claude Code zuvor mit npm installiert haben, wechseln Sie zum nativen Installationsprogramm:

```bash theme={null}
# Installieren Sie die native Binärdatei
curl -fsSL https://claude.ai/install.sh | bash

# Entfernen Sie die alte npm-Installation
npm uninstall -g @anthropic-ai/claude-code
```

Sie können auch `claude install` aus einer bestehenden npm-Installation ausführen, um die native Binärdatei neben ihr zu installieren, und dann die npm-Version entfernen.

#### Mit npm installieren

Wenn Sie die npm-Installation aus Kompatibilitätsgründen benötigen, müssen Sie [Node.js 18+](https://nodejs.org/en/download) installiert haben. Installieren Sie das Paket global:

```bash theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  Verwenden Sie NICHT `sudo npm install -g`, da dies zu Berechtigungsproblemen und Sicherheitsrisiken führen kann. Wenn Sie auf Berechtigungsfehler stoßen, siehe [Fehlerbehebung bei Berechtigungsfehlern](/de/troubleshooting#permission-errors-during-installation).
</Warning>

### Binärintegrität und Code-Signierung

Jede Veröffentlichung veröffentlicht eine `manifest.json`, die SHA256-Checksummen für jede Plattform-Binärdatei enthält. Das Manifest ist mit einem Anthropic GPG-Schlüssel signiert, daher überprüft die Überprüfung der Signatur auf dem Manifest transitiv jede Binärdatei, die es auflistet.

#### Manifest-Signatur überprüfen

Die Schritte 1-3 erfordern eine POSIX-Shell mit `gpg` und `curl`. Unter Windows führen Sie sie in Git Bash oder WSL aus. Schritt 4 enthält eine PowerShell-Option.

<Steps>
  <Step title="Laden Sie den öffentlichen Schlüssel herunter und importieren Sie ihn">
    Der Release-Signaturschlüssel wird unter einer festen URL veröffentlicht.

    ```bash theme={null}
    curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import
    ```

    Zeigen Sie den Fingerabdruck des importierten Schlüssels an.

    ```bash theme={null}
    gpg --fingerprint security@anthropic.com
    ```

    Bestätigen Sie, dass die Ausgabe diesen Fingerabdruck enthält:

    ```text theme={null}
    31DD DE24 DDFA B679 F42D  7BD2 BAA9 29FF 1A7E CACE
    ```
  </Step>

  <Step title="Laden Sie das Manifest und die Signatur herunter">
    Setzen Sie `VERSION` auf die Veröffentlichung, die Sie überprüfen möchten.

    ```bash theme={null}
    REPO=https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases
    VERSION=2.1.89
    curl -fsSLO "$REPO/$VERSION/manifest.json"
    curl -fsSLO "$REPO/$VERSION/manifest.json.sig"
    ```
  </Step>

  <Step title="Überprüfen Sie die Signatur">
    Überprüfen Sie die abgelöste Signatur gegen das Manifest.

    ```bash theme={null}
    gpg --verify manifest.json.sig manifest.json
    ```

    Ein gültiges Ergebnis meldet `Good signature from "Anthropic Claude Code Release Signing <security@anthropic.com>"`.

    `gpg` druckt auch `WARNING: This key is not certified with a trusted signature!` für jeden neu importierten Schlüssel. Dies ist zu erwarten. Die Zeile `Good signature` bestätigt, dass die kryptografische Überprüfung bestanden wurde. Der Fingerabdruckvergleich in Schritt 1 bestätigt, dass der Schlüssel selbst authentisch ist.
  </Step>

  <Step title="Überprüfen Sie die Binärdatei gegen das Manifest">
    Vergleichen Sie die SHA256-Prüfsumme Ihrer heruntergeladenen Binärdatei mit dem Wert, der unter `platforms.<platform>.checksum` in `manifest.json` aufgelistet ist.

    <Tabs>
      <Tab title="Linux">
        ```bash theme={null}
        sha256sum claude
        ```
      </Tab>

      <Tab title="macOS">
        ```bash theme={null}
        shasum -a 256 claude
        ```
      </Tab>

      <Tab title="Windows PowerShell">
        ```powershell theme={null}
        (Get-FileHash claude.exe -Algorithm SHA256).Hash.ToLower()
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>

<Note>
  Manifest-Signaturen sind für Veröffentlichungen ab `2.1.89` verfügbar. Frühere Veröffentlichungen veröffentlichen Checksummen in `manifest.json` ohne abgelöste Signatur.
</Note>

#### Plattform-Code-Signaturen

Zusätzlich zum signierten Manifest tragen einzelne Binärdateien plattformspezifische Code-Signaturen, wo unterstützt.

* **macOS**: signiert von „Anthropic PBC" und beglaubigt von Apple. Überprüfen Sie mit `codesign --verify --verbose ./claude`.
* **Windows**: signiert von „Anthropic, PBC". Überprüfen Sie mit `Get-AuthenticodeSignature .\claude.exe`.
* **Linux**: verwenden Sie die Manifest-Signatur oben, um die Integrität zu überprüfen. Linux-Binärdateien sind nicht einzeln code-signiert.

## Claude Code deinstallieren

Um Claude Code zu entfernen, folgen Sie den Anweisungen für Ihre Installationsmethode.

### Native Installation

Entfernen Sie die Claude Code-Binärdatei und Versionsdateien:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    rm -f ~/.local/bin/claude
    rm -rf ~/.local/share/claude
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
    Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
    ```
  </Tab>
</Tabs>

### Homebrew-Installation

Entfernen Sie das Homebrew-Cask:

```bash theme={null}
brew uninstall --cask claude-code
```

### WinGet-Installation

Entfernen Sie das WinGet-Paket:

```powershell theme={null}
winget uninstall Anthropic.ClaudeCode
```

### npm

Entfernen Sie das globale npm-Paket:

```bash theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Konfigurationsdateien entfernen

<Warning>
  Das Entfernen von Konfigurationsdateien löscht alle Ihre Einstellungen, zulässigen Tools, MCP-Serverkonfigurationen und Sitzungsverlauf.
</Warning>

So entfernen Sie Claude Code-Einstellungen und zwischengespeicherte Daten:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    # Entfernen Sie Benutzereinstellungen und Status
    rm -rf ~/.claude
    rm ~/.claude.json

    # Entfernen Sie projektspezifische Einstellungen (führen Sie dies aus Ihrem Projektverzeichnis aus)
    rm -rf .claude
    rm -f .mcp.json
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    # Entfernen Sie Benutzereinstellungen und Status
    Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
    Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

    # Entfernen Sie projektspezifische Einstellungen (führen Sie dies aus Ihrem Projektverzeichnis aus)
    Remove-Item -Path ".claude" -Recurse -Force
    Remove-Item -Path ".mcp.json" -Force
    ```
  </Tab>
</Tabs>
