> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Ottimizza la configurazione del tuo terminale

> Claude Code funziona al meglio quando il tuo terminale è correttamente configurato. Segui queste linee guida per ottimizzare la tua esperienza.

### Temi e aspetto

Claude non può controllare il tema del tuo terminale. Questo è gestito dall'applicazione del tuo terminale. Puoi far corrispondere il tema di Claude Code al tuo terminale in qualsiasi momento tramite il comando `/config`.

Per ulteriori personalizzazioni dell'interfaccia di Claude Code stesso, puoi configurare una [linea di stato personalizzata](/it/statusline) per visualizzare informazioni contestuali come il modello corrente, la directory di lavoro o il ramo git nella parte inferiore del tuo terminale.

### Interruzioni di riga

Hai diverse opzioni per inserire interruzioni di riga in Claude Code:

* **Escape rapido**: Digita `\` seguito da Invio per creare una nuova riga
* **Shift+Invio**: Funziona immediatamente in iTerm2, WezTerm, Ghostty e Kitty
* **Scorciatoia da tastiera**: Configura un keybinding per inserire una nuova riga in altri terminali

**Configura Shift+Invio per altri terminali**

Esegui `/terminal-setup` all'interno di Claude Code per configurare automaticamente Shift+Invio per VS Code, Alacritty, Zed e Warp.

<Note>
  Il comando `/terminal-setup` è visibile solo nei terminali che richiedono una configurazione manuale. Se stai utilizzando iTerm2, WezTerm, Ghostty o Kitty, non vedrai questo comando perché Shift+Invio funziona già nativamente.
</Note>

**Configura Option+Invio (VS Code, iTerm2 o macOS Terminal.app)**

**Per Mac Terminal.app:**

1. Apri Impostazioni → Profili → Tastiera
2. Seleziona "Usa Option come Meta Key"

**Per il terminale iTerm2 e VS Code:**

1. Apri Impostazioni → Profili → Tasti
2. In Generale, imposta il tasto Option sinistro/destro su "Esc+"

### Configurazione delle notifiche

Non perdere mai quando Claude completa un'attività con una corretta configurazione delle notifiche:

#### Notifiche di sistema iTerm 2

Per gli avvisi di iTerm 2 quando le attività si completano:

1. Apri Preferenze di iTerm 2
2. Vai a Profili → Terminale
3. Abilita "Silence bell" e Filtra avvisi → "Invia avvisi generati da sequenza di escape"
4. Imposta il ritardo di notifica preferito

Nota che queste notifiche sono specifiche di iTerm 2 e non disponibili nel Terminal predefinito di macOS.

#### Hook di notifica personalizzati

Per la gestione avanzata delle notifiche, puoi creare [hook di notifica](/it/hooks#notification) per eseguire la tua logica personalizzata.

### Gestione di input di grandi dimensioni

Quando lavori con codice esteso o istruzioni lunghe:

* **Evita l'incollamento diretto**: Claude Code potrebbe avere difficoltà con contenuti incollati molto lunghi
* **Usa flussi di lavoro basati su file**: Scrivi il contenuto in un file e chiedi a Claude di leggerlo
* **Sii consapevole delle limitazioni di VS Code**: Il terminale di VS Code è particolarmente soggetto al troncamento di incollamenti lunghi

### Modalità Vim

Claude Code supporta un sottoinsieme di keybinding Vim che può essere abilitato con `/vim` o configurato tramite `/config`.

Il sottoinsieme supportato include:

* Cambio di modalità: `Esc` (a NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (a INSERT)
* Navigazione: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`, `f`/`F`/`t`/`T` con ripetizione `;`/`,`
* Modifica: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (ripeti)
* Copia/incolla: `yy`/`Y`, `yw`/`ye`/`yb`, `p`/`P`
* Oggetti di testo: `iw`/`aw`, `iW`/`aW`, `i"`/`a"`, `i'`/`a'`, `i(`/`a(`, `i[`/`a[`, `i{`/`a{`
* Indentazione: `>>`/`<<`
* Operazioni di riga: `J` (unisci righe)

Vedi [Modalità interattiva](/it/interactive-mode#vim-editor-mode) per il riferimento completo.
