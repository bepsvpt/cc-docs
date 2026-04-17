> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Usa Claude Code Desktop

> Sfrutta al massimo Claude Code Desktop: utilizzo del computer, sessioni Dispatch dal tuo telefono, sessioni parallele con isolamento Git, revisione visiva dei diff, anteprime delle app, monitoraggio dei PR, connettori e configurazione aziendale.

La scheda Code all'interno dell'app Claude Desktop consente di utilizzare Claude Code tramite un'interfaccia grafica invece del terminale.

Desktop aggiunge queste funzionalità all'esperienza standard di Claude Code:

* [Revisione visiva dei diff](#review-changes-with-diff-view) con commenti inline
* [Anteprima live dell'app](#preview-your-app) con server di sviluppo
* [Utilizzo del computer](#let-claude-use-your-computer) per aprire app e controllare lo schermo su macOS
* [Monitoraggio dei PR su GitHub](#monitor-pull-request-status) con correzione automatica e merge automatico
* [Sessioni parallele](#work-in-parallel-with-sessions) con isolamento automatico dei worktree Git
* [Dispatch](#sessions-from-dispatch) integration: invia un'attività dal tuo telefono, ottieni una sessione qui
* [Attività pianificate](#schedule-recurring-tasks) che eseguono Claude secondo una pianificazione ricorrente
* [Connettori](#connect-external-tools) per GitHub, Slack, Linear e altri
* Ambienti locali, [SSH](#ssh-sessions) e [cloud](#run-long-running-tasks-remotely)

<Tip>
  Nuovo a Desktop? Inizia con [Guida introduttiva](/it/desktop-quickstart) per installare l'app e fare il tuo primo edit.
</Tip>

Questa pagina copre [lavorare con il codice](#work-with-code), [utilizzo del computer](#let-claude-use-your-computer), [gestire le sessioni](#manage-sessions), [estendere Claude Code](#extend-claude-code), [attività pianificate](#schedule-recurring-tasks) e [configurazione](#environment-configuration). Include anche un [confronto CLI](#coming-from-the-cli) e [risoluzione dei problemi](#troubleshooting).

## Avvia una sessione

Prima di inviare il tuo primo messaggio, configura quattro cose nell'area del prompt:

* **Ambiente**: scegli dove Claude viene eseguito. Seleziona **Local** per la tua macchina, **Remote** per sessioni cloud ospitate da Anthropic, o una [**connessione SSH**](#ssh-sessions) per una macchina remota che gestisci. Vedi [configurazione dell'ambiente](#environment-configuration).
* **Cartella del progetto**: seleziona la cartella o il repository su cui Claude lavora. Per le sessioni remote, puoi aggiungere [più repository](#run-long-running-tasks-remotely).
* **Modello**: scegli un [modello](/it/model-config#available-models) dal menu a discesa accanto al pulsante di invio. Il modello viene bloccato una volta avviata la sessione.
* **Modalità di autorizzazione**: scegli quanta autonomia ha Claude dal [selettore di modalità](#choose-a-permission-mode). Puoi cambiare questo durante la sessione.

Digita il tuo compito e premi **Invio** per iniziare. Ogni sessione traccia il suo proprio contesto e le modifiche in modo indipendente.

## Lavora con il codice

Dai a Claude il contesto giusto, controlla quanto fa da solo e rivedi cosa ha cambiato.

### Usa la casella del prompt

Digita quello che vuoi che Claude faccia e premi **Invio** per inviare. Claude legge i file del tuo progetto, apporta modifiche ed esegue comandi in base alla tua [modalità di autorizzazione](#choose-a-permission-mode). Puoi interrompere Claude in qualsiasi momento: fai clic sul pulsante di arresto o digita la tua correzione e premi **Invio**. Claude smette di fare quello che sta facendo e si adatta in base al tuo input.

Il pulsante **+** accanto alla casella del prompt ti dà accesso agli allegati di file, [skills](#use-skills), [connettori](#connect-external-tools) e [plugin](#install-plugins).

### Aggiungi file e contesto ai prompt

La casella del prompt supporta due modi per portare contesto esterno:

* **@mention file**: digita `@` seguito da un nome di file per aggiungere un file al contesto della conversazione. Claude può quindi leggere e fare riferimento a quel file. @mention non è disponibile nelle sessioni remote.
* **Allega file**: allega immagini, PDF e altri file al tuo prompt usando il pulsante di allegato, o trascina e rilascia i file direttamente nel prompt. Questo è utile per condividere screenshot di bug, mockup di design o documenti di riferimento.

### Scegli una modalità di autorizzazione

Le modalità di autorizzazione controllano quanta autonomia ha Claude durante una sessione: se chiede prima di modificare file, eseguire comandi o entrambi. Puoi cambiare modalità in qualsiasi momento usando il selettore di modalità accanto al pulsante di invio. Inizia con Chiedi autorizzazioni per vedere esattamente cosa fa Claude, quindi passa a Accetta automaticamente modifiche o Plan mode man mano che acquisisci familiarità.

| Modalità                              | Chiave di impostazione | Comportamento                                                                                                                                                                                                                                                                                                                                            |
| ------------------------------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Chiedi autorizzazioni**             | `default`              | Claude chiede prima di modificare file o eseguire comandi. Vedi un diff e puoi accettare o rifiutare ogni modifica. Consigliato per i nuovi utenti.                                                                                                                                                                                                      |
| **Accetta automaticamente modifiche** | `acceptEdits`          | Claude accetta automaticamente le modifiche ai file ma chiede comunque prima di eseguire comandi di terminale. Usa questo quando ti fidi delle modifiche ai file e vuoi un'iterazione più veloce.                                                                                                                                                        |
| **Plan mode**                         | `plan`                 | Claude analizza il tuo codice e crea un piano senza modificare file o eseguire comandi. Buono per compiti complessi dove vuoi rivedere l'approccio prima.                                                                                                                                                                                                |
| **Auto**                              | `auto`                 | Claude esegue tutte le azioni con controlli di sicurezza in background che verificano l'allineamento con la tua richiesta. Riduce i prompt di autorizzazione mantenendo la supervisione. Attualmente un'anteprima di ricerca. Disponibile su piani Team, Enterprise e API. Richiede Claude Sonnet 4.6 o Opus 4.6. Abilita in Impostazioni → Claude Code. |
| **Bypass permissions**                | `bypassPermissions`    | Claude viene eseguito senza alcun prompt di autorizzazione, equivalente a `--dangerously-skip-permissions` nella CLI. Abilita in Impostazioni → Claude Code sotto "Allow bypass permissions mode". Usa solo in container sandbox o VM. Gli amministratori aziendali possono disabilitare questa opzione.                                                 |

La modalità di autorizzazione `dontAsk` è disponibile solo nella [CLI](/it/permission-modes#allow-only-pre-approved-tools-with-dontask-mode).

<Tip title="Best practice">
  Inizia compiti complessi in Plan mode in modo che Claude mappi un approccio prima di apportare modifiche. Una volta approvato il piano, passa a Accetta automaticamente modifiche o Chiedi autorizzazioni per eseguirlo. Vedi [esplora prima, poi pianifica, poi codifica](/it/best-practices#explore-first-then-plan-then-code) per ulteriori informazioni su questo flusso di lavoro.
</Tip>

Le sessioni remote supportano Accetta automaticamente modifiche e Plan mode. Chiedi autorizzazioni non è disponibile perché le sessioni remote accettano automaticamente le modifiche ai file per impostazione predefinita, e Bypass permissions non è disponibile perché l'ambiente remoto è già sandbox.

Gli amministratori aziendali possono limitare quali modalità di autorizzazione sono disponibili. Vedi [configurazione aziendale](#enterprise-configuration) per i dettagli.

### Anteprima della tua app

Claude può avviare un server di sviluppo e aprire un browser incorporato per verificare le sue modifiche. Questo funziona per app web frontend così come per server backend: Claude può testare endpoint API, visualizzare log del server e iterare su problemi che trova. Nella maggior parte dei casi, Claude avvia il server automaticamente dopo aver modificato i file del progetto. Puoi anche chiedere a Claude di visualizzare un'anteprima in qualsiasi momento. Per impostazione predefinita, Claude [verifica automaticamente](#auto-verify-changes) le modifiche dopo ogni edit.

Dal pannello di anteprima, puoi:

* Interagire con la tua app in esecuzione direttamente nel browser incorporato
* Guardare Claude verificare automaticamente le sue stesse modifiche: scatta screenshot, ispeziona il DOM, fa clic su elementi, compila moduli e corregge i problemi che trova
* Avviare o arrestare server dal menu a discesa **Preview** nella barra degli strumenti della sessione
* Persistere cookie e archiviazione locale tra i riavvii del server selezionando **Persist sessions** nel menu a discesa, in modo da non dover effettuare di nuovo l'accesso durante lo sviluppo
* Modificare la configurazione del server o arrestare tutti i server contemporaneamente

Claude crea la configurazione iniziale del server in base al tuo progetto. Se la tua app utilizza un comando dev personalizzato, modifica `.claude/launch.json` per adattarlo alla tua configurazione. Vedi [Configura server di anteprima](#configure-preview-servers) per il riferimento completo.

Per cancellare i dati della sessione salvati, attiva/disattiva **Persist preview sessions** in Impostazioni → Claude Code. Per disabilitare completamente l'anteprima, attiva/disattiva **Preview** in Impostazioni → Claude Code.

### Rivedi le modifiche con la visualizzazione diff

Dopo che Claude apporta modifiche al tuo codice, la visualizzazione diff ti consente di rivedere le modifiche file per file prima di creare una pull request.

Quando Claude modifica i file, appare un indicatore di statistiche diff che mostra il numero di righe aggiunte e rimosse, come `+12 -1`. Fai clic su questo indicatore per aprire il visualizzatore diff, che visualizza un elenco di file a sinistra e le modifiche per ogni file a destra.

Per commentare righe specifiche, fai clic su qualsiasi riga nel diff per aprire una casella di commento. Digita il tuo feedback e premi **Invio** per aggiungere il commento. Dopo aver aggiunto commenti a più righe, invia tutti i commenti contemporaneamente:

* **macOS**: premi **Cmd+Invio**
* **Windows**: premi **Ctrl+Invio**

Claude legge i tuoi commenti e apporta le modifiche richieste, che appaiono come un nuovo diff che puoi rivedere.

### Rivedi il tuo codice

Nella visualizzazione diff, fai clic su **Review code** nella barra degli strumenti in alto a destra per chiedere a Claude di valutare le modifiche prima di eseguire il commit. Claude esamina i diff attuali e lascia commenti direttamente nella visualizzazione diff. Puoi rispondere a qualsiasi commento o chiedere a Claude di rivedere.

La revisione si concentra su problemi ad alto segnale: errori di compilazione, errori logici definitivi, vulnerabilità di sicurezza e bug ovvi. Non contrassegna stile, formattazione, problemi preesistenti o qualsiasi cosa che un linter catturebbe.

### Monitora lo stato della pull request

Dopo aver aperto una pull request, una barra di stato CI appare nella sessione. Claude Code utilizza GitHub CLI per eseguire il polling dei risultati dei controlli e visualizzare i guasti.

* **Auto-fix**: quando abilitato, Claude tenta automaticamente di correggere i controlli CI non riusciti leggendo l'output del guasto e iterando.
* **Auto-merge**: quando abilitato, Claude unisce il PR una volta che tutti i controlli passano. Il metodo di merge è squash. Auto-merge deve essere [abilitato nelle impostazioni del tuo repository GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository) affinché questo funzioni.

Usa gli interruttori **Auto-fix** e **Auto-merge** nella barra di stato CI per abilitare una delle due opzioni. Claude Code invia anche una notifica desktop quando CI termina.

<Note>
  Il monitoraggio dei PR richiede che [GitHub CLI (`gh`)](https://cli.github.com/) sia installato e autenticato sulla tua macchina. Se `gh` non è installato, Desktop ti chiede di installarlo la prima volta che tenti di creare un PR.
</Note>

## Lascia che Claude usi il tuo computer

L'utilizzo del computer consente a Claude di aprire le tue app, controllare lo schermo e lavorare direttamente sulla tua macchina come faresti tu. Chiedi a Claude di testare un'app nativa nel simulatore iOS, interagire con uno strumento desktop che non ha CLI, o automatizzare qualcosa che funziona solo tramite una GUI.

<Note>
  L'utilizzo del computer è un'anteprima di ricerca su macOS che richiede un piano Pro o Max. Non è disponibile su piani Team o Enterprise. L'app Claude Desktop deve essere in esecuzione.
</Note>

L'utilizzo del computer è disabilitato per impostazione predefinita. [Abilitalo in Impostazioni](#enable-computer-use) e concedi i permessi macOS richiesti prima che Claude possa controllare lo schermo.

<Warning>
  A differenza dello [strumento Bash sandbox](/it/sandboxing), l'utilizzo del computer viene eseguito sul tuo desktop effettivo con accesso a tutto ciò che approvi. Claude controlla ogni azione e contrassegna potenziali iniezioni di prompt dal contenuto sullo schermo, ma il limite di fiducia è diverso. Vedi la [guida alla sicurezza dell'utilizzo del computer](https://support.claude.com/en/articles/14128542) per le best practice.
</Warning>

### Quando si applica l'utilizzo del computer

Claude ha diversi modi per interagire con un'app o un servizio, e l'utilizzo del computer è il più ampio e lento. Prova prima lo strumento più preciso:

* Se hai un [connettore](#connect-external-tools) per un servizio, Claude usa il connettore.
* Se l'attività è un comando shell, Claude usa Bash.
* Se l'attività è lavoro nel browser e hai [Claude in Chrome](/it/chrome) configurato, Claude usa quello.
* Se nessuno di questi si applica, Claude usa l'utilizzo del computer.

I [livelli di accesso per app](#app-permissions) rafforzano questo: i browser sono limitati a sola visualizzazione, e i terminali e gli IDE a solo clic, indirizzando Claude verso lo strumento dedicato anche quando l'utilizzo del computer è attivo. Il controllo dello schermo è riservato a cose che nient'altro può raggiungere, come app native, pannelli di controllo hardware, il simulatore iOS o strumenti proprietari senza un'API.

### Abilita l'utilizzo del computer

L'utilizzo del computer è disabilitato per impostazione predefinita. Se chiedi a Claude di fare qualcosa che ne ha bisogno mentre è disabilitato, Claude ti dice che potrebbe fare l'attività se abiliti l'utilizzo del computer in Impostazioni.

<Steps>
  <Step title="Aggiorna l'app desktop">
    Assicurati di avere l'ultima versione di Claude Desktop. Scarica o aggiorna su [claude.com/download](https://claude.com/download), quindi riavvia l'app.
  </Step>

  <Step title="Attiva l'interruttore">
    Nell'app desktop, vai a **Impostazioni > Generale** (sotto **App Desktop**). Trova l'interruttore **Utilizzo del computer** e attivalo.

    Se non vedi l'interruttore, conferma che sei su macOS con un piano Pro o Max, quindi aggiorna e riavvia l'app.
  </Step>

  <Step title="Concedi i permessi macOS">
    Prima che l'interruttore abbia effetto, concedi due permessi di sistema macOS:

    * **Accessibilità**: consente a Claude di fare clic, digitare e scorrere
    * **Registrazione dello schermo**: consente a Claude di vedere cosa c'è sullo schermo

    La pagina Impostazioni mostra lo stato attuale di ogni permesso. Se uno è negato, fai clic sul badge per aprire il riquadro Impostazioni di sistema pertinente.
  </Step>
</Steps>

### Permessi delle app

La prima volta che Claude ha bisogno di usare un'app, appare un prompt nella tua sessione. Fai clic su **Consenti per questa sessione** o **Nega**. Le approvazioni durano per la sessione corrente, o 30 minuti nelle [sessioni generate da Dispatch](#sessions-from-dispatch).

Il prompt mostra anche quale livello di controllo Claude ottiene per quell'app. Questi livelli sono fissi per categoria di app e non possono essere modificati:

| Livello              | Cosa può fare Claude                                                  | Si applica a                    |
| :------------------- | :-------------------------------------------------------------------- | :------------------------------ |
| Solo visualizzazione | Vedere l'app negli screenshot                                         | Browser, piattaforme di trading |
| Solo clic            | Fare clic e scorrere, ma non digitare o usare scorciatoie da tastiera | Terminali, IDE                  |
| Controllo completo   | Fare clic, digitare, trascinare e usare scorciatoie da tastiera       | Tutto il resto                  |

Le app con ampia portata come Terminal, Finder e Impostazioni di sistema mostrano un avviso aggiuntivo nel prompt in modo che tu sappia cosa approvare loro concede.

Puoi configurare due impostazioni in **Impostazioni > Generale** (sotto **App Desktop**):

* **App negate**: aggiungi app qui per rifiutarle senza chiedere. Claude potrebbe comunque influenzare un'app negata indirettamente tramite azioni in un'app consentita, ma non può interagire direttamente con l'app negata.
* **Mostra app quando Claude finisce**: mentre Claude sta lavorando, le tue altre finestre sono nascoste in modo che interagisca solo con l'app approvata. Quando Claude finisce, le finestre nascoste vengono ripristinate a meno che non disattivi questa impostazione.

## Gestisci le sessioni

Ogni sessione è una conversazione indipendente con il suo proprio contesto e modifiche. Puoi eseguire più sessioni in parallelo, inviare il lavoro al cloud, o lasciare che Dispatch avvii sessioni per te dal tuo telefono.

### Lavora in parallelo con le sessioni

Fai clic su **+ New session** nella barra laterale per lavorare su più compiti in parallelo. Per i repository Git, ogni sessione ottiene la sua copia isolata del tuo progetto usando [Git worktrees](/it/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), in modo che le modifiche in una sessione non influiscano su altre sessioni fino a quando non le esegui il commit.

I worktree sono archiviati in `<project-root>/.claude/worktrees/` per impostazione predefinita. Puoi cambiare questo in una directory personalizzata in Impostazioni → Claude Code sotto "Worktree location". Puoi anche impostare un prefisso di ramo che viene anteposto a ogni nome di ramo worktree, il che è utile per mantenere organizzati i rami creati da Claude. Per rimuovere un worktree quando hai finito, passa il mouse sulla sessione nella barra laterale e fai clic sull'icona di archivio.

Per includere file gitignored come `.env` nei nuovi worktree, crea un [file `.worktreeinclude`](/it/common-workflows#copy-gitignored-files-to-worktrees) nella radice del tuo progetto.

<Note>
  L'isolamento della sessione richiede [Git](https://git-scm.com/downloads). La maggior parte dei Mac include Git per impostazione predefinita. Esegui `git --version` in Terminal per verificare. Su Windows, Git è richiesto affinché la scheda Code funzioni: [scarica Git per Windows](https://git-scm.com/downloads/win), installalo e riavvia l'app. Se riscontri errori Git, prova una sessione Cowork per aiutare a risolvere i problemi della tua configurazione.
</Note>

Usa l'icona del filtro in cima alla barra laterale per filtrare le sessioni per stato (Active, Archived) e ambiente (Local, Cloud). Per rinominare una sessione o controllare l'utilizzo del contesto, fai clic sul titolo della sessione nella barra degli strumenti in cima alla sessione attiva. Quando il contesto si riempie, Claude riassume automaticamente la conversazione e continua a lavorare. Puoi anche digitare `/compact` per attivare la compattazione prima e liberare spazio di contesto. Vedi [la finestra di contesto](/it/how-claude-code-works#the-context-window) per i dettagli su come funziona la compattazione.

### Esegui attività a lunga esecuzione in remoto

Per grandi refactor, suite di test, migrazioni o altre attività a lunga esecuzione, seleziona **Remote** invece di **Local** quando avvii una sessione. Le sessioni remote vengono eseguite sull'infrastruttura cloud di Anthropic e continuano anche se chiudi l'app o spegni il computer. Torna indietro in qualsiasi momento per vedere i progressi o indirizzare Claude in una direzione diversa. Puoi anche monitorare le sessioni remote da [claude.ai/code](https://claude.ai/code) o dall'app Claude iOS.

Le sessioni remote supportano anche più repository. Dopo aver selezionato un ambiente cloud, fai clic sul pulsante **+** accanto alla pillola del repo per aggiungere repository aggiuntivi alla sessione. Ogni repo ottiene il suo selettore di ramo. Questo è utile per compiti che si estendono su più codebase, come l'aggiornamento di una libreria condivisa e dei suoi consumatori.

Vedi [Claude Code sul web](/it/claude-code-on-the-web) per ulteriori informazioni su come funzionano le sessioni remote.

### Continua su un'altra superficie

Il menu **Continue in**, accessibile dall'icona VS Code in basso a destra della barra degli strumenti della sessione, ti consente di spostare la tua sessione su un'altra superficie:

* **Claude Code sul web**: invia la tua sessione locale per continuare l'esecuzione in remoto. Desktop esegue il push del tuo ramo, genera un riepilogo della conversazione e crea una nuova sessione remota con il contesto completo. Puoi quindi scegliere di archiviare la sessione locale o mantenerla. Questo richiede un albero di lavoro pulito e non è disponibile per le sessioni SSH.
* **Il tuo IDE**: apre il tuo progetto in un IDE supportato nella directory di lavoro corrente.

### Sessioni da Dispatch

[Dispatch](https://support.claude.com/en/articles/13947068) è una conversazione persistente con Claude che vive nella scheda [Cowork](https://claude.com/product/cowork#dispatch-and-computer-use). Invii a Dispatch un'attività, e decide come gestirla.

Un'attività può finire come una sessione Code in due modi: chiedi direttamente una, come "apri una sessione Claude Code e correggi il bug di accesso", o Dispatch decide che l'attività è lavoro di sviluppo e ne genera una automaticamente. Le attività che tipicamente vengono indirizzate a Code includono correzione di bug, aggiornamento delle dipendenze, esecuzione di test o apertura di pull request. La ricerca, la modifica di documenti e il lavoro con fogli di calcolo rimangono in Cowork.

In entrambi i casi, la sessione Code appare nella barra laterale della scheda Code con un badge **Dispatch**. Ricevi una notifica push sul tuo telefono quando finisce o ha bisogno della tua approvazione.

Se hai [l'utilizzo del computer](#let-claude-use-your-computer) abilitato, le sessioni Code generate da Dispatch possono usarlo anche. Le approvazioni delle app in quelle sessioni scadono dopo 30 minuti e ripromptano, piuttosto che durare l'intera sessione come le sessioni Code regolari.

Per la configurazione, l'accoppiamento e le impostazioni di Dispatch, vedi l'[articolo di aiuto di Dispatch](https://support.claude.com/en/articles/13947068). Dispatch richiede un piano Pro o Max e non è disponibile su piani Team o Enterprise.

Dispatch è uno dei diversi modi per lavorare con Claude quando sei lontano dal tuo terminale. Vedi [Piattaforme e integrazioni](/it/platforms#work-when-you-are-away-from-your-terminal) per confrontarlo con Remote Control, Channels, Slack e attività pianificate.

## Estendi Claude Code

Connetti servizi esterni, aggiungi flussi di lavoro riutilizzabili, personalizza il comportamento di Claude e configura server di anteprima.

### Connetti strumenti esterni

Per le sessioni locali e [SSH](#ssh-sessions), fai clic sul pulsante **+** accanto alla casella del prompt e seleziona **Connectors** per aggiungere integrazioni come Google Calendar, Slack, GitHub, Linear, Notion e altri. Puoi aggiungere connettori prima o durante una sessione. Il pulsante **+** non è disponibile nelle sessioni remote, ma le [attività pianificate](/it/web-scheduled-tasks) configurano i connettori al momento della creazione dell'attività.

Per gestire o disconnettere i connettori, vai a Impostazioni → Connectors nell'app desktop, o seleziona **Manage connectors** dal menu Connectors nella casella del prompt.

Una volta connesso, Claude può leggere il tuo calendario, inviare messaggi, creare problemi e interagire direttamente con i tuoi strumenti. Puoi chiedere a Claude quali connettori sono configurati nella tua sessione.

I connettori sono [MCP servers](/it/mcp) con un flusso di configurazione grafico. Usali per l'integrazione rapida con i servizi supportati. Per le integrazioni non elencate in Connectors, aggiungi MCP servers manualmente tramite [file di impostazioni](/it/mcp#installing-mcp-servers). Puoi anche [creare connettori personalizzati](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

### Usa skills

[Skills](/it/skills) estendono quello che Claude può fare. Claude le carica automaticamente quando rilevante, o puoi invocarne una direttamente: digita `/` nella casella del prompt o fai clic sul pulsante **+** e seleziona **Slash commands** per sfogliare cosa è disponibile. Questo include [comandi incorporati](/it/commands), le tue [skill personalizzate](/it/skills#create-custom-skills), skill del progetto dal tuo codebase e skill da qualsiasi [plugin installato](/it/plugins). Selezionane uno e appare evidenziato nel campo di input. Digita il tuo compito dopo di esso e invia come al solito.

### Installa plugin

[Plugins](/it/plugins) sono pacchetti riutilizzabili che aggiungono skills, agents, hooks, MCP servers e configurazioni LSP a Claude Code. Puoi installare plugin dall'app desktop senza usare il terminale.

Per le sessioni locali e [SSH](#ssh-sessions), fai clic sul pulsante **+** accanto alla casella del prompt e seleziona **Plugins** per vedere i tuoi plugin installati e i loro comandi. Per aggiungere un plugin, seleziona **Add plugin** dal sottomenu per aprire il browser dei plugin, che mostra i plugin disponibili dai tuoi [marketplace](/it/plugin-marketplaces) configurati incluso il marketplace ufficiale di Anthropic. Seleziona **Manage plugins** per abilitare, disabilitare o disinstallare plugin.

I plugin possono essere limitati al tuo account utente, a un progetto specifico o solo locali. I plugin non sono disponibili per le sessioni remote. Per il riferimento completo dei plugin inclusa la creazione dei tuoi plugin, vedi [plugin](/it/plugins).

### Configura server di anteprima

Claude rileva automaticamente la tua configurazione del server di sviluppo e archivia la configurazione in `.claude/launch.json` alla radice della cartella che hai selezionato quando hai avviato la sessione. Preview utilizza questa cartella come directory di lavoro, quindi se hai selezionato una cartella padre, le sottocartelle con i loro stessi server di sviluppo non verranno rilevate automaticamente. Per lavorare con il server di una sottocartella, avvia una sessione in quella cartella direttamente o aggiungi una configurazione manualmente.

Per personalizzare come il tuo server si avvia, ad esempio per usare `yarn dev` invece di `npm run dev` o per cambiare la porta, modifica il file manualmente o fai clic su **Edit configuration** nel menu a discesa Preview per aprirlo nel tuo editor di codice. Il file supporta JSON con commenti.

```json theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

Puoi definire più configurazioni per eseguire server diversi dallo stesso progetto, come un frontend e un'API. Vedi gli [esempi](#examples) di seguito.

#### Auto-verify changes

Quando `autoVerify` è abilitato, Claude verifica automaticamente le modifiche al codice dopo aver modificato i file. Scatta screenshot, controlla gli errori e conferma che le modifiche funzionano prima di completare la sua risposta.

Auto-verify è abilitato per impostazione predefinita. Disabilitalo per progetto aggiungendo `"autoVerify": false` a `.claude/launch.json`, o attiva/disattivalo dal menu a discesa **Preview**.

```json theme={null}
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [...]
}
```

Quando disabilitato, gli strumenti di anteprima sono ancora disponibili e puoi chiedere a Claude di verificare in qualsiasi momento. Auto-verify lo rende automatico dopo ogni edit.

#### Configuration fields

Ogni voce nell'array `configurations` accetta i seguenti campi:

| Campo               | Tipo      | Descrizione                                                                                                                                                                                                                                                      |
| ------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`              | string    | Un identificatore univoco per questo server                                                                                                                                                                                                                      |
| `runtimeExecutable` | string    | Il comando da eseguire, come `npm`, `yarn` o `node`                                                                                                                                                                                                              |
| `runtimeArgs`       | string\[] | Argomenti passati a `runtimeExecutable`, come `["run", "dev"]`                                                                                                                                                                                                   |
| `port`              | number    | La porta su cui il tuo server ascolta. Predefinito a 3000                                                                                                                                                                                                        |
| `cwd`               | string    | Directory di lavoro relativa alla radice del tuo progetto. Predefinito alla radice del progetto. Usa `${workspaceFolder}` per fare riferimento alla radice del progetto esplicitamente                                                                           |
| `env`               | object    | Variabili di ambiente aggiuntive come coppie chiave-valore, come `{ "NODE_ENV": "development" }`. Non mettere segreti qui poiché questo file viene eseguito il commit nel tuo repo. I segreti impostati nel tuo profilo shell vengono ereditati automaticamente. |
| `autoPort`          | boolean   | Come gestire i conflitti di porta. Vedi di seguito                                                                                                                                                                                                               |
| `program`           | string    | Uno script da eseguire con `node`. Vedi [quando usare `program` vs `runtimeExecutable`](#when-to-use-program-vs-runtimeexecutable)                                                                                                                               |
| `args`              | string\[] | Argomenti passati a `program`. Usato solo quando `program` è impostato                                                                                                                                                                                           |

##### When to use `program` vs `runtimeExecutable`

Usa `runtimeExecutable` con `runtimeArgs` per avviare un server di sviluppo tramite un gestore di pacchetti. Ad esempio, `"runtimeExecutable": "npm"` con `"runtimeArgs": ["run", "dev"]` esegue `npm run dev`.

Usa `program` quando hai uno script autonomo che vuoi eseguire con `node` direttamente. Ad esempio, `"program": "server.js"` esegue `node server.js`. Passa flag aggiuntivi con `args`.

#### Port conflicts

Il campo `autoPort` controlla cosa succede quando la tua porta preferita è già in uso:

* **`true`**: Claude trova e utilizza una porta libera automaticamente. Adatto per la maggior parte dei server di sviluppo.
* **`false`**: Claude fallisce con un errore. Usa questo quando il tuo server deve usare una porta specifica, come per i callback OAuth o gli allowlist CORS.
* **Non impostato (predefinito)**: Claude chiede se il server ha bisogno di quella porta esatta, quindi salva la tua risposta.

Quando Claude sceglie una porta diversa, passa la porta assegnata al tuo server tramite la variabile di ambiente `PORT`.

#### Examples

Queste configurazioni mostrano configurazioni comuni per diversi tipi di progetto:

<Tabs>
  <Tab title="Next.js">
    Questa configurazione esegue un'app Next.js usando Yarn sulla porta 3000:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "web",
          "runtimeExecutable": "yarn",
          "runtimeArgs": ["dev"],
          "port": 3000
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Multiple servers">
    Per un monorepo con un frontend e un server API, definisci più configurazioni. Il frontend usa `autoPort: true` in modo che scelga una porta libera se 3000 è occupata, mentre il server API richiede la porta 8080 esattamente:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "frontend",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "dev"],
          "cwd": "apps/web",
          "port": 3000,
          "autoPort": true
        },
        {
          "name": "api",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "start"],
          "cwd": "server",
          "port": 8080,
          "env": { "NODE_ENV": "development" },
          "autoPort": false
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Node.js script">
    Per eseguire uno script Node.js direttamente invece di usare un comando del gestore di pacchetti, usa il campo `program`:

    ```json theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "server",
          "program": "server.js",
          "args": ["--verbose"],
          "port": 4000
        }
      ]
    }
    ```
  </Tab>
</Tabs>

## Pianifica attività ricorrenti

Per impostazione predefinita, le attività pianificate avviano una nuova sessione automaticamente a un'ora e una frequenza che scegli. Usale per lavori ricorrenti come revisioni di codice giornaliere, controlli di aggiornamento delle dipendenze o briefing mattutini che traggono dal tuo calendario e dalla tua inbox.

### Confronta le opzioni di pianificazione

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

La pagina Schedule supporta due tipi di attività:

* **Attività locali**: vengono eseguite sulla tua macchina. Hanno accesso diretto ai tuoi file e strumenti locali, ma l'app desktop deve essere aperta e il tuo computer sveglio affinché si attivino.
* **Attività remote**: vengono eseguite sull'infrastruttura cloud gestita da Anthropic. Continuano a funzionare anche quando il tuo computer è spento, ma funzionano su un clone fresco del tuo repository piuttosto che sul tuo checkout locale.

Entrambi i tipi appaiono nella stessa griglia di attività. Fai clic su **New task** per scegliere quale tipo creare. Il resto di questa sezione copre le attività locali; per le attività remote, vedi [Attività pianificate cloud](/it/web-scheduled-tasks).

Vedi [Come vengono eseguite le attività pianificate](#how-scheduled-tasks-run) per i dettagli sui run mancati e il comportamento di recupero per le attività locali.

<Note>
  Per impostazione predefinita, le attività pianificate locali vengono eseguite contro qualsiasi stato la tua directory di lavoro sia, incluse le modifiche non eseguite il commit. Abilita l'interruttore worktree nell'input del prompt per dare a ogni run il suo worktree Git isolato, nello stesso modo in cui funzionano le [sessioni parallele](#work-in-parallel-with-sessions).
</Note>

Per creare un'attività pianificata locale, fai clic su **Schedule** nella barra laterale, fai clic su **New task** e scegli **New local task**. Configura questi campi:

| Campo       | Descrizione                                                                                                                                                                                                                                                                          |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Name        | Identificatore per l'attività. Convertito in minuscolo kebab-case e usato come nome della cartella su disco. Deve essere univoco tra le tue attività.                                                                                                                                |
| Description | Breve riepilogo mostrato nell'elenco delle attività.                                                                                                                                                                                                                                 |
| Prompt      | Le istruzioni inviate a Claude quando l'attività viene eseguita. Scrivi questo nello stesso modo in cui scriveresti qualsiasi messaggio nella casella del prompt. L'input del prompt include anche controlli per modello, modalità di autorizzazione, cartella di lavoro e worktree. |
| Frequency   | Con quale frequenza l'attività viene eseguita. Vedi [opzioni di frequenza](#frequency-options) di seguito.                                                                                                                                                                           |

Puoi anche creare un'attività descrivendo quello che vuoi in qualsiasi sessione. Ad esempio, "configura una revisione di codice giornaliera che viene eseguita ogni mattina alle 9am."

### Frequency options

* **Manual**: nessuna pianificazione, viene eseguita solo quando fai clic su **Run now**. Utile per salvare un prompt che attivi su richiesta
* **Hourly**: viene eseguita ogni ora. Ogni attività ottiene un offset fisso di fino a 10 minuti dall'inizio dell'ora per scaglionare il traffico API
* **Daily**: mostra un selettore di ora, predefinito alle 9:00 AM ora locale
* **Weekdays**: uguale a Daily ma salta sabato e domenica
* **Weekly**: mostra un selettore di ora e un selettore di giorno

Per intervalli che il selettore non offre (ogni 15 minuti, primo di ogni mese, ecc.), chiedi a Claude in qualsiasi sessione Desktop di impostare la pianificazione. Usa il linguaggio naturale; ad esempio, "pianifica un'attività per eseguire tutti i test ogni 6 ore."

### How scheduled tasks run

Le attività pianificate locali vengono eseguite sulla tua macchina. Desktop controlla la pianificazione ogni minuto mentre l'app è aperta e avvia una sessione nuova quando un'attività è dovuta, indipendentemente da qualsiasi sessione manuale che hai aperta. Ogni attività ottiene un ritardo fisso di fino a 10 minuti dopo l'ora pianificata per scaglionare il traffico API. Il ritardo è deterministico: la stessa attività inizia sempre allo stesso offset.

Quando un'attività si attiva, ricevi una notifica desktop e una nuova sessione appare sotto una sezione **Scheduled** nella barra laterale. Aprila per vedere cosa ha fatto Claude, rivedere le modifiche o rispondere ai prompt di autorizzazione. La sessione funziona come qualsiasi altra: Claude può modificare file, eseguire comandi, creare commit e aprire pull request.

Le attività vengono eseguite solo mentre l'app desktop è in esecuzione e il tuo computer è sveglio. Se il tuo computer dorme durante un'ora pianificata, il run viene saltato. Per prevenire il sonno inattivo, abilita **Keep computer awake** in Impostazioni sotto **Desktop app → General**. Chiudere il coperchio del laptop lo mette comunque a dormire. Per le attività che devono funzionare anche quando il tuo computer è spento, usa un'[attività remota](/it/web-scheduled-tasks) invece.

### Missed runs

Quando l'app si avvia o il tuo computer si sveglia, Desktop controlla se ogni attività ha perso run negli ultimi sette giorni. Se lo ha fatto, Desktop avvia esattamente un run di recupero per l'ora più recentemente mancata e scarta qualsiasi cosa più vecchia. Un'attività giornaliera che ha perso sei giorni viene eseguita una volta al risveglio. Desktop mostra una notifica quando inizia un run di recupero.

Tieni questo in mente quando scrivi i prompt. Un'attività pianificata per le 9am potrebbe essere eseguita alle 23:00 se il tuo computer è stato addormentato tutto il giorno. Se il timing è importante, aggiungi guardrail al prompt stesso, ad esempio: "Rivedi solo i commit di oggi. Se è dopo le 17:00, salta la revisione e pubblica solo un riepilogo di quello che è stato perso."

### Permissions for scheduled tasks

Ogni attività ha la sua propria modalità di autorizzazione, che imposti quando crei o modifichi l'attività. Le regole di autorizzazione da `~/.claude/settings.json` si applicano anche alle sessioni di attività pianificate. Se un'attività viene eseguita in modalità Ask e ha bisogno di eseguire uno strumento per il quale non ha autorizzazione, il run si blocca fino a quando non lo approvi. La sessione rimane aperta nella barra laterale in modo che tu possa rispondere in seguito.

Per evitare blocchi, fai clic su **Run now** dopo aver creato un'attività, guarda i prompt di autorizzazione e seleziona "always allow" per ognuno. I run futuri di quell'attività approvano automaticamente gli stessi strumenti senza chiedere. Puoi rivedere e revocare queste approvazioni dalla pagina dei dettagli dell'attività.

### Manage scheduled tasks

Fai clic su un'attività nell'elenco **Schedule** per aprire la sua pagina di dettagli. Da qui puoi:

* **Run now**: avvia l'attività immediatamente senza aspettare l'ora pianificata successiva
* **Toggle repeats**: metti in pausa o riprendi i run pianificati senza eliminare l'attività
* **Edit**: cambia il prompt, la frequenza, la cartella o altre impostazioni
* **Review history**: vedi ogni run passato, inclusi quelli che sono stati saltati perché il tuo computer era addormentato
* **Review allowed permissions**: vedi e revoca le approvazioni degli strumenti salvate per questa attività dal pannello **Always allowed**
* **Delete**: rimuovi l'attività e archivia tutte le sessioni che ha creato

Puoi anche gestire le attività chiedendo a Claude in qualsiasi sessione Desktop. Ad esempio, "metti in pausa la mia attività dependency-audit", "elimina l'attività standup-prep" o "mostrami le mie attività pianificate."

Per modificare il prompt di un'attività su disco, apri `~/.claude/scheduled-tasks/<task-name>/SKILL.md` (o sotto [`CLAUDE_CONFIG_DIR`](/it/env-vars) se impostato). Il file utilizza frontmatter YAML per `name` e `description`, con il prompt come corpo. Le modifiche hanno effetto al prossimo run. Pianificazione, cartella, modello e stato abilitato non sono in questo file: cambiali tramite il modulo Edit o chiedi a Claude.

## Environment configuration

L'ambiente che scegli quando [avvii una sessione](#start-a-session) determina dove Claude viene eseguito e come ti connetti:

* **Local**: viene eseguito sulla tua macchina con accesso diretto ai tuoi file
* **Remote**: viene eseguito sull'infrastruttura cloud di Anthropic. Le sessioni continuano anche se chiudi l'app.
* **SSH**: viene eseguito su una macchina remota a cui ti connetti tramite SSH, come i tuoi stessi server, VM cloud o dev container

### Local sessions

Le sessioni locali ereditano variabili di ambiente dalla tua shell. Se hai bisogno di variabili aggiuntive, impostale nel tuo profilo shell, come `~/.zshrc` o `~/.bashrc`, e riavvia l'app desktop. Vedi [variabili di ambiente](/it/env-vars) per l'elenco completo delle variabili supportate.

[Extended thinking](/it/common-workflows#use-extended-thinking-thinking-mode) è abilitato per impostazione predefinita, il che migliora le prestazioni su compiti di ragionamento complesso ma utilizza token aggiuntivi. Per disabilitare completamente il thinking, imposta `MAX_THINKING_TOKENS=0` nel tuo profilo shell. Su Opus, `MAX_THINKING_TOKENS` viene ignorato tranne per `0` perché il ragionamento adattivo controlla la profondità del thinking.

### Remote sessions

Le sessioni remote continuano in background anche se chiudi l'app. L'utilizzo conta verso i limiti del tuo [piano di abbonamento](/it/costs) senza costi di calcolo separati.

Puoi creare ambienti cloud personalizzati con diversi livelli di accesso alla rete e variabili di ambiente. Seleziona il menu a discesa dell'ambiente quando avvii una sessione remota e scegli **Add environment**. Vedi [cloud environments](/it/claude-code-on-the-web#cloud-environment) per i dettagli sulla configurazione dell'accesso alla rete e delle variabili di ambiente.

### SSH sessions

Le sessioni SSH ti consentono di eseguire Claude Code su una macchina remota mentre usi l'app desktop come tua interfaccia. Questo è utile per lavorare con codebase che vivono su VM cloud, dev container o server con hardware o dipendenze specifiche.

Per aggiungere una connessione SSH, fai clic sul menu a discesa dell'ambiente prima di avviare una sessione e seleziona **+ Add SSH connection**. La finestra di dialogo chiede:

* **Name**: un'etichetta amichevole per questa connessione
* **SSH Host**: `user@hostname` o un host definito in `~/.ssh/config`
* **SSH Port**: predefinito a 22 se lasciato vuoto, o utilizza la porta dal tuo SSH config
* **Identity File**: percorso della tua chiave privata, come `~/.ssh/id_rsa`. Lascia vuoto per usare la chiave predefinita o il tuo SSH config.

Una volta aggiunta, la connessione appare nel menu a discesa dell'ambiente. Selezionala per avviare una sessione su quella macchina. Claude viene eseguito sulla macchina remota con accesso ai suoi file e strumenti.

Claude Code deve essere installato sulla macchina remota. Una volta connesso, le sessioni SSH supportano modalità di autorizzazione, connettori, plugin e MCP servers.

## Enterprise configuration

Le organizzazioni su piani Teams o Enterprise possono gestire il comportamento dell'app desktop tramite controlli della console di amministrazione, file di impostazioni gestiti e criteri di gestione dei dispositivi.

### Admin console controls

Queste impostazioni sono configurate tramite la [console delle impostazioni di amministrazione](https://claude.ai/admin-settings/claude-code):

* **Code in the desktop**: controlla se gli utenti della tua organizzazione possono accedere a Claude Code nell'app desktop
* **Code in the web**: abilita o disabilita le [sessioni web](/it/claude-code-on-the-web) per la tua organizzazione
* **Remote Control**: abilita o disabilita [Remote Control](/it/remote-control) per la tua organizzazione
* **Disable Bypass permissions mode**: impedisci agli utenti della tua organizzazione di abilitare la modalità bypass permissions

### Managed settings

Le impostazioni gestite sovrascrivono le impostazioni del progetto e dell'utente e si applicano quando Desktop genera sessioni CLI. Puoi impostare queste chiavi nel file [impostazioni gestite](/it/settings#settings-precedence) della tua organizzazione o inviarle in remoto tramite la console di amministrazione.

| Chiave                                     | Descrizione                                                                                                                                                                                                          |
| ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `permissions.disableBypassPermissionsMode` | imposta su `"disable"` per impedire agli utenti di abilitare la modalità bypass permissions.                                                                                                                         |
| `disableAutoMode`                          | imposta su `"disable"` per impedire agli utenti di abilitare la modalità [Auto](/it/permission-modes#eliminate-prompts-with-auto-mode). Rimuove Auto dal selettore di modalità. Accettato anche sotto `permissions`. |
| `autoMode`                                 | personalizza cosa il classificatore della modalità auto si fida e blocca in tutta la tua organizzazione. Vedi [Configura il classificatore della modalità auto](/it/permissions#configure-the-auto-mode-classifier). |

`permissions.disableBypassPermissionsMode` e `disableAutoMode` funzionano anche nelle impostazioni dell'utente e del progetto, ma metterli nelle impostazioni gestite impedisce agli utenti di sovrascriverli. `autoMode` viene letto dalle impostazioni dell'utente, `.claude/settings.local.json` e impostazioni gestite, ma non da `.claude/settings.json` controllato: un repo clonato non può iniettare le sue stesse regole del classificatore. Per l'elenco completo delle impostazioni solo gestite incluse `allowManagedPermissionRulesOnly` e `allowManagedHooksOnly`, vedi [impostazioni solo gestite](/it/permissions#managed-only-settings).

Le impostazioni gestite remote caricate tramite la console di amministrazione attualmente si applicano solo alle sessioni CLI e IDE. Per le restrizioni specifiche di Desktop, usa i controlli della console di amministrazione sopra.

### Device management policies

I team IT possono gestire l'app desktop tramite MDM su macOS o criteri di gruppo su Windows. I criteri disponibili includono l'abilitazione o la disabilitazione della funzione Claude Code, il controllo degli aggiornamenti automatici e l'impostazione di un URL di distribuzione personalizzato.

* **macOS**: configura tramite il dominio di preferenza `com.anthropic.Claude` usando strumenti come Jamf o Kandji
* **Windows**: configura tramite il registro in `SOFTWARE\Policies\Claude`

### Authentication and SSO

Le organizzazioni aziendali possono richiedere SSO per tutti gli utenti. Vedi [autenticazione](/it/authentication) per i dettagli a livello di piano e [Configurazione di SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso) per la configurazione SAML e OIDC.

### Data handling

Claude Code elabora il tuo codice localmente nelle sessioni locali o sull'infrastruttura cloud di Anthropic nelle sessioni remote. Le conversazioni e il contesto del codice vengono inviati all'API di Anthropic per l'elaborazione. Vedi [gestione dei dati](/it/data-usage) per i dettagli sulla conservazione dei dati, la privacy e la conformità.

### Deployment

Desktop può essere distribuito tramite strumenti di distribuzione aziendale:

* **macOS**: distribuisci tramite MDM come Jamf o Kandji usando il programma di installazione `.dmg`
* **Windows**: distribuisci tramite pacchetto MSIX o programma di installazione `.exe`. Vedi [Distribuisci Claude Desktop per Windows](https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows) per le opzioni di distribuzione aziendale inclusa l'installazione silenziosa

Per la configurazione della rete come impostazioni proxy, allowlist del firewall e gateway LLM, vedi [configurazione della rete](/it/network-config).

Per il riferimento completo della configurazione aziendale, vedi la [guida alla configurazione aziendale](https://support.claude.com/en/articles/12622667-enterprise-configuration).

## Coming from the CLI?

Se usi già la CLI di Claude Code, Desktop esegue lo stesso motore sottostante con un'interfaccia grafica. Puoi eseguire entrambi contemporaneamente sulla stessa macchina, anche sullo stesso progetto. Ognuno mantiene una storia di sessione separata, ma condividono configurazione e memoria del progetto tramite file CLAUDE.md.

Per spostare una sessione CLI in Desktop, esegui `/desktop` nel terminale. Claude salva la tua sessione e l'apre nell'app desktop, quindi esce dalla CLI. Questo comando è disponibile solo su macOS e Windows.

<Tip>
  Quando usare Desktop vs CLI: usa Desktop quando vuoi revisione visiva dei diff, allegati di file o gestione della sessione in una barra laterale. Usa la CLI quando hai bisogno di scripting, automazione, provider di terze parti o preferisci un flusso di lavoro di terminale.
</Tip>

### CLI flag equivalents

Questa tabella mostra l'equivalente dell'app desktop per i flag CLI comuni. I flag non elencati non hanno equivalente desktop perché sono progettati per scripting o automazione.

| CLI                                   | Equivalente desktop                                                                                                                                                          |
| ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--model sonnet`                      | menu a discesa del modello accanto al pulsante di invio, prima di avviare una sessione                                                                                       |
| `--resume`, `--continue`              | fai clic su una sessione nella barra laterale                                                                                                                                |
| `--permission-mode`                   | selettore di modalità accanto al pulsante di invio                                                                                                                           |
| `--dangerously-skip-permissions`      | Modalità Bypass permissions. Abilita in Impostazioni → Claude Code → "Allow bypass permissions mode". Gli amministratori aziendali possono disabilitare questa impostazione. |
| `--add-dir`                           | aggiungi più repo con il pulsante **+** nelle sessioni remote                                                                                                                |
| `--allowedTools`, `--disallowedTools` | non disponibile in Desktop                                                                                                                                                   |
| `--verbose`                           | non disponibile. Controlla i log di sistema: Console.app su macOS, Event Viewer → Windows Logs → Application su Windows                                                      |
| `--print`, `--output-format`          | non disponibile. Desktop è solo interattivo.                                                                                                                                 |
| `ANTHROPIC_MODEL` env var             | menu a discesa del modello accanto al pulsante di invio                                                                                                                      |
| `MAX_THINKING_TOKENS` env var         | imposta nel profilo shell; si applica alle sessioni locali. Vedi [configurazione dell'ambiente](#environment-configuration).                                                 |

### Shared configuration

Desktop e CLI leggono gli stessi file di configurazione, quindi la tua configurazione viene trasferita:

* I file **[CLAUDE.md](/it/memory)** nel tuo progetto vengono utilizzati da entrambi
* I **[MCP servers](/it/mcp)** configurati in `~/.claude.json` o `.mcp.json` funzionano in entrambi
* **[Hooks](/it/hooks)** e **[skills](/it/skills)** definiti nelle impostazioni si applicano a entrambi
* **[Impostazioni](/it/settings)** in `~/.claude.json` e `~/.claude/settings.json` sono condivise. Le regole di autorizzazione, gli strumenti consentiti e altre impostazioni in `settings.json` si applicano alle sessioni Desktop.
* **Modelli**: Sonnet, Opus e Haiku sono disponibili in entrambi. In Desktop, seleziona il modello dal menu a discesa accanto al pulsante di invio prima di avviare una sessione. Non puoi cambiare il modello durante una sessione attiva.

<Note>
  **MCP servers: app desktop chat vs Claude Code**: i MCP servers configurati per l'app desktop chat Claude in `claude_desktop_config.json` sono separati da Claude Code e non appariranno nella scheda Code. Per usare MCP servers in Claude Code, configurali in `~/.claude.json` o nel file `.mcp.json` del tuo progetto. Vedi [configurazione MCP](/it/mcp#installing-mcp-servers) per i dettagli.
</Note>

### Feature comparison

Questa tabella confronta le capacità principali tra CLI e Desktop. Per un elenco completo dei flag CLI, vedi il [riferimento CLI](/it/cli-reference).

| Funzionalità                                            | CLI                                                       | Desktop                                                                                                             |
| ------------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Modalità di autorizzazione                              | tutte le modalità inclusa `dontAsk`                       | Chiedi autorizzazioni, Accetta automaticamente modifiche, Plan mode, Auto e Bypass permissions tramite Impostazioni |
| `--dangerously-skip-permissions`                        | Flag CLI                                                  | Modalità Bypass permissions. Abilita in Impostazioni → Claude Code → "Allow bypass permissions mode"                |
| [Provider di terze parti](/it/third-party-integrations) | Bedrock, Vertex, Foundry                                  | non disponibile. Desktop si connette direttamente all'API di Anthropic.                                             |
| [MCP servers](/it/mcp)                                  | configura nei file di impostazioni                        | UI Connectors per sessioni locali e SSH, o file di impostazioni                                                     |
| [Plugins](/it/plugins)                                  | comando `/plugin`                                         | UI gestore plugin                                                                                                   |
| @mention file                                           | basato su testo                                           | con autocomplete; sessioni locali e SSH solo                                                                        |
| Allegati di file                                        | non disponibile                                           | immagini, PDF                                                                                                       |
| Isolamento della sessione                               | flag [`--worktree`](/it/cli-reference)                    | worktree automatici                                                                                                 |
| Sessioni multiple                                       | terminali separati                                        | schede della barra laterale                                                                                         |
| Attività ricorrenti                                     | cron job, pipeline CI                                     | [attività pianificate](#schedule-recurring-tasks)                                                                   |
| Utilizzo del computer                                   | non disponibile                                           | [Controllo di app e schermo](#let-claude-use-your-computer) su macOS                                                |
| Integrazione Dispatch                                   | non disponibile                                           | [Sessioni Dispatch](#sessions-from-dispatch) nella barra laterale                                                   |
| Scripting e automazione                                 | [`--print`](/it/cli-reference), [Agent SDK](/it/headless) | non disponibile                                                                                                     |

### What's not available in Desktop

Le seguenti funzionalità sono disponibili solo nella CLI o nell'estensione VS Code:

* **Provider di terze parti**: Desktop si connette direttamente all'API di Anthropic. Usa la [CLI](/it/quickstart) con Bedrock, Vertex o Foundry.
* **Linux**: l'app desktop è disponibile solo su macOS e Windows.
* **Suggerimenti di codice inline**: Desktop non fornisce suggerimenti in stile autocomplete. Funziona tramite prompt conversazionali e modifiche di codice esplicite.
* **Team di agent**: l'orchestrazione multi-agent è disponibile tramite la [CLI](/it/agent-teams) e [Agent SDK](/it/headless), non in Desktop.

## Troubleshooting

### Check your version

Per vedere quale versione dell'app desktop stai eseguendo:

* **macOS**: fai clic su **Claude** nella barra dei menu, quindi **About Claude**
* **Windows**: fai clic su **Help**, quindi **About**

Fai clic sul numero di versione per copiarlo negli appunti.

### 403 or authentication errors in the Code tab

Se vedi `Error 403: Forbidden` o altri errori di autenticazione quando usi la scheda Code:

1. Esci e accedi di nuovo dal menu dell'app. Questo è il fix più comune.
2. Verifica di avere un abbonamento a pagamento attivo: Pro, Max, Teams o Enterprise.
3. Se la CLI funziona ma Desktop no, esci completamente dall'app desktop, non solo chiudere la finestra, quindi riapri e accedi di nuovo.
4. Controlla la tua connessione Internet e le impostazioni del proxy.

### Blank or stuck screen on launch

Se l'app si apre ma mostra una schermata vuota o non reattiva:

1. Riavvia l'app.
2. Controlla gli aggiornamenti in sospeso. L'app si aggiorna automaticamente al lancio.
3. Su Windows, controlla Event Viewer per i log di crash sotto **Windows Logs → Application**.

### "Failed to load session"

Se vedi `Failed to load session`, la cartella selezionata potrebbe non esistere più, un repository Git potrebbe richiedere Git LFS che non è installato, o i permessi dei file potrebbero impedire l'accesso. Prova a selezionare una cartella diversa o riavvia l'app.

### Session not finding installed tools

Se Claude non riesce a trovare strumenti come `npm`, `node` o altri comandi CLI, verifica che gli strumenti funzionino nel tuo terminale regolare, controlla che il tuo profilo shell configuri correttamente PATH e riavvia l'app desktop per ricaricare le variabili di ambiente.

### Git and Git LFS errors

Su Windows, Git è richiesto affinché la scheda Code avvii sessioni locali. Se vedi "Git is required," installa [Git per Windows](https://git-scm.com/downloads/win) e riavvia l'app.

Se vedi "Git LFS is required by this repository but is not installed," installa Git LFS da [git-lfs.com](https://git-lfs.com/), esegui `git lfs install` e riavvia l'app.

### MCP servers not working on Windows

Se gli interruttori del server MCP non rispondono o i server non riescono a connettersi su Windows, controlla che il server sia configurato correttamente nelle tue impostazioni, riavvia l'app, verifica che il processo del server sia in esecuzione in Task Manager e rivedi i log del server per gli errori di connessione.

### App won't quit

* **macOS**: premi Cmd+Q. Se l'app non risponde, usa Force Quit con Cmd+Option+Esc, seleziona Claude e fai clic su Force Quit.
* **Windows**: usa Task Manager con Ctrl+Shift+Esc per terminare il processo Claude.

### Windows-specific issues

* **PATH not updated after install**: apri una nuova finestra di terminale. Gli aggiornamenti di PATH si applicano solo alle nuove sessioni di terminale.
* **Concurrent installation error**: se vedi un errore su un'altra installazione in corso ma non ce n'è una, prova a eseguire il programma di installazione come Amministratore.
* **ARM64**: i dispositivi Windows ARM64 sono completamente supportati.

### Cowork tab unavailable on Intel Macs

La scheda Cowork richiede Apple Silicon (M1 o successivo) su macOS. Su Windows, Cowork è disponibile su tutto l'hardware supportato. Le schede Chat e Code funzionano normalmente su Mac Intel.

### "Branch doesn't exist yet" when opening in CLI

Le sessioni remote possono creare rami che non esistono sulla tua macchina locale. Fai clic sul nome del ramo nella barra degli strumenti della sessione per copiarlo, quindi recuperalo localmente:

```bash theme={null}
git fetch origin <branch-name>
git checkout <branch-name>
```

### Still stuck?

* Cerca o segnala un bug su [GitHub Issues](https://github.com/anthropics/claude-code/issues)
* Visita il [centro di supporto Claude](https://support.claude.com/)

Quando segnali un bug, includi la versione dell'app desktop, il tuo sistema operativo, il messaggio di errore esatto e i log pertinenti. Su macOS, controlla Console.app. Su Windows, controlla Event Viewer → Windows Logs → Application.
