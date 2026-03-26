> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Usa Claude Code in VS Code

> Installa e configura l'estensione Claude Code per VS Code. Ottieni assistenza di codifica con IA con diff inline, @-mention, revisione del piano e scorciatoie da tastiera.

<img src="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=300652d5678c63905e6b0ea9e50835f8" alt="Editor VS Code con il pannello dell'estensione Claude Code aperto sul lato destro, che mostra una conversazione con Claude" width="2500" height="1155" data-path="images/vs-code-extension-interface.jpg" />

L'estensione VS Code fornisce un'interfaccia grafica nativa per Claude Code, integrata direttamente nel tuo IDE. Questo è il modo consigliato per utilizzare Claude Code in VS Code.

Con l'estensione, puoi rivedere e modificare i piani di Claude prima di accettarli, accettare automaticamente le modifiche mentre vengono apportate, @-mention file con intervalli di righe specifici dalla tua selezione, accedere alla cronologia delle conversazioni e aprire più conversazioni in schede o finestre separate.

## Prerequisiti

Prima di installare, assicurati di avere:

* VS Code 1.98.0 o superiore
* Un account Anthropic (accederai quando aprirai l'estensione per la prima volta). Se stai utilizzando un provider di terze parti come Amazon Bedrock o Google Vertex AI, consulta invece [Usa provider di terze parti](#use-third-party-providers).

<Tip>
  L'estensione include la CLI (interfaccia della riga di comando), a cui puoi accedere dal terminale integrato di VS Code per funzioni avanzate. Consulta [Estensione VS Code vs. Claude Code CLI](#vs-code-extension-vs-claude-code-cli) per i dettagli.
</Tip>

## Installa l'estensione

Fai clic sul link per il tuo IDE per installare direttamente:

* [Installa per VS Code](vscode:extension/anthropic.claude-code)
* [Installa per Cursor](cursor:extension/anthropic.claude-code)

Oppure in VS Code, premi `Cmd+Shift+X` (Mac) o `Ctrl+Shift+X` (Windows/Linux) per aprire la visualizzazione Estensioni, cerca "Claude Code" e fai clic su **Installa**.

<Note>Se l'estensione non appare dopo l'installazione, riavvia VS Code o esegui "Developer: Reload Window" dalla Tavolozza dei comandi.</Note>

## Inizia

Una volta installata, puoi iniziare a utilizzare Claude Code tramite l'interfaccia VS Code:

<Steps>
  <Step title="Apri il pannello Claude Code">
    In tutto VS Code, l'icona Spark indica Claude Code: <img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/vs-code-spark-icon.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=3ca45e00deadec8c8f4b4f807da94505" alt="Icona Spark" style={{display: "inline", height: "0.85em", verticalAlign: "middle"}} width="16" height="16" data-path="images/vs-code-spark-icon.svg" />

    Il modo più veloce per aprire Claude è fare clic sull'icona Spark nella **Barra degli strumenti dell'editor** (angolo in alto a destra dell'editor). L'icona appare solo quando hai un file aperto.

        <img src="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=eb4540325d94664c51776dbbfec4cf02" alt="Editor VS Code che mostra l'icona Spark nella Barra degli strumenti dell'editor" width="2796" height="734" data-path="images/vs-code-editor-icon.png" />

    Altri modi per aprire Claude Code:

    * **Barra attività**: fai clic sull'icona Spark nella barra laterale sinistra per aprire l'elenco delle sessioni. Fai clic su qualsiasi sessione per aprirla come scheda dell'editor completa, o avvia una nuova. Questa icona è sempre visibile nella Barra attività.
    * **Tavolozza dei comandi**: `Cmd+Shift+P` (Mac) o `Ctrl+Shift+P` (Windows/Linux), digita "Claude Code" e seleziona un'opzione come "Apri in Nuova Scheda"
    * **Barra di stato**: fai clic su **✱ Claude Code** nell'angolo in basso a destra della finestra. Funziona anche quando nessun file è aperto.

    Quando apri il pannello per la prima volta, appare una checklist **Impara Claude Code**. Completa ogni elemento facendo clic su **Mostrami**, oppure chiudila con la X. Per riaprirla in seguito, deseleziona **Nascondi onboarding** nelle impostazioni di VS Code in Estensioni → Claude Code.

    Puoi trascinare il pannello Claude per riposizionarlo ovunque in VS Code. Consulta [Personalizza il tuo flusso di lavoro](#customize-your-workflow) per i dettagli.
  </Step>

  <Step title="Invia un prompt">
    Chiedi a Claude di aiutarti con il tuo codice o i tuoi file, che si tratti di spiegare come funziona qualcosa, eseguire il debug di un problema o apportare modifiche.

    <Tip>Claude vede automaticamente il testo selezionato. Premi `Option+K` (Mac) / `Alt+K` (Windows/Linux) per inserire anche un riferimento @-mention (come `@file.ts#5-10`) nel tuo prompt.</Tip>

    Ecco un esempio di domanda su una riga particolare in un file:

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=ede3ed8d8d5f940e01c5de636d009cfd" alt="Editor VS Code con le righe 2-3 selezionate in un file Python e il pannello Claude Code che mostra una domanda su quelle righe con un riferimento @-mention" width="3288" height="1876" data-path="images/vs-code-send-prompt.png" />
  </Step>

  <Step title="Rivedi le modifiche">
    Quando Claude vuole modificare un file, mostra un confronto affiancato dell'originale e delle modifiche proposte, quindi chiede il permesso. Puoi accettare, rifiutare o dire a Claude cosa fare invece.

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=e005f9b41c541c5c7c59c082f7c4841c" alt="VS Code che mostra un diff delle modifiche proposte da Claude con un prompt di permesso che chiede se apportare la modifica" width="3292" height="1876" data-path="images/vs-code-edits.png" />
  </Step>
</Steps>

Per altre idee su cosa puoi fare con Claude Code, consulta [Flussi di lavoro comuni](/it/common-workflows).

<Tip>
  Esegui "Claude Code: Open Walkthrough" dalla Tavolozza dei comandi per una visita guidata delle nozioni di base.
</Tip>

## Usa la casella dei prompt

La casella dei prompt supporta diverse funzioni:

* **Modalità di permesso**: fai clic sull'indicatore di modalità in fondo alla casella dei prompt per cambiare modalità. In modalità normale, Claude chiede il permesso prima di ogni azione. In Plan Mode, Claude descrive cosa farà e attende l'approvazione prima di apportare modifiche. VS Code apre automaticamente il piano come documento markdown completo dove puoi aggiungere commenti inline per fornire feedback prima che Claude inizi. In modalità auto-accept, Claude apporta modifiche senza chiedere. Imposta il valore predefinito nelle impostazioni di VS Code in `claudeCode.initialPermissionMode`.
* **Menu dei comandi**: fai clic su `/` o digita `/` per aprire il menu dei comandi. Le opzioni includono l'allegato di file, il cambio di modelli, l'attivazione del pensiero esteso, la visualizzazione dell'utilizzo del piano (`/usage`) e l'avvio di una sessione [Remote Control](/it/remote-control) (`/remote-control`). La sezione Personalizza fornisce accesso ai server MCP, hooks, memoria, autorizzazioni e plugin. Gli elementi con un'icona del terminale si aprono nel terminale integrato.
* **Indicatore di contesto**: la casella dei prompt mostra quanto della finestra di contesto di Claude stai utilizzando. Claude si compatta automaticamente quando necessario, oppure puoi eseguire `/compact` manualmente.
* **Pensiero esteso**: consente a Claude di dedicare più tempo al ragionamento su problemi complessi. Attivalo tramite il menu dei comandi (`/`). Consulta [Pensiero esteso](/it/common-workflows#use-extended-thinking-thinking-mode) per i dettagli.
* **Input multi-riga**: premi `Shift+Enter` per aggiungere una nuova riga senza inviare. Funziona anche nell'input di testo libero "Altro" dei dialoghi delle domande.

### Riferisci file e cartelle

Usa @-mention per dare a Claude il contesto su file o cartelle specifiche. Quando digiti `@` seguito da un nome di file o cartella, Claude legge quel contenuto e può rispondere a domande su di esso o apportare modifiche. Claude Code supporta la corrispondenza fuzzy, quindi puoi digitare nomi parziali per trovare quello che ti serve:

```text  theme={null}
> Explain the logic in @auth (fuzzy matches auth.js, AuthService.ts, etc.)
> What's in @src/components/ (include a trailing slash for folders)
```

Per i PDF di grandi dimensioni, puoi chiedere a Claude di leggere pagine specifiche invece dell'intero file: una singola pagina, un intervallo come pagine 1-10, o un intervallo aperto come pagina 3 in poi.

Quando selezioni il testo nell'editor, Claude può vedere il tuo codice evidenziato automaticamente. Il piè di pagina della casella dei prompt mostra quante righe sono selezionate. Premi `Option+K` (Mac) / `Alt+K` (Windows/Linux) per inserire un @-mention con il percorso del file e i numeri di riga (ad es. `@app.ts#5-10`). Fai clic sull'indicatore di selezione per attivare/disattivare se Claude può vedere il tuo testo evidenziato - l'icona occhio-barra significa che la selezione è nascosta a Claude.

Puoi anche tenere premuto `Shift` mentre trascini i file nella casella dei prompt per aggiungerli come allegati. Fai clic sulla X su qualsiasi allegato per rimuoverlo dal contesto.

### Riprendi conversazioni passate

Fai clic sul menu a discesa in cima al pannello Claude Code per accedere alla cronologia delle conversazioni. Puoi cercare per parola chiave o sfogliare per tempo (Oggi, Ieri, Ultimi 7 giorni, ecc.). Fai clic su qualsiasi conversazione per riprenderla con la cronologia completa dei messaggi. Le nuove sessioni ricevono titoli generati dall'IA in base al tuo primo messaggio. Passa il mouse su una sessione per rivelare le azioni di rinomina e rimozione: rinomina per darle un titolo descrittivo, o rimuovi per eliminarla dall'elenco. Per ulteriori informazioni sulla ripresa delle sessioni, consulta [Flussi di lavoro comuni](/it/common-workflows#resume-previous-conversations).

### Riprendi sessioni remote da Claude.ai

Se utilizzi [Claude Code sul web](/it/claude-code-on-the-web), puoi riprendere quelle sessioni remote direttamente in VS Code. Ciò richiede l'accesso con **Claude.ai Subscription**, non Anthropic Console.

<Steps>
  <Step title="Apri Conversazioni Passate">
    Fai clic sul menu a discesa **Conversazioni Passate** in cima al pannello Claude Code.
  </Step>

  <Step title="Seleziona la scheda Remote">
    La finestra di dialogo mostra due schede: Local e Remote. Fai clic su **Remote** per vedere le sessioni da claude.ai.
  </Step>

  <Step title="Seleziona una sessione da riprendere">
    Sfoglia o cerca le tue sessioni remote. Fai clic su qualsiasi sessione per scaricarla e continuare la conversazione localmente.
  </Step>
</Steps>

<Note>
  Solo le sessioni web avviate con un repository GitHub appaiono nella scheda Remote. La ripresa carica la cronologia della conversazione localmente; le modifiche non vengono sincronizzate di nuovo a claude.ai.
</Note>

## Personalizza il tuo flusso di lavoro

Una volta che sei operativo, puoi riposizionare il pannello Claude, eseguire più sessioni o passare alla modalità terminale.

### Scegli dove vive Claude

Puoi trascinare il pannello Claude per riposizionarlo ovunque in VS Code. Afferra la scheda o la barra del titolo del pannello e trascinalo a:

* **Barra laterale secondaria**: il lato destro della finestra. Mantiene Claude visibile mentre codifichi.
* **Barra laterale primaria**: la barra laterale sinistra con icone per Explorer, Search, ecc.
* **Area dell'editor**: apre Claude come scheda insieme ai tuoi file. Utile per attività secondarie.

<Tip>
  Usa la barra laterale per la tua sessione Claude principale e apri schede aggiuntive per attività secondarie. Claude ricorda la tua posizione preferita. L'icona dell'elenco delle sessioni della Barra attività è separata dal pannello Claude: l'elenco delle sessioni è sempre visibile nella Barra attività, mentre l'icona del pannello Claude appare lì solo quando il pannello è ancorato alla barra laterale sinistra.
</Tip>

### Esegui più conversazioni

Usa **Apri in Nuova Scheda** o **Apri in Nuova Finestra** dalla Tavolozza dei comandi per avviare conversazioni aggiuntive. Ogni conversazione mantiene la propria cronologia e contesto, permettendoti di lavorare su diversi compiti in parallelo.

Quando usi le schede, un piccolo punto colorato sull'icona spark indica lo stato: blu significa che una richiesta di permesso è in sospeso, arancione significa che Claude ha finito mentre la scheda era nascosta.

### Passa alla modalità terminale

Per impostazione predefinita, l'estensione apre un pannello di chat grafico. Se preferisci l'interfaccia in stile CLI, apri l'[impostazione Use Terminal](vscode://settings/claudeCode.useTerminal) e seleziona la casella.

Puoi anche aprire le impostazioni di VS Code (`Cmd+,` su Mac o `Ctrl+,` su Windows/Linux), vai a Estensioni → Claude Code e seleziona **Use Terminal**.

## Gestisci i plugin

L'estensione VS Code include un'interfaccia grafica per installare e gestire i [plugin](/it/plugins). Digita `/plugins` nella casella dei prompt per aprire l'interfaccia **Gestisci plugin**.

### Installa i plugin

La finestra di dialogo del plugin mostra due schede: **Plugin** e **Marketplaces**.

Nella scheda Plugin:

* I **plugin installati** appaiono in cima con interruttori per abilitarli o disabilitarli
* I **plugin disponibili** dai tuoi marketplace configurati appaiono sotto
* Cerca per filtrare i plugin per nome o descrizione
* Fai clic su **Installa** su qualsiasi plugin disponibile

Quando installi un plugin, scegli l'ambito di installazione:

* **Installa per te**: disponibile in tutti i tuoi progetti (ambito utente)
* **Installa per questo progetto**: condiviso con i collaboratori del progetto (ambito progetto)
* **Installa localmente**: solo per te, solo in questo repository (ambito locale)

### Gestisci i marketplace

Passa alla scheda **Marketplaces** per aggiungere o rimuovere fonti di plugin:

* Inserisci un repository GitHub, URL o percorso locale per aggiungere un nuovo marketplace
* Fai clic sull'icona di aggiornamento per aggiornare l'elenco dei plugin di un marketplace
* Fai clic sull'icona del cestino per rimuovere un marketplace

Dopo aver apportato modifiche, un banner ti chiede di riavviare Claude Code per applicare gli aggiornamenti.

<Note>
  La gestione dei plugin in VS Code utilizza gli stessi comandi CLI sotto il cofano. I plugin e i marketplace che configuri nell'estensione sono disponibili anche nella CLI e viceversa.
</Note>

Per ulteriori informazioni sul sistema dei plugin, consulta [Plugins](/it/plugins) e [Plugin marketplaces](/it/plugin-marketplaces).

## Automatizza le attività del browser con Chrome

Connetti Claude al tuo browser Chrome per testare app web, eseguire il debug con i log della console e automatizzare i flussi di lavoro del browser senza lasciare VS Code. Ciò richiede l'[estensione Claude in Chrome](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) versione 1.0.36 o superiore.

Digita `@browser` nella casella dei prompt seguito da quello che vuoi che Claude faccia:

```text  theme={null}
@browser go to localhost:3000 and check the console for errors
```

Puoi anche aprire il menu degli allegati per selezionare strumenti specifici del browser come aprire una nuova scheda o leggere il contenuto della pagina.

Claude apre nuove schede per le attività del browser e condivide lo stato di accesso del tuo browser, quindi può accedere a qualsiasi sito a cui sei già connesso.

Per le istruzioni di configurazione, l'elenco completo delle funzionalità e la risoluzione dei problemi, consulta [Usa Claude Code con Chrome](/it/chrome).

## Comandi e scorciatoie da tastiera di VS Code

Apri la Tavolozza dei comandi (`Cmd+Shift+P` su Mac o `Ctrl+Shift+P` su Windows/Linux) e digita "Claude Code" per vedere tutti i comandi VS Code disponibili per l'estensione Claude Code.

Alcuni scorciatoie dipendono da quale pannello è "focalizzato" (riceve input da tastiera). Quando il tuo cursore è in un file di codice, l'editor è focalizzato. Quando il tuo cursore è nella casella dei prompt di Claude, Claude è focalizzato. Usa `Cmd+Esc` / `Ctrl+Esc` per alternare tra loro.

<Note>
  Questi sono comandi VS Code per controllare l'estensione. Non tutti i comandi Claude Code incorporati sono disponibili nell'estensione. Consulta [Estensione VS Code vs. Claude Code CLI](#vs-code-extension-vs-claude-code-cli) per i dettagli.
</Note>

| Comando                    | Scorciatoia                                              | Descrizione                                                                                        |
| -------------------------- | -------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Focus Input                | `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux)             | Alterna lo stato attivo tra editor e Claude                                                        |
| Open in Side Bar           | -                                                        | Apri Claude nella barra laterale sinistra                                                          |
| Open in Terminal           | -                                                        | Apri Claude in modalità terminale                                                                  |
| Open in New Tab            | `Cmd+Shift+Esc` (Mac) / `Ctrl+Shift+Esc` (Windows/Linux) | Apri una nuova conversazione come scheda dell'editor                                               |
| Open in New Window         | -                                                        | Apri una nuova conversazione in una finestra separata                                              |
| New Conversation           | `Cmd+N` (Mac) / `Ctrl+N` (Windows/Linux)                 | Avvia una nuova conversazione (richiede che Claude sia focalizzato)                                |
| Insert @-Mention Reference | `Option+K` (Mac) / `Alt+K` (Windows/Linux)               | Inserisci un riferimento al file corrente e alla selezione (richiede che l'editor sia focalizzato) |
| Show Logs                  | -                                                        | Visualizza i log di debug dell'estensione                                                          |
| Logout                     | -                                                        | Esci dal tuo account Anthropic                                                                     |

### Avvia una scheda VS Code da altri strumenti

L'estensione registra un gestore URI in `vscode://anthropic.claude-code/open`. Usalo per aprire una nuova scheda Claude Code dal tuo strumento: un alias shell, un bookmarklet del browser o qualsiasi script che possa aprire un URL. Se VS Code non è già in esecuzione, l'apertura dell'URL lo avvia prima. Se VS Code è già in esecuzione, l'URL si apre nella finestra attualmente focalizzata.

Richiama il gestore con l'opener URL del tuo sistema operativo. Su macOS:

```bash  theme={null}
open "vscode://anthropic.claude-code/open"
```

Usa `xdg-open` su Linux o `start` su Windows.

Il gestore accetta due parametri di query facoltativi:

| Parametro | Descrizione                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prompt`  | Testo per pre-compilare nella casella dei prompt. Deve essere codificato in URL. Il prompt è pre-compilato ma non inviato automaticamente.                                                                                                                                                                                                                                                                                                          |
| `session` | Un ID di sessione da riprendere invece di avviare una nuova conversazione. La sessione deve appartenere all'area di lavoro attualmente aperta in VS Code. Se la sessione non viene trovata, viene avviata una conversazione nuova. Se la sessione è già aperta in una scheda, quella scheda viene focalizzata. Per acquisire un ID di sessione a livello di programmazione, consulta [Continua conversazioni](/it/headless#continue-conversations). |

Ad esempio, per aprire una scheda pre-compilata con "review my changes":

```text  theme={null}
vscode://anthropic.claude-code/open?prompt=review%20my%20changes
```

## Configura le impostazioni

L'estensione ha due tipi di impostazioni:

* **Impostazioni dell'estensione** in VS Code: controllano il comportamento dell'estensione all'interno di VS Code. Apri con `Cmd+,` (Mac) o `Ctrl+,` (Windows/Linux), quindi vai a Estensioni → Claude Code. Puoi anche digitare `/` e selezionare **General Config** per aprire le impostazioni.
* **Impostazioni Claude Code** in `~/.claude/settings.json`: condivise tra l'estensione e la CLI. Usa per comandi consentiti, variabili di ambiente, hooks e server MCP. Consulta [Impostazioni](/it/settings) per i dettagli.

<Tip>
  Aggiungi `"$schema": "https://json.schemastore.org/claude-code-settings.json"` al tuo `settings.json` per ottenere l'autocompletamento e la convalida inline per tutte le impostazioni disponibili direttamente in VS Code.
</Tip>

### Impostazioni dell'estensione

| Impostazione                      | Predefinito | Descrizione                                                                                                                                                                                                                                                                                                                                         |
| --------------------------------- | ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `selectedModel`                   | `default`   | Modello per le nuove conversazioni. Cambia per sessione con `/model`.                                                                                                                                                                                                                                                                               |
| `useTerminal`                     | `false`     | Avvia Claude in modalità terminale invece di pannello grafico                                                                                                                                                                                                                                                                                       |
| `initialPermissionMode`           | `default`   | Controlla i prompt di approvazione per le nuove conversazioni: `default`, `plan`, `acceptEdits`, `auto`, o `bypassPermissions`. Consulta [modalità di permesso](/it/permission-modes).                                                                                                                                                              |
| `preferredLocation`               | `panel`     | Dove Claude si apre: `sidebar` (destra) o `panel` (nuova scheda)                                                                                                                                                                                                                                                                                    |
| `autosave`                        | `true`      | Salva automaticamente i file prima che Claude li legga o scriva                                                                                                                                                                                                                                                                                     |
| `useCtrlEnterToSend`              | `false`     | Usa Ctrl/Cmd+Enter invece di Enter per inviare i prompt                                                                                                                                                                                                                                                                                             |
| `enableNewConversationShortcut`   | `true`      | Abilita Cmd/Ctrl+N per avviare una nuova conversazione                                                                                                                                                                                                                                                                                              |
| `hideOnboarding`                  | `false`     | Nascondi la checklist di onboarding (icona del berretto di laurea)                                                                                                                                                                                                                                                                                  |
| `respectGitIgnore`                | `true`      | Escludi i modelli .gitignore dalle ricerche di file                                                                                                                                                                                                                                                                                                 |
| `environmentVariables`            | `[]`        | Imposta le variabili di ambiente per il processo Claude. Usa invece le impostazioni Claude Code per la configurazione condivisa.                                                                                                                                                                                                                    |
| `disableLoginPrompt`              | `false`     | Salta i prompt di autenticazione (per configurazioni di provider di terze parti)                                                                                                                                                                                                                                                                    |
| `allowDangerouslySkipPermissions` | `false`     | Aggiunge le modalità [Auto](/it/permission-modes#eliminate-prompts-with-auto-mode) e Bypass al selettore di modalità. Auto richiede un piano Team e Claude Sonnet 4.6 o Opus 4.6, quindi l'opzione potrebbe rimanere non disponibile anche con questo interruttore attivato. Usa le autorizzazioni Bypass solo in sandbox senza accesso a Internet. |
| `claudeProcessWrapper`            | -           | Percorso eseguibile utilizzato per avviare il processo Claude                                                                                                                                                                                                                                                                                       |

## Estensione VS Code vs. Claude Code CLI

Claude Code è disponibile sia come estensione VS Code (pannello grafico) che come CLI (interfaccia della riga di comando nel terminale). Alcune funzioni sono disponibili solo nella CLI. Se hai bisogno di una funzione solo CLI, esegui `claude` nel terminale integrato di VS Code.

| Funzione                      | CLI                   | Estensione VS Code                                                                                  |
| ----------------------------- | --------------------- | --------------------------------------------------------------------------------------------------- |
| Comandi e skills              | [Tutti](/it/commands) | Sottoinsieme (digita `/` per vedere quelli disponibili)                                             |
| Configurazione del server MCP | Sì                    | Parziale (aggiungi server tramite CLI; gestisci i server esistenti con `/mcp` nel pannello di chat) |
| Checkpoint                    | Sì                    | Sì                                                                                                  |
| Scorciatoia bash `!`          | Sì                    | No                                                                                                  |
| Completamento scheda          | Sì                    | No                                                                                                  |

### Riavvolgi con i checkpoint

L'estensione VS Code supporta i checkpoint, che tracciano le modifiche ai file di Claude e ti permettono di riavvolgere a uno stato precedente. Passa il mouse su qualsiasi messaggio per rivelare il pulsante di riavvolgimento, quindi scegli tra tre opzioni:

* **Crea un ramo di conversazione da qui**: avvia un nuovo ramo di conversazione da questo messaggio mantenendo intatte tutte le modifiche al codice
* **Riavvolgi il codice a qui**: ripristina le modifiche ai file a questo punto della conversazione mantenendo la cronologia completa della conversazione
* **Crea un ramo di conversazione e riavvolgi il codice**: avvia un nuovo ramo di conversazione e ripristina le modifiche ai file a questo punto

Per i dettagli completi su come funzionano i checkpoint e le loro limitazioni, consulta [Checkpointing](/it/checkpointing).

### Esegui CLI in VS Code

Per utilizzare la CLI mentre rimani in VS Code, apri il terminale integrato (`` Ctrl+` `` su Windows/Linux o `` Cmd+` `` su Mac) ed esegui `claude`. La CLI si integra automaticamente con il tuo IDE per funzioni come la visualizzazione dei diff e la condivisione dei diagnostici.

Se utilizzi un terminale esterno, esegui `/ide` all'interno di Claude Code per collegarlo a VS Code.

### Passa tra l'estensione e la CLI

L'estensione e la CLI condividono la stessa cronologia delle conversazioni. Per continuare una conversazione dell'estensione nella CLI, esegui `claude --resume` nel terminale. Questo apre un selettore interattivo dove puoi cercare e selezionare la tua conversazione.

### Includi l'output del terminale nei prompt

Fai riferimento all'output del terminale nei tuoi prompt usando `@terminal:name` dove `name` è il titolo del terminale. Questo consente a Claude di vedere l'output dei comandi, i messaggi di errore o i log senza copia-incolla.

### Monitora i processi in background

Quando Claude esegue comandi di lunga durata, l'estensione mostra l'avanzamento nella barra di stato. Tuttavia, la visibilità per le attività in background è limitata rispetto alla CLI. Per una migliore visibilità, chiedi a Claude di emettere il comando in modo da poterlo eseguire nel terminale integrato di VS Code.

### Connettiti a strumenti esterni con MCP

I server MCP (Model Context Protocol) danno a Claude accesso a strumenti esterni, database e API.

Per aggiungere un server MCP, apri il terminale integrato (`` Ctrl+` `` o `` Cmd+` ``) ed esegui:

```bash  theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Una volta configurato, chiedi a Claude di utilizzare gli strumenti (ad es. "Review PR #456").

Per gestire i server MCP senza lasciare VS Code, digita `/mcp` nel pannello di chat. La finestra di dialogo di gestione MCP ti consente di abilitare o disabilitare i server, riconnetterti a un server e gestire l'autenticazione OAuth. Consulta la [documentazione MCP](/it/mcp) per i server disponibili.

## Lavora con git

Claude Code si integra con git per aiutare con i flussi di lavoro di controllo della versione direttamente in VS Code. Chiedi a Claude di eseguire il commit delle modifiche, creare pull request o lavorare tra i rami.

### Crea commit e pull request

Claude può mettere in stage le modifiche, scrivere messaggi di commit e creare pull request in base al tuo lavoro:

```text  theme={null}
> commit my changes with a descriptive message
> create a pr for this feature
> summarize the changes I've made to the auth module
```

Quando crei pull request, Claude genera descrizioni in base alle modifiche effettive del codice e può aggiungere contesto su test o decisioni di implementazione.

### Usa git worktrees per attività parallele

Usa il flag `--worktree` (`-w`) per avviare Claude in un worktree isolato con i suoi file e ramo:

```bash  theme={null}
claude --worktree feature-auth
```

Ogni worktree mantiene uno stato di file indipendente mentre condivide la cronologia di git. Ciò impedisce alle istanze di Claude di interferire l'una con l'altra quando lavorano su diversi compiti. Per ulteriori dettagli, consulta [Esegui sessioni parallele di Claude Code con Git worktrees](/it/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees).

## Usa provider di terze parti

Per impostazione predefinita, Claude Code si connette direttamente all'API di Anthropic. Se la tua organizzazione utilizza Amazon Bedrock, Google Vertex AI o Microsoft Foundry per accedere a Claude, configura l'estensione per utilizzare il tuo provider:

<Steps>
  <Step title="Disabilita il prompt di accesso">
    Apri l'[impostazione Disable Login Prompt](vscode://settings/claudeCode.disableLoginPrompt) e seleziona la casella.

    Puoi anche aprire le impostazioni di VS Code (`Cmd+,` su Mac o `Ctrl+,` su Windows/Linux), cercare "Claude Code login" e selezionare **Disable Login Prompt**.
  </Step>

  <Step title="Configura il tuo provider">
    Segui la guida di configurazione per il tuo provider:

    * [Claude Code su Amazon Bedrock](/it/amazon-bedrock)
    * [Claude Code su Google Vertex AI](/it/google-vertex-ai)
    * [Claude Code su Microsoft Foundry](/it/microsoft-foundry)

    Queste guide coprono la configurazione del tuo provider in `~/.claude/settings.json`, che garantisce che le tue impostazioni siano condivise tra l'estensione VS Code e la CLI.
  </Step>
</Steps>

## Sicurezza e privacy

Il tuo codice rimane privato. Claude Code elabora il tuo codice per fornire assistenza ma non lo utilizza per addestrare i modelli. Per i dettagli sulla gestione dei dati e su come rinunciare alla registrazione, consulta [Dati e privacy](/it/data-usage).

Con le autorizzazioni di auto-edit abilitate, Claude Code può modificare i file di configurazione di VS Code (come `settings.json` o `tasks.json`) che VS Code potrebbe eseguire automaticamente. Per ridurre il rischio quando si lavora con codice non attendibile:

* Abilita la [Modalità limitata di VS Code](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode) per gli spazi di lavoro non attendibili
* Usa la modalità di approvazione manuale invece di auto-accept per le modifiche
* Rivedi attentamente le modifiche prima di accettarle

### Il server IDE MCP incorporato

Quando l'estensione è attiva, esegue un server MCP locale a cui la CLI si connette automaticamente. Questo è il modo in cui la CLI apre i diff nel visualizzatore diff nativo di VS Code, legge la tua selezione corrente per i riferimenti `@` e — quando stai lavorando in un notebook Jupyter — chiede a VS Code di eseguire le celle.

Il server è denominato `ide` ed è nascosto da `/mcp` perché non c'è nulla da configurare. Se la tua organizzazione utilizza un hook `PreToolUse` per consentire gli strumenti MCP, tuttavia, dovrai sapere che esiste.

**Trasporto e autenticazione.** Il server si associa a `127.0.0.1` su una porta alta casuale e non è raggiungibile da altre macchine. Ogni attivazione dell'estensione genera un token di autenticazione casuale fresco che la CLI deve presentare per connettersi. Il token viene scritto in un file di blocco in `~/.claude/ide/` con autorizzazioni `0600` in una directory `0700`, quindi solo l'utente che esegue VS Code può leggerlo.

**Strumenti esposti al modello.** Il server ospita una dozzina di strumenti, ma solo due sono visibili al modello. Il resto è RPC interno che la CLI utilizza per la sua stessa UI — apertura di diff, lettura di selezioni, salvataggio di file — e viene filtrato prima che l'elenco degli strumenti raggiunga Claude.

| Nome dello strumento (come visto dagli hook) | Cosa fa                                                                                                                                        | Scrive? |
| -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `mcp__ide__getDiagnostics`                   | Restituisce i diagnostici del language server — gli errori e gli avvisi nel pannello Problemi di VS Code. Facoltativamente limitato a un file. | No      |
| `mcp__ide__executeCode`                      | Esegue il codice Python nel kernel del notebook Jupyter attivo. Consulta il flusso di conferma di seguito.                                     | Sì      |

**L'esecuzione di Jupyter chiede sempre prima.** `mcp__ide__executeCode` non può eseguire nulla silenziosamente. Ad ogni chiamata, il codice viene inserito come una nuova cella alla fine del notebook attivo, VS Code lo scorre in vista e una Quick Pick nativa ti chiede di **Eseguire** o **Annullare**. L'annullamento — o la chiusura della selezione con `Esc` — restituisce un errore a Claude e nulla viene eseguito. Lo strumento rifiuta anche completamente quando non c'è un notebook attivo, quando l'estensione Jupyter (`ms-toolsai.jupyter`) non è installata, o quando il kernel non è Python.

<Note>
  La conferma Quick Pick è separata dagli hook `PreToolUse`. Una voce di elenco consentiti per `mcp__ide__executeCode` consente a Claude di *proporre* l'esecuzione di una cella; la Quick Pick all'interno di VS Code è quello che le consente di *effettivamente* eseguirla.
</Note>

## Risolvi i problemi comuni

### L'estensione non si installa

* Assicurati di avere una versione compatibile di VS Code (1.98.0 o successiva)
* Verifica che VS Code abbia il permesso di installare estensioni
* Prova a installare direttamente dal [VS Code Marketplace](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)

### L'icona Spark non è visibile

L'icona Spark appare nella **Barra degli strumenti dell'editor** (in alto a destra dell'editor) quando hai un file aperto. Se non la vedi:

1. **Apri un file**: L'icona richiede che un file sia aperto. Avere solo una cartella aperta non è sufficiente.
2. **Controlla la versione di VS Code**: Richiede 1.98.0 o superiore (Aiuto → Informazioni)
3. **Riavvia VS Code**: Esegui "Developer: Reload Window" dalla Tavolozza dei comandi
4. **Disabilita le estensioni in conflitto**: Disabilita temporaneamente altre estensioni AI (Cline, Continue, ecc.)
5. **Controlla l'affidabilità dell'area di lavoro**: L'estensione non funziona in Modalità limitata

In alternativa, fai clic su "✱ Claude Code" nella **Barra di stato** (angolo in basso a destra). Funziona anche senza un file aperto. Puoi anche usare la **Tavolozza dei comandi** (`Cmd+Shift+P` / `Ctrl+Shift+P`) e digitare "Claude Code".

### Claude Code non risponde mai

Se Claude Code non risponde ai tuoi prompt:

1. **Controlla la tua connessione Internet**: Assicurati di avere una connessione Internet stabile
2. **Avvia una nuova conversazione**: Prova ad avviare una conversazione nuova per vedere se il problema persiste
3. **Prova la CLI**: Esegui `claude` dal terminale per vedere se ottieni messaggi di errore più dettagliati

Se i problemi persistono, [apri un problema su GitHub](https://github.com/anthropics/claude-code/issues) con i dettagli dell'errore.

## Disinstalla l'estensione

Per disinstallare l'estensione Claude Code:

1. Apri la visualizzazione Estensioni (`Cmd+Shift+X` su Mac o `Ctrl+Shift+X` su Windows/Linux)
2. Cerca "Claude Code"
3. Fai clic su **Disinstalla**

Per rimuovere anche i dati dell'estensione e ripristinare tutte le impostazioni:

```bash  theme={null}
rm -rf ~/.vscode/globalStorage/anthropic.claude-code
```

Per ulteriore aiuto, consulta la [guida alla risoluzione dei problemi](/it/troubleshooting).

## Passaggi successivi

Ora che hai Claude Code configurato in VS Code:

* [Esplora i flussi di lavoro comuni](/it/common-workflows) per ottenere il massimo da Claude Code
* [Configura i server MCP](/it/mcp) per estendere le capacità di Claude con strumenti esterni. Aggiungi i server usando la CLI, quindi gestiscili con `/mcp` nel pannello di chat.
* [Configura le impostazioni di Claude Code](/it/settings) per personalizzare i comandi consentiti, gli hooks e altro. Queste impostazioni sono condivise tra l'estensione e la CLI.
