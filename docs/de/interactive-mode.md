> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Interaktiver Modus

> Vollständige Referenz für Tastaturkürzel, Eingabemodi und interaktive Funktionen in Claude Code-Sitzungen.

## Tastaturkürzel

<Note>
  Tastaturkürzel können je nach Plattform und Terminal variieren. Drücken Sie `?`, um die verfügbaren Kürzel für Ihre Umgebung anzuzeigen.

  **macOS-Benutzer**: Option/Alt-Tastenkürzel (`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`) erfordern die Konfiguration von Option als Meta in Ihrem Terminal:

  * **iTerm2**: Einstellungen → Profile → Keys → Left/Right Option key auf „Esc+" setzen
  * **Terminal.app**: Einstellungen → Profile → Keyboard → „Use Option as Meta Key" aktivieren
  * **VS Code**: Einstellungen → Profile → Keys → Left/Right Option key auf „Esc+" setzen

  Weitere Informationen finden Sie unter [Terminal-Konfiguration](/de/terminal-config).
</Note>

### Allgemeine Steuerelemente

| Tastaturkürzel                                        | Beschreibung                                                                                 | Kontext                                                                                                                                       |
| :---------------------------------------------------- | :------------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+C`                                              | Aktuelle Eingabe oder Generierung abbrechen                                                  | Standard-Interrupt                                                                                                                            |
| `Ctrl+F`                                              | Alle Hintergrund-Agenten beenden. Zweimal innerhalb von 3 Sekunden drücken, um zu bestätigen | Steuerung von Hintergrund-Agenten                                                                                                             |
| `Ctrl+D`                                              | Claude Code-Sitzung beenden                                                                  | EOF-Signal                                                                                                                                    |
| `Ctrl+G`                                              | Im Standard-Texteditor öffnen                                                                | Bearbeiten Sie Ihren Prompt oder benutzerdefinierte Antwort in Ihrem Standard-Texteditor                                                      |
| `Ctrl+L`                                              | Terminal-Bildschirm löschen                                                                  | Behält Gesprächsverlauf bei                                                                                                                   |
| `Ctrl+O`                                              | Ausführliche Ausgabe umschalten                                                              | Zeigt detaillierte Tool-Nutzung und Ausführung                                                                                                |
| `Ctrl+R`                                              | Reverse-Suche im Befehlsverlauf                                                              | Durchsuchen Sie vorherige Befehle interaktiv                                                                                                  |
| `Ctrl+V` oder `Cmd+V` (iTerm2) oder `Alt+V` (Windows) | Bild aus Zwischenablage einfügen                                                             | Fügt ein Bild oder einen Pfad zu einer Bilddatei ein                                                                                          |
| `Ctrl+B`                                              | Hintergrund-Ausführung von Aufgaben                                                          | Führt Bash-Befehle und Agenten im Hintergrund aus. Tmux-Benutzer drücken zweimal                                                              |
| `Ctrl+T`                                              | Task-Liste umschalten                                                                        | Zeigen oder verbergen Sie die [Task-Liste](#task-list) im Terminal-Statusbereich                                                              |
| `Left/Right arrows`                                   | Durch Dialog-Registerkarten navigieren                                                       | Navigieren Sie zwischen Registerkarten in Berechtigungsdialogen und Menüs                                                                     |
| `Up/Down arrows`                                      | Befehlsverlauf navigieren                                                                    | Rufen Sie vorherige Eingaben ab                                                                                                               |
| `Esc` + `Esc`                                         | Zurückspulen oder zusammenfassen                                                             | Stellen Sie Code und/oder Konversation auf einen vorherigen Punkt wieder her, oder fassen Sie ab einer ausgewählten Nachricht zusammen        |
| `Shift+Tab` oder `Alt+M` (einige Konfigurationen)     | Berechtigungsmodi umschalten                                                                 | Wechseln Sie zwischen Auto-Accept Mode, Plan Mode und normalem Modus.                                                                         |
| `Option+P` (macOS) oder `Alt+P` (Windows/Linux)       | Modell wechseln                                                                              | Wechseln Sie Modelle, ohne Ihren Prompt zu löschen                                                                                            |
| `Option+T` (macOS) oder `Alt+T` (Windows/Linux)       | Extended Thinking umschalten                                                                 | Aktivieren oder deaktivieren Sie den Extended Thinking-Modus. Führen Sie zuerst `/terminal-setup` aus, um dieses Tastaturkürzel zu aktivieren |

### Textbearbeitung

| Tastaturkürzel          | Beschreibung                           | Kontext                                                                                                                    |
| :---------------------- | :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+K`                | Bis zum Zeilenende löschen             | Speichert gelöschten Text zum Einfügen                                                                                     |
| `Ctrl+U`                | Ganze Zeile löschen                    | Speichert gelöschten Text zum Einfügen                                                                                     |
| `Ctrl+Y`                | Gelöschten Text einfügen               | Fügen Sie Text ein, der mit `Ctrl+K` oder `Ctrl+U` gelöscht wurde                                                          |
| `Alt+Y` (nach `Ctrl+Y`) | Einfügen-Verlauf durchlaufen           | Nach dem Einfügen können Sie zuvor gelöschten Text durchlaufen. Erfordert [Option als Meta](#keyboard-shortcuts) auf macOS |
| `Alt+B`                 | Cursor um ein Wort nach hinten bewegen | Wort-Navigation. Erfordert [Option als Meta](#keyboard-shortcuts) auf macOS                                                |
| `Alt+F`                 | Cursor um ein Wort nach vorne bewegen  | Wort-Navigation. Erfordert [Option als Meta](#keyboard-shortcuts) auf macOS                                                |

### Design und Anzeige

| Tastaturkürzel | Beschreibung                                   | Kontext                                                                                                  |
| :------------- | :--------------------------------------------- | :------------------------------------------------------------------------------------------------------- |
| `Ctrl+T`       | Syntax-Hervorhebung für Code-Blöcke umschalten | Funktioniert nur im `/theme`-Auswahlmenü. Steuert, ob Code in Claudes Antworten Syntax-Färbung verwendet |

<Note>
  Syntax-Hervorhebung ist nur in der nativen Version von Claude Code verfügbar.
</Note>

### Mehrzeilige Eingabe

| Methode          | Tastaturkürzel  | Kontext                                                       |
| :--------------- | :-------------- | :------------------------------------------------------------ |
| Schneller Escape | `\` + `Enter`   | Funktioniert in allen Terminals                               |
| macOS Standard   | `Option+Enter`  | Standard auf macOS                                            |
| Shift+Enter      | `Shift+Enter`   | Funktioniert standardmäßig in iTerm2, WezTerm, Ghostty, Kitty |
| Steuersequenz    | `Ctrl+J`        | Zeilenumbruch-Zeichen für mehrzeilig                          |
| Einfügemodus     | Direkt einfügen | Für Code-Blöcke, Protokolle                                   |

<Tip>
  Shift+Enter funktioniert ohne Konfiguration in iTerm2, WezTerm, Ghostty und Kitty. Für andere Terminals (VS Code, Alacritty, Zed, Warp) führen Sie `/terminal-setup` aus, um die Bindung zu installieren.
</Tip>

### Schnellbefehle

| Tastaturkürzel | Beschreibung        | Notizen                                                                              |
| :------------- | :------------------ | :----------------------------------------------------------------------------------- |
| `/` am Anfang  | Befehl oder Skill   | Siehe [integrierte Befehle](#built-in-commands) und [Skills](/de/skills)             |
| `!` am Anfang  | Bash-Modus          | Führen Sie Befehle direkt aus und fügen Sie die Ausführungsausgabe zur Sitzung hinzu |
| `@`            | Dateipfad-Erwähnung | Trigger-Dateipfad-Autovervollständigung                                              |

## Integrierte Befehle

Geben Sie `/` in Claude Code ein, um alle verfügbaren Befehle anzuzeigen, oder geben Sie `/` gefolgt von beliebigen Buchstaben ein, um zu filtern. Nicht alle Befehle sind für jeden Benutzer sichtbar. Einige hängen von Ihrer Plattform, Ihrem Plan oder Ihrer Umgebung ab. Beispielsweise erscheint `/desktop` nur auf macOS und Windows, `/upgrade` und `/privacy-settings` sind nur für Pro- und Max-Pläne verfügbar, und `/terminal-setup` ist verborgen, wenn Ihr Terminal seine Tastenbindungen nativ unterstützt.

Claude Code wird auch mit [gebündelten Skills](/de/skills#bundled-skills) wie `/simplify`, `/batch` und `/debug` ausgeliefert, die neben integrierten Befehlen angezeigt werden, wenn Sie `/` eingeben. Um Ihre eigenen Befehle zu erstellen, siehe [Skills](/de/skills).

In der folgenden Tabelle gibt `<arg>` ein erforderliches Argument an und `[arg]` ein optionales.

| Befehl                    | Zweck                                                                                                                                                                                                                                                                                           |
| :------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/add-dir <path>`         | Fügen Sie ein neues Arbeitsverzeichnis zur aktuellen Sitzung hinzu                                                                                                                                                                                                                              |
| `/agents`                 | Verwalten Sie [Agent](/de/sub-agents)-Konfigurationen                                                                                                                                                                                                                                           |
| `/btw <question>`         | Stellen Sie eine schnelle [Nebenfrage](#side-questions-with-%2Fbtw), ohne sie zum Gespräch hinzuzufügen                                                                                                                                                                                         |
| `/chrome`                 | Konfigurieren Sie [Claude in Chrome](/de/chrome)-Einstellungen                                                                                                                                                                                                                                  |
| `/clear`                  | Löschen Sie den Gesprächsverlauf und geben Sie Kontext frei. Aliase: `/reset`, `/new`                                                                                                                                                                                                           |
| `/compact [instructions]` | Komprimieren Sie das Gespräch mit optionalen Fokus-Anweisungen                                                                                                                                                                                                                                  |
| `/config`                 | Öffnen Sie die [Einstellungen](/de/settings)-Schnittstelle, um Design, Modell, [Ausgabestil](/de/output-styles) und andere Einstellungen anzupassen. Alias: `/settings`                                                                                                                         |
| `/context`                | Visualisieren Sie die aktuelle Kontextnutzung als farbiges Gitter                                                                                                                                                                                                                               |
| `/copy`                   | Kopieren Sie die letzte Antwort des Assistenten in die Zwischenablage. Wenn Code-Blöcke vorhanden sind, zeigt eine interaktive Auswahl an, um einzelne Blöcke oder die vollständige Antwort auszuwählen                                                                                         |
| `/cost`                   | Zeigen Sie Token-Nutzungsstatistiken an. Siehe [Kostenverfolgungs-Leitfaden](/de/costs#using-the-cost-command) für abonnementspezifische Details                                                                                                                                                |
| `/desktop`                | Setzen Sie die aktuelle Sitzung in der Claude Code Desktop-App fort. Nur macOS und Windows. Alias: `/app`                                                                                                                                                                                       |
| `/diff`                   | Öffnen Sie einen interaktiven Diff-Viewer, der nicht committete Änderungen und Pro-Turn-Diffs anzeigt. Verwenden Sie Links-/Rechts-Pfeile, um zwischen dem aktuellen Git-Diff und einzelnen Claude-Turns zu wechseln, und Auf-/Ab-Pfeile zum Durchsuchen von Dateien                            |
| `/doctor`                 | Diagnostizieren und überprüfen Sie Ihre Claude Code-Installation und -Einstellungen                                                                                                                                                                                                             |
| `/exit`                   | Beenden Sie die CLI. Alias: `/quit`                                                                                                                                                                                                                                                             |
| `/export [filename]`      | Exportieren Sie das aktuelle Gespräch als Klartext. Mit einem Dateinamen wird direkt in diese Datei geschrieben. Ohne öffnet einen Dialog zum Kopieren in die Zwischenablage oder Speichern in einer Datei                                                                                      |
| `/extra-usage`            | Konfigurieren Sie zusätzliche Nutzung, um weiterzuarbeiten, wenn Ratenlimits erreicht werden                                                                                                                                                                                                    |
| `/fast [on\|off]`         | Schalten Sie [Fast Mode](/de/fast-mode) ein oder aus                                                                                                                                                                                                                                            |
| `/feedback [report]`      | Senden Sie Feedback zu Claude Code. Alias: `/bug`                                                                                                                                                                                                                                               |
| `/fork [name]`            | Erstellen Sie einen Fork des aktuellen Gesprächs an diesem Punkt                                                                                                                                                                                                                                |
| `/help`                   | Zeigen Sie Hilfe und verfügbare Befehle an                                                                                                                                                                                                                                                      |
| `/hooks`                  | Verwalten Sie [Hook](/de/hooks)-Konfigurationen für Tool-Ereignisse                                                                                                                                                                                                                             |
| `/ide`                    | Verwalten Sie IDE-Integrationen und zeigen Sie den Status an                                                                                                                                                                                                                                    |
| `/init`                   | Initialisieren Sie das Projekt mit `CLAUDE.md`-Leitfaden                                                                                                                                                                                                                                        |
| `/insights`               | Generieren Sie einen Bericht, der Ihre Claude Code-Sitzungen analysiert, einschließlich Projektbereiche, Interaktionsmuster und Reibungspunkte                                                                                                                                                  |
| `/install-github-app`     | Richten Sie die [Claude GitHub Actions](/de/github-actions)-App für ein Repository ein. Führt Sie durch die Auswahl eines Repos und die Konfiguration der Integration                                                                                                                           |
| `/install-slack-app`      | Installieren Sie die Claude Slack-App. Öffnet einen Browser, um den OAuth-Flow abzuschließen                                                                                                                                                                                                    |
| `/keybindings`            | Öffnen oder erstellen Sie Ihre Tastenbindungs-Konfigurationsdatei                                                                                                                                                                                                                               |
| `/login`                  | Melden Sie sich bei Ihrem Anthropic-Konto an                                                                                                                                                                                                                                                    |
| `/logout`                 | Melden Sie sich von Ihrem Anthropic-Konto ab                                                                                                                                                                                                                                                    |
| `/mcp`                    | Verwalten Sie MCP-Serververbindungen und OAuth-Authentifizierung                                                                                                                                                                                                                                |
| `/memory`                 | Bearbeiten Sie `CLAUDE.md`-Speicherdateien, aktivieren oder deaktivieren Sie [Auto-Memory](/de/memory#auto-memory), und zeigen Sie Auto-Memory-Einträge an                                                                                                                                      |
| `/mobile`                 | Zeigen Sie QR-Code zum Herunterladen der Claude Mobile-App an. Aliase: `/ios`, `/android`                                                                                                                                                                                                       |
| `/model [model]`          | Wählen Sie das KI-Modell aus oder ändern Sie es. Für Modelle, die dies unterstützen, verwenden Sie Links-/Rechts-Pfeile, um [Anstrengungsstufe anzupassen](/de/model-config#adjust-effort-level). Die Änderung wird sofort wirksam, ohne auf die Fertigstellung der aktuellen Antwort zu warten |
| `/passes`                 | Teilen Sie eine kostenlose Woche Claude Code mit Freunden. Nur sichtbar, wenn Ihr Konto berechtigt ist                                                                                                                                                                                          |
| `/permissions`            | Zeigen Sie [Berechtigungen](/de/permissions#manage-permissions) an oder aktualisieren Sie sie. Alias: `/allowed-tools`                                                                                                                                                                          |
| `/plan`                   | Geben Sie den Plan Mode direkt vom Prompt ein                                                                                                                                                                                                                                                   |
| `/plugin`                 | Verwalten Sie Claude Code [Plugins](/de/plugins)                                                                                                                                                                                                                                                |
| `/pr-comments [PR]`       | Rufen Sie Kommentare aus einem GitHub Pull Request ab und zeigen Sie sie an. Erkennt automatisch den PR für den aktuellen Branch, oder übergeben Sie eine PR-URL oder -Nummer. Erfordert die `gh` CLI                                                                                           |
| `/privacy-settings`       | Zeigen Sie Ihre Datenschutzeinstellungen an und aktualisieren Sie sie. Nur für Pro- und Max-Plan-Abonnenten verfügbar                                                                                                                                                                           |
| `/release-notes`          | Zeigen Sie das vollständige Änderungsprotokoll an, wobei die neueste Version am nächsten zu Ihrem Prompt liegt                                                                                                                                                                                  |
| `/reload-plugins`         | Laden Sie alle aktiven [Plugins](/de/plugins) neu, um ausstehende Änderungen anzuwenden, ohne neu zu starten. Meldet, was geladen wurde, und notiert alle Änderungen, die einen Neustart erfordern                                                                                              |
| `/remote-control`         | Machen Sie diese Sitzung für [Remote-Steuerung](/de/remote-control) von claude.ai verfügbar. Alias: `/rc`                                                                                                                                                                                       |
| `/remote-env`             | Konfigurieren Sie die Standard-Remote-Umgebung für [Teleport-Sitzungen](/de/claude-code-on-the-web#teleport-a-web-session-to-your-terminal)                                                                                                                                                     |
| `/rename [name]`          | Benennen Sie die aktuelle Sitzung um. Ohne Namen wird automatisch eine aus dem Gesprächsverlauf generiert                                                                                                                                                                                       |
| `/resume [session]`       | Setzen Sie ein Gespräch nach ID oder Name fort, oder öffnen Sie die Sitzungsauswahl. Alias: `/continue`                                                                                                                                                                                         |
| `/review`                 | Veraltet. Installieren Sie stattdessen das [`code-review`-Plugin](https://github.com/anthropics/claude-code-marketplace/blob/main/code-review/README.md): `claude plugin install code-review@claude-code-marketplace`                                                                           |
| `/rewind`                 | Spulen Sie das Gespräch und/oder den Code zu einem vorherigen Punkt zurück, oder fassen Sie ab einer ausgewählten Nachricht zusammen. Siehe [Checkpointing](/de/checkpointing). Alias: `/checkpoint`                                                                                            |
| `/sandbox`                | Schalten Sie [Sandbox-Modus](/de/sandboxing) um. Nur auf unterstützten Plattformen verfügbar                                                                                                                                                                                                    |
| `/security-review`        | Analysieren Sie ausstehende Änderungen im aktuellen Branch auf Sicherheitslücken. Überprüft den Git-Diff und identifiziert Risiken wie Injection, Auth-Probleme und Datenexposition                                                                                                             |
| `/skills`                 | Listet verfügbare [Skills](/de/skills) auf                                                                                                                                                                                                                                                      |
| `/stats`                  | Visualisieren Sie tägliche Nutzung, Sitzungsverlauf, Streaks und Modelleinstellungen                                                                                                                                                                                                            |
| `/status`                 | Öffnen Sie die Einstellungen-Schnittstelle (Status-Registerkarte) mit Version, Modell, Konto und Konnektivität                                                                                                                                                                                  |
| `/statusline`             | Konfigurieren Sie Claude Codes [Status-Zeile](/de/statusline). Beschreiben Sie, was Sie möchten, oder führen Sie ohne Argumente aus, um automatisch von Ihrem Shell-Prompt zu konfigurieren                                                                                                     |
| `/stickers`               | Bestellen Sie Claude Code-Aufkleber                                                                                                                                                                                                                                                             |
| `/tasks`                  | Listet und verwaltet Hintergrund-Aufgaben                                                                                                                                                                                                                                                       |
| `/terminal-setup`         | Konfigurieren Sie Terminal-Tastenbindungen für Shift+Enter und andere Kürzel. Nur in Terminals sichtbar, die dies benötigen, wie VS Code, Alacritty oder Warp                                                                                                                                   |
| `/theme`                  | Ändern Sie das Farbschema. Umfasst helle und dunkle Varianten, farbenblind-zugängliche (daltonisierte) Designs und ANSI-Designs, die die Farbpalette Ihres Terminals verwenden                                                                                                                  |
| `/upgrade`                | Öffnen Sie die Upgrade-Seite, um zu einem höheren Plan-Tier zu wechseln                                                                                                                                                                                                                         |
| `/usage`                  | Zeigen Sie Plan-Nutzungslimits und Ratenlimit-Status an                                                                                                                                                                                                                                         |
| `/vim`                    | Wechseln Sie zwischen Vim- und Normal-Bearbeitungsmodi                                                                                                                                                                                                                                          |

### MCP-Prompts

MCP-Server können Prompts verfügbar machen, die als Befehle angezeigt werden. Diese verwenden das Format `/mcp__<server>__<prompt>` und werden dynamisch von verbundenen Servern erkannt. Siehe [MCP-Prompts](/de/mcp#use-mcp-prompts-as-commands) für Details.

## Vim-Editor-Modus

Aktivieren Sie Vim-ähnliche Bearbeitung mit dem `/vim`-Befehl oder konfigurieren Sie dauerhaft über `/config`.

### Modusumschaltung

| Befehl | Aktion                         | Aus Modus |
| :----- | :----------------------------- | :-------- |
| `Esc`  | Geben Sie den NORMAL-Modus ein | INSERT    |
| `i`    | Einfügen vor Cursor            | NORMAL    |
| `I`    | Einfügen am Anfang der Zeile   | NORMAL    |
| `a`    | Einfügen nach Cursor           | NORMAL    |
| `A`    | Einfügen am Ende der Zeile     | NORMAL    |
| `o`    | Zeile unten öffnen             | NORMAL    |
| `O`    | Zeile oben öffnen              | NORMAL    |

### Navigation (NORMAL-Modus)

| Befehl          | Aktion                                                         |
| :-------------- | :------------------------------------------------------------- |
| `h`/`j`/`k`/`l` | Nach links/unten/oben/rechts bewegen                           |
| `w`             | Nächstes Wort                                                  |
| `e`             | Ende des Wortes                                                |
| `b`             | Vorheriges Wort                                                |
| `0`             | Anfang der Zeile                                               |
| `$`             | Ende der Zeile                                                 |
| `^`             | Erstes Nicht-Leerzeichen-Zeichen                               |
| `gg`            | Anfang der Eingabe                                             |
| `G`             | Ende der Eingabe                                               |
| `f{char}`       | Zur nächsten Vorkommen des Zeichens springen                   |
| `F{char}`       | Zum vorherigen Vorkommen des Zeichens springen                 |
| `t{char}`       | Direkt vor das nächste Vorkommen des Zeichens springen         |
| `T{char}`       | Direkt nach das vorherige Vorkommen des Zeichens springen      |
| `;`             | Letzte f/F/t/T-Bewegung wiederholen                            |
| `,`             | Letzte f/F/t/T-Bewegung in umgekehrter Reihenfolge wiederholen |

<Note>
  Im Vim-Normal-Modus navigieren die Pfeiltasten den Befehlsverlauf, wenn sich der Cursor am Anfang oder Ende der Eingabe befindet und nicht weiter bewegt werden kann.
</Note>

### Bearbeitung (NORMAL-Modus)

| Befehl         | Aktion                       |
| :------------- | :--------------------------- |
| `x`            | Zeichen löschen              |
| `dd`           | Zeile löschen                |
| `D`            | Bis zum Zeilenende löschen   |
| `dw`/`de`/`db` | Wort löschen/bis Ende/zurück |
| `cc`           | Zeile ändern                 |
| `C`            | Bis zum Zeilenende ändern    |
| `cw`/`ce`/`cb` | Wort ändern/bis Ende/zurück  |
| `yy`/`Y`       | Zeile yanken (kopieren)      |
| `yw`/`ye`/`yb` | Wort yanken/bis Ende/zurück  |
| `p`            | Nach Cursor einfügen         |
| `P`            | Vor Cursor einfügen          |
| `>>`           | Zeile einrücken              |
| `<<`           | Zeile ausrücken              |
| `J`            | Zeilen verbinden             |
| `.`            | Letzte Änderung wiederholen  |

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

## Befehlsverlauf

Claude Code verwaltet den Befehlsverlauf für die aktuelle Sitzung:

* Der Eingabeverlauf wird pro Arbeitsverzeichnis gespeichert
* Der Eingabeverlauf wird zurückgesetzt, wenn Sie `/clear` ausführen, um eine neue Sitzung zu starten. Das vorherige Gesprächs der Sitzung wird beibehalten und kann fortgesetzt werden.
* Verwenden Sie Auf-/Ab-Pfeile zum Navigieren (siehe Tastaturkürzel oben)
* **Hinweis**: Verlaufserweiterung (`!`) ist standardmäßig deaktiviert

### Reverse-Suche mit Ctrl+R

Drücken Sie `Ctrl+R`, um interaktiv durch Ihren Befehlsverlauf zu suchen:

1. **Suche starten**: Drücken Sie `Ctrl+R`, um die Reverse-Verlaufssuche zu aktivieren
2. **Abfrage eingeben**: Geben Sie Text ein, um in vorherigen Befehlen zu suchen. Der Suchbegriff wird in übereinstimmenden Ergebnissen hervorgehoben
3. **Übereinstimmungen navigieren**: Drücken Sie `Ctrl+R` erneut, um durch ältere Übereinstimmungen zu navigieren
4. **Übereinstimmung akzeptieren**:
   * Drücken Sie `Tab` oder `Esc`, um die aktuelle Übereinstimmung zu akzeptieren und die Bearbeitung fortzusetzen
   * Drücken Sie `Enter`, um die Übereinstimmung zu akzeptieren und den Befehl sofort auszuführen
5. **Suche abbrechen**:
   * Drücken Sie `Ctrl+C`, um abzubrechen und Ihre ursprüngliche Eingabe wiederherzustellen
   * Drücken Sie `Backspace` bei leerer Suche, um abzubrechen

Die Suche zeigt übereinstimmende Befehle mit dem hervorgehobenen Suchbegriff an, sodass Sie vorherige Eingaben finden und wiederverwenden können.

## Hintergrund-Bash-Befehle

Claude Code unterstützt die Ausführung von Bash-Befehlen im Hintergrund, sodass Sie weiterarbeiten können, während lange laufende Prozesse ausgeführt werden.

### Wie Backgrounding funktioniert

Wenn Claude Code einen Befehl im Hintergrund ausführt, führt es den Befehl asynchron aus und gibt sofort eine Hintergrund-Task-ID zurück. Claude Code kann auf neue Prompts reagieren, während der Befehl im Hintergrund weiter ausgeführt wird.

Um Befehle im Hintergrund auszuführen, können Sie entweder:

* Claude Code auffordern, einen Befehl im Hintergrund auszuführen
* Drücken Sie Ctrl+B, um eine reguläre Bash-Tool-Invokation in den Hintergrund zu verschieben. (Tmux-Benutzer müssen Ctrl+B zweimal drücken, da Tmux einen Präfix-Schlüssel hat.)

**Wichtige Funktionen:**

* Die Ausgabe wird gepuffert und Claude kann sie mit dem TaskOutput-Tool abrufen
* Hintergrund-Tasks haben eindeutige IDs zum Verfolgen und Abrufen von Ausgaben
* Hintergrund-Tasks werden automatisch bereinigt, wenn Claude Code beendet wird

Um alle Hintergrund-Task-Funktionalität zu deaktivieren, setzen Sie die Umgebungsvariable `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` auf `1`. Siehe [Umgebungsvariablen](/de/settings#environment-variables) für Details.

**Häufig backgroundete Befehle:**

* Build-Tools (webpack, vite, make)
* Paketmanager (npm, yarn, pnpm)
* Test-Runner (jest, pytest)
* Entwicklungsserver
* Lange laufende Prozesse (docker, terraform)

### Bash-Modus mit `!`-Präfix

Führen Sie Bash-Befehle direkt aus, ohne Claude zu durchlaufen, indem Sie Ihre Eingabe mit `!` präfixieren:

```bash  theme={null}
! npm test
! git status
! ls -la
```

Bash-Modus:

* Fügt den Befehl und seine Ausgabe zum Gesprächskontext hinzu
* Zeigt Echtzeit-Fortschritt und Ausgabe
* Unterstützt das gleiche `Ctrl+B`-Backgrounding für lange laufende Befehle
* Erfordert nicht, dass Claude den Befehl interpretiert oder genehmigt
* Unterstützt verlaufsbasierte Autovervollständigung: Geben Sie einen Teilbefehl ein und drücken Sie **Tab**, um aus vorherigen `!`-Befehlen im aktuellen Projekt zu vervollständigen
* Beenden Sie mit `Escape`, `Backspace` oder `Ctrl+U` bei einer leeren Eingabeaufforderung

Dies ist nützlich für schnelle Shell-Operationen bei Beibehaltung des Gesprächskontexts.

## Prompt-Vorschläge

Wenn Sie eine Sitzung zum ersten Mal öffnen, wird ein ausgegrauter Beispielbefehl in der Prompt-Eingabe angezeigt, um Ihnen den Einstieg zu erleichtern. Claude Code wählt dies aus Ihrem Projekt-Git-Verlauf aus, sodass es Dateien widerspiegelt, an denen Sie kürzlich gearbeitet haben.

Nach Claudes Antwort werden Vorschläge weiterhin basierend auf Ihrem Gesprächsverlauf angezeigt, z. B. ein Folgenschritt aus einer mehrteiligen Anfrage oder eine natürliche Fortsetzung Ihres Workflows.

* Drücken Sie **Tab**, um den Vorschlag zu akzeptieren, oder drücken Sie **Enter**, um zu akzeptieren und einzureichen
* Beginnen Sie zu tippen, um ihn zu verwerfen

Der Vorschlag wird als Hintergrund-Anfrage ausgeführt, die den Prompt-Cache des übergeordneten Gesprächs wiederverwenden, sodass die zusätzlichen Kosten minimal sind. Claude Code überspringt die Vorschlagsgenerierung, wenn der Cache kalt ist, um unnötige Kosten zu vermeiden.

Vorschläge werden automatisch nach dem ersten Turn eines Gesprächs, im nicht-interaktiven Modus und im Plan Mode übersprungen.

Um Prompt-Vorschläge vollständig zu deaktivieren, setzen Sie die Umgebungsvariable oder schalten Sie die Einstellung in `/config` um:

```bash  theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## Nebenfragen mit /btw

Verwenden Sie `/btw`, um eine schnelle Frage zu Ihrer aktuellen Arbeit zu stellen, ohne sie zum Gesprächsverlauf hinzuzufügen. Dies ist nützlich, wenn Sie eine schnelle Antwort möchten, aber nicht den Hauptkontext unordentlich machen oder Claude von einer lange laufenden Aufgabe ablenken möchten.

```
/btw what was the name of that config file again?
```

Nebenfragen haben vollständige Sichtbarkeit des aktuellen Gesprächs, sodass Sie nach Code fragen können, den Claude bereits gelesen hat, Entscheidungen, die es früher getroffen hat, oder alles andere aus der Sitzung. Die Frage und Antwort sind flüchtig: Sie erscheinen in einer verwerfbaren Überlagerung und treten niemals in den Gesprächsverlauf ein.

* **Verfügbar während Claude arbeitet**: Sie können `/btw` ausführen, auch während Claude eine Antwort verarbeitet. Die Nebenfrage wird unabhängig ausgeführt und unterbricht den Hauptturn nicht.
* **Kein Tool-Zugriff**: Nebenfragen beantworten nur aus dem, was bereits im Kontext ist. Claude kann keine Dateien lesen, Befehle ausführen oder suchen, wenn eine Nebenfrage beantwortet wird.
* **Einzelne Antwort**: Es gibt keine Folgeversuche. Wenn Sie einen Hin- und Herwechsel benötigen, verwenden Sie stattdessen einen normalen Prompt.
* **Niedrige Kosten**: Die Nebenfrage verwendet den Prompt-Cache des übergeordneten Gesprächs wieder, sodass die zusätzlichen Kosten minimal sind.

Drücken Sie **Space**, **Enter** oder **Escape**, um die Antwort zu verwerfen und zur Eingabeaufforderung zurückzukehren.

`/btw` ist das Gegenteil eines [Subagenten](/de/sub-agents): Es sieht Ihr vollständiges Gespräch, hat aber keine Tools, während ein Subagent vollständige Tools hat, aber mit einem leeren Kontext beginnt. Verwenden Sie `/btw`, um nach dem zu fragen, was Claude bereits aus dieser Sitzung weiß; verwenden Sie einen Subagenten, um etwas Neues herauszufinden.

## Task-Liste

Bei der Arbeit an komplexen, mehrstufigen Arbeiten erstellt Claude eine Task-Liste, um den Fortschritt zu verfolgen. Aufgaben werden im Statusbereich Ihres Terminals mit Indikatoren angezeigt, die zeigen, was ausstehend, in Bearbeitung oder abgeschlossen ist.

* Drücken Sie `Ctrl+T`, um die Task-Listen-Ansicht umzuschalten. Die Anzeige zeigt bis zu 10 Aufgaben gleichzeitig
* Um alle Aufgaben anzuzeigen oder zu löschen, fragen Sie Claude direkt: „show me all tasks" oder „clear all tasks"
* Aufgaben bleiben über Kontext-Komprimierungen hinweg bestehen und helfen Claude, bei größeren Projekten organisiert zu bleiben
* Um eine Task-Liste über Sitzungen hinweg zu teilen, setzen Sie `CLAUDE_CODE_TASK_LIST_ID`, um ein benanntes Verzeichnis in `~/.claude/tasks/` zu verwenden: `CLAUDE_CODE_TASK_LIST_ID=my-project claude`
* Um zur vorherigen TODO-Liste zurückzukehren, setzen Sie `CLAUDE_CODE_ENABLE_TASKS=false`.

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
