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

**Posizione**: Directory `skills/` o `commands/` nella radice del plugin

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
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

I plugin hooks rispondono agli stessi eventi del ciclo di vita degli [hooks definiti dall'utente](/it/hooks):

| Event                | When it fires                                                                                                                                          |
| :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                                       |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                                   |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`  | When a permission dialog appears                                                                                                                       |
| `PermissionDenied`   | When a tool call is denied by the auto mode classifier. Return `{retry: true}` to tell the model it may retry the denied tool call                     |
| `PostToolUse`        | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure` | After a tool call fails                                                                                                                                |
| `Notification`       | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`      | When a subagent is spawned                                                                                                                             |
| `SubagentStop`       | When a subagent finishes                                                                                                                               |
| `TaskCreated`        | When a task is being created via `TaskCreate`                                                                                                          |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                               |
| `Stop`               | When Claude finishes responding                                                                                                                        |
| `StopFailure`        | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`       | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`         | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`        | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`         | Before context compaction                                                                                                                              |
| `PostCompact`        | After context compaction completes                                                                                                                     |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`         | When a session terminates                                                                                                                              |

**Tipi di hook**:

* `command`: esegui comandi shell o script
* `http`: invia l'evento JSON come richiesta POST a un URL
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

| Plugin           | Server di linguaggio       | Comando di installazione                                                                        |
| :--------------- | :------------------------- | :---------------------------------------------------------------------------------------------- |
| `pyright-lsp`    | Pyright (Python)           | `pip install pyright` o `npm install -g pyright`                                                |
| `typescript-lsp` | TypeScript Language Server | `npm install -g typescript-language-server typescript`                                          |
| `rust-lsp`       | rust-analyzer              | [Vedi installazione di rust-analyzer](https://rust-analyzer.github.io/manual.html#installation) |

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
    "command": "${CLAUDE_PLUGIN_ROOT}/scripts/poll-deploy.sh ${user_config.api_endpoint}",
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

Per dichiarare monitor inline, imposta la chiave `monitors` in `plugin.json` sullo stesso array. Per caricare da un percorso non predefinito, imposta `monitors` su una stringa di percorso relativo come `"./config/monitors.json"`.

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

Il valore `command` supporta le stesse [sostituzioni di variabili](#environment-variables) delle configurazioni dei server MCP e LSP: `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${user_config.*}` e qualsiasi `${ENV_VAR}` dall'ambiente. Prefissa il comando con `cd "${CLAUDE_PLUGIN_ROOT}" && ` se lo script ha bisogno di essere eseguito dalla directory del plugin stesso.

La disabilitazione di un plugin a metà sessione non interrompe i monitor già in esecuzione. Si interrompono quando la sessione termina.

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
  "agents": "./custom/agents/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json",
  "monitors": "./monitors.json",
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

### Campi di metadati

| Campo         | Tipo   | Descrizione                                                                                                                     | Esempio                                            |
| :------------ | :----- | :------------------------------------------------------------------------------------------------------------------------------ | :------------------------------------------------- |
| `version`     | string | Versione semantica. Se impostata anche nella voce del marketplace, `plugin.json` ha priorità. Devi impostarla in un solo posto. | `"2.1.0"`                                          |
| `description` | string | Breve spiegazione dello scopo del plugin                                                                                        | `"Deployment automation tools"`                    |
| `author`      | object | Informazioni sull'autore                                                                                                        | `{"name": "Dev Team", "email": "dev@company.com"}` |
| `homepage`    | string | URL della documentazione                                                                                                        | `"https://docs.example.com"`                       |
| `repository`  | string | URL del codice sorgente                                                                                                         | `"https://github.com/user/plugin"`                 |
| `license`     | string | Identificatore della licenza                                                                                                    | `"MIT"`, `"Apache-2.0"`                            |
| `keywords`    | array  | Tag di scoperta                                                                                                                 | `["deployment", "ci-cd"]`                          |

### Campi del percorso del componente

| Campo          | Tipo                  | Descrizione                                                                                                                                                                    | Esempio                                              |
| :------------- | :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- |
| `skills`       | string\|array         | Directory di skills personalizzate contenenti `<name>/SKILL.md` (sostituisce il valore predefinito `skills/`)                                                                  | `"./custom/skills/"`                                 |
| `commands`     | string\|array         | File di skill markdown flat personalizzati o directory (sostituisce il valore predefinito `commands/`)                                                                         | `"./custom/cmd.md"` o `["./cmd1.md"]`                |
| `agents`       | string\|array         | File di agent personalizzati (sostituisce il valore predefinito `agents/`)                                                                                                     | `"./custom/agents/reviewer.md"`                      |
| `hooks`        | string\|array\|object | Percorsi di configurazione degli hook o configurazione inline                                                                                                                  | `"./my-extra-hooks.json"`                            |
| `mcpServers`   | string\|array\|object | Percorsi di configurazione MCP o configurazione inline                                                                                                                         | `"./my-extra-mcp-config.json"`                       |
| `outputStyles` | string\|array         | File/directory di stili di output personalizzati (sostituisce il valore predefinito `output-styles/`)                                                                          | `"./styles/"`                                        |
| `lspServers`   | string\|array\|object | Configurazioni [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) per l'intelligenza del codice (vai alla definizione, trova riferimenti, ecc.) | `"./.lsp.json"`                                      |
| `monitors`     | string\|array         | Configurazioni di [Monitor](/it/tools-reference#monitor-tool) in background che si avviano automaticamente quando il plugin è attivo. Vedi [Monitors](#monitors)               | `"./monitors.json"`                                  |
| `userConfig`   | object                | Valori configurabili dall'utente richiesti al momento dell'abilitazione. Vedi [Configurazione utente](#user-configuration)                                                     | Vedi sotto                                           |
| `channels`     | array                 | Dichiarazioni di canale per l'iniezione di messaggi (stile Telegram, Slack, Discord). Vedi [Canali](#channels)                                                                 | Vedi sotto                                           |
| `dependencies` | array                 | Altri plugin richiesti da questo plugin, facoltativamente con vincoli di versione semver. Vedi [Vincola le versioni delle dipendenze del plugin](/it/plugin-dependencies)      | `[{ "name": "secrets-vault", "version": "~2.1.0" }]` |

### Configurazione utente

Il campo `userConfig` dichiara i valori per i quali Claude Code chiede all'utente quando il plugin è abilitato. Usa questo invece di richiedere agli utenti di modificare manualmente `settings.json`.

```json theme={null}
{
  "userConfig": {
    "api_endpoint": {
      "description": "L'endpoint API del tuo team",
      "sensitive": false
    },
    "api_token": {
      "description": "Token di autenticazione API",
      "sensitive": true
    }
  }
}
```

Le chiavi devono essere identificatori validi. Ogni valore è disponibile per la sostituzione come `${user_config.KEY}` nelle configurazioni dei server MCP e LSP, nei comandi degli hook, nei comandi dei monitor e (solo per i valori non sensibili) nel contenuto delle skills e degli agents. I valori vengono anche esportati ai sottoprocessi del plugin come variabili di ambiente `CLAUDE_PLUGIN_OPTION_<KEY>`.

I valori non sensibili vengono archiviati in `settings.json` sotto `pluginConfigs[<plugin-id>].options`. I valori sensibili vanno al portachiavi di sistema (o `~/.claude/.credentials.json` dove il portachiavi non è disponibile). L'archiviazione del portachiavi è condivisa con i token OAuth e ha un limite totale approssimativo di 2 KB, quindi mantieni i valori sensibili piccoli.

### Canali

Il campo `channels` consente a un plugin di dichiarare uno o più canali di messaggi che iniettano contenuto nella conversazione. Ogni canale si associa a un server MCP fornito dal plugin.

```json theme={null}
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": { "description": "Token bot Telegram", "sensitive": true },
        "owner_id": { "description": "Il tuo ID utente Telegram", "sensitive": false }
      }
    }
  ]
}
```

Il campo `server` è obbligatorio e deve corrispondere a una chiave in `mcpServers` del plugin. Il `userConfig` facoltativo per canale utilizza lo stesso schema del campo di livello superiore, consentendo al plugin di richiedere token bot o ID proprietario quando il plugin è abilitato.

### Regole del comportamento del percorso

Per `skills`, `commands`, `agents`, `outputStyles` e `monitors`, un percorso personalizzato sostituisce il valore predefinito. Se il manifest specifica `skills`, la directory predefinita `skills/` non viene scansionata; se specifica `monitors`, il valore predefinito `monitors/monitors.json` non viene caricato. [Hooks](#hooks), [MCP servers](#mcp-servers) e [LSP servers](#lsp-servers) hanno semantica diversa per gestire più fonti.

* Tutti i percorsi devono essere relativi alla radice del plugin e iniziare con `./`
* I componenti dai percorsi personalizzati utilizzano le stesse regole di denominazione e spazio dei nomi
* È possibile specificare più percorsi come array
* Per mantenere la directory predefinita e aggiungere più percorsi per skills, commands, agents o output styles, includi il valore predefinito nel tuo array: `"skills": ["./skills/", "./extras/"]`
* Quando un percorso di skill punta a una directory che contiene direttamente un `SKILL.md`, ad esempio `"skills": ["./"]` che punta alla radice del plugin, il campo frontmatter `name` in `SKILL.md` determina il nome di invocazione della skill. Questo fornisce un nome stabile indipendentemente dalla directory di installazione. Se `name` non è impostato nel frontmatter, il nome della directory viene utilizzato come fallback.

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

Claude Code fornisce due variabili per fare riferimento ai percorsi del plugin. Entrambe vengono sostituite inline ovunque appaiano nel contenuto delle skills, nel contenuto degli agents, nei comandi degli hook, nei comandi dei monitor e nelle configurazioni dei server MCP o LSP. Entrambe vengono anche esportate come variabili di ambiente ai processi degli hook e ai sottoprocessi dei server MCP o LSP.

**`${CLAUDE_PLUGIN_ROOT}`**: il percorso assoluto della directory di installazione del tuo plugin. Usalo per fare riferimento a script, binari e file di configurazione forniti con il plugin. Questo percorso cambia quando il plugin viene aggiornato, quindi i file che scrivi qui non sopravvivono a un aggiornamento.

**`${CLAUDE_PLUGIN_DATA}`**: una directory persistente per lo stato del plugin che sopravvive agli aggiornamenti. Usalo per le dipendenze installate come `node_modules` o ambienti virtuali Python, codice generato, cache e qualsiasi altro file che dovrebbe persistere tra le versioni del plugin. La directory viene creata automaticamente la prima volta che questa variabile viene referenziata.

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
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

* Tramite `claude --plugin-dir`, per la durata di una sessione.
* Tramite un marketplace, installato per sessioni future.

Per motivi di sicurezza e verifica, Claude Code copia i plugin del *marketplace* nella **cache dei plugin** locale dell'utente (`~/.claude/plugins/cache`) piuttosto che usarli sul posto. Comprendere questo comportamento è importante quando si sviluppano plugin che fanno riferimento a file esterni.

Ogni versione installata è una directory separata nella cache. Quando aggiorni o disinstalli un plugin, la directory della versione precedente viene contrassegnata come orfana e rimossa automaticamente 7 giorni dopo. Il periodo di grazia consente alle sessioni di Claude Code concorrenti che hanno già caricato la versione precedente di continuare a funzionare senza errori.

Gli strumenti Glob e Grep di Claude saltano le directory delle versioni orfane durante le ricerche, quindi i risultati dei file non includono il codice del plugin obsoleto.

### Limitazioni dell'attraversamento dei percorsi

I plugin installati non possono fare riferimento a file al di fuori della loro directory. I percorsi che attraversano al di fuori della radice del plugin (come `../shared-utils`) non funzioneranno dopo l'installazione perché questi file esterni non vengono copiati nella cache.

### Lavorare con dipendenze esterne

Se il tuo plugin ha bisogno di accedere a file al di fuori della sua directory, puoi creare link simbolici a file esterni all'interno della directory del tuo plugin. I symlink vengono preservati nella cache piuttosto che dereferenziati e si risolvono al loro target in fase di esecuzione. Il seguente comando crea un link dall'interno della directory del tuo plugin a una posizione di utilità condivise:

```bash theme={null}
ln -s /path/to/shared-utils ./shared-utils
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
  La directory `.claude-plugin/` contiene il file `plugin.json`. Tutte le altre directory (commands/, agents/, skills/, output-styles/, monitors/, hooks/) devono essere nella radice del plugin, non all'interno di `.claude-plugin/`.
</Warning>

### Riferimento delle posizioni dei file

| Componente        | Posizione predefinita        | Scopo                                                                                                                                                                                                  |
| :---------------- | :--------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Manifest**      | `.claude-plugin/plugin.json` | Metadati e configurazione del plugin (opzionale)                                                                                                                                                       |
| **Skills**        | `skills/`                    | Skills con struttura `<name>/SKILL.md`                                                                                                                                                                 |
| **Commands**      | `commands/`                  | Skills come file Markdown flat. Usa `skills/` per i nuovi plugin                                                                                                                                       |
| **Agents**        | `agents/`                    | File Markdown del subagent                                                                                                                                                                             |
| **Output styles** | `output-styles/`             | Definizioni dello stile di output                                                                                                                                                                      |
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

| Opzione               | Descrizione                                                                        | Predefinito |
| :-------------------- | :--------------------------------------------------------------------------------- | :---------- |
| `-s, --scope <scope>` | Disinstalla dall'ambito: `user`, `project`, o `local`                              | `user`      |
| `--keep-data`         | Preserva la [directory di dati persistenti](#persistent-data-directory) del plugin |             |
| `-h, --help`          | Visualizza la guida per il comando                                                 |             |

**Alias:** `remove`, `rm`

Per impostazione predefinita, la disinstallazione dall'ultimo ambito rimanente elimina anche la directory `${CLAUDE_PLUGIN_DATA}` del plugin. Usa `--keep-data` per preservarla, ad esempio quando reinstalli dopo aver testato una nuova versione.

### plugin enable

Abilita un plugin disabilitato.

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

Disabilita un plugin senza disinstallarlo.

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
3. Conferma che il tipo di hook sia valido: `command`, `http`, `prompt`, o `agent`

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

Segui il versionamento semantico per i rilasci del plugin:

```json theme={null}
{
  "name": "my-plugin",
  "version": "2.1.0"
}
```

**Formato della versione**: `MAJOR.MINOR.PATCH`

* **MAJOR**: Modifiche di rilievo (modifiche API incompatibili)
* **MINOR**: Nuove funzionalità (aggiunte compatibili con le versioni precedenti)
* **PATCH**: Correzioni di bug (correzioni compatibili con le versioni precedenti)

**Best practice**:

* Inizia con `1.0.0` per il tuo primo rilascio stabile
* Aggiorna la versione in `plugin.json` prima di distribuire le modifiche
* Documenta le modifiche in un file `CHANGELOG.md`
* Usa versioni pre-release come `2.0.0-beta.1` per i test

<Warning>
  Claude Code utilizza la versione per determinare se aggiornare il tuo plugin. Se modifichi il codice del tuo plugin ma non aumenti la versione in `plugin.json`, gli utenti esistenti del tuo plugin non vedranno le tue modifiche a causa del caching.

  Se il tuo plugin si trova all'interno di una directory [marketplace](/it/plugin-marketplaces), puoi gestire la versione tramite `marketplace.json` e omettere il campo `version` da `plugin.json`.
</Warning>

***

## Vedi anche

* [Plugin](/it/plugins) - Tutorial e utilizzo pratico
* [Marketplace dei plugin](/it/plugin-marketplaces) - Creazione e gestione dei marketplace
* [Skills](/it/skills) - Dettagli dello sviluppo delle skill
* [Subagents](/it/sub-agents) - Configurazione e capacità dell'agent
* [Hooks](/it/hooks) - Gestione degli eventi e automazione
* [MCP](/it/mcp) - Integrazione di strumenti esterni
* [Impostazioni](/it/settings) - Opzioni di configurazione per i plugin
