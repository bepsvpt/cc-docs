> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Eseguire prompt in base a una pianificazione

> Utilizzare /loop e gli strumenti di pianificazione cron per eseguire prompt ripetutamente, eseguire il polling dello stato o impostare promemoria una tantum all'interno di una sessione Claude Code.

<Note>
  Le attività pianificate richiedono Claude Code v2.1.72 o versione successiva. Controllare la versione con `claude --version`.
</Note>

Le attività pianificate consentono a Claude di rieseguire automaticamente un prompt a intervalli regolari. Utilizzarle per eseguire il polling di una distribuzione, monitorare una PR, controllare una compilazione a lunga esecuzione o ricordarsi di fare qualcosa più tardi nella sessione. Per reagire agli eventi man mano che si verificano invece di eseguire il polling, vedere [Channels](/it/channels): il vostro CI può inviare il fallimento direttamente nella sessione.

Le attività hanno ambito di sessione: vivono nel processo Claude Code corrente e scompaiono quando si esce. Per la pianificazione durevole che sopravvive ai riavvii, utilizzare [Routines](/it/routines), [Attività pianificate Desktop](/it/desktop-scheduled-tasks) o [GitHub Actions](/it/github-actions).

## Confrontare le opzioni di pianificazione

Claude Code offers three ways to schedule recurring work:

|                            | [Cloud](/en/routines)          | [Desktop](/en/desktop-scheduled-tasks) | [`/loop`](/en/scheduled-tasks)      |
| :------------------------- | :----------------------------- | :------------------------------------- | :---------------------------------- |
| Runs on                    | Anthropic cloud                | Your machine                           | Your machine                        |
| Requires machine on        | No                             | Yes                                    | Yes                                 |
| Requires open session      | No                             | No                                     | Yes                                 |
| Persistent across restarts | Yes                            | Yes                                    | Restored on `--resume` if unexpired |
| Access to local files      | No (fresh clone)               | Yes                                    | Yes                                 |
| MCP servers                | Connectors configured per task | [Config files](/en/mcp) and connectors | Inherits from session               |
| Permission prompts         | No (runs autonomously)         | Configurable per task                  | Inherits from session               |
| Customizable schedule      | Via `/schedule` in the CLI     | Yes                                    | Yes                                 |
| Minimum interval           | 1 hour                         | 1 minute                               | 1 minute                            |

<Tip>
  Use **cloud tasks** for work that should run reliably without your machine. Use **Desktop tasks** when you need access to local files and tools. Use **`/loop`** for quick polling during a session.
</Tip>

## Eseguire un prompt ripetutamente con /loop

Lo [skill bundled](/it/commands) `/loop` è il modo più rapido per eseguire un prompt ripetutamente mentre la sessione rimane aperta. Sia l'intervallo che il prompt sono facoltativi, e quello che fornite determina il comportamento del ciclo.

| Quello che fornite       | Esempio                     | Cosa accade                                                                                                                      |
| :----------------------- | :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| Intervallo e prompt      | `/loop 5m check the deploy` | Il vostro prompt viene eseguito su un [programma fisso](#run-on-a-fixed-interval)                                                |
| Solo prompt              | `/loop check the deploy`    | Il vostro prompt viene eseguito a un [intervallo scelto da Claude](#let-claude-choose-the-interval) ad ogni iterazione           |
| Solo intervallo, o nulla | `/loop`                     | Il [prompt di manutenzione integrato](#run-the-built-in-maintenance-prompt) viene eseguito, oppure il vostro `loop.md` se esiste |

Potete anche passare un altro comando come prompt, ad esempio `/loop 20m /review-pr 1234`, per rieseguire un flusso di lavoro confezionato ad ogni iterazione.

### Eseguire su un intervallo fisso

Quando fornite un intervallo, Claude lo converte in un'espressione cron, pianifica il processo e conferma la cadenza e l'ID del processo.

```text theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

L'intervallo può precedere il prompt come token nudo come `30m`, oppure seguirlo come clausola come `every 2 hours`. Le unità supportate sono `s` per secondi, `m` per minuti, `h` per ore e `d` per giorni.

I secondi vengono arrotondati al minuto più vicino poiché cron ha una granularità di un minuto. Gli intervalli che non si dividono uniformemente in un passo cron pulito, come `7m` o `90m`, vengono arrotondati all'intervallo più vicino che lo fa e Claude vi dice quale ha scelto.

### Lasciare che Claude scelga l'intervallo

Quando omettete l'intervallo, Claude ne sceglie uno dinamicamente invece di eseguire su un programma cron fisso. Dopo ogni iterazione sceglie un ritardo tra un minuto e un'ora in base a quello che ha osservato: attese brevi mentre una compilazione sta terminando o una PR è attiva, attese più lunghe quando non c'è nulla in sospeso. Il ritardo scelto e il motivo sono stampati alla fine di ogni iterazione.

L'esempio seguente controlla CI e i commenti di revisione, con Claude che attende più a lungo tra le iterazioni una volta che la PR diventa silenziosa:

```text theme={null}
/loop check whether CI passed and address any review comments
```

Quando chiedete un programma `/loop` dinamico, Claude potrebbe utilizzare direttamente lo [strumento Monitor](/it/tools-reference#monitor-tool). Monitor esegue uno script in background e trasmette ogni riga di output, il che evita completamente il polling ed è spesso più efficiente in termini di token e più reattivo rispetto alla riesecuzione di un prompt a intervalli.

Un ciclo pianificato dinamicamente appare nel vostro [elenco di attività pianificate](#manage-scheduled-tasks) come qualsiasi altra attività, quindi potete elencarla o annullarla nello stesso modo. Le [regole di jitter](#jitter) non si applicano ad esso, ma la [scadenza di sette giorni](#seven-day-expiry) sì: il ciclo termina automaticamente sette giorni dopo averlo avviato.

<Note>
  Su Bedrock, Vertex AI e Microsoft Foundry, un prompt senza intervallo viene eseguito su un programma fisso di 10 minuti.
</Note>

### Eseguire il prompt di manutenzione integrato

Quando omettete il prompt, Claude utilizza un prompt di manutenzione integrato invece di uno che fornite. Ad ogni iterazione lavora attraverso quanto segue, in ordine:

* continuare qualsiasi lavoro non terminato dalla conversazione
* prendersi cura della pull request del ramo corrente: commenti di revisione, esecuzioni CI non riuscite, conflitti di merge
* eseguire passaggi di pulizia come cacce ai bug o semplificazione quando non c'è nulla di altro in sospeso

Claude non avvia nuove iniziative al di fuori di tale ambito, e le azioni irreversibili come il push o l'eliminazione procedono solo quando continuano qualcosa che il trascritto ha già autorizzato.

```text theme={null}
/loop
```

Un `/loop` nudo esegue questo prompt a un [intervallo scelto dinamicamente](#let-claude-choose-the-interval). Aggiungete un intervallo, ad esempio `/loop 15m`, per eseguirlo su un programma fisso. Per sostituire il prompt integrato con il vostro predefinito, vedere [Personalizzare il prompt predefinito con loop.md](#customize-the-default-prompt-with-loop-md).

<Note>
  Su Bedrock, Vertex AI e Microsoft Foundry, `/loop` senza prompt stampa il messaggio di utilizzo invece di avviare il ciclo di manutenzione.
</Note>

### Personalizzare il prompt predefinito con loop.md

Un file `loop.md` sostituisce il prompt di manutenzione integrato con le vostre istruzioni. Definisce un singolo prompt predefinito per un `/loop` nudo, non un elenco di attività pianificate separate, ed è ignorato ogni volta che fornite un prompt sulla riga di comando. Per pianificare prompt aggiuntivi insieme ad esso, utilizzate `/loop <prompt>` o [chiedete direttamente a Claude](#manage-scheduled-tasks).

Claude cerca il file in due posizioni e utilizza il primo che trova.

| Percorso            | Ambito                                                                              |
| :------------------ | :---------------------------------------------------------------------------------- |
| `.claude/loop.md`   | A livello di progetto. Ha la precedenza quando entrambi i file esistono.            |
| `~/.claude/loop.md` | A livello di utente. Si applica in qualsiasi progetto che non definisce il proprio. |

Il file è Markdown semplice senza struttura richiesta. Scrivete come se steste digitando il prompt `/loop` direttamente. L'esempio seguente mantiene un ramo di rilascio sano:

```markdown title=".claude/loop.md" theme={null}
Check the `release/next` PR. If CI is red, pull the failing job log,
diagnose, and push a minimal fix. If new review comments have arrived,
address each one and resolve the thread. If everything is green and
quiet, say so in one line.
```

Le modifiche a `loop.md` hanno effetto alla successiva iterazione, quindi potete perfezionare le istruzioni mentre un ciclo è in esecuzione. Quando nessun `loop.md` esiste in nessuna posizione, il ciclo ritorna al prompt di manutenzione integrato. Mantenete il file conciso: il contenuto oltre 25.000 byte viene troncato.

## Impostare un promemoria una tantum

Per promemoria una tantum, descrivete quello che volete in linguaggio naturale invece di utilizzare `/loop`. Claude pianifica un'attività a fuoco singolo che si elimina dopo l'esecuzione.

```text theme={null}
remind me at 3pm to push the release branch
```

```text theme={null}
in 45 minutes, check whether the integration tests passed
```

Claude fissa l'ora di attivazione a un minuto e un'ora specifici utilizzando un'espressione cron e conferma quando si attiverà.

## Gestire le attività pianificate

Chiedete a Claude in linguaggio naturale di elencare o annullare le attività, oppure fate riferimento direttamente agli strumenti sottostanti.

```text theme={null}
what scheduled tasks do I have?
```

```text theme={null}
cancel the deploy check job
```

Dietro le quinte, Claude utilizza questi strumenti:

| Strumento    | Scopo                                                                                                                                 |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| `CronCreate` | Pianificare una nuova attività. Accetta un'espressione cron a 5 campi, il prompt da eseguire e se ricorre o si attiva una sola volta. |
| `CronList`   | Elencare tutte le attività pianificate con i loro ID, pianificazioni e prompt.                                                        |
| `CronDelete` | Annullare un'attività per ID.                                                                                                         |

Ogni attività pianificata ha un ID di 8 caratteri che potete passare a `CronDelete`. Una sessione può contenere fino a 50 attività pianificate contemporaneamente.

## Come vengono eseguite le attività pianificate

Lo scheduler controlla ogni secondo le attività dovute e le accoda a bassa priorità. Un prompt pianificato si attiva tra i vostri turni, non mentre Claude sta rispondendo. Se Claude è occupato quando un'attività scade, il prompt attende fino al termine del turno corrente.

Tutti i tempi vengono interpretati nel vostro fuso orario locale. Un'espressione cron come `0 9 * * *` significa le 9 del mattino ovunque stiate eseguendo Claude Code, non UTC.

### Jitter

Per evitare che ogni sessione colpisca l'API nello stesso momento del muro, lo scheduler aggiunge un piccolo offset deterministico ai tempi di attivazione:

* Le attività ricorrenti si attivano fino al 10% del loro periodo in ritardo, limitato a 15 minuti. Un processo orario potrebbe attivarsi da `:00` a `:06`.
* Le attività una tantum pianificate per l'inizio o la fine dell'ora si attivano fino a 90 secondi prima.

L'offset è derivato dall'ID dell'attività, quindi la stessa attività ottiene sempre lo stesso offset. Se il timing esatto è importante, scegliete un minuto che non sia `:00` o `:30`, ad esempio `3 9 * * *` invece di `0 9 * * *`, e il jitter una tantum non si applicherà.

### Scadenza di sette giorni

Le attività ricorrenti scadono automaticamente 7 giorni dopo la creazione. L'attività si attiva un'ultima volta, quindi si elimina. Questo limita il tempo di esecuzione di un ciclo dimenticato. Se avete bisogno che un'attività ricorrente duri più a lungo, annullate e ricreate prima che scada, oppure utilizzate [Routines](/it/routines) o [Attività pianificate Desktop](/it/desktop-scheduled-tasks) per la pianificazione durevole.

## Riferimento dell'espressione cron

`CronCreate` accetta espressioni cron standard a 5 campi: `minute hour day-of-month month day-of-week`. Tutti i campi supportano caratteri jolly (`*`), valori singoli (`5`), step (`*/15`), intervalli (`1-5`) e elenchi separati da virgole (`1,15,30`).

| Esempio        | Significato                              |
| :------------- | :--------------------------------------- |
| `*/5 * * * *`  | Ogni 5 minuti                            |
| `0 * * * *`    | Ogni ora in punto                        |
| `7 * * * *`    | Ogni ora alle 7 minuti passati           |
| `0 9 * * *`    | Ogni giorno alle 9 del mattino locale    |
| `0 9 * * 1-5`  | Giorni feriali alle 9 del mattino locale |
| `30 14 15 3 *` | 15 marzo alle 14:30 locale               |

Day-of-week utilizza `0` o `7` per domenica fino a `6` per sabato. La sintassi estesa come `L`, `W`, `?` e gli alias dei nomi come `MON` o `JAN` non sono supportati.

Quando sia day-of-month che day-of-week sono vincolati, una data corrisponde se uno dei campi corrisponde. Questo segue la semantica standard di vixie-cron.

## Disabilitare le attività pianificate

Impostare `CLAUDE_CODE_DISABLE_CRON=1` nel vostro ambiente per disabilitare completamente lo scheduler. Gli strumenti cron e `/loop` diventano non disponibili e tutte le attività già pianificate smettono di attivarsi. Vedere [Variabili di ambiente](/it/env-vars) per l'elenco completo dei flag di disabilitazione.

## Limitazioni

La pianificazione con ambito di sessione ha vincoli intrinseci:

* Le attività si attivano solo mentre Claude Code è in esecuzione e inattivo. La chiusura del terminale o l'uscita dalla sessione annulla tutto.
* Nessun recupero per attivazioni perse. Se l'ora pianificata di un'attività passa mentre Claude è occupato in una richiesta a lunga esecuzione, si attiva una sola volta quando Claude diventa inattivo, non una volta per ogni intervallo perso.
* Nessuna persistenza tra i riavvii. Il riavvio di Claude Code cancella tutte le attività con ambito di sessione.

Per l'automazione basata su cron che deve essere eseguita senza supervisione:

* [Routines](/it/routines): eseguite su infrastruttura gestita da Anthropic su un programma, tramite chiamata API o su eventi GitHub
* [GitHub Actions](/it/github-actions): utilizzare un trigger `schedule` in CI
* [Attività pianificate Desktop](/it/desktop-scheduled-tasks): eseguite localmente sulla vostra macchina
