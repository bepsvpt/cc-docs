> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Plugins erstellen

> Erstellen Sie benutzerdefinierte Plugins, um Claude Code mit Skills, Agents, Hooks und MCP-Servern zu erweitern.

Plugins ermöglichen es Ihnen, Claude Code mit benutzerdefinierten Funktionen zu erweitern, die projektübergreifend und teamübergreifend freigegeben werden können. Diese Anleitung behandelt die Erstellung eigener Plugins mit Skills, Agents, Hooks und MCP-Servern.

Möchten Sie vorhandene Plugins installieren? Siehe [Plugins entdecken und installieren](/de/discover-plugins). Für vollständige technische Spezifikationen siehe [Plugins-Referenz](/de/plugins-reference).

## Wann Plugins vs. eigenständige Konfiguration verwenden

Claude Code unterstützt zwei Möglichkeiten, um benutzerdefinierte Skills, Agents und Hooks hinzuzufügen:

| Ansatz                                                       | Skill-Namen          | Am besten für                                                                                                        |
| :----------------------------------------------------------- | :------------------- | :------------------------------------------------------------------------------------------------------------------- |
| **Eigenständig** (`.claude/`-Verzeichnis)                    | `/hello`             | Persönliche Workflows, projektspezifische Anpassungen, schnelle Experimente                                          |
| **Plugins** (Verzeichnisse mit `.claude-plugin/plugin.json`) | `/plugin-name:hello` | Freigabe für Teamkollegen, Verteilung an die Community, versionierte Releases, wiederverwendbar über Projekte hinweg |

**Verwenden Sie eigenständige Konfiguration, wenn**:

* Sie Claude Code für ein einzelnes Projekt anpassen
* Die Konfiguration persönlich ist und nicht freigegeben werden muss
* Sie mit Skills oder Hooks experimentieren, bevor Sie diese verpacken
* Sie kurze Skill-Namen wie `/hello` oder `/deploy` möchten

**Verwenden Sie Plugins, wenn**:

* Sie Funktionen mit Ihrem Team oder der Community teilen möchten
* Sie die gleichen Skills/Agents über mehrere Projekte hinweg benötigen
* Sie Versionskontrolle und einfache Updates für Ihre Erweiterungen möchten
* Sie über einen Marketplace verteilen
* Sie mit Namespace-Skills wie `/my-plugin:hello` einverstanden sind (Namespacing verhindert Konflikte zwischen Plugins)

<Tip>
  Beginnen Sie mit eigenständiger Konfiguration in `.claude/` für schnelle Iteration, dann [konvertieren Sie zu einem Plugin](#convert-existing-configurations-to-plugins), wenn Sie bereit sind zu teilen.
</Tip>

## Schnellstart

Dieser Schnellstart führt Sie durch die Erstellung eines Plugins mit einem benutzerdefinierten Skill. Sie erstellen ein Manifest (die Konfigurationsdatei, die Ihr Plugin definiert), fügen einen Skill hinzu und testen ihn lokal mit dem Flag `--plugin-dir`.

### Voraussetzungen

* Claude Code [installiert und authentifiziert](/de/quickstart#step-1-install-claude-code)
* Claude Code Version 1.0.33 oder später (führen Sie `claude --version` aus, um zu überprüfen)

<Note>
  Wenn Sie den Befehl `/plugin` nicht sehen, aktualisieren Sie Claude Code auf die neueste Version. Siehe [Troubleshooting](/de/troubleshooting) für Upgrade-Anweisungen.
</Note>

### Erstellen Sie Ihr erstes Plugin

<Steps>
  <Step title="Erstellen Sie das Plugin-Verzeichnis">
    Jedes Plugin befindet sich in seinem eigenen Verzeichnis, das ein Manifest und Ihre Skills, Agents oder Hooks enthält. Erstellen Sie jetzt eines:

    ```bash  theme={null}
    mkdir my-first-plugin
    ```
  </Step>

  <Step title="Erstellen Sie das Plugin-Manifest">
    Die Manifestdatei unter `.claude-plugin/plugin.json` definiert die Identität Ihres Plugins: seinen Namen, die Beschreibung und die Version. Claude Code verwendet diese Metadaten, um Ihr Plugin im Plugin-Manager anzuzeigen.

    Erstellen Sie das `.claude-plugin`-Verzeichnis in Ihrem Plugin-Ordner:

    ```bash  theme={null}
    mkdir my-first-plugin/.claude-plugin
    ```

    Erstellen Sie dann `my-first-plugin/.claude-plugin/plugin.json` mit diesem Inhalt:

    ```json my-first-plugin/.claude-plugin/plugin.json theme={null}
    {
    "name": "my-first-plugin",
    "description": "A greeting plugin to learn the basics",
    "version": "1.0.0",
    "author": {
    "name": "Your Name"
    }
    }
    ```

    | Feld          | Zweck                                                                                                              |
    | :------------ | :----------------------------------------------------------------------------------------------------------------- |
    | `name`        | Eindeutige Kennung und Skill-Namespace. Skills werden mit diesem Präfix versehen (z. B. `/my-first-plugin:hello`). |
    | `description` | Wird im Plugin-Manager angezeigt, wenn Sie Plugins durchsuchen oder installieren.                                  |
    | `version`     | Verfolgen Sie Releases mit [semantischer Versionierung](/de/plugins-reference#version-management).                 |
    | `author`      | Optional. Hilfreich für die Zuordnung.                                                                             |

    Für zusätzliche Felder wie `homepage`, `repository` und `license` siehe das [vollständige Manifest-Schema](/de/plugins-reference#plugin-manifest-schema).
  </Step>

  <Step title="Fügen Sie einen Skill hinzu">
    Skills befinden sich im Verzeichnis `skills/`. Jeder Skill ist ein Ordner, der eine Datei `SKILL.md` enthält. Der Ordnername wird zum Skill-Namen, mit dem Präfix des Plugin-Namespace (`hello/` in einem Plugin namens `my-first-plugin` erstellt `/my-first-plugin:hello`).

    Erstellen Sie ein Skill-Verzeichnis in Ihrem Plugin-Ordner:

    ```bash  theme={null}
    mkdir -p my-first-plugin/skills/hello
    ```

    Erstellen Sie dann `my-first-plugin/skills/hello/SKILL.md` mit diesem Inhalt:

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    description: Greet the user with a friendly message
    disable-model-invocation: true
    ---

    Greet the user warmly and ask how you can help them today.
    ```
  </Step>

  <Step title="Testen Sie Ihr Plugin">
    Führen Sie Claude Code mit dem Flag `--plugin-dir` aus, um Ihr Plugin zu laden:

    ```bash  theme={null}
    claude --plugin-dir ./my-first-plugin
    ```

    Sobald Claude Code startet, versuchen Sie Ihren neuen Skill:

    ```shell  theme={null}
    /my-first-plugin:hello
    ```

    Sie sehen Claude mit einer Begrüßung antworten. Führen Sie `/help` aus, um Ihren Skill unter dem Plugin-Namespace aufgelistet zu sehen.

    <Note>
      **Warum Namespacing?** Plugin-Skills sind immer mit Namespace versehen (wie `/greet:hello`), um Konflikte zu vermeiden, wenn mehrere Plugins Skills mit demselben Namen haben.

      Um das Namespace-Präfix zu ändern, aktualisieren Sie das Feld `name` in `plugin.json`.
    </Note>
  </Step>

  <Step title="Fügen Sie Skill-Argumente hinzu">
    Machen Sie Ihren Skill dynamisch, indem Sie Benutzereingaben akzeptieren. Der Platzhalter `$ARGUMENTS` erfasst jeden Text, den der Benutzer nach dem Skill-Namen bereitstellt.

    Aktualisieren Sie Ihre Datei `SKILL.md`:

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    description: Greet the user with a personalized message
    ---

    # Hello Skill

    Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.
    ```

    Führen Sie `/reload-plugins` aus, um die Änderungen zu übernehmen, und versuchen Sie dann den Skill mit Ihrem Namen:

    ```shell  theme={null}
    /my-first-plugin:hello Alex
    ```

    Claude wird Sie beim Namen begrüßen. Weitere Informationen zum Übergeben von Argumenten an Skills finden Sie unter [Skills](/de/skills#pass-arguments-to-skills).
  </Step>
</Steps>

Sie haben erfolgreich ein Plugin mit diesen Schlüsselkomponenten erstellt und getestet:

* **Plugin-Manifest** (`.claude-plugin/plugin.json`): beschreibt die Metadaten Ihres Plugins
* **Skills-Verzeichnis** (`skills/`): enthält Ihre benutzerdefinierten Skills
* **Skill-Argumente** (`$ARGUMENTS`): erfasst Benutzereingaben für dynamisches Verhalten

<Tip>
  Das Flag `--plugin-dir` ist nützlich für Entwicklung und Tests. Wenn Sie bereit sind, Ihr Plugin mit anderen zu teilen, siehe [Erstellen und verteilen Sie einen Plugin-Marketplace](/de/plugin-marketplaces).
</Tip>

## Übersicht über die Plugin-Struktur

Sie haben ein Plugin mit einem Skill erstellt, aber Plugins können viel mehr enthalten: benutzerdefinierte Agents, Hooks, MCP-Server und LSP-Server.

<Warning>
  **Häufiger Fehler**: Platzieren Sie `commands/`, `agents/`, `skills/` oder `hooks/` nicht im Verzeichnis `.claude-plugin/`. Nur `plugin.json` gehört in `.claude-plugin/`. Alle anderen Verzeichnisse müssen auf der Plugin-Root-Ebene sein.
</Warning>

| Verzeichnis       | Speicherort | Zweck                                                                                        |
| :---------------- | :---------- | :------------------------------------------------------------------------------------------- |
| `.claude-plugin/` | Plugin-Root | Enthält `plugin.json`-Manifest (optional, wenn Komponenten Standardspeicherorte verwenden)   |
| `commands/`       | Plugin-Root | Skills als Markdown-Dateien                                                                  |
| `agents/`         | Plugin-Root | Benutzerdefinierte Agent-Definitionen                                                        |
| `skills/`         | Plugin-Root | Agent-Skills mit `SKILL.md`-Dateien                                                          |
| `hooks/`          | Plugin-Root | Event-Handler in `hooks.json`                                                                |
| `.mcp.json`       | Plugin-Root | MCP-Server-Konfigurationen                                                                   |
| `.lsp.json`       | Plugin-Root | LSP-Server-Konfigurationen für Code-Intelligenz                                              |
| `settings.json`   | Plugin-Root | Standard-[Einstellungen](/de/settings), die angewendet werden, wenn das Plugin aktiviert ist |

<Note>
  **Nächste Schritte**: Bereit, weitere Funktionen hinzuzufügen? Springen Sie zu [Entwickeln Sie komplexere Plugins](#develop-more-complex-plugins), um Agents, Hooks, MCP-Server und LSP-Server hinzuzufügen. Für vollständige technische Spezifikationen aller Plugin-Komponenten siehe [Plugins-Referenz](/de/plugins-reference).
</Note>

## Entwickeln Sie komplexere Plugins

Sobald Sie sich mit grundlegenden Plugins vertraut gemacht haben, können Sie anspruchsvollere Erweiterungen erstellen.

### Fügen Sie Skills zu Ihrem Plugin hinzu

Plugins können [Agent-Skills](/de/skills) enthalten, um die Fähigkeiten von Claude zu erweitern. Skills werden vom Modell aufgerufen: Claude verwendet sie automatisch basierend auf dem Task-Kontext.

Fügen Sie ein Verzeichnis `skills/` auf Ihrer Plugin-Root mit Skill-Ordnern hinzu, die `SKILL.md`-Dateien enthalten:

```text  theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── code-review/
        └── SKILL.md
```

Jede `SKILL.md` benötigt Frontmatter mit den Feldern `name` und `description`, gefolgt von Anweisungen:

```yaml  theme={null}
---
name: code-review
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

Nach der Installation des Plugins führen Sie `/reload-plugins` aus, um die Skills zu laden. Für vollständige Anleitung zur Skill-Erstellung, einschließlich progressiver Offenlegung und Tool-Einschränkungen, siehe [Agent-Skills](/de/skills).

### Fügen Sie LSP-Server zu Ihrem Plugin hinzu

<Tip>
  Für gängige Sprachen wie TypeScript, Python und Rust installieren Sie die vorgefertigten LSP-Plugins aus dem offiziellen Marketplace. Erstellen Sie benutzerdefinierte LSP-Plugins nur, wenn Sie Unterstützung für Sprachen benötigen, die noch nicht abgedeckt sind.
</Tip>

LSP-Plugins (Language Server Protocol) geben Claude Echtzeit-Code-Intelligenz. Wenn Sie eine Sprache unterstützen müssen, die kein offizielles LSP-Plugin hat, können Sie ein eigenes erstellen, indem Sie eine `.lsp.json`-Datei zu Ihrem Plugin hinzufügen:

```json .lsp.json theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

Benutzer, die Ihr Plugin installieren, müssen die Language-Server-Binärdatei auf ihrem Computer installiert haben.

Für vollständige LSP-Konfigurationsoptionen siehe [LSP-Server](/de/plugins-reference#lsp-servers).

### Versenden Sie Standard-Einstellungen mit Ihrem Plugin

Plugins können eine Datei `settings.json` auf der Plugin-Root enthalten, um Standard-Konfiguration anzuwenden, wenn das Plugin aktiviert ist. Derzeit wird nur der Schlüssel `agent` unterstützt.

Das Setzen von `agent` aktiviert einen der [benutzerdefinierten Agents](/de/sub-agents) des Plugins als Haupt-Thread und wendet seinen System-Prompt, Tool-Einschränkungen und Modell an. Dies ermöglicht es einem Plugin, das Standardverhalten von Claude Code zu ändern, wenn es aktiviert ist.

```json settings.json theme={null}
{
  "agent": "security-reviewer"
}
```

Dieses Beispiel aktiviert den Agent `security-reviewer`, der im Verzeichnis `agents/` des Plugins definiert ist. Einstellungen aus `settings.json` haben Vorrang vor `settings`, die in `plugin.json` deklariert sind. Unbekannte Schlüssel werden stillschweigend ignoriert.

### Organisieren Sie komplexe Plugins

Für Plugins mit vielen Komponenten organisieren Sie Ihre Verzeichnisstruktur nach Funktionalität. Für vollständige Verzeichnislayouts und Organisationsmuster siehe [Plugin-Verzeichnisstruktur](/de/plugins-reference#plugin-directory-structure).

### Testen Sie Ihre Plugins lokal

Verwenden Sie das Flag `--plugin-dir`, um Plugins während der Entwicklung zu testen. Dies lädt Ihr Plugin direkt, ohne dass eine Installation erforderlich ist.

```bash  theme={null}
claude --plugin-dir ./my-plugin
```

Wenn ein `--plugin-dir`-Plugin denselben Namen wie ein installiertes Marketplace-Plugin hat, hat die lokale Kopie in dieser Sitzung Vorrang. Dies ermöglicht es Ihnen, Änderungen an einem Plugin zu testen, das Sie bereits installiert haben, ohne es zuerst zu deinstallieren. Marketplace-Plugins, die durch verwaltete Einstellungen erzwungen aktiviert sind, sind die einzige Ausnahme und können nicht überschrieben werden.

Wenn Sie Änderungen an Ihrem Plugin vornehmen, führen Sie `/reload-plugins` aus, um die Updates zu übernehmen, ohne neu zu starten. Dies lädt Befehle, Skills, Agents, Hooks, Plugin-MCP-Server und Plugin-LSP-Server neu. Testen Sie Ihre Plugin-Komponenten:

* Versuchen Sie Ihre Skills mit `/plugin-name:skill-name`
* Überprüfen Sie, dass Agents in `/agents` angezeigt werden
* Überprüfen Sie, dass Hooks wie erwartet funktionieren

<Tip>
  Sie können mehrere Plugins gleichzeitig laden, indem Sie das Flag mehrmals angeben:

  ```bash  theme={null}
  claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
  ```
</Tip>

### Debuggen Sie Plugin-Probleme

Wenn Ihr Plugin nicht wie erwartet funktioniert:

1. **Überprüfen Sie die Struktur**: Stellen Sie sicher, dass Ihre Verzeichnisse auf der Plugin-Root sind, nicht in `.claude-plugin/`
2. **Testen Sie Komponenten einzeln**: Überprüfen Sie jeden Befehl, Agent und Hook separat
3. **Verwenden Sie Validierungs- und Debugging-Tools**: Siehe [Debugging- und Entwicklungstools](/de/plugins-reference#debugging-and-development-tools) für CLI-Befehle und Troubleshooting-Techniken

### Teilen Sie Ihre Plugins

Wenn Ihr Plugin bereit zum Teilen ist:

1. **Fügen Sie Dokumentation hinzu**: Fügen Sie eine `README.md` mit Installations- und Verwendungsanweisungen ein
2. **Versionieren Sie Ihr Plugin**: Verwenden Sie [semantische Versionierung](/de/plugins-reference#version-management) in Ihrer `plugin.json`
3. **Erstellen oder verwenden Sie einen Marketplace**: Verteilen Sie über [Plugin-Marketplaces](/de/plugin-marketplaces) zur Installation
4. **Testen Sie mit anderen**: Lassen Sie Teamkollegen das Plugin vor einer breiteren Verteilung testen

Sobald Ihr Plugin in einem Marketplace ist, können andere es mit den Anweisungen in [Plugins entdecken und installieren](/de/discover-plugins) installieren.

### Reichen Sie Ihr Plugin beim offiziellen Marketplace ein

Um ein Plugin beim offiziellen Anthropic-Marketplace einzureichen, verwenden Sie eines der In-App-Einreichungsformulare:

* **Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
* **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

<Note>
  Für vollständige technische Spezifikationen, Debugging-Techniken und Verteilungsstrategien siehe [Plugins-Referenz](/de/plugins-reference).
</Note>

## Konvertieren Sie vorhandene Konfigurationen in Plugins

Wenn Sie bereits Skills oder Hooks in Ihrem Verzeichnis `.claude/` haben, können Sie diese in ein Plugin konvertieren, um die Freigabe und Verteilung zu vereinfachen.

### Migrationschritte

<Steps>
  <Step title="Erstellen Sie die Plugin-Struktur">
    Erstellen Sie ein neues Plugin-Verzeichnis:

    ```bash  theme={null}
    mkdir -p my-plugin/.claude-plugin
    ```

    Erstellen Sie die Manifestdatei unter `my-plugin/.claude-plugin/plugin.json`:

    ```json my-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "my-plugin",
      "description": "Migrated from standalone configuration",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Kopieren Sie Ihre vorhandenen Dateien">
    Kopieren Sie Ihre vorhandenen Konfigurationen in das Plugin-Verzeichnis:

    ```bash  theme={null}
    # Copy commands
    cp -r .claude/commands my-plugin/

    # Copy agents (if any)
    cp -r .claude/agents my-plugin/

    # Copy skills (if any)
    cp -r .claude/skills my-plugin/
    ```
  </Step>

  <Step title="Migrieren Sie Hooks">
    Wenn Sie Hooks in Ihren Einstellungen haben, erstellen Sie ein Hooks-Verzeichnis:

    ```bash  theme={null}
    mkdir my-plugin/hooks
    ```

    Erstellen Sie `my-plugin/hooks/hooks.json` mit Ihrer Hooks-Konfiguration. Kopieren Sie das Objekt `hooks` aus Ihrer `.claude/settings.json` oder `settings.local.json`, da das Format gleich ist. Der Befehl empfängt Hook-Eingaben als JSON auf stdin, verwenden Sie also `jq`, um den Dateipfad zu extrahieren:

    ```json my-plugin/hooks/hooks.json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }]
          }
        ]
      }
    }
    ```
  </Step>

  <Step title="Testen Sie Ihr migriertes Plugin">
    Laden Sie Ihr Plugin, um zu überprüfen, ob alles funktioniert:

    ```bash  theme={null}
    claude --plugin-dir ./my-plugin
    ```

    Testen Sie jede Komponente: Führen Sie Ihre Befehle aus, überprüfen Sie, dass Agents in `/agents` angezeigt werden, und überprüfen Sie, dass Hooks korrekt ausgelöst werden.
  </Step>
</Steps>

### Was sich bei der Migration ändert

| Eigenständig (`.claude/`)                 | Plugin                                    |
| :---------------------------------------- | :---------------------------------------- |
| Nur in einem Projekt verfügbar            | Kann über Marketplaces freigegeben werden |
| Dateien in `.claude/commands/`            | Dateien in `plugin-name/commands/`        |
| Hooks in `settings.json`                  | Hooks in `hooks/hooks.json`               |
| Muss manuell kopiert werden, um zu teilen | Mit `/plugin install` installieren        |

<Note>
  Nach der Migration können Sie die ursprünglichen Dateien aus `.claude/` entfernen, um Duplikate zu vermeiden. Die Plugin-Version hat Vorrang, wenn sie geladen wird.
</Note>

## Nächste Schritte

Jetzt, da Sie das Plugin-System von Claude Code verstehen, finden Sie hier vorgeschlagene Pfade für verschiedene Ziele:

### Für Plugin-Benutzer

* [Plugins entdecken und installieren](/de/discover-plugins): Durchsuchen Sie Marketplaces und installieren Sie Plugins
* [Konfigurieren Sie Team-Marketplaces](/de/discover-plugins#configure-team-marketplaces): Richten Sie Repository-Level-Plugins für Ihr Team ein

### Für Plugin-Entwickler

* [Erstellen und verteilen Sie einen Marketplace](/de/plugin-marketplaces): Verpacken und teilen Sie Ihre Plugins
* [Plugins-Referenz](/de/plugins-reference): Vollständige technische Spezifikationen
* Tauchen Sie tiefer in spezifische Plugin-Komponenten ein:
  * [Skills](/de/skills): Details zur Skill-Entwicklung
  * [Subagents](/de/sub-agents): Agent-Konfiguration und Fähigkeiten
  * [Hooks](/de/hooks): Event-Handling und Automatisierung
  * [MCP](/de/mcp): Integration externer Tools
