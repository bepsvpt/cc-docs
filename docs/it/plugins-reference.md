> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Riferimento dei plugin

> Riferimento tecnico completo per il sistema di plugin di Claude Code, inclusi schemi, comandi CLI e specifiche dei componenti.

<Tip>
  Stai cercando di installare plugin? Vedi [Scopri e installa plugin](/it/discover-plugins). Per creare plugin, vedi [Plugin](/it/plugins). Per distribuire plugin, vedi [Marketplace dei plugin](/it/plugin-marketplaces).
</Tip>

Questo riferimento fornisce specifiche tecniche complete per il sistema di plugin di Claude Code, inclusi schemi dei componenti, comandi CLI e strumenti di sviluppo.

Un **plugin** è una directory autonoma di componenti che estende Claude Code con funzionalità personalizzate. I componenti del plugin includono skills, agents, hooks, server MCP, server LSP e monitor.

## Riferimento dei componenti del plugin

### Skills

I plugin aggiungono skills a Claude Code, creando scorciatoie `/name` che Lei o Claude potete invocare.

**Posizione**: Directory `skills/` o `commands/` nella radice del plugin, o un singolo file `SKILL.md` nella radice del plugin

**Formato file**: Le skills sono directory con `SKILL.md`; i comandi sono semplici file markdown

**Struttura della skill**:

```text theme={null}
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (opzionale)
│   └── scripts/ (opzionale)
└── code-reviewer/
    └── SKILL.md
```

**Comportamento dell'integrazione**:

* Le skills e i comandi vengono rilevati automaticamente quando il plugin viene installato
* Claude può invocarli automaticamente in base al contesto dell'attività
* Le skills possono includere file di supporto insieme a SKILL.md

Per i dettagli completi, vedi [Skills](/it/skills).

### Agents

I plugin possono fornire subagents specializzati per attività specifiche che Claude può invocare automaticamente quando appropriato.

**Posizione**: Directory `agents/` nella radice del plugin

**Formato file**: File markdown che descrivono le capacità dell'agent

**Struttura dell'agent**:

```markdown theme={null}
---
name: agent-name
description: In cosa si specializza questo agent e quando Claude dovrebbe invocarlo
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Write, Edit
---

Prompt di sistema dettagliato per l'agent che descrive il suo ruolo, competenza e comportamento.
```

I plugin agents supportano i campi frontmatter `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background` e `isolation`. L'unico valore valido per `isolation` è `"worktree"`. Per motivi di sicurezza, `hooks`, `mcpServers` e `permissionMode` non sono supportati per gli agents forniti dai plugin.

**Punti di integrazione**:

* Gli agents appaiono nell'interfaccia `/agents`
* Claude può invocare gli agents automaticamente in base al contesto dell'attività
* Gli agents possono essere invocati manualmente dagli utenti
* I plugin agents funzionano insieme agli agents Claude integrati

Per i dettagli completi, vedi [Subagents](/it/sub-agents).

### Hooks

I plugin possono fornire gestori di eventi che rispondono automaticamente agli eventi di Claude Code.

**Posizione**: `hooks/hooks.json` nella radice del plugin, o inline in plugin.json

**Formato**: Configurazione JSON con matcher di eventi e azioni

**Configurazione dell'hook**:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

I plugin hooks rispondono agli stessi eventi del ciclo di vita degli [hooks definiti dall'utente](/it/hooks):

| Event                 | When it fires                                                                                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`        | When a session begins or resumes                                                                                                                       |
| `Setup`               | When you start Claude Code with `--init-only`, or with `--init` or `--maintenance` in `-p` mode. For one-time preparation in CI or scripts             |
| `UserPromptSubmit`    | When you submit a prompt, before Claude processes it                                                                                                   |
| `UserPromptExpansion` | When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion                                                     |
| `PreToolUse`          | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`   | When a permission dialog appears                                                                                                                       |
| `PermissionDenied`    | When a tool call is denied by the auto mode classifier. Return `{retry: true}` to tell the model it may retry the denied tool call                     |
| `PostToolUse`         | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure`  | After a tool call fails                                                                                                                                |
| `PostToolBatch`       | After a full batch of parallel tool calls resolves, before the next model call                                                                         |
| `Notification`        | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`       | When a subagent is spawned                                                                                                                             |
| `SubagentStop`        | When a subagent finishes                                                                                                                               |
| `TaskCreated`         | When a task is being created via `TaskCreate`                                                                                                          |
| `TaskCompleted`       | When a task is being marked as completed                                                                                                               |
| `Stop`                | When Claude finishes responding                                                                                                                        |
| `StopFailure`         | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`        | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `InstructionsLoaded`  | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`        | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`          | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`         | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`      | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`      | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`          | Before context compaction                                                                                                                              |
| `PostCompact`         | After context compaction completes                                                                                                                     |
| `Elicitation`         | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`   | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`          | When a session terminates                                                                                                                              |

**Tipi di hook**:

* `command`: esegui comandi shell o script
* `http`: invia l'evento JSON come richiesta POST a un URL
* `mcp_tool`: chiama uno strumento su un server [MCP](/it/mcp) configurato
* `prompt`: valuta un prompt con un LLM (usa il placeholder `$ARGUMENTS` per il contesto)
* `agent`: esegui un verificatore agentico con strumenti per attività di verifica complesse

### MCP servers

I plugin possono raggruppare server Model Context Protocol (MCP) per connettere Claude Code con strumenti e servizi esterni.

**Posizione**: `.mcp.json` nella radice del plugin, o inline in plugin.json

**Formato**: Configurazione standard del server MCP

**Configurazione del server MCP**:

```json theme={null}
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**Comportamento dell'integrazione**:

* I server MCP del plugin si avviano automaticamente quando il plugin è abilitato
* I server appaiono come strumenti MCP standard nel toolkit di Claude
* Le capacità del server si integrano perfettamente con gli strumenti esistenti di Claude
* I server del plugin possono essere configurati indipendentemente dai server MCP dell'utente

### LSP servers

<Tip>
  Stai cercando di usare plugin LSP? Installali dal marketplace ufficiale: cerca "lsp" nella scheda Discover di `/plugin`. Questa sezione documenta come creare plugin LSP per linguaggi non coperti dal marketplace ufficiale.
</Tip>

I plugin possono fornire server [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) per dare a Claude intelligenza del codice in tempo reale mentre lavori sul tuo codebase.

L'integrazione LSP fornisce:

* **Diagnostica istantanea**: Claude vede errori e avvisi immediatamente dopo ogni modifica
* **Navigazione del codice**: vai alla definizione, trova riferimenti e informazioni al passaggio del mouse
* **Consapevolezza del linguaggio**: informazioni sul tipo e documentazione per i simboli del codice

**Posizione**: `.lsp.json` nella radice del plugin, o inline in `plugin.json`

**Formato**: Configurazione JSON che mappa i nomi dei server di linguaggio alle loro configurazioni

**Formato del file `.lsp.json`**:

```json theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**Inline in `plugin.json`**:

```json theme={null}
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**Campi obbligatori:**

| Campo                 | Descrizione                                                   |
| :-------------------- | :------------------------------------------------------------ |
| `command`             | Il binario LSP da eseguire (deve essere in PATH)              |
| `extensionToLanguage` | Mappa le estensioni di file agli identificatori di linguaggio |

**Campi opzionali:**

| Campo                   | Descrizione                                                       |
| :---------------------- | :---------------------------------------------------------------- |
| `args`                  | Argomenti della riga di comando per il server LSP                 |
| `transport`             | Trasporto di comunicazione: `stdio` (predefinito) o `socket`      |
| `env`                   | Variabili di ambiente da impostare all'avvio del server           |
| `initializationOptions` | Opzioni passate al server durante l'inizializzazione              |
| `settings`              | Impostazioni passate tramite `workspace/didChangeConfiguration`   |
| `workspaceFolder`       | Percorso della cartella di lavoro per il server                   |
| `startupTimeout`        | Tempo massimo di attesa per l'avvio del server (millisecondi)     |
| `shutdownTimeout`       | Tempo massimo di attesa per l'arresto graduale (millisecondi)     |
| `restartOnCrash`        | Se riavviare automaticamente il server in caso di arresto anomalo |
| `maxRestarts`           | Numero massimo di tentativi di riavvio prima di rinunciare        |

<Warning>
  **Devi installare il binario del server di linguaggio separatamente.** I plugin LSP configurano come Claude Code si connette a un server di linguaggio, ma non includono il server stesso. Se vedi `Executable not found in $PATH` nella scheda Errors di `/plugin`, installa il binario richiesto per il tuo linguaggio.
</Warning>

**Plugin LSP disponibili:**

| Plugin              | Server di linguaggio       | Comando di installazione                                                                        |
| :------------------ | :------------------------- | :---------------------------------------------------------------------------------------------- |
| `pyright-lsp`       | Pyright (Python)           | `pip install pyright` o `npm install -g pyright`                                                |
| `typescript-lsp`    | TypeScript Language Server | `npm install -g typescript-language-server typescript`                                          |
| `rust-analyzer-lsp` | rust-analyzer              | [Vedi installazione di rust-analyzer](https://rust-analyzer.github.io/manual.html#installation) |

Installa il server di linguaggio per primo, quindi installa il plugin dal marketplace.

### Monitors

I plugin possono dichiarare monitor in background che Claude Code avvia automaticamente quando il plugin è attivo. Ogni monitor esegue un comando shell per la durata della sessione e fornisce ogni riga stdout a Claude come notifica, in modo che Claude possa reagire alle voci di log, ai cambiamenti di stato o agli eventi sottoposti a polling senza essere chiesto di avviare il watch stesso.

I monitor dei plugin utilizzano lo stesso meccanismo dello [strumento Monitor](/it/tools-reference#monitor-tool) e condividono i suoi vincoli di disponibilità. Vengono eseguiti solo in sessioni CLI interattive, vengono eseguiti senza sandbox allo stesso livello di fiducia degli [hooks](#hooks) e vengono saltati su host in cui lo strumento Monitor non è disponibile.

<Note>
  I monitor dei plugin richiedono Claude Code v2.1.105 o successivo.
</Note>

**Posizione**: `monitors/monitors.json` nella radice del plugin, o inline in `plugin.json`

**Formato**: Array JSON di voci di monitor

Il seguente `monitors/monitors.json` monitora un endpoint di stato di distribuzione e un log di errore locale:

```json theme={null}
[
  {
    "name": "deploy-status",
    "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/poll-deploy.sh ${user_config.api_endpoint}",
    "description": "Deployment status changes"
  },
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log",
    "when": "on-skill-invoke:debug"
  }
]
```

Per dichiarare monitor inline, imposta `experimental.monitors` in `plugin.json` sullo stesso array. Per caricare da un percorso non predefinito, imposta `experimental.monitors` su una stringa di percorso relativo come `"./config/monitors.json"`. I monitor sono un [componente sperimentale](#experimental-components).

**Campi obbligatori:**

| Campo         | Descrizione                                                                                                                                 |
| :------------ | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`        | Identificatore univoco all'interno del plugin. Previene processi duplicati quando il plugin si ricarica o una skill viene invocata di nuovo |
| `command`     | Comando shell eseguito come processo in background persistente nella directory di lavoro della sessione                                     |
| `description` | Breve riepilogo di ciò che viene monitorato. Mostrato nel pannello attività e nei riepiloghi delle notifiche                                |

**Campi opzionali:**

| Campo  | Descrizione                                                                                                                                                                                                                                            |
| :----- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `when` | Controlla quando il monitor si avvia. `"always"` lo avvia all'avvio della sessione e al ricaricamento del plugin, ed è il predefinito. `"on-skill-invoke:<skill-name>"` lo avvia la prima volta che la skill denominata in questo plugin viene inviata |

Il valore `command` supporta le stesse [sostituzioni di variabili](#environment-variables) delle configurazioni dei server MCP e LSP: `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${CLAUDE_PROJECT_DIR}`, `${user_config.*}` e qualsiasi `${ENV_VAR}` dall'ambiente. Prefissa il comando con `cd "${CLAUDE_PLUGIN_ROOT}" && ` se lo script ha bisogno di essere eseguito dalla directory del plugin stesso.

La disabilitazione di un plugin a metà sessione non interrompe i monitor già in esecuzione. Si interrompono quando la sessione termina.

### Themes

I plugin possono fornire temi di colore che appaiono in `/theme` insieme ai preset integrati e ai temi locali dell'utente. Un tema è un file JSON in `themes/` con un preset `base` e una mappa sparsa `overrides` di token di colore. I temi sono un [componente sperimentale](#experimental-components).

```json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

Selezionando un tema del plugin si persiste `custom:<plugin-name>:<slug>` nella configurazione dell'utente. I temi del plugin sono di sola lettura; premendo `Ctrl+E` su uno in `/theme` lo copia in `~/.claude/themes/` in modo che l'utente possa modificare la copia.

***

## Ambiti di installazione del plugin

Quando installi un plugin, scegli un **ambito** che determina dove il plugin è disponibile e chi altro può usarlo:

| Ambito    | File di impostazioni                                | Caso d'uso                                                     |
| :-------- | :-------------------------------------------------- | :------------------------------------------------------------- |
| `user`    | `~/.claude/settings.json`                           | Plugin personali disponibili in tutti i progetti (predefinito) |
| `project` | `.claude/settings.json`                             | Plugin del team condivisi tramite controllo della versione     |
| `local`   | `.claude/settings.local.json`                       | Plugin specifici del progetto, gitignored                      |
| `managed` | [Impostazioni gestite](/it/settings#settings-files) | Plugin gestiti (sola lettura, solo aggiornamento)              |

I plugin utilizzano lo stesso sistema di ambito di altre configurazioni di Claude Code. Per le istruzioni di installazione e i flag di ambito, vedi [Installa plugin](/it/discover-plugins#install-plugins). Per una spiegazione completa degli ambiti, vedi [Ambiti di configurazione](/it/settings#configuration-scopes).

***

## Schema del manifest del plugin

Il file `.claude-plugin/plugin.json` definisce i metadati e la configurazione del tuo plugin. Questa sezione documenta tutti i campi e le opzioni supportati.

Il manifest è opzionale. Se omesso, Claude Code scopre automaticamente i componenti nelle [posizioni predefinite](#file-locations-reference) e deriva il nome del plugin dal nome della directory. Usa un manifest quando hai bisogno di fornire metadati o percorsi di componenti personalizzati.

### Schema completo

```json theme={null}
{
  "name": "plugin-name",
  "displayName": "Plugin Name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "skills": "./custom/skills/",
  "commands": ["./custom/commands/special.md"],
  "agents": ["./custom/agents/reviewer.md"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json",
  "experimental": {
    "themes": "./themes/",
    "monitors": "./monitors.json"
  },
  "dependencies": [
    "helper-lib",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

### Campi obbligatori

Se includi un manifest, `name` è l'unico campo obbligatorio.

| Campo  | Tipo   | Descrizione                                      | Esempio              |
| :----- | :----- | :----------------------------------------------- | :------------------- |
| `name` | string | Identificatore univoco (kebab-case, senza spazi) | `"deployment-tools"` |

Questo nome viene utilizzato per lo spazio dei nomi dei componenti. Ad esempio, nell'interfaccia utente, l'agent `agent-creator` per il plugin con nome `plugin-dev` apparirà come `plugin-dev:agent-creator`.

### Campi non riconosciuti

Claude Code ignora i campi di livello superiore che non riconosce. Potete mantenere i metadati da un altro ecosistema in `plugin.json` e il plugin continua a caricarsi. Questo rende pratico mantenere un unico manifest che funge anche da manifest dell'estensione VS Code o Cursor, da `package.json` npm, o da manifest del bundle MCPB/DXT.

`claude plugin validate` segnala i campi non riconosciuti come avvisi, non come errori. Se un campo è uno o due caratteri diverso da uno riconosciuto, l'avviso suggerisce il nome probabilmente inteso. Un plugin con solo avvisi di campi non riconosciuti passa comunque la convalida e si carica al runtime.

I campi con il tipo sbagliato comunque falliscono. Ad esempio, un valore `keywords` che è una stringa invece di un array è un errore di caricamento, e `claude plugin validate` lo segnala come tale.

Passa `--strict` per trattare gli avvisi come errori. Usalo in CI per rilevare un nome di campo scritto male o un campo rimasto da un altro manifest dello strumento prima della pubblicazione, anche se il plugin si caricherà al runtime.

```bash theme={null}
claude plugin validate ./my-plugin --strict
```

### Campi di metadati

| Campo         | Tipo   | Descrizione                                                                                                                                                                                                                                                                                                                                                                                                                       | Esempio                                                           |
| :------------ | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------- |
| `$schema`     | string | URL dello schema JSON per l'autocompletamento dell'editor e la convalida. Claude Code ignora questo campo al momento del caricamento.                                                                                                                                                                                                                                                                                             | `"https://json.schemastore.org/claude-code-plugin-manifest.json"` |
| `displayName` | string | {/* min-version: 2.1.143 */}Nome leggibile mostrato nel selettore `/plugin` e in altre superfici dell'interfaccia utente. Ricade su `name` quando omesso. A differenza di `name`, può contenere spazi e qualsiasi maiuscola/minuscola. Non utilizzato per lo spazio dei nomi o la ricerca. Richiede Claude Code v2.1.143 o successivo.                                                                                            | `"Deployment Tools"`                                              |
| `version`     | string | Opzionale. Versione semantica. L'impostazione di questo valore fissa il plugin a quella stringa di versione, quindi gli utenti ricevono aggiornamenti solo quando la modifichi. Se omesso, Claude Code ricade sulla SHA del commit git, quindi ogni commit viene trattato come una nuova versione. Se impostato anche nella voce del marketplace, `plugin.json` ha priorità. Vedi [Gestione delle versioni](#version-management). | `"2.1.0"`                                                         |
| `description` | string | Breve spiegazione dello scopo del plugin                                                                                                                                                                                                                                                                                                                                                                                          | `"Deployment automation tools"`                                   |
| `author`      | object | Informazioni sull'autore                                                                                                                                                                                                                                                                                                                                                                                                          | `{"name": "Dev Team", "email": "dev@company.com"}`                |
| `homepage`    | string | URL della documentazione                                                                                                                                                                                                                                                                                                                                                                                                          | `"https://docs.example.com"`                                      |
| `repository`  | string | URL del codice sorgente                                                                                                                                                                                                                                                                                                                                                                                                           | `"https://github.com/user/plugin"`                                |
| `license`     | string | Identificatore della licenza                                                                                                                                                                                                                                                                                                                                                                                                      | `"MIT"`, `"Apache-2.0"`                                           |
| `keywords`    | array  | Tag di scoperta                                                                                                                                                                                                                                                                                                                                                                                                                   | `["deployment", "ci-cd"]`                                         |

### Campi del percorso del componente

| Campo                   | Tipo                  | Descrizione                                                                                                                                                                    | Esempio                                              |
| :---------------------- | :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- |
| `skills`                | string\|array         | Directory di skills personalizzate contenenti `<name>/SKILL.md` (in aggiunta al valore predefinito `skills/`)                                                                  | `"./custom/skills/"`                                 |
| `commands`              | string\|array         | File di skill markdown flat personalizzati o directory (sostituisce il valore predefinito `commands/`)                                                                         | `"./custom/cmd.md"` o `["./cmd1.md"]`                |
| `agents`                | string\|array         | File di agent personalizzati (sostituisce il valore predefinito `agents/`)                                                                                                     | `"./custom/agents/reviewer.md"`                      |
| `hooks`                 | string\|array\|object | Percorsi di configurazione degli hooks o configurazione inline                                                                                                                 | `"./my-extra-hooks.json"`                            |
| `mcpServers`            | string\|array\|object | Percorsi di configurazione MCP o configurazione inline                                                                                                                         | `"./my-extra-mcp-config.json"`                       |
| `outputStyles`          | string\|array         | File/directory di stili di output personalizzati (sostituisce il valore predefinito `output-styles/`)                                                                          | `"./styles/"`                                        |
| `lspServers`            | string\|array\|object | Configurazioni [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) per l'intelligenza del codice (vai alla definizione, trova riferimenti, ecc.) | `"./.lsp.json"`                                      |
| `experimental.themes`   | string\|array         | File/directory di temi di colore (sostituisce il valore predefinito `themes/`). Vedi [Themes](#themes)                                                                         | `"./themes/"`                                        |
| `experimental.monitors` | string\|array         | Configurazioni di [Monitor](/it/tools-reference#monitor-tool) in background che si avviano automaticamente quando il plugin è attivo. Vedi [Monitors](#monitors)               | `"./monitors.json"`                                  |
| `userConfig`            | object                | Valori configurabili dall'utente richiesti al momento dell'abilitazione. Vedi [Configurazione utente](#user-configuration)                                                     | Vedi sotto                                           |
| `channels`              | array                 | Dichiarazioni di canale per l'iniezione di messaggi (stile Telegram, Slack, Discord). Vedi [Channels](#channels)                                                               | Vedi sotto                                           |
| `dependencies`          | array                 | Altri plugin richiesti da questo plugin, facoltativamente con vincoli di versione semver. Vedi [Vincola le versioni delle dipendenze del plugin](/it/plugin-dependencies)      | `[{ "name": "secrets-vault", "version": "~2.1.0" }]` |

### Componenti sperimentali

I componenti sotto la chiave `experimental`, `themes` e `monitors`, hanno uno schema del manifest che potrebbe cambiare tra le versioni mentre si stabilizzano. Il luogo in cui li dichiari è una migrazione separata: il livello superiore funziona ancora, `claude plugin validate` avvisa, e una versione futura richiederà `experimental.*`.

### Configurazione utente

Il campo `userConfig` dichiara i valori per i quali Claude Code chiede all'utente quando il plugin è abilitato. Usa questo invece di richiedere agli utenti di modificare manualmente `settings.json`.

```json theme={null}
{
  "userConfig": {
    "api_endpoint": {
      "type": "string",
      "title": "API endpoint",
      "description": "Your team's API endpoint"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "API authentication token",
      "sensitive": true
    }
  }
}
```

Le chiavi devono essere identificatori validi. Ogni opzione supporta questi campi:

| Campo         | Obbligatorio | Descrizione                                                                                          |
| :------------ | :----------- | :--------------------------------------------------------------------------------------------------- |
| `type`        | Sì           | Uno di `string`, `number`, `boolean`, `directory`, o `file`                                          |
| `title`       | Sì           | Etichetta mostrata nella finestra di dialogo di configurazione                                       |
| `description` | Sì           | Testo di aiuto mostrato sotto il campo                                                               |
| `sensitive`   | No           | Se `true`, maschera l'input e archivia il valore nell'archiviazione sicura invece di `settings.json` |
| `required`    | No           | Se `true`, la convalida non riesce quando il campo è vuoto                                           |
| `default`     | No           | Valore utilizzato quando l'utente non fornisce nulla                                                 |
| `multiple`    | No           | Per il tipo `string`, consenti un array di stringhe                                                  |
| `min` / `max` | No           | Limiti per il tipo `number`                                                                          |

Ogni valore è disponibile per la sostituzione come `${user_config.KEY}` nelle configurazioni dei server MCP e LSP, nei comandi degli hooks e nei comandi dei monitor. I valori non sensibili possono anche essere sostituiti nel contenuto delle skills e degli agents. Tutti i valori vengono esportati ai sottoprocessi del plugin come variabili di ambiente `CLAUDE_PLUGIN_OPTION_<KEY>`.

I valori non sensibili vengono archiviati in `settings.json` sotto `pluginConfigs[<plugin-id>].options`. I valori sensibili vanno al portachiavi di sistema (o `~/.claude/.credentials.json` dove il portachiavi non è disponibile). L'archiviazione del portachiavi è condivisa con i token OAuth e ha un limite totale approssimativo di 2 KB, quindi mantieni i valori sensibili piccoli.

### Channels

Il campo `channels` consente a un plugin di dichiarare uno o più canali di messaggi che iniettano contenuto nella conversazione. Ogni canale si associa a un server MCP fornito dal plugin.

```json theme={null}
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": {
          "type": "string",
          "title": "Bot token",
          "description": "Telegram bot token",
          "sensitive": true
        },
        "owner_id": {
          "type": "string",
          "title": "Owner ID",
          "description": "Your Telegram user ID"
        }
      }
    }
  ]
}
```

Il campo `server` è obbligatorio e deve corrispondere a una chiave in `mcpServers` del plugin. Il `userConfig` facoltativo per canale utilizza lo stesso schema del campo di livello superiore, consentendo al plugin di richiedere token bot o ID proprietario quando il plugin è abilitato.

### Regole del comportamento del percorso

Se un percorso personalizzato sostituisce o estende la directory predefinita del plugin dipende dal campo:

* **Sostituisce il valore predefinito**: `commands`, `agents`, `outputStyles`, `experimental.themes`, `experimental.monitors`. Ad esempio, quando il manifest specifica `commands`, la directory predefinita `commands/` non viene scansionata. Per mantenere il valore predefinito e aggiungerne altri, elencalo esplicitamente: `"commands": ["./commands/", "./extras/"]`
* **Aggiunge al valore predefinito**: `skills`. La directory predefinita `skills/` viene sempre scansionata e le directory elencate in `skills` vengono caricate insieme ad essa
* **Regole di merge proprie**: [hooks](#hooks), [MCP servers](#mcp-servers) e [LSP servers](#lsp-servers). Vedi ogni sezione per come più fonti si combinano

Quando un plugin ha sia una cartella predefinita che la chiave manifest corrispondente, Claude Code v2.1.140 e versioni successive contrassegnano la cartella ignorata in `/doctor`, `claude plugin list` e la vista dettagli `/plugin`. Il plugin continua a caricarsi utilizzando i percorsi del manifest. Nessun avviso viene mostrato quando la chiave manifest punta nella cartella predefinita, ad esempio `"commands": ["./commands/deploy.md"]`, perché la cartella è indirizzata esplicitamente in quel caso.

Per tutti i campi del percorso:

* Tutti i percorsi devono essere relativi alla radice del plugin e iniziare con `./`
* I componenti dai percorsi personalizzati utilizzano le stesse regole di denominazione e spazio dei nomi
* È possibile specificare più percorsi come array
* Quando un percorso di skill punta a una directory che contiene direttamente un `SKILL.md`, ad esempio `"skills": ["./"]` che punta alla radice del plugin, il campo frontmatter `name` in `SKILL.md` determina il nome di invocazione della skill. Questo fornisce un nome stabile indipendentemente dalla directory di installazione. Se `name` non è impostato nel frontmatter, il nome della directory viene utilizzato come fallback.

Un plugin che ha un `SKILL.md` alla sua radice, nessuna sottodirectory `skills/`, e nessun campo manifest `skills` viene caricato automaticamente come plugin a singola skill in Claude Code v2.1.142 e versioni successive. Non è necessario impostare `"skills": ["./"]` in `plugin.json` per questo layout. Il nome di invocazione della skill segue la stessa regola di cui sopra: il campo frontmatter `name`, o il nome della directory come fallback.

**Esempi di percorso**:

```json theme={null}
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### Variabili di ambiente

Claude Code fornisce tre variabili per fare riferimento ai percorsi. Tutte vengono sostituite inline ovunque appaiano nel contenuto delle skills, nel contenuto degli agents, nei comandi degli hooks, nei comandi dei monitor e nelle configurazioni dei server MCP o LSP. Tutte vengono anche esportate come variabili di ambiente ai processi degli hooks e ai sottoprocessi dei server MCP o LSP.

**`${CLAUDE_PLUGIN_ROOT}`**: il percorso assoluto della directory di installazione del tuo plugin. Usalo per fare riferimento a script, binari e file di configurazione forniti con il plugin. Nei comandi degli hooks, usa la [forma exec](/it/hooks#exec-form-and-shell-form) con `args` in modo che il percorso venga passato come un singolo argomento senza virgolette. Nei comandi degli hooks in forma shell e nei comandi dei monitor, racchiudilo tra virgolette doppie, come in `"${CLAUDE_PLUGIN_ROOT}"`. Questo percorso cambia quando il plugin viene aggiornato. La directory della versione precedente rimane su disco per circa sette giorni dopo un aggiornamento prima della pulizia, ma trattala come effimera e non scrivere stato qui.

Quando un plugin viene aggiornato a metà sessione, i comandi degli hooks, i monitor, i server MCP e i server LSP continuano a utilizzare il percorso della versione precedente. Esegui `/reload-plugins` per passare gli hooks, i server MCP e i server LSP al nuovo percorso; i monitor richiedono un riavvio della sessione.

**`${CLAUDE_PLUGIN_DATA}`**: una directory persistente per lo stato del plugin che sopravvive agli aggiornamenti. Usalo per le dipendenze installate come `node_modules` o ambienti virtuali Python, codice generato, cache e qualsiasi altro file che dovrebbe persistere tra le versioni del plugin. La directory viene creata automaticamente la prima volta che questa variabile viene referenziata.

**`${CLAUDE_PROJECT_DIR}`**: la radice del progetto. Questa è la stessa directory che gli hooks ricevono nella loro variabile `CLAUDE_PROJECT_DIR`. Usala per fare riferimento a script locali del progetto o file di configurazione. Racchiudila tra virgolette per gestire i percorsi con spazi, ad esempio `"${CLAUDE_PROJECT_DIR}/scripts/server.sh"`. I server MCP possono anche chiamare la richiesta MCP `roots/list`, che restituisce la directory da cui Claude Code è stato avviato.

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"${CLAUDE_PLUGIN_ROOT}\"/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

#### Directory di dati persistenti

La directory `${CLAUDE_PLUGIN_DATA}` si risolve in `~/.claude/plugins/data/{id}/`, dove `{id}` è l'identificatore del plugin con caratteri al di fuori di `a-z`, `A-Z`, `0-9`, `_` e `-` sostituiti da `-`. Per un plugin installato come `formatter@my-marketplace`, la directory è `~/.claude/plugins/data/formatter-my-marketplace/`.

Un uso comune è installare le dipendenze del linguaggio una volta e riutilizzarle tra le sessioni e gli aggiornamenti del plugin. Poiché la directory dei dati sopravvive a qualsiasi singola versione del plugin, un controllo dell'esistenza della directory da solo non può rilevare quando un aggiornamento cambia il manifest delle dipendenze del plugin. Il modello consigliato confronta il manifest fornito con una copia nella directory dei dati e reinstalla quando differiscono.

Questo hook `SessionStart` installa `node_modules` alla prima esecuzione e di nuovo ogni volta che un aggiornamento del plugin include un `package.json` modificato:

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

Il `diff` esce con codice diverso da zero quando la copia archiviata è mancante o differisce da quella fornita, coprendo sia la prima esecuzione che gli aggiornamenti che cambiano le dipendenze. Se `npm install` non riesce, il trailing `rm` rimuove il manifest copiato in modo che la prossima sessione riprovi.

Gli script forniti in `${CLAUDE_PLUGIN_ROOT}` possono quindi essere eseguiti contro il `node_modules` persistente:

```json theme={null}
{
  "mcpServers": {
    "routines": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "NODE_PATH": "${CLAUDE_PLUGIN_DATA}/node_modules"
      }
    }
  }
}
```

La directory dei dati viene eliminata automaticamente quando disinstalli il plugin dall'ultimo ambito in cui è installato. L'interfaccia `/plugin` mostra la dimensione della directory e chiede conferma prima di eliminare. La CLI elimina per impostazione predefinita; passa [`--keep-data`](#plugin-uninstall) per preservarla.

***

## Caching del plugin e risoluzione dei file

I plugin vengono specificati in uno di due modi:

* Tramite `claude --plugin-dir` o `claude --plugin-url`, per la durata di una sessione.
* Tramite un marketplace, installato per sessioni future.

Per motivi di sicurezza e verifica, Claude Code copia i plugin del *marketplace* nella **cache dei plugin** locale dell'utente (`~/.claude/plugins/cache`) piuttosto che usarli sul posto. Comprendere questo comportamento è importante quando si sviluppano plugin che fanno riferimento a file esterni.

Ogni versione installata è una directory separata nella cache. Quando aggiorni o disinstalli un plugin, la directory della versione precedente viene contrassegnata come orfana e rimossa automaticamente 7 giorni dopo. Il periodo di grazia consente alle sessioni di Claude Code concorrenti che hanno già caricato la versione precedente di continuare a funzionare senza errori.

Gli strumenti Glob e Grep di Claude saltano le directory delle versioni orfane durante le ricerche, quindi i risultati dei file non includono il codice del plugin obsoleto.

### Limitazioni dell'attraversamento dei percorsi

I plugin installati non possono fare riferimento a file al di fuori della loro directory. I percorsi che attraversano al di fuori della radice del plugin (come `../shared-utils`) non funzioneranno dopo l'installazione perché questi file esterni non vengono copiati nella cache.

### Condividere file all'interno di un marketplace con symlink

Se il tuo plugin ha bisogno di condividere file con altre parti dello stesso marketplace, puoi creare link simbolici all'interno della directory del tuo plugin. Il modo in cui un symlink viene gestito quando il plugin viene copiato nella cache dipende da dove si risolve il suo target:

* **All'interno della directory del plugin stesso:** il symlink viene preservato come symlink relativo nella cache, quindi continua a risolversi al target copiato in fase di esecuzione.
* **Altrove all'interno dello stesso marketplace:** il symlink viene dereferenziato. Il contenuto del target viene copiato nella cache al suo posto. Questo consente a un meta-plugin di collegare la sua directory `skills/` alle skill definite da altri plugin nel marketplace.
* **Al di fuori del marketplace:** il symlink viene saltato per motivi di sicurezza. Questo impedisce ai plugin di estrarre file arbitrari dell'host come percorsi di sistema nella cache.

Per i plugin installati con `--plugin-dir` o da un percorso locale, solo i symlink che si risolvono all'interno della directory del plugin stesso vengono preservati. Tutti gli altri vengono saltati.

Il seguente comando crea un link dall'interno di un plugin del marketplace a una skill condivisa definita da un plugin sibling. Su Windows, usa `mklink /D` da un Command Prompt elevato o abilita Developer Mode:

```bash theme={null}
ln -s ../../shared-plugin/skills/foo ./skills/foo
```

Questo fornisce flessibilità mantenendo i vantaggi di sicurezza del sistema di caching.

***

## Struttura della directory del plugin

### Layout standard del plugin

Un plugin completo segue questa struttura:

```text theme={null}
enterprise-plugin/
├── .claude-plugin/           # Directory dei metadati (opzionale)
│   └── plugin.json             # manifest del plugin
├── skills/                   # Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── commands/                 # Skills come file markdown flat
│   ├── status.md
│   └── logs.md
├── agents/                   # Definizioni dei subagent
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── output-styles/            # Definizioni dello stile di output
│   └── terse.md
├── themes/                   # Definizioni del tema colore
│   └── dracula.json
├── monitors/                 # Configurazioni dei monitor in background
│   └── monitors.json
├── hooks/                    # Configurazioni degli hook
│   ├── hooks.json           # Configurazione principale degli hook
│   └── security-hooks.json  # Hook aggiuntivi
├── bin/                      # Eseguibili del plugin aggiunti a PATH
│   └── my-tool               # Invocabile come comando bare nello strumento Bash
├── settings.json            # Impostazioni predefinite per il plugin
├── .mcp.json                # Definizioni del server MCP
├── .lsp.json                # Configurazioni del server LSP
├── scripts/                 # Script degli hook e utilità
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # File di licenza
└── CHANGELOG.md             # Cronologia delle versioni
```

<Warning>
  La directory `.claude-plugin/` contiene il file `plugin.json`. Tutte le altre directory (commands/, agents/, skills/, output-styles/, themes/, monitors/, hooks/) devono essere nella radice del plugin, non all'interno di `.claude-plugin/`.
</Warning>

Un file `CLAUDE.md` nella radice del plugin non viene caricato come contesto del progetto. I plugin contribuiscono al contesto attraverso skills, agents e hooks piuttosto che tramite CLAUDE.md. Per fornire istruzioni che si carichino nel contesto di Claude, inseritele in uno [skill](#skills).

### Riferimento delle posizioni dei file

| Componente        | Posizione predefinita        | Scopo                                                                                                                                                                                                  |
| :---------------- | :--------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Manifest**      | `.claude-plugin/plugin.json` | Metadati e configurazione del plugin (opzionale)                                                                                                                                                       |
| **Skills**        | `skills/`                    | Skills con struttura `<name>/SKILL.md`                                                                                                                                                                 |
| **Commands**      | `commands/`                  | Skills come file Markdown flat. Usa `skills/` per i nuovi plugin                                                                                                                                       |
| **Agents**        | `agents/`                    | File Markdown del subagent                                                                                                                                                                             |
| **Output styles** | `output-styles/`             | Definizioni dello stile di output                                                                                                                                                                      |
| **Themes**        | `themes/`                    | Definizioni del tema colore                                                                                                                                                                            |
| **Hooks**         | `hooks/hooks.json`           | Configurazione degli hook                                                                                                                                                                              |
| **MCP servers**   | `.mcp.json`                  | Definizioni del server MCP                                                                                                                                                                             |
| **LSP servers**   | `.lsp.json`                  | Configurazioni del server di linguaggio                                                                                                                                                                |
| **Monitors**      | `monitors/monitors.json`     | Configurazioni dei monitor in background                                                                                                                                                               |
| **Executables**   | `bin/`                       | Eseguibili aggiunti al `PATH` dello strumento Bash. I file qui sono invocabili come comandi bare in qualsiasi chiamata dello strumento Bash mentre il plugin è abilitato                               |
| **Settings**      | `settings.json`              | Configurazione predefinita applicata quando il plugin è abilitato. Attualmente sono supportate solo le chiavi [`agent`](/it/sub-agents) e [`subagentStatusLine`](/it/statusline#subagent-status-lines) |

***

## Riferimento dei comandi CLI

Claude Code fornisce comandi CLI per la gestione non interattiva dei plugin, utile per scripting e automazione.

### plugin install

Installa un plugin dai marketplace disponibili.

```bash theme={null}
claude plugin install <plugin> [options]
```

**Argomenti:**

* `<plugin>`: Nome del plugin o `plugin-name@marketplace-name` per un marketplace specifico

**Opzioni:**

| Opzione               | Descrizione                                           | Predefinito |
| :-------------------- | :---------------------------------------------------- | :---------- |
| `-s, --scope <scope>` | Ambito di installazione: `user`, `project`, o `local` | `user`      |
| `-h, --help`          | Visualizza la guida per il comando                    |             |

L'ambito determina quale file di impostazioni viene aggiunto al plugin installato. Ad esempio, `--scope project` scrive in `enabledPlugins` in .claude/settings.json, rendendo il plugin disponibile a tutti coloro che clonano il repository del progetto.

**Esempi:**

```bash theme={null}
# Installa nell'ambito utente (predefinito)
claude plugin install formatter@my-marketplace

# Installa nell'ambito del progetto (condiviso con il team)
claude plugin install formatter@my-marketplace --scope project

# Installa nell'ambito locale (gitignored)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

Rimuovi un plugin installato.

```bash theme={null}
claude plugin uninstall <plugin> [options]
```

**Argomenti:**

* `<plugin>`: Nome del plugin o `plugin-name@marketplace-name`

**Opzioni:**

| Opzione               | Descrizione                                                                                                      | Predefinito |
| :-------------------- | :--------------------------------------------------------------------------------------------------------------- | :---------- |
| `-s, --scope <scope>` | Disinstalla dall'ambito: `user`, `project`, o `local`                                                            | `user`      |
| `--keep-data`         | Preserva la [directory di dati persistenti](#persistent-data-directory) del plugin                               |             |
| `--prune`             | Rimuovi anche le dipendenze auto-installate che nessun altro plugin richiede. Vedi [plugin prune](#plugin-prune) |             |
| `-y, --yes`           | Salta il prompt di conferma `--prune`. Richiesto quando stdin non è un TTY                                       |             |
| `-h, --help`          | Visualizza la guida per il comando                                                                               |             |

**Alias:** `remove`, `rm`

Per impostazione predefinita, la disinstallazione dall'ultimo ambito rimanente elimina anche la directory `${CLAUDE_PLUGIN_DATA}` del plugin. Usa `--keep-data` per preservarla, ad esempio quando reinstalli dopo aver testato una nuova versione.

### plugin prune

Rimuovi le dipendenze auto-installate dei plugin che non sono più richieste da nessun plugin installato. Le dipendenze che Claude Code ha incluso per soddisfare il campo [`dependencies`](/it/plugin-dependencies) di un altro plugin vengono rimosse; i plugin che hai installato direttamente non vengono mai toccati.

```bash theme={null}
claude plugin prune [options]
```

**Opzioni:**

| Opzione               | Descrizione                                                      | Predefinito |
| :-------------------- | :--------------------------------------------------------------- | :---------- |
| `-s, --scope <scope>` | Pulisci all'ambito: `user`, `project`, o `local`                 | `user`      |
| `--dry-run`           | Elenca cosa verrebbe rimosso senza rimuovere nulla               |             |
| `-y, --yes`           | Salta il prompt di conferma. Richiesto quando stdin non è un TTY |             |
| `-h, --help`          | Visualizza la guida per il comando                               |             |

**Alias:** `autoremove`

Il comando elenca le dipendenze orfane e chiede conferma prima di rimuoverle. Per rimuovere un plugin e pulire le sue dipendenze in un unico passaggio, esegui `claude plugin uninstall <plugin> --prune`.

<Note>
  `claude plugin prune` richiede Claude Code v2.1.121 o successivo.
</Note>

### plugin enable

Abilita un plugin disabilitato. Se il plugin dichiara [dipendenze](/it/plugin-dependencies), Claude Code le abilita transitivamente nello stesso ambito, e il comando fallisce quando una dipendenza non è installata.

```bash theme={null}
claude plugin enable <plugin> [options]
```

**Argomenti:**

* `<plugin>`: Nome del plugin o `plugin-name@marketplace-name`

**Opzioni:**

| Opzione               | Descrizione                                       | Predefinito |
| :-------------------- | :------------------------------------------------ | :---------- |
| `-s, --scope <scope>` | Ambito da abilitare: `user`, `project`, o `local` | `user`      |
| `-h, --help`          | Visualizza la guida per il comando                |             |

### plugin disable

Disabilita un plugin senza disinstallarlo. Fallisce quando un altro plugin abilitato [dipende da](/it/plugin-dependencies#enable-or-disable-a-plugin-with-dependencies) il target. Il messaggio di errore include un comando concatenato che disabilita prima ogni dipendente.

```bash theme={null}
claude plugin disable <plugin> [options]
```

**Argomenti:**

* `<plugin>`: Nome del plugin o `plugin-name@marketplace-name`

**Opzioni:**

| Opzione               | Descrizione                                          | Predefinito |
| :-------------------- | :--------------------------------------------------- | :---------- |
| `-s, --scope <scope>` | Ambito da disabilitare: `user`, `project`, o `local` | `user`      |
| `-h, --help`          | Visualizza la guida per il comando                   |             |

### plugin update

Aggiorna un plugin all'ultima versione.

```bash theme={null}
claude plugin update <plugin> [options]
```

**Argomenti:**

* `<plugin>`: Nome del plugin o `plugin-name@marketplace-name`

**Opzioni:**

| Opzione               | Descrizione                                                   | Predefinito |
| :-------------------- | :------------------------------------------------------------ | :---------- |
| `-s, --scope <scope>` | Ambito da aggiornare: `user`, `project`, `local`, o `managed` | `user`      |
| `-h, --help`          | Visualizza la guida per il comando                            |             |

***

### plugin list

Elenca i plugin installati con la loro versione, marketplace di origine e stato di abilitazione.

```bash theme={null}
claude plugin list [options]
```

**Opzioni:**

| Opzione       | Descrizione                                                   | Predefinito |
| :------------ | :------------------------------------------------------------ | :---------- |
| `--json`      | Output come JSON                                              |             |
| `--available` | Includi plugin disponibili dai marketplace. Richiede `--json` |             |
| `-h, --help`  | Visualizza la guida per il comando                            |             |

### plugin details

Mostra l'inventario dei componenti di un plugin e il costo dei token previsto. L'output elenca tutti i componenti che il plugin contribuisce, raggruppati come Skills, Agents, Hooks, server MCP e server LSP, insieme a una stima di quanti token aggiunge a ogni sessione. Il gruppo Skills include sia le voci `skills/` che `commands/`.

```bash theme={null}
claude plugin details <name>
```

**Argomenti:**

* `<name>`: Nome del plugin o `plugin-name@marketplace-name`

**Opzioni:**

| Opzione      | Descrizione                        | Predefinito |
| :----------- | :--------------------------------- | :---------- |
| `-h, --help` | Visualizza la guida per il comando |             |

L'output mostra due cifre di costo per ogni componente:

* **Always-on:** token aggiunti a ogni sessione dal testo dell'elenco del plugin, come descrizioni di skill, descrizioni di agent e nomi di comandi, indipendentemente dal fatto che un componente si attivi.
* **On-invoke:** token che un componente costa quando si attiva. Mostrato per componente, non come totale del plugin, perché una sessione tipica invoca solo un sottoinsieme di componenti.

Questo esempio mostra come appare l'output per un plugin con due skill:

```
security-guidance 1.2.0
  Real-time security analysis for Claude Code sessions
  Source: security-guidance@claude-code-marketplace

Component inventory
  Skills (2)  scan-dependencies, review-changes
  Agents (0)
  Hooks (1)  (harness-only — no model context cost)
  MCP servers (0)
  LSP servers (0)

Projected token cost
  Always-on:   ~180 tok   added to every session

Per-component (rounded)
  component            always-on  on-invoke
  scan-dependencies        ~100      ~2400
  review-changes            ~80      ~1800

  On-invoke cost is paid each time a skill or agent fires.
  Token counts are estimates and may differ from actual usage.
```

Il totale always-on viene calcolato tramite l'API `count_tokens` per il tuo modello attivo. I numeri per componente sono proporzionalmente scalati da quel totale. Se l'API non è raggiungibile, il comando ricade su una stima basata sui caratteri.

### plugin tag

Crea un tag git di rilascio per il plugin nella directory corrente. Esegui dall'interno della cartella del plugin. Vedi [Tag plugin releases](/it/plugin-dependencies#tag-plugin-releases-for-version-resolution).

```bash theme={null}
claude plugin tag [options]
```

**Opzioni:**

| Opzione       | Descrizione                                                          | Predefinito |
| :------------ | :------------------------------------------------------------------- | :---------- |
| `--push`      | Esegui il push del tag al repository remoto dopo averlo creato       |             |
| `--dry-run`   | Stampa cosa verrebbe taggato senza creare il tag                     |             |
| `-f, --force` | Crea il tag anche se l'albero di lavoro è sporco o il tag esiste già |             |
| `-h, --help`  | Visualizza la guida per il comando                                   |             |

***

## Strumenti di debug e sviluppo

### Comandi di debug

Usa `claude --debug` per vedere i dettagli del caricamento del plugin:

Questo mostra:

* Quali plugin vengono caricati
* Eventuali errori nei manifest del plugin
* Registrazione di skill, agent e hook
* Inizializzazione del server MCP

### Problemi comuni

| Problema                            | Causa                               | Soluzione                                                                                                                                                                      |
| :---------------------------------- | :---------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Plugin non caricato                 | `plugin.json` non valido            | Esegui `claude plugin validate` o `/plugin validate` per controllare `plugin.json`, il frontmatter di skill/agent/command e `hooks/hooks.json` per errori di sintassi e schema |
| Skills non visualizzate             | Struttura della directory errata    | Assicurati che `skills/` o `commands/` sia alla radice del plugin, non all'interno di `.claude-plugin/`                                                                        |
| Hooks non attivati                  | Script non eseguibile               | Esegui `chmod +x script.sh`                                                                                                                                                    |
| Server MCP non riesce               | `${CLAUDE_PLUGIN_ROOT}` mancante    | Usa la variabile per tutti i percorsi del plugin                                                                                                                               |
| Errori di percorso                  | Percorsi assoluti utilizzati        | Tutti i percorsi devono essere relativi e iniziare con `./`                                                                                                                    |
| LSP `Executable not found in $PATH` | Server di linguaggio non installato | Installa il binario (ad es., `npm install -g typescript-language-server typescript`)                                                                                           |

### Messaggi di errore di esempio

**Errori di convalida del manifest**:

* `Invalid JSON syntax: Unexpected token } in JSON at position 142`: controlla la mancanza di virgole, virgole extra o stringhe non quotate
* `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required`: un campo obbligatorio è mancante
* `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`: errore di sintassi JSON

**Errori di caricamento del plugin**:

* `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`: il percorso del comando esiste ma non contiene file di comando validi
* `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`: il percorso `source` in marketplace.json punta a una directory inesistente
* `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`: rimuovi le definizioni di componenti duplicate o rimuovi `strict: false` nella voce del marketplace

### Risoluzione dei problemi degli hook

**Script dell'hook non in esecuzione**:

1. Controlla che lo script sia eseguibile: `chmod +x ./scripts/your-script.sh`
2. Verifica la riga shebang: La prima riga dovrebbe essere `#!/bin/bash` o `#!/usr/bin/env bash`
3. Controlla che il percorso usi `${CLAUDE_PLUGIN_ROOT}`: `"command": "${CLAUDE_PLUGIN_ROOT}/scripts/your-script.sh"`
4. Testa lo script manualmente: `./scripts/your-script.sh`

**Hook non attivato su eventi previsti**:

1. Verifica che il nome dell'evento sia corretto (sensibile alle maiuscole): `PostToolUse`, non `postToolUse`
2. Controlla che il pattern del matcher corrisponda ai tuoi tool: `"matcher": "Write|Edit"` per le operazioni sui file
3. Conferma che il tipo di hook sia valido: `command`, `http`, `mcp_tool`, `prompt`, o `agent`

### Risoluzione dei problemi del server MCP

**Server non si avvia**:

1. Controlla che il comando esista e sia eseguibile
2. Verifica che tutti i percorsi utilizzino la variabile `${CLAUDE_PLUGIN_ROOT}`
3. Controlla i log del server MCP: `claude --debug` mostra gli errori di inizializzazione
4. Testa il server manualmente al di fuori di Claude Code

**Strumenti del server non visualizzati**:

1. Assicurati che il server sia configurato correttamente in `.mcp.json` o `plugin.json`
2. Verifica che il server implementi correttamente il protocollo MCP
3. Controlla i timeout di connessione nell'output di debug

### Errori di struttura della directory

**Sintomi**: Il plugin si carica ma i componenti (skills, agents, hooks) sono mancanti.

**Struttura corretta**: I componenti devono essere nella radice del plugin, non all'interno di `.claude-plugin/`. Solo `plugin.json` appartiene a `.claude-plugin/`.

```text theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← Solo manifest qui
├── commands/            ← A livello di radice
├── agents/              ← A livello di radice
└── hooks/               ← A livello di radice
```

Se i tuoi componenti sono all'interno di `.claude-plugin/`, spostali nella radice del plugin.

**Checklist di debug**:

1. Esegui `claude --debug` e cerca i messaggi "loading plugin"
2. Controlla che ogni directory di componenti sia elencata nell'output di debug
3. Verifica che i permessi dei file consentano la lettura dei file del plugin

***

## Riferimento di distribuzione e versioning

### Gestione della versione

Claude Code utilizza la versione del plugin come chiave di cache che determina se un aggiornamento è disponibile. Quando esegui `/plugin update` o l'aggiornamento automatico si attiva, Claude Code calcola la versione corrente e salta l'aggiornamento se corrisponde a quella già installata.

La versione viene risolta dal primo di questi che è impostato:

1. Il campo `version` nel `plugin.json` del plugin
2. Il campo `version` nella voce del marketplace del plugin in `marketplace.json`
3. Lo SHA del commit git del plugin, per le fonti `github`, `url`, `git-subdir` e relative-path in un marketplace ospitato su git
4. `unknown`, per le fonti `npm` o le directory locali non all'interno di un repository git

Questo ti offre due modi per versionare un plugin:

| Approccio               | Come                                                                 | Comportamento dell'aggiornamento                                                                                                                                                       | Migliore per                                    |
| :---------------------- | :------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------- |
| **Versione esplicita**  | Imposta `"version": "2.1.0"` in `plugin.json`                        | Gli utenti ricevono aggiornamenti solo quando aumenti questo campo. Spingere nuovi commit senza aumentarlo non ha effetto, e `/plugin update` segnala "already at the latest version". | Plugin pubblicati con cicli di rilascio stabili |
| **Versione Commit-SHA** | Ometti `version` sia da `plugin.json` che dalla voce del marketplace | Gli utenti ricevono aggiornamenti ad ogni nuovo commit alla fonte git del plugin                                                                                                       | Plugin interni o di team in sviluppo attivo     |

<Warning>
  Se imposti `version` in `plugin.json`, devi aumentarlo ogni volta che desideri che gli utenti ricevano le modifiche. Spingere nuovi commit da solo non è sufficiente, perché Claude Code vede la stessa stringa di versione e mantiene la copia in cache. Se stai iterando rapidamente, lascia `version` non impostato in modo che lo SHA del commit git venga utilizzato invece.
</Warning>

Se utilizzi versioni esplicite, segui il [versionamento semantico](https://semver.org) (`MAJOR.MINOR.PATCH`): aumenta MAJOR per modifiche di rilievo, MINOR per nuove funzionalità, PATCH per correzioni di bug. Documenta le modifiche in un `CHANGELOG.md`.

***

## Vedi anche

* [Plugin](/it/plugins) - Tutorial e utilizzo pratico
* [Marketplace dei plugin](/it/plugin-marketplaces) - Creazione e gestione dei marketplace
* [Skills](/it/skills) - Dettagli dello sviluppo delle skill
* [Subagents](/it/sub-agents) - Configurazione e capacità dell'agent
* [Hooks](/it/hooks) - Gestione degli eventi e automazione
* [MCP](/it/mcp) - Integrazione di strumenti esterni
* [Impostazioni](/it/settings) - Opzioni di configurazione per i plugin
