> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Personalizzare le scorciatoie da tastiera

> Personalizzare le scorciatoie da tastiera in Claude Code con un file di configurazione keybindings.

<Note>
  Le scorciatoie da tastiera personalizzabili richiedono Claude Code v2.1.18 o versioni successive. Controllare la versione con `claude --version`.
</Note>

Claude Code supporta scorciatoie da tastiera personalizzabili. Eseguire `/keybindings` per creare o aprire il file di configurazione in `~/.claude/keybindings.json`.

## File di configurazione

Il file di configurazione delle scorciatoie da tastiera è un oggetto con un array `bindings`. Ogni blocco specifica un contesto e una mappa di sequenze di tasti per le azioni.

<Note>Le modifiche al file keybindings vengono rilevate automaticamente e applicate senza riavviare Claude Code.</Note>

| Campo      | Descrizione                                                         |
| :--------- | :------------------------------------------------------------------ |
| `$schema`  | URL dello schema JSON opzionale per l'autocompletamento dell'editor |
| `$docs`    | URL della documentazione opzionale                                  |
| `bindings` | Array di blocchi di binding per contesto                            |

Questo esempio associa `Ctrl+E` per aprire un editor esterno nel contesto della chat e annulla l'associazione di `Ctrl+U`:

```json  theme={null}
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/it/keybindings",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null
      }
    }
  ]
}
```

## Contesti

Ogni blocco di binding specifica un **contesto** dove si applicano i binding:

| Contesto          | Descrizione                                                                    |
| :---------------- | :----------------------------------------------------------------------------- |
| `Global`          | Si applica ovunque nell'app                                                    |
| `Chat`            | Area di input della chat principale                                            |
| `Autocomplete`    | Menu di autocompletamento è aperto                                             |
| `Settings`        | Menu delle impostazioni (chiusura solo con escape)                             |
| `Confirmation`    | Dialoghi di permesso e conferma                                                |
| `Tabs`            | Componenti di navigazione delle schede                                         |
| `Help`            | Menu della guida è visibile                                                    |
| `Transcript`      | Visualizzatore di trascrizione                                                 |
| `HistorySearch`   | Modalità di ricerca nella cronologia (Ctrl+R)                                  |
| `Task`            | Attività in background in esecuzione                                           |
| `ThemePicker`     | Dialogo di selezione del tema                                                  |
| `Attachments`     | Navigazione della barra immagini/allegati                                      |
| `Footer`          | Navigazione dell'indicatore di piè di pagina (attività, team, diff)            |
| `MessageSelector` | Selezione dei messaggi nella finestra di dialogo di riavvolgimento e riepilogo |
| `DiffDialog`      | Navigazione del visualizzatore diff                                            |
| `ModelPicker`     | Livello di sforzo del selezionatore di modelli                                 |
| `Select`          | Componenti generici di selezione/elenco                                        |
| `Plugin`          | Dialogo dei plugin (sfoglia, scopri, gestisci)                                 |

## Azioni disponibili

Le azioni seguono un formato `namespace:action`, come `chat:submit` per inviare un messaggio o `app:toggleTodos` per mostrare l'elenco delle attività. Ogni contesto ha azioni specifiche disponibili.

### Azioni dell'app

Azioni disponibili nel contesto `Global`:

| Azione                 | Predefinito | Descrizione                                               |
| :--------------------- | :---------- | :-------------------------------------------------------- |
| `app:interrupt`        | Ctrl+C      | Annulla l'operazione corrente                             |
| `app:exit`             | Ctrl+D      | Esci da Claude Code                                       |
| `app:toggleTodos`      | Ctrl+T      | Attiva/disattiva la visibilità dell'elenco delle attività |
| `app:toggleTranscript` | Ctrl+O      | Attiva/disattiva la trascrizione dettagliata              |

### Azioni della cronologia

Azioni per navigare nella cronologia dei comandi:

| Azione             | Predefinito | Descrizione                          |
| :----------------- | :---------- | :----------------------------------- |
| `history:search`   | Ctrl+R      | Apri ricerca nella cronologia        |
| `history:previous` | Su          | Elemento della cronologia precedente |
| `history:next`     | Giù         | Elemento della cronologia successivo |

### Azioni della chat

Azioni disponibili nel contesto `Chat`:

| Azione                | Predefinito               | Descrizione                            |
| :-------------------- | :------------------------ | :------------------------------------- |
| `chat:cancel`         | Escape                    | Annulla l'input corrente               |
| `chat:killAgents`     | Ctrl+X Ctrl+K             | Termina tutti gli agenti in background |
| `chat:cycleMode`      | Shift+Tab\*               | Cicla le modalità di permesso          |
| `chat:modelPicker`    | Cmd+P / Meta+P            | Apri il selezionatore di modelli       |
| `chat:fastMode`       | Meta+O                    | Attiva/disattiva la modalità veloce    |
| `chat:thinkingToggle` | Cmd+T / Meta+T            | Attiva/disattiva il pensiero esteso    |
| `chat:submit`         | Invio                     | Invia il messaggio                     |
| `chat:undo`           | Ctrl+\_                   | Annulla l'ultima azione                |
| `chat:externalEditor` | Ctrl+G, Ctrl+X Ctrl+E     | Apri nell'editor esterno               |
| `chat:stash`          | Ctrl+S                    | Nascondi il prompt corrente            |
| `chat:imagePaste`     | Ctrl+V (Alt+V su Windows) | Incolla immagine                       |

\*Su Windows senza modalità VT (Node \<24.2.0/\<22.17.0, Bun \<1.2.23), il valore predefinito è Meta+M.

### Azioni di autocompletamento

Azioni disponibili nel contesto `Autocomplete`:

| Azione                  | Predefinito | Descrizione             |
| :---------------------- | :---------- | :---------------------- |
| `autocomplete:accept`   | Tab         | Accetta il suggerimento |
| `autocomplete:dismiss`  | Escape      | Chiudi il menu          |
| `autocomplete:previous` | Su          | Suggerimento precedente |
| `autocomplete:next`     | Giù         | Suggerimento successivo |

### Azioni di conferma

Azioni disponibili nel contesto `Confirmation`:

| Azione                      | Predefinito     | Descrizione                                  |
| :-------------------------- | :-------------- | :------------------------------------------- |
| `confirm:yes`               | Y, Invio        | Conferma l'azione                            |
| `confirm:no`                | N, Escape       | Rifiuta l'azione                             |
| `confirm:previous`          | Su              | Opzione precedente                           |
| `confirm:next`              | Giù             | Opzione successiva                           |
| `confirm:nextField`         | Tab             | Campo successivo                             |
| `confirm:previousField`     | (non associato) | Campo precedente                             |
| `confirm:cycleMode`         | Shift+Tab       | Cicla le modalità di permesso                |
| `confirm:toggleExplanation` | Ctrl+E          | Attiva/disattiva la spiegazione del permesso |

### Azioni di permesso

Azioni disponibili nel contesto `Confirmation` per i dialoghi di permesso:

| Azione                   | Predefinito | Descrizione                                            |
| :----------------------- | :---------- | :----------------------------------------------------- |
| `permission:toggleDebug` | Ctrl+D      | Attiva/disattiva le informazioni di debug del permesso |

### Azioni di trascrizione

Azioni disponibili nel contesto `Transcript`:

| Azione                     | Predefinito    | Descrizione                                               |
| :------------------------- | :------------- | :-------------------------------------------------------- |
| `transcript:toggleShowAll` | Ctrl+E         | Attiva/disattiva la visualizzazione di tutto il contenuto |
| `transcript:exit`          | Ctrl+C, Escape | Esci dalla visualizzazione della trascrizione             |

### Azioni di ricerca nella cronologia

Azioni disponibili nel contesto `HistorySearch`:

| Azione                  | Predefinito | Descrizione                   |
| :---------------------- | :---------- | :---------------------------- |
| `historySearch:next`    | Ctrl+R      | Corrispondenza successiva     |
| `historySearch:accept`  | Escape, Tab | Accetta la selezione          |
| `historySearch:cancel`  | Ctrl+C      | Annulla la ricerca            |
| `historySearch:execute` | Invio       | Esegui il comando selezionato |

### Azioni delle attività

Azioni disponibili nel contesto `Task`:

| Azione            | Predefinito | Descrizione                     |
| :---------------- | :---------- | :------------------------------ |
| `task:background` | Ctrl+B      | Attività in background corrente |

### Azioni del tema

Azioni disponibili nel contesto `ThemePicker`:

| Azione                           | Predefinito | Descrizione                                      |
| :------------------------------- | :---------- | :----------------------------------------------- |
| `theme:toggleSyntaxHighlighting` | Ctrl+T      | Attiva/disattiva l'evidenziazione della sintassi |

### Azioni della guida

Azioni disponibili nel contesto `Help`:

| Azione         | Predefinito | Descrizione                |
| :------------- | :---------- | :------------------------- |
| `help:dismiss` | Escape      | Chiudi il menu della guida |

### Azioni delle schede

Azioni disponibili nel contesto `Tabs`:

| Azione          | Predefinito         | Descrizione       |
| :-------------- | :------------------ | :---------------- |
| `tabs:next`     | Tab, Destra         | Scheda successiva |
| `tabs:previous` | Shift+Tab, Sinistra | Scheda precedente |

### Azioni degli allegati

Azioni disponibili nel contesto `Attachments`:

| Azione                 | Predefinito     | Descrizione                     |
| :--------------------- | :-------------- | :------------------------------ |
| `attachments:next`     | Destra          | Allegato successivo             |
| `attachments:previous` | Sinistra        | Allegato precedente             |
| `attachments:remove`   | Backspace, Canc | Rimuovi l'allegato selezionato  |
| `attachments:exit`     | Giù, Escape     | Esci dalla barra degli allegati |

### Azioni del piè di pagina

Azioni disponibili nel contesto `Footer`:

| Azione                  | Predefinito | Descrizione                                   |
| :---------------------- | :---------- | :-------------------------------------------- |
| `footer:next`           | Destra      | Elemento del piè di pagina successivo         |
| `footer:previous`       | Sinistra    | Elemento del piè di pagina precedente         |
| `footer:openSelected`   | Invio       | Apri l'elemento del piè di pagina selezionato |
| `footer:clearSelection` | Escape      | Cancella la selezione del piè di pagina       |

### Azioni del selezionatore di messaggi

Azioni disponibili nel contesto `MessageSelector`:

| Azione                   | Predefinito                            | Descrizione                       |
| :----------------------- | :------------------------------------- | :-------------------------------- |
| `messageSelector:up`     | Su, K, Ctrl+P                          | Sposta verso l'alto nell'elenco   |
| `messageSelector:down`   | Giù, J, Ctrl+N                         | Sposta verso il basso nell'elenco |
| `messageSelector:top`    | Ctrl+Su, Shift+Su, Meta+Su, Shift+K    | Salta all'inizio                  |
| `messageSelector:bottom` | Ctrl+Giù, Shift+Giù, Meta+Giù, Shift+J | Salta alla fine                   |
| `messageSelector:select` | Invio                                  | Seleziona il messaggio            |

### Azioni diff

Azioni disponibili nel contesto `DiffDialog`:

| Azione                | Predefinito              | Descrizione                            |
| :-------------------- | :----------------------- | :------------------------------------- |
| `diff:dismiss`        | Escape                   | Chiudi il visualizzatore diff          |
| `diff:previousSource` | Sinistra                 | Sorgente diff precedente               |
| `diff:nextSource`     | Destra                   | Sorgente diff successiva               |
| `diff:previousFile`   | Su                       | File precedente nel diff               |
| `diff:nextFile`       | Giù                      | File successivo nel diff               |
| `diff:viewDetails`    | Invio                    | Visualizza i dettagli del diff         |
| `diff:back`           | (specifico del contesto) | Torna indietro nel visualizzatore diff |

### Azioni del selezionatore di modelli

Azioni disponibili nel contesto `ModelPicker`:

| Azione                       | Predefinito | Descrizione                     |
| :--------------------------- | :---------- | :------------------------------ |
| `modelPicker:decreaseEffort` | Sinistra    | Diminuisci il livello di sforzo |
| `modelPicker:increaseEffort` | Destra      | Aumenta il livello di sforzo    |

### Azioni di selezione

Azioni disponibili nel contesto `Select`:

| Azione            | Predefinito    | Descrizione          |
| :---------------- | :------------- | :------------------- |
| `select:next`     | Giù, J, Ctrl+N | Opzione successiva   |
| `select:previous` | Su, K, Ctrl+P  | Opzione precedente   |
| `select:accept`   | Invio          | Accetta la selezione |
| `select:cancel`   | Escape         | Annulla la selezione |

### Azioni dei plugin

Azioni disponibili nel contesto `Plugin`:

| Azione           | Predefinito | Descrizione                              |
| :--------------- | :---------- | :--------------------------------------- |
| `plugin:toggle`  | Spazio      | Attiva/disattiva la selezione del plugin |
| `plugin:install` | I           | Installa i plugin selezionati            |

### Azioni delle impostazioni

Azioni disponibili nel contesto `Settings`:

| Azione            | Predefinito | Descrizione                                               |
| :---------------- | :---------- | :-------------------------------------------------------- |
| `settings:search` | /           | Entra in modalità di ricerca                              |
| `settings:retry`  | R           | Riprova a caricare i dati di utilizzo (in caso di errore) |

### Azioni vocali

Azioni disponibili nel contesto `Chat` quando la [dettatura vocale](/it/voice-dictation) è abilitata:

| Azione             | Predefinito | Descrizione                         |
| :----------------- | :---------- | :---------------------------------- |
| `voice:pushToTalk` | Spazio      | Tieni premuto per dettare un prompt |

## Sintassi delle sequenze di tasti

### Modificatori

Utilizzare i tasti modificatori con il separatore `+`:

* `ctrl` o `control` - Tasto Control
* `alt`, `opt`, o `option` - Tasto Alt/Option
* `shift` - Tasto Shift
* `meta`, `cmd`, o `command` - Tasto Meta/Command

Ad esempio:

```text  theme={null}
ctrl+k          Singolo tasto con modificatore
shift+tab       Shift + Tab
meta+p          Command/Meta + P
ctrl+shift+c    Più modificatori
```

### Lettere maiuscole

Una lettera maiuscola autonoma implica Shift. Ad esempio, `K` è equivalente a `shift+k`. Questo è utile per i binding in stile vim dove i tasti maiuscoli e minuscoli hanno significati diversi.

Le lettere maiuscole con modificatori (ad es. `ctrl+K`) sono trattate come stilistiche e **non** implicano Shift — `ctrl+K` è lo stesso di `ctrl+k`.

### Accordi

Gli accordi sono sequenze di tasti separate da spazi:

```text  theme={null}
ctrl+k ctrl+s   Premi Ctrl+K, rilascia, quindi Ctrl+S
```

### Tasti speciali

* `escape` o `esc` - Tasto Escape
* `enter` o `return` - Tasto Invio
* `tab` - Tasto Tab
* `space` - Barra spaziatrice
* `up`, `down`, `left`, `right` - Tasti freccia
* `backspace`, `delete` - Tasti Canc

## Annulla l'associazione delle scorciatoie predefinite

Impostare un'azione su `null` per annullare l'associazione di una scorciatoia predefinita:

```json  theme={null}
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+s": null
      }
    }
  ]
}
```

## Scorciatoie riservate

Queste scorciatoie non possono essere riassociate:

| Scorciatoia | Motivo                                               |
| :---------- | :--------------------------------------------------- |
| Ctrl+C      | Interrupt/annullamento hardcoded                     |
| Ctrl+D      | Uscita hardcoded                                     |
| Ctrl+M      | Identico a Invio nei terminali (entrambi inviano CR) |

## Conflitti del terminale

Alcune scorciatoie potrebbero entrare in conflitto con i multiplexer di terminale:

| Scorciatoia | Conflitto                                     |
| :---------- | :-------------------------------------------- |
| Ctrl+B      | Prefisso tmux (premere due volte per inviare) |
| Ctrl+A      | Prefisso GNU screen                           |
| Ctrl+Z      | Sospensione del processo Unix (SIGTSTP)       |

## Interazione con la modalità Vim

Quando la modalità vim è abilitata (`/vim`), i keybindings e la modalità vim operano indipendentemente:

* **Modalità Vim** gestisce l'input a livello di input di testo (movimento del cursore, modalità, movimenti)
* **Keybindings** gestisce le azioni a livello di componente (attiva/disattiva attività, invia, ecc.)
* Il tasto Escape in modalità vim passa da INSERT a NORMAL; non attiva `chat:cancel`
* La maggior parte delle scorciatoie Ctrl+tasto passano attraverso la modalità vim al sistema di keybinding
* In modalità vim NORMAL, `?` mostra il menu della guida (comportamento vim)

## Convalida

Claude Code convalida i tuoi keybindings e mostra avvisi per:

* Errori di analisi (JSON non valido o struttura non valida)
* Nomi di contesto non validi
* Conflitti di scorciatoie riservate
* Conflitti di multiplexer di terminale
* Binding duplicati nello stesso contesto

Eseguire `/doctor` per visualizzare eventuali avvisi di keybinding.
