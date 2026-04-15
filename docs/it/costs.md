> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Gestisci i costi in modo efficace

> Traccia l'utilizzo dei token, imposta i limiti di spesa del team e riduci i costi di Claude Code con la gestione del contesto, la selezione del modello, le impostazioni del pensiero esteso e gli hook di pre-elaborazione.

Claude Code consuma token per ogni interazione. I costi variano in base alle dimensioni della codebase, alla complessità della query e alla lunghezza della conversazione. Il costo medio è di \$6 per sviluppatore al giorno, con costi giornalieri che rimangono al di sotto di \$12 per il 90% degli utenti.

Per l'utilizzo del team, Claude Code addebita il consumo di token API. In media, Claude Code costa circa \$100-200 per sviluppatore al mese con Sonnet 4.6, anche se c'è una grande varianza a seconda di quante istanze gli utenti stanno eseguendo e se la stanno utilizzando nell'automazione.

Questa pagina spiega come [tracciare i tuoi costi](#track-your-costs), [gestire i costi per i team](#managing-costs-for-teams) e [ridurre l'utilizzo dei token](#reduce-token-usage).

## Traccia i tuoi costi

### Utilizzo del comando `/cost`

<Note>
  Il comando `/cost` mostra l'utilizzo dei token API ed è destinato agli utenti API. I sottoscrittori di Claude Max e Pro hanno l'utilizzo incluso nel loro abbonamento, quindi i dati di `/cost` non sono rilevanti per scopi di fatturazione. I sottoscrittori possono utilizzare `/stats` per visualizzare i modelli di utilizzo.
</Note>

Il comando `/cost` fornisce statistiche dettagliate sull'utilizzo dei token per la tua sessione attuale:

```text theme={null}
Total cost:            $0.55
Total duration (API):  6m 19.7s
Total duration (wall): 6h 33m 10.2s
Total code changes:    0 lines added, 0 lines removed
```

## Gestione dei costi per i team

Quando utilizzi Claude API, puoi [impostare i limiti di spesa dell'area di lavoro](https://platform.claude.com/docs/it/build-with-claude/workspaces#workspace-limits) sulla spesa totale dell'area di lavoro di Claude Code. Gli amministratori possono [visualizzare i rapporti di costo e utilizzo](https://platform.claude.com/docs/it/build-with-claude/workspaces#usage-and-cost-tracking) nella Console.

<Note>
  Quando autentichi per la prima volta Claude Code con il tuo account Claude Console, viene creata automaticamente un'area di lavoro chiamata "Claude Code". Questa area di lavoro fornisce il tracciamento e la gestione centralizzati dei costi per tutto l'utilizzo di Claude Code nella tua organizzazione. Non puoi creare chiavi API per questa area di lavoro; è esclusivamente per l'autenticazione e l'utilizzo di Claude Code.
</Note>

Su Bedrock, Vertex e Foundry, Claude Code non invia metriche dal tuo cloud. Per ottenere metriche di costo, diversi grandi enterprise hanno riferito di utilizzare [LiteLLM](/it/llm-gateway#litellm-configuration), uno strumento open-source che aiuta le aziende a [tracciare la spesa per chiave](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend). Questo progetto non è affiliato ad Anthropic e non è stato sottoposto a audit di sicurezza.

### Raccomandazioni sui limiti di velocità

Quando configuri Claude Code per i team, considera queste raccomandazioni Token Per Minuto (TPM) e Richieste Per Minuto (RPM) per utente in base alle dimensioni della tua organizzazione:

| Dimensione del team | TPM per utente | RPM per utente |
| ------------------- | -------------- | -------------- |
| 1-5 utenti          | 200k-300k      | 5-7            |
| 5-20 utenti         | 100k-150k      | 2.5-3.5        |
| 20-50 utenti        | 50k-75k        | 1.25-1.75      |
| 50-100 utenti       | 25k-35k        | 0.62-0.87      |
| 100-500 utenti      | 15k-20k        | 0.37-0.47      |
| 500+ utenti         | 10k-15k        | 0.25-0.35      |

Ad esempio, se hai 200 utenti, potresti richiedere 20k TPM per ogni utente, o 4 milioni di TPM totali (200\*20.000 = 4 milioni).

Il TPM per utente diminuisce man mano che le dimensioni del team crescono perché meno utenti tendono a utilizzare Claude Code contemporaneamente nelle organizzazioni più grandi. Questi limiti di velocità si applicano a livello organizzativo, non per singolo utente, il che significa che i singoli utenti possono temporaneamente consumare più della loro quota calcolata quando altri non stanno utilizzando attivamente il servizio.

<Note>
  Se prevedi scenari con utilizzo concorrente insolitamente elevato (come sessioni di formazione dal vivo con grandi gruppi), potresti aver bisogno di allocazioni TPM più elevate per utente.
</Note>

### Costi dei token del team di agenti

I [team di agenti](/it/agent-teams) generano più istanze di Claude Code, ognuna con la propria finestra di contesto. L'utilizzo dei token si ridimensiona con il numero di compagni di squadra attivi e per quanto tempo ognuno viene eseguito.

Per mantenere i costi del team di agenti gestibili:

* Utilizza Sonnet per i compagni di squadra. Bilancia la capacità e il costo per i compiti di coordinamento.
* Mantieni i team piccoli. Ogni compagno di squadra esegue la propria finestra di contesto, quindi l'utilizzo dei token è approssimativamente proporzionale alle dimensioni del team.
* Mantieni i prompt di generazione focalizzati. I compagni di squadra caricano automaticamente CLAUDE.md, i server MCP e le skills, ma tutto nel prompt di generazione si aggiunge al loro contesto dall'inizio.
* Pulisci i team quando il lavoro è terminato. I compagni di squadra attivi continuano a consumare token anche se inattivi.
* I team di agenti sono disabilitati per impostazione predefinita. Imposta `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` nel tuo [settings.json](/it/settings) o nell'ambiente per abilitarli. Vedi [abilita i team di agenti](/it/agent-teams#enable-agent-teams).

## Riduci l'utilizzo dei token

I costi dei token si ridimensionano con la dimensione del contesto: più contesto Claude elabora, più token utilizzi. Claude Code ottimizza automaticamente i costi attraverso il prompt caching (che riduce i costi per il contenuto ripetuto come i prompt di sistema) e l'auto-compaction (che riassume la cronologia della conversazione quando ci si avvicina ai limiti del contesto).

Le seguenti strategie ti aiutano a mantenere il contesto piccolo e ridurre i costi per messaggio.

### Gestisci il contesto in modo proattivo

Utilizza `/cost` per controllare l'utilizzo attuale dei token, o [configura la tua linea di stato](/it/statusline#context-window-usage) per visualizzarla continuamente.

* **Cancella tra i compiti**: Utilizza `/clear` per ricominciare da capo quando passi a lavori non correlati. Il contesto obsoleto spreca token su ogni messaggio successivo. Utilizza `/rename` prima di cancellare in modo da poter trovare facilmente la sessione in seguito, quindi `/resume` per tornare ad essa.
* **Aggiungi istruzioni di compaction personalizzate**: `/compact Focus on code samples and API usage` dice a Claude cosa preservare durante la sintesi.

Puoi anche personalizzare il comportamento della compaction nel tuo CLAUDE.md:

```markdown theme={null}
# Compact instructions

When you are using compact, please focus on test output and code changes
```

### Scegli il modello giusto

Sonnet gestisce bene la maggior parte dei compiti di codifica e costa meno di Opus. Riserva Opus per decisioni architettoniche complesse o ragionamento multi-step. Utilizza `/model` per cambiare modello a metà sessione, o imposta un valore predefinito in `/config`. Per semplici compiti subagent, specifica `model: haiku` nella tua [configurazione subagent](/it/sub-agents#choose-a-model).

### Riduci l'overhead del server MCP

Ogni server MCP aggiunge definizioni di strumenti al tuo contesto, anche quando inattivo. Esegui `/context` per vedere cosa sta consumando spazio.

* **Preferisci gli strumenti CLI quando disponibili**: Strumenti come `gh`, `aws`, `gcloud` e `sentry-cli` sono più efficienti dal punto di vista del contesto rispetto ai server MCP perché non aggiungono definizioni di strumenti persistenti. Claude può eseguire comandi CLI direttamente senza l'overhead.
* **Disabilita i server inutilizzati**: Esegui `/mcp` per vedere i server configurati e disabilita quelli che non stai utilizzando attivamente.
* **La ricerca degli strumenti è automatica**: Quando le descrizioni degli strumenti MCP superano il 10% della tua finestra di contesto, Claude Code li rinvia automaticamente e carica gli strumenti su richiesta tramite [ricerca degli strumenti](/it/mcp#scale-with-mcp-tool-search). Poiché gli strumenti rinviati entrano nel contesto solo quando effettivamente utilizzati, una soglia più bassa significa meno definizioni di strumenti inattivi che consumano spazio. Imposta una soglia più bassa con `ENABLE_TOOL_SEARCH=auto:<N>` (ad esempio, `auto:5` si attiva quando gli strumenti superano il 5% della tua finestra di contesto).

### Installa plugin di intelligenza del codice per i linguaggi tipizzati

I [plugin di intelligenza del codice](/it/discover-plugins#code-intelligence) danno a Claude una navigazione precisa dei simboli invece della ricerca basata su testo, riducendo le letture di file non necessarie quando si esplora codice sconosciuto. Una singola chiamata "vai alla definizione" sostituisce quello che altrimenti potrebbe essere un grep seguito dalla lettura di più file candidati. I server di linguaggio installati segnalano anche gli errori di tipo automaticamente dopo le modifiche, quindi Claude cattura gli errori senza eseguire un compilatore.

### Offload dell'elaborazione agli hook e alle skills

Gli [hook](/it/hooks) personalizzati possono pre-elaborare i dati prima che Claude li veda. Invece di Claude che legge un file di log di 10.000 righe per trovare errori, un hook può cercare `ERROR` e restituire solo le righe corrispondenti, riducendo il contesto da decine di migliaia di token a centinaia.

Una [skill](/it/skills) può dare a Claude la conoscenza del dominio in modo che non debba esplorare. Ad esempio, una skill "codebase-overview" potrebbe descrivere l'architettura del tuo progetto, le directory chiave e le convenzioni di denominazione. Quando Claude invoca la skill, ottiene questo contesto immediatamente invece di spendere token leggendo più file per comprendere la struttura.

Ad esempio, questo hook PreToolUse filtra l'output del test per mostrare solo i fallimenti:

<Tabs>
  <Tab title="settings.json">
    Aggiungi questo al tuo [settings.json](/it/settings#settings-files) per eseguire l'hook prima di ogni comando Bash:

    ```json theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "~/.claude/hooks/filter-test-output.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="filter-test-output.sh">
    L'hook chiama questo script, che controlla se il comando è un test runner e lo modifica per mostrare solo i fallimenti:

    ```bash theme={null}
    #!/bin/bash
    input=$(cat)
    cmd=$(echo "$input" | jq -r '.tool_input.command')

    # If running tests, filter to show only failures
    if [[ "$cmd" =~ ^(npm test|pytest|go test) ]]; then
      filtered_cmd="$cmd 2>&1 | grep -A 5 -E '(FAIL|ERROR|error:)' | head -100"
      echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"updatedInput\":{\"command\":\"$filtered_cmd\"}}}"
    else
      echo "{}"
    fi
    ```
  </Tab>
</Tabs>

### Sposta le istruzioni da CLAUDE.md alle skills

Il tuo file [CLAUDE.md](/it/memory) viene caricato nel contesto all'inizio della sessione. Se contiene istruzioni dettagliate per flussi di lavoro specifici (come revisioni PR o migrazioni di database), quei token sono presenti anche quando stai facendo lavori non correlati. Le [skills](/it/skills) si caricano su richiesta solo quando invocate, quindi spostare le istruzioni specializzate nelle skills mantiene il tuo contesto di base più piccolo. Mira a mantenere CLAUDE.md sotto circa 500 righe includendo solo gli elementi essenziali.

### Regola il pensiero esteso

Il pensiero esteso è abilitato per impostazione predefinita con un budget di 31.999 token perché migliora significativamente le prestazioni su compiti complessi di pianificazione e ragionamento. Tuttavia, i token di pensiero vengono fatturati come token di output, quindi per compiti più semplici dove il ragionamento profondo non è necessario, puoi ridurre i costi abbassando il [livello di sforzo](/it/model-config#adjust-effort-level) con `/effort` o in `/model`, disabilitando il pensiero in `/config`, o abbassando il budget (ad esempio, `MAX_THINKING_TOKENS=8000`).

### Delega le operazioni dettagliate ai subagent

L'esecuzione di test, il recupero della documentazione o l'elaborazione di file di log possono consumare un contesto significativo. Delega questi ai [subagent](/it/sub-agents#isolate-high-volume-operations) in modo che l'output dettagliato rimanga nel contesto del subagent mentre solo un riassunto ritorna alla tua conversazione principale.

### Gestisci i costi del team di agenti

I team di agenti utilizzano approssimativamente 7 volte più token rispetto alle sessioni standard quando i compagni di squadra vengono eseguiti in plan mode, perché ogni compagno di squadra mantiene la propria finestra di contesto ed esegue come un'istanza Claude separata. Mantieni i compiti del team piccoli e autonomi per limitare l'utilizzo dei token per compagno di squadra. Vedi [team di agenti](/it/agent-teams) per i dettagli.

### Scrivi prompt specifici

Richieste vaghe come "migliora questa codebase" attivano una scansione ampia. Richieste specifiche come "aggiungi la convalida dell'input alla funzione di accesso in auth.ts" permettono a Claude di lavorare in modo efficiente con letture di file minime.

### Lavora in modo efficiente su compiti complessi

Per lavori più lunghi o complessi, queste abitudini aiutano a evitare token sprecati andando nella direzione sbagliata:

* **Utilizza plan mode per compiti complessi**: Premi Shift+Tab per entrare in [plan mode](/it/common-workflows#use-plan-mode-for-safe-code-analysis) prima dell'implementazione. Claude esplora la codebase e propone un approccio per la tua approvazione, prevenendo la rielaborazione costosa quando la direzione iniziale è sbagliata.
* **Correggi la rotta presto**: Se Claude inizia a andare nella direzione sbagliata, premi Escape per fermarti immediatamente. Utilizza `/rewind` o doppio tocco Escape per ripristinare la conversazione e il codice a un checkpoint precedente.
* **Fornisci target di verifica**: Includi casi di test, incolla screenshot o definisci l'output previsto nel tuo prompt. Quando Claude può verificare il suo lavoro, cattura i problemi prima che tu debba richiedere correzioni.
* **Testa in modo incrementale**: Scrivi un file, testalo, quindi continua. Questo cattura i problemi presto quando sono economici da risolvere.

## Utilizzo dei token in background

Claude Code utilizza token per alcune funzionalità in background anche quando inattivo:

* **Sintesi della conversazione**: Processi in background che riassumono le conversazioni precedenti per la funzione `claude --resume`
* **Elaborazione dei comandi**: Alcuni comandi come `/cost` possono generare richieste per controllare lo stato

Questi processi in background consumano una piccola quantità di token (in genere meno di \$0,04 per sessione) anche senza interazione attiva.

## Comprensione dei cambiamenti nel comportamento di Claude Code

Claude Code riceve regolarmente aggiornamenti che possono cambiare il funzionamento delle funzionalità, inclusa la segnalazione dei costi. Esegui `claude --version` per controllare la tua versione attuale. Per domande specifiche sulla fatturazione, contatta il supporto di Anthropic tramite il tuo [account Console](https://platform.claude.com/login). Per distribuzioni di team, inizia con un piccolo gruppo pilota per stabilire i modelli di utilizzo prima di un rollout più ampio.
