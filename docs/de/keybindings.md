> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Tastaturkürzel anpassen

> Passen Sie Tastaturkürzel in Claude Code mit einer Keybindings-Konfigurationsdatei an.

<Note>
  Anpassbare Tastaturkürzel erfordern Claude Code v2.1.18 oder später. Überprüfen Sie Ihre Version mit `claude --version`.
</Note>

Claude Code unterstützt anpassbare Tastaturkürzel. Führen Sie `/keybindings` aus, um Ihre Konfigurationsdatei unter `~/.claude/keybindings.json` zu erstellen oder zu öffnen.

## Konfigurationsdatei

Die Keybindings-Konfigurationsdatei ist ein Objekt mit einem `bindings`-Array. Jeder Block gibt einen Kontext und eine Zuordnung von Tastenkombinationen zu Aktionen an.

<Note>Änderungen an der Keybindings-Datei werden automatisch erkannt und angewendet, ohne Claude Code neu zu starten.</Note>

| Feld       | Beschreibung                                               |
| :--------- | :--------------------------------------------------------- |
| `$schema`  | Optionale JSON-Schema-URL für Editor-Autovervollständigung |
| `$docs`    | Optionale Dokumentations-URL                               |
| `bindings` | Array von Binding-Blöcken nach Kontext                     |

Dieses Beispiel bindet `Ctrl+E` zum Öffnen eines externen Editors im Chat-Kontext und hebt die Bindung von `Ctrl+U` auf:

```json  theme={null}
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/en/keybindings",
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

## Kontexte

Jeder Binding-Block gibt einen **Kontext** an, in dem die Bindings gelten:

| Kontext           | Beschreibung                                              |
| :---------------- | :-------------------------------------------------------- |
| `Global`          | Gilt überall in der App                                   |
| `Chat`            | Haupteingabebereich für Chat                              |
| `Autocomplete`    | Autovervollständigungsmenü ist offen                      |
| `Settings`        | Einstellungsmenü                                          |
| `Confirmation`    | Berechtigungs- und Bestätigungsdialoge                    |
| `Tabs`            | Tab-Navigationskomponenten                                |
| `Help`            | Hilfemenü ist sichtbar                                    |
| `Transcript`      | Transkript-Viewer                                         |
| `HistorySearch`   | Verlaufssuchmodus (Ctrl+R)                                |
| `Task`            | Hintergrundaufgabe wird ausgeführt                        |
| `ThemePicker`     | Design-Picker-Dialog                                      |
| `Attachments`     | Bildanhang-Navigation in Auswahldialogen                  |
| `Footer`          | Fußzeilen-Indikator-Navigation (Aufgaben, Teams, Diff)    |
| `MessageSelector` | Nachrichtenauswahl für Rewind- und Zusammenfassungsdialog |
| `DiffDialog`      | Diff-Viewer-Navigation                                    |
| `ModelPicker`     | Modell-Picker-Aufwandsstufe                               |
| `Select`          | Generische Select/List-Komponenten                        |
| `Plugin`          | Plugin-Dialog (durchsuchen, entdecken, verwalten)         |

## Verfügbare Aktionen

Aktionen folgen einem `namespace:action`-Format, wie `chat:submit` zum Senden einer Nachricht oder `app:toggleTodos` zum Anzeigen der Aufgabenliste. Jeder Kontext hat spezifische verfügbare Aktionen.

### App-Aktionen

Aktionen verfügbar im `Global`-Kontext:

| Aktion                 | Standard | Beschreibung                              |
| :--------------------- | :------- | :---------------------------------------- |
| `app:interrupt`        | Ctrl+C   | Aktuelle Operation abbrechen              |
| `app:exit`             | Ctrl+D   | Claude Code beenden                       |
| `app:redraw`           | Ctrl+L   | Bildschirm neu zeichnen                   |
| `app:toggleTodos`      | Ctrl+T   | Sichtbarkeit der Aufgabenliste umschalten |
| `app:toggleTranscript` | Ctrl+O   | Ausführliches Transkript umschalten       |

### Verlaufsaktionen

Aktionen zum Navigieren im Befehlsverlauf:

| Aktion             | Standard | Beschreibung               |
| :----------------- | :------- | :------------------------- |
| `history:search`   | Ctrl+R   | Verlaufssuche öffnen       |
| `history:previous` | Oben     | Vorheriges Verlaufselement |
| `history:next`     | Unten    | Nächstes Verlaufselement   |

### Chat-Aktionen

Aktionen verfügbar im `Chat`-Kontext:

| Aktion                | Standard                     | Beschreibung                           |
| :-------------------- | :--------------------------- | :------------------------------------- |
| `chat:cancel`         | Escape                       | Aktuelle Eingabe abbrechen             |
| `chat:killAgents`     | Ctrl+X Ctrl+K                | Alle Hintergrund-Agenten beenden       |
| `chat:cycleMode`      | Shift+Tab\*                  | Berechtigungsmodi durchlaufen          |
| `chat:modelPicker`    | Cmd+P / Meta+P               | Modell-Picker öffnen                   |
| `chat:fastMode`       | Meta+O                       | Schnellmodus umschalten                |
| `chat:thinkingToggle` | Cmd+T / Meta+T               | Erweitertes Denken umschalten          |
| `chat:submit`         | Enter                        | Nachricht senden                       |
| `chat:newline`        | (nicht gebunden)             | Zeilenumbruch einfügen, ohne zu senden |
| `chat:undo`           | Ctrl+\_, Ctrl+Shift+-        | Letzte Aktion rückgängig machen        |
| `chat:externalEditor` | Ctrl+G, Ctrl+X Ctrl+E        | In externem Editor öffnen              |
| `chat:stash`          | Ctrl+S                       | Aktuelle Eingabeaufforderung speichern |
| `chat:imagePaste`     | Ctrl+V (Alt+V unter Windows) | Bild einfügen                          |

\*Unter Windows ohne VT-Modus (Node \<24.2.0/\<22.17.0, Bun \<1.2.23) Standard auf Meta+M.

### Autovervollständigungsaktionen

Aktionen verfügbar im `Autocomplete`-Kontext:

| Aktion                  | Standard | Beschreibung          |
| :---------------------- | :------- | :-------------------- |
| `autocomplete:accept`   | Tab      | Vorschlag akzeptieren |
| `autocomplete:dismiss`  | Escape   | Menü schließen        |
| `autocomplete:previous` | Oben     | Vorheriger Vorschlag  |
| `autocomplete:next`     | Unten    | Nächster Vorschlag    |

### Bestätigungsaktionen

Aktionen verfügbar im `Confirmation`-Kontext:

| Aktion                      | Standard         | Beschreibung                      |
| :-------------------------- | :--------------- | :-------------------------------- |
| `confirm:yes`               | Y, Enter         | Aktion bestätigen                 |
| `confirm:no`                | N, Escape        | Aktion ablehnen                   |
| `confirm:previous`          | Oben             | Vorherige Option                  |
| `confirm:next`              | Unten            | Nächste Option                    |
| `confirm:nextField`         | Tab              | Nächstes Feld                     |
| `confirm:previousField`     | (nicht gebunden) | Vorheriges Feld                   |
| `confirm:toggle`            | Leertaste        | Auswahl umschalten                |
| `confirm:cycleMode`         | Shift+Tab        | Berechtigungsmodi durchlaufen     |
| `confirm:toggleExplanation` | Ctrl+E           | Berechtigungserklärung umschalten |

### Berechtigungsaktionen

Aktionen verfügbar im `Confirmation`-Kontext für Berechtigungsdialoge:

| Aktion                   | Standard | Beschreibung                        |
| :----------------------- | :------- | :---------------------------------- |
| `permission:toggleDebug` | Ctrl+D   | Berechtigungs-Debug-Info umschalten |

### Transkript-Aktionen

Aktionen verfügbar im `Transcript`-Kontext:

| Aktion                     | Standard          | Beschreibung                     |
| :------------------------- | :---------------- | :------------------------------- |
| `transcript:toggleShowAll` | Ctrl+E            | Alle Inhalte anzeigen umschalten |
| `transcript:exit`          | q, Ctrl+C, Escape | Transkript-Ansicht beenden       |

### Verlaufssuch-Aktionen

Aktionen verfügbar im `HistorySearch`-Kontext:

| Aktion                  | Standard    | Beschreibung                  |
| :---------------------- | :---------- | :---------------------------- |
| `historySearch:next`    | Ctrl+R      | Nächster Treffer              |
| `historySearch:accept`  | Escape, Tab | Auswahl akzeptieren           |
| `historySearch:cancel`  | Ctrl+C      | Suche abbrechen               |
| `historySearch:execute` | Enter       | Ausgewählten Befehl ausführen |

### Aufgaben-Aktionen

Aktionen verfügbar im `Task`-Kontext:

| Aktion            | Standard | Beschreibung                                    |
| :---------------- | :------- | :---------------------------------------------- |
| `task:background` | Ctrl+B   | Aktuelle Aufgabe in den Hintergrund verschieben |

### Design-Aktionen

Aktionen verfügbar im `ThemePicker`-Kontext:

| Aktion                           | Standard | Beschreibung                  |
| :------------------------------- | :------- | :---------------------------- |
| `theme:toggleSyntaxHighlighting` | Ctrl+T   | Syntaxhervorhebung umschalten |

### Hilfe-Aktionen

Aktionen verfügbar im `Help`-Kontext:

| Aktion         | Standard | Beschreibung        |
| :------------- | :------- | :------------------ |
| `help:dismiss` | Escape   | Hilfemenü schließen |

### Tabs-Aktionen

Aktionen verfügbar im `Tabs`-Kontext:

| Aktion          | Standard         | Beschreibung   |
| :-------------- | :--------------- | :------------- |
| `tabs:next`     | Tab, Rechts      | Nächster Tab   |
| `tabs:previous` | Shift+Tab, Links | Vorheriger Tab |

### Anhänge-Aktionen

Aktionen verfügbar im `Attachments`-Kontext:

| Aktion                 | Standard           | Beschreibung                  |
| :--------------------- | :----------------- | :---------------------------- |
| `attachments:next`     | Rechts             | Nächster Anhang               |
| `attachments:previous` | Links              | Vorheriger Anhang             |
| `attachments:remove`   | Rücktaste, Löschen | Ausgewählten Anhang entfernen |
| `attachments:exit`     | Unten, Escape      | Anhang-Navigation beenden     |

### Fußzeilen-Aktionen

Aktionen verfügbar im `Footer`-Kontext:

| Aktion                  | Standard | Beschreibung                                                 |
| :---------------------- | :------- | :----------------------------------------------------------- |
| `footer:next`           | Rechts   | Nächstes Fußzeilen-Element                                   |
| `footer:previous`       | Links    | Vorheriges Fußzeilen-Element                                 |
| `footer:up`             | Oben     | In der Fußzeile nach oben navigieren (Auswahl oben aufheben) |
| `footer:down`           | Unten    | In der Fußzeile nach unten navigieren                        |
| `footer:openSelected`   | Enter    | Ausgewähltes Fußzeilen-Element öffnen                        |
| `footer:clearSelection` | Escape   | Fußzeilen-Auswahl löschen                                    |

### Nachrichtenauswahl-Aktionen

Aktionen verfügbar im `MessageSelector`-Kontext:

| Aktion                   | Standard                                     | Beschreibung                    |
| :----------------------- | :------------------------------------------- | :------------------------------ |
| `messageSelector:up`     | Oben, K, Ctrl+P                              | In der Liste nach oben bewegen  |
| `messageSelector:down`   | Unten, J, Ctrl+N                             | In der Liste nach unten bewegen |
| `messageSelector:top`    | Ctrl+Oben, Shift+Oben, Meta+Oben, Shift+K    | Zum Anfang springen             |
| `messageSelector:bottom` | Ctrl+Unten, Shift+Unten, Meta+Unten, Shift+J | Zum Ende springen               |
| `messageSelector:select` | Enter                                        | Nachricht auswählen             |

### Diff-Aktionen

Aktionen verfügbar im `DiffDialog`-Kontext:

| Aktion                | Standard            | Beschreibung               |
| :-------------------- | :------------------ | :------------------------- |
| `diff:dismiss`        | Escape              | Diff-Viewer schließen      |
| `diff:previousSource` | Links               | Vorherige Diff-Quelle      |
| `diff:nextSource`     | Rechts              | Nächste Diff-Quelle        |
| `diff:previousFile`   | Oben                | Vorherige Datei im Diff    |
| `diff:nextFile`       | Unten               | Nächste Datei im Diff      |
| `diff:viewDetails`    | Enter               | Diff-Details anzeigen      |
| `diff:back`           | (kontextspezifisch) | Im Diff-Viewer zurückgehen |

### Modell-Picker-Aktionen

Aktionen verfügbar im `ModelPicker`-Kontext:

| Aktion                       | Standard | Beschreibung             |
| :--------------------------- | :------- | :----------------------- |
| `modelPicker:decreaseEffort` | Links    | Aufwandsstufe verringern |
| `modelPicker:increaseEffort` | Rechts   | Aufwandsstufe erhöhen    |

### Select-Aktionen

Aktionen verfügbar im `Select`-Kontext:

| Aktion            | Standard         | Beschreibung        |
| :---------------- | :--------------- | :------------------ |
| `select:next`     | Unten, J, Ctrl+N | Nächste Option      |
| `select:previous` | Oben, K, Ctrl+P  | Vorherige Option    |
| `select:accept`   | Enter            | Auswahl akzeptieren |
| `select:cancel`   | Escape           | Auswahl abbrechen   |

### Plugin-Aktionen

Aktionen verfügbar im `Plugin`-Kontext:

| Aktion           | Standard  | Beschreibung                     |
| :--------------- | :-------- | :------------------------------- |
| `plugin:toggle`  | Leertaste | Plugin-Auswahl umschalten        |
| `plugin:install` | I         | Ausgewählte Plugins installieren |

### Einstellungs-Aktionen

Aktionen verfügbar im `Settings`-Kontext:

| Aktion            | Standard | Beschreibung                                                                                    |
| :---------------- | :------- | :---------------------------------------------------------------------------------------------- |
| `settings:search` | /        | Suchmodus aktivieren                                                                            |
| `settings:retry`  | R        | Nutzungsdaten neu laden (bei Fehler)                                                            |
| `settings:close`  | Enter    | Änderungen speichern und Konfigurationspanel schließen. Escape verwirft Änderungen und schließt |

### Sprach-Aktionen

Aktionen verfügbar im `Chat`-Kontext, wenn [Sprachdiktat](/de/voice-dictation) aktiviert ist:

| Aktion             | Standard  | Beschreibung                                                  |
| :----------------- | :-------- | :------------------------------------------------------------ |
| `voice:pushToTalk` | Leertaste | Halten Sie gedrückt, um eine Eingabeaufforderung zu diktieren |

## Tastenkombinations-Syntax

### Modifizierer

Verwenden Sie Modifizierer-Tasten mit dem `+`-Trennzeichen:

* `ctrl` oder `control` - Strg-Taste
* `alt`, `opt`, oder `option` - Alt/Option-Taste
* `shift` - Umschalt-Taste
* `meta`, `cmd`, oder `command` - Meta/Befehlstaste

Beispiele:

```text  theme={null}
ctrl+k          Einzelne Taste mit Modifizierer
shift+tab       Umschalt + Tab
meta+p          Befehl/Meta + P
ctrl+shift+c    Mehrere Modifizierer
```

### Großbuchstaben

Ein eigenständiger Großbuchstabe impliziert Umschalt. Zum Beispiel ist `K` gleichbedeutend mit `shift+k`. Dies ist nützlich für Vim-ähnliche Bindings, bei denen Groß- und Kleinbuchstaben unterschiedliche Bedeutungen haben.

Großbuchstaben mit Modifizierern (z. B. `ctrl+K`) werden als stilistisch behandelt und implizieren **nicht** Umschalt: `ctrl+K` ist dasselbe wie `ctrl+k`.

### Akkorde

Akkorde sind Sequenzen von Tastenkombinationen, die durch Leerzeichen getrennt sind:

```text  theme={null}
ctrl+k ctrl+s   Drücken Sie Ctrl+K, loslassen, dann Ctrl+S
```

### Spezielle Tasten

* `escape` oder `esc` - Escape-Taste
* `enter` oder `return` - Enter-Taste
* `tab` - Tab-Taste
* `space` - Leertaste
* `up`, `down`, `left`, `right` - Pfeiltasten
* `backspace`, `delete` - Löschtasten

## Standardkürzel aufheben

Setzen Sie eine Aktion auf `null`, um ein Standardkürzel aufzuheben:

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

Dies funktioniert auch für Akkord-Bindings. Das Aufheben aller Akkorde, die ein Präfix teilen, gibt dieses Präfix für die Verwendung als Single-Key-Binding frei:

```json  theme={null}
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+x ctrl+k": null,
        "ctrl+x ctrl+e": null,
        "ctrl+x": "chat:newline"
      }
    }
  ]
}
```

Wenn Sie einige, aber nicht alle Akkorde auf einem Präfix aufheben, führt das Drücken des Präfix immer noch in den Akkord-Wartmodus für die verbleibenden Bindings ein.

## Reservierte Kürzel

Diese Kürzel können nicht neu gebunden werden:

| Kürzel | Grund                                              |
| :----- | :------------------------------------------------- |
| Ctrl+C | Hardcodierter Interrupt/Abbruch                    |
| Ctrl+D | Hardcodierter Ausstieg                             |
| Ctrl+M | Identisch mit Enter in Terminals (beide senden CR) |

## Terminal-Konflikte

Einige Kürzel können mit Terminal-Multiplexern in Konflikt geraten:

| Kürzel | Konflikt                                 |
| :----- | :--------------------------------------- |
| Ctrl+B | tmux-Präfix (zweimal drücken zum Senden) |
| Ctrl+A | GNU Screen-Präfix                        |
| Ctrl+Z | Unix-Prozess-Suspend (SIGTSTP)           |

## Vim-Modus-Interaktion

Wenn der Vim-Modus aktiviert ist (`/vim`), arbeiten Keybindings und Vim-Modus unabhängig:

* **Vim-Modus** verarbeitet Eingaben auf der Texteingangsebene (Cursor-Bewegung, Modi, Bewegungen)
* **Keybindings** verarbeiten Aktionen auf der Komponentenebene (Aufgaben umschalten, senden usw.)
* Die Escape-Taste im Vim-Modus wechselt von INSERT zu NORMAL-Modus; sie löst nicht `chat:cancel` aus
* Die meisten Ctrl+Taste-Kürzel werden durch den Vim-Modus zum Keybinding-System weitergeleitet
* Im Vim-NORMAL-Modus zeigt `?` das Hilfemenü an (Vim-Verhalten)

## Validierung

Claude Code validiert Ihre Keybindings und zeigt Warnungen für:

* Parse-Fehler (ungültiges JSON oder Struktur)
* Ungültige Kontextnamen
* Reservierte Kürzel-Konflikte
* Terminal-Multiplexer-Konflikte
* Doppelte Bindings im selben Kontext

Führen Sie `/doctor` aus, um Keybinding-Warnungen anzuzeigen.
