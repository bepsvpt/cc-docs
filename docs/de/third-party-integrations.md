> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Übersicht zur Enterprise-Bereitstellung

> Erfahren Sie, wie Claude Code mit verschiedenen Drittanbieter-Services und Infrastrukturen integriert werden kann, um Enterprise-Bereitstellungsanforderungen zu erfüllen.

Diese Seite bietet einen Überblick über verfügbare Bereitstellungsoptionen und hilft Ihnen, die richtige Konfiguration für Ihre Organisation zu wählen.

## Anbietervergleich

<table>
  <thead>
    <tr>
      <th>Funktion</th>
      <th>Anthropic</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Regionen</td>
      <td>Unterstützte [Länder](https://www.anthropic.com/supported-countries)</td>
      <td>Mehrere AWS [Regionen](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)</td>
      <td>Mehrere GCP [Regionen](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)</td>
      <td>Mehrere Azure [Regionen](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)</td>
    </tr>

    <tr>
      <td>Prompt-Caching</td>
      <td>Standardmäßig aktiviert</td>
      <td>Standardmäßig aktiviert</td>
      <td>Standardmäßig aktiviert</td>
      <td>Standardmäßig aktiviert</td>
    </tr>

    <tr>
      <td>Authentifizierung</td>
      <td>API-Schlüssel</td>
      <td>API-Schlüssel oder AWS-Anmeldedaten</td>
      <td>GCP-Anmeldedaten</td>
      <td>API-Schlüssel oder Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>Kostenverfolgung</td>
      <td>Dashboard</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
      <td>Azure Cost Management</td>
    </tr>

    <tr>
      <td>Enterprise-Funktionen</td>
      <td>Teams, Nutzungsüberwachung</td>
      <td>IAM-Richtlinien, CloudTrail</td>
      <td>IAM-Rollen, Cloud Audit Logs</td>
      <td>RBAC-Richtlinien, Azure Monitor</td>
    </tr>
  </tbody>
</table>

## Cloud-Anbieter

<CardGroup cols={3}>
  <Card title="Amazon Bedrock" icon="aws" href="/de/amazon-bedrock">
    Nutzen Sie Claude-Modelle über AWS-Infrastruktur mit API-Schlüssel- oder IAM-basierter Authentifizierung und AWS-nativer Überwachung
  </Card>

  <Card title="Google Vertex AI" icon="google" href="/de/google-vertex-ai">
    Greifen Sie auf Claude-Modelle über Google Cloud Platform mit Enterprise-Sicherheit und Compliance zu
  </Card>

  <Card title="Microsoft Foundry" icon="microsoft" href="/de/microsoft-foundry">
    Greifen Sie auf Claude über Azure mit API-Schlüssel- oder Microsoft Entra ID-Authentifizierung und Azure-Abrechnung zu
  </Card>
</CardGroup>

## Unternehmensinfrastruktur

<CardGroup cols={2}>
  <Card title="Enterprise Network" icon="shield" href="/de/network-config">
    Konfigurieren Sie Claude Code für die Zusammenarbeit mit den Proxy-Servern und SSL/TLS-Anforderungen Ihrer Organisation
  </Card>

  <Card title="LLM Gateway" icon="server" href="/de/llm-gateway">
    Stellen Sie zentralisierten Modellzugriff mit Nutzungsverfolgung, Budgetierung und Audit-Protokollierung bereit
  </Card>
</CardGroup>

## Konfigurationsübersicht

Claude Code unterstützt flexible Konfigurationsoptionen, mit denen Sie verschiedene Anbieter und Infrastrukturen kombinieren können:

<Note>
  Verstehen Sie den Unterschied zwischen:

  * **Unternehmens-Proxy**: Ein HTTP/HTTPS-Proxy für die Weiterleitung von Datenverkehr (festgelegt über `HTTPS_PROXY` oder `HTTP_PROXY`)
  * **LLM Gateway**: Ein Service, der die Authentifizierung verwaltet und anbieterkompatible Endpunkte bereitstellt (festgelegt über `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL` oder `ANTHROPIC_VERTEX_BASE_URL`)

  Beide Konfigurationen können zusammen verwendet werden.
</Note>

### Bedrock mit Unternehmens-Proxy verwenden

Leiten Sie Bedrock-Datenverkehr über einen Unternehmens-HTTP/HTTPS-Proxy weiter:

```bash  theme={null}
# Bedrock aktivieren
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

# Unternehmens-Proxy konfigurieren
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Bedrock mit LLM Gateway verwenden

Verwenden Sie einen Gateway-Service, der Bedrock-kompatible Endpunkte bereitstellt:

```bash  theme={null}
# Bedrock aktivieren
export CLAUDE_CODE_USE_BEDROCK=1

# LLM Gateway konfigurieren
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # Falls Gateway AWS-Authentifizierung verwaltet
```

### Foundry mit Unternehmens-Proxy verwenden

Leiten Sie Azure-Datenverkehr über einen Unternehmens-HTTP/HTTPS-Proxy weiter:

```bash  theme={null}
# Microsoft Foundry aktivieren
export CLAUDE_CODE_USE_FOUNDRY=1
export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # Oder weglassen für Entra ID-Authentifizierung

# Unternehmens-Proxy konfigurieren
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Foundry mit LLM Gateway verwenden

Verwenden Sie einen Gateway-Service, der Azure-kompatible Endpunkte bereitstellt:

```bash  theme={null}
# Microsoft Foundry aktivieren
export CLAUDE_CODE_USE_FOUNDRY=1

# LLM Gateway konfigurieren
export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # Falls Gateway Azure-Authentifizierung verwaltet
```

### Vertex AI mit Unternehmens-Proxy verwenden

Leiten Sie Vertex AI-Datenverkehr über einen Unternehmens-HTTP/HTTPS-Proxy weiter:

```bash  theme={null}
# Vertex aktivieren
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

# Unternehmens-Proxy konfigurieren
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Vertex AI mit LLM Gateway verwenden

Kombinieren Sie Google Vertex AI-Modelle mit einem LLM Gateway für zentralisierte Verwaltung:

```bash  theme={null}
# Vertex aktivieren
export CLAUDE_CODE_USE_VERTEX=1

# LLM Gateway konfigurieren
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # Falls Gateway GCP-Authentifizierung verwaltet
```

### Authentifizierungskonfiguration

Claude Code verwendet `ANTHROPIC_AUTH_TOKEN` für den `Authorization`-Header, wenn erforderlich. Die `SKIP_AUTH`-Flags (`CLAUDE_CODE_SKIP_BEDROCK_AUTH`, `CLAUDE_CODE_SKIP_VERTEX_AUTH`) werden in LLM Gateway-Szenarien verwendet, in denen das Gateway die Anbieter-Authentifizierung verwaltet.

## Wahl der richtigen Bereitstellungskonfiguration

Berücksichtigen Sie diese Faktoren bei der Auswahl Ihres Bereitstellungsansatzes:

### Direkter Anbieter-Zugriff

Am besten für Organisationen, die:

* Das einfachste Setup wünschen
* Bereits über AWS- oder GCP-Infrastruktur verfügen
* Anbieter-native Überwachung und Compliance benötigen

### Unternehmens-Proxy

Am besten für Organisationen, die:

* Bereits Anforderungen für Unternehmens-Proxy haben
* Datenverkehrsüberwachung und Compliance benötigen
* Alle Datenverkehr über bestimmte Netzwerkpfade leiten müssen

### LLM Gateway

Am besten für Organisationen, die:

* Nutzungsverfolgung über Teams hinweg benötigen
* Dynamisch zwischen Modellen wechseln möchten
* Benutzerdefinierte Ratenbegrenzung oder Budgets benötigen
* Zentralisierte Authentifizierungsverwaltung benötigen

## Debugging

Beim Debuggen Ihrer Bereitstellung:

* Verwenden Sie den `claude /status` [Schrägstrich-Befehl](/de/slash-commands). Dieser Befehl bietet Observability in alle angewendeten Authentifizierungs-, Proxy- und URL-Einstellungen.
* Setzen Sie die Umgebungsvariable `export ANTHROPIC_LOG=debug`, um Anfragen zu protokollieren.

## Best Practices für Organisationen

### 1. Investieren Sie in Dokumentation und Speicher

Wir empfehlen dringend, in Dokumentation zu investieren, damit Claude Code Ihre Codebasis versteht. Organisationen können CLAUDE.md-Dateien auf mehreren Ebenen bereitstellen:

* **Organisationsweit**: Stellen Sie in Systemverzeichnissen wie `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) bereit, um unternehmensweite Standards zu setzen
* **Repository-Ebene**: Erstellen Sie `CLAUDE.md`-Dateien in Repository-Wurzeln mit Projektarchitektur, Build-Befehlen und Beitragsrichtlinien. Checken Sie diese in die Versionskontrolle ein, damit alle Benutzer davon profitieren

  [Weitere Informationen](/de/memory).

### 2. Vereinfachen Sie die Bereitstellung

Wenn Sie eine benutzerdefinierte Entwicklungsumgebung haben, stellen wir fest, dass die Schaffung einer „Ein-Klick"-Möglichkeit zur Installation von Claude Code der Schlüssel zum Wachstum der Akzeptanz in einer Organisation ist.

### 3. Beginnen Sie mit gesteuerter Nutzung

Ermutigen Sie neue Benutzer, Claude Code für Codebasis-Q\&A oder bei kleineren Fehlerbehebungen oder Feature-Anfragen zu versuchen. Bitten Sie Claude Code, einen Plan zu erstellen. Überprüfen Sie Claudes Vorschläge und geben Sie Feedback, wenn es falsch ist. Mit der Zeit, wenn Benutzer dieses neue Paradigma besser verstehen, werden sie effektiver darin, Claude Code agentischer laufen zu lassen.

### 4. Konfigurieren Sie Sicherheitsrichtlinien

Sicherheitsteams können verwaltete Berechtigungen für das konfigurieren, was Claude Code darf und nicht darf, was nicht durch lokale Konfiguration überschrieben werden kann. [Weitere Informationen](/de/security).

### 5. Nutzen Sie MCP für Integrationen

MCP ist eine großartige Möglichkeit, Claude Code mehr Informationen zu geben, z. B. die Verbindung zu Ticket-Management-Systemen oder Fehlerprotokollen. Wir empfehlen, dass ein zentrales Team MCP-Server konfiguriert und eine `.mcp.json`-Konfiguration in die Codebasis eincheckt, damit alle Benutzer davon profitieren. [Weitere Informationen](/de/mcp).

Bei Anthropic vertrauen wir Claude Code, um die Entwicklung in jeder Anthropic-Codebasis voranzutreiben. Wir hoffen, dass Sie Claude Code genauso gerne verwenden wie wir.

## Nächste Schritte

* [Amazon Bedrock einrichten](/de/amazon-bedrock) für AWS-native Bereitstellung
* [Google Vertex AI konfigurieren](/de/google-vertex-ai) für GCP-Bereitstellung
* [Microsoft Foundry einrichten](/de/microsoft-foundry) für Azure-Bereitstellung
* [Enterprise Network konfigurieren](/de/network-config) für Netzwerkanforderungen
* [LLM Gateway bereitstellen](/de/llm-gateway) für Enterprise-Verwaltung
* [Einstellungen](/de/settings) für Konfigurationsoptionen und Umgebungsvariablen
