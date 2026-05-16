> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code mit Tools über MCP verbinden

> Erfahren Sie, wie Sie Claude Code mit Ihren Tools über das Model Context Protocol verbinden.

Claude Code kann sich über das [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), einen offenen Standard für KI-Tool-Integrationen, mit Hunderten von externen Tools und Datenquellen verbinden. MCP-Server geben Claude Code Zugriff auf Ihre Tools, Datenbanken und APIs.

Verbinden Sie einen Server, wenn Sie feststellen, dass Sie Daten aus einem anderen Tool wie einem Issue-Tracker oder einem Überwachungs-Dashboard in den Chat kopieren. Nach der Verbindung kann Claude direkt auf dieses System zugreifen und handeln, anstatt mit dem zu arbeiten, was Sie einfügen.

## Was Sie mit MCP tun können

Mit verbundenen MCP-Servern können Sie Claude Code auffordern:

* **Funktionen aus Issue-Trackern implementieren**: „Füge die in JIRA-Issue ENG-4521 beschriebene Funktion hinzu und erstelle einen PR auf GitHub."
* **Überwachungsdaten analysieren**: „Überprüfe Sentry und Statsig, um die Nutzung der in ENG-4521 beschriebenen Funktion zu überprüfen."
* **Datenbanken abfragen**: „Finde E-Mail-Adressen von 10 zufälligen Benutzern, die die Funktion ENG-4521 verwendet haben, basierend auf unserer PostgreSQL-Datenbank."
* **Designs integrieren**: „Aktualisiere unsere Standard-E-Mail-Vorlage basierend auf den neuen Figma-Designs, die in Slack gepostet wurden"
* **Workflows automatisieren**: „Erstelle Gmail-Entwürfe, die diese 10 Benutzer zu einer Feedback-Sitzung zur neuen Funktion einladen."
* **Auf externe Ereignisse reagieren**: Ein MCP-Server kann auch als [Kanal](/de/channels) fungieren, der Nachrichten in Ihre Sitzung pusht, sodass Claude auf Telegram-Nachrichten, Discord-Chats oder Webhook-Ereignisse reagiert, während Sie weg sind.

## MCP-Server finden und erstellen

Durchsuchen Sie überprüfte Konnektoren im [Anthropic Directory](https://claude.ai/directory). Directory-Konnektoren verwenden die gleiche MCP-Infrastruktur wie Claude Code, sodass Sie jeden dort aufgelisteten Remote-Server mit `claude mcp add` hinzufügen können.

<Warning>
  Überprüfen Sie, dass Sie jedem Server vertrauen, bevor Sie ihn verbinden. Server, die externe Inhalte abrufen, können Sie dem [Risiko von Prompt-Injection aussetzen](/de/security#protect-against-prompt-injection).
</Warning>

Um Ihren eigenen Server zu erstellen, lesen Sie das [MCP-Server-Handbuch](https://modelcontextprotocol.io/docs/develop/build-server) für Protokoll-Grundlagen und die [Claude-Konnektoren-Dokumentation zum Erstellen](https://claude.com/docs/connectors/building) für Authentifizierung, Tests und Directory-Einreichung.

Sie können Claude auch einen Server für Sie mit dem offiziellen [`mcp-server-dev` Plugin](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/mcp-server-dev) erstellen lassen.

<Steps>
  <Step title="Installieren Sie das Plugin">
    Führen Sie in einer Claude Code-Sitzung Folgendes aus:

    ```
    /plugin install mcp-server-dev@claude-plugins-official
    ```

    Führen Sie dann `/reload-plugins` aus, um es in der aktuellen Sitzung zu aktivieren.
  </Step>

  <Step title="Führen Sie die Build-Skill aus">
    ```
    /mcp-server-dev:build-mcp-server
    ```

    Claude fragt nach Ihrem Anwendungsfall und erstellt einen Remote-HTTP- oder lokalen Stdio-Server.
  </Step>
</Steps>

## MCP-Server installieren

MCP-Server können je nach Ihren Anforderungen auf drei verschiedene Arten konfiguriert werden:

### Option 1: Einen Remote-HTTP-Server hinzufügen

HTTP-Server sind die empfohlene Option für die Verbindung mit Remote-MCP-Servern. Dies ist das am weitesten unterstützte Transportprotokoll für Cloud-basierte Dienste.

```bash theme={null}
# Grundlegende Syntax
claude mcp add --transport http <name> <url>

# Echtes Beispiel: Mit Notion verbinden
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Beispiel mit Bearer-Token
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

Bei der Konfiguration von MCP-Servern über JSON in `.mcp.json`, `~/.claude.json` oder `claude mcp add-json` akzeptiert das Feld `type` `streamable-http` als Alias für `http`. Die MCP-Spezifikation verwendet den Namen `streamable-http` für dieses Transportprotokoll, sodass Konfigurationen, die aus der Server-Dokumentation kopiert werden, ohne Änderungen funktionieren.

### Option 2: Einen Remote-SSE-Server hinzufügen

<Warning>
  Das SSE-Transportprotokoll (Server-Sent Events) ist veraltet. Verwenden Sie stattdessen HTTP-Server, wo verfügbar.
</Warning>

```bash theme={null}
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

Claude Code setzt `CLAUDE_PROJECT_DIR` in der Umgebung des erzeugten Servers auf das Projektstammverzeichnis, sodass Ihr Server projektrelative Pfade auflösen kann, ohne vom Arbeitsverzeichnis abhängig zu sein. Dies ist das gleiche Verzeichnis, das Hooks in ihrer `CLAUDE_PROJECT_DIR`-Variable erhalten. Lesen Sie es aus Ihrem Serverprozess, zum Beispiel `process.env.CLAUDE_PROJECT_DIR` in Node oder `os.environ["CLAUDE_PROJECT_DIR"]` in Python. Ihr Server kann auch die MCP-Anfrage `roots/list` aufrufen, die das Verzeichnis zurückgibt, aus dem Claude Code gestartet wurde.

Diese Variable wird in der Umgebung des Servers gesetzt, nicht in der Umgebung von Claude Code selbst, daher erfordert das Referenzieren über `${VAR}`-Erweiterung in einer projekt- oder benutzergesteuerten `.mcp.json` `command` oder `args` einen Standard wie `${CLAUDE_PROJECT_DIR:-.}`. Von Plugins bereitgestellte MCP-Konfigurationen ersetzen `${CLAUDE_PROJECT_DIR}` direkt und benötigen keinen Standard.

```bash theme={null}
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

```bash theme={null}
# Alle konfigurierten Server auflisten
claude mcp list

# Details für einen bestimmten Server abrufen
claude mcp get github

# Einen Server entfernen
claude mcp remove github

# (innerhalb von Claude Code) Serverstatus überprüfen
/mcp
```

Das `/mcp`-Panel zeigt die Tool-Anzahl neben jedem verbundenen Server an und kennzeichnet Server, die die Tools-Funktion ankündigen, aber keine Tools bereitstellen.

Der Servername `workspace` ist für interne Verwendung reserviert. Wenn Ihre Konfiguration einen Server mit diesem Namen definiert, überspringt Claude Code ihn beim Laden und zeigt eine Warnung an, die Sie auffordert, ihn umzubenennen.

### Dynamische Tool-Updates

Claude Code unterstützt MCP-`list_changed`-Benachrichtigungen, die es MCP-Servern ermöglichen, ihre verfügbaren Tools, Prompts und Ressourcen dynamisch zu aktualisieren, ohne dass Sie die Verbindung trennen und erneut verbinden müssen. Wenn ein MCP-Server eine `list_changed`-Benachrichtigung sendet, aktualisiert Claude Code automatisch die verfügbaren Funktionen von diesem Server.

### Automatische Wiederverbindung

Wenn ein HTTP- oder SSE-Server während einer Sitzung die Verbindung trennt, verbindet sich Claude Code automatisch mit exponentiellem Backoff wieder: bis zu fünf Versuche, beginnend mit einer Verzögerung von einer Sekunde und sich jedes Mal verdoppelnd. Der Server wird als ausstehend in `/mcp` angezeigt, während die Wiederverbindung läuft. Nach fünf fehlgeschlagenen Versuchen wird der Server als fehlgeschlagen markiert und Sie können ihn manuell von `/mcp` aus erneut versuchen. Stdio-Server sind lokale Prozesse und werden nicht automatisch wiederverbunden.

Das gleiche Backoff gilt, wenn ein HTTP- oder SSE-Server beim Start seine anfängliche Verbindung nicht herstellt. Ab v2.1.121 versucht Claude Code die anfängliche Verbindung bis zu dreimal bei vorübergehenden Fehlern wie einer 5xx-Antwort, einer Verbindungsverweigerung oder einem Timeout erneut, markiert den Server dann als fehlgeschlagen, wenn er immer noch keine Verbindung herstellen kann. Authentifizierungs- und Not-Found-Fehler werden nicht erneut versucht, da sie eine Konfigurationsänderung erfordern, um behoben zu werden.

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

### Von Plugins bereitgestellte MCP-Server

[Plugins](/de/plugins) können MCP-Server bündeln und automatisch Tools und Integrationen bereitstellen, wenn das Plugin aktiviert ist. Plugin-MCP-Server funktionieren identisch mit benutzerkonfigurierten Servern.

**Wie Plugin-MCP-Server funktionieren**:

* Plugins definieren MCP-Server in `.mcp.json` im Plugin-Root oder inline in `plugin.json`
* Wenn ein Plugin aktiviert ist, starten seine MCP-Server automatisch
* Plugin-MCP-Tools erscheinen neben manuell konfigurierten MCP-Tools
* Plugin-Server werden durch die Plugin-Installation verwaltet (nicht durch `/mcp`-Befehle)

**Beispiel-Plugin-MCP-Konfiguration**:

In `.mcp.json` im Plugin-Root:

```json theme={null}
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

```json theme={null}
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
* **Umgebungsvariablen**: Verwenden Sie `${CLAUDE_PLUGIN_ROOT}` für gebündelte Plugin-Dateien, `${CLAUDE_PLUGIN_DATA}` für [persistente Daten](/de/plugins-reference#persistent-data-directory), die Plugin-Updates überstehen, und `${CLAUDE_PROJECT_DIR}` für das stabile Projektstammverzeichnis
* **Zugriff auf Benutzerumgebung**: Zugriff auf die gleichen Umgebungsvariablen wie manuell konfigurierte Server
* **Mehrere Transporttypen**: Unterstützung für Stdio-, SSE- und HTTP-Transporte (die Transportunterstützung kann je nach Server variieren)

**Anzeigen von Plugin-MCP-Servern**:

```bash theme={null}
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

MCP-Server können auf drei verschiedenen Bereichsebenen konfiguriert werden. Der Bereich, den Sie wählen, steuert, in welchen Projekten der Server geladen wird und ob die Konfiguration mit Ihrem Team geteilt wird. Administratoren können Server auch auf Unternehmensebene über [verwaltete Konfiguration](#managed-mcp-configuration) bereitstellen.

| Bereich                   | Wird geladen in       | Mit Team geteilt           | Gespeichert in              |
| ------------------------- | --------------------- | -------------------------- | --------------------------- |
| [Lokal](#local-scope)     | Nur aktuelles Projekt | Nein                       | `~/.claude.json`            |
| [Projekt](#project-scope) | Nur aktuelles Projekt | Ja, über Versionskontrolle | `.mcp.json` im Projekt-Root |
| [Benutzer](#user-scope)   | Alle Ihre Projekte    | Nein                       | `~/.claude.json`            |

### Lokaler Bereich

Der lokale Bereich ist der Standard. Ein lokal begrenzter Server wird nur in dem Projekt geladen, in dem Sie ihn hinzugefügt haben, und bleibt privat für Sie. Claude Code speichert ihn in `~/.claude.json` unter dem Pfad dieses Projekts, daher wird derselbe Server nicht in Ihren anderen Projekten angezeigt. Verwenden Sie den lokalen Bereich für persönliche Entwicklungsserver, experimentelle Konfigurationen oder Server mit Anmeldedaten, die Sie nicht in der Versionskontrolle haben möchten.

<Note>
  Der Begriff „lokaler Bereich" für MCP-Server unterscheidet sich von allgemeinen lokalen Einstellungen. Lokal begrenzte MCP-Server werden in `~/.claude.json` (Ihr Home-Verzeichnis) gespeichert, während allgemeine lokale Einstellungen `.claude/settings.local.json` (im Projektverzeichnis) verwenden. Siehe [Einstellungen](/de/settings#settings-files) für Details zu Einstellungsdatei-Speicherorten.
</Note>

```bash theme={null}
# Einen lokal begrenzten Server hinzufügen (Standard)
claude mcp add --transport http stripe https://mcp.stripe.com

# Lokalen Bereich explizit angeben
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

Der Befehl schreibt den Server in den Eintrag für Ihr aktuelles Projekt in `~/.claude.json`. Das folgende Beispiel zeigt das Ergebnis, wenn Sie ihn von `/path/to/your/project` aus ausführen:

```json theme={null}
{
  "projects": {
    "/path/to/your/project": {
      "mcpServers": {
        "stripe": {
          "type": "http",
          "url": "https://mcp.stripe.com"
        }
      }
    }
  }
}
```

### Projektbereich

Projektbegrenzte Server ermöglichen Teamzusammenarbeit durch das Speichern von Konfigurationen in einer `.mcp.json`-Datei im Root-Verzeichnis Ihres Projekts. Diese Datei ist dazu bestimmt, in die Versionskontrolle eingecheckt zu werden, um sicherzustellen, dass alle Teammitglieder Zugriff auf die gleichen MCP-Tools und -Dienste haben. Wenn Sie einen projektbegrenzten Server hinzufügen, erstellt oder aktualisiert Claude Code automatisch diese Datei mit der entsprechenden Konfigurationsstruktur.

```bash theme={null}
# Einen projektbegrenzten Server hinzufügen
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

Die resultierende `.mcp.json`-Datei folgt einem standardisierten Format:

```json theme={null}
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

```bash theme={null}
# Einen Benutzer-Server hinzufügen
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### Bereichshierarchie und Vorrang

Wenn derselbe Server auf mehreren Bereichen definiert ist, verbindet sich Claude Code einmal damit und verwendet die Definition aus der höchsten Vorrangsquelle:

1. Lokaler Bereich
2. Projektbereich
3. Benutzerbereich
4. [Von Plugins bereitgestellte Server](/de/plugins)
5. [Claude.ai-Connectoren](#use-mcp-servers-from-claude-ai)

Die drei Bereiche stimmen Duplikate nach Name ab. Plugins und Connectoren stimmen nach Endpunkt ab, daher wird einer, der auf die gleiche URL oder den gleichen Befehl wie ein Server oben verweist, als Duplikat behandelt.

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

```json theme={null}
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

```bash theme={null}
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

Authentifizieren Sie sich mit Ihrem Sentry-Konto:

```text theme={null}
/mcp
```

Debuggen Sie dann Produktionsprobleme:

```text theme={null}
What are the most common errors in the last 24 hours?
```

```text theme={null}
Show me the stack trace for error ID abc123
```

```text theme={null}
Which deployment introduced these new errors?
```

### Beispiel: Mit GitHub für Code-Reviews verbinden

GitHubs Remote-MCP-Server authentifiziert sich mit einem GitHub-Personal-Access-Token, der als Header übergeben wird. Um einen zu erhalten, öffnen Sie Ihre [GitHub-Token-Einstellungen](https://github.com/settings/personal-access-tokens), generieren Sie ein neues feingranulares Token mit Zugriff auf die Repositories, mit denen Claude arbeiten soll, und fügen Sie dann den Server hinzu:

```bash theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

Arbeiten Sie dann mit GitHub:

```text theme={null}
Review PR #456 and suggest improvements
```

```text theme={null}
Create a new issue for the bug we just found
```

```text theme={null}
Show me all open PRs assigned to me
```

### Beispiel: Ihre PostgreSQL-Datenbank abfragen

```bash theme={null}
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"
```

Fragen Sie dann Ihre Datenbank natürlich ab:

```text theme={null}
What's our total revenue this month?
```

```text theme={null}
Show me the schema for the orders table
```

```text theme={null}
Find customers who haven't made a purchase in 90 days
```

## Mit Remote-MCP-Servern authentifizieren

Viele Cloud-basierte MCP-Server erfordern Authentifizierung. Claude Code unterstützt OAuth 2.0 für sichere Verbindungen.

Claude Code markiert einen Remote-Server als authentifizierungsbedürftig, wenn der Server mit `401 Unauthorized` oder `403 Forbidden` antwortet. Jeder dieser Statuscodes kennzeichnet den Server in `/mcp`, damit Sie den OAuth-Fluss abschließen können. Ein benutzerdefinierter Server, der einen `WWW-Authenticate`-Header zurückgibt, der auf seinen Autorisierungsserver verweist, erhält die gleiche automatische Erkennung wie jeder andere Remote-Server.

<Steps>
  <Step title="Fügen Sie den Server hinzu, der Authentifizierung erfordert">
    Zum Beispiel:

    ```bash theme={null}
    claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
    ```
  </Step>

  <Step title="Verwenden Sie den /mcp-Befehl innerhalb von Claude Code">
    In Claude Code verwenden Sie den Befehl:

    ```text theme={null}
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

```bash theme={null}
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

        ```bash theme={null}
        claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>

      <Tab title="claude mcp add-json">
        Fügen Sie das Objekt `oauth` in die JSON-Konfiguration ein und übergeben Sie `--client-secret` als separates Flag:

        ```bash theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' \
          --client-secret
        ```
      </Tab>

      <Tab title="claude mcp add-json (nur Callback-Port)">
        Verwenden Sie `--callback-port` ohne Client-ID, um den Port zu fixieren und gleichzeitig die dynamische Client-Registrierung zu verwenden:

        ```bash theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"callbackPort":8080}}'
        ```
      </Tab>

      <Tab title="CI / Umgebungsvariable">
        Legen Sie das Secret über eine Umgebungsvariable fest, um die interaktive Eingabeaufforderung zu überspringen:

        ```bash theme={null}
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

Verweisen Sie Claude Code auf eine spezifische OAuth-Autorisierungsserver-Metadaten-URL, um die Standard-Erkennungskette zu umgehen. Legen Sie `authServerMetadataUrl` fest, wenn die Standard-Endpunkte des MCP-Servers Fehler zurückgeben, oder wenn Sie die Erkennung durch einen internen Proxy leiten möchten. Standardmäßig überprüft Claude Code zunächst RFC 9728 Protected Resource Metadata unter `/.well-known/oauth-protected-resource` und fällt dann auf RFC 8414 Authorization Server Metadata unter `/.well-known/oauth-authorization-server` zurück.

Legen Sie `authServerMetadataUrl` im Objekt `oauth` der Konfiguration Ihres Servers in `.mcp.json` fest:

```json theme={null}
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

Die URL muss `https://` verwenden. `authServerMetadataUrl` erfordert Claude Code v2.1.64 oder später. Die `scopes_supported` der Metadaten-URL überschreiben die Bereiche, die der Upstream-Server bewirbt.

### Beschränken Sie OAuth-Bereiche

Legen Sie `oauth.scopes` fest, um die Bereiche zu fixieren, die Claude Code während des Autorisierungsflusses anfordert. Dies ist die unterstützte Methode, um einen MCP-Server auf eine von Ihrem Sicherheitsteam genehmigte Teilmenge zu beschränken, wenn der Upstream-Autorisierungsserver mehr Bereiche bewirbt, als Sie gewähren möchten. Der Wert ist eine einzelne durch Leerzeichen getrennte Zeichenkette, die dem `scope`-Parameter-Format in RFC 6749 §3.3 entspricht.

```json theme={null}
{
  "mcpServers": {
    "slack": {
      "type": "http",
      "url": "https://mcp.slack.com/mcp",
      "oauth": {
        "scopes": "channels:read chat:write search:read"
      }
    }
  }
}
```

`oauth.scopes` hat Vorrang vor sowohl `authServerMetadataUrl` als auch den Bereichen, die der Server unter `/.well-known` entdeckt. Lassen Sie es ungesetzt, damit der MCP-Server den angeforderten Bereichssatz bestimmt.

Wenn der Autorisierungsserver `offline_access` in `scopes_supported` bewirbt, fügt Claude Code es zu den fixierten Bereichen hinzu, damit das Zugriffs-Token ohne neue Browser-Anmeldung aktualisiert werden kann.

Wenn der Server später einen 403 `insufficient_scope` für einen Tool-Aufruf zurückgibt, authentifiziert sich Claude Code mit den gleichen fixierten Bereichen erneut. Erweitern Sie `oauth.scopes`, wenn ein Tool, das Sie benötigen, einen Bereich außerhalb der Fixierung erfordert.

### Verwenden Sie dynamische Header für benutzerdefinierte Authentifizierung

Wenn Ihr MCP-Server ein anderes Authentifizierungsschema verwendet als OAuth (wie Kerberos, kurzlebige Token oder ein internes SSO), verwenden Sie `headersHelper`, um Request-Header zur Verbindungszeit zu generieren. Claude Code führt den Befehl aus und fügt seine Ausgabe in die Verbindungs-Header ein.

```json theme={null}
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

```json theme={null}
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
    ```bash theme={null}
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
    ```bash theme={null}
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
    ```bash theme={null}
    # Grundlegende Syntax 
    claude mcp add-from-claude-desktop 
    ```
  </Step>

  <Step title="Wählen Sie aus, welche Server importiert werden sollen">
    Nach dem Ausführen des Befehls wird ein interaktives Dialogfeld angezeigt, in dem Sie auswählen können, welche Server Sie importieren möchten.
  </Step>

  <Step title="Überprüfen Sie, dass die Server importiert wurden">
    ```bash theme={null}
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
    Fügen Sie Server unter [claude.ai/customize/connectors](https://claude.ai/customize/connectors) hinzu. Bei Team- und Enterprise-Plänen können nur Administratoren Server hinzufügen.
  </Step>

  <Step title="Authentifizieren Sie den MCP-Server">
    Führen Sie alle erforderlichen Authentifizierungsschritte in Claude.ai durch.
  </Step>

  <Step title="Zeigen Sie Server in Claude Code an und verwalten Sie sie">
    In Claude Code verwenden Sie den Befehl:

    ```text theme={null}
    /mcp
    ```

    Claude.ai-Server erscheinen in der Liste mit Indikatoren, die zeigen, dass sie von Claude.ai stammen.
  </Step>
</Steps>

Ein Server, den Sie in Claude Code hinzugefügt haben, hat [Vorrang](#scope-hierarchy-and-precedence) vor einem Claude.ai-Connector, der auf dieselbe URL verweist. Wenn dies geschieht, listet `/mcp` den Connector als verborgen auf und zeigt, wie Sie das Duplikat entfernen können, wenn Sie lieber den Connector verwenden möchten.

Um Claude.ai-MCP-Server in Claude Code zu deaktivieren, setzen Sie die Umgebungsvariable `ENABLE_CLAUDEAI_MCP_SERVERS` auf `false`:

```bash theme={null}
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

## Claude Code als MCP-Server verwenden

Sie können Claude Code selbst als MCP-Server verwenden, mit dem sich andere Anwendungen verbinden können:

```bash theme={null}
# Starten Sie Claude als Stdio-MCP-Server
claude mcp serve
```

Sie können dies in Claude Desktop verwenden, indem Sie diese Konfiguration zu claude\_desktop\_config.json hinzufügen:

```json theme={null}
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

  ```bash theme={null}
  which claude
  ```

  Verwenden Sie dann den vollständigen Pfad in Ihrer Konfiguration:

  ```json theme={null}
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
* **Bereich**: Die Umgebungsvariable gilt für Tools, die kein eigenes Limit deklarieren. Tools, die [`anthropic/maxResultSizeChars`](#raise-the-limit-for-a-specific-tool) setzen, verwenden diesen Wert stattdessen für Textinhalte, unabhängig davon, auf was `MAX_MCP_OUTPUT_TOKENS` gesetzt ist. Tools, die Bilddaten zurückgeben, unterliegen immer noch `MAX_MCP_OUTPUT_TOKENS`

Um das Limit für Tools zu erhöhen, die große Ausgaben erzeugen:

```bash theme={null}
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

Dies ist besonders nützlich bei der Arbeit mit MCP-Servern, die:

* Große Datensätze oder Datenbanken abfragen
* Detaillierte Berichte oder Dokumentation generieren
* Umfangreiche Protokolldateien oder Debugging-Informationen verarbeiten

### Erhöhen Sie das Limit für ein bestimmtes Tool

Wenn Sie einen MCP-Server erstellen, können Sie einzelnen Tools ermöglichen, Ergebnisse größer als die Standard-Persist-to-Disk-Schwelle zurückzugeben, indem Sie `_meta["anthropic/maxResultSizeChars"]` in der Tool-Antwort des `tools/list` einstellen. Claude Code erhöht die Schwelle dieses Tools auf den annotierten Wert, bis zu einer harten Obergrenze von 500.000 Zeichen.

Dies ist nützlich für Tools, die inhärent große, aber notwendige Ausgaben zurückgeben, wie Datenbankschemas oder vollständige Dateibäume. Ohne die Anmerkung werden Ergebnisse, die die Standard-Schwelle überschreiten, auf die Festplatte persistiert und durch eine Dateireferenz im Gespräch ersetzt.

```json theme={null}
{
  "name": "get_schema",
  "description": "Returns the full database schema",
  "_meta": {
    "anthropic/maxResultSizeChars": 200000
  }
}
```

Die Anmerkung gilt unabhängig von `MAX_MCP_OUTPUT_TOKENS` für Textinhalte, daher müssen Benutzer die Umgebungsvariable nicht für Tools erhöhen, die sie deklarieren. Tools, die Bilddaten zurückgeben, unterliegen immer noch dem Token-Limit.

<Warning>
  Wenn Sie häufig Ausgabewarnungen bei bestimmten MCP-Servern erhalten, die Sie nicht kontrollieren, erwägen Sie, das Limit `MAX_MCP_OUTPUT_TOKENS` zu erhöhen. Sie können auch den Server-Autor bitten, die Anmerkung `anthropic/maxResultSizeChars` hinzuzufügen oder ihre Antworten zu paginieren. Die Anmerkung hat keine Auswirkung auf Tools, die Bildinhalte zurückgeben; für diese ist das Erhöhen von `MAX_MCP_OUTPUT_TOKENS` die einzige Option.
</Warning>

## Reagieren Sie auf MCP-Elicitierungsanfragen

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

    ```text theme={null}
    Can you analyze @github:issue://123 and suggest a fix?
    ```

    ```text theme={null}
    Please review the API documentation at @docs:file://api/authentication
    ```
  </Step>

  <Step title="Mehrere Ressourcenreferenzen">
    Sie können mehrere Ressourcen in einer einzelnen Eingabeaufforderung referenzieren:

    ```text theme={null}
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

### Tool-Suche konfigurieren

Die Tool-Suche ist standardmäßig aktiviert: MCP-Tools werden aufgeschoben und bei Bedarf entdeckt. Claude Code deaktiviert sie standardmäßig auf Vertex AI. Sie ist auch deaktiviert, wenn `ANTHROPIC_BASE_URL` auf einen Host von Drittanbietern verweist, da die meisten Proxys `tool_reference`-Blöcke nicht weiterleiten. Setzen Sie `ENABLE_TOOL_SEARCH` explizit fest, um eine der beiden Fallback-Einstellungen zu überschreiben.

Die Tool-Suche erfordert ein Modell, das `tool_reference`-Blöcke unterstützt: Sonnet 4 und später oder Opus 4 und später. Haiku-Modelle unterstützen dies nicht. Auf Vertex AI wird die Tool-Suche für Claude Sonnet 4.5 und später sowie Claude Opus 4.5 und später unterstützt.

Steuern Sie das Verhalten der Tool-Suche mit der Umgebungsvariablen `ENABLE_TOOL_SEARCH`:

| Wert            | Verhalten                                                                                                                                                                                                                                                    |
| :-------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| (nicht gesetzt) | Alle MCP-Tools werden aufgeschoben und bei Bedarf geladen. Fällt auf das Laden vorab zurück auf Vertex AI oder wenn `ANTHROPIC_BASE_URL` ein Host von Drittanbietern ist                                                                                     |
| `true`          | Alle MCP-Tools werden aufgeschoben. Claude Code sendet den Beta-Header auch auf Vertex AI und durch Proxys. Anfragen schlagen fehl bei Vertex AI-Modellen älter als Sonnet 4.5 oder Opus 4.5 oder bei Proxys, die `tool_reference`-Blöcke nicht unterstützen |
| `auto`          | Schwellenmodus: Tools werden vorab geladen, wenn sie in 10 % des Kontextfensters passen, andernfalls aufgeschoben                                                                                                                                            |
| `auto:N`        | Schwellenmodus mit benutzerdefiniertem Prozentsatz, wobei `N` 0-100 ist. Beispiel: `auto:5` für 5 %                                                                                                                                                          |
| `false`         | Alle MCP-Tools werden vorab geladen, keine Verschiebung                                                                                                                                                                                                      |

```bash theme={null}
# Verwenden Sie eine benutzerdefinierte 5%-Schwelle
ENABLE_TOOL_SEARCH=auto:5 claude

# Deaktivieren Sie die Tool-Suche vollständig
ENABLE_TOOL_SEARCH=false claude
```

Oder legen Sie den Wert im Feld `env` Ihrer [settings.json](/de/settings#available-settings) fest.

Sie können das `ToolSearch`-Tool auch spezifisch deaktivieren:

```json theme={null}
{
  "permissions": {
    "deny": ["ToolSearch"]
  }
}
```

### Einen Server von der Verschiebung ausnehmen

Wenn die Tools eines Servers für Claude immer sichtbar sein sollten, ohne einen Suchschritt durchzuführen, setzen Sie `alwaysLoad` in der Konfiguration dieses Servers auf `true`. Jedes Tool von diesem Server wird dann beim Sitzungsstart in den Kontext geladen, unabhängig von der Einstellung `ENABLE_TOOL_SEARCH`. Verwenden Sie dies für eine kleine Anzahl von Tools, die Claude bei jedem Durchgang benötigt, da jedes vorab geladene Tool Kontext verbraucht, der sonst für Ihr Gespräch verfügbar wäre.

Der folgende `.mcp.json`-Eintrag nimmt einen HTTP-Server von der Verschiebung aus, während andere Server aufgeschoben bleiben:

```json theme={null}
{
  "mcpServers": {
    "core-tools": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "alwaysLoad": true
    }
  }
}
```

Das Feld `alwaysLoad` ist auf allen Server-Typen verfügbar und erfordert Claude Code v2.1.121 oder später. Ein MCP-Server kann auch einzelne Tools als immer geladen markieren, indem `"anthropic/alwaysLoad": true` im `_meta`-Objekt des Tools enthalten ist, was denselben Effekt nur für dieses Tool hat.

Das Setzen von `alwaysLoad: true` blockiert auch den Start, bis sich der Server verbindet, begrenzt auf das Standard-Verbindungs-Timeout von 5 Sekunden. Dies gilt auch, wenn [`MCP_CONNECTION_NONBLOCKING=1`](/de/env-vars) gesetzt ist, da die Tools vorhanden sein müssen, wenn der erste Prompt erstellt wird. Andere Server verbinden sich weiterhin im Hintergrund, wenn Nonblocking aktiviert ist.

## MCP-Prompts als Befehle verwenden

MCP-Server können Prompts verfügbar machen, die in Claude Code als Befehle verfügbar werden.

### Führen Sie MCP-Prompts aus

<Steps>
  <Step title="Entdecken Sie verfügbare Prompts">
    Geben Sie `/` ein, um alle verfügbaren Befehle anzuzeigen, einschließlich derer von MCP-Servern. MCP-Prompts erscheinen mit dem Format `/mcp__servername__promptname`.
  </Step>

  <Step title="Führen Sie einen Prompt ohne Argumente aus">
    ```text theme={null}
    /mcp__github__list_prs
    ```
  </Step>

  <Step title="Führen Sie einen Prompt mit Argumenten aus">
    Viele Prompts akzeptieren Argumente. Übergeben Sie sie durch Leerzeichen getrennt nach dem Befehl:

    ```text theme={null}
    /mcp__github__pr_review 456
    ```

    ```text theme={null}
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

```json theme={null}
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

```json theme={null}
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

Hostname-Abgleich ist case-insensitiv und ignoriert einen nachgestellten FQDN-Punkt, was DNS-Semantik entspricht. Ein Muster wie `*://Mcp.Example.com/*` entspricht `https://mcp.example.com/api`, und `https://mcp.example.com.` wird genauso behandelt wie `https://mcp.example.com`. Schemata und Pfade bleiben case-sensitiv.

**Verhalten von Remote-Servern**:

* Wenn die Allowlist **irgendwelche** `serverUrl`-Einträge enthält, müssen Remote-Server einem dieser URL-Muster entsprechen
* Remote-Server können nicht allein nach Name bestehen, wenn URL-Beschränkungen vorhanden sind
* Dies stellt sicher, dass Administratoren erzwingen können, welche Remote-Endpunkte zulässig sind

<Accordion title="Beispiel: Nur-URL-Allowlist">
  ```json theme={null}
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
  ```json theme={null}
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
  ```json theme={null}
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
  ```json theme={null}
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
