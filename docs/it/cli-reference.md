> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Riferimento CLI

> Riferimento completo per l'interfaccia da riga di comando di Claude Code, inclusi comandi e flag.

## Comandi CLI

Puoi avviare sessioni, inviare contenuti tramite pipe, riprendere conversazioni e gestire gli aggiornamenti con questi comandi:

| Comando                         | Descrizione                                                                                                                                                                                                | Esempio                                            |
| :------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `claude`                        | Avvia sessione interattiva                                                                                                                                                                                 | `claude`                                           |
| `claude "query"`                | Avvia sessione interattiva con prompt iniziale                                                                                                                                                             | `claude "explain this project"`                    |
| `claude -p "query"`             | Esegui query tramite SDK, quindi esci                                                                                                                                                                      | `claude -p "explain this function"`                |
| `cat file \| claude -p "query"` | Elabora contenuto inviato tramite pipe                                                                                                                                                                     | `cat logs.txt \| claude -p "explain"`              |
| `claude -c`                     | Continua la conversazione più recente nella directory corrente                                                                                                                                             | `claude -c`                                        |
| `claude -c -p "query"`          | Continua tramite SDK                                                                                                                                                                                       | `claude -c -p "Check for type errors"`             |
| `claude -r "<session>" "query"` | Riprendi sessione per ID o nome                                                                                                                                                                            | `claude -r "auth-refactor" "Finish this PR"`       |
| `claude update`                 | Aggiorna alla versione più recente                                                                                                                                                                         | `claude update`                                    |
| `claude auth login`             | Accedi al tuo account Anthropic. Usa `--email` per pre-compilare il tuo indirizzo email e `--sso` per forzare l'autenticazione SSO                                                                         | `claude auth login --email user@example.com --sso` |
| `claude auth logout`            | Esci dal tuo account Anthropic                                                                                                                                                                             | `claude auth logout`                               |
| `claude auth status`            | Mostra lo stato di autenticazione come JSON. Usa `--text` per output leggibile dall'uomo. Esce con codice 0 se connesso, 1 se no                                                                           | `claude auth status`                               |
| `claude agents`                 | Elenca tutti i [subagents](/it/sub-agents) configurati, raggruppati per fonte                                                                                                                              | `claude agents`                                    |
| `claude mcp`                    | Configura i server Model Context Protocol (MCP)                                                                                                                                                            | Vedi la [documentazione Claude Code MCP](/it/mcp). |
| `claude remote-control`         | Avvia una [sessione Remote Control](/it/remote-control) per controllare Claude Code da Claude.ai o dall'app Claude mentre è in esecuzione localmente. Vedi [Remote Control](/it/remote-control) per i flag | `claude remote-control`                            |

## Flag CLI

Personalizza il comportamento di Claude Code con questi flag da riga di comando:

| Flag                                   | Descrizione                                                                                                                                                                                                                                  | Esempio                                                                                            |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `--add-dir`                            | Aggiungi directory di lavoro aggiuntive per l'accesso di Claude (convalida che ogni percorso esista come directory)                                                                                                                          | `claude --add-dir ../apps ../lib`                                                                  |
| `--agent`                              | Specifica un agente per la sessione corrente (sostituisce l'impostazione `agent`)                                                                                                                                                            | `claude --agent my-custom-agent`                                                                   |
| `--agents`                             | Definisci [subagents](/it/sub-agents) personalizzati dinamicamente tramite JSON (vedi sotto per il formato)                                                                                                                                  | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allow-dangerously-skip-permissions` | Abilita il bypass dei permessi come opzione senza attivarlo immediatamente. Consente di comporre con `--permission-mode` (usa con cautela)                                                                                                   | `claude --permission-mode plan --allow-dangerously-skip-permissions`                               |
| `--allowedTools`                       | Strumenti che si eseguono senza richiedere il permesso. Vedi [sintassi della regola di permesso](/it/settings#permission-rule-syntax) per la corrispondenza dei pattern. Per limitare quali strumenti sono disponibili, usa `--tools` invece | `"Bash(git log *)" "Bash(git diff *)" "Read"`                                                      |
| `--append-system-prompt`               | Aggiungi testo personalizzato alla fine del prompt di sistema predefinito                                                                                                                                                                    | `claude --append-system-prompt "Always use TypeScript"`                                            |
| `--append-system-prompt-file`          | Carica testo di prompt di sistema aggiuntivo da un file e aggiungi al prompt predefinito                                                                                                                                                     | `claude --append-system-prompt-file ./extra-rules.txt`                                             |
| `--betas`                              | Intestazioni beta da includere nelle richieste API (solo utenti con chiave API)                                                                                                                                                              | `claude --betas interleaved-thinking`                                                              |
| `--chrome`                             | Abilita [integrazione del browser Chrome](/it/chrome) per l'automazione web e i test                                                                                                                                                         | `claude --chrome`                                                                                  |
| `--continue`, `-c`                     | Carica la conversazione più recente nella directory corrente                                                                                                                                                                                 | `claude --continue`                                                                                |
| `--dangerously-skip-permissions`       | Salta tutti i prompt di permesso (usa con cautela)                                                                                                                                                                                           | `claude --dangerously-skip-permissions`                                                            |
| `--debug`                              | Abilita la modalità debug con filtro di categoria opzionale (ad esempio, `"api,hooks"` o `"!statsig,!file"`)                                                                                                                                 | `claude --debug "api,mcp"`                                                                         |
| `--disable-slash-commands`             | Disabilita tutti gli skills e i comandi per questa sessione                                                                                                                                                                                  | `claude --disable-slash-commands`                                                                  |
| `--disallowedTools`                    | Strumenti che vengono rimossi dal contesto del modello e non possono essere utilizzati                                                                                                                                                       | `"Bash(git log *)" "Bash(git diff *)" "Edit"`                                                      |
| `--fallback-model`                     | Abilita il fallback automatico al modello specificato quando il modello predefinito è sovraccarico (solo modalità print)                                                                                                                     | `claude -p --fallback-model sonnet "query"`                                                        |
| `--fork-session`                       | Quando riprendi, crea un nuovo ID di sessione invece di riutilizzare l'originale (usa con `--resume` o `--continue`)                                                                                                                         | `claude --resume abc123 --fork-session`                                                            |
| `--from-pr`                            | Riprendi sessioni collegate a una PR GitHub specifica. Accetta un numero di PR o un URL. Le sessioni vengono collegate automaticamente quando create tramite `gh pr create`                                                                  | `claude --from-pr 123`                                                                             |
| `--ide`                                | Connettiti automaticamente all'IDE all'avvio se esattamente un IDE valido è disponibile                                                                                                                                                      | `claude --ide`                                                                                     |
| `--init`                               | Esegui gli hook di inizializzazione e avvia la modalità interattiva                                                                                                                                                                          | `claude --init`                                                                                    |
| `--init-only`                          | Esegui gli hook di inizializzazione e esci (nessuna sessione interattiva)                                                                                                                                                                    | `claude --init-only`                                                                               |
| `--include-partial-messages`           | Includi gli eventi di streaming parziale nell'output (richiede `--print` e `--output-format=stream-json`)                                                                                                                                    | `claude -p --output-format stream-json --include-partial-messages "query"`                         |
| `--input-format`                       | Specifica il formato di input per la modalità print (opzioni: `text`, `stream-json`)                                                                                                                                                         | `claude -p --output-format json --input-format stream-json`                                        |
| `--json-schema`                        | Ottieni output JSON convalidato corrispondente a uno JSON Schema dopo che l'agente completa il suo flusso di lavoro (solo modalità print, vedi [structured outputs](https://platform.claude.com/docs/en/agent-sdk/structured-outputs))       | `claude -p --json-schema '{"type":"object","properties":{...}}' "query"`                           |
| `--maintenance`                        | Esegui gli hook di manutenzione e esci                                                                                                                                                                                                       | `claude --maintenance`                                                                             |
| `--max-budget-usd`                     | Importo massimo in dollari da spendere nelle chiamate API prima di fermarsi (solo modalità print)                                                                                                                                            | `claude -p --max-budget-usd 5.00 "query"`                                                          |
| `--max-turns`                          | Limita il numero di turni agentici (solo modalità print). Esce con un errore quando il limite viene raggiunto. Nessun limite per impostazione predefinita                                                                                    | `claude -p --max-turns 3 "query"`                                                                  |
| `--mcp-config`                         | Carica i server MCP da file JSON o stringhe (separati da spazi)                                                                                                                                                                              | `claude --mcp-config ./mcp.json`                                                                   |
| `--model`                              | Imposta il modello per la sessione corrente con un alias per il modello più recente (`sonnet` o `opus`) o il nome completo di un modello                                                                                                     | `claude --model claude-sonnet-4-6`                                                                 |
| `--no-chrome`                          | Disabilita [integrazione del browser Chrome](/it/chrome) per questa sessione                                                                                                                                                                 | `claude --no-chrome`                                                                               |
| `--no-session-persistence`             | Disabilita la persistenza della sessione in modo che le sessioni non vengano salvate su disco e non possano essere riprese (solo modalità print)                                                                                             | `claude -p --no-session-persistence "query"`                                                       |
| `--output-format`                      | Specifica il formato di output per la modalità print (opzioni: `text`, `json`, `stream-json`)                                                                                                                                                | `claude -p "query" --output-format json`                                                           |
| `--permission-mode`                    | Inizia in una [modalità di permesso](/it/permissions#permission-modes) specificata                                                                                                                                                           | `claude --permission-mode plan`                                                                    |
| `--permission-prompt-tool`             | Specifica uno strumento MCP per gestire i prompt di permesso in modalità non interattiva                                                                                                                                                     | `claude -p --permission-prompt-tool mcp_auth_tool "query"`                                         |
| `--plugin-dir`                         | Carica i plugin da directory per questa sessione solo (ripetibile)                                                                                                                                                                           | `claude --plugin-dir ./my-plugins`                                                                 |
| `--print`, `-p`                        | Stampa la risposta senza modalità interattiva (vedi [documentazione Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) per i dettagli di utilizzo programmatico)                                                             | `claude -p "query"`                                                                                |
| `--remote`                             | Crea una nuova [sessione web](/it/claude-code-on-the-web) su claude.ai con la descrizione dell'attività fornita                                                                                                                              | `claude --remote "Fix the login bug"`                                                              |
| `--resume`, `-r`                       | Riprendi una sessione specifica per ID o nome, o mostra un selettore interattivo per scegliere una sessione                                                                                                                                  | `claude --resume auth-refactor`                                                                    |
| `--session-id`                         | Usa un ID di sessione specifico per la conversazione (deve essere un UUID valido)                                                                                                                                                            | `claude --session-id "550e8400-e29b-41d4-a716-446655440000"`                                       |
| `--setting-sources`                    | Elenco separato da virgole delle fonti di impostazioni da caricare (`user`, `project`, `local`)                                                                                                                                              | `claude --setting-sources user,project`                                                            |
| `--settings`                           | Percorso di un file JSON di impostazioni o una stringa JSON da cui caricare impostazioni aggiuntive                                                                                                                                          | `claude --settings ./settings.json`                                                                |
| `--strict-mcp-config`                  | Usa solo i server MCP da `--mcp-config`, ignorando tutte le altre configurazioni MCP                                                                                                                                                         | `claude --strict-mcp-config --mcp-config ./mcp.json`                                               |
| `--system-prompt`                      | Sostituisci l'intero prompt di sistema con testo personalizzato                                                                                                                                                                              | `claude --system-prompt "You are a Python expert"`                                                 |
| `--system-prompt-file`                 | Carica il prompt di sistema da un file, sostituendo il prompt predefinito                                                                                                                                                                    | `claude --system-prompt-file ./custom-prompt.txt`                                                  |
| `--teleport`                           | Riprendi una [sessione web](/it/claude-code-on-the-web) nel tuo terminale locale                                                                                                                                                             | `claude --teleport`                                                                                |
| `--teammate-mode`                      | Imposta come i compagni di squadra dell'[agent team](/it/agent-teams) vengono visualizzati: `auto` (predefinito), `in-process`, o `tmux`. Vedi [configurare agent teams](/it/agent-teams#set-up-agent-teams)                                 | `claude --teammate-mode in-process`                                                                |
| `--tools`                              | Limita quali strumenti integrati Claude può utilizzare. Usa `""` per disabilitare tutti, `"default"` per tutti, o nomi di strumenti come `"Bash,Edit,Read"`                                                                                  | `claude --tools "Bash,Edit,Read"`                                                                  |
| `--verbose`                            | Abilita la registrazione dettagliata, mostra l'output completo turno per turno                                                                                                                                                               | `claude --verbose`                                                                                 |
| `--version`, `-v`                      | Restituisce il numero di versione                                                                                                                                                                                                            | `claude -v`                                                                                        |
| `--worktree`, `-w`                     | Avvia Claude in un [git worktree](/it/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) isolato in `<repo>/.claude/worktrees/<name>`. Se non viene fornito alcun nome, uno viene generato automaticamente               | `claude -w feature-auth`                                                                           |

<Tip>
  Il flag `--output-format json` è particolarmente utile per lo scripting e
  l'automazione, consentendoti di analizzare le risposte di Claude a livello di programmazione.
</Tip>

### Formato del flag agents

Il flag `--agents` accetta un oggetto JSON che definisce uno o più subagents personalizzati. Ogni subagent richiede un nome univoco (come chiave) e un oggetto di definizione con i seguenti campi:

| Campo             | Obbligatorio | Descrizione                                                                                                                                                                                                                                    |
| :---------------- | :----------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `description`     | Sì           | Descrizione in linguaggio naturale di quando il subagent dovrebbe essere invocato                                                                                                                                                              |
| `prompt`          | Sì           | Il prompt di sistema che guida il comportamento del subagent                                                                                                                                                                                   |
| `tools`           | No           | Array di strumenti specifici che il subagent può utilizzare, ad esempio `["Read", "Edit", "Bash"]`. Se omesso, eredita tutti gli strumenti. Supporta la sintassi [`Agent(agent_type)`](/it/sub-agents#restrict-which-subagents-can-be-spawned) |
| `disallowedTools` | No           | Array di nomi di strumenti da negare esplicitamente per questo subagent                                                                                                                                                                        |
| `model`           | No           | Alias del modello da utilizzare: `sonnet`, `opus`, `haiku`, o `inherit`. Se omesso, per impostazione predefinita è `inherit`                                                                                                                   |
| `skills`          | No           | Array di nomi di [skill](/it/skills) da precaricare nel contesto del subagent                                                                                                                                                                  |
| `mcpServers`      | No           | Array di [MCP servers](/it/mcp) per questo subagent. Ogni voce è una stringa del nome del server o un oggetto `{name: config}`                                                                                                                 |
| `maxTurns`        | No           | Numero massimo di turni agentici prima che il subagent si fermi                                                                                                                                                                                |

Esempio:

```bash  theme={null}
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

Per ulteriori dettagli sulla creazione e l'utilizzo di subagents, vedi la [documentazione dei subagents](/it/sub-agents).

### Flag del prompt di sistema

Claude Code fornisce quattro flag per personalizzare il prompt di sistema. Tutti e quattro funzionano sia in modalità interattiva che non interattiva.

| Flag                          | Comportamento                                            | Caso d'uso                                                                            |
| :---------------------------- | :------------------------------------------------------- | :------------------------------------------------------------------------------------ |
| `--system-prompt`             | **Sostituisce** l'intero prompt predefinito              | Controllo completo sul comportamento e le istruzioni di Claude                        |
| `--system-prompt-file`        | **Sostituisce** con il contenuto del file                | Carica i prompt dai file per la riproducibilità e il controllo della versione         |
| `--append-system-prompt`      | **Aggiunge** al prompt predefinito                       | Aggiungi istruzioni specifiche mantenendo il comportamento predefinito di Claude Code |
| `--append-system-prompt-file` | **Aggiunge** il contenuto del file al prompt predefinito | Carica istruzioni aggiuntive dai file mantenendo i valori predefiniti                 |

**Quando usare ciascuno:**

* **`--system-prompt`**: usa quando hai bisogno di un controllo completo sul prompt di sistema di Claude. Questo rimuove tutte le istruzioni predefinite di Claude Code, dandoti una lavagna pulita.
  ```bash  theme={null}
  claude --system-prompt "You are a Python expert who only writes type-annotated code"
  ```

* **`--system-prompt-file`**: usa quando vuoi caricare un prompt personalizzato da un file, utile per la coerenza del team o per i modelli di prompt controllati dalla versione.
  ```bash  theme={null}
  claude --system-prompt-file ./prompts/code-review.txt
  ```

* **`--append-system-prompt`**: usa quando vuoi aggiungere istruzioni specifiche mantenendo intatte le capacità predefinite di Claude Code. Questa è l'opzione più sicura per la maggior parte dei casi d'uso.
  ```bash  theme={null}
  claude --append-system-prompt "Always use TypeScript and include JSDoc comments"
  ```

* **`--append-system-prompt-file`**: usa quando vuoi aggiungere istruzioni da un file mantenendo i valori predefiniti di Claude Code. Utile per le aggiunte controllate dalla versione.
  ```bash  theme={null}
  claude --append-system-prompt-file ./prompts/style-rules.txt
  ```

`--system-prompt` e `--system-prompt-file` si escludono a vicenda. I flag di aggiunta possono essere utilizzati insieme a uno dei flag di sostituzione.

Per la maggior parte dei casi d'uso, `--append-system-prompt` o `--append-system-prompt-file` è consigliato poiché preservano le capacità integrate di Claude Code mentre aggiungono i tuoi requisiti personalizzati. Usa `--system-prompt` o `--system-prompt-file` solo quando hai bisogno di un controllo completo sul prompt di sistema.

## Vedi anche

* [Estensione Chrome](/it/chrome) - Automazione del browser e test web
* [Modalità interattiva](/it/interactive-mode) - Scorciatoie, modalità di input e funzionalità interattive
* [Guida di avvio rapido](/it/quickstart) - Introduzione a Claude Code
* [Flussi di lavoro comuni](/it/common-workflows) - Flussi di lavoro e pattern avanzati
* [Impostazioni](/it/settings) - Opzioni di configurazione
* [Documentazione Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) - Utilizzo programmatico e integrazioni
