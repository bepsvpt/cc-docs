> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Optimieren Sie Ihr Terminal-Setup

> Claude Code funktioniert am besten, wenn Ihr Terminal richtig konfiguriert ist. Befolgen Sie diese Richtlinien, um Ihr Erlebnis zu optimieren.

### Designs und Erscheinungsbild

Claude kann das Design Ihres Terminals nicht steuern. Das wird von Ihrer Terminalanwendung verwaltet. Sie können das Design von Claude Code jederzeit über den Befehl `/config` an Ihr Terminal anpassen.

Für zusätzliche Anpassungen der Claude Code-Oberfläche selbst können Sie eine [benutzerdefinierte Statuszeile](/de/statusline) konfigurieren, um kontextbezogene Informationen wie das aktuelle Modell, das Arbeitsverzeichnis oder den Git-Branch am unteren Rand Ihres Terminals anzuzeigen.

### Zeilenumbrüche

Sie haben mehrere Optionen, um Zeilenumbrüche in Claude Code einzugeben:

* **Schnelle Flucht**: Geben Sie `\` gefolgt von Enter ein, um einen Zeilenumbruch zu erstellen
* **Shift+Enter**: Funktioniert standardmäßig in iTerm2, WezTerm, Ghostty und Kitty
* **Tastaturkürzel**: Richten Sie eine Tastenkombination ein, um einen Zeilenumbruch in anderen Terminals einzufügen

**Shift+Enter für andere Terminals einrichten**

Führen Sie `/terminal-setup` in Claude Code aus, um Shift+Enter automatisch für VS Code, Alacritty, Zed und Warp zu konfigurieren.

<Note>
  Der Befehl `/terminal-setup` ist nur in Terminals sichtbar, die eine manuelle Konfiguration erfordern. Wenn Sie iTerm2, WezTerm, Ghostty oder Kitty verwenden, sehen Sie diesen Befehl nicht, da Shift+Enter bereits nativ funktioniert.
</Note>

**Option+Enter einrichten (VS Code, iTerm2 oder macOS Terminal.app)**

**Für Mac Terminal.app:**

1. Öffnen Sie Einstellungen → Profile → Tastatur
2. Aktivieren Sie „Option als Meta-Taste verwenden"

**Für iTerm2 und VS Code Terminal:**

1. Öffnen Sie Einstellungen → Profile → Tasten
2. Stellen Sie unter Allgemein die linke/rechte Optionstaste auf „Esc+" ein

### Benachrichtigungseinrichtung

Wenn Claude die Arbeit abgeschlossen hat und auf Ihre Eingabe wartet, wird ein Benachrichtigungsereignis ausgelöst. Sie können dieses Ereignis als Desktop-Benachrichtigung über Ihr Terminal anzeigen oder benutzerdefinierte Logik mit [Benachrichtigungshooks](/de/hooks#notification) ausführen.

#### Terminal-Benachrichtigungen

Kitty und Ghostty unterstützen Desktop-Benachrichtigungen ohne zusätzliche Konfiguration. iTerm 2 erfordert Setup:

1. Öffnen Sie iTerm 2 Einstellungen → Profile → Terminal
2. Aktivieren Sie „Notification Center Alerts"
3. Klicken Sie auf „Filter Alerts" und aktivieren Sie „Send escape sequence-generated alerts"

Wenn Benachrichtigungen nicht angezeigt werden, überprüfen Sie, ob Ihre Terminalanwendung in Ihren Betriebssystemeinstellungen Benachrichtigungsberechtigungen hat.

Andere Terminals, einschließlich des Standard-macOS-Terminals, unterstützen keine nativen Benachrichtigungen. Verwenden Sie stattdessen [Benachrichtigungshooks](/de/hooks#notification).

#### Benachrichtigungshooks

Um benutzerdefiniertes Verhalten hinzuzufügen, wenn Benachrichtigungen ausgelöst werden, z. B. das Abspielen eines Sounds oder das Senden einer Nachricht, konfigurieren Sie einen [Benachrichtigungshook](/de/hooks#notification). Hooks werden neben Terminal-Benachrichtigungen ausgeführt, nicht als Ersatz.

### Umgang mit großen Eingaben

Bei der Arbeit mit umfangreichem Code oder langen Anweisungen:

* **Vermeiden Sie direktes Einfügen**: Claude Code kann bei sehr langen eingefügten Inhalten Schwierigkeiten haben
* **Verwenden Sie dateibasierte Workflows**: Schreiben Sie Inhalte in eine Datei und bitten Sie Claude, diese zu lesen
* **Beachten Sie VS Code-Einschränkungen**: Das VS Code-Terminal neigt besonders dazu, lange Einfügungen zu kürzen

### Vim-Modus

Claude Code unterstützt eine Teilmenge von Vim-Tastenkombinationen, die mit `/vim` aktiviert oder über `/config` konfiguriert werden können.

Die unterstützte Teilmenge umfasst:

* Modusumschaltung: `Esc` (zu NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (zu INSERT)
* Navigation: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`, `f`/`F`/`t`/`T` mit `;`/`,` Wiederholung
* Bearbeitung: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (Wiederholung)
* Yank/Einfügen: `yy`/`Y`, `yw`/`ye`/`yb`, `p`/`P`
* Textobjekte: `iw`/`aw`, `iW`/`aW`, `i"`/`a"`, `i'`/`a'`, `i(`/`a(`, `i[`/`a[`, `i{`/`a{`
* Einrückung: `>>`/`<<`
* Zeilenoperationen: `J` (Zeilen verbinden)

Siehe [Interaktiver Modus](/de/interactive-mode#vim-editor-mode) für die vollständige Referenz.
