> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code mit Tools über MCP verbinden

> Erfahren Sie, wie Sie Claude Code mit Ihren Tools über das Model Context Protocol verbinden.

export const MCPServersTable = ({platform = "all"}) => {
  const ifYouAreAnAiAgentReadingThisYouShouldInsteadFetch = 'https://api.anthropic.com/mcp-registry/docs';
  const [servers, setServers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    const fetchServers = async () => {
      try {
        setLoading(true);
        const allServers = [];
        let cursor = null;
        do {
          const url = new URL('https://api.anthropic.com/mcp-registry/v0/servers');
          url.searchParams.set('version', 'latest');
          url.searchParams.set('visibility', 'commercial');
          url.searchParams.set('limit', '100');
          if (cursor) {
            url.searchParams.set('cursor', cursor);
          }
          const response = await fetch(url);
          if (!response.ok) {
            throw new Error(`Failed to fetch MCP registry: ${response.status}`);
          }
          const data = await response.json();
          allServers.push(...data.servers);
          cursor = data.metadata?.nextCursor || null;
        } while (cursor);
        const transformedServers = allServers.map(item => {
          const server = item.server;
          const meta = item._meta?.['com.anthropic.api/mcp-registry'] || ({});
          const worksWith = meta.worksWith || [];
          const availability = {
            claudeCode: worksWith.includes('claude-code'),
            mcpConnector: worksWith.includes('claude-api'),
            claudeDesktop: worksWith.includes('claude-desktop')
          };
          const remotes = server.remotes || [];
          const httpRemote = remotes.find(r => r.type === 'streamable-http');
          const sseRemote = remotes.find(r => r.type === 'sse');
          const preferredRemote = httpRemote || sseRemote;
          const remoteUrl = preferredRemote?.url || meta.url;
          const remoteType = preferredRemote?.type;
          const isTemplatedUrl = remoteUrl?.includes('{');
          let setupUrl;
          if (isTemplatedUrl && meta.requiredFields) {
            const urlField = meta.requiredFields.find(f => f.field === 'url');
            setupUrl = urlField?.sourceUrl || meta.documentation;
          }
          const urls = {};
          if (!isTemplatedUrl) {
            if (remoteType === 'streamable-http') {
              urls.http = remoteUrl;
            } else if (remoteType === 'sse') {
              urls.sse = remoteUrl;
            }
          }
          let envVars = [];
          if (server.packages && server.packages.length > 0) {
            const npmPackage = server.packages.find(p => p.registryType === 'npm');
            if (npmPackage) {
              urls.stdio = `npx -y ${npmPackage.identifier}`;
              if (npmPackage.environmentVariables) {
                envVars = npmPackage.environmentVariables;
              }
            }
          }
          return {
            name: meta.displayName || server.title || server.name,
            description: meta.oneLiner || server.description,
            documentation: meta.documentation,
            urls: urls,
            envVars: envVars,
            availability: availability,
            customCommands: meta.claudeCodeCopyText ? {
              claudeCode: meta.claudeCodeCopyText
            } : undefined,
            setupUrl: setupUrl
          };
        });
        setServers(transformedServers);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching MCP registry:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchServers();
  }, []);
  const generateClaudeCodeCommand = server => {
    if (server.customCommands && server.customCommands.claudeCode) {
      return server.customCommands.claudeCode.replace('--transport streamable-http', '--transport http');
    }
    const serverSlug = server.name.toLowerCase().replace(/[^a-z0-9]/g, '-');
    if (server.urls.http) {
      return `claude mcp add ${serverSlug} --transport http ${server.urls.http}`;
    }
    if (server.urls.sse) {
      return `claude mcp add ${serverSlug} --transport sse ${server.urls.sse}`;
    }
    if (server.urls.stdio) {
      const envFlags = server.envVars && server.envVars.length > 0 ? server.envVars.map(v => `--env ${v.name}=YOUR_${v.name}`).join(' ') : '';
      const baseCommand = `claude mcp add ${serverSlug} --transport stdio`;
      return envFlags ? `${baseCommand} ${envFlags} -- ${server.urls.stdio}` : `${baseCommand} -- ${server.urls.stdio}`;
    }
    return null;
  };
  if (loading) {
    return <div>Loading MCP servers...</div>;
  }
  if (error) {
    return <div>Error loading MCP servers: {error}</div>;
  }
  const filteredServers = servers.filter(server => {
    if (platform === "claudeCode") {
      return server.availability.claudeCode;
    } else if (platform === "mcpConnector") {
      return server.availability.mcpConnector;
    } else if (platform === "claudeDesktop") {
      return server.availability.claudeDesktop;
    } else if (platform === "all") {
      return true;
    } else {
      throw new Error(`Unknown platform: ${platform}`);
    }
  });
  return <>
      <style jsx>{`
        .cards-container {
          display: grid;
          gap: 1rem;
          margin-bottom: 2rem;
        }
        .server-card {
          border: 1px solid var(--border-color, #e5e7eb);
          border-radius: 6px;
          padding: 1rem;
        }
        .command-row {
          display: flex;
          align-items: center;
          gap: 0.25rem;
        }
        .command-row code {
          font-size: 0.75rem;
          overflow-x: auto;
        }
      `}</style>

      <div className="cards-container">
        {filteredServers.map(server => {
    const claudeCodeCommand = generateClaudeCodeCommand(server);
    const mcpUrl = server.urls.http || server.urls.sse;
    const commandToShow = platform === "claudeCode" ? claudeCodeCommand : mcpUrl;
    return <div key={server.name} className="server-card">
              <div>
                {server.documentation ? <a href={server.documentation}>
                    <strong>{server.name}</strong>
                  </a> : <strong>{server.name}</strong>}
              </div>

              <p style={{
      margin: '0.5rem 0',
      fontSize: '0.9rem'
    }}>
                {server.description}
              </p>

              {server.setupUrl && <p style={{
      margin: '0.25rem 0',
      fontSize: '0.8rem',
      fontStyle: 'italic',
      opacity: 0.7
    }}>
                  Requires user-specific URL.{' '}
                  <a href={server.setupUrl} style={{
      textDecoration: 'underline'
    }}>
                    Get your URL here
                  </a>.
                </p>}

              {commandToShow && !server.setupUrl && <>
                <p style={{
      display: 'block',
      fontSize: '0.75rem',
      fontWeight: 500,
      minWidth: 'fit-content',
      marginTop: '0.5rem',
      marginBottom: 0
    }}>
                  {platform === "claudeCode" ? "Command" : "URL"}
                </p>
                <div className="command-row">
                  <code>
                    {commandToShow}
                  </code>
                </div>
              </>}
            </div>;
  })}
      </div>
    </>;
};

Claude Code kann sich über das [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), einen offenen Standard für KI-Tool-Integrationen, mit Hunderten von externen Tools und Datenquellen verbinden. MCP-Server geben Claude Code Zugriff auf Ihre Tools, Datenbanken und APIs.

## Was Sie mit MCP tun können

Mit verbundenen MCP-Servern können Sie Claude Code auffordern:

* **Funktionen aus Issue-Trackern implementieren**: „Füge die in JIRA-Issue ENG-4521 beschriebene Funktion hinzu und erstelle einen PR auf GitHub."
* **Überwachungsdaten analysieren**: „Überprüfe Sentry und Statsig, um die Nutzung der in ENG-4521 beschriebenen Funktion zu überprüfen."
* **Datenbanken abfragen**: „Finde E-Mail-Adressen von 10 zufälligen Benutzern, die die Funktion ENG-4521 verwendet haben, basierend auf unserer PostgreSQL-Datenbank."
* **Designs integrieren**: „Aktualisiere unsere Standard-E-Mail-Vorlage basierend auf den neuen Figma-Designs, die in Slack gepostet wurden"
* **Workflows automatisieren**: „Erstelle Gmail-Entwürfe, die diese 10 Benutzer zu einer Feedback-Sitzung zur neuen Funktion einladen."
* **Auf externe Ereignisse reagieren**: Ein MCP-Server kann auch als [Kanal](/de/channels) fungieren, der Nachrichten in Ihre Sitzung pusht, sodass Claude auf Telegram-Nachrichten, Discord-Chats oder Webhook-Ereignisse reagiert, während Sie weg sind.

## Beliebte MCP-Server

Hier sind einige häufig verwendete MCP-Server, die Sie mit Claude Code verbinden können:

<Warning>
  Verwenden Sie MCP-Server von Drittanbietern auf eigenes Risiko – Anthropic hat
  die Korrektheit oder Sicherheit aller dieser Server nicht überprüft.
  Stellen Sie sicher, dass Sie den MCP-Servern vertrauen, die Sie installieren.
  Seien Sie besonders vorsichtig bei der Verwendung von MCP-Servern, die nicht vertrauenswürdige
  Inhalte abrufen könnten, da diese Sie dem Risiko von Prompt-Injection aussetzen können.
</Warning>

<MCPServersTable platform="claudeCode" />

<Note>
  **Benötigen Sie eine spezifische Integration?** [Finden Sie Hunderte weitere MCP-Server auf GitHub](https://github.com/modelcontextprotocol/servers), oder erstellen Sie Ihren eigenen mit dem [MCP SDK](https://modelcontextprotocol.io/quickstart/server).
</Note>

## MCP-Server installieren

MCP-Server können je nach Ihren Anforderungen auf drei verschiedene Arten konfiguriert werden:

### Option 1: Einen Remote-HTTP-Server hinzufügen

HTTP-Server sind die empfohlene Option für die Verbindung mit Remote-MCP-Servern. Dies ist das am weitesten unterstützte Transportprotokoll für Cloud-basierte Dienste.

```bash  theme={null}
# Grundlegende Syntax
claude mcp add --transport http <name> <url>

# Echtes Beispiel: Mit Notion verbinden
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Beispiel mit Bearer-Token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### Option 2: Einen Remote-SSE-Server hinzufügen

<Warning>
  Das SSE-Transportprotokoll (Server-Sent Events) ist veraltet. Verwenden Sie stattdessen HTTP-Server, wo verfügbar.
</Warning>

```bash  theme={null}
# Grundlegende Syntax
claude mcp add --transport sse <name> <url>

# Echtes Beispiel: Mit Asana verbinden
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Beispiel mit Authentifizierungs-Header
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

### Option 3: Einen lokalen Stdio-Server hinzufügen

Stdio-Server werden als lokale Prozesse auf Ihrem Computer ausgeführt. Sie sind ideal für Tools, die direkten Systemzugriff oder benutzerdefinierte Skripte benötigen.

```bash  theme={null}
# Grundlegende Syntax
claude mcp add [options] <name> -- <command> [args...]

# Echtes Beispiel: Airtable-Server hinzufügen
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server
```

<Note>
  **Wichtig: Reihenfolge der Optionen**

  Alle Optionen (`--transport`, `--env`, `--scope`, `--header`) müssen **vor** dem Servernamen kommen. Der `--` (Doppelstrich) trennt dann den Servernamen von dem Befehl und den Argumenten, die an den MCP-Server übergeben werden.

  Zum Beispiel:

  * `claude mcp add --transport stdio myserver -- npx server` → führt `npx server` aus
  * `claude mcp add --transport stdio --env KEY=value myserver -- python server.py --port 8080` → führt `python server.py --port 8080` mit `KEY=value` in der Umgebung aus

  Dies verhindert Konflikte zwischen Claudes Flags und den Flags des Servers.
</Note>

### Verwalten Ihrer Server

Nach der Konfiguration können Sie Ihre MCP-Server mit diesen Befehlen verwalten:

```bash  theme={null}
# Alle konfigurierten Server auflisten
claude mcp list

# Details für einen bestimmten Server abrufen
claude mcp get github

# Einen Server entfernen
claude mcp remove github

# (innerhalb von Claude Code) Serverstatus überprüfen
/mcp
```

### Dynamische Tool-Updates

Claude Code unterstützt MCP-`list_changed`-Benachrichtigungen, die es MCP-Servern ermöglichen, ihre verfügbaren Tools, Prompts und Ressourcen dynamisch zu aktualisieren, ohne dass Sie die Verbindung trennen und erneut verbinden müssen. Wenn ein MCP-Server eine `list_changed`-Benachrichtigung sendet, aktualisiert Claude Code automatisch die verfügbaren Funktionen von diesem Server.

### Push-Nachrichten mit Kanälen

Ein MCP-Server kann auch Nachrichten direkt in Ihre Sitzung pushen, sodass Claude auf externe Ereignisse wie CI-Ergebnisse, Überwachungswarnungen oder Chat-Nachrichten reagieren kann. Um dies zu aktivieren, deklariert Ihr Server die Funktion `claude/channel` und Sie aktivieren sie mit dem Flag `--channels` beim Start. Siehe [Kanäle](/de/channels), um einen offiziell unterstützten Kanal zu verwenden, oder [Kanäle-Referenz](/de/channels-reference), um Ihren eigenen zu erstellen.

<Tip>
  Tipps:

  * Verwenden Sie das Flag `--scope`, um anzugeben, wo die Konfiguration gespeichert wird:
    * `local` (Standard): Nur für Sie im aktuellen Projekt verfügbar (hieß in älteren Versionen `project`)
    * `project`: Geteilt mit allen im Projekt über die Datei `.mcp.json`
    * `user`: Für Sie über alle Projekte hinweg verfügbar (hieß in älteren Versionen `global`)
  * Legen Sie Umgebungsvariablen mit `--env`-Flags fest (zum Beispiel `--env KEY=value`)
  * Konfigurieren Sie das Startup-Timeout des MCP-Servers mit der Umgebungsvariablen MCP\_TIMEOUT (zum Beispiel `MCP_TIMEOUT=10000 claude` setzt ein 10-Sekunden-Timeout)
  * Claude Code zeigt eine Warnung an, wenn die MCP-Tool-Ausgabe 10.000 Token überschreitet. Um dieses Limit zu erhöhen, setzen Sie die Umgebungsvariable `MAX_MCP_OUTPUT_TOKENS` (zum Beispiel `MAX_MCP_OUTPUT_TOKENS=50000`)
  * Verwenden Sie `/mcp`, um sich bei Remote-Servern zu authentifizieren, die OAuth 2.0-Authentifizierung erfordern
</Tip>

<Warning>
  **Windows-Benutzer**: Auf nativem Windows (nicht WSL) erfordern lokale MCP-Server, die `npx` verwenden, den `cmd /c`-Wrapper, um eine ordnungsgemäße Ausführung zu gewährleisten.

  ```bash  theme={null}
  # Dies erstellt command="cmd", das Windows ausführen kann
  claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
  ```

  Ohne den `cmd /c`-Wrapper treten „Connection closed"-Fehler auf, da Windows `npx` nicht direkt ausführen kann. (Siehe die obige Notiz für eine Erklärung des `--`-Parameters.)
</Warning>

### Von Plugins bereitgestellte MCP-Server

[Plugins](/de/plugins) können MCP-Server bündeln und automatisch Tools und Integrationen bereitstellen, wenn das Plugin aktiviert ist. Plugin-MCP-Server funktionieren identisch mit benutzerkonfigurierten Servern.

**Wie Plugin-MCP-Server funktionieren**:

* Plugins definieren MCP-Server in `.mcp.json` im Plugin-Root oder inline in `plugin.json`
* Wenn ein Plugin aktiviert ist, starten seine MCP-Server automatisch
* Plugin-MCP-Tools erscheinen neben manuell konfigurierten MCP-Tools
* Plugin-Server werden durch die Plugin-Installation verwaltet (nicht durch `/mcp`-Befehle)

**Beispiel-Plugin-MCP-Konfiguration**:

In `.mcp.json` im Plugin-Root:

```json  theme={null}
{
  "mcpServers": {
    "database-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_URL": "${DB_URL}"
      }
    }
  }
}
```

Oder inline in `plugin.json`:

```json  theme={null}
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

**Plugin-MCP-Funktionen**:

* **Automatischer Lebenszyklus**: Bei Sitzungsstart verbinden sich Server für aktivierte Plugins automatisch. Wenn Sie ein Plugin während einer Sitzung aktivieren oder deaktivieren, führen Sie `/reload-plugins` aus, um seine MCP-Server zu verbinden oder zu trennen
* **Umgebungsvariablen**: Verwenden Sie `${CLAUDE_PLUGIN_ROOT}` für gebündelte Plugin-Dateien und `${CLAUDE_PLUGIN_DATA}` für [persistente Daten](/de/plugins-reference#persistent-data-directory), die Plugin-Updates überstehen
* **Zugriff auf Benutzerumgebung**: Zugriff auf die gleichen Umgebungsvariablen wie manuell konfigurierte Server
* **Mehrere Transporttypen**: Unterstützung für Stdio-, SSE- und HTTP-Transporte (die Transportunterstützung kann je nach Server variieren)

**Anzeigen von Plugin-MCP-Servern**:

```bash  theme={null}
# Innerhalb von Claude Code alle MCP-Server einschließlich Plugin-Server anzeigen
/mcp
```

Plugin-Server erscheinen in der Liste mit Indikatoren, die zeigen, dass sie von Plugins stammen.

**Vorteile von Plugin-MCP-Servern**:

* **Gebündelte Verteilung**: Tools und Server zusammen verpackt
* **Automatische Einrichtung**: Keine manuelle MCP-Konfiguration erforderlich
* **Team-Konsistenz**: Alle erhalten die gleichen Tools, wenn das Plugin installiert ist

Siehe die [Plugin-Komponenten-Referenz](/de/plugins-reference#mcp-servers) für Details zum Bündeln von MCP-Servern mit Plugins.

## MCP-Installationsbereiche

MCP-Server können auf drei verschiedenen Bereichsebenen konfiguriert werden, die jeweils unterschiedliche Zwecke für die Verwaltung der Serverzugänglichkeit und des Austauschs erfüllen. Das Verständnis dieser Bereiche hilft Ihnen, die beste Methode zur Konfiguration von Servern für Ihre spezifischen Anforderungen zu bestimmen.

### Lokaler Bereich

Lokal begrenzte Server stellen die Standard-Konfigurationsebene dar und werden in `~/.claude.json` unter dem Pfad Ihres Projekts gespeichert. Diese Server bleiben privat für Sie und sind nur zugänglich, wenn Sie im aktuellen Projektverzeichnis arbeiten. Dieser Bereich ist ideal für persönliche Entwicklungsserver, experimentelle Konfigurationen oder Server, die vertrauliche Anmeldedaten enthalten, die nicht geteilt werden sollten.

<Note>
  Der Begriff „lokaler Bereich" für MCP-Server unterscheidet sich von allgemeinen lokalen Einstellungen. Lokal begrenzte MCP-Server werden in `~/.claude.json` (Ihr Home-Verzeichnis) gespeichert, während allgemeine lokale Einstellungen `.claude/settings.local.json` (im Projektverzeichnis) verwenden. Siehe [Einstellungen](/de/settings#settings-files) für Details zu Einstellungsdatei-Speicherorten.
</Note>

```bash  theme={null}
# Einen lokal begrenzten Server hinzufügen (Standard)
claude mcp add --transport http stripe https://mcp.stripe.com

# Lokalen Bereich explizit angeben
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

### Projektbereich

Projektbegrenzte Server ermöglichen Teamzusammenarbeit durch das Speichern von Konfigurationen in einer `.mcp.json`-Datei im Root-Verzeichnis Ihres Projekts. Diese Datei ist dazu bestimmt, in die Versionskontrolle eingecheckt zu werden, um sicherzustellen, dass alle Teammitglieder Zugriff auf die gleichen MCP-Tools und -Dienste haben. Wenn Sie einen projektbegrenzten Server hinzufügen, erstellt oder aktualisiert Claude Code automatisch diese Datei mit der entsprechenden Konfigurationsstruktur.

```bash  theme={null}
# Einen projektbegrenzten Server hinzufügen
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

Die resultierende `.mcp.json`-Datei folgt einem standardisierten Format:

```json  theme={null}
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

Aus Sicherheitsgründen fordert Claude Code eine Genehmigung an, bevor projektbegrenzte Server aus `.mcp.json`-Dateien verwendet werden. Wenn Sie diese Genehmigungswahlmöglichkeiten zurücksetzen müssen, verwenden Sie den Befehl `claude mcp reset-project-choices`.

### Benutzerbereich

Benutzerbegrenzte Server werden in `~/.claude.json` gespeichert und bieten projektübergreifende Zugänglichkeit, wodurch sie über alle Projekte auf Ihrem Computer verfügbar sind und gleichzeitig privat für Ihr Benutzerkonto bleiben. Dieser Bereich funktioniert gut für persönliche Utility-Server, Entwicklungstools oder Dienste, die Sie häufig über verschiedene Projekte hinweg verwenden.

```bash  theme={null}
# Einen Benutzer-Server hinzufügen
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### Den richtigen Bereich wählen

Wählen Sie Ihren Bereich basierend auf:

* **Lokaler Bereich**: Persönliche Server, experimentelle Konfigurationen oder vertrauliche Anmeldedaten, die spezifisch für ein Projekt sind
* **Projektbereich**: Von Teams gemeinsam genutzte Server, projektspezifische Tools oder Dienste, die für die Zusammenarbeit erforderlich sind
* **Benutzerbereich**: Persönliche Utilities, die über mehrere Projekte hinweg benötigt werden, Entwicklungstools oder häufig verwendete Dienste

<Note>
  **Wo werden MCP-Server gespeichert?**

  * **Benutzer- und lokaler Bereich**: `~/.claude.json` (im Feld `mcpServers` oder unter Projektpfaden)
  * **Projektbereich**: `.mcp.json` im Projekt-Root (eingecheckt in die Versionskontrolle)
  * **Verwaltet**: `managed-mcp.json` in Systemverzeichnissen (siehe [Verwaltete MCP-Konfiguration](#managed-mcp-configuration))
</Note>

### Bereichshierarchie und Vorrang

MCP-Server-Konfigurationen folgen einer klaren Vorranghierarchie. Wenn Server mit dem gleichen Namen auf mehreren Bereichen vorhanden sind, löst das System Konflikte durch Priorisierung lokal begrenzter Server zuerst, gefolgt von projektbegrenzten Servern und schließlich benutzerbegrenzten Servern. Dieses Design stellt sicher, dass persönliche Konfigurationen gemeinsame Konfigurationen bei Bedarf überschreiben können.

Wenn ein Server sowohl lokal als auch über einen [Claude.ai-Connector](#use-mcp-servers-from-claude-ai) konfiguriert ist, hat die lokale Konfiguration Vorrang und der Connector-Eintrag wird übersprungen.

### Umgebungsvariablen-Erweiterung in `.mcp.json`

Claude Code unterstützt die Umgebungsvariablen-Erweiterung in `.mcp.json`-Dateien, die es Teams ermöglicht, Konfigurationen zu teilen und gleichzeitig Flexibilität für maschinenspezifische Pfade und vertrauliche Werte wie API-Schlüssel zu bewahren.

**Unterstützte Syntax:**

* `${VAR}` - Erweitert sich zum Wert der Umgebungsvariablen `VAR`
* `${VAR:-default}` - Erweitert sich zu `VAR`, wenn gesetzt, andernfalls wird `default` verwendet

**Erweiterungsorte:**
Umgebungsvariablen können erweitert werden in:

* `command` - Der Server-Ausführungspfad
* `args` - Befehlszeilenargumente
* `env` - Umgebungsvariablen, die an den Server übergeben werden
* `url` - Für HTTP-Server-Typen
* `headers` - Für HTTP-Server-Authentifizierung

**Beispiel mit Variablenerweiterung:**

```json  theme={null}
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

Wenn eine erforderliche Umgebungsvariable nicht gesetzt ist und keinen Standardwert hat, kann Claude Code die Konfiguration nicht analysieren.

## Praktische Beispiele

{/* ### Beispiel: Browser-Tests mit Playwright automatisieren

  ```bash
  claude mcp add --transport stdio playwright -- npx -y @playwright/mcp@latest
  ```

  Dann schreiben und führen Sie Browser-Tests aus:

  ```text
  Test if the login flow works with test@example.com
  ```
  ```text
  Take a screenshot of the checkout page on mobile
  ```
  ```text
  Verify that the search feature returns results
  ``` */}

### Beispiel: Fehler mit Sentry überwachen

```bash  theme={null}
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

Authentifizieren Sie sich mit Ihrem Sentry-Konto:

```text  theme={null}
/mcp
```

Debuggen Sie dann Produktionsprobleme:

```text  theme={null}
What are the most common errors in the last 24 hours?
```

```text  theme={null}
Show me the stack trace for error ID abc123
```

```text  theme={null}
Which deployment introduced these new errors?
```

### Beispiel: Mit GitHub für Code-Reviews verbinden

```bash  theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Authentifizieren Sie sich bei Bedarf, indem Sie „Authenticate" für GitHub auswählen:

```text  theme={null}
/mcp
```

Arbeiten Sie dann mit GitHub:

```text  theme={null}
Review PR #456 and suggest improvements
```

```text  theme={null}
Create a new issue for the bug we just found
```

```text  theme={null}
Show me all open PRs assigned to me
```

### Beispiel: Ihre PostgreSQL-Datenbank abfragen

```bash  theme={null}
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"
```

Fragen Sie dann Ihre Datenbank natürlich ab:

```text  theme={null}
What's our total revenue this month?
```

```text  theme={null}
Show me the schema for the orders table
```

```text  theme={null}
Find customers who haven't made a purchase in 90 days
```

## Mit Remote-MCP-Servern authentifizieren

Viele Cloud-basierte MCP-Server erfordern Authentifizierung. Claude Code unterstützt OAuth 2.0 für sichere Verbindungen.

<Steps>
  <Step title="Fügen Sie den Server hinzu, der Authentifizierung erfordert">
    Zum Beispiel:

    ```bash  theme={null}
    claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
    ```
  </Step>

  <Step title="Verwenden Sie den /mcp-Befehl innerhalb von Claude Code">
    In Claude Code verwenden Sie den Befehl:

    ```text  theme={null}
    /mcp
    ```

    Folgen Sie dann den Schritten in Ihrem Browser, um sich anzumelden.
  </Step>
</Steps>

<Tip>
  Tipps:

  * Authentifizierungstoken werden sicher gespeichert und automatisch aktualisiert
  * Verwenden Sie „Clear authentication" im `/mcp`-Menü, um den Zugriff zu widerrufen
  * Wenn Ihr Browser nicht automatisch geöffnet wird, kopieren Sie die bereitgestellte URL und öffnen Sie sie manuell
  * Wenn die Browser-Umleitung nach der Authentifizierung mit einem Verbindungsfehler fehlschlägt, fügen Sie die vollständige Callback-URL aus der Adressleiste Ihres Browsers in die URL-Eingabeaufforderung ein, die in Claude Code angezeigt wird
  * OAuth-Authentifizierung funktioniert mit HTTP-Servern
</Tip>

### Verwenden Sie einen festen OAuth-Callback-Port

Einige MCP-Server erfordern einen spezifischen Redirect-URI, der im Voraus registriert ist. Standardmäßig wählt Claude Code einen zufällig verfügbaren Port für den OAuth-Callback. Verwenden Sie `--callback-port`, um den Port zu fixieren, damit er einem vorregistrierten Redirect-URI der Form `http://localhost:PORT/callback` entspricht.

Sie können `--callback-port` allein (mit dynamischer Client-Registrierung) oder zusammen mit `--client-id` (mit vorkonfigurierten Anmeldedaten) verwenden.

```bash  theme={null}
# Fester Callback-Port mit dynamischer Client-Registrierung
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

### Verwenden Sie vorkonfigurierte OAuth-Anmeldedaten

Einige MCP-Server unterstützen keine automatische OAuth-Einrichtung über Dynamic Client Registration. Wenn Sie einen Fehler wie „Incompatible auth server: does not support dynamic client registration" sehen, erfordert der Server vorkonfigurierte Anmeldedaten. Claude Code unterstützt auch Server, die ein Client ID Metadata Document (CIMD) anstelle von Dynamic Client Registration verwenden, und erkennt diese automatisch. Wenn die automatische Erkennung fehlschlägt, registrieren Sie zunächst eine OAuth-App über das Entwicklerportal des Servers und geben Sie dann die Anmeldedaten beim Hinzufügen des Servers an.

<Steps>
  <Step title="Registrieren Sie eine OAuth-App beim Server">
    Erstellen Sie eine App über das Entwicklerportal des Servers und notieren Sie sich Ihre Client-ID und Ihren Client-Secret.

    Viele Server erfordern auch einen Redirect-URI. Wenn ja, wählen Sie einen Port und registrieren Sie einen Redirect-URI im Format `http://localhost:PORT/callback`. Verwenden Sie denselben Port mit `--callback-port` im nächsten Schritt.
  </Step>

  <Step title="Fügen Sie den Server mit Ihren Anmeldedaten hinzu">
    Wählen Sie eine der folgenden Methoden. Der für `--callback-port` verwendete Port kann ein beliebiger verfügbarer Port sein. Er muss nur dem Redirect-URI entsprechen, den Sie im vorherigen Schritt registriert haben.

    <Tabs>
      <Tab title="claude mcp add">
        Verwenden Sie `--client-id`, um die Client-ID Ihrer App zu übergeben. Das Flag `--client-secret` fordert das Secret mit maskierter Eingabe an:

        ```bash  theme={null}
        claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>

      <Tab title="claude mcp add-json">
        Fügen Sie das Objekt `oauth` in die JSON-Konfiguration ein und übergeben Sie `--client-secret` als separates Flag:

        ```bash  theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' \
          --client-secret
        ```
      </Tab>

      <Tab title="claude mcp add-json (nur Callback-Port)">
        Verwenden Sie `--callback-port` ohne Client-ID, um den Port zu fixieren und gleichzeitig die dynamische Client-Registrierung zu verwenden:

        ```bash  theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"callbackPort":8080}}'
        ```
      </Tab>

      <Tab title="CI / Umgebungsvariable">
        Legen Sie das Secret über eine Umgebungsvariable fest, um die interaktive Eingabeaufforderung zu überspringen:

        ```bash  theme={null}
        MCP_CLIENT_SECRET=your-secret claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Authentifizieren Sie sich in Claude Code">
    Führen Sie `/mcp` in Claude Code aus und folgen Sie dem Browser-Login-Ablauf.
  </Step>
</Steps>

<Tip>
  Tipps:

  * Das Client-Secret wird sicher in Ihrem System-Keychain (macOS) oder einer Anmeldedatei gespeichert, nicht in Ihrer Konfiguration
  * Wenn der Server einen öffentlichen OAuth-Client ohne Secret verwendet, verwenden Sie nur `--client-id` ohne `--client-secret`
  * `--callback-port` kann mit oder ohne `--client-id` verwendet werden
  * Diese Flags gelten nur für HTTP- und SSE-Transporte. Sie haben keine Auswirkung auf Stdio-Server
  * Verwenden Sie `claude mcp get <name>`, um zu überprüfen, dass OAuth-Anmeldedaten für einen Server konfiguriert sind
</Tip>

### Überschreiben Sie die OAuth-Metadaten-Erkennung

Wenn Ihr MCP-Server Fehler auf den Standard-OAuth-Metadaten-Endpunkten zurückgibt, aber einen funktionierenden OIDC-Endpunkt verfügbar macht, können Sie Claude Code auf eine bestimmte Metadaten-URL verweisen, um die Standard-Erkennungskette zu umgehen. Standardmäßig überprüft Claude Code zunächst RFC 9728 Protected Resource Metadata unter `/.well-known/oauth-protected-resource` und fällt dann auf RFC 8414 Authorization Server Metadata unter `/.well-known/oauth-authorization-server` zurück.

Legen Sie `authServerMetadataUrl` im Objekt `oauth` der Konfiguration Ihres Servers in `.mcp.json` fest:

```json  theme={null}
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

Die URL muss `https://` verwenden. Diese Option erfordert Claude Code v2.1.64 oder später.

### Verwenden Sie dynamische Header für benutzerdefinierte Authentifizierung

Wenn Ihr MCP-Server ein anderes Authentifizierungsschema verwendet als OAuth (wie Kerberos, kurzlebige Token oder ein internes SSO), verwenden Sie `headersHelper`, um Request-Header zur Verbindungszeit zu generieren. Claude Code führt den Befehl aus und fügt seine Ausgabe in die Verbindungs-Header ein.

```json  theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "/opt/bin/get-mcp-auth-headers.sh"
    }
  }
}
```

Der Befehl kann auch inline sein:

```json  theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "echo '{\"Authorization\": \"Bearer '\"$(get-token)\"'\"}'"
    }
  }
}
```

**Anforderungen:**

* Der Befehl muss ein JSON-Objekt mit String-Schlüssel-Wert-Paaren auf stdout schreiben
* Der Befehl wird in einer Shell mit einem 10-Sekunden-Timeout ausgeführt
* Dynamische Header überschreiben alle statischen `headers` mit dem gleichen Namen

Der Helper wird bei jeder Verbindung neu ausgeführt (beim Sitzungsstart und bei Wiederverbindung). Es gibt kein Caching, daher ist Ihr Skript für jede Token-Wiederverwendung verantwortlich.

Claude Code setzt diese Umgebungsvariablen beim Ausführen des Helpers:

| Variable                      | Wert                     |
| :---------------------------- | :----------------------- |
| `CLAUDE_CODE_MCP_SERVER_NAME` | der Name des MCP-Servers |
| `CLAUDE_CODE_MCP_SERVER_URL`  | die URL des MCP-Servers  |

Verwenden Sie diese, um ein einzelnes Helper-Skript zu schreiben, das mehrere MCP-Server bedient.

<Note>
  `headersHelper` führt beliebige Shell-Befehle aus. Wenn es auf Projekt- oder lokalem Bereich definiert ist, wird es nur nach Ihrer Zustimmung zum Workspace-Trust-Dialog ausgeführt.
</Note>

## MCP-Server aus JSON-Konfiguration hinzufügen

Wenn Sie eine JSON-Konfiguration für einen MCP-Server haben, können Sie sie direkt hinzufügen:

<Steps>
  <Step title="Fügen Sie einen MCP-Server aus JSON hinzu">
    ```bash  theme={null}
    # Grundlegende Syntax
    claude mcp add-json <name> '<json>'

    # Beispiel: Hinzufügen eines HTTP-Servers mit JSON-Konfiguration
    claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'

    # Beispiel: Hinzufügen eines Stdio-Servers mit JSON-Konfiguration
    claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'

    # Beispiel: Hinzufügen eines HTTP-Servers mit vorkonfigurierten OAuth-Anmeldedaten
    claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' --client-secret
    ```
  </Step>

  <Step title="Überprüfen Sie, dass der Server hinzugefügt wurde">
    ```bash  theme={null}
    claude mcp get weather-api
    ```
  </Step>
</Steps>

<Tip>
  Tipps:

  * Stellen Sie sicher, dass das JSON in Ihrer Shell ordnungsgemäß escaped ist
  * Das JSON muss dem MCP-Server-Konfigurationsschema entsprechen
  * Sie können `--scope user` verwenden, um den Server zu Ihrer Benutzerkonfiguration statt zur projektspezifischen hinzuzufügen
</Tip>

## MCP-Server aus Claude Desktop importieren

Wenn Sie bereits MCP-Server in Claude Desktop konfiguriert haben, können Sie diese importieren:

<Steps>
  <Step title="Importieren Sie Server aus Claude Desktop">
    ```bash  theme={null}
    # Grundlegende Syntax 
    claude mcp add-from-claude-desktop 
    ```
  </Step>

  <Step title="Wählen Sie aus, welche Server importiert werden sollen">
    Nach dem Ausführen des Befehls wird ein interaktives Dialogfeld angezeigt, in dem Sie auswählen können, welche Server Sie importieren möchten.
  </Step>

  <Step title="Überprüfen Sie, dass die Server importiert wurden">
    ```bash  theme={null}
    claude mcp list 
    ```
  </Step>
</Steps>

<Tip>
  Tipps:

  * Diese Funktion funktioniert nur auf macOS und Windows Subsystem for Linux (WSL)
  * Sie liest die Claude Desktop-Konfigurationsdatei von ihrem Standardort auf diesen Plattformen
  * Verwenden Sie das Flag `--scope user`, um Server zu Ihrer Benutzerkonfiguration hinzuzufügen
  * Importierte Server haben die gleichen Namen wie in Claude Desktop
  * Wenn Server mit den gleichen Namen bereits vorhanden sind, erhalten sie ein numerisches Suffix (zum Beispiel `server_1`)
</Tip>

## MCP-Server von Claude.ai verwenden

Wenn Sie sich in Claude Code mit einem [Claude.ai](https://claude.ai)-Konto angemeldet haben, sind MCP-Server, die Sie in Claude.ai hinzugefügt haben, automatisch in Claude Code verfügbar:

<Steps>
  <Step title="Konfigurieren Sie MCP-Server in Claude.ai">
    Fügen Sie Server unter [claude.ai/settings/connectors](https://claude.ai/settings/connectors) hinzu. Bei Team- und Enterprise-Plänen können nur Administratoren Server hinzufügen.
  </Step>

  <Step title="Authentifizieren Sie den MCP-Server">
    Führen Sie alle erforderlichen Authentifizierungsschritte in Claude.ai durch.
  </Step>

  <Step title="Zeigen Sie Server in Claude Code an und verwalten Sie sie">
    In Claude Code verwenden Sie den Befehl:

    ```text  theme={null}
    /mcp
    ```

    Claude.ai-Server erscheinen in der Liste mit Indikatoren, die zeigen, dass sie von Claude.ai stammen.
  </Step>
</Steps>

Um Claude.ai-MCP-Server in Claude Code zu deaktivieren, setzen Sie die Umgebungsvariable `ENABLE_CLAUDEAI_MCP_SERVERS` auf `false`:

```bash  theme={null}
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

## Claude Code als MCP-Server verwenden

Sie können Claude Code selbst als MCP-Server verwenden, mit dem sich andere Anwendungen verbinden können:

```bash  theme={null}
# Starten Sie Claude als Stdio-MCP-Server
claude mcp serve
```

Sie können dies in Claude Desktop verwenden, indem Sie diese Konfiguration zu claude\_desktop\_config.json hinzufügen:

```json  theme={null}
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

<Warning>
  **Konfigurieren Sie den Pfad der ausführbaren Datei**: Das Feld `command` muss auf die Claude Code-Ausführungsdatei verweisen. Wenn der Befehl `claude` nicht in Ihrem System-PATH vorhanden ist, müssen Sie den vollständigen Pfad zur ausführbaren Datei angeben.

  Um den vollständigen Pfad zu finden:

  ```bash  theme={null}
  which claude
  ```

  Verwenden Sie dann den vollständigen Pfad in Ihrer Konfiguration:

  ```json  theme={null}
  {
    "mcpServers": {
      "claude-code": {
        "type": "stdio",
        "command": "/full/path/to/claude",
        "args": ["mcp", "serve"],
        "env": {}
      }
    }
  }
  ```

  Ohne den korrekten Pfad der ausführbaren Datei treten Fehler wie `spawn claude ENOENT` auf.
</Warning>

<Tip>
  Tipps:

  * Der Server bietet Zugriff auf Claudes Tools wie View, Edit, LS usw.
  * In Claude Desktop versuchen Sie, Claude aufzufordern, Dateien in einem Verzeichnis zu lesen, Änderungen vorzunehmen und mehr.
  * Beachten Sie, dass dieser MCP-Server nur Claudes Tools für Ihren MCP-Client verfügbar macht, daher ist Ihr eigener Client dafür verantwortlich, Benutzerbestätigung für einzelne Tool-Aufrufe zu implementieren.
</Tip>

## MCP-Ausgabelimits und Warnungen

Wenn MCP-Tools große Ausgaben erzeugen, hilft Claude Code bei der Verwaltung der Token-Nutzung, um zu verhindern, dass Ihr Gesprächskontext überwältigt wird:

* **Ausgabe-Warnungsschwelle**: Claude Code zeigt eine Warnung an, wenn eine MCP-Tool-Ausgabe 10.000 Token überschreitet
* **Konfigurierbares Limit**: Sie können die maximale zulässige MCP-Ausgabe-Token mit der Umgebungsvariablen `MAX_MCP_OUTPUT_TOKENS` anpassen
* **Standardlimit**: Das Standardmaximum beträgt 25.000 Token

Um das Limit für Tools zu erhöhen, die große Ausgaben erzeugen:

```bash  theme={null}
# Legen Sie ein höheres Limit für MCP-Tool-Ausgaben fest
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

Dies ist besonders nützlich bei der Arbeit mit MCP-Servern, die:

* Große Datensätze oder Datenbanken abfragen
* Detaillierte Berichte oder Dokumentation generieren
* Umfangreiche Protokolldateien oder Debugging-Informationen verarbeiten

<Warning>
  Wenn Sie häufig Ausgabewarnungen bei bestimmten MCP-Servern erhalten, erwägen Sie, das Limit zu erhöhen oder den Server so zu konfigurieren, dass er seine Antworten paginiert oder filtert.
</Warning>

## Auf MCP-Elicitierungsanfragen reagieren

MCP-Server können während einer Aufgabe strukturierte Eingaben von Ihnen anfordern, indem sie Elicitierung verwenden. Wenn ein Server Informationen benötigt, die er nicht selbst abrufen kann, zeigt Claude Code einen interaktiven Dialog an und leitet Ihre Antwort an den Server weiter. Auf Ihrer Seite ist keine Konfiguration erforderlich: Elicitierungs-Dialoge erscheinen automatisch, wenn ein Server sie anfordert.

Server können Eingaben auf zwei Arten anfordern:

* **Formularmodus**: Claude Code zeigt einen Dialog mit Formularfeldern an, die vom Server definiert werden (zum Beispiel eine Eingabeaufforderung für Benutzername und Passwort). Füllen Sie die Felder aus und senden Sie sie ab.
* **URL-Modus**: Claude Code öffnet eine Browser-URL für Authentifizierung oder Genehmigung. Führen Sie den Ablauf im Browser durch und bestätigen Sie dann in der CLI.

Um automatisch auf Elicitierungsanfragen ohne Dialog zu reagieren, verwenden Sie den [`Elicitation`-Hook](/de/hooks#Elicitation).

Wenn Sie einen MCP-Server erstellen, der Elicitierung verwendet, siehe die [MCP-Elicitierungs-Spezifikation](https://modelcontextprotocol.io/docs/learn/client-concepts#elicitation) für Protokolldetails und Schema-Beispiele.

## MCP-Ressourcen verwenden

MCP-Server können Ressourcen verfügbar machen, auf die Sie mit @-Erwähnungen verweisen können, ähnlich wie Sie auf Dateien verweisen.

### Referenzieren Sie MCP-Ressourcen

<Steps>
  <Step title="Verfügbare Ressourcen auflisten">
    Geben Sie `@` in Ihre Eingabeaufforderung ein, um verfügbare Ressourcen von allen verbundenen MCP-Servern anzuzeigen. Ressourcen erscheinen neben Dateien im Autocomplete-Menü.
  </Step>

  <Step title="Referenzieren Sie eine bestimmte Ressource">
    Verwenden Sie das Format `@server:protocol://resource/path`, um auf eine Ressource zu verweisen:

    ```text  theme={null}
    Can you analyze @github:issue://123 and suggest a fix?
    ```

    ```text  theme={null}
    Please review the API documentation at @docs:file://api/authentication
    ```
  </Step>

  <Step title="Mehrere Ressourcenreferenzen">
    Sie können mehrere Ressourcen in einer einzelnen Eingabeaufforderung referenzieren:

    ```text  theme={null}
    Compare @postgres:schema://users with @docs:file://database/user-model
    ```
  </Step>
</Steps>

<Tip>
  Tipps:

  * Ressourcen werden automatisch abgerufen und als Anhänge eingefügt, wenn sie referenziert werden
  * Ressourcenpfade sind fuzzy-durchsuchbar im @-Erwähnungs-Autocomplete
  * Claude Code stellt automatisch Tools zur Verfügung, um MCP-Ressourcen aufzulisten und zu lesen, wenn Server diese unterstützen
  * Ressourcen können jeden Inhaltstyp enthalten, den der MCP-Server bereitstellt (Text, JSON, strukturierte Daten usw.)
</Tip>

## Mit MCP-Tool-Suche skalieren

Die Tool-Suche hält die MCP-Kontextnutzung niedrig, indem Tool-Definitionen aufgeschoben werden, bis Claude sie benötigt. Nur Tool-Namen werden beim Sitzungsstart geladen, daher hat das Hinzufügen weiterer MCP-Server minimale Auswirkungen auf Ihr Kontextfenster.

### Wie es funktioniert

Die Tool-Suche ist standardmäßig aktiviert. MCP-Tools werden aufgeschoben, anstatt sie vorab in den Kontext zu laden, und Claude verwendet ein Such-Tool, um relevante Tools zu entdecken, wenn eine Aufgabe sie benötigt. Nur die Tools, die Claude tatsächlich verwendet, gelangen in den Kontext. Aus Ihrer Perspektive funktionieren MCP-Tools genau wie zuvor.

Wenn Sie schwellenwertbasiertes Laden bevorzugen, setzen Sie `ENABLE_TOOL_SEARCH=auto`, um Schemas vorab zu laden, wenn sie in 10 % des Kontextfensters passen, und verschieben Sie nur den Überschuss. Siehe [Tool-Suche konfigurieren](#configure-tool-search) für alle Optionen.

### Für MCP-Server-Autoren

Wenn Sie einen MCP-Server erstellen, wird das Feld für Server-Anweisungen mit aktivierter Tool-Suche nützlicher. Server-Anweisungen helfen Claude zu verstehen, wann nach Ihren Tools gesucht werden soll, ähnlich wie [Skills](/de/skills) funktionieren.

Fügen Sie klare, aussagekräftige Server-Anweisungen hinzu, die erklären:

* Welche Kategorie von Aufgaben Ihre Tools verarbeiten
* Wann Claude nach Ihren Tools suchen sollte
* Wichtige Funktionen, die Ihr Server bietet

Claude Code schneidet Tool-Beschreibungen und Server-Anweisungen bei 2 KB ab. Halten Sie sie prägnant, um Kürzungen zu vermeiden, und platzieren Sie kritische Details am Anfang.

### Konfigurieren Sie die Tool-Suche

Die Tool-Suche ist standardmäßig aktiviert: MCP-Tools werden aufgeschoben und bei Bedarf entdeckt. Wenn `ANTHROPIC_BASE_URL` auf einen Host von Drittanbietern verweist, ist die Tool-Suche standardmäßig deaktiviert, da die meisten Proxys `tool_reference`-Blöcke nicht weiterleiten. Legen Sie `ENABLE_TOOL_SEARCH` explizit fest, wenn Ihr Proxy dies tut. Diese Funktion erfordert Modelle, die `tool_reference`-Blöcke unterstützen: Sonnet 4 und später oder Opus 4 und später. Haiku-Modelle unterstützen die Tool-Suche nicht.

Steuern Sie das Verhalten der Tool-Suche mit der Umgebungsvariablen `ENABLE_TOOL_SEARCH`:

| Wert            | Verhalten                                                                                                                                              |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| (nicht gesetzt) | Alle MCP-Tools werden aufgeschoben und bei Bedarf geladen. Fällt auf das Laden vorab zurück, wenn `ANTHROPIC_BASE_URL` ein Host von Drittanbietern ist |
| `true`          | Alle MCP-Tools werden aufgeschoben, auch für `ANTHROPIC_BASE_URL` von Drittanbietern                                                                   |
| `auto`          | Schwellenmodus: Tools werden vorab geladen, wenn sie in 10 % des Kontextfensters passen, andernfalls aufgeschoben                                      |
| `auto:<N>`      | Schwellenmodus mit benutzerdefiniertem Prozentsatz, wobei `<N>` 0-100 ist (z. B. `auto:5` für 5 %)                                                     |
| `false`         | Alle MCP-Tools werden vorab geladen, keine Verschiebung                                                                                                |

```bash  theme={null}
# Verwenden Sie eine benutzerdefinierte 5%-Schwelle
ENABLE_TOOL_SEARCH=auto:5 claude

# Deaktivieren Sie die Tool-Suche vollständig
ENABLE_TOOL_SEARCH=false claude
```

Oder legen Sie den Wert im Feld `env` Ihrer [settings.json](/de/settings#available-settings) fest.

Sie können das `ToolSearch`-Tool auch spezifisch deaktivieren:

```json  theme={null}
{
  "permissions": {
    "deny": ["ToolSearch"]
  }
}
```

## MCP-Prompts als Befehle verwenden

MCP-Server können Prompts verfügbar machen, die in Claude Code als Befehle verfügbar werden.

### Führen Sie MCP-Prompts aus

<Steps>
  <Step title="Entdecken Sie verfügbare Prompts">
    Geben Sie `/` ein, um alle verfügbaren Befehle anzuzeigen, einschließlich derer von MCP-Servern. MCP-Prompts erscheinen mit dem Format `/mcp__servername__promptname`.
  </Step>

  <Step title="Führen Sie einen Prompt ohne Argumente aus">
    ```text  theme={null}
    /mcp__github__list_prs
    ```
  </Step>

  <Step title="Führen Sie einen Prompt mit Argumenten aus">
    Viele Prompts akzeptieren Argumente. Übergeben Sie sie durch Leerzeichen getrennt nach dem Befehl:

    ```text  theme={null}
    /mcp__github__pr_review 456
    ```

    ```text  theme={null}
    /mcp__jira__create_issue "Bug in login flow" high
    ```
  </Step>
</Steps>

<Tip>
  Tipps:

  * MCP-Prompts werden dynamisch von verbundenen Servern entdeckt
  * Argumente werden basierend auf den definierten Parametern des Prompts analysiert
  * Prompt-Ergebnisse werden direkt in das Gespräch eingefügt
  * Server- und Prompt-Namen werden normalisiert (Leerzeichen werden zu Unterstrichen)
</Tip>

## Verwaltete MCP-Konfiguration

Für Organisationen, die eine zentralisierte Kontrolle über MCP-Server benötigen, unterstützt Claude Code zwei Konfigurationsoptionen:

1. **Exklusive Kontrolle mit `managed-mcp.json`**: Stellen Sie einen festen Satz von MCP-Servern bereit, die Benutzer nicht ändern oder erweitern können
2. **Richtlinienbasierte Kontrolle mit Allowlists/Denylists**: Ermöglichen Sie Benutzern, ihre eigenen Server hinzuzufügen, aber beschränken Sie, welche zulässig sind

Diese Optionen ermöglichen IT-Administratoren:

* **Kontrollieren Sie, auf welche MCP-Server Mitarbeiter zugreifen können**: Stellen Sie einen standardisierten Satz genehmigter MCP-Server in der gesamten Organisation bereit
* **Verhindern Sie nicht autorisierte MCP-Server**: Beschränken Sie Benutzer daran, nicht genehmigte MCP-Server hinzuzufügen
* **Deaktivieren Sie MCP vollständig**: Entfernen Sie die MCP-Funktionalität vollständig, falls erforderlich

### Option 1: Exklusive Kontrolle mit managed-mcp.json

Wenn Sie eine `managed-mcp.json`-Datei bereitstellen, übernimmt sie die **exklusive Kontrolle** über alle MCP-Server. Benutzer können keine MCP-Server außer denen, die in dieser Datei definiert sind, hinzufügen, ändern oder verwenden. Dies ist der einfachste Ansatz für Organisationen, die vollständige Kontrolle wünschen.

Systemadministratoren stellen die Konfigurationsdatei in einem systemweiten Verzeichnis bereit:

* macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
* Linux und WSL: `/etc/claude-code/managed-mcp.json`
* Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

<Note>
  Dies sind systemweite Pfade (nicht Benutzer-Home-Verzeichnisse wie `~/Library/...`), die Administratorrechte erfordern. Sie sind dazu bestimmt, von IT-Administratoren bereitgestellt zu werden.
</Note>

Die `managed-mcp.json`-Datei verwendet das gleiche Format wie eine Standard-`.mcp.json`-Datei:

```json  theme={null}
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.company.com"
      }
    }
  }
}
```

### Option 2: Richtlinienbasierte Kontrolle mit Allowlists und Denylists

Anstatt exklusive Kontrolle zu übernehmen, können Administratoren Benutzern erlauben, ihre eigenen MCP-Server zu konfigurieren, während sie Einschränkungen durchsetzen, welche Server zulässig sind. Dieser Ansatz verwendet `allowedMcpServers` und `deniedMcpServers` in der [verwalteten Einstellungsdatei](/de/settings#settings-files).

<Note>
  **Wahl zwischen Optionen**: Verwenden Sie Option 1 (`managed-mcp.json`), wenn Sie einen festen Satz von Servern ohne Benutzeranpassung bereitstellen möchten. Verwenden Sie Option 2 (Allowlists/Denylists), wenn Sie Benutzern erlauben möchten, ihre eigenen Server innerhalb von Richtlinienbeschränkungen hinzuzufügen.
</Note>

#### Einschränkungsoptionen

Jeder Eintrag in der Allowlist oder Denylist kann Server auf drei Arten einschränken:

1. **Nach Servername** (`serverName`): Entspricht dem konfigurierten Namen des Servers
2. **Nach Befehl** (`serverCommand`): Entspricht dem genauen Befehl und den Argumenten, die zum Starten von Stdio-Servern verwendet werden
3. **Nach URL-Muster** (`serverUrl`): Entspricht Remote-Server-URLs mit Wildcard-Unterstützung

**Wichtig**: Jeder Eintrag muss genau einen von `serverName`, `serverCommand` oder `serverUrl` haben.

#### Beispielkonfiguration

```json  theme={null}
{
  "allowedMcpServers": [
    // Nach Servername zulassen
    { "serverName": "github" },
    { "serverName": "sentry" },

    // Nach exaktem Befehl zulassen (für Stdio-Server)
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] },
    { "serverCommand": ["python", "/usr/local/bin/approved-server.py"] },

    // Nach URL-Muster zulassen (für Remote-Server)
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverUrl": "https://*.internal.corp/*" }
  ],
  "deniedMcpServers": [
    // Nach Servername blockieren
    { "serverName": "dangerous-server" },

    // Nach exaktem Befehl blockieren (für Stdio-Server)
    { "serverCommand": ["npx", "-y", "unapproved-package"] },

    // Nach URL-Muster blockieren (für Remote-Server)
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

#### Wie befehlsbasierte Einschränkungen funktionieren

**Exakte Übereinstimmung**:

* Befehlsarrays müssen **genau** übereinstimmen – sowohl der Befehl als auch alle Argumente in der richtigen Reihenfolge
* Beispiel: `["npx", "-y", "server"]` entspricht NICHT `["npx", "server"]` oder `["npx", "-y", "server", "--flag"]`

**Stdio-Server-Verhalten**:

* Wenn die Allowlist **irgendwelche** `serverCommand`-Einträge enthält, müssen Stdio-Server einem dieser Befehle entsprechen
* Stdio-Server können nicht allein nach Name bestehen, wenn Befehlsbeschränkungen vorhanden sind
* Dies stellt sicher, dass Administratoren erzwingen können, welche Befehle ausgeführt werden dürfen

**Verhalten von Remote-Servern**:

* Remote-Server (HTTP, SSE, WebSocket) verwenden URL-basierte Übereinstimmung, wenn `serverUrl`-Einträge in der Allowlist vorhanden sind
* Wenn keine URL-Einträge vorhanden sind, greifen Remote-Server auf namensbasierte Übereinstimmung zurück
* Befehlsbeschränkungen gelten nicht für Remote-Server

#### Wie URL-basierte Einschränkungen funktionieren

URL-Muster unterstützen Wildcards mit `*`, um eine beliebige Zeichenfolge zu entsprechen. Dies ist nützlich, um ganze Domänen oder Subdomänen zuzulassen.

**Wildcard-Beispiele**:

* `https://mcp.company.com/*` – Alle Pfade auf einer bestimmten Domäne zulassen
* `https://*.example.com/*` – Jede Subdomain von example.com zulassen
* `http://localhost:*/*` – Jeden Port auf localhost zulassen

**Verhalten von Remote-Servern**:

* Wenn die Allowlist **irgendwelche** `serverUrl`-Einträge enthält, müssen Remote-Server einem dieser URL-Muster entsprechen
* Remote-Server können nicht allein nach Name bestehen, wenn URL-Beschränkungen vorhanden sind
* Dies stellt sicher, dass Administratoren erzwingen können, welche Remote-Endpunkte zulässig sind

<Accordion title="Beispiel: Nur-URL-Allowlist">
  ```json  theme={null}
  {
    "allowedMcpServers": [
      { "serverUrl": "https://mcp.company.com/*" },
      { "serverUrl": "https://*.internal.corp/*" }
    ]
  }
  ```

  **Ergebnis**:

  * HTTP-Server unter `https://mcp.company.com/api`: ✅ Zulässig (entspricht URL-Muster)
  * HTTP-Server unter `https://api.internal.corp/mcp`: ✅ Zulässig (entspricht Wildcard-Subdomain)
  * HTTP-Server unter `https://external.com/mcp`: ❌ Blockiert (entspricht keinem URL-Muster)
  * Stdio-Server mit beliebigem Befehl: ❌ Blockiert (keine Namen- oder Befehlseinträge zum Abgleichen)
</Accordion>

<Accordion title="Beispiel: Nur-Befehl-Allowlist">
  ```json  theme={null}
  {
    "allowedMcpServers": [
      { "serverCommand": ["npx", "-y", "approved-package"] }
    ]
  }
  ```

  **Ergebnis**:

  * Stdio-Server mit `["npx", "-y", "approved-package"]`: ✅ Zulässig (entspricht Befehl)
  * Stdio-Server mit `["node", "server.js"]`: ❌ Blockiert (entspricht nicht dem Befehl)
  * HTTP-Server mit Namen „my-api": ❌ Blockiert (keine Nameneinträge zum Abgleichen)
</Accordion>

<Accordion title="Beispiel: Gemischte Namen- und Befehl-Allowlist">
  ```json  theme={null}
  {
    "allowedMcpServers": [
      { "serverName": "github" },
      { "serverCommand": ["npx", "-y", "approved-package"] }
    ]
  }
  ```

  **Ergebnis**:

  * Stdio-Server mit Namen „local-tool" und `["npx", "-y", "approved-package"]`: ✅ Zulässig (entspricht Befehl)
  * Stdio-Server mit Namen „local-tool" und `["node", "server.js"]`: ❌ Blockiert (Befehlseinträge vorhanden, aber entspricht nicht)
  * Stdio-Server mit Namen „github" und `["node", "server.js"]`: ❌ Blockiert (Stdio-Server müssen Befehlen entsprechen, wenn Befehlseinträge vorhanden sind)
  * HTTP-Server mit Namen „github": ✅ Zulässig (entspricht Name)
  * HTTP-Server mit Namen „other-api": ❌ Blockiert (Name entspricht nicht)
</Accordion>

<Accordion title="Beispiel: Nur-Namen-Allowlist">
  ```json  theme={null}
  {
    "allowedMcpServers": [
      { "serverName": "github" },
      { "serverName": "internal-tool" }
    ]
  }
  ```

  **Ergebnis**:

  * Stdio-Server mit Namen „github" und beliebigem Befehl: ✅ Zulässig (keine Befehlsbeschränkungen)
  * Stdio-Server mit Namen „internal-tool" und beliebigem Befehl: ✅ Zulässig (keine Befehlsbeschränkungen)
  * HTTP-Server mit Namen „github": ✅ Zulässig (entspricht Name)
  * Beliebiger Server mit Namen „other": ❌ Blockiert (Name entspricht nicht)
</Accordion>

#### Allowlist-Verhalten (`allowedMcpServers`)

* `undefined` (Standard): Keine Einschränkungen – Benutzer können jeden MCP-Server konfigurieren
* Leeres Array `[]`: Vollständige Sperrung – Benutzer können keinen MCP-Server konfigurieren
* Liste von Einträgen: Benutzer können nur Server konfigurieren, die nach Name, Befehl oder URL-Muster übereinstimmen

#### Denylist-Verhalten (`deniedMcpServers`)

* `undefined` (Standard): Keine Server werden blockiert
* Leeres Array `[]`: Keine Server werden blockiert
* Liste von Einträgen: Angegebene Server werden über alle Bereiche hinweg explizit blockiert

#### Wichtige Hinweise

* **Option 1 und Option 2 können kombiniert werden**: Wenn `managed-mcp.json` vorhanden ist, hat es exklusive Kontrolle und Benutzer können keine Server hinzufügen. Allowlists/Denylists gelten immer noch für die verwalteten Server selbst.
* **Denylist hat absolute Vorrang**: Wenn ein Server einem Denylist-Eintrag entspricht (nach Name, Befehl oder URL), wird er blockiert, auch wenn er auf der Allowlist ist
* Namensbasierte, befehlsbasierte und URL-basierte Einschränkungen funktionieren zusammen: Ein Server wird zugelassen, wenn er einem Namenseintrag, einem Befehlseintrag oder einem URL-Muster entspricht (es sei denn, er wird durch Denylist blockiert)

<Note>
  **Bei Verwendung von `managed-mcp.json`**: Benutzer können MCP-Server nicht über `claude mcp add` oder Konfigurationsdateien hinzufügen. Die Einstellungen `allowedMcpServers` und `deniedMcpServers` gelten immer noch, um zu filtern, welche verwalteten Server tatsächlich geladen werden.
</Note>
