> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> Configura revisioni automatiche dei PR che rilevano errori logici, vulnerabilità di sicurezza e regressioni utilizzando l'analisi multi-agente dell'intero codebase

<Note>
  Code Review è in anteprima di ricerca, disponibile per gli abbonamenti [Teams e Enterprise](https://claude.ai/admin-settings/claude-code). Non è disponibile per le organizzazioni con [Zero Data Retention](/it/zero-data-retention) abilitato.
</Note>

Code Review analizza i tuoi pull request su GitHub e pubblica i risultati come commenti inline sulle righe di codice dove ha trovato problemi. Una flotta di agenti specializzati esamina i cambiamenti del codice nel contesto dell'intero codebase, cercando errori logici, vulnerabilità di sicurezza, edge case interrotti e regressioni sottili.

I risultati sono contrassegnati per gravità e non approvano o bloccano il tuo PR, quindi i flussi di lavoro di revisione esistenti rimangono intatti. Puoi regolare cosa Claude segnala aggiungendo un file `CLAUDE.md` o `REVIEW.md` al tuo repository.

Per eseguire Claude nella tua infrastruttura CI invece di questo servizio gestito, vedi [GitHub Actions](/it/github-actions) o [GitLab CI/CD](/it/gitlab-ci-cd). Per i repository su un'istanza GitHub self-hosted, vedi [GitHub Enterprise Server](/it/github-enterprise-server).

Questa pagina copre:

* [Come funzionano le revisioni](#how-reviews-work)
* [Configurazione](#set-up-code-review)
* [Attivazione manuale delle revisioni](#manually-trigger-reviews) con `@claude review` e `@claude review once`
* [Personalizzazione delle revisioni](#customize-reviews) con `CLAUDE.md` e `REVIEW.md`
* [Prezzi](#pricing)
* [Risoluzione dei problemi](#troubleshooting) esecuzioni non riuscite e commenti mancanti

## Come funzionano le revisioni

Una volta che un amministratore [abilita Code Review](#set-up-code-review) per la tua organizzazione, le revisioni si attivano quando un PR si apre, ad ogni push, o quando richiesto manualmente, a seconda del comportamento configurato del repository. Commentando `@claude review` [avvia le revisioni su un PR](#manually-trigger-reviews) in qualsiasi modalità.

Quando una revisione viene eseguita, più agenti analizzano il diff e il codice circostante in parallelo sull'infrastruttura Anthropic. Ogni agente cerca una classe diversa di problema, quindi un passaggio di verifica controlla i candidati rispetto al comportamento effettivo del codice per filtrare i falsi positivi. I risultati vengono deduplicati, classificati per gravità e pubblicati come commenti inline sulle righe specifiche dove sono stati trovati i problemi. Se non vengono trovati problemi, Claude pubblica un breve commento di conferma sul PR.

Le revisioni si scalano in costo con la dimensione e la complessità del PR, completandosi in media in 20 minuti. Gli amministratori possono monitorare l'attività di revisione e la spesa tramite il [dashboard di analisi](#view-usage).

### Livelli di gravità

Ogni risultato è contrassegnato con un livello di gravità:

| Marcatore | Gravità       | Significato                                                           |
| :-------- | :------------ | :-------------------------------------------------------------------- |
| 🔴        | Importante    | Un bug che dovrebbe essere corretto prima del merge                   |
| 🟡        | Nit           | Un problema minore, vale la pena correggerlo ma non bloccante         |
| 🟣        | Pre-esistente | Un bug che esiste nel codebase ma non è stato introdotto da questo PR |

I risultati includono una sezione di ragionamento esteso comprimibile che puoi espandere per capire perché Claude ha segnalato il problema e come ha verificato il problema.

### Output del check run

Oltre ai commenti di revisione inline, ogni revisione popola il check run **Claude Code Review** che appare insieme ai tuoi check CI. Espandi il suo link **Details** per vedere un riepilogo di ogni risultato in un unico posto, ordinato per gravità:

| Gravità       | File:Riga                 | Problema                                                                                      |
| ------------- | ------------------------- | --------------------------------------------------------------------------------------------- |
| 🔴 Importante | `src/auth/session.ts:142` | L'aggiornamento del token corre in parallelo con il logout, lasciando sessioni stantie attive |
| 🟡 Nit        | `src/auth/session.ts:88`  | `parseExpiry` restituisce silenziosamente 0 su input malformato                               |

Ogni risultato appare anche come un'annotazione nella scheda **Files changed**, contrassegnato direttamente sulle righe diff rilevanti. I risultati importanti vengono visualizzati con un marcatore rosso, i nit con un avviso giallo e i bug pre-esistenti con un avviso grigio. Le annotazioni e la tabella di gravità vengono scritte nel check run indipendentemente dai commenti di revisione inline, quindi rimangono disponibili anche se GitHub rifiuta un commento inline su una riga che si è spostata.

Il check run si completa sempre con una conclusione neutra, quindi non blocca mai il merge attraverso le regole di protezione del ramo. Se vuoi bloccare i merge sui risultati di Code Review, leggi il breakdown della gravità dall'output del check run nel tuo CI. L'ultima riga del testo Details è un commento leggibile da macchina che il tuo flusso di lavoro può analizzare con `gh` e jq:

```bash theme={null}
gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID \
  --jq '.output.text | split("bughunter-severity: ")[1] | split(" -->")[0] | fromjson'
```

Questo restituisce un oggetto JSON con conteggi per gravità, ad esempio `{"normal": 2, "nit": 1, "pre_existing": 0}`. La chiave `normal` contiene il conteggio dei risultati Importanti; un valore diverso da zero significa che Claude ha trovato almeno un bug che vale la pena correggere prima del merge.

### Cosa controlla Code Review

Per impostazione predefinita, Code Review si concentra sulla correttezza: bug che interromperebbero la produzione, non preferenze di formattazione o copertura di test mancante. Puoi espandere cosa controlla [aggiungendo file di guida](#customize-reviews) al tuo repository.

## Configura Code Review

Un amministratore abilita Code Review una volta per l'organizzazione e seleziona quali repository includere.

<Steps>
  <Step title="Apri le impostazioni di amministrazione di Claude Code">
    Vai a [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) e trova la sezione Code Review. Hai bisogno dell'accesso amministratore alla tua organizzazione Claude e del permesso di installare GitHub App nella tua organizzazione GitHub.
  </Step>

  <Step title="Avvia la configurazione">
    Fai clic su **Setup**. Questo inizia il flusso di installazione dell'app GitHub.
  </Step>

  <Step title="Installa l'app GitHub di Claude">
    Segui i prompt per installare l'app GitHub di Claude nella tua organizzazione GitHub. L'app richiede questi permessi del repository:

    * **Contents**: lettura e scrittura
    * **Issues**: lettura e scrittura
    * **Pull requests**: lettura e scrittura

    Code Review utilizza l'accesso in lettura ai contenuti e l'accesso in scrittura ai pull request. L'insieme di permessi più ampio supporta anche [GitHub Actions](/it/github-actions) se lo abiliti in seguito.
  </Step>

  <Step title="Seleziona i repository">
    Scegli quali repository abilitare per Code Review. Se non vedi un repository, assicurati di aver dato all'app GitHub di Claude l'accesso durante l'installazione. Puoi aggiungere altri repository in seguito.
  </Step>

  <Step title="Imposta i trigger di revisione per repository">
    Dopo il completamento della configurazione, la sezione Code Review mostra i tuoi repository in una tabella. Per ogni repository, utilizza il dropdown **Review Behavior** per scegliere quando vengono eseguite le revisioni:

    * **Once after PR creation**: la revisione viene eseguita una volta quando un PR viene aperto o contrassegnato come pronto per la revisione
    * **After every push**: la revisione viene eseguita ad ogni push al ramo PR, catturando nuovi problemi mentre il PR si evolve e risolvendo automaticamente i thread quando correggi i problemi segnalati
    * **Manual**: le revisioni iniziano solo quando qualcuno [commenta `@claude review` o `@claude review once` su un PR](#manually-trigger-reviews); `@claude review` sottoscrive anche il PR alle revisioni su push successivi

    La revisione ad ogni push esegue il maggior numero di revisioni e costa di più. La modalità manuale è utile per i repository ad alto traffico dove vuoi optare per PR specifici nella revisione, o per iniziare a revisionare i tuoi PR solo quando sono pronti.
  </Step>
</Steps>

La tabella dei repository mostra anche il costo medio per revisione per ogni repository in base all'attività recente. Utilizza il menu delle azioni della riga per attivare o disattivare Code Review per repository, o per rimuovere completamente un repository.

Per verificare la configurazione, apri un PR di test. Se hai scelto un trigger automatico, un check run denominato **Claude Code Review** appare entro pochi minuti. Se hai scelto Manual, commenta `@claude review` sul PR per avviare la prima revisione. Se non appare alcun check run, conferma che il repository è elencato nelle tue impostazioni di amministrazione e che l'app GitHub di Claude ha accesso ad esso.

## Attiva manualmente le revisioni

Due comandi di commento avviano una revisione su richiesta. Entrambi funzionano indipendentemente dal trigger configurato del repository, quindi puoi usarli per optare per PR specifici nella revisione in modalità Manual o per ottenere una re-revisione immediata in altre modalità.

| Comando               | Cosa fa                                                                                        |
| :-------------------- | :--------------------------------------------------------------------------------------------- |
| `@claude review`      | Avvia una revisione e sottoscrive il PR alle revisioni attivate da push da quel momento in poi |
| `@claude review once` | Avvia una singola revisione senza sottoscrivere il PR ai push futuri                           |

Usa `@claude review once` quando vuoi feedback sullo stato attuale di un PR ma non vuoi che ogni push successivo comporti una revisione. Questo è utile per i PR di lunga durata con push frequenti, o quando vuoi un secondo parere una tantum senza cambiare il comportamento di revisione del PR.

Affinché uno dei due comandi attivi una revisione:

* Postalo come commento PR di primo livello, non come commento inline su una riga diff
* Metti il comando all'inizio del commento, con `once` sulla stessa riga se stai usando la forma one-shot
* Devi avere accesso come proprietario, membro o collaboratore al repository
* Il PR deve essere aperto

A differenza dei trigger automatici, i trigger manuali vengono eseguiti su PR bozza, poiché una richiesta esplicita segnala che vuoi la revisione ora indipendentemente dallo stato di bozza.

Se una revisione è già in esecuzione su quel PR, la richiesta viene messa in coda fino al completamento della revisione in corso. Puoi monitorare l'avanzamento tramite il check run sul PR.

## Personalizza le revisioni

Code Review legge due file dal tuo repository per guidare cosa segnala. Entrambi sono additivi oltre ai controlli di correttezza predefiniti:

* **`CLAUDE.md`**: istruzioni di progetto condivise che Claude Code utilizza per tutti i compiti, non solo le revisioni. Usalo quando la guida si applica anche alle sessioni interattive di Claude Code.
* **`REVIEW.md`**: guida solo per la revisione, letta esclusivamente durante le revisioni del codice. Usalo per regole che riguardano strettamente cosa segnalare o saltare durante la revisione e che ingombrerebbero il tuo `CLAUDE.md` generale.

### CLAUDE.md

Code Review legge i file `CLAUDE.md` del tuo repository e tratta le violazioni appena introdotte come risultati a livello di nit. Questo funziona bidirezionalmente: se il tuo PR cambia il codice in un modo che rende una dichiarazione `CLAUDE.md` obsoleta, Claude segnala che i documenti devono essere aggiornati anche loro.

Claude legge i file `CLAUDE.md` a ogni livello della gerarchia di directory, quindi le regole nel `CLAUDE.md` di una sottodirectory si applicano solo ai file sotto quel percorso. Vedi la [documentazione della memoria](/it/memory) per ulteriori informazioni su come funziona `CLAUDE.md`.

Per una guida specifica della revisione che non vuoi applicata alle sessioni generali di Claude Code, usa [`REVIEW.md`](#review-md) invece.

### REVIEW\.md

Aggiungi un file `REVIEW.md` alla radice del tuo repository per regole specifiche della revisione. Usalo per codificare:

* Linee guida di stile aziendali o di team: "preferisci i ritorni anticipati ai condizionali annidati"
* Convenzioni specifiche del linguaggio o del framework non coperte dai linter
* Cose che Claude dovrebbe sempre segnalare: "qualsiasi nuova rotta API deve avere un test di integrazione"
* Cose che Claude dovrebbe saltare: "non commentare la formattazione nel codice generato sotto `/gen/`"

Esempio di `REVIEW.md`:

```markdown theme={null}
# Linee guida per la revisione del codice

## Controlla sempre
- I nuovi endpoint API hanno test di integrazione corrispondenti
- Le migrazioni del database sono retrocompatibili
- I messaggi di errore non perdono dettagli interni agli utenti

## Stile
- Preferisci le istruzioni `match` ai controlli `isinstance` concatenati
- Usa la registrazione strutturata, non l'interpolazione di stringhe f nelle chiamate di log

## Salta
- File generati sotto `src/gen/`
- Modifiche solo di formattazione nei file `*.lock`
```

Claude scopre automaticamente `REVIEW.md` alla radice del repository. Nessuna configurazione necessaria.

## Visualizza l'utilizzo

Vai a [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) per vedere l'attività di Code Review in tutta la tua organizzazione. Il dashboard mostra:

| Sezione              | Cosa mostra                                                                                                                  |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| PRs reviewed         | Conteggio giornaliero dei pull request revisionati nell'intervallo di tempo selezionato                                      |
| Cost weekly          | Spesa settimanale su Code Review                                                                                             |
| Feedback             | Conteggio dei commenti di revisione che sono stati risolti automaticamente perché uno sviluppatore ha affrontato il problema |
| Repository breakdown | Conteggi per repository dei PR revisionati e dei commenti risolti                                                            |

La tabella dei repository nelle impostazioni di amministrazione mostra anche il costo medio per revisione per ogni repository.

## Prezzi

Code Review viene fatturato in base all'utilizzo dei token. Ogni revisione costa in media \$15-25, scalando con la dimensione del PR, la complessità del codebase e quanti problemi richiedono verifica. L'utilizzo di Code Review viene fatturato separatamente tramite [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) e non conta rispetto all'utilizzo incluso nel tuo piano.

Il trigger di revisione che scegli influisce sul costo totale:

* **Once after PR creation**: viene eseguito una volta per PR
* **After every push**: viene eseguito ad ogni push, moltiplicando il costo per il numero di push
* **Manual**: nessuna revisione fino a quando qualcuno non commenta `@claude review` su un PR

In qualsiasi modalità, commentando `@claude review` [opta il PR nelle revisioni attivate da push](#manually-trigger-reviews), quindi il costo aggiuntivo si accumula per push dopo quel commento. Per eseguire una singola revisione senza sottoscrivere ai push futuri, commenta `@claude review once` invece.

I costi appaiono sulla tua fattura Anthropic indipendentemente dal fatto che la tua organizzazione utilizzi AWS Bedrock o Google Vertex AI per altre funzionalità di Claude Code. Per impostare un limite di spesa mensile per Code Review, vai a [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) e configura il limite per il servizio Claude Code Review.

Monitora la spesa tramite il grafico dei costi settimanali in [analytics](#view-usage) o la colonna del costo medio per repository nelle impostazioni di amministrazione.

## Risoluzione dei problemi

Le esecuzioni di revisione sono best-effort. Un'esecuzione non riuscita non blocca mai il tuo PR, ma non si ritenta nemmeno automaticamente. Questa sezione copre come recuperare da un'esecuzione non riuscita e dove cercare quando il check run segnala problemi che non riesci a trovare.

### Riattiva una revisione non riuscita o scaduta

Quando l'infrastruttura di revisione incontra un errore interno o supera il limite di tempo, il check run si completa con un titolo di **Code review encountered an error** o **Code review timed out**. La conclusione è ancora neutra, quindi nulla blocca il tuo merge, ma non vengono pubblicati risultati.

Per eseguire di nuovo la revisione, commenta `@claude review once` sul PR. Questo avvia una revisione nuova senza sottoscrivere il PR ai push futuri. Se il PR è già sottoscritto alle revisioni attivate da push, fare un push di un nuovo commit avvia anche una nuova revisione.

Il pulsante **Re-run** nella scheda Checks di GitHub non riattiva Code Review. Usa il comando di commento o un nuovo push invece.

### Trova problemi che non vengono visualizzati come commenti inline

Se il titolo del check run dice che sono stati trovati problemi ma non vedi commenti di revisione inline sul diff, cerca in questi altri luoghi dove vengono visualizzati i risultati:

* **Check run Details**: fai clic su **Details** accanto al check Claude Code Review nella scheda Checks. La tabella di gravità elenca ogni risultato con il suo file, riga e riepilogo indipendentemente dal fatto che il commento inline sia stato accettato.
* **Files changed annotations**: apri la scheda **Files changed** sul PR. I risultati vengono visualizzati come annotazioni allegate direttamente alle righe diff, separate dai commenti di revisione.
* **Review body**: se hai fatto un push al PR mentre una revisione era in esecuzione, alcuni risultati potrebbero fare riferimento a righe che non esistono più nel diff attuale. Questi appaiono sotto un'intestazione **Additional findings** nel testo del corpo della revisione piuttosto che come commenti inline.

## Risorse correlate

Code Review è progettato per funzionare insieme al resto di Claude Code. Se vuoi eseguire revisioni localmente prima di aprire un PR, hai bisogno di una configurazione self-hosted, o vuoi approfondire come `CLAUDE.md` modella il comportamento di Claude in tutti gli strumenti, queste pagine sono buoni prossimi passi:

* [Plugins](/it/discover-plugins): sfoglia il marketplace dei plugin, incluso un plugin `code-review` per eseguire revisioni on-demand localmente prima di fare push
* [GitHub Actions](/it/github-actions): esegui Claude nei tuoi flussi di lavoro GitHub Actions per l'automazione personalizzata oltre la revisione del codice
* [GitLab CI/CD](/it/gitlab-ci-cd): integrazione Claude self-hosted per le pipeline GitLab
* [Memory](/it/memory): come funzionano i file `CLAUDE.md` in Claude Code
* [Analytics](/it/analytics): traccia l'utilizzo di Claude Code oltre la revisione del codice
