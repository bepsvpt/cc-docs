> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Eseguire prompt in base a una pianificazione

> Utilizzare /loop e gli strumenti di pianificazione cron per eseguire prompt ripetutamente, eseguire il polling dello stato o impostare promemoria una tantum all'interno di una sessione Claude Code.

<Note>
  Le attività pianificate richiedono Claude Code v2.1.72 o versione successiva. Controllare la versione con `claude --version`.
</Note>

Le attività pianificate consentono a Claude di rieseguire automaticamente un prompt a intervalli regolari. Utilizzarle per eseguire il polling di una distribuzione, monitorare una PR, controllare una compilazione a lunga esecuzione o ricordarsi di fare qualcosa più tardi nella sessione. Per reagire agli eventi man mano che si verificano invece di eseguire il polling, vedere [Channels](/it/channels): il vostro CI può inviare il fallimento direttamente nella sessione.

Le attività hanno ambito di sessione: vivono nel processo Claude Code corrente e scompaiono quando si esce. Per la pianificazione durevole che sopravvive ai riavvii, utilizzare [Cloud](/it/web-scheduled-tasks) o [Desktop](/it/desktop#schedule-recurring-tasks) attività pianificate, oppure [GitHub Actions](/it/github-actions).

## Confrontare le opzioni di pianificazione

Claude Code offers three ways to schedule recurring work:

|                            | [Cloud](/en/routines)          | [Desktop](/en/desktop-scheduled-tasks) | [`/loop`](/en/scheduled-tasks) |
| :------------------------- | :----------------------------- | :------------------------------------- | :----------------------------- |
| Runs on                    | Anthropic cloud                | Your machine                           | Your machine                   |
| Requires machine on        | No                             | Yes                                    | Yes                            |
| Requires open session      | No                             | No                                     | Yes                            |
| Persistent across restarts | Yes                            | Yes                                    | No (session-scoped)            |
| Access to local files      | No (fresh clone)               | Yes                                    | Yes                            |
| MCP servers                | Connectors configured per task | [Config files](/en/mcp) and connectors | Inherits from session          |
| Permission prompts         | No (runs autonomously)         | Configurable per task                  | Inherits from session          |
| Customizable schedule      | Via `/schedule` in the CLI     | Yes                                    | Yes                            |
| Minimum interval           | 1 hour                         | 1 minute                               | 1 minute                       |

<Tip>
  Use **cloud tasks** for work that should run reliably without your machine. Use **Desktop tasks** when you need access to local files and tools. Use **`/loop`** for quick polling during a session.
</Tip>

## Pianificare un prompt ricorrente con /loop

Lo [skill bundled](/it/skills#bundled-skills) `/loop` è il modo più rapido per pianificare un prompt ricorrente. Passare un intervallo facoltativo e un prompt, e Claude configura un processo cron che si attiva in background mentre la sessione rimane aperta.

```text theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

Claude analizza l'intervallo, lo converte in un'espressione cron, pianifica il processo e conferma la cadenza e l'ID del processo.

### Sintassi dell'intervallo

Gli intervalli sono facoltativi. È possibile iniziare con essi, terminarli o ometterli completamente.

| Form                    | Example                               | Parsed interval            |
| :---------------------- | :------------------------------------ | :------------------------- |
| Leading token           | `/loop 30m check the build`           | ogni 30 minuti             |
| Trailing `every` clause | `/loop check the build every 2 hours` | ogni 2 ore                 |
| No interval             | `/loop check the build`               | predefinito ogni 10 minuti |

Le unità supportate sono `s` per secondi, `m` per minuti, `h` per ore e `d` per giorni. I secondi vengono arrotondati al minuto più vicino poiché cron ha una granularità di un minuto. Gli intervalli che non si dividono uniformemente nella loro unità, come `7m` o `90m`, vengono arrotondati all'intervallo più pulito e Claude vi dice quale ha scelto.

### Eseguire un ciclo su un altro comando

Il prompt pianificato può essere esso stesso un'invocazione di comando o skill. Questo è utile per rieseguire un flusso di lavoro che avete già confezionato.

```text theme={null}
/loop 20m /review-pr 1234
```

Ogni volta che il processo si attiva, Claude esegue `/review-pr 1234` come se lo aveste digitato.

## Impostare un promemoria una tantum

Per promemoria una tantum, descrivete quello che volete in linguaggio naturale invece di usare `/loop`. Claude pianifica un'attività a fuoco singolo che si elimina dopo l'esecuzione.

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

| Tool         | Purpose                                                                                                                               |
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

Le attività ricorrenti scadono automaticamente 7 giorni dopo la creazione. L'attività si attiva un'ultima volta, quindi si elimina. Questo limita il tempo di esecuzione di un ciclo dimenticato. Se avete bisogno che un'attività ricorrente duri più a lungo, annullate e ricreate prima che scada, oppure utilizzate [Attività pianificate Cloud](/it/web-scheduled-tasks) o [Attività pianificate Desktop](/it/desktop#schedule-recurring-tasks) per la pianificazione durevole.

## Riferimento dell'espressione cron

`CronCreate` accetta espressioni cron standard a 5 campi: `minute hour day-of-month month day-of-week`. Tutti i campi supportano caratteri jolly (`*`), valori singoli (`5`), step (`*/15`), intervalli (`1-5`) e elenchi separati da virgole (`1,15,30`).

| Example        | Meaning                                  |
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

* [Attività pianificate Cloud](/it/web-scheduled-tasks): eseguite su infrastruttura gestita da Anthropic
* [GitHub Actions](/it/github-actions): utilizzare un trigger `schedule` in CI
* [Attività pianificate Desktop](/it/desktop#schedule-recurring-tasks): eseguite localmente sulla vostra macchina
