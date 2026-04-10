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

# Ottimizza la configurazione del tuo terminale

> Claude Code funziona al meglio quando il tuo terminale è correttamente configurato. Segui queste linee guida per ottimizzare la tua esperienza.

### Temi e aspetto

Claude non può controllare il tema del tuo terminale. Questo è gestito dall'applicazione del tuo terminale. Puoi far corrispondere il tema di Claude Code al tuo terminale in qualsiasi momento tramite il comando `/config`.

Per ulteriori personalizzazioni dell'interfaccia di Claude Code stesso, puoi configurare una [linea di stato personalizzata](/it/statusline) per visualizzare informazioni contestuali come il modello corrente, la directory di lavoro o il ramo git nella parte inferiore del tuo terminale.

### Interruzioni di riga

Hai diverse opzioni per inserire interruzioni di riga in Claude Code:

* **Escape rapido**: Digita `\` seguito da Invio per creare una nuova riga
* **Shift+Invio**: Funziona immediatamente in iTerm2, WezTerm, Ghostty e Kitty
* **Scorciatoia da tastiera**: Configura una scorciatoia da tastiera per inserire una nuova riga in altri terminali

**Configura Shift+Invio per altri terminali**

Esegui `/terminal-setup` all'interno di Claude Code per configurare automaticamente Shift+Invio per VS Code, Alacritty, Zed e Warp.

<Note>
  Il comando `/terminal-setup` è visibile solo nei terminali che richiedono una configurazione manuale. Se stai utilizzando iTerm2, WezTerm, Ghostty o Kitty, non vedrai questo comando perché Shift+Invio funziona già nativamente.
</Note>

**Configura Option+Invio (VS Code, iTerm2 o macOS Terminal.app)**

**Per Mac Terminal.app:**

1. Apri Impostazioni → Profili → Tastiera
2. Seleziona "Usa Option come Meta Key"

**Per iTerm2:**

1. Apri Impostazioni → Profili → Tasti
2. In Generale, imposta il tasto Option sinistro/destro su "Esc+"

**Per il terminale VS Code:**

Imposta `"terminal.integrated.macOptionIsMeta": true` nelle impostazioni di VS Code.

### Configurazione delle notifiche

Quando Claude finisce di lavorare ed è in attesa del tuo input, genera un evento di notifica. Puoi visualizzare questo evento come una notifica desktop tramite il tuo terminale o eseguire logica personalizzata con [hook di notifica](/it/hooks#notification).

#### Notifiche del terminale

Kitty e Ghostty supportano le notifiche desktop senza configurazione aggiuntiva. iTerm 2 richiede una configurazione:

1. Apri Impostazioni di iTerm 2 → Profili → Terminale
2. Abilita "Notification Center Alerts"
3. Fai clic su "Filter Alerts" e seleziona "Send escape sequence-generated alerts"

Se le notifiche non vengono visualizzate, verifica che l'applicazione del tuo terminale abbia i permessi di notifica nelle impostazioni del tuo sistema operativo.

Quando esegui Claude Code all'interno di tmux, le notifiche e la [barra di avanzamento del terminale](/it/settings#global-config-settings) raggiungono il terminale esterno, come iTerm2, Kitty o Ghostty, solo se abiliti il passthrough nella tua configurazione di tmux:

```
set -g allow-passthrough on
```

Senza questa impostazione, tmux intercetta le sequenze di escape e non raggiungono l'applicazione del terminale.

Altri terminali, incluso il Terminal predefinito di macOS, non supportano le notifiche native. Utilizza invece gli [hook di notifica](/it/hooks#notification).

#### Hook di notifica

Per aggiungere un comportamento personalizzato quando le notifiche vengono attivate, come riprodurre un suono o inviare un messaggio, configura un [hook di notifica](/it/hooks#notification). Gli hook vengono eseguiti insieme alle notifiche del terminale, non come sostituzione.

### Riduci lo sfarfallio e l'utilizzo della memoria

Se vedi sfarfallio durante sessioni lunghe, o la posizione di scorrimento del tuo terminale salta in alto mentre Claude sta lavorando, prova il [rendering a schermo intero](/it/fullscreen). Utilizza un percorso di rendering alternativo che mantiene la memoria piatta e aggiunge il supporto del mouse. Abilitalo con `CLAUDE_CODE_NO_FLICKER=1`.

### Gestione di input di grandi dimensioni

Quando lavori con codice esteso o istruzioni lunghe:

* **Evita l'incollamento diretto**: Claude Code potrebbe avere difficoltà con contenuti incollati molto lunghi
* **Usa flussi di lavoro basati su file**: Scrivi il contenuto in un file e chiedi a Claude di leggerlo
* **Sii consapevole delle limitazioni di VS Code**: Il terminale di VS Code è particolarmente soggetto al troncamento di incollamenti lunghi

### Modalità Vim

Claude Code supporta un sottoinsieme di scorciatoie da tastiera Vim che può essere abilitato con `/vim` o configurato tramite `/config`. Per impostare la modalità direttamente nel tuo file di configurazione, imposta la chiave di configurazione globale [`editorMode`](/it/settings#global-config-settings) su `"vim"` in `~/.claude.json`.

Il sottoinsieme supportato include:

* Cambio di modalità: `Esc` (a NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (a INSERT)
* Navigazione: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`, `f`/`F`/`t`/`T` con ripetizione `;`/`,`
* Modifica: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (ripeti)
* Copia/incolla: `yy`/`Y`, `yw`/`ye`/`yb`, `p`/`P`
* Oggetti di testo: `iw`/`aw`, `iW`/`aW`, `i"`/`a"`, `i'`/`a'`, `i(`/`a(`, `i[`/`a[`, `i{`/`a{`
* Indentazione: `>>`/`<<`
* Operazioni di riga: `J` (unisci righe)

Vedi [Modalità interattiva](/it/interactive-mode#vim-editor-mode) per il riferimento completo.
