> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Riferimento dei hooks

> Riferimento per gli eventi dei hook di Claude Code, schema di configurazione, formati JSON di input/output, codici di uscita, hook asincroni, hook HTTP, hook di prompt e hook degli strumenti MCP.

<Tip>
  Per una guida di avvio rapido con esempi, consultare [Automatizzare i flussi di lavoro con i hook](/it/hooks-guide).
</Tip>

Gli hook sono comandi shell definiti dall'utente, endpoint HTTP o prompt LLM che si eseguono automaticamente in punti specifici del ciclo di vita di Claude Code. Utilizzare questo riferimento per cercare schemi di eventi, opzioni di configurazione, formati JSON di input/output e funzionalità avanzate come hook asincroni, hook HTTP e hook degli strumenti MCP. Se si stanno configurando i hook per la prima volta, iniziare con la [guida](/it/hooks-guide).

## Ciclo di vita dei hook

Gli hook si attivano in punti specifici durante una sessione di Claude Code. Quando un evento si attiva e un matcher corrisponde, Claude Code passa il contesto JSON dell'evento al gestore del hook. Per i hook di comando, l'input arriva su stdin. Per i hook HTTP, arriva come corpo della richiesta POST. Il gestore può quindi ispezionare l'input, intraprendere un'azione e facoltativamente restituire una decisione. Alcuni eventi si attivano una volta per sessione, mentre altri si attivano ripetutamente all'interno del ciclo agentico:

<div style={{maxWidth: "500px", margin: "0 auto"}}>
  <Frame>
    <img src="https://mintcdn.com/claude-code/UMJp-WgTWngzO609/images/hooks-lifecycle.svg?fit=max&auto=format&n=UMJp-WgTWngzO609&q=85&s=3f4de67df216c87dc313943b32c15f62" alt="Diagramma del ciclo di vita dei hook che mostra la sequenza dei hook da SessionStart attraverso il ciclo agentico (PreToolUse, PermissionRequest, PostToolUse, SubagentStart/Stop, TaskCreated, TaskCompleted) a Stop o StopFailure, TeammateIdle, PreCompact, PostCompact e SessionEnd, con Elicitation e ElicitationResult annidati all'interno dell'esecuzione dello strumento MCP, PermissionDenied come ramo laterale di PermissionRequest per i rifiuti in modalità automatica, e WorktreeCreate, WorktreeRemove, Notification, ConfigChange, InstructionsLoaded, CwdChanged e FileChanged come eventi asincroni autonomi" width="520" height="1155" data-path="images/hooks-lifecycle.svg" />
  </Frame>
</div>

La tabella seguente riassume quando si attiva ogni evento. La sezione [Hook events](#hook-events) documenta lo schema di input completo e le opzioni di controllo della decisione per ognuno.

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

### Come si risolve un hook

Per vedere come questi elementi si combinano, considerare questo hook `PreToolUse` che blocca i comandi shell distruttivi. Il `matcher` si restringe alle chiamate dello strumento Bash e la condizione `if` si restringe ulteriormente ai comandi che iniziano con `rm`, quindi `block-rm.sh` viene eseguito solo quando entrambi i filtri corrispondono:

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

Lo script legge l'input JSON da stdin, estrae il comando e restituisce una `permissionDecision` di `"deny"` se contiene `rm -rf`:

```bash  theme={null}
#!/bin/bash
# .claude/hooks/block-rm.sh
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0  # allow the command
fi
```

Supponiamo che Claude Code decida di eseguire `Bash "rm -rf /tmp/build"`. Ecco cosa accade:

<Frame>
  <img src="https://mintcdn.com/claude-code/-tYw1BD_DEqfyyOZ/images/hook-resolution.svg?fit=max&auto=format&n=-tYw1BD_DEqfyyOZ&q=85&s=c73ebc1eeda2037570427d7af1e0a891" alt="Flusso di risoluzione del hook: l'evento PreToolUse si attiva, il matcher controlla la corrispondenza di Bash, la condizione if controlla la corrispondenza di Bash(rm *), il gestore del hook viene eseguito, il risultato ritorna a Claude Code" width="930" height="290" data-path="images/hook-resolution.svg" />
</Frame>

<Steps>
  <Step title="L'evento si attiva">
    L'evento `PreToolUse` si attiva. Claude Code invia l'input dello strumento come JSON su stdin al hook:

    ```json  theme={null}
    { "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
    ```
  </Step>

  <Step title="Il matcher controlla">
    Il matcher `"Bash"` corrisponde al nome dello strumento, quindi questo gruppo di hook si attiva. Se si omette il matcher o si utilizza `"*"`, il gruppo si attiva ad ogni occorrenza dell'evento.
  </Step>

  <Step title="La condizione if controlla">
    La condizione `if` `"Bash(rm *)"` corrisponde perché il comando inizia con `rm`, quindi questo gestore viene eseguito. Se il comando fosse stato `npm test`, il controllo `if` avrebbe fallito e `block-rm.sh` non sarebbe mai stato eseguito, evitando il sovraccarico di spawn del processo. Il campo `if` è facoltativo; senza di esso, ogni gestore nel gruppo corrispondente viene eseguito.
  </Step>

  <Step title="Il gestore del hook viene eseguito">
    Lo script ispeziona il comando completo e trova `rm -rf`, quindi stampa una decisione su stdout:

    ```json  theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Destructive command blocked by hook"
      }
    }
    ```

    Se il comando fosse stato una variante più sicura di `rm` come `rm file.txt`, lo script avrebbe raggiunto `exit 0` invece, che dice a Claude Code di consentire la chiamata dello strumento senza ulteriori azioni.
  </Step>

  <Step title="Claude Code agisce sul risultato">
    Claude Code legge la decisione JSON, blocca la chiamata dello strumento e mostra a Claude il motivo.
  </Step>
</Steps>

La sezione [Configuration](#configuration) seguente documenta lo schema completo, e ogni sezione [hook event](#hook-events) documenta quale input riceve il comando e quale output può restituire.

## Configuration

Gli hook sono definiti in file di impostazioni JSON. La configurazione ha tre livelli di annidamento:

1. Scegliere un [hook event](#hook-events) a cui rispondere, come `PreToolUse` o `Stop`
2. Aggiungere un [matcher group](#matcher-patterns) per filtrare quando si attiva, come "solo per lo strumento Bash"
3. Definire uno o più [hook handlers](#hook-handler-fields) da eseguire quando corrisponde

Consultare [Come si risolve un hook](#how-a-hook-resolves) sopra per una procedura dettagliata completa con un esempio annotato.

<Note>
  Questa pagina utilizza termini specifici per ogni livello: **hook event** per il punto del ciclo di vita, **matcher group** per il filtro e **hook handler** per il comando shell, endpoint HTTP, prompt o agente che viene eseguito. "Hook" da solo si riferisce alla funzionalità generale.
</Note>

### Posizioni dei hook

Il luogo in cui si definisce un hook determina il suo ambito:

| Posizione                                                 | Ambito                        | Condivisibile                            |
| :-------------------------------------------------------- | :---------------------------- | :--------------------------------------- |
| `~/.claude/settings.json`                                 | Tutti i progetti              | No, locale al computer                   |
| `.claude/settings.json`                                   | Singolo progetto              | Sì, può essere committato nel repository |
| `.claude/settings.local.json`                             | Singolo progetto              | No, gitignored                           |
| Impostazioni della politica gestita                       | Organizzazione intera         | Sì, controllato dall'amministratore      |
| [Plugin](/it/plugins) `hooks/hooks.json`                  | Quando il plugin è abilitato  | Sì, fornito con il plugin                |
| [Skill](/it/skills) o [agent](/it/sub-agents) frontmatter | Mentre il componente è attivo | Sì, definito nel file del componente     |

Per i dettagli sulla risoluzione del file di impostazioni, consultare [settings](/it/settings). Gli amministratori aziendali possono utilizzare `allowManagedHooksOnly` per bloccare i hook dell'utente, del progetto e del plugin. Consultare [Hook configuration](/it/settings#hook-configuration).

### Modelli di matcher

Il campo `matcher` è una stringa regex che filtra quando gli hook si attivano. Utilizzare `"*"`, `""` o omettere completamente `matcher` per corrispondere a tutte le occorrenze. Ogni tipo di evento corrisponde a un campo diverso:

| Evento                                                                                                         | Su cosa filtra il matcher                | Valori matcher di esempio                                                                                                 |
| :------------------------------------------------------------------------------------------------------------- | :--------------------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`                     | nome dello strumento                     | `Bash`, `Edit\|Write`, `mcp__.*`                                                                                          |
| `SessionStart`                                                                                                 | come è iniziata la sessione              | `startup`, `resume`, `clear`, `compact`                                                                                   |
| `SessionEnd`                                                                                                   | perché è terminata la sessione           | `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`                                  |
| `Notification`                                                                                                 | tipo di notifica                         | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`                                                  |
| `SubagentStart`                                                                                                | tipo di agente                           | `Bash`, `Explore`, `Plan` o nomi di agenti personalizzati                                                                 |
| `PreCompact`, `PostCompact`                                                                                    | cosa ha attivato la compattazione        | `manual`, `auto`                                                                                                          |
| `SubagentStop`                                                                                                 | tipo di agente                           | stessi valori di `SubagentStart`                                                                                          |
| `ConfigChange`                                                                                                 | fonte di configurazione                  | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`                                        |
| `CwdChanged`                                                                                                   | nessun supporto matcher                  | si attiva sempre ad ogni cambio di directory                                                                              |
| `FileChanged`                                                                                                  | nome file (basename del file modificato) | `.envrc`, `.env`, qualsiasi nome file che si desidera monitorare                                                          |
| `StopFailure`                                                                                                  | tipo di errore                           | `rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown` |
| `InstructionsLoaded`                                                                                           | motivo del caricamento                   | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`                                              |
| `Elicitation`                                                                                                  | nome del server MCP                      | i nomi dei server MCP configurati                                                                                         |
| `ElicitationResult`                                                                                            | nome del server MCP                      | stessi valori di `Elicitation`                                                                                            |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | nessun supporto matcher                  | si attiva sempre ad ogni occorrenza                                                                                       |

Il matcher è una regex, quindi `Edit|Write` corrisponde a entrambi gli strumenti e `Notebook.*` corrisponde a qualsiasi strumento che inizia con Notebook. Il matcher viene eseguito su un campo dall'[input JSON](#hook-input-and-output) che Claude Code invia al hook su stdin. Per gli eventi degli strumenti, quel campo è `tool_name`. Ogni sezione [hook event](#hook-events) elenca l'insieme completo di valori matcher e lo schema di input per quell'evento.

Questo esempio esegue uno script di linting solo quando Claude scrive o modifica un file:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```

`UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` e `CwdChanged` non supportano i matcher e si attivano sempre ad ogni occorrenza. Se si aggiunge un campo `matcher` a questi eventi, viene silenziosamente ignorato.

Per gli eventi degli strumenti, è possibile filtrare più strettamente impostando il campo [`if`](#common-fields) sui singoli gestori del hook. `if` utilizza la [sintassi delle regole di autorizzazione](/it/permissions) per corrispondere al nome dello strumento e agli argomenti insieme, quindi `"Bash(git *)"` viene eseguito solo per i comandi `git` e `"Edit(*.ts)"` viene eseguito solo per i file TypeScript.

#### Corrispondere ai strumenti MCP

Gli strumenti del server [MCP](/it/mcp) appaiono come strumenti regolari negli eventi degli strumenti (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`), quindi è possibile farvi corrispondere lo stesso modo in cui si fa corrispondere qualsiasi altro nome di strumento.

Gli strumenti MCP seguono il modello di denominazione `mcp__<server>__<tool>`, ad esempio:

* `mcp__memory__create_entities`: strumento create entities del server Memory
* `mcp__filesystem__read_file`: strumento read file del server Filesystem
* `mcp__github__search_repositories`: strumento search del server GitHub

Utilizzare modelli regex per indirizzare strumenti MCP specifici o gruppi di strumenti:

* `mcp__memory__.*` corrisponde a tutti gli strumenti dal server `memory`
* `mcp__.*__write.*` corrisponde a qualsiasi strumento contenente "write" da qualsiasi server

Questo esempio registra tutte le operazioni del server memory e convalida le operazioni di scrittura da qualsiasi server MCP:

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

### Campi del gestore del hook

Ogni oggetto nell'array `hooks` interno è un gestore del hook: il comando shell, endpoint HTTP, prompt LLM o agente che viene eseguito quando il matcher corrisponde. Ci sono quattro tipi:

* **[Command hooks](#command-hook-fields)** (`type: "command"`): eseguono un comando shell. Lo script riceve l'[input JSON](#hook-input-and-output) dell'evento su stdin e comunica i risultati attraverso codici di uscita e stdout.
* **[HTTP hooks](#http-hook-fields)** (`type: "http"`): inviano l'input JSON dell'evento come richiesta HTTP POST a un URL. L'endpoint comunica i risultati attraverso il corpo della risposta utilizzando lo stesso [formato JSON di output](#json-output) dei command hook.
* **[Prompt hooks](#prompt-and-agent-hook-fields)** (`type: "prompt"`): inviano un prompt a un modello Claude per la valutazione a turno singolo. Il modello restituisce una decisione sì/no come JSON. Consultare [Prompt-based hooks](#prompt-based-hooks).
* **[Agent hooks](#prompt-and-agent-hook-fields)** (`type: "agent"`): generano un subagent che può utilizzare strumenti come Read, Grep e Glob per verificare le condizioni prima di restituire una decisione. Consultare [Agent-based hooks](#agent-based-hooks).

#### Campi comuni

Questi campi si applicano a tutti i tipi di hook:

| Campo           | Obbligatorio | Descrizione                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| :-------------- | :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`          | sì           | `"command"`, `"http"`, `"prompt"` o `"agent"`                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| `if`            | no           | Sintassi della regola di autorizzazione per filtrare quando questo hook viene eseguito, come `"Bash(git *)"` o `"Edit(*.ts)"`. L'hook viene eseguito solo se la chiamata dello strumento corrisponde al modello. Valutato solo su eventi degli strumenti: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` e `PermissionDenied`. Su altri eventi, un hook con `if` impostato non viene mai eseguito. Utilizza la stessa sintassi delle [regole di autorizzazione](/it/permissions) |
| `timeout`       | no           | Secondi prima dell'annullamento. Impostazioni predefinite: 600 per command, 30 per prompt, 60 per agent                                                                                                                                                                                                                                                                                                                                                                                                  |
| `statusMessage` | no           | Messaggio spinner personalizzato visualizzato mentre l'hook viene eseguito                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `once`          | no           | Se `true`, viene eseguito una sola volta per sessione e poi rimosso. Solo skill, non agenti. Consultare [Hooks in skills and agents](#hooks-in-skills-and-agents)                                                                                                                                                                                                                                                                                                                                        |

#### Campi del command hook

Oltre ai [campi comuni](#common-fields), i command hook accettano questi campi:

| Campo     | Obbligatorio | Descrizione                                                                                                                                                                                                                                                          |
| :-------- | :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `command` | sì           | Comando shell da eseguire                                                                                                                                                                                                                                            |
| `async`   | no           | Se `true`, viene eseguito in background senza bloccare. Consultare [Run hooks in the background](#run-hooks-in-the-background)                                                                                                                                       |
| `shell`   | no           | Shell da utilizzare per questo hook. Accetta `"bash"` (predefinito) o `"powershell"`. L'impostazione `"powershell"` esegue il comando tramite PowerShell su Windows. Non richiede `CLAUDE_CODE_USE_POWERSHELL_TOOL` poiché gli hook generano PowerShell direttamente |

#### Campi del HTTP hook

Oltre ai [campi comuni](#common-fields), gli HTTP hook accettano questi campi:

| Campo            | Obbligatorio | Descrizione                                                                                                                                                                                                                                                  |
| :--------------- | :----------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`            | sì           | URL a cui inviare la richiesta POST                                                                                                                                                                                                                          |
| `headers`        | no           | Intestazioni HTTP aggiuntive come coppie chiave-valore. I valori supportano l'interpolazione delle variabili di ambiente utilizzando la sintassi `$VAR_NAME` o `${VAR_NAME}`. Solo le variabili elencate in `allowedEnvVars` vengono risolte                 |
| `allowedEnvVars` | no           | Elenco dei nomi delle variabili di ambiente che possono essere interpolate nei valori dell'intestazione. I riferimenti alle variabili non elencate vengono sostituiti con stringhe vuote. Obbligatorio per qualsiasi interpolazione di variabili di ambiente |

Claude Code invia l'[input JSON](#hook-input-and-output) del hook come corpo della richiesta POST con `Content-Type: application/json`. Il corpo della risposta utilizza lo stesso [formato JSON di output](#json-output) dei command hook.

La gestione degli errori differisce dai command hook: le risposte non-2xx, i guasti di connessione e i timeout producono tutti errori non bloccanti che consentono l'esecuzione di continuare. Per bloccare una chiamata dello strumento o negare un'autorizzazione, restituire una risposta 2xx con un corpo JSON contenente `decision: "block"` o un `hookSpecificOutput` con `permissionDecision: "deny"`.

Questo esempio invia gli eventi `PreToolUse` a un servizio di convalida locale, autenticandosi con un token dalla variabile di ambiente `MY_TOKEN`:

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/pre-tool-use",
            "timeout": 30,
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

#### Campi dei prompt hook e agent hook

Oltre ai [campi comuni](#common-fields), i prompt hook e agent hook accettano questi campi:

| Campo    | Obbligatorio | Descrizione                                                                                               |
| :------- | :----------- | :-------------------------------------------------------------------------------------------------------- |
| `prompt` | sì           | Testo del prompt da inviare al modello. Utilizzare `$ARGUMENTS` come segnaposto per l'input JSON del hook |
| `model`  | no           | Modello da utilizzare per la valutazione. Impostazione predefinita: un modello veloce                     |

Tutti gli hook corrispondenti vengono eseguiti in parallelo e i gestori identici vengono automaticamente deduplicati. I command hook vengono deduplicati per stringa di comando e gli HTTP hook vengono deduplicati per URL. I gestori vengono eseguiti nella directory corrente con l'ambiente di Claude Code. La variabile di ambiente `$CLAUDE_CODE_REMOTE` è impostata su `"true"` negli ambienti web remoti e non è impostata nella CLI locale.

### Fare riferimento agli script per percorso

Utilizzare le variabili di ambiente per fare riferimento agli script del hook relativi alla radice del progetto o del plugin, indipendentemente dalla directory di lavoro quando l'hook viene eseguito:

* `$CLAUDE_PROJECT_DIR`: la radice del progetto. Racchiudere tra virgolette per gestire i percorsi con spazi.
* `${CLAUDE_PLUGIN_ROOT}`: la directory radice del plugin, per gli script forniti con un [plugin](/it/plugins). Cambia ad ogni aggiornamento del plugin.
* `${CLAUDE_PLUGIN_DATA}`: la [directory di dati persistenti](/it/plugins-reference#persistent-data-directory) del plugin, per le dipendenze e lo stato che dovrebbero sopravvivere agli aggiornamenti del plugin.

<Tabs>
  <Tab title="Script del progetto">
    Questo esempio utilizza `$CLAUDE_PROJECT_DIR` per eseguire un controllo dello stile dalla directory `.claude/hooks/` del progetto dopo qualsiasi chiamata dello strumento `Write` o `Edit`:

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Script del plugin">
    Definire i hook del plugin in `hooks/hooks.json` con un campo `description` facoltativo di livello superiore. Quando un plugin è abilitato, i suoi hook si uniscono ai hook dell'utente e del progetto.

    Questo esempio esegue uno script di formattazione fornito con il plugin:

    ```json  theme={null}
    {
      "description": "Automatic code formatting",
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
                "timeout": 30
              }
            ]
          }
        ]
      }
    }
    ```

    Consultare il [plugin components reference](/it/plugins-reference#hooks) per i dettagli sulla creazione dei hook del plugin.
  </Tab>
</Tabs>

### Hook in skills e agents

Oltre ai file di impostazioni e ai plugin, gli hook possono essere definiti direttamente in [skills](/it/skills) e [subagents](/it/sub-agents) utilizzando il frontmatter. Questi hook sono limitati al ciclo di vita del componente e vengono eseguiti solo quando quel componente è attivo.

Tutti gli hook event sono supportati. Per i subagent, gli hook `Stop` vengono automaticamente convertiti in `SubagentStop` poiché questo è l'evento che si attiva quando un subagent termina.

Gli hook utilizzano lo stesso formato di configurazione dei hook basati su impostazioni ma sono limitati alla durata del componente e vengono puliti quando termina.

Questa skill definisce un hook `PreToolUse` che esegue uno script di convalida della sicurezza prima di ogni comando `Bash`:

```yaml  theme={null}
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

Gli agenti utilizzano lo stesso formato nel loro frontmatter YAML.

### Il menu `/hooks`

Digitare `/hooks` in Claude Code per aprire un browser di sola lettura per i hook configurati. Il menu mostra ogni hook event con un conteggio dei hook configurati, consente di approfondire i matcher e mostra i dettagli completi di ogni gestore del hook. Utilizzarlo per verificare la configurazione, controllare da quale file di impostazioni proviene un hook o ispezionare il comando, il prompt o l'URL di un hook.

Il menu visualizza tutti e quattro i tipi di hook: `command`, `prompt`, `agent` e `http`. Ogni hook è etichettato con un prefisso `[type]` e una fonte che indica dove è stato definito:

* `User`: da `~/.claude/settings.json`
* `Project`: da `.claude/settings.json`
* `Local`: da `.claude/settings.local.json`
* `Plugin`: da `hooks/hooks.json` di un plugin
* `Session`: registrato in memoria per la sessione corrente
* `Built-in`: registrato internamente da Claude Code

Selezionando un hook si apre una vista dettagliata che mostra il suo evento, matcher, tipo, file di origine e il comando, il prompt o l'URL completo. Il menu è di sola lettura: per aggiungere, modificare o rimuovere i hook, modificare il JSON delle impostazioni direttamente o chiedere a Claude di fare la modifica.

### Disabilitare o rimuovere i hook

Per rimuovere un hook, eliminare la sua voce dal file di impostazioni JSON.

Per disabilitare temporaneamente tutti gli hook senza rimuoverli, impostare `"disableAllHooks": true` nel file di impostazioni. Non c'è modo di disabilitare un singolo hook mantenendolo nella configurazione.

L'impostazione `disableAllHooks` rispetta la gerarchia delle impostazioni gestite. Se un amministratore ha configurato i hook attraverso le impostazioni della politica gestita, `disableAllHooks` impostato nelle impostazioni dell'utente, del progetto o locali non può disabilitare quei hook gestiti. Solo `disableAllHooks` impostato a livello di impostazioni gestite può disabilitare i hook gestiti.

Le modifiche dirette ai hook nei file di impostazioni vengono normalmente acquisite automaticamente dal file watcher.

## Hook input e output

I command hook ricevono dati JSON tramite stdin e comunicano i risultati attraverso codici di uscita, stdout e stderr. Gli HTTP hook ricevono lo stesso JSON come corpo della richiesta POST e comunicano i risultati attraverso il corpo della risposta HTTP. Questa sezione copre i campi e il comportamento comuni a tutti gli eventi. Ogni sezione dell'evento sotto [Hook events](#hook-events) include il suo schema di input specifico e le opzioni di controllo della decisione.

### Campi di input comuni

Gli hook event ricevono questi campi come JSON, oltre ai campi specifici dell'evento documentati in ogni sezione [hook event](#hook-events). Per i command hook, questo JSON arriva tramite stdin. Per gli HTTP hook, arriva come corpo della richiesta POST.

| Campo             | Descrizione                                                                                                                                                                                                                                                                     |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `session_id`      | Identificatore della sessione corrente                                                                                                                                                                                                                                          |
| `transcript_path` | Percorso al JSON della conversazione                                                                                                                                                                                                                                            |
| `cwd`             | Directory di lavoro corrente quando l'hook viene invocato                                                                                                                                                                                                                       |
| `permission_mode` | [Modalità di autorizzazione](/it/permissions#permission-modes) corrente: `"default"`, `"plan"`, `"acceptEdits"`, `"auto"`, `"dontAsk"` o `"bypassPermissions"`. Non tutti gli eventi ricevono questo campo: consultare ogni esempio JSON dell'evento di seguito per controllare |
| `hook_event_name` | Nome dell'evento che si è attivato                                                                                                                                                                                                                                              |

Quando si esegue con `--agent` o all'interno di un subagent, vengono inclusi due campi aggiuntivi:

| Campo        | Descrizione                                                                                                                                                                                                                                                  |
| :----------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id`   | Identificatore univoco per il subagent. Presente solo quando l'hook si attiva all'interno di una chiamata di subagent. Utilizzare questo per distinguere le chiamate del hook del subagent dalle chiamate del thread principale.                             |
| `agent_type` | Nome dell'agente (ad esempio, `"Explore"` o `"security-reviewer"`). Presente quando la sessione utilizza `--agent` o l'hook si attiva all'interno di un subagent. Per i subagent, il tipo del subagent ha la precedenza sul valore `--agent` della sessione. |

Ad esempio, un hook `PreToolUse` per un comando Bash riceve questo su stdin:

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

I campi `tool_name` e `tool_input` sono specifici dell'evento. Ogni sezione [hook event](#hook-events) documenta i campi aggiuntivi per quell'evento.

### Output del codice di uscita

Il codice di uscita dal comando del hook dice a Claude Code se l'azione deve procedere, essere bloccata o essere ignorata.

**Exit 0** significa successo. Claude Code analizza stdout per i [campi di output JSON](#json-output). L'output JSON viene elaborato solo su exit 0. Per la maggior parte degli eventi, stdout viene mostrato solo in modalità verbose (`Ctrl+O`). Le eccezioni sono `UserPromptSubmit` e `SessionStart`, dove stdout viene aggiunto come contesto che Claude può vedere e su cui agire.

**Exit 2** significa un errore bloccante. Claude Code ignora stdout e qualsiasi JSON in esso. Invece, il testo stderr viene restituito a Claude come messaggio di errore. L'effetto dipende dall'evento: `PreToolUse` blocca la chiamata dello strumento, `UserPromptSubmit` rifiuta il prompt e così via. Consultare [exit code 2 behavior](#exit-code-2-behavior-per-event) per l'elenco completo.

**Qualsiasi altro codice di uscita** è un errore non bloccante. stderr viene mostrato in modalità verbose (`Ctrl+O`) e l'esecuzione continua.

Ad esempio, uno script di comando hook che blocca i comandi Bash pericolosi:

```bash  theme={null}
#!/bin/bash
# Legge l'input JSON da stdin, controlla il comando
command=$(jq -r '.tool_input.command' < /dev/stdin)

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # Errore bloccante: la chiamata dello strumento viene impedita
fi

exit 0  # Successo: la chiamata dello strumento procede
```

#### Comportamento del codice di uscita 2 per evento

Il codice di uscita 2 è il modo in cui un hook segnala "fermarsi, non farlo". L'effetto dipende dall'evento, perché alcuni eventi rappresentano azioni che possono essere bloccate (come una chiamata dello strumento che non è ancora accaduta) e altri rappresentano cose che sono già accadute o non possono essere prevenute.

| Hook event           | Può bloccare? | Cosa accade su exit 2                                                                                                                                             |
| :------------------- | :------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PreToolUse`         | Sì            | Blocca la chiamata dello strumento                                                                                                                                |
| `PermissionRequest`  | Sì            | Nega l'autorizzazione                                                                                                                                             |
| `UserPromptSubmit`   | Sì            | Blocca l'elaborazione del prompt e cancella il prompt                                                                                                             |
| `Stop`               | Sì            | Impedisce a Claude di fermarsi, continua la conversazione                                                                                                         |
| `SubagentStop`       | Sì            | Impedisce al subagent di fermarsi                                                                                                                                 |
| `TeammateIdle`       | Sì            | Impedisce al compagno di squadra di andare inattivo (il compagno di squadra continua a lavorare)                                                                  |
| `TaskCreated`        | Sì            | Annulla la creazione dell'attività                                                                                                                                |
| `TaskCompleted`      | Sì            | Impedisce che l'attività sia contrassegnata come completata                                                                                                       |
| `ConfigChange`       | Sì            | Blocca la modifica della configurazione dall'avere effetto (tranne `policy_settings`)                                                                             |
| `StopFailure`        | No            | L'output e il codice di uscita vengono ignorati                                                                                                                   |
| `PostToolUse`        | No            | Mostra stderr a Claude (lo strumento è già stato eseguito)                                                                                                        |
| `PostToolUseFailure` | No            | Mostra stderr a Claude (lo strumento è già fallito)                                                                                                               |
| `PermissionDenied`   | No            | Il codice di uscita e stderr vengono ignorati (il rifiuto è già avvenuto). Utilizzare JSON `hookSpecificOutput.retry: true` per dire al modello che può riprovare |
| `Notification`       | No            | Mostra stderr solo all'utente                                                                                                                                     |
| `SubagentStart`      | No            | Mostra stderr solo all'utente                                                                                                                                     |
| `SessionStart`       | No            | Mostra stderr solo all'utente                                                                                                                                     |
| `SessionEnd`         | No            | Mostra stderr solo all'utente                                                                                                                                     |
| `CwdChanged`         | No            | Mostra stderr solo all'utente                                                                                                                                     |
| `FileChanged`        | No            | Mostra stderr solo all'utente                                                                                                                                     |
| `PreCompact`         | No            | Mostra stderr solo all'utente                                                                                                                                     |
| `PostCompact`        | No            | Mostra stderr solo all'utente                                                                                                                                     |
| `Elicitation`        | Sì            | Nega l'elicitazione                                                                                                                                               |
| `ElicitationResult`  | Sì            | Blocca la risposta (l'azione diventa decline)                                                                                                                     |
| `WorktreeCreate`     | Sì            | Qualsiasi codice di uscita diverso da zero causa il fallimento della creazione del worktree                                                                       |
| `WorktreeRemove`     | No            | I guasti vengono registrati solo in modalità debug                                                                                                                |
| `InstructionsLoaded` | No            | Il codice di uscita viene ignorato                                                                                                                                |

### Gestione della risposta HTTP

Gli HTTP hook utilizzano i codici di stato HTTP e i corpi della risposta invece dei codici di uscita e stdout:

* **2xx con corpo vuoto**: successo, equivalente al codice di uscita 0 senza output
* **2xx con corpo di testo semplice**: successo, il testo viene aggiunto come contesto
* **2xx con corpo JSON**: successo, analizzato utilizzando lo stesso schema [JSON output](#json-output) dei command hook
* **Stato non-2xx**: errore non bloccante, l'esecuzione continua
* **Guasto di connessione o timeout**: errore non bloccante, l'esecuzione continua

A differenza dei command hook, gli HTTP hook non possono segnalare un errore bloccante solo attraverso i codici di stato. Per bloccare una chiamata dello strumento o negare un'autorizzazione, restituire una risposta 2xx con un corpo JSON contenente i campi di decisione appropriati.

### Output JSON

I codici di uscita consentono di consentire o bloccare, ma l'output JSON offre un controllo più granulare. Invece di uscire con il codice 2 per bloccare, uscire 0 e stampare un oggetto JSON su stdout. Claude Code legge campi specifici da quel JSON per controllare il comportamento, incluso il [decision control](#decision-control) per bloccare, consentire o escalare all'utente.

<Note>
  È necessario scegliere un approccio per hook, non entrambi: utilizzare i codici di uscita da soli per la segnalazione oppure uscire 0 e stampare JSON per il controllo strutturato. Claude Code elabora JSON solo su exit 0. Se si esce con 2, qualsiasi JSON viene ignorato.
</Note>

Lo stdout del hook deve contenere solo l'oggetto JSON. Se il profilo shell stampa testo all'avvio, può interferire con l'analisi JSON. Consultare [JSON validation failed](/it/hooks-guide#json-validation-failed) nella guida alla risoluzione dei problemi.

L'output del hook iniettato nel contesto (`additionalContext`, `systemMessage` o stdout semplice) è limitato a 10.000 caratteri. L'output che supera questo limite viene salvato in un file e sostituito con un'anteprima e un percorso di file, nello stesso modo in cui vengono gestiti i risultati degli strumenti di grandi dimensioni.

L'oggetto JSON supporta tre tipi di campi:

* **Campi universali** come `continue` funzionano su tutti gli eventi. Questi sono elencati nella tabella seguente.
* **`decision` e `reason` di livello superiore** vengono utilizzati da alcuni eventi per bloccare o fornire feedback.
* **`hookSpecificOutput`** è un oggetto annidato per gli eventi che necessitano di un controllo più ricco. Richiede un campo `hookEventName` impostato sul nome dell'evento.

| Campo            | Impostazione predefinita | Descrizione                                                                                                                                                   |
| :--------------- | :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `continue`       | `true`                   | Se `false`, Claude interrompe completamente l'elaborazione dopo l'esecuzione del hook. Ha la precedenza su qualsiasi campo di decisione specifico dell'evento |
| `stopReason`     | nessuno                  | Messaggio mostrato all'utente quando `continue` è `false`. Non mostrato a Claude                                                                              |
| `suppressOutput` | `false`                  | Se `true`, nasconde stdout dall'output della modalità verbose                                                                                                 |
| `systemMessage`  | nessuno                  | Messaggio di avviso mostrato all'utente                                                                                                                       |

Per fermare Claude completamente indipendentemente dal tipo di evento:

```json  theme={null}
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

#### Controllo della decisione

Non ogni evento supporta il blocco o il controllo del comportamento attraverso JSON. Gli eventi che lo fanno utilizzano ciascuno un insieme diverso di campi per esprimere quella decisione. Utilizzare questa tabella come riferimento rapido prima di scrivere un hook:

| Eventi                                                                                                                      | Modello di decisione                 | Campi chiave                                                                                                                                                                                                       |
| :-------------------------------------------------------------------------------------------------------------------------- | :----------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UserPromptSubmit, PostToolUse, PostToolUseFailure, Stop, SubagentStop, ConfigChange                                         | `decision` di livello superiore      | `decision: "block"`, `reason`                                                                                                                                                                                      |
| TeammateIdle, TaskCreated, TaskCompleted                                                                                    | Codice di uscita o `continue: false` | Il codice di uscita 2 blocca l'azione con feedback stderr. JSON `{"continue": false, "stopReason": "..."}` interrompe anche completamente il compagno di squadra, corrispondendo al comportamento dell'hook `Stop` |
| PreToolUse                                                                                                                  | `hookSpecificOutput`                 | `permissionDecision` (allow/deny/ask/defer), `permissionDecisionReason`                                                                                                                                            |
| PermissionRequest                                                                                                           | `hookSpecificOutput`                 | `decision.behavior` (allow/deny)                                                                                                                                                                                   |
| PermissionDenied                                                                                                            | `hookSpecificOutput`                 | `retry: true` dice al modello che può riprovare la chiamata dello strumento negata                                                                                                                                 |
| WorktreeCreate                                                                                                              | percorso stdout                      | L'hook stampa il percorso su stdout; l'hook HTTP restituisce `hookSpecificOutput.worktreePath`. Il fallimento del hook o il percorso mancante non riesce nella creazione                                           |
| Elicitation                                                                                                                 | `hookSpecificOutput`                 | `action` (accept/decline/cancel), `content` (valori dei campi del modulo per accept)                                                                                                                               |
| ElicitationResult                                                                                                           | `hookSpecificOutput`                 | `action` (accept/decline/cancel), `content` (valori dei campi del modulo override)                                                                                                                                 |
| WorktreeRemove, Notification, SessionEnd, PreCompact, PostCompact, InstructionsLoaded, StopFailure, CwdChanged, FileChanged | Nessuno                              | Nessun controllo della decisione. Utilizzato per effetti collaterali come la registrazione o la pulizia                                                                                                            |

Ecco esempi di ogni modello in azione:

<Tabs>
  <Tab title="Decisione di livello superiore">
    Utilizzato da `UserPromptSubmit`, `PostToolUse`, `PostToolUseFailure`, `Stop`, `SubagentStop` e `ConfigChange`. L'unico valore è `"block"`. Per consentire all'azione di procedere, omettere `decision` dal JSON o uscire 0 senza alcun JSON:

    ```json  theme={null}
    {
      "decision": "block",
      "reason": "Test suite must pass before proceeding"
    }
    ```
  </Tab>

  <Tab title="PreToolUse">
    Utilizza `hookSpecificOutput` per un controllo più ricco: consentire, negare, chiedere o rinviare. È anche possibile modificare l'input dello strumento prima che venga eseguito o iniettare contesto aggiuntivo per Claude. Consultare [PreToolUse decision control](#pretooluse-decision-control) per l'insieme completo di opzioni.

    ```json  theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Database writes are not allowed"
      }
    }
    ```
  </Tab>

  <Tab title="PermissionRequest">
    Utilizza `hookSpecificOutput` per consentire o negare una richiesta di autorizzazione per conto dell'utente. Quando si consente, è anche possibile modificare l'input dello strumento o applicare regole di autorizzazione in modo che l'utente non venga richiesto di nuovo. Consultare [PermissionRequest decision control](#permissionrequest-decision-control) per l'insieme completo di opzioni.

    ```json  theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PermissionRequest",
        "decision": {
          "behavior": "allow",
          "updatedInput": {
            "command": "npm run lint"
          }
        }
      }
    }
    ```
  </Tab>
</Tabs>

Per esempi estesi inclusa la convalida dei comandi Bash, il filtraggio dei prompt e gli script di approvazione automatica, consultare [What you can automate](/it/hooks-guide#what-you-can-automate) nella guida e l'[implementazione di riferimento del validatore di comandi Bash](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py).

## Hook events

Ogni evento corrisponde a un punto nel ciclo di vita di Claude Code in cui gli hook possono essere eseguiti. Le sezioni seguenti sono ordinate per corrispondere al ciclo di vita: dalla configurazione della sessione attraverso il ciclo agentico alla fine della sessione. Ogni sezione descrive quando l'evento si attiva, quali matcher supporta, l'input JSON che riceve e come controllare il comportamento attraverso l'output.

### SessionStart

Viene eseguito quando Claude Code avvia una nuova sessione o riprende una sessione esistente. Utile per caricare il contesto di sviluppo come problemi esistenti o modifiche recenti al codebase, o per configurare le variabili di ambiente. Per il contesto statico che non richiede uno script, utilizzare [CLAUDE.md](/it/memory) invece.

SessionStart viene eseguito ad ogni sessione, quindi mantenere questi hook veloci. Solo gli hook `type: "command"` sono supportati.

Il valore del matcher corrisponde a come è stata avviata la sessione:

| Matcher   | Quando si attiva                     |
| :-------- | :----------------------------------- |
| `startup` | Nuova sessione                       |
| `resume`  | `--resume`, `--continue` o `/resume` |
| `clear`   | `/clear`                             |
| `compact` | Compattazione automatica o manuale   |

#### Input di SessionStart

Oltre ai [campi di input comuni](#common-input-fields), gli hook SessionStart ricevono `source`, `model` e facoltativamente `agent_type`. Il campo `source` indica come è iniziata la sessione: `"startup"` per le nuove sessioni, `"resume"` per le sessioni riprese, `"clear"` dopo `/clear` o `"compact"` dopo la compattazione. Il campo `model` contiene l'identificatore del modello. Se si avvia Claude Code con `claude --agent <name>`, un campo `agent_type` contiene il nome dell'agente.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-6"
}
```

#### Controllo della decisione di SessionStart

Qualsiasi testo che lo script del hook stampa su stdout viene aggiunto come contesto per Claude. Oltre ai [campi di output JSON](#json-output) disponibili per tutti gli hook, è possibile restituire questi campi specifici dell'evento:

| Campo               | Descrizione                                                                      |
| :------------------ | :------------------------------------------------------------------------------- |
| `additionalContext` | Stringa aggiunta al contesto di Claude. I valori di più hook vengono concatenati |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

#### Persistere le variabili di ambiente

Gli hook SessionStart hanno accesso alla variabile di ambiente `CLAUDE_ENV_FILE`, che fornisce un percorso di file in cui è possibile persistere le variabili di ambiente per i comandi Bash successivi.

Per impostare le singole variabili di ambiente, scrivere le istruzioni `export` in `CLAUDE_ENV_FILE`. Utilizzare l'aggiunta (`>>`) per preservare le variabili impostate da altri hook:

```bash  theme={null}
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Per acquisire tutte le modifiche dell'ambiente dai comandi di configurazione, confrontare le variabili esportate prima e dopo:

```bash  theme={null}
#!/bin/bash

ENV_BEFORE=$(export -p | sort)

# Eseguire i comandi di configurazione che modificano l'ambiente
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Qualsiasi variabile scritta in questo file sarà disponibile in tutti i comandi Bash successivi che Claude Code esegue durante la sessione.

<Note>
  `CLAUDE_ENV_FILE` è disponibile per gli hook SessionStart, [CwdChanged](#cwdchanged) e [FileChanged](#filechanged). Gli altri tipi di hook non hanno accesso a questa variabile.
</Note>

### InstructionsLoaded

Si attiva quando un file `CLAUDE.md` o `.claude/rules/*.md` viene caricato nel contesto. Questo evento si attiva all'avvio della sessione per i file caricati con entusiasmo e di nuovo in seguito quando i file vengono caricati in modo pigro, ad esempio quando Claude accede a una sottodirectory che contiene un `CLAUDE.md` annidato o quando le regole condizionali con frontmatter `paths:` corrispondono. L'hook non supporta il blocco o il controllo della decisione. Viene eseguito in modo asincrono per scopi di osservabilità.

Il matcher viene eseguito su `load_reason`. Ad esempio, utilizzare `"matcher": "session_start"` per attivarsi solo per i file caricati all'avvio della sessione, o `"matcher": "path_glob_match|nested_traversal"` per attivarsi solo per i caricamenti pigri.

#### Input di InstructionsLoaded

Oltre ai [campi di input comuni](#common-input-fields), gli hook InstructionsLoaded ricevono questi campi:

| Campo               | Descrizione                                                                                                                                                                                                                              |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `file_path`         | Percorso assoluto al file di istruzioni che è stato caricato                                                                                                                                                                             |
| `memory_type`       | Ambito del file: `"User"`, `"Project"`, `"Local"` o `"Managed"`                                                                                                                                                                          |
| `load_reason`       | Perché il file è stato caricato: `"session_start"`, `"nested_traversal"`, `"path_glob_match"`, `"include"` o `"compact"`. Il valore `"compact"` si attiva quando i file di istruzioni vengono ricaricati dopo un evento di compattazione |
| `globs`             | Modelli glob del percorso dal frontmatter `paths:` del file, se presenti. Presente solo per i caricamenti `path_glob_match`                                                                                                              |
| `trigger_file_path` | Percorso al file il cui accesso ha attivato questo caricamento, per i caricamenti pigri                                                                                                                                                  |
| `parent_file_path`  | Percorso al file di istruzioni padre che ha incluso questo, per i caricamenti `include`                                                                                                                                                  |

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "InstructionsLoaded",
  "file_path": "/Users/my-project/CLAUDE.md",
  "memory_type": "Project",
  "load_reason": "session_start"
}
```

#### Controllo della decisione di InstructionsLoaded

Gli hook InstructionsLoaded non hanno controllo della decisione. Non possono bloccare o modificare il caricamento delle istruzioni. Utilizzare questo evento per la registrazione di audit, il tracciamento della conformità o l'osservabilità.

### UserPromptSubmit

Viene eseguito quando l'utente invia un prompt, prima che Claude lo elabori. Ciò consente di aggiungere contesto aggiuntivo in base al prompt/conversazione, convalidare i prompt o bloccare determinati tipi di prompt.

#### Input di UserPromptSubmit

Oltre ai [campi di input comuni](#common-input-fields), gli hook UserPromptSubmit ricevono il campo `prompt` contenente il testo che l'utente ha inviato.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

#### Controllo della decisione di UserPromptSubmit

Gli hook `UserPromptSubmit` possono controllare se un prompt dell'utente viene elaborato e aggiungere contesto. Tutti i [campi di output JSON](#json-output) sono disponibili.

Ci sono due modi per aggiungere contesto alla conversazione su exit code 0:

* **Stdout di testo semplice**: qualsiasi testo non-JSON scritto su stdout viene aggiunto come contesto
* **JSON con `additionalContext`**: utilizzare il formato JSON seguente per un controllo maggiore. Il campo `additionalContext` viene aggiunto come contesto

Lo stdout semplice viene mostrato come output del hook nella trascrizione. Il campo `additionalContext` viene aggiunto più discretamente.

Per bloccare un prompt, restituire un oggetto JSON con `decision` impostato su `"block"`:

| Campo               | Descrizione                                                                                                              |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------- |
| `decision`          | `"block"` impedisce l'elaborazione del prompt e lo cancella dal contesto. Omettere per consentire al prompt di procedere |
| `reason`            | Mostrato all'utente quando `decision` è `"block"`. Non aggiunto al contesto                                              |
| `additionalContext` | Stringa aggiunta al contesto di Claude                                                                                   |

```json  theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

<Note>
  Il formato JSON non è obbligatorio per i casi semplici. Per aggiungere contesto, è possibile stampare testo semplice su stdout con exit code 0. Utilizzare JSON quando è necessario bloccare i prompt o si desidera un controllo più strutturato.
</Note>

### PreToolUse

Viene eseguito dopo che Claude crea i parametri dello strumento e prima dell'elaborazione della chiamata dello strumento. Corrisponde al nome dello strumento: `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `WebFetch`, `WebSearch`, `AskUserQuestion`, `ExitPlanMode` e qualsiasi [nome di strumento MCP](#match-mcp-tools).

Utilizzare il [PreToolUse decision control](#pretooluse-decision-control) per consentire, negare, chiedere o rinviare il permesso di utilizzare lo strumento.

#### Input di PreToolUse

Oltre ai [campi di input comuni](#common-input-fields), gli hook PreToolUse ricevono `tool_name`, `tool_input` e `tool_use_id`. I campi `tool_input` dipendono dallo strumento:

##### Bash

Esegue comandi shell.

| Campo               | Tipo    | Esempio            | Descrizione                                   |
| :------------------ | :------ | :----------------- | :-------------------------------------------- |
| `command`           | string  | `"npm test"`       | Il comando shell da eseguire                  |
| `description`       | string  | `"Run test suite"` | Descrizione facoltativa di cosa fa il comando |
| `timeout`           | number  | `120000`           | Timeout facoltativo in millisecondi           |
| `run_in_background` | boolean | `false`            | Se eseguire il comando in background          |

##### Write

Crea o sovrascrive un file.

| Campo       | Tipo   | Esempio               | Descrizione                           |
| :---------- | :----- | :-------------------- | :------------------------------------ |
| `file_path` | string | `"/path/to/file.txt"` | Percorso assoluto al file da scrivere |
| `content`   | string | `"file content"`      | Contenuto da scrivere nel file        |

##### Edit

Sostituisce una stringa in un file esistente.

| Campo         | Tipo    | Esempio               | Descrizione                             |
| :------------ | :------ | :-------------------- | :-------------------------------------- |
| `file_path`   | string  | `"/path/to/file.txt"` | Percorso assoluto al file da modificare |
| `old_string`  | string  | `"original text"`     | Testo da trovare e sostituire           |
| `new_string`  | string  | `"replacement text"`  | Testo di sostituzione                   |
| `replace_all` | boolean | `false`               | Se sostituire tutte le occorrenze       |

##### Read

Legge il contenuto del file.

| Campo       | Tipo   | Esempio               | Descrizione                                           |
| :---------- | :----- | :-------------------- | :---------------------------------------------------- |
| `file_path` | string | `"/path/to/file.txt"` | Percorso assoluto al file da leggere                  |
| `offset`    | number | `10`                  | Numero di riga facoltativo da cui iniziare la lettura |
| `limit`     | number | `50`                  | Numero facoltativo di righe da leggere                |

##### Glob

Trova i file che corrispondono a un modello glob.

| Campo     | Tipo   | Esempio          | Descrizione                                                                                  |
| :-------- | :----- | :--------------- | :------------------------------------------------------------------------------------------- |
| `pattern` | string | `"**/*.ts"`      | Modello glob per abbinare i file                                                             |
| `path`    | string | `"/path/to/dir"` | Directory facoltativa in cui cercare. Impostazione predefinita: directory di lavoro corrente |

##### Grep

Cerca il contenuto dei file con espressioni regolari.

| Campo         | Tipo    | Esempio          | Descrizione                                                                                       |
| :------------ | :------ | :--------------- | :------------------------------------------------------------------------------------------------ |
| `pattern`     | string  | `"TODO.*fix"`    | Modello di espressione regolare da cercare                                                        |
| `path`        | string  | `"/path/to/dir"` | File o directory facoltativa in cui cercare                                                       |
| `glob`        | string  | `"*.ts"`         | Modello glob facoltativo per filtrare i file                                                      |
| `output_mode` | string  | `"content"`      | `"content"`, `"files_with_matches"` o `"count"`. Impostazione predefinita: `"files_with_matches"` |
| `-i`          | boolean | `true`           | Ricerca senza distinzione tra maiuscole e minuscole                                               |
| `multiline`   | boolean | `false`          | Abilita l'abbinamento multilinea                                                                  |

##### WebFetch

Recupera ed elabora il contenuto web.

| Campo    | Tipo   | Esempio                       | Descrizione                                 |
| :------- | :----- | :---------------------------- | :------------------------------------------ |
| `url`    | string | `"https://example.com/api"`   | URL da cui recuperare il contenuto          |
| `prompt` | string | `"Extract the API endpoints"` | Prompt da eseguire sul contenuto recuperato |

##### WebSearch

Cerca il web.

| Campo             | Tipo   | Esempio                        | Descrizione                                              |
| :---------------- | :----- | :----------------------------- | :------------------------------------------------------- |
| `query`           | string | `"react hooks best practices"` | Query di ricerca                                         |
| `allowed_domains` | array  | `["docs.example.com"]`         | Facoltativo: includere solo i risultati da questi domini |
| `blocked_domains` | array  | `["spam.example.com"]`         | Facoltativo: escludere i risultati da questi domini      |

##### Agent

Genera un [subagent](/it/sub-agents).

| Campo           | Tipo   | Esempio                    | Descrizione                                                                |
| :-------------- | :----- | :------------------------- | :------------------------------------------------------------------------- |
| `prompt`        | string | `"Find all API endpoints"` | L'attività per l'agente da eseguire                                        |
| `description`   | string | `"Find API endpoints"`     | Breve descrizione dell'attività                                            |
| `subagent_type` | string | `"Explore"`                | Tipo di agente specializzato da utilizzare                                 |
| `model`         | string | `"sonnet"`                 | Alias del modello facoltativo per sovrascrivere l'impostazione predefinita |

##### AskUserQuestion

Chiede all'utente da una a quattro domande a scelta multipla.

| Campo       | Tipo   | Esempio                                                                                                            | Descrizione                                                                                                                                                                                                                                               |
| :---------- | :----- | :----------------------------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `questions` | array  | `[{"question": "Which framework?", "header": "Framework", "options": [{"label": "React"}], "multiSelect": false}]` | Domande da presentare, ciascuna con una stringa `question`, un `header` breve, un array `options` e un flag `multiSelect` facoltativo                                                                                                                     |
| `answers`   | object | `{"Which framework?": "React"}`                                                                                    | Facoltativo. Mappa il testo della domanda all'etichetta dell'opzione selezionata. Le risposte multi-select uniscono le etichette con virgole. Claude non imposta questo campo; fornirlo tramite `updatedInput` per rispondere a livello di programmazione |

#### PreToolUse decision control

Gli hook `PreToolUse` possono controllare se una chiamata dello strumento procede. A differenza di altri hook che utilizzano un campo `decision` di livello superiore, PreToolUse restituisce la sua decisione all'interno di un oggetto `hookSpecificOutput`. Ciò gli dà un controllo più ricco: quattro risultati (consentire, negare, chiedere o rinviare) più la capacità di modificare l'input dello strumento prima dell'esecuzione.

| Campo                      | Descrizione                                                                                                                                                                                                                                                                                                                                            |
| :------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `permissionDecision`       | `"allow"` bypassa il prompt di autorizzazione. `"deny"` impedisce la chiamata dello strumento. `"ask"` richiede all'utente di confermare. `"defer"` esce correttamente in modo che lo strumento possa essere ripreso in seguito. Le regole [Deny and ask](/it/permissions#manage-permissions) si applicano ancora quando un hook restituisce `"allow"` |
| `permissionDecisionReason` | Per `"allow"` e `"ask"`, mostrato all'utente ma non a Claude. Per `"deny"`, mostrato a Claude. Per `"defer"`, ignorato                                                                                                                                                                                                                                 |
| `updatedInput`             | Modifica i parametri di input dello strumento prima dell'esecuzione. Sostituisce l'intero oggetto di input, quindi includere i campi invariati insieme a quelli modificati. Combinare con `"allow"` per l'approvazione automatica o `"ask"` per mostrare l'input modificato all'utente. Per `"defer"`, ignorato                                        |
| `additionalContext`        | Stringa aggiunta al contesto di Claude prima dell'esecuzione dello strumento. Per `"defer"`, ignorato                                                                                                                                                                                                                                                  |

Quando più hook PreToolUse restituiscono decisioni diverse, la precedenza è `deny` > `defer` > `ask` > `allow`.

Quando un hook restituisce `"ask"`, il prompt di autorizzazione visualizzato all'utente include un'etichetta che identifica da dove proviene l'hook: ad esempio, `[User]`, `[Project]`, `[Plugin]` o `[Local]`. Ciò aiuta gli utenti a capire quale fonte di configurazione sta richiedendo la conferma.

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

`AskUserQuestion` e `ExitPlanMode` richiedono l'interazione dell'utente e normalmente bloccano in [modalità non interattiva](/it/headless) con il flag `-p`. Restituire `permissionDecision: "allow"` insieme a `updatedInput` soddisfa quel requisito: l'hook legge l'input dello strumento da stdin, raccoglie la risposta attraverso la propria interfaccia utente e la restituisce in `updatedInput` in modo che lo strumento venga eseguito senza richiedere. Restituire `"allow"` da solo non è sufficiente per questi strumenti. Per `AskUserQuestion`, ripetere l'array `questions` originale e aggiungere un oggetto [`answers`](#askuserquestion) che mappa il testo di ogni domanda alla risposta scelta.

<Note>
  PreToolUse in precedenza utilizzava i campi `decision` e `reason` di livello superiore, ma questi sono deprecati per questo evento. Utilizzare invece `hookSpecificOutput.permissionDecision` e `hookSpecificOutput.permissionDecisionReason`. I valori deprecati `"approve"` e `"block"` si mappano a `"allow"` e `"deny"` rispettivamente. Gli altri eventi come PostToolUse e Stop continuano a utilizzare `decision` e `reason` di livello superiore come formato corrente.
</Note>

#### Rinviare una chiamata dello strumento per dopo

`"defer"` è per le integrazioni che eseguono `claude -p` come subprocess e leggono il suo output JSON, come un'app Agent SDK o un'interfaccia utente personalizzata costruita su Claude Code. Consente a quel processo chiamante di mettere in pausa Claude in una chiamata dello strumento, raccogliere input attraverso la sua interfaccia e riprendere da dove era rimasto. Claude Code onora questo valore solo in [modalità non interattiva](/it/headless) con il flag `-p`. Nelle sessioni interattive registra un avviso e ignora il risultato del hook.

<Note>
  Il valore `defer` richiede Claude Code v2.1.89 o successivo. Le versioni precedenti non lo riconoscono e lo strumento procede attraverso il flusso di autorizzazione normale.
</Note>

Lo strumento `AskUserQuestion` è il caso tipico: Claude vuole chiedere qualcosa all'utente, ma non c'è un terminale per rispondere. Il round trip funziona così:

1. Claude chiama `AskUserQuestion`. L'hook `PreToolUse` si attiva.
2. L'hook restituisce `permissionDecision: "defer"`. Lo strumento non viene eseguito. Il processo esce con `stop_reason: "tool_deferred"` e la chiamata dello strumento in sospeso preservata nella trascrizione.
3. Il processo chiamante legge `deferred_tool_use` dal risultato SDK, visualizza la domanda nella sua interfaccia utente e attende una risposta.
4. Il processo chiamante esegue `claude -p --resume <session-id>`. La stessa chiamata dello strumento attiva `PreToolUse` di nuovo.
5. L'hook restituisce `permissionDecision: "allow"` con la risposta in `updatedInput`. Lo strumento viene eseguito e Claude continua.

Il campo `deferred_tool_use` contiene l'`id`, il `name` e l'`input` dello strumento. L'`input` è i parametri che Claude ha generato per la chiamata dello strumento, acquisiti prima dell'esecuzione:

```json  theme={null}
{
  "type": "result",
  "subtype": "success",
  "stop_reason": "tool_deferred",
  "session_id": "abc123",
  "deferred_tool_use": {
    "id": "toolu_01abc",
    "name": "AskUserQuestion",
    "input": { "questions": [{ "question": "Which framework?", "header": "Framework", "options": [{"label": "React"}, {"label": "Vue"}], "multiSelect": false }] }
  }
}
```

Non c'è timeout o limite di tentativi. La sessione rimane su disco fino a quando non la riprendi. Se la risposta non è pronta quando riprendi, l'hook può restituire `"defer"` di nuovo e il processo esce nello stesso modo. Il processo chiamante controlla quando interrompere il ciclo restituendo infine `"allow"` o `"deny"` dall'hook.

`"defer"` funziona solo quando Claude effettua una singola chiamata dello strumento nel turno. Se Claude effettua più chiamate dello strumento contemporaneamente, `"defer"` viene ignorato con un avviso e lo strumento procede attraverso il flusso di autorizzazione normale. Il vincolo esiste perché resume può solo rieseguire uno strumento: non c'è modo di rinviare una chiamata da un batch senza lasciare le altre irrisolte.

Se lo strumento rinviato non è più disponibile quando riprendi, il processo esce con `stop_reason: "tool_deferred_unavailable"` e `is_error: true` prima che l'hook si attivi. Questo accade quando un server MCP che ha fornito lo strumento non è connesso per la sessione ripresa. Il payload `deferred_tool_use` è ancora incluso in modo da poter identificare quale strumento è scomparso.

<Warning>
  `--resume` non ripristina la modalità di autorizzazione dalla sessione precedente. Passare lo stesso flag `--permission-mode` su resume che era attivo quando lo strumento è stato rinviato. Claude Code registra un avviso se le modalità differiscono.
</Warning>

### PermissionRequest

Viene eseguito quando all'utente viene mostrata una finestra di dialogo di autorizzazione.
Utilizzare il [PermissionRequest decision control](#permissionrequest-decision-control) per consentire o negare per conto dell'utente.

Corrisponde al nome dello strumento, stessi valori di PreToolUse.

#### Input di PermissionRequest

Gli hook PermissionRequest ricevono i campi `tool_name` e `tool_input` come gli hook PreToolUse, ma senza `tool_use_id`. Un array `permission_suggestions` facoltativo contiene le opzioni "consenti sempre" che l'utente normalmente vedrebbe nella finestra di dialogo di autorizzazione. La differenza è quando l'hook si attiva: gli hook PermissionRequest vengono eseguiti quando una finestra di dialogo di autorizzazione sta per essere mostrata all'utente, mentre gli hook PreToolUse vengono eseguiti prima dell'esecuzione dello strumento indipendentemente dallo stato di autorizzazione.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules",
    "description": "Remove node_modules directory"
  },
  "permission_suggestions": [
    {
      "type": "addRules",
      "rules": [{ "toolName": "Bash", "ruleContent": "rm -rf node_modules" }],
      "behavior": "allow",
      "destination": "localSettings"
    }
  ]
}
```

#### Controllo della decisione di PermissionRequest

Gli hook `PermissionRequest` possono consentire o negare le richieste di autorizzazione. Oltre ai [campi di output JSON](#json-output) disponibili per tutti gli hook, lo script del hook può restituire un oggetto `decision` con questi campi specifici dell'evento:

| Campo                | Descrizione                                                                                                                                                                                                     |
| :------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `behavior`           | `"allow"` concede l'autorizzazione, `"deny"` la nega                                                                                                                                                            |
| `updatedInput`       | Solo per `"allow"`: modifica i parametri di input dello strumento prima dell'esecuzione. Sostituisce l'intero oggetto di input, quindi includere i campi invariati insieme a quelli modificati                  |
| `updatedPermissions` | Solo per `"allow"`: array di [permission update entries](#permission-update-entries) da applicare, come l'aggiunta di una regola di consentimento o la modifica della modalità di autorizzazione della sessione |
| `message`            | Solo per `"deny"`: dice a Claude perché l'autorizzazione è stata negata                                                                                                                                         |
| `interrupt`          | Solo per `"deny"`: se `true`, interrompe Claude                                                                                                                                                                 |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

#### Permission update entries

Il campo di output `updatedPermissions` e il campo di input [`permission_suggestions`](#permissionrequest-input) utilizzano entrambi lo stesso array di oggetti di voce. Ogni voce ha un `type` che determina i suoi altri campi e una `destination` che controlla dove viene scritta la modifica.

| `type`              | Campi                              | Effetto                                                                                                                                                                                         |
| :------------------ | :--------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `addRules`          | `rules`, `behavior`, `destination` | Aggiunge regole di autorizzazione. `rules` è un array di oggetti `{toolName, ruleContent?}`. Omettere `ruleContent` per abbinare l'intero strumento. `behavior` è `"allow"`, `"deny"` o `"ask"` |
| `replaceRules`      | `rules`, `behavior`, `destination` | Sostituisce tutte le regole del `behavior` dato alla `destination` con le `rules` fornite                                                                                                       |
| `removeRules`       | `rules`, `behavior`, `destination` | Rimuove le regole corrispondenti del `behavior` dato                                                                                                                                            |
| `setMode`           | `mode`, `destination`              | Modifica la modalità di autorizzazione. Le modalità valide sono `default`, `acceptEdits`, `dontAsk`, `bypassPermissions` e `plan`                                                               |
| `addDirectories`    | `directories`, `destination`       | Aggiunge directory di lavoro. `directories` è un array di stringhe di percorso                                                                                                                  |
| `removeDirectories` | `directories`, `destination`       | Rimuove directory di lavoro                                                                                                                                                                     |

Il campo `destination` su ogni voce determina se la modifica rimane in memoria o persiste in un file di impostazioni.

| `destination`     | Scrive in                                            |
| :---------------- | :--------------------------------------------------- |
| `session`         | solo in memoria, scartato quando la sessione termina |
| `localSettings`   | `.claude/settings.local.json`                        |
| `projectSettings` | `.claude/settings.json`                              |
| `userSettings`    | `~/.claude/settings.json`                            |

Un hook può ripetere uno dei `permission_suggestions` che ha ricevuto come suo proprio output `updatedPermissions`, che è equivalente all'utente che seleziona quell'opzione "consenti sempre" nella finestra di dialogo.

### PostToolUse

Viene eseguito immediatamente dopo il completamento riuscito di uno strumento.

Corrisponde al nome dello strumento, stessi valori di PreToolUse.

#### Input di PostToolUse

Gli hook `PostToolUse` si attivano dopo che uno strumento è già stato eseguito con successo. L'input include sia `tool_input`, gli argomenti inviati allo strumento, che `tool_response`, il risultato che ha restituito. Lo schema esatto per entrambi dipende dallo strumento.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

#### Controllo della decisione di PostToolUse

Gli hook `PostToolUse` possono fornire feedback a Claude dopo l'esecuzione dello strumento. Oltre ai [campi di output JSON](#json-output) disponibili per tutti gli hook, lo script del hook può restituire questi campi specifici dell'evento:

| Campo                  | Descrizione                                                                                            |
| :--------------------- | :----------------------------------------------------------------------------------------------------- |
| `decision`             | `"block"` richiede a Claude con il `reason`. Omettere per consentire all'azione di procedere           |
| `reason`               | Spiegazione mostrata a Claude quando `decision` è `"block"`                                            |
| `additionalContext`    | Contesto aggiuntivo per Claude da considerare                                                          |
| `updatedMCPToolOutput` | Solo per [strumenti MCP](#match-mcp-tools): sostituisce l'output dello strumento con il valore fornito |

```json  theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}
```

### PostToolUseFailure

Viene eseguito quando l'esecuzione di uno strumento non riesce. Questo evento si attiva per le chiamate dello strumento che generano errori o restituiscono risultati di errore. Utilizzare questo per registrare i guasti, inviare avvisi o fornire feedback correttivo a Claude.

Corrisponde al nome dello strumento, stessi valori di PreToolUse.

#### Input di PostToolUseFailure

Gli hook PostToolUseFailure ricevono gli stessi campi `tool_name` e `tool_input` di PostToolUse, insieme alle informazioni di errore come campi di livello superiore:

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite"
  },
  "tool_use_id": "toolu_01ABC123...",
  "error": "Command exited with non-zero status code 1",
  "is_interrupt": false
}
```

| Campo          | Descrizione                                                                                |
| :------------- | :----------------------------------------------------------------------------------------- |
| `error`        | Stringa che descrive cosa è andato storto                                                  |
| `is_interrupt` | Booleano facoltativo che indica se il guasto è stato causato dall'interruzione dell'utente |

#### Controllo della decisione di PostToolUseFailure

Gli hook `PostToolUseFailure` possono fornire contesto a Claude dopo un guasto dello strumento. Oltre ai [campi di output JSON](#json-output) disponibili per tutti gli hook, lo script del hook può restituire questi campi specifici dell'evento:

| Campo               | Descrizione                                                      |
| :------------------ | :--------------------------------------------------------------- |
| `additionalContext` | Contesto aggiuntivo per Claude da considerare insieme all'errore |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### PermissionDenied

Viene eseguito quando il classificatore della [modalità automatica](/it/permission-modes#eliminate-prompts-with-auto-mode) nega una chiamata dello strumento. Questo hook si attiva solo in modalità automatica: non viene eseguito quando si nega manualmente una finestra di dialogo di autorizzazione, quando un hook `PreToolUse` blocca una chiamata o quando una regola `deny` corrisponde. Utilizzare questo per registrare i rifiuti del classificatore, regolare la configurazione o dire al modello che può riprovare la chiamata dello strumento.

Corrisponde al nome dello strumento, stessi valori di PreToolUse.

#### Input di PermissionDenied

Oltre ai [campi di input comuni](#common-input-fields), gli hook PermissionDenied ricevono `tool_name`, `tool_input`, `tool_use_id` e `reason`.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "auto",
  "hook_event_name": "PermissionDenied",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/build",
    "description": "Clean build directory"
  },
  "tool_use_id": "toolu_01ABC123...",
  "reason": "Auto mode denied: command targets a path outside the project"
}
```

| Campo    | Descrizione                                                                                        |
| :------- | :------------------------------------------------------------------------------------------------- |
| `reason` | La spiegazione del classificatore per il motivo per cui la chiamata dello strumento è stata negata |

#### Controllo della decisione di PermissionDenied

Gli hook PermissionDenied possono dire al modello che può riprovare la chiamata dello strumento negata. Restituire un oggetto JSON con `hookSpecificOutput.retry` impostato su `true`:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

Quando `retry` è `true`, Claude Code aggiunge un messaggio alla conversazione dicendo al modello che può riprovare la chiamata dello strumento. Il rifiuto stesso non viene invertito. Se l'hook non restituisce JSON o restituisce `retry: false`, il rifiuto rimane e il modello riceve il messaggio di rifiuto originale.

### Notification

Viene eseguito quando Claude Code invia notifiche. Corrisponde al tipo di notifica: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`. Omettere il matcher per eseguire gli hook per tutti i tipi di notifica.

Utilizzare matcher separati per eseguire gestori diversi a seconda del tipo di notifica. Questa configurazione attiva uno script di avviso specifico per l'autorizzazione quando Claude ha bisogno dell'approvazione dell'autorizzazione e una notifica diversa quando Claude è stato inattivo:

```json  theme={null}
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/permission-alert.sh"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/idle-notification.sh"
          }
        ]
      }
    ]
  }
}
```

#### Input di Notification

Oltre ai [campi di input comuni](#common-input-fields), gli hook Notification ricevono `message` con il testo della notifica, un `title` facoltativo e `notification_type` che indica quale tipo si è attivato.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

Gli hook Notification non possono bloccare o modificare le notifiche. Oltre ai [campi di output JSON](#json-output) disponibili per tutti gli hook, è possibile restituire `additionalContext` per aggiungere contesto alla conversazione:

| Campo               | Descrizione                            |
| :------------------ | :------------------------------------- |
| `additionalContext` | Stringa aggiunta al contesto di Claude |

### SubagentStart

Viene eseguito quando un subagent di Claude Code viene generato tramite lo strumento Agent. Supporta i matcher per filtrare per nome del tipo di agente (agenti incorporati come `Bash`, `Explore`, `Plan` o nomi di agenti personalizzati da `.claude/agents/`).

#### Input di SubagentStart

Oltre ai [campi di input comuni](#common-input-fields), gli hook SubagentStart ricevono `agent_id` con l'identificatore univoco per il subagent e `agent_type` con il nome dell'agente (agenti incorporati come `"Bash"`, `"Explore"`, `"Plan"` o nomi di agenti personalizzati).

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

Gli hook SubagentStart non possono bloccare la creazione del subagent, ma possono iniettare contesto nel subagent. Oltre ai [campi di output JSON](#json-output) disponibili per tutti gli hook, è possibile restituire:

| Campo               | Descrizione                               |
| :------------------ | :---------------------------------------- |
| `additionalContext` | Stringa aggiunta al contesto del subagent |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

### SubagentStop

Viene eseguito quando un subagent di Claude Code ha finito di rispondere. Corrisponde al tipo di agente, stessi valori di SubagentStart.

#### Input di SubagentStop

Oltre ai [campi di input comuni](#common-input-fields), gli hook SubagentStop ricevono `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path` e `last_assistant_message`. Il campo `agent_type` è il valore utilizzato per il filtraggio del matcher. Il `transcript_path` è la trascrizione della sessione principale, mentre `agent_transcript_path` è la trascrizione propria del subagent archiviata in una cartella `subagents/` annidato. Il campo `last_assistant_message` contiene il contenuto del testo della risposta finale del subagent, quindi gli hook possono accedervi senza analizzare il file della trascrizione.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../abc123.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/projects/.../abc123/subagents/agent-def456.jsonl",
  "last_assistant_message": "Analysis complete. Found 3 potential issues..."
}
```

Gli hook SubagentStop utilizzano lo stesso formato di controllo della decisione degli [hook Stop](#stop-decision-control).

### TaskCreated

Viene eseguito quando un'attività sta per essere creata tramite lo strumento `TaskCreate`. Utilizzare questo per applicare le convenzioni di denominazione, richiedere descrizioni delle attività o impedire la creazione di determinate attività.

Quando un hook `TaskCreated` esce con il codice 2, l'attività non viene creata e il messaggio stderr viene restituito al modello come feedback. Per interrompere completamente il compagno di squadra invece di rieseguirlo, restituire JSON con `{"continue": false, "stopReason": "..."}`. Gli hook TaskCreated non supportano i matcher e si attivano ad ogni occorrenza.

#### Input di TaskCreated

Oltre ai [campi di input comuni](#common-input-fields), gli hook TaskCreated ricevono `task_id`, `task_subject` e facoltativamente `task_description`, `teammate_name` e `team_name`.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCreated",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

| Campo              | Descrizione                                                          |
| :----------------- | :------------------------------------------------------------------- |
| `task_id`          | Identificatore dell'attività in corso di creazione                   |
| `task_subject`     | Titolo dell'attività                                                 |
| `task_description` | Descrizione dettagliata dell'attività. Può essere assente            |
| `teammate_name`    | Nome del compagno di squadra che crea l'attività. Può essere assente |
| `team_name`        | Nome del team. Può essere assente                                    |

#### Controllo della decisione di TaskCreated

Gli hook TaskCreated supportano due modi per controllare la creazione dell'attività:

* **Codice di uscita 2**: l'attività non viene creata e il messaggio stderr viene restituito al modello come feedback.
* **JSON `{"continue": false, "stopReason": "..."}`**: interrompe completamente il compagno di squadra, corrispondendo al comportamento dell'hook `Stop`. Il `stopReason` viene mostrato all'utente.

Questo esempio blocca le attività i cui soggetti non seguono il formato richiesto:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

if [[ ! "$TASK_SUBJECT" =~ ^\[TICKET-[0-9]+\] ]]; then
  echo "Task subject must start with a ticket number, e.g. '[TICKET-123] Add feature'" >&2
  exit 2
fi

exit 0
```

### TaskCompleted

Viene eseguito quando un'attività sta per essere contrassegnata come completata. Questo si attiva in due situazioni: quando qualsiasi agente contrassegna esplicitamente un'attività come completata attraverso lo strumento TaskUpdate, o quando un compagno di squadra di un [agent team](/it/agent-teams) finisce il suo turno con attività in corso. Utilizzare questo per applicare i criteri di completamento come il passaggio dei test o dei controlli di linting prima che un'attività possa chiudersi.

Quando un hook `TaskCompleted` esce con il codice 2, l'attività non viene contrassegnata come completata e il messaggio stderr viene restituito al modello come feedback. Per interrompere completamente il compagno di squadra invece di rieseguirlo, restituire JSON con `{"continue": false, "stopReason": "..."}`. Gli hook TaskCompleted non supportano i matcher e si attivano ad ogni occorrenza.

#### Input di TaskCompleted

Oltre ai [campi di input comuni](#common-input-fields), gli hook TaskCompleted ricevono `task_id`, `task_subject` e facoltativamente `task_description`, `teammate_name` e `team_name`.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCompleted",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

| Campo              | Descrizione                                                              |
| :----------------- | :----------------------------------------------------------------------- |
| `task_id`          | Identificatore dell'attività in corso di completamento                   |
| `task_subject`     | Titolo dell'attività                                                     |
| `task_description` | Descrizione dettagliata dell'attività. Può essere assente                |
| `teammate_name`    | Nome del compagno di squadra che completa l'attività. Può essere assente |
| `team_name`        | Nome del team. Può essere assente                                        |

#### Controllo della decisione di TaskCompleted

Gli hook TaskCompleted supportano due modi per controllare il completamento dell'attività:

* **Codice di uscita 2**: l'attività non viene contrassegnata come completata e il messaggio stderr viene restituito al modello come feedback.
* **JSON `{"continue": false, "stopReason": "..."}`**: interrompe completamente il compagno di squadra, corrispondendo al comportamento dell'hook `Stop`. Il `stopReason` viene mostrato all'utente.

Questo esempio esegue i test e blocca il completamento dell'attività se non riescono:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

# Eseguire la suite di test
if ! npm test 2>&1; then
  echo "Tests not passing. Fix failing tests before completing: $TASK_SUBJECT" >&2
  exit 2
fi

exit 0
```

### Stop

Viene eseguito quando l'agente Claude Code principale ha finito di rispondere. Non viene eseguito se l'arresto si è verificato a causa di un'interruzione dell'utente. Gli errori API attivano [StopFailure](#stopfailure) invece.

#### Input di Stop

Oltre ai [campi di input comuni](#common-input-fields), gli hook Stop ricevono `stop_hook_active` e `last_assistant_message`. Il campo `stop_hook_active` è `true` quando Claude Code sta già continuando a causa di un hook di arresto. Controllare questo valore o elaborare la trascrizione per impedire a Claude Code di eseguire indefinitamente. Il campo `last_assistant_message` contiene il contenuto del testo della risposta finale di Claude, quindi gli hook possono accedervi senza analizzare il file della trascrizione.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true,
  "last_assistant_message": "I've completed the refactoring. Here's a summary..."
}
```

#### Controllo della decisione di Stop

Gli hook `Stop` e `SubagentStop` possono controllare se Claude continua. Oltre ai [campi di output JSON](#json-output) disponibili per tutti gli hook, lo script del hook può restituire questi campi specifici dell'evento:

| Campo      | Descrizione                                                                            |
| :--------- | :------------------------------------------------------------------------------------- |
| `decision` | `"block"` impedisce a Claude di fermarsi. Omettere per consentire a Claude di fermarsi |
| `reason`   | Obbligatorio quando `decision` è `"block"`. Dice a Claude perché dovrebbe continuare   |

```json  theme={null}
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

### StopFailure

Viene eseguito invece di [Stop](#stop) quando il turno termina a causa di un errore API. L'output e il codice di uscita vengono ignorati. Utilizzare questo per registrare i guasti, inviare avvisi o intraprendere azioni di recupero quando Claude non può completare una risposta a causa di limiti di velocità, problemi di autenticazione o altri errori API.

#### Input di StopFailure

Oltre ai [campi di input comuni](#common-input-fields), gli hook StopFailure ricevono `error`, `error_details` facoltativo e `last_assistant_message` facoltativo. Il campo `error` identifica il tipo di errore ed è utilizzato per il filtraggio del matcher.

| Campo                    | Descrizione                                                                                                                                                                                                                                                              |
| :----------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `error`                  | Tipo di errore: `rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens` o `unknown`                                                                                                                               |
| `error_details`          | Dettagli aggiuntivi sull'errore, quando disponibili                                                                                                                                                                                                                      |
| `last_assistant_message` | Il testo di errore renderizzato mostrato nella conversazione. A differenza di `Stop` e `SubagentStop`, dove questo campo contiene l'output conversazionale di Claude, per `StopFailure` contiene la stringa di errore API stessa, come `"API Error: Rate limit reached"` |

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "StopFailure",
  "error": "rate_limit",
  "error_details": "429 Too Many Requests",
  "last_assistant_message": "API Error: Rate limit reached"
}
```

Gli hook StopFailure non hanno controllo della decisione. Vengono eseguiti solo per scopi di notifica e registrazione.

### TeammateIdle

Viene eseguito quando un compagno di squadra di un [agent team](/it/agent-teams) sta per andare inattivo dopo aver finito il suo turno. Utilizzare questo per applicare gate di qualità prima che un compagno di squadra smetta di lavorare, come richiedere il passaggio dei controlli di linting o verificare che i file di output esistano.

Quando un hook `TeammateIdle` esce con il codice 2, il compagno di squadra riceve il messaggio stderr come feedback e continua a lavorare invece di andare inattivo. Per interrompere completamente il compagno di squadra invece di rieseguirlo, restituire JSON con `{"continue": false, "stopReason": "..."}`. Gli hook TeammateIdle non supportano i matcher e si attivano ad ogni occorrenza.

#### Input di TeammateIdle

Oltre ai [campi di input comuni](#common-input-fields), gli hook TeammateIdle ricevono `teammate_name` e `team_name`.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "my-project"
}
```

| Campo           | Descrizione                                              |
| :-------------- | :------------------------------------------------------- |
| `teammate_name` | Nome del compagno di squadra che sta per andare inattivo |
| `team_name`     | Nome del team                                            |

#### Controllo della decisione di TeammateIdle

Gli hook TeammateIdle supportano due modi per controllare il comportamento del compagno di squadra:

* **Codice di uscita 2**: il compagno di squadra riceve il messaggio stderr come feedback e continua a lavorare invece di andare inattivo.
* **JSON `{"continue": false, "stopReason": "..."}`**: interrompe completamente il compagno di squadra, corrispondendo al comportamento dell'hook `Stop`. Il `stopReason` viene mostrato all'utente.

Questo esempio controlla che un artefatto di build esista prima di consentire a un compagno di squadra di andare inattivo:

```bash  theme={null}
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2
fi

exit 0
```

### ConfigChange

Viene eseguito quando un file di configurazione cambia durante una sessione. Utilizzare questo per controllare le modifiche alle impostazioni, applicare le politiche di sicurezza o bloccare le modifiche non autorizzate ai file di configurazione.

Gli hook ConfigChange si attivano per le modifiche ai file di impostazioni, alle impostazioni della politica gestita e ai file di skill. Il campo `source` nell'input dice quale tipo di configurazione è cambiato e il campo `file_path` facoltativo fornisce il percorso al file modificato.

Il matcher filtra sulla fonte di configurazione:

| Matcher            | Quando si attiva                                |
| :----------------- | :---------------------------------------------- |
| `user_settings`    | `~/.claude/settings.json` cambia                |
| `project_settings` | `.claude/settings.json` cambia                  |
| `local_settings`   | `.claude/settings.local.json` cambia            |
| `policy_settings`  | Le impostazioni della politica gestita cambiano |
| `skills`           | Un file di skill in `.claude/skills/` cambia    |

Questo esempio registra tutte le modifiche di configurazione per il controllo della sicurezza:

```json  theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/audit-config-change.sh"
          }
        ]
      }
    ]
  }
}
```

#### Input di ConfigChange

Oltre ai [campi di input comuni](#common-input-fields), gli hook ConfigChange ricevono `source` e facoltativamente `file_path`. Il campo `source` indica quale tipo di configurazione è cambiato e `file_path` fornisce il percorso al file specifico che è stato modificato.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "ConfigChange",
  "source": "project_settings",
  "file_path": "/Users/.../my-project/.claude/settings.json"
}
```

#### Controllo della decisione di ConfigChange

Gli hook ConfigChange possono bloccare le modifiche di configurazione dall'avere effetto. Utilizzare il codice di uscita 2 o un JSON `decision` per impedire la modifica. Quando bloccato, le nuove impostazioni non vengono applicate alla sessione in esecuzione.

| Campo      | Descrizione                                                                                              |
| :--------- | :------------------------------------------------------------------------------------------------------- |
| `decision` | `"block"` impedisce l'applicazione della modifica di configurazione. Omettere per consentire la modifica |
| `reason`   | Spiegazione mostrata all'utente quando `decision` è `"block"`                                            |

```json  theme={null}
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

Le modifiche a `policy_settings` non possono essere bloccate. Gli hook si attivano ancora per le fonti `policy_settings`, quindi è possibile utilizzarli per la registrazione di audit, ma qualsiasi decisione di blocco viene ignorata. Ciò garantisce che le impostazioni gestite dall'azienda abbiano sempre effetto.

### CwdChanged

Viene eseguito quando la directory di lavoro cambia durante una sessione, ad esempio quando Claude esegue un comando `cd`. Utilizzare questo per reagire ai cambi di directory: ricaricare le variabili di ambiente, attivare toolchain specifiche del progetto o eseguire script di configurazione automaticamente. Si accoppia con [FileChanged](#filechanged) per strumenti come [direnv](https://direnv.net/) che gestiscono l'ambiente per directory.

Gli hook CwdChanged hanno accesso a `CLAUDE_ENV_FILE`. Le variabili scritte in quel file persistono nei comandi Bash successivi per la sessione, proprio come negli [hook SessionStart](#persist-environment-variables). Solo gli hook `type: "command"` sono supportati.

CwdChanged non supporta i matcher e si attiva ad ogni cambio di directory.

#### Input di CwdChanged

Oltre ai [campi di input comuni](#common-input-fields), gli hook CwdChanged ricevono `old_cwd` e `new_cwd`.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project/src",
  "hook_event_name": "CwdChanged",
  "old_cwd": "/Users/my-project",
  "new_cwd": "/Users/my-project/src"
}
```

#### Output di CwdChanged

Oltre ai [campi di output JSON](#json-output) disponibili per tutti gli hook, gli hook CwdChanged possono restituire `watchPaths` per impostare dinamicamente quali percorsi di file [FileChanged](#filechanged) monitora:

| Campo        | Descrizione                                                                                                                                                                                                                                                             |
| :----------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `watchPaths` | Array di percorsi assoluti. Sostituisce l'elenco di monitoraggio dinamico corrente (i percorsi dalla configurazione del `matcher` vengono sempre monitorati). Restituire un array vuoto cancella l'elenco dinamico, che è tipico quando si entra in una nuova directory |

Gli hook CwdChanged non hanno controllo della decisione. Non possono bloccare il cambio di directory.

### FileChanged

Viene eseguito quando un file monitorato cambia su disco. Il campo `matcher` nella configurazione del hook controlla quali nomi di file monitorare: è un elenco separato da pipe di basename (nomi di file senza percorsi di directory, ad esempio `".envrc|.env"`). Lo stesso valore `matcher` viene anche utilizzato per filtrare quali hook vengono eseguiti quando un file cambia, abbinando il basename del file modificato. Utile per ricaricare le variabili di ambiente quando i file di configurazione del progetto vengono modificati.

Gli hook FileChanged hanno accesso a `CLAUDE_ENV_FILE`. Le variabili scritte in quel file persistono nei comandi Bash successivi per la sessione, proprio come negli [hook SessionStart](#persist-environment-variables). Solo gli hook `type: "command"` sono supportati.

#### Input di FileChanged

Oltre ai [campi di input comuni](#common-input-fields), gli hook FileChanged ricevono `file_path` e `event`.

| Campo       | Descrizione                                                                                        |
| :---------- | :------------------------------------------------------------------------------------------------- |
| `file_path` | Percorso assoluto al file che è cambiato                                                           |
| `event`     | Cosa è accaduto: `"change"` (file modificato), `"add"` (file creato) o `"unlink"` (file eliminato) |

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "FileChanged",
  "file_path": "/Users/my-project/.envrc",
  "event": "change"
}
```

#### Output di FileChanged

Oltre ai [campi di output JSON](#json-output) disponibili per tutti gli hook, gli hook FileChanged possono restituire `watchPaths` per aggiornare dinamicamente quali percorsi di file vengono monitorati:

| Campo        | Descrizione                                                                                                                                                                                                                                                               |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `watchPaths` | Array di percorsi assoluti. Sostituisce l'elenco di monitoraggio dinamico corrente (i percorsi dalla configurazione del `matcher` vengono sempre monitorati). Utilizzare questo quando lo script del hook scopre file aggiuntivi da monitorare in base al file modificato |

Gli hook FileChanged non hanno controllo della decisione. Non possono bloccare il cambio di file dall'occorrenza.

### WorktreeCreate

Quando si esegue `claude --worktree` o un [subagent utilizza `isolation: "worktree"`](/it/sub-agents#choose-the-subagent-scope), Claude Code crea una copia di lavoro isolata utilizzando `git worktree`. Se si configura un hook WorktreeCreate, sostituisce il comportamento git predefinito, consentendo di utilizzare un sistema di controllo della versione diverso come SVN, Perforce o Mercurial.

Poiché l'hook sostituisce completamente il comportamento predefinito, [`.worktreeinclude`](/it/common-workflows#copy-gitignored-files-to-worktrees) non viene elaborato. Se è necessario copiare i file di configurazione locali come `.env` nel nuovo worktree, farlo all'interno dello script del hook.

L'hook deve restituire il percorso assoluto della directory del worktree creato. Claude Code utilizza questo percorso come directory di lavoro per la sessione isolata. I command hook lo stampano su stdout; gli HTTP hook lo restituiscono tramite `hookSpecificOutput.worktreePath`. Il fallimento del hook o il percorso mancante non riesce nella creazione.

Questo esempio crea una copia di lavoro SVN e stampa il percorso per Claude Code da utilizzare. Sostituire l'URL del repository con il proprio:

```json  theme={null}
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

L'hook legge il `name` del worktree dall'input JSON su stdin, controlla una copia fresca in una nuova directory e stampa il percorso della directory. L'`echo` sull'ultima riga è quello che Claude Code legge come percorso del worktree. Reindirizzare qualsiasi altro output a stderr in modo che non interferisca con il percorso.

#### Input di WorktreeCreate

Oltre ai [campi di input comuni](#common-input-fields), gli hook WorktreeCreate ricevono il campo `name`. Questo è un identificatore slug per il nuovo worktree, specificato dall'utente o generato automaticamente (ad esempio, `bold-oak-a3f2`).

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

#### Output di WorktreeCreate

Gli hook WorktreeCreate non utilizzano il modello di decisione di blocco/consentimento standard. Invece, il successo o il fallimento dell'hook determina il risultato. L'hook deve restituire il percorso assoluto della directory del worktree creato:

* **Command hooks** (`type: "command"`): stampano il percorso su stdout.
* **HTTP hooks** (`type: "http"`): restituiscono `{ "hookSpecificOutput": { "hookEventName": "WorktreeCreate", "worktreePath": "/absolute/path" } }` nel corpo della risposta.

Se l'hook non riesce o non produce un percorso, la creazione del worktree non riesce con un errore.

### WorktreeRemove

La controparte di pulizia di [WorktreeCreate](#worktreecreate). Questo hook si attiva quando un worktree viene rimosso, sia quando si esce da una sessione `--worktree` e si sceglie di rimuoverla, sia quando un subagent con `isolation: "worktree"` termina. Per i worktree basati su git, Claude gestisce la pulizia automaticamente con `git worktree remove`. Se si è configurato un hook WorktreeCreate per un sistema di controllo della versione non-git, accoppiarlo con un hook WorktreeRemove per gestire la pulizia. Senza uno, la directory del worktree viene lasciata su disco.

Claude Code passa il percorso restituito da WorktreeCreate come `worktree_path` nell'input del hook. Questo esempio legge quel percorso e rimuove la directory:

```json  theme={null}
{
  "hooks": {
    "WorktreeRemove": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'jq -r .worktree_path | xargs rm -rf'"
          }
        ]
      }
    ]
  }
}
```

#### Input di WorktreeRemove

Oltre ai [campi di input comuni](#common-input-fields), gli hook WorktreeRemove ricevono il campo `worktree_path`, che è il percorso assoluto al worktree in corso di rimozione.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

Gli hook WorktreeRemove non hanno controllo della decisione. Non possono bloccare la rimozione del worktree ma possono eseguire attività di pulizia come la rimozione dello stato del controllo della versione o l'archiviazione delle modifiche. I guasti degli hook vengono registrati solo in modalità debug.

### PreCompact

Viene eseguito prima che Claude Code stia per eseguire un'operazione di compattazione.

Il valore del matcher indica se la compattazione è stata attivata manualmente o automaticamente:

| Matcher  | Quando si attiva                                                |
| :------- | :-------------------------------------------------------------- |
| `manual` | `/compact`                                                      |
| `auto`   | Compattazione automatica quando la finestra di contesto è piena |

#### Input di PreCompact

Oltre ai [campi di input comuni](#common-input-fields), gli hook PreCompact ricevono `trigger` e `custom_instructions`. Per `manual`, `custom_instructions` contiene quello che l'utente passa in `/compact`. Per `auto`, `custom_instructions` è vuoto.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### PostCompact

Viene eseguito dopo che Claude Code completa un'operazione di compattazione. Utilizzare questo evento per reagire al nuovo stato compattato, ad esempio per registrare il riepilogo generato o aggiornare lo stato esterno.

Gli stessi valori di matcher si applicano come per `PreCompact`:

| Matcher  | Quando si attiva                                                        |
| :------- | :---------------------------------------------------------------------- |
| `manual` | Dopo `/compact`                                                         |
| `auto`   | Dopo la compattazione automatica quando la finestra di contesto è piena |

#### Input di PostCompact

Oltre ai [campi di input comuni](#common-input-fields), gli hook PostCompact ricevono `trigger` e `compact_summary`. Il campo `compact_summary` contiene il riepilogo della conversazione generato dall'operazione di compattazione.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostCompact",
  "trigger": "manual",
  "compact_summary": "Summary of the compacted conversation..."
}
```

Gli hook PostCompact non hanno controllo della decisione. Non possono influenzare il risultato della compattazione ma possono eseguire attività di follow-up.

### SessionEnd

Viene eseguito quando una sessione di Claude Code termina. Utile per le attività di pulizia, la registrazione delle statistiche della sessione o il salvataggio dello stato della sessione. Supporta i matcher per filtrare per motivo di uscita.

Il campo `reason` nell'input del hook indica perché la sessione è terminata:

| Motivo                        | Descrizione                                                     |
| :---------------------------- | :-------------------------------------------------------------- |
| `clear`                       | Sessione cancellata con il comando `/clear`                     |
| `resume`                      | Sessione commutata tramite `/resume` interattivo                |
| `logout`                      | L'utente ha effettuato il logout                                |
| `prompt_input_exit`           | L'utente è uscito mentre l'input del prompt era visibile        |
| `bypass_permissions_disabled` | La modalità di bypass delle autorizzazioni è stata disabilitata |
| `other`                       | Altri motivi di uscita                                          |

#### Input di SessionEnd

Oltre ai [campi di input comuni](#common-input-fields), gli hook SessionEnd ricevono un campo `reason` che indica perché la sessione è terminata. Consultare la [tabella dei motivi](#sessionend) sopra per tutti i valori.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

Gli hook SessionEnd non hanno controllo della decisione. Non possono bloccare la terminazione della sessione ma possono eseguire attività di pulizia.

Gli hook SessionEnd hanno un timeout predefinito di 1,5 secondi. Questo si applica all'uscita della sessione, `/clear` e al cambio di sessioni tramite `/resume` interattivo. Se i hook hanno bisogno di più tempo, impostare la variabile di ambiente `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` su un valore più alto in millisecondi. Qualsiasi impostazione `timeout` per hook è anche limitata da questo valore.

```bash  theme={null}
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000 claude
```

### Elicitation

Viene eseguito quando un server MCP richiede l'input dell'utente a metà attività. Per impostazione predefinita, Claude Code mostra una finestra di dialogo interattiva per l'utente per rispondere. Gli hook possono intercettare questa richiesta e rispondere a livello di programmazione, saltando completamente la finestra di dialogo.

Il campo matcher corrisponde al nome del server MCP.

#### Input di Elicitation

Oltre ai [campi di input comuni](#common-input-fields), gli hook Elicitation ricevono `mcp_server_name`, `message` e campi facoltativi `mode`, `url`, `elicitation_id` e `requested_schema`.

Per l'elicitazione in modalità modulo (il caso più comune):

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please provide your credentials",
  "mode": "form",
  "requested_schema": {
    "type": "object",
    "properties": {
      "username": { "type": "string", "title": "Username" }
    }
  }
}
```

Per l'elicitazione in modalità URL (autenticazione basata su browser):

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please authenticate",
  "mode": "url",
  "url": "https://auth.example.com/login"
}
```

#### Output di Elicitation

Per rispondere a livello di programmazione senza mostrare la finestra di dialogo, restituire un oggetto JSON con `hookSpecificOutput`:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept",
    "content": {
      "username": "alice"
    }
  }
}
```

| Campo     | Valori                        | Descrizione                                                                        |
| :-------- | :---------------------------- | :--------------------------------------------------------------------------------- |
| `action`  | `accept`, `decline`, `cancel` | Se accettare, rifiutare o annullare la richiesta                                   |
| `content` | object                        | Valori dei campi del modulo da inviare. Utilizzato solo quando `action` è `accept` |

Il codice di uscita 2 nega l'elicitazione e mostra stderr all'utente.

### ElicitationResult

Viene eseguito dopo che un utente risponde a un'elicitazione MCP. Gli hook possono osservare, modificare o bloccare la risposta prima che venga inviata al server MCP.

Il campo matcher corrisponde al nome del server MCP.

#### Input di ElicitationResult

Oltre ai [campi di input comuni](#common-input-fields), gli hook ElicitationResult ricevono `mcp_server_name`, `action` e campi facoltativi `mode`, `elicitation_id` e `content`.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "ElicitationResult",
  "mcp_server_name": "my-mcp-server",
  "action": "accept",
  "content": { "username": "alice" },
  "mode": "form",
  "elicitation_id": "elicit-123"
}
```

#### Output di ElicitationResult

Per sovrascrivere la risposta dell'utente, restituire un oggetto JSON con `hookSpecificOutput`:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "ElicitationResult",
    "action": "decline",
    "content": {}
  }
}
```

| Campo     | Valori                        | Descrizione                                                                              |
| :-------- | :---------------------------- | :--------------------------------------------------------------------------------------- |
| `action`  | `accept`, `decline`, `cancel` | Sovrascrive l'azione dell'utente                                                         |
| `content` | object                        | Sovrascrive i valori dei campi del modulo. Significativo solo quando `action` è `accept` |

Il codice di uscita 2 blocca la risposta, cambiando l'azione effettiva in `decline`.

## Hook basati su prompt

Oltre ai command hook e agli HTTP hook, Claude Code supporta gli hook basati su prompt (`type: "prompt"`) che utilizzano un LLM per valutare se consentire o bloccare un'azione, e gli hook basati su agenti (`type: "agent"`) che generano un verificatore agentico con accesso agli strumenti. Non tutti gli eventi supportano ogni tipo di hook.

Gli eventi che supportano tutti e quattro i tipi di hook (`command`, `http`, `prompt` e `agent`):

* `PermissionRequest`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `TaskCreated`
* `UserPromptSubmit`

Gli eventi che supportano gli hook `command` e `http` ma non `prompt` o `agent`:

* `ConfigChange`
* `CwdChanged`
* `Elicitation`
* `ElicitationResult`
* `FileChanged`
* `InstructionsLoaded`
* `Notification`
* `PermissionDenied`
* `PostCompact`
* `PreCompact`
* `SessionEnd`
* `StopFailure`
* `SubagentStart`
* `TeammateIdle`
* `WorktreeCreate`
* `WorktreeRemove`

`SessionStart` supporta solo gli hook `command`.

### Come funzionano gli hook basati su prompt

Invece di eseguire un comando Bash, gli hook basati su prompt:

1. Inviano l'input del hook e il prompt a un modello Claude, Haiku per impostazione predefinita
2. L'LLM risponde con JSON strutturato contenente una decisione
3. Claude Code elabora automaticamente la decisione

### Configurazione del prompt hook

Impostare `type` su `"prompt"` e fornire una stringa `prompt` invece di un `command`. Utilizzare il segnaposto `$ARGUMENTS` per iniettare i dati di input JSON del hook nel testo del prompt. Claude Code invia il prompt combinato e l'input a un modello Claude veloce, che restituisce una decisione JSON.

Questo hook `Stop` chiede all'LLM di valutare se Claude dovrebbe fermarsi prima di consentire a Claude di finire:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
          }
        ]
      }
    ]
  }
}
```

| Campo     | Obbligatorio | Descrizione                                                                                                                                                                      |
| :-------- | :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`    | sì           | Deve essere `"prompt"`                                                                                                                                                           |
| `prompt`  | sì           | Il testo del prompt da inviare all'LLM. Utilizzare `$ARGUMENTS` come segnaposto per l'input JSON del hook. Se `$ARGUMENTS` non è presente, l'input JSON viene aggiunto al prompt |
| `model`   | no           | Modello da utilizzare per la valutazione. Impostazione predefinita: un modello veloce                                                                                            |
| `timeout` | no           | Timeout in secondi. Impostazione predefinita: 30                                                                                                                                 |

### Schema di risposta

L'LLM deve rispondere con JSON contenente:

```json  theme={null}
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

| Campo    | Descrizione                                                       |
| :------- | :---------------------------------------------------------------- |
| `ok`     | `true` consente l'azione, `false` la impedisce                    |
| `reason` | Obbligatorio quando `ok` è `false`. Spiegazione mostrata a Claude |

### Esempio: Hook Stop con criteri multipli

Questo hook `Stop` utilizza un prompt dettagliato per controllare tre condizioni prima di consentire a Claude di fermarsi. Se `"ok"` è `false`, Claude continua a lavorare con il motivo fornito come sua prossima istruzione. Gli hook `SubagentStop` utilizzano lo stesso formato per valutare se un [subagent](/it/sub-agents) dovrebbe fermarsi:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Hook basati su agenti

Gli hook basati su agenti (`type: "agent"`) sono come gli hook basati su prompt ma con accesso agli strumenti multi-turno. Invece di una singola chiamata LLM, un hook agente genera un subagent che può leggere file, cercare codice e ispezionare il codebase per verificare le condizioni. Gli hook agente supportano gli stessi eventi degli hook basati su prompt.

### Come funzionano gli hook basati su agenti

Quando un hook agente si attiva:

1. Claude Code genera un subagent con il prompt e l'input JSON del hook
2. Il subagent può utilizzare strumenti come Read, Grep e Glob per investigare
3. Dopo fino a 50 turni, il subagent restituisce una decisione strutturata `{ "ok": true/false }`
4. Claude Code elabora la decisione nello stesso modo di un hook di prompt

Gli hook agente sono utili quando la verifica richiede l'ispezione dei file effettivi o dell'output dei test, non solo la valutazione dei dati di input del hook da soli.

### Configurazione dell'hook agente

Impostare `type` su `"agent"` e fornire una stringa `prompt`. I campi di configurazione sono gli stessi degli [hook di prompt](#prompt-hook-configuration), con un timeout predefinito più lungo:

| Campo     | Obbligatorio | Descrizione                                                                                            |
| :-------- | :----------- | :----------------------------------------------------------------------------------------------------- |
| `type`    | sì           | Deve essere `"agent"`                                                                                  |
| `prompt`  | sì           | Prompt che descrive cosa verificare. Utilizzare `$ARGUMENTS` come segnaposto per l'input JSON del hook |
| `model`   | no           | Modello da utilizzare. Impostazione predefinita: un modello veloce                                     |
| `timeout` | no           | Timeout in secondi. Impostazione predefinita: 60                                                       |

Lo schema di risposta è lo stesso degli hook di prompt: `{ "ok": true }` per consentire o `{ "ok": false, "reason": "..." }` per bloccare.

Questo hook `Stop` verifica che tutti i test unitari passino prima di consentire a Claude di finire:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

## Eseguire i hook in background

Per impostazione predefinita, gli hook bloccano l'esecuzione di Claude fino al completamento. Per le attività a lunga esecuzione come distribuzioni, suite di test o chiamate API esterne, impostare `"async": true` per eseguire l'hook in background mentre Claude continua a lavorare. Gli hook asincroni non possono bloccare o controllare il comportamento di Claude: i campi di risposta come `decision`, `permissionDecision` e `continue` non hanno effetto, perché l'azione che avrebbero controllato è già stata completata.

### Configurare un hook asincrono

Aggiungere `"async": true` alla configurazione di un command hook per eseguirlo in background senza bloccare Claude. Questo campo è disponibile solo sui hook `type: "command"`.

Questo hook esegue uno script di test dopo ogni chiamata dello strumento `Write`. Claude continua a lavorare immediatamente mentre `run-tests.sh` viene eseguito per un massimo di 120 secondi. Quando lo script termina, l'output viene consegnato al turno di conversazione successivo:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

Il campo `timeout` imposta il tempo massimo in secondi per il processo in background. Se non specificato, gli hook asincroni utilizzano lo stesso timeout predefinito di 10 minuti degli hook sincroni.

### Come vengono eseguiti gli hook asincroni

Quando un hook asincrono si attiva, Claude Code avvia il processo del hook e continua immediatamente senza aspettare il completamento. L'hook riceve lo stesso input JSON tramite stdin di un hook sincrono.

Dopo che il processo in background esce, se l'hook ha prodotto una risposta JSON con un campo `systemMessage` o `additionalContext`, quel contenuto viene consegnato a Claude come contesto al turno di conversazione successivo.

Le notifiche di completamento degli hook asincroni sono soppresse per impostazione predefinita. Per vederle, abilitare la modalità verbose con `Ctrl+O` o avviare Claude Code con `--verbose`.

### Esempio: eseguire i test dopo le modifiche ai file

Questo hook avvia una suite di test in background ogni volta che Claude scrive un file, quindi segnala i risultati a Claude quando i test terminano. Salvare questo script in `.claude/hooks/run-tests-async.sh` nel progetto e renderlo eseguibile con `chmod +x`:

```bash  theme={null}
#!/bin/bash
# run-tests-async.sh

# Leggere l'input del hook da stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Eseguire i test solo per i file di origine
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# Eseguire i test e segnalare i risultati tramite systemMessage
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "{\"systemMessage\": \"Tests passed after editing $FILE_PATH\"}"
else
  echo "{\"systemMessage\": \"Tests failed after editing $FILE_PATH: $RESULT\"}"
fi
```

Quindi aggiungere questa configurazione a `.claude/settings.json` nella radice del progetto. Il flag `async: true` consente a Claude di continuare a lavorare mentre i test vengono eseguiti:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run-tests-async.sh",
            "async": true,
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

### Limitazioni

Gli hook asincroni hanno diversi vincoli rispetto agli hook sincroni:

* Solo gli hook `type: "command"` supportano `async`. Gli hook basati su prompt non possono essere eseguiti in modo asincrono.
* Gli hook asincroni non possono bloccare le chiamate dello strumento o restituire decisioni. Nel momento in cui l'hook si completa, l'azione che lo ha attivato è già stata eseguita.
* L'output del hook viene consegnato al turno di conversazione successivo. Se la sessione è inattiva, la risposta attende fino alla prossima interazione dell'utente.
* Ogni esecuzione crea un processo in background separato. Non c'è deduplicazione tra più attivazioni dello stesso hook asincrono.

## Considerazioni sulla sicurezza

### Disclaimer

I command hook vengono eseguiti con i permessi completi dell'utente del sistema.

<Warning>
  I command hook eseguono comandi shell con i permessi completi dell'utente. Possono modificare, eliminare o accedere a qualsiasi file a cui l'account utente può accedere. Rivedere e testare tutti i comandi del hook prima di aggiungerli alla configurazione.
</Warning>

### Migliori pratiche di sicurezza

Tenere presenti queste pratiche quando si scrivono i hook:

* **Convalidare e disinfettare gli input**: non fidarsi mai ciecamente dei dati di input
* **Citare sempre le variabili shell**: utilizzare `"$VAR"` non `$VAR`
* **Bloccare l'attraversamento del percorso**: controllare `..` nei percorsi dei file
* **Utilizzare percorsi assoluti**: specificare percorsi completi per gli script, utilizzando `"$CLAUDE_PROJECT_DIR"` per la radice del progetto
* **Saltare i file sensibili**: evitare `.env`, `.git/`, chiavi, ecc.

## Strumento Windows PowerShell

Su Windows, è possibile eseguire singoli hook in PowerShell impostando `"shell": "powershell"` su un command hook. Gli hook generano PowerShell direttamente, quindi questo funziona indipendentemente dal fatto che `CLAUDE_CODE_USE_POWERSHELL_TOOL` sia impostato. Claude Code rileva automaticamente `pwsh.exe` (PowerShell 7+) con un fallback a `powershell.exe` (5.1).

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "command": "Write-Host 'File written'"
          }
        ]
      }
    ]
  }
}
```

## Debug dei hook

Eseguire `claude --debug` per visualizzare i dettagli dell'esecuzione del hook, inclusi quali hook corrispondono, i loro codici di uscita e l'output.

```text  theme={null}
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

Per dettagli di corrispondenza dei hook più granulari, impostare `CLAUDE_CODE_DEBUG_LOG_LEVEL=verbose` per visualizzare righe di log aggiuntive come i conteggi dei matcher del hook e la corrispondenza delle query.

Per la risoluzione dei problemi comuni come i hook che non si attivano, i cicli infiniti di Stop hook o gli errori di configurazione, consultare [Limitations and troubleshooting](/it/hooks-guide#limitations-and-troubleshooting) nella guida.
