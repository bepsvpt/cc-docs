> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurare Claude Code

> Installa, autentica e inizia a utilizzare Claude Code sulla tua macchina di sviluppo.

## Requisiti di sistema

* **Sistema operativo**:
  * macOS 13.0+
  * Windows 10 1809+ o Windows Server 2019+ ([vedere le note di configurazione](#platform-specific-setup))
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+ ([dipendenze aggiuntive richieste](#platform-specific-setup))
* **Hardware**: 4 GB+ di RAM
* **Rete**: Connessione Internet richiesta (vedere [configurazione di rete](/it/network-config#network-access-requirements))
* **Shell**: Funziona meglio in Bash o Zsh
* **Posizione**: [Paesi supportati da Anthropic](https://www.anthropic.com/supported-countries)

### Dipendenze aggiuntive

* **ripgrep**: Solitamente incluso con Claude Code. Se la ricerca non funziona, vedere [risoluzione dei problemi di ricerca](/it/troubleshooting#search-and-discovery-issues).
* **[Node.js 18+](https://nodejs.org/en/download)**: Richiesto solo per [installazione npm deprecata](#npm-installation-deprecated)

## Installazione

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

Dopo il completamento del processo di installazione, accedi al tuo progetto e avvia Claude Code:

```bash  theme={null}
cd your-awesome-project
claude
```

Se riscontri problemi durante l'installazione, consulta la [guida alla risoluzione dei problemi](/it/troubleshooting).

<Tip>
  Esegui `claude doctor` dopo l'installazione per verificare il tipo di installazione e la versione.
</Tip>

### Configurazione specifica della piattaforma

**Windows**: Esegui Claude Code in modo nativo (richiede [Git Bash](https://git-scm.com/downloads/win)) o all'interno di WSL. Sia WSL 1 che WSL 2 sono supportati, ma WSL 1 ha supporto limitato e non supporta funzionalità come il sandboxing dello strumento Bash.

**Alpine Linux e altre distribuzioni basate su musl/uClibc**:

Il programma di installazione nativo su Alpine e altre distribuzioni basate su musl/uClibc richiede `libgcc`, `libstdc++` e `ripgrep`. Installa questi utilizzando il gestore di pacchetti della tua distribuzione, quindi imposta `USE_BUILTIN_RIPGREP=0`.

Su Alpine:

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

### Autenticazione

#### Per i singoli utenti

1. **Piano Claude Pro o Max** (consigliato): Sottoscrivi il [piano Pro o Max](https://claude.ai/pricing) di Claude per un abbonamento unificato che include sia Claude Code che Claude sul web. Gestisci il tuo account in un unico posto e accedi con il tuo account Claude.ai.
2. **Claude Console**: Connettiti tramite la [Claude Console](https://console.anthropic.com) e completa il processo OAuth. Richiede fatturazione attiva nella Console Anthropic. Uno spazio di lavoro "Claude Code" viene creato automaticamente per il tracciamento dell'utilizzo e la gestione dei costi. Non puoi creare chiavi API per lo spazio di lavoro Claude Code; è dedicato esclusivamente all'utilizzo di Claude Code.

#### Per team e organizzazioni

1. **Claude for Teams o Enterprise** (consigliato): Sottoscrivi [Claude for Teams](https://claude.com/pricing#team-&-enterprise) o [Claude for Enterprise](https://anthropic.com/contact-sales) per fatturazione centralizzata, gestione del team e accesso sia a Claude Code che a Claude sul web. I membri del team accedono con i loro account Claude.ai.
2. **Claude Console con fatturazione del team**: Configura un'organizzazione [Claude Console](https://console.anthropic.com) condivisa con fatturazione del team. Invita i membri del team e assegna ruoli per il tracciamento dell'utilizzo.
3. **Provider cloud**: Configura Claude Code per utilizzare [Amazon Bedrock, Google Vertex AI o Microsoft Foundry](/it/third-party-integrations) per distribuzioni con la tua infrastruttura cloud esistente.

### Installa una versione specifica

Il programma di installazione nativo accetta un numero di versione specifico o un canale di rilascio (`latest` o `stable`). Il canale che scegli al momento dell'installazione diventa il tuo predefinito per gli aggiornamenti automatici. Vedere [Configurare il canale di rilascio](#configure-release-channel) per ulteriori informazioni.

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

### Integrità binaria e firma del codice

* I checksum SHA256 per tutte le piattaforme sono pubblicati nei manifesti di rilascio, attualmente ubicati in `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json` (esempio: sostituisci `{VERSION}` con `2.0.30`)
* I binari firmati sono distribuiti per le seguenti piattaforme:
  * macOS: Firmato da "Anthropic PBC" e notarizzato da Apple
  * Windows: Firmato da "Anthropic, PBC"

## Installazione NPM (deprecata)

L'installazione NPM è deprecata. Utilizza il metodo di [installazione nativa](#installation) quando possibile. Per migrare un'installazione npm esistente a nativa, esegui `claude install`.

**Installazione npm globale**

```sh  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  NON utilizzare `sudo npm install -g` poiché ciò può portare a problemi di autorizzazione e rischi di sicurezza.
  Se riscontri errori di autorizzazione, vedere [risoluzione dei problemi di autorizzazione](/it/troubleshooting#command-not-found-claude-or-permission-errors) per le soluzioni consigliate.
</Warning>

## Configurazione di Windows

**Opzione 1: Claude Code all'interno di WSL**

* Sia WSL 1 che WSL 2 sono supportati
* WSL 2 supporta il [sandboxing](/it/sandboxing) per una sicurezza migliorata. WSL 1 non supporta il sandboxing.

**Opzione 2: Claude Code su Windows nativo con Git Bash**

* Richiede [Git for Windows](https://git-scm.com/downloads/win)
* Per le installazioni Git portatili, specifica il percorso del tuo `bash.exe`:
  ```powershell  theme={null}
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Aggiorna Claude Code

### Aggiornamenti automatici

Claude Code si aggiorna automaticamente per assicurarti di avere le funzionalità più recenti e le correzioni di sicurezza.

* **Controlli degli aggiornamenti**: Eseguiti all'avvio e periodicamente durante l'esecuzione
* **Processo di aggiornamento**: Scarica e installa automaticamente in background
* **Notifiche**: Vedrai una notifica quando gli aggiornamenti vengono installati
* **Applicazione degli aggiornamenti**: Gli aggiornamenti hanno effetto la prossima volta che avvii Claude Code

<Note>
  Le installazioni Homebrew e WinGet non si aggiornano automaticamente. Utilizza `brew upgrade claude-code` o `winget upgrade Anthropic.ClaudeCode` per aggiornare manualmente.

  **Problema noto:** Claude Code potrebbe notificarti gli aggiornamenti prima che la nuova versione sia disponibile in questi gestori di pacchetti. Se un aggiornamento non riesce, attendi e riprova più tardi.
</Note>

### Configurare il canale di rilascio

Configura quale canale di rilascio Claude Code segue sia per gli aggiornamenti automatici che per `claude update` con l'impostazione `autoUpdatesChannel`:

* `"latest"` (predefinito): Ricevi nuove funzionalità non appena vengono rilasciate
* `"stable"`: Utilizza una versione che è tipicamente circa una settimana più vecchia, saltando i rilasci con regressioni importanti

Configura questo tramite `/config` → **Canale di aggiornamento automatico**, o aggiungilo al tuo [file settings.json](/it/settings):

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Per distribuzioni aziendali, puoi applicare un canale di rilascio coerente in tutta l'organizzazione utilizzando [impostazioni gestite](/it/settings#settings-files).

### Disabilita gli aggiornamenti automatici

Imposta la variabile di ambiente `DISABLE_AUTOUPDATER` nella tua shell o nel [file settings.json](/it/settings):

```bash  theme={null}
export DISABLE_AUTOUPDATER=1
```

### Aggiorna manualmente

```bash  theme={null}
claude update
```

## Disinstalla Claude Code

Se hai bisogno di disinstallare Claude Code, segui le istruzioni per il tuo metodo di installazione.

### Installazione nativa

Rimuovi il binario Claude Code e i file di versione:

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

### Installazione Homebrew

```bash  theme={null}
brew uninstall --cask claude-code
```

### Installazione WinGet

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### Installazione NPM

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Pulisci i file di configurazione (facoltativo)

<Warning>
  La rimozione dei file di configurazione eliminerà tutte le tue impostazioni, gli strumenti consentiti, le configurazioni del server MCP e la cronologia della sessione.
</Warning>

Per rimuovere le impostazioni e i dati memorizzati nella cache di Claude Code:

**macOS, Linux, WSL:**

```bash  theme={null}
# Rimuovi le impostazioni utente e lo stato
rm -rf ~/.claude
rm ~/.claude.json

# Rimuovi le impostazioni specifiche del progetto (esegui dalla directory del tuo progetto)
rm -rf .claude
rm -f .mcp.json
```

**Windows PowerShell:**

```powershell  theme={null}
# Rimuovi le impostazioni utente e lo stato
Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

# Rimuovi le impostazioni specifiche del progetto (esegui dalla directory del tuo progetto)
Remove-Item -Path ".claude" -Recurse -Force
Remove-Item -Path ".mcp.json" -Force
```

**Windows CMD:**

```batch  theme={null}
REM Rimuovi le impostazioni utente e lo stato
rmdir /s /q "%USERPROFILE%\.claude"
del "%USERPROFILE%\.claude.json"

REM Rimuovi le impostazioni specifiche del progetto (esegui dalla directory del tuo progetto)
rmdir /s /q ".claude"
del ".mcp.json"
```
