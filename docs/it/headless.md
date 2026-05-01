> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Eseguire Claude Code a livello programmatico

> Utilizza l'Agent SDK per eseguire Claude Code a livello programmatico dalla CLI, Python o TypeScript.

L'[Agent SDK](/it/agent-sdk/overview) ti fornisce gli stessi strumenti, il ciclo dell'agente e la gestione del contesto che alimentano Claude Code. È disponibile come CLI per script e CI/CD, oppure come pacchetti [Python](/it/agent-sdk/python) e [TypeScript](/it/agent-sdk/typescript) per il controllo programmatico completo.

<Note>
  La CLI era precedentemente chiamata "headless mode". Il flag `-p` e tutte le opzioni CLI funzionano allo stesso modo.
</Note>

Per eseguire Claude Code a livello programmatico dalla CLI, passa `-p` con il tuo prompt e qualsiasi [opzione CLI](/it/cli-reference):

```bash theme={null}
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

Questa pagina copre l'utilizzo dell'Agent SDK tramite la CLI (`claude -p`). Per i pacchetti SDK Python e TypeScript con output strutturati, callback di approvazione degli strumenti e oggetti messaggio nativi, consulta la [documentazione completa dell'Agent SDK](/it/agent-sdk/overview).

## Utilizzo di base

Aggiungi il flag `-p` (o `--print`) a qualsiasi comando `claude` per eseguirlo in modo non interattivo. Tutte le [opzioni CLI](/it/cli-reference) funzionano con `-p`, incluse:

* `--continue` per [continuare le conversazioni](#continue-conversations)
* `--allowedTools` per [approvare automaticamente gli strumenti](#auto-approve-tools)
* `--output-format` per [ottenere output strutturato](#get-structured-output)

Questo esempio chiede a Claude una domanda sulla tua base di codice e stampa la risposta:

```bash theme={null}
claude -p "What does the auth module do?"
```

### Inizia più velocemente con la modalità bare

Aggiungi `--bare` per ridurre il tempo di avvio saltando l'auto-discovery di hooks, skills, plugins, server MCP, memoria automatica e CLAUDE.md. Senza di esso, `claude -p` carica lo stesso [contesto](/it/how-claude-code-works#the-context-window) che una sessione interattiva avrebbe, incluso tutto ciò che è configurato nella directory di lavoro o in `~/.claude`.

La modalità bare è utile per CI e script dove hai bisogno dello stesso risultato su ogni macchina. Un hook nel `~/.claude` di un collega o un server MCP nel `.mcp.json` del progetto non verranno eseguiti, perché la modalità bare non li legge mai. Solo i flag che passi esplicitamente hanno effetto.

Questo esempio esegue un'attività di riepilogo una tantum in modalità bare e pre-approva lo strumento Read in modo che la chiamata si completi senza un prompt di autorizzazione:

```bash theme={null}
claude --bare -p "Summarize this file" --allowedTools "Read"
```

In modalità bare Claude ha accesso agli strumenti Bash, lettura file e modifica file. Passa qualsiasi contesto di cui hai bisogno con un flag:

| Per caricare                  | Utilizza                                                |
| ----------------------------- | ------------------------------------------------------- |
| Aggiunte al prompt di sistema | `--append-system-prompt`, `--append-system-prompt-file` |
| Impostazioni                  | `--settings <file-or-json>`                             |
| Server MCP                    | `--mcp-config <file-or-json>`                           |
| Agenti personalizzati         | `--agents <json>`                                       |
| Una directory plugin          | `--plugin-dir <path>`                                   |

La modalità bare salta le letture OAuth e keychain. L'autenticazione Anthropic deve provenire da `ANTHROPIC_API_KEY` o da un `apiKeyHelper` nel JSON passato a `--settings`. Bedrock, Vertex e Foundry utilizzano le loro credenziali provider usuali.

<Note>
  `--bare` è la modalità consigliata per le chiamate con script e SDK, e diventerà l'impostazione predefinita per `-p` in una versione futura.
</Note>

## Esempi

Questi esempi evidenziano i modelli CLI comuni. Per CI e altre chiamate con script, aggiungi [`--bare`](#start-faster-with-bare-mode) in modo che non raccolgano qualsiasi cosa sia configurata localmente.

### Ottenere output strutturato

Utilizza `--output-format` per controllare come vengono restituite le risposte:

* `text` (predefinito): output di testo semplice
* `json`: JSON strutturato con risultato, ID sessione e metadati
* `stream-json`: JSON delimitato da newline per lo streaming in tempo reale

Questo esempio restituisce un riepilogo del progetto come JSON con metadati della sessione, con il risultato del testo nel campo `result`:

```bash theme={null}
claude -p "Summarize this project" --output-format json
```

Per ottenere output conforme a uno schema specifico, utilizza `--output-format json` con `--json-schema` e una definizione [JSON Schema](https://json-schema.org/). La risposta include metadati sulla richiesta (ID sessione, utilizzo, ecc.) con l'output strutturato nel campo `structured_output`.

Questo esempio estrae i nomi delle funzioni e li restituisce come array di stringhe:

```bash theme={null}
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

<Tip>
  Utilizza uno strumento come [jq](https://jqlang.github.io/jq/) per analizzare la risposta ed estrarre campi specifici:

  ```bash theme={null}
  # Extract the text result
  claude -p "Summarize this project" --output-format json | jq -r '.result'

  # Extract structured output
  claude -p "Extract function names from auth.py" \
    --output-format json \
    --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
    | jq '.structured_output'
  ```
</Tip>

### Streaming delle risposte

Utilizza `--output-format stream-json` con `--verbose` e `--include-partial-messages` per ricevere i token mentre vengono generati. Ogni riga è un oggetto JSON che rappresenta un evento:

```bash theme={null}
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

L'esempio seguente utilizza [jq](https://jqlang.github.io/jq/) per filtrare i delta di testo e visualizzare solo il testo in streaming. Il flag `-r` restituisce stringhe non elaborate (senza virgolette) e `-j` si unisce senza newline in modo che i token fluiscano continuamente:

```bash theme={null}
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

Quando una richiesta API non riesce con un errore ritentabile, Claude Code emette un evento `system/api_retry` prima di ritentare. Puoi utilizzarlo per visualizzare il progresso del tentativo o implementare una logica di backoff personalizzata.

| Campo            | Tipo           | Descrizione                                                                                                                                                               |
| ---------------- | -------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`           | `"system"`     | tipo di messaggio                                                                                                                                                         |
| `subtype`        | `"api_retry"`  | identifica questo come un evento di tentativo                                                                                                                             |
| `attempt`        | integer        | numero del tentativo corrente, a partire da 1                                                                                                                             |
| `max_retries`    | integer        | tentativi totali consentiti                                                                                                                                               |
| `retry_delay_ms` | integer        | millisecondi fino al prossimo tentativo                                                                                                                                   |
| `error_status`   | integer o null | codice di stato HTTP, o `null` per errori di connessione senza risposta HTTP                                                                                              |
| `error`          | string         | categoria di errore: `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `rate_limit`, `invalid_request`, `server_error`, `max_output_tokens`, o `unknown` |
| `uuid`           | string         | identificatore evento univoco                                                                                                                                             |
| `session_id`     | string         | sessione a cui appartiene l'evento                                                                                                                                        |

L'evento `system/init` segnala i metadati della sessione inclusi il modello, gli strumenti, i server MCP e i plugin caricati. È il primo evento nel flusso a meno che [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/it/env-vars) non sia impostato, nel qual caso gli eventi `plugin_install` lo precedono. Utilizza i campi plugin per far fallire CI quando un plugin non è stato caricato:

| Campo           | Tipo  | Descrizione                                                                                                                                                                                                                                 |
| --------------- | ----- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plugins`       | array | plugin che sono stati caricati con successo, ognuno con `name` e `path`                                                                                                                                                                     |
| `plugin_errors` | array | errori di caricamento del plugin come una versione di dipendenza non soddisfatta, ognuno con `plugin`, `type` e `message`. I plugin interessati vengono declassati e assenti da `plugins`. La chiave viene omessa quando non ci sono errori |

Quando [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/it/env-vars) è impostato, Claude Code emette eventi `system/plugin_install` mentre i plugin del marketplace si installano prima del primo turno. Utilizza questi per visualizzare il progresso dell'installazione nella tua interfaccia utente.

| Campo        | Tipo                                                    | Descrizione                                                                                                             |
| ------------ | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `type`       | `"system"`                                              | tipo di messaggio                                                                                                       |
| `subtype`    | `"plugin_install"`                                      | identifica questo come un evento di installazione plugin                                                                |
| `status`     | `"started"`, `"installed"`, `"failed"`, o `"completed"` | `started` e `completed` racchiudono l'installazione complessiva; `installed` e `failed` segnalano i singoli marketplace |
| `name`       | string, opzionale                                       | nome del marketplace, presente su `installed` e `failed`                                                                |
| `error`      | string, opzionale                                       | messaggio di errore, presente su `failed`                                                                               |
| `uuid`       | string                                                  | identificatore evento univoco                                                                                           |
| `session_id` | string                                                  | sessione a cui appartiene l'evento                                                                                      |

Per lo streaming programmatico con callback e oggetti messaggio, consulta [Stream responses in real-time](/it/agent-sdk/streaming-output) nella documentazione dell'Agent SDK.

### Approvare automaticamente gli strumenti

Utilizza `--allowedTools` per consentire a Claude di utilizzare determinati strumenti senza chiedere. Questo esempio esegue una suite di test e corregge i guasti, consentendo a Claude di eseguire comandi Bash e leggere/modificare file senza chiedere il permesso:

```bash theme={null}
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

Per impostare una linea di base per l'intera sessione invece di elencare i singoli strumenti, passa una [modalità di autorizzazione](/it/permission-modes). `dontAsk` nega qualsiasi cosa non sia nelle tue regole `permissions.allow` o nel [set di comandi di sola lettura](/it/permissions#read-only-commands), utile per esecuzioni CI bloccate. `acceptEdits` consente a Claude di scrivere file senza chiedere e approva automaticamente anche i comandi del filesystem comuni come `mkdir`, `touch`, `mv` e `cp`. Gli altri comandi shell e le richieste di rete hanno ancora bisogno di una voce `--allowedTools` o di una regola `permissions.allow`, altrimenti l'esecuzione si interrompe quando uno viene tentato:

```bash theme={null}
claude -p "Apply the lint fixes" --permission-mode acceptEdits
```

### Creare un commit

Questo esempio esamina le modifiche in staging e crea un commit con un messaggio appropriato:

```bash theme={null}
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

Il flag `--allowedTools` utilizza la [sintassi delle regole di autorizzazione](/it/settings#permission-rule-syntax). Lo spazio finale ` *` abilita la corrispondenza dei prefissi, quindi `Bash(git diff *)` consente qualsiasi comando che inizia con `git diff`. Lo spazio prima di `*` è importante: senza di esso, `Bash(git diff*)` corrisponderebbe anche a `git diff-index`.

<Note>
  Le [skills](/it/skills) richiamate dall'utente come `/commit` e i [comandi incorporati](/it/commands) sono disponibili solo in modalità interattiva. In modalità `-p`, descrivi invece l'attività che desideri completare.
</Note>

### Personalizzare il prompt di sistema

Utilizza `--append-system-prompt` per aggiungere istruzioni mantenendo il comportamento predefinito di Claude Code. Questo esempio invia un diff PR a Claude e gli istruisce di esaminarlo per vulnerabilità di sicurezza:

```bash theme={null}
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

Consulta i [flag del prompt di sistema](/it/cli-reference#system-prompt-flags) per ulteriori opzioni incluso `--system-prompt` per sostituire completamente il prompt predefinito.

### Continuare le conversazioni

Utilizza `--continue` per continuare la conversazione più recente, oppure `--resume` con un ID sessione per continuare una conversazione specifica. Questo esempio esegue una revisione, quindi invia prompt di follow-up:

```bash theme={null}
# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

Se stai eseguendo più conversazioni, acquisisci l'ID sessione per riprendere una specifica:

```bash theme={null}
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

## Passaggi successivi

* [Agent SDK quickstart](/it/agent-sdk/quickstart): costruisci il tuo primo agente con Python o TypeScript
* [CLI reference](/it/cli-reference): tutti i flag e le opzioni CLI
* [GitHub Actions](/it/github-actions): utilizza l'Agent SDK nei flussi di lavoro GitHub
* [GitLab CI/CD](/it/gitlab-ci-cd): utilizza l'Agent SDK nelle pipeline GitLab
