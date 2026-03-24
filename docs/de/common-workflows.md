> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Häufige Workflows

> Schritt-für-Schritt-Anleitungen zum Erkunden von Codebases, Beheben von Fehlern, Refaktorierung, Testen und anderen alltäglichen Aufgaben mit Claude Code.

Diese Seite behandelt praktische Workflows für die alltägliche Entwicklung: Erkunden unbekannter Code, Debugging, Refaktorierung, Schreiben von Tests, Erstellen von PRs und Verwalten von Sitzungen. Jeder Abschnitt enthält Beispiel-Prompts, die Sie an Ihre eigenen Projekte anpassen können. Für übergeordnete Muster und Tipps siehe [Best Practices](/de/best-practices).

## Neue Codebases verstehen

### Schnelle Codebase-Übersicht erhalten

Angenommen, Sie sind gerade einem neuen Projekt beigetreten und müssen dessen Struktur schnell verstehen.

<Steps>
  <Step title="Navigieren Sie zum Projektroot-Verzeichnis">
    ```bash  theme={null}
    cd /path/to/project 
    ```
  </Step>

  <Step title="Starten Sie Claude Code">
    ```bash  theme={null}
    claude 
    ```
  </Step>

  <Step title="Fragen Sie nach einer Übersicht auf hoher Ebene">
    ```text  theme={null}
    give me an overview of this codebase
    ```
  </Step>

  <Step title="Tauchen Sie tiefer in spezifische Komponenten ein">
    ```text  theme={null}
    explain the main architecture patterns used here
    ```

    ```text  theme={null}
    what are the key data models?
    ```

    ```text  theme={null}
    how is authentication handled?
    ```
  </Step>
</Steps>

<Tip>
  Tipps:

  * Beginnen Sie mit breiten Fragen und grenzen Sie dann auf spezifische Bereiche ein
  * Fragen Sie nach Coding-Konventionen und Mustern, die im Projekt verwendet werden
  * Fordern Sie ein Glossar projektspezifischer Begriffe an
</Tip>

### Relevanten Code finden

Angenommen, Sie müssen Code finden, der sich auf eine bestimmte Funktion oder Funktionalität bezieht.

<Steps>
  <Step title="Bitten Sie Claude, relevante Dateien zu finden">
    ```text  theme={null}
    find the files that handle user authentication
    ```
  </Step>

  <Step title="Erhalten Sie Kontext darüber, wie Komponenten zusammenwirken">
    ```text  theme={null}
    how do these authentication files work together?
    ```
  </Step>

  <Step title="Verstehen Sie den Ausführungsfluss">
    ```text  theme={null}
    trace the login process from front-end to database
    ```
  </Step>
</Steps>

<Tip>
  Tipps:

  * Seien Sie spezifisch bei dem, was Sie suchen
  * Verwenden Sie Domänensprache aus dem Projekt
  * Installieren Sie ein [Code-Intelligence-Plugin](/de/discover-plugins#code-intelligence) für Ihre Sprache, um Claude präzise 'Go to Definition"- und „Find References"-Navigation zu geben
</Tip>

***

## Fehler effizient beheben

Angenommen, Sie sind auf eine Fehlermeldung gestoßen und müssen deren Quelle finden und beheben.

<Steps>
  <Step title="Teilen Sie den Fehler mit Claude">
    ```text  theme={null}
    I'm seeing an error when I run npm test
    ```
  </Step>

  <Step title="Fragen Sie nach Behebungsempfehlungen">
    ```text  theme={null}
    suggest a few ways to fix the @ts-ignore in user.ts
    ```
  </Step>

  <Step title="Wenden Sie die Behebung an">
    ```text  theme={null}
    update user.ts to add the null check you suggested
    ```
  </Step>
</Steps>

<Tip>
  Tipps:

  * Teilen Sie Claude den Befehl mit, um das Problem zu reproduzieren und einen Stack Trace zu erhalten
  * Erwähnen Sie alle Schritte, um den Fehler zu reproduzieren
  * Lassen Sie Claude wissen, ob der Fehler intermittierend oder konsistent ist
</Tip>

***

## Code refaktorieren

Angenommen, Sie müssen alten Code aktualisieren, um moderne Muster und Praktiken zu verwenden.

<Steps>
  <Step title="Identifizieren Sie Legacy-Code zur Refaktorierung">
    ```text  theme={null}
    find deprecated API usage in our codebase
    ```
  </Step>

  <Step title="Erhalten Sie Refaktorierungsempfehlungen">
    ```text  theme={null}
    suggest how to refactor utils.js to use modern JavaScript features
    ```
  </Step>

  <Step title="Wenden Sie die Änderungen sicher an">
    ```text  theme={null}
    refactor utils.js to use ES2024 features while maintaining the same behavior
    ```
  </Step>

  <Step title="Überprüfen Sie die Refaktorierung">
    ```text  theme={null}
    run tests for the refactored code
    ```
  </Step>
</Steps>

<Tip>
  Tipps:

  * Bitten Sie Claude, die Vorteile des modernen Ansatzes zu erklären
  * Fordern Sie an, dass Änderungen die Rückwärtskompatibilität beibehalten, wenn nötig
  * Führen Sie Refaktorierung in kleinen, testbaren Schritten durch
</Tip>

***

## Spezialisierte Subagents verwenden

Angenommen, Sie möchten spezialisierte KI-Subagents verwenden, um bestimmte Aufgaben effektiver zu bewältigen.

<Steps>
  <Step title="Verfügbare Subagents anzeigen">
    ```text  theme={null}
    /agents
    ```

    Dies zeigt alle verfügbaren Subagents und ermöglicht es Ihnen, neue zu erstellen.
  </Step>

  <Step title="Subagents automatisch verwenden">
    Claude Code delegiert automatisch geeignete Aufgaben an spezialisierte Subagents:

    ```text  theme={null}
    review my recent code changes for security issues
    ```

    ```text  theme={null}
    run all tests and fix any failures
    ```
  </Step>

  <Step title="Fordern Sie explizit spezifische Subagents an">
    ```text  theme={null}
    use the code-reviewer subagent to check the auth module
    ```

    ```text  theme={null}
    have the debugger subagent investigate why users can't log in
    ```
  </Step>

  <Step title="Erstellen Sie benutzerdefinierte Subagents für Ihren Workflow">
    ```text  theme={null}
    /agents
    ```

    Wählen Sie dann 'Create New subagent" und folgen Sie den Aufforderungen, um Folgendes zu definieren:

    * Eine eindeutige Kennung, die den Zweck des Subagent beschreibt (z. B. `code-reviewer`, `api-designer`).
    * Wann Claude diesen Agent verwenden sollte
    * Welche Tools er verwenden kann
    * Ein System-Prompt, der die Rolle und das Verhalten des Agents beschreibt
  </Step>
</Steps>

<Tip>
  Tipps:

  * Erstellen Sie projektspezifische Subagents in `.claude/agents/` zum Teilen im Team
  * Verwenden Sie beschreibende `description`-Felder, um automatische Delegation zu ermöglichen
  * Begrenzen Sie den Tool-Zugriff auf das, was jeder Subagent tatsächlich benötigt
  * Überprüfen Sie die [Subagents-Dokumentation](/de/sub-agents) für detaillierte Beispiele
</Tip>

***

## Plan Mode für sichere Code-Analyse verwenden

Plan Mode weist Claude an, einen Plan zu erstellen, indem die Codebase mit schreibgeschützten Operationen analysiert wird. Dies ist perfekt zum Erkunden von Codebases, Planen komplexer Änderungen oder sicheren Überprüfen von Code. Im Plan Mode verwendet Claude [`AskUserQuestion`](/de/tools-reference), um Anforderungen zu sammeln und Ihre Ziele zu klären, bevor ein Plan vorgeschlagen wird.

### Wann Plan Mode verwendet werden sollte

* **Multi-Schritt-Implementierung**: Wenn Ihre Funktion Änderungen an vielen Dateien erfordert
* **Code-Exploration**: Wenn Sie die Codebase gründlich erforschen möchten, bevor Sie etwas ändern
* **Interaktive Entwicklung**: Wenn Sie die Richtung mit Claude iterieren möchten

### Wie Plan Mode verwendet wird

**Aktivieren Sie Plan Mode während einer Sitzung**

Sie können während einer Sitzung mit **Shift+Tab** in Plan Mode wechseln, um durch Berechtigungsmodi zu zyklisieren.

Wenn Sie sich im Normal Mode befinden, wechselt **Shift+Tab** zunächst in Auto-Accept Mode, angezeigt durch `⏵⏵ accept edits on` am unteren Rand des Terminals. Ein nachfolgendes **Shift+Tab** wechselt in Plan Mode, angezeigt durch `⏸ plan mode on`.

**Starten Sie eine neue Sitzung im Plan Mode**

Um eine neue Sitzung im Plan Mode zu starten, verwenden Sie das Flag `--permission-mode plan`:

```bash  theme={null}
claude --permission-mode plan
```

**Führen Sie „Headless"-Abfragen im Plan Mode aus**

Sie können auch eine Abfrage im Plan Mode direkt mit `-p` ausführen (d. h. im ["Headless-Modus"](/de/headless)):

```bash  theme={null}
claude --permission-mode plan -p "Analyze the authentication system and suggest improvements"
```

### Beispiel: Planen einer komplexen Refaktorierung

```bash  theme={null}
claude --permission-mode plan
```

```text  theme={null}
I need to refactor our authentication system to use OAuth2. Create a detailed migration plan.
```

Claude analysiert die aktuelle Implementierung und erstellt einen umfassenden Plan. Verfeinern Sie mit Folgefragen:

```text  theme={null}
What about backward compatibility?
```

```text  theme={null}
How should we handle database migration?
```

<Tip>Drücken Sie `Ctrl+G`, um den Plan in Ihrem Standard-Texteditor zu öffnen, wo Sie ihn direkt bearbeiten können, bevor Claude fortfährt.</Tip>

### Konfigurieren Sie Plan Mode als Standard

```json  theme={null}
// .claude/settings.json
{
  "permissions": {
    "defaultMode": "plan"
  }
}
```

Weitere Konfigurationsoptionen finden Sie in der [Einstellungsdokumentation](/de/settings#available-settings).

***

## Mit Tests arbeiten

Angenommen, Sie müssen Tests für nicht abgedeckten Code hinzufügen.

<Steps>
  <Step title="Identifizieren Sie nicht getesteten Code">
    ```text  theme={null}
    find functions in NotificationsService.swift that are not covered by tests
    ```
  </Step>

  <Step title="Generieren Sie Test-Gerüste">
    ```text  theme={null}
    add tests for the notification service
    ```
  </Step>

  <Step title="Fügen Sie aussagekräftige Testfälle hinzu">
    ```text  theme={null}
    add test cases for edge conditions in the notification service
    ```
  </Step>

  <Step title="Führen Sie Tests aus und überprüfen Sie sie">
    ```text  theme={null}
    run the new tests and fix any failures
    ```
  </Step>
</Steps>

Claude kann Tests generieren, die den vorhandenen Mustern und Konventionen Ihres Projekts entsprechen. Seien Sie beim Anfordern von Tests spezifisch darüber, welches Verhalten Sie überprüfen möchten. Claude untersucht Ihre vorhandenen Testdateien, um den Stil, die Frameworks und die Assertion-Muster zu entsprechen, die bereits verwendet werden.

Für umfassende Abdeckung bitten Sie Claude, Grenzfälle zu identifizieren, die Sie möglicherweise übersehen haben. Claude kann Ihre Code-Pfade analysieren und Tests für Fehlerbedingungen, Grenzwerte und unerwartete Eingaben vorschlagen, die leicht zu übersehen sind.

***

## Pull Requests erstellen

Sie können Pull Requests erstellen, indem Sie Claude direkt fragen („create a pr for my changes"), oder Claude Schritt für Schritt führen:

<Steps>
  <Step title="Fassen Sie Ihre Änderungen zusammen">
    ```text  theme={null}
    summarize the changes I've made to the authentication module
    ```
  </Step>

  <Step title="Generieren Sie einen Pull Request">
    ```text  theme={null}
    create a pr
    ```
  </Step>

  <Step title="Überprüfen und verfeinern Sie">
    ```text  theme={null}
    enhance the PR description with more context about the security improvements
    ```
  </Step>
</Steps>

Wenn Sie einen PR mit `gh pr create` erstellen, wird die Sitzung automatisch mit diesem PR verknüpft. Sie können sie später mit `claude --from-pr <number>` fortsetzen.

<Tip>
  Überprüfen Sie den von Claude generierten PR vor dem Einreichen und bitten Sie Claude, potenzielle Risiken oder Überlegungen hervorzuheben.
</Tip>

## Dokumentation verwalten

Angenommen, Sie müssen Dokumentation für Ihren Code hinzufügen oder aktualisieren.

<Steps>
  <Step title="Identifizieren Sie nicht dokumentierten Code">
    ```text  theme={null}
    find functions without proper JSDoc comments in the auth module
    ```
  </Step>

  <Step title="Generieren Sie Dokumentation">
    ```text  theme={null}
    add JSDoc comments to the undocumented functions in auth.js
    ```
  </Step>

  <Step title="Überprüfen und verbessern Sie">
    ```text  theme={null}
    improve the generated documentation with more context and examples
    ```
  </Step>

  <Step title="Überprüfen Sie die Dokumentation">
    ```text  theme={null}
    check if the documentation follows our project standards
    ```
  </Step>
</Steps>

<Tip>
  Tipps:

  * Geben Sie den Dokumentationsstil an, den Sie möchten (JSDoc, Docstrings usw.)
  * Fordern Sie Beispiele in der Dokumentation an
  * Fordern Sie Dokumentation für öffentliche APIs, Schnittstellen und komplexe Logik an
</Tip>

***

## Mit Bildern arbeiten

Angenommen, Sie müssen mit Bildern in Ihrer Codebase arbeiten und möchten Claudes Hilfe bei der Analyse von Bildinhalten.

<Steps>
  <Step title="Fügen Sie ein Bild zum Gespräch hinzu">
    Sie können eine dieser Methoden verwenden:

    1. Ziehen Sie ein Bild per Drag & Drop in das Claude Code-Fenster
    2. Kopieren Sie ein Bild und fügen Sie es in die CLI mit Strg+V ein (verwenden Sie nicht Cmd+V)
    3. Geben Sie Claude einen Bildpfad an. Z. B. „Analyze this image: /path/to/your/image.png"
  </Step>

  <Step title="Bitten Sie Claude, das Bild zu analysieren">
    ```text  theme={null}
    What does this image show?
    ```

    ```text  theme={null}
    Describe the UI elements in this screenshot
    ```

    ```text  theme={null}
    Are there any problematic elements in this diagram?
    ```
  </Step>

  <Step title="Verwenden Sie Bilder für Kontext">
    ```text  theme={null}
    Here's a screenshot of the error. What's causing it?
    ```

    ```text  theme={null}
    This is our current database schema. How should we modify it for the new feature?
    ```
  </Step>

  <Step title="Erhalten Sie Code-Vorschläge aus visuellem Inhalt">
    ```text  theme={null}
    Generate CSS to match this design mockup
    ```

    ```text  theme={null}
    What HTML structure would recreate this component?
    ```
  </Step>
</Steps>

<Tip>
  Tipps:

  * Verwenden Sie Bilder, wenn Textbeschreibungen unklar oder umständlich wären
  * Fügen Sie Screenshots von Fehlern, UI-Designs oder Diagrammen für besseren Kontext ein
  * Sie können mehrere Bilder in einem Gespräch verwenden
  * Die Bildanalyse funktioniert mit Diagrammen, Screenshots, Mockups und mehr
  * Wenn Claude auf Bilder verweist (z. B. `[Image #1]`), `Cmd+Click` (Mac) oder `Ctrl+Click` (Windows/Linux) den Link, um das Bild in Ihrem Standard-Viewer zu öffnen
</Tip>

***

## Dateien und Verzeichnisse referenzieren

Verwenden Sie @, um schnell Dateien oder Verzeichnisse einzubeziehen, ohne auf Claude zu warten, um sie zu lesen.

<Steps>
  <Step title="Referenzieren Sie eine einzelne Datei">
    ```text  theme={null}
    Explain the logic in @src/utils/auth.js
    ```

    Dies fügt den vollständigen Inhalt der Datei in das Gespräch ein.
  </Step>

  <Step title="Referenzieren Sie ein Verzeichnis">
    ```text  theme={null}
    What's the structure of @src/components?
    ```

    Dies bietet eine Verzeichnisauflistung mit Dateiinformationen.
  </Step>

  <Step title="Referenzieren Sie MCP-Ressourcen">
    ```text  theme={null}
    Show me the data from @github:repos/owner/repo/issues
    ```

    Dies ruft Daten von verbundenen MCP-Servern im Format @server:resource ab. Weitere Details finden Sie unter [MCP-Ressourcen](/de/mcp#use-mcp-resources).
  </Step>
</Steps>

<Tip>
  Tipps:

  * Dateipfade können relativ oder absolut sein
  * @ Dateireferenzen fügen `CLAUDE.md` im Verzeichnis der Datei und übergeordneten Verzeichnissen zum Kontext hinzu
  * Verzeichnisreferenzen zeigen Dateiauflistungen, keine Inhalte
  * Sie können mehrere Dateien in einer einzelnen Nachricht referenzieren (z. B. „@file1.js and @file2.js")
</Tip>

***

## Verwenden Sie erweitertes Denken (Thinking Mode)

[Erweitertes Denken](https://platform.claude.com/docs/en/build-with-claude/extended-thinking) ist standardmäßig aktiviert und gibt Claude Platz, um komplexe Probleme Schritt für Schritt zu durchdenken, bevor er antwortet. Dieses Denken ist im ausführlichen Modus sichtbar, den Sie mit `Ctrl+O` umschalten können.

Darüber hinaus unterstützen Opus 4.6 und Sonnet 4.6 adaptives Denken: Anstelle eines festen Thinking-Token-Budgets weist das Modell Thinking dynamisch basierend auf Ihrer [Effort-Level](/de/model-config#adjust-effort-level)-Einstellung zu. Erweitertes Denken und adaptives Denken arbeiten zusammen, um Ihnen Kontrolle darüber zu geben, wie tief Claude denkt, bevor er antwortet.

Erweitertes Denken ist besonders wertvoll für komplexe architektonische Entscheidungen, schwierige Fehler, mehrstufige Implementierungsplanung und Bewertung von Kompromissen zwischen verschiedenen Ansätzen.

<Note>
  Phrasen wie „think", „think hard" und „think more" werden als reguläre Prompt-Anweisungen interpretiert und weisen keine Thinking-Tokens zu.
</Note>

### Konfigurieren Sie Thinking Mode

Thinking ist standardmäßig aktiviert, aber Sie können es anpassen oder deaktivieren.

| Bereich                        | Wie man konfiguriert                                                                                            | Details                                                                                                                                                                                         |
| ------------------------------ | --------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Effort Level**               | Führen Sie `/effort` aus, passen Sie in `/model` an, oder setzen Sie [`CLAUDE_CODE_EFFORT_LEVEL`](/de/env-vars) | Steuern Sie die Thinking-Tiefe für Opus 4.6 und Sonnet 4.6. Siehe [Effort Level anpassen](/de/model-config#adjust-effort-level)                                                                 |
| **`ultrathink` Schlüsselwort** | Fügen Sie „ultrathink" irgendwo in Ihrem Prompt ein                                                             | Setzt Effort auf high für diesen Turn auf Opus 4.6 und Sonnet 4.6. Nützlich für einmalige Aufgaben, die tiefes Denken erfordern, ohne Ihre Effort-Einstellung dauerhaft zu ändern               |
| **Toggle-Verknüpfung**         | Drücken Sie `Option+T` (macOS) oder `Alt+T` (Windows/Linux)                                                     | Schalten Sie Thinking für die aktuelle Sitzung ein/aus (alle Modelle). Kann [Terminal-Konfiguration](/de/terminal-config) erfordern, um Option-Tasten-Verknüpfungen zu aktivieren               |
| **Globaler Standard**          | Verwenden Sie `/config`, um Thinking Mode umzuschalten                                                          | Setzt Ihren Standard über alle Projekte (alle Modelle).<br />Gespeichert als `alwaysThinkingEnabled` in `~/.claude/settings.json`                                                               |
| **Token-Budget begrenzen**     | Setzen Sie die Umgebungsvariable [`MAX_THINKING_TOKENS`](/de/env-vars)                                          | Begrenzen Sie das Thinking-Budget auf eine bestimmte Anzahl von Tokens (ignoriert auf Opus 4.6 und Sonnet 4.6, es sei denn, es ist auf 0 gesetzt). Beispiel: `export MAX_THINKING_TOKENS=10000` |

Um Claudes Thinking-Prozess anzuzeigen, drücken Sie `Ctrl+O`, um den ausführlichen Modus umzuschalten und das interne Denken als grauer kursiver Text angezeigt zu sehen.

### Wie erweitertes Denken funktioniert

Erweitertes Denken steuert, wie viel internes Denken Claude vor der Antwort durchführt. Mehr Denken bietet mehr Platz, um Lösungen zu erkunden, Grenzfälle zu analysieren und Fehler selbst zu korrigieren.

**Mit Opus 4.6 und Sonnet 4.6** verwendet Thinking adaptives Denken: Das Modell weist Thinking-Tokens dynamisch basierend auf dem [Effort Level](/de/model-config#adjust-effort-level) zu, den Sie auswählen. Dies ist die empfohlene Methode, um den Kompromiss zwischen Geschwindigkeit und Reasoning-Tiefe zu optimieren.

**Mit älteren Modellen** verwendet Thinking ein festes Budget von bis zu 31.999 Tokens aus Ihrem Output-Budget. Sie können dies mit der Umgebungsvariable [`MAX_THINKING_TOKENS`](/de/env-vars) begrenzen oder Thinking vollständig über `/config` oder den `Option+T`/`Alt+T`-Toggle deaktivieren.

`MAX_THINKING_TOKENS` wird auf Opus 4.6 und Sonnet 4.6 ignoriert, da adaptives Denken stattdessen die Thinking-Tiefe steuert. Die eine Ausnahme: Das Setzen von `MAX_THINKING_TOKENS=0` deaktiviert Thinking immer noch vollständig auf jedem Modell. Um adaptives Thinking zu deaktivieren und zum festen Thinking-Budget zurückzukehren, setzen Sie `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. Siehe [Umgebungsvariablen](/de/env-vars).

<Warning>
  Ihnen werden alle verwendeten Thinking-Tokens berechnet, obwohl Claude 4-Modelle zusammengefasstes Thinking anzeigen
</Warning>

***

## Vorherige Gespräche fortsetzen

Wenn Sie Claude Code starten, können Sie eine vorherige Sitzung fortsetzen:

* `claude --continue` setzt das neueste Gespräch im aktuellen Verzeichnis fort
* `claude --resume` öffnet eine Gesprächsauswahl oder setzt nach Name fort
* `claude --from-pr 123` setzt Sitzungen fort, die mit einem bestimmten Pull Request verknüpft sind

Verwenden Sie innerhalb einer aktiven Sitzung `/resume`, um zu einem anderen Gespräch zu wechseln.

Sitzungen werden pro Projektverzeichnis gespeichert. Die `/resume`-Auswahl zeigt Sitzungen aus demselben Git-Repository, einschließlich Worktrees.

### Benennen Sie Ihre Sitzungen

Geben Sie Sitzungen beschreibende Namen, um sie später zu finden. Dies ist eine Best Practice, wenn Sie an mehreren Aufgaben oder Funktionen arbeiten.

<Steps>
  <Step title="Benennen Sie die Sitzung">
    Benennen Sie eine Sitzung beim Start mit `-n`:

    ```bash  theme={null}
    claude -n auth-refactor
    ```

    Oder verwenden Sie `/rename` während einer Sitzung, was auch den Namen in der Prompt-Leiste anzeigt:

    ```text  theme={null}
    /rename auth-refactor
    ```

    Sie können jede Sitzung auch aus der Auswahl umbenennen: Führen Sie `/resume` aus, navigieren Sie zu einer Sitzung und drücken Sie `R`.
  </Step>

  <Step title="Später nach Name fortsetzen">
    Aus der Befehlszeile:

    ```bash  theme={null}
    claude --resume auth-refactor
    ```

    Oder innerhalb einer aktiven Sitzung:

    ```text  theme={null}
    /resume auth-refactor
    ```
  </Step>
</Steps>

### Verwenden Sie die Sitzungsauswahl

Der Befehl `/resume` (oder `claude --resume` ohne Argumente) öffnet eine interaktive Sitzungsauswahl mit diesen Funktionen:

**Tastaturkürzel in der Auswahl:**

| Verknüpfung | Aktion                                                            |
| :---------- | :---------------------------------------------------------------- |
| `↑` / `↓`   | Navigieren Sie zwischen Sitzungen                                 |
| `→` / `←`   | Erweitern oder reduzieren Sie gruppierte Sitzungen                |
| `Enter`     | Wählen Sie die hervorgehobene Sitzung aus und setzen Sie sie fort |
| `P`         | Zeigen Sie eine Vorschau des Sitzungsinhalts an                   |
| `R`         | Benennen Sie die hervorgehobene Sitzung um                        |
| `/`         | Suchen Sie, um Sitzungen zu filtern                               |
| `A`         | Wechseln Sie zwischen aktuellem Verzeichnis und allen Projekten   |
| `B`         | Filtern Sie nach Sitzungen aus Ihrem aktuellen Git-Branch         |
| `Esc`       | Beenden Sie die Auswahl oder den Suchmodus                        |

**Sitzungsorganisation:**

Die Auswahl zeigt Sitzungen mit hilfreichen Metadaten an:

* Sitzungsname oder anfänglicher Prompt
* Verstrichene Zeit seit letzter Aktivität
* Nachrichtenanzahl
* Git-Branch (falls zutreffend)

Verzweigte Sitzungen (erstellt mit `/rewind` oder `--fork-session`) werden unter ihrer Root-Sitzung gruppiert, was es einfacher macht, verwandte Gespräche zu finden.

<Tip>
  Tipps:

  * **Benennen Sie Sitzungen früh**: Verwenden Sie `/rename`, wenn Sie mit einer bestimmten Aufgabe beginnen – es ist viel einfacher, „payment-integration" später zu finden als „explain this function"
  * Verwenden Sie `--continue` für schnellen Zugriff auf Ihr letztes Gespräch im aktuellen Verzeichnis
  * Verwenden Sie `--resume session-name`, wenn Sie wissen, welche Sitzung Sie benötigen
  * Verwenden Sie `--resume` (ohne Namen), wenn Sie durchsuchen und auswählen müssen
  * Verwenden Sie für Skripte `claude --continue --print "prompt"`, um im nicht-interaktiven Modus fortzufahren
  * Drücken Sie `P` in der Auswahl, um eine Sitzung vor dem Fortsetzen in der Vorschau anzuzeigen
  * Die fortgesetzte Konversation beginnt mit demselben Modell und der gleichen Konfiguration wie das Original

  Wie es funktioniert:

  1. **Gesprächsspeicherung**: Alle Gespräche werden automatisch lokal mit ihrer vollständigen Nachrichtenhistorie gespeichert
  2. **Nachricht-Deserialisierung**: Beim Fortsetzen wird die gesamte Nachrichtenhistorie wiederhergestellt, um den Kontext zu bewahren
  3. **Tool-Status**: Die Tool-Nutzung und Ergebnisse aus dem vorherigen Gespräch werden beibehalten
  4. **Kontext-Wiederherstellung**: Das Gespräch wird mit allen vorherigen Kontexten intakt fortgesetzt
</Tip>

***

## Führen Sie parallele Claude Code-Sitzungen mit Git Worktrees aus

Wenn Sie an mehreren Aufgaben gleichzeitig arbeiten, benötigt jede Claude-Sitzung ihre eigene Kopie der Codebase, damit Änderungen nicht kollidieren. Git Worktrees lösen dies, indem sie separate Arbeitsverzeichnisse erstellen, die jeweils ihre eigenen Dateien und Branches haben, während sie die gleiche Repository-Historie und Remote-Verbindungen teilen. Dies bedeutet, dass Sie Claude an einer Funktion in einem Worktree arbeiten lassen können, während Sie einen Fehler in einem anderen beheben, ohne dass eine Sitzung die andere beeinträchtigt.

Verwenden Sie das Flag `--worktree` (`-w`), um einen isolierten Worktree zu erstellen und Claude darin zu starten. Der Wert, den Sie übergeben, wird zum Worktree-Verzeichnisnamen und Branch-Namen:

```bash  theme={null}
# Starten Sie Claude in einem Worktree namens „feature-auth"
# Erstellt .claude/worktrees/feature-auth/ mit einem neuen Branch
claude --worktree feature-auth

# Starten Sie eine weitere Sitzung in einem separaten Worktree
claude --worktree bugfix-123
```

Wenn Sie den Namen weglassen, generiert Claude automatisch einen zufälligen:

```bash  theme={null}
# Generiert automatisch einen Namen wie „bright-running-fox"
claude --worktree
```

Worktrees werden unter `<repo>/.claude/worktrees/<name>` erstellt und verzweigen sich vom Standard-Remote-Branch. Der Worktree-Branch wird `worktree-<name>` genannt.

Sie können Claude auch während einer Sitzung bitten, „in einem Worktree zu arbeiten" oder „einen Worktree zu starten", und er erstellt automatisch einen.

### Subagent Worktrees

Subagents können auch Worktree-Isolation verwenden, um parallel ohne Konflikte zu arbeiten. Bitten Sie Claude, „Worktrees für Ihre Agents zu verwenden" oder konfigurieren Sie es in einem [benutzerdefinierten Subagent](/de/sub-agents#supported-frontmatter-fields), indem Sie `isolation: worktree` zum Frontmatter des Agents hinzufügen. Jeder Subagent erhält seinen eigenen Worktree, der automatisch bereinigt wird, wenn der Subagent ohne Änderungen beendet wird.

### Worktree-Bereinigung

Wenn Sie eine Worktree-Sitzung beenden, handhabt Claude die Bereinigung basierend darauf, ob Sie Änderungen vorgenommen haben:

* **Keine Änderungen**: Der Worktree und sein Branch werden automatisch entfernt
* **Änderungen oder Commits vorhanden**: Claude fragt Sie, ob Sie den Worktree behalten oder entfernen möchten. Das Behalten bewahrt das Verzeichnis und den Branch, damit Sie später zurückkehren können. Das Entfernen löscht das Worktree-Verzeichnis und seinen Branch und verwirft alle nicht committeten Änderungen und Commits

Um Worktrees außerhalb einer Claude-Sitzung zu bereinigen, verwenden Sie [manuelle Worktree-Verwaltung](#manage-worktrees-manually).

<Tip>
  Fügen Sie `.claude/worktrees/` zu Ihrer `.gitignore` hinzu, um zu verhindern, dass Worktree-Inhalte als nicht verfolgte Dateien in Ihrem Haupt-Repository angezeigt werden.
</Tip>

### Verwalten Sie Worktrees manuell

Für mehr Kontrolle über den Worktree-Speicherort und die Branch-Konfiguration erstellen Sie Worktrees direkt mit Git. Dies ist nützlich, wenn Sie einen bestimmten vorhandenen Branch auschecken oder den Worktree außerhalb des Repositorys platzieren müssen.

```bash  theme={null}
# Erstellen Sie einen Worktree mit einem neuen Branch
git worktree add ../project-feature-a -b feature-a

# Erstellen Sie einen Worktree mit einem vorhandenen Branch
git worktree add ../project-bugfix bugfix-123

# Starten Sie Claude im Worktree
cd ../project-feature-a && claude

# Bereinigen Sie, wenn Sie fertig sind
git worktree list
git worktree remove ../project-feature-a
```

Weitere Informationen finden Sie in der [offiziellen Git Worktree-Dokumentation](https://git-scm.com/docs/git-worktree).

<Tip>
  Denken Sie daran, Ihre Entwicklungsumgebung in jedem neuen Worktree gemäß der Einrichtung Ihres Projekts zu initialisieren. Je nach Ihrem Stack kann dies die Ausführung der Abhängigkeitsinstallation (`npm install`, `yarn`), das Einrichten virtueller Umgebungen oder das Befolgen des Standard-Setup-Prozesses Ihres Projekts umfassen.
</Tip>

### Nicht-Git-Versionskontrolle

Worktree-Isolation funktioniert standardmäßig mit Git. Für andere Versionskontrollsysteme wie SVN, Perforce oder Mercurial konfigurieren Sie [WorktreeCreate und WorktreeRemove Hooks](/de/hooks#worktreecreate), um benutzerdefinierte Worktree-Erstellungs- und Bereinigungslogik bereitzustellen. Wenn konfiguriert, ersetzen diese Hooks das Standard-Git-Verhalten, wenn Sie `--worktree` verwenden.

Für automatisierte Koordination paralleler Sitzungen mit gemeinsamen Aufgaben und Messaging siehe [Agent Teams](/de/agent-teams).

***

## Erhalten Sie Benachrichtigungen, wenn Claude Ihre Aufmerksamkeit benötigt

Wenn Sie eine lange laufende Aufgabe starten und zu einem anderen Fenster wechseln, können Sie Desktop-Benachrichtigungen einrichten, damit Sie wissen, wenn Claude fertig ist oder Ihre Eingabe benötigt. Dies verwendet das `Notification` [Hook-Ereignis](/de/hooks-guide#get-notified-when-claude-needs-input), das immer dann ausgelöst wird, wenn Claude auf Berechtigung wartet, untätig ist und bereit für einen neuen Prompt ist, oder die Authentifizierung abgeschlossen ist.

<Steps>
  <Step title="Fügen Sie den Hook zu Ihren Einstellungen hinzu">
    Öffnen Sie `~/.claude/settings.json` und fügen Sie einen `Notification` Hook hinzu, der den nativen Benachrichtigungsbefehl Ihrer Plattform aufruft:

    <Tabs>
      <Tab title="macOS">
        ```json  theme={null}
        {
          "hooks": {
            "Notification": [
              {
                "matcher": "",
                "hooks": [
                  {
                    "type": "command",
                    "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
                  }
                ]
              }
            ]
          }
        }
        ```
      </Tab>

      <Tab title="Linux">
        ```json  theme={null}
        {
          "hooks": {
            "Notification": [
              {
                "matcher": "",
                "hooks": [
                  {
                    "type": "command",
                    "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
                  }
                ]
              }
            ]
          }
        }
        ```
      </Tab>

      <Tab title="Windows">
        ```json  theme={null}
        {
          "hooks": {
            "Notification": [
              {
                "matcher": "",
                "hooks": [
                  {
                    "type": "command",
                    "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
                  }
                ]
              }
            ]
          }
        }
        ```
      </Tab>
    </Tabs>

    Wenn Ihre Einstellungsdatei bereits einen `hooks`-Schlüssel hat, führen Sie den `Notification`-Eintrag darin zusammen, anstatt ihn zu überschreiben. Sie können Claude auch bitten, den Hook für Sie zu schreiben, indem Sie beschreiben, was Sie in der CLI möchten.
  </Step>

  <Step title="Grenzen Sie den Matcher optional ein">
    Standardmäßig wird der Hook bei allen Benachrichtigungstypen ausgelöst. Um nur für bestimmte Ereignisse ausgelöst zu werden, setzen Sie das Feld `matcher` auf einen dieser Werte:

    | Matcher              | Wird ausgelöst, wenn                                   |
    | :------------------- | :----------------------------------------------------- |
    | `permission_prompt`  | Claude benötigt Ihre Genehmigung für eine Tool-Nutzung |
    | `idle_prompt`        | Claude ist fertig und wartet auf Ihren nächsten Prompt |
    | `auth_success`       | Die Authentifizierung ist abgeschlossen                |
    | `elicitation_dialog` | Claude stellt Ihnen eine Frage                         |
  </Step>

  <Step title="Überprüfen Sie den Hook">
    Geben Sie `/hooks` ein und wählen Sie `Notification` aus, um zu bestätigen, dass der Hook angezeigt wird. Wenn Sie ihn auswählen, wird der Befehl angezeigt, der ausgeführt wird. Um ihn end-to-end zu testen, bitten Sie Claude, einen Befehl auszuführen, der Berechtigung erfordert, und wechseln Sie weg vom Terminal, oder bitten Sie Claude, direkt eine Benachrichtigung auszulösen.
  </Step>
</Steps>

Für das vollständige Ereignisschema und die Benachrichtigungstypen siehe die [Benachrichtigungsreferenz](/de/hooks#notification).

***

## Verwenden Sie Claude als Unix-ähnliches Dienstprogramm

### Fügen Sie Claude zu Ihrem Überprüfungsprozess hinzu

Angenommen, Sie möchten Claude Code als Linter oder Code-Reviewer verwenden.

**Fügen Sie Claude zu Ihrem Build-Skript hinzu:**

```json  theme={null}
// package.json
{
    ...
    "scripts": {
        ...
        "lint:claude": "claude -p 'you are a linter. please look at the changes vs. main and report any issues related to typos. report the filename and line number on one line, and a description of the issue on the second line. do not return any other text.'"
    }
}
```

<Tip>
  Tipps:

  * Verwenden Sie Claude für automatisierte Code-Überprüfung in Ihrer CI/CD-Pipeline
  * Passen Sie den Prompt an, um auf spezifische Probleme zu überprüfen, die für Ihr Projekt relevant sind
  * Erwägen Sie, mehrere Skripte für verschiedene Arten von Überprüfungen zu erstellen
</Tip>

### Pipe in, Pipe out

Angenommen, Sie möchten Daten in Claude pipen und Daten in einem strukturierten Format zurückbekommen.

**Pipen Sie Daten durch Claude:**

```bash  theme={null}
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

<Tip>
  Tipps:

  * Verwenden Sie Pipes, um Claude in vorhandene Shell-Skripte zu integrieren
  * Kombinieren Sie mit anderen Unix-Tools für leistungsstarke Workflows
  * Erwägen Sie die Verwendung von --output-format für strukturierte Ausgabe
</Tip>

### Steuern Sie das Ausgabeformat

Angenommen, Sie benötigen Claudes Ausgabe in einem bestimmten Format, besonders wenn Sie Claude Code in Skripte oder andere Tools integrieren.

<Steps>
  <Step title="Verwenden Sie Textformat (Standard)">
    ```bash  theme={null}
    cat data.txt | claude -p 'summarize this data' --output-format text > summary.txt
    ```

    Dies gibt nur Claudes einfache Textantwort aus (Standardverhalten).
  </Step>

  <Step title="Verwenden Sie JSON-Format">
    ```bash  theme={null}
    cat code.py | claude -p 'analyze this code for bugs' --output-format json > analysis.json
    ```

    Dies gibt ein JSON-Array von Nachrichten mit Metadaten einschließlich Kosten und Dauer aus.
  </Step>

  <Step title="Verwenden Sie Streaming-JSON-Format">
    ```bash  theme={null}
    cat log.txt | claude -p 'parse this log file for errors' --output-format stream-json
    ```

    Dies gibt eine Reihe von JSON-Objekten in Echtzeit aus, während Claude die Anfrage verarbeitet. Jede Nachricht ist ein gültiges JSON-Objekt, aber die gesamte Ausgabe ist kein gültiges JSON, wenn es verkettet wird.
  </Step>
</Steps>

<Tip>
  Tipps:

  * Verwenden Sie `--output-format text` für einfache Integrationen, bei denen Sie nur Claudes Antwort benötigen
  * Verwenden Sie `--output-format json`, wenn Sie das vollständige Gesprächsprotokoll benötigen
  * Verwenden Sie `--output-format stream-json` für Echtzeit-Ausgabe jedes Gesprächsturn
</Tip>

***

## Fragen Sie Claude nach seinen Fähigkeiten

Claude hat integrierten Zugriff auf seine Dokumentation und kann Fragen zu seinen eigenen Funktionen und Einschränkungen beantworten.

### Beispielfragen

```text  theme={null}
can Claude Code create pull requests?
```

```text  theme={null}
how does Claude Code handle permissions?
```

```text  theme={null}
what skills are available?
```

```text  theme={null}
how do I use MCP with Claude Code?
```

```text  theme={null}
how do I configure Claude Code for Amazon Bedrock?
```

```text  theme={null}
what are the limitations of Claude Code?
```

<Note>
  Claude bietet dokumentationsgestützte Antworten auf diese Fragen. Für ausführbare Beispiele und praktische Demonstrationen verweisen Sie auf die spezifischen Workflow-Abschnitte oben.
</Note>

<Tip>
  Tipps:

  * Claude hat immer Zugriff auf die neueste Claude Code-Dokumentation, unabhängig von der Version, die Sie verwenden
  * Stellen Sie spezifische Fragen, um detaillierte Antworten zu erhalten
  * Claude kann komplexe Funktionen wie MCP-Integration, Enterprise-Konfigurationen und erweiterte Workflows erklären
</Tip>

***

## Nächste Schritte

<CardGroup cols={2}>
  <Card title="Best Practices" icon="lightbulb" href="/de/best-practices">
    Muster zum Herausholen des Besten aus Claude Code
  </Card>

  <Card title="Wie Claude Code funktioniert" icon="gear" href="/de/how-claude-code-works">
    Verstehen Sie die agentic Loop und Kontextverwaltung
  </Card>

  <Card title="Erweitern Sie Claude Code" icon="puzzle-piece" href="/de/features-overview">
    Fügen Sie Skills, Hooks, MCP, Subagents und Plugins hinzu
  </Card>

  <Card title="Referenzimplementierung" icon="code" href="https://github.com/anthropics/claude-code/tree/main/.devcontainer">
    Klonen Sie unsere Referenzimplementierung des Development Containers
  </Card>
</CardGroup>
