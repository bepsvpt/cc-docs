> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Automatizzare i flussi di lavoro con hooks

> Esegui comandi shell automaticamente quando Claude Code modifica file, completa attività o ha bisogno di input. Formatta il codice, invia notifiche, convalida comandi e applica le regole del progetto.

Gli hooks sono comandi shell definiti dall'utente che si eseguono in punti specifici del ciclo di vita di Claude Code. Forniscono un controllo deterministico sul comportamento di Claude Code, garantendo che determinate azioni avvengano sempre piuttosto che affidarsi al modello linguistico per scegliere di eseguirle. Utilizzate gli hooks per applicare le regole del progetto, automatizzare attività ripetitive e integrare Claude Code con i vostri strumenti esistenti.

Per decisioni che richiedono giudizio piuttosto che regole deterministiche, potete anche utilizzare [hooks basati su prompt](#prompt-based-hooks) o [hooks basati su agenti](#agent-based-hooks) che utilizzano un modello Claude per valutare le condizioni.

Per altri modi di estendere Claude Code, consultate [skills](/it/skills) per fornire a Claude istruzioni aggiuntive e comandi eseguibili, [subagents](/it/sub-agents) per eseguire attività in contesti isolati, e [plugins](/it/plugins) per pacchettizzare estensioni da condividere tra i progetti.

<Tip>
  Questa guida copre i casi d'uso comuni e come iniziare. Per schemi di eventi completi, formati di input/output JSON e funzionalità avanzate come hooks asincroni e hooks di strumenti MCP, consultate il [riferimento Hooks](/it/hooks).
</Tip>

## Configurare il vostro primo hook

Per creare un hook, aggiungete un blocco `hooks` a un [file di impostazioni](#configure-hook-location). Questa procedura crea un hook di notifica desktop, in modo da ricevere un avviso ogni volta che Claude sta aspettando il vostro input invece di guardare il terminale.

<Steps>
  <Step title="Aggiungere l'hook alle vostre impostazioni">
    Aprite `~/.claude/settings.json` e aggiungete un hook `Notification`. L'esempio sottostante utilizza `osascript` per macOS; consultate [Ricevere una notifica quando Claude ha bisogno di input](#get-notified-when-claude-needs-input) per i comandi Linux e Windows.

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

    Se il vostro file di impostazioni ha già una chiave `hooks`, unite la voce `Notification` ad essa piuttosto che sostituire l'intero oggetto. Potete anche chiedere a Claude di scrivere l'hook per voi descrivendo quello che volete nella CLI.
  </Step>

  <Step title="Verificare la configurazione">
    Digitate `/hooks` per aprire il browser degli hooks. Vedrete un elenco di tutti gli eventi hook disponibili, con un conteggio accanto a ogni evento che ha hook configurati. Selezionate `Notification` per confermare che il vostro nuovo hook appare nell'elenco. Selezionando l'hook vengono mostrati i suoi dettagli: l'evento, il matcher, il tipo, il file di origine e il comando.
  </Step>

  <Step title="Testare l'hook">
    Premete `Esc` per tornare alla CLI. Chiedete a Claude di fare qualcosa che richieda autorizzazione, quindi passate a un'altra finestra dal terminale. Dovreste ricevere una notifica desktop.
  </Step>
</Steps>

<Tip>
  Il menu `/hooks` è di sola lettura. Per aggiungere, modificare o rimuovere hooks, modificate il vostro JSON di impostazioni direttamente o chiedete a Claude di fare il cambiamento.
</Tip>

## Cosa potete automatizzare

Gli hooks vi permettono di eseguire codice in punti chiave del ciclo di vita di Claude Code: formattare file dopo le modifiche, bloccare comandi prima che si eseguano, inviare notifiche quando Claude ha bisogno di input, iniettare contesto all'inizio della sessione, e altro ancora. Per l'elenco completo degli eventi hook, consultate il [riferimento Hooks](/it/hooks#hook-lifecycle).

Ogni esempio include un blocco di configurazione pronto all'uso che aggiungete a un [file di impostazioni](#configure-hook-location). I modelli più comuni:

* [Ricevere una notifica quando Claude ha bisogno di input](#get-notified-when-claude-needs-input)
* [Formattare automaticamente il codice dopo le modifiche](#auto-format-code-after-edits)
* [Bloccare le modifiche ai file protetti](#block-edits-to-protected-files)
* [Reiniettare il contesto dopo la compattazione](#re-inject-context-after-compaction)
* [Controllare le modifiche di configurazione](#audit-configuration-changes)
* [Approvare automaticamente specifici prompt di autorizzazione](#auto-approve-specific-permission-prompts)

### Ricevere una notifica quando Claude ha bisogno di input

Ricevete una notifica desktop ogni volta che Claude finisce di lavorare e ha bisogno del vostro input, in modo da poter passare ad altri compiti senza controllare il terminale.

Questo hook utilizza l'evento `Notification`, che si attiva quando Claude sta aspettando input o autorizzazione. Ogni scheda sottostante utilizza il comando di notifica nativo della piattaforma. Aggiungete questo a `~/.claude/settings.json`:

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

### Formattare automaticamente il codice dopo le modifiche

Eseguite automaticamente [Prettier](https://prettier.io/) su ogni file che Claude modifica, in modo che la formattazione rimanga coerente senza intervento manuale.

Questo hook utilizza l'evento `PostToolUse` con un matcher `Edit|Write`, quindi si esegue solo dopo gli strumenti di modifica dei file. Il comando estrae il percorso del file modificato con [`jq`](https://jqlang.github.io/jq/) e lo passa a Prettier. Aggiungete questo a `.claude/settings.json` nella radice del vostro progetto:

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
  Gli esempi Bash in questa pagina utilizzano `jq` per l'analisi JSON. Installatelo con `brew install jq` (macOS), `apt-get install jq` (Debian/Ubuntu), o consultate i [download di `jq`](https://jqlang.github.io/jq/download/).
</Note>

### Bloccare le modifiche ai file protetti

Impedite a Claude di modificare file sensibili come `.env`, `package-lock.json`, o qualsiasi cosa in `.git/`. Claude riceve un feedback che spiega perché la modifica è stata bloccata, in modo da poter adattare il suo approccio.

Questo esempio utilizza un file di script separato che l'hook chiama. Lo script controlla il percorso del file di destinazione rispetto a un elenco di modelli protetti ed esce con il codice 2 per bloccare la modifica.

<Steps>
  <Step title="Creare lo script dell'hook">
    Salvate questo in `.claude/hooks/protect-files.sh`:

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

  <Step title="Rendere lo script eseguibile (macOS/Linux)">
    Gli script degli hook devono essere eseguibili affinché Claude Code li esegua:

    ```bash  theme={null}
    chmod +x .claude/hooks/protect-files.sh
    ```
  </Step>

  <Step title="Registrare l'hook">
    Aggiungete un hook `PreToolUse` a `.claude/settings.json` che esegue lo script prima di qualsiasi chiamata dello strumento `Edit` o `Write`:

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

### Reiniettare il contesto dopo la compattazione

Quando la finestra di contesto di Claude si riempie, la compattazione riassume la conversazione per liberare spazio. Questo può perdere dettagli importanti. Utilizzate un hook `SessionStart` con un matcher `compact` per reiniettare il contesto critico dopo ogni compattazione.

Qualsiasi testo che il vostro comando scrive su stdout viene aggiunto al contesto di Claude. Questo esempio ricorda a Claude le convenzioni del progetto e il lavoro recente. Aggiungete questo a `.claude/settings.json` nella radice del vostro progetto:

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

Potete sostituire l'`echo` con qualsiasi comando che produce output dinamico, come `git log --oneline -5` per mostrare i commit recenti. Per iniettare contesto all'inizio di ogni sessione, considerate di utilizzare [CLAUDE.md](/it/memory) invece. Per le variabili di ambiente, consultate [`CLAUDE_ENV_FILE`](/it/hooks#persist-environment-variables) nel riferimento.

### Controllare le modifiche di configurazione

Tracciate quando i file di impostazioni o skills cambiano durante una sessione. L'evento `ConfigChange` si attiva quando un processo esterno o un editor modifica un file di configurazione, in modo da poter registrare le modifiche per la conformità o bloccare le modifiche non autorizzate.

Questo esempio aggiunge ogni modifica a un registro di controllo. Aggiungete questo a `~/.claude/settings.json`:

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

Il matcher filtra per tipo di configurazione: `user_settings`, `project_settings`, `local_settings`, `policy_settings`, o `skills`. Per bloccare una modifica dall'avere effetto, uscite con il codice 2 o restituite `{"decision": "block"}`. Consultate il [riferimento ConfigChange](/it/hooks#configchange) per lo schema di input completo.

### Approvare automaticamente specifici prompt di autorizzazione

Saltate la finestra di dialogo di approvazione per le chiamate di strumenti che consentite sempre. Questo esempio approva automaticamente `ExitPlanMode`, lo strumento che Claude chiama quando finisce di presentare un piano e chiede di procedere, in modo da non essere richiesto ogni volta che un piano è pronto.

A differenza degli esempi di codice di uscita sopra, l'approvazione automatica richiede che il vostro hook scriva una decisione JSON su stdout. Un hook `PermissionRequest` si attiva quando Claude Code sta per mostrare una finestra di dialogo di autorizzazione, e restituire `"behavior": "allow"` la risponde per vostro conto.

Il matcher limita l'hook a `ExitPlanMode` solo, in modo che nessun altro prompt sia interessato. Aggiungete questo a `~/.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"PermissionRequest\", \"decision\": {\"behavior\": \"allow\"}}}'"
          }
        ]
      }
    ]
  }
}
```

Quando l'hook approva, Claude Code esce dalla modalità piano e ripristina qualsiasi modalità di autorizzazione fosse attiva prima di entrare in modalità piano. La trascrizione mostra "Allowed by PermissionRequest hook" dove la finestra di dialogo sarebbe apparsa. Il percorso dell'hook mantiene sempre la conversazione corrente: non può cancellare il contesto e avviare una sessione di implementazione fresca come la finestra di dialogo può.

Per impostare una modalità di autorizzazione specifica invece, l'output del vostro hook può includere un array `updatedPermissions` con una voce `setMode`. Il valore `mode` è qualsiasi modalità di autorizzazione come `default`, `acceptEdits`, o `bypassPermissions`, e `destination: "session"` la applica solo per la sessione corrente.

Per passare la sessione a `acceptEdits`, il vostro hook scrive questo JSON su stdout:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedPermissions": [
        { "type": "setMode", "mode": "acceptEdits", "destination": "session" }
      ]
    }
  }
}
```

Mantenete il matcher il più ristretto possibile. Corrispondere a `.*` o lasciare il matcher vuoto approverebbe automaticamente ogni prompt di autorizzazione, incluse le scritture di file e i comandi shell. Consultate il [riferimento PermissionRequest](/it/hooks#permissionrequest-decision-control) per l'insieme completo di campi di decisione.

## Come funzionano gli hooks

Gli eventi hook si attivano in punti specifici del ciclo di vita di Claude Code. Quando un evento si attiva, tutti gli hooks corrispondenti si eseguono in parallelo, e i comandi hook identici vengono automaticamente deduplicati. La tabella sottostante mostra ogni evento e quando si attiva:

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

* `"type": "http"`: POST dei dati dell'evento a un URL. Consultate [HTTP hooks](#http-hooks).
* `"type": "prompt"`: valutazione LLM a turno singolo. Consultate [Hooks basati su prompt](#prompt-based-hooks).
* `"type": "agent"`: verifica multi-turno con accesso agli strumenti. Consultate [Hooks basati su agenti](#agent-based-hooks).

### Leggere l'input e restituire l'output

Gli hooks comunicano con Claude Code attraverso stdin, stdout, stderr e codici di uscita. Quando un evento si attiva, Claude Code passa i dati specifici dell'evento come JSON allo stdin del vostro script. Il vostro script legge quei dati, fa il suo lavoro, e dice a Claude Code cosa fare dopo tramite il codice di uscita.

#### Input dell'hook

Ogni evento include campi comuni come `session_id` e `cwd`, ma ogni tipo di evento aggiunge dati diversi. Ad esempio, quando Claude esegue un comando Bash, un hook `PreToolUse` riceve qualcosa di simile su stdin:

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

Il vostro script può analizzare quel JSON e agire su qualsiasi di quei campi. Gli hooks `UserPromptSubmit` ricevono il testo `prompt` invece, gli hook `SessionStart` ricevono la `source` (startup, resume, clear, compact), e così via. Consultate [Campi di input comuni](/it/hooks#common-input-fields) nel riferimento per i campi condivisi, e la sezione di ogni evento per gli schemi specifici dell'evento.

#### Output dell'hook

Il vostro script dice a Claude Code cosa fare dopo scrivendo su stdout o stderr e uscendo con un codice specifico. Ad esempio, un hook `PreToolUse` che vuole bloccare un comando:

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

* **Exit 0**: l'azione procede. Per gli hook `UserPromptSubmit` e `SessionStart`, qualsiasi cosa scriviate su stdout viene aggiunta al contesto di Claude.
* **Exit 2**: l'azione è bloccata. Scrivete un motivo su stderr, e Claude lo riceve come feedback in modo da poter adattarsi.
* **Qualsiasi altro codice di uscita**: l'azione procede. Stderr viene registrato ma non mostrato a Claude. Attivate la modalità verbose con `Ctrl+O` per vedere questi messaggi nella trascrizione.

#### Output JSON strutturato

I codici di uscita vi danno due opzioni: consentire o bloccare. Per un controllo maggiore, uscite con 0 e stampate un oggetto JSON su stdout invece.

<Note>
  Utilizzate exit 2 per bloccare con un messaggio stderr, o exit 0 con JSON per un controllo strutturato. Non mescolateli: Claude Code ignora JSON quando uscite con 2.
</Note>

Ad esempio, un hook `PreToolUse` può negare una chiamata di strumento e dire a Claude perché, o escalarlo all'utente per l'approvazione:

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

Altri eventi utilizzano modelli di decisione diversi. Ad esempio, gli hook `PostToolUse` e `Stop` utilizzano un campo `decision: "block"` di livello superiore, mentre `PermissionRequest` utilizza `hookSpecificOutput.decision.behavior`. Consultate la [tabella di riepilogo](/it/hooks#decision-control) nel riferimento per una suddivisione completa per evento.

Per gli hook `UserPromptSubmit`, utilizzate `additionalContext` invece per iniettare testo nel contesto di Claude. Gli hooks basati su prompt (`type: "prompt"`) gestiscono l'output diversamente: consultate [Hooks basati su prompt](#prompt-based-hooks).

### Filtrare gli hooks con i matcher

Senza un matcher, un hook si attiva su ogni occorrenza del suo evento. I matcher vi permettono di restringerlo. Ad esempio, se volete eseguire un formattatore solo dopo le modifiche ai file (non dopo ogni chiamata di strumento), aggiungete un matcher al vostro hook `PostToolUse`:

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
  <Tab title="Registrare ogni comando Bash">
    Corrispondere solo alle chiamate dello strumento `Bash` e registrare ogni comando in un file. L'evento `PostToolUse` si attiva dopo che il comando è completato, quindi `tool_input.command` contiene quello che è stato eseguito. L'hook riceve i dati dell'evento come JSON su stdin, e `jq -r '.tool_input.command'` estrae solo la stringa del comando, che `>>` aggiunge al file di log:

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

  <Tab title="Corrispondere agli strumenti MCP">
    Gli strumenti MCP utilizzano una convenzione di denominazione diversa rispetto agli strumenti integrati: `mcp__<server>__<tool>`, dove `<server>` è il nome del server MCP e `<tool>` è lo strumento che fornisce. Ad esempio, `mcp__github__search_repositories` o `mcp__filesystem__read_file`. Utilizzate un matcher regex per indirizzare tutti gli strumenti da un server specifico, o corrispondere tra i server con un modello come `mcp__.*__write.*`. Consultate [Corrispondere agli strumenti MCP](/it/hooks#match-mcp-tools) nel riferimento per l'elenco completo degli esempi.

    Il comando sottostante estrae il nome dello strumento dall'input JSON dell'hook con `jq` e lo scrive su stderr, dove appare in modalità verbose (`Ctrl+O`):

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

  <Tab title="Pulire alla fine della sessione">
    L'evento `SessionEnd` supporta i matcher sul motivo per cui la sessione è terminata. Questo hook si attiva solo su `clear` (quando eseguite `/clear`), non su uscite normali:

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

Per la sintassi completa del matcher, consultate il [riferimento Hooks](/it/hooks#configuration).

### Configurare la posizione dell'hook

Dove aggiungete un hook determina il suo ambito:

| Posizione                                                  | Ambito                              | Condivisibile                        |
| :--------------------------------------------------------- | :---------------------------------- | :----------------------------------- |
| `~/.claude/settings.json`                                  | Tutti i vostri progetti             | No, locale alla vostra macchina      |
| `.claude/settings.json`                                    | Singolo progetto                    | Sì, può essere committato nel repo   |
| `.claude/settings.local.json`                              | Singolo progetto                    | No, gitignored                       |
| Impostazioni di policy gestite                             | Organizzazione intera               | Sì, controllato dall'amministratore  |
| [Plugin](/it/plugins) `hooks/hooks.json`                   | Quando il plugin è abilitato        | Sì, raggruppato con il plugin        |
| [Skill](/it/skills) o [agente](/it/sub-agents) frontmatter | Mentre la skill o l'agente è attivo | Sì, definito nel file del componente |

Eseguite [`/hooks`](/it/hooks#the-hooks-menu) in Claude Code per sfogliare tutti gli hooks configurati raggruppati per evento. Per disabilitare tutti gli hooks contemporaneamente, impostate `"disableAllHooks": true` nel vostro file di impostazioni.

Se modificate i file di impostazioni direttamente mentre Claude Code è in esecuzione, il file watcher normalmente raccoglie i cambiamenti degli hook automaticamente.

## Hooks basati su prompt

Per decisioni che richiedono giudizio piuttosto che regole deterministiche, utilizzate gli hook `type: "prompt"`. Invece di eseguire un comando shell, Claude Code invia il vostro prompt e i dati di input dell'hook a un modello Claude (Haiku per impostazione predefinita) per prendere la decisione. Potete specificare un modello diverso con il campo `model` se avete bisogno di più capacità.

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

Per le opzioni di configurazione complete, consultate [Hooks basati su prompt](/it/hooks#prompt-based-hooks) nel riferimento.

## Hooks basati su agenti

Quando la verifica richiede l'ispezione di file o l'esecuzione di comandi, utilizzate gli hook `type: "agent"`. A differenza degli hook di prompt che effettuano una singola chiamata LLM, gli hook di agenti generano un subagent che può leggere file, cercare codice e utilizzare altri strumenti per verificare le condizioni prima di restituire una decisione.

Gli hook di agenti utilizzano lo stesso formato di risposta `"ok"` / `"reason"` degli hook di prompt, ma con un timeout predefinito più lungo di 60 secondi e fino a 50 turni di utilizzo dello strumento.

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

Utilizzate gli hook di prompt quando i dati di input dell'hook da soli sono sufficienti per prendere una decisione. Utilizzate gli hook di agenti quando avete bisogno di verificare qualcosa rispetto allo stato effettivo della base di codice.

Per le opzioni di configurazione complete, consultate [Hooks basati su agenti](/it/hooks#agent-based-hooks) nel riferimento.

## HTTP hooks

Utilizzate gli hook `type: "http"` per POST dei dati dell'evento a un endpoint HTTP invece di eseguire un comando shell. L'endpoint riceve lo stesso JSON che un hook di comando riceverebbe su stdin, e restituisce i risultati attraverso il corpo della risposta HTTP utilizzando lo stesso formato JSON.

Gli HTTP hooks sono utili quando volete che un server web, una funzione cloud o un servizio esterno gestisca la logica dell'hook: ad esempio, un servizio di controllo condiviso che registra gli eventi di utilizzo dello strumento in un team.

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

L'endpoint dovrebbe restituire un corpo di risposta JSON utilizzando lo stesso [formato di output](/it/hooks#json-output) degli hook di comando. Per bloccare una chiamata di strumento, restituite una risposta 2xx con i campi `hookSpecificOutput` appropriati. I codici di stato HTTP da soli non possono bloccare le azioni.

I valori dell'intestazione supportano l'interpolazione delle variabili di ambiente utilizzando la sintassi `$VAR_NAME` o `${VAR_NAME}`. Solo le variabili elencate nell'array `allowedEnvVars` vengono risolte; tutti gli altri riferimenti `$VAR` rimangono vuoti.

Per le opzioni di configurazione complete e la gestione delle risposte, consultate [HTTP hooks](/it/hooks#http-hook-fields) nel riferimento.

## Limitazioni e risoluzione dei problemi

### Limitazioni

* Gli hook di comando comunicano solo attraverso stdout, stderr e codici di uscita. Non possono attivare comandi o chiamate di strumenti direttamente. Gli HTTP hooks comunicano attraverso il corpo della risposta invece.
* Il timeout dell'hook è di 10 minuti per impostazione predefinita, configurabile per hook con il campo `timeout` (in secondi).
* Gli hook `PostToolUse` non possono annullare le azioni poiché lo strumento è già stato eseguito.
* Gli hook `PermissionRequest` non si attivano in [modalità non interattiva](/it/headless) (`-p`). Utilizzate gli hook `PreToolUse` per le decisioni di autorizzazione automatizzate.
* Gli hook `Stop` si attivano ogni volta che Claude finisce di rispondere, non solo al completamento dell'attività. Non si attivano su interruzioni dell'utente.

### Hook non si attiva

L'hook è configurato ma non si esegue mai.

* Eseguite `/hooks` e confermate che l'hook appare sotto l'evento corretto
* Controllate che il modello del matcher corrisponda esattamente al nome dello strumento (i matcher sono sensibili alle maiuscole)
* Verificate che state attivando il tipo di evento corretto (ad esempio, `PreToolUse` si attiva prima dell'esecuzione dello strumento, `PostToolUse` si attiva dopo)
* Se utilizzate gli hook `PermissionRequest` in modalità non interattiva (`-p`), passate a `PreToolUse` invece

### Errore dell'hook nell'output

Vedete un messaggio come "PreToolUse hook error: ..." nella trascrizione.

* Il vostro script è uscito con un codice diverso da zero inaspettatamente. Testatelo manualmente inviando JSON di esempio:
  ```bash  theme={null}
  echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
  echo $?  # Check the exit code
  ```
* Se vedete "command not found", utilizzate percorsi assoluti o `$CLAUDE_PROJECT_DIR` per fare riferimento agli script
* Se vedete "jq: command not found", installate `jq` o utilizzate Python/Node.js per l'analisi JSON
* Se lo script non si esegue affatto, rendetelo eseguibile: `chmod +x ./my-hook.sh`

### `/hooks` non mostra hook configurati

Avete modificato un file di impostazioni ma gli hooks non appaiono nel menu.

* Le modifiche ai file vengono normalmente raccolte automaticamente. Se non sono apparse dopo alcuni secondi, il file watcher potrebbe aver perso il cambiamento: riavviate la vostra sessione per forzare un ricaricamento.
* Verificate che il vostro JSON sia valido (le virgole finali e i commenti non sono consentiti)
* Confermate che il file di impostazioni è nella posizione corretta: `.claude/settings.json` per gli hook del progetto, `~/.claude/settings.json` per gli hook globali

### L'hook Stop si esegue per sempre

Claude continua a lavorare in un ciclo infinito invece di fermarsi.

Il vostro script di hook Stop deve controllare se ha già attivato una continuazione. Analizzate il campo `stop_hook_active` dall'input JSON e uscite presto se è `true`:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # Allow Claude to stop
fi
# ... rest of your hook logic
```

### Convalida JSON non riuscita

Claude Code mostra un errore di analisi JSON anche se il vostro script di hook produce JSON valido.

Quando Claude Code esegue un hook, genera una shell che fornisce il vostro profilo (`~/.zshrc` o `~/.bashrc`). Se il vostro profilo contiene istruzioni `echo` incondizionate, quell'output viene anteposto al vostro JSON dell'hook:

```text  theme={null}
Shell ready on arm64
{"decision": "block", "reason": "Not allowed"}
```

Claude Code tenta di analizzare questo come JSON e fallisce. Per risolvere questo, avvolgete le istruzioni echo nel vostro profilo shell in modo che si eseguano solo in shell interattive:

```bash  theme={null}
# In ~/.zshrc or ~/.bashrc
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

La variabile `$-` contiene i flag della shell, e `i` significa interattiva. Gli hooks si eseguono in shell non interattive, quindi l'echo viene saltato.

### Tecniche di debug

Attivate la modalità verbose con `Ctrl+O` per vedere l'output dell'hook nella trascrizione, o eseguite `claude --debug` per i dettagli di esecuzione completi incluso quali hook hanno corrisposto e i loro codici di uscita.

## Ulteriori informazioni

* [Riferimento Hooks](/it/hooks): schemi di eventi completi, formato di output JSON, hook asincroni e hook di strumenti MCP
* [Considerazioni sulla sicurezza](/it/hooks#security-considerations): esaminate prima di distribuire gli hooks in ambienti condivisi o di produzione
* [Esempio di validatore di comandi Bash](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py): implementazione di riferimento completa
