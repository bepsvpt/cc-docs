> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Schnellstart

> Willkommen bei Claude Code!

Diese Schnellstartanleitung ermöglicht es Ihnen, in wenigen Minuten KI-gestützte Codierungshilfe zu nutzen. Am Ende werden Sie verstehen, wie Sie Claude Code für häufige Entwicklungsaufgaben einsetzen.

## Bevor Sie beginnen

Stellen Sie sicher, dass Sie folgende Voraussetzungen erfüllen:

* Ein offenes Terminal oder eine offene Eingabeaufforderung
  * Wenn Sie das Terminal noch nie verwendet haben, lesen Sie den [Terminal-Leitfaden](/de/terminal-guide)
* Ein Codeprojekt zum Arbeiten
* Ein [Claude-Abonnement](https://claude.com/pricing) (Pro, Max, Teams oder Enterprise), ein [Claude Console](https://console.anthropic.com/)-Konto oder Zugriff über einen [unterstützten Cloud-Anbieter](/de/third-party-integrations)

<Note>
  Diese Anleitung behandelt die Terminal-CLI. Claude Code ist auch im [Web](https://claude.ai/code) verfügbar, als [Desktop-App](/de/desktop), in [VS Code](/de/vs-code) und [JetBrains IDEs](/de/jetbrains), in [Slack](/de/slack) und in CI/CD mit [GitHub Actions](/de/github-actions) und [GitLab](/de/gitlab-ci-cd). Siehe [alle Schnittstellen](/de/overview#use-claude-code-everywhere).
</Note>

## Schritt 1: Claude Code installieren

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell  theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

## Schritt 2: Melden Sie sich bei Ihrem Konto an

Claude Code erfordert ein Konto zur Nutzung. Wenn Sie eine interaktive Sitzung mit dem Befehl `claude` starten, müssen Sie sich anmelden:

```bash  theme={null}
claude
# Sie werden beim ersten Gebrauch aufgefordert, sich anzumelden
```

```bash  theme={null}
/login
# Folgen Sie den Aufforderungen, um sich mit Ihrem Konto anzumelden
```

Sie können sich mit einem dieser Kontotypen anmelden:

* [Claude Pro, Max, Teams oder Enterprise](https://claude.com/pricing) (empfohlen)
* [Claude Console](https://console.anthropic.com/) (API-Zugriff mit Prepaid-Guthaben). Bei der ersten Anmeldung wird automatisch ein „Claude Code"-Arbeitsbereich in der Console erstellt, um die Kosten zentral zu verfolgen.
* [Amazon Bedrock, Google Vertex AI oder Microsoft Foundry](/de/third-party-integrations) (Enterprise-Cloud-Anbieter)

Nach der Anmeldung werden Ihre Anmeldedaten gespeichert und Sie müssen sich nicht erneut anmelden. Um später zu einem anderen Konto zu wechseln, verwenden Sie den Befehl `/login`.

## Schritt 3: Starten Sie Ihre erste Sitzung

Öffnen Sie Ihr Terminal in einem beliebigen Projektverzeichnis und starten Sie Claude Code:

```bash  theme={null}
cd /path/to/your/project
claude
```

Sie sehen den Claude Code-Willkommensbildschirm mit Ihren Sitzungsinformationen, kürzlichen Unterhaltungen und den neuesten Updates. Geben Sie `/help` ein, um verfügbare Befehle anzuzeigen, oder `/resume`, um eine vorherige Unterhaltung fortzusetzen.

<Tip>
  Nach der Anmeldung (Schritt 2) werden Ihre Anmeldedaten auf Ihrem System gespeichert. Weitere Informationen finden Sie unter [Verwaltung von Anmeldedaten](/de/authentication#credential-management).
</Tip>

## Schritt 4: Stellen Sie Ihre erste Frage

Beginnen Sie damit, Ihre Codebasis zu verstehen. Versuchen Sie einen dieser Befehle:

```text  theme={null}
what does this project do?
```

Claude wird Ihre Dateien analysieren und eine Zusammenfassung bereitstellen. Sie können auch spezifischere Fragen stellen:

```text  theme={null}
what technologies does this project use?
```

```text  theme={null}
where is the main entry point?
```

```text  theme={null}
explain the folder structure
```

Sie können Claude auch nach seinen eigenen Fähigkeiten fragen:

```text  theme={null}
what can Claude Code do?
```

```text  theme={null}
how do I create custom skills in Claude Code?
```

```text  theme={null}
can Claude Code work with Docker?
```

<Note>
  Claude Code liest Ihre Projektdateien nach Bedarf. Sie müssen den Kontext nicht manuell hinzufügen.
</Note>

## Schritt 5: Nehmen Sie Ihre erste Codeänderung vor

Jetzt lassen Sie Claude Code tatsächlich programmieren. Versuchen Sie eine einfache Aufgabe:

```text  theme={null}
add a hello world function to the main file
```

Claude Code wird:

1. Die entsprechende Datei finden
2. Die vorgeschlagenen Änderungen anzeigen
3. Um Ihre Genehmigung bitten
4. Die Bearbeitung durchführen

<Note>
  Claude Code fragt immer um Erlaubnis, bevor Dateien geändert werden. Sie können einzelne Änderungen genehmigen oder den Modus „Alle akzeptieren" für eine Sitzung aktivieren.
</Note>

## Schritt 6: Verwenden Sie Git mit Claude Code

Claude Code macht Git-Operationen gesprächig:

```text  theme={null}
what files have I changed?
```

```text  theme={null}
commit my changes with a descriptive message
```

Sie können auch komplexere Git-Operationen anfordern:

```text  theme={null}
create a new branch called feature/quickstart
```

```text  theme={null}
show me the last 5 commits
```

```text  theme={null}
help me resolve merge conflicts
```

## Schritt 7: Beheben Sie einen Fehler oder fügen Sie eine Funktion hinzu

Claude ist versiert im Debuggen und in der Implementierung von Funktionen.

Beschreiben Sie, was Sie möchten, in natürlicher Sprache:

```text  theme={null}
add input validation to the user registration form
```

Oder beheben Sie vorhandene Probleme:

```text  theme={null}
there's a bug where users can submit empty forms - fix it
```

Claude Code wird:

* Den relevanten Code lokalisieren
* Den Kontext verstehen
* Eine Lösung implementieren
* Tests ausführen, falls verfügbar

## Schritt 8: Testen Sie andere häufige Arbeitsabläufe

Es gibt verschiedene Möglichkeiten, mit Claude zu arbeiten:

**Code umgestalten**

```text  theme={null}
refactor the authentication module to use async/await instead of callbacks
```

**Tests schreiben**

```text  theme={null}
write unit tests for the calculator functions
```

**Dokumentation aktualisieren**

```text  theme={null}
update the README with installation instructions
```

**Code-Überprüfung**

```text  theme={null}
review my changes and suggest improvements
```

<Tip>
  Sprechen Sie mit Claude wie mit einem hilfreichen Kollegen. Beschreiben Sie, was Sie erreichen möchten, und es wird Ihnen helfen, dorthin zu gelangen.
</Tip>

## Wesentliche Befehle

Hier sind die wichtigsten Befehle für die tägliche Nutzung:

| Befehl              | Was er tut                                              | Beispiel                            |
| ------------------- | ------------------------------------------------------- | ----------------------------------- |
| `claude`            | Interaktiven Modus starten                              | `claude`                            |
| `claude "task"`     | Eine einmalige Aufgabe ausführen                        | `claude "fix the build error"`      |
| `claude -p "query"` | Einmalige Abfrage ausführen und dann beenden            | `claude -p "explain this function"` |
| `claude -c`         | Letzte Unterhaltung im aktuellen Verzeichnis fortsetzen | `claude -c`                         |
| `claude -r`         | Eine vorherige Unterhaltung fortsetzen                  | `claude -r`                         |
| `claude commit`     | Einen Git-Commit erstellen                              | `claude commit`                     |
| `/clear`            | Unterhaltungsverlauf löschen                            | `/clear`                            |
| `/help`             | Verfügbare Befehle anzeigen                             | `/help`                             |
| `exit` oder Strg+C  | Claude Code beenden                                     | `exit`                              |

Siehe die [CLI-Referenz](/de/cli-reference) für eine vollständige Liste der Befehle.

## Profitipps für Anfänger

Weitere Informationen finden Sie unter [Best Practices](/de/best-practices) und [häufige Arbeitsabläufe](/de/common-workflows).

<AccordionGroup>
  <Accordion title="Seien Sie spezifisch bei Ihren Anfragen">
    Statt: 'Beheben Sie den Fehler"

    Versuchen Sie: „Beheben Sie den Login-Fehler, bei dem Benutzer einen leeren Bildschirm sehen, nachdem sie falsche Anmeldedaten eingegeben haben"
  </Accordion>

  <Accordion title="Verwenden Sie Schritt-für-Schritt-Anweisungen">
    Unterteilen Sie komplexe Aufgaben in Schritte:

    ```text  theme={null}
    1. create a new database table for user profiles
    2. create an API endpoint to get and update user profiles
    3. build a webpage that allows users to see and edit their information
    ```
  </Accordion>

  <Accordion title="Lassen Sie Claude zuerst erkunden">
    Bevor Sie Änderungen vornehmen, lassen Sie Claude Ihren Code verstehen:

    ```text  theme={null}
    analyze the database schema
    ```

    ```text  theme={null}
    build a dashboard showing products that are most frequently returned by our UK customers
    ```
  </Accordion>

  <Accordion title="Sparen Sie Zeit mit Verknüpfungen">
    * Drücken Sie `?`, um alle verfügbaren Tastaturkürzel anzuzeigen
    * Verwenden Sie Tab für Befehlsvervollständigung
    * Drücken Sie ↑ für Befehlsverlauf
    * Geben Sie `/` ein, um alle Befehle und skills anzuzeigen
  </Accordion>
</AccordionGroup>

## Was kommt als Nächstes?

Nachdem Sie die Grundlagen gelernt haben, erkunden Sie erweiterte Funktionen:

<CardGroup cols={2}>
  <Card title="Wie Claude Code funktioniert" icon="microchip" href="/de/how-claude-code-works">
    Verstehen Sie die agentengestützte Schleife, integrierte Tools und wie Claude Code mit Ihrem Projekt interagiert
  </Card>

  <Card title="Best Practices" icon="star" href="/de/best-practices">
    Erzielen Sie bessere Ergebnisse mit effektivem Prompting und Projektsetup
  </Card>

  <Card title="Häufige Arbeitsabläufe" icon="graduation-cap" href="/de/common-workflows">
    Schritt-für-Schritt-Anleitungen für häufige Aufgaben
  </Card>

  <Card title="Claude Code erweitern" icon="puzzle-piece" href="/de/features-overview">
    Passen Sie mit CLAUDE.md, skills, hooks, MCP und mehr an
  </Card>
</CardGroup>

## Hilfe erhalten

* **In Claude Code**: Geben Sie `/help` ein oder fragen Sie „how do I..."
* **Dokumentation**: Sie sind hier! Durchsuchen Sie andere Leitfäden
* **Community**: Treten Sie unserem [Discord](https://www.anthropic.com/discord) bei, um Tipps und Support zu erhalten
