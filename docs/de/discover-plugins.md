> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Entdecken und installieren Sie vorgefertigte Plugins über Marktplätze

> Finden und installieren Sie Plugins aus Marktplätzen, um Claude Code mit neuen Befehlen, Agenten und Funktionen zu erweitern.

Plugins erweitern Claude Code mit skills, agents, hooks und MCP servers. Plugin-Marktplätze sind Kataloge, die Ihnen helfen, diese Erweiterungen zu entdecken und zu installieren, ohne sie selbst zu erstellen.

Möchten Sie Ihren eigenen Marktplatz erstellen und verteilen? Siehe [Erstellen und verteilen Sie einen Plugin-Marktplatz](/de/plugin-marketplaces).

## Wie Marktplätze funktionieren

Ein Marktplatz ist ein Katalog von Plugins, die jemand anderes erstellt und geteilt hat. Die Verwendung eines Marktplatzes ist ein zweistufiger Prozess:

<Steps>
  <Step title="Fügen Sie den Marktplatz hinzu">
    Dies registriert den Katalog bei Claude Code, damit Sie durchsuchen können, was verfügbar ist. Es werden noch keine Plugins installiert.
  </Step>

  <Step title="Installieren Sie einzelne Plugins">
    Durchsuchen Sie den Katalog und installieren Sie die Plugins, die Sie möchten.
  </Step>
</Steps>

Stellen Sie sich das vor wie das Hinzufügen eines App-Stores: Das Hinzufügen des Stores gibt Ihnen Zugriff zum Durchsuchen seiner Sammlung, aber Sie wählen immer noch aus, welche Apps Sie einzeln herunterladen möchten.

## Offizieller Anthropic-Marktplatz

Der offizielle Anthropic-Marktplatz (`claude-plugins-official`) ist automatisch verfügbar, wenn Sie Claude Code starten. Führen Sie `/plugin` aus und gehen Sie zur Registerkarte **Discover**, um zu sehen, was verfügbar ist.

So installieren Sie ein Plugin aus dem offiziellen Marktplatz:

```shell  theme={null}
/plugin install plugin-name@claude-plugins-official
```

<Note>
  Der offizielle Marktplatz wird von Anthropic gepflegt. Um ein Plugin beim offiziellen Marktplatz einzureichen, verwenden Sie eines der In-App-Einreichungsformulare:

  * **Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
  * **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

  Um Plugins unabhängig zu verteilen, [erstellen Sie Ihren eigenen Marktplatz](/de/plugin-marketplaces) und teilen Sie ihn mit Benutzern.
</Note>

Der offizielle Marktplatz umfasst mehrere Plugin-Kategorien:

### Code-Intelligenz

Code-Intelligenz-Plugins aktivieren das integrierte LSP-Tool von Claude Code und geben Claude die Möglichkeit, zu Definitionen zu springen, Referenzen zu finden und Typfehler unmittelbar nach Änderungen zu sehen. Diese Plugins konfigurieren [Language Server Protocol](https://microsoft.github.io/language-server-protocol/)-Verbindungen, die gleiche Technologie, die die Code-Intelligenz von VS Code antreibt.

Diese Plugins erfordern, dass die Language-Server-Binärdatei auf Ihrem System installiert ist. Wenn Sie bereits einen Language Server installiert haben, kann Claude Sie möglicherweise auffordern, das entsprechende Plugin zu installieren, wenn Sie ein Projekt öffnen.

| Sprache    | Plugin              | Erforderliche Binärdatei     |
| :--------- | :------------------ | :--------------------------- |
| C/C++      | `clangd-lsp`        | `clangd`                     |
| C#         | `csharp-lsp`        | `csharp-ls`                  |
| Go         | `gopls-lsp`         | `gopls`                      |
| Java       | `jdtls-lsp`         | `jdtls`                      |
| Kotlin     | `kotlin-lsp`        | `kotlin-language-server`     |
| Lua        | `lua-lsp`           | `lua-language-server`        |
| PHP        | `php-lsp`           | `intelephense`               |
| Python     | `pyright-lsp`       | `pyright-langserver`         |
| Rust       | `rust-analyzer-lsp` | `rust-analyzer`              |
| Swift      | `swift-lsp`         | `sourcekit-lsp`              |
| TypeScript | `typescript-lsp`    | `typescript-language-server` |

Sie können auch [Ihr eigenes LSP-Plugin erstellen](/de/plugins-reference#lsp-servers) für andere Sprachen.

<Note>
  Wenn Sie nach der Installation eines Plugins `Executable not found in $PATH` in der Registerkarte `/plugin` Errors sehen, installieren Sie die erforderliche Binärdatei aus der obigen Tabelle.
</Note>

#### Was Claude von Code-Intelligenz-Plugins gewinnt

Sobald ein Code-Intelligenz-Plugin installiert ist und seine Language-Server-Binärdatei verfügbar ist, gewinnt Claude zwei Funktionen:

* **Automatische Diagnose**: Nach jeder Dateiänderung, die Claude vornimmt, analysiert der Language Server die Änderungen und meldet Fehler und Warnungen automatisch zurück. Claude sieht Typfehler, fehlende Importe und Syntaxprobleme, ohne einen Compiler oder Linter ausführen zu müssen. Wenn Claude einen Fehler einführt, bemerkt es das Problem und behebt es in derselben Runde. Dies erfordert keine Konfiguration über die Installation des Plugins hinaus. Sie können Diagnosen inline anzeigen, indem Sie **Strg+O** drücken, wenn der Indikator „Diagnosen gefunden" angezeigt wird.
* **Code-Navigation**: Claude kann den Language Server verwenden, um zu Definitionen zu springen, Referenzen zu finden, Typinformationen beim Hover zu erhalten, Symbole aufzulisten, Implementierungen zu finden und Call-Hierarchien zu verfolgen. Diese Operationen geben Claude eine präzisere Navigation als grep-basierte Suche, obwohl die Verfügbarkeit je nach Sprache und Umgebung variieren kann.

Wenn Sie auf Probleme stoßen, siehe [Code-Intelligenz-Fehlerbehebung](#code-intelligence-issues).

### Externe Integrationen

Diese Plugins bündeln vorkonfigurierte [MCP servers](/de/mcp), damit Sie Claude mit externen Diensten verbinden können, ohne manuelle Einrichtung:

* **Quellcodeverwaltung**: `github`, `gitlab`
* **Projektmanagement**: `atlassian` (Jira/Confluence), `asana`, `linear`, `notion`
* **Design**: `figma`
* **Infrastruktur**: `vercel`, `firebase`, `supabase`
* **Kommunikation**: `slack`
* **Überwachung**: `sentry`

### Entwicklungs-Workflows

Plugins, die Befehle und Agenten für häufige Entwicklungsaufgaben hinzufügen:

* **commit-commands**: Git-Commit-Workflows einschließlich Commit, Push und PR-Erstellung
* **pr-review-toolkit**: Spezialisierte Agenten für die Überprüfung von Pull Requests
* **agent-sdk-dev**: Tools zum Erstellen mit dem Claude Agent SDK
* **plugin-dev**: Toolkit zum Erstellen Ihrer eigenen Plugins

### Ausgabestile

Passen Sie an, wie Claude antwortet:

* **explanatory-output-style**: Pädagogische Einblicke in Implementierungsentscheidungen
* **learning-output-style**: Interaktiver Lernmodus zum Aufbau von Fähigkeiten

## Probieren Sie es aus: Fügen Sie den Demo-Marktplatz hinzu

Anthropic verwaltet auch einen [Demo-Plugins-Marktplatz](https://github.com/anthropics/claude-code/tree/main/plugins) (`claude-code-plugins`) mit Beispiel-Plugins, die zeigen, was mit dem Plugin-System möglich ist. Im Gegensatz zum offiziellen Marktplatz müssen Sie diesen manuell hinzufügen.

<Steps>
  <Step title="Fügen Sie den Marktplatz hinzu">
    Führen Sie in Claude Code den Befehl `plugin marketplace add` für den Marktplatz `anthropics/claude-code` aus:

    ```shell  theme={null}
    /plugin marketplace add anthropics/claude-code
    ```

    Dies lädt den Marktplatz-Katalog herunter und macht seine Plugins für Sie verfügbar.
  </Step>

  <Step title="Durchsuchen Sie verfügbare Plugins">
    Führen Sie `/plugin` aus, um den Plugin-Manager zu öffnen. Dies öffnet eine Schnittstelle mit Registerkarten mit vier Registerkarten, die Sie mit **Tab** durchlaufen können (oder **Shift+Tab**, um rückwärts zu gehen):

    * **Discover**: Durchsuchen Sie verfügbare Plugins aus allen Ihren Marktplätzen
    * **Installed**: Zeigen Sie Ihre installierten Plugins an und verwalten Sie sie
    * **Marketplaces**: Fügen Sie Marktplätze hinzu, entfernen Sie sie oder aktualisieren Sie sie
    * **Errors**: Zeigen Sie alle Plugin-Ladefehler an

    Gehen Sie zur Registerkarte **Discover**, um Plugins aus dem Marktplatz zu sehen, den Sie gerade hinzugefügt haben.
  </Step>

  <Step title="Installieren Sie ein Plugin">
    Wählen Sie ein Plugin aus, um seine Details anzuzeigen, und wählen Sie dann einen Installationsbereich:

    * **User scope**: Installieren Sie für sich selbst in allen Projekten
    * **Project scope**: Installieren Sie für alle Mitarbeiter in diesem Repository
    * **Local scope**: Installieren Sie für sich selbst nur in diesem Repository

    Wählen Sie beispielsweise **commit-commands** (ein Plugin, das Git-Workflow-Befehle hinzufügt) und installieren Sie es in Ihrem Benutzerbereich.

    Sie können auch direkt über die Befehlszeile installieren:

    ```shell  theme={null}
    /plugin install commit-commands@anthropics-claude-code
    ```

    Siehe [Konfigurationsbereiche](/de/settings#configuration-scopes), um mehr über Bereiche zu erfahren.
  </Step>

  <Step title="Verwenden Sie Ihr neues Plugin">
    Nach der Installation sind die Befehle des Plugins sofort verfügbar. Plugin-Befehle werden nach dem Plugin-Namen benannt, daher bietet **commit-commands** Befehle wie `/commit-commands:commit`.

    Probieren Sie es aus, indem Sie eine Änderung an einer Datei vornehmen und ausführen:

    ```shell  theme={null}
    /commit-commands:commit
    ```

    Dies stellt Ihre Änderungen bereit, generiert eine Commit-Nachricht und erstellt den Commit.

    Jedes Plugin funktioniert anders. Überprüfen Sie die Beschreibung des Plugins in der Registerkarte **Discover** oder auf seiner Homepage, um zu erfahren, welche Befehle und Funktionen es bietet.
  </Step>
</Steps>

Der Rest dieses Leitfadens behandelt alle Möglichkeiten, wie Sie Marktplätze hinzufügen, Plugins installieren und Ihre Konfiguration verwalten können.

## Marktplätze hinzufügen

Verwenden Sie den Befehl `/plugin marketplace add`, um Marktplätze aus verschiedenen Quellen hinzuzufügen.

<Tip>
  **Verknüpfungen**: Sie können `/plugin market` anstelle von `/plugin marketplace` verwenden und `rm` anstelle von `remove`.
</Tip>

* **GitHub-Repositories**: Format `owner/repo` (z. B. `anthropics/claude-code`)
* **Git-URLs**: Beliebige Git-Repository-URL (GitLab, Bitbucket, selbstgehostet)
* **Lokale Pfade**: Verzeichnisse oder direkte Pfade zu `marketplace.json`-Dateien
* **Remote-URLs**: Direkte URLs zu gehosteten `marketplace.json`-Dateien

### Hinzufügen von GitHub

Fügen Sie ein GitHub-Repository hinzu, das eine `.claude-plugin/marketplace.json`-Datei enthält, indem Sie das Format `owner/repo` verwenden – wobei `owner` der GitHub-Benutzername oder die Organisation und `repo` der Repository-Name ist.

Beispielsweise bezieht sich `anthropics/claude-code` auf das Repository `claude-code`, das sich im Besitz von `anthropics` befindet:

```shell  theme={null}
/plugin marketplace add anthropics/claude-code
```

### Hinzufügen von anderen Git-Hosts

Fügen Sie ein beliebiges Git-Repository hinzu, indem Sie die vollständige URL angeben. Dies funktioniert mit jedem Git-Host, einschließlich GitLab, Bitbucket und selbstgehosteten Servern:

Mit HTTPS:

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

Mit SSH:

```shell  theme={null}
/plugin marketplace add git@gitlab.com:company/plugins.git
```

Um einen bestimmten Branch oder Tag hinzuzufügen, hängen Sie `#` gefolgt von der Referenz an:

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

### Hinzufügen von lokalen Pfaden

Fügen Sie ein lokales Verzeichnis hinzu, das eine `.claude-plugin/marketplace.json`-Datei enthält:

```shell  theme={null}
/plugin marketplace add ./my-marketplace
```

Sie können auch einen direkten Pfad zu einer `marketplace.json`-Datei hinzufügen:

```shell  theme={null}
/plugin marketplace add ./path/to/marketplace.json
```

### Hinzufügen von Remote-URLs

Fügen Sie eine Remote-`marketplace.json`-Datei über URL hinzu:

```shell  theme={null}
/plugin marketplace add https://example.com/marketplace.json
```

<Note>
  URL-basierte Marktplätze haben einige Einschränkungen im Vergleich zu Git-basierten Marktplätzen. Wenn beim Installieren von Plugins Fehler „Pfad nicht gefunden" auftreten, siehe [Fehlerbehebung](/de/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces).
</Note>

## Installieren Sie Plugins

Nachdem Sie Marktplätze hinzugefügt haben, können Sie Plugins direkt installieren (wird standardmäßig im Benutzerbereich installiert):

```shell  theme={null}
/plugin install plugin-name@marketplace-name
```

Um einen anderen [Installationsbereich](/de/settings#configuration-scopes) zu wählen, verwenden Sie die interaktive Benutzeroberfläche: Führen Sie `/plugin` aus, gehen Sie zur Registerkarte **Discover**, und drücken Sie **Enter** auf einem Plugin. Sie sehen Optionen für:

* **User scope** (Standard): Installieren Sie für sich selbst in allen Projekten
* **Project scope**: Installieren Sie für alle Mitarbeiter in diesem Repository (fügt zu `.claude/settings.json` hinzu)
* **Local scope**: Installieren Sie für sich selbst nur in diesem Repository (nicht mit Mitarbeitern geteilt)

Sie können auch Plugins mit **managed**-Bereich sehen – diese werden von Administratoren über [verwaltete Einstellungen](/de/settings#settings-files) installiert und können nicht geändert werden.

Führen Sie `/plugin` aus und gehen Sie zur Registerkarte **Installed**, um Ihre Plugins nach Bereich gruppiert zu sehen.

<Warning>
  Stellen Sie sicher, dass Sie einem Plugin vertrauen, bevor Sie es installieren. Anthropic kontrolliert nicht, welche MCP servers, Dateien oder andere Software in Plugins enthalten sind, und kann nicht überprüfen, dass sie wie beabsichtigt funktionieren. Überprüfen Sie die Homepage jedes Plugins für weitere Informationen.
</Warning>

## Verwalten Sie installierte Plugins

Führen Sie `/plugin` aus und gehen Sie zur Registerkarte **Installed**, um Ihre Plugins anzuzeigen, zu aktivieren, zu deaktivieren oder zu deinstallieren. Geben Sie ein, um die Liste nach Plugin-Name oder Beschreibung zu filtern.

Sie können Plugins auch mit direkten Befehlen verwalten.

Deaktivieren Sie ein Plugin, ohne es zu deinstallieren:

```shell  theme={null}
/plugin disable plugin-name@marketplace-name
```

Aktivieren Sie ein deaktiviertes Plugin erneut:

```shell  theme={null}
/plugin enable plugin-name@marketplace-name
```

Entfernen Sie ein Plugin vollständig:

```shell  theme={null}
/plugin uninstall plugin-name@marketplace-name
```

Die Option `--scope` ermöglicht es Ihnen, einen bestimmten Bereich mit CLI-Befehlen anzusteuern:

```shell  theme={null}
claude plugin install formatter@your-org --scope project
claude plugin uninstall formatter@your-org --scope project
```

### Wenden Sie Plugin-Änderungen an, ohne neu zu starten

Wenn Sie während einer Sitzung Plugins installieren, aktivieren oder deaktivieren, werden einige Änderungen (wie neue Befehle und hooks) sofort wirksam. Andere, einschließlich LSP-Server-Updates, erfordern einen Neustart.

Um alle ausstehenden Plugin-Änderungen ohne Neustart zu aktivieren, führen Sie aus:

```shell  theme={null}
/reload-plugins
```

Claude Code lädt alle aktiven Plugins neu und meldet, was geladen wurde. Wenn LSP-Server hinzugefügt oder aktualisiert wurden, wird Ihnen mitgeteilt, dass diese einen Neustart erfordern, um wirksam zu werden.

## Verwalten Sie Marktplätze

Sie können Marktplätze über die interaktive `/plugin`-Schnittstelle oder mit CLI-Befehlen verwalten.

### Verwenden Sie die interaktive Schnittstelle

Führen Sie `/plugin` aus und gehen Sie zur Registerkarte **Marketplaces**, um:

* Alle Ihre hinzugefügten Marktplätze mit ihren Quellen und Status anzuzeigen
* Neue Marktplätze hinzuzufügen
* Marktplatz-Auflistungen aktualisieren, um die neuesten Plugins abzurufen
* Marktplätze zu entfernen, die Sie nicht mehr benötigen

### Verwenden Sie CLI-Befehle

Sie können Marktplätze auch mit direkten Befehlen verwalten.

Listet alle konfigurierten Marktplätze auf:

```shell  theme={null}
/plugin marketplace list
```

Aktualisieren Sie Plugin-Auflistungen von einem Marktplatz:

```shell  theme={null}
/plugin marketplace update marketplace-name
```

Entfernen Sie einen Marktplatz:

```shell  theme={null}
/plugin marketplace remove marketplace-name
```

<Warning>
  Das Entfernen eines Marktplatzes deinstalliert alle Plugins, die Sie von ihm installiert haben.
</Warning>

### Konfigurieren Sie automatische Updates

Claude Code kann Marktplätze und ihre installierten Plugins beim Start automatisch aktualisieren. Wenn die automatische Aktualisierung für einen Marktplatz aktiviert ist, aktualisiert Claude Code die Marktplatzdaten und aktualisiert installierte Plugins auf ihre neuesten Versionen. Wenn Plugins aktualisiert wurden, sehen Sie eine Benachrichtigung, die Sie auffordert, `/reload-plugins` auszuführen.

Schalten Sie die automatische Aktualisierung für einzelne Marktplätze über die Benutzeroberfläche um:

1. Führen Sie `/plugin` aus, um den Plugin-Manager zu öffnen
2. Wählen Sie **Marketplaces**
3. Wählen Sie einen Marktplatz aus der Liste
4. Wählen Sie **Enable auto-update** oder **Disable auto-update**

Offizielle Anthropic-Marktplätze haben die automatische Aktualisierung standardmäßig aktiviert. Marktplätze von Drittanbietern und lokale Entwicklungsmarktplätze haben die automatische Aktualisierung standardmäßig deaktiviert.

Um alle automatischen Updates vollständig für Claude Code und alle Plugins zu deaktivieren, setzen Sie die Umgebungsvariable `DISABLE_AUTOUPDATER`. Siehe [Automatische Updates](/de/setup#auto-updates) für Details.

Um Plugin-Auto-Updates aktiviert zu halten und gleichzeitig Claude Code-Auto-Updates zu deaktivieren, setzen Sie `FORCE_AUTOUPDATE_PLUGINS=true` zusammen mit `DISABLE_AUTOUPDATER`:

```shell  theme={null}
export DISABLE_AUTOUPDATER=true
export FORCE_AUTOUPDATE_PLUGINS=true
```

Dies ist nützlich, wenn Sie Claude Code-Updates manuell verwalten möchten, aber immer noch automatische Plugin-Updates erhalten möchten.

## Konfigurieren Sie Team-Marktplätze

Team-Administratoren können die automatische Marktplatz-Installation für Projekte einrichten, indem sie Marktplatz-Konfiguration zu `.claude/settings.json` hinzufügen. Wenn Team-Mitglieder dem Repository-Ordner vertrauen, fordert Claude Code sie auf, diese Marktplätze und Plugins zu installieren.

Fügen Sie `extraKnownMarketplaces` zu Ihrer Projekt-`.claude/settings.json` hinzu:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "my-team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

Für vollständige Konfigurationsoptionen einschließlich `extraKnownMarketplaces` und `enabledPlugins` siehe [Plugin-Einstellungen](/de/settings#plugin-settings).

## Sicherheit

Plugins und Marktplätze sind hochgradig vertrauenswürdige Komponenten, die beliebigen Code auf Ihrem Computer mit Ihren Benutzerrechten ausführen können. Installieren Sie nur Plugins und fügen Sie Marktplätze aus Quellen hinzu, denen Sie vertrauen. Organisationen können einschränken, welche Marktplätze Benutzer hinzufügen dürfen, indem sie [verwaltete Marktplatz-Einschränkungen](/de/plugin-marketplaces#managed-marketplace-restrictions) verwenden.

## Fehlerbehebung

### /plugin-Befehl nicht erkannt

Wenn Sie „unknown command" sehen oder der `/plugin`-Befehl nicht angezeigt wird:

1. **Überprüfen Sie Ihre Version**: Führen Sie `claude --version` aus. Plugins erfordern Version 1.0.33 oder später.
2. **Aktualisieren Sie Claude Code**:
   * **Homebrew**: `brew upgrade claude-code`
   * **npm**: `npm update -g @anthropic-ai/claude-code`
   * **Native Installer**: Führen Sie den Installationsbefehl von [Setup](/de/setup) erneut aus
3. **Starten Sie Claude Code neu**: Starten Sie nach dem Update Ihr Terminal neu und führen Sie `claude` erneut aus.

### Häufige Probleme

* **Marktplatz wird nicht geladen**: Überprüfen Sie, dass die URL zugänglich ist und dass `.claude-plugin/marketplace.json` unter dem Pfad vorhanden ist
* **Plugin-Installationsfehler**: Überprüfen Sie, dass Plugin-Quell-URLs zugänglich sind und Repositories öffentlich sind (oder Sie haben Zugriff)
* **Dateien nach der Installation nicht gefunden**: Plugins werden in einen Cache kopiert, daher funktionieren Pfade, die auf Dateien außerhalb des Plugin-Verzeichnisses verweisen, nicht
* **Plugin-Skills werden nicht angezeigt**: Löschen Sie den Cache mit `rm -rf ~/.claude/plugins/cache`, starten Sie Claude Code neu und installieren Sie das Plugin erneut.

Für detaillierte Fehlerbehebung mit Lösungen siehe [Fehlerbehebung](/de/plugin-marketplaces#troubleshooting) im Marktplatz-Leitfaden. Für Debugging-Tools siehe [Debugging- und Entwicklungstools](/de/plugins-reference#debugging-and-development-tools).

### Code-Intelligenz-Probleme

* **Language Server startet nicht**: Überprüfen Sie, dass die Binärdatei installiert ist und in Ihrem `$PATH` verfügbar ist. Überprüfen Sie die Registerkarte `/plugin` Errors für Details.
* **Hohe Speichernutzung**: Language Server wie `rust-analyzer` und `pyright` können bei großen Projekten erhebliche Speichermengen verbrauchen. Wenn Sie Speicherprobleme haben, deaktivieren Sie das Plugin mit `/plugin disable <plugin-name>` und verlassen Sie sich stattdessen auf Claudes integrierte Suchtools.
* **Falsch positive Diagnosen in Monorepos**: Language Server können ungelöste Importfehler für interne Pakete melden, wenn der Arbeitsbereich nicht richtig konfiguriert ist. Diese beeinflussen nicht Claudes Fähigkeit, Code zu bearbeiten.

## Nächste Schritte

* **Erstellen Sie Ihre eigenen Plugins**: Siehe [Plugins](/de/plugins), um skills, agents und hooks zu erstellen
* **Erstellen Sie einen Marktplatz**: Siehe [Erstellen Sie einen Plugin-Marktplatz](/de/plugin-marketplaces), um Plugins an Ihr Team oder Ihre Community zu verteilen
* **Technische Referenz**: Siehe [Plugins-Referenz](/de/plugins-reference) für vollständige Spezifikationen
