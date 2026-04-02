> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurazione avanzata

> Requisiti di sistema, installazione specifica per piattaforma, gestione delle versioni e disinstallazione per Claude Code.

Questa pagina copre i requisiti di sistema, i dettagli di installazione specifici per piattaforma, gli aggiornamenti e la disinstallazione. Per una procedura guidata della vostra prima sessione, consultate la [guida rapida](/it/quickstart). Se non avete mai utilizzato un terminale prima, consultate la [guida del terminale](/it/terminal-guide).

## Requisiti di sistema

Claude Code funziona sulle seguenti piattaforme e configurazioni:

* **Sistema operativo**:
  * macOS 13.0+
  * Windows 10 1809+ o Windows Server 2019+
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+
* **Hardware**: 4 GB+ di RAM
* **Rete**: connessione a Internet richiesta. Consultate la [configurazione di rete](/it/network-config#network-access-requirements).
* **Shell**: Bash, Zsh, PowerShell o CMD. Su Windows, è richiesto [Git for Windows](https://git-scm.com/downloads/win).
* **Posizione**: [paesi supportati da Anthropic](https://www.anthropic.com/supported-countries)

### Dipendenze aggiuntive

* **ripgrep**: solitamente incluso con Claude Code. Se la ricerca non funziona, consultate la [risoluzione dei problemi di ricerca](/it/troubleshooting#search-and-discovery-issues).

## Installare Claude Code

<Tip>
  Preferite un'interfaccia grafica? L'[app Desktop](/it/desktop-quickstart) vi consente di utilizzare Claude Code senza il terminale. Scaricatela per [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) o [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs).

  Siete nuovi al terminale? Consultate la [guida del terminale](/it/terminal-guide) per istruzioni passo dopo passo.
</Tip>

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

    If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. Use the PowerShell command above instead. Your prompt shows `PS C:\` when you're in PowerShell.

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

Dopo il completamento dell'installazione, aprite un terminale nel progetto su cui desiderate lavorare e avviate Claude Code:

```bash  theme={null}
claude
```

Se riscontrate problemi durante l'installazione, consultate la [guida alla risoluzione dei problemi](/it/troubleshooting).

### Configurazione su Windows

Claude Code su Windows richiede [Git for Windows](https://git-scm.com/downloads/win) o WSL. Potete avviare `claude` da PowerShell, CMD o Git Bash. Claude Code utilizza Git Bash internamente per eseguire i comandi. Non è necessario eseguire PowerShell come Amministratore.

**Opzione 1: Windows nativo con Git Bash**

Installate [Git for Windows](https://git-scm.com/downloads/win), quindi eseguite il comando di installazione da PowerShell o CMD.

Se Claude Code non riesce a trovare l'installazione di Git Bash, impostate il percorso nel vostro [file settings.json](/it/settings):

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

**Opzione 2: WSL**

Sia WSL 1 che WSL 2 sono supportati. WSL 2 supporta il [sandboxing](/it/sandboxing) per una sicurezza migliorata. WSL 1 non supporta il sandboxing.

### Alpine Linux e distribuzioni basate su musl

L'installer nativo su Alpine e altre distribuzioni basate su musl/uClibc richiede `libgcc`, `libstdc++` e `ripgrep`. Installate questi utilizzando il gestore di pacchetti della vostra distribuzione, quindi impostate `USE_BUILTIN_RIPGREP=0`.

Questo esempio installa i pacchetti richiesti su Alpine:

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

Quindi impostate `USE_BUILTIN_RIPGREP` a `0` nel vostro file [`settings.json`](/it/settings#available-settings):

```json  theme={null}
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

## Verificare l'installazione

Dopo l'installazione, confermate che Claude Code funziona:

```bash  theme={null}
claude --version
```

Per un controllo più dettagliato dell'installazione e della configurazione, eseguite [`claude doctor`](/it/troubleshooting#get-more-help):

```bash  theme={null}
claude doctor
```

## Autenticazione

Claude Code richiede un account Pro, Max, Teams, Enterprise o Console. Il piano gratuito di Claude.ai non include l'accesso a Claude Code. Potete anche utilizzare Claude Code con un provider API di terze parti come [Amazon Bedrock](/it/amazon-bedrock), [Google Vertex AI](/it/google-vertex-ai) o [Microsoft Foundry](/it/microsoft-foundry).

Dopo l'installazione, accedete eseguendo `claude` e seguendo i prompt del browser. Consultate [Autenticazione](/it/authentication) per tutti i tipi di account e le opzioni di configurazione del team.

## Aggiornare Claude Code

Le installazioni native si aggiornano automaticamente in background. Potete [configurare il canale di rilascio](#configure-release-channel) per controllare se ricevere gli aggiornamenti immediatamente o secondo una pianificazione stabile ritardata, oppure [disabilitare gli aggiornamenti automatici](#disable-auto-updates) completamente. Le installazioni Homebrew e WinGet richiedono aggiornamenti manuali.

### Aggiornamenti automatici

Claude Code verifica la disponibilità di aggiornamenti all'avvio e periodicamente durante l'esecuzione. Gli aggiornamenti si scaricano e si installano in background, quindi hanno effetto la prossima volta che avviate Claude Code.

<Note>
  Le installazioni Homebrew e WinGet non si aggiornano automaticamente. Utilizzate `brew upgrade claude-code` o `winget upgrade Anthropic.ClaudeCode` per aggiornare manualmente.

  **Problema noto:** Claude Code potrebbe notificarvi gli aggiornamenti prima che la nuova versione sia disponibile in questi gestori di pacchetti. Se un aggiornamento non riesce, attendete e riprovate più tardi.

  Homebrew mantiene le versioni precedenti su disco dopo gli aggiornamenti. Eseguite `brew cleanup claude-code` periodicamente per recuperare spazio su disco.
</Note>

### Configurare il canale di rilascio

Controllate quale canale di rilascio Claude Code segue per gli aggiornamenti automatici e `claude update` con l'impostazione `autoUpdatesChannel`:

* `"latest"`, l'impostazione predefinita: ricevete le nuove funzionalità non appena vengono rilasciate
* `"stable"`: utilizzate una versione che è tipicamente circa una settimana più vecchia, saltando i rilasci con regressioni importanti

Configurate questo tramite `/config` → **Auto-update channel**, oppure aggiungetelo al vostro [file settings.json](/it/settings):

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Per le distribuzioni aziendali, potete applicare un canale di rilascio coerente in tutta l'organizzazione utilizzando [impostazioni gestite](/it/permissions#managed-settings).

### Disabilitare gli aggiornamenti automatici

Impostate `DISABLE_AUTOUPDATER` a `"1"` nella chiave `env` del vostro file [`settings.json`](/it/settings#available-settings):

```json  theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

### Aggiornare manualmente

Per applicare un aggiornamento immediatamente senza attendere il prossimo controllo in background, eseguite:

```bash  theme={null}
claude update
```

## Opzioni di installazione avanzate

Queste opzioni sono per il pinning delle versioni, la migrazione da npm e la verifica dell'integrità dei binari.

### Installare una versione specifica

L'installer nativo accetta un numero di versione specifico o un canale di rilascio (`latest` o `stable`). Il canale che scegliete al momento dell'installazione diventa il vostro predefinito per gli aggiornamenti automatici. Consultate [configurare il canale di rilascio](#configure-release-channel) per ulteriori informazioni.

Per installare la versione più recente (predefinita):

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

Per installare la versione stabile:

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

Per installare un numero di versione specifico:

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

### Installazione npm deprecata

L'installazione npm è deprecata. L'installer nativo è più veloce, non richiede dipendenze e si aggiorna automaticamente in background. Utilizzate il metodo di [installazione nativa](#install-claude-code) quando possibile.

#### Migrare da npm a nativo

Se avete precedentemente installato Claude Code con npm, passate all'installer nativo:

```bash  theme={null}
# Installare il binario nativo
curl -fsSL https://claude.ai/install.sh | bash

# Rimuovere la vecchia installazione npm
npm uninstall -g @anthropic-ai/claude-code
```

Potete anche eseguire `claude install` da un'installazione npm esistente per installare il binario nativo insieme ad essa, quindi rimuovere la versione npm.

#### Installare con npm

Se avete bisogno dell'installazione npm per motivi di compatibilità, dovete avere [Node.js 18+](https://nodejs.org/en/download) installato. Installate il pacchetto globalmente:

```bash  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  NON utilizzate `sudo npm install -g` poiché ciò può portare a problemi di permessi e rischi di sicurezza. Se riscontrate errori di permessi, consultate la [risoluzione dei problemi di permessi](/it/troubleshooting#permission-errors-during-installation).
</Warning>

### Integrità dei binari e firma del codice

Potete verificare l'integrità dei binari di Claude Code utilizzando checksum SHA256 e firme del codice.

* I checksum SHA256 per tutte le piattaforme sono pubblicati nei manifesti di rilascio su `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json`. Sostituite `{VERSION}` con un numero di versione come `2.0.30`.
* I binari firmati sono distribuiti per le seguenti piattaforme:
  * **macOS**: firmato da "Anthropic PBC" e notarizzato da Apple
  * **Windows**: firmato da "Anthropic, PBC"

## Disinstallare Claude Code

Per rimuovere Claude Code, seguite le istruzioni per il vostro metodo di installazione.

### Installazione nativa

Rimuovete il binario di Claude Code e i file di versione:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    rm -f ~/.local/bin/claude
    rm -rf ~/.local/share/claude
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
    Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
    ```
  </Tab>
</Tabs>

### Installazione Homebrew

Rimuovete il cask Homebrew:

```bash  theme={null}
brew uninstall --cask claude-code
```

### Installazione WinGet

Rimuovete il pacchetto WinGet:

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### npm

Rimuovete il pacchetto npm globale:

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Rimuovere i file di configurazione

<Warning>
  La rimozione dei file di configurazione eliminerà tutte le vostre impostazioni, gli strumenti consentiti, le configurazioni del server MCP e la cronologia delle sessioni.
</Warning>

Per rimuovere le impostazioni di Claude Code e i dati memorizzati nella cache:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    # Rimuovere le impostazioni utente e lo stato
    rm -rf ~/.claude
    rm ~/.claude.json

    # Rimuovere le impostazioni specifiche del progetto (eseguire dalla directory del progetto)
    rm -rf .claude
    rm -f .mcp.json
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    # Rimuovere le impostazioni utente e lo stato
    Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
    Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

    # Rimuovere le impostazioni specifiche del progetto (eseguire dalla directory del progetto)
    Remove-Item -Path ".claude" -Recurse -Force
    Remove-Item -Path ".mcp.json" -Force
    ```
  </Tab>
</Tabs>
