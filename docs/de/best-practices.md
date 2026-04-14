> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Best Practices für Claude Code

> Tipps und Muster, um das Beste aus Claude Code herauszuholen – von der Konfiguration Ihrer Umgebung bis zur Skalierung über parallele Sessions.

Claude Code ist eine agentengesteuerte Coding-Umgebung. Im Gegensatz zu einem Chatbot, der Fragen beantwortet und wartet, kann Claude Code Ihre Dateien lesen, Befehle ausführen, Änderungen vornehmen und autonom Probleme lösen, während Sie zuschauen, umleiten oder sich ganz zurückziehen.

Dies ändert Ihre Arbeitsweise. Anstatt Code selbst zu schreiben und Claude zur Überprüfung zu bitten, beschreiben Sie, was Sie möchten, und Claude findet heraus, wie es zu bauen ist. Claude erkundet, plant und implementiert.

Aber diese Autonomie bringt immer noch eine Lernkurve mit sich. Claude arbeitet innerhalb bestimmter Einschränkungen, die Sie verstehen müssen.

Dieser Leitfaden behandelt Muster, die sich in den internen Teams von Anthropic und bei Ingenieuren, die Claude Code in verschiedenen Codebases, Sprachen und Umgebungen nutzen, als wirksam erwiesen haben. Informationen zur Funktionsweise der agentengesteuerten Schleife finden Sie unter [How Claude Code works](/de/how-claude-code-works).

***

Die meisten Best Practices basieren auf einer Einschränkung: Claudes Kontextfenster füllt sich schnell, und die Leistung verschlechtert sich, wenn es sich füllt.

Claudes Kontextfenster enthält Ihre gesamte Konversation, einschließlich jeder Nachricht, jeder Datei, die Claude liest, und jeder Befehlsausgabe. Dies kann sich jedoch schnell füllen. Eine einzelne Debugging-Sitzung oder Codebase-Erkundung könnte Zehntausende von Tokens generieren und verbrauchen.

Dies ist wichtig, da die LLM-Leistung abnimmt, wenn sich der Kontext füllt. Wenn das Kontextfenster voll wird, könnte Claude anfangen, frühere Anweisungen zu „vergessen" oder mehr Fehler zu machen. Das Kontextfenster ist die wichtigste Ressource, die verwaltet werden muss. Verfolgen Sie die Kontextnutzung kontinuierlich mit einer [benutzerdefinierten Statuszeile](/de/statusline), und siehe [Token-Nutzung reduzieren](/de/costs#reduce-token-usage) für Strategien zur Reduzierung der Token-Nutzung.

***

## Geben Sie Claude eine Möglichkeit, seine Arbeit zu überprüfen

<Tip>
  Fügen Sie Tests, Screenshots oder erwartete Ausgaben ein, damit Claude sich selbst überprüfen kann. Dies ist das Wichtigste, das Sie tun können.
</Tip>

Claude funktioniert dramatisch besser, wenn er seine eigene Arbeit überprüfen kann, wie Tests ausführen, Screenshots vergleichen und Ausgaben validieren.

Ohne klare Erfolgskriterien könnte es etwas produzieren, das richtig aussieht, aber tatsächlich nicht funktioniert. Sie werden zur einzigen Feedback-Schleife, und jeder Fehler erfordert Ihre Aufmerksamkeit.

| Strategie                                 | Vorher                                                         | Nachher                                                                                                                                                                                                                        |
| ----------------------------------------- | -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Überprüfungskriterien bereitstellen**   | *„implementiere eine Funktion, die E-Mail-Adressen validiert"* | *„schreibe eine validateEmail-Funktion. Beispiel-Testfälle: [user@example.com](mailto:user@example.com) ist wahr, invalid ist falsch, [user@.com](mailto:user@.com) ist falsch. führe die Tests nach der Implementierung aus"* |
| **UI-Änderungen visuell überprüfen**      | *„mache das Dashboard besser aussehen"*                        | *„\[Screenshot einfügen] implementiere dieses Design. mache einen Screenshot des Ergebnisses und vergleiche ihn mit dem Original. liste Unterschiede auf und behebe sie"*                                                      |
| **Grundursachen beheben, nicht Symptome** | *„der Build schlägt fehl"*                                     | *„der Build schlägt mit diesem Fehler fehl: \[Fehler einfügen]. behebe ihn und überprüfe, dass der Build erfolgreich ist. behebe die Grundursache, unterdrücke den Fehler nicht"*                                              |

UI-Änderungen können mit der [Claude in Chrome-Erweiterung](/de/chrome) überprüft werden. Sie öffnet neue Registerkarten in Ihrem Browser, testet die UI und iteriert, bis der Code funktioniert.

Ihre Überprüfung kann auch eine Test-Suite, ein Linter oder ein Bash-Befehl sein, der die Ausgabe überprüft. Investieren Sie darin, Ihre Überprüfung solide zu machen.

***

## Erkunden Sie zuerst, dann planen Sie, dann codieren Sie

<Tip>
  Trennen Sie Forschung und Planung von der Implementierung, um zu vermeiden, das falsche Problem zu lösen.
</Tip>

Wenn Claude direkt zum Codieren springt, kann dies zu Code führen, der das falsche Problem löst. Verwenden Sie [Plan Mode](/de/common-workflows#use-plan-mode-for-safe-code-analysis), um Erkundung von Ausführung zu trennen.

Der empfohlene Workflow hat vier Phasen:

<Steps>
  <Step title="Erkunden">
    Geben Sie Plan Mode ein. Claude liest Dateien und beantwortet Fragen, ohne Änderungen vorzunehmen.

    ```txt claude (Plan Mode) theme={null}
    read /src/auth and understand how we handle sessions and login.
    also look at how we manage environment variables for secrets.
    ```
  </Step>

  <Step title="Planen">
    Bitten Sie Claude, einen detaillierten Implementierungsplan zu erstellen.

    ```txt claude (Plan Mode) theme={null}
    I want to add Google OAuth. What files need to change?
    What's the session flow? Create a plan.
    ```

    Drücken Sie `Ctrl+G`, um den Plan in Ihrem Texteditor zur direkten Bearbeitung zu öffnen, bevor Claude fortfährt.
  </Step>

  <Step title="Implementieren">
    Wechseln Sie zurück zum Normal Mode und lassen Sie Claude codieren, wobei Sie gegen seinen Plan überprüfen.

    ```txt claude (Normal Mode) theme={null}
    implement the OAuth flow from your plan. write tests for the
    callback handler, run the test suite and fix any failures.
    ```
  </Step>

  <Step title="Commit">
    Bitten Sie Claude, mit einer aussagekräftigen Nachricht zu committen und einen PR zu erstellen.

    ```txt claude (Normal Mode) theme={null}
    commit with a descriptive message and open a PR
    ```
  </Step>
</Steps>

<Callout>
  Plan Mode ist nützlich, bringt aber auch Overhead mit sich.

  Für Aufgaben, bei denen der Umfang klar ist und die Lösung klein ist (wie das Beheben eines Tippfehlers, das Hinzufügen einer Log-Zeile oder das Umbenennen einer Variablen), bitten Sie Claude, es direkt zu tun.

  Planung ist am nützlichsten, wenn Sie unsicher über den Ansatz sind, wenn die Änderung mehrere Dateien ändert, oder wenn Sie mit dem zu ändernden Code nicht vertraut sind. Wenn Sie den Diff in einem Satz beschreiben könnten, überspringen Sie den Plan.
</Callout>

***

## Geben Sie spezifischen Kontext in Ihren Prompts an

<Tip>
  Je präziser Ihre Anweisungen sind, desto weniger Korrektionen benötigen Sie.
</Tip>

Claude kann Absichten ableiten, aber er kann nicht Ihre Gedanken lesen. Verweisen Sie auf spezifische Dateien, erwähnen Sie Einschränkungen und zeigen Sie auf Beispielmuster.

| Strategie                                                                                                        | Vorher                                               | Nachher                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ---------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Begrenzen Sie die Aufgabe.** Geben Sie an, welche Datei, welches Szenario und Testpräferenzen.                 | *„füge Tests für foo.py hinzu"*                      | *„schreibe einen Test für foo.py, der den Edge Case abdeckt, in dem der Benutzer abgemeldet ist. vermeide Mocks."*                                                                                                                                                                                                                                                                                                                        |
| **Zeigen Sie auf Quellen.** Leiten Sie Claude zur Quelle, die eine Frage beantworten kann.                       | *„warum hat ExecutionFactory eine so seltsame API?"* | *„schaue dir die Git-Historie von ExecutionFactory an und fasse zusammen, wie seine API entstanden ist"*                                                                                                                                                                                                                                                                                                                                  |
| **Verweisen Sie auf vorhandene Muster.** Zeigen Sie Claude Muster in Ihrer Codebase.                             | *„füge ein Calendar-Widget hinzu"*                   | *„schaue dir an, wie vorhandene Widgets auf der Startseite implementiert sind, um die Muster zu verstehen. HotDogWidget.php ist ein gutes Beispiel. folge dem Muster, um ein neues Calendar-Widget zu implementieren, das dem Benutzer ermöglicht, einen Monat auszuwählen und vorwärts/rückwärts zu blättern, um ein Jahr auszuwählen. baue von Grund auf ohne Bibliotheken außer denen, die bereits in der Codebase verwendet werden."* |
| **Beschreiben Sie das Symptom.** Geben Sie das Symptom, den wahrscheinlichen Ort und an, wie „behoben" aussieht. | *„behebe den Login-Bug"*                             | *„Benutzer berichten, dass Login nach Session-Timeout fehlschlägt. überprüfe den Auth-Flow in src/auth/, besonders Token-Refresh. schreibe einen fehlgeschlagenen Test, der das Problem reproduziert, dann behebe es"*                                                                                                                                                                                                                    |

Vage Prompts können nützlich sein, wenn Sie erkunden und Kurskorrektionen vornehmen können. Ein Prompt wie `„was würdest du in dieser Datei verbessern?"` kann Dinge an die Oberfläche bringen, an die Sie nicht gedacht hätten zu fragen.

### Geben Sie umfangreiche Inhalte an

<Tip>
  Verwenden Sie `@`, um auf Dateien zu verweisen, fügen Sie Screenshots/Bilder ein oder leiten Sie Daten direkt weiter.
</Tip>

Sie können Claude auf mehrere Arten umfangreiche Daten bereitstellen:

* **Verweisen Sie auf Dateien mit `@`** anstatt zu beschreiben, wo Code lebt. Claude liest die Datei, bevor er antwortet.
* **Fügen Sie Bilder direkt ein**. Kopieren/fügen Sie Bilder ein oder ziehen Sie sie in den Prompt.
* **Geben Sie URLs** für Dokumentation und API-Referenzen an. Verwenden Sie `/permissions`, um häufig verwendete Domains auf die Whitelist zu setzen.
* **Leiten Sie Daten weiter**, indem Sie `cat error.log | claude` ausführen, um Dateiinhalte direkt zu senden.
* **Lassen Sie Claude abrufen, was es braucht**. Sagen Sie Claude, dass es Kontext selbst mit Bash-Befehlen, MCP-Tools oder durch Lesen von Dateien abrufen soll.

***

## Konfigurieren Sie Ihre Umgebung

Ein paar Einrichtungsschritte machen Claude Code über alle Ihre Sessions hinweg erheblich effektiver. Einen vollständigen Überblick über Erweiterungsfunktionen und wann Sie jede verwenden sollten, finden Sie unter [Extend Claude Code](/de/features-overview).

### Schreiben Sie eine effektive CLAUDE.md

<Tip>
  Führen Sie `/init` aus, um eine Starter-CLAUDE.md-Datei basierend auf Ihrer aktuellen Projektstruktur zu generieren, und verfeinern Sie sie dann im Laufe der Zeit.
</Tip>

CLAUDE.md ist eine spezielle Datei, die Claude zu Beginn jeder Konversation liest. Fügen Sie Bash-Befehle, Code-Stil und Workflow-Regeln ein. Dies gibt Claude persistenten Kontext, den es nicht aus Code allein ableiten kann.

Der `/init`-Befehl analysiert Ihre Codebase, um Build-Systeme, Test-Frameworks und Code-Muster zu erkennen, und gibt Ihnen eine solide Grundlage zum Verfeinern.

Es gibt kein erforderliches Format für CLAUDE.md-Dateien, aber halten Sie es kurz und für Menschen lesbar. Zum Beispiel:

```markdown CLAUDE.md theme={null}
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

CLAUDE.md wird jede Session geladen, also fügen Sie nur Dinge ein, die weit verbreitet gelten. Für Domänenwissen oder Workflows, die nur manchmal relevant sind, verwenden Sie stattdessen [skills](/de/skills). Claude lädt sie bei Bedarf, ohne jede Konversation zu überlasten.

Halten Sie es prägnant. Fragen Sie sich für jede Zeile: *„Würde das Entfernen dieser Zeile dazu führen, dass Claude Fehler macht?"* Wenn nicht, streichen Sie es. Überladene CLAUDE.md-Dateien führen dazu, dass Claude Ihre tatsächlichen Anweisungen ignoriert!

| ✅ Einschließen                                                       | ❌ Ausschließen                                                      |
| -------------------------------------------------------------------- | ------------------------------------------------------------------- |
| Bash-Befehle, die Claude nicht erraten kann                          | Alles, was Claude durch Lesen von Code herausfinden kann            |
| Code-Stil-Regeln, die von Standardwerten abweichen                   | Standard-Sprachkonventionen, die Claude bereits kennt               |
| Test-Anweisungen und bevorzugte Test-Runner                          | Detaillierte API-Dokumentation (verlinken Sie stattdessen auf Docs) |
| Repository-Etikette (Branch-Naming, PR-Konventionen)                 | Informationen, die sich häufig ändern                               |
| Architektonische Entscheidungen, die für Ihr Projekt spezifisch sind | Lange Erklärungen oder Tutorials                                    |
| Entwicklungsumgebungs-Eigenheiten (erforderliche Umgebungsvariablen) | Datei-für-Datei-Beschreibungen der Codebase                         |
| Häufige Fallstricke oder nicht offensichtliche Verhaltensweisen      | Selbstverständliche Praktiken wie „schreibe sauberen Code"          |

Wenn Claude etwas tut, das Sie nicht möchten, obwohl es eine Regel dagegen gibt, ist die Datei wahrscheinlich zu lang und die Regel geht verloren. Wenn Claude Fragen stellt, die in CLAUDE.md beantwortet werden, könnte die Formulierung mehrdeutig sein. Behandeln Sie CLAUDE.md wie Code: überprüfen Sie es, wenn etwas schiefgeht, bereinigen Sie es regelmäßig, und testen Sie Änderungen, indem Sie beobachten, ob sich Claudes Verhalten tatsächlich ändert.

Sie können Anweisungen durch Hinzufügen von Betonung (z. B. „WICHTIG" oder „DU MUSST") abstimmen, um die Einhaltung zu verbessern. Überprüfen Sie CLAUDE.md in Git, damit Ihr Team beitragen kann. Die Datei nimmt im Laufe der Zeit an Wert zu.

CLAUDE.md-Dateien können zusätzliche Dateien mit der `@path/to/import`-Syntax importieren:

```markdown CLAUDE.md theme={null}
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

Sie können CLAUDE.md-Dateien an mehreren Orten platzieren:

* **Home-Ordner (`~/.claude/CLAUDE.md`)**: gilt für alle Claude-Sessions
* **Projekt-Root (`./CLAUDE.md`)**: überprüfen Sie in Git, um mit Ihrem Team zu teilen
* **Übergeordnete Verzeichnisse**: nützlich für Monorepos, bei denen sowohl `root/CLAUDE.md` als auch `root/foo/CLAUDE.md` automatisch eingezogen werden
* **Untergeordnete Verzeichnisse**: Claude zieht untergeordnete CLAUDE.md-Dateien bei Bedarf ein, wenn mit Dateien in diesen Verzeichnissen gearbeitet wird

### Konfigurieren Sie Berechtigungen

<Tip>
  Verwenden Sie [Auto Mode](/de/permission-modes#eliminate-prompts-with-auto-mode), um einen Klassifizierer die Genehmigungen handhaben zu lassen, `/permissions`, um spezifische Befehle auf die Whitelist zu setzen, oder `/sandbox` für Isolation auf Betriebssystemebene. Jede reduziert Unterbrechungen, während Sie die Kontrolle behalten.
</Tip>

Standardmäßig fordert Claude Code Berechtigung für Aktionen an, die Ihr System ändern könnten: Dateischreibvorgänge, Bash-Befehle, MCP-Tools usw. Dies ist sicher, aber mühsam. Nach der zehnten Genehmigung überprüfen Sie nicht wirklich mehr, Sie klicken einfach durch. Es gibt drei Möglichkeiten, diese Unterbrechungen zu reduzieren:

* **Auto Mode**: ein separates Klassifizierer-Modell überprüft Befehle und blockiert nur das, was riskant aussieht: Scope-Eskalation, unbekannte Infrastruktur oder feindselige-Inhalts-getriebene Aktionen. Am besten, wenn Sie der allgemeinen Richtung einer Aufgabe vertrauen, aber nicht jeden Schritt durchklicken möchten
* **Berechtigungs-Whitelists**: erlauben Sie spezifische Tools, die Sie kennen und die sicher sind, wie `npm run lint` oder `git commit`
* **Sandboxing**: aktivieren Sie Isolation auf Betriebssystemebene, die Dateisystem- und Netzwerkzugriff einschränkt und Claude ermöglicht, freier innerhalb definierter Grenzen zu arbeiten

Lesen Sie mehr über [Berechtigungsmodi](/de/permission-modes), [Berechtigungsregeln](/de/permissions) und [Sandboxing](/de/sandboxing).

### Verwenden Sie CLI-Tools

<Tip>
  Sagen Sie Claude Code, dass es CLI-Tools wie `gh`, `aws`, `gcloud` und `sentry-cli` bei der Interaktion mit externen Diensten verwenden soll.
</Tip>

CLI-Tools sind die kontexteffizienteste Möglichkeit, mit externen Diensten zu interagieren. Wenn Sie GitHub verwenden, installieren Sie die `gh`-CLI. Claude weiß, wie man sie zum Erstellen von Issues, Öffnen von Pull Requests und Lesen von Kommentaren verwendet. Ohne `gh` kann Claude immer noch die GitHub-API verwenden, aber unauthentifizierte Anfragen treffen oft auf Rate Limits.

Claude ist auch effektiv beim Erlernen von CLI-Tools, die er nicht bereits kennt. Versuchen Sie Prompts wie `Use 'foo-cli-tool --help' to learn about foo tool, then use it to solve A, B, C.`

### Verbinden Sie MCP-Server

<Tip>
  Führen Sie `claude mcp add` aus, um externe Tools wie Notion, Figma oder Ihre Datenbank zu verbinden.
</Tip>

Mit [MCP-Servern](/de/mcp) können Sie Claude bitten, Funktionen von Issue-Trackern zu implementieren, Datenbanken abzufragen, Überwachungsdaten zu analysieren, Designs von Figma zu integrieren und Workflows zu automatisieren.

### Richten Sie Hooks ein

<Tip>
  Verwenden Sie Hooks für Aktionen, die jedes Mal mit null Ausnahmen stattfinden müssen.
</Tip>

[Hooks](/de/hooks-guide) führen Skripte automatisch an bestimmten Punkten in Claudes Workflow aus. Im Gegensatz zu CLAUDE.md-Anweisungen, die beratend sind, sind Hooks deterministisch und garantieren, dass die Aktion stattfindet.

Claude kann Hooks für Sie schreiben. Versuchen Sie Prompts wie *„Schreibe einen Hook, der eslint nach jeder Dateibearbeitung ausführt"* oder *„Schreibe einen Hook, der Schreibvorgänge in den Migrations-Ordner blockiert."* Bearbeiten Sie `.claude/settings.json` direkt, um Hooks von Hand zu konfigurieren, und führen Sie `/hooks` aus, um zu durchsuchen, was konfiguriert ist.

### Erstellen Sie Skills

<Tip>
  Erstellen Sie `SKILL.md`-Dateien in `.claude/skills/`, um Claude Domänenwissen und wiederverwendbare Workflows zu geben.
</Tip>

[Skills](/de/skills) erweitern Claudes Wissen mit Informationen, die für Ihr Projekt, Team oder Ihre Domäne spezifisch sind. Claude wendet sie automatisch an, wenn relevant, oder Sie können sie direkt mit `/skill-name` aufrufen.

Erstellen Sie einen Skill, indem Sie ein Verzeichnis mit einer `SKILL.md` zu `.claude/skills/` hinzufügen:

```markdown .claude/skills/api-conventions/SKILL.md theme={null}
---
name: api-conventions
description: REST API design conventions for our services
---
# API Conventions
- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
- Version APIs in the URL path (/v1/, /v2/)
```

Skills können auch wiederverwendbare Workflows definieren, die Sie direkt aufrufen:

```markdown .claude/skills/fix-issue/SKILL.md theme={null}
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Analyze and fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

Führen Sie `/fix-issue 1234` aus, um es aufzurufen. Verwenden Sie `disable-model-invocation: true` für Workflows mit Nebenwirkungen, die Sie manuell auslösen möchten.

### Erstellen Sie benutzerdefinierte Subagents

<Tip>
  Definieren Sie spezialisierte Assistenten in `.claude/agents/`, an die Claude für isolierte Aufgaben delegieren kann.
</Tip>

[Subagents](/de/sub-agents) laufen in ihrem eigenen Kontext mit ihrem eigenen Satz erlaubter Tools. Sie sind nützlich für Aufgaben, die viele Dateien lesen oder spezialisierte Aufmerksamkeit benötigen, ohne Ihre Hauptkonversation zu überlasten.

```markdown .claude/agents/security-reviewer.md theme={null}
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

Sagen Sie Claude explizit, dass es Subagents verwenden soll: *„Verwende einen Subagent, um diesen Code auf Sicherheitsprobleme zu überprüfen."*

### Installieren Sie Plugins

<Tip>
  Führen Sie `/plugin` aus, um den Marketplace zu durchsuchen. Plugins fügen Skills, Tools und Integrationen ohne Konfiguration hinzu.
</Tip>

[Plugins](/de/plugins) bündeln Skills, Hooks, Subagents und MCP-Server in eine einzelne installierbare Einheit aus der Community und von Anthropic. Wenn Sie mit einer typisierten Sprache arbeiten, installieren Sie ein [Code-Intelligence-Plugin](/de/discover-plugins#code-intelligence), um Claude präzise Symbol-Navigation und automatische Fehlererkennung nach Bearbeitungen zu geben.

Anleitungen zur Auswahl zwischen Skills, Subagents, Hooks und MCP finden Sie unter [Extend Claude Code](/de/features-overview#match-features-to-your-goal).

***

## Kommunizieren Sie effektiv

Die Art und Weise, wie Sie mit Claude Code kommunizieren, hat einen großen Einfluss auf die Qualität der Ergebnisse.

### Stellen Sie Codebase-Fragen

<Tip>
  Stellen Sie Claude Fragen, die Sie einem Senior Engineer stellen würden.
</Tip>

Wenn Sie sich in eine neue Codebase einarbeiten, verwenden Sie Claude Code zum Lernen und Erkunden. Sie können Claude die gleichen Fragen stellen, die Sie einem anderen Engineer stellen würden:

* Wie funktioniert Logging?
* Wie erstelle ich einen neuen API-Endpunkt?
* Was macht `async move { ... }` auf Zeile 134 von `foo.rs`?
* Welche Edge Cases behandelt `CustomerOnboardingFlowImpl`?
* Warum ruft dieser Code `foo()` anstelle von `bar()` auf Zeile 333 auf?

Die Verwendung von Claude Code auf diese Weise ist ein effektiver Onboarding-Workflow, der die Einarbeitungszeit verbessert und die Belastung anderer Engineers reduziert. Keine spezielle Prompt-Formulierung erforderlich: stellen Sie Fragen direkt.

### Lassen Sie Claude Sie interviewen

<Tip>
  Für größere Features lassen Sie Claude Sie zuerst interviewen. Beginnen Sie mit einem minimalen Prompt und bitten Sie Claude, Sie mit dem `AskUserQuestion`-Tool zu interviewen.
</Tip>

Claude stellt Fragen zu Dingen, die Sie möglicherweise noch nicht berücksichtigt haben, einschließlich technischer Implementierung, UI/UX, Edge Cases und Tradeoffs.

```text  theme={null}
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered.

Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

Sobald die Spezifikation fertig ist, starten Sie eine neue Session, um sie auszuführen. Die neue Session hat einen sauberen Kontext, der sich vollständig auf die Implementierung konzentriert, und Sie haben eine geschriebene Spezifikation zum Referenzieren.

***

## Verwalten Sie Ihre Session

Konversationen sind persistent und reversibel. Nutzen Sie dies zu Ihrem Vorteil!

### Korrigieren Sie früh und oft

<Tip>
  Korrigieren Sie Claude, sobald Sie bemerken, dass es vom Weg abkommt.
</Tip>

Die besten Ergebnisse kommen aus engen Feedback-Schleifen. Obwohl Claude gelegentlich Probleme beim ersten Versuch perfekt löst, führt eine schnelle Korrektur im Allgemeinen zu besseren Lösungen schneller.

* **`Esc`**: stoppen Sie Claude mitten in einer Aktion mit der `Esc`-Taste. Der Kontext wird beibehalten, sodass Sie umleiten können.
* **`Esc + Esc` oder `/rewind`**: drücken Sie `Esc` zweimal oder führen Sie `/rewind` aus, um das Rewind-Menü zu öffnen und die vorherige Konversation und den Code-Status wiederherzustellen, oder fassen Sie eine ausgewählte Nachricht zusammen.
* **`"Undo that"`**: lassen Sie Claude seine Änderungen rückgängig machen.
* **`/clear`**: setzen Sie den Kontext zwischen nicht verwandten Aufgaben zurück. Lange Sessions mit irrelevantem Kontext können die Leistung reduzieren.

Wenn Sie Claude mehr als zweimal bei demselben Problem in einer Session korrigiert haben, ist der Kontext mit fehlgeschlagenen Ansätzen überladen. Führen Sie `/clear` aus und beginnen Sie mit einem spezifischeren Prompt, der das Gelernte einbezieht. Eine saubere Session mit einem besseren Prompt übertrifft fast immer eine lange Session mit angesammelten Korrektionen.

### Verwalten Sie den Kontext aggressiv

<Tip>
  Führen Sie `/clear` zwischen nicht verwandten Aufgaben aus, um den Kontext zurückzusetzen.
</Tip>

Claude Code komprimiert automatisch die Konversationshistorie, wenn Sie sich den Kontextlimits nähern, was wichtigen Code und Entscheidungen bewahrt und Platz freimacht.

Während langer Sessions kann sich Claudes Kontextfenster mit irrelevanten Konversationen, Dateiinhalten und Befehlen füllen. Dies kann die Leistung reduzieren und Claude manchmal ablenken.

* Verwenden Sie `/clear` häufig zwischen Aufgaben, um das Kontextfenster vollständig zurückzusetzen
* Wenn die automatische Komprimierung ausgelöst wird, fasst Claude zusammen, was am wichtigsten ist, einschließlich Code-Muster, Dateizustände und wichtige Entscheidungen
* Für mehr Kontrolle führen Sie `/compact <instructions>` aus, wie `/compact Focus on the API changes`
* Um nur einen Teil der Konversation zu komprimieren, verwenden Sie `Esc + Esc` oder `/rewind`, wählen Sie einen Nachricht-Checkpoint und wählen Sie **Summarize from here**. Dies verdichtet Nachrichten von diesem Punkt an, während der frühere Kontext erhalten bleibt.
* Passen Sie das Komprimierungsverhalten in CLAUDE.md mit Anweisungen wie `„When compacting, always preserve the full list of modified files and any test commands"` an, um sicherzustellen, dass kritischer Kontext die Zusammenfassung überlebt
* Für schnelle Fragen, die nicht im Kontext bleiben müssen, verwenden Sie [`/btw`](/de/interactive-mode#side-questions-with-btw). Die Antwort erscheint in einer verwerfbaren Überlagerung und gelangt niemals in die Konversationshistorie, sodass Sie ein Detail überprüfen können, ohne den Kontext zu vergrößern.

### Verwenden Sie Subagents für Untersuchungen

<Tip>
  Delegieren Sie Forschung mit `„use subagents to investigate X"`. Sie erkunden in einem separaten Kontext und halten Ihre Hauptkonversation sauber für die Implementierung.
</Tip>

Da der Kontext Ihre grundlegende Einschränkung ist, sind Subagents eines der mächtigsten verfügbaren Tools. Wenn Claude eine Codebase erforscht, liest er viele Dateien, die alle Ihren Kontext verbrauchen. Subagents laufen in separaten Kontextfenstern und berichten Zusammenfassungen zurück:

```text  theme={null}
Use subagents to investigate how our authentication system handles token
refresh, and whether we have any existing OAuth utilities I should reuse.
```

Der Subagent erkundet die Codebase, liest relevante Dateien und berichtet Erkenntnisse zurück, alles ohne Ihre Hauptkonversation zu überlasten.

Sie können Subagents auch zur Überprüfung verwenden, nachdem Claude etwas implementiert hat:

```text  theme={null}
use a subagent to review this code for edge cases
```

### Rewind mit Checkpoints

<Tip>
  Jede Aktion, die Claude macht, erstellt einen Checkpoint. Sie können Konversation, Code oder beides zu jedem vorherigen Checkpoint wiederherstellen.
</Tip>

Claude erstellt automatisch Checkpoints vor Änderungen. Doppeltippen Sie auf `Escape` oder führen Sie `/rewind` aus, um das Rewind-Menü zu öffnen. Sie können nur Konversation wiederherstellen, nur Code wiederherstellen, beides wiederherstellen oder eine ausgewählte Nachricht zusammenfassen. Siehe [Checkpointing](/de/checkpointing) für Details.

Anstatt jeden Schritt sorgfältig zu planen, können Sie Claude bitten, etwas Riskantes zu versuchen. Wenn es nicht funktioniert, rewind und versuchen Sie einen anderen Ansatz. Checkpoints bleiben über Sessions hinweg erhalten, sodass Sie Ihr Terminal schließen und später immer noch rewind können.

<Warning>
  Checkpoints verfolgen nur Änderungen, die *von Claude* vorgenommen wurden, nicht externe Prozesse. Dies ist kein Ersatz für Git.
</Warning>

### Setzen Sie Konversationen fort

<Tip>
  Führen Sie `claude --continue` aus, um dort weiterzumachen, wo Sie aufgehört haben, oder `--resume`, um aus aktuellen Sessions auszuwählen.
</Tip>

Claude Code speichert Konversationen lokal. Wenn sich eine Aufgabe über mehrere Sessions erstreckt, müssen Sie den Kontext nicht erneut erklären:

```bash  theme={null}
claude --continue    # Resume the most recent conversation
claude --resume      # Select from recent conversations
```

Verwenden Sie `/rename`, um Sessions aussagekräftige Namen wie `„oauth-migration"` oder `„debugging-memory-leak"` zu geben, damit Sie sie später finden können. Behandeln Sie Sessions wie Branches: verschiedene Workstreams können separate, persistente Kontexte haben.

***

## Automatisieren und skalieren Sie

Sobald Sie mit einem Claude effektiv sind, multiplizieren Sie Ihre Ausgabe mit parallelen Sessions, nicht-interaktivem Modus und Fan-Out-Mustern.

Alles bisher geht von einem Menschen, einem Claude und einer Konversation aus. Aber Claude Code skaliert horizontal. Die Techniken in diesem Abschnitt zeigen, wie Sie mehr erreichen können.

### Führen Sie nicht-interaktiven Modus aus

<Tip>
  Verwenden Sie `claude -p "prompt"` in CI, Pre-Commit-Hooks oder Skripten. Fügen Sie `--output-format stream-json` für Streaming-JSON-Ausgabe hinzu.
</Tip>

Mit `claude -p "your prompt"` können Sie Claude nicht-interaktiv ohne eine Session ausführen. Der nicht-interaktive Modus ist, wie Sie Claude in CI-Pipelines, Pre-Commit-Hooks oder jeden automatisierten Workflow integrieren. Die Ausgabeformate ermöglichen es Ihnen, Ergebnisse programmgesteuert zu analysieren: Klartext, JSON oder Streaming-JSON.

```bash  theme={null}
# One-off queries
claude -p "Explain what this project does"

# Structured output for scripts
claude -p "List all API endpoints" --output-format json

# Streaming for real-time processing
claude -p "Analyze this log file" --output-format stream-json
```

### Führen Sie mehrere Claude-Sessions aus

<Tip>
  Führen Sie mehrere Claude-Sessions parallel aus, um die Entwicklung zu beschleunigen, isolierte Experimente auszuführen oder komplexe Workflows zu starten.
</Tip>

Es gibt drei Hauptmöglichkeiten, parallele Sessions auszuführen:

* [Claude Code Desktop-App](/de/desktop#work-in-parallel-with-sessions): Verwalten Sie mehrere lokale Sessions visuell. Jede Session erhält ihren eigenen isolierten Worktree.
* [Claude Code im Web](/de/claude-code-on-the-web): Führen Sie auf der sicheren Cloud-Infrastruktur von Anthropic in isolierten VMs aus.
* [Agent Teams](/de/agent-teams): Automatisierte Koordination mehrerer Sessions mit gemeinsamen Aufgaben, Messaging und einem Team Lead.

Über die Parallelisierung von Arbeit hinaus ermöglichen mehrere Sessions qualitätsorientierte Workflows. Ein frischer Kontext verbessert die Code-Überprüfung, da Claude nicht durch Code, den es gerade geschrieben hat, voreingenommen ist.

Verwenden Sie beispielsweise ein Writer/Reviewer-Muster:

| Session A (Writer)                                                      | Session B (Reviewer)                                                                                                                                                     |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Implement a rate limiter for our API endpoints`                        |                                                                                                                                                                          |
|                                                                         | `Review the rate limiter implementation in @src/middleware/rateLimiter.ts. Look for edge cases, race conditions, and consistency with our existing middleware patterns.` |
| `Here's the review feedback: [Session B output]. Address these issues.` |                                                                                                                                                                          |

Sie können etwas Ähnliches mit Tests tun: lassen Sie einen Claude Tests schreiben, dann schreiben Sie einen anderen Code, um sie zu bestehen.

### Fan Out über Dateien

<Tip>
  Schleifen Sie durch Aufgaben, die `claude -p` für jede aufrufen. Verwenden Sie `--allowedTools`, um Berechtigungen für Batch-Operationen zu begrenzen.
</Tip>

Für große Migrationen oder Analysen können Sie Arbeit über viele parallele Claude-Aufrufe verteilen:

<Steps>
  <Step title="Generieren Sie eine Aufgabenliste">
    Lassen Sie Claude alle Dateien auflisten, die migriert werden müssen (z. B. `list all 2,000 Python files that need migrating`)
  </Step>

  <Step title="Schreiben Sie ein Skript, um die Liste zu durchlaufen">
    ```bash  theme={null}
    for file in $(cat files.txt); do
      claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
        --allowedTools "Edit,Bash(git commit *)"
    done
    ```
  </Step>

  <Step title="Testen Sie auf ein paar Dateien, dann führen Sie in großem Maßstab aus">
    Verfeinern Sie Ihren Prompt basierend auf dem, was bei den ersten 2-3 Dateien schiefgeht, dann führen Sie auf dem vollständigen Satz aus. Das `--allowedTools`-Flag beschränkt, was Claude tun kann, was wichtig ist, wenn Sie unbeaufsichtigt laufen.
  </Step>
</Steps>

Sie können Claude auch in vorhandene Daten-/Verarbeitungs-Pipelines integrieren:

```bash  theme={null}
claude -p "<your prompt>" --output-format json | your_command
```

Verwenden Sie `--verbose` zum Debuggen während der Entwicklung und schalten Sie es in der Produktion aus.

### Führen Sie autonom mit Auto Mode aus

Für ununterbrochene Ausführung mit Hintergrund-Sicherheitsprüfungen verwenden Sie [Auto Mode](/de/permission-modes#eliminate-prompts-with-auto-mode). Ein Klassifizierer-Modell überprüft Befehle vor ihrer Ausführung, blockiert Scope-Eskalation, unbekannte Infrastruktur und feindselige-Inhalts-getriebene Aktionen, während es Routinearbeit ohne Prompts durchlaufen lässt.

```bash  theme={null}
claude --permission-mode auto -p "fix all lint errors"
```

Für nicht-interaktive Läufe mit dem `-p`-Flag bricht Auto Mode ab, wenn der Klassifizierer Aktionen wiederholt blockiert, da es keinen Benutzer gibt, auf den man zurückfallen kann. Siehe [wenn Auto Mode zurückfällt](/de/permission-modes#when-auto-mode-falls-back) für Schwellenwerte.

***

## Vermeiden Sie häufige Fehlermuster

Dies sind häufige Fehler. Sie früh zu erkennen spart Zeit:

* **Die Kitchen-Sink-Session.** Sie beginnen mit einer Aufgabe, dann fragen Claude etwas Unverwandtes, dann gehen Sie zurück zur ersten Aufgabe. Der Kontext ist voll mit irrelevanten Informationen.
  > **Lösung**: `/clear` zwischen nicht verwandten Aufgaben.
* **Immer wieder korrigieren.** Claude macht etwas falsch, Sie korrigieren es, es ist immer noch falsch, Sie korrigieren erneut. Der Kontext ist mit fehlgeschlagenen Ansätzen verschmutzt.
  > **Lösung**: Nach zwei fehlgeschlagenen Korrektionen `/clear` und schreiben Sie einen besseren anfänglichen Prompt, der das Gelernte einbezieht.
* **Die über-spezifizierte CLAUDE.md.** Wenn Ihre CLAUDE.md zu lang ist, ignoriert Claude die Hälfte davon, weil wichtige Regeln in dem Lärm verloren gehen.
  > **Lösung**: Rücksichtslos bereinigen. Wenn Claude etwas bereits ohne die Anweisung richtig macht, löschen Sie es oder konvertieren Sie es in einen Hook.
* **Die Trust-then-Verify-Lücke.** Claude produziert eine plausibel aussehende Implementierung, die Edge Cases nicht behandelt.
  > **Lösung**: Geben Sie immer Überprüfung an (Tests, Skripte, Screenshots). Wenn Sie es nicht überprüfen können, versenden Sie es nicht.
* **Die unendliche Erkundung.** Sie bitten Claude, etwas zu „untersuchen", ohne es zu begrenzen. Claude liest Hunderte von Dateien und füllt den Kontext.
  > **Lösung**: Begrenzen Sie Untersuchungen eng oder verwenden Sie Subagents, damit die Erkundung Ihren Hauptkontext nicht verbraucht.

***

## Entwickeln Sie Ihre Intuition

Die Muster in diesem Leitfaden sind nicht in Stein gemeißelt. Sie sind Ausgangspunkte, die im Allgemeinen gut funktionieren, aber möglicherweise nicht optimal für jede Situation sind.

Manchmal *sollten* Sie den Kontext ansammeln lassen, weil Sie tief in einem komplexen Problem stecken und die Geschichte wertvoll ist. Manchmal sollten Sie die Planung überspringen und Claude es herausfinden lassen, weil die Aufgabe explorativ ist. Manchmal ist ein vager Prompt genau richtig, weil Sie sehen möchten, wie Claude das Problem interpretiert, bevor Sie es einschränken.

Achten Sie auf das, was funktioniert. Wenn Claude großartige Ausgabe produziert, bemerken Sie, was Sie getan haben: die Prompt-Struktur, den Kontext, den Sie bereitgestellt haben, den Modus, in dem Sie waren. Wenn Claude kämpft, fragen Sie warum. War der Kontext zu laut? Der Prompt zu vage? Die Aufgabe zu groß für einen Pass?

Im Laufe der Zeit werden Sie Intuition entwickeln, die kein Leitfaden erfassen kann. Sie werden wissen, wann Sie spezifisch und wann offen sein sollten, wann Sie planen und wann Sie erkunden sollten, wann Sie den Kontext löschen und wann Sie ihn ansammeln lassen sollten.

## Verwandte Ressourcen

* [How Claude Code works](/de/how-claude-code-works): die agentengesteuerte Schleife, Tools und Kontextverwaltung
* [Extend Claude Code](/de/features-overview): Skills, Hooks, MCP, Subagents und Plugins
* [Common workflows](/de/common-workflows): Schritt-für-Schritt-Rezepte zum Debuggen, Testen, PRs und mehr
* [CLAUDE.md](/de/memory): speichern Sie Projektkonventionen und persistenten Kontext
