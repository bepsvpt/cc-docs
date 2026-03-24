> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Utilizzo dei dati

> Scopri le politiche di utilizzo dei dati di Anthropic per Claude

## Politiche sui dati

### Politica di addestramento dei dati

**Utenti consumer (piani Free, Pro e Max)**:
Vi diamo la possibilità di consentire l'utilizzo dei vostri dati per migliorare i futuri modelli Claude. Addestreremo nuovi modelli utilizzando i dati degli account Free, Pro e Max quando questa impostazione è attiva (incluso quando utilizzate Claude Code da questi account).

**Utenti commerciali**: (piani Team ed Enterprise, API, piattaforme di terze parti e Claude Gov) mantengono le politiche esistenti: Anthropic non addestra modelli generativi utilizzando codice o prompt inviati a Claude Code secondo i termini commerciali, a meno che il cliente non abbia scelto di fornirci i propri dati per il miglioramento del modello (ad esempio, il [Development Partner Program](https://support.claude.com/en/articles/11174108-about-the-development-partner-program)).

### Development Partner Program

Se vi iscrivete esplicitamente a metodi per fornirci materiali su cui addestrare, come tramite il [Development Partner Program](https://support.claude.com/en/articles/11174108-about-the-development-partner-program), potremmo utilizzare tali materiali forniti per addestrare i nostri modelli. Un amministratore dell'organizzazione può iscriversi esplicitamente al Development Partner Program per la propria organizzazione. Si noti che questo programma è disponibile solo per l'API di Anthropic di prima parte e non per gli utenti di Bedrock o Vertex.

### Feedback utilizzando il comando `/bug`

Se scegliete di inviarci feedback su Claude Code utilizzando il comando `/bug`, potremmo utilizzare il vostro feedback per migliorare i nostri prodotti e servizi. I transcript condivisi tramite `/bug` vengono conservati per 5 anni.

### Sondaggi sulla qualità della sessione

Quando vedete il prompt "Come sta andando Claude in questa sessione?" in Claude Code, rispondendo a questo sondaggio (inclusa la selezione di "Ignora"), viene registrato solo il vostro voto numerico (1, 2, 3 o ignora). Non raccogliamo né archiviamo alcun transcript di conversazione, input, output o altri dati di sessione come parte di questo sondaggio. A differenza del feedback con pollice su/giù o dei report `/bug`, questo sondaggio sulla qualità della sessione è una semplice metrica di soddisfazione del prodotto. Le vostre risposte a questo sondaggio non influiscono sulle vostre preferenze di addestramento dei dati e non possono essere utilizzate per addestrare i nostri modelli di IA.

Per disabilitare questi sondaggi, impostate `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`. Il sondaggio viene anche disabilitato quando `DISABLE_TELEMETRY` o `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` è impostato. Per controllare la frequenza invece di disabilitare, impostate [`feedbackSurveyRate`](/it/settings#available-settings) nel vostro file di impostazioni su una probabilità tra `0` e `1`.

### Conservazione dei dati

Anthropic conserva i dati di Claude Code in base al tipo di account e alle preferenze dell'utente.

**Utenti consumer (piani Free, Pro e Max)**:

* Utenti che consentono l'utilizzo dei dati per il miglioramento del modello: periodo di conservazione di 5 anni per supportare lo sviluppo del modello e i miglioramenti della sicurezza
* Utenti che non consentono l'utilizzo dei dati per il miglioramento del modello: periodo di conservazione di 30 giorni
* Le impostazioni sulla privacy possono essere modificate in qualsiasi momento su [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls).

**Utenti commerciali (Team, Enterprise e API)**:

* Standard: periodo di conservazione di 30 giorni
* [Zero data retention](/it/zero-data-retention): disponibile per Claude Code su Claude for Enterprise. ZDR è abilitato su base per organizzazione; ogni nuova organizzazione deve avere ZDR abilitato separatamente dal vostro team di account
* Caching locale: i client di Claude Code possono archiviare le sessioni localmente fino a 30 giorni per abilitare la ripresa della sessione (configurabile)

Potete eliminare le singole sessioni di Claude Code sul web in qualsiasi momento. L'eliminazione di una sessione rimuove permanentemente i dati dell'evento della sessione. Per istruzioni su come eliminare le sessioni, consultate [Gestione delle sessioni](/it/claude-code-on-the-web#managing-sessions).

Scopri di più sulle pratiche di conservazione dei dati nel nostro [Privacy Center](https://privacy.anthropic.com/).

Per i dettagli completi, consultate i nostri [Termini di servizio commerciali](https://www.anthropic.com/legal/commercial-terms) (per gli utenti Team, Enterprise e API) o [Termini consumer](https://www.anthropic.com/legal/consumer-terms) (per gli utenti Free, Pro e Max) e [Informativa sulla privacy](https://www.anthropic.com/legal/privacy).

## Accesso ai dati

Per tutti gli utenti di prima parte, potete scoprire di più su quali dati vengono registrati per [Claude Code locale](#local-claude-code-data-flow-and-dependencies) e [Claude Code remoto](#cloud-execution-data-flow-and-dependencies). Le sessioni di [Remote Control](/it/remote-control) seguono il flusso di dati locale poiché tutta l'esecuzione avviene sulla vostra macchina. Si noti che per Claude Code remoto, Claude accede al repository in cui avviate la vostra sessione di Claude Code. Claude non accede ai repository che avete collegato ma in cui non avete avviato una sessione.

## Claude Code locale: flusso di dati e dipendenze

Il diagramma sottostante mostra come Claude Code si connette ai servizi esterni durante l'installazione e il funzionamento normale. Le linee continue indicano connessioni richieste, mentre le linee tratteggiate rappresentano flussi di dati facoltativi o avviati dall'utente.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/claude-code-data-flow.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=b3f71c69d743bff63343207dfb7ad6ce" alt="Diagramma che mostra le connessioni esterne di Claude Code: install/update si connette a NPM e le richieste dell'utente si connettono ai servizi Anthropic inclusi Console auth, public-api e facoltativamente Statsig, Sentry e bug reporting" width="720" height="520" data-path="images/claude-code-data-flow.svg" />

Claude Code viene installato da [NPM](https://www.npmjs.com/package/@anthropic-ai/claude-code). Claude Code viene eseguito localmente. Per interagire con l'LLM, Claude Code invia dati sulla rete. Questi dati includono tutti i prompt dell'utente e gli output del modello. I dati vengono crittografati in transito tramite TLS e non vengono crittografati a riposo. Claude Code è compatibile con la maggior parte dei VPN e dei proxy LLM più diffusi.

Claude Code è costruito sulle API di Anthropic. Per i dettagli sui controlli di sicurezza della nostra API, incluse le nostre procedure di registrazione dell'API, consultate gli artefatti di conformità offerti nel [Anthropic Trust Center](https://trust.anthropic.com).

### Esecuzione nel cloud: flusso di dati e dipendenze

Quando si utilizza [Claude Code sul web](/it/claude-code-on-the-web), le sessioni vengono eseguite in macchine virtuali gestite da Anthropic invece che localmente. Negli ambienti cloud:

* **Archiviazione di codice e dati:** Il vostro repository viene clonato su una VM isolata. Il codice e i dati della sessione sono soggetti alle politiche di conservazione e utilizzo per il vostro tipo di account (consultate la sezione Conservazione dei dati sopra)
* **Credenziali:** L'autenticazione GitHub viene gestita tramite un proxy sicuro; le vostre credenziali GitHub non entrano mai nella sandbox
* **Traffico di rete:** Tutto il traffico in uscita passa attraverso un proxy di sicurezza per la registrazione di audit e la prevenzione degli abusi
* **Dati della sessione:** I prompt, le modifiche al codice e gli output seguono le stesse politiche sui dati dell'utilizzo locale di Claude Code

Per i dettagli sulla sicurezza dell'esecuzione nel cloud, consultate [Sicurezza](/it/security#cloud-execution-security).

## Servizi di telemetria

Claude Code si connette dalle macchine degli utenti al servizio Statsig per registrare metriche operative come latenza, affidabilità e modelli di utilizzo. Questa registrazione non include alcun codice o percorso di file. I dati vengono crittografati in transito utilizzando TLS e a riposo utilizzando la crittografia AES a 256 bit. Scopri di più nella [documentazione sulla sicurezza di Statsig](https://www.statsig.com/trust/security). Per rinunciare alla telemetria di Statsig, impostate la variabile di ambiente `DISABLE_TELEMETRY`.

Claude Code si connette dalle macchine degli utenti a Sentry per la registrazione degli errori operativi. I dati vengono crittografati in transito utilizzando TLS e a riposo utilizzando la crittografia AES a 256 bit. Scopri di più nella [documentazione sulla sicurezza di Sentry](https://sentry.io/security/). Per rinunciare alla registrazione degli errori, impostate la variabile di ambiente `DISABLE_ERROR_REPORTING`.

Quando gli utenti eseguono il comando `/bug`, una copia della loro cronologia completa della conversazione incluso il codice viene inviata ad Anthropic. I dati vengono crittografati in transito e a riposo. Facoltativamente, viene creato un problema Github nel nostro repository pubblico. Per rinunciare alla segnalazione di bug, impostate la variabile di ambiente `DISABLE_BUG_COMMAND`.

## Comportamenti predefiniti per provider API

Per impostazione predefinita, la segnalazione degli errori, la telemetria e la segnalazione dei bug sono disabilitati quando si utilizza Bedrock, Vertex o Foundry. I sondaggi sulla qualità della sessione sono l'eccezione e vengono visualizzati indipendentemente dal provider. Potete rinunciare a tutto il traffico non essenziale, inclusi i sondaggi, contemporaneamente impostando `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. Ecco i comportamenti predefiniti completi:

| Servizio                                  | Claude API                                                                                          | Vertex API                                                                                          | Bedrock API                                                                                         | Foundry API                                                                                         |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------- |
| **Statsig (Metriche)**                    | Attivo per impostazione predefinita.<br />`DISABLE_TELEMETRY=1` per disabilitare.                   | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_VERTEX` deve essere 1.                | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_BEDROCK` deve essere 1.               | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_FOUNDRY` deve essere 1.               |
| **Sentry (Errori)**                       | Attivo per impostazione predefinita.<br />`DISABLE_ERROR_REPORTING=1` per disabilitare.             | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_VERTEX` deve essere 1.                | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_BEDROCK` deve essere 1.               | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_FOUNDRY` deve essere 1.               |
| **Claude API (report `/bug`)**            | Attivo per impostazione predefinita.<br />`DISABLE_BUG_COMMAND=1` per disabilitare.                 | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_VERTEX` deve essere 1.                | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_BEDROCK` deve essere 1.               | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_FOUNDRY` deve essere 1.               |
| **Sondaggi sulla qualità della sessione** | Attivo per impostazione predefinita.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` per disabilitare. | Attivo per impostazione predefinita.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` per disabilitare. | Attivo per impostazione predefinita.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` per disabilitare. | Attivo per impostazione predefinita.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` per disabilitare. |

Tutte le variabili di ambiente possono essere controllate in `settings.json` ([scopri di più](/it/settings)).
