> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Benutzerdefinierte Subagenten erstellen

> Erstellen und verwenden Sie spezialisierte KI-Subagenten in Claude Code für aufgabenspezifische Workflows und verbesserte Kontextverwaltung.

Subagenten sind spezialisierte KI-Assistenten, die bestimmte Arten von Aufgaben bearbeiten. Jeder Subagent läuft in seinem eigenen Kontextfenster mit einem benutzerdefinierten Systemprompt, spezifischem Werkzeugzugriff und unabhängigen Berechtigungen. Wenn Claude auf eine Aufgabe trifft, die der Beschreibung eines Subagenten entspricht, delegiert es an diesen Subagenten, der unabhängig arbeitet und Ergebnisse zurückgibt. Um die Kontexteinsparungen in der Praxis zu sehen, zeigt die [Kontextfenster-Visualisierung](/de/context-window) eine Sitzung, in der ein Subagent Recherchen in seinem eigenen separaten Fenster durchführt.

<Note>
  Wenn Sie mehrere Agenten benötigen, die parallel arbeiten und miteinander kommunizieren, siehe stattdessen [Agent-Teams](/de/agent-teams). Subagenten arbeiten innerhalb einer einzelnen Sitzung; Agent-Teams koordinieren über separate Sitzungen hinweg.
</Note>

Subagenten helfen Ihnen:

* **Kontext bewahren**, indem Sie Exploration und Implementierung aus Ihrer Hauptkonversation heraushalten
* **Einschränkungen durchsetzen**, indem Sie begrenzen, welche Werkzeuge ein Subagent verwenden kann
* **Konfigurationen wiederverwenden** über Projekte hinweg mit Subagenten auf Benutzerebene
* **Verhalten spezialisieren** mit fokussierten Systemprompts für spezifische Domänen
* **Kosten kontrollieren**, indem Sie Aufgaben an schnellere, günstigere Modelle wie Haiku weiterleiten

Claude verwendet die Beschreibung jedes Subagenten, um zu entscheiden, wann Aufgaben delegiert werden. Wenn Sie einen Subagenten erstellen, schreiben Sie eine klare Beschreibung, damit Claude weiß, wann er ihn verwenden soll.

Claude Code enthält mehrere integrierte Subagenten wie **Explore**, **Plan** und **general-purpose**. Sie können auch benutzerdefinierte Subagenten erstellen, um spezifische Aufgaben zu bearbeiten. Diese Seite behandelt die [integrierten Subagenten](#built-in-subagents), [wie Sie Ihre eigenen erstellen](#quickstart-create-your-first-subagent), [vollständige Konfigurationsoptionen](#configure-subagents), [Muster für die Arbeit mit Subagenten](#work-with-subagents) und [Beispiel-Subagenten](#example-subagents).

## Integrierte Subagenten

Claude Code enthält integrierte Subagenten, die Claude automatisch bei Bedarf verwendet. Jeder erbt die Berechtigungen der übergeordneten Konversation mit zusätzlichen Werkzeugbeschränkungen.

<Tabs>
  <Tab title="Explore">
    Ein schneller, schreibgeschützter Agent, der für die Suche und Analyse von Codebases optimiert ist.

    * **Modell**: Haiku (schnell, niedrige Latenz)
    * **Werkzeuge**: Schreibgeschützte Werkzeuge (kein Zugriff auf Write- und Edit-Werkzeuge)
    * **Zweck**: Dateiermittlung, Codesuche, Codebase-Exploration

    Claude delegiert an Explore, wenn es eine Codebase durchsuchen oder verstehen muss, ohne Änderungen vorzunehmen. Dies hält Explorationsergebnisse aus Ihrem Hauptkonversationskontext heraus.

    Beim Aufrufen von Explore gibt Claude ein Gründlichkeitsniveau an: **quick** für gezielte Lookups, **medium** für ausgewogene Exploration oder **very thorough** für umfassende Analyse.
  </Tab>

  <Tab title="Plan">
    Ein Forschungsagent, der während des [Plan-Modus](/de/common-workflows#use-plan-mode-for-safe-code-analysis) verwendet wird, um Kontext zu sammeln, bevor ein Plan präsentiert wird.

    * **Modell**: Erbt von Hauptkonversation
    * **Werkzeuge**: Schreibgeschützte Werkzeuge (kein Zugriff auf Write- und Edit-Werkzeuge)
    * **Zweck**: Codebase-Recherche für Planung

    Wenn Sie sich im Plan-Modus befinden und Claude Ihre Codebase verstehen muss, delegiert es die Recherche an den Plan-Subagenten. Dies verhindert unendliche Verschachtelung (Subagenten können keine anderen Subagenten spawnen), während dennoch notwendiger Kontext gesammelt wird.
  </Tab>

  <Tab title="General-purpose">
    Ein fähiger Agent für komplexe, mehrstufige Aufgaben, die sowohl Exploration als auch Aktion erfordern.

    * **Modell**: Erbt von Hauptkonversation
    * **Werkzeuge**: Alle Werkzeuge
    * **Zweck**: Komplexe Recherche, mehrstufige Operationen, Code-Änderungen

    Claude delegiert an general-purpose, wenn die Aufgabe sowohl Exploration als auch Änderung, komplexes Denken zur Interpretation von Ergebnissen oder mehrere abhängige Schritte erfordert.
  </Tab>

  <Tab title="Other">
    Claude Code enthält zusätzliche Hilfagenten für spezifische Aufgaben. Diese werden normalerweise automatisch aufgerufen, daher müssen Sie sie nicht direkt verwenden.

    | Agent             | Modell | Wann Claude ihn verwendet                                              |
    | :---------------- | :----- | :--------------------------------------------------------------------- |
    | statusline-setup  | Sonnet | Wenn Sie `/statusline` ausführen, um Ihre Statuszeile zu konfigurieren |
    | Claude Code Guide | Haiku  | Wenn Sie Fragen zu Claude Code-Funktionen stellen                      |
  </Tab>
</Tabs>

Über diese integrierten Subagenten hinaus können Sie Ihre eigenen mit benutzerdefinierten Prompts, Werkzeugbeschränkungen, Berechtigungsmodi, Hooks und Skills erstellen. Die folgenden Abschnitte zeigen, wie Sie anfangen und Subagenten anpassen.

## Schnellstart: Erstellen Sie Ihren ersten Subagenten

Subagenten werden in Markdown-Dateien mit YAML-Frontmatter definiert. Sie können sie [manuell erstellen](#write-subagent-files) oder den `/agents`-Befehl verwenden.

Diese Anleitung führt Sie durch die Erstellung eines Subagenten auf Benutzerebene mit dem `/agents`-Befehl. Der Subagent überprüft Code und schlägt Verbesserungen für die Codebase vor.

<Steps>
  <Step title="Öffnen Sie die Subagenten-Schnittstelle">
    In Claude Code führen Sie aus:

    ```text  theme={null}
    /agents
    ```
  </Step>

  <Step title="Wählen Sie einen Ort">
    Wählen Sie **Create new agent**, dann wählen Sie **Personal**. Dies speichert den Subagenten in `~/.claude/agents/`, sodass er in allen Ihren Projekten verfügbar ist.
  </Step>

  <Step title="Mit Claude generieren">
    Wählen Sie **Generate with Claude**. Wenn Sie dazu aufgefordert werden, beschreiben Sie den Subagenten:

    ```text  theme={null}
    A code improvement agent that scans files and suggests improvements
    for readability, performance, and best practices. It should explain
    each issue, show the current code, and provide an improved version.
    ```

    Claude generiert die Kennung, Beschreibung und den Systemprompt für Sie.
  </Step>

  <Step title="Wählen Sie Werkzeuge">
    Für einen schreibgeschützten Reviewer deselektieren Sie alles außer **Read-only tools**. Wenn Sie alle Werkzeuge ausgewählt lassen, erbt der Subagent alle Werkzeuge, die der Hauptkonversation zur Verfügung stehen.
  </Step>

  <Step title="Wählen Sie Modell">
    Wählen Sie, welches Modell der Subagent verwendet. Wählen Sie für diesen Beispielagenten **Sonnet**, das Fähigkeit und Geschwindigkeit für die Analyse von Code-Mustern ausgleicht.
  </Step>

  <Step title="Wählen Sie eine Farbe">
    Wählen Sie eine Hintergrundfarbe für den Subagenten. Dies hilft Ihnen, zu identifizieren, welcher Subagent in der Benutzeroberfläche ausgeführt wird.
  </Step>

  <Step title="Konfigurieren Sie Speicher">
    Wählen Sie **User scope**, um dem Subagenten ein [persistentes Speicherverzeichnis](#enable-persistent-memory) unter `~/.claude/agent-memory/` zu geben. Der Subagent verwendet dies, um Erkenntnisse über Konversationen hinweg zu sammeln, wie z. B. Codebase-Muster und wiederkehrende Probleme. Wählen Sie **None**, wenn der Subagent keine Erkenntnisse speichern soll.
  </Step>

  <Step title="Speichern und testen Sie">
    Überprüfen Sie die Konfigurationszusammenfassung. Drücken Sie `s` oder `Enter`, um zu speichern, oder drücken Sie `e`, um zu speichern und die Datei in Ihrem Editor zu bearbeiten. Der Subagent ist sofort verfügbar. Testen Sie ihn:

    ```text  theme={null}
    Use the code-improver agent to suggest improvements in this project
    ```

    Claude delegiert an Ihren neuen Subagenten, der die Codebase durchsucht und Verbesserungsvorschläge zurückgibt.
  </Step>
</Steps>

Sie haben jetzt einen Subagenten, den Sie in jedem Projekt auf Ihrem Computer verwenden können, um Codebases zu analysieren und Verbesserungen vorzuschlagen.

Sie können Subagenten auch manuell als Markdown-Dateien erstellen, sie über CLI-Flags definieren oder sie über Plugins verteilen. Die folgenden Abschnitte behandeln alle Konfigurationsoptionen.

## Konfigurieren Sie Subagenten

### Verwenden Sie den /agents-Befehl

Der `/agents`-Befehl bietet eine interaktive Schnittstelle zur Verwaltung von Subagenten. Führen Sie `/agents` aus, um:

* Alle verfügbaren Subagenten anzuzeigen (integriert, Benutzer, Projekt und Plugin)
* Neue Subagenten mit geführtem Setup oder Claude-Generierung zu erstellen
* Vorhandene Subagenten-Konfiguration und Werkzeugzugriff zu bearbeiten
* Benutzerdefinierte Subagenten zu löschen
* Zu sehen, welche Subagenten aktiv sind, wenn Duplikate vorhanden sind

Dies ist die empfohlene Methode zum Erstellen und Verwalten von Subagenten. Für manuelle Erstellung oder Automatisierung können Sie auch Subagenten-Dateien direkt hinzufügen.

Um alle konfigurierten Subagenten von der Befehlszeile aus ohne Starten einer interaktiven Sitzung aufzulisten, führen Sie `claude agents` aus. Dies zeigt Agenten gruppiert nach Quelle und gibt an, welche durch höherrangige Definitionen überschrieben werden.

### Wählen Sie den Subagenten-Umfang

Subagenten sind Markdown-Dateien mit YAML-Frontmatter. Speichern Sie sie an verschiedenen Orten je nach Umfang. Wenn mehrere Subagenten denselben Namen haben, gewinnt der höherrangige Ort.

| Ort                          | Umfang                  | Priorität      | Wie zu erstellen                                             |
| :--------------------------- | :---------------------- | :------------- | :----------------------------------------------------------- |
| Verwaltete Einstellungen     | Organisationsweit       | 1 (höchste)    | Bereitgestellt über [verwaltete Einstellungen](/de/settings) |
| `--agents` CLI-Flag          | Aktuelle Sitzung        | 2              | JSON beim Starten von Claude Code übergeben                  |
| `.claude/agents/`            | Aktuelles Projekt       | 3              | Interaktiv oder manuell                                      |
| `~/.claude/agents/`          | Alle Ihre Projekte      | 4              | Interaktiv oder manuell                                      |
| Plugin-Verzeichnis `agents/` | Wo Plugin aktiviert ist | 5 (niedrigste) | Installiert mit [Plugins](/de/plugins)                       |

**Projekt-Subagenten** (`.claude/agents/`) sind ideal für Subagenten, die spezifisch für eine Codebase sind. Checken Sie sie in die Versionskontrolle ein, damit Ihr Team sie gemeinsam verwenden und verbessern kann.

Projekt-Subagenten werden durch Aufwärts-Traversierung vom aktuellen Arbeitsverzeichnis entdeckt. Verzeichnisse, die mit `--add-dir` hinzugefügt werden, [gewähren nur Dateizugriff](/de/permissions#additional-directories-grant-file-access-not-configuration) und werden nicht nach Subagenten durchsucht. Um Subagenten über Projekte hinweg zu teilen, verwenden Sie `~/.claude/agents/` oder ein [Plugin](/de/plugins).

**Benutzer-Subagenten** (`~/.claude/agents/`) sind persönliche Subagenten, die in allen Ihren Projekten verfügbar sind.

**CLI-definierte Subagenten** werden als JSON beim Starten von Claude Code übergeben. Sie existieren nur für diese Sitzung und werden nicht auf der Festplatte gespeichert, was sie für schnelle Tests oder Automatisierungsskripte nützlich macht. Sie können mehrere Subagenten in einem einzigen `--agents`-Aufruf definieren:

```bash  theme={null}
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

Das `--agents`-Flag akzeptiert JSON mit denselben [Frontmatter](#supported-frontmatter-fields)-Feldern wie dateibasierte Subagenten: `description`, `prompt`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation` und `color`. Verwenden Sie `prompt` für den Systemprompt, äquivalent zum Markdown-Body in dateibasierten Subagenten.

**Verwaltete Subagenten** werden von Organisationsadministratoren bereitgestellt. Platzieren Sie Markdown-Dateien in `.claude/agents/` im [Verzeichnis der verwalteten Einstellungen](/de/settings#settings-files), wobei Sie das gleiche Frontmatter-Format wie bei Projekt- und Benutzer-Subagenten verwenden. Verwaltete Definitionen haben Vorrang vor Projekt- und Benutzer-Subagenten mit demselben Namen.

**Plugin-Subagenten** stammen von [Plugins](/de/plugins), die Sie installiert haben. Sie erscheinen in `/agents` neben Ihren benutzerdefinierten Subagenten. Siehe die [Plugin-Komponenten-Referenz](/de/plugins-reference#agents) für Details zum Erstellen von Plugin-Subagenten.

<Note>
  Aus Sicherheitsgründen unterstützen Plugin-Subagenten die Frontmatter-Felder `hooks`, `mcpServers` oder `permissionMode` nicht. Diese Felder werden ignoriert, wenn Agenten aus einem Plugin geladen werden. Wenn Sie sie benötigen, kopieren Sie die Agent-Datei in `.claude/agents/` oder `~/.claude/agents/`. Sie können auch Regeln zu [`permissions.allow`](/de/settings#permission-settings) in `settings.json` oder `settings.local.json` hinzufügen, aber diese Regeln gelten für die gesamte Sitzung, nicht nur für den Plugin-Subagenten.
</Note>

Subagenten-Definitionen aus einem dieser Umfänge sind auch für [Agent-Teams](/de/agent-teams#use-subagent-definitions-for-teammates) verfügbar: Beim Spawnen eines Teammates können Sie auf einen Subagenten-Typ verweisen und der Teammate erbt seinen Systemprompt, seine Werkzeuge und sein Modell.

### Schreiben Sie Subagenten-Dateien

Subagenten-Dateien verwenden YAML-Frontmatter für die Konfiguration, gefolgt vom Systemprompt in Markdown:

<Note>
  Subagenten werden beim Sitzungsstart geladen. Wenn Sie einen Subagenten durch manuelles Hinzufügen einer Datei erstellen, starten Sie Ihre Sitzung neu oder verwenden Sie `/agents`, um ihn sofort zu laden.
</Note>

```markdown  theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

Das Frontmatter definiert die Metadaten und Konfiguration des Subagenten. Der Body wird zum Systemprompt, der das Verhalten des Subagenten leitet. Subagenten erhalten nur diesen Systemprompt (plus grundlegende Umgebungsdetails wie Arbeitsverzeichnis), nicht den vollständigen Claude Code-Systemprompt.

#### Unterstützte Frontmatter-Felder

Die folgenden Felder können im YAML-Frontmatter verwendet werden. Nur `name` und `description` sind erforderlich.

| Feld              | Erforderlich | Beschreibung                                                                                                                                                                                                                                                                                                                       |
| :---------------- | :----------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | Ja           | Eindeutige Kennung mit Kleinbuchstaben und Bindestrichen                                                                                                                                                                                                                                                                           |
| `description`     | Ja           | Wann Claude an diesen Subagenten delegieren sollte                                                                                                                                                                                                                                                                                 |
| `tools`           | Nein         | [Werkzeuge](#available-tools), die der Subagent verwenden kann. Erbt alle Werkzeuge, wenn weggelassen                                                                                                                                                                                                                              |
| `disallowedTools` | Nein         | Werkzeuge zum Verweigern, entfernt aus geerbter oder angegebener Liste                                                                                                                                                                                                                                                             |
| `model`           | Nein         | [Modell](#choose-a-model) zu verwenden: `sonnet`, `opus`, `haiku`, eine vollständige Modell-ID (z. B. `claude-opus-4-6`) oder `inherit`. Standard ist `inherit`                                                                                                                                                                    |
| `permissionMode`  | Nein         | [Berechtigungsmodus](#permission-modes): `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions` oder `plan`                                                                                                                                                                                                              |
| `maxTurns`        | Nein         | Maximale Anzahl von Agenten-Turns, bevor der Subagent stoppt                                                                                                                                                                                                                                                                       |
| `skills`          | Nein         | [Skills](/de/skills) zum Laden in den Kontext des Subagenten beim Start. Der vollständige Skill-Inhalt wird eingespritzt, nicht nur zur Invokation verfügbar gemacht. Subagenten erben keine Skills von der übergeordneten Konversation                                                                                            |
| `mcpServers`      | Nein         | [MCP-Server](/de/mcp) verfügbar für diesen Subagenten. Jeder Eintrag ist entweder ein Servername, der auf einen bereits konfigurierten Server verweist (z. B. `"slack"`) oder eine Inline-Definition mit dem Servernamen als Schlüssel und einer vollständigen [MCP-Server-Konfiguration](/de/mcp#installing-mcp-servers) als Wert |
| `hooks`           | Nein         | [Lifecycle-Hooks](#define-hooks-for-subagents) mit Umfang auf diesen Subagenten                                                                                                                                                                                                                                                    |
| `memory`          | Nein         | [Persistenter Speicherumfang](#enable-persistent-memory): `user`, `project` oder `local`. Ermöglicht sitzungsübergreifendes Lernen                                                                                                                                                                                                 |
| `background`      | Nein         | Auf `true` setzen, um diesen Subagenten immer als [Hintergrundaufgabe](#run-subagents-in-foreground-or-background) auszuführen. Standard: `false`                                                                                                                                                                                  |
| `effort`          | Nein         | Aufwandsstufe, wenn dieser Subagent aktiv ist. Überschreibt die Aufwandsstufe der Sitzung. Standard: erbt von Sitzung. Optionen: `low`, `medium`, `high`, `max` (nur Opus 4.6)                                                                                                                                                     |
| `isolation`       | Nein         | Auf `worktree` setzen, um den Subagenten in einem temporären [Git-Worktree](/de/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) auszuführen, was ihm eine isolierte Kopie des Repositorys gibt. Der Worktree wird automatisch bereinigt, wenn der Subagent keine Änderungen vornimmt                        |
| `color`           | Nein         | Anzeigefarbe für den Subagenten in der Aufgabenliste und dem Transkript. Akzeptiert `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink` oder `cyan`                                                                                                                                                                       |
| `initialPrompt`   | Nein         | Auto-eingereicht als der erste Benutzer-Turn, wenn dieser Agent als Hauptsitzungs-Agent läuft (über `--agent` oder die `agent`-Einstellung). [Befehle](/de/commands) und [Skills](/de/skills) werden verarbeitet. Vorangestellt zu jedem vom Benutzer bereitgestellten Prompt                                                      |

### Wählen Sie ein Modell

Das `model`-Feld steuert, welches [KI-Modell](/de/model-config) der Subagent verwendet:

* **Modell-Alias**: Verwenden Sie einen der verfügbaren Aliase: `sonnet`, `opus` oder `haiku`
* **Vollständige Modell-ID**: Verwenden Sie eine vollständige Modell-ID wie `claude-opus-4-6` oder `claude-sonnet-4-6`. Akzeptiert dieselben Werte wie das `--model`-Flag
* **inherit**: Verwenden Sie dasselbe Modell wie die Hauptkonversation
* **Weggelassen**: Wenn nicht angegeben, wird standardmäßig `inherit` verwendet (verwendet dasselbe Modell wie die Hauptkonversation)

Wenn Claude einen Subagenten aufruft, kann es auch einen `model`-Parameter für diese spezifische Invokation übergeben. Claude Code löst das Modell des Subagenten in dieser Reihenfolge auf:

1. Die Umgebungsvariable [`CLAUDE_CODE_SUBAGENT_MODEL`](/de/model-config#environment-variables), falls gesetzt
2. Der `model`-Parameter pro Invokation
3. Das `model`-Frontmatter der Subagenten-Definition
4. Das Modell der Hauptkonversation

### Kontrollieren Sie Subagenten-Fähigkeiten

Sie können kontrollieren, was Subagenten durch Werkzeugzugriff, Berechtigungsmodi und bedingte Regeln tun können.

#### Verfügbare Werkzeuge

Subagenten können alle [internen Werkzeuge](/de/tools-reference) von Claude Code verwenden. Standardmäßig erben Subagenten alle Werkzeuge von der Hauptkonversation, einschließlich MCP-Werkzeuge.

Um Werkzeuge einzuschränken, verwenden Sie das `tools`-Feld (Allowlist) oder das `disallowedTools`-Feld (Denylist). Dieses Beispiel verwendet `tools`, um ausschließlich Read, Grep, Glob und Bash zuzulassen. Der Subagent kann keine Dateien bearbeiten, keine Dateien schreiben oder MCP-Werkzeuge verwenden:

```yaml  theme={null}
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

Dieses Beispiel verwendet `disallowedTools`, um alle Werkzeuge von der Hauptkonversation zu erben, außer Write und Edit. Der Subagent behält Bash, MCP-Werkzeuge und alles andere:

```yaml  theme={null}
---
name: no-writes
description: Inherits every tool except file writes
disallowedTools: Write, Edit
---
```

Wenn beide gesetzt sind, wird `disallowedTools` zuerst angewendet, dann wird `tools` gegen den verbleibenden Pool aufgelöst. Ein Werkzeug, das in beiden aufgelistet ist, wird entfernt.

#### Beschränken Sie, welche Subagenten spawned werden können

Wenn ein Agent als Hauptthread mit `claude --agent` läuft, kann er Subagenten mit dem Agent-Werkzeug spawnen. Um zu beschränken, welche Subagenten-Typen er spawnen kann, verwenden Sie die `Agent(agent_type)`-Syntax im `tools`-Feld.

<Note>In Version 2.1.63 wurde das Task-Werkzeug in Agent umbenannt. Vorhandene `Task(...)`-Verweise in Einstellungen und Agent-Definitionen funktionieren weiterhin als Aliase.</Note>

```yaml  theme={null}
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

Dies ist eine Allowlist: Nur die `worker`- und `researcher`-Subagenten können gespawnt werden. Wenn der Agent versucht, einen anderen Typ zu spawnen, schlägt die Anfrage fehl und der Agent sieht nur die zulässigen Typen in seinem Prompt. Um bestimmte Agenten zu blockieren und alle anderen zuzulassen, verwenden Sie stattdessen [`permissions.deny`](#disable-specific-subagents).

Um das Spawnen eines beliebigen Subagenten ohne Einschränkungen zu ermöglichen, verwenden Sie `Agent` ohne Klammern:

```yaml  theme={null}
tools: Agent, Read, Bash
```

Wenn `Agent` vollständig aus der `tools`-Liste weggelassen wird, kann der Agent keine Subagenten spawnen. Diese Einschränkung gilt nur für Agenten, die als Hauptthread mit `claude --agent` laufen. Subagenten können keine anderen Subagenten spawnen, daher hat `Agent(agent_type)` keine Auswirkung in Subagenten-Definitionen.

#### Umfang von MCP-Servern auf einen Subagenten

Verwenden Sie das `mcpServers`-Feld, um einem Subagenten Zugriff auf [MCP](/de/mcp)-Server zu geben, die in der Hauptkonversation nicht verfügbar sind. Inline-Server, die hier definiert sind, werden verbunden, wenn der Subagent startet, und getrennt, wenn er endet. String-Verweise teilen die Verbindung der übergeordneten Sitzung.

Jeder Eintrag in der Liste ist entweder eine Inline-Server-Definition oder ein String, der auf einen bereits konfigurierten MCP-Server in Ihrer Sitzung verweist:

```yaml  theme={null}
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.
```

Inline-Definitionen verwenden dasselbe Schema wie `.mcp.json`-Server-Einträge (`stdio`, `http`, `sse`, `ws`), mit dem Servernamen als Schlüssel.

Um einen MCP-Server vollständig aus der Hauptkonversation herauszuhalten und zu vermeiden, dass seine Werkzeugbeschreibungen dort Kontext verbrauchen, definieren Sie ihn inline hier statt in `.mcp.json`. Der Subagent erhält die Werkzeuge; die übergeordnete Konversation nicht.

#### Berechtigungsmodi

Das `permissionMode`-Feld steuert, wie der Subagent Berechtigungsaufforderungen bearbeitet. Subagenten erben den Berechtigungskontext von der Hauptkonversation und können den Modus überschreiben, außer wenn der übergeordnete Modus Vorrang hat, wie unten beschrieben.

| Modus               | Verhalten                                                                                                                                                     |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `default`           | Standardberechtigungsprüfung mit Aufforderungen                                                                                                               |
| `acceptEdits`       | Automatische Akzeptanz von Dateibearbeitungen außer in geschützten Verzeichnissen                                                                             |
| `auto`              | [Auto-Modus](/de/permission-modes#eliminate-prompts-with-auto-mode): ein KI-Klassifizierer bewertet Befehle und Schreibvorgänge in geschützten Verzeichnissen |
| `dontAsk`           | Automatische Ablehnung von Berechtigungsaufforderungen (explizit zulässige Werkzeuge funktionieren weiterhin)                                                 |
| `bypassPermissions` | Alle Berechtigungsprüfungen überspringen                                                                                                                      |
| `plan`              | Plan-Modus (schreibgeschützte Exploration)                                                                                                                    |

<Warning>
  Verwenden Sie `bypassPermissions` mit Vorsicht. Es überspringt Berechtigungsaufforderungen und ermöglicht dem Subagenten, Operationen ohne Genehmigung auszuführen. Schreibvorgänge in `.git`-, `.claude`-, `.vscode`-, `.idea`- und `.husky`-Verzeichnissen werden weiterhin zur Bestätigung aufgefordert, außer für `.claude/commands`, `.claude/agents` und `.claude/skills`. Siehe [Berechtigungsmodi](/de/permission-modes#skip-all-checks-with-bypasspermissions-mode) für Details.
</Warning>

Wenn das übergeordnete Element `bypassPermissions` verwendet, hat dies Vorrang und kann nicht überschrieben werden. Wenn das übergeordnete Element den [Auto-Modus](/de/permission-modes#eliminate-prompts-with-auto-mode) verwendet, erbt der Subagent den Auto-Modus und jedes `permissionMode` in seinem Frontmatter wird ignoriert: der Klassifizierer bewertet die Werkzeugaufrufe des Subagenten mit denselben Block- und Zulassungsregeln wie die übergeordnete Sitzung.

#### Laden Sie Skills in Subagenten vor

Verwenden Sie das `skills`-Feld, um Skill-Inhalte beim Start in den Kontext eines Subagenten einzuspeisen. Dies gibt dem Subagenten Domänenwissen, ohne dass er Skills während der Ausführung entdecken und laden muss.

```yaml  theme={null}
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

Der vollständige Inhalt jedes Skills wird in den Kontext des Subagenten eingespritzt, nicht nur zur Invokation verfügbar gemacht. Subagenten erben keine Skills von der übergeordneten Konversation; Sie müssen sie explizit auflisten.

<Note>
  Dies ist das Gegenteil von [Ausführen eines Skills in einem Subagenten](/de/skills#run-skills-in-a-subagent). Mit `skills` in einem Subagenten kontrolliert der Subagent den Systemprompt und lädt Skill-Inhalte. Mit `context: fork` in einem Skill wird der Skill-Inhalt in den von Ihnen angegebenen Agent eingespritzt. Beide verwenden dasselbe zugrunde liegende System.
</Note>

#### Aktivieren Sie persistenten Speicher

Das `memory`-Feld gibt dem Subagenten ein persistentes Verzeichnis, das über Konversationen hinweg bestehen bleibt. Der Subagent verwendet dieses Verzeichnis, um im Laufe der Zeit Wissen aufzubauen, wie z. B. Codebase-Muster, Debugging-Erkenntnisse und architektonische Entscheidungen.

```yaml  theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

Wählen Sie einen Umfang basierend darauf, wie breit der Speicher angewendet werden sollte:

| Umfang    | Ort                                           | Verwenden Sie, wenn                                                                                            |
| :-------- | :-------------------------------------------- | :------------------------------------------------------------------------------------------------------------- |
| `user`    | `~/.claude/agent-memory/<name-of-agent>/`     | der Subagent Erkenntnisse über alle Projekte hinweg merken sollte                                              |
| `project` | `.claude/agent-memory/<name-of-agent>/`       | das Wissen des Subagenten projektspezifisch ist und über Versionskontrolle teilbar ist                         |
| `local`   | `.claude/agent-memory-local/<name-of-agent>/` | das Wissen des Subagenten projektspezifisch ist, aber nicht in die Versionskontrolle eingecheckt werden sollte |

Wenn der Speicher aktiviert ist:

* Der Systemprompt des Subagenten enthält Anweisungen zum Lesen und Schreiben in das Speicherverzeichnis.
* Der Systemprompt des Subagenten enthält auch die ersten 200 Zeilen oder 25 KB von `MEMORY.md` im Speicherverzeichnis, je nachdem, was zuerst kommt, mit Anweisungen zur Verwaltung von `MEMORY.md`, wenn es diese Grenze überschreitet.
* Read-, Write- und Edit-Werkzeuge werden automatisch aktiviert, damit der Subagent seine Speicherdateien verwalten kann.

##### Tipps zum persistenten Speicher

* `project` ist der empfohlene Standard-Umfang. Es macht Subagenten-Wissen über Versionskontrolle teilbar. Verwenden Sie `user`, wenn das Wissen des Subagenten über Projekte hinweg breit anwendbar ist, oder `local`, wenn das Wissen nicht in die Versionskontrolle eingecheckt werden sollte.
* Bitten Sie den Subagenten, seinen Speicher vor dem Start zu konsultieren: "Review this PR, and check your memory for patterns you've seen before."
* Bitten Sie den Subagenten, seinen Speicher nach Abschluss einer Aufgabe zu aktualisieren: "Now that you're done, save what you learned to your memory." Im Laufe der Zeit baut dies eine Wissensdatenbank auf, die den Subagenten effektiver macht.
* Fügen Sie Speicheranweisungen direkt in die Markdown-Datei des Subagenten ein, damit er proaktiv seine eigene Wissensdatenbank verwaltet:

  ```markdown  theme={null}
  Update your agent memory as you discover codepaths, patterns, library
  locations, and key architectural decisions. This builds up institutional
  knowledge across conversations. Write concise notes about what you found
  and where.
  ```

#### Bedingte Regeln mit Hooks

Für dynamischere Kontrolle über die Werkzeugnutzung verwenden Sie `PreToolUse`-Hooks, um Operationen vor ihrer Ausführung zu validieren. Dies ist nützlich, wenn Sie einige Operationen eines Werkzeugs zulassen möchten, während Sie andere blockieren.

Dieses Beispiel erstellt einen Subagenten, der nur schreibgeschützte Datenbankabfragen zulässt. Der `PreToolUse`-Hook führt das in `command` angegebene Skript vor jeder Bash-Befehlsausführung aus:

```yaml  theme={null}
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

Claude Code [übergibt Hook-Eingabe als JSON](/de/hooks#pretooluse-input) über stdin an Hook-Befehle. Das Validierungsskript liest dieses JSON, extrahiert den Bash-Befehl und [beendet mit Code 2](/de/hooks#exit-code-2-behavior-per-event), um Schreibvorgänge zu blockieren:

```bash  theme={null}
#!/bin/bash
# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

Siehe [Hook-Eingabe](/de/hooks#pretooluse-input) für das vollständige Eingabeschema und [Exit-Codes](/de/hooks#exit-code-output) für die Auswirkungen von Exit-Codes auf das Verhalten.

#### Deaktivieren Sie spezifische Subagenten

Sie können verhindern, dass Claude bestimmte Subagenten verwendet, indem Sie sie zum `deny`-Array in Ihren [Einstellungen](/de/settings#permission-settings) hinzufügen. Verwenden Sie das Format `Agent(subagent-name)`, wobei `subagent-name` dem `name`-Feld des Subagenten entspricht.

```json  theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

Dies funktioniert für integrierte und benutzerdefinierte Subagenten. Sie können auch das `--disallowedTools`-CLI-Flag verwenden:

```bash  theme={null}
claude --disallowedTools "Agent(Explore)"
```

Siehe [Berechtigungsdokumentation](/de/permissions#tool-specific-permission-rules) für weitere Details zu Berechtigungsregeln.

### Definieren Sie Hooks für Subagenten

Subagenten können [Hooks](/de/hooks) definieren, die während des Lebenszyklus des Subagenten ausgeführt werden. Es gibt zwei Möglichkeiten, Hooks zu konfigurieren:

1. **Im Frontmatter des Subagenten**: Definieren Sie Hooks, die nur ausgeführt werden, während dieser Subagent aktiv ist
2. **In `settings.json`**: Definieren Sie Hooks, die in der Hauptsitzung ausgeführt werden, wenn Subagenten starten oder stoppen

#### Hooks im Subagenten-Frontmatter

Definieren Sie Hooks direkt in der Markdown-Datei des Subagenten. Diese Hooks werden nur ausgeführt, während dieser spezifische Subagent aktiv ist, und werden bereinigt, wenn er endet.

Alle [Hook-Ereignisse](/de/hooks#hook-events) werden unterstützt. Die häufigsten Ereignisse für Subagenten sind:

| Ereignis      | Matcher-Eingabe | Wann es ausgelöst wird                                                    |
| :------------ | :-------------- | :------------------------------------------------------------------------ |
| `PreToolUse`  | Werkzeugname    | Bevor der Subagent ein Werkzeug verwendet                                 |
| `PostToolUse` | Werkzeugname    | Nachdem der Subagent ein Werkzeug verwendet hat                           |
| `Stop`        | (keine)         | Wenn der Subagent endet (wird zur Laufzeit in `SubagentStop` konvertiert) |

Dieses Beispiel validiert Bash-Befehle mit dem `PreToolUse`-Hook und führt einen Linter nach Dateibearbeitungen mit `PostToolUse` aus:

```yaml  theme={null}
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

`Stop`-Hooks im Frontmatter werden automatisch in `SubagentStop`-Ereignisse konvertiert.

#### Hooks auf Projektebene für Subagenten-Ereignisse

Konfigurieren Sie Hooks in `settings.json`, die auf Subagenten-Lebenszyklus-Ereignisse in der Hauptsitzung reagieren.

| Ereignis        | Matcher-Eingabe | Wann es ausgelöst wird                       |
| :-------------- | :-------------- | :------------------------------------------- |
| `SubagentStart` | Agent-Typname   | Wenn ein Subagent mit der Ausführung beginnt |
| `SubagentStop`  | Agent-Typname   | Wenn ein Subagent abgeschlossen ist          |

Beide Ereignisse unterstützen Matcher, um bestimmte Agent-Typen nach Name zu adressieren. Dieses Beispiel führt ein Setup-Skript nur aus, wenn der `db-agent`-Subagent startet, und ein Cleanup-Skript, wenn ein beliebiger Subagent stoppt:

```json  theme={null}
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

Siehe [Hooks](/de/hooks) für das vollständige Hook-Konfigurationsformat.

## Arbeiten Sie mit Subagenten

### Verstehen Sie automatische Delegation

Claude delegiert automatisch Aufgaben basierend auf der Aufgabenbeschreibung in Ihrer Anfrage, dem `description`-Feld in Subagenten-Konfigurationen und dem aktuellen Kontext. Um proaktive Delegation zu fördern, fügen Sie Phrasen wie "use proactively" in das `description`-Feld Ihres Subagenten ein.

### Rufen Sie Subagenten explizit auf

Wenn automatische Delegation nicht ausreicht, können Sie einen Subagenten selbst anfordern. Drei Muster eskalieren von einem einmaligen Vorschlag zu einem sitzungsweiten Standard:

* **Natürliche Sprache**: Nennen Sie den Subagenten in Ihrem Prompt; Claude entscheidet, ob delegiert werden soll
* **@-Erwähnung**: Garantiert, dass der Subagent für eine Aufgabe ausgeführt wird
* **Sitzungsweit**: Die gesamte Sitzung verwendet den Systemprompt, die Werkzeugbeschränkungen und das Modell dieses Subagenten über das `--agent`-Flag oder die `agent`-Einstellung

Für natürliche Sprache gibt es keine spezielle Syntax. Nennen Sie den Subagenten und Claude delegiert normalerweise:

```text  theme={null}
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

**@-Erwähnen Sie den Subagenten.** Geben Sie `@` ein und wählen Sie den Subagenten aus der Typeahead-Liste, genauso wie Sie Dateien @-erwähnen. Dies stellt sicher, dass dieser spezifische Subagent ausgeführt wird, anstatt die Wahl Claude zu überlassen:

```text  theme={null}
@"code-reviewer (agent)" look at the auth changes
```

Ihre vollständige Nachricht geht immer noch an Claude, das den Task-Prompt des Subagenten basierend auf Ihrer Anfrage schreibt. Die @-Erwähnung steuert, welcher Subagent Claude aufruft, nicht welchen Prompt er erhält.

Subagenten, die von einem aktivierten [Plugin](/de/plugins) bereitgestellt werden, erscheinen in der Typeahead-Liste als `<plugin-name>:<agent-name>`. Benannte Hintergrund-Subagenten, die derzeit in der Sitzung ausgeführt werden, erscheinen auch in der Typeahead-Liste und zeigen ihren Status neben dem Namen an. Sie können die Erwähnung auch manuell eingeben, ohne den Picker zu verwenden: `@agent-<name>` für lokale Subagenten oder `@agent-<plugin-name>:<agent-name>` für Plugin-Subagenten.

**Führen Sie die gesamte Sitzung als Subagent aus.** Übergeben Sie [`--agent <name>`](/de/cli-reference), um eine Sitzung zu starten, in der der Hauptthread selbst den Systemprompt, die Werkzeugbeschränkungen und das Modell dieses Subagenten annimmt:

```bash  theme={null}
claude --agent code-reviewer
```

Der Systemprompt des Subagenten ersetzt den Standard-Claude Code-Systemprompt vollständig, genauso wie [`--system-prompt`](/de/cli-reference) es tut. `CLAUDE.md`-Dateien und Projekt-Memory werden weiterhin durch den normalen Nachrichtenfluss geladen. Der Agent-Name erscheint als `@<name>` in der Startup-Kopfzeile, damit Sie bestätigen können, dass er aktiv ist.

Dies funktioniert mit integrierten und benutzerdefinierten Subagenten, und die Wahl bleibt bestehen, wenn Sie die Sitzung fortsetzen.

Für einen von einem Plugin bereitgestellten Subagenten übergeben Sie den scoped Namen: `claude --agent <plugin-name>:<agent-name>`.

Um es zum Standard für jede Sitzung in einem Projekt zu machen, setzen Sie `agent` in `.claude/settings.json`:

```json  theme={null}
{
  "agent": "code-reviewer"
}
```

Das CLI-Flag überschreibt die Einstellung, wenn beide vorhanden sind.

### Führen Sie Subagenten im Vordergrund oder Hintergrund aus

Subagenten können im Vordergrund (blockierend) oder Hintergrund (gleichzeitig) ausgeführt werden:

* **Vordergrund-Subagenten** blockieren die Hauptkonversation bis zur Fertigstellung. Berechtigungsaufforderungen und Klarstellungsfragen (wie [`AskUserQuestion`](/de/tools-reference)) werden an Sie weitergeleitet.
* **Hintergrund-Subagenten** laufen gleichzeitig, während Sie weiterarbeiten. Vor dem Start fordert Claude Code alle Werkzeugberechtigungen an, die der Subagent benötigt, um sicherzustellen, dass er die erforderlichen Genehmigungen hat. Nach dem Start erbt der Subagent diese Berechtigungen und lehnt automatisch alles ab, was nicht vorab genehmigt wurde. Wenn ein Hintergrund-Subagent Klarstellungsfragen stellen muss, schlägt dieser Werkzeugaufruf fehl, aber der Subagent setzt fort.

Wenn ein Hintergrund-Subagent aufgrund fehlender Berechtigungen fehlschlägt, können Sie einen neuen Vordergrund-Subagenten mit derselben Aufgabe starten, um es mit interaktiven Aufforderungen erneut zu versuchen.

Claude entscheidet, ob Subagenten im Vordergrund oder Hintergrund ausgeführt werden, basierend auf der Aufgabe. Sie können auch:

* Claude bitten, "run this in the background" auszuführen
* **Ctrl+B** drücken, um eine laufende Aufgabe in den Hintergrund zu verschieben

Um alle Hintergrund-Aufgaben-Funktionalität zu deaktivieren, setzen Sie die Umgebungsvariable `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` auf `1`. Siehe [Umgebungsvariablen](/de/env-vars).

### Häufige Muster

#### Isolieren Sie hochvolumige Operationen

Eine der effektivsten Verwendungen für Subagenten ist die Isolierung von Operationen, die große Mengen an Ausgaben erzeugen. Das Ausführen von Tests, das Abrufen von Dokumentation oder die Verarbeitung von Protokolldateien kann erheblichen Kontext verbrauchen. Durch die Delegierung an einen Subagenten bleibt die ausführliche Ausgabe im Kontext des Subagenten, während nur die relevante Zusammenfassung zu Ihrer Hauptkonversation zurückkehrt.

```text  theme={null}
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### Führen Sie parallele Recherche durch

Für unabhängige Untersuchungen spawnen Sie mehrere Subagenten, um gleichzeitig zu arbeiten:

```text  theme={null}
Research the authentication, database, and API modules in parallel using separate subagents
```

Jeder Subagent erkundet seinen Bereich unabhängig, dann synthetisiert Claude die Erkenntnisse. Dies funktioniert am besten, wenn die Recherchepfade nicht voneinander abhängen.

<Warning>
  Wenn Subagenten abgeschlossen sind, kehren ihre Ergebnisse zu Ihrer Hauptkonversation zurück. Das Ausführen vieler Subagenten, die jeweils detaillierte Ergebnisse zurückgeben, kann erheblichen Kontext verbrauchen.
</Warning>

Für Aufgaben, die anhaltende Parallelität benötigen oder Ihr Kontextfenster überschreiten, geben [Agent-Teams](/de/agent-teams) jedem Worker seinen eigenen unabhängigen Kontext.

#### Verketten Sie Subagenten

Für mehrstufige Workflows bitten Sie Claude, Subagenten nacheinander zu verwenden. Jeder Subagent vervollständigt seine Aufgabe und gibt Ergebnisse an Claude zurück, das dann relevanten Kontext an den nächsten Subagenten übergibt.

```text  theme={null}
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Wählen Sie zwischen Subagenten und Hauptkonversation

Verwenden Sie die **Hauptkonversation**, wenn:

* Die Aufgabe häufiges Hin und Her oder iterative Verfeinerung benötigt
* Mehrere Phasen teilen erheblichen Kontext (Planung → Implementierung → Testen)
* Sie eine schnelle, gezielte Änderung vornehmen
* Latenz ist wichtig. Subagenten starten von vorne und benötigen möglicherweise Zeit, um Kontext zu sammeln

Verwenden Sie **Subagenten**, wenn:

* Die Aufgabe ausführliche Ausgaben erzeugt, die Sie nicht in Ihrem Hauptkontext benötigen
* Sie spezifische Werkzeugbeschränkungen oder Berechtigungen durchsetzen möchten
* Die Arbeit in sich geschlossen ist und eine Zusammenfassung zurückgeben kann

Erwägen Sie stattdessen [Skills](/de/skills), wenn Sie wiederverwendbare Prompts oder Workflows möchten, die im Kontext der Hauptkonversation ausgeführt werden, anstatt in isoliertem Subagenten-Kontext.

Für eine schnelle Frage zu etwas, das bereits in Ihrer Konversation ist, verwenden Sie stattdessen [`/btw`](/de/interactive-mode#side-questions-with-btw). Es sieht Ihren vollständigen Kontext, hat aber keinen Werkzeugzugriff, und die Antwort wird verworfen, anstatt zur Historie hinzugefügt zu werden.

<Note>
  Subagenten können keine anderen Subagenten spawnen. Wenn Ihr Workflow verschachtelte Delegation erfordert, verwenden Sie [Skills](/de/skills) oder [verketten Sie Subagenten](#chain-subagents) von der Hauptkonversation.
</Note>

### Verwalten Sie den Subagenten-Kontext

#### Setzen Sie Subagenten fort

Jede Subagenten-Invokation erstellt eine neue Instanz mit frischem Kontext. Um die Arbeit eines vorhandenen Subagenten fortzusetzen, anstatt von vorne zu beginnen, bitten Sie Claude, ihn fortzusetzen.

Fortgesetzte Subagenten behalten ihre vollständige Konversationshistorie, einschließlich aller vorherigen Werkzeugaufrufe, Ergebnisse und Überlegungen. Der Subagent setzt genau dort an, wo er gestoppt hat, anstatt von vorne zu beginnen.

Wenn ein Subagent abgeschlossen ist, erhält Claude seine Agent-ID. Claude verwendet das `SendMessage`-Werkzeug mit der Agent-ID des Agenten als `to`-Feld, um ihn fortzusetzen. Das `SendMessage`-Werkzeug ist nur verfügbar, wenn [Agent-Teams](/de/agent-teams) über `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` aktiviert sind.

Um einen Subagenten fortzusetzen, bitten Sie Claude, die vorherige Arbeit fortzusetzen:

```text  theme={null}
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

Wenn ein gestoppter Subagent eine `SendMessage` erhält, wird er automatisch im Hintergrund fortgesetzt, ohne dass eine neue `Agent`-Invokation erforderlich ist.

Sie können Claude auch nach der Agent-ID fragen, wenn Sie sie explizit referenzieren möchten, oder IDs in den Transkriptdateien unter `~/.claude/projects/{project}/{sessionId}/subagents/` finden. Jedes Transkript wird als `agent-{agentId}.jsonl` gespeichert.

Subagenten-Transkripte bleiben unabhängig von der Hauptkonversation bestehen:

* **Hauptkonversations-Komprimierung**: Wenn die Hauptkonversation komprimiert wird, sind Subagenten-Transkripte nicht betroffen. Sie werden in separaten Dateien gespeichert.
* **Sitzungs-Persistenz**: Subagenten-Transkripte bleiben innerhalb ihrer Sitzung bestehen. Sie können [einen Subagenten fortsetzen](#resume-subagents), nachdem Sie Claude Code neu gestartet haben, indem Sie dieselbe Sitzung fortsetzen.
* **Automatische Bereinigung**: Transkripte werden basierend auf der `cleanupPeriodDays`-Einstellung bereinigt (Standard: 30 Tage).

#### Auto-Komprimierung

Subagenten unterstützen automatische Komprimierung mit derselben Logik wie die Hauptkonversation. Standardmäßig wird die Auto-Komprimierung bei ungefähr 95 % Kapazität ausgelöst. Um die Komprimierung früher auszulösen, setzen Sie `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` auf einen niedrigeren Prozentsatz (z. B. `50`). Siehe [Umgebungsvariablen](/de/env-vars) für Details.

Komprimierungsereignisse werden in Subagenten-Transkriptdateien protokolliert:

```json  theme={null}
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}
```

Der `preTokens`-Wert zeigt, wie viele Token vor der Komprimierung verwendet wurden.

## Beispiel-Subagenten

Diese Beispiele demonstrieren effektive Muster für die Erstellung von Subagenten. Verwenden Sie sie als Ausgangspunkte oder generieren Sie eine angepasste Version mit Claude.

<Tip>
  **Best Practices:**

  * **Entwerfen Sie fokussierte Subagenten:** Jeder Subagent sollte bei einer spezifischen Aufgabe hervorragend sein
  * **Schreiben Sie detaillierte Beschreibungen:** Claude verwendet die Beschreibung, um zu entscheiden, wann delegiert werden soll
  * **Begrenzen Sie den Werkzeugzugriff:** Gewähren Sie nur notwendige Berechtigungen für Sicherheit und Fokus
  * **Checken Sie in die Versionskontrolle ein:** Teilen Sie Projekt-Subagenten mit Ihrem Team
</Tip>

### Code-Reviewer

Ein schreibgeschützter Subagent, der Code überprüft, ohne ihn zu ändern. Dieses Beispiel zeigt, wie man einen fokussierten Subagenten mit begrenztem Werkzeugzugriff (kein Edit oder Write) und einem detaillierten Prompt entwirft, der genau angibt, worauf zu achten ist und wie die Ausgabe formatiert wird.

```markdown  theme={null}
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### Debugger

Ein Subagent, der sowohl Probleme analysieren als auch beheben kann. Im Gegensatz zum Code-Reviewer enthält dieser Edit, da das Beheben von Bugs die Änderung von Code erfordert. Der Prompt bietet einen klaren Workflow von der Diagnose zur Verifizierung.

```markdown  theme={null}
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### Data Scientist

Ein domänenspezifischer Subagent für Datenanalyse-Arbeiten. Dieses Beispiel zeigt, wie man Subagenten für spezialisierte Workflows außerhalb typischer Coding-Aufgaben erstellt. Es setzt explizit `model: sonnet` für fähigere Analysen.

```markdown  theme={null}
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

### Datenbankabfrage-Validator

Ein Subagent, der Bash-Zugriff zulässt, aber Befehle validiert, um nur schreibgeschützte SQL-Abfragen zu ermöglichen. Dieses Beispiel zeigt, wie man `PreToolUse`-Hooks für bedingte Validierung verwendet, wenn Sie feinere Kontrolle benötigen, als das `tools`-Feld bietet.

```markdown  theme={null}
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.
```

Claude Code [übergibt Hook-Eingabe als JSON](/de/hooks#pretooluse-input) über stdin an Hook-Befehle. Das Validierungsskript liest dieses JSON, extrahiert den auszuführenden Befehl und prüft ihn gegen eine Liste von SQL-Schreibvorgängen. Wenn ein Schreibvorgang erkannt wird, [beendet das Skript mit Code 2](/de/hooks#exit-code-2-behavior-per-event), um die Ausführung zu blockieren, und gibt eine Fehlermeldung an Claude über stderr zurück.

Erstellen Sie das Validierungsskript überall in Ihrem Projekt. Der Pfad muss dem `command`-Feld in Ihrer Hook-Konfiguration entsprechen:

```bash  theme={null}
#!/bin/bash
# Blocks SQL write operations, allows SELECT queries

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0
```

Machen Sie das Skript ausführbar:

```bash  theme={null}
chmod +x ./scripts/validate-readonly-query.sh
```

Der Hook empfängt JSON über stdin mit dem Bash-Befehl in `tool_input.command`. Exit-Code 2 blockiert die Operation und leitet die Fehlermeldung an Claude weiter. Siehe [Hooks](/de/hooks#exit-code-output) für Details zu Exit-Codes und [Hook-Eingabe](/de/hooks#pretooluse-input) für das vollständige Eingabeschema.

## Nächste Schritte

Jetzt, da Sie Subagenten verstehen, erkunden Sie diese verwandten Funktionen:

* [Verteilen Sie Subagenten mit Plugins](/de/plugins), um Subagenten über Teams oder Projekte hinweg zu teilen
* [Führen Sie Claude Code programmgesteuert aus](/de/headless) mit dem Agent SDK für CI/CD und Automatisierung
* [Verwenden Sie MCP-Server](/de/mcp), um Subagenten Zugriff auf externe Werkzeuge und Daten zu geben
