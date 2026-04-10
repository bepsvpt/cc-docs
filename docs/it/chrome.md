> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Usa Claude Code con Chrome (beta)

> Connetti Claude Code al tuo browser Chrome per testare app web, eseguire il debug con i log della console, automatizzare la compilazione di moduli ed estrarre dati dalle pagine web.

Claude Code si integra con l'estensione Claude in Chrome per darti capacità di automazione del browser dalla CLI o dall'[estensione VS Code](/it/vs-code#automate-browser-tasks-with-chrome). Costruisci il tuo codice, quindi testa ed esegui il debug nel browser senza cambiare contesto.

Claude apre nuove schede per le attività del browser e condivide lo stato di accesso del tuo browser, quindi può accedere a qualsiasi sito in cui sei già connesso. Le azioni del browser vengono eseguite in una finestra Chrome visibile in tempo reale. Quando Claude incontra una pagina di accesso o un CAPTCHA, si ferma e ti chiede di gestirlo manualmente.

<Note>
  L'integrazione con Chrome è in beta e attualmente funziona solo con Google Chrome. Non è ancora supportata su Brave, Arc o altri browser basati su Chromium. Anche WSL (Windows Subsystem for Linux) non è supportato.
</Note>

## Capacità

Con Chrome connesso, puoi concatenare azioni del browser con attività di codifica in un singolo flusso di lavoro:

* **Debug in tempo reale**: leggi gli errori della console e lo stato del DOM direttamente, quindi correggi il codice che li ha causati
* **Verifica del design**: costruisci un'interfaccia utente da un mock di Figma, quindi aprila nel browser per verificare che corrisponda
* **Test di app web**: testa la convalida dei moduli, verifica la presenza di regressioni visive o verifica i flussi utente
* **App web autenticate**: interagisci con Google Docs, Gmail, Notion o qualsiasi app in cui sei connesso senza connettori API
* **Estrazione di dati**: estrai informazioni strutturate dalle pagine web e salvale localmente
* **Automazione delle attività**: automatizza le attività ripetitive del browser come l'immissione di dati, la compilazione di moduli o i flussi di lavoro multi-sito
* **Registrazione della sessione**: registra le interazioni del browser come GIF per documentare o condividere ciò che è accaduto

## Prerequisiti

Prima di utilizzare Claude Code con Chrome, hai bisogno di:

* Browser [Google Chrome](https://www.google.com/chrome/)
* Estensione [Claude in Chrome](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) versione 1.0.36 o superiore
* [Claude Code](/it/quickstart#step-1-install-claude-code) versione 2.0.73 o superiore
* Un piano Anthropic diretto (Pro, Max, Team o Enterprise)

<Note>
  L'integrazione con Chrome non è disponibile tramite provider di terze parti come Amazon Bedrock, Google Cloud Vertex AI o Microsoft Foundry. Se accedi a Claude esclusivamente tramite un provider di terze parti, hai bisogno di un account claude.ai separato per utilizzare questa funzione.
</Note>

## Inizia nella CLI

<Steps>
  <Step title="Avvia Claude Code con Chrome">
    Avvia Claude Code con il flag `--chrome`:

    ```bash  theme={null}
    claude --chrome
    ```

    Puoi anche abilitare Chrome da una sessione esistente eseguendo `/chrome`.
  </Step>

  <Step title="Chiedi a Claude di usare il browser">
    Questo esempio naviga verso una pagina, interagisce con essa e segnala ciò che trova, tutto dal tuo terminale o editor:

    ```text  theme={null}
    Go to code.claude.com/docs, click on the search box,
    type "hooks", and tell me what results appear
    ```
  </Step>
</Steps>

Esegui `/chrome` in qualsiasi momento per verificare lo stato della connessione, gestire le autorizzazioni o riconnettere l'estensione.

Per VS Code, vedi [automazione del browser in VS Code](/it/vs-code#automate-browser-tasks-with-chrome).

### Abilita Chrome per impostazione predefinita

Per evitare di passare `--chrome` ogni sessione, esegui `/chrome` e seleziona "Enabled by default".

Nell'[estensione VS Code](/it/vs-code#automate-browser-tasks-with-chrome), Chrome è disponibile ogni volta che l'estensione Chrome è installata. Non è necessario alcun flag aggiuntivo.

<Note>
  L'abilitazione di Chrome per impostazione predefinita nella CLI aumenta l'utilizzo del contesto poiché gli strumenti del browser vengono sempre caricati. Se noti un aumento del consumo di contesto, disabilita questa impostazione e utilizza `--chrome` solo quando necessario.
</Note>

### Gestisci le autorizzazioni del sito

Le autorizzazioni a livello di sito vengono ereditate dall'estensione Chrome. Gestisci le autorizzazioni nelle impostazioni dell'estensione Chrome per controllare quali siti Claude può navigare, fare clic e digitare.

## Flussi di lavoro di esempio

Questi esempi mostrano i modi comuni per combinare azioni del browser con attività di codifica. Esegui `/mcp` e seleziona `claude-in-chrome` per vedere l'elenco completo degli strumenti del browser disponibili.

### Testa un'applicazione web locale

Quando sviluppi un'app web, chiedi a Claude di verificare che le tue modifiche funzionino correttamente:

```text  theme={null}
I just updated the login form validation. Can you open localhost:3000,
try submitting the form with invalid data, and check if the error
messages appear correctly?
```

Claude naviga verso il tuo server locale, interagisce con il modulo e segnala ciò che osserva.

### Debug con i log della console

Claude può leggere l'output della console per aiutare a diagnosticare i problemi. Dì a Claude quali modelli cercare piuttosto che chiedere tutto l'output della console, poiché i log possono essere dettagliati:

```text  theme={null}
Open the dashboard page and check the console for any errors when
the page loads.
```

Claude legge i messaggi della console e può filtrare per modelli specifici o tipi di errore.

### Automatizza la compilazione dei moduli

Velocizza le attività ripetitive di immissione dati:

```text  theme={null}
I have a spreadsheet of customer contacts in contacts.csv. For each row,
go to the CRM at crm.example.com, click "Add Contact", and fill in the
name, email, and phone fields.
```

Claude legge il tuo file locale, naviga nell'interfaccia web e immette i dati per ogni record.

### Bozza di contenuto in Google Docs

Usa Claude per scrivere direttamente nei tuoi documenti senza configurazione API:

```text  theme={null}
Draft a project update based on the recent commits and add it to my
Google Doc at docs.google.com/document/d/abc123
```

Claude apre il documento, fa clic nell'editor e digita il contenuto. Questo funziona con qualsiasi app web in cui sei connesso: Gmail, Notion, Sheets e altro.

### Estrai dati dalle pagine web

Estrai informazioni strutturate dai siti web:

```text  theme={null}
Go to the product listings page and extract the name, price, and
availability for each item. Save the results as a CSV file.
```

Claude naviga verso la pagina, legge il contenuto e compila i dati in un formato strutturato.

### Esegui flussi di lavoro multi-sito

Coordina le attività su più siti web:

```text  theme={null}
Check my calendar for meetings tomorrow, then for each meeting with
an external attendee, look up their company website and add a note
about what they do.
```

Claude lavora su più schede per raccogliere informazioni e completare il flusso di lavoro.

### Registra una GIF demo

Crea registrazioni condivisibili delle interazioni del browser:

```text  theme={null}
Record a GIF showing how to complete the checkout flow, from adding
an item to the cart through to the confirmation page.
```

Claude registra la sequenza di interazione e la salva come file GIF.

## Troubleshooting

### Estensione non rilevata

Se Claude Code mostra "Chrome extension not detected":

1. Verifica che l'estensione Chrome sia installata e abilitata in `chrome://extensions`
2. Verifica che Claude Code sia aggiornato eseguendo `claude --version`
3. Verifica che Chrome sia in esecuzione
4. Esegui `/chrome` e seleziona "Reconnect extension" per ristabilire la connessione
5. Se il problema persiste, riavvia sia Claude Code che Chrome

La prima volta che abiliti l'integrazione con Chrome, Claude Code installa un file di configurazione dell'host di messaggistica nativa. Chrome legge questo file all'avvio, quindi se l'estensione non viene rilevata al primo tentativo, riavvia Chrome per raccogliere la nuova configurazione.

Se la connessione continua a non funzionare, verifica che il file di configurazione dell'host esista in:

* **macOS**: `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Linux**: `~/.config/google-chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Windows**: controlla `HKCU\Software\Google\Chrome\NativeMessagingHosts\` nel Registro di Windows

### Browser non risponde

Se i comandi del browser di Claude smettono di funzionare:

1. Verifica se una finestra di dialogo modale (avviso, conferma, prompt) sta bloccando la pagina. Le finestre di dialogo JavaScript bloccano gli eventi del browser e impediscono a Claude di ricevere comandi. Chiudi manualmente la finestra di dialogo, quindi dì a Claude di continuare.
2. Chiedi a Claude di creare una nuova scheda e riprovare
3. Riavvia l'estensione Chrome disabilitandola e riabilitandola in `chrome://extensions`

### La connessione si interrompe durante le sessioni lunghe

Il service worker dell'estensione Chrome può diventare inattivo durante le sessioni estese, il che interrompe la connessione. Se gli strumenti del browser smettono di funzionare dopo un periodo di inattività, esegui `/chrome` e seleziona "Reconnect extension".

### Problemi specifici di Windows

Su Windows, potresti riscontrare:

* **Conflitti di named pipe (EADDRINUSE)**: se un altro processo sta utilizzando la stessa named pipe, riavvia Claude Code. Chiudi tutte le altre sessioni di Claude Code che potrebbero utilizzare Chrome.
* **Errori dell'host di messaggistica nativa**: se l'host di messaggistica nativa si arresta in modo anomalo all'avvio, prova a reinstallare Claude Code per rigenerare la configurazione dell'host.

### Messaggi di errore comuni

Questi sono gli errori più frequentemente riscontrati e come risolverli:

| Errore                               | Causa                                                           | Soluzione                                                               |
| ------------------------------------ | --------------------------------------------------------------- | ----------------------------------------------------------------------- |
| "Browser extension is not connected" | L'host di messaggistica nativa non può raggiungere l'estensione | Riavvia Chrome e Claude Code, quindi esegui `/chrome` per riconnetterti |
| "Extension not detected"             | L'estensione Chrome non è installata o è disabilitata           | Installa o abilita l'estensione in `chrome://extensions`                |
| "No tab available"                   | Claude ha tentato di agire prima che una scheda fosse pronta    | Chiedi a Claude di creare una nuova scheda e riprovare                  |
| "Receiving end does not exist"       | Il service worker dell'estensione è diventato inattivo          | Esegui `/chrome` e seleziona "Reconnect extension"                      |

## Vedi anche

* [Usa Claude Code in VS Code](/it/vs-code#automate-browser-tasks-with-chrome): automazione del browser nell'estensione VS Code
* [Riferimento CLI](/it/cli-reference): flag della riga di comando incluso `--chrome`
* [Flussi di lavoro comuni](/it/common-workflows): altri modi per utilizzare Claude Code
* [Dati e privacy](/it/data-usage): come Claude Code gestisce i tuoi dati
* [Introduzione a Claude in Chrome](https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome): documentazione completa per l'estensione Chrome, incluse scorciatoie, pianificazione e autorizzazioni
