> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configura il tuo terminale per Claude Code

> Correggi Shift+Invio per le nuove righe, ricevi un segnale acustico del terminale quando Claude finisce, configura tmux, abbina il tema dei colori e abilita la modalità Vim nella CLI di Claude Code.

Claude Code funziona in qualsiasi terminale senza configurazione. Questa pagina è per quando qualcosa di specifico non si comporta come previsto. Trova il tuo sintomo di seguito. Se tutto ti sembra già corretto, non hai bisogno di questa pagina.

* [Shift+Invio invia invece di inserire una nuova riga](#enter-multiline-prompts)
* [Le scorciatoie del tasto Option non funzionano su macOS](#enable-option-key-shortcuts-on-macos)
* [Nessun suono o avviso quando Claude finisce](#get-a-terminal-bell-or-notification)
* [Esegui Claude Code dentro tmux](#configure-tmux)
* [Lo schermo sfarfalla o il scrollback salta](#switch-to-fullscreen-rendering)
* [Vuoi i tasti Vim nel prompt](#edit-prompts-with-vim-keybindings)

Questa pagina riguarda come far inviare al tuo terminale i segnali giusti a Claude Code. Per modificare i tasti a cui Claude Code stesso risponde, consulta invece [scorciatoie da tastiera](/it/keybindings).

## Enter multiline prompts

Premere Invio invia il tuo messaggio. Per aggiungere un'interruzione di riga senza inviare, premi Ctrl+J, oppure digita `\` e poi premi Invio. Entrambi funzionano in ogni terminale senza configurazione.

Nella maggior parte dei terminali puoi anche premere Shift+Invio, ma il supporto varia a seconda dell'emulatore di terminale:

| Terminale                                                                      | Shift+Invio per nuova riga                  |
| :----------------------------------------------------------------------------- | :------------------------------------------ |
| Ghostty, Kitty, iTerm2, WezTerm, Warp, Apple Terminal                          | Funziona senza configurazione               |
| VS Code, Cursor, Windsurf, Alacritty, Zed                                      | Esegui `/terminal-setup` una volta          |
| Windows Terminal, gnome-terminal, JetBrains IDEs come PyCharm e Android Studio | Non disponibile; usa Ctrl+J o `\` poi Invio |

Per VS Code, Cursor, Windsurf, Alacritty e Zed, `/terminal-setup` scrive Shift+Invio e altre scorciatoie da tastiera nel file di configurazione del terminale. Se segnala un conflitto come `Found existing VSCode terminal Shift+Enter key binding`, rimuovi quella voce dal file delle scorciatoie da tastiera del terminale, ad esempio `keybindings.json` di VS Code, ed esegui il comando di nuovo. Esegui `/terminal-setup` direttamente nel terminale host piuttosto che dentro tmux o screen, poiché ha bisogno di scrivere nella configurazione del terminale host.

Se stai eseguendo dentro tmux, Shift+Invio richiede anche la [configurazione tmux di seguito](#configure-tmux) anche quando il terminale esterno la supporta.

Per associare la nuova riga a un tasto diverso, o per scambiare il comportamento in modo che Invio inserisca una nuova riga e Shift+Invio invii, mappa le azioni `chat:newline` e `chat:submit` nel tuo [file delle scorciatoie da tastiera](/it/keybindings).

## Enable Option key shortcuts on macOS

Alcuni scorciatoie di Claude Code utilizzano il tasto Option, come Option+Invio per una nuova riga o Option+P per cambiare modelli. Su macOS, la maggior parte dei terminali non invia Option come modificatore per impostazione predefinita, quindi questi scorciatoie non funzionano finché non lo abiliti. L'impostazione del terminale per questo è solitamente etichettata "Use Option as Meta Key"; Meta è il nome storico Unix per il tasto ora etichettato come Option o Alt.

<Tabs>
  <Tab title="Apple Terminal">
    Apri Impostazioni → Profili → Tastiera e seleziona "Use Option as Meta Key".

    Se hai accettato il prompt di primo avvio di Claude Code che offriva "Option+Invio per nuove righe e campanello visivo", questo è già fatto. Quel prompt esegue `/terminal-setup` per te, che abilita Option come Meta e cambia il campanello audio a un flash di schermo visivo nel tuo profilo Apple Terminal.
  </Tab>

  <Tab title="iTerm2">
    Apri Impostazioni → Profili → Tasti → Generale e imposta il tasto Option sinistro e il tasto Option destro su "Esc+".
  </Tab>

  <Tab title="VS Code">
    Aggiungi `"terminal.integrated.macOptionIsMeta": true` alle tue impostazioni di VS Code.
  </Tab>
</Tabs>

Per Ghostty, Kitty e altri terminali, cerca un'impostazione Option-as-Alt o Option-as-Meta nel file di configurazione del terminale.

## Get a terminal bell or notification

Quando Claude finisce un'attività o si mette in pausa per un prompt di autorizzazione, attiva un evento di notifica. Visualizzare questo come un campanello del terminale o una notifica desktop ti consente di passare ad altro lavoro mentre un'attività lunga è in esecuzione.

Claude Code invia una notifica desktop solo in Ghostty, Kitty e iTerm2; ogni altro terminale ha bisogno di un [hook Notification](#play-a-sound-with-a-notification-hook) invece. La notifica raggiunge anche la tua macchina locale tramite SSH, quindi una sessione remota può comunque avvertirti. Ghostty e Kitty la inoltrano al tuo centro notifiche del sistema operativo senza ulteriore configurazione. iTerm2 richiede che tu abiliti l'inoltro:

<Steps>
  <Step title="Apri le impostazioni di notifica di iTerm2">
    Vai a Impostazioni → Profili → Terminale.
  </Step>

  <Step title="Abilita gli avvisi">
    Seleziona "Notification Center Alerts", poi fai clic su "Filter Alerts" e abilita "Send escape sequence-generated alerts".
  </Step>
</Steps>

Se le notifiche ancora non appaiono, conferma che la tua applicazione di terminale ha il permesso di notifica nelle impostazioni del tuo sistema operativo, e se stai eseguendo dentro tmux, [abilita il passthrough](#configure-tmux).

### Play a sound with a Notification hook

In qualsiasi terminale puoi configurare un [hook Notification](/it/hooks-guide#get-notified-when-claude-needs-input) per riprodurre un suono o eseguire un comando personalizzato quando Claude ha bisogno della tua attenzione. Gli hook vengono eseguiti insieme alla notifica desktop piuttosto che sostituirla. I terminali come Warp o Apple Terminal si affidano a un hook da solo poiché Claude Code non invia loro una notifica desktop.

L'esempio di seguito riproduce un suono di sistema su macOS. La guida collegata ha comandi di notifica desktop per macOS, Linux e Windows.

```json ~/.claude/settings.json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "hooks": [{ "type": "command", "command": "afplay /System/Library/Sounds/Glass.aiff" }]
      }
    ]
  }
}
```

## Configure tmux

Quando Claude Code viene eseguito dentro tmux, due cose si rompono per impostazione predefinita: Shift+Invio invia invece di inserire una nuova riga, e le notifiche desktop e la [barra di avanzamento](/it/settings#global-config-settings) non raggiungono mai il terminale esterno. Aggiungi queste righe a `~/.tmux.conf`, poi esegui `tmux source-file ~/.tmux.conf` per applicarle al server in esecuzione:

```bash ~/.tmux.conf theme={null}
set -g allow-passthrough on
set -s extended-keys on
set -as terminal-features 'xterm*:extkeys'
```

La riga `allow-passthrough` consente alle notifiche e agli aggiornamenti di avanzamento di raggiungere iTerm2, Ghostty o Kitty invece di essere inghiottiti da tmux. Le righe `extended-keys` consentono a tmux di distinguere Shift+Invio da Invio semplice in modo che il scorciatoia della nuova riga funzioni.

## Match the color theme

Usa il comando `/theme`, o il selettore di tema in `/config`, per scegliere un tema di Claude Code che corrisponda al tuo terminale. Selezionando l'opzione auto rileva lo sfondo chiaro o scuro del tuo terminale, quindi il tema segue i cambiamenti di aspetto del sistema operativo ogni volta che il tuo terminale lo fa. I temi disponibili sono incorporati; non c'è un file di tema personalizzato. Claude Code non controlla lo schema di colori del terminale stesso, che è impostato dall'applicazione del terminale.

Per personalizzare ciò che appare in fondo all'interfaccia, configura una [linea di stato personalizzata](/it/statusline) che mostra il modello corrente, la directory di lavoro, il ramo git o altro contesto.

## Switch to fullscreen rendering

Se lo schermo sfarfalla o la posizione di scorrimento salta mentre Claude sta lavorando, passa alla [modalità di rendering a schermo intero](/it/fullscreen). Disegna su uno schermo separato che il terminale riserva per le app a schermo intero invece di aggiungere al tuo normale scrollback, il che mantiene l'utilizzo della memoria piatto e aggiunge il supporto del mouse per lo scorrimento e la selezione. In questa modalità scorri con il mouse o PageUp dentro Claude Code piuttosto che con lo scrollback nativo del tuo terminale; consulta la [pagina fullscreen](/it/fullscreen#search-and-review-the-conversation) per come cercare e copiare.

Esegui `/tui fullscreen` per passare nella sessione corrente con la tua conversazione intatta. Per renderlo predefinito, imposta la variabile di ambiente `CLAUDE_CODE_NO_FLICKER` prima di avviare Claude Code:

<CodeGroup>
  ```bash Bash and Zsh theme={null}
  CLAUDE_CODE_NO_FLICKER=1 claude
  ```

  ```powershell PowerShell theme={null}
  $env:CLAUDE_CODE_NO_FLICKER = "1"; claude
  ```

  ```json ~/.claude/settings.json theme={null}
  {
    "env": {
      "CLAUDE_CODE_NO_FLICKER": "1"
    }
  }
  ```
</CodeGroup>

## Paste large content

Quando incolla più di 10.000 caratteri nel prompt, Claude Code comprime l'input a un placeholder `[Pasted text]` in modo che la casella di input rimanga utilizzabile. Il contenuto completo viene comunque inviato a Claude quando invii.

Il terminale integrato di VS Code può perdere caratteri da incollamenti molto grandi prima che raggiungano Claude Code, quindi preferisci flussi di lavoro basati su file lì. Per input molto grandi come interi file o lunghi log, scrivi il contenuto in un file e chiedi a Claude di leggerlo invece di incollare. Questo mantiene la trascrizione della conversazione leggibile e consente a Claude di fare riferimento al file per percorso nei turni successivi.

## Edit prompts with Vim keybindings

Claude Code include una modalità di editing in stile Vim per l'input del prompt. Abilitala tramite `/config` → Editor mode, o impostando la chiave di configurazione globale [`editorMode`](/it/settings#global-config-settings) su `"vim"` in `~/.claude.json`. Imposta Editor mode di nuovo su `normal` per disattivarla.

La modalità Vim supporta un sottoinsieme di motions in modalità NORMAL e operatori, come la navigazione `hjkl` e `d`/`c`/`y` con oggetti di testo. Consulta la [tabella di riferimento della modalità editor Vim](/it/interactive-mode#vim-editor-mode) per la tabella completa dei tasti. I motions Vim non sono rimappabili tramite il file delle scorciatoie da tastiera.

Premere Invio invia comunque il tuo prompt in modalità INSERT, a differenza di Vim standard. Usa `o` o `O` in modalità NORMAL, o Ctrl+J, per inserire una nuova riga invece.

## Related resources

* [Interactive mode](/it/interactive-mode): riferimento completo delle scorciatoie da tastiera e la tabella dei tasti Vim
* [Keybindings](/it/keybindings): rimappa qualsiasi scorciatoia di Claude Code, inclusi Invio e Shift+Invio
* [Fullscreen rendering](/it/fullscreen): dettagli su scorrimento, ricerca e copia in modalità fullscreen
* [Hooks guide](/it/hooks-guide): altri esempi di hook Notification per Linux e Windows
* [Troubleshooting](/it/troubleshooting): correzioni per problemi al di fuori della configurazione del terminale
