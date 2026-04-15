> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Flussi di lavoro comuni

> Guide passo dopo passo per esplorare basi di codice, correggere bug, effettuare refactoring, testare e altri compiti quotidiani con Claude Code.

Questa pagina copre flussi di lavoro pratici per lo sviluppo quotidiano: esplorare codice non familiare, eseguire il debug, effettuare refactoring, scrivere test, creare PR e gestire sessioni. Ogni sezione include prompt di esempio che puoi adattare ai tuoi progetti. Per modelli e suggerimenti di livello superiore, vedi [Best practices](/it/best-practices).

## Comprendere nuove basi di codice

### Ottenere una rapida panoramica della base di codice

Supponiamo che tu abbia appena aderito a un nuovo progetto e debba comprendere rapidamente la sua struttura.

<Steps>
  <Step title="Navigare alla directory radice del progetto">
    ```bash theme={null}
    cd /path/to/project 
    ```
  </Step>

  <Step title="Avviare Claude Code">
    ```bash theme={null}
    claude 
    ```
  </Step>

  <Step title="Chiedere una panoramica di alto livello">
    ```text theme={null}
    give me an overview of this codebase
    ```
  </Step>

  <Step title="Approfondire componenti specifici">
    ```text theme={null}
    explain the main architecture patterns used here
    ```

    ```text theme={null}
    what are the key data models?
    ```

    ```text theme={null}
    how is authentication handled?
    ```
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * Inizia con domande ampie, quindi restringi a aree specifiche
  * Chiedi informazioni sulle convenzioni di codifica e sui modelli utilizzati nel progetto
  * Richiedi un glossario di termini specifici del progetto
</Tip>

### Trovare codice rilevante

Supponiamo che tu debba individuare il codice relativo a una funzionalità o funzione specifica.

<Steps>
  <Step title="Chiedere a Claude di trovare file rilevanti">
    ```text theme={null}
    find the files that handle user authentication
    ```
  </Step>

  <Step title="Ottenere contesto su come i componenti interagiscono">
    ```text theme={null}
    how do these authentication files work together?
    ```
  </Step>

  <Step title="Comprendere il flusso di esecuzione">
    ```text theme={null}
    trace the login process from front-end to database
    ```
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * Sii specifico su ciò che stai cercando
  * Usa il linguaggio del dominio dal progetto
  * Installa un [plugin di code intelligence](/it/discover-plugins#code-intelligence) per il tuo linguaggio per dare a Claude una navigazione precisa "go to definition" e "find references"
</Tip>

***

## Correggere bug in modo efficiente

Supponiamo che tu abbia riscontrato un messaggio di errore e debba trovare e correggere la sua fonte.

<Steps>
  <Step title="Condividere l'errore con Claude">
    ```text theme={null}
    I'm seeing an error when I run npm test
    ```
  </Step>

  <Step title="Chiedere raccomandazioni per la correzione">
    ```text theme={null}
    suggest a few ways to fix the @ts-ignore in user.ts
    ```
  </Step>

  <Step title="Applicare la correzione">
    ```text theme={null}
    update user.ts to add the null check you suggested
    ```
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * Comunica a Claude il comando per riprodurre il problema e ottenere una stack trace
  * Menziona eventuali passaggi per riprodurre l'errore
  * Fai sapere a Claude se l'errore è intermittente o coerente
</Tip>

***

## Effettuare refactoring del codice

Supponiamo che tu debba aggiornare il codice precedente per utilizzare modelli e pratiche moderne.

<Steps>
  <Step title="Identificare il codice legacy per il refactoring">
    ```text theme={null}
    find deprecated API usage in our codebase
    ```
  </Step>

  <Step title="Ottenere raccomandazioni per il refactoring">
    ```text theme={null}
    suggest how to refactor utils.js to use modern JavaScript features
    ```
  </Step>

  <Step title="Applicare le modifiche in modo sicuro">
    ```text theme={null}
    refactor utils.js to use ES2024 features while maintaining the same behavior
    ```
  </Step>

  <Step title="Verificare il refactoring">
    ```text theme={null}
    run tests for the refactored code
    ```
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * Chiedi a Claude di spiegare i vantaggi dell'approccio moderno
  * Richiedi che le modifiche mantengano la compatibilità all'indietro quando necessario
  * Effettua il refactoring in piccoli incrementi testabili
</Tip>

***

## Utilizzare subagent specializzati

Supponiamo che tu voglia utilizzare subagent AI specializzati per gestire attività specifiche in modo più efficace.

<Steps>
  <Step title="Visualizzare i subagent disponibili">
    ```text theme={null}
    /agents
    ```

    Questo mostra tutti i subagent disponibili e ti consente di crearne di nuovi.
  </Step>

  <Step title="Utilizzare i subagent automaticamente">
    Claude Code delega automaticamente le attività appropriate ai subagent specializzati:

    ```text theme={null}
    review my recent code changes for security issues
    ```

    ```text theme={null}
    run all tests and fix any failures
    ```
  </Step>

  <Step title="Richiedere esplicitamente subagent specifici">
    ```text theme={null}
    use the code-reviewer subagent to check the auth module
    ```

    ```text theme={null}
    have the debugger subagent investigate why users can't log in
    ```
  </Step>

  <Step title="Creare subagent personalizzati per il tuo flusso di lavoro">
    ```text theme={null}
    /agents
    ```

    Quindi seleziona "Create New subagent" e segui i prompt per definire:

    * Un identificatore univoco che descrive lo scopo del subagent (ad esempio, `code-reviewer`, `api-designer`).
    * Quando Claude dovrebbe utilizzare questo agente
    * Quali strumenti può accedere
    * Un prompt di sistema che descrive il ruolo e il comportamento dell'agente
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * Crea subagent specifici del progetto in `.claude/agents/` per la condivisione del team
  * Usa campi `description` descrittivi per abilitare la delegazione automatica
  * Limita l'accesso agli strumenti a ciò di cui ogni subagent ha effettivamente bisogno
  * Controlla la [documentazione dei subagent](/it/sub-agents) per esempi dettagliati
</Tip>

***

## Utilizzare Plan Mode per l'analisi sicura del codice

Plan Mode istruisce Claude a creare un piano analizzando la base di codice con operazioni di sola lettura, perfetto per esplorare basi di codice, pianificare modifiche complesse o rivedere il codice in modo sicuro. In Plan Mode, Claude utilizza [`AskUserQuestion`](/it/tools-reference) per raccogliere requisiti e chiarire i tuoi obiettivi prima di proporre un piano.

### Quando utilizzare Plan Mode

* **Implementazione multi-step**: Quando la tua funzionalità richiede di apportare modifiche a molti file
* **Esplorazione del codice**: Quando desideri ricercare a fondo la base di codice prima di modificare qualsiasi cosa
* **Sviluppo interattivo**: Quando desideri iterare sulla direzione con Claude

### Come utilizzare Plan Mode

**Attivare Plan Mode durante una sessione**

Puoi passare a Plan Mode durante una sessione utilizzando **Shift+Tab** per scorrere le modalità di autorizzazione.

Se sei in Normal Mode, **Shift+Tab** passa prima a Auto-Accept Mode, indicato da `⏵⏵ accept edits on` nella parte inferiore del terminale. Un successivo **Shift+Tab** passerà a Plan Mode, indicato da `⏸ plan mode on`.

**Avviare una nuova sessione in Plan Mode**

Per avviare una nuova sessione in Plan Mode, usa il flag `--permission-mode plan`:

```bash theme={null}
claude --permission-mode plan
```

**Eseguire query "headless" in Plan Mode**

Puoi anche eseguire una query in Plan Mode direttamente con `-p` (cioè in ["headless mode"](/it/headless)):

```bash theme={null}
claude --permission-mode plan -p "Analyze the authentication system and suggest improvements"
```

### Esempio: Pianificazione di un refactoring complesso

```bash theme={null}
claude --permission-mode plan
```

```text theme={null}
I need to refactor our authentication system to use OAuth2. Create a detailed migration plan.
```

Claude analizza l'implementazione attuale e crea un piano completo. Affina con follow-up:

```text theme={null}
What about backward compatibility?
```

```text theme={null}
How should we handle database migration?
```

<Tip>Premi `Ctrl+G` per aprire il piano nel tuo editor di testo predefinito, dove puoi modificarlo direttamente prima che Claude proceda.</Tip>

Quando accetti un piano, Claude denomina automaticamente la sessione dal contenuto del piano. Il nome appare sulla barra del prompt e nel selettore di sessione. Se hai già impostato un nome con `--name` o `/rename`, accettare un piano non lo sovrascriverà.

### Configurare Plan Mode come predefinito

```json theme={null}
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

Vedi la [documentazione delle impostazioni](/it/settings#available-settings) per ulteriori opzioni di configurazione.

***

## Lavorare con i test

Supponiamo che tu debba aggiungere test per il codice non coperto.

<Steps>
  <Step title="Identificare il codice non testato">
    ```text theme={null}
    find functions in NotificationsService.swift that are not covered by tests
    ```
  </Step>

  <Step title="Generare lo scaffolding dei test">
    ```text theme={null}
    add tests for the notification service
    ```
  </Step>

  <Step title="Aggiungere casi di test significativi">
    ```text theme={null}
    add test cases for edge conditions in the notification service
    ```
  </Step>

  <Step title="Eseguire e verificare i test">
    ```text theme={null}
    run the new tests and fix any failures
    ```
  </Step>
</Steps>

Claude può generare test che seguono i modelli e le convenzioni esistenti del tuo progetto. Quando chiedi test, sii specifico sul comportamento che desideri verificare. Claude esamina i tuoi file di test esistenti per abbinare lo stile, i framework e i modelli di asserzione già in uso.

Per una copertura completa, chiedi a Claude di identificare i casi limite che potresti aver perso. Claude può analizzare i tuoi percorsi di codice e suggerire test per condizioni di errore, valori limite e input inaspettati che sono facili da trascurare.

***

## Creare pull request

Puoi creare pull request chiedendo direttamente a Claude ("create a pr for my changes"), oppure guidare Claude attraverso i passaggi:

<Steps>
  <Step title="Riassumere le tue modifiche">
    ```text theme={null}
    summarize the changes I've made to the authentication module
    ```
  </Step>

  <Step title="Generare una pull request">
    ```text theme={null}
    create a pr
    ```
  </Step>

  <Step title="Rivedere e affinare">
    ```text theme={null}
    enhance the PR description with more context about the security improvements
    ```
  </Step>
</Steps>

Quando crei una PR utilizzando `gh pr create`, la sessione viene automaticamente collegata a quella PR. Puoi riprenderla in seguito con `claude --from-pr <number>`.

<Tip>
  Rivedi la PR generata da Claude prima di inviarla e chiedi a Claude di evidenziare i rischi potenziali o le considerazioni.
</Tip>

## Gestire la documentazione

Supponiamo che tu debba aggiungere o aggiornare la documentazione per il tuo codice.

<Steps>
  <Step title="Identificare il codice non documentato">
    ```text theme={null}
    find functions without proper JSDoc comments in the auth module
    ```
  </Step>

  <Step title="Generare la documentazione">
    ```text theme={null}
    add JSDoc comments to the undocumented functions in auth.js
    ```
  </Step>

  <Step title="Rivedere e migliorare">
    ```text theme={null}
    improve the generated documentation with more context and examples
    ```
  </Step>

  <Step title="Verificare la documentazione">
    ```text theme={null}
    check if the documentation follows our project standards
    ```
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * Specifica lo stile di documentazione che desideri (JSDoc, docstrings, ecc.)
  * Chiedi esempi nella documentazione
  * Richiedi documentazione per API pubbliche, interfacce e logica complessa
</Tip>

***

## Lavorare con le immagini

Supponiamo che tu debba lavorare con immagini nella tua base di codice e desideri l'aiuto di Claude nell'analizzare il contenuto dell'immagine.

<Steps>
  <Step title="Aggiungere un'immagine alla conversazione">
    Puoi utilizzare uno di questi metodi:

    1. Trascina e rilascia un'immagine nella finestra di Claude Code
    2. Copia un'immagine e incollala nella CLI con ctrl+v (Non usare cmd+v)
    3. Fornisci un percorso di immagine a Claude. Ad esempio, "Analyze this image: /path/to/your/image.png"
  </Step>

  <Step title="Chiedere a Claude di analizzare l'immagine">
    ```text theme={null}
    What does this image show?
    ```

    ```text theme={null}
    Describe the UI elements in this screenshot
    ```

    ```text theme={null}
    Are there any problematic elements in this diagram?
    ```
  </Step>

  <Step title="Utilizzare le immagini per il contesto">
    ```text theme={null}
    Here's a screenshot of the error. What's causing it?
    ```

    ```text theme={null}
    This is our current database schema. How should we modify it for the new feature?
    ```
  </Step>

  <Step title="Ottenere suggerimenti di codice dal contenuto visivo">
    ```text theme={null}
    Generate CSS to match this design mockup
    ```

    ```text theme={null}
    What HTML structure would recreate this component?
    ```
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * Usa le immagini quando le descrizioni di testo sarebbero poco chiare o ingombranti
  * Includi screenshot di errori, design dell'interfaccia utente o diagrammi per un contesto migliore
  * Puoi lavorare con più immagini in una conversazione
  * L'analisi delle immagini funziona con diagrammi, screenshot, mockup e altro
  * Quando Claude fa riferimento a immagini (ad esempio, `[Image #1]`), `Cmd+Click` (Mac) o `Ctrl+Click` (Windows/Linux) il collegamento per aprire l'immagine nel tuo visualizzatore predefinito
</Tip>

***

## Fare riferimento a file e directory

Usa @ per includere rapidamente file o directory senza aspettare che Claude li legga.

<Steps>
  <Step title="Fare riferimento a un singolo file">
    ```text theme={null}
    Explain the logic in @src/utils/auth.js
    ```

    Questo include il contenuto completo del file nella conversazione.
  </Step>

  <Step title="Fare riferimento a una directory">
    ```text theme={null}
    What's the structure of @src/components?
    ```

    Questo fornisce un elenco di directory con informazioni sui file.
  </Step>

  <Step title="Fare riferimento alle risorse MCP">
    ```text theme={null}
    Show me the data from @github:repos/owner/repo/issues
    ```

    Questo recupera i dati dai server MCP connessi utilizzando il formato @server:resource. Vedi [risorse MCP](/it/mcp#use-mcp-resources) per i dettagli.
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * I percorsi dei file possono essere relativi o assoluti
  * I riferimenti ai file @ aggiungono `CLAUDE.md` nella directory del file e nelle directory padre al contesto
  * I riferimenti alle directory mostrano elenchi di file, non contenuti
  * Puoi fare riferimento a più file in un singolo messaggio (ad esempio, "@file1.js and @file2.js")
</Tip>

***

## Utilizzare il pensiero esteso (Thinking Mode)

[Extended thinking](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) è abilitato per impostazione predefinita, dando a Claude lo spazio per ragionare attraverso problemi complessi passo dopo passo prima di rispondere. Questo ragionamento è visibile in modalità verbose, che puoi attivare con `Ctrl+O`.

Inoltre, Opus 4.6 e Sonnet 4.6 supportano il ragionamento adattivo: invece di un budget di token di pensiero fisso, il modello alloca dinamicamente il pensiero in base alla tua impostazione di [livello di sforzo](/it/model-config#adjust-effort-level). Extended thinking e il ragionamento adattivo lavorano insieme per darti il controllo su quanto profondamente Claude ragiona prima di rispondere.

Extended thinking è particolarmente prezioso per decisioni architettoniche complesse, bug impegnativi, pianificazione dell'implementazione multi-step e valutazione dei compromessi tra diversi approcci.

<Note>
  Frasi come "think", "think hard" e "think more" sono interpretate come istruzioni di prompt regolari e non allocano token di pensiero.
</Note>

### Configurare Thinking Mode

Il pensiero è abilitato per impostazione predefinita, ma puoi regolarlo o disabilitarlo.

| Ambito                                        | Come configurare                                                                           | Dettagli                                                                                                                                                                                                         |
| --------------------------------------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Livello di sforzo**                         | Esegui `/effort`, regola in `/model`, o imposta [`CLAUDE_CODE_EFFORT_LEVEL`](/it/env-vars) | Controlla la profondità del pensiero per Opus 4.6 e Sonnet 4.6. Vedi [Regola il livello di sforzo](/it/model-config#adjust-effort-level)                                                                         |
| **Parola chiave `ultrathink`**                | Includi "ultrathink" in qualsiasi punto del tuo prompt                                     | Imposta lo sforzo su alto per quel turno su Opus 4.6 e Sonnet 4.6. Utile per attività una tantum che richiedono un ragionamento profondo senza modificare permanentemente la tua impostazione di sforzo          |
| **Scorciatoia di attivazione/disattivazione** | Premi `Option+T` (macOS) o `Alt+T` (Windows/Linux)                                         | Attiva/disattiva il pensiero per la sessione corrente (tutti i modelli). Potrebbe richiedere la [configurazione del terminale](/it/terminal-config) per abilitare le scorciatoie da tastiera Option              |
| **Predefinito globale**                       | Usa `/config` per attivare/disattivare Thinking Mode                                       | Imposta il tuo predefinito in tutti i progetti (tutti i modelli).<br />Salvato come `alwaysThinkingEnabled` in `~/.claude/settings.json`                                                                         |
| **Limitare il budget dei token**              | Imposta la variabile di ambiente [`MAX_THINKING_TOKENS`](/it/env-vars)                     | Limita il budget di pensiero a un numero specifico di token. Su Opus 4.6 e Sonnet 4.6, solo `0` si applica a meno che il ragionamento adattivo non sia disabilitato. Esempio: `export MAX_THINKING_TOKENS=10000` |

Per visualizzare il processo di pensiero di Claude, premi `Ctrl+O` per attivare la modalità verbose e vedi il ragionamento interno visualizzato come testo grigio in corsivo.

### Come funziona il pensiero esteso

Extended thinking controlla quanto ragionamento interno Claude esegue prima di rispondere. Più pensiero fornisce più spazio per esplorare soluzioni, analizzare casi limite e autocorreggersi gli errori.

**Con Opus 4.6 e Sonnet 4.6**, il pensiero utilizza il ragionamento adattivo: il modello alloca dinamicamente i token di pensiero in base al [livello di sforzo](/it/model-config#adjust-effort-level) che selezioni. Questo è il modo consigliato per sintonizzare il compromesso tra velocità e profondità di ragionamento.

**Con modelli più vecchi**, il pensiero utilizza un budget fisso di token prelevato dalla tua allocazione di output. Il budget varia in base al modello; vedi [`MAX_THINKING_TOKENS`](/it/env-vars) per i massimali per modello. Puoi limitare il budget con quella variabile di ambiente, o disabilitare completamente il pensiero tramite `/config` o l'attivazione/disattivazione `Option+T`/`Alt+T`.

Su Opus 4.6 e Sonnet 4.6, il [ragionamento adattivo](/it/model-config#adjust-effort-level) controlla la profondità del pensiero, quindi `MAX_THINKING_TOKENS` si applica solo quando impostato su `0` per disabilitare il pensiero, o quando `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` ripristina questi modelli al budget fisso. Vedi [variabili di ambiente](/it/env-vars).

<Warning>
  Ti viene addebitato per tutti i token di pensiero utilizzati anche quando i riassunti di pensiero sono redatti. In modalità interattiva, il pensiero appare come uno stub compresso per impostazione predefinita. Imposta `showThinkingSummaries: true` in `settings.json` per mostrare riassunti completi.
</Warning>

***

## Riprendere conversazioni precedenti

Quando avvii Claude Code, puoi riprendere una sessione precedente:

* `claude --continue` continua la conversazione più recente nella directory corrente
* `claude --resume` apre un selettore di conversazione o riprende per nome
* `claude --from-pr 123` riprende le sessioni collegate a una pull request specifica

Da una sessione attiva, usa `/resume` per passare a una conversazione diversa.

Le sessioni vengono archiviate per directory di progetto. Il selettore `/resume` mostra le sessioni interattive dallo stesso repository git, inclusi i worktree. Le sessioni create da `claude -p` o da invocazioni SDK non appaiono nel selettore, ma puoi comunque riprenderne una passando il suo ID di sessione direttamente a `claude --resume <session-id>`.

### Denominare le tue sessioni

Dai alle sessioni nomi descrittivi per trovarle in seguito. Questa è una best practice quando lavori su più attività o funzionalità.

<Steps>
  <Step title="Denominare la sessione">
    Denomina una sessione all'avvio con `-n`:

    ```bash theme={null}
    claude -n auth-refactor
    ```

    Oppure usa `/rename` durante una sessione, che mostra anche il nome sulla barra del prompt:

    ```text theme={null}
    /rename auth-refactor
    ```

    Puoi anche rinominare qualsiasi sessione dal selettore: esegui `/resume`, naviga a una sessione e premi `R`.
  </Step>

  <Step title="Riprendere per nome in seguito">
    Dalla riga di comando:

    ```bash theme={null}
    claude --resume auth-refactor
    ```

    O da una sessione attiva:

    ```text theme={null}
    /resume auth-refactor
    ```
  </Step>
</Steps>

### Utilizzare il selettore di sessione

Il comando `/resume` (o `claude --resume` senza argomenti) apre un selettore di sessione interattivo con queste funzionalità:

**Scorciatoie da tastiera nel selettore:**

| Scorciatoia | Azione                                                 |
| :---------- | :----------------------------------------------------- |
| `↑` / `↓`   | Navigare tra le sessioni                               |
| `→` / `←`   | Espandere o comprimere le sessioni raggruppate         |
| `Enter`     | Selezionare e riprendere la sessione evidenziata       |
| `P`         | Visualizzare l'anteprima del contenuto della sessione  |
| `R`         | Rinominare la sessione evidenziata                     |
| `/`         | Cercare per filtrare le sessioni                       |
| `A`         | Alternare tra la directory corrente e tutti i progetti |
| `B`         | Filtrare le sessioni dal tuo ramo git corrente         |
| `Esc`       | Uscire dal selettore o dalla modalità di ricerca       |

**Organizzazione della sessione:**

Il selettore visualizza le sessioni con metadati utili:

* Nome della sessione o prompt iniziale
* Tempo trascorso dall'ultima attività
* Conteggio dei messaggi
* Ramo Git (se applicabile)

Le sessioni fork (create con `/branch`, `/rewind`, o `--fork-session`) sono raggruppate insieme sotto la loro sessione radice, rendendo più facile trovare conversazioni correlate.

<Tip>
  Suggerimenti:

  * **Denominare le sessioni in anticipo**: Usa `/rename` quando inizi a lavorare su un'attività distinta, è molto più facile trovare "payment-integration" che "explain this function" in seguito
  * Usa `--continue` per un accesso rapido alla tua conversazione più recente nella directory corrente
  * Usa `--resume session-name` quando sai quale sessione ti serve
  * Usa `--resume` (senza un nome) quando hai bisogno di sfogliare e selezionare
  * Per gli script, usa `claude --continue --print "prompt"` per riprendere in modalità non interattiva
  * Premi `P` nel selettore per visualizzare l'anteprima di una sessione prima di riprenderla
  * La conversazione ripresa inizia con lo stesso modello e configurazione dell'originale

  Come funziona:

  1. **Archiviazione della conversazione**: Tutte le conversazioni vengono salvate automaticamente localmente con la loro cronologia completa dei messaggi
  2. **Deserializzazione dei messaggi**: Quando si riprende, l'intera cronologia dei messaggi viene ripristinata per mantenere il contesto
  3. **Stato dello strumento**: L'utilizzo dello strumento e i risultati della conversazione precedente vengono preservati
  4. **Ripristino del contesto**: La conversazione riprende con tutto il contesto precedente intatto
</Tip>

***

## Eseguire sessioni parallele di Claude Code con Git worktrees

Quando lavori su più attività contemporaneamente, hai bisogno che ogni sessione di Claude abbia la sua copia della base di codice in modo che le modifiche non si scontrino. I worktree Git risolvono questo creando directory di lavoro separate che hanno ciascuna i propri file e ramo, mentre condividono la stessa cronologia del repository e le connessioni remote. Ciò significa che puoi avere Claude che lavora su una funzionalità in un worktree mentre corregge un bug in un altro, senza che nessuna sessione interferisca con l'altra.

Usa il flag `--worktree` (`-w`) per creare un worktree isolato e avviare Claude in esso. Il valore che passi diventa il nome della directory del worktree e il nome del ramo:

```bash theme={null}
# Avviare Claude in un worktree denominato "feature-auth"
# Crea .claude/worktrees/feature-auth/ con un nuovo ramo
claude --worktree feature-auth

# Avviare un'altra sessione in un worktree separato
claude --worktree bugfix-123
```

Se ometti il nome, Claude ne genera uno casuale automaticamente:

```bash theme={null}
# Genera automaticamente un nome come "bright-running-fox"
claude --worktree
```

I worktree vengono creati in `<repo>/.claude/worktrees/<name>` e si diramano dal ramo remoto predefinito, che è dove `origin/HEAD` punta. Il ramo del worktree è denominato `worktree-<name>`.

Il ramo di base non è configurabile tramite un flag o un'impostazione di Claude Code. `origin/HEAD` è un riferimento archiviato nella tua directory `.git` locale che Git ha impostato una volta quando hai clonato. Se il ramo predefinito del repository cambia successivamente su GitHub o GitLab, il tuo `origin/HEAD` locale continua a puntare a quello vecchio, e i worktree si diramano da lì. Per risincronizzare il tuo riferimento locale con quello che il remoto considera attualmente il suo predefinito:

```bash theme={null}
git remote set-head origin -a
```

Questo è un comando Git standard che aggiorna solo la tua directory `.git` locale. Nulla sul server remoto cambia. Se desideri che i worktree si basino su un ramo specifico piuttosto che sul predefinito del remoto, impostalo esplicitamente con `git remote set-head origin your-branch-name`.

Per il controllo completo su come vengono creati i worktree, inclusa la scelta di una base diversa per invocazione, configura un [hook WorktreeCreate](/it/hooks#worktreecreate). L'hook sostituisce completamente la logica predefinita di `git worktree` di Claude Code, quindi puoi recuperare e diramati da qualsiasi ref di cui hai bisogno.

Puoi anche chiedere a Claude di "work in a worktree" o "start a worktree" durante una sessione, e creerà uno automaticamente.

### Worktree dei subagent

I subagent possono anche utilizzare l'isolamento del worktree per lavorare in parallelo senza conflitti. Chiedi a Claude di "use worktrees for your agents" o configuralo in un [subagent personalizzato](/it/sub-agents#supported-frontmatter-fields) aggiungendo `isolation: worktree` al frontmatter dell'agente. Ogni subagent ottiene il suo worktree che viene automaticamente pulito quando il subagent finisce senza modifiche.

### Pulizia del worktree

Quando esci da una sessione di worktree, Claude gestisce la pulizia in base al fatto che tu abbia apportato modifiche:

* **Nessuna modifica**: il worktree e il suo ramo vengono rimossi automaticamente
* **Modifiche o commit esistenti**: Claude ti chiede se mantenere o rimuovere il worktree. Mantenere preserva la directory e il ramo in modo da poter tornare in seguito. Rimuovere elimina la directory del worktree e il suo ramo, scartando tutte le modifiche non sottoposte a commit e i commit

Per pulire i worktree al di fuori di una sessione di Claude, usa la [gestione manuale del worktree](#manage-worktrees-manually).

<Tip>
  Aggiungi `.claude/worktrees/` al tuo `.gitignore` per evitare che il contenuto del worktree appaia come file non tracciati nel tuo repository principale.
</Tip>

### Copiare file ignorati da git nei worktree

I worktree Git sono checkout freschi, quindi non includono file non tracciati come `.env` o `.env.local` dal tuo repository principale. Per copiare automaticamente questi file quando Claude crea un worktree, aggiungi un file `.worktreeinclude` alla radice del tuo progetto.

Il file utilizza la sintassi `.gitignore` per elencare quali file copiare. Solo i file che corrispondono a un modello e sono anche ignorati da git vengono copiati, quindi i file tracciati non vengono mai duplicati.

```text .worktreeinclude theme={null}
.env
.env.local
config/secrets.json
```

Questo si applica ai worktree creati con `--worktree`, ai worktree dei subagent e alle sessioni parallele nell'[app desktop](/it/desktop#work-in-parallel-with-sessions).

### Gestire i worktree manualmente

Per un maggiore controllo sulla posizione del worktree e sulla configurazione del ramo, crea i worktree direttamente con Git. Questo è utile quando hai bisogno di controllare un ramo esistente specifico o posizionare il worktree al di fuori del repository.

```bash theme={null}
# Creare un worktree con un nuovo ramo
git worktree add ../project-feature-a -b feature-a

# Creare un worktree con un ramo esistente
git worktree add ../project-bugfix bugfix-123

# Avviare Claude nel worktree
cd ../project-feature-a && claude

# Pulire al termine
git worktree list
git worktree remove ../project-feature-a
```

Scopri di più nella [documentazione ufficiale di Git worktree](https://git-scm.com/docs/git-worktree).

<Tip>
  Ricorda di inizializzare il tuo ambiente di sviluppo in ogni nuovo worktree secondo la configurazione del tuo progetto. A seconda del tuo stack, questo potrebbe includere l'esecuzione dell'installazione delle dipendenze (`npm install`, `yarn`), la configurazione di ambienti virtuali o il seguire il processo di configurazione standard del tuo progetto.
</Tip>

### Controllo della versione non git

L'isolamento del worktree funziona con git per impostazione predefinita. Per altri sistemi di controllo della versione come SVN, Perforce o Mercurial, configura gli hook [WorktreeCreate e WorktreeRemove](/it/hooks#worktreecreate) per fornire logica personalizzata di creazione e pulizia del worktree. Quando configurati, questi hook sostituiscono il comportamento git predefinito quando usi `--worktree`, quindi [`.worktreeinclude`](#copy-gitignored-files-to-worktrees) non viene elaborato. Copia qualsiasi file di configurazione locale all'interno dello script del tuo hook.

Per il coordinamento automatizzato di sessioni parallele con attività condivise e messaggistica, vedi [team di agenti](/it/agent-teams).

***

## Ricevere notifiche quando Claude ha bisogno della tua attenzione

Quando avvii un'attività a lunga esecuzione e passi a un'altra finestra, puoi configurare notifiche desktop in modo da sapere quando Claude finisce o ha bisogno del tuo input. Questo utilizza l'evento `Notification` [hook](/it/hooks-guide#get-notified-when-claude-needs-input), che si attiva ogni volta che Claude è in attesa di autorizzazione, inattivo e pronto per un nuovo prompt, o completando l'autenticazione.

<Steps>
  <Step title="Aggiungere l'hook alle tue impostazioni">
    Apri `~/.claude/settings.json` e aggiungi un hook `Notification` che chiama il comando di notifica nativa della tua piattaforma:

    <Tabs>
      <Tab title="macOS">
        ```json theme={null}
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
        ```json theme={null}
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

      <Tab title="Windows">
        ```json theme={null}
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

    Se il tuo file di impostazioni ha già una chiave `hooks`, unisci la voce `Notification` in essa piuttosto che sovrascrivere. Puoi anche chiedere a Claude di scrivere l'hook per te descrivendo ciò che desideri nella CLI.
  </Step>

  <Step title="Facoltativamente restringere il matcher">
    Per impostazione predefinita l'hook si attiva su tutti i tipi di notifica. Per attivarsi solo per eventi specifici, imposta il campo `matcher` su uno di questi valori:

    | Matcher              | Si attiva quando                                             |
    | :------------------- | :----------------------------------------------------------- |
    | `permission_prompt`  | Claude ha bisogno che tu approvi un utilizzo dello strumento |
    | `idle_prompt`        | Claude ha finito ed è in attesa del tuo prossimo prompt      |
    | `auth_success`       | L'autenticazione si completa                                 |
    | `elicitation_dialog` | Claude ti sta facendo una domanda                            |
  </Step>

  <Step title="Verificare l'hook">
    Digita `/hooks` e seleziona `Notification` per confermare che l'hook appare. Selezionarlo mostra il comando che verrà eseguito. Per testarlo end-to-end, chiedi a Claude di eseguire un comando che richiede autorizzazione e passa a un'altra finestra, oppure chiedi a Claude di attivare una notifica direttamente.
  </Step>
</Steps>

Per lo schema completo dell'evento e i tipi di notifica, vedi il [riferimento Notification](/it/hooks#notification).

***

## Utilizzare Claude come utilità di tipo unix

### Aggiungere Claude al tuo processo di verifica

Supponiamo che tu voglia utilizzare Claude Code come linter o revisore del codice.

**Aggiungere Claude al tuo script di build:**

```json theme={null}
// package.json
{
    ...
    "scripts": {
        ...
        "lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos. report the filename and line number on one line, and a description of the issue on the second line. do not return any other text.'"
    }
}
```

<Tip>
  Suggerimenti:

  * Usa Claude per la revisione automatica del codice nella tua pipeline CI/CD
  * Personalizza il prompt per verificare i problemi specifici rilevanti per il tuo progetto
  * Considera di creare più script per diversi tipi di verifica
</Tip>

### Pipe in, pipe out

Supponiamo che tu voglia inviare dati a Claude e ottenere dati in un formato strutturato.

**Inviare dati attraverso Claude:**

```bash theme={null}
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

<Tip>
  Suggerimenti:

  * Usa i pipe per integrare Claude negli script shell esistenti
  * Combina con altri strumenti Unix per flussi di lavoro potenti
  * Considera di utilizzare `--output-format` per output strutturato
</Tip>

### Controllare il formato di output

Supponiamo che tu abbia bisogno dell'output di Claude in un formato specifico, specialmente quando integri Claude Code in script o altri strumenti.

<Steps>
  <Step title="Utilizzare il formato testo (predefinito)">
    ```bash theme={null}
    cat data.txt | claude -p 'summarize this data' --output-format text > summary.txt
    ```

    Questo restituisce solo la risposta di testo semplice di Claude (comportamento predefinito).
  </Step>

  <Step title="Utilizzare il formato JSON">
    ```bash theme={null}
    cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json
    ```

    Questo restituisce un array JSON di messaggi con metadati inclusi costo e durata.
  </Step>

  <Step title="Utilizzare il formato JSON in streaming">
    ```bash theme={null}
    cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json
    ```

    Questo restituisce una serie di oggetti JSON in tempo reale mentre Claude elabora la richiesta. Ogni messaggio è un oggetto JSON valido, ma l'intero output non è JSON valido se concatenato.
  </Step>
</Steps>

<Tip>
  Suggerimenti:

  * Usa `--output-format text` per integrazioni semplici dove hai solo bisogno della risposta di Claude
  * Usa `--output-format json` quando hai bisogno del registro completo della conversazione
  * Usa `--output-format stream-json` per l'output in tempo reale di ogni turno di conversazione
</Tip>

***

## Eseguire Claude su una pianificazione

Supponiamo che tu voglia che Claude gestisca un'attività automaticamente su base ricorrente, come rivedere le PR aperte ogni mattina, controllare le dipendenze settimanalmente o verificare i fallimenti di CI durante la notte.

Scegli un'opzione di pianificazione in base a dove desideri che l'attività venga eseguita:

| Opzione                                                              | Dove viene eseguita                    | Migliore per                                                                                                                                              |
| :------------------------------------------------------------------- | :------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Attività pianificate nel cloud](/it/web-scheduled-tasks)            | Infrastruttura gestita da Anthropic    | Attività che dovrebbero essere eseguite anche quando il tuo computer è spento. Configura su [claude.ai/code](https://claude.ai/code).                     |
| [Attività pianificate desktop](/it/desktop#schedule-recurring-tasks) | La tua macchina, tramite l'app desktop | Attività che hanno bisogno di accesso diretto a file locali, strumenti o modifiche non sottoposte a commit.                                               |
| [GitHub Actions](/it/github-actions)                                 | La tua pipeline CI                     | Attività legate a eventi del repository come PR aperte, o pianificazioni cron che dovrebbero vivere insieme alla tua configurazione del flusso di lavoro. |
| [`/loop`](/it/scheduled-tasks)                                       | La sessione CLI corrente               | Polling rapido mentre una sessione è aperta. Le attività vengono annullate quando esci.                                                                   |

<Tip>
  Quando scrivi prompt per attività pianificate, sii esplicito su cosa significhi il successo e cosa fare con i risultati. L'attività viene eseguita autonomamente, quindi non può fare domande di chiarimento. Ad esempio: "Review open PRs labeled `needs-review`, leave inline comments on any issues, and post a summary in the `#eng-reviews` Slack channel."
</Tip>

***

## Chiedere a Claude delle sue capacità

Claude ha accesso integrato alla sua documentazione e può rispondere a domande sulle sue stesse funzionalità e limitazioni.

### Domande di esempio

```text theme={null}
can Claude Code create pull requests?
```

```text theme={null}
how does Claude Code handle permissions?
```

```text theme={null}
what skills are available?
```

```text theme={null}
how do I use MCP with Claude Code?
```

```text theme={null}
how do I configure Claude Code for Amazon Bedrock?
```

```text theme={null}
what are the limitations of Claude Code?
```

<Note>
  Claude fornisce risposte basate sulla documentazione a queste domande. Per esempi eseguibili e dimostrazioni pratiche, fai riferimento alle sezioni di flusso di lavoro specifiche sopra.
</Note>

<Tip>
  Suggerimenti:

  * Claude ha sempre accesso alla documentazione più recente di Claude Code, indipendentemente dalla versione che stai utilizzando
  * Fai domande specifiche per ottenere risposte dettagliate
  * Claude può spiegare funzionalità complesse come integrazione MCP, configurazioni aziendali e flussi di lavoro avanzati
</Tip>

***

## Passaggi successivi

<CardGroup cols={2}>
  <Card title="Best practices" icon="lightbulb" href="/it/best-practices">
    Modelli per ottenere il massimo da Claude Code
  </Card>

  <Card title="Come funziona Claude Code" icon="gear" href="/it/how-claude-code-works">
    Comprendi il ciclo agentico e la gestione del contesto
  </Card>

  <Card title="Estendere Claude Code" icon="puzzle-piece" href="/it/features-overview">
    Aggiungi skills, hooks, MCP, subagent e plugin
  </Card>

  <Card title="Implementazione di riferimento" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
    Clona l'implementazione di riferimento del contenitore di sviluppo
  </Card>
</CardGroup>
