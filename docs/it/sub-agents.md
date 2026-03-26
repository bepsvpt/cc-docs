> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Creare subagent personalizzati

> Creare e utilizzare subagent AI specializzati in Claude Code per flussi di lavoro specifici di attività e una migliore gestione del contesto.

I subagent sono assistenti AI specializzati che gestiscono tipi specifici di attività. Ogni subagent viene eseguito nella propria finestra di contesto con un prompt di sistema personalizzato, accesso a strumenti specifici e autorizzazioni indipendenti. Quando Claude incontra un'attività che corrisponde alla descrizione di un subagent, la delega a quel subagent, che lavora in modo indipendente e restituisce i risultati.

<Note>
  Se hai bisogno di più agenti che lavorano in parallelo e comunicano tra loro, consulta invece [agent teams](/it/agent-teams). I subagent lavorano all'interno di una singola sessione; i team di agenti coordinano tra sessioni separate.
</Note>

I subagent ti aiutano a:

* **Preservare il contesto** mantenendo l'esplorazione e l'implementazione fuori dalla tua conversazione principale
* **Applicare vincoli** limitando quali strumenti un subagent può utilizzare
* **Riutilizzare configurazioni** tra progetti con subagent a livello utente
* **Specializzare il comportamento** con prompt di sistema focalizzati per domini specifici
* **Controllare i costi** instradando le attività a modelli più veloci e economici come Haiku

Claude utilizza la descrizione di ogni subagent per decidere quando delegare le attività. Quando crei un subagent, scrivi una descrizione chiara in modo che Claude sappia quando utilizzarlo.

Claude Code include diversi subagent integrati come **Explore**, **Plan** e **general-purpose**. Puoi anche creare subagent personalizzati per gestire attività specifiche. Questa pagina copre i [subagent integrati](#built-in-subagents), [come creare i tuoi](#quickstart-create-your-first-subagent), [opzioni di configurazione complete](#configure-subagents), [modelli per lavorare con i subagent](#work-with-subagents) e [subagent di esempio](#example-subagents).

## Subagent integrati

Claude Code include subagent integrati che Claude utilizza automaticamente quando appropriato. Ognuno eredita le autorizzazioni della conversazione principale con restrizioni di strumenti aggiuntive.

<Tabs>
  <Tab title="Explore">
    Un agente veloce e di sola lettura ottimizzato per la ricerca e l'analisi delle basi di codice.

    * **Model**: Haiku (veloce, bassa latenza)
    * **Tools**: Strumenti di sola lettura (accesso negato agli strumenti Write e Edit)
    * **Purpose**: Scoperta di file, ricerca di codice, esplorazione della base di codice

    Claude delega a Explore quando ha bisogno di cercare o comprendere una base di codice senza apportare modifiche. Questo mantiene i risultati dell'esplorazione fuori dal contesto della tua conversazione principale.

    Quando invoca Explore, Claude specifica un livello di accuratezza: **quick** per ricerche mirate, **medium** per esplorazione equilibrata, o **very thorough** per analisi completa.
  </Tab>

  <Tab title="Plan">
    Un agente di ricerca utilizzato durante la [plan mode](/it/common-workflows#use-plan-mode-for-safe-code-analysis) per raccogliere contesto prima di presentare un piano.

    * **Model**: Eredita dalla conversazione principale
    * **Tools**: Strumenti di sola lettura (accesso negato agli strumenti Write e Edit)
    * **Purpose**: Ricerca della base di codice per la pianificazione

    Quando sei in plan mode e Claude ha bisogno di comprendere la tua base di codice, delega la ricerca al subagent Plan. Questo previene l'annidamento infinito (i subagent non possono generare altri subagent) mentre raccoglie comunque il contesto necessario.
  </Tab>

  <Tab title="General-purpose">
    Un agente capace per attività complesse e multi-step che richiedono sia esplorazione che azione.

    * **Model**: Eredita dalla conversazione principale
    * **Tools**: Tutti gli strumenti
    * **Purpose**: Ricerca complessa, operazioni multi-step, modifiche del codice

    Claude delega a general-purpose quando l'attività richiede sia esplorazione che modifica, ragionamento complesso per interpretare i risultati, o più step dipendenti.
  </Tab>

  <Tab title="Other">
    Claude Code include agenti helper aggiuntivi per attività specifiche. Questi vengono generalmente invocati automaticamente, quindi non hai bisogno di utilizzarli direttamente.

    | Agent             | Model   | Quando Claude lo utilizza                                         |
    | :---------------- | :------ | :---------------------------------------------------------------- |
    | Bash              | Eredita | Esecuzione di comandi terminali in un contesto separato           |
    | statusline-setup  | Sonnet  | Quando esegui `/statusline` per configurare la tua linea di stato |
    | Claude Code Guide | Haiku   | Quando fai domande sulle funzionalità di Claude Code              |
  </Tab>
</Tabs>

Oltre a questi subagent integrati, puoi creare i tuoi con prompt personalizzati, restrizioni di strumenti, modalità di autorizzazione, hooks e skills. Le sezioni seguenti mostrano come iniziare e personalizzare i subagent.

## Quickstart: crea il tuo primo subagent

I subagent sono definiti in file Markdown con frontmatter YAML. Puoi [crearli manualmente](#write-subagent-files) o utilizzare il comando `/agents`.

Questa procedura ti guida attraverso la creazione di un subagent a livello utente con il comando `/agents`. Il subagent esamina il codice e suggerisce miglioramenti per la base di codice.

<Steps>
  <Step title="Apri l'interfaccia dei subagent">
    In Claude Code, esegui:

    ```text  theme={null}
    /agents
    ```
  </Step>

  <Step title="Scegli una posizione">
    Seleziona **Create new agent**, quindi scegli **Personal**. Questo salva il subagent in `~/.claude/agents/` in modo che sia disponibile in tutti i tuoi progetti.
  </Step>

  <Step title="Genera con Claude">
    Seleziona **Generate with Claude**. Quando richiesto, descrivi il subagent:

    ```text  theme={null}
    A code improvement agent that scans files and suggests improvements
    for readability, performance, and best practices. It should explain
    each issue, show the current code, and provide an improved version.
    ```

    Claude genera l'identificatore, la descrizione e il prompt di sistema per te.
  </Step>

  <Step title="Seleziona gli strumenti">
    Per un revisore di sola lettura, deseleziona tutto tranne **Read-only tools**. Se mantieni tutti gli strumenti selezionati, il subagent eredita tutti gli strumenti disponibili per la conversazione principale.
  </Step>

  <Step title="Seleziona il modello">
    Scegli quale modello utilizza il subagent. Per questo agente di esempio, seleziona **Sonnet**, che bilancia capacità e velocità per analizzare i modelli di codice.
  </Step>

  <Step title="Scegli un colore">
    Scegli un colore di sfondo per il subagent. Questo ti aiuta a identificare quale subagent è in esecuzione nell'interfaccia utente.
  </Step>

  <Step title="Configura la memoria">
    Seleziona **User scope** per dare al subagent una [directory di memoria persistente](#enable-persistent-memory) in `~/.claude/agent-memory/`. Il subagent utilizza questo per accumulare intuizioni tra le conversazioni, come modelli di base di codice e problemi ricorrenti. Seleziona **None** se non vuoi che il subagent persista gli insegnamenti.
  </Step>

  <Step title="Salva e provalo">
    Esamina il riepilogo della configurazione. Premi `s` o `Enter` per salvare, oppure premi `e` per salvare e modificare il file nel tuo editor. Il subagent è disponibile immediatamente. Provalo:

    ```text  theme={null}
    Use the code-improver agent to suggest improvements in this project
    ```

    Claude delega al tuo nuovo subagent, che scansiona la base di codice e restituisce suggerimenti di miglioramento.
  </Step>
</Steps>

Ora hai un subagent che puoi utilizzare in qualsiasi progetto sulla tua macchina per analizzare le basi di codice e suggerire miglioramenti.

Puoi anche creare subagent manualmente come file Markdown, definirli tramite flag CLI, o distribuirli tramite plugin. Le sezioni seguenti coprono tutte le opzioni di configurazione.

## Configura i subagent

### Usa il comando /agents

Il comando `/agents` fornisce un'interfaccia interattiva per gestire i subagent. Esegui `/agents` per:

* Visualizzare tutti i subagent disponibili (integrati, utente, progetto e plugin)
* Creare nuovi subagent con configurazione guidata o generazione Claude
* Modificare la configurazione del subagent esistente e l'accesso agli strumenti
* Eliminare subagent personalizzati
* Vedere quali subagent sono attivi quando esistono duplicati

Questo è il modo consigliato per creare e gestire i subagent. Per la creazione manuale o l'automazione, puoi anche aggiungere file subagent direttamente.

Per elencare tutti i subagent configurati dalla riga di comando senza avviare una sessione interattiva, esegui `claude agents`. Questo mostra gli agenti raggruppati per fonte e indica quali sono sovrascritti da definizioni di priorità più alta.

### Scegli l'ambito del subagent

I subagent sono file Markdown con frontmatter YAML. Archiviali in posizioni diverse a seconda dell'ambito. Quando più subagent condividono lo stesso nome, la posizione con priorità più alta vince.

| Location                       | Scope                      | Priority    | Come creare                           |
| :----------------------------- | :------------------------- | :---------- | :------------------------------------ |
| Flag CLI `--agents`            | Sessione corrente          | 1 (massima) | Passa JSON quando avvii Claude Code   |
| `.claude/agents/`              | Progetto corrente          | 2           | Interattivo o manuale                 |
| `~/.claude/agents/`            | Tutti i tuoi progetti      | 3           | Interattivo o manuale                 |
| Directory `agents/` del plugin | Dove il plugin è abilitato | 4 (minima)  | Installato con [plugins](/it/plugins) |

I **subagent di progetto** (`.claude/agents/`) sono ideali per subagent specifici di una base di codice. Archiviali nel controllo della versione in modo che il tuo team possa utilizzarli e migliorarli in modo collaborativo.

I **subagent utente** (`~/.claude/agents/`) sono subagent personali disponibili in tutti i tuoi progetti.

I **subagent definiti da CLI** vengono passati come JSON quando avvii Claude Code. Esistono solo per quella sessione e non vengono salvati su disco, rendendoli utili per test rapidi o script di automazione. Puoi definire più subagent in una singola chiamata `--agents`:

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

Il flag `--agents` accetta JSON con gli stessi campi [frontmatter](#supported-frontmatter-fields) dei subagent basati su file: `description`, `prompt`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background` e `isolation`. Usa `prompt` per il prompt di sistema, equivalente al corpo markdown nei subagent basati su file.

I **subagent plugin** provengono da [plugins](/it/plugins) che hai installato. Appaiono in `/agents` insieme ai tuoi subagent personalizzati. Consulta il [riferimento dei componenti plugin](/it/plugins-reference#agents) per i dettagli sulla creazione di subagent plugin.

<Note>
  Per motivi di sicurezza, i subagent plugin non supportano i campi frontmatter `hooks`, `mcpServers` o `permissionMode`. Questi campi vengono ignorati durante il caricamento degli agenti da un plugin. Se ne hai bisogno, copia il file dell'agente in `.claude/agents/` o `~/.claude/agents/`. Puoi anche aggiungere regole a [`permissions.allow`](/it/settings#permission-settings) in `settings.json` o `settings.local.json`, ma queste regole si applicano all'intera sessione, non solo al subagent plugin.
</Note>

### Scrivi file subagent

I file subagent utilizzano frontmatter YAML per la configurazione, seguito dal prompt di sistema in Markdown:

<Note>
  I subagent vengono caricati all'avvio della sessione. Se crei un subagent aggiungendo manualmente un file, riavvia la tua sessione o usa `/agents` per caricarlo immediatamente.
</Note>

```markdown  theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

Il frontmatter definisce i metadati e la configurazione del subagent. Il corpo diventa il prompt di sistema che guida il comportamento del subagent. I subagent ricevono solo questo prompt di sistema (più dettagli di base sull'ambiente come la directory di lavoro), non il prompt di sistema completo di Claude Code.

#### Campi frontmatter supportati

I seguenti campi possono essere utilizzati nel frontmatter YAML. Solo `name` e `description` sono obbligatori.

| Field             | Required | Description                                                                                                                                                                                                                                                                                                    |
| :---------------- | :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | Yes      | Identificatore univoco utilizzando lettere minuscole e trattini                                                                                                                                                                                                                                                |
| `description`     | Yes      | Quando Claude dovrebbe delegare a questo subagent                                                                                                                                                                                                                                                              |
| `tools`           | No       | [Strumenti](#available-tools) che il subagent può utilizzare. Eredita tutti gli strumenti se omesso                                                                                                                                                                                                            |
| `disallowedTools` | No       | Strumenti da negare, rimossi dall'elenco ereditato o specificato                                                                                                                                                                                                                                               |
| `model`           | No       | [Modello](#choose-a-model) da utilizzare: `sonnet`, `opus`, `haiku`, un ID modello completo (ad esempio, `claude-opus-4-6`), o `inherit`. Predefinito: `inherit`                                                                                                                                               |
| `permissionMode`  | No       | [Modalità di autorizzazione](#permission-modes): `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, o `plan`                                                                                                                                                                                            |
| `maxTurns`        | No       | Numero massimo di turni agentici prima che il subagent si fermi                                                                                                                                                                                                                                                |
| `skills`          | No       | [Skills](/it/skills) da caricare nel contesto del subagent all'avvio. Il contenuto completo della skill viene iniettato, non solo reso disponibile per l'invocazione. I subagent non ereditano skills dalla conversazione principale                                                                           |
| `mcpServers`      | No       | [MCP servers](/it/mcp) disponibili per questo subagent. Ogni voce è un nome di server che fa riferimento a un server già configurato (ad esempio, `"slack"`) o una definizione inline con il nome del server come chiave e una [configurazione MCP server](/it/mcp#configure-mcp-servers) completa come valore |
| `hooks`           | No       | [Lifecycle hooks](#define-hooks-for-subagents) limitati a questo subagent                                                                                                                                                                                                                                      |
| `memory`          | No       | [Ambito di memoria persistente](#enable-persistent-memory): `user`, `project`, o `local`. Abilita l'apprendimento tra sessioni                                                                                                                                                                                 |
| `background`      | No       | Imposta su `true` per eseguire sempre questo subagent come [background task](#run-subagents-in-foreground-or-background). Predefinito: `false`                                                                                                                                                                 |
| `effort`          | No       | Livello di sforzo quando questo subagent è attivo. Sostituisce il livello di sforzo della sessione. Predefinito: eredita dalla sessione. Opzioni: `low`, `medium`, `high`, `max` (solo Opus 4.6)                                                                                                               |
| `isolation`       | No       | Imposta su `worktree` per eseguire il subagent in un [git worktree](/it/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) temporaneo, dandogli una copia isolata del repository. Il worktree viene automaticamente pulito se il subagent non apporta modifiche                            |
| `initialPrompt`   | No       | Auto-inviato come primo turno utente quando questo agente viene eseguito come agente della sessione principale (tramite `--agent` o l'impostazione `agent`). [Commands](/it/commands) e [skills](/it/skills) vengono elaborati. Anteposto a qualsiasi prompt fornito dall'utente                               |

### Scegli un modello

Il campo `model` controlla quale [modello AI](/it/model-config) utilizza il subagent:

* **Alias modello**: Usa uno degli alias disponibili: `sonnet`, `opus`, o `haiku`
* **ID modello completo**: Usa un ID modello completo come `claude-opus-4-6` o `claude-sonnet-4-6`. Accetta gli stessi valori del flag `--model`
* **inherit**: Usa lo stesso modello della conversazione principale
* **Omesso**: Se non specificato, predefinito a `inherit` (usa lo stesso modello della conversazione principale)

Quando Claude invoca un subagent, può anche passare un parametro `model` per quella specifica invocazione. Claude Code risolve il modello del subagent in questo ordine:

1. La variabile di ambiente [`CLAUDE_CODE_SUBAGENT_MODEL`](/it/model-config#environment-variables), se impostata
2. Il parametro `model` per invocazione
3. Il frontmatter `model` della definizione del subagent
4. Il modello della conversazione principale

### Controlla le capacità del subagent

Puoi controllare cosa possono fare i subagent attraverso l'accesso agli strumenti, le modalità di autorizzazione e le regole condizionali.

#### Strumenti disponibili

I subagent possono utilizzare qualsiasi [strumento interno](/it/tools-reference) di Claude Code. Per impostazione predefinita, i subagent ereditano tutti gli strumenti dalla conversazione principale, inclusi gli strumenti MCP.

Per limitare gli strumenti, usa il campo `tools` (allowlist) o il campo `disallowedTools` (denylist). Questo esempio usa `tools` per consentire esclusivamente Read, Grep, Glob e Bash. Il subagent non può modificare file, scrivere file o utilizzare alcuno strumento MCP:

```yaml  theme={null}
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

Questo esempio usa `disallowedTools` per ereditare ogni strumento dalla conversazione principale tranne Write e Edit. Il subagent mantiene Bash, strumenti MCP e tutto il resto:

```yaml  theme={null}
---
name: no-writes
description: Inherits every tool except file writes
disallowedTools: Write, Edit
---
```

Se entrambi sono impostati, `disallowedTools` viene applicato per primo, quindi `tools` viene risolto rispetto al pool rimanente. Uno strumento elencato in entrambi viene rimosso.

#### Limita quali subagent possono essere generati

Quando un agente viene eseguito come thread principale con `claude --agent`, può generare subagent utilizzando lo strumento Agent. Per limitare quali tipi di subagent può generare, usa la sintassi `Agent(agent_type)` nel campo `tools`.

<Note>Nella versione 2.1.63, lo strumento Task è stato rinominato in Agent. I riferimenti `Task(...)` esistenti nelle impostazioni e nelle definizioni degli agenti continuano a funzionare come alias.</Note>

```yaml  theme={null}
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

Questo è un allowlist: solo i subagent `worker` e `researcher` possono essere generati. Se l'agente tenta di generare qualsiasi altro tipo, la richiesta fallisce e l'agente vede solo i tipi consentiti nel suo prompt. Per bloccare agenti specifici mentre consenti tutti gli altri, usa [`permissions.deny`](#disable-specific-subagents) invece.

Per consentire la generazione di qualsiasi subagent senza restrizioni, usa `Agent` senza parentesi:

```yaml  theme={null}
tools: Agent, Read, Bash
```

Se `Agent` è completamente omesso dall'elenco `tools`, l'agente non può generare alcun subagent. Questa restrizione si applica solo agli agenti eseguiti come thread principale con `claude --agent`. I subagent non possono generare altri subagent, quindi `Agent(agent_type)` non ha effetto nelle definizioni dei subagent.

#### Limita i server MCP a un subagent

Usa il campo `mcpServers` per dare a un subagent accesso ai server [MCP](/it/mcp) che non sono disponibili nella conversazione principale. I server inline definiti qui vengono connessi quando il subagent inizia e disconnessi quando finisce. I riferimenti stringa condividono la connessione della sessione principale.

Ogni voce nell'elenco è una definizione di server inline o una stringa che fa riferimento a un server MCP già configurato nella tua sessione:

```yaml  theme={null}
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.
```

Le definizioni inline utilizzano lo stesso schema delle voci del server `.mcp.json` (`stdio`, `http`, `sse`, `ws`), con chiave il nome del server.

Per mantenere un server MCP fuori dalla conversazione principale e evitare che le descrizioni dei suoi strumenti consumino contesto lì, definiscilo inline qui piuttosto che in `.mcp.json`. Il subagent ottiene gli strumenti; la conversazione principale no.

#### Modalità di autorizzazione

Il campo `permissionMode` controlla come il subagent gestisce i prompt di autorizzazione. I subagent ereditano il contesto di autorizzazione dalla conversazione principale e possono sovrascrivere la modalità, tranne quando la modalità principale ha la precedenza come descritto di seguito.

| Mode                | Behavior                                                                                             |
| :------------------ | :--------------------------------------------------------------------------------------------------- |
| `default`           | Controllo di autorizzazione standard con prompt                                                      |
| `acceptEdits`       | Auto-accetta modifiche ai file                                                                       |
| `dontAsk`           | Auto-nega prompt di autorizzazione (gli strumenti esplicitamente consentiti continuano a funzionare) |
| `bypassPermissions` | Salta i prompt di autorizzazione                                                                     |
| `plan`              | Plan mode (esplorazione di sola lettura)                                                             |

<Warning>
  Usa `bypassPermissions` con cautela. Salta i prompt di autorizzazione, consentendo al subagent di eseguire operazioni senza approvazione. Le scritture nelle directory `.git`, `.claude`, `.vscode` e `.idea` continuano a richiedere conferma, tranne per `.claude/commands`, `.claude/agents` e `.claude/skills`. Consulta [permission modes](/it/permission-modes#skip-all-checks-with-bypasspermissions-mode) per i dettagli.
</Warning>

Se il principale utilizza `bypassPermissions`, questo ha la precedenza e non può essere sovrascritto. Se il principale utilizza [auto mode](/it/permission-modes#eliminate-prompts-with-auto-mode), il subagent eredita auto mode e qualsiasi `permissionMode` nel suo frontmatter viene ignorato: il classificatore valuta le chiamate di strumenti del subagent con le stesse regole di blocco e consentimento della sessione principale.

#### Precarica skills nei subagent

Usa il campo `skills` per iniettare il contenuto della skill nel contesto del subagent all'avvio. Questo dà al subagent conoscenza del dominio senza richiedere che scopra e carichi le skills durante l'esecuzione.

```yaml  theme={null}
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

Il contenuto completo di ogni skill viene iniettato nel contesto del subagent, non solo reso disponibile per l'invocazione. I subagent non ereditano skills dalla conversazione principale; devi elencarle esplicitamente.

<Note>
  Questo è l'inverso di [eseguire una skill in un subagent](/it/skills#run-skills-in-a-subagent). Con `skills` in un subagent, il subagent controlla il prompt di sistema e carica il contenuto della skill. Con `context: fork` in una skill, il contenuto della skill viene iniettato nell'agente che specifichi. Entrambi utilizzano lo stesso sistema sottostante.
</Note>

#### Abilita memoria persistente

Il campo `memory` dà al subagent una directory persistente che sopravvive tra le conversazioni. Il subagent utilizza questa directory per costruire conoscenza nel tempo, come modelli di base di codice, intuizioni di debug e decisioni architettoniche.

```yaml  theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

Scegli un ambito in base a quanto ampiamente la memoria dovrebbe applicarsi:

| Scope     | Location                                      | Usa quando                                                                                                         |
| :-------- | :-------------------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `user`    | `~/.claude/agent-memory/<name-of-agent>/`     | il subagent dovrebbe ricordare gli insegnamenti tra tutti i progetti                                               |
| `project` | `.claude/agent-memory/<name-of-agent>/`       | la conoscenza del subagent è specifica del progetto e condivisibile tramite controllo della versione               |
| `local`   | `.claude/agent-memory-local/<name-of-agent>/` | la conoscenza del subagent è specifica del progetto ma non dovrebbe essere archiviata nel controllo della versione |

Quando la memoria è abilitata:

* Il prompt di sistema del subagent include istruzioni per leggere e scrivere nella directory di memoria.
* Il prompt di sistema del subagent include anche le prime 200 righe di `MEMORY.md` nella directory di memoria, con istruzioni per curare `MEMORY.md` se supera 200 righe.
* Gli strumenti Read, Write e Edit vengono automaticamente abilitati in modo che il subagent possa gestire i suoi file di memoria.

##### Suggerimenti per la memoria persistente

* `project` è l'ambito predefinito consigliato. Lo rende condivisibile tramite controllo della versione. Usa `user` quando la conoscenza del subagent è ampiamente applicabile tra progetti, o `local` quando la conoscenza non dovrebbe essere archiviata nel controllo della versione.
* Chiedi al subagent di consultare la sua memoria prima di iniziare il lavoro: "Review this PR, and check your memory for patterns you've seen before."
* Chiedi al subagent di aggiornare la sua memoria dopo aver completato un'attività: "Now that you're done, save what you learned to your memory." Nel tempo, questo costruisce una base di conoscenza che rende il subagent più efficace.
* Includi istruzioni di memoria direttamente nel file markdown del subagent in modo che mantenga proattivamente la sua stessa base di conoscenza:

  ```markdown  theme={null}
  Update your agent memory as you discover codepaths, patterns, library
  locations, and key architectural decisions. This builds up institutional
  knowledge across conversations. Write concise notes about what you found
  and where.
  ```

#### Regole condizionali con hooks

Per un controllo più dinamico sull'utilizzo degli strumenti, usa gli hook `PreToolUse` per convalidare le operazioni prima che vengano eseguite. Questo è utile quando hai bisogno di consentire alcune operazioni di uno strumento mentre ne blocchi altre.

Questo esempio crea un subagent che consente solo query di database di sola lettura. L'hook `PreToolUse` esegue lo script specificato in `command` prima di ogni comando Bash:

```yaml  theme={null}
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

Claude Code [passa l'input dell'hook come JSON](/it/hooks#pretooluse-input) tramite stdin ai comandi dell'hook. Lo script di convalida legge questo JSON, estrae il comando Bash e [esce con codice 2](/it/hooks#exit-code-2-behavior-per-event) per bloccare le operazioni di scrittura:

```bash  theme={null}
#!/bin/bash
# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

Consulta [Hook input](/it/hooks#pretooluse-input) per lo schema di input completo e [exit codes](/it/hooks#exit-code-output) per come i codici di uscita influenzano il comportamento.

#### Disabilita subagent specifici

Puoi impedire a Claude di utilizzare subagent specifici aggiungendoli all'array `deny` nelle tue [impostazioni](/it/settings#permission-settings). Usa il formato `Agent(subagent-name)` dove `subagent-name` corrisponde al campo name del subagent.

```json  theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

Questo funziona sia per i subagent integrati che personalizzati. Puoi anche usare il flag CLI `--disallowedTools`:

```bash  theme={null}
claude --disallowedTools "Agent(Explore)"
```

Consulta la [documentazione Permissions](/it/permissions#tool-specific-permission-rules) per più dettagli sulle regole di autorizzazione.

### Definisci hook per i subagent

I subagent possono definire [hook](/it/hooks) che vengono eseguiti durante il ciclo di vita del subagent. Ci sono due modi per configurare gli hook:

1. **Nel frontmatter del subagent**: Definisci hook che vengono eseguiti solo mentre quel subagent è attivo
2. **In `settings.json`**: Definisci hook che vengono eseguiti nella sessione principale quando i subagent iniziano o si fermano

#### Hook nel frontmatter del subagent

Definisci gli hook direttamente nel file markdown del subagent. Questi hook vengono eseguiti solo mentre quel subagent specifico è attivo e vengono puliti quando finisce.

Tutti gli [hook events](/it/hooks#hook-events) sono supportati. Gli eventi più comuni per i subagent sono:

| Event         | Matcher input        | Quando si attiva                                                     |
| :------------ | :------------------- | :------------------------------------------------------------------- |
| `PreToolUse`  | Nome dello strumento | Prima che il subagent utilizzi uno strumento                         |
| `PostToolUse` | Nome dello strumento | Dopo che il subagent ha utilizzato uno strumento                     |
| `Stop`        | (nessuno)            | Quando il subagent finisce (convertito in `SubagentStop` al runtime) |

Questo esempio convalida i comandi Bash con l'hook `PreToolUse` ed esegue un linter dopo le modifiche ai file con `PostToolUse`:

```yaml  theme={null}
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

Gli hook `Stop` nel frontmatter vengono automaticamente convertiti in eventi `SubagentStop`.

#### Hook a livello di progetto per gli eventi dei subagent

Configura gli hook in `settings.json` che rispondono agli eventi del ciclo di vita dei subagent nella sessione principale.

| Event           | Matcher input           | Quando si attiva                       |
| :-------------- | :---------------------- | :------------------------------------- |
| `SubagentStart` | Nome del tipo di agente | Quando un subagent inizia l'esecuzione |
| `SubagentStop`  | Nome del tipo di agente | Quando un subagent completa            |

Entrambi gli eventi supportano matcher per indirizzare tipi di agenti specifici per nome. Questo esempio esegue uno script di configurazione solo quando il subagent `db-agent` inizia e uno script di pulizia quando qualsiasi subagent si ferma:

```json  theme={null}
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

Consulta [Hooks](/it/hooks) per il formato di configurazione dell'hook completo.

## Lavora con i subagent

### Comprendi la delegazione automatica

Claude delega automaticamente le attività in base alla descrizione dell'attività nella tua richiesta, al campo `description` nelle configurazioni dei subagent e al contesto attuale. Per incoraggiare la delegazione proattiva, includi frasi come "use proactively" nel campo description del tuo subagent.

### Invoca i subagent esplicitamente

Quando la delegazione automatica non è sufficiente, puoi richiedere un subagent tu stesso. Tre modelli escalation da un suggerimento una tantum a un predefinito a livello di sessione:

* **Linguaggio naturale**: nomina il subagent nel tuo prompt; Claude decide se delegare
* **@-mention**: garantisce che il subagent viene eseguito per un'attività
* **A livello di sessione**: l'intera sessione utilizza il prompt di sistema, le restrizioni di strumenti e il modello di quel subagent tramite il flag `--agent` o l'impostazione `agent`

Per il linguaggio naturale, non c'è sintassi speciale. Nomina il subagent e Claude generalmente delega:

```text  theme={null}
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

**@-mention il subagent.** Digita `@` e scegli il subagent dal typeahead, nello stesso modo in cui @-mention i file. Questo assicura che quel subagent specifico viene eseguito piuttosto che lasciare la scelta a Claude:

```text  theme={null}
@"code-reviewer (agent)" look at the auth changes
```

Il tuo messaggio completo va ancora a Claude, che scrive il prompt dell'attività del subagent in base a quello che hai chiesto. L'@-mention controlla quale subagent Claude invoca, non quale prompt riceve.

I subagent forniti da un [plugin](/it/plugins) abilitato appaiono nel typeahead come `<plugin-name>:<agent-name>`. Puoi anche digitare la mention manualmente senza usare il picker: `@agent-<name>` per i subagent locali, o `@agent-<plugin-name>:<agent-name>` per i subagent plugin.

**Esegui l'intera sessione come un subagent.** Passa [`--agent <name>`](/it/cli-reference) per avviare una sessione in cui il thread principale stesso assume il prompt di sistema, le restrizioni di strumenti e il modello di quel subagent:

```bash  theme={null}
claude --agent code-reviewer
```

Il prompt di sistema del subagent sostituisce completamente il prompt di sistema predefinito di Claude Code, nello stesso modo in cui [`--system-prompt`](/it/cli-reference) fa. I file `CLAUDE.md` e la memoria del progetto continuano a caricarsi attraverso il flusso di messaggi normale. Il nome dell'agente appare come `@<name>` nell'intestazione di avvio in modo che tu possa confermare che è attivo.

Questo funziona con i subagent integrati e personalizzati, e la scelta persiste quando riprendi la sessione.

Per un subagent fornito da un plugin, passa il nome con ambito: `claude --agent <plugin-name>:<agent-name>`.

Per renderlo il predefinito per ogni sessione in un progetto, imposta `agent` in `.claude/settings.json`:

```json  theme={null}
{
  "agent": "code-reviewer"
}
```

Il flag CLI sostituisce l'impostazione se entrambi sono presenti.

### Esegui i subagent in primo piano o in background

I subagent possono essere eseguiti in primo piano (bloccante) o in background (concorrente):

* **Subagent in primo piano** bloccano la conversazione principale fino al completamento. I prompt di autorizzazione e le domande di chiarimento (come [`AskUserQuestion`](/it/tools-reference)) vengono passati a te.
* **Subagent in background** vengono eseguiti contemporaneamente mentre continui a lavorare. Prima di avviare, Claude Code richiede le autorizzazioni di strumenti di cui il subagent avrà bisogno, assicurando che abbia le approvazioni necessarie in anticipo. Una volta in esecuzione, il subagent eredita queste autorizzazioni e auto-nega qualsiasi cosa non pre-approvata. Se un subagent in background ha bisogno di fare domande di chiarimento, quella chiamata di strumento fallisce ma il subagent continua.

Se un subagent in background fallisce a causa di autorizzazioni mancanti, puoi avviare un nuovo subagent in primo piano con lo stesso compito per riprovare con prompt interattivi.

Claude decide se eseguire i subagent in primo piano o in background in base all'attività. Puoi anche:

* Chiedere a Claude di "run this in the background"
* Premere **Ctrl+B** per mettere in background un'attività in esecuzione

Per disabilitare tutta la funzionalità di background task, imposta la variabile di ambiente `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` su `1`. Consulta [Environment variables](/it/env-vars).

### Modelli comuni

#### Isola operazioni ad alto volume

Uno degli usi più efficaci per i subagent è isolare le operazioni che producono grandi quantità di output. L'esecuzione di test, il recupero della documentazione o l'elaborazione di file di log possono consumare contesto significativo. Delegando questi a un subagent, l'output dettagliato rimane nel contesto del subagent mentre solo il riassunto rilevante ritorna alla tua conversazione principale.

```text  theme={null}
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### Esegui ricerca parallela

Per indagini indipendenti, genera più subagent per lavorare simultaneamente:

```text  theme={null}
Research the authentication, database, and API modules in parallel using separate subagents
```

Ogni subagent esplora la sua area in modo indipendente, quindi Claude sintetizza i risultati. Questo funziona meglio quando i percorsi di ricerca non dipendono l'uno dall'altro.

<Warning>
  Quando i subagent completano, i loro risultati ritornano alla tua conversazione principale. L'esecuzione di molti subagent che ognuno restituisce risultati dettagliati può consumare contesto significativo.
</Warning>

Per attività che necessitano di parallelismo sostenuto o superano la tua finestra di contesto, [agent teams](/it/agent-teams) danno a ogni worker il suo contesto indipendente.

#### Concatena i subagent

Per flussi di lavoro multi-step, chiedi a Claude di utilizzare i subagent in sequenza. Ogni subagent completa la sua attività e restituisce i risultati a Claude, che poi passa il contesto rilevante al subagent successivo.

```text  theme={null}
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Scegli tra subagent e conversazione principale

Usa la **conversazione principale** quando:

* L'attività necessita di frequenti scambi o raffinamento iterativo
* Più fasi condividono contesto significativo (pianificazione → implementazione → test)
* Stai facendo un cambio rapido e mirato
* La latenza è importante. I subagent iniziano da zero e potrebbero aver bisogno di tempo per raccogliere contesto

Usa **subagent** quando:

* L'attività produce output dettagliato che non hai bisogno nel tuo contesto principale
* Vuoi applicare restrizioni di strumenti o autorizzazioni specifiche
* Il lavoro è autonomo e può restituire un riassunto

Considera [Skills](/it/skills) invece quando vuoi prompt o flussi di lavoro riutilizzabili che vengono eseguiti nel contesto della conversazione principale piuttosto che nel contesto isolato del subagent.

Per una domanda rapida su qualcosa già nella tua conversazione, usa [`/btw`](/it/interactive-mode#side-questions-with-btw) invece di un subagent. Vede il tuo contesto completo ma non ha accesso agli strumenti e la risposta viene scartata piuttosto che aggiunta alla cronologia.

<Note>
  I subagent non possono generare altri subagent. Se il tuo flusso di lavoro richiede delegazione annidata, usa [Skills](/it/skills) o [concatena i subagent](#chain-subagents) dalla conversazione principale.
</Note>

### Gestisci il contesto del subagent

#### Riprendi i subagent

Ogni invocazione di subagent crea una nuova istanza con contesto fresco. Per continuare il lavoro di un subagent esistente invece di ricominciare, chiedi a Claude di riprendere.

I subagent ripresi mantengono la loro cronologia di conversazione completa, incluse tutte le precedenti chiamate di strumenti, risultati e ragionamento. Il subagent riprende esattamente da dove si era fermato piuttosto che ricominciare da zero.

Quando un subagent completa, Claude riceve il suo ID agente. Claude utilizza lo strumento `SendMessage` con l'ID dell'agente come campo `to` per riprendere. Per riprendere un subagent, chiedi a Claude di continuare il lavoro precedente:

```text  theme={null}
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

Puoi anche chiedere a Claude l'ID agente se vuoi fare riferimento ad esso esplicitamente, o trovare gli ID nei file di trascrizione in `~/.claude/projects/{project}/{sessionId}/subagents/`. Ogni trascrizione è archiviata come `agent-{agentId}.jsonl`.

Le trascrizioni dei subagent persistono indipendentemente dalla conversazione principale:

* **Compattazione della conversazione principale**: Quando la conversazione principale si compatta, le trascrizioni dei subagent non sono interessate. Sono archiviate in file separati.
* **Persistenza della sessione**: Le trascrizioni dei subagent persistono all'interno della loro sessione. Puoi [riprendere un subagent](#resume-subagents) dopo aver riavviato Claude Code riprendendo la stessa sessione.
* **Pulizia automatica**: Le trascrizioni vengono pulite in base all'impostazione `cleanupPeriodDays` (predefinito: 30 giorni).

#### Auto-compattazione

I subagent supportano la compattazione automatica utilizzando la stessa logica della conversazione principale. Per impostazione predefinita, la compattazione automatica si attiva a circa il 95% della capacità. Per attivare la compattazione prima, imposta `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` su una percentuale inferiore (ad esempio, `50`). Consulta [environment variables](/it/env-vars) per i dettagli.

Gli eventi di compattazione vengono registrati nei file di trascrizione dei subagent:

```json  theme={null}
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}
```

Il valore `preTokens` mostra quanti token sono stati utilizzati prima che si verificasse la compattazione.

## Subagent di esempio

Questi esempi dimostrano modelli efficaci per la costruzione di subagent. Usali come punti di partenza, o genera una versione personalizzata con Claude.

<Tip>
  **Best practices:**

  * **Progetta subagent focalizzati:** ogni subagent dovrebbe eccellere in un'attività specifica
  * **Scrivi descrizioni dettagliate:** Claude utilizza la descrizione per decidere quando delegare
  * **Limita l'accesso agli strumenti:** concedi solo le autorizzazioni necessarie per la sicurezza e la focalizzazione
  * **Archivia nel controllo della versione:** condividi i subagent di progetto con il tuo team
</Tip>

### Revisore di codice

Un subagent di sola lettura che esamina il codice senza modificarlo. Questo esempio mostra come progettare un subagent focalizzato con accesso limitato agli strumenti (nessun Edit o Write) e un prompt dettagliato che specifica esattamente cosa cercare e come formattare l'output.

```markdown  theme={null}
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### Debugger

Un subagent che può sia analizzare che correggere i problemi. A differenza del revisore di codice, questo include Edit perché correggere i bug richiede la modifica del codice. Il prompt fornisce un flusso di lavoro chiaro dalla diagnosi alla verifica.

```markdown  theme={null}
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### Data scientist

Un subagent specifico del dominio per il lavoro di analisi dei dati. Questo esempio mostra come creare subagent per flussi di lavoro specializzati al di fuori dei tipici compiti di codifica. Imposta esplicitamente `model: sonnet` per un'analisi più capace.

```markdown  theme={null}
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

### Validatore di query di database

Un subagent che consente l'accesso a Bash ma convalida i comandi per consentire solo query SQL di sola lettura. Questo esempio mostra come usare gli hook `PreToolUse` per la convalida condizionale quando hai bisogno di un controllo più fine di quello che il campo `tools` fornisce.

```markdown  theme={null}
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.
```

Claude Code [passa l'input dell'hook come JSON](/it/hooks#pretooluse-input) tramite stdin ai comandi dell'hook. Lo script di convalida legge questo JSON, estrae il comando in esecuzione e lo controlla rispetto a un elenco di operazioni di scrittura SQL. Se viene rilevata un'operazione di scrittura, lo script [esce con codice 2](/it/hooks#exit-code-2-behavior-per-event) per bloccare l'esecuzione e restituisce un messaggio di errore a Claude tramite stderr.

Crea lo script di convalida in qualsiasi punto del tuo progetto. Il percorso deve corrispondere al campo `command` nella tua configurazione dell'hook:

```bash  theme={null}
#!/bin/bash
# Blocks SQL write operations, allows SELECT queries

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0
```

Rendi lo script eseguibile:

```bash  theme={null}
chmod +x ./scripts/validate-readonly-query.sh
```

L'hook riceve JSON tramite stdin con il comando Bash in `tool_input.command`. Il codice di uscita 2 blocca l'operazione e alimenta il messaggio di errore a Claude. Consulta [Hooks](/it/hooks#exit-code-output) per i dettagli sui codici di uscita e [Hook input](/it/hooks#pretooluse-input) per lo schema di input completo.

## Passaggi successivi

Ora che comprendi i subagent, esplora queste funzionalità correlate:

* [Distribuisci subagent con i plugin](/it/plugins) per condividere i subagent tra team o progetti
* [Esegui Claude Code a livello di programmazione](/it/headless) con l'Agent SDK per CI/CD e automazione
* [Usa i server MCP](/it/mcp) per dare ai subagent accesso a strumenti e dati esterni
