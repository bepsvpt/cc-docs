> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Riferimento dei plugin

> Riferimento tecnico completo per il sistema di plugin di Claude Code, inclusi schemi, comandi CLI e specifiche dei componenti.

<Tip>
  Stai cercando di installare plugin? Vedi [Scopri e installa plugin](/it/discover-plugins). Per creare plugin, vedi [Plugin](/it/plugins). Per distribuire plugin, vedi [Marketplace dei plugin](/it/plugin-marketplaces).
</Tip>

Questo riferimento fornisce specifiche tecniche complete per il sistema di plugin di Claude Code, inclusi schemi dei componenti, comandi CLI e strumenti di sviluppo.

Un **plugin** è una directory autonoma di componenti che estende Claude Code con funzionalità personalizzate. I componenti del plugin includono skills, agents, hooks, MCP servers e LSP servers.

## Riferimento dei componenti del plugin

### Skills

I plugin aggiungono skills a Claude Code, creando scorciatoie `/name` che Lei o Claude potete invocare.

**Posizione**: Directory `skills/` o `commands/` nella radice del plugin

**Formato file**: Le skills sono directory con `SKILL.md`; i comandi sono semplici file markdown

**Struttura della skill**:

```text  theme={null}
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

```markdown  theme={null}
---
name: agent-name
description: In cosa si specializza questo agent e quando Claude dovrebbe invocarlo
---

Prompt di sistema dettagliato per l'agent che descrive il suo ruolo, competenza e comportamento.
```

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

```json  theme={null}
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

**Eventi disponibili**:

* `PreToolUse`: Prima che Claude usi qualsiasi tool
* `PostToolUse`: Dopo che Claude ha usato con successo qualsiasi tool
* `PostToolUseFailure`: Dopo che l'esecuzione del tool di Claude non riesce
* `PermissionRequest`: Quando viene mostrata una finestra di dialogo di autorizzazione
* `UserPromptSubmit`: Quando l'utente invia un prompt
* `Notification`: Quando Claude Code invia notifiche
* `Stop`: Quando Claude tenta di fermarsi
* `SubagentStart`: Quando un subagent viene avviato
* `SubagentStop`: Quando un subagent tenta di fermarsi
* `SessionStart`: All'inizio delle sessioni
* `SessionEnd`: Alla fine delle sessioni
* `TeammateIdle`: Quando un compagno di squadra di un team di agent sta per andare inattivo
* `TaskCompleted`: Quando un'attività viene contrassegnata come completata
* `PreCompact`: Prima che la cronologia della conversazione venga compattata

**Tipi di hook**:

* `command`: Esegui comandi shell o script
* `prompt`: Valuta un prompt con un LLM (usa il placeholder `$ARGUMENTS` per il contesto)
* `agent`: Esegui un verificatore agentico con strumenti per attività di verifica complesse

### MCP servers

I plugin possono raggruppare server Model Context Protocol (MCP) per connettere Claude Code con strumenti e servizi esterni.

**Posizione**: `.mcp.json` nella radice del plugin, o inline in plugin.json

**Formato**: Configurazione standard del server MCP

**Configurazione del server MCP**:

```json  theme={null}
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

I plugin possono fornire server [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) per dare a Claude intelligenza del codice in tempo reale mentre lavora sul tuo codebase.

L'integrazione LSP fornisce:

* **Diagnostica istantanea**: Claude vede errori e avvisi immediatamente dopo ogni modifica
* **Navigazione del codice**: vai alla definizione, trova riferimenti e informazioni al passaggio del mouse
* **Consapevolezza del linguaggio**: informazioni sul tipo e documentazione per i simboli del codice

**Posizione**: `.lsp.json` nella radice del plugin, o inline in `plugin.json`

**Formato**: Configurazione JSON che mappa i nomi dei server di linguaggio alle loro configurazioni

**Formato del file `.lsp.json`**:

```json  theme={null}
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

```json  theme={null}
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

```json  theme={null}
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
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
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

| Campo          | Tipo                  | Descrizione                                                                                                                                                                    | Esempio                               |
| :------------- | :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------ |
| `commands`     | string\|array         | File/directory di comandi aggiuntivi                                                                                                                                           | `"./custom/cmd.md"` o `["./cmd1.md"]` |
| `agents`       | string\|array         | File di agent aggiuntivi                                                                                                                                                       | `"./custom/agents/reviewer.md"`       |
| `skills`       | string\|array         | Directory di skills aggiuntive                                                                                                                                                 | `"./custom/skills/"`                  |
| `hooks`        | string\|array\|object | Percorsi di configurazione degli hook o configurazione inline                                                                                                                  | `"./my-extra-hooks.json"`             |
| `mcpServers`   | string\|array\|object | Percorsi di configurazione MCP o configurazione inline                                                                                                                         | `"./my-extra-mcp-config.json"`        |
| `outputStyles` | string\|array         | File/directory di stili di output aggiuntivi                                                                                                                                   | `"./styles/"`                         |
| `lspServers`   | string\|array\|object | Configurazioni [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) per l'intelligenza del codice (vai alla definizione, trova riferimenti, ecc.) | `"./.lsp.json"`                       |

### Regole del comportamento del percorso

**Importante**: I percorsi personalizzati integrano le directory predefinite - non le sostituiscono.

* Se `commands/` esiste, viene caricato in aggiunta ai percorsi di comandi personalizzati
* Tutti i percorsi devono essere relativi alla radice del plugin e iniziare con `./`
* I comandi dai percorsi personalizzati utilizzano le stesse regole di denominazione e spazio dei nomi
* È possibile specificare più percorsi come array per flessibilità

**Esempi di percorso**:

```json  theme={null}
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

**`${CLAUDE_PLUGIN_ROOT}`**: Contiene il percorso assoluto della directory del tuo plugin. Usalo in hooks, server MCP e script per garantire percorsi corretti indipendentemente dalla posizione di installazione.

```json  theme={null}
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

***

## Caching del plugin e risoluzione dei file

I plugin vengono specificati in uno di due modi:

* Tramite `claude --plugin-dir`, per la durata di una sessione.
* Tramite un marketplace, installato per sessioni future.

Per motivi di sicurezza e verifica, Claude Code copia i plugin del *marketplace* nella **cache dei plugin** locale dell'utente (`~/.claude/plugins/cache`) piuttosto che usarli sul posto. Comprendere questo comportamento è importante quando si sviluppano plugin che fanno riferimento a file esterni.

### Limitazioni dell'attraversamento dei percorsi

I plugin installati non possono fare riferimento a file al di fuori della loro directory. I percorsi che attraversano al di fuori della radice del plugin (come `../shared-utils`) non funzioneranno dopo l'installazione perché questi file esterni non vengono copiati nella cache.

### Lavorare con dipendenze esterne

Se il tuo plugin ha bisogno di accedere a file al di fuori della sua directory, puoi creare link simbolici a file esterni all'interno della directory del tuo plugin. I symlink vengono rispettati durante il processo di copia:

```bash  theme={null}
# All'interno della directory del tuo plugin
ln -s /path/to/shared-utils ./shared-utils
```

Il contenuto collegato simbolicamente verrà copiato nella cache del plugin. Questo fornisce flessibilità mantenendo i vantaggi di sicurezza del sistema di caching.

***

## Struttura della directory del plugin

### Layout standard del plugin

Un plugin completo segue questa struttura:

```text  theme={null}
enterprise-plugin/
├── .claude-plugin/           # Directory dei metadati (opzionale)
│   └── plugin.json             # manifest del plugin
├── commands/                 # Posizione predefinita del comando
│   ├── status.md
│   └── logs.md
├── agents/                   # Posizione predefinita dell'agent
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                   # Skills dell'agent
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Configurazioni degli hook
│   ├── hooks.json           # Configurazione principale degli hook
│   └── security-hooks.json  # Hook aggiuntivi
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
  La directory `.claude-plugin/` contiene il file `plugin.json`. Tutte le altre directory (commands/, agents/, skills/, hooks/) devono essere nella radice del plugin, non all'interno di `.claude-plugin/`.
</Warning>

### Riferimento delle posizioni dei file

| Componente       | Posizione predefinita        | Scopo                                                                                                                                         |
| :--------------- | :--------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| **Manifest**     | `.claude-plugin/plugin.json` | Metadati e configurazione del plugin (opzionale)                                                                                              |
| **Comandi**      | `commands/`                  | File Markdown della skill (legacy; usa `skills/` per le nuove skills)                                                                         |
| **Agents**       | `agents/`                    | File Markdown del subagent                                                                                                                    |
| **Skills**       | `skills/`                    | Skills con struttura `<name>/SKILL.md`                                                                                                        |
| **Hooks**        | `hooks/hooks.json`           | Configurazione degli hook                                                                                                                     |
| **Server MCP**   | `.mcp.json`                  | Definizioni del server MCP                                                                                                                    |
| **Server LSP**   | `.lsp.json`                  | Configurazioni del server di linguaggio                                                                                                       |
| **Impostazioni** | `settings.json`              | Configurazione predefinita applicata quando il plugin è abilitato. Attualmente sono supportate solo le impostazioni [`agent`](/it/sub-agents) |

***

## Riferimento dei comandi CLI

Claude Code fornisce comandi CLI per la gestione non interattiva dei plugin, utile per scripting e automazione.

### plugin install

Installa un plugin dai marketplace disponibili.

```bash  theme={null}
claude plugin install <plugin> [options]
```

**Argomenti:**

* `<plugin>`: Nome del plugin o `plugin-name@marketplace-name` per un marketplace specifico

**Opzioni:**

| Opzione               | Descrizione                                           | Predefinito |
| :-------------------- | :---------------------------------------------------- | :---------- |
| `-s, --scope <scope>` | Ambito di installazione: `user`, `project`, o `local` | `user`      |
| `-h, --help`          | Visualizza la guida per il comando                    |             |

L'ambito determina quale file di impostazioni viene aggiunto al plugin installato. Ad esempio, --scope project scrive in `enabledPlugins` in .claude/settings.json, rendendo il plugin disponibile a tutti coloro che clonano il repository del progetto.

**Esempi:**

```bash  theme={null}
# Installa nell'ambito utente (predefinito)
claude plugin install formatter@my-marketplace

# Installa nell'ambito del progetto (condiviso con il team)
claude plugin install formatter@my-marketplace --scope project

# Installa nell'ambito locale (gitignored)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

Rimuovi un plugin installato.

```bash  theme={null}
claude plugin uninstall <plugin> [options]
```

**Argomenti:**

* `<plugin>`: Nome del plugin o `plugin-name@marketplace-name`

**Opzioni:**

| Opzione               | Descrizione                                           | Predefinito |
| :-------------------- | :---------------------------------------------------- | :---------- |
| `-s, --scope <scope>` | Disinstalla dall'ambito: `user`, `project`, o `local` | `user`      |
| `-h, --help`          | Visualizza la guida per il comando                    |             |

**Alias:** `remove`, `rm`

### plugin enable

Abilita un plugin disabilitato.

```bash  theme={null}
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

```bash  theme={null}
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

```bash  theme={null}
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

Usa `claude --debug` (o `/debug` all'interno del TUI) per vedere i dettagli del caricamento del plugin:

Questo mostra:

* Quali plugin vengono caricati
* Eventuali errori nei manifest del plugin
* Registrazione di comandi, agents e hook
* Inizializzazione del server MCP

### Problemi comuni

| Problema                            | Causa                               | Soluzione                                                                            |
| :---------------------------------- | :---------------------------------- | :----------------------------------------------------------------------------------- |
| Plugin non caricato                 | `plugin.json` non valido            | Convalida la sintassi JSON con `claude plugin validate` o `/plugin validate`         |
| Comandi non visualizzati            | Struttura della directory errata    | Assicurati che `commands/` sia alla radice, non in `.claude-plugin/`                 |
| Hook non attivati                   | Script non eseguibile               | Esegui `chmod +x script.sh`                                                          |
| Server MCP non riesce               | `${CLAUDE_PLUGIN_ROOT}` mancante    | Usa la variabile per tutti i percorsi del plugin                                     |
| Errori di percorso                  | Percorsi assoluti utilizzati        | Tutti i percorsi devono essere relativi e iniziare con `./`                          |
| LSP `Executable not found in $PATH` | Server di linguaggio non installato | Installa il binario (ad es., `npm install -g typescript-language-server typescript`) |

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
3. Conferma che il tipo di hook sia valido: `command`, `prompt`, o `agent`

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

**Sintomi**: Il plugin si carica ma i componenti (comandi, agents, hook) sono mancanti.

**Struttura corretta**: I componenti devono essere nella radice del plugin, non all'interno di `.claude-plugin/`. Solo `plugin.json` appartiene a `.claude-plugin/`.

```text  theme={null}
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

```json  theme={null}
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
