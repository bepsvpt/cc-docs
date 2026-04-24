> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Konfigurieren Sie Ihr Terminal für Claude Code

> Beheben Sie Shift+Enter für Zeilenumbrüche, erhalten Sie einen Terminalton, wenn Claude fertig ist, konfigurieren Sie tmux, passen Sie das Farbschema an, und aktivieren Sie den Vim-Modus in der Claude Code CLI.

Claude Code funktioniert in jedem Terminal ohne Konfiguration. Diese Seite ist für den Fall, dass etwas nicht so funktioniert, wie Sie es erwarten. Finden Sie Ihr Symptom unten. Wenn alles bereits richtig funktioniert, benötigen Sie diese Seite nicht.

* [Shift+Enter sendet statt einen Zeilenumbruch einzufügen](#enter-multiline-prompts)
* [Option-Taste-Verknüpfungen funktionieren nicht auf macOS](#enable-option-key-shortcuts-on-macos)
* [Kein Ton oder Benachrichtigung, wenn Claude fertig ist](#get-a-terminal-bell-or-notification)
* [Sie führen Claude Code in tmux aus](#configure-tmux)
* [Die Anzeige flimmert oder die Scrollposition springt](#switch-to-fullscreen-rendering)
* [Sie möchten Vim-Tasten in der Eingabeaufforderung](#edit-prompts-with-vim-keybindings)

Diese Seite behandelt das Konfigurieren Ihres Terminals, um die richtigen Signale an Claude Code zu senden. Um zu ändern, auf welche Tasten Claude Code selbst reagiert, siehe stattdessen [Tastenbelegungen](/de/keybindings).

## Mehrzeilige Eingabeaufforderungen eingeben

Durch Drücken von Enter wird Ihre Nachricht gesendet. Um einen Zeilenumbruch ohne Absenden hinzuzufügen, drücken Sie Ctrl+J, oder geben Sie `\` ein und drücken dann Enter. Beide funktionieren in jedem Terminal ohne Setup.

In den meisten Terminals können Sie auch Shift+Enter drücken, aber die Unterstützung variiert je nach Terminal-Emulator:

| Terminal                                                                        | Shift+Enter für Zeilenumbruch                             |
| :------------------------------------------------------------------------------ | :-------------------------------------------------------- |
| Ghostty, Kitty, iTerm2, WezTerm, Warp, Apple Terminal                           | Funktioniert ohne Setup                                   |
| VS Code, Cursor, Windsurf, Alacritty, Zed                                       | Führen Sie `/terminal-setup` einmal aus                   |
| Windows Terminal, gnome-terminal, JetBrains IDEs wie PyCharm und Android Studio | Nicht verfügbar; verwenden Sie Ctrl+J oder `\` dann Enter |

Für VS Code, Cursor, Windsurf, Alacritty und Zed schreibt `/terminal-setup` Shift+Enter und andere Tastenbelegungen in die Konfigurationsdatei des Terminals. In VS Code, Cursor und Windsurf wird auch `terminal.integrated.mouseWheelScrollSensitivity` in den Editor-Einstellungen für sanfteres Scrollen im [Vollbildmodus](/de/fullscreen) gesetzt. Vorhandene Bindungen und Einstellungen bleiben erhalten; wenn Sie eine Meldung wie `VSCode terminal Shift+Enter key binding already configured` sehen, wurde keine Änderung vorgenommen. Führen Sie `/terminal-setup` direkt im Host-Terminal aus, nicht in tmux oder screen, da es in die Konfiguration des Host-Terminals schreiben muss.

Wenn Sie in tmux ausgeführt werden, erfordert Shift+Enter auch die [tmux-Konfiguration unten](#configure-tmux), selbst wenn das äußere Terminal es unterstützt.

Um Zeilenumbruch an eine andere Taste zu binden oder das Verhalten zu tauschen, sodass Enter einen Zeilenumbruch einfügt und Shift+Enter sendet, ordnen Sie die Aktionen `chat:newline` und `chat:submit` in Ihrer [Tastenbelegungsdatei](/de/keybindings) zu.

## Aktivieren Sie Option-Taste-Verknüpfungen auf macOS

Einige Claude Code-Verknüpfungen verwenden die Option-Taste, z. B. Option+Enter für einen Zeilenumbruch oder Option+P zum Wechsel von Modellen. Auf macOS senden die meisten Terminals die Option-Taste standardmäßig nicht als Modifizierer, daher funktionieren diese Verknüpfungen nicht, bis Sie sie aktivieren. Die Terminal-Einstellung dafür wird normalerweise als „Option als Meta-Taste verwenden" bezeichnet; Meta ist der historische Unix-Name für die Taste, die jetzt Option oder Alt genannt wird.

<Tabs>
  <Tab title="Apple Terminal">
    Öffnen Sie Einstellungen → Profile → Tastatur und aktivieren Sie 'Option als Meta-Taste verwenden".

    Wenn Sie die erste Eingabeaufforderung von Claude Code akzeptiert haben, die „Option+Enter für Zeilenumbrüche und visuellen Ton" angeboten hat, ist dies bereits erledigt. Diese Eingabeaufforderung führt `/terminal-setup` für Sie aus, das Option als Meta aktiviert und den Audioton auf einen visuellen Bildschirmblitz in Ihrem Apple Terminal-Profil umschaltet.
  </Tab>

  <Tab title="iTerm2">
    Öffnen Sie Einstellungen → Profile → Tasten → Allgemein und stellen Sie die linke Option-Taste und die rechte Option-Taste auf 'Esc+" ein.
  </Tab>

  <Tab title="VS Code">
    Fügen Sie `"terminal.integrated.macOptionIsMeta": true` zu Ihren VS Code-Einstellungen hinzu.
  </Tab>
</Tabs>

Für Ghostty, Kitty und andere Terminals suchen Sie nach einer Option-als-Alt- oder Option-als-Meta-Einstellung in der Konfigurationsdatei des Terminals.

## Erhalten Sie einen Terminalton oder eine Benachrichtigung

Wenn Claude eine Aufgabe abschließt oder bei einer Berechtigungsaufforderung pausiert, wird ein Benachrichtigungsereignis ausgelöst. Wenn Sie dies als Terminalton oder Desktop-Benachrichtigung anzeigen, können Sie zu anderen Arbeiten wechseln, während eine lange Aufgabe ausgeführt wird.

Claude Code sendet eine Desktop-Benachrichtigung nur in Ghostty, Kitty und iTerm2; jedes andere Terminal benötigt stattdessen einen [Benachrichtigungshook](#play-a-sound-with-a-notification-hook). Die Benachrichtigung erreicht auch Ihren lokalen Computer über SSH, sodass eine Remote-Sitzung Sie immer noch benachrichtigen kann. Ghostty und Kitty leiten sie ohne weitere Einrichtung an Ihr Betriebssystem-Benachrichtigungscenter weiter. iTerm2 erfordert, dass Sie die Weiterleitung aktivieren:

<Steps>
  <Step title="Öffnen Sie iTerm2-Benachrichtigungseinstellungen">
    Gehen Sie zu Einstellungen → Profile → Terminal.
  </Step>

  <Step title="Aktivieren Sie Benachrichtigungen">
    Aktivieren Sie „Notification Center Alerts", klicken Sie dann auf „Filter Alerts" und aktivieren Sie „Send escape sequence-generated alerts".
  </Step>
</Steps>

Wenn Benachrichtigungen immer noch nicht angezeigt werden, bestätigen Sie, dass Ihre Terminalanwendung in Ihren Betriebssystemeinstellungen Benachrichtigungsberechtigung hat, und wenn Sie in tmux ausgeführt werden, [aktivieren Sie Passthrough](#configure-tmux).

### Spielen Sie einen Ton mit einem Benachrichtigungshook ab

In jedem Terminal können Sie einen [Benachrichtigungshook](/de/hooks-guide#get-notified-when-claude-needs-input) konfigurieren, um einen Ton abzuspielen oder einen benutzerdefinierten Befehl auszuführen, wenn Claude Ihre Aufmerksamkeit benötigt. Hooks werden neben der Desktop-Benachrichtigung ausgeführt, nicht als Ersatz. Terminals wie Warp oder Apple Terminal verlassen sich allein auf einen Hook, da Claude Code ihnen keine Desktop-Benachrichtigung sendet.

Das folgende Beispiel spielt einen Systemton auf macOS ab. Der verlinkte Leitfaden enthält Desktop-Benachrichtigungsbefehle für macOS, Linux und Windows.

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

## Konfigurieren Sie tmux

Wenn Claude Code in tmux ausgeführt wird, brechen zwei Dinge standardmäßig: Shift+Enter sendet statt einen Zeilenumbruch einzufügen, und Desktop-Benachrichtigungen und die [Fortschrittsleiste](/de/settings#global-config-settings) erreichen niemals das äußere Terminal. Fügen Sie diese Zeilen zu `~/.tmux.conf` hinzu und führen Sie dann `tmux source-file ~/.tmux.conf` aus, um sie auf den laufenden Server anzuwenden:

```bash ~/.tmux.conf theme={null}
set -g allow-passthrough on
set -s extended-keys on
set -as terminal-features 'xterm*:extkeys'
```

Die `allow-passthrough`-Zeile ermöglicht es, dass Benachrichtigungen und Fortschrittsaktualisierungen iTerm2, Ghostty oder Kitty erreichen, anstatt von tmux verschluckt zu werden. Die `extended-keys`-Zeilen ermöglichen es tmux, Shift+Enter von einfachem Enter zu unterscheiden, sodass die Zeilenumbruch-Verknüpfung funktioniert.

## Passen Sie das Farbschema an

Verwenden Sie den Befehl `/theme` oder die Designauswahl in `/config`, um ein Claude Code-Design auszuwählen, das Ihrem Terminal entspricht. Wenn Sie die Auto-Option auswählen, wird der helle oder dunkle Hintergrund Ihres Terminals erkannt, sodass das Design den Änderungen des Betriebssystem-Erscheinungsbilds folgt, wenn Ihr Terminal dies tut. Claude Code steuert nicht das Farbschema des Terminals selbst, das von der Terminalanwendung festgelegt wird.

Um anzupassen, was am unteren Rand der Benutzeroberfläche angezeigt wird, konfigurieren Sie eine [benutzerdefinierte Statuszeile](/de/statusline), die das aktuelle Modell, das Arbeitsverzeichnis, den Git-Branch oder andere Kontextinformationen anzeigt.

### Erstellen Sie ein benutzerdefiniertes Design

<Note>
  Benutzerdefinierte Designs erfordern Claude Code v2.1.118 oder später.
</Note>

Zusätzlich zu den integrierten Voreinstellungen listet `/theme` alle benutzerdefinierten Designs auf, die Sie definiert haben, sowie alle Designs, die von installierten [Plugins](/de/plugins-reference#themes) beigetragen wurden. Wählen Sie **Neues benutzerdefiniertes Design…** am Ende der Liste aus, um eines interaktiv zu erstellen: Sie benennen das Design und wählen dann einzelne Farbtoken aus, um sie zu überschreiben. Drücken Sie `Ctrl+E`, während ein benutzerdefiniertes Design hervorgehoben ist, um es zu bearbeiten.

Jedes benutzerdefinierte Design ist eine JSON-Datei in `~/.claude/themes/`. Der Dateiname ohne die `.json`-Erweiterung ist der Slug des Designs, und das Auswählen des Designs speichert `custom:<slug>` als Ihre Design-Einstellung. Die Datei hat drei optionale Felder:

| Feld        | Typ    | Beschreibung                                                                                                                                                        |
| :---------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`      | string | Anzeigebezeichnung in `/theme`. Standardmäßig der Dateiname-Slug                                                                                                    |
| `base`      | string | Integrierte Voreinstellung, von der das Design ausgeht: `dark`, `light`, `dark-daltonized`, `light-daltonized`, `dark-ansi` oder `light-ansi`. Standardmäßig `dark` |
| `overrides` | object | Zuordnung von Farbtoken-Namen zu Farbwerten. Token, die hier nicht aufgelistet sind, fallen auf die Basisvoreinstellung zurück                                      |

Farbwerte akzeptieren `#rrggbb`, `#rgb`, `rgb(r,g,b)`, `ansi256(n)` oder `ansi:<name>`, wobei `<name>` einer der 16 standardmäßigen ANSI-Farbnamen wie `red` oder `cyanBright` ist. Unbekannte Token und ungültige Farbwerte werden ignoriert, sodass ein Tippfehler das Rendering nicht beschädigen kann.

Das folgende Beispiel definiert ein Design, das die dunkle Voreinstellung beibehält, aber die Eingabeaufforderungs-Akzentfarbe, Fehlertext und Erfolgstexte umfärbt:

```json ~/.claude/themes/dracula.json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

Claude Code überwacht `~/.claude/themes/` und lädt neu, wenn sich eine Datei ändert, sodass Änderungen, die in Ihrem Editor vorgenommen werden, auf eine laufende Sitzung angewendet werden, ohne dass ein Neustart erforderlich ist.

## Wechseln Sie zum Vollbildrendering

Wenn die Anzeige flimmert oder die Scrollposition springt, während Claude arbeitet, wechseln Sie zum [Vollbildrendering-Modus](/de/fullscreen). Es zeichnet auf einen separaten Bildschirm, den das Terminal für Vollbild-Apps reserviert, anstatt an Ihren normalen Scrollback anzuhängen, was die Speichernutzung flach hält und Mausunterstützung zum Scrollen und Auswählen hinzufügt. In diesem Modus scrollen Sie mit der Maus oder PageUp in Claude Code, nicht mit dem nativen Scrollback Ihres Terminals; siehe die [Vollbildseite](/de/fullscreen#search-and-review-the-conversation) für die Suche und das Kopieren.

Führen Sie `/tui fullscreen` aus, um in der aktuellen Sitzung mit Ihrem Gespräch intakt zu wechseln. Um es zur Standardeinstellung zu machen, setzen Sie die Umgebungsvariable `CLAUDE_CODE_NO_FLICKER`, bevor Sie Claude Code starten:

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

## Großen Inhalt einfügen

Wenn Sie mehr als 10.000 Zeichen in die Eingabeaufforderung einfügen, reduziert Claude Code die Eingabe auf einen `[Pasted text]`-Platzhalter, damit das Eingabefeld verwendbar bleibt. Der vollständige Inhalt wird immer noch an Claude gesendet, wenn Sie absenden.

Das integrierte VS Code-Terminal kann Zeichen aus sehr großen Einfügungen verlieren, bevor sie Claude Code erreichen, daher bevorzugen Sie dort dateibasierte Workflows. Für sehr große Eingaben wie ganze Dateien oder lange Protokolle schreiben Sie den Inhalt in eine Datei und bitten Claude, diese zu lesen, anstatt einzufügen. Dies hält das Gesprächstranskript lesbar und ermöglicht es Claude, die Datei in späteren Zügen nach Pfad zu referenzieren.

## Bearbeiten Sie Eingabeaufforderungen mit Vim-Tastenbelegungen

Claude Code enthält einen Vim-ähnlichen Bearbeitungsmodus für die Eingabeaufforderungseingabe. Aktivieren Sie ihn über `/config` → Editor-Modus, oder indem Sie den globalen Konfigurationsschlüssel [`editorMode`](/de/settings#global-config-settings) auf `"vim"` in `~/.claude.json` setzen. Setzen Sie den Editor-Modus zurück auf `normal`, um ihn auszuschalten.

Der Vim-Modus unterstützt eine Teilmenge von NORMAL- und VISUAL-Modus-Bewegungen und Operatoren, wie z. B. `hjkl`-Navigation, `v`/`V`-Auswahl und `d`/`c`/`y` mit Textobjekten. Siehe die [Vim-Editor-Modus-Referenz](/de/interactive-mode#vim-editor-mode) für die vollständige Schlüsseltabelle. Vim-Bewegungen können nicht über die Tastenbelegungsdatei neu zugeordnet werden.

Das Drücken von Enter sendet Ihre Eingabeaufforderung immer noch im INSERT-Modus, anders als Standard-Vim. Verwenden Sie `o` oder `O` im NORMAL-Modus oder Ctrl+J, um stattdessen einen Zeilenumbruch einzufügen.

## Verwandte Ressourcen

* [Interaktiver Modus](/de/interactive-mode): vollständige Tastaturverknüpfungs-Referenz und die Vim-Schlüsseltabelle
* [Tastenbelegungen](/de/keybindings): ordnen Sie jede Claude Code-Verknüpfung neu zu, einschließlich Enter und Shift+Enter
* [Vollbildrendering](/de/fullscreen): Details zum Scrollen, Suchen und Kopieren im Vollbildmodus
* [Hooks-Leitfaden](/de/hooks-guide): weitere Benachrichtigungshook-Beispiele für Linux und Windows
* [Fehlerbehebung](/de/troubleshooting): Behebungen für Probleme außerhalb der Terminalkonfiguration
