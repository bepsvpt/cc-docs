> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> Configura revisioni automatiche dei PR che rilevano errori logici, vulnerabilità di sicurezza e regressioni utilizzando l'analisi multi-agente della tua intera codebase

<Note>
  Code Review è in anteprima di ricerca, disponibile per gli abbonamenti [Teams e Enterprise](https://claude.ai/admin-settings/claude-code). Non è disponibile per le organizzazioni con [Zero Data Retention](/it/zero-data-retention) abilitato.
</Note>

Code Review analizza le tue pull request di GitHub e pubblica i risultati come commenti inline sulle righe di codice in cui ha trovato problemi. Una flotta di agenti specializzati esamina le modifiche al codice nel contesto della tua intera codebase, cercando errori logici, vulnerabilità di sicurezza, edge case non gestiti e regressioni sottili.

I risultati sono contrassegnati per gravità e non approvano o bloccano il tuo PR, quindi i flussi di lavoro di revisione esistenti rimangono intatti. Puoi regolare cosa Claude segnala aggiungendo un file `CLAUDE.md` o `REVIEW.md` al tuo repository.

Per eseguire Claude nella tua infrastruttura CI invece di questo servizio gestito, vedi [GitHub Actions](/it/github-actions) o [GitLab CI/CD](/it/gitlab-ci-cd).

Questa pagina copre:

* [Come funzionano le revisioni](#how-reviews-work)
* [Setup](#set-up-code-review)
* [Personalizzazione delle revisioni](#customize-reviews) con `CLAUDE.md` e `REVIEW.md`
* [Prezzi](#pricing)

## Come funzionano le revisioni

Una volta che un amministratore [abilita Code Review](#set-up-code-review) per la tua organizzazione, le revisioni vengono eseguite automaticamente quando una pull request si apre o si aggiorna. Più agenti analizzano il diff e il codice circostante in parallelo sull'infrastruttura Anthropic. Ogni agente cerca una classe diversa di problema, quindi un passaggio di verifica controlla i candidati rispetto al comportamento effettivo del codice per filtrare i falsi positivi. I risultati vengono deduplicati, classificati per gravità e pubblicati come commenti inline sulle righe specifiche in cui sono stati trovati i problemi. Se non vengono trovati problemi, Claude pubblica un breve commento di conferma sul PR.

Le revisioni si scalano in costo con la dimensione e la complessità del PR, completandosi in media in 20 minuti. Gli amministratori possono monitorare l'attività di revisione e la spesa tramite il [dashboard di analisi](#view-usage).

### Livelli di gravità

Ogni risultato è contrassegnato con un livello di gravità:

| Marcatore | Gravità       | Significato                                                             |
| :-------- | :------------ | :---------------------------------------------------------------------- |
| 🔴        | Normale       | Un bug che dovrebbe essere corretto prima del merge                     |
| 🟡        | Nit           | Un problema minore, vale la pena correggerlo ma non bloccante           |
| 🟣        | Pre-esistente | Un bug che esiste nella codebase ma non è stato introdotto da questo PR |

I risultati includono una sezione di ragionamento esteso comprimibile che puoi espandere per capire perché Claude ha segnalato il problema e come ha verificato il problema.

### Cosa controlla Code Review

Per impostazione predefinita, Code Review si concentra sulla correttezza: bug che interromperebbero la produzione, non preferenze di formattazione o copertura di test mancante. Puoi espandere cosa controlla [aggiungendo file di guida](#customize-reviews) al tuo repository.

## Configura Code Review

Un amministratore abilita Code Review una volta per l'organizzazione e seleziona quali repository includere.

<Steps>
  <Step title="Apri le impostazioni di amministrazione di Claude Code">
    Vai a [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) e trova la sezione Code Review. Hai bisogno dell'accesso amministratore alla tua organizzazione Claude e del permesso di installare GitHub Apps nella tua organizzazione GitHub.
  </Step>

  <Step title="Avvia il setup">
    Fai clic su **Setup**. Questo avvia il flusso di installazione dell'app GitHub.
  </Step>

  <Step title="Installa l'app GitHub di Claude">
    Segui i prompt per installare l'app GitHub di Claude nella tua organizzazione GitHub. L'app richiede questi permessi del repository:

    * **Contents**: lettura e scrittura
    * **Issues**: lettura e scrittura
    * **Pull requests**: lettura e scrittura

    Code Review utilizza l'accesso in lettura ai contenuti e l'accesso in scrittura alle pull request. L'insieme di permessi più ampio supporta anche [GitHub Actions](/it/github-actions) se lo abiliti in seguito.
  </Step>

  <Step title="Seleziona i repository">
    Scegli quali repository abilitare per Code Review. Se non vedi un repository, assicurati di aver dato all'app GitHub di Claude l'accesso durante l'installazione. Puoi aggiungere altri repository in seguito.
  </Step>

  <Step title="Imposta i trigger di revisione per repository">
    Dopo il completamento del setup, la sezione Code Review mostra i tuoi repository in una tabella. Per ogni repository, usa il dropdown per scegliere quando vengono eseguite le revisioni:

    * **After PR creation only**: la revisione viene eseguita una volta quando un PR viene aperto o contrassegnato come pronto per la revisione
    * **After every push to PR branch**: la revisione viene eseguita ad ogni push, rilevando nuovi problemi mentre il PR evolve e risolvendo automaticamente i thread quando correggi i problemi segnalati

    La revisione ad ogni push esegue più revisioni e costa di più. Inizia con la creazione del PR e passa a on-push per i repository in cui desideri una copertura continua e la pulizia automatica dei thread.
  </Step>
</Steps>

La tabella dei repository mostra anche il costo medio per revisione per ogni repository in base all'attività recente. Usa il menu delle azioni della riga per attivare o disattivare Code Review per repository, o per rimuovere completamente un repository.

Per verificare il setup, apri un PR di test. Un check run denominato **Claude Code Review** appare entro pochi minuti. Se non appare, conferma che il repository è elencato nelle tue impostazioni di amministrazione e che l'app GitHub di Claude ha accesso ad esso.

## Personalizza le revisioni

Code Review legge due file dal tuo repository per guidare cosa segnala. Entrambi sono additivi rispetto ai controlli di correttezza predefiniti:

* **`CLAUDE.md`**: istruzioni di progetto condivise che Claude Code utilizza per tutti i compiti, non solo le revisioni. Usalo quando la guida si applica anche alle sessioni interattive di Claude Code.
* **`REVIEW.md`**: guida solo per la revisione, letta esclusivamente durante le revisioni del codice. Usalo per le regole che riguardano strettamente cosa segnalare o saltare durante la revisione e che ingombrerebbero il tuo `CLAUDE.md` generale.

### CLAUDE.md

Code Review legge i file `CLAUDE.md` del tuo repository e tratta le violazioni appena introdotte come risultati a livello di nit. Questo funziona bidirezionalmente: se il tuo PR modifica il codice in modo da rendere obsoleta un'affermazione `CLAUDE.md`, Claude segnala che i documenti devono essere aggiornati.

Claude legge i file `CLAUDE.md` a ogni livello della tua gerarchia di directory, quindi le regole nel `CLAUDE.md` di una sottodirectory si applicano solo ai file sotto quel percorso. Vedi la [documentazione della memoria](/it/memory) per ulteriori informazioni su come funziona `CLAUDE.md`.

Per la guida specifica della revisione che non desideri applicare alle sessioni generali di Claude Code, usa [`REVIEW.md`](#review-md) invece.

### REVIEW\.md

Aggiungi un file `REVIEW.md` alla radice del tuo repository per le regole specifiche della revisione. Usalo per codificare:

* Linee guida di stile dell'azienda o del team: "preferisci i ritorni anticipati ai condizionali annidati"
* Convenzioni specifiche del linguaggio o del framework non coperte dai linter
* Cose che Claude dovrebbe sempre segnalare: "qualsiasi nuova rotta API deve avere un test di integrazione"
* Cose che Claude dovrebbe saltare: "non commentare la formattazione nel codice generato sotto `/gen/`"

Esempio di `REVIEW.md`:

```markdown  theme={null}
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
| PRs reviewed         | Conteggio giornaliero delle pull request revisionate nell'intervallo di tempo selezionato                                    |
| Cost weekly          | Spesa settimanale su Code Review                                                                                             |
| Feedback             | Conteggio dei commenti di revisione che sono stati risolti automaticamente perché uno sviluppatore ha affrontato il problema |
| Repository breakdown | Conteggi per repository dei PR revisionati e dei commenti risolti                                                            |

La tabella dei repository nelle impostazioni di amministrazione mostra anche il costo medio per revisione per ogni repository.

## Prezzi

Code Review viene fatturato in base all'utilizzo dei token. Le revisioni costano in media \$15-25, scalando con la dimensione del PR, la complessità della codebase e quanti problemi richiedono verifica. L'utilizzo di Code Review viene fatturato separatamente tramite [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) e non conta rispetto all'utilizzo incluso nel tuo piano.

Il trigger di revisione che scegli influisce sul costo totale:

* **After PR creation only**: viene eseguito una volta per PR
* **After every push**: viene eseguito ad ogni commit, moltiplicando il costo per il numero di push

I costi appaiono sulla tua fattura Anthropic indipendentemente dal fatto che la tua organizzazione utilizzi AWS Bedrock o Google Vertex AI per altre funzionalità di Claude Code. Per impostare un limite di spesa mensile per Code Review, vai a [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) e configura il limite per il servizio Claude Code Review.

Monitora la spesa tramite il grafico dei costi settimanali in [analytics](#view-usage) o la colonna del costo medio per repository nelle impostazioni di amministrazione.

## Risorse correlate

Code Review è progettato per funzionare insieme al resto di Claude Code. Se desideri eseguire revisioni localmente prima di aprire un PR, hai bisogno di una configurazione self-hosted, o desideri approfondire come `CLAUDE.md` modella il comportamento di Claude in tutti gli strumenti, queste pagine sono buoni prossimi passi:

* [Plugins](/it/discover-plugins): sfoglia il marketplace dei plugin, incluso un plugin `code-review` per eseguire revisioni on-demand localmente prima di eseguire il push
* [GitHub Actions](/it/github-actions): esegui Claude nei tuoi flussi di lavoro GitHub Actions per l'automazione personalizzata oltre la revisione del codice
* [GitLab CI/CD](/it/gitlab-ci-cd): integrazione Claude self-hosted per le pipeline GitLab
* [Memory](/it/memory): come funzionano i file `CLAUDE.md` in Claude Code
* [Analytics](/it/analytics): traccia l'utilizzo di Claude Code oltre la revisione del codice
