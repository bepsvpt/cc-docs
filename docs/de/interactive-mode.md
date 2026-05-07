> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Interaktiver Modus

> Vollständige Referenz für Tastaturkürzel, Eingabemodi und interaktive Funktionen in Claude Code-Sitzungen.

## Tastaturkürzel

<Note>
  Tastaturkürzel können je nach Plattform und Terminal variieren. Drücken Sie `?`, um die verfügbaren Kürzel für Ihre Umgebung anzuzeigen.

  **macOS-Benutzer**: Option/Alt-Tastenkürzel (`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`) erfordern die Konfiguration von Option als Meta in Ihrem Terminal:

  * **iTerm2**: Einstellungen → Profile → Keys → General → Left/Right Option key auf „Esc+" setzen
  * **Apple Terminal**: Einstellungen → Profile → Keyboard → „Use Option as Meta Key" aktivieren
  * **VS Code**: `"terminal.integrated.macOptionIsMeta": true` in VS Code-Einstellungen setzen

  Weitere Informationen finden Sie unter [Terminal-Konfiguration](/de/terminal-config).
</Note>

### Allgemeine Steuerelemente

| Kürzel                                                | Beschreibung                                                                                 | Kontext                                                                                                                                                                                                                                                                                                                                                  |
| :---------------------------------------------------- | :------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+C`                                              | Aktuelle Eingabe oder Generierung abbrechen                                                  | Standard-Interrupt                                                                                                                                                                                                                                                                                                                                       |
| `Ctrl+X Ctrl+K`                                       | Alle Hintergrund-Agenten beenden. Zweimal innerhalb von 3 Sekunden drücken, um zu bestätigen | Steuerung von Hintergrund-Agenten                                                                                                                                                                                                                                                                                                                        |
| `Ctrl+D`                                              | Claude Code-Sitzung beenden                                                                  | EOF-Signal                                                                                                                                                                                                                                                                                                                                               |
| `Ctrl+G` oder `Ctrl+X Ctrl+E`                         | Im Standard-Texteditor öffnen                                                                | Bearbeiten Sie Ihren Prompt oder benutzerdefinierte Antwort in Ihrem Standard-Texteditor. `Ctrl+X Ctrl+E` ist die readline-native Bindung. Aktivieren Sie „Show last response in external editor" in `/config`, um Claudes vorherige Antwort als `#`-kommentierter Kontext über Ihrem Prompt einzufügen; der Kommentarblock wird beim Speichern entfernt |
| `Ctrl+L`                                              | Bildschirm neu zeichnen                                                                      | Erzwingt eine vollständige Terminal-Neuzeichnung. Eingabe und Gesprächsverlauf werden beibehalten. Verwenden Sie dies, um die Anzeige wiederherzustellen, wenn sie verzerrt oder teilweise leer wird                                                                                                                                                     |
| `Ctrl+O`                                              | Transkript-Viewer umschalten                                                                 | Zeigt detaillierte Tool-Nutzung und Ausführung. Erweitert auch MCP-Aufrufe, die standardmäßig zu einer einzelnen Zeile wie „Called slack 3 times" zusammengefasst werden                                                                                                                                                                                 |
| `Ctrl+R`                                              | Reverse-Suche im Befehlsverlauf                                                              | Durchsuchen Sie vorherige Befehle interaktiv                                                                                                                                                                                                                                                                                                             |
| `Ctrl+V` oder `Cmd+V` (iTerm2) oder `Alt+V` (Windows) | Bild aus Zwischenablage einfügen                                                             | Fügt einen `[Image #N]`-Chip an der Cursor-Position ein, sodass Sie ihn positionell in Ihrem Prompt referenzieren können                                                                                                                                                                                                                                 |
| `Ctrl+B`                                              | Hintergrund-Ausführung von Aufgaben                                                          | Führt Bash-Befehle und Agenten im Hintergrund aus. Tmux-Benutzer drücken zweimal                                                                                                                                                                                                                                                                         |
| `Ctrl+T`                                              | Task-Liste umschalten                                                                        | Zeigen oder verbergen Sie die [Task-Liste](#task-list) im Terminal-Statusbereich                                                                                                                                                                                                                                                                         |
| `Left/Right arrows`                                   | Durch Dialog-Registerkarten navigieren                                                       | Navigieren Sie zwischen Registerkarten in Berechtigungsdialogen und Menüs                                                                                                                                                                                                                                                                                |
| `Up/Down arrows` oder `Ctrl+P`/`Ctrl+N`               | Cursor bewegen oder Befehlsverlauf navigieren                                                | Bei mehrzeiliger Eingabe bewegt sich der Cursor zunächst innerhalb der Eingabeaufforderung. Sobald sich der Cursor bereits am oberen oder unteren Rand befindet, navigiert das erneute Drücken durch den Befehlsverlauf                                                                                                                                  |
| `Esc` + `Esc`                                         | Zurückspulen oder zusammenfassen                                                             | Stellen Sie Code und/oder Gespräch auf einen vorherigen Punkt wieder her, oder fassen Sie ab einer ausgewählten Nachricht zusammen                                                                                                                                                                                                                       |
| `Shift+Tab` oder `Alt+M` (einige Konfigurationen)     | Berechtigungsmodi umschalten                                                                 | Wechseln Sie zwischen `default`, `acceptEdits`, `plan` und allen Modi, die Sie aktiviert haben, z. B. `auto` oder `bypassPermissions`. Siehe [Berechtigungsmodi](/de/permission-modes).                                                                                                                                                                  |
| `Option+P` (macOS) oder `Alt+P` (Windows/Linux)       | Modell wechseln                                                                              | Wechseln Sie Modelle, ohne Ihren Prompt zu löschen                                                                                                                                                                                                                                                                                                       |
| `Option+T` (macOS) oder `Alt+T` (Windows/Linux)       | Extended Thinking umschalten                                                                 | Aktivieren oder deaktivieren Sie den Extended Thinking-Modus. {/* min-version: 2.1.132 */}Ab v2.1.132 funktioniert dieses Kürzel auf macOS ohne Konfiguration von Option als Meta                                                                                                                                                                        |
| `Option+O` (macOS) oder `Alt+O` (Windows/Linux)       | Schnellmodus umschalten                                                                      | Aktivieren oder deaktivieren Sie den [Schnellmodus](/de/fast-mode)                                                                                                                                                                                                                                                                                       |

### Textbearbeitung

| Kürzel                  | Beschreibung                                     | Kontext                                                                                                                                                                                                                  |
| :---------------------- | :----------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+A`                | Cursor an den Anfang der aktuellen Zeile bewegen | Bei mehrzeiliger Eingabe bewegt sich der Cursor an den Anfang der aktuellen logischen Zeile                                                                                                                              |
| `Ctrl+E`                | Cursor an das Ende der aktuellen Zeile bewegen   | Bei mehrzeiliger Eingabe bewegt sich der Cursor an das Ende der aktuellen logischen Zeile                                                                                                                                |
| `Ctrl+K`                | Bis zum Ende der Zeile löschen                   | Speichert gelöschten Text zum Einfügen                                                                                                                                                                                   |
| `Ctrl+U`                | Vom Cursor bis zum Zeilenanfang löschen          | Speichert gelöschten Text zum Einfügen. Wiederholen Sie, um über Zeilen in mehrzeiliger Eingabe zu löschen. Auf macOS ordnen Terminal-Emulatoren einschließlich iTerm2 und Terminal.app `Cmd+Backspace` diesem Kürzel zu |
| `Ctrl+W`                | Vorheriges Wort löschen                          | Speichert gelöschten Text zum Einfügen. Unter Windows löscht `Ctrl+Backspace` auch das vorherige Wort                                                                                                                    |
| `Ctrl+Y`                | Gelöschten Text einfügen                         | Fügen Sie Text ein, der mit `Ctrl+K`, `Ctrl+U` oder `Ctrl+W` gelöscht wurde                                                                                                                                              |
| `Alt+Y` (nach `Ctrl+Y`) | Einfügeverlauf durchlaufen                       | Nach dem Einfügen können Sie durch zuvor gelöschten Text navigieren. Erfordert [Option als Meta](#keyboard-shortcuts) auf macOS                                                                                          |
| `Alt+B`                 | Cursor um ein Wort nach hinten bewegen           | Wort-Navigation. Erfordert [Option als Meta](#keyboard-shortcuts) auf macOS                                                                                                                                              |
| `Alt+F`                 | Cursor um ein Wort nach vorne bewegen            | Wort-Navigation. Erfordert [Option als Meta](#keyboard-shortcuts) auf macOS                                                                                                                                              |

### Design und Anzeige

| Kürzel   | Beschreibung                                   | Kontext                                                                                                  |
| :------- | :--------------------------------------------- | :------------------------------------------------------------------------------------------------------- |
| `Ctrl+T` | Syntax-Hervorhebung für Code-Blöcke umschalten | Funktioniert nur im `/theme`-Auswahlmenü. Steuert, ob Code in Claudes Antworten Syntax-Färbung verwendet |

### Mehrzeilige Eingabe

| Methode          | Kürzel          | Kontext                                                                                                    |
| :--------------- | :-------------- | :--------------------------------------------------------------------------------------------------------- |
| Schneller Escape | `\` + `Enter`   | Funktioniert in allen Terminals                                                                            |
| Option-Taste     | `Option+Enter`  | Nach Aktivierung von [Option als Meta](/de/terminal-config#enable-option-key-shortcuts-on-macos) auf macOS |
| Shift+Enter      | `Shift+Enter`   | Nativ in iTerm2, WezTerm, Ghostty, Kitty, Warp, Apple Terminal, Windows Terminal                           |
| Steuersequenz    | `Ctrl+J`        | Funktioniert in jedem Terminal ohne Konfiguration                                                          |
| Einfügemodus     | Direkt einfügen | Für Code-Blöcke, Protokolle                                                                                |

<Tip>
  Shift+Enter funktioniert ohne Konfiguration in iTerm2, WezTerm, Ghostty, Kitty, Warp, Apple Terminal und Windows Terminal. Für VS Code, Cursor, Windsurf, Alacritty und Zed führen Sie `/terminal-setup` aus, um die Bindung zu installieren.
</Tip>

### Schnellbefehle

| Kürzel        | Beschreibung        | Notizen                                                                              |
| :------------ | :------------------ | :----------------------------------------------------------------------------------- |
| `/` am Anfang | Befehl oder Skill   | Siehe [Befehle](#commands) und [Skills](/de/skills)                                  |
| `!` am Anfang | Shell-Modus         | Führen Sie Befehle direkt aus und fügen Sie die Ausführungsausgabe zur Sitzung hinzu |
| `@`           | Dateipfad-Erwähnung | Trigger für Dateipfad-Autovervollständigung                                          |

### Transkript-Viewer

Wenn der Transkript-Viewer offen ist (umgeschaltet mit `Ctrl+O`), sind diese Kürzel verfügbar. `Ctrl+E` kann über [`transcript:toggleShowAll`](/de/keybindings) neu zugewiesen werden.

| Kürzel               | Beschreibung                                                                                                                                                                                                                                        |
| :------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+E`             | Alle Inhalte anzeigen umschalten                                                                                                                                                                                                                    |
| `[`                  | Schreiben Sie das vollständige Gespräch in den nativen Scrollback Ihres Terminals, sodass `Cmd+F`, tmux-Kopiermodus und andere native Tools es durchsuchen können. Erfordert [Vollbildrendering](/de/fullscreen#search-and-review-the-conversation) |
| `v`                  | Schreiben Sie das Gespräch in eine temporäre Datei und öffnen Sie es in `$VISUAL` oder `$EDITOR`. Erfordert [Vollbildrendering](/de/fullscreen)                                                                                                     |
| `q`, `Ctrl+C`, `Esc` | Transkript-Ansicht beenden. Alle drei können über [`transcript:exit`](/de/keybindings) neu zugewiesen werden                                                                                                                                        |

### Spracheingabe

| Kürzel                     | Beschreibung     | Notizen                                                                                                                                                                                                                          |
| :------------------------- | :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `Space` halten oder tippen | Sprach-Diktieren | Erfordert, dass [Sprach-Diktieren](/de/voice-dictation) aktiviert ist. Halten Sie gedrückt zum Aufnehmen, oder führen Sie `/voice tap` aus für Tap-zum-Umschalten. [Neu zuweisbar](/de/voice-dictation#rebind-the-dictation-key) |

## Befehle

Geben Sie `/` in Claude Code ein, um alle verfügbaren Befehle anzuzeigen, oder geben Sie `/` gefolgt von beliebigen Buchstaben ein, um zu filtern. Das `/`-Menü zeigt alles, was Sie aufrufen können: integrierte Befehle, gebündelte und von Benutzern erstellte [Skills](/de/skills) sowie Befehle, die von [Plugins](/de/plugins) und [MCP-Servern](/de/mcp#use-mcp-prompts-as-commands) beigetragen werden. Nicht alle integrierten Befehle sind für jeden Benutzer sichtbar, da einige von Ihrer Plattform oder Ihrem Plan abhängen.

Siehe die [Befehls-Referenz](/de/commands) für die vollständige Liste der in Claude Code enthaltenen Befehle.

## Vim-Editor-Modus

Aktivieren Sie Vim-ähnliche Bearbeitung über `/config` → Editor mode.

### Modusumschaltung

| Befehl | Aktion                                | Aus Modus      |
| :----- | :------------------------------------ | :------------- |
| `Esc`  | NORMAL-Modus eingeben                 | INSERT, VISUAL |
| `i`    | Vor Cursor einfügen                   | NORMAL         |
| `I`    | Am Anfang der Zeile einfügen          | NORMAL         |
| `a`    | Nach Cursor einfügen                  | NORMAL         |
| `A`    | Am Ende der Zeile einfügen            | NORMAL         |
| `o`    | Zeile unten öffnen                    | NORMAL         |
| `O`    | Zeile oben öffnen                     | NORMAL         |
| `v`    | Zeichenweise visuelle Auswahl starten | NORMAL         |
| `V`    | Zeilenweise visuelle Auswahl starten  | NORMAL         |

### Navigation (NORMAL-Modus)

| Befehl          | Aktion                                                         |
| :-------------- | :------------------------------------------------------------- |
| `h`/`j`/`k`/`l` | Nach links/unten/oben/rechts bewegen                           |
| `Space`         | Nach rechts bewegen                                            |
| `w`             | Nächstes Wort                                                  |
| `e`             | Ende des Wortes                                                |
| `b`             | Vorheriges Wort                                                |
| `0`             | Anfang der Zeile                                               |
| `$`             | Ende der Zeile                                                 |
| `^`             | Erstes Nicht-Leerzeichen-Zeichen                               |
| `gg`            | Anfang der Eingabe                                             |
| `G`             | Ende der Eingabe                                               |
| `f{char}`       | Zum nächsten Vorkommen des Zeichens springen                   |
| `F{char}`       | Zum vorherigen Vorkommen des Zeichens springen                 |
| `t{char}`       | Direkt vor das nächste Vorkommen des Zeichens springen         |
| `T{char}`       | Direkt nach das vorherige Vorkommen des Zeichens springen      |
| `;`             | Letzte f/F/t/T-Bewegung wiederholen                            |
| `,`             | Letzte f/F/t/T-Bewegung in umgekehrter Reihenfolge wiederholen |

<Note>
  Im Vim-Normal-Modus navigieren `j`/`k` und die Pfeiltasten den Befehlsverlauf, wenn sich der Cursor am Anfang oder Ende der Eingabe befindet und nicht weiter bewegt werden kann.
</Note>

### Bearbeitung (NORMAL-Modus)

| Befehl         | Aktion                         |
| :------------- | :----------------------------- |
| `x`            | Zeichen löschen                |
| `dd`           | Zeile löschen                  |
| `D`            | Bis zum Ende der Zeile löschen |
| `dw`/`de`/`db` | Wort löschen/bis Ende/zurück   |
| `cc`           | Zeile ändern                   |
| `C`            | Bis zum Ende der Zeile ändern  |
| `cw`/`ce`/`cb` | Wort ändern/bis Ende/zurück    |
| `yy`/`Y`       | Zeile yanken (kopieren)        |
| `yw`/`ye`/`yb` | Wort yanken/bis Ende/zurück    |
| `p`            | Nach Cursor einfügen           |
| `P`            | Vor Cursor einfügen            |
| `>>`           | Zeile einrücken                |
| `<<`           | Zeile ausrücken                |
| `J`            | Zeilen verbinden               |
| `u`            | Rückgängig machen              |
| `.`            | Letzte Änderung wiederholen    |

### Textobjekte (NORMAL-Modus)

Textobjekte funktionieren mit Operatoren wie `d`, `c` und `y`:

| Befehl    | Aktion                                 |
| :-------- | :------------------------------------- |
| `iw`/`aw` | Inneres/um Wort                        |
| `iW`/`aW` | Inneres/um WORT (Leerzeichen-begrenzt) |
| `i"`/`a"` | Inneres/um doppelte Anführungszeichen  |
| `i'`/`a'` | Inneres/um einfache Anführungszeichen  |
| `i(`/`a(` | Inneres/um Klammern                    |
| `i[`/`a[` | Inneres/um eckige Klammern             |
| `i{`/`a{` | Inneres/um geschweifte Klammern        |

### Visueller Modus

Drücken Sie `v` für zeichenweise Auswahl oder `V` für zeilenweise Auswahl. Bewegungen erweitern die Auswahl, und Operatoren wirken direkt darauf.

| Befehl           | Aktion                                                        |
| :--------------- | :------------------------------------------------------------ |
| `d`/`x`          | Auswahl löschen                                               |
| `y`              | Auswahl yanken                                                |
| `c`/`s`          | Auswahl ändern                                                |
| `p`              | Auswahl durch Registerinhalt ersetzen                         |
| `r{char}`        | Jedes ausgewählte Zeichen durch `{char}` ersetzen             |
| `~`/`u`/`U`      | Auswahl umschalten, Kleinbuchstaben oder Großbuchstaben       |
| `>`/`<`          | Ausgewählte Zeilen einrücken oder ausrücken                   |
| `J`              | Ausgewählte Zeilen verbinden                                  |
| `o`              | Cursor und Anker tauschen                                     |
| `iw`/`aw`/`i"`/… | Ein Textobjekt auswählen                                      |
| `v`/`V`          | Zwischen zeichenweise und zeilenweise umschalten oder beenden |

Der blockweise visuelle Modus mit `Ctrl+V` wird nicht unterstützt.

## Befehlsverlauf

Claude Code verwaltet den Befehlsverlauf für die aktuelle Sitzung:

* Der Eingabeverlauf wird pro Arbeitsverzeichnis gespeichert
* Der Eingabeverlauf wird zurückgesetzt, wenn Sie `/clear` ausführen, um eine neue Sitzung zu starten. Das Gespräch der vorherigen Sitzung wird beibehalten und kann fortgesetzt werden.
* Verwenden Sie die Pfeiltasten nach oben/unten zum Navigieren (siehe Tastaturkürzel oben)
* **Hinweis**: Verlaufserweiterung (`!`) ist standardmäßig deaktiviert

### Reverse-Suche mit Ctrl+R

Drücken Sie `Ctrl+R`, um interaktiv durch Ihren Befehlsverlauf zu suchen:

1. **Suche starten**: Drücken Sie `Ctrl+R`, um die Reverse-Verlaufssuche zu aktivieren
2. **Abfrage eingeben**: Geben Sie Text ein, um in vorherigen Befehlen zu suchen. Der Suchbegriff wird in übereinstimmenden Ergebnissen hervorgehoben
3. **Übereinstimmungen navigieren**: Drücken Sie `Ctrl+R` erneut, um durch ältere Übereinstimmungen zu navigieren
4. **Bereich ändern**: Die Suche bezieht sich standardmäßig auf Eingabeaufforderungen aus allen Projekten. Drücken Sie `Ctrl+S`, um den Bereich durch diese Sitzung, dieses Projekt und alle Projekte zu durchlaufen
5. **Übereinstimmung akzeptieren**:
   * Drücken Sie `Tab` oder `Esc`, um die aktuelle Übereinstimmung zu akzeptieren und die Bearbeitung fortzusetzen
   * Drücken Sie `Enter`, um die Übereinstimmung zu akzeptieren und den Befehl sofort auszuführen
6. **Suche abbrechen**:
   * Drücken Sie `Ctrl+C`, um abzubrechen und Ihre ursprüngliche Eingabe wiederherzustellen
   * Drücken Sie `Backspace` bei leerer Suche, um abzubrechen

Die Suche zeigt übereinstimmende Befehle mit dem hervorgehobenen Suchbegriff an, sodass Sie vorherige Eingaben finden und wiederverwenden können.

## Bash-Befehle im Hintergrund

Claude Code unterstützt die Ausführung von Bash-Befehlen im Hintergrund, sodass Sie weiterarbeiten können, während lange laufende Prozesse ausgeführt werden.

### Wie Hintergrund-Ausführung funktioniert

Wenn Claude Code einen Befehl im Hintergrund ausführt, führt es den Befehl asynchron aus und gibt sofort eine Hintergrund-Task-ID zurück. Claude Code kann auf neue Prompts reagieren, während der Befehl weiterhin im Hintergrund ausgeführt wird.

Um Befehle im Hintergrund auszuführen, können Sie entweder:

* Claude Code auffordern, einen Befehl im Hintergrund auszuführen
* Drücken Sie Ctrl+B, um eine reguläre Bash-Tool-Invokation in den Hintergrund zu verschieben. (Tmux-Benutzer müssen Ctrl+B zweimal drücken, da Tmux einen Präfix-Schlüssel hat.)

**Wichtige Funktionen:**

* Die Ausgabe wird in eine Datei geschrieben und Claude kann sie mit dem Read-Tool abrufen
* Hintergrund-Tasks haben eindeutige IDs zum Tracking und zur Ausgabebeschaffung
* Hintergrund-Tasks werden automatisch bereinigt, wenn Claude Code beendet wird
* Hintergrund-Tasks werden automatisch beendet, wenn die Ausgabe 5 GB überschreitet, mit einem Hinweis in stderr, der erklärt, warum

Um alle Hintergrund-Task-Funktionen zu deaktivieren, setzen Sie die Umgebungsvariable `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` auf `1`. Siehe [Umgebungsvariablen](/de/env-vars) für Details.

**Häufig im Hintergrund ausgeführte Befehle:**

* Build-Tools (webpack, vite, make)
* Paketmanager (npm, yarn, pnpm)
* Test-Runner (jest, pytest)
* Entwicklungsserver
* Lange laufende Prozesse (docker, terraform)

### Bash-Modus mit `!`-Präfix

Führen Sie Bash-Befehle direkt aus, ohne Claude zu durchlaufen, indem Sie Ihre Eingabe mit `!` präfixieren:

```bash theme={null}
! npm test
! git status
! ls -la
```

Bash-Modus:

* Fügt den Befehl und seine Ausgabe zum Gesprächskontext hinzu
* Zeigt Echtzeit-Fortschritt und Ausgabe
* Unterstützt die gleiche `Ctrl+B`-Hintergrund-Ausführung für lange laufende Befehle
* Erfordert nicht, dass Claude den Befehl interpretiert oder genehmigt
* Unterstützt verlaufsbasierte Autovervollständigung: Geben Sie einen Teilbefehl ein und drücken Sie **Tab**, um aus vorherigen `!`-Befehlen im aktuellen Projekt zu vervollständigen
* Beenden Sie mit `Escape`, `Backspace` oder `Ctrl+U` bei einer leeren Eingabeaufforderung
* Das Einfügen von Text, der mit `!` beginnt, in eine leere Eingabeaufforderung aktiviert automatisch den Bash-Modus und entspricht dem eingegebenen `!`-Verhalten

Dies ist nützlich für schnelle Shell-Operationen bei Beibehaltung des Gesprächskontexts.

## Prompt-Vorschläge

Wenn Sie eine Sitzung zum ersten Mal öffnen, wird ein ausgegrautes Beispiel-Befehl in der Eingabeaufforderung angezeigt, um Ihnen den Einstieg zu erleichtern. Claude Code wählt dies aus dem Git-Verlauf Ihres Projekts aus, sodass es die Dateien widerspiegelt, an denen Sie kürzlich gearbeitet haben.

Nachdem Claude antwortet, werden weiterhin Vorschläge basierend auf Ihrem Gesprächsverlauf angezeigt, z. B. ein Folgenschritt aus einer mehrteiligen Anfrage oder eine natürliche Fortsetzung Ihres Workflows.

* Drücken Sie **Tab** oder **Rechts-Pfeil**, um den Vorschlag zu akzeptieren, oder drücken Sie **Enter**, um zu akzeptieren und einzureichen
* Beginnen Sie zu tippen, um ihn zu verwerfen

Der Vorschlag wird als Hintergrund-Anfrage ausgeführt, die den Prompt-Cache des übergeordneten Gesprächs wiederverwenden, sodass die zusätzlichen Kosten minimal sind. Claude Code überspringt die Vorschlagsgenerierung, wenn der Cache kalt ist, um unnötige Kosten zu vermeiden.

Vorschläge werden automatisch nach dem ersten Turn eines Gesprächs, im nicht-interaktiven Modus und im Plan-Modus übersprungen.

Um Prompt-Vorschläge vollständig zu deaktivieren, setzen Sie die Umgebungsvariable oder schalten Sie die Einstellung in `/config` um:

```bash theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## Nebenfragen mit /btw

Verwenden Sie `/btw`, um eine schnelle Frage zu Ihrer aktuellen Arbeit zu stellen, ohne sie zum Gesprächsverlauf hinzuzufügen. Dies ist nützlich, wenn Sie eine schnelle Antwort möchten, aber nicht den Hauptkontext unordentlich machen oder Claude von einer lange laufenden Aufgabe ablenken möchten.

```
/btw what was the name of that config file again?
```

Nebenfragen haben vollständige Sichtbarkeit des aktuellen Gesprächs, sodass Sie Fragen zu Code stellen können, den Claude bereits gelesen hat, Entscheidungen, die es früher getroffen hat, oder alles andere aus der Sitzung. Die Frage und Antwort sind flüchtig: Sie erscheinen in einer verwerfbaren Überlagerung und gelangen niemals in den Gesprächsverlauf.

* **Verfügbar während Claude arbeitet**: Sie können `/btw` auch ausführen, während Claude eine Antwort verarbeitet. Die Nebenfrage wird unabhängig ausgeführt und unterbricht den Hauptturn nicht.
* **Kein Tool-Zugriff**: Nebenfragen beantworten nur aus dem, was bereits im Kontext ist. Claude kann keine Dateien lesen, Befehle ausführen oder suchen, wenn eine Nebenfrage beantwortet wird.
* **Einzelne Antwort**: Es gibt keine Folgeversuche. Wenn Sie einen Hin- und Herwechsel benötigen, verwenden Sie stattdessen einen normalen Prompt.
* **Niedrige Kosten**: Die Nebenfrage verwendet den Prompt-Cache des übergeordneten Gesprächs wieder, sodass die zusätzlichen Kosten minimal sind.

Drücken Sie **Space**, **Enter** oder **Escape**, um die Antwort zu verwerfen und zur Eingabeaufforderung zurückzukehren.

`/btw` ist das Gegenteil eines [Subagenten](/de/sub-agents): Es sieht Ihr vollständiges Gespräch, hat aber keine Tools, während ein Subagent vollständige Tools hat, aber mit einem leeren Kontext beginnt. Verwenden Sie `/btw`, um zu fragen, was Claude bereits aus dieser Sitzung weiß; verwenden Sie einen Subagenten, um etwas Neues herauszufinden.

## Task-Liste

Bei der Arbeit an komplexen, mehrstufigen Aufgaben erstellt Claude eine Task-Liste, um den Fortschritt zu verfolgen. Tasks erscheinen im Statusbereich Ihres Terminals mit Indikatoren, die zeigen, was ausstehend, in Bearbeitung oder abgeschlossen ist.

* Drücken Sie `Ctrl+T`, um die Task-Listen-Ansicht umzuschalten. Die Anzeige zeigt bis zu 5 Tasks gleichzeitig
* Um alle Tasks anzuzeigen oder zu löschen, fragen Sie Claude direkt: "show me all tasks" oder "clear all tasks"
* Tasks bleiben über Kontext-Kompaktionen hinweg bestehen und helfen Claude, bei größeren Projekten organisiert zu bleiben
* Um eine Task-Liste über Sitzungen hinweg zu teilen, setzen Sie `CLAUDE_CODE_TASK_LIST_ID`, um ein benanntes Verzeichnis in `~/.claude/tasks/` zu verwenden: `CLAUDE_CODE_TASK_LIST_ID=my-project claude`

## Sitzungs-Zusammenfassung

Wenn Sie zum Terminal zurückkehren, nachdem Sie sich entfernt haben, zeigt Claude Code eine einzeilige Zusammenfassung dessen an, was bisher in der Sitzung passiert ist. Die Zusammenfassung wird im Hintergrund generiert, sobald mindestens drei Minuten seit dem letzten abgeschlossenen Turn vergangen sind und das Terminal nicht fokussiert ist, sodass sie bereit ist, wenn Sie zurückwechseln. Zusammenfassungen erscheinen nur, wenn die Sitzung mindestens drei Turns hat, und nie zweimal hintereinander.

Führen Sie `/recap` aus, um eine Zusammenfassung auf Anfrage zu generieren. Um automatische Zusammenfassungen auszuschalten, öffnen Sie `/config` und deaktivieren Sie **Session recap**.

Die Sitzungs-Zusammenfassung ist standardmäßig für jeden Plan und Provider aktiviert. Die Zusammenfassung wird im nicht-interaktiven Modus immer übersprungen.

## PR-Review-Status

Bei der Arbeit an einem Branch mit einem offenen Pull Request zeigt Claude Code einen anklickbaren PR-Link in der Fußzeile an (z. B. „PR #446"). Der Link hat eine farbige Unterstreichung, die den Review-Status anzeigt:

* Grün: genehmigt
* Gelb: Review ausstehend
* Rot: Änderungen angefordert
* Grau: Entwurf
* Lila: zusammengeführt

`Cmd+click` (Mac) oder `Ctrl+click` (Windows/Linux) auf den Link, um den Pull Request in Ihrem Browser zu öffnen. Der Status wird automatisch alle 60 Sekunden aktualisiert.

<Note>
  Der PR-Status erfordert, dass die `gh` CLI installiert und authentifiziert ist (`gh auth login`).
</Note>

## Siehe auch

* [Skills](/de/skills) - Benutzerdefinierte Prompts und Workflows
* [Checkpointing](/de/checkpointing) - Spulen Sie Claudes Änderungen zurück und stellen Sie vorherige Zustände wieder her
* [CLI-Referenz](/de/cli-reference) - Befehlszeilenflags und Optionen
* [Einstellungen](/de/settings) - Konfigurationsoptionen
* [Speicherverwaltung](/de/memory) - Verwalten von CLAUDE.md-Dateien
