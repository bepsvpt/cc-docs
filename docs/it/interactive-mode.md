> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Modalità interattiva

> Riferimento completo per le scorciatoie da tastiera, le modalità di input e le funzioni interattive nelle sessioni di Claude Code.

## Scorciatoie da tastiera

<Note>
  Le scorciatoie da tastiera possono variare a seconda della piattaforma e del terminale. Premere `?` per visualizzare le scorciatoie disponibili per il vostro ambiente.

  **Utenti macOS**: Le scorciatoie con il tasto Option/Alt (`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`) richiedono la configurazione di Option come Meta nel vostro terminale:

  * **iTerm2**: impostazioni → Profili → Tasti → impostare il tasto Option sinistro/destro su "Esc+"
  * **Terminal.app**: impostazioni → Profili → Tastiera → selezionare "Usa Option come Meta Key"
  * **VS Code**: impostazioni → Profili → Tasti → impostare il tasto Option sinistro/destro su "Esc+"

  Vedere [Configurazione del terminale](/it/terminal-config) per i dettagli.
</Note>

### Controlli generali

| Scorciatoia                                     | Descrizione                                                                              | Contesto                                                                                                               |
| :---------------------------------------------- | :--------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+C`                                        | Annulla l'input corrente o la generazione                                                | Interruzione standard                                                                                                  |
| `Ctrl+F`                                        | Termina tutti gli agenti in background. Premere due volte entro 3 secondi per confermare | Controllo agente background                                                                                            |
| `Ctrl+D`                                        | Esci dalla sessione di Claude Code                                                       | Segnale EOF                                                                                                            |
| `Ctrl+G`                                        | Apri nell'editor di testo predefinito                                                    | Modifica il vostro prompt o la risposta personalizzata nell'editor di testo predefinito                                |
| `Ctrl+L`                                        | Cancella lo schermo del terminale                                                        | Mantiene la cronologia della conversazione                                                                             |
| `Ctrl+O`                                        | Attiva/disattiva l'output dettagliato                                                    | Mostra l'utilizzo dettagliato degli strumenti e l'esecuzione                                                           |
| `Ctrl+R`                                        | Ricerca inversa nella cronologia dei comandi                                             | Cerca i comandi precedenti in modo interattivo                                                                         |
| `Ctrl+V` o `Cmd+V` (iTerm2) o `Alt+V` (Windows) | Incolla immagine dagli appunti                                                           | Incolla un'immagine o un percorso a un file immagine                                                                   |
| `Ctrl+B`                                        | Attività in esecuzione in background                                                     | Esegue i comandi bash e gli agenti in background. Gli utenti Tmux premono due volte                                    |
| `Ctrl+T`                                        | Attiva/disattiva l'elenco delle attività                                                 | Mostra o nascondi l'[elenco delle attività](#task-list) nell'area di stato del terminale                               |
| `Frecce sinistra/destra`                        | Scorrere le schede della finestra di dialogo                                             | Navigare tra le schede nelle finestre di dialogo delle autorizzazioni e nei menu                                       |
| `Frecce su/giù`                                 | Navigare nella cronologia dei comandi                                                    | Richiamare gli input precedenti                                                                                        |
| `Esc` + `Esc`                                   | Riavvolgi o riassumi                                                                     | Ripristina il codice e/o la conversazione a un punto precedente, o riassumi da un messaggio selezionato                |
| `Shift+Tab` o `Alt+M` (alcune configurazioni)   | Attiva/disattiva le modalità di autorizzazione                                           | Passa tra la modalità Auto-Accept, Plan Mode e la modalità normale.                                                    |
| `Option+P` (macOS) o `Alt+P` (Windows/Linux)    | Cambia modello                                                                           | Cambia modelli senza cancellare il vostro prompt                                                                       |
| `Option+T` (macOS) o `Alt+T` (Windows/Linux)    | Attiva/disattiva il pensiero esteso                                                      | Abilita o disabilita la modalità di pensiero esteso. Eseguire prima `/terminal-setup` per abilitare questa scorciatoia |

### Modifica del testo

| Scorciatoia             | Descrizione                               | Contesto                                                                                                                         |
| :---------------------- | :---------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+K`                | Elimina fino alla fine della riga         | Memorizza il testo eliminato per l'incollamento                                                                                  |
| `Ctrl+U`                | Elimina l'intera riga                     | Memorizza il testo eliminato per l'incollamento                                                                                  |
| `Ctrl+Y`                | Incolla il testo eliminato                | Incolla il testo eliminato con `Ctrl+K` o `Ctrl+U`                                                                               |
| `Alt+Y` (dopo `Ctrl+Y`) | Scorrere la cronologia degli incollamenti | Dopo l'incollamento, scorrere il testo precedentemente eliminato. Richiede [Option come Meta](#scorciatoie-da-tastiera) su macOS |
| `Alt+B`                 | Sposta il cursore indietro di una parola  | Navigazione per parole. Richiede [Option come Meta](#scorciatoie-da-tastiera) su macOS                                           |
| `Alt+F`                 | Sposta il cursore in avanti di una parola | Navigazione per parole. Richiede [Option come Meta](#scorciatoie-da-tastiera) su macOS                                           |

### Tema e visualizzazione

| Scorciatoia | Descrizione                                                              | Contesto                                                                                                                                         |
| :---------- | :----------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+T`    | Attiva/disattiva l'evidenziazione della sintassi per i blocchi di codice | Funziona solo all'interno del menu di selezione `/theme`. Controlla se il codice nelle risposte di Claude utilizza la colorazione della sintassi |

<Note>
  L'evidenziazione della sintassi è disponibile solo nella build nativa di Claude Code.
</Note>

### Input multilinea

| Metodo                | Scorciatoia          | Contesto                                                   |
| :-------------------- | :------------------- | :--------------------------------------------------------- |
| Escape rapido         | `\` + `Enter`        | Funziona in tutti i terminali                              |
| Predefinito macOS     | `Option+Enter`       | Predefinito su macOS                                       |
| Shift+Enter           | `Shift+Enter`        | Funziona immediatamente in iTerm2, WezTerm, Ghostty, Kitty |
| Sequenza di controllo | `Ctrl+J`             | Carattere di avanzamento riga per multilinea               |
| Modalità incolla      | Incolla direttamente | Per blocchi di codice, log                                 |

<Tip>
  Shift+Enter funziona senza configurazione in iTerm2, WezTerm, Ghostty e Kitty. Per altri terminali (VS Code, Alacritty, Zed, Warp), eseguire `/terminal-setup` per installare il binding.
</Tip>

### Comandi rapidi

| Scorciatoia    | Descrizione                    | Note                                                                          |
| :------------- | :----------------------------- | :---------------------------------------------------------------------------- |
| `/` all'inizio | Comando o skill                | Vedere [comandi integrati](#comandi-integrati) e [skills](/it/skills)         |
| `!` all'inizio | Modalità Bash                  | Esegui i comandi direttamente e aggiungi l'output di esecuzione alla sessione |
| `@`            | Menzione del percorso del file | Attiva l'autocompletamento del percorso del file                              |

## Comandi integrati

Digitare `/` in Claude Code per visualizzare tutti i comandi disponibili, oppure digitare `/` seguito da qualsiasi lettera per filtrare. Non tutti i comandi sono visibili a ogni utente. Alcuni dipendono dalla vostra piattaforma, dal piano o dall'ambiente. Ad esempio, `/desktop` appare solo su macOS e Windows, `/upgrade` e `/privacy-settings` sono disponibili solo per i piani Pro e Max, e `/terminal-setup` è nascosto quando il vostro terminale supporta nativamente i suoi keybindings.

Claude Code viene anche fornito con [skills in bundle](/it/skills#bundled-skills) come `/simplify`, `/batch` e `/debug` che appaiono insieme ai comandi integrati quando digitate `/`. Per creare i vostri comandi, vedere [skills](/it/skills).

Nella tabella sottostante, `<arg>` indica un argomento obbligatorio e `[arg]` indica uno facoltativo.

| Comando                   | Scopo                                                                                                                                                                                                                                                                  |
| :------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/add-dir <path>`         | Aggiungi una nuova directory di lavoro alla sessione corrente                                                                                                                                                                                                          |
| `/agents`                 | Gestisci le configurazioni [agent](/it/sub-agents)                                                                                                                                                                                                                     |
| `/btw <question>`         | Fai una rapida [domanda laterale](#domande-laterali-con-%2Fbtw) senza aggiungere alla conversazione                                                                                                                                                                    |
| `/chrome`                 | Configura le impostazioni di [Claude in Chrome](/it/chrome)                                                                                                                                                                                                            |
| `/clear`                  | Cancella la cronologia della conversazione e libera il contesto. Alias: `/reset`, `/new`                                                                                                                                                                               |
| `/compact [instructions]` | Compatta la conversazione con istruzioni di focus facoltative                                                                                                                                                                                                          |
| `/config`                 | Apri l'interfaccia [Impostazioni](/it/settings) per regolare il tema, il modello, lo [stile di output](/it/output-styles) e altre preferenze. Alias: `/settings`                                                                                                       |
| `/context`                | Visualizza l'utilizzo del contesto corrente come una griglia colorata                                                                                                                                                                                                  |
| `/copy`                   | Copia l'ultima risposta dell'assistente negli appunti. Quando sono presenti blocchi di codice, mostra un selettore interattivo per selezionare singoli blocchi o la risposta completa                                                                                  |
| `/cost`                   | Mostra le statistiche di utilizzo dei token. Vedere la [guida al tracciamento dei costi](/it/costs#using-the-cost-command) per i dettagli specifici dell'abbonamento                                                                                                   |
| `/desktop`                | Continua la sessione corrente nell'app Claude Code Desktop. Solo macOS e Windows. Alias: `/app`                                                                                                                                                                        |
| `/diff`                   | Apri un visualizzatore diff interattivo che mostra le modifiche non sottoposte a commit e i diff per turno. Usa le frecce sinistra/destra per passare tra il diff git corrente e i singoli turni di Claude, e su/giù per sfogliare i file                              |
| `/doctor`                 | Diagnostica e verifica l'installazione e le impostazioni di Claude Code                                                                                                                                                                                                |
| `/exit`                   | Esci dalla CLI. Alias: `/quit`                                                                                                                                                                                                                                         |
| `/export [filename]`      | Esporta la conversazione corrente come testo semplice. Con un nome file, scrive direttamente in quel file. Senza, apre una finestra di dialogo per copiare negli appunti o salvare in un file                                                                          |
| `/extra-usage`            | Configura l'utilizzo extra per continuare a lavorare quando vengono raggiunti i limiti di velocità                                                                                                                                                                     |
| `/fast [on\|off]`         | Attiva/disattiva la [modalità veloce](/it/fast-mode)                                                                                                                                                                                                                   |
| `/feedback [report]`      | Invia feedback su Claude Code. Alias: `/bug`                                                                                                                                                                                                                           |
| `/fork [name]`            | Crea un fork della conversazione corrente a questo punto                                                                                                                                                                                                               |
| `/help`                   | Mostra la guida e i comandi disponibili                                                                                                                                                                                                                                |
| `/hooks`                  | Gestisci le configurazioni [hook](/it/hooks) per gli eventi degli strumenti                                                                                                                                                                                            |
| `/ide`                    | Gestisci le integrazioni IDE e mostra lo stato                                                                                                                                                                                                                         |
| `/init`                   | Inizializza il progetto con la guida `CLAUDE.md`                                                                                                                                                                                                                       |
| `/insights`               | Genera un rapporto che analizza le vostre sessioni di Claude Code, incluse le aree del progetto, i modelli di interazione e i punti di attrito                                                                                                                         |
| `/install-github-app`     | Configura l'app [Claude GitHub Actions](/it/github-actions) per un repository. Vi guida nella selezione di un repo e nella configurazione dell'integrazione                                                                                                            |
| `/install-slack-app`      | Installa l'app Claude Slack. Apre un browser per completare il flusso OAuth                                                                                                                                                                                            |
| `/keybindings`            | Apri o crea il vostro file di configurazione delle scorciatoie da tastiera                                                                                                                                                                                             |
| `/login`                  | Accedi al vostro account Anthropic                                                                                                                                                                                                                                     |
| `/logout`                 | Esci dal vostro account Anthropic                                                                                                                                                                                                                                      |
| `/mcp`                    | Gestisci le connessioni ai server MCP e l'autenticazione OAuth                                                                                                                                                                                                         |
| `/memory`                 | Modifica i file di memoria `CLAUDE.md`, abilita o disabilita la [memoria automatica](/it/memory#auto-memory) e visualizza le voci di memoria automatica                                                                                                                |
| `/mobile`                 | Mostra il codice QR per scaricare l'app mobile Claude. Alias: `/ios`, `/android`                                                                                                                                                                                       |
| `/model [model]`          | Seleziona o cambia il modello di IA. Per i modelli che lo supportano, usa le frecce sinistra/destra per [regolare il livello di sforzo](/it/model-config#adjust-effort-level). Il cambio ha effetto immediato senza aspettare il completamento della risposta corrente |
| `/passes`                 | Condividi una settimana gratuita di Claude Code con gli amici. Visibile solo se il vostro account è idoneo                                                                                                                                                             |
| `/permissions`            | Visualizza o aggiorna le [autorizzazioni](/it/permissions#manage-permissions). Alias: `/allowed-tools`                                                                                                                                                                 |
| `/plan`                   | Entra direttamente in plan mode dal prompt                                                                                                                                                                                                                             |
| `/plugin`                 | Gestisci i [plugins](/it/plugins) di Claude Code                                                                                                                                                                                                                       |
| `/pr-comments [PR]`       | Recupera e visualizza i commenti da una pull request di GitHub. Rileva automaticamente il PR per il ramo corrente, oppure passa un URL o un numero di PR. Richiede la CLI `gh`                                                                                         |
| `/privacy-settings`       | Visualizza e aggiorna le vostre impostazioni di privacy. Disponibile solo per gli abbonati ai piani Pro e Max                                                                                                                                                          |
| `/release-notes`          | Visualizza il changelog completo, con la versione più recente più vicina al vostro prompt                                                                                                                                                                              |
| `/reload-plugins`         | Ricarica tutti i [plugins](/it/plugins) attivi per applicare le modifiche in sospeso senza riavviare. Segnala cosa è stato caricato e nota le modifiche che richiedono un riavvio                                                                                      |
| `/remote-control`         | Rendi questa sessione disponibile per il [controllo remoto](/it/remote-control) da claude.ai. Alias: `/rc`                                                                                                                                                             |
| `/remote-env`             | Configura l'ambiente remoto predefinito per le [sessioni teleport](/it/claude-code-on-the-web#teleport-a-web-session-to-your-terminal)                                                                                                                                 |
| `/rename [name]`          | Rinomina la sessione corrente. Senza un nome, ne genera uno automaticamente dalla cronologia della conversazione                                                                                                                                                       |
| `/resume [session]`       | Riprendi una conversazione per ID o nome, oppure apri il selettore di sessione. Alias: `/continue`                                                                                                                                                                     |
| `/review`                 | Deprecato. Installa invece il [`code-review` plugin](https://github.com/anthropics/claude-code-marketplace/blob/main/code-review/README.md): `claude plugin install code-review@claude-code-marketplace`                                                               |
| `/rewind`                 | Riavvolgi la conversazione e/o il codice a un punto precedente, o riassumi da un messaggio selezionato. Vedere [checkpointing](/it/checkpointing). Alias: `/checkpoint`                                                                                                |
| `/sandbox`                | Attiva/disattiva la [modalità sandbox](/it/sandboxing). Disponibile solo su piattaforme supportate                                                                                                                                                                     |
| `/security-review`        | Analizza le modifiche in sospeso sul ramo corrente per le vulnerabilità di sicurezza. Esamina il diff git e identifica i rischi come iniezione, problemi di autenticazione e esposizione dei dati                                                                      |
| `/skills`                 | Elenca le [skills](/it/skills) disponibili                                                                                                                                                                                                                             |
| `/stats`                  | Visualizza l'utilizzo giornaliero, la cronologia delle sessioni, le serie e le preferenze dei modelli                                                                                                                                                                  |
| `/status`                 | Apri l'interfaccia Impostazioni (scheda Stato) che mostra la versione, il modello, l'account e la connettività                                                                                                                                                         |
| `/statusline`             | Configura la [status line](/it/statusline) di Claude Code. Descrivi cosa desideri, oppure esegui senza argomenti per auto-configurare dal vostro prompt della shell                                                                                                    |
| `/stickers`               | Ordina gli adesivi di Claude Code                                                                                                                                                                                                                                      |
| `/tasks`                  | Elenca e gestisci le attività in background                                                                                                                                                                                                                            |
| `/terminal-setup`         | Configura i keybindings del terminale per Shift+Enter e altre scorciatoie. Visibile solo nei terminali che ne hanno bisogno, come VS Code, Alacritty o Warp                                                                                                            |
| `/theme`                  | Cambia il tema del colore. Include varianti chiare e scure, temi accessibili ai daltonici (daltonizzati) e temi ANSI che utilizzano la tavolozza dei colori del vostro terminale                                                                                       |
| `/upgrade`                | Apri la pagina di upgrade per passare a un livello di piano superiore                                                                                                                                                                                                  |
| `/usage`                  | Mostra i limiti di utilizzo del piano e lo stato del limite di velocità                                                                                                                                                                                                |
| `/vim`                    | Attiva/disattiva tra le modalità di modifica Vim e Normale                                                                                                                                                                                                             |

### Prompt MCP

I server MCP possono esporre prompt che appaiono come comandi. Questi utilizzano il formato `/mcp__<server>__<prompt>` e vengono scoperti dinamicamente dai server connessi. Vedere [Prompt MCP](/it/mcp#use-mcp-prompts-as-commands) per i dettagli.

## Modalità editor Vim

Abilita la modifica in stile Vim con il comando `/vim` o configura permanentemente tramite `/config`.

### Cambio di modalità

| Comando | Azione                          | Dalla modalità |
| :------ | :------------------------------ | :------------- |
| `Esc`   | Entra in modalità NORMAL        | INSERT         |
| `i`     | Inserisci prima del cursore     | NORMAL         |
| `I`     | Inserisci all'inizio della riga | NORMAL         |
| `a`     | Inserisci dopo il cursore       | NORMAL         |
| `A`     | Inserisci alla fine della riga  | NORMAL         |
| `o`     | Apri riga sotto                 | NORMAL         |
| `O`     | Apri riga sopra                 | NORMAL         |

### Navigazione (modalità NORMAL)

| Comando         | Azione                                                     |
| :-------------- | :--------------------------------------------------------- |
| `h`/`j`/`k`/`l` | Sposta sinistra/giù/su/destra                              |
| `w`             | Parola successiva                                          |
| `e`             | Fine della parola                                          |
| `b`             | Parola precedente                                          |
| `0`             | Inizio della riga                                          |
| `$`             | Fine della riga                                            |
| `^`             | Primo carattere non vuoto                                  |
| `gg`            | Inizio dell'input                                          |
| `G`             | Fine dell'input                                            |
| `f{char}`       | Salta alla prossima occorrenza del carattere               |
| `F{char}`       | Salta alla precedente occorrenza del carattere             |
| `t{char}`       | Salta appena prima della prossima occorrenza del carattere |
| `T{char}`       | Salta appena dopo la precedente occorrenza del carattere   |
| `;`             | Ripeti l'ultimo movimento f/F/t/T                          |
| `,`             | Ripeti l'ultimo movimento f/F/t/T in ordine inverso        |

<Note>
  In modalità normale vim, se il cursore è all'inizio o alla fine dell'input e non può muoversi ulteriormente, i tasti freccia navigano nella cronologia dei comandi.
</Note>

### Modifica (modalità NORMAL)

| Comando        | Azione                                 |
| :------------- | :------------------------------------- |
| `x`            | Elimina carattere                      |
| `dd`           | Elimina riga                           |
| `D`            | Elimina fino alla fine della riga      |
| `dw`/`de`/`db` | Elimina parola/fino alla fine/indietro |
| `cc`           | Cambia riga                            |
| `C`            | Cambia fino alla fine della riga       |
| `cw`/`ce`/`cb` | Cambia parola/fino alla fine/indietro  |
| `yy`/`Y`       | Copia (yank) riga                      |
| `yw`/`ye`/`yb` | Copia parola/fino alla fine/indietro   |
| `p`            | Incolla dopo il cursore                |
| `P`            | Incolla prima del cursore              |
| `>>`           | Indenta riga                           |
| `<<`           | Dedenta riga                           |
| `J`            | Unisci righe                           |
| `.`            | Ripeti l'ultima modifica               |

### Oggetti di testo (modalità NORMAL)

Gli oggetti di testo funzionano con operatori come `d`, `c` e `y`:

| Comando   | Azione                                               |
| :-------- | :--------------------------------------------------- |
| `iw`/`aw` | Parola interna/intorno                               |
| `iW`/`aW` | PAROLA interna/intorno (delimitata da spazi bianchi) |
| `i"`/`a"` | Interno/intorno a virgolette doppie                  |
| `i'`/`a'` | Interno/intorno a virgolette singole                 |
| `i(`/`a(` | Interno/intorno a parentesi                          |
| `i[`/`a[` | Interno/intorno a parentesi quadre                   |
| `i{`/`a{` | Interno/intorno a parentesi graffe                   |

## Cronologia dei comandi

Claude Code mantiene la cronologia dei comandi per la sessione corrente:

* La cronologia degli input viene memorizzata per directory di lavoro
* La cronologia degli input si ripristina quando eseguite `/clear` per avviare una nuova sessione. La conversazione della sessione precedente viene preservata e può essere ripresa.
* Usate le frecce Su/Giù per navigare (vedere le scorciatoie da tastiera sopra)
* **Nota**: l'espansione della cronologia (`!`) è disabilitata per impostazione predefinita

### Ricerca inversa con Ctrl+R

Premere `Ctrl+R` per cercare in modo interattivo nella vostra cronologia dei comandi:

1. **Avvia la ricerca**: premere `Ctrl+R` per attivare la ricerca inversa nella cronologia
2. **Digita la query**: inserire il testo da cercare nei comandi precedenti. Il termine di ricerca è evidenziato nei risultati corrispondenti
3. **Navigare i risultati**: premere `Ctrl+R` di nuovo per scorrere i risultati più vecchi
4. **Accetta il risultato**:
   * Premere `Tab` o `Esc` per accettare il risultato corrente e continuare a modificare
   * Premere `Enter` per accettare ed eseguire il comando immediatamente
5. **Annulla la ricerca**:
   * Premere `Ctrl+C` per annullare e ripristinare l'input originale
   * Premere `Backspace` su una ricerca vuota per annullare

La ricerca visualizza i comandi corrispondenti con il termine di ricerca evidenziato, in modo da poter trovare e riutilizzare gli input precedenti.

## Comandi bash in background

Claude Code supporta l'esecuzione di comandi bash in background, consentendovi di continuare a lavorare mentre i processi a lunga esecuzione vengono eseguiti.

### Come funziona l'esecuzione in background

Quando Claude Code esegue un comando in background, esegue il comando in modo asincrono e restituisce immediatamente un ID di attività in background. Claude Code può rispondere a nuovi prompt mentre il comando continua a essere eseguito in background.

Per eseguire i comandi in background, potete:

* Chiedere a Claude Code di eseguire un comando in background
* Premere Ctrl+B per spostare una normale invocazione dello strumento Bash in background. (Gli utenti Tmux devono premere Ctrl+B due volte a causa del tasto di prefisso di tmux.)

**Caratteristiche principali:**

* L'output viene memorizzato nel buffer e Claude può recuperarlo utilizzando lo strumento TaskOutput
* Le attività in background hanno ID univoci per il tracciamento e il recupero dell'output
* Le attività in background vengono pulite automaticamente quando Claude Code esce

Per disabilitare tutta la funzionalità di attività in background, impostare la variabile di ambiente `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` su `1`. Vedere [Variabili di ambiente](/it/settings#environment-variables) per i dettagli.

**Comandi comunemente eseguiti in background:**

* Strumenti di build (webpack, vite, make)
* Gestori di pacchetti (npm, yarn, pnpm)
* Test runner (jest, pytest)
* Server di sviluppo
* Processi a lunga esecuzione (docker, terraform)

### Modalità Bash con prefisso `!`

Esegui i comandi bash direttamente senza passare per Claude aggiungendo il prefisso `!` al vostro input:

```bash  theme={null}
! npm test
! git status
! ls -la
```

Modalità Bash:

* Aggiunge il comando e il suo output al contesto della conversazione
* Mostra il progresso e l'output in tempo reale
* Supporta lo stesso backgrounding `Ctrl+B` per i comandi a lunga esecuzione
* Non richiede a Claude di interpretare o approvare il comando
* Supporta l'autocompletamento basato sulla cronologia: digitate un comando parziale e premete **Tab** per completare dai comandi `!` precedenti nel progetto corrente
* Esci con `Escape`, `Backspace` o `Ctrl+U` su un prompt vuoto

Questo è utile per le operazioni shell rapide mantenendo il contesto della conversazione.

## Suggerimenti di prompt

Quando aprite una sessione per la prima volta, un comando di esempio in grigio appare nell'input del prompt per aiutarvi a iniziare. Claude Code lo sceglie dalla cronologia git del vostro progetto, quindi riflette i file su cui avete lavorato di recente.

Dopo che Claude risponde, i suggerimenti continuano ad apparire in base alla vostra cronologia della conversazione, come un passaggio di follow-up da una richiesta in più parti o una continuazione naturale del vostro flusso di lavoro.

* Premete **Tab** per accettare il suggerimento, oppure premete **Enter** per accettare e inviare
* Iniziate a digitare per dismissarlo

Il suggerimento viene eseguito come una richiesta in background che riutilizza la cache del prompt della conversazione padre, quindi il costo aggiuntivo è minimo. Claude Code salta la generazione di suggerimenti quando la cache è fredda per evitare costi inutili.

I suggerimenti vengono automaticamente saltati dopo il primo turno di una conversazione, in modalità non interattiva e in plan mode.

Per disabilitare completamente i suggerimenti di prompt, impostare la variabile di ambiente o attivare l'impostazione in `/config`:

```bash  theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## Domande laterali con /btw

Usate `/btw` per fare una domanda rapida sul vostro lavoro corrente senza aggiungere alla cronologia della conversazione. Questo è utile quando desiderate una risposta veloce ma non volete ingombrare il contesto principale o far deviare Claude da un'attività a lunga esecuzione.

```
/btw what was the name of that config file again?
```

Le domande laterali hanno piena visibilità nella conversazione corrente, quindi potete chiedere informazioni sul codice che Claude ha già letto, sulle decisioni che ha preso in precedenza, o su qualsiasi altra cosa della sessione. La domanda e la risposta sono effimere: appaiono in un overlay dismissibile e non entrano mai nella cronologia della conversazione.

* **Disponibile mentre Claude sta lavorando**: potete eseguire `/btw` anche mentre Claude sta elaborando una risposta. La domanda laterale viene eseguita in modo indipendente e non interrompe il turno principale.
* **Nessun accesso agli strumenti**: le domande laterali rispondono solo da ciò che è già nel contesto. Claude non può leggere file, eseguire comandi o cercare quando risponde a una domanda laterale.
* **Risposta singola**: non ci sono turni di follow-up. Se avete bisogno di un dialogo, usate un prompt normale.
* **Costo basso**: la domanda laterale riutilizza la cache del prompt della conversazione padre, quindi il costo aggiuntivo è minimo.

Premete **Spazio**, **Enter** o **Escape** per dismissere la risposta e tornare al prompt.

`/btw` è l'inverso di un [subagent](/it/sub-agents): vede la vostra conversazione completa ma non ha strumenti, mentre un subagent ha strumenti completi ma inizia con un contesto vuoto. Usate `/btw` per chiedere informazioni su ciò che Claude già conosce da questa sessione; usate un subagent per scoprire qualcosa di nuovo.

## Elenco delle attività

Quando si lavora su lavori complessi e multistep, Claude crea un elenco di attività per tracciare i progressi. Le attività appaiono nell'area di stato del vostro terminale con indicatori che mostrano cosa è in sospeso, in corso o completato.

* Premete `Ctrl+T` per attivare/disattivare la visualizzazione dell'elenco delle attività. La visualizzazione mostra fino a 10 attività alla volta
* Per visualizzare tutte le attività o cancellarle, chiedete direttamente a Claude: "mostrami tutte le attività" o "cancella tutte le attività"
* Le attività persistono attraverso le compattazioni del contesto, aiutando Claude a rimanere organizzato su progetti più grandi
* Per condividere un elenco di attività tra sessioni, impostare `CLAUDE_CODE_TASK_LIST_ID` per utilizzare una directory denominata in `~/.claude/tasks/`: `CLAUDE_CODE_TASK_LIST_ID=my-project claude`
* Per ripristinare l'elenco TODO precedente, impostare `CLAUDE_CODE_ENABLE_TASKS=false`.

## Stato della revisione PR

Quando si lavora su un ramo con una pull request aperta, Claude Code visualizza un collegamento PR cliccabile nel footer (ad esempio, "PR #446"). Il collegamento ha un sottolineatura colorata che indica lo stato della revisione:

* Verde: approvato
* Giallo: revisione in sospeso
* Rosso: modifiche richieste
* Grigio: bozza
* Viola: unito

`Cmd+click` (Mac) o `Ctrl+click` (Windows/Linux) sul collegamento per aprire la pull request nel vostro browser. Lo stato si aggiorna automaticamente ogni 60 secondi.

<Note>
  Lo stato PR richiede che la CLI `gh` sia installata e autenticata (`gh auth login`).
</Note>

## Vedere anche

* [Skills](/it/skills) - Prompt e flussi di lavoro personalizzati
* [Checkpointing](/it/checkpointing) - Riavvolgi le modifiche di Claude e ripristina gli stati precedenti
* [Riferimento CLI](/it/cli-reference) - Flag e opzioni della riga di comando
* [Impostazioni](/it/settings) - Opzioni di configurazione
* [Gestione della memoria](/it/memory) - Gestione dei file CLAUDE.md
