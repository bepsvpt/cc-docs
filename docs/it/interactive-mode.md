> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Modalità interattiva

> Riferimento completo per le scorciatoie da tastiera, le modalità di input e le funzioni interattive nelle sessioni di Claude Code.

## Scorciatoie da tastiera

<Note>
  Le scorciatoie da tastiera possono variare a seconda della piattaforma e del terminale. Premere `?` per visualizzare le scorciatoie disponibili per il vostro ambiente.

  **Utenti macOS**: Le scorciatoie con il tasto Option/Alt (`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`) richiedono la configurazione di Option come Meta nel vostro terminale:

  * **iTerm2**: Impostazioni → Profili → Tasti → Generale → impostare il tasto Option sinistro/destro su "Esc+"
  * **Apple Terminal**: Impostazioni → Profili → Tastiera → selezionare "Usa Option come Meta Key"
  * **VS Code**: impostare `"terminal.integrated.macOptionIsMeta": true` nelle impostazioni di VS Code

  Vedere [Configurazione del terminale](/it/terminal-config) per i dettagli.
</Note>

### Controlli generali

| Scorciatoia                                     | Descrizione                                                                              | Contesto                                                                                                                                                                                                                                                                                                                                                              |
| :---------------------------------------------- | :--------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+C`                                        | Annulla l'input corrente o la generazione                                                | Interruzione standard                                                                                                                                                                                                                                                                                                                                                 |
| `Ctrl+X Ctrl+K`                                 | Termina tutti gli agenti in background. Premere due volte entro 3 secondi per confermare | Controllo agente in background                                                                                                                                                                                                                                                                                                                                        |
| `Ctrl+D`                                        | Esci dalla sessione di Claude Code                                                       | Segnale EOF                                                                                                                                                                                                                                                                                                                                                           |
| `Ctrl+G` o `Ctrl+X Ctrl+E`                      | Apri nell'editor di testo predefinito                                                    | Modifica il vostro prompt o la risposta personalizzata nell'editor di testo predefinito. `Ctrl+X Ctrl+E` è il binding nativo di readline. Attivare Mostra ultima risposta nell'editor esterno in `/config` per anteporre la risposta precedente di Claude come contesto commentato con `#` sopra il vostro prompt; il blocco di commento viene rimosso quando salvate |
| `Ctrl+L`                                        | Ridisegna lo schermo                                                                     | Forza un ridisegno completo del terminale. L'input e la cronologia della conversazione vengono mantenuti. Utilizzate questo per recuperare se la visualizzazione diventa distorta o parzialmente vuota                                                                                                                                                                |
| `Ctrl+O`                                        | Attiva/disattiva il visualizzatore di trascrizione                                       | Mostra l'utilizzo e l'esecuzione dettagliati degli strumenti. Inoltre espande le chiamate MCP, che si compattano in una singola riga come "Called slack 3 times" per impostazione predefinita                                                                                                                                                                         |
| `Ctrl+R`                                        | Ricerca inversa nella cronologia dei comandi                                             | Cerca i comandi precedenti in modo interattivo                                                                                                                                                                                                                                                                                                                        |
| `Ctrl+V` o `Cmd+V` (iTerm2) o `Alt+V` (Windows) | Incolla immagine dagli appunti                                                           | Inserisce un chip `[Image #N]` al cursore in modo da poter farvi riferimento posizionalmente nel vostro prompt                                                                                                                                                                                                                                                        |
| `Ctrl+B`                                        | Attività in esecuzione in background                                                     | Esegue i comandi bash e gli agenti in background. Gli utenti Tmux premono due volte                                                                                                                                                                                                                                                                                   |
| `Ctrl+T`                                        | Attiva/disattiva l'elenco delle attività                                                 | Mostra o nascondi l'[elenco delle attività](#task-list) nell'area di stato del terminale                                                                                                                                                                                                                                                                              |
| `Frecce sinistra/destra`                        | Cicla attraverso le schede della finestra di dialogo                                     | Naviga tra le schede nelle finestre di dialogo dei permessi e nei menu                                                                                                                                                                                                                                                                                                |
| `Frecce su/giù` o `Ctrl+P`/`Ctrl+N`             | Sposta il cursore o naviga nella cronologia dei comandi                                  | Nell'input multilinea, prima sposta il cursore all'interno del prompt. Una volta che il cursore è già sul bordo superiore o inferiore, premere di nuovo naviga nella cronologia dei comandi                                                                                                                                                                           |
| `Esc` + `Esc`                                   | Riavvolgi o riassumi                                                                     | Ripristina il codice e/o la conversazione a un punto precedente, o riassumi da un messaggio selezionato                                                                                                                                                                                                                                                               |
| `Shift+Tab` o `Alt+M` (alcune configurazioni)   | Cicla le modalità di permesso                                                            | Cicla attraverso `default`, `acceptEdits`, `plan` e qualsiasi modalità abilitata, come `auto` o `bypassPermissions`. Vedere [modalità di permesso](/it/permission-modes).                                                                                                                                                                                             |
| `Option+P` (macOS) o `Alt+P` (Windows/Linux)    | Cambia modello                                                                           | Cambia modelli senza cancellare il vostro prompt                                                                                                                                                                                                                                                                                                                      |
| `Option+T` (macOS) o `Alt+T` (Windows/Linux)    | Attiva/disattiva il pensiero esteso                                                      | Abilita o disabilita la modalità di pensiero esteso. A partire dalla v2.1.132 questa scorciatoia funziona su macOS senza configurare Option come Meta                                                                                                                                                                                                                 |
| `Option+O` (macOS) o `Alt+O` (Windows/Linux)    | Attiva/disattiva la modalità veloce                                                      | Abilita o disabilita la [modalità veloce](/it/fast-mode)                                                                                                                                                                                                                                                                                                              |

### Modifica del testo

| Scorciatoia             | Descrizione                                      | Contesto                                                                                                                                                                                                                     |
| :---------------------- | :----------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+A`                | Sposta il cursore all'inizio della riga corrente | Nell'input multilinea, sposta all'inizio della riga logica corrente                                                                                                                                                          |
| `Ctrl+E`                | Sposta il cursore alla fine della riga corrente  | Nell'input multilinea, sposta alla fine della riga logica corrente                                                                                                                                                           |
| `Ctrl+K`                | Elimina fino alla fine della riga                | Memorizza il testo eliminato per l'incollamento                                                                                                                                                                              |
| `Ctrl+U`                | Elimina dal cursore all'inizio della riga        | Memorizza il testo eliminato per l'incollamento. Ripetere per cancellare su più righe nell'input multilinea. Su macOS, gli emulatori di terminale inclusi iTerm2 e Terminal.app mappano `Cmd+Backspace` a questa scorciatoia |
| `Ctrl+W`                | Elimina la parola precedente                     | Memorizza il testo eliminato per l'incollamento. Su Windows, `Ctrl+Backspace` elimina anche la parola precedente                                                                                                             |
| `Ctrl+Y`                | Incolla il testo eliminato                       | Incolla il testo eliminato con `Ctrl+K`, `Ctrl+U` o `Ctrl+W`                                                                                                                                                                 |
| `Alt+Y` (dopo `Ctrl+Y`) | Cicla la cronologia degli incollamenti           | Dopo l'incollamento, cicla attraverso il testo precedentemente eliminato. Richiede [Option come Meta](#keyboard-shortcuts) su macOS                                                                                          |
| `Alt+B`                 | Sposta il cursore indietro di una parola         | Navigazione per parole. Richiede [Option come Meta](#keyboard-shortcuts) su macOS                                                                                                                                            |
| `Alt+F`                 | Sposta il cursore in avanti di una parola        | Navigazione per parole. Richiede [Option come Meta](#keyboard-shortcuts) su macOS                                                                                                                                            |

### Tema e visualizzazione

| Scorciatoia | Descrizione                                                              | Contesto                                                                                                                                         |
| :---------- | :----------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+T`    | Attiva/disattiva l'evidenziazione della sintassi per i blocchi di codice | Funziona solo all'interno del menu di selezione `/theme`. Controlla se il codice nelle risposte di Claude utilizza la colorazione della sintassi |

### Input multilinea

| Metodo                | Scorciatoia          | Contesto                                                                                                  |
| :-------------------- | :------------------- | :-------------------------------------------------------------------------------------------------------- |
| Escape rapido         | `\` + `Enter`        | Funziona in tutti i terminali                                                                             |
| Tasto Option          | `Option+Enter`       | Dopo aver abilitato [Option come Meta](/it/terminal-config#enable-option-key-shortcuts-on-macos) su macOS |
| Shift+Enter           | `Shift+Enter`        | Nativo in iTerm2, WezTerm, Ghostty, Kitty, Warp, Apple Terminal, Windows Terminal                         |
| Sequenza di controllo | `Ctrl+J`             | Funziona in qualsiasi terminale senza configurazione                                                      |
| Modalità incolla      | Incolla direttamente | Per blocchi di codice, log                                                                                |

<Tip>
  Shift+Enter funziona senza configurazione in iTerm2, WezTerm, Ghostty, Kitty, Warp, Apple Terminal e Windows Terminal. Per VS Code, Cursor, Windsurf, Alacritty e Zed, eseguire `/terminal-setup` per installare il binding.
</Tip>

### Comandi rapidi

| Scorciatoia    | Descrizione                    | Note                                                                          |
| :------------- | :----------------------------- | :---------------------------------------------------------------------------- |
| `/` all'inizio | Comando o skill                | Vedere [comandi](#commands) e [skills](/it/skills)                            |
| `!` all'inizio | Modalità Bash                  | Esegui i comandi direttamente e aggiungi l'output di esecuzione alla sessione |
| `@`            | Menzione del percorso del file | Attiva l'autocompletamento del percorso del file                              |

### Visualizzatore di trascrizione

Quando il visualizzatore di trascrizione è aperto (attivato con `Ctrl+O`), queste scorciatoie sono disponibili. `Ctrl+E` può essere riassegnato tramite [`transcript:toggleShowAll`](/it/keybindings).

| Scorciatoia          | Descrizione                                                                                                                                                                                                                                                       |
| :------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+E`             | Attiva/disattiva mostra tutto il contenuto                                                                                                                                                                                                                        |
| `[`                  | Scrivi la conversazione completa nel scrollback nativo del vostro terminale in modo che `Cmd+F`, la modalità copia di tmux e altri strumenti nativi possano cercarla. Richiede il [rendering a schermo intero](/it/fullscreen#search-and-review-the-conversation) |
| `v`                  | Scrivi la conversazione in un file temporaneo e aprilo in `$VISUAL` o `$EDITOR`. Richiede il [rendering a schermo intero](/it/fullscreen)                                                                                                                         |
| `q`, `Ctrl+C`, `Esc` | Esci dalla visualizzazione della trascrizione. Tutti e tre possono essere riassegnati tramite [`transcript:exit`](/it/keybindings)                                                                                                                                |

### Input vocale

| Scorciatoia                   | Descrizione      | Note                                                                                                                                                                                                                        |
| :---------------------------- | :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Tieni premuto o tocca `Space` | Dettatura vocale | Richiede che la [dettatura vocale](/it/voice-dictation) sia abilitata. Tieni premuto per registrare, o esegui `/voice tap` per attivare/disattivare al tocco. [Riassegnabile](/it/voice-dictation#rebind-the-dictation-key) |

## Comandi

Digitate `/` in Claude Code per visualizzare tutti i comandi disponibili, oppure digitate `/` seguito da qualsiasi lettera per filtrare. Il menu `/` mostra tutto ciò che potete invocare: comandi integrati, [skills](/it/skills) in bundle e create dagli utenti, e comandi forniti da [plugin](/it/plugins) e [server MCP](/it/mcp#use-mcp-prompts-as-commands). Non tutti i comandi integrati sono visibili a ogni utente poiché alcuni dipendono dalla vostra piattaforma o dal vostro piano.

Vedere il [riferimento dei comandi](/it/commands) per l'elenco completo dei comandi inclusi in Claude Code.

## Modalità editor Vim

Abilitate la modifica in stile vim tramite `/config` → Editor mode.

### Cambio di modalità

| Comando | Azione                                          | Dalla modalità |
| :------ | :---------------------------------------------- | :------------- |
| `Esc`   | Entra in modalità NORMAL                        | INSERT, VISUAL |
| `i`     | Inserisci prima del cursore                     | NORMAL         |
| `I`     | Inserisci all'inizio della riga                 | NORMAL         |
| `a`     | Inserisci dopo il cursore                       | NORMAL         |
| `A`     | Inserisci alla fine della riga                  | NORMAL         |
| `o`     | Apri riga sotto                                 | NORMAL         |
| `O`     | Apri riga sopra                                 | NORMAL         |
| `v`     | Avvia selezione visuale carattere per carattere | NORMAL         |
| `V`     | Avvia selezione visuale riga per riga           | NORMAL         |

### Navigazione (modalità NORMAL)

| Comando         | Azione                                                     |
| :-------------- | :--------------------------------------------------------- |
| `h`/`j`/`k`/`l` | Sposta sinistra/giù/su/destra                              |
| `Space`         | Sposta a destra                                            |
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
  In modalità normale vim, se il cursore è all'inizio o alla fine dell'input e non può muoversi ulteriormente, `j`/`k` e i tasti freccia navigano nella cronologia dei comandi.
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
| `u`            | Annulla                                |
| `.`            | Ripeti l'ultimo cambiamento            |

### Oggetti di testo (modalità NORMAL)

Gli oggetti di testo funzionano con operatori come `d`, `c` e `y`:

| Comando   | Azione                                       |
| :-------- | :------------------------------------------- |
| `iw`/`aw` | Parola interna/intorno                       |
| `iW`/`aW` | PAROLA interna/intorno (delimitata da spazi) |
| `i"`/`a"` | Interno/intorno a virgolette doppie          |
| `i'`/`a'` | Interno/intorno a virgolette singole         |
| `i(`/`a(` | Interno/intorno a parentesi tonde            |
| `i[`/`a[` | Interno/intorno a parentesi quadre           |
| `i{`/`a{` | Interno/intorno a parentesi graffe           |

### Modalità visuale

Premete `v` per la selezione carattere per carattere o `V` per la selezione riga per riga. I movimenti estendono la selezione e gli operatori agiscono direttamente su di essa.

| Comando          | Azione                                                               |
| :--------------- | :------------------------------------------------------------------- |
| `d`/`x`          | Elimina selezione                                                    |
| `y`              | Copia selezione                                                      |
| `c`/`s`          | Cambia selezione                                                     |
| `p`              | Sostituisci selezione con il contenuto del registro                  |
| `r{char}`        | Sostituisci ogni carattere selezionato con `{char}`                  |
| `~`/`u`/`U`      | Attiva/disattiva, minuscole o maiuscole selezione                    |
| `>`/`<`          | Indenta o dedenta le righe selezionate                               |
| `J`              | Unisci le righe selezionate                                          |
| `o`              | Scambia cursore e ancoraggio                                         |
| `iw`/`aw`/`i"`/… | Seleziona un oggetto di testo                                        |
| `v`/`V`          | Attiva/disattiva tra carattere per carattere e riga per riga, o esci |

La modalità visuale blocco con `Ctrl+V` non è supportata.

## Cronologia dei comandi

Claude Code mantiene la cronologia dei comandi per la sessione corrente:

* La cronologia dell'input viene memorizzata per directory di lavoro
* La cronologia dell'input si ripristina quando eseguite `/clear` per avviare una nuova sessione. La conversazione della sessione precedente viene preservata e può essere ripresa.
* Utilizzate i tasti freccia su/giù per navigare (vedere le scorciatoie da tastiera sopra)
* **Nota**: l'espansione della cronologia (`!`) è disabilitata per impostazione predefinita

### Ricerca inversa con Ctrl+R

Premete `Ctrl+R` per cercare in modo interattivo nella vostra cronologia dei comandi:

1. **Avvia ricerca**: premete `Ctrl+R` per attivare la ricerca inversa nella cronologia
2. **Digita query**: inserite il testo da cercare nei comandi precedenti. Il termine di ricerca è evidenziato nei risultati corrispondenti
3. **Naviga tra i risultati**: premete `Ctrl+R` di nuovo per scorrere i risultati più vecchi
4. **Cambia ambito**: la ricerca è impostata per impostazione predefinita su prompt da tutti i progetti. Premete `Ctrl+S` per alternare l'ambito tra questa sessione, questo progetto e tutti i progetti
5. **Accetta il risultato**:
   * Premete `Tab` o `Esc` per accettare il risultato corrente e continuare a modificare
   * Premete `Enter` per accettare ed eseguire il comando immediatamente
6. **Annulla ricerca**:
   * Premete `Ctrl+C` per annullare e ripristinare l'input originale
   * Premete `Backspace` su una ricerca vuota per annullare

La ricerca visualizza i comandi corrispondenti con il termine di ricerca evidenziato, in modo da poter trovare e riutilizzare gli input precedenti.

## Comandi bash in background

Claude Code supporta l'esecuzione di comandi bash in background, consentendovi di continuare a lavorare mentre i processi a lunga esecuzione vengono eseguiti.

### Come funziona l'esecuzione in background

Quando Claude Code esegue un comando in background, esegue il comando in modo asincrono e restituisce immediatamente un ID di attività in background. Claude Code può rispondere a nuovi prompt mentre il comando continua a essere eseguito in background.

Per eseguire i comandi in background, potete:

* Chiedere a Claude Code di eseguire un comando in background
* Premere Ctrl+B per spostare una normale invocazione dello strumento Bash in background. (Gli utenti Tmux devono premere Ctrl+B due volte a causa del tasto di prefisso di tmux.)

**Caratteristiche principali:**

* L'output viene scritto in un file e Claude può recuperarlo utilizzando lo strumento Read
* Le attività in background hanno ID univoci per il tracciamento e il recupero dell'output
* Le attività in background vengono pulite automaticamente quando Claude Code esce
* Le attività in background vengono terminate automaticamente se l'output supera 5GB, con una nota in stderr che spiega il motivo

Per disabilitare tutta la funzionalità di attività in background, impostare la variabile di ambiente `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` su `1`. Vedere [Variabili di ambiente](/it/env-vars) per i dettagli.

**Comandi comunemente eseguiti in background:**

* Strumenti di build (webpack, vite, make)
* Gestori di pacchetti (npm, yarn, pnpm)
* Test runner (jest, pytest)
* Server di sviluppo
* Processi a lunga esecuzione (docker, terraform)

### Modalità Bash con prefisso `!`

Eseguite i comandi bash direttamente senza passare per Claude aggiungendo il prefisso `!` al vostro input:

```bash theme={null}
! npm test
! git status
! ls -la
```

Modalità Bash:

* Aggiunge il comando e il suo output al contesto della conversazione
* Mostra l'avanzamento e l'output in tempo reale
* Supporta lo stesso backgrounding `Ctrl+B` per i comandi a lunga esecuzione
* Non richiede a Claude di interpretare o approvare il comando
* Supporta l'autocompletamento basato sulla cronologia: digitate un comando parziale e premete **Tab** per completare dai comandi `!` precedenti nel progetto corrente
* Esci con `Escape`, `Backspace` o `Ctrl+U` su un prompt vuoto
* Incollare il testo che inizia con `!` in un prompt vuoto entra automaticamente in modalità bash, corrispondendo al comportamento digitato `!`

Questo è utile per le operazioni shell rapide mantenendo il contesto della conversazione.

## Suggerimenti di prompt

Quando aprite una sessione per la prima volta, un comando di esempio in grigio appare nell'input del prompt per aiutarvi a iniziare. Claude Code lo sceglie dalla cronologia git del vostro progetto, quindi riflette i file su cui avete lavorato di recente.

Dopo che Claude risponde, i suggerimenti continuano ad apparire in base alla vostra cronologia di conversazione, come un passaggio di follow-up da una richiesta in più parti o una continuazione naturale del vostro flusso di lavoro.

* Premete **Tab** o **Freccia destra** per inserire il suggerimento nell'input del prompt, quindi **Invio** per inviare
* Iniziate a digitare per dismissarlo

Il suggerimento viene eseguito come una richiesta in background che riutilizza la cache del prompt della conversazione padre, quindi il costo aggiuntivo è minimo. Claude Code salta la generazione di suggerimenti quando la cache è fredda per evitare costi inutili.

I suggerimenti vengono automaticamente saltati dopo il primo turno di una conversazione, in modalità non interattiva e in Plan Mode.

Per disabilitare completamente i suggerimenti di prompt, impostare la variabile di ambiente o attivare/disattivare l'impostazione in `/config`:

```bash theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## Domande laterali con /btw

Utilizzate `/btw` per fare una domanda rapida sul vostro lavoro corrente senza aggiungerla alla cronologia della conversazione. Questo è utile quando volete una risposta veloce ma non volete ingombrare il contesto principale o far deviare Claude da un'attività a lunga esecuzione.

```
/btw what was the name of that config file again?
```

Le domande laterali hanno piena visibilità nella conversazione corrente, quindi potete chiedere informazioni sul codice che Claude ha già letto, sulle decisioni che ha preso in precedenza, o su qualsiasi altra cosa della sessione. La domanda e la risposta sono effimere: appaiono in un overlay dismissibile e non entrano mai nella cronologia della conversazione.

* **Disponibile mentre Claude sta lavorando**: potete eseguire `/btw` anche mentre Claude sta elaborando una risposta. La domanda laterale viene eseguita in modo indipendente e non interrompe il turno principale.
* **Nessun accesso agli strumenti**: le domande laterali rispondono solo da ciò che è già nel contesto. Claude non può leggere file, eseguire comandi o cercare quando risponde a una domanda laterale.
* **Risposta singola**: non ci sono turni di follow-up. Se avete bisogno di un dialogo, utilizzate un prompt normale.
* **Costo basso**: la domanda laterale riutilizza la cache del prompt della conversazione padre, quindi il costo aggiuntivo è minimo.

Premete **Space**, **Enter** o **Escape** per dismissere la risposta e tornare al prompt.

`/btw` è l'inverso di un [subagent](/it/sub-agents): vede la vostra conversazione completa ma non ha strumenti, mentre un subagent ha strumenti completi ma inizia con un contesto vuoto. Utilizzate `/btw` per chiedere informazioni su ciò che Claude già conosce da questa sessione; utilizzate un subagent per scoprire qualcosa di nuovo.

## Elenco delle attività

Quando lavorate su lavori complessi e multistep, Claude crea un elenco di attività per tracciare l'avanzamento. Le attività appaiono nell'area di stato del vostro terminale con indicatori che mostrano cosa è in sospeso, in corso o completato.

* Premete `Ctrl+T` per attivare/disattivare la visualizzazione dell'elenco delle attività. La visualizzazione mostra fino a 5 attività alla volta
* Per visualizzare tutte le attività o cancellarle, chiedete direttamente a Claude: "show me all tasks" o "clear all tasks"
* Le attività persistono attraverso i compattamenti del contesto, aiutando Claude a rimanere organizzato su progetti più grandi
* Per condividere un elenco di attività tra sessioni, impostare `CLAUDE_CODE_TASK_LIST_ID` per utilizzare una directory denominata in `~/.claude/tasks/`: `CLAUDE_CODE_TASK_LIST_ID=my-project claude`

## Riepilogo della sessione

Quando tornate al terminale dopo esservi allontanati, Claude Code mostra un riepilogo di una riga di ciò che è accaduto nella sessione finora. Il riepilogo viene generato in background una volta che sono trascorsi almeno tre minuti dall'ultimo turno completato e il terminale non è a fuoco, quindi è pronto quando tornate. I riepiloghi appaiono solo una volta che la sessione ha almeno tre turni, e mai due volte di seguito.

Eseguite `/recap` per generare un riepilogo su richiesta. Per disattivare i riepiloghi automatici, aprite `/config` e disabilitate **Session recap**.

Il riepilogo della sessione è abilitato per impostazione predefinita per ogni piano e provider. Il riepilogo viene sempre saltato in modalità non interattiva.

## Stato della revisione PR

Quando lavorate su un ramo con una pull request aperta, Claude Code visualizza un collegamento PR cliccabile nel footer (ad esempio, "PR #446"). Il collegamento ha una sottolineatura colorata che indica lo stato della revisione:

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

* [Skills](/it/skills) - Prompt personalizzati e flussi di lavoro
* [Checkpointing](/it/checkpointing) - Riavvolgi le modifiche di Claude e ripristina gli stati precedenti
* [Riferimento CLI](/it/cli-reference) - Flag e opzioni della riga di comando
* [Impostazioni](/it/settings) - Opzioni di configurazione
* [Gestione della memoria](/it/memory) - Gestione dei file CLAUDE.md
