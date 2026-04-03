> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Erstellen und Verteilen eines Plugin-Marktplatzes

> Erstellen und hosten Sie Plugin-Marktplätze, um Claude Code-Erweiterungen in Teams und Communities zu verteilen.

Ein **Plugin-Marktplatz** ist ein Katalog, mit dem Sie Plugins an andere verteilen können. Marktplätze bieten zentrale Entdeckung, Versionsverfolgung, automatische Updates und Unterstützung für mehrere Quellentypen (Git-Repositories, lokale Pfade und mehr). Diese Anleitung zeigt Ihnen, wie Sie Ihren eigenen Marktplatz erstellen, um Plugins mit Ihrem Team oder Ihrer Community zu teilen.

Möchten Sie Plugins aus einem vorhandenen Marktplatz installieren? Siehe [Entdecken und Installieren vorgefertigter Plugins](/de/discover-plugins).

## Übersicht

Das Erstellen und Verteilen eines Marktplatzes umfasst:

1. **Plugins erstellen**: Erstellen Sie ein oder mehrere Plugins mit Befehlen, Agents, hooks, MCP servers oder LSP servers. Diese Anleitung setzt voraus, dass Sie bereits Plugins zum Verteilen haben; siehe [Plugins erstellen](/de/plugins) für Details zum Erstellen von Plugins.
2. **Marktplatzdatei erstellen**: Definieren Sie eine `marketplace.json`, die Ihre Plugins und deren Speicherorte auflistet (siehe [Marktplatzdatei erstellen](#create-the-marketplace-file)).
3. **Marktplatz hosten**: Pushen Sie zu GitHub, GitLab oder einem anderen Git-Host (siehe [Marktplätze hosten und verteilen](#host-and-distribute-marketplaces)).
4. **Mit Benutzern teilen**: Benutzer fügen Ihren Marktplatz mit `/plugin marketplace add` hinzu und installieren einzelne Plugins (siehe [Plugins entdecken und installieren](/de/discover-plugins)).

Sobald Ihr Marktplatz live ist, können Sie ihn aktualisieren, indem Sie Änderungen in Ihr Repository pushen. Benutzer aktualisieren ihre lokale Kopie mit `/plugin marketplace update`.

## Anleitung: Erstellen Sie einen lokalen Marktplatz

Dieses Beispiel erstellt einen Marktplatz mit einem Plugin: ein `/quality-review` skill für Code-Reviews. Sie erstellen die Verzeichnisstruktur, fügen ein skill hinzu, erstellen das Plugin-Manifest und den Marktplatzkatalog und installieren und testen ihn dann.

<Steps>
  <Step title="Erstellen Sie die Verzeichnisstruktur">
    ```bash  theme={null}
    mkdir -p my-marketplace/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/skills/quality-review
    ```
  </Step>

  <Step title="Erstellen Sie das skill">
    Erstellen Sie eine `SKILL.md`-Datei, die definiert, was das `/quality-review` skill tut.

    ```markdown my-marketplace/plugins/quality-review-plugin/skills/quality-review/SKILL.md theme={null}
    ---
    description: Review code for bugs, security, and performance
    disable-model-invocation: true
    ---

    Review the code I've selected or the recent changes for:
    - Potential bugs or edge cases
    - Security concerns
    - Performance issues
    - Readability improvements

    Be concise and actionable.
    ```
  </Step>

  <Step title="Erstellen Sie das Plugin-Manifest">
    Erstellen Sie eine `plugin.json`-Datei, die das Plugin beschreibt. Das Manifest befindet sich im `.claude-plugin/`-Verzeichnis.

    ```json my-marketplace/plugins/quality-review-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "quality-review-plugin",
      "description": "Adds a /quality-review skill for quick code reviews",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Erstellen Sie die Marktplatzdatei">
    Erstellen Sie den Marktplatzkatalog, der Ihr Plugin auflistet.

    ```json my-marketplace/.claude-plugin/marketplace.json theme={null}
    {
      "name": "my-plugins",
      "owner": {
        "name": "Your Name"
      },
      "plugins": [
        {
          "name": "quality-review-plugin",
          "source": "./plugins/quality-review-plugin",
          "description": "Adds a /quality-review skill for quick code reviews"
        }
      ]
    }
    ```
  </Step>

  <Step title="Hinzufügen und Installieren">
    Fügen Sie den Marktplatz hinzu und installieren Sie das Plugin.

    ```shell  theme={null}
    /plugin marketplace add ./my-marketplace
    /plugin install quality-review-plugin@my-plugins
    ```
  </Step>

  <Step title="Probieren Sie es aus">
    Wählen Sie etwas Code in Ihrem Editor aus und führen Sie Ihren neuen Befehl aus.

    ```shell  theme={null}
    /quality-review
    ```
  </Step>
</Steps>

Um mehr über die Möglichkeiten von Plugins zu erfahren, einschließlich hooks, Agents, MCP servers und LSP servers, siehe [Plugins](/de/plugins).

<Note>
  **Wie Plugins installiert werden**: Wenn Benutzer ein Plugin installieren, kopiert Claude Code das Plugin-Verzeichnis an einen Cache-Speicherort. Das bedeutet, dass Plugins keine Dateien außerhalb ihres Verzeichnisses mit Pfaden wie `../shared-utils` referenzieren können, da diese Dateien nicht kopiert werden.

  Wenn Sie Dateien über Plugins hinweg teilen müssen, verwenden Sie Symlinks (die während des Kopierens verfolgt werden). Siehe [Plugin-Caching und Dateiauflösung](/de/plugins-reference#plugin-caching-and-file-resolution) für Details.
</Note>

## Marktplatzdatei erstellen

Erstellen Sie `.claude-plugin/marketplace.json` im Stammverzeichnis Ihres Repositories. Diese Datei definiert den Namen Ihres Marktplatzes, Eigentümerinformationen und eine Liste von Plugins mit ihren Quellen.

Jeder Plugin-Eintrag benötigt mindestens einen `name` und eine `source` (wo man ihn abrufen kann). Siehe das [vollständige Schema](#marketplace-schema) unten für alle verfügbaren Felder.

```json  theme={null}
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting on save",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      }
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Deployment automation tools"
    }
  ]
}
```

## Marktplatz-Schema

### Erforderliche Felder

| Feld      | Typ    | Beschreibung                                                                                                                                                                             | Beispiel       |
| :-------- | :----- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------- |
| `name`    | string | Marktplatz-Identifier (Kebab-Case, keine Leerzeichen). Dies ist öffentlich sichtbar: Benutzer sehen es beim Installieren von Plugins (z. B. `/plugin install my-tool@your-marketplace`). | `"acme-tools"` |
| `owner`   | object | Informationen zum Marktplatz-Betreuer ([siehe Felder unten](#owner-fields))                                                                                                              |                |
| `plugins` | array  | Liste der verfügbaren Plugins                                                                                                                                                            | Siehe unten    |

<Note>
  **Reservierte Namen**: Die folgenden Marktplatznamen sind für die offizielle Nutzung durch Anthropic reserviert und können nicht von Drittanbieter-Marktplätzen verwendet werden: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `knowledge-work-plugins`, `life-sciences`. Namen, die offizielle Marktplätze imitieren (wie `official-claude-plugins` oder `anthropic-tools-v2`), sind ebenfalls blockiert.
</Note>

### Eigentümer-Felder

| Feld    | Typ    | Erforderlich | Beschreibung                    |
| :------ | :----- | :----------- | :------------------------------ |
| `name`  | string | Ja           | Name des Betreuers oder Teams   |
| `email` | string | Nein         | Kontakt-E-Mail für den Betreuer |

### Optionale Metadaten

| Feld                   | Typ    | Beschreibung                                                                                                                                                                                  |
| :--------------------- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `metadata.description` | string | Kurze Marktplatzbeschreibung                                                                                                                                                                  |
| `metadata.version`     | string | Marktplatz-Version                                                                                                                                                                            |
| `metadata.pluginRoot`  | string | Basisverzeichnis, das relativen Plugin-Quellpfaden vorangestellt wird (z. B. `"./plugins"` ermöglicht es Ihnen, `"source": "formatter"` statt `"source": "./plugins/formatter"` zu schreiben) |

## Plugin-Einträge

Jeder Plugin-Eintrag im `plugins`-Array beschreibt ein Plugin und wo man es findet. Sie können jedes Feld aus dem [Plugin-Manifest-Schema](/de/plugins-reference#plugin-manifest-schema) einbeziehen (wie `description`, `version`, `author`, `commands`, `hooks` usw.), plus diese Marktplatz-spezifischen Felder: `source`, `category`, `tags` und `strict`.

### Erforderliche Felder

| Feld     | Typ            | Beschreibung                                                                                                                                                          |
| :------- | :------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`   | string         | Plugin-Identifier (Kebab-Case, keine Leerzeichen). Dies ist öffentlich sichtbar: Benutzer sehen es beim Installieren (z. B. `/plugin install my-plugin@marketplace`). |
| `source` | string\|object | Wo das Plugin abgerufen werden soll (siehe [Plugin-Quellen](#plugin-sources) unten)                                                                                   |

### Optionale Plugin-Felder

**Standard-Metadatenfelder:**

| Feld          | Typ     | Beschreibung                                                                                                                       |
| :------------ | :------ | :--------------------------------------------------------------------------------------------------------------------------------- |
| `description` | string  | Kurze Plugin-Beschreibung                                                                                                          |
| `version`     | string  | Plugin-Version                                                                                                                     |
| `author`      | object  | Plugin-Autoreninformationen (`name` erforderlich, `email` optional)                                                                |
| `homepage`    | string  | Plugin-Homepage oder Dokumentations-URL                                                                                            |
| `repository`  | string  | Quellcode-Repository-URL                                                                                                           |
| `license`     | string  | SPDX-Lizenz-Identifier (z. B. MIT, Apache-2.0)                                                                                     |
| `keywords`    | array   | Tags für Plugin-Entdeckung und Kategorisierung                                                                                     |
| `category`    | string  | Plugin-Kategorie zur Organisation                                                                                                  |
| `tags`        | array   | Tags für Suchbarkeit                                                                                                               |
| `strict`      | boolean | Steuert, ob `plugin.json` die Autorität für Komponentendefinitionen ist (Standard: true). Siehe [Strict Mode](#strict-mode) unten. |

**Komponenten-Konfigurationsfelder:**

| Feld         | Typ            | Beschreibung                                                    |
| :----------- | :------------- | :-------------------------------------------------------------- |
| `commands`   | string\|array  | Benutzerdefinierte Pfade zu Befehlsdateien oder -verzeichnissen |
| `agents`     | string\|array  | Benutzerdefinierte Pfade zu Agent-Dateien                       |
| `hooks`      | string\|object | Benutzerdefinierte hooks-Konfiguration oder Pfad zu hooks-Datei |
| `mcpServers` | string\|object | MCP server-Konfigurationen oder Pfad zu MCP-Konfiguration       |
| `lspServers` | string\|object | LSP server-Konfigurationen oder Pfad zu LSP-Konfiguration       |

## Plugin-Quellen

Plugin-Quellen teilen Claude Code mit, wo jedes einzelne Plugin in Ihrem Marktplatz abgerufen werden soll. Diese werden im `source`-Feld jedes Plugin-Eintrags in `marketplace.json` festgelegt.

Sobald ein Plugin geklont oder auf den lokalen Computer kopiert wird, wird es in den lokalen versionierten Plugin-Cache unter `~/.claude/plugins/cache` kopiert.

| Quelle         | Typ                              | Felder                             | Notizen                                                                                          |
| -------------- | -------------------------------- | ---------------------------------- | ------------------------------------------------------------------------------------------------ |
| Relativer Pfad | `string` (z. B. `"./my-plugin"`) | —                                  | Lokales Verzeichnis im Marktplatz-Repo. Muss mit `./` beginnen                                   |
| `github`       | object                           | `repo`, `ref?`, `sha?`             |                                                                                                  |
| `url`          | object                           | `url`, `ref?`, `sha?`              | Git-URL-Quelle                                                                                   |
| `git-subdir`   | object                           | `url`, `path`, `ref?`, `sha?`      | Unterverzeichnis in einem Git-Repo. Klont sparsam, um die Bandbreite für Monorepos zu minimieren |
| `npm`          | object                           | `package`, `version?`, `registry?` | Installiert über `npm install`                                                                   |

<Note>
  **Marktplatz-Quellen vs. Plugin-Quellen**: Dies sind unterschiedliche Konzepte, die unterschiedliche Dinge steuern.

  * **Marktplatz-Quelle** — wo der `marketplace.json`-Katalog selbst abgerufen werden soll. Wird festgelegt, wenn Benutzer `/plugin marketplace add` ausführen oder in `extraKnownMarketplaces`-Einstellungen. Unterstützt `ref` (Branch/Tag), aber nicht `sha`.
  * **Plugin-Quelle** — wo ein einzelnes Plugin in der Marktplatz-Liste abgerufen werden soll. Wird im `source`-Feld jedes Plugin-Eintrags in `marketplace.json` festgelegt. Unterstützt sowohl `ref` (Branch/Tag) als auch `sha` (exakter Commit).

  Beispielsweise kann ein Marktplatz, der unter `acme-corp/plugin-catalog` gehostet wird (Marktplatz-Quelle), ein Plugin auflisten, das von `acme-corp/code-formatter` abgerufen wird (Plugin-Quelle). Die Marktplatz-Quelle und die Plugin-Quelle verweisen auf unterschiedliche Repositories und werden unabhängig voneinander angeheftet.
</Note>

### Relative Pfade

Für Plugins im selben Repository verwenden Sie einen Pfad, der mit `./` beginnt:

```json  theme={null}
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

Pfade werden relativ zum Marktplatz-Root aufgelöst, das ist das Verzeichnis, das `.claude-plugin/` enthält. Im obigen Beispiel verweist `./plugins/my-plugin` auf `<repo>/plugins/my-plugin`, obwohl `marketplace.json` unter `<repo>/.claude-plugin/marketplace.json` lebt. Verwenden Sie nicht `../`, um aus `.claude-plugin/` herauszuklettern.

<Note>
  Relative Pfade funktionieren nur, wenn Benutzer Ihren Marktplatz über Git hinzufügen (GitHub, GitLab oder Git-URL). Wenn Benutzer Ihren Marktplatz über eine direkte URL zur `marketplace.json`-Datei hinzufügen, werden relative Pfade nicht korrekt aufgelöst. Verwenden Sie für URL-basierte Verteilung stattdessen GitHub-, npm- oder Git-URL-Quellen. Siehe [Fehlerbehebung](#plugins-with-relative-paths-fail-in-url-based-marketplaces) für Details.
</Note>

### GitHub-Repositories

```json  theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

Sie können an einen bestimmten Branch, Tag oder Commit anheften:

```json  theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Feld   | Typ    | Beschreibung                                                                            |
| :----- | :----- | :-------------------------------------------------------------------------------------- |
| `repo` | string | Erforderlich. GitHub-Repository im Format `owner/repo`                                  |
| `ref`  | string | Optional. Git-Branch oder Tag (Standard: Standard-Branch des Repositories)              |
| `sha`  | string | Optional. Vollständiger 40-stelliger Git-Commit-SHA zum Anheften an eine exakte Version |

### Git-Repositories

```json  theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

Sie können an einen bestimmten Branch, Tag oder Commit anheften:

```json  theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Feld  | Typ    | Beschreibung                                                                                                                                                                      |
| :---- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url` | string | Erforderlich. Vollständige Git-Repository-URL (`https://` oder `git@`). Das `.git`-Suffix ist optional, daher funktionieren Azure DevOps- und AWS CodeCommit-URLs ohne das Suffix |
| `ref` | string | Optional. Git-Branch oder Tag (Standard: Standard-Branch des Repositories)                                                                                                        |
| `sha` | string | Optional. Vollständiger 40-stelliger Git-Commit-SHA zum Anheften an eine exakte Version                                                                                           |

### Git-Unterverzeichnisse

Verwenden Sie `git-subdir`, um auf ein Plugin zu verweisen, das sich in einem Unterverzeichnis eines Git-Repositories befindet. Claude Code verwendet einen sparsamen, teilweisen Klon, um nur das Unterverzeichnis abzurufen und die Bandbreite für große Monorepos zu minimieren.

```json  theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin"
  }
}
```

Sie können an einen bestimmten Branch, Tag oder Commit anheften:

```json  theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

Das `url`-Feld akzeptiert auch eine GitHub-Kurzform (`owner/repo`) oder SSH-URLs (`git@github.com:owner/repo.git`).

| Feld   | Typ    | Beschreibung                                                                                       |
| :----- | :----- | :------------------------------------------------------------------------------------------------- |
| `url`  | string | Erforderlich. Git-Repository-URL, GitHub `owner/repo`-Kurzform oder SSH-URL                        |
| `path` | string | Erforderlich. Unterverzeichnispfad im Repo, das das Plugin enthält (z. B. `"tools/claude-plugin"`) |
| `ref`  | string | Optional. Git-Branch oder Tag (Standard: Standard-Branch des Repositories)                         |
| `sha`  | string | Optional. Vollständiger 40-stelliger Git-Commit-SHA zum Anheften an eine exakte Version            |

### npm-Pakete

Plugins, die als npm-Pakete verteilt werden, werden mit `npm install` installiert. Dies funktioniert mit jedem Paket in der öffentlichen npm-Registry oder einer privaten Registry, die Ihr Team hostet.

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin"
  }
}
```

Um an eine bestimmte Version anzuheften, fügen Sie das `version`-Feld hinzu:

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "2.1.0"
  }
}
```

Um von einer privaten oder internen Registry zu installieren, fügen Sie das `registry`-Feld hinzu:

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

| Feld       | Typ    | Beschreibung                                                                                                  |
| :--------- | :----- | :------------------------------------------------------------------------------------------------------------ |
| `package`  | string | Erforderlich. Paketname oder Scoped-Paket (z. B. `@org/plugin`)                                               |
| `version`  | string | Optional. Version oder Versionsspanne (z. B. `2.1.0`, `^2.0.0`, `~1.5.0`)                                     |
| `registry` | string | Optional. Benutzerdefinierte npm-Registry-URL. Standard ist die System-npm-Registry (normalerweise npmjs.org) |

### Erweiterte Plugin-Einträge

Dieses Beispiel zeigt einen Plugin-Eintrag mit vielen optionalen Feldern, einschließlich benutzerdefinierter Pfade für Befehle, Agents, hooks und MCP servers:

```json  theme={null}
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Enterprise workflow automation tools",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "enterprise@example.com"
  },
  "homepage": "https://docs.example.com/plugins/enterprise-tools",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity",
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": ["./agents/security-reviewer.md", "./agents/compliance-checker.md"],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "enterprise-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  },
  "strict": false
}
```

Wichtige Dinge zu beachten:

* **`commands` und `agents`**: Sie können mehrere Verzeichnisse oder einzelne Dateien angeben. Pfade sind relativ zum Plugin-Root.
* **`${CLAUDE_PLUGIN_ROOT}`**: Verwenden Sie diese Variable in hooks und MCP server-Konfigurationen, um auf Dateien im Installationsverzeichnis des Plugins zu verweisen. Dies ist notwendig, da Plugins beim Installieren an einen Cache-Speicherort kopiert werden. Verwenden Sie für Abhängigkeiten oder Status, die Plugin-Updates überstehen sollten, stattdessen [`${CLAUDE_PLUGIN_DATA}`](/de/plugins-reference#persistent-data-directory).
* **`strict: false`**: Da dies auf false gesetzt ist, benötigt das Plugin keine eigene `plugin.json`. Der Marktplatz-Eintrag definiert alles. Siehe [Strict Mode](#strict-mode) unten.

### Strict Mode

Das `strict`-Feld steuert, ob `plugin.json` die Autorität für Komponentendefinitionen ist (Befehle, Agents, hooks, skills, MCP servers, Ausgabestile).

| Wert              | Verhalten                                                                                                                                                                                  |
| :---------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `true` (Standard) | `plugin.json` ist die Autorität. Der Marktplatz-Eintrag kann es mit zusätzlichen Komponenten ergänzen, und beide Quellen werden zusammengeführt.                                           |
| `false`           | Der Marktplatz-Eintrag ist die gesamte Definition. Wenn das Plugin auch eine `plugin.json` hat, die Komponenten deklariert, ist das ein Konflikt und das Plugin kann nicht geladen werden. |

**Wann jeder Modus verwendet werden sollte:**

* **`strict: true`**: Das Plugin hat seine eigene `plugin.json` und verwaltet seine eigenen Komponenten. Der Marktplatz-Eintrag kann zusätzliche Befehle oder hooks hinzufügen. Dies ist der Standard und funktioniert für die meisten Plugins.
* **`strict: false`**: Der Marktplatz-Betreiber möchte vollständige Kontrolle. Das Plugin-Repo stellt Rohdateien bereit, und der Marktplatz-Eintrag definiert, welche dieser Dateien als Befehle, Agents, hooks usw. verfügbar gemacht werden. Nützlich, wenn der Marktplatz die Komponenten eines Plugins anders strukturiert oder kuratiert als vom Plugin-Autor beabsichtigt.

## Marktplätze hosten und verteilen

### Auf GitHub hosten (empfohlen)

GitHub bietet die einfachste Verteilungsmethode:

1. **Repository erstellen**: Richten Sie ein neues Repository für Ihren Marktplatz ein
2. **Marktplatzdatei hinzufügen**: Erstellen Sie `.claude-plugin/marketplace.json` mit Ihren Plugin-Definitionen
3. **Mit Teams teilen**: Benutzer fügen Ihren Marktplatz mit `/plugin marketplace add owner/repo` hinzu

**Vorteile**: Integrierte Versionskontrolle, Issue-Tracking und Team-Zusammenarbeitsfunktionen.

### Auf anderen Git-Services hosten

Jeder Git-Hosting-Service funktioniert, wie GitLab, Bitbucket und selbstgehostete Server. Benutzer fügen mit der vollständigen Repository-URL hinzu:

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### Private Repositories

Claude Code unterstützt die Installation von Plugins aus privaten Repositories. Für manuelle Installation und Updates verwendet Claude Code Ihre vorhandenen Git-Credential-Helper. Wenn `git clone` für ein privates Repository in Ihrem Terminal funktioniert, funktioniert es auch in Claude Code. Häufige Credential-Helper sind `gh auth login` für GitHub, macOS Keychain und `git-credential-store`.

Hintergrund-Auto-Updates werden beim Start ohne Credential-Helper ausgeführt, da interaktive Eingabeaufforderungen Claude Code am Start hindern würden. Um Auto-Updates für private Marktplätze zu aktivieren, legen Sie das entsprechende Authentifizierungstoken in Ihrer Umgebung fest:

| Anbieter  | Umgebungsvariablen             | Notizen                                           |
| :-------- | :----------------------------- | :------------------------------------------------ |
| GitHub    | `GITHUB_TOKEN` oder `GH_TOKEN` | Persönliches Zugriffs-Token oder GitHub App-Token |
| GitLab    | `GITLAB_TOKEN` oder `GL_TOKEN` | Persönliches Zugriffs-Token oder Projekt-Token    |
| Bitbucket | `BITBUCKET_TOKEN`              | App-Passwort oder Repository-Zugriffs-Token       |

Legen Sie das Token in Ihrer Shell-Konfiguration fest (z. B. `.bashrc`, `.zshrc`) oder übergeben Sie es beim Ausführen von Claude Code:

```bash  theme={null}
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

<Note>
  Konfigurieren Sie das Token für CI/CD-Umgebungen als geheime Umgebungsvariable. GitHub Actions stellt automatisch `GITHUB_TOKEN` für Repositories in derselben Organisation bereit.
</Note>

### Lokal vor der Verteilung testen

Testen Sie Ihren Marktplatz lokal, bevor Sie ihn teilen:

```shell  theme={null}
/plugin marketplace add ./my-local-marketplace
/plugin install test-plugin@my-local-marketplace
```

Für die vollständige Palette von Add-Befehlen (GitHub, Git-URLs, lokale Pfade, Remote-URLs) siehe [Marktplätze hinzufügen](/de/discover-plugins#add-marketplaces).

### Marktplätze für Ihr Team erforderlich machen

Sie können Ihr Repository so konfigurieren, dass Teammitglieder automatisch aufgefordert werden, Ihren Marktplatz zu installieren, wenn sie dem Projektordner vertrauen. Fügen Sie Ihren Marktplatz zu `.claude/settings.json` hinzu:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

Sie können auch angeben, welche Plugins standardmäßig aktiviert sein sollen:

```json  theme={null}
{
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

Für vollständige Konfigurationsoptionen siehe [Plugin-Einstellungen](/de/settings#plugin-settings).

<Note>
  Wenn Sie eine lokale `directory`- oder `file`-Quelle mit einem relativen Pfad verwenden, wird der Pfad gegen den Haupt-Checkout Ihres Repositories aufgelöst. Wenn Sie Claude Code aus einem Git Worktree ausführen, verweist der Pfad immer noch auf den Haupt-Checkout, sodass alle Worktrees denselben Marktplatz-Speicherort teilen. Der Marktplatz-Status wird einmal pro Benutzer in `~/.claude/plugins/known_marketplaces.json` gespeichert, nicht pro Projekt.
</Note>

### Plugins für Container vorab ausfüllen

Für Container-Images und CI-Umgebungen können Sie ein Plugins-Verzeichnis zur Build-Zeit vorab ausfüllen, damit Claude Code mit bereits verfügbaren Marktplätzen und Plugins startet, ohne zur Laufzeit etwas zu klonen. Legen Sie die Umgebungsvariable `CLAUDE_CODE_PLUGIN_SEED_DIR` fest, um auf dieses Verzeichnis zu verweisen.

Um mehrere Seed-Verzeichnisse zu schichten, trennen Sie Pfade mit `:` auf Unix oder `;` auf Windows. Claude Code durchsucht jedes Verzeichnis in der Reihenfolge, und der erste Seed, der einen bestimmten Marktplatz oder Plugin-Cache enthält, gewinnt.

Das Seed-Verzeichnis spiegelt die Struktur von `~/.claude/plugins`:

```
$CLAUDE_CODE_PLUGIN_SEED_DIR/
  known_marketplaces.json
  marketplaces/<name>/...
  cache/<marketplace>/<plugin>/<version>/...
```

Der einfachste Weg, ein Seed-Verzeichnis zu erstellen, ist, Claude Code einmal während des Image-Builds auszuführen, die benötigten Plugins zu installieren, dann das resultierende `~/.claude/plugins`-Verzeichnis in Ihr Image zu kopieren und `CLAUDE_CODE_PLUGIN_SEED_DIR` darauf zu verweisen.

Beim Start registriert Claude Code Marktplätze, die in der Seed-Datei `known_marketplaces.json` gefunden werden, in der primären Konfiguration und verwendet Plugin-Caches, die unter `cache/` gefunden werden, ohne erneut zu klonen. Dies funktioniert sowohl im interaktiven Modus als auch im nicht-interaktiven Modus mit dem `-p`-Flag.

Verhaltensdetails:

* **Schreibgeschützt**: Das Seed-Verzeichnis wird nie geschrieben. Auto-Updates sind für Seed-Marktplätze deaktiviert, da git pull auf einem schreibgeschützten Dateisystem fehlschlagen würde.
* **Seed-Einträge haben Vorrang**: Marktplätze, die in der Seed deklariert sind, überschreiben alle übereinstimmenden Einträge in der Benutzerkonfiguration bei jedem Start. Um sich von einem Seed-Plugin abzumelden, verwenden Sie `/plugin disable`, anstatt den Marktplatz zu entfernen.
* **Pfadauflösung**: Claude Code lokalisiert Marktplatz-Inhalte, indem es `$CLAUDE_CODE_PLUGIN_SEED_DIR/marketplaces/<name>/` zur Laufzeit durchsucht, nicht indem es Pfaden vertraut, die in der Seed-JSON gespeichert sind. Dies bedeutet, dass die Seed korrekt funktioniert, auch wenn sie an einem anderen Pfad als dort, wo sie erstellt wurde, bereitgestellt wird.
* **Komponiert mit Einstellungen**: Wenn `extraKnownMarketplaces` oder `enabledPlugins` einen Marktplatz deklarieren, der bereits in der Seed vorhanden ist, verwendet Claude Code die Seed-Kopie, anstatt zu klonen.

### Verwaltete Marktplatz-Einschränkungen

Für Organisationen, die strikte Kontrolle über Plugin-Quellen benötigen, können Administratoren einschränken, welche Plugin-Marktplätze Benutzer hinzufügen dürfen, indem sie die Einstellung [`strictKnownMarketplaces`](/de/settings#strictknownmarketplaces) in verwalteten Einstellungen verwenden.

Wenn `strictKnownMarketplaces` in verwalteten Einstellungen konfiguriert ist, hängt das Einschränkungsverhalten vom Wert ab:

| Wert                       | Verhalten                                                                                    |
| -------------------------- | -------------------------------------------------------------------------------------------- |
| Nicht definiert (Standard) | Keine Einschränkungen. Benutzer können jeden Marktplatz hinzufügen                           |
| Leeres Array `[]`          | Vollständige Sperrung. Benutzer können keine neuen Marktplätze hinzufügen                    |
| Liste von Quellen          | Benutzer können nur Marktplätze hinzufügen, die genau mit der Zulassungsliste übereinstimmen |

#### Häufige Konfigurationen

Deaktivieren Sie alle Marktplatz-Ergänzungen:

```json  theme={null}
{
  "strictKnownMarketplaces": []
}
```

Nur bestimmte Marktplätze zulassen:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    }
  ]
}
```

Alle Marktplätze von einem internen Git-Server mit Regex-Musterabgleich auf dem Host zulassen. Dies ist der empfohlene Ansatz für [GitHub Enterprise Server](/de/github-enterprise-server#plugin-marketplaces-on-ghes) oder selbstgehostete GitLab-Instanzen:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

Dateisystem-basierte Marktplätze aus einem bestimmten Verzeichnis mit Regex-Musterabgleich auf dem Pfad zulassen:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "pathPattern",
      "pathPattern": "^/opt/approved/"
    }
  ]
}
```

Verwenden Sie `".*"` als `pathPattern`, um jeden Dateisystempfad zuzulassen und gleichzeitig Netzwerkquellen mit `hostPattern` zu steuern.

<Note>
  `strictKnownMarketplaces` schränkt ein, was Benutzer hinzufügen können, registriert aber nicht selbst Marktplätze. Um zulässige Marktplätze automatisch verfügbar zu machen, ohne dass Benutzer `/plugin marketplace add` ausführen müssen, kombinieren Sie es mit [`extraKnownMarketplaces`](/de/settings#extraknownmarketplaces) in derselben `managed-settings.json`. Siehe [Beide zusammen verwenden](/de/settings#strictknownmarketplaces).
</Note>

#### Wie Einschränkungen funktionieren

Einschränkungen werden früh im Plugin-Installationsprozess validiert, bevor Netzwerkanfragen oder Dateisystemoperationen auftreten. Dies verhindert unbefugte Marktplatz-Zugriffversuche.

Die Zulassungsliste verwendet exakten Abgleich für die meisten Quellentypen. Damit ein Marktplatz zulässig ist, müssen alle angegebenen Felder genau übereinstimmen:

* Für GitHub-Quellen: `repo` ist erforderlich, und `ref` oder `path` müssen auch übereinstimmen, wenn sie in der Zulassungsliste angegeben sind
* Für URL-Quellen: Die vollständige URL muss genau übereinstimmen
* Für `hostPattern`-Quellen: Der Marktplatz-Host wird gegen das Regex-Muster abgeglichen
* Für `pathPattern`-Quellen: Der Dateisystempfad des Marktplatzes wird gegen das Regex-Muster abgeglichen

Da `strictKnownMarketplaces` in [verwalteten Einstellungen](/de/settings#settings-files) festgelegt ist, können einzelne Benutzer und Projektkonfigurationen diese Einschränkungen nicht überschreiben.

Für vollständige Konfigurationsdetails einschließlich aller unterstützten Quellentypen und Vergleich mit `extraKnownMarketplaces` siehe die [strictKnownMarketplaces-Referenz](/de/settings#strictknownmarketplaces).

### Versionsauflösung und Release-Kanäle

Plugin-Versionen bestimmen Cache-Pfade und Update-Erkennung. Sie können die Version im Plugin-Manifest (`plugin.json`) oder im Marktplatz-Eintrag (`marketplace.json`) angeben.

<Warning>
  Vermeiden Sie nach Möglichkeit, die Version an beiden Stellen festzulegen. Das Plugin-Manifest gewinnt immer stillschweigend, was dazu führen kann, dass die Marktplatz-Version ignoriert wird. Legen Sie für Plugins mit relativen Pfaden die Version im Marktplatz-Eintrag fest. Legen Sie für alle anderen Plugin-Quellen die Version im Plugin-Manifest fest.
</Warning>

#### Richten Sie Release-Kanäle ein

Um "stabile" und "neueste" Release-Kanäle für Ihre Plugins zu unterstützen, können Sie zwei Marktplätze einrichten, die auf verschiedene Refs oder SHAs desselben Repos verweisen. Sie können dann die beiden Marktplätze verschiedenen Benutzergruppen über [verwaltete Einstellungen](/de/settings#settings-files) zuweisen.

<Warning>
  Die `plugin.json` des Plugins muss eine andere `version` bei jedem angehefteten Ref oder Commit deklarieren. Wenn zwei Refs oder Commits die gleiche Manifest-Version haben, behandelt Claude Code sie als identisch und überspringt das Update.
</Warning>

##### Beispiel

```json  theme={null}
{
  "name": "stable-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "stable"
      }
    }
  ]
}
```

```json  theme={null}
{
  "name": "latest-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "latest"
      }
    }
  ]
}
```

##### Kanäle Benutzergruppen zuweisen

Weisen Sie jeden Marktplatz der entsprechenden Benutzergruppe über verwaltete Einstellungen zu. Beispielsweise erhält die stabile Gruppe:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "stable-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/stable-tools"
      }
    }
  }
}
```

Die Early-Access-Gruppe erhält stattdessen `latest-tools`:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "latest-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/latest-tools"
      }
    }
  }
}
```

## Validierung und Tests

Testen Sie Ihren Marktplatz vor dem Teilen.

Validieren Sie Ihre Marktplatz-JSON-Syntax:

```bash  theme={null}
claude plugin validate .
```

Oder von innerhalb von Claude Code:

```shell  theme={null}
/plugin validate .
```

Fügen Sie den Marktplatz zum Testen hinzu:

```shell  theme={null}
/plugin marketplace add ./path/to/marketplace
```

Installieren Sie ein Test-Plugin, um zu überprüfen, ob alles funktioniert:

```shell  theme={null}
/plugin install test-plugin@marketplace-name
```

Für vollständige Plugin-Test-Workflows siehe [Testen Sie Ihre Plugins lokal](/de/plugins#test-your-plugins-locally). Für technische Fehlerbehebung siehe [Plugins-Referenz](/de/plugins-reference).

## Fehlerbehebung

### Marktplatz wird nicht geladen

**Symptome**: Kann Marktplatz nicht hinzufügen oder Plugins von ihm nicht sehen

**Lösungen**:

* Überprüfen Sie, dass die Marktplatz-URL erreichbar ist
* Überprüfen Sie, dass `.claude-plugin/marketplace.json` im angegebenen Pfad vorhanden ist
* Stellen Sie sicher, dass die JSON-Syntax gültig ist und das Frontmatter wohlgeformt ist, indem Sie `claude plugin validate` oder `/plugin validate` verwenden
* Bestätigen Sie für private Repositories, dass Sie Zugriffsberechtigung haben

### Marktplatz-Validierungsfehler

Führen Sie `claude plugin validate .` oder `/plugin validate .` aus Ihrem Marktplatz-Verzeichnis aus, um auf Probleme zu überprüfen. Der Validator überprüft `plugin.json`, Skill/Agent/Befehl-Frontmatter und `hooks/hooks.json` auf Syntax- und Schema-Fehler. Häufige Fehler:

| Fehler                                            | Ursache                                                   | Lösung                                                                                                           |
| :------------------------------------------------ | :-------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- |
| `File not found: .claude-plugin/marketplace.json` | Fehlendes Manifest                                        | Erstellen Sie `.claude-plugin/marketplace.json` mit erforderlichen Feldern                                       |
| `Invalid JSON syntax: Unexpected token...`        | JSON-Syntaxfehler in marketplace.json                     | Überprüfen Sie auf fehlende Kommas, zusätzliche Kommas oder nicht zitierte Strings                               |
| `Duplicate plugin name "x" found in marketplace`  | Zwei Plugins teilen denselben Namen                       | Geben Sie jedem Plugin einen eindeutigen `name`-Wert                                                             |
| `plugins[0].source: Path contains ".."`           | Quellpfad enthält `..`                                    | Verwenden Sie Pfade relativ zum Marktplatz-Root ohne `..`. Siehe [Relative Pfade](#relative-paths)               |
| `YAML frontmatter failed to parse: ...`           | Ungültiges YAML in einer Skill-, Agent- oder Befehlsdatei | Beheben Sie die YAML-Syntax im Frontmatter-Block. Zur Laufzeit wird diese Datei ohne Metadaten geladen.          |
| `Invalid JSON syntax: ...` (hooks.json)           | Malformed `hooks/hooks.json`                              | Beheben Sie die JSON-Syntax. Eine malformed `hooks/hooks.json` verhindert, dass das gesamte Plugin geladen wird. |

**Warnungen** (nicht blockierend):

* `Marketplace has no plugins defined`: Fügen Sie mindestens ein Plugin zum `plugins`-Array hinzu
* `No marketplace description provided`: Fügen Sie `metadata.description` hinzu, um Benutzern zu helfen, Ihren Marktplatz zu verstehen
* `Plugin name "x" is not kebab-case`: Der Plugin-Name enthält Großbuchstaben, Leerzeichen oder Sonderzeichen. Benennen Sie in Kleinbuchstaben, Ziffern und Bindestriche um (z. B. `my-plugin`). Claude Code akzeptiert andere Formen, aber die Claude.ai-Marktplatz-Synchronisierung lehnt sie ab.

### Plugin-Installationsfehler

**Symptome**: Marktplatz wird angezeigt, aber Plugin-Installation schlägt fehl

**Lösungen**:

* Überprüfen Sie, dass Plugin-Quell-URLs erreichbar sind
* Überprüfen Sie, dass Plugin-Verzeichnisse erforderliche Dateien enthalten
* Überprüfen Sie für GitHub-Quellen, dass Repositories öffentlich sind oder Sie Zugriff haben
* Testen Sie Plugin-Quellen manuell durch Klonen/Herunterladen

### Authentifizierung für private Repositories schlägt fehl

**Symptome**: Authentifizierungsfehler beim Installieren von Plugins aus privaten Repositories

**Lösungen**:

Für manuelle Installation und Updates:

* Überprüfen Sie, dass Sie bei Ihrem Git-Anbieter authentifiziert sind (führen Sie z. B. `gh auth status` für GitHub aus)
* Überprüfen Sie, dass Ihr Credential-Helper korrekt konfiguriert ist: `git config --global credential.helper`
* Versuchen Sie, das Repository manuell zu klonen, um zu überprüfen, dass Ihre Anmeldedaten funktionieren

Für Hintergrund-Auto-Updates:

* Legen Sie das entsprechende Token in Ihrer Umgebung fest: `echo $GITHUB_TOKEN`
* Überprüfen Sie, dass das Token die erforderlichen Berechtigungen hat (Lesezugriff auf das Repository)
* Überprüfen Sie für GitHub, dass das Token den `repo`-Scope für private Repositories hat
* Überprüfen Sie für GitLab, dass das Token mindestens den `read_repository`-Scope hat
* Überprüfen Sie, dass das Token nicht abgelaufen ist

### Marktplatz-Updates schlagen in Offline-Umgebungen fehl

**Symptome**: Marktplatz `git pull` schlägt fehl und Claude Code löscht den vorhandenen Cache, wodurch Plugins nicht mehr verfügbar werden.

**Ursache**: Standardmäßig entfernt Claude Code den veralteten Klon und versucht erneut zu klonen, wenn ein `git pull` fehlschlägt. In Offline- oder Airgapped-Umgebungen schlägt das erneute Klonen auf die gleiche Weise fehl, wodurch das Marktplatz-Verzeichnis leer bleibt.

**Lösung**: Legen Sie `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1` fest, um den vorhandenen Cache beizubehalten, wenn der Pull fehlschlägt, anstatt ihn zu löschen:

```bash  theme={null}
export CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1
```

Mit dieser Variable gesetzt behält Claude Code den veralteten Marktplatz-Klon bei `git pull`-Fehler bei und verwendet weiterhin den letzten bekannten guten Status. Verwenden Sie für vollständig Offline-Bereitstellungen, bei denen das Repository nie erreichbar sein wird, stattdessen [`CLAUDE_CODE_PLUGIN_SEED_DIR`](#pre-populate-plugins-for-containers), um das Plugins-Verzeichnis zur Build-Zeit vorab auszufüllen.

### Git-Operationen zeitüberschreitung

**Symptome**: Plugin-Installation oder Marktplatz-Updates schlagen mit einem Timeout-Fehler fehl, wie "Git clone timed out after 120s" oder "Git pull timed out after 120s".

**Ursache**: Claude Code verwendet ein 120-Sekunden-Timeout für alle Git-Operationen, einschließlich Klonen von Plugin-Repositories und Abrufen von Marktplatz-Updates. Große Repositories oder langsame Netzwerkverbindungen können dieses Limit überschreiten.

**Lösung**: Erhöhen Sie das Timeout mit der Umgebungsvariable `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`. Der Wert ist in Millisekunden:

```bash  theme={null}
export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000  # 5 Minuten
```

### Plugins mit relativen Pfaden schlagen in URL-basierten Marktplätzen fehl

**Symptome**: Einen Marktplatz über URL hinzugefügt (z. B. `https://example.com/marketplace.json`), aber Plugins mit relativen Pfadquellen wie `"./plugins/my-plugin"` schlagen mit "path not found"-Fehlern fehl.

**Ursache**: URL-basierte Marktplätze laden nur die `marketplace.json`-Datei selbst herunter. Sie laden keine Plugin-Dateien vom Server herunter. Relative Pfade im Marktplatz-Eintrag verweisen auf Dateien auf dem Remote-Server, die nicht heruntergeladen wurden.

**Lösungen**:

* **Verwenden Sie externe Quellen**: Ändern Sie Plugin-Einträge, um stattdessen GitHub-, npm- oder Git-URL-Quellen zu verwenden:
  ```json  theme={null}
  { "name": "my-plugin", "source": { "source": "github", "repo": "owner/repo" } }
  ```
* **Verwenden Sie einen Git-basierten Marktplatz**: Hosten Sie Ihren Marktplatz in einem Git-Repository und fügen Sie ihn mit der Git-URL hinzu. Git-basierte Marktplätze klonen das gesamte Repository, wodurch relative Pfade funktionieren.

### Dateien nicht gefunden nach Installation

**Symptome**: Plugin wird installiert, aber Verweise auf Dateien schlagen fehl, besonders Dateien außerhalb des Plugin-Verzeichnisses

**Ursache**: Plugins werden in ein Cache-Verzeichnis kopiert, anstatt an Ort und Stelle verwendet zu werden. Pfade, die auf Dateien außerhalb des Plugin-Verzeichnisses verweisen (wie `../shared-utils`), funktionieren nicht, da diese Dateien nicht kopiert werden.

**Lösungen**: Siehe [Plugin-Caching und Dateiauflösung](/de/plugins-reference#plugin-caching-and-file-resolution) für Workarounds, einschließlich Symlinks und Verzeichnisumstrukturierung.

Für zusätzliche Debugging-Tools und häufige Probleme siehe [Debugging- und Entwicklungstools](/de/plugins-reference#debugging-and-development-tools).

## Siehe auch

* [Entdecken und Installieren vorgefertigter Plugins](/de/discover-plugins) - Installieren von Plugins aus vorhandenen Marktplätzen
* [Plugins](/de/plugins) - Erstellen Ihrer eigenen Plugins
* [Plugins-Referenz](/de/plugins-reference) - Vollständige technische Spezifikationen und Schemas
* [Plugin-Einstellungen](/de/settings#plugin-settings) - Plugin-Konfigurationsoptionen
* [strictKnownMarketplaces-Referenz](/de/settings#strictknownmarketplaces) - Verwaltete Marktplatz-Einschränkungen
