> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Personalizza la tua barra di stato

> Configura una barra di stato personalizzata per monitorare l'utilizzo della finestra di contesto, i costi e lo stato git in Claude Code

La barra di stato è una barra personalizzabile nella parte inferiore di Claude Code che esegue qualsiasi script di shell che configuri. Riceve dati di sessione JSON su stdin e visualizza tutto ciò che il tuo script stampa, fornendoti una visualizzazione persistente e immediata dell'utilizzo del contesto, dei costi, dello stato git o di qualsiasi altra cosa tu voglia tracciare.

Le barre di stato sono utili quando:

* Vuoi monitorare l'utilizzo della finestra di contesto mentre lavori
* Hai bisogno di tracciare i costi della sessione
* Lavori su più sessioni e hai bisogno di distinguerle
* Vuoi che il ramo git e lo stato siano sempre visibili

Ecco un esempio di una [barra di stato multi-riga](#display-multiple-lines) che visualizza le informazioni git sulla prima riga e una barra di contesto codificata a colori sulla seconda.

<Frame>
  <img src="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=60f11387658acc9ff75158ae85f2ac87" alt="Una barra di stato multi-riga che mostra il nome del modello, la directory, il ramo git sulla prima riga, e una barra di progresso dell'utilizzo del contesto con costo e durata sulla seconda riga" width="776" height="212" data-path="images/statusline-multiline.png" />
</Frame>

Questa pagina illustra come [configurare una barra di stato di base](#set-up-a-status-line), spiega [come fluiscono i dati](#how-status-lines-work) da Claude Code al tuo script, elenca [tutti i campi che puoi visualizzare](#available-data), e fornisce [esempi pronti all'uso](#examples) per modelli comuni come lo stato git, il tracciamento dei costi e le barre di progresso.

## Configura una barra di stato

Usa il [comando `/statusline`](#use-the-statusline-command) per far generare uno script a Claude Code, oppure [crea manualmente uno script](#manually-configure-a-status-line) e aggiungilo alle tue impostazioni.

### Usa il comando /statusline

Il comando `/statusline` accetta istruzioni in linguaggio naturale che descrivono cosa vuoi visualizzare. Claude Code genera un file di script in `~/.claude/` e aggiorna automaticamente le tue impostazioni:

```text  theme={null}
/statusline show model name and context percentage with a progress bar
```

### Configura manualmente una barra di stato

Aggiungi un campo `statusLine` alle tue impostazioni utente (`~/.claude/settings.json`, dove `~` è la tua directory home) o alle [impostazioni del progetto](/it/settings#settings-files). Imposta `type` su `"command"` e punta `command` a un percorso di script o a un comando di shell inline. Per una procedura dettagliata sulla creazione di uno script, vedi [Costruisci una barra di stato passo dopo passo](#build-a-status-line-step-by-step).

```json  theme={null}
{
  "statusLine": {
    "type": "command",
    "command": "~/.claude/statusline.sh",
    "padding": 2
  }
}
```

Il campo `command` viene eseguito in una shell, quindi puoi anche usare comandi inline invece di un file di script. Questo esempio usa `jq` per analizzare l'input JSON e visualizzare il nome del modello e la percentuale di contesto:

```json  theme={null}
{
  "statusLine": {
    "type": "command",
    "command": "jq -r '\"[\\(.model.display_name)] \\(.context_window.used_percentage // 0)% context\"'"
  }
}
```

Il campo opzionale `padding` aggiunge spazi orizzontali extra (in caratteri) al contenuto della barra di stato. Il valore predefinito è `0`. Questo padding è in aggiunta alla spaziatura integrata dell'interfaccia, quindi controlla l'indentazione relativa piuttosto che la distanza assoluta dal bordo del terminale.

### Disabilita la barra di stato

Esegui `/statusline` e chiedigli di rimuovere o cancellare la tua barra di stato (ad esempio, `/statusline delete`, `/statusline clear`, `/statusline remove it`). Puoi anche eliminare manualmente il campo `statusLine` dal tuo settings.json.

## Costruisci una barra di stato passo dopo passo

Questa procedura mostra cosa sta accadendo dietro le quinte creando manualmente una barra di stato che visualizza il modello corrente, la directory di lavoro e la percentuale di utilizzo della finestra di contesto.

<Note>Eseguire [`/statusline`](#use-the-statusline-command) con una descrizione di quello che vuoi configura tutto questo automaticamente per te.</Note>

Questi esempi usano script Bash, che funzionano su macOS e Linux. Su Windows, vedi [Configurazione Windows](#windows-configuration) per esempi PowerShell e Git Bash.

<Frame>
  <img src="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-quickstart.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=696445e59ca0059213250651ad23db6b" alt="Una barra di stato che mostra il nome del modello, la directory e la percentuale di contesto" width="726" height="164" data-path="images/statusline-quickstart.png" />
</Frame>

<Steps>
  <Step title="Crea uno script che legge JSON e stampa l'output">
    Claude Code invia dati JSON al tuo script tramite stdin. Questo script usa [`jq`](https://jqlang.github.io/jq/), un parser JSON da riga di comando che potrebbe essere necessario installare, per estrarre il nome del modello, la directory e la percentuale di contesto, quindi stampa una riga formattata.

    Salva questo in `~/.claude/statusline.sh` (dove `~` è la tua directory home, come `/Users/username` su macOS o `/home/username` su Linux):

    ```bash  theme={null}
    #!/bin/bash
    # Read JSON data that Claude Code sends to stdin
    input=$(cat)

    # Extract fields using jq
    MODEL=$(echo "$input" | jq -r '.model.display_name')
    DIR=$(echo "$input" | jq -r '.workspace.current_dir')
    # The "// 0" provides a fallback if the field is null
    PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

    # Output the status line - ${DIR##*/} extracts just the folder name
    echo "[$MODEL] 📁 ${DIR##*/} | ${PCT}% context"
    ```
  </Step>

  <Step title="Rendilo eseguibile">
    Contrassegna lo script come eseguibile in modo che la tua shell possa eseguirlo:

    ```bash  theme={null}
    chmod +x ~/.claude/statusline.sh
    ```
  </Step>

  <Step title="Aggiungi alle impostazioni">
    Dì a Claude Code di eseguire il tuo script come barra di stato. Aggiungi questa configurazione a `~/.claude/settings.json`, che imposta `type` su `"command"` (che significa "esegui questo comando di shell") e punta `command` al tuo script:

    ```json  theme={null}
    {
      "statusLine": {
        "type": "command",
        "command": "~/.claude/statusline.sh"
      }
    }
    ```

    La tua barra di stato appare nella parte inferiore dell'interfaccia. Le impostazioni si ricaricano automaticamente, ma le modifiche non appariranno fino alla tua prossima interazione con Claude Code.
  </Step>
</Steps>

## Come funzionano le barre di stato

Claude Code esegue il tuo script e invia i [dati di sessione JSON](#available-data) ad esso tramite stdin. Il tuo script legge il JSON, estrae quello di cui ha bisogno e stampa il testo su stdout. Claude Code visualizza tutto ciò che il tuo script stampa.

**Quando si aggiorna**

Il tuo script viene eseguito dopo ogni nuovo messaggio dell'assistente, quando cambia la modalità di autorizzazione o quando la modalità vim si attiva/disattiva. Gli aggiornamenti vengono debounced a 300ms, il che significa che i cambiamenti rapidi si raggruppano insieme e il tuo script viene eseguito una volta che le cose si stabilizzano. Se un nuovo aggiornamento si attiva mentre il tuo script è ancora in esecuzione, l'esecuzione in corso viene annullata. Se modifichi il tuo script, le modifiche non appariranno fino al prossimo aggiornamento di Claude Code.

**Cosa può produrre il tuo script**

* **Più righe**: ogni istruzione `echo` o `print` viene visualizzata come una riga separata. Vedi l'[esempio multi-riga](#display-multiple-lines).
* **Colori**: usa [codici di escape ANSI](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors) come `\033[32m` per il verde (il terminale deve supportarli). Vedi l'[esempio di stato git](#git-status-with-colors).
* **Link**: usa [sequenze di escape OSC 8](https://en.wikipedia.org/wiki/ANSI_escape_code#OSC) per rendere il testo cliccabile (Cmd+clic su macOS, Ctrl+clic su Windows/Linux). Richiede un terminale che supporti i hyperlink come iTerm2, Kitty o WezTerm. Vedi l'[esempio di link cliccabili](#clickable-links).

<Note>La barra di stato viene eseguita localmente e non consuma token API. Si nasconde temporaneamente durante determinate interazioni dell'interfaccia utente, inclusi i suggerimenti di completamento automatico, il menu della guida e i prompt di autorizzazione.</Note>

## Dati disponibili

Claude Code invia i seguenti campi JSON al tuo script tramite stdin:

| Campo                                                                            | Descrizione                                                                                                                                                                                                               |
| -------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `model.id`, `model.display_name`                                                 | Identificatore del modello corrente e nome visualizzato                                                                                                                                                                   |
| `cwd`, `workspace.current_dir`                                                   | Directory di lavoro corrente. Entrambi i campi contengono lo stesso valore; `workspace.current_dir` è preferito per coerenza con `workspace.project_dir`.                                                                 |
| `workspace.project_dir`                                                          | Directory in cui Claude Code è stato avviato, che potrebbe differire da `cwd` se la directory di lavoro cambia durante una sessione                                                                                       |
| `workspace.added_dirs`                                                           | Directory aggiuntive aggiunte tramite `/add-dir` o `--add-dir`. Array vuoto se nessuna è stata aggiunta                                                                                                                   |
| `cost.total_cost_usd`                                                            | Costo totale della sessione in USD                                                                                                                                                                                        |
| `cost.total_duration_ms`                                                         | Tempo totale trascorso dal momento dell'avvio della sessione, in millisecondi                                                                                                                                             |
| `cost.total_api_duration_ms`                                                     | Tempo totale trascorso in attesa delle risposte API in millisecondi                                                                                                                                                       |
| `cost.total_lines_added`, `cost.total_lines_removed`                             | Righe di codice modificate                                                                                                                                                                                                |
| `context_window.total_input_tokens`, `context_window.total_output_tokens`        | Conteggi cumulativi dei token nella sessione                                                                                                                                                                              |
| `context_window.context_window_size`                                             | Dimensione massima della finestra di contesto in token. 200000 per impostazione predefinita, o 1000000 per i modelli con contesto esteso.                                                                                 |
| `context_window.used_percentage`                                                 | Percentuale pre-calcolata della finestra di contesto utilizzata                                                                                                                                                           |
| `context_window.remaining_percentage`                                            | Percentuale pre-calcolata della finestra di contesto rimanente                                                                                                                                                            |
| `context_window.current_usage`                                                   | Conteggi dei token dall'ultima chiamata API, descritti in [campi della finestra di contesto](#context-window-fields)                                                                                                      |
| `exceeds_200k_tokens`                                                            | Se il conteggio totale dei token (token di input, cache e output combinati) dalla risposta API più recente supera 200k. Questo è un limite fisso indipendentemente dalla dimensione effettiva della finestra di contesto. |
| `rate_limits.five_hour.used_percentage`, `rate_limits.seven_day.used_percentage` | Percentuale del limite di velocità di 5 ore o 7 giorni consumato, da 0 a 100                                                                                                                                              |
| `rate_limits.five_hour.resets_at`, `rate_limits.seven_day.resets_at`             | Secondi di epoca Unix quando la finestra del limite di velocità di 5 ore o 7 giorni si ripristina                                                                                                                         |
| `session_id`                                                                     | Identificatore univoco della sessione                                                                                                                                                                                     |
| `session_name`                                                                   | Nome della sessione personalizzato impostato con il flag `--name` o `/rename`. Assente se nessun nome personalizzato è stato impostato                                                                                    |
| `transcript_path`                                                                | Percorso del file di trascrizione della conversazione                                                                                                                                                                     |
| `version`                                                                        | Versione di Claude Code                                                                                                                                                                                                   |
| `output_style.name`                                                              | Nome dello stile di output corrente                                                                                                                                                                                       |
| `vim.mode`                                                                       | Modalità vim corrente (`NORMAL` o `INSERT`) quando la [modalità vim](/it/interactive-mode#vim-editor-mode) è abilitata                                                                                                    |
| `agent.name`                                                                     | Nome dell'agente quando si esegue con il flag `--agent` o le impostazioni dell'agente configurate                                                                                                                         |
| `worktree.name`                                                                  | Nome del worktree attivo. Presente solo durante le sessioni `--worktree`                                                                                                                                                  |
| `worktree.path`                                                                  | Percorso assoluto della directory del worktree                                                                                                                                                                            |
| `worktree.branch`                                                                | Nome del ramo git per il worktree (ad esempio, `"worktree-my-feature"`). Assente per i worktree basati su hook                                                                                                            |
| `worktree.original_cwd`                                                          | La directory in cui Claude si trovava prima di entrare nel worktree                                                                                                                                                       |
| `worktree.original_branch`                                                       | Ramo git estratto prima di entrare nel worktree. Assente per i worktree basati su hook                                                                                                                                    |

<Accordion title="Schema JSON completo">
  Il tuo comando della barra di stato riceve questa struttura JSON tramite stdin:

  ```json  theme={null}
  {
    "cwd": "/current/working/directory",
    "session_id": "abc123...",
    "session_name": "my-session",
    "transcript_path": "/path/to/transcript.jsonl",
    "model": {
      "id": "claude-opus-4-6",
      "display_name": "Opus"
    },
    "workspace": {
      "current_dir": "/current/working/directory",
      "project_dir": "/original/project/directory",
      "added_dirs": []
    },
    "version": "2.1.90",
    "output_style": {
      "name": "default"
    },
    "cost": {
      "total_cost_usd": 0.01234,
      "total_duration_ms": 45000,
      "total_api_duration_ms": 2300,
      "total_lines_added": 156,
      "total_lines_removed": 23
    },
    "context_window": {
      "total_input_tokens": 15234,
      "total_output_tokens": 4521,
      "context_window_size": 200000,
      "used_percentage": 8,
      "remaining_percentage": 92,
      "current_usage": {
        "input_tokens": 8500,
        "output_tokens": 1200,
        "cache_creation_input_tokens": 5000,
        "cache_read_input_tokens": 2000
      }
    },
    "exceeds_200k_tokens": false,
    "rate_limits": {
      "five_hour": {
        "used_percentage": 23.5,
        "resets_at": 1738425600
      },
      "seven_day": {
        "used_percentage": 41.2,
        "resets_at": 1738857600
      }
    },
    "vim": {
      "mode": "NORMAL"
    },
    "agent": {
      "name": "security-reviewer"
    },
    "worktree": {
      "name": "my-feature",
      "path": "/path/to/.claude/worktrees/my-feature",
      "branch": "worktree-my-feature",
      "original_cwd": "/path/to/project",
      "original_branch": "main"
    }
  }
  ```

  **Campi che potrebbero essere assenti** (non presenti in JSON):

  * `session_name`: appare solo quando un nome personalizzato è stato impostato con `--name` o `/rename`
  * `vim`: appare solo quando la modalità vim è abilitata
  * `agent`: appare solo quando si esegue con il flag `--agent` o le impostazioni dell'agente configurate
  * `worktree`: appare solo durante le sessioni `--worktree`. Quando presente, `branch` e `original_branch` potrebbero anche essere assenti per i worktree basati su hook
  * `rate_limits`: appare solo per gli abbonati Claude.ai (Pro/Max) dopo la prima risposta API nella sessione. Ogni finestra (`five_hour`, `seven_day`) potrebbe essere indipendentemente assente. Usa `jq -r '.rate_limits.five_hour.used_percentage // empty'` per gestire l'assenza con eleganza.

  **Campi che potrebbero essere `null`**:

  * `context_window.current_usage`: `null` prima della prima chiamata API in una sessione
  * `context_window.used_percentage`, `context_window.remaining_percentage`: potrebbero essere `null` all'inizio della sessione

  Gestisci i campi mancanti con accesso condizionale e i valori null con fallback predefiniti nei tuoi script.
</Accordion>

### Campi della finestra di contesto

L'oggetto `context_window` fornisce due modi per tracciare l'utilizzo del contesto:

* **Totali cumulativi** (`total_input_tokens`, `total_output_tokens`): somma di tutti i token nell'intera sessione, utile per tracciare il consumo totale
* **Utilizzo corrente** (`current_usage`): conteggi dei token dall'ultima chiamata API, usa questo per una percentuale di contesto accurata poiché riflette lo stato effettivo del contesto

L'oggetto `current_usage` contiene:

* `input_tokens`: token di input nel contesto corrente
* `output_tokens`: token di output generati
* `cache_creation_input_tokens`: token scritti nella cache
* `cache_read_input_tokens`: token letti dalla cache

Il campo `used_percentage` viene calcolato solo dai token di input: `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`. Non include `output_tokens`.

Se calcoli manualmente la percentuale di contesto da `current_usage`, usa la stessa formula solo per l'input per corrispondere a `used_percentage`.

L'oggetto `current_usage` è `null` prima della prima chiamata API in una sessione.

## Esempi

Questi esempi mostrano modelli comuni della barra di stato. Per usare qualsiasi esempio:

1. Salva lo script in un file come `~/.claude/statusline.sh` (o `.py`/`.js`)
2. Rendilo eseguibile: `chmod +x ~/.claude/statusline.sh`
3. Aggiungi il percorso alle tue [impostazioni](#manually-configure-a-status-line)

Gli esempi Bash usano [`jq`](https://jqlang.github.io/jq/) per analizzare JSON. Python e Node.js hanno l'analisi JSON integrata.

### Utilizzo della finestra di contesto

Visualizza il modello corrente e l'utilizzo della finestra di contesto con una barra di progresso visiva. Ogni script legge JSON da stdin, estrae il campo `used_percentage` e costruisce una barra di 10 caratteri dove i blocchi pieni (▓) rappresentano l'utilizzo:

<Frame>
  <img src="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-context-window-usage.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=15b58ab3602f036939145dde3165c6f7" alt="Una barra di stato che mostra il nome del modello e una barra di progresso con percentuale" width="448" height="152" data-path="images/statusline-context-window-usage.png" />
</Frame>

<CodeGroup>
  ```bash Bash theme={null}
  #!/bin/bash
  # Read all of stdin into a variable
  input=$(cat)

  # Extract fields with jq, "// 0" provides fallback for null
  MODEL=$(echo "$input" | jq -r '.model.display_name')
  PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)

  # Build progress bar: printf -v creates a run of spaces, then
  # ${var// /▓} replaces each space with a block character
  BAR_WIDTH=10
  FILLED=$((PCT * BAR_WIDTH / 100))
  EMPTY=$((BAR_WIDTH - FILLED))
  BAR=""
  [ "$FILLED" -gt 0 ] && printf -v FILL "%${FILLED}s" && BAR="${FILL// /▓}"
  [ "$EMPTY" -gt 0 ] && printf -v PAD "%${EMPTY}s" && BAR="${BAR}${PAD// /░}"

  echo "[$MODEL] $BAR $PCT%"
  ```

  ```python Python theme={null}
  #!/usr/bin/env python3
  import json, sys

  # json.load reads and parses stdin in one step
  data = json.load(sys.stdin)
  model = data['model']['display_name']
  # "or 0" handles null values
  pct = int(data.get('context_window', {}).get('used_percentage', 0) or 0)

  # String multiplication builds the bar
  filled = pct * 10 // 100
  bar = '▓' * filled + '░' * (10 - filled)

  print(f"[{model}] {bar} {pct}%")
  ```

  ```javascript Node.js theme={null}
  #!/usr/bin/env node
  // Node.js reads stdin asynchronously with events
  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      // Optional chaining (?.) safely handles null fields
      const pct = Math.floor(data.context_window?.used_percentage || 0);

      // String.repeat() builds the bar
      const filled = Math.floor(pct * 10 / 100);
      const bar = '▓'.repeat(filled) + '░'.repeat(10 - filled);

      console.log(`[${model}] ${bar} ${pct}%`);
  });
  ```
</CodeGroup>

### Stato git con colori

Mostra il ramo git con indicatori codificati a colori per i file in staging e modificati. Questo script usa [codici di escape ANSI](https://en.wikipedia.org/wiki/ANSI_escape_code#Colors) per i colori del terminale: `\033[32m` è verde, `\033[33m` è giallo e `\033[0m` ripristina il valore predefinito.

<Frame>
  <img src="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-git-context.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=e656f34f90d1d9a1d0e220988914345f" alt="Una barra di stato che mostra il modello, la directory, il ramo git e indicatori codificati a colori per i file in staging e modificati" width="742" height="178" data-path="images/statusline-git-context.png" />
</Frame>

Ogni script verifica se la directory corrente è un repository git, conta i file in staging e modificati e visualizza indicatori codificati a colori:

<CodeGroup>
  ```bash Bash theme={null}
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')
  DIR=$(echo "$input" | jq -r '.workspace.current_dir')

  GREEN='\033[32m'
  YELLOW='\033[33m'
  RESET='\033[0m'

  if git rev-parse --git-dir > /dev/null 2>&1; then
      BRANCH=$(git branch --show-current 2>/dev/null)
      STAGED=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
      MODIFIED=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')

      GIT_STATUS=""
      [ "$STAGED" -gt 0 ] && GIT_STATUS="${GREEN}+${STAGED}${RESET}"
      [ "$MODIFIED" -gt 0 ] && GIT_STATUS="${GIT_STATUS}${YELLOW}~${MODIFIED}${RESET}"

      echo -e "[$MODEL] 📁 ${DIR##*/} | 🌿 $BRANCH $GIT_STATUS"
  else
      echo "[$MODEL] 📁 ${DIR##*/}"
  fi
  ```

  ```python Python theme={null}
  #!/usr/bin/env python3
  import json, sys, subprocess, os

  data = json.load(sys.stdin)
  model = data['model']['display_name']
  directory = os.path.basename(data['workspace']['current_dir'])

  GREEN, YELLOW, RESET = '\033[32m', '\033[33m', '\033[0m'

  try:
      subprocess.check_output(['git', 'rev-parse', '--git-dir'], stderr=subprocess.DEVNULL)
      branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
      staged_output = subprocess.check_output(['git', 'diff', '--cached', '--numstat'], text=True).strip()
      modified_output = subprocess.check_output(['git', 'diff', '--numstat'], text=True).strip()
      staged = len(staged_output.split('\n')) if staged_output else 0
      modified = len(modified_output.split('\n')) if modified_output else 0

      git_status = f"{GREEN}+{staged}{RESET}" if staged else ""
      git_status += f"{YELLOW}~{modified}{RESET}" if modified else ""

      print(f"[{model}] 📁 {directory} | 🌿 {branch} {git_status}")
  except:
      print(f"[{model}] 📁 {directory}")
  ```

  ```javascript Node.js theme={null}
  #!/usr/bin/env node
  const { execSync } = require('child_process');
  const path = require('path');

  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      const dir = path.basename(data.workspace.current_dir);

      const GREEN = '\x1b[32m', YELLOW = '\x1b[33m', RESET = '\x1b[0m';

      try {
          execSync('git rev-parse --git-dir', { stdio: 'ignore' });
          const branch = execSync('git branch --show-current', { encoding: 'utf8' }).trim();
          const staged = execSync('git diff --cached --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;
          const modified = execSync('git diff --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;

          let gitStatus = staged ? `${GREEN}+${staged}${RESET}` : '';
          gitStatus += modified ? `${YELLOW}~${modified}${RESET}` : '';

          console.log(`[${model}] 📁 ${dir} | 🌿 ${branch} ${gitStatus}`);
      } catch {
          console.log(`[${model}] 📁 ${dir}`);
      }
  });
  ```
</CodeGroup>

### Tracciamento di costi e durata

Traccia i costi API della tua sessione e il tempo trascorso. Il campo `cost.total_cost_usd` accumula il costo di tutte le chiamate API nella sessione corrente. Il campo `cost.total_duration_ms` misura il tempo totale trascorso dall'inizio della sessione, mentre `cost.total_api_duration_ms` traccia solo il tempo trascorso in attesa delle risposte API.

Ogni script formatta il costo come valuta e converte i millisecondi in minuti e secondi:

<Frame>
  <img src="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-cost-tracking.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=e3444a51fe6f3440c134bd5f1f08ad29" alt="Una barra di stato che mostra il nome del modello, il costo della sessione e la durata" width="588" height="180" data-path="images/statusline-cost-tracking.png" />
</Frame>

<CodeGroup>
  ```bash Bash theme={null}
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')
  COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
  DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')

  COST_FMT=$(printf '$%.2f' "$COST")
  DURATION_SEC=$((DURATION_MS / 1000))
  MINS=$((DURATION_SEC / 60))
  SECS=$((DURATION_SEC % 60))

  echo "[$MODEL] 💰 $COST_FMT | ⏱️ ${MINS}m ${SECS}s"
  ```

  ```python Python theme={null}
  #!/usr/bin/env python3
  import json, sys

  data = json.load(sys.stdin)
  model = data['model']['display_name']
  cost = data.get('cost', {}).get('total_cost_usd', 0) or 0
  duration_ms = data.get('cost', {}).get('total_duration_ms', 0) or 0

  duration_sec = duration_ms // 1000
  mins, secs = duration_sec // 60, duration_sec % 60

  print(f"[{model}] 💰 ${cost:.2f} | ⏱️ {mins}m {secs}s")
  ```

  ```javascript Node.js theme={null}
  #!/usr/bin/env node
  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      const cost = data.cost?.total_cost_usd || 0;
      const durationMs = data.cost?.total_duration_ms || 0;

      const durationSec = Math.floor(durationMs / 1000);
      const mins = Math.floor(durationSec / 60);
      const secs = durationSec % 60;

      console.log(`[${model}] 💰 $${cost.toFixed(2)} | ⏱️ ${mins}m ${secs}s`);
  });
  ```
</CodeGroup>

### Visualizza più righe

Il tuo script può produrre più righe per creare una visualizzazione più ricca. Ogni istruzione `echo` produce una riga separata nell'area di stato.

<Frame>
  <img src="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-multiline.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=60f11387658acc9ff75158ae85f2ac87" alt="Una barra di stato multi-riga che mostra il nome del modello, la directory, il ramo git sulla prima riga, e una barra di progresso dell'utilizzo del contesto con costo e durata sulla seconda riga" width="776" height="212" data-path="images/statusline-multiline.png" />
</Frame>

Questo esempio combina diverse tecniche: colori basati su soglie (verde sotto il 70%, giallo 70-89%, rosso 90%+), una barra di progresso e informazioni sul ramo git. Ogni istruzione `print` o `echo` crea una riga separata:

<CodeGroup>
  ```bash Bash theme={null}
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')
  DIR=$(echo "$input" | jq -r '.workspace.current_dir')
  COST=$(echo "$input" | jq -r '.cost.total_cost_usd // 0')
  PCT=$(echo "$input" | jq -r '.context_window.used_percentage // 0' | cut -d. -f1)
  DURATION_MS=$(echo "$input" | jq -r '.cost.total_duration_ms // 0')

  CYAN='\033[36m'; GREEN='\033[32m'; YELLOW='\033[33m'; RED='\033[31m'; RESET='\033[0m'

  # Pick bar color based on context usage
  if [ "$PCT" -ge 90 ]; then BAR_COLOR="$RED"
  elif [ "$PCT" -ge 70 ]; then BAR_COLOR="$YELLOW"
  else BAR_COLOR="$GREEN"; fi

  FILLED=$((PCT / 10)); EMPTY=$((10 - FILLED))
  printf -v FILL "%${FILLED}s"; printf -v PAD "%${EMPTY}s"
  BAR="${FILL// /█}${PAD// /░}"

  MINS=$((DURATION_MS / 60000)); SECS=$(((DURATION_MS % 60000) / 1000))

  BRANCH=""
  git rev-parse --git-dir > /dev/null 2>&1 && BRANCH=" | 🌿 $(git branch --show-current 2>/dev/null)"

  echo -e "${CYAN}[$MODEL]${RESET} 📁 ${DIR##*/}$BRANCH"
  COST_FMT=$(printf '$%.2f' "$COST")
  echo -e "${BAR_COLOR}${BAR}${RESET} ${PCT}% | ${YELLOW}${COST_FMT}${RESET} | ⏱️ ${MINS}m ${SECS}s"
  ```

  ```python Python theme={null}
  #!/usr/bin/env python3
  import json, sys, subprocess, os

  data = json.load(sys.stdin)
  model = data['model']['display_name']
  directory = os.path.basename(data['workspace']['current_dir'])
  cost = data.get('cost', {}).get('total_cost_usd', 0) or 0
  pct = int(data.get('context_window', {}).get('used_percentage', 0) or 0)
  duration_ms = data.get('cost', {}).get('total_duration_ms', 0) or 0

  CYAN, GREEN, YELLOW, RED, RESET = '\033[36m', '\033[32m', '\033[33m', '\033[31m', '\033[0m'

  bar_color = RED if pct >= 90 else YELLOW if pct >= 70 else GREEN
  filled = pct // 10
  bar = '█' * filled + '░' * (10 - filled)

  mins, secs = duration_ms // 60000, (duration_ms % 60000) // 1000

  try:
      branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True, stderr=subprocess.DEVNULL).strip()
      branch = f" | 🌿 {branch}" if branch else ""
  except:
      branch = ""

  print(f"{CYAN}[{model}]{RESET} 📁 {directory}{branch}")
  print(f"{bar_color}{bar}{RESET} {pct}% | {YELLOW}${cost:.2f}{RESET} | ⏱️ {mins}m {secs}s")
  ```

  ```javascript Node.js theme={null}
  #!/usr/bin/env node
  const { execSync } = require('child_process');
  const path = require('path');

  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      const dir = path.basename(data.workspace.current_dir);
      const cost = data.cost?.total_cost_usd || 0;
      const pct = Math.floor(data.context_window?.used_percentage || 0);
      const durationMs = data.cost?.total_duration_ms || 0;

      const CYAN = '\x1b[36m', GREEN = '\x1b[32m', YELLOW = '\x1b[33m', RED = '\x1b[31m', RESET = '\x1b[0m';

      const barColor = pct >= 90 ? RED : pct >= 70 ? YELLOW : GREEN;
      const filled = Math.floor(pct / 10);
      const bar = '█'.repeat(filled) + '░'.repeat(10 - filled);

      const mins = Math.floor(durationMs / 60000);
      const secs = Math.floor((durationMs % 60000) / 1000);

      let branch = '';
      try {
          branch = execSync('git branch --show-current', { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] }).trim();
          branch = branch ? ` | 🌿 ${branch}` : '';
      } catch {}

      console.log(`${CYAN}[${model}]${RESET} 📁 ${dir}${branch}`);
      console.log(`${barColor}${bar}${RESET} ${pct}% | ${YELLOW}$${cost.toFixed(2)}${RESET} | ⏱️ ${mins}m ${secs}s`);
  });
  ```
</CodeGroup>

### Link cliccabili

Questo esempio crea un link cliccabile al tuo repository GitHub. Legge l'URL del remote git, converte il formato SSH in HTTPS con `sed` e avvolge il nome del repository nei codici di escape OSC 8. Tieni premuto Cmd (macOS) o Ctrl (Windows/Linux) e fai clic per aprire il link nel tuo browser.

<Frame>
  <img src="https://mintcdn.com/claude-code/nibzesLaJVh4ydOq/images/statusline-links.png?fit=max&auto=format&n=nibzesLaJVh4ydOq&q=85&s=4bcc6e7deb7cf52f41ab85a219b52661" alt="Una barra di stato che mostra un link cliccabile a un repository GitHub" width="726" height="198" data-path="images/statusline-links.png" />
</Frame>

Ogni script ottiene l'URL del remote git, converte il formato SSH in HTTPS e avvolge il nome del repository nei codici di escape OSC 8. La versione Bash usa `printf '%b'` che interpreta gli escape di backslash in modo più affidabile rispetto a `echo -e` su diverse shell:

<CodeGroup>
  ```bash Bash theme={null}
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')

  # Convert git SSH URL to HTTPS
  REMOTE=$(git remote get-url origin 2>/dev/null | sed 's/git@github.com:/https:\/\/github.com\//' | sed 's/\.git$//')

  if [ -n "$REMOTE" ]; then
      REPO_NAME=$(basename "$REMOTE")
      # OSC 8 format: \e]8;;URL\a then TEXT then \e]8;;\a
      # printf %b interprets escape sequences reliably across shells
      printf '%b' "[$MODEL] 🔗 \e]8;;${REMOTE}\a${REPO_NAME}\e]8;;\a\n"
  else
      echo "[$MODEL]"
  fi
  ```

  ```python Python theme={null}
  #!/usr/bin/env python3
  import json, sys, subprocess, re, os

  data = json.load(sys.stdin)
  model = data['model']['display_name']

  # Get git remote URL
  try:
      remote = subprocess.check_output(
          ['git', 'remote', 'get-url', 'origin'],
          stderr=subprocess.DEVNULL, text=True
      ).strip()
      # Convert SSH to HTTPS format
      remote = re.sub(r'^git@github\.com:', 'https://github.com/', remote)
      remote = re.sub(r'\.git$', '', remote)
      repo_name = os.path.basename(remote)
      # OSC 8 escape sequences
      link = f"\033]8;;{remote}\a{repo_name}\033]8;;\a"
      print(f"[{model}] 🔗 {link}")
  except:
      print(f"[{model}]")
  ```

  ```javascript Node.js theme={null}
  #!/usr/bin/env node
  const { execSync } = require('child_process');
  const path = require('path');

  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;

      try {
          let remote = execSync('git remote get-url origin', { encoding: 'utf8', stdio: ['pipe', 'pipe', 'ignore'] }).trim();
          // Convert SSH to HTTPS format
          remote = remote.replace(/^git@github\.com:/, 'https://github.com/').replace(/\.git$/, '');
          const repoName = path.basename(remote);
          // OSC 8 escape sequences
          const link = `\x1b]8;;${remote}\x07${repoName}\x1b]8;;\x07`;
          console.log(`[${model}] 🔗 ${link}`);
      } catch {
          console.log(`[${model}]`);
      }
  });
  ```
</CodeGroup>

### Utilizzo del limite di velocità

Visualizza l'utilizzo del limite di velocità dell'abbonamento Claude.ai nella barra di stato. L'oggetto `rate_limits` contiene `five_hour` (finestra mobile di 5 ore) e `seven_day` (finestra settimanale). Ogni finestra fornisce `used_percentage` (0-100) e `resets_at` (secondi di epoca Unix quando la finestra si ripristina).

Questo campo è presente solo per gli abbonati Claude.ai (Pro/Max) dopo la prima risposta API. Ogni script gestisce il campo assente con eleganza:

<CodeGroup>
  ```bash Bash theme={null}
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')
  # "// empty" produces no output when rate_limits is absent
  FIVE_H=$(echo "$input" | jq -r '.rate_limits.five_hour.used_percentage // empty')
  WEEK=$(echo "$input" | jq -r '.rate_limits.seven_day.used_percentage // empty')

  LIMITS=""
  [ -n "$FIVE_H" ] && LIMITS="5h: $(printf '%.0f' "$FIVE_H")%"
  [ -n "$WEEK" ] && LIMITS="${LIMITS:+$LIMITS }7d: $(printf '%.0f' "$WEEK")%"

  [ -n "$LIMITS" ] && echo "[$MODEL] | $LIMITS" || echo "[$MODEL]"
  ```

  ```python Python theme={null}
  #!/usr/bin/env python3
  import json, sys

  data = json.load(sys.stdin)
  model = data['model']['display_name']

  parts = []
  rate = data.get('rate_limits', {})
  five_h = rate.get('five_hour', {}).get('used_percentage')
  week = rate.get('seven_day', {}).get('used_percentage')

  if five_h is not None:
      parts.append(f"5h: {five_h:.0f}%")
  if week is not None:
      parts.append(f"7d: {week:.0f}%")

  if parts:
      print(f"[{model}] | {' '.join(parts)}")
  else:
      print(f"[{model}]")
  ```

  ```javascript Node.js theme={null}
  #!/usr/bin/env node
  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;

      const parts = [];
      const fiveH = data.rate_limits?.five_hour?.used_percentage;
      const week = data.rate_limits?.seven_day?.used_percentage;

      if (fiveH != null) parts.push(`5h: ${Math.round(fiveH)}%`);
      if (week != null) parts.push(`7d: ${Math.round(week)}%`);

      console.log(parts.length ? `[${model}] | ${parts.join(' ')}` : `[${model}]`);
  });
  ```
</CodeGroup>

### Memorizza nella cache le operazioni costose

Il tuo script della barra di stato viene eseguito frequentemente durante le sessioni attive. Comandi come `git status` o `git diff` possono essere lenti, specialmente in repository di grandi dimensioni. Questo esempio memorizza nella cache le informazioni git in un file temporaneo e le aggiorna solo ogni 5 secondi.

Usa un nome di file stabile e fisso per il file di cache come `/tmp/statusline-git-cache`. Ogni invocazione della barra di stato viene eseguita come un nuovo processo, quindi gli identificatori basati su processi come `$$`, `os.getpid()` o `process.pid` producono un valore diverso ogni volta e la cache non viene mai riutilizzata.

Ogni script verifica se il file di cache è mancante o più vecchio di 5 secondi prima di eseguire i comandi git:

<CodeGroup>
  ```bash Bash theme={null}
  #!/bin/bash
  input=$(cat)

  MODEL=$(echo "$input" | jq -r '.model.display_name')
  DIR=$(echo "$input" | jq -r '.workspace.current_dir')

  CACHE_FILE="/tmp/statusline-git-cache"
  CACHE_MAX_AGE=5  # seconds

  cache_is_stale() {
      [ ! -f "$CACHE_FILE" ] || \
      # stat -f %m is macOS, stat -c %Y is Linux
      [ $(($(date +%s) - $(stat -f %m "$CACHE_FILE" 2>/dev/null || stat -c %Y "$CACHE_FILE" 2>/dev/null || echo 0))) -gt $CACHE_MAX_AGE ]
  }

  if cache_is_stale; then
      if git rev-parse --git-dir > /dev/null 2>&1; then
          BRANCH=$(git branch --show-current 2>/dev/null)
          STAGED=$(git diff --cached --numstat 2>/dev/null | wc -l | tr -d ' ')
          MODIFIED=$(git diff --numstat 2>/dev/null | wc -l | tr -d ' ')
          echo "$BRANCH|$STAGED|$MODIFIED" > "$CACHE_FILE"
      else
          echo "||" > "$CACHE_FILE"
      fi
  fi

  IFS='|' read -r BRANCH STAGED MODIFIED < "$CACHE_FILE"

  if [ -n "$BRANCH" ]; then
      echo "[$MODEL] 📁 ${DIR##*/} | 🌿 $BRANCH +$STAGED ~$MODIFIED"
  else
      echo "[$MODEL] 📁 ${DIR##*/}"
  fi
  ```

  ```python Python theme={null}
  #!/usr/bin/env python3
  import json, sys, subprocess, os, time

  data = json.load(sys.stdin)
  model = data['model']['display_name']
  directory = os.path.basename(data['workspace']['current_dir'])

  CACHE_FILE = "/tmp/statusline-git-cache"
  CACHE_MAX_AGE = 5  # seconds

  def cache_is_stale():
      if not os.path.exists(CACHE_FILE):
          return True
      return time.time() - os.path.getmtime(CACHE_FILE) > CACHE_MAX_AGE

  if cache_is_stale():
      try:
          subprocess.check_output(['git', 'rev-parse', '--git-dir'], stderr=subprocess.DEVNULL)
          branch = subprocess.check_output(['git', 'branch', '--show-current'], text=True).strip()
          staged = subprocess.check_output(['git', 'diff', '--cached', '--numstat'], text=True).strip()
          modified = subprocess.check_output(['git', 'diff', '--numstat'], text=True).strip()
          staged_count = len(staged.split('\n')) if staged else 0
          modified_count = len(modified.split('\n')) if modified else 0
          with open(CACHE_FILE, 'w') as f:
              f.write(f"{branch}|{staged_count}|{modified_count}")
      except:
          with open(CACHE_FILE, 'w') as f:
              f.write("||")

  with open(CACHE_FILE) as f:
      branch, staged, modified = f.read().strip().split('|')

  if branch:
      print(f"[{model}] 📁 {directory} | 🌿 {branch} +{staged} ~{modified}")
  else:
      print(f"[{model}] 📁 {directory}")
  ```

  ```javascript Node.js theme={null}
  #!/usr/bin/env node
  const { execSync } = require('child_process');
  const fs = require('fs');
  const path = require('path');

  let input = '';
  process.stdin.on('data', chunk => input += chunk);
  process.stdin.on('end', () => {
      const data = JSON.parse(input);
      const model = data.model.display_name;
      const dir = path.basename(data.workspace.current_dir);

      const CACHE_FILE = '/tmp/statusline-git-cache';
      const CACHE_MAX_AGE = 5; // seconds

      const cacheIsStale = () => {
          if (!fs.existsSync(CACHE_FILE)) return true;
          return (Date.now() / 1000) - fs.statSync(CACHE_FILE).mtimeMs / 1000 > CACHE_MAX_AGE;
      };

      if (cacheIsStale()) {
          try {
              execSync('git rev-parse --git-dir', { stdio: 'ignore' });
              const branch = execSync('git branch --show-current', { encoding: 'utf8' }).trim();
              const staged = execSync('git diff --cached --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;
              const modified = execSync('git diff --numstat', { encoding: 'utf8' }).trim().split('\n').filter(Boolean).length;
              fs.writeFileSync(CACHE_FILE, `${branch}|${staged}|${modified}`);
          } catch {
              fs.writeFileSync(CACHE_FILE, '||');
          }
      }

      const [branch, staged, modified] = fs.readFileSync(CACHE_FILE, 'utf8').trim().split('|');

      if (branch) {
          console.log(`[${model}] 📁 ${dir} | 🌿 ${branch} +${staged} ~${modified}`);
      } else {
          console.log(`[${model}] 📁 ${dir}`);
      }
  });
  ```
</CodeGroup>

### Configurazione Windows

Su Windows, Claude Code esegue i comandi della barra di stato tramite Git Bash. Puoi invocare PowerShell da quella shell:

<CodeGroup>
  ```json settings.json theme={null}
  {
    "statusLine": {
      "type": "command",
      "command": "powershell -NoProfile -File C:/Users/username/.claude/statusline.ps1"
    }
  }
  ```

  ```powershell statusline.ps1 theme={null}
  $input_json = $input | Out-String | ConvertFrom-Json
  $cwd = $input_json.cwd
  $model = $input_json.model.display_name
  $used = $input_json.context_window.used_percentage
  $dirname = Split-Path $cwd -Leaf

  if ($used) {
      Write-Host "$dirname [$model] ctx: $used%"
  } else {
      Write-Host "$dirname [$model]"
  }
  ```
</CodeGroup>

Oppure esegui uno script Bash direttamente:

<CodeGroup>
  ```json settings.json theme={null}
  {
    "statusLine": {
      "type": "command",
      "command": "~/.claude/statusline.sh"
    }
  }
  ```

  ```bash statusline.sh theme={null}
  #!/usr/bin/env bash
  input=$(cat)
  cwd=$(echo "$input" | grep -o '"cwd":"[^"]*"' | cut -d'"' -f4)
  model=$(echo "$input" | grep -o '"display_name":"[^"]*"' | cut -d'"' -f4)
  dirname="${cwd##*[/\\]}"
  echo "$dirname [$model]"
  ```
</CodeGroup>

## Suggerimenti

* **Testa con input simulato**: `echo '{"model":{"display_name":"Opus"},"context_window":{"used_percentage":25}}' | ./statusline.sh`
* **Mantieni l'output breve**: la barra di stato ha una larghezza limitata, quindi l'output lungo potrebbe essere troncato o andare a capo in modo sgradevole
* **Memorizza nella cache le operazioni lente**: il tuo script viene eseguito frequentemente durante le sessioni attive, quindi comandi come `git status` possono causare lag. Vedi l'[esempio di caching](#cache-expensive-operations) per come gestire questo.

Progetti della comunità come [ccstatusline](https://github.com/sirmalloc/ccstatusline) e [starship-claude](https://github.com/martinemde/starship-claude) forniscono configurazioni pre-costruite con temi e funzionalità aggiuntive.

## Risoluzione dei problemi

**La barra di stato non appare**

* Verifica che il tuo script sia eseguibile: `chmod +x ~/.claude/statusline.sh`
* Controlla che il tuo script stampi su stdout, non su stderr
* Esegui il tuo script manualmente per verificare che produca output
* Se `disableAllHooks` è impostato su `true` nelle tue impostazioni, anche la barra di stato è disabilitata. Rimuovi questa impostazione o impostala su `false` per riabilitarla.
* Esegui `claude --debug` per registrare il codice di uscita e stderr dalla prima invocazione della barra di stato in una sessione
* Chiedi a Claude di leggere il tuo file di impostazioni ed eseguire il comando `statusLine` direttamente per far emergere gli errori

**La barra di stato mostra `--` o valori vuoti**

* I campi potrebbero essere `null` prima che la prima risposta API si completi
* Gestisci i valori null nel tuo script con fallback come `// 0` in jq
* Riavvia Claude Code se i valori rimangono vuoti dopo più messaggi

**La percentuale di contesto mostra valori inaspettati**

* Usa `used_percentage` per uno stato di contesto accurato piuttosto che i totali cumulativi
* `total_input_tokens` e `total_output_tokens` sono cumulativi nella sessione e potrebbero superare la dimensione della finestra di contesto
* La percentuale di contesto potrebbe differire dall'output `/context` a causa di quando ciascuno viene calcolato

**I link OSC 8 non sono cliccabili**

* Verifica che il tuo terminale supporti i hyperlink OSC 8 (iTerm2, Kitty, WezTerm)
* Terminal.app non supporta i link cliccabili
* Le sessioni SSH e tmux potrebbero eliminare le sequenze OSC a seconda della configurazione
* Se le sequenze di escape appaiono come testo letterale come `\e]8;;`, usa `printf '%b'` invece di `echo -e` per una gestione più affidabile degli escape

**Glitch di visualizzazione con sequenze di escape**

* Le sequenze di escape complesse (colori ANSI, link OSC 8) possono occasionalmente causare output corrotto se si sovrappongono ad altri aggiornamenti dell'interfaccia utente
* Se vedi testo corrotto, prova a semplificare il tuo script in output di testo semplice
* Le barre di stato multi-riga con codici di escape sono più soggette a problemi di rendering rispetto al testo semplice su una sola riga

**Fiducia nell'area di lavoro richiesta**

* Il comando della barra di stato viene eseguito solo se hai accettato la finestra di dialogo di fiducia dell'area di lavoro per la directory corrente. Poiché `statusLine` esegue un comando di shell, richiede la stessa accettazione di fiducia di hook e altre impostazioni che eseguono shell.
* Se la fiducia non è accettata, vedrai la notifica `statusline skipped · restart to fix` invece dell'output della tua barra di stato. Riavvia Claude Code e accetta il prompt di fiducia per abilitarla.

**Errori di script o blocchi**

* Gli script che escono con codici diversi da zero o non producono output causano il vuoto della barra di stato
* Gli script lenti bloccano l'aggiornamento della barra di stato fino al completamento. Mantieni gli script veloci per evitare output obsoleto.
* Se un nuovo aggiornamento si attiva mentre uno script lento è in esecuzione, lo script in corso viene annullato
* Testa il tuo script indipendentemente con input simulato prima di configurarlo

**Le notifiche condividono la riga della barra di stato**

* Le notifiche di sistema come errori del server MCP, aggiornamenti automatici e avvisi di token vengono visualizzate sul lato destro della stessa riga della tua barra di stato
* L'abilitazione della modalità verbose aggiunge un contatore di token a questa area
* Su terminali stretti, queste notifiche potrebbero troncare l'output della tua barra di stato
