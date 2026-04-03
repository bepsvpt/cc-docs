> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Scopri e installa plugin precostruiti tramite marketplace

> Trova e installa plugin dai marketplace per estendere Claude Code con nuovi comandi, agenti e funzionalità.

I plugin estendono Claude Code con skills, agenti, hooks e MCP servers. I marketplace dei plugin sono cataloghi che vi aiutano a scoprire e installare queste estensioni senza doverle costruire da soli.

Cercate di creare e distribuire il vostro marketplace? Consultate [Creare e distribuire un marketplace di plugin](/it/plugin-marketplaces).

## Come funzionano i marketplace

Un marketplace è un catalogo di plugin che qualcun altro ha creato e condiviso. Utilizzare un marketplace è un processo in due fasi:

<Steps>
  <Step title="Aggiungere il marketplace">
    Questo registra il catalogo con Claude Code in modo che possiate sfogliare ciò che è disponibile. Nessun plugin viene installato ancora.
  </Step>

  <Step title="Installare singoli plugin">
    Sfogliate il catalogo e installate i plugin che desiderate.
  </Step>
</Steps>

Pensatelo come aggiungere un app store: aggiungere lo store vi dà accesso per sfogliare la sua collezione, ma voi scegliete comunque quali app scaricare individualmente.

## Marketplace ufficiale Anthropic

Il marketplace ufficiale Anthropic (`claude-plugins-official`) è automaticamente disponibile quando avviate Claude Code. Eseguite `/plugin` e andate alla scheda **Discover** per sfogliare ciò che è disponibile, oppure visualizzate il catalogo su [claude.com/plugins](https://claude.com/plugins).

Per installare un plugin dal marketplace ufficiale, utilizzate `/plugin install <name>@claude-plugins-official`. Ad esempio, per installare l'integrazione GitHub:

```shell  theme={null}
/plugin install github@claude-plugins-official
```

<Note>
  Il marketplace ufficiale è mantenuto da Anthropic. Per inviare un plugin al marketplace ufficiale, utilizzate uno dei moduli di invio in-app:

  * **Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
  * **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

  Per distribuire plugin in modo indipendente, [create il vostro marketplace](/it/plugin-marketplaces) e condividetelo con gli utenti.
</Note>

Il marketplace ufficiale include diverse categorie di plugin:

### Code intelligence

I plugin di code intelligence abilitano lo strumento LSP integrato di Claude Code, dando a Claude la capacità di saltare alle definizioni, trovare riferimenti e vedere errori di tipo immediatamente dopo le modifiche. Questi plugin configurano connessioni [Language Server Protocol](https://microsoft.github.io/language-server-protocol/), la stessa tecnologia che alimenta la code intelligence di VS Code.

Questi plugin richiedono che il binario del language server sia installato sul vostro sistema. Se avete già un language server installato, Claude potrebbe chiedervi di installare il plugin corrispondente quando aprite un progetto.

| Linguaggio | Plugin              | Binario richiesto            |
| :--------- | :------------------ | :--------------------------- |
| C/C++      | `clangd-lsp`        | `clangd`                     |
| C#         | `csharp-lsp`        | `csharp-ls`                  |
| Go         | `gopls-lsp`         | `gopls`                      |
| Java       | `jdtls-lsp`         | `jdtls`                      |
| Kotlin     | `kotlin-lsp`        | `kotlin-language-server`     |
| Lua        | `lua-lsp`           | `lua-language-server`        |
| PHP        | `php-lsp`           | `intelephense`               |
| Python     | `pyright-lsp`       | `pyright-langserver`         |
| Rust       | `rust-analyzer-lsp` | `rust-analyzer`              |
| Swift      | `swift-lsp`         | `sourcekit-lsp`              |
| TypeScript | `typescript-lsp`    | `typescript-language-server` |

Potete anche [creare il vostro plugin LSP](/it/plugins-reference#lsp-servers) per altri linguaggi.

<Note>
  Se vedete `Executable not found in $PATH` nella scheda `/plugin` Errors dopo aver installato un plugin, installate il binario richiesto dalla tabella sopra.
</Note>

#### Cosa Claude guadagna dai plugin di code intelligence

Una volta che un plugin di code intelligence è installato e il suo binario del language server è disponibile, Claude guadagna due capacità:

* **Diagnostica automatica**: dopo ogni modifica di file che Claude fa, il language server analizza i cambiamenti e segnala errori e avvisi automaticamente. Claude vede errori di tipo, import mancanti e problemi di sintassi senza dover eseguire un compilatore o linter. Se Claude introduce un errore, lo nota e corregge il problema nello stesso turno. Questo non richiede alcuna configurazione oltre all'installazione del plugin. Potete vedere la diagnostica inline premendo **Ctrl+O** quando appare l'indicatore "diagnostics found".
* **Navigazione del codice**: Claude può utilizzare il language server per saltare alle definizioni, trovare riferimenti, ottenere informazioni sul tipo al passaggio del mouse, elencare simboli, trovare implementazioni e tracciare gerarchie di chiamate. Queste operazioni danno a Claude una navigazione più precisa rispetto alla ricerca basata su grep, anche se la disponibilità può variare a seconda del linguaggio e dell'ambiente.

Se riscontrate problemi, consultate [Risoluzione dei problemi di code intelligence](#code-intelligence-issues).

### Integrazioni esterne

Questi plugin raggruppano [MCP servers](/it/mcp) preconfigurati in modo che possiate connettere Claude a servizi esterni senza configurazione manuale:

* **Controllo del codice sorgente**: `github`, `gitlab`
* **Gestione dei progetti**: `atlassian` (Jira/Confluence), `asana`, `linear`, `notion`
* **Design**: `figma`
* **Infrastruttura**: `vercel`, `firebase`, `supabase`
* **Comunicazione**: `slack`
* **Monitoraggio**: `sentry`

### Flussi di lavoro di sviluppo

Plugin che aggiungono comandi e agenti per attività di sviluppo comuni:

* **commit-commands**: Flussi di lavoro di commit Git inclusi commit, push e creazione di PR
* **pr-review-toolkit**: Agenti specializzati per la revisione delle pull request
* **agent-sdk-dev**: Strumenti per la costruzione con Claude Agent SDK
* **plugin-dev**: Toolkit per la creazione dei vostri plugin

### Stili di output

Personalizzate come Claude risponde:

* **explanatory-output-style**: Approfondimenti educativi sulle scelte di implementazione
* **learning-output-style**: Modalità di apprendimento interattivo per la costruzione di competenze

## Provate: aggiungere il marketplace demo

Anthropic mantiene anche un [marketplace di plugin demo](https://github.com/anthropics/claude-code/tree/main/plugins) (`claude-code-plugins`) con plugin di esempio che mostrano cosa è possibile con il sistema di plugin. A differenza del marketplace ufficiale, dovete aggiungere questo manualmente.

<Steps>
  <Step title="Aggiungere il marketplace">
    Da Claude Code, eseguite il comando `plugin marketplace add` per il marketplace `anthropics/claude-code`:

    ```shell  theme={null}
    /plugin marketplace add anthropics/claude-code
    ```

    Questo scarica il catalogo del marketplace e rende i suoi plugin disponibili per voi.
  </Step>

  <Step title="Sfogliare i plugin disponibili">
    Eseguite `/plugin` per aprire il gestore dei plugin. Questo apre un'interfaccia a schede con quattro schede che potete scorrere utilizzando **Tab** (o **Shift+Tab** per andare indietro):

    * **Discover**: sfogliate i plugin disponibili da tutti i vostri marketplace
    * **Installed**: visualizzate e gestite i vostri plugin installati
    * **Marketplaces**: aggiungete, rimuovete o aggiornate i vostri marketplace aggiunti
    * **Errors**: visualizzate eventuali errori di caricamento dei plugin

    Andate alla scheda **Discover** per vedere i plugin dal marketplace che avete appena aggiunto.
  </Step>

  <Step title="Installare un plugin">
    Selezionate un plugin per visualizzare i suoi dettagli, quindi scegliete un ambito di installazione:

    * **User scope**: installate per voi stessi in tutti i progetti
    * **Project scope**: installate per tutti i collaboratori su questo repository
    * **Local scope**: installate per voi stessi solo in questo repository

    Ad esempio, selezionate **commit-commands** (un plugin che aggiunge comandi di flusso di lavoro git) e installatelo nel vostro ambito utente.

    Potete anche installare direttamente dalla riga di comando:

    ```shell  theme={null}
    /plugin install commit-commands@anthropics-claude-code
    ```

    Consultate [Ambiti di configurazione](/it/settings#configuration-scopes) per saperne di più sugli ambiti.
  </Step>

  <Step title="Utilizzare il vostro nuovo plugin">
    Dopo l'installazione, eseguite `/reload-plugins` per attivare il plugin. I comandi dei plugin sono nello spazio dei nomi del nome del plugin, quindi **commit-commands** fornisce comandi come `/commit-commands:commit`.

    Provate eseguendo una modifica a un file e eseguendo:

    ```shell  theme={null}
    /commit-commands:commit
    ```

    Questo mette in stage le vostre modifiche, genera un messaggio di commit e crea il commit.

    Ogni plugin funziona diversamente. Controllate la descrizione del plugin nella scheda **Discover** o la sua homepage per sapere quali comandi e funzionalità fornisce.
  </Step>
</Steps>

Il resto di questa guida copre tutti i modi in cui potete aggiungere marketplace, installare plugin e gestire la vostra configurazione.

## Aggiungere marketplace

Utilizzate il comando `/plugin marketplace add` per aggiungere marketplace da diverse fonti.

<Tip>
  **Scorciatoie**: Potete utilizzare `/plugin market` invece di `/plugin marketplace` e `rm` invece di `remove`.
</Tip>

* **Repository GitHub**: formato `owner/repo` (ad esempio, `anthropics/claude-code`)
* **URL Git**: qualsiasi URL di repository git (GitLab, Bitbucket, self-hosted)
* **Percorsi locali**: directory o percorsi diretti ai file `marketplace.json`
* **URL remoti**: URL diretti ai file `marketplace.json` ospitati

### Aggiungere da GitHub

Aggiungete un repository GitHub che contiene un file `.claude-plugin/marketplace.json` utilizzando il formato `owner/repo`—dove `owner` è il nome utente GitHub o l'organizzazione e `repo` è il nome del repository.

Ad esempio, `anthropics/claude-code` si riferisce al repository `claude-code` di proprietà di `anthropics`:

```shell  theme={null}
/plugin marketplace add anthropics/claude-code
```

### Aggiungere da altri host Git

Aggiungete qualsiasi repository git fornendo l'URL completo. Questo funziona con qualsiasi host Git, inclusi GitLab, Bitbucket e server self-hosted:

Utilizzando HTTPS:

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

Utilizzando SSH:

```shell  theme={null}
/plugin marketplace add git@gitlab.com:company/plugins.git
```

Per aggiungere un branch o tag specifico, aggiungete `#` seguito dal ref:

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

### Aggiungere da percorsi locali

Aggiungete una directory locale che contiene un file `.claude-plugin/marketplace.json`:

```shell  theme={null}
/plugin marketplace add ./my-marketplace
```

Potete anche aggiungere un percorso diretto a un file `marketplace.json`:

```shell  theme={null}
/plugin marketplace add ./path/to/marketplace.json
```

### Aggiungere da URL remoti

Aggiungete un file `marketplace.json` remoto tramite URL:

```shell  theme={null}
/plugin marketplace add https://example.com/marketplace.json
```

<Note>
  I marketplace basati su URL hanno alcune limitazioni rispetto ai marketplace basati su Git. Se riscontrate errori "path not found" durante l'installazione di plugin, consultate [Risoluzione dei problemi](/it/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces).
</Note>

## Installare plugin

Una volta aggiunti i marketplace, potete installare plugin direttamente (installa nell'ambito utente per impostazione predefinita):

```shell  theme={null}
/plugin install plugin-name@marketplace-name
```

Per scegliere un [ambito di installazione](/it/settings#configuration-scopes) diverso, utilizzate l'interfaccia interattiva: eseguite `/plugin`, andate alla scheda **Discover** e premete **Enter** su un plugin. Vedrete opzioni per:

* **User scope** (predefinito): installate per voi stessi in tutti i progetti
* **Project scope**: installate per tutti i collaboratori su questo repository (aggiunge a `.claude/settings.json`)
* **Local scope**: installate per voi stessi solo in questo repository (non condiviso con i collaboratori)

Potete anche vedere plugin con ambito **managed**—questi sono installati dagli amministratori tramite [impostazioni gestite](/it/settings#settings-files) e non possono essere modificati.

Eseguite `/plugin` e andate alla scheda **Installed** per vedere i vostri plugin raggruppati per ambito.

<Warning>
  Assicuratevi di fidarvi di un plugin prima di installarlo. Anthropic non controlla quali MCP server, file o altro software sono inclusi nei plugin e non può verificare che funzionino come previsto. Controllate la homepage di ogni plugin per ulteriori informazioni.
</Warning>

## Gestire i plugin installati

Eseguite `/plugin` e andate alla scheda **Installed** per visualizzare, abilitare, disabilitare o disinstallare i vostri plugin. Digitate per filtrare l'elenco per nome o descrizione del plugin.

Potete anche gestire i plugin con comandi diretti.

Disabilitate un plugin senza disinstallarlo:

```shell  theme={null}
/plugin disable plugin-name@marketplace-name
```

Riabilitate un plugin disabilitato:

```shell  theme={null}
/plugin enable plugin-name@marketplace-name
```

Rimuovete completamente un plugin:

```shell  theme={null}
/plugin uninstall plugin-name@marketplace-name
```

L'opzione `--scope` vi consente di indirizzare un ambito specifico con comandi CLI:

```shell  theme={null}
claude plugin install formatter@your-org --scope project
claude plugin uninstall formatter@your-org --scope project
```

### Applicare le modifiche dei plugin senza riavviare

Quando installate, abilitate o disabilitate plugin durante una sessione, eseguite `/reload-plugins` per raccogliere tutte le modifiche senza riavviare:

```shell  theme={null}
/reload-plugins
```

Claude Code ricarica tutti i plugin attivi e mostra i conteggi per i plugin, le skills, gli agenti, gli hook, i server MCP dei plugin e i server LSP dei plugin.

## Gestire i marketplace

Potete gestire i marketplace tramite l'interfaccia interattiva `/plugin` o con comandi CLI.

### Utilizzare l'interfaccia interattiva

Eseguite `/plugin` e andate alla scheda **Marketplaces** per:

* Visualizzare tutti i vostri marketplace aggiunti con le loro fonti e stato
* Aggiungere nuovi marketplace
* Aggiornare gli elenchi dei marketplace per recuperare i plugin più recenti
* Rimuovere i marketplace di cui non avete più bisogno

### Utilizzare comandi CLI

Potete anche gestire i marketplace con comandi diretti.

Elencate tutti i marketplace configurati:

```shell  theme={null}
/plugin marketplace list
```

Aggiornate gli elenchi dei plugin da un marketplace:

```shell  theme={null}
/plugin marketplace update marketplace-name
```

Rimuovete un marketplace:

```shell  theme={null}
/plugin marketplace remove marketplace-name
```

<Warning>
  La rimozione di un marketplace disinstallerà tutti i plugin che avete installato da esso.
</Warning>

### Configurare gli aggiornamenti automatici

Claude Code può aggiornare automaticamente i marketplace e i loro plugin installati all'avvio. Quando l'aggiornamento automatico è abilitato per un marketplace, Claude Code aggiorna i dati del marketplace e aggiorna i plugin installati alle loro versioni più recenti. Se sono stati aggiornati plugin, vedrete una notifica che vi chiede di eseguire `/reload-plugins`.

Attivate/disattivate l'aggiornamento automatico per singoli marketplace tramite l'interfaccia utente:

1. Eseguite `/plugin` per aprire il gestore dei plugin
2. Selezionate **Marketplaces**
3. Scegliete un marketplace dall'elenco
4. Selezionate **Enable auto-update** o **Disable auto-update**

I marketplace ufficiali Anthropic hanno l'aggiornamento automatico abilitato per impostazione predefinita. I marketplace di terze parti e di sviluppo locale hanno l'aggiornamento automatico disabilitato per impostazione predefinita.

Per disabilitare completamente tutti gli aggiornamenti automatici sia per Claude Code che per tutti i plugin, impostate la variabile di ambiente `DISABLE_AUTOUPDATER`. Consultate [Aggiornamenti automatici](/it/setup#auto-updates) per i dettagli.

Per mantenere gli aggiornamenti automatici dei plugin abilitati mentre disabilitate gli aggiornamenti di Claude Code, impostate `FORCE_AUTOUPDATE_PLUGINS=1` insieme a `DISABLE_AUTOUPDATER`:

```bash  theme={null}
export DISABLE_AUTOUPDATER=1
export FORCE_AUTOUPDATE_PLUGINS=1
```

Questo è utile quando volete gestire gli aggiornamenti di Claude Code manualmente ma ricevere comunque aggiornamenti automatici dei plugin.

## Configurare i marketplace del team

Gli amministratori del team possono configurare l'installazione automatica del marketplace per i progetti aggiungendo la configurazione del marketplace a `.claude/settings.json`. Quando i membri del team si fidano della cartella del repository, Claude Code li invita a installare questi marketplace e plugin.

Aggiungete `extraKnownMarketplaces` al file `.claude/settings.json` del vostro progetto:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "my-team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

Per le opzioni di configurazione complete incluse `extraKnownMarketplaces` e `enabledPlugins`, consultate [Impostazioni dei plugin](/it/settings#plugin-settings).

## Sicurezza

I plugin e i marketplace sono componenti altamente affidabili che possono eseguire codice arbitrario sulla vostra macchina con i vostri privilegi utente. Installate solo plugin e aggiungete marketplace da fonti di cui vi fidate. Le organizzazioni possono limitare quali marketplace gli utenti sono autorizzati ad aggiungere utilizzando [restrizioni gestite dei marketplace](/it/plugin-marketplaces#managed-marketplace-restrictions).

## Risoluzione dei problemi

### Comando /plugin non riconosciuto

Se vedete "unknown command" o il comando `/plugin` non appare:

1. **Controllate la vostra versione**: Eseguite `claude --version` per vedere cosa è installato.
2. **Aggiornate Claude Code**:
   * **Homebrew**: `brew upgrade claude-code`
   * **npm**: `npm update -g @anthropic-ai/claude-code`
   * **Programma di installazione nativo**: Rieseguite il comando di installazione da [Setup](/it/setup)
3. **Riavviate Claude Code**: Dopo l'aggiornamento, riavviate il vostro terminale ed eseguite `claude` di nuovo.

### Problemi comuni

* **Marketplace non caricato**: Verificate che l'URL sia accessibile e che `.claude-plugin/marketplace.json` esista nel percorso
* **Errori di installazione dei plugin**: Controllate che gli URL di origine dei plugin siano accessibili e che i repository siano pubblici (o che abbiate accesso)
* **File non trovati dopo l'installazione**: I plugin vengono copiati in una cache, quindi i percorsi che fanno riferimento a file al di fuori della directory del plugin non funzioneranno
* **Le skill dei plugin non appaiono**: Cancellate la cache con `rm -rf ~/.claude/plugins/cache`, riavviate Claude Code e reinstallate il plugin.

Per la risoluzione dettagliata dei problemi con soluzioni, consultate [Risoluzione dei problemi](/it/plugin-marketplaces#troubleshooting) nella guida del marketplace. Per gli strumenti di debug, consultate [Strumenti di debug e sviluppo](/it/plugins-reference#debugging-and-development-tools).

### Problemi di code intelligence

* **Language server non avviato**: verificate che il binario sia installato e disponibile nel vostro `$PATH`. Controllate la scheda `/plugin` Errors per i dettagli.
* **Utilizzo elevato della memoria**: i language server come `rust-analyzer` e `pyright` possono consumare memoria significativa su progetti di grandi dimensioni. Se riscontrate problemi di memoria, disabilitate il plugin con `/plugin disable <plugin-name>` e affidatevi invece agli strumenti di ricerca integrati di Claude.
* **Diagnostica falsa positiva nei monorepo**: i language server possono segnalare errori di import non risolti per i pacchetti interni se l'area di lavoro non è configurata correttamente. Questi non influiscono sulla capacità di Claude di modificare il codice.

## Passaggi successivi

* **Costruite i vostri plugin**: Consultate [Plugin](/it/plugins) per creare skills, agenti e hook
* **Create un marketplace**: Consultate [Creare un marketplace di plugin](/it/plugin-marketplaces) per distribuire plugin al vostro team o comunità
* **Riferimento tecnico**: Consultate [Riferimento dei plugin](/it/plugins-reference) per le specifiche complete
