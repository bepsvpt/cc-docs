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

### Feedback utilizzando il comando `/feedback`

Se scegliete di inviarci feedback su Claude Code utilizzando il comando `/feedback`, potremmo utilizzare il vostro feedback per migliorare i nostri prodotti e servizi. I transcript condivisi tramite `/feedback` vengono conservati per 5 anni.

### Sondaggi sulla qualità della sessione

Quando vedete il prompt "Come sta andando Claude in questa sessione?" in Claude Code, rispondendo a questo sondaggio, inclusa la selezione di "Ignora", viene registrato solo il vostro voto. Non raccogliamo né archiviamo alcun transcript di conversazione, input, output o altri dati di sessione come parte del prompt di valutazione stesso. A differenza del feedback con pollice su/giù o dei report `/feedback`, questo sondaggio sulla qualità della sessione è una semplice metrica di soddisfazione del prodotto.

Dopo il prompt di valutazione, potete vedere una domanda di follow-up separata che chiede "Anthropic può guardare il transcript della vostra sessione per aiutarci a migliorare Claude Code?". Questo è un secondo passaggio facoltativo distinto dalla valutazione:

* **Sì**: carica il transcript della vostra conversazione, i transcript di qualsiasi subagent e il file di log della sessione non elaborato dal disco su Anthropic. I modelli di chiave API e token noti vengono oscurati prima del caricamento. Il codice sorgente, i contenuti dei file e altri contenuti della conversazione vengono caricati così come sono. I transcript condivisi vengono conservati fino a 6 mesi.
* **No**: rifiuta senza inviare nulla
* **Non chiedere più**: rifiuta e impedisce che questo follow-up appaia nelle sessioni future

Nulla viene caricato a meno che non selezioniate esplicitamente **Sì**. Le organizzazioni con [zero data retention](/it/zero-data-retention), o dove il feedback sui prodotti è disabilitato dalla politica dell'organizzazione, non vedono mai questo follow-up. Le vostre risposte a questo sondaggio, inclusi i transcript delle sessioni inviati dopo il prompt di valutazione, non influiscono sulle vostre preferenze di addestramento dei dati e non possono essere utilizzate per addestrare i nostri modelli di IA.

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
* Caching locale: i client di Claude Code archiviano i transcript delle sessioni localmente in testo semplice sotto `~/.claude/projects/` per 30 giorni per impostazione predefinita per abilitare la ripresa della sessione. Regolate il periodo con `cleanupPeriodDays`. Consultate [application data](/it/claude-directory#application-data) per sapere cosa viene archiviato e come cancellarlo.

Potete eliminare le singole sessioni di Claude Code sul web in qualsiasi momento. L'eliminazione di una sessione rimuove permanentemente i dati dell'evento della sessione. Per istruzioni su come eliminare le sessioni, consultate [Eliminare le sessioni](/it/claude-code-on-the-web#delete-sessions).

Scopri di più sulle pratiche di conservazione dei dati nel nostro [Privacy Center](https://privacy.anthropic.com/).

Per i dettagli completi, consultate i nostri [Termini di servizio commerciali](https://www.anthropic.com/legal/commercial-terms) (per gli utenti Team, Enterprise e API) o [Termini consumer](https://www.anthropic.com/legal/consumer-terms) (per gli utenti Free, Pro e Max) e [Informativa sulla privacy](https://www.anthropic.com/legal/privacy).

## Accesso ai dati

Per tutti gli utenti di prima parte, potete scoprire di più su quali dati vengono registrati per [Claude Code locale](#local-claude-code-data-flow-and-dependencies) e [Claude Code remoto](#cloud-execution-data-flow-and-dependencies). Le sessioni di [Remote Control](/it/remote-control) seguono il flusso di dati locale poiché tutta l'esecuzione avviene sulla vostra macchina. Si noti che per Claude Code remoto, Claude accede al repository in cui avviate la vostra sessione di Claude Code. Claude non accede ai repository che avete collegato ma in cui non avete avviato una sessione.

## Claude Code locale: flusso di dati e dipendenze

Il diagramma sottostante mostra come Claude Code si connette ai servizi esterni durante l'installazione e il funzionamento normale. Le linee continue indicano connessioni richieste, mentre le linee tratteggiate rappresentano flussi di dati facoltativi o avviati dall'utente.

<img src="https://mintcdn.com/claude-code/RcOyXc06Ja8cuvMZ/images/claude-code-data-flow.svg?fit=max&auto=format&n=RcOyXc06Ja8cuvMZ&q=85&s=b5be40abf333defe984993af89546c19" alt="Diagramma che mostra le connessioni esterne di Claude Code: install/update si connette al server di distribuzione e le richieste dell'utente si connettono ai servizi Anthropic inclusi Console auth, public-api e facoltativamente metrics, Sentry e bug reporting" width="720" height="520" data-path="images/claude-code-data-flow.svg" />

Claude Code viene eseguito localmente. Per interagire con l'LLM, Claude Code invia dati sulla rete. Questi dati includono tutti i prompt dell'utente e gli output del modello, crittografati in transito tramite TLS 1.2+. Claude Code è compatibile con la maggior parte dei VPN e dei proxy LLM più diffusi.

La crittografia a riposo dipende dal vostro provider di modelli:

| Provider               | Crittografia a riposo                                                                                                                                       |
| ---------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Anthropic API          | Crittografia del disco a livello di infrastruttura (AES-256). Abilitate [Zero Data Retention](/it/zero-data-retention) per nessuna persistenza lato server. |
| Amazon Bedrock         | AES-256 con chiavi gestite da AWS. Chiavi gestite dal cliente disponibili tramite AWS KMS.                                                                  |
| Google Cloud Vertex AI | Chiavi di crittografia gestite da Google. CMEK disponibile.                                                                                                 |
| Microsoft Foundry      | Le richieste vengono instradate all'infrastruttura Anthropic con crittografia del disco AES-256.                                                            |

Claude Code è costruito sulle API di Anthropic. Per i dettagli sui controlli di sicurezza della nostra API, incluse le nostre procedure di registrazione dell'API, consultate gli artefatti di conformità offerti nel [Anthropic Trust Center](https://trust.anthropic.com).

### Esecuzione nel cloud: flusso di dati e dipendenze

Quando si utilizza [Claude Code sul web](/it/claude-code-on-the-web), le sessioni vengono eseguite in macchine virtuali gestite da Anthropic invece che localmente. Negli ambienti cloud:

* **Archiviazione di codice e dati:** Il vostro repository viene clonato su una VM isolata. Il codice e i dati della sessione sono soggetti alle politiche di conservazione e utilizzo per il vostro tipo di account (consultate la sezione Conservazione dei dati sopra)
* **Credenziali:** L'autenticazione GitHub viene gestita tramite un proxy sicuro; le vostre credenziali GitHub non entrano mai nella sandbox
* **Traffico di rete:** Tutto il traffico in uscita passa attraverso un proxy di sicurezza per la registrazione di audit e la prevenzione degli abusi
* **Dati della sessione:** I prompt, le modifiche al codice e gli output seguono le stesse politiche sui dati dell'utilizzo locale di Claude Code

Per i dettagli sulla sicurezza dell'esecuzione nel cloud, consultate [Sicurezza](/it/security#cloud-execution-security).

## Servizi di telemetria

Claude Code si connette dalle macchine degli utenti ad Anthropic per registrare metriche operative come latenza, affidabilità e modelli di utilizzo. Questa registrazione non include alcun codice o percorso di file. I dati vengono crittografati in transito e a riposo. Per rinunciare alla telemetria, impostate la variabile di ambiente `DISABLE_TELEMETRY`.

Claude Code si connette dalle macchine degli utenti a Sentry per la registrazione degli errori operativi. I dati vengono crittografati in transito utilizzando TLS e a riposo utilizzando la crittografia AES a 256 bit. Scopri di più nella [documentazione sulla sicurezza di Sentry](https://sentry.io/security/). Per rinunciare alla registrazione degli errori, impostate la variabile di ambiente `DISABLE_ERROR_REPORTING`.

Quando gli utenti eseguono il comando `/feedback`, una copia della loro cronologia completa della conversazione incluso il codice viene inviata ad Anthropic. I dati vengono crittografati in transito via TLS. Facoltativamente, viene creato un problema GitHub nel repository pubblico. Per rinunciare, impostate la variabile di ambiente `DISABLE_FEEDBACK_COMMAND` su `1`.

## Comportamenti predefiniti per provider API

Per impostazione predefinita, la segnalazione degli errori, la telemetria e la segnalazione dei bug sono disabilitati quando si utilizza Bedrock, Vertex, Foundry o Claude Platform su AWS. I sondaggi sulla qualità della sessione e il controllo di sicurezza del dominio WebFetch sono eccezioni e vengono eseguiti indipendentemente dal provider. Potete rinunciare a tutto il traffico non essenziale, inclusi i sondaggi, contemporaneamente impostando `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. Questa variabile non influisce sul controllo WebFetch, che ha il suo proprio opt-out. Ecco i comportamenti predefiniti completi:

| Servizio                                        | Claude API                                                                                                            | Vertex API                                                                                                            | Bedrock API                                                                                                           | Foundry API                                                                                                           | Claude Platform su AWS                                                                                                |
| ----------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------- |
| **Anthropic (Metriche)**                        | Attivo per impostazione predefinita.<br />`DISABLE_TELEMETRY=1` per disabilitare.                                     | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_VERTEX` deve essere 1.                                  | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_BEDROCK` deve essere 1.                                 | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_FOUNDRY` deve essere 1.                                 | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_ANTHROPIC_AWS` deve essere 1.                           |
| **Sentry (Errori)**                             | Attivo per impostazione predefinita.<br />`DISABLE_ERROR_REPORTING=1` per disabilitare.                               | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_VERTEX` deve essere 1.                                  | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_BEDROCK` deve essere 1.                                 | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_FOUNDRY` deve essere 1.                                 | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_ANTHROPIC_AWS` deve essere 1.                           |
| **Claude API (report `/feedback`)**             | Attivo per impostazione predefinita.<br />`DISABLE_FEEDBACK_COMMAND=1` per disabilitare.                              | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_VERTEX` deve essere 1.                                  | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_BEDROCK` deve essere 1.                                 | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_FOUNDRY` deve essere 1.                                 | Disattivo per impostazione predefinita.<br />`CLAUDE_CODE_USE_ANTHROPIC_AWS` deve essere 1.                           |
| **Sondaggi sulla qualità della sessione**       | Attivo per impostazione predefinita.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` per disabilitare.                   | Attivo per impostazione predefinita.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` per disabilitare.                   | Attivo per impostazione predefinita.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` per disabilitare.                   | Attivo per impostazione predefinita.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` per disabilitare.                   | Attivo per impostazione predefinita.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` per disabilitare.                   |
| **Controllo di sicurezza del dominio WebFetch** | Attivo per impostazione predefinita.<br />`skipWebFetchPreflight: true` in [settings](/it/settings) per disabilitare. | Attivo per impostazione predefinita.<br />`skipWebFetchPreflight: true` in [settings](/it/settings) per disabilitare. | Attivo per impostazione predefinita.<br />`skipWebFetchPreflight: true` in [settings](/it/settings) per disabilitare. | Attivo per impostazione predefinita.<br />`skipWebFetchPreflight: true` in [settings](/it/settings) per disabilitare. | Attivo per impostazione predefinita.<br />`skipWebFetchPreflight: true` in [settings](/it/settings) per disabilitare. |

Tutte le variabili di ambiente possono essere controllate in `settings.json` (consultate [riferimento delle impostazioni](/it/settings)).

A partire dalla v2.1.126, quando una piattaforma host imposta `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`, le metriche sono attive per impostazione predefinita per Vertex, Bedrock e Foundry, e seguono l'opt-out standard `DISABLE_TELEMETRY`. La segnalazione degli errori Sentry e i report `/feedback` rimangono disattivi per impostazione predefinita su questi provider.

### Controllo di sicurezza del dominio WebFetch

Prima di recuperare un URL, lo strumento WebFetch invia il nome host richiesto a `api.anthropic.com` per verificarlo rispetto a un elenco di blocco della sicurezza mantenuto da Anthropic. Viene inviato solo il nome host, non l'URL completo, il percorso o il contenuto della pagina. I risultati vengono memorizzati nella cache per nome host per cinque minuti.

Questo controllo viene eseguito indipendentemente da quale provider di modelli utilizzate e non è influenzato da `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. Se la vostra rete blocca `api.anthropic.com`, le richieste WebFetch non riescono finché non consentite il dominio o non impostate `skipWebFetchPreflight: true` in [settings](/it/settings). La disabilitazione del controllo significa che WebFetch tenta di recuperare qualsiasi URL senza consultare l'elenco di blocco, quindi combinatelo con le [regole di autorizzazione `WebFetch`](/it/permissions#webfetch) se dovete limitare quali domini Claude può raggiungere.
