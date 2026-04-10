> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Übersicht zur Enterprise-Bereitstellung

> Erfahren Sie, wie Claude Code mit verschiedenen Drittanbieterdiensten und Infrastrukturen integriert werden kann, um Enterprise-Bereitstellungsanforderungen zu erfüllen.

Organisationen können Claude Code direkt über Anthropic oder über einen Cloud-Anbieter bereitstellen. Diese Seite hilft Ihnen, die richtige Konfiguration auszuwählen.

## Bereitstellungsoptionen vergleichen

Für die meisten Organisationen bieten Claude for Teams oder Claude for Enterprise die beste Erfahrung. Teammitglieder erhalten Zugriff auf sowohl Claude Code als auch Claude im Web mit einem einzigen Abonnement, zentralisierte Abrechnung und ohne erforderliche Infrastruktureinrichtung.

**Claude for Teams** ist Self-Service und umfasst Zusammenarbeitsfunktionen, Admin-Tools und Abrechnungsverwaltung. Am besten für kleinere Teams, die schnell starten möchten.

**Claude for Enterprise** fügt SSO und Domain-Erfassung, rollenbasierte Berechtigungen, Compliance-API-Zugriff und verwaltete Richtlinieneinstellungen für die Bereitstellung von organisationsweiten Claude Code-Konfigurationen hinzu. Am besten für größere Organisationen mit Sicherheits- und Compliance-Anforderungen.

Erfahren Sie mehr über [Team-Pläne](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) und [Enterprise-Pläne](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan).

Wenn Ihre Organisation spezifische Infrastrukturanforderungen hat, vergleichen Sie die folgenden Optionen:

<table>
  <thead>
    <tr>
      <th>Funktion</th>
      <th>Claude for Teams/Enterprise</th>
      <th>Anthropic Console</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Am besten für</td>
      <td>Die meisten Organisationen (empfohlen)</td>
      <td>Einzelne Entwickler</td>
      <td>AWS-native Bereitstellungen</td>
      <td>GCP-native Bereitstellungen</td>
      <td>Azure-native Bereitstellungen</td>
    </tr>

    <tr>
      <td>Abrechnung</td>
      <td><strong>Teams:</strong> 150 USD/Platz (Premium) mit PAYG verfügbar<br /><strong>Enterprise:</strong> <a href="https://claude.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=third_party_enterprise">Kontaktieren Sie den Vertrieb</a></td>
      <td>PAYG</td>
      <td>PAYG über AWS</td>
      <td>PAYG über GCP</td>
      <td>PAYG über Azure</td>
    </tr>

    <tr>
      <td>Regionen</td>
      <td>Unterstützte [Länder](https://www.anthropic.com/supported-countries)</td>
      <td>Unterstützte [Länder](https://www.anthropic.com/supported-countries)</td>
      <td>Mehrere AWS [Regionen](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)</td>
      <td>Mehrere GCP [Regionen](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)</td>
      <td>Mehrere Azure [Regionen](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)</td>
    </tr>

    <tr>
      <td>Prompt caching</td>
      <td>Standardmäßig aktiviert</td>
      <td>Standardmäßig aktiviert</td>
      <td>Standardmäßig aktiviert</td>
      <td>Standardmäßig aktiviert</td>
      <td>Standardmäßig aktiviert</td>
    </tr>

    <tr>
      <td>Authentifizierung</td>
      <td>Claude.ai SSO oder E-Mail</td>
      <td>API-Schlüssel</td>
      <td>API-Schlüssel oder AWS-Anmeldedaten</td>
      <td>GCP-Anmeldedaten</td>
      <td>API-Schlüssel oder Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>Kostenverfolgung</td>
      <td>Nutzungs-Dashboard</td>
      <td>Nutzungs-Dashboard</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
      <td>Azure Cost Management</td>
    </tr>

    <tr>
      <td>Umfasst Claude im Web</td>
      <td>Ja</td>
      <td>Nein</td>
      <td>Nein</td>
      <td>Nein</td>
      <td>Nein</td>
    </tr>

    <tr>
      <td>Enterprise-Funktionen</td>
      <td>Teamverwaltung, SSO, Nutzungsüberwachung</td>
      <td>Keine</td>
      <td>IAM-Richtlinien, CloudTrail</td>
      <td>IAM-Rollen, Cloud Audit Logs</td>
      <td>RBAC-Richtlinien, Azure Monitor</td>
    </tr>
  </tbody>
</table>

Wählen Sie eine Bereitstellungsoption aus, um Setupanweisungen anzuzeigen:

* [Claude for Teams oder Enterprise](/de/authentication#claude-for-teams-or-enterprise)
* [Anthropic Console](/de/authentication#claude-console-authentication)
* [Amazon Bedrock](/de/amazon-bedrock)
* [Google Vertex AI](/de/google-vertex-ai)
* [Microsoft Foundry](/de/microsoft-foundry)

## Proxys und Gateways konfigurieren

Die meisten Organisationen können einen Cloud-Anbieter direkt ohne zusätzliche Konfiguration nutzen. Möglicherweise müssen Sie jedoch einen Unternehmens-Proxy oder LLM-Gateway konfigurieren, wenn Ihre Organisation spezifische Netzwerk- oder Verwaltungsanforderungen hat. Dies sind unterschiedliche Konfigurationen, die zusammen verwendet werden können:

* **Unternehmens-Proxy**: Leitet Datenverkehr über einen HTTP/HTTPS-Proxy weiter. Verwenden Sie dies, wenn Ihre Organisation verlangt, dass der gesamte ausgehende Datenverkehr einen Proxy-Server für Sicherheitsüberwachung, Compliance oder Netzwerkrichtliniendurchsetzung durchläuft. Konfigurieren Sie mit den Umgebungsvariablen `HTTPS_PROXY` oder `HTTP_PROXY`. Erfahren Sie mehr in [Enterprise-Netzwerkkonfiguration](/de/network-config).
* **LLM-Gateway**: Ein Dienst, der sich zwischen Claude Code und dem Cloud-Anbieter befindet, um Authentifizierung und Routing zu verwalten. Verwenden Sie dies, wenn Sie eine zentralisierte Nutzungsverfolgung über Teams, benutzerdefinierte Ratenbegrenzung oder Budgets oder zentralisierte Authentifizierungsverwaltung benötigen. Konfigurieren Sie mit den Umgebungsvariablen `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL` oder `ANTHROPIC_VERTEX_BASE_URL`. Erfahren Sie mehr in [LLM-Gateway-Konfiguration](/de/llm-gateway).

Die folgenden Beispiele zeigen die Umgebungsvariablen, die in Ihrer Shell oder Shell-Profildatei (`.bashrc`, `.zshrc`) gesetzt werden sollen. Siehe [Einstellungen](/de/settings) für andere Konfigurationsmethoden.

### Amazon Bedrock

<Tabs>
  <Tab title="Unternehmens-Proxy">
    Leiten Sie Bedrock-Datenverkehr über Ihren Unternehmens-Proxy weiter, indem Sie die folgenden [Umgebungsvariablen](/de/env-vars) setzen:

    ```bash  theme={null}
    # Enable Bedrock
    export CLAUDE_CODE_USE_BEDROCK=1
    export AWS_REGION=us-east-1

    # Configure corporate proxy
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="LLM-Gateway">
    Leiten Sie Bedrock-Datenverkehr über Ihr LLM-Gateway weiter, indem Sie die folgenden [Umgebungsvariablen](/de/env-vars) setzen:

    ```bash  theme={null}
    # Enable Bedrock
    export CLAUDE_CODE_USE_BEDROCK=1

    # Configure LLM gateway
    export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
    export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # If gateway handles AWS auth
    ```
  </Tab>
</Tabs>

### Microsoft Foundry

<Tabs>
  <Tab title="Unternehmens-Proxy">
    Leiten Sie Foundry-Datenverkehr über Ihren Unternehmens-Proxy weiter, indem Sie die folgenden [Umgebungsvariablen](/de/env-vars) setzen:

    ```bash  theme={null}
    # Enable Microsoft Foundry
    export CLAUDE_CODE_USE_FOUNDRY=1
    export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
    export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # Or omit for Entra ID auth

    # Configure corporate proxy
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="LLM-Gateway">
    Leiten Sie Foundry-Datenverkehr über Ihr LLM-Gateway weiter, indem Sie die folgenden [Umgebungsvariablen](/de/env-vars) setzen:

    ```bash  theme={null}
    # Enable Microsoft Foundry
    export CLAUDE_CODE_USE_FOUNDRY=1

    # Configure LLM gateway
    export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
    export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # If gateway handles Azure auth
    ```
  </Tab>
</Tabs>

### Google Vertex AI

<Tabs>
  <Tab title="Unternehmens-Proxy">
    Leiten Sie Vertex AI-Datenverkehr über Ihren Unternehmens-Proxy weiter, indem Sie die folgenden [Umgebungsvariablen](/de/env-vars) setzen:

    ```bash  theme={null}
    # Enable Vertex
    export CLAUDE_CODE_USE_VERTEX=1
    export CLOUD_ML_REGION=us-east5
    export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

    # Configure corporate proxy
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="LLM-Gateway">
    Leiten Sie Vertex AI-Datenverkehr über Ihr LLM-Gateway weiter, indem Sie die folgenden [Umgebungsvariablen](/de/env-vars) setzen:

    ```bash  theme={null}
    # Enable Vertex
    export CLAUDE_CODE_USE_VERTEX=1

    # Configure LLM gateway
    export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
    export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # If gateway handles GCP auth
    ```
  </Tab>
</Tabs>

<Tip>
  Verwenden Sie `/status` in Claude Code, um zu überprüfen, ob Ihre Proxy- und Gateway-Konfiguration korrekt angewendet wird.
</Tip>

## Best Practices für Organisationen

### Investieren Sie in Dokumentation und Memory

Wir empfehlen dringend, in Dokumentation zu investieren, damit Claude Code Ihre Codebasis versteht. Organisationen können CLAUDE.md-Dateien auf mehreren Ebenen bereitstellen:

* **Organisationsweit**: Bereitstellen in Systemverzeichnissen wie `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) für unternehmensweite Standards
* **Repository-Ebene**: Erstellen Sie `CLAUDE.md`-Dateien in Repository-Wurzeln mit Projektarchitektur, Build-Befehlen und Beitragsleitlinien. Checken Sie diese in die Versionskontrolle ein, damit alle Benutzer davon profitieren

Erfahren Sie mehr in [Memory und CLAUDE.md-Dateien](/de/memory).

### Vereinfachen Sie die Bereitstellung

Wenn Sie eine benutzerdefinierte Entwicklungsumgebung haben, stellen wir fest, dass die Schaffung einer „Ein-Klick"-Möglichkeit zur Installation von Claude Code der Schlüssel zum Wachstum der Akzeptanz in einer Organisation ist.

### Beginnen Sie mit gesteuerter Nutzung

Ermutigen Sie neue Benutzer, Claude Code für Codebasis-Fragen oder bei kleineren Fehlerbehebungen oder Funktionsanfragen zu versuchen. Bitten Sie Claude Code, einen Plan zu erstellen. Überprüfen Sie Claudes Vorschläge und geben Sie Feedback, wenn es nicht stimmt. Mit der Zeit, wenn Benutzer dieses neue Paradigma besser verstehen, werden sie effektiver darin, Claude Code agentischer laufen zu lassen.

### Pinnen Sie Modellversionen für Cloud-Anbieter

Wenn Sie über [Bedrock](/de/amazon-bedrock), [Vertex AI](/de/google-vertex-ai) oder [Foundry](/de/microsoft-foundry) bereitstellen, pinnen Sie spezifische Modellversionen mit `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` und `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Ohne Pinning werden Claude Code-Aliase zur neuesten Version aufgelöst, was Benutzer unterbrechen kann, wenn Anthropic ein neues Modell veröffentlicht, das noch nicht in Ihrem Konto aktiviert ist. Siehe [Modellkonfiguration](/de/model-config#pin-models-for-third-party-deployments) für Details.

### Konfigurieren Sie Sicherheitsrichtlinien

Sicherheitsteams können verwaltete Berechtigungen für das konfigurieren, was Claude Code darf und nicht darf, was nicht durch lokale Konfiguration überschrieben werden kann. [Erfahren Sie mehr](/de/security).

### Nutzen Sie MCP für Integrationen

MCP ist eine großartige Möglichkeit, Claude Code mehr Informationen zu geben, z. B. die Verbindung mit Ticketverwaltungssystemen oder Fehlerprotokollen. Wir empfehlen, dass ein zentrales Team MCP-Server konfiguriert und eine `.mcp.json`-Konfiguration in die Codebasis eincheckt, damit alle Benutzer davon profitieren. [Erfahren Sie mehr](/de/mcp).

Bei Anthropic vertrauen wir Claude Code, um die Entwicklung in jeder Anthropic-Codebasis zu unterstützen. Wir hoffen, dass Sie Claude Code genauso gerne verwenden wie wir.

## Nächste Schritte

Nachdem Sie eine Bereitstellungsoption ausgewählt und den Zugriff für Ihr Team konfiguriert haben:

1. **Rollout für Ihr Team**: Teilen Sie Installationsanweisungen mit und lassen Sie Teammitglieder [Claude Code installieren](/de/setup) und sich mit ihren Anmeldedaten authentifizieren.
2. **Richten Sie gemeinsame Konfiguration ein**: Erstellen Sie eine [CLAUDE.md-Datei](/de/memory) in Ihren Repositories, um Claude Code dabei zu helfen, Ihre Codebasis und Codierungsstandards zu verstehen.
3. **Konfigurieren Sie Berechtigungen**: Überprüfen Sie [Sicherheitseinstellungen](/de/security), um zu definieren, was Claude Code in Ihrer Umgebung darf und nicht darf.
