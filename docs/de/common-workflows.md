> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Häufige Workflows

> Schritt-für-Schritt-Anleitungen zum Erkunden von Codebases, Beheben von Fehlern, Refaktorierung, Testen und anderen alltäglichen Aufgaben mit Claude Code.

Diese Seite sammelt kurze Rezepte für die alltägliche Entwicklung. Für übergeordnete Anleitungen zum Prompting und zur Kontextverwaltung siehe [Best Practices](/de/best-practices).

Diese Seite behandelt:

* [Prompt-Rezepte](#prompt-recipes) zum Erkunden von Code, Beheben von Fehlern, Refaktorierung, Testen, PRs und Dokumentation
* [Vorherige Gespräche fortsetzen](#resume-previous-conversations), damit eine Aufgabe mehrere Sitzungen umfassen kann
* [Parallele Sitzungen mit Worktrees ausführen](#run-parallel-sessions-with-worktrees), damit gleichzeitige Änderungen nicht kollidieren
* [Vor dem Bearbeiten planen](#plan-before-editing), um Änderungen zu überprüfen, bevor sie die Festplatte berühren
* [Forschung an Subagents delegieren](#delegate-research-to-subagents), um Ihren Hauptkontext sauber zu halten
* [Claude in Skripte pipen](#pipe-claude-into-scripts) für CI und Batch-Verarbeitung

## Prompt-Rezepte

Dies sind Prompt-Muster für alltägliche Aufgaben wie das Erkunden unbekannter Code, Debugging, Refaktorierung, Schreiben von Tests und Erstellen von PRs. Jedes funktioniert auf jeder Claude Code-Oberfläche; passen Sie die Formulierung an Ihr Projekt an.

### Neue Codebases verstehen

#### Schnelle Codebase-Übersicht erhalten

Angenommen, Sie sind gerade einem neuen Projekt beigetreten und müssen dessen Struktur schnell verstehen.

<Steps>
  <Step title="Navigieren Sie zum Projektroot-Verzeichnis">
    ```bash theme={null}
    cd /path/to/project 
    ```
  </Step>

  <Step title="Starten Sie Claude Code">
    ```bash theme={null}
    claude 
    ```
  </Step>

  <Step title="Fragen Sie nach einer Übersicht auf hoher Ebene">
    ```text theme={null}
    give me an overview of this codebase
    ```
  </Step>

  <Step title="Tauchen Sie tiefer in spezifische Komponenten ein">
    ```text theme={null}
    explain the main architecture patterns used here
    ```

    ```text theme={null}
    what are the key data models?
    ```

    ```text theme={null}
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

#### Relevanten Code finden

Angenommen, Sie müssen Code finden, der sich auf eine bestimmte Funktion oder Funktionalität bezieht.

<Steps>
  <Step title="Bitten Sie Claude, relevante Dateien zu finden">
    ```text theme={null}
    find the files that handle user authentication
    ```
  </Step>

  <Step title="Erhalten Sie Kontext darüber, wie Komponenten zusammenwirken">
    ```text theme={null}
    how do these authentication files work together?
    ```
  </Step>

  <Step title="Verstehen Sie den Ausführungsfluss">
    ```text theme={null}
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

### Fehler effizient beheben

Angenommen, Sie sind auf eine Fehlermeldung gestoßen und müssen deren Quelle finden und beheben.

<Steps>
  <Step title="Teilen Sie den Fehler mit Claude">
    ```text theme={null}
    I'm seeing an error when I run npm test
    ```
  </Step>

  <Step title="Fragen Sie nach Behebungsempfehlungen">
    ```text theme={null}
    suggest a few ways to fix the @ts-ignore in user.ts
    ```
  </Step>

  <Step title="Wenden Sie die Behebung an">
    ```text theme={null}
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

### Code refaktorieren

Angenommen, Sie müssen alten Code aktualisieren, um moderne Muster und Praktiken zu verwenden.

<Steps>
  <Step title="Identifizieren Sie Legacy-Code zur Refaktorierung">
    ```text theme={null}
    find deprecated API usage in our codebase
    ```
  </Step>

  <Step title="Erhalten Sie Refaktorierungsempfehlungen">
    ```text theme={null}
    suggest how to refactor utils.js to use modern JavaScript features
    ```
  </Step>

  <Step title="Wenden Sie die Änderungen sicher an">
    ```text theme={null}
    refactor utils.js to use ES2024 features while maintaining the same behavior
    ```
  </Step>

  <Step title="Überprüfen Sie die Refaktorierung">
    ```text theme={null}
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

### Mit Tests arbeiten

Angenommen, Sie müssen Tests für nicht abgedeckten Code hinzufügen.

<Steps>
  <Step title="Identifizieren Sie nicht getesteten Code">
    ```text theme={null}
    find functions in NotificationsService.swift that are not covered by tests
    ```
  </Step>

  <Step title="Generieren Sie Test-Gerüste">
    ```text theme={null}
    add tests for the notification service
    ```
  </Step>

  <Step title="Fügen Sie aussagekräftige Testfälle hinzu">
    ```text theme={null}
    add test cases for edge conditions in the notification service
    ```
  </Step>

  <Step title="Führen Sie Tests aus und überprüfen Sie sie">
    ```text theme={null}
    run the new tests and fix any failures
    ```
  </Step>
</Steps>

Claude kann Tests generieren, die den vorhandenen Mustern und Konventionen Ihres Projekts entsprechen. Seien Sie beim Anfordern von Tests spezifisch darüber, welches Verhalten Sie überprüfen möchten. Claude untersucht Ihre vorhandenen Testdateien, um den Stil, die Frameworks und die Assertion-Muster zu entsprechen, die bereits verwendet werden.

Für umfassende Abdeckung bitten Sie Claude, Grenzfälle zu identifizieren, die Sie möglicherweise übersehen haben. Claude kann Ihre Code-Pfade analysieren und Tests für Fehlerbedingungen, Grenzwerte und unerwartete Eingaben vorschlagen, die leicht zu übersehen sind.

***

### Pull Requests erstellen

Sie können Pull Requests erstellen, indem Sie Claude direkt fragen ('create a pr for my changes"), oder Claude Schritt für Schritt führen:

<Steps>
  <Step title="Fassen Sie Ihre Änderungen zusammen">
    ```text theme={null}
    summarize the changes I've made to the authentication module
    ```
  </Step>

  <Step title="Generieren Sie einen Pull Request">
    ```text theme={null}
    create a pr
    ```
  </Step>

  <Step title="Überprüfen und verfeinern Sie">
    ```text theme={null}
    enhance the PR description with more context about the security improvements
    ```
  </Step>
</Steps>

Wenn Sie einen PR mit `gh pr create` erstellen, wird die Sitzung automatisch mit diesem PR verknüpft. Um später zu ihr zurückzukehren, führen Sie `claude --from-pr <number>` aus oder fügen Sie die PR-URL in die [`/resume` Auswahl](/de/sessions#use-the-session-picker) ein.

<Tip>
  Überprüfen Sie den von Claude generierten PR vor dem Einreichen und bitten Sie Claude, potenzielle Risiken oder Überlegungen hervorzuheben.
</Tip>

### Dokumentation verwalten

Angenommen, Sie müssen Dokumentation für Ihren Code hinzufügen oder aktualisieren.

<Steps>
  <Step title="Identifizieren Sie nicht dokumentierten Code">
    ```text theme={null}
    find functions without proper JSDoc comments in the auth module
    ```
  </Step>

  <Step title="Generieren Sie Dokumentation">
    ```text theme={null}
    add JSDoc comments to the undocumented functions in auth.js
    ```
  </Step>

  <Step title="Überprüfen und verbessern Sie">
    ```text theme={null}
    improve the generated documentation with more context and examples
    ```
  </Step>

  <Step title="Überprüfen Sie die Dokumentation">
    ```text theme={null}
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

### Mit Notizen und Nicht-Code-Ordnern arbeiten

Claude Code funktioniert in jedem Verzeichnis. Führen Sie es in einem Notiz-Vault, einem Dokumentationsordner oder einer beliebigen Sammlung von Markdown-Dateien aus, um Inhalte auf die gleiche Weise zu suchen, zu bearbeiten und zu reorganisieren wie Code.

Das Verzeichnis `.claude/` und `CLAUDE.md` befinden sich neben den Konfigurationsverzeichnissen anderer Tools ohne Konflikte. Claude liest Dateien bei jedem Tool-Aufruf neu, daher sieht es Änderungen, die Sie in einer anderen Anwendung vornehmen, beim nächsten Lesen dieser Datei.

***

### Mit Bildern arbeiten

Angenommen, Sie müssen mit Bildern in Ihrer Codebase arbeiten und möchten Claudes Hilfe bei der Analyse von Bildinhalten.

<Steps>
  <Step title="Fügen Sie ein Bild zum Gespräch hinzu">
    Sie können eine dieser Methoden verwenden:

    1. Ziehen Sie ein Bild per Drag & Drop in das Claude Code-Fenster
    2. Kopieren Sie ein Bild und fügen Sie es in die CLI mit Strg+V ein (verwenden Sie nicht Cmd+V)
    3. Geben Sie Claude einen Bildpfad an. Z. B. „Analyze this image: /path/to/your/image.png"
  </Step>

  <Step title="Bitten Sie Claude, das Bild zu analysieren">
    ```text theme={null}
    What does this image show?
    ```

    ```text theme={null}
    Describe the UI elements in this screenshot
    ```

    ```text theme={null}
    Are there any problematic elements in this diagram?
    ```
  </Step>

  <Step title="Verwenden Sie Bilder für Kontext">
    ```text theme={null}
    Here's a screenshot of the error. What's causing it?
    ```

    ```text theme={null}
    This is our current database schema. How should we modify it for the new feature?
    ```
  </Step>

  <Step title="Erhalten Sie Code-Vorschläge aus visuellem Inhalt">
    ```text theme={null}
    Generate CSS to match this design mockup
    ```

    ```text theme={null}
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

### Dateien und Verzeichnisse referenzieren

Verwenden Sie @ um schnell Dateien oder Verzeichnisse einzubeziehen, ohne auf Claude zu warten, um sie zu lesen.

<Steps>
  <Step title="Referenzieren Sie eine einzelne Datei">
    ```text theme={null}
    Explain the logic in @src/utils/auth.js
    ```

    Dies fügt den vollständigen Inhalt der Datei in das Gespräch ein.
  </Step>

  <Step title="Referenzieren Sie ein Verzeichnis">
    ```text theme={null}
    What's the structure of @src/components?
    ```

    Dies bietet eine Verzeichnisauflistung mit Dateiinformationen.
  </Step>

  <Step title="Referenzieren Sie MCP-Ressourcen">
    ```text theme={null}
    Show me the data from @github:repos/owner/repo/issues
    ```

    Dies ruft Daten von verbundenen MCP-Servern im Format @server:resource ab. Siehe [MCP-Ressourcen](/de/mcp#use-mcp-resources) für Details.
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

### Claude nach einem Zeitplan ausführen

Angenommen, Sie möchten Claude automatisch eine Aufgabe auf wiederkehrender Basis ausführen, z. B. offene PRs jeden Morgen überprüfen, Abhängigkeiten wöchentlich prüfen oder über Nacht auf CI-Fehler überprüfen.

Wählen Sie eine Planungsoption basierend darauf, wo Sie die Aufgabe ausführen möchten:

| Option                                                   | Wo es ausgeführt wird                  | Am besten für                                                                                                                                                                                                                                                                   |
| :------------------------------------------------------- | :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Routines](/de/routines)                                 | Von Anthropic verwaltete Infrastruktur | Aufgaben, die auch dann ausgeführt werden sollten, wenn Ihr Computer ausgeschaltet ist. Können auch durch API-Aufrufe oder GitHub-Ereignisse zusätzlich zu einem Zeitplan ausgelöst werden. Konfigurieren Sie unter [claude.ai/code/routines](https://claude.ai/code/routines). |
| [Desktop-geplante Aufgaben](/de/desktop-scheduled-tasks) | Ihr Computer, über die Desktop-App     | Aufgaben, die direkten Zugriff auf lokale Dateien, Tools oder nicht committete Änderungen benötigen.                                                                                                                                                                            |
| [GitHub Actions](/de/github-actions)                     | Ihre CI-Pipeline                       | Aufgaben, die an Repository-Ereignisse wie geöffnete PRs gebunden sind, oder Cron-Zeitpläne, die neben Ihrer Workflow-Konfiguration leben sollten.                                                                                                                              |
| [`/loop`](/de/scheduled-tasks)                           | Die aktuelle CLI-Sitzung               | Schnelle Abfragen während eine Sitzung offen ist. Aufgaben werden abgebrochen, wenn Sie beenden.                                                                                                                                                                                |

<Tip>
  Wenn Sie Prompts für geplante Aufgaben schreiben, seien Sie explizit darüber, wie Erfolg aussieht und was mit Ergebnissen zu tun ist. Die Aufgabe wird autonom ausgeführt, daher kann sie keine Klärungsfragen stellen. Beispiel: „Überprüfen Sie offene PRs mit dem Label `needs-review`, hinterlassen Sie Inline-Kommentare zu Problemen und posten Sie eine Zusammenfassung im `#eng-reviews` Slack-Kanal."
</Tip>

***

### Fragen Sie Claude nach seinen Fähigkeiten

Claude hat integrierten Zugriff auf seine Dokumentation und kann Fragen zu seinen eigenen Funktionen und Einschränkungen beantworten.

#### Beispielfragen

```text theme={null}
can Claude Code create pull requests?
```

```text theme={null}
how does Claude Code handle permissions?
```

```text theme={null}
what skills are available?
```

```text theme={null}
how do I use MCP with Claude Code?
```

```text theme={null}
how do I configure Claude Code for Amazon Bedrock?
```

```text theme={null}
what are the limitations of Claude Code?
```

<Note>
  Claude bietet dokumentationsgestützte Antworten auf diese Fragen. Für praktische Demonstrationen führen Sie `/powerup` für interaktive Lektionen mit animierten Demos aus, oder beziehen Sie sich auf die spezifischen Workflow-Abschnitte oben.
</Note>

<Tip>
  Tipps:

  * Claude hat immer Zugriff auf die neueste Claude Code-Dokumentation, unabhängig von der Version, die Sie verwenden
  * Stellen Sie spezifische Fragen, um detaillierte Antworten zu erhalten
  * Claude kann komplexe Funktionen wie MCP-Integration, Enterprise-Konfigurationen und erweiterte Workflows erklären
</Tip>

***

## Vorherige Gespräche fortsetzen

Wenn eine Aufgabe mehrere Sitzungen umfasst, setzen Sie dort fort, wo Sie aufgehört haben, anstatt den Kontext erneut zu erklären. Claude Code speichert jedes Gespräch lokal.

```bash theme={null}
claude --continue
```

Dies setzt die neueste Sitzung im aktuellen Verzeichnis fort; wenn es noch keine gibt, wird `No conversation found to continue` gedruckt und das Programm beendet. Verwenden Sie `claude --resume`, um aus einer Liste auszuwählen, oder `/resume` innerhalb einer laufenden Sitzung. Siehe [Sitzungen verwalten](/de/sessions) für Benennung, Verzweigung und die vollständige Auswahl-Referenz.

## Parallele Sitzungen mit Worktrees ausführen

Arbeiten Sie an einer Funktion in einem Terminal, während Claude einen Fehler in einem anderen behebt, ohne dass die Änderungen kollidieren. Jeder Worktree ist ein separater Checkout auf seinem eigenen Branch.

```bash theme={null}
claude --worktree feature-auth
```

Führen Sie denselben Befehl mit einem anderen Namen in einem zweiten Terminal aus, um eine isolierte parallele Sitzung zu starten. Siehe [Worktrees](/de/worktrees) für Bereinigung, `.worktreeinclude` und Unterstützung für nicht-Git-VCS. Um parallele Sitzungen von einem Bildschirm aus zu überwachen, anstatt separate Terminals zu verwenden, siehe [Background Agents](/de/agent-view).

## Vor dem Bearbeiten planen

Für Änderungen, die Sie überprüfen möchten, bevor sie die Festplatte berühren, wechseln Sie in den Plan Mode. Claude liest Dateien und schlägt einen Plan vor, macht aber keine Änderungen, bis Sie zustimmen.

```bash theme={null}
claude --permission-mode plan
```

Sie können auch `Shift+Tab` während einer Sitzung drücken, um in den Plan Mode zu wechseln. Siehe [Plan Mode](/de/permission-modes#analyze-before-you-edit-with-plan-mode) für den Genehmigungsfluss und das Bearbeiten des Plans in Ihrem Text-Editor.

## Forschung an Subagents delegieren

Das Erkunden einer großen Codebase füllt Ihren Kontext mit Dateilesevorgängen. Delegieren Sie die Erkundung, damit nur die Ergebnisse zurückkommen.

```text theme={null}
use a subagent to investigate how our auth system handles token refresh
```

Der Subagent liest Dateien in seinem eigenen Kontextfenster und meldet eine Zusammenfassung. Siehe [Subagents](/de/sub-agents) für die Definition benutzerdefinierter Agents mit ihren eigenen Tools und Prompts.

## Claude in Skripte pipen

Führen Sie Claude nicht-interaktiv für CI, Pre-Commit-Hooks oder Batch-Verarbeitung aus. Stdin und Stdout funktionieren wie jedes Unix-Tool.

```bash theme={null}
git log --oneline -20 | claude -p "summarize these recent commits"
```

Siehe [Non-Interactive Mode](/de/headless) für Ausgabeformate, Berechtigungsflags und Fan-Out-Muster.

## Nächste Schritte

<CardGroup cols={2}>
  <Card title="Best Practices" icon="lightbulb" href="/de/best-practices">
    Muster zum Herausholen des Besten aus Claude Code
  </Card>

  <Card title="Sitzungen verwalten" icon="rotate-left" href="/de/sessions">
    Fortsetzen, Benennen und Verzweigen von Gesprächen
  </Card>

  <Card title="Worktrees" icon="code-branch" href="/de/worktrees">
    Führen Sie isolierte parallele Sitzungen aus
  </Card>

  <Card title="Claude Code erweitern" icon="puzzle-piece" href="/de/features-overview">
    Fügen Sie Skills, Hooks, MCP, Subagents und Plugins hinzu
  </Card>
</CardGroup>
