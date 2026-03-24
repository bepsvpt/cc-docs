> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Continua le sessioni locali da qualsiasi dispositivo con Remote Control

> Continua una sessione locale di Claude Code dal tuo telefono, tablet o da qualsiasi browser utilizzando Remote Control. Funziona con claude.ai/code e l'app Claude per dispositivi mobili.

<Note>
  Remote Control è disponibile su tutti i piani. Gli amministratori di Team e Enterprise devono prima abilitare Claude Code nelle [impostazioni di amministrazione](https://claude.ai/admin-settings/claude-code).
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

* **Abbonamento**: disponibile su piani Pro, Max, Team e Enterprise. Gli amministratori di Team e Enterprise devono prima abilitare Claude Code nelle [impostazioni di amministrazione](https://claude.ai/admin-settings/claude-code). Le chiavi API non sono supportate.
* **Autenticazione**: esegui `claude` e utilizza `/login` per accedere tramite claude.ai se non l'hai già fatto.
* **Fiducia dell'area di lavoro**: esegui `claude` nella directory del tuo progetto almeno una volta per accettare la finestra di dialogo di fiducia dell'area di lavoro.

## Avvia una sessione Remote Control

Puoi avviare un server Remote Control dedicato, avviare una sessione interattiva con Remote Control abilitato, o connetterti a una sessione già in esecuzione.

<Tabs>
  <Tab title="Modalità server">
    Accedi alla directory del tuo progetto ed esegui:

    ```bash  theme={null}
    claude remote-control
    ```

    Il processo rimane in esecuzione nel tuo terminale in modalità server, in attesa di connessioni remote. Visualizza un URL di sessione che puoi utilizzare per [connetterti da un altro dispositivo](#connect-from-another-device), e puoi premere la barra spaziatrice per mostrare un codice QR per un accesso rapido dal tuo telefono. Mentre una sessione remota è attiva, il terminale mostra lo stato della connessione e l'attività dello strumento.

    Flag disponibili:

    | Flag                         | Descrizione                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
    | ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `--name "My Project"`        | Imposta un titolo di sessione personalizzato visibile nell'elenco delle sessioni su claude.ai/code.                                                                                                                                                                                                                                                                                                                                                             |
    | `--spawn <mode>`             | Come vengono create le sessioni simultanee. Premi `w` durante l'esecuzione per attivare/disattivare.<br />• `same-dir` (predefinito): tutte le sessioni condividono la directory di lavoro corrente, quindi possono entrare in conflitto se modificano gli stessi file.<br />• `worktree`: ogni sessione su richiesta ottiene il proprio [git worktree](/it/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees). Richiede un repository git. |
    | `--capacity <N>`             | Numero massimo di sessioni simultanee. Il valore predefinito è 32.                                                                                                                                                                                                                                                                                                                                                                                              |
    | `--verbose`                  | Mostra log dettagliati di connessione e sessione.                                                                                                                                                                                                                                                                                                                                                                                                               |
    | `--sandbox` / `--no-sandbox` | Abilita o disabilita il [sandboxing](/it/sandboxing) per l'isolamento del filesystem e della rete. Disabilitato per impostazione predefinita.                                                                                                                                                                                                                                                                                                                   |
  </Tab>

  <Tab title="Sessione interattiva">
    Per avviare una normale sessione interattiva di Claude Code con Remote Control abilitato, utilizza il flag `--remote-control` (o `--rc`):

    ```bash  theme={null}
    claude --remote-control
    ```

    Facoltativamente passa un nome per la sessione:

    ```bash  theme={null}
    claude --remote-control "My Project"
    ```

    Questo ti dà una sessione interattiva completa nel tuo terminale che puoi anche controllare da claude.ai o dall'app Claude. A differenza di `claude remote-control` (modalità server), puoi digitare messaggi localmente mentre la sessione è anche disponibile da remoto.
  </Tab>

  <Tab title="Da una sessione esistente">
    Se sei già in una sessione di Claude Code e vuoi continuarla da remoto, utilizza il comando `/remote-control` (o `/rc`):

    ```text  theme={null}
    /remote-control
    ```

    Passa un nome come argomento per impostare un titolo di sessione personalizzato:

    ```text  theme={null}
    /remote-control My Project
    ```

    Questo avvia una sessione Remote Control che mantiene la cronologia della conversazione corrente e visualizza un URL di sessione e un codice QR che puoi utilizzare per [connetterti da un altro dispositivo](#connect-from-another-device). I flag `--verbose`, `--sandbox` e `--no-sandbox` non sono disponibili con questo comando.
  </Tab>
</Tabs>

### Connettiti da un altro dispositivo

Una volta che una sessione Remote Control è attiva, hai alcuni modi per connetterti da un altro dispositivo:

* **Apri l'URL della sessione** in qualsiasi browser per andare direttamente alla sessione su [claude.ai/code](https://claude.ai/code). Sia `claude remote-control` che `/remote-control` visualizzano questo URL nel terminale.
* **Scansiona il codice QR** mostrato accanto all'URL della sessione per aprirlo direttamente nell'app Claude. Con `claude remote-control`, premi la barra spaziatrice per attivare/disattivare la visualizzazione del codice QR.
* **Apri [claude.ai/code](https://claude.ai/code) o l'app Claude** e trova la sessione per nome nell'elenco delle sessioni. Le sessioni Remote Control mostrano un'icona di computer con un punto di stato verde quando sono online.

La sessione remota prende il suo nome dall'argomento `--name` (o dal nome passato a `/remote-control`), dal tuo ultimo messaggio, dal tuo valore `/rename`, o da "Remote Control session" se non c'è cronologia della conversazione. Se l'ambiente ha già una sessione attiva, ti verrà chiesto se continuarla o avviarne una nuova.

Se non hai ancora l'app Claude, utilizza il comando `/mobile` all'interno di Claude Code per visualizzare un codice QR di download per [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) o [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).

### Abilita Remote Control per tutte le sessioni

Per impostazione predefinita, Remote Control si attiva solo quando esegui esplicitamente `claude remote-control`, `claude --remote-control`, o `/remote-control`. Per abilitarlo automaticamente per ogni sessione interattiva, esegui `/config` all'interno di Claude Code e imposta **Enable Remote Control for all sessions** su `true`. Impostalo di nuovo su `false` per disabilitarlo.

Con questa impostazione attiva, ogni processo Claude Code interattivo registra una sessione remota. Se esegui più istanze, ognuna ottiene il proprio ambiente e sessione. Per eseguire più sessioni simultanee da un singolo processo, utilizza invece la modalità server con `--spawn`.

## Connessione e sicurezza

La tua sessione locale di Claude Code effettua solo richieste HTTPS in uscita e non apre mai porte in ingresso sulla tua macchina. Quando avvii Remote Control, si registra con l'API Anthropic e esegue il polling per il lavoro. Quando ti connetti da un altro dispositivo, il server instrada i messaggi tra il client web o mobile e la tua sessione locale su una connessione in streaming.

Tutto il traffico viaggia attraverso l'API Anthropic su TLS, lo stesso trasporto di sicurezza di qualsiasi sessione di Claude Code. La connessione utilizza più credenziali di breve durata, ognuna limitata a un singolo scopo e con scadenza indipendente.

## Remote Control vs Claude Code sul web

Remote Control e [Claude Code sul web](/it/claude-code-on-the-web) utilizzano entrambi l'interfaccia claude.ai/code. La differenza chiave è dove viene eseguita la sessione: Remote Control viene eseguito sulla tua macchina, quindi i tuoi server MCP locali, strumenti e configurazione del progetto rimangono disponibili. Claude Code sul web viene eseguito nell'infrastruttura cloud gestita da Anthropic.

Utilizza Remote Control quando sei nel mezzo di un lavoro locale e vuoi continuare da un altro dispositivo. Utilizza Claude Code sul web quando vuoi avviare un'attività senza alcuna configurazione locale, lavorare su un repository che non hai clonato, o eseguire più attività in parallelo.

## Limitazioni

* **Una sessione remota per processo interattivo**: al di fuori della modalità server, ogni istanza di Claude Code supporta una sessione remota alla volta. Utilizza la modalità server con `--spawn` per eseguire più sessioni simultanee da un singolo processo.
* **Il terminale deve rimanere aperto**: Remote Control viene eseguito come processo locale. Se chiudi il terminale o interrompi il processo `claude`, la sessione termina. Esegui di nuovo `claude remote-control` per avviare una nuova sessione.
* **Interruzione di rete prolungata**: se la tua macchina è accesa ma non riesce a raggiungere la rete per più di circa 10 minuti, la sessione scade e il processo esce. Esegui di nuovo `claude remote-control` per avviare una nuova sessione.

## Risorse correlate

* [Claude Code sul web](/it/claude-code-on-the-web): esegui sessioni in ambienti cloud gestiti da Anthropic invece che sulla tua macchina
* [Autenticazione](/it/authentication): configura `/login` e gestisci le credenziali per claude.ai
* [Riferimento CLI](/it/cli-reference): elenco completo di flag e comandi incluso `claude remote-control`
* [Sicurezza](/it/security): come le sessioni Remote Control si adattano al modello di sicurezza di Claude Code
* [Utilizzo dei dati](/it/data-usage): quali dati fluiscono attraverso l'API Anthropic durante le sessioni locali e remote
