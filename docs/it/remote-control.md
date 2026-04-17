> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Continua le sessioni locali da qualsiasi dispositivo con Remote Control

> Continua una sessione locale di Claude Code dal tuo telefono, tablet o da qualsiasi browser utilizzando Remote Control. Funziona con claude.ai/code e l'app Claude per dispositivi mobili.

<Note>
  Remote Control è disponibile su tutti i piani. Su Team e Enterprise, è disabilitato per impostazione predefinita fino a quando un amministratore non abilita l'interruttore Remote Control nelle [impostazioni di amministrazione di Claude Code](https://claude.ai/admin-settings/claude-code).
</Note>

Remote Control connette [claude.ai/code](https://claude.ai/code) o l'app Claude per [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) e [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) a una sessione di Claude Code in esecuzione sulla tua macchina. Avvia un'attività alla tua scrivania, quindi riprendi dal tuo telefono sul divano o da un browser su un altro computer.

Quando avvii una sessione Remote Control sulla tua macchina, Claude continua a funzionare localmente per tutto il tempo, quindi nulla si sposta nel cloud. Con Remote Control puoi:

* **Utilizzare il tuo ambiente locale completo da remoto**: il tuo filesystem, i [server MCP](/it/mcp), gli strumenti e la configurazione del progetto rimangono disponibili
* **Lavorare da entrambe le superfici contemporaneamente**: la conversazione rimane sincronizzata su tutti i dispositivi connessi, quindi puoi inviare messaggi dal tuo terminale, browser e telefono in modo intercambiabile
* **Sopravvivere alle interruzioni**: se il tuo laptop va in sospensione o la tua rete si interrompe, la sessione si riconnette automaticamente quando la tua macchina torna online

A differenza di [Claude Code sul web](/it/claude-code-on-the-web), che funziona su infrastrutture cloud, le sessioni Remote Control vengono eseguite direttamente sulla tua macchina e interagiscono con il tuo filesystem locale. Le interfacce web e mobile sono solo una finestra in quella sessione locale.

<Note>
  Remote Control richiede Claude Code v2.1.51 o successivo. Controlla la tua versione con `claude --version`.
</Note>

Questa pagina copre la configurazione, come avviare e connettersi alle sessioni, e come Remote Control si confronta con Claude Code sul web.

## Requisiti

Prima di utilizzare Remote Control, conferma che il tuo ambiente soddisfi queste condizioni:

* **Abbonamento**: disponibile su piani Pro, Max, Team e Enterprise. Le chiavi API non sono supportate. Su Team e Enterprise, un amministratore deve prima abilitare l'interruttore Remote Control nelle [impostazioni di amministrazione di Claude Code](https://claude.ai/admin-settings/claude-code).
* **Autenticazione**: esegui `claude` e utilizza `/login` per accedere tramite claude.ai se non l'hai già fatto.
* **Fiducia dell'area di lavoro**: esegui `claude` nella directory del tuo progetto almeno una volta per accettare la finestra di dialogo di fiducia dell'area di lavoro.

## Avvia una sessione Remote Control

Puoi avviare una sessione Remote Control dalla CLI o dall'estensione VS Code. La CLI offre tre modalità di invocazione; VS Code utilizza il comando `/remote-control`.

<Tabs>
  <Tab title="Modalità server">
    Accedi alla directory del tuo progetto ed esegui:

    ```bash theme={null}
    claude remote-control
    ```

    Il processo rimane in esecuzione nel tuo terminale in modalità server, in attesa di connessioni remote. Visualizza un URL di sessione che puoi utilizzare per [connetterti da un altro dispositivo](#connect-from-another-device), e puoi premere la barra spaziatrice per mostrare un codice QR per un accesso rapido dal tuo telefono. Mentre una sessione remota è attiva, il terminale mostra lo stato della connessione e l'attività dello strumento.

    Flag disponibili:

    | Flag                                            | Descrizione                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
    | ----------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `--name "My Project"`                           | Imposta un titolo di sessione personalizzato visibile nell'elenco delle sessioni su claude.ai/code.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
    | `--remote-control-session-name-prefix <prefix>` | Prefisso per i nomi di sessione generati automaticamente quando non è impostato un nome esplicito. Per impostazione predefinita è il nome host della tua macchina, producendo nomi come `myhost-graceful-unicorn`. Imposta `CLAUDE_REMOTE_CONTROL_SESSION_NAME_PREFIX` per lo stesso effetto.                                                                                                                                                                                                                                                                                                                                   |
    | `--spawn <mode>`                                | Come il server crea le sessioni.<br />• `same-dir` (predefinito): tutte le sessioni condividono la directory di lavoro corrente, quindi possono entrare in conflitto se modificano gli stessi file.<br />• `worktree`: ogni sessione su richiesta ottiene il proprio [git worktree](/it/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees). Richiede un repository git.<br />• `session`: modalità a sessione singola. Serve esattamente una sessione e rifiuta connessioni aggiuntive. Impostato solo all'avvio.<br />Premi `w` durante l'esecuzione per attivare/disattivare tra `same-dir` e `worktree`. |
    | `--capacity <N>`                                | Numero massimo di sessioni simultanee. Il valore predefinito è 32. Non può essere utilizzato con `--spawn=session`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
    | `--verbose`                                     | Mostra log dettagliati di connessione e sessione.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
    | `--sandbox` / `--no-sandbox`                    | Abilita o disabilita il [sandboxing](/it/sandboxing) per l'isolamento del filesystem e della rete. Disabilitato per impostazione predefinita.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
  </Tab>

  <Tab title="Sessione interattiva">
    Per avviare una normale sessione interattiva di Claude Code con Remote Control abilitato, utilizza il flag `--remote-control` (o `--rc`):

    ```bash theme={null}
    claude --remote-control
    ```

    Facoltativamente passa un nome per la sessione:

    ```bash theme={null}
    claude --remote-control "My Project"
    ```

    Questo ti dà una sessione interattiva completa nel tuo terminale che puoi anche controllare da claude.ai o dall'app Claude. A differenza di `claude remote-control` (modalità server), puoi digitare messaggi localmente mentre la sessione è anche disponibile da remoto.
  </Tab>

  <Tab title="Da una sessione esistente">
    Se sei già in una sessione di Claude Code e vuoi continuarla da remoto, utilizza il comando `/remote-control` (o `/rc`):

    ```text theme={null}
    /remote-control
    ```

    Passa un nome come argomento per impostare un titolo di sessione personalizzato:

    ```text theme={null}
    /remote-control My Project
    ```

    Questo avvia una sessione Remote Control che mantiene la cronologia della conversazione corrente e visualizza un URL di sessione e un codice QR che puoi utilizzare per [connetterti da un altro dispositivo](#connect-from-another-device). I flag `--verbose`, `--sandbox` e `--no-sandbox` non sono disponibili con questo comando.
  </Tab>

  <Tab title="VS Code">
    Nell'[estensione VS Code di Claude Code](/it/vs-code), digita `/remote-control` o `/rc` nella casella del prompt, oppure apri il menu dei comandi con `/` e selezionalo. Richiede Claude Code v2.1.79 o successivo.

    ```text theme={null}
    /remote-control
    ```

    Un banner appare sopra la casella del prompt mostrando lo stato della connessione. Una volta connesso, fai clic su **Open in browser** nel banner per andare direttamente alla sessione, oppure trovala nell'elenco delle sessioni su [claude.ai/code](https://claude.ai/code). L'URL della sessione è anche pubblicato nella conversazione.

    Per disconnetterti, fai clic sull'icona di chiusura sul banner o esegui `/remote-control` di nuovo.

    A differenza della CLI, il comando VS Code non accetta un argomento di nome e non visualizza un codice QR. Il titolo della sessione è derivato dalla cronologia della conversazione o dal primo prompt.
  </Tab>
</Tabs>

### Connettiti da un altro dispositivo

Una volta che una sessione Remote Control è attiva, hai alcuni modi per connetterti da un altro dispositivo:

* **Apri l'URL della sessione** in qualsiasi browser per andare direttamente alla sessione su [claude.ai/code](https://claude.ai/code).
* **Scansiona il codice QR** mostrato accanto all'URL della sessione per aprirlo direttamente nell'app Claude. Con `claude remote-control`, premi la barra spaziatrice per attivare/disattivare la visualizzazione del codice QR.
* **Apri [claude.ai/code](https://claude.ai/code) o l'app Claude** e trova la sessione per nome nell'elenco delle sessioni. Le sessioni Remote Control mostrano un'icona di computer con un punto di stato verde quando sono online.

Il titolo della sessione remota viene scelto in questo ordine:

1. Il nome che hai passato a `--name`, `--remote-control`, o `/remote-control`
2. Il titolo che hai impostato con `/rename`
3. L'ultimo messaggio significativo nella cronologia della conversazione esistente
4. Un nome generato automaticamente come `myhost-graceful-unicorn`, dove `myhost` è il nome host della tua macchina o il prefisso che hai impostato con `--remote-control-session-name-prefix`

Se non hai impostato un nome esplicito, il titolo si aggiorna per riflettere il tuo prompt una volta che ne invii uno.

Se l'ambiente ha già una sessione attiva, ti verrà chiesto se continuarla o avviarne una nuova.

Se non hai ancora l'app Claude, utilizza il comando `/mobile` all'interno di Claude Code per visualizzare un codice QR di download per [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) o [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).

### Abilita Remote Control per tutte le sessioni

Per impostazione predefinita, Remote Control si attiva solo quando esegui esplicitamente `claude remote-control`, `claude --remote-control`, o `/remote-control`. Per abilitarlo automaticamente per ogni sessione interattiva, esegui `/config` all'interno di Claude Code e imposta **Enable Remote Control for all sessions** su `true`. Impostalo di nuovo su `false` per disabilitarlo.

Con questa impostazione attiva, ogni processo Claude Code interattivo registra una sessione remota. Se esegui più istanze, ognuna ottiene il proprio ambiente e sessione. Per eseguire più sessioni simultanee da un singolo processo, utilizza invece la [modalità server](#start-a-remote-control-session).

## Connessione e sicurezza

La tua sessione locale di Claude Code effettua solo richieste HTTPS in uscita e non apre mai porte in ingresso sulla tua macchina. Quando avvii Remote Control, si registra con l'API Anthropic e esegue il polling per il lavoro. Quando ti connetti da un altro dispositivo, il server instrada i messaggi tra il client web o mobile e la tua sessione locale su una connessione in streaming.

Tutto il traffico viaggia attraverso l'API Anthropic su TLS, lo stesso trasporto di sicurezza di qualsiasi sessione di Claude Code. La connessione utilizza più credenziali di breve durata, ognuna limitata a un singolo scopo e con scadenza indipendente.

## Remote Control vs Claude Code sul web

Remote Control e [Claude Code sul web](/it/claude-code-on-the-web) utilizzano entrambi l'interfaccia claude.ai/code. La differenza chiave è dove viene eseguita la sessione: Remote Control viene eseguito sulla tua macchina, quindi i tuoi server MCP locali, strumenti e configurazione del progetto rimangono disponibili. Claude Code sul web viene eseguito nell'infrastruttura cloud gestita da Anthropic.

Utilizza Remote Control quando sei nel mezzo di un lavoro locale e vuoi continuare da un altro dispositivo. Utilizza Claude Code sul web quando vuoi avviare un'attività senza alcuna configurazione locale, lavorare su un repository che non hai clonato, o eseguire più attività in parallelo.

## Notifiche push mobili

Quando Remote Control è attivo, Claude può inviare notifiche push al tuo telefono.

Claude decide quando inviare una notifica. Tipicamente ne invia una quando un'attività a lunga esecuzione termina o quando ha bisogno di una decisione da te per continuare. Puoi anche richiedere una notifica nel tuo prompt, ad esempio `notify me when the tests finish`. Oltre all'interruttore on/off qui sotto, non c'è configurazione per evento.

<Note>
  Le notifiche push mobili richiedono Claude Code v2.1.110 o successivo.
</Note>

Per configurare le notifiche push mobili:

<Steps>
  <Step title="Installa l'app Claude per dispositivi mobili">
    Scarica l'app Claude per [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) o [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).
  </Step>

  <Step title="Accedi con il tuo account Claude Code">
    Utilizza lo stesso account e organizzazione che usi per Claude Code nel terminale.
  </Step>

  <Step title="Consenti le notifiche">
    Accetta il prompt di autorizzazione delle notifiche dal sistema operativo.
  </Step>

  <Step title="Abilita push in Claude Code">
    Nel tuo terminale, esegui `/config` e abilita **Push when Claude decides**.
  </Step>
</Steps>

Se le notifiche non arrivano:

* Se `/config` mostra **No mobile registered**, apri l'app Claude sul tuo telefono in modo che possa aggiornare il suo token push. L'avviso si cancella la prossima volta che Remote Control si connette.
* Su iOS, le modalità Focus e i riepiloghi delle notifiche possono sopprimere o ritardare le notifiche push. Controlla Impostazioni → Notifiche → Claude.
* Su Android, l'ottimizzazione aggressiva della batteria può ritardare la consegna. Escludi l'app Claude dall'ottimizzazione della batteria nelle impostazioni di sistema.

## Limitazioni

* **Una sessione remota per processo interattivo**: al di fuori della modalità server, ogni istanza di Claude Code supporta una sessione remota alla volta. Utilizza la [modalità server](#start-a-remote-control-session) per eseguire più sessioni simultanee da un singolo processo.
* **Il processo locale deve continuare a funzionare**: Remote Control viene eseguito come processo locale. Se chiudi il terminale, esci da VS Code, o altrimenti interrompi il processo `claude`, la sessione termina.
* **Interruzione di rete prolungata**: se la tua macchina è accesa ma non riesce a raggiungere la rete per più di circa 10 minuti, la sessione scade e il processo esce. Esegui di nuovo `claude remote-control` per avviare una nuova sessione.
* **Ultraplan disconnette Remote Control**: avviare una sessione [ultraplan](/it/ultraplan) disconnette qualsiasi sessione Remote Control attiva perché entrambe le funzioni occupano l'interfaccia claude.ai/code e solo una può essere connessa alla volta.

## Risoluzione dei problemi

### "Remote Control requires a claude.ai subscription"

Non sei autenticato con un account claude.ai. Esegui `claude auth login` e scegli l'opzione claude.ai. Se `ANTHROPIC_API_KEY` è impostato nel tuo ambiente, annulla l'impostazione prima.

### "Remote Control requires a full-scope login token"

Sei autenticato con un token di lunga durata da `claude setup-token` o dalla variabile di ambiente `CLAUDE_CODE_OAUTH_TOKEN`. Questi token sono limitati solo all'inferenza e non possono stabilire sessioni Remote Control. Esegui `claude auth login` per autenticarti con un token di sessione a scopo completo.

### "Unable to determine your organization for Remote Control eligibility"

Le informazioni dell'account memorizzate nella cache sono obsolete o incomplete. Esegui `claude auth login` per aggiornarlo.

### "Remote Control is not yet enabled for your account"

Il controllo di idoneità può fallire con determinate variabili di ambiente presenti:

* `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` o `DISABLE_TELEMETRY`: annulla l'impostazione e riprova.
* `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX`, o `CLAUDE_CODE_USE_FOUNDRY`: Remote Control richiede l'autenticazione claude.ai e non funziona con provider di terze parti.

Se nessuno di questi è impostato, esegui `/logout` quindi `/login` per aggiornare.

### "Remote Control is disabled by your organization's policy"

Questo errore ha tre cause distinte. Esegui prima `/status` per vedere quale metodo di accesso e abbonamento stai utilizzando.

* **Sei autenticato con una chiave API o un account Console**: Remote Control richiede OAuth claude.ai. Esegui `/login` e scegli l'opzione claude.ai. Se `ANTHROPIC_API_KEY` è impostato nel tuo ambiente, annulla l'impostazione.
* **Il tuo amministratore di Team o Enterprise non l'ha abilitato**: Remote Control è disabilitato per impostazione predefinita su questi piani. Un amministratore può abilitarlo su [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) attivando l'interruttore **Remote Control**. Questa è un'impostazione organizzativa lato server, non una chiave di [impostazioni gestite](/it/permissions#managed-only-settings).
* **L'interruttore di amministrazione è disattivato**: la tua organizzazione ha una configurazione di conservazione dei dati o conformità incompatibile con Remote Control. Questo non può essere modificato dal pannello di amministrazione. Contatta il supporto Anthropic per discutere le opzioni.

### "Remote credentials fetch failed"

Claude Code non ha potuto ottenere una credenziale di breve durata dall'API Anthropic per stabilire la connessione. Esegui di nuovo con `--verbose` per vedere l'errore completo:

```bash theme={null}
claude remote-control --verbose
```

Cause comuni:

* Non sei connesso: esegui `claude` e utilizza `/login` per autenticarti con il tuo account claude.ai. L'autenticazione con chiave API non è supportata per Remote Control.
* Problema di rete o proxy: un firewall o proxy potrebbe bloccare la richiesta HTTPS in uscita. Remote Control richiede l'accesso all'API Anthropic sulla porta 443.
* Creazione della sessione non riuscita: se vedi anche `Session creation failed — see debug log`, l'errore si è verificato in precedenza nella configurazione. Verifica che il tuo abbonamento sia attivo.

## Scegli l'approccio giusto

Claude Code offers several ways to work when you're not at your terminal. They differ in what triggers the work, where Claude runs, and how much you need to set up.

|                                                | Trigger                                                                                        | Claude runs on                                                                               | Setup                                                                                                                                | Best for                                                      |
| :--------------------------------------------- | :--------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------ |
| [Dispatch](/en/desktop#sessions-from-dispatch) | Message a task from the Claude mobile app                                                      | Your machine (Desktop)                                                                       | [Pair the mobile app with Desktop](https://support.claude.com/en/articles/13947068)                                                  | Delegating work while you're away, minimal setup              |
| [Remote Control](/en/remote-control)           | Drive a running session from [claude.ai/code](https://claude.ai/code) or the Claude mobile app | Your machine (CLI or VS Code)                                                                | Run `claude remote-control`                                                                                                          | Steering in-progress work from another device                 |
| [Channels](/en/channels)                       | Push events from a chat app like Telegram or Discord, or your own server                       | Your machine (CLI)                                                                           | [Install a channel plugin](/en/channels#quickstart) or [build your own](/en/channels-reference)                                      | Reacting to external events like CI failures or chat messages |
| [Slack](/en/slack)                             | Mention `@Claude` in a team channel                                                            | Anthropic cloud                                                                              | [Install the Slack app](/en/slack#setting-up-claude-code-in-slack) with [Claude Code on the web](/en/claude-code-on-the-web) enabled | PRs and reviews from team chat                                |
| [Scheduled tasks](/en/scheduled-tasks)         | Set a schedule                                                                                 | [CLI](/en/scheduled-tasks), [Desktop](/en/desktop-scheduled-tasks), or [cloud](/en/routines) | Pick a frequency                                                                                                                     | Recurring automation like daily reviews                       |

## Risorse correlate

* [Claude Code sul web](/it/claude-code-on-the-web): esegui sessioni in ambienti cloud gestiti da Anthropic invece che sulla tua macchina
* [Ultraplan](/it/ultraplan): avvia una sessione di pianificazione cloud dal tuo terminale e rivedi il piano nel tuo browser
* [Canali](/it/channels): inoltra Telegram, Discord o iMessage in una sessione in modo che Claude reagisca ai messaggi mentre sei assente
* [Dispatch](/it/desktop#sessions-from-dispatch): invia un'attività dal tuo telefono e può generare una sessione Desktop per gestirla
* [Autenticazione](/it/authentication): configura `/login` e gestisci le credenziali per claude.ai
* [Riferimento CLI](/it/cli-reference): elenco completo di flag e comandi incluso `claude remote-control`
* [Sicurezza](/it/security): come le sessioni Remote Control si adattano al modello di sicurezza di Claude Code
* [Utilizzo dei dati](/it/data-usage): quali dati fluiscono attraverso l'API Anthropic durante le sessioni locali e remote
