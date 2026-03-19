> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Automatizzare i flussi di lavoro con hooks

> Esegui comandi shell automaticamente quando Claude Code modifica file, completa attività o ha bisogno di input. Formatta il codice, invia notifiche, convalida comandi e applica le regole del progetto.

Gli hooks sono comandi shell definiti dall'utente che si eseguono in punti specifici del ciclo di vita di Claude Code. Forniscono un controllo deterministico sul comportamento di Claude Code, garantendo che determinate azioni avvengano sempre piuttosto che affidarsi al modello linguistico per scegliere di eseguirle. Utilizza gli hooks per applicare le regole del progetto, automatizzare attività ripetitive e integrare Claude Code con i tuoi strumenti esistenti.

Per decisioni che richiedono giudizio piuttosto che regole deterministiche, puoi anche utilizzare [hooks basati su prompt](#prompt-based-hooks) o [hooks basati su agenti](#agent-based-hooks) che utilizzano un modello Claude per valutare le condizioni.

Per altri modi di estendere Claude Code, vedi [skills](/it/skills) per fornire a Claude istruzioni aggiuntive e comandi eseguibili, [subagents](/it/sub-agents) per eseguire attività in contesti isolati, e [plugins](/it/plugins) per pacchettizzare estensioni da condividere tra i progetti.

<Tip>
  Questa guida copre i casi d'uso comuni e come iniziare. Per schemi di eventi completi, formati di input/output JSON e funzionalità avanzate come hooks asincroni e hooks di strumenti MCP, vedi il [riferimento Hooks](/it/hooks).
</Tip>

## Configura il tuo primo hook

Il modo più veloce per creare un hook è attraverso il menu interattivo `/hooks` in Claude Code. Questa procedura crea un hook di notifica desktop, in modo da ricevere un avviso ogni volta che Claude sta aspettando il tuo input invece di guardare il terminale.

<Steps>
  <Step title="Apri il menu degli hooks">
    Digita `/hooks` nella CLI di Claude Code. Vedrai un elenco di tutti gli eventi hook disponibili, più un'opzione per disabilitare tutti gli hooks. Ogni evento corrisponde a un punto nel ciclo di vita di Claude dove puoi eseguire codice personalizzato. Seleziona `Notification` per creare un hook che si attiva quando Claude ha bisogno della tua attenzione.
  </Step>

  <Step title="Configura il matcher">
    Il menu mostra un elenco di matcher, che filtrano quando l'hook si attiva. Imposta il matcher su `*` per attivarsi su tutti i tipi di notifica. Puoi restringerlo in seguito cambiando il matcher a un valore specifico come `permission_prompt` o `idle_prompt`.
  </Step>

  <Step title="Aggiungi il tuo comando">
    Seleziona `+ Add new hook…`. Il menu ti chiede un comando shell da eseguire quando l'evento si attiva. Gli hooks eseguono qualsiasi comando shell tu fornisca, quindi puoi utilizzare lo strumento di notifica integrato della tua piattaforma. Copia il comando per il tuo sistema operativo:

    <Tabs>
      <Tab title="macOS">
        Utilizza [`osascript`](https://ss64.com/mac/osascript.html) per attivare una notifica macOS nativa tramite AppleScript:

        ```bash  theme={null}
        osascript -e 'display notification "Claude Code needs your attention" with title "Claude Code"'
        ```
      </Tab>

      <Tab title="Linux">
        Utilizza `notify-send`, che è preinstallato sulla maggior parte dei desktop Linux con un daemon di notifica:

        ```bash  theme={null}
        notify-send 'Claude Code' 'Claude Code needs your attention'
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        Utilizza PowerShell per mostrare una finestra di messaggio nativa tramite Windows Forms di .NET:

        ```powershell  theme={null}
        powershell.exe -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')"
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Scegli una posizione di archiviazione">
    Il menu ti chiede dove salvare la configurazione dell'hook. Seleziona `User settings` per archiviarla in `~/.claude/settings.json`, che applica l'hook a tutti i tuoi progetti. Potresti anche scegliere `Project settings` per limitarlo al progetto corrente. Vedi [Configura la posizione dell'hook](#configure-hook-location) per tutti gli ambiti disponibili.
  </Step>

  <Step title="Testa l'hook">
    Premi `Esc` per tornare alla CLI. Chiedi a Claude di fare qualcosa che richieda autorizzazione, quindi allontanati dal terminale. Dovresti ricevere una notifica desktop.
  </Step>
</Steps>

## Cosa puoi automatizzare

Gli hooks ti permettono di eseguire codice in punti chiave del ciclo di vita di Claude Code: formattare file dopo le modifiche, bloccare comandi prima che si eseguano, inviare notifiche quando Claude ha bisogno di input, iniettare contesto all'inizio della sessione, e altro ancora. Per l'elenco completo degli eventi hook, vedi il [riferimento Hooks](/it/hooks#hook-lifecycle).

Ogni esempio include un blocco di configurazione pronto all'uso che aggiungi a un [file di impostazioni](#configure-hook-location). I modelli più comuni:

* [Ricevi una notifica quando Claude ha bisogno di input](#get-notified-when-claude-needs-input)
* [Formatta automaticamente il codice dopo le modifiche](#auto-format-code-after-edits)
* [Blocca le modifiche ai file protetti](#block-edits-to-protected-files)
* [Reinietta il contesto dopo la compattazione](#re-inject-context-after-compaction)
* [Controlla le modifiche di configurazione](#audit-configuration-changes)

### Ricevi una notifica quando Claude ha bisogno di input

Ricevi una notifica desktop ogni volta che Claude finisce di lavorare e ha bisogno del tuo input, in modo da poter passare ad altri compiti senza controllare il terminale.

Questo hook utilizza l'evento `Notification`, che si attiva quando Claude sta aspettando input o autorizzazione. Ogni scheda di seguito utilizza il comando di notifica nativo della piattaforma. Aggiungi questo a `~/.claude/settings.json`, o utilizza la [procedura interattiva](#set-up-your-first-hook) sopra per configurarlo con `/hooks`:

<Tabs>
  <Tab title="macOS">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Linux">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Windows (PowerShell)">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

### Formatta automaticamente il codice dopo le modifiche

Esegui automaticamente [Prettier](https://prettier.io/) su ogni file che Claude modifica, in modo che la formattazione rimanga coerente senza intervento manuale.

Questo hook utilizza l'evento `PostToolUse` con un matcher `Edit|Write`, quindi si esegue solo dopo gli strumenti di modifica dei file. Il comando estrae il percorso del file modificato con [`jq`](https://jqlang.github.io/jq/) e lo passa a Prettier. Aggiungi questo a `.claude/settings.json` nella radice del tuo progetto:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

<Note>
  Gli esempi Bash in questa pagina utilizzano `jq` per l'analisi JSON. Installalo con `brew install jq` (macOS), `apt-get install jq` (Debian/Ubuntu), o vedi [download di `jq`](https://jqlang.github.io/jq/download/).
</Note>

### Blocca le modifiche ai file protetti

Impedisci a Claude di modificare file sensibili come `.env`, `package-lock.json`, o qualsiasi cosa in `.git/`. Claude riceve un feedback che spiega perché la modifica è stata bloccata, in modo da poter adattare il suo approccio.

Questo esempio utilizza un file di script separato che l'hook chiama. Lo script controlla il percorso del file di destinazione rispetto a un elenco di modelli protetti ed esce con il codice 2 per bloccare la modifica.

<Steps>
  <Step title="Crea lo script dell'hook">
    Salva questo in `.claude/hooks/protect-files.sh`:

    ```bash  theme={null}
    #!/bin/bash
    # protect-files.sh

    INPUT=$(cat)
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

    PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

    for pattern in "${PROTECTED_PATTERNS[@]}"; do
      if [[ "$FILE_PATH" == *"$pattern"* ]]; then
        echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
        exit 2
      fi
    done

    exit 0
    ```
  </Step>

  <Step title="Rendi lo script eseguibile (macOS/Linux)">
    Gli script degli hook devono essere eseguibili affinché Claude Code li esegua:

    ```bash  theme={null}
    chmod +x .claude/hooks/protect-files.sh
    ```
  </Step>

  <Step title="Registra l'hook">
    Aggiungi un hook `PreToolUse` a `.claude/settings.json` che esegue lo script prima di qualsiasi chiamata dello strumento `Edit` o `Write`:

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Step>
</Steps>

### Reinietta il contesto dopo la compattazione

Quando la finestra di contesto di Claude si riempie, la compattazione riassume la conversazione per liberare spazio. Questo può perdere dettagli importanti. Utilizza un hook `SessionStart` con un matcher `compact` per reiniettare il contesto critico dopo ogni compattazione.

Qualsiasi testo che il tuo comando scrive su stdout viene aggiunto al contesto di Claude. Questo esempio ricorda a Claude le convenzioni del progetto e il lavoro recente. Aggiungi questo a `.claude/settings.json` nella radice del tuo progetto:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
          }
        ]
      }
    ]
  }
}
```

Puoi sostituire l'`echo` con qualsiasi comando che produce output dinamico, come `git log --oneline -5` per mostrare i commit recenti. Per iniettare contesto all'inizio di ogni sessione, considera invece di utilizzare [CLAUDE.md](/it/memory). Per le variabili di ambiente, vedi [`CLAUDE_ENV_FILE`](/it/hooks#persist-environment-variables) nel riferimento.

### Controlla le modifiche di configurazione

Traccia quando i file di impostazioni o skills cambiano durante una sessione. L'evento `ConfigChange` si attiva quando un processo esterno o un editor modifica un file di configurazione, in modo da poter registrare le modifiche per la conformità o bloccare le modifiche non autorizzate.

Questo esempio aggiunge ogni modifica a un registro di controllo. Aggiungi questo a `~/.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> ~/claude-config-audit.log"
          }
        ]
      }
    ]
  }
}
```

Il matcher filtra per tipo di configurazione: `user_settings`, `project_settings`, `local_settings`, `policy_settings`, o `skills`. Per bloccare una modifica dall'avere effetto, esci con il codice 2 o restituisci `{"decision": "block"}`. Vedi il [riferimento ConfigChange](/it/hooks#configchange) per lo schema di input completo.

## Come funzionano gli hooks

Gli eventi degli hooks si attivano in punti specifici del ciclo di vita di Claude Code. Quando un evento si attiva, tutti gli hooks corrispondenti si eseguono in parallelo, e i comandi degli hooks identici vengono automaticamente deduplicati. La tabella di seguito mostra ogni evento e quando si attiva:

| Event                | When it fires                                                                                                                                  |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                               |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                           |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                      |
| `PermissionRequest`  | When a permission dialog appears                                                                                                               |
| `PostToolUse`        | After a tool call succeeds                                                                                                                     |
| `PostToolUseFailure` | After a tool call fails                                                                                                                        |
| `Notification`       | When Claude Code sends a notification                                                                                                          |
| `SubagentStart`      | When a subagent is spawned                                                                                                                     |
| `SubagentStop`       | When a subagent finishes                                                                                                                       |
| `Stop`               | When Claude finishes responding                                                                                                                |
| `StopFailure`        | When the turn ends due to an API error. Output and exit code are ignored                                                                       |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                             |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                       |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session |
| `ConfigChange`       | When a configuration file changes during a session                                                                                             |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                    |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                           |
| `PreCompact`         | Before context compaction                                                                                                                      |
| `PostCompact`        | After context compaction completes                                                                                                             |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                      |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                    |
| `SessionEnd`         | When a session terminates                                                                                                                      |

Ogni hook ha un `type` che determina come si esegue. La maggior parte degli hooks utilizza `"type": "command"`, che esegue un comando shell. Sono disponibili altri tre tipi:

* `"type": "http"`: POST dei dati dell'evento a un URL. Vedi [HTTP hooks](#http-hooks).
* `"type": "prompt"`: valutazione LLM a turno singolo. Vedi [Prompt-based hooks](#prompt-based-hooks).
* `"type": "agent"`: verifica multi-turno con accesso agli strumenti. Vedi [Agent-based hooks](#agent-based-hooks).

### Leggi l'input e restituisci l'output

Gli hooks comunicano con Claude Code attraverso stdin, stdout, stderr e codici di uscita. Quando un evento si attiva, Claude Code passa i dati specifici dell'evento come JSON allo stdin del tuo script. Il tuo script legge quei dati, fa il suo lavoro, e dice a Claude Code cosa fare dopo tramite il codice di uscita.

#### Input dell'hook

Ogni evento include campi comuni come `session_id` e `cwd`, ma ogni tipo di evento aggiunge dati diversi. Ad esempio, quando Claude esegue un comando Bash, un hook `PreToolUse` riceve qualcosa di simile a questo su stdin:

```json  theme={null}
{
  "session_id": "abc123",          // unique ID for this session
  "cwd": "/Users/sarah/myproject", // working directory when the event fired
  "hook_event_name": "PreToolUse", // which event triggered this hook
  "tool_name": "Bash",             // the tool Claude is about to use
  "tool_input": {                  // the arguments Claude passed to the tool
    "command": "npm test"          // for Bash, this is the shell command
  }
}
```

Il tuo script può analizzare quel JSON e agire su qualsiasi di quei campi. Gli hooks `UserPromptSubmit` ottengono il testo `prompt` invece, gli hook `SessionStart` ottengono la `source` (startup, resume, clear, compact), e così via. Vedi [Campi di input comuni](/it/hooks#common-input-fields) nel riferimento per i campi condivisi, e la sezione di ogni evento per gli schemi specifici dell'evento.

#### Output dell'hook

Il tuo script dice a Claude Code cosa fare dopo scrivendo su stdout o stderr e uscendo con un codice specifico. Ad esempio, un hook `PreToolUse` che vuole bloccare un comando:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q "drop table"; then
  echo "Blocked: dropping tables is not allowed" >&2  # stderr becomes Claude's feedback
  exit 2 # exit 2 = block the action
fi

exit 0  # exit 0 = let it proceed
```

Il codice di uscita determina cosa succede dopo:

* **Exit 0**: l'azione procede. Per gli hook `UserPromptSubmit` e `SessionStart`, qualsiasi cosa tu scriva su stdout viene aggiunta al contesto di Claude.
* **Exit 2**: l'azione è bloccata. Scrivi un motivo su stderr, e Claude lo riceve come feedback in modo da poter adattarsi.
* **Qualsiasi altro codice di uscita**: l'azione procede. Stderr viene registrato ma non mostrato a Claude. Attiva la modalità verbose con `Ctrl+O` per vedere questi messaggi nella trascrizione.

#### Output JSON strutturato

I codici di uscita ti danno due opzioni: consentire o bloccare. Per un controllo maggiore, esci con 0 e stampa un oggetto JSON su stdout invece.

<Note>
  Utilizza exit 2 per bloccare con un messaggio stderr, o exit 0 con JSON per un controllo strutturato. Non mischiarli: Claude Code ignora JSON quando esci con 2.
</Note>

Ad esempio, un hook `PreToolUse` può negare una chiamata di strumento e dire a Claude perché, o escalare al utente per l'approvazione:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep for better performance"
  }
}
```

Claude Code legge `permissionDecision` e annulla la chiamata dello strumento, quindi alimenta `permissionDecisionReason` di nuovo a Claude come feedback. Queste tre opzioni sono specifiche per `PreToolUse`:

* `"allow"`: procedi senza mostrare un prompt di autorizzazione
* `"deny"`: annulla la chiamata dello strumento e invia il motivo a Claude
* `"ask"`: mostra il prompt di autorizzazione all'utente come al solito

Altri eventi utilizzano diversi modelli di decisione. Ad esempio, gli hook `PostToolUse` e `Stop` utilizzano un campo `decision: "block"` di livello superiore, mentre `PermissionRequest` utilizza `hookSpecificOutput.decision.behavior`. Vedi la [tabella di riepilogo](/it/hooks#decision-control) nel riferimento per una suddivisione completa per evento.

Per gli hook `UserPromptSubmit`, utilizza `additionalContext` invece per iniettare testo nel contesto di Claude. Gli hooks basati su prompt (`type: "prompt"`) gestiscono l'output diversamente: vedi [Prompt-based hooks](#prompt-based-hooks).

### Filtra gli hooks con i matcher

Senza un matcher, un hook si attiva su ogni occorrenza del suo evento. I matcher ti permettono di restringere questo. Ad esempio, se vuoi eseguire un formattatore solo dopo le modifiche ai file (non dopo ogni chiamata di strumento), aggiungi un matcher al tuo hook `PostToolUse`:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "prettier --write ..." }
        ]
      }
    ]
  }
}
```

Il matcher `"Edit|Write"` è un modello regex che corrisponde al nome dello strumento. L'hook si attiva solo quando Claude utilizza lo strumento `Edit` o `Write`, non quando utilizza `Bash`, `Read`, o qualsiasi altro strumento.

Ogni tipo di evento corrisponde a un campo specifico. I matcher supportano stringhe esatte e modelli regex:

| Evento                                                                                          | Cosa filtra il matcher            | Valori matcher di esempio                                                          |
| :---------------------------------------------------------------------------------------------- | :-------------------------------- | :--------------------------------------------------------------------------------- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`                          | nome dello strumento              | `Bash`, `Edit\|Write`, `mcp__.*`                                                   |
| `SessionStart`                                                                                  | come è iniziata la sessione       | `startup`, `resume`, `clear`, `compact`                                            |
| `SessionEnd`                                                                                    | perché è terminata la sessione    | `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`     |
| `Notification`                                                                                  | tipo di notifica                  | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`           |
| `SubagentStart`                                                                                 | tipo di agente                    | `Bash`, `Explore`, `Plan`, o nomi di agenti personalizzati                         |
| `PreCompact`                                                                                    | cosa ha attivato la compattazione | `manual`, `auto`                                                                   |
| `SubagentStop`                                                                                  | tipo di agente                    | stessi valori di `SubagentStart`                                                   |
| `ConfigChange`                                                                                  | fonte di configurazione           | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | nessun supporto matcher           | si attiva sempre su ogni occorrenza                                                |

Alcuni altri esempi che mostrano i matcher su diversi tipi di evento:

<Tabs>
  <Tab title="Registra ogni comando Bash">
    Corrisponde solo alle chiamate dello strumento `Bash` e registra ogni comando in un file. L'evento `PostToolUse` si attiva dopo che il comando è completato, quindi `tool_input.command` contiene quello che è stato eseguito. L'hook riceve i dati dell'evento come JSON su stdin, e `jq -r '.tool_input.command'` estrae solo la stringa del comando, che `>>` aggiunge al file di registro:

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Corrisponde agli strumenti MCP">
    Gli strumenti MCP utilizzano una convenzione di denominazione diversa rispetto agli strumenti integrati: `mcp__<server>__<tool>`, dove `<server>` è il nome del server MCP e `<tool>` è lo strumento che fornisce. Ad esempio, `mcp__github__search_repositories` o `mcp__filesystem__read_file`. Utilizza un matcher regex per indirizzare tutti gli strumenti da un server specifico, o corrispondere tra i server con un modello come `mcp__.*__write.*`. Vedi [Corrisponde agli strumenti MCP](/it/hooks#match-mcp-tools) nel riferimento per l'elenco completo degli esempi.

    Il comando di seguito estrae il nome dello strumento dall'input JSON dell'hook con `jq` e lo scrive su stderr, dove appare in modalità verbose (`Ctrl+O`):

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "mcp__github__.*",
            "hooks": [
              {
                "type": "command",
                "command": "echo \"GitHub tool called: $(jq -r '.tool_name')\" >&2"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Pulisci alla fine della sessione">
    L'evento `SessionEnd` supporta i matcher sul motivo per cui la sessione è terminata. Questo hook si attiva solo su `clear` (quando esegui `/clear`), non su uscite normali:

    ```json  theme={null}
    {
      "hooks": {
        "SessionEnd": [
          {
            "matcher": "clear",
            "hooks": [
              {
                "type": "command",
                "command": "rm -f /tmp/claude-scratch-*.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

Per la sintassi completa del matcher, vedi il [riferimento Hooks](/it/hooks#configuration).

### Configura la posizione dell'hook

Dove aggiungi un hook determina il suo ambito:

| Posizione                                                  | Ambito                              | Condivisibile                        |
| :--------------------------------------------------------- | :---------------------------------- | :----------------------------------- |
| `~/.claude/settings.json`                                  | Tutti i tuoi progetti               | No, locale alla tua macchina         |
| `.claude/settings.json`                                    | Singolo progetto                    | Sì, può essere committato nel repo   |
| `.claude/settings.local.json`                              | Singolo progetto                    | No, gitignored                       |
| Impostazioni di policy gestite                             | Organizzazione intera               | Sì, controllato dall'amministratore  |
| [Plugin](/it/plugins) `hooks/hooks.json`                   | Quando il plugin è abilitato        | Sì, raggruppato con il plugin        |
| [Skill](/it/skills) o [agente](/it/sub-agents) frontmatter | Mentre la skill o l'agente è attivo | Sì, definito nel file del componente |

Puoi anche utilizzare il menu [`/hooks`](/it/hooks#the-hooks-menu) in Claude Code per aggiungere, eliminare e visualizzare gli hooks in modo interattivo. Per disabilitare tutti gli hooks contemporaneamente, utilizza l'interruttore in fondo al menu `/hooks` o imposta `"disableAllHooks": true` nel tuo file di impostazioni.

Gli hooks aggiunti tramite il menu `/hooks` hanno effetto immediato. Se modifichi i file di impostazioni direttamente mentre Claude Code è in esecuzione, le modifiche non avranno effetto fino a quando non le esamini nel menu `/hooks` o non riavvii la tua sessione.

## Prompt-based hooks

Per decisioni che richiedono giudizio piuttosto che regole deterministiche, utilizza gli hook `type: "prompt"`. Invece di eseguire un comando shell, Claude Code invia il tuo prompt e i dati di input dell'hook a un modello Claude (Haiku per impostazione predefinita) per prendere la decisione. Puoi specificare un modello diverso con il campo `model` se hai bisogno di più capacità.

L'unico lavoro del modello è restituire una decisione sì/no come JSON:

* `"ok": true`: l'azione procede
* `"ok": false`: l'azione è bloccata. Il `"reason"` del modello viene alimentato di nuovo a Claude in modo da poter adattarsi.

Questo esempio utilizza un hook `Stop` per chiedere al modello se tutti i compiti richiesti sono completi. Se il modello restituisce `"ok": false`, Claude continua a lavorare e utilizza il `reason` come sua prossima istruzione:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
          }
        ]
      }
    ]
  }
}
```

Per le opzioni di configurazione complete, vedi [Prompt-based hooks](/it/hooks#prompt-based-hooks) nel riferimento.

## Agent-based hooks

Quando la verifica richiede l'ispezione di file o l'esecuzione di comandi, utilizza gli hook `type: "agent"`. A differenza degli hook di prompt che effettuano una singola chiamata LLM, gli hook di agente generano un subagent che può leggere file, cercare codice e utilizzare altri strumenti per verificare le condizioni prima di restituire una decisione.

Gli hook di agente utilizzano lo stesso formato di risposta `"ok"` / `"reason"` degli hook di prompt, ma con un timeout predefinito più lungo di 60 secondi e fino a 50 turni di utilizzo dello strumento.

Questo esempio verifica che i test passino prima di consentire a Claude di fermarsi:

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

Utilizza gli hook di prompt quando i dati di input dell'hook da soli sono sufficienti per prendere una decisione. Utilizza gli hook di agente quando hai bisogno di verificare qualcosa rispetto allo stato effettivo della base di codice.

Per le opzioni di configurazione complete, vedi [Agent-based hooks](/it/hooks#agent-based-hooks) nel riferimento.

## HTTP hooks

Utilizza gli hook `type: "http"` per POST dei dati dell'evento a un endpoint HTTP invece di eseguire un comando shell. L'endpoint riceve lo stesso JSON che un hook di comando riceverebbe su stdin, e restituisce i risultati attraverso il corpo della risposta HTTP utilizzando lo stesso formato JSON.

Gli HTTP hooks sono utili quando vuoi che un server web, una funzione cloud o un servizio esterno gestisca la logica dell'hook: ad esempio, un servizio di controllo condiviso che registra gli eventi di utilizzo dello strumento in un team.

Questo esempio pubblica ogni utilizzo dello strumento a un servizio di registrazione locale:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/tool-use",
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

L'endpoint dovrebbe restituire un corpo di risposta JSON utilizzando lo stesso [formato di output](/it/hooks#json-output) degli hook di comando. Per bloccare una chiamata di strumento, restituisci una risposta 2xx con i campi `hookSpecificOutput` appropriati. I codici di stato HTTP da soli non possono bloccare le azioni.

I valori dell'intestazione supportano l'interpolazione delle variabili di ambiente utilizzando la sintassi `$VAR_NAME` o `${VAR_NAME}`. Solo le variabili elencate nell'array `allowedEnvVars` vengono risolte; tutti gli altri riferimenti `$VAR` rimangono vuoti.

<Note>
  Gli HTTP hooks devono essere configurati modificando direttamente il tuo JSON di impostazioni. Il menu interattivo `/hooks` supporta solo l'aggiunta di hook di comando.
</Note>

Per le opzioni di configurazione complete e la gestione delle risposte, vedi [HTTP hooks](/it/hooks#http-hook-fields) nel riferimento.

## Limitazioni e risoluzione dei problemi

### Limitazioni

* Gli hook di comando comunicano solo attraverso stdout, stderr e codici di uscita. Non possono attivare comandi o chiamate di strumenti direttamente. Gli HTTP hooks comunicano attraverso il corpo della risposta invece.
* Il timeout dell'hook è di 10 minuti per impostazione predefinita, configurabile per hook con il campo `timeout` (in secondi).
* Gli hook `PostToolUse` non possono annullare le azioni poiché lo strumento è già stato eseguito.
* Gli hook `PermissionRequest` non si attivano in [modalità non interattiva](/it/headless) (`-p`). Utilizza gli hook `PreToolUse` per le decisioni di autorizzazione automatizzate.
* Gli hook `Stop` si attivano ogni volta che Claude finisce di rispondere, non solo al completamento dell'attività. Non si attivano su interruzioni dell'utente.

### Hook non si attiva

L'hook è configurato ma non si esegue mai.

* Esegui `/hooks` e conferma che l'hook appare sotto l'evento corretto
* Controlla che il modello del matcher corrisponda al nome dello strumento esattamente (i matcher sono sensibili alle maiuscole)
* Verifica che stai attivando il tipo di evento corretto (ad esempio, `PreToolUse` si attiva prima dell'esecuzione dello strumento, `PostToolUse` si attiva dopo)
* Se utilizzi gli hook `PermissionRequest` in modalità non interattiva (`-p`), passa agli hook `PreToolUse` invece

### Errore dell'hook nell'output

Vedi un messaggio come "PreToolUse hook error: ..." nella trascrizione.

* Il tuo script è uscito con un codice diverso da zero inaspettatamente. Testalo manualmente inviando JSON di esempio:
  ```bash  theme={null}
  echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
  echo $?  # Check the exit code
  ```
* Se vedi "command not found", utilizza percorsi assoluti o `$CLAUDE_PROJECT_DIR` per fare riferimento agli script
* Se vedi "jq: command not found", installa `jq` o utilizza Python/Node.js per l'analisi JSON
* Se lo script non si esegue affatto, rendilo eseguibile: `chmod +x ./my-hook.sh`

### `/hooks` non mostra hook configurati

Hai modificato un file di impostazioni ma gli hook non appaiono nel menu.

* Riavvia la tua sessione o apri `/hooks` per ricaricare. Gli hook aggiunti tramite il menu `/hooks` hanno effetto immediato, ma le modifiche manuali ai file richiedono un ricaricamento.
* Verifica che il tuo JSON sia valido (le virgole finali e i commenti non sono consentiti)
* Conferma che il file di impostazioni è nella posizione corretta: `.claude/settings.json` per gli hook del progetto, `~/.claude/settings.json` per gli hook globali

### L'hook Stop si esegue per sempre

Claude continua a lavorare in un ciclo infinito invece di fermarsi.

Il tuo script dell'hook Stop deve controllare se ha già attivato una continuazione. Analizza il campo `stop_hook_active` dall'input JSON e esci presto se è `true`:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # Allow Claude to stop
fi
# ... rest of your hook logic
```

### Convalida JSON non riuscita

Claude Code mostra un errore di analisi JSON anche se il tuo script dell'hook produce JSON valido.

Quando Claude Code esegue un hook, genera una shell che fornisce il tuo profilo (`~/.zshrc` o `~/.bashrc`). Se il tuo profilo contiene istruzioni `echo` incondizionate, quell'output viene anteposto al JSON del tuo hook:

```text  theme={null}
Shell ready on arm64
{"decision": "block", "reason": "Not allowed"}
```

Claude Code tenta di analizzare questo come JSON e fallisce. Per risolvere questo, avvolgi le istruzioni echo nel tuo profilo shell in modo che si eseguano solo in shell interattive:

```bash  theme={null}
# In ~/.zshrc or ~/.bashrc
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

La variabile `$-` contiene i flag della shell, e `i` significa interattivo. Gli hook si eseguono in shell non interattive, quindi l'echo viene saltato.

### Tecniche di debug

Attiva la modalità verbose con `Ctrl+O` per vedere l'output dell'hook nella trascrizione, o esegui `claude --debug` per i dettagli di esecuzione completi incluso quali hook hanno corrisposto e i loro codici di uscita.

## Scopri di più

* [Riferimento Hooks](/it/hooks): schemi di eventi completi, formato di output JSON, hook asincroni e hook di strumenti MCP
* [Considerazioni sulla sicurezza](/it/hooks#security-considerations): esamina prima di distribuire gli hook in ambienti condivisi o di produzione
* [Esempio di validatore di comandi Bash](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py): implementazione di riferimento completa
