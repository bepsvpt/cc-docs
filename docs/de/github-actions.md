> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code GitHub Actions

> Erfahren Sie, wie Sie Claude Code in Ihren Entwicklungs-Workflow mit Claude Code GitHub Actions integrieren

Claude Code GitHub Actions bringt KI-gestützte Automatisierung in Ihren GitHub-Workflow. Mit einer einfachen `@claude`-Erwähnung in einem beliebigen PR oder Issue kann Claude Ihren Code analysieren, Pull Requests erstellen, Features implementieren und Bugs beheben – alles während er die Standards Ihres Projekts befolgt. Für automatische Reviews, die auf jedem PR ohne Trigger gepostet werden, siehe [GitHub Code Review](/de/code-review).

<Note>
  Claude Code GitHub Actions basiert auf dem [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview), das die programmgesteuerte Integration von Claude Code in Ihre Anwendungen ermöglicht. Sie können das SDK verwenden, um benutzerdefinierte Automatisierungs-Workflows über GitHub Actions hinaus zu erstellen.
</Note>

<Info>
  **Claude Opus 4.6 ist jetzt verfügbar.** Claude Code GitHub Actions verwenden standardmäßig Sonnet. Um Opus 4.6 zu verwenden, konfigurieren Sie den [Model-Parameter](#breaking-changes-reference) auf `claude-opus-4-6`.
</Info>

## Warum Claude Code GitHub Actions verwenden?

* **Sofortige PR-Erstellung**: Beschreiben Sie, was Sie benötigen, und Claude erstellt einen vollständigen PR mit allen notwendigen Änderungen
* **Automatisierte Code-Implementierung**: Verwandeln Sie Issues in funktionierenden Code mit einem einzigen Befehl
* **Befolgt Ihre Standards**: Claude respektiert Ihre `CLAUDE.md`-Richtlinien und vorhandene Code-Muster
* **Einfaches Setup**: Beginnen Sie in Minuten mit unserem Installer und API-Schlüssel
* **Sicher von Anfang an**: Ihr Code bleibt auf Githubs Runnern

## Was kann Claude tun?

Claude Code bietet eine leistungsstarke GitHub Action, die verändert, wie Sie mit Code arbeiten:

### Claude Code Action

Diese GitHub Action ermöglicht es Ihnen, Claude Code in Ihren GitHub Actions-Workflows auszuführen. Sie können dies verwenden, um jeden benutzerdefinierten Workflow auf Basis von Claude Code zu erstellen.

[Repository anzeigen →](https://github.com/anthropics/claude-code-action)

## Setup

## Schnelles Setup

Der einfachste Weg, diese Action einzurichten, ist über Claude Code im Terminal. Öffnen Sie einfach Claude und führen Sie `/install-github-app` aus.

Dieser Befehl führt Sie durch die Einrichtung der GitHub-App und erforderlichen Secrets.

<Note>
  * Sie müssen ein Repository-Admin sein, um die GitHub-App zu installieren und Secrets hinzuzufügen
  * Die GitHub-App fordert Lese- und Schreibberechtigungen für Contents, Issues und Pull Requests an
  * Diese Schnellstart-Methode ist nur für direkte Claude API-Benutzer verfügbar. Wenn Sie AWS Bedrock oder Google Vertex AI verwenden, siehe bitte den Abschnitt [Verwendung mit AWS Bedrock & Google Vertex AI](#using-with-aws-bedrock-%26-google-vertex-ai).
</Note>

## Manuelles Setup

Wenn der Befehl `/install-github-app` fehlschlägt oder Sie manuelles Setup bevorzugen, folgen Sie bitte diesen manuellen Setup-Anweisungen:

1. **Installieren Sie die Claude GitHub-App** in Ihrem Repository: [https://github.com/apps/claude](https://github.com/apps/claude)

   Die Claude GitHub-App erfordert die folgenden Repository-Berechtigungen:

   * **Contents**: Lesen & Schreiben (zum Ändern von Repository-Dateien)
   * **Issues**: Lesen & Schreiben (zum Antworten auf Issues)
   * **Pull requests**: Lesen & Schreiben (zum Erstellen von PRs und Pushen von Änderungen)

   Weitere Details zu Sicherheit und Berechtigungen finden Sie in der [Sicherheitsdokumentation](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md).
2. **Fügen Sie ANTHROPIC\_API\_KEY** zu Ihren Repository-Secrets hinzu ([Erfahren Sie, wie Sie Secrets in GitHub Actions verwenden](https://docs.github.com/en/actions/security-guides/using-secrets-in-github-actions))
3. **Kopieren Sie die Workflow-Datei** von [examples/claude.yml](https://github.com/anthropics/claude-code-action/blob/main/examples/claude.yml) in das Verzeichnis `.github/workflows/` Ihres Repositories

<Tip>
  Nach Abschluss des Schnellstarts oder manuellen Setups testen Sie die Action, indem Sie `@claude` in einem Issue- oder PR-Kommentar markieren.
</Tip>

## Upgrade von Beta

<Warning>
  Claude Code GitHub Actions v1.0 führt Breaking Changes ein, die ein Update Ihrer Workflow-Dateien erfordern, um von der Beta-Version auf v1.0 zu aktualisieren.
</Warning>

Wenn Sie derzeit die Beta-Version von Claude Code GitHub Actions verwenden, empfehlen wir Ihnen, Ihre Workflows auf die GA-Version zu aktualisieren. Die neue Version vereinfacht die Konfiguration und fügt leistungsstarke neue Funktionen wie automatische Modusterkennung hinzu.

### Wesentliche Änderungen

Alle Beta-Benutzer müssen diese Änderungen an ihren Workflow-Dateien vornehmen, um zu aktualisieren:

1. **Aktualisieren Sie die Action-Version**: Ändern Sie `@beta` zu `@v1`
2. **Entfernen Sie die Moduskonfiguration**: Löschen Sie `mode: "tag"` oder `mode: "agent"` (wird jetzt automatisch erkannt)
3. **Aktualisieren Sie Prompt-Eingaben**: Ersetzen Sie `direct_prompt` durch `prompt`
4. **Verschieben Sie CLI-Optionen**: Konvertieren Sie `max_turns`, `model`, `custom_instructions` usw. zu `claude_args`

### Breaking Changes Referenz

| Alte Beta-Eingabe     | Neue v1.0-Eingabe                     |
| --------------------- | ------------------------------------- |
| `mode`                | *(Entfernt - automatisch erkannt)*    |
| `direct_prompt`       | `prompt`                              |
| `override_prompt`     | `prompt` mit GitHub-Variablen         |
| `custom_instructions` | `claude_args: --append-system-prompt` |
| `max_turns`           | `claude_args: --max-turns`            |
| `model`               | `claude_args: --model`                |
| `allowed_tools`       | `claude_args: --allowedTools`         |
| `disallowed_tools`    | `claude_args: --disallowedTools`      |
| `claude_env`          | `settings` JSON-Format                |

### Vorher- und Nachher-Beispiel

**Beta-Version:**

```yaml theme={null}
- uses: anthropics/claude-code-action@beta
  with:
    mode: "tag"
    direct_prompt: "Review this PR for security issues"
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    custom_instructions: "Follow our coding standards"
    max_turns: "10"
    model: "claude-sonnet-4-6"
```

**GA-Version (v1.0):**

```yaml theme={null}
- uses: anthropics/claude-code-action@v1
  with:
    prompt: "Review this PR for security issues"
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    claude_args: |
      --append-system-prompt "Follow our coding standards"
      --max-turns 10
      --model claude-sonnet-4-6
```

<Tip>
  Die Action erkennt jetzt automatisch, ob sie im interaktiven Modus (antwortet auf `@claude`-Erwähnungen) oder im Automatisierungsmodus (wird sofort mit einem Prompt ausgeführt) ausgeführt werden soll, basierend auf Ihrer Konfiguration.
</Tip>

## Beispiel-Anwendungsfälle

Claude Code GitHub Actions kann Ihnen bei einer Vielzahl von Aufgaben helfen. Das [Beispielverzeichnis](https://github.com/anthropics/claude-code-action/tree/main/examples) enthält einsatzbereite Workflows für verschiedene Szenarien.

### Basis-Workflow

```yaml theme={null}
name: Claude Code
on:
  issue_comment:
    types: [created]
  pull_request_review_comment:
    types: [created]
jobs:
  claude:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          # Responds to @claude mentions in comments
```

### Verwendung von skills

```yaml theme={null}
name: Code Review
on:
  pull_request:
    types: [opened, synchronize]
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Review this pull request for code quality, correctness, and security. Analyze the diff, then post your findings as review comments."
          claude_args: "--max-turns 5"
```

### Benutzerdefinierte Automatisierung mit Prompts

```yaml theme={null}
name: Daily Report
on:
  schedule:
    - cron: "0 9 * * *"
jobs:
  report:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
          prompt: "Generate a summary of yesterday's commits and open issues"
          claude_args: "--model opus"
```

### Häufige Anwendungsfälle

In Issue- oder PR-Kommentaren:

```text theme={null}
@claude implement this feature based on the issue description
@claude how should I implement user authentication for this endpoint?
@claude fix the TypeError in the user dashboard component
```

Claude wird automatisch den Kontext analysieren und angemessen antworten.

## Best Practices

### CLAUDE.md-Konfiguration

Erstellen Sie eine `CLAUDE.md`-Datei im Root-Verzeichnis Ihres Repositories, um Code-Style-Richtlinien, Review-Kriterien, projektspezifische Regeln und bevorzugte Muster zu definieren. Diese Datei leitet Claudes Verständnis Ihrer Projektstandards.

### Sicherheitsüberlegungen

<Warning>Committen Sie API-Schlüssel niemals direkt in Ihr Repository.</Warning>

Umfassende Sicherheitsleitlinien einschließlich Berechtigungen, Authentifizierung und Best Practices finden Sie in der [Claude Code Action-Sicherheitsdokumentation](https://github.com/anthropics/claude-code-action/blob/main/docs/security.md).

Verwenden Sie immer GitHub Secrets für API-Schlüssel:

* Fügen Sie Ihren API-Schlüssel als Repository-Secret namens `ANTHROPIC_API_KEY` hinzu
* Referenzieren Sie ihn in Workflows: `anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}`
* Begrenzen Sie Action-Berechtigungen auf nur das Notwendigste
* Überprüfen Sie Claudes Vorschläge vor dem Mergen

Verwenden Sie immer GitHub Secrets (zum Beispiel `${{ secrets.ANTHROPIC_API_KEY }}`), anstatt API-Schlüssel direkt in Ihren Workflow-Dateien zu hardcodieren.

### Optimierung der Leistung

Verwenden Sie Issue-Templates, um Kontext bereitzustellen, halten Sie Ihre `CLAUDE.md` prägnant und fokussiert, und konfigurieren Sie angemessene Timeouts für Ihre Workflows.

### CI-Kosten

Bei der Verwendung von Claude Code GitHub Actions sollten Sie sich der damit verbundenen Kosten bewusst sein:

**GitHub Actions-Kosten:**

* Claude Code wird auf GitHub-gehosteten Runnern ausgeführt, die Ihre GitHub Actions-Minuten verbrauchen
* Siehe [Abrechnungsdokumentation von GitHub](https://docs.github.com/en/billing/managing-billing-for-your-products/managing-billing-for-github-actions/about-billing-for-github-actions) für detaillierte Preise und Minutenlimits

**API-Kosten:**

* Jede Claude-Interaktion verbraucht API-Token basierend auf der Länge von Prompts und Antworten
* Die Token-Nutzung variiert je nach Aufgabenkomplexität und Codebase-Größe
* Siehe [Claudes Preisseite](https://claude.com/platform/api) für aktuelle Token-Raten

**Tipps zur Kostenoptimierung:**

* Verwenden Sie spezifische `@claude`-Befehle, um unnötige API-Aufrufe zu reduzieren
* Konfigurieren Sie angemessene `--max-turns` in `claude_args`, um übermäßige Iterationen zu verhindern
* Legen Sie Workflow-Level-Timeouts fest, um unkontrollierte Jobs zu vermeiden
* Erwägen Sie die Verwendung von Githubs Concurrency-Kontrollen, um parallele Ausführungen zu begrenzen

## Konfigurationsbeispiele

Die Claude Code Action v1 vereinfacht die Konfiguration mit einheitlichen Parametern:

```yaml theme={null}
- uses: anthropics/claude-code-action@v1
  with:
    anthropic_api_key: ${{ secrets.ANTHROPIC_API_KEY }}
    prompt: "Your instructions here" # Optional
    claude_args: "--max-turns 5" # Optional CLI arguments
```

Wichtige Funktionen:

* **Einheitliche Prompt-Schnittstelle** - Verwenden Sie `prompt` für alle Anweisungen
* **Skills** - Rufen Sie installierte [skills](/de/skills) direkt aus dem Prompt auf
* **CLI-Passthrough** - Jedes Claude Code CLI-Argument über `claude_args`
* **Flexible Trigger** - Funktioniert mit jedem GitHub-Event

Besuchen Sie das [Beispielverzeichnis](https://github.com/anthropics/claude-code-action/tree/main/examples) für vollständige Workflow-Dateien.

<Tip>
  Wenn Claude auf Issue- oder PR-Kommentare antwortet, antwortet er automatisch auf @claude-Erwähnungen. Für andere Events verwenden Sie den `prompt`-Parameter, um Anweisungen bereitzustellen.
</Tip>

## Verwendung mit AWS Bedrock & Google Vertex AI

Für Unternehmensumgebungen können Sie Claude Code GitHub Actions mit Ihrer eigenen Cloud-Infrastruktur verwenden. Dieser Ansatz gibt Ihnen Kontrolle über Datenresidenz und Abrechnung, während Sie die gleiche Funktionalität beibehalten.

### Voraussetzungen

Bevor Sie Claude Code GitHub Actions mit Cloud-Providern einrichten, benötigen Sie:

#### Für Google Cloud Vertex AI:

1. Ein Google Cloud-Projekt mit aktiviertem Vertex AI
2. Workload Identity Federation für GitHub Actions konfiguriert
3. Ein Service-Konto mit erforderlichen Berechtigungen
4. Eine GitHub-App (empfohlen) oder verwenden Sie das Standard-GITHUB\_TOKEN

#### Für AWS Bedrock:

1. Ein AWS-Konto mit aktiviertem Amazon Bedrock
2. GitHub OIDC Identity Provider in AWS konfiguriert
3. Eine IAM-Rolle mit Bedrock-Berechtigungen
4. Eine GitHub-App (empfohlen) oder verwenden Sie das Standard-GITHUB\_TOKEN

<Steps>
  <Step title="Erstellen Sie eine benutzerdefinierte GitHub-App (empfohlen für 3P-Provider)">
    Für beste Kontrolle und Sicherheit bei der Verwendung von 3P-Providern wie Vertex AI oder Bedrock empfehlen wir, Ihre eigene GitHub-App zu erstellen:

    1. Gehen Sie zu [https://github.com/settings/apps/new](https://github.com/settings/apps/new)
    2. Füllen Sie die grundlegenden Informationen aus:
       * **GitHub App-Name**: Wählen Sie einen eindeutigen Namen (z. B. 'YourOrg Claude Assistant")
       * **Homepage URL**: Website Ihrer Organisation oder die Repository-URL
    3. Konfigurieren Sie die App-Einstellungen:
       * **Webhooks**: Deaktivieren Sie „Active" (nicht erforderlich für diese Integration)
    4. Legen Sie die erforderlichen Berechtigungen fest:
       * **Repository-Berechtigungen**:
         * Contents: Lesen & Schreiben
         * Issues: Lesen & Schreiben
         * Pull requests: Lesen & Schreiben
    5. Klicken Sie auf „Create GitHub App"
    6. Nach der Erstellung klicken Sie auf „Generate a private key" und speichern Sie die heruntergeladene `.pem`-Datei
    7. Notieren Sie sich Ihre App-ID von der App-Einstellungsseite
    8. Installieren Sie die App in Ihrem Repository:
       * Klicken Sie auf der Einstellungsseite Ihrer App auf „Install App" in der linken Seitenleiste
       * Wählen Sie Ihr Konto oder Ihre Organisation
       * Wählen Sie „Only select repositories" und wählen Sie das spezifische Repository
       * Klicken Sie auf „Install"
    9. Fügen Sie den privaten Schlüssel als Secret zu Ihrem Repository hinzu:
       * Gehen Sie zu den Einstellungen Ihres Repositories → Secrets and variables → Actions
       * Erstellen Sie ein neues Secret namens `APP_PRIVATE_KEY` mit dem Inhalt der `.pem`-Datei
    10. Fügen Sie die App-ID als Secret hinzu:

    * Erstellen Sie ein neues Secret namens `APP_ID` mit der ID Ihrer GitHub-App

    <Note>
      Diese App wird mit der [actions/create-github-app-token](https://github.com/actions/create-github-app-token)-Action verwendet, um Authentifizierungs-Token in Ihren Workflows zu generieren.
    </Note>

    **Alternative für Claude API oder wenn Sie keine eigene Github-App einrichten möchten**: Verwenden Sie die offizielle Anthropic-App:

    1. Installieren Sie von: [https://github.com/apps/claude](https://github.com/apps/claude)
    2. Keine zusätzliche Konfiguration erforderlich für die Authentifizierung
  </Step>

  <Step title="Konfigurieren Sie die Cloud-Provider-Authentifizierung">
    Wählen Sie Ihren Cloud-Provider und richten Sie sichere Authentifizierung ein:

    <AccordionGroup>
      <Accordion title="AWS Bedrock">
        **Konfigurieren Sie AWS, um GitHub Actions die sichere Authentifizierung ohne Speicherung von Anmeldedaten zu ermöglichen.**

        > **Sicherheitshinweis**: Verwenden Sie Repository-spezifische Konfigurationen und gewähren Sie nur die minimal erforderlichen Berechtigungen.

        **Erforderliches Setup**:

        1. **Aktivieren Sie Amazon Bedrock**:
           * Fordern Sie Zugriff auf Claude-Modelle in Amazon Bedrock an
           * Für regionsübergreifende Modelle fordern Sie Zugriff in allen erforderlichen Regionen an

        2. **Richten Sie GitHub OIDC Identity Provider ein**:
           * Provider-URL: `https://token.actions.githubusercontent.com`
           * Audience: `sts.amazonaws.com`

        3. **Erstellen Sie eine IAM-Rolle für GitHub Actions**:
           * Vertrauenswürdiger Entity-Typ: Web Identity
           * Identity Provider: `token.actions.githubusercontent.com`
           * Berechtigungen: `AmazonBedrockFullAccess`-Richtlinie
           * Konfigurieren Sie die Trust-Richtlinie für Ihr spezifisches Repository

        **Erforderliche Werte**:

        Nach dem Setup benötigen Sie:

        * **AWS\_ROLE\_TO\_ASSUME**: Das ARN der IAM-Rolle, die Sie erstellt haben

        <Tip>
          OIDC ist sicherer als die Verwendung statischer AWS-Zugriffstasten, da Anmeldedaten temporär sind und automatisch rotiert werden.
        </Tip>

        Siehe [AWS-Dokumentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_providers_create_oidc.html) für detaillierte OIDC-Setup-Anweisungen.
      </Accordion>

      <Accordion title="Google Vertex AI">
        **Konfigurieren Sie Google Cloud, um GitHub Actions die sichere Authentifizierung ohne Speicherung von Anmeldedaten zu ermöglichen.**

        > **Sicherheitshinweis**: Verwenden Sie Repository-spezifische Konfigurationen und gewähren Sie nur die minimal erforderlichen Berechtigungen.

        **Erforderliches Setup**:

        1. **Aktivieren Sie APIs** in Ihrem Google Cloud-Projekt:
           * IAM Credentials API
           * Security Token Service (STS) API
           * Vertex AI API

        2. **Erstellen Sie Workload Identity Federation-Ressourcen**:
           * Erstellen Sie einen Workload Identity Pool
           * Fügen Sie einen GitHub OIDC-Provider mit hinzu:
             * Issuer: `https://token.actions.githubusercontent.com`
             * Attribut-Mappings für Repository und Owner
             * **Sicherheitsempfehlung**: Verwenden Sie Repository-spezifische Attribut-Bedingungen

        3. **Erstellen Sie ein Service-Konto**:
           * Gewähren Sie nur die Rolle `Vertex AI User`
           * **Sicherheitsempfehlung**: Erstellen Sie ein dediziertes Service-Konto pro Repository

        4. **Konfigurieren Sie IAM-Bindungen**:
           * Erlauben Sie dem Workload Identity Pool, das Service-Konto zu imitieren
           * **Sicherheitsempfehlung**: Verwenden Sie Repository-spezifische Principal-Sets

        **Erforderliche Werte**:

        Nach dem Setup benötigen Sie:

        * **GCP\_WORKLOAD\_IDENTITY\_PROVIDER**: Der vollständige Provider-Ressourcenname
        * **GCP\_SERVICE\_ACCOUNT**: Die Service-Konto-E-Mail-Adresse

        <Tip>
          Workload Identity Federation eliminiert die Notwendigkeit herunterladbarer Service-Konto-Schlüssel und verbessert die Sicherheit.
        </Tip>

        Für detaillierte Setup-Anweisungen konsultieren Sie die [Google Cloud Workload Identity Federation-Dokumentation](https://cloud.google.com/iam/docs/workload-identity-federation).
      </Accordion>
    </AccordionGroup>
  </Step>

  <Step title="Fügen Sie erforderliche Secrets hinzu">
    Fügen Sie die folgenden Secrets zu Ihrem Repository hinzu (Settings → Secrets and variables → Actions):

    #### Für Claude API (direkt):

    1. **Für API-Authentifizierung**:
       * `ANTHROPIC_API_KEY`: Ihr Claude API-Schlüssel von [console.anthropic.com](https://console.anthropic.com)

    2. **Für GitHub-App (wenn Sie Ihre eigene App verwenden)**:
       * `APP_ID`: Die ID Ihrer GitHub-App
       * `APP_PRIVATE_KEY`: Der Inhalt des privaten Schlüssels (.pem)

    #### Für Google Cloud Vertex AI

    1. **Für GCP-Authentifizierung**:
       * `GCP_WORKLOAD_IDENTITY_PROVIDER`
       * `GCP_SERVICE_ACCOUNT`

    2. **Für GitHub-App (wenn Sie Ihre eigene App verwenden)**:
       * `APP_ID`: Die ID Ihrer GitHub-App
       * `APP_PRIVATE_KEY`: Der Inhalt des privaten Schlüssels (.pem)

    #### Für AWS Bedrock

    1. **Für AWS-Authentifizierung**:
       * `AWS_ROLE_TO_ASSUME`

    2. **Für GitHub-App (wenn Sie Ihre eigene App verwenden)**:
       * `APP_ID`: Die ID Ihrer GitHub-App
       * `APP_PRIVATE_KEY`: Der Inhalt des privaten Schlüssels (.pem)
  </Step>

  <Step title="Erstellen Sie Workflow-Dateien">
    Erstellen Sie GitHub Actions-Workflow-Dateien, die sich in Ihren Cloud-Provider integrieren. Die folgenden Beispiele zeigen vollständige Konfigurationen für AWS Bedrock und Google Vertex AI:

    <AccordionGroup>
      <Accordion title="AWS Bedrock-Workflow">
        **Voraussetzungen:**

        * AWS Bedrock-Zugriff aktiviert mit Claude-Modell-Berechtigungen
        * GitHub als OIDC-Identity-Provider in AWS konfiguriert
        * IAM-Rolle mit Bedrock-Berechtigungen, die GitHub Actions vertraut

        **Erforderliche GitHub-Secrets:**

        | Secret-Name          | Beschreibung                                                       |
        | -------------------- | ------------------------------------------------------------------ |
        | `AWS_ROLE_TO_ASSUME` | ARN der IAM-Rolle für Bedrock-Zugriff                              |
        | `APP_ID`             | Ihre GitHub-App-ID (aus App-Einstellungen)                         |
        | `APP_PRIVATE_KEY`    | Der private Schlüssel, den Sie für Ihre GitHub-App generiert haben |

        ```yaml theme={null}
        name: Claude PR Action

        permissions:
          contents: write
          pull-requests: write
          issues: write
          id-token: write

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened, assigned]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
            runs-on: ubuntu-latest
            env:
              AWS_REGION: us-west-2
            steps:
              - name: Checkout repository
                uses: actions/checkout@v4

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Configure AWS Credentials (OIDC)
                uses: aws-actions/configure-aws-credentials@v4
                with:
                  role-to-assume: ${{ secrets.AWS_ROLE_TO_ASSUME }}
                  aws-region: us-west-2

              - uses: anthropics/claude-code-action@v1
                with:
                  github_token: ${{ steps.app-token.outputs.token }}
                  use_bedrock: "true"
                  claude_args: '--model us.anthropic.claude-sonnet-4-6 --max-turns 10'
        ```

        <Tip>
          Das Modell-ID-Format für Bedrock enthält ein Regions-Präfix (zum Beispiel `us.anthropic.claude-sonnet-4-6`).
        </Tip>
      </Accordion>

      <Accordion title="Google Vertex AI-Workflow">
        **Voraussetzungen:**

        * Vertex AI API in Ihrem GCP-Projekt aktiviert
        * Workload Identity Federation für GitHub konfiguriert
        * Service-Konto mit Vertex AI-Berechtigungen

        **Erforderliche GitHub-Secrets:**

        | Secret-Name                      | Beschreibung                                                       |
        | -------------------------------- | ------------------------------------------------------------------ |
        | `GCP_WORKLOAD_IDENTITY_PROVIDER` | Workload Identity Provider-Ressourcenname                          |
        | `GCP_SERVICE_ACCOUNT`            | Service-Konto-E-Mail mit Vertex AI-Zugriff                         |
        | `APP_ID`                         | Ihre GitHub-App-ID (aus App-Einstellungen)                         |
        | `APP_PRIVATE_KEY`                | Der private Schlüssel, den Sie für Ihre GitHub-App generiert haben |

        ```yaml theme={null}
        name: Claude PR Action

        permissions:
          contents: write
          pull-requests: write
          issues: write
          id-token: write

        on:
          issue_comment:
            types: [created]
          pull_request_review_comment:
            types: [created]
          issues:
            types: [opened, assigned]

        jobs:
          claude-pr:
            if: |
              (github.event_name == 'issue_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'pull_request_review_comment' && contains(github.event.comment.body, '@claude')) ||
              (github.event_name == 'issues' && contains(github.event.issue.body, '@claude'))
            runs-on: ubuntu-latest
            steps:
              - name: Checkout repository
                uses: actions/checkout@v4

              - name: Generate GitHub App token
                id: app-token
                uses: actions/create-github-app-token@v2
                with:
                  app-id: ${{ secrets.APP_ID }}
                  private-key: ${{ secrets.APP_PRIVATE_KEY }}

              - name: Authenticate to Google Cloud
                id: auth
                uses: google-github-actions/auth@v2
                with:
                  workload_identity_provider: ${{ secrets.GCP_WORKLOAD_IDENTITY_PROVIDER }}
                  service_account: ${{ secrets.GCP_SERVICE_ACCOUNT }}

              - uses: anthropics/claude-code-action@v1
                with:
                  github_token: ${{ steps.app-token.outputs.token }}
                  trigger_phrase: "@claude"
                  use_vertex: "true"
                  claude_args: '--model claude-sonnet-4-5@20250929 --max-turns 10'
                env:
                  ANTHROPIC_VERTEX_PROJECT_ID: ${{ steps.auth.outputs.project_id }}
                  CLOUD_ML_REGION: us-east5
                  VERTEX_REGION_CLAUDE_4_5_SONNET: us-east5
        ```

        <Tip>
          Die Projekt-ID wird automatisch aus dem Google Cloud-Authentifizierungsschritt abgerufen, daher müssen Sie sie nicht hardcodieren.
        </Tip>
      </Accordion>
    </AccordionGroup>
  </Step>
</Steps>

## Fehlerbehebung

### Claude antwortet nicht auf @claude-Befehle

Überprüfen Sie, dass die GitHub-App korrekt installiert ist, stellen Sie sicher, dass Workflows aktiviert sind, überprüfen Sie, dass der API-Schlüssel in Repository-Secrets gesetzt ist, und bestätigen Sie, dass der Kommentar `@claude` enthält (nicht `/claude`).

### CI wird nicht auf Claudes Commits ausgeführt

Stellen Sie sicher, dass Sie die GitHub-App oder benutzerdefinierte App verwenden (nicht Actions-Benutzer), überprüfen Sie, dass Workflow-Trigger die erforderlichen Events enthalten, und überprüfen Sie, dass App-Berechtigungen CI-Trigger enthalten.

### Authentifizierungsfehler

Bestätigen Sie, dass der API-Schlüssel gültig ist und ausreichende Berechtigungen hat. Für Bedrock/Vertex überprüfen Sie die Anmeldedaten-Konfiguration und stellen Sie sicher, dass Secrets in Workflows korrekt benannt sind.

## Erweiterte Konfiguration

### Action-Parameter

Die Claude Code Action v1 verwendet eine vereinfachte Konfiguration:

| Parameter           | Beschreibung                                                        | Erforderlich |
| ------------------- | ------------------------------------------------------------------- | ------------ |
| `prompt`            | Anweisungen für Claude (Klartext oder ein [skill](/de/skills)-Name) | Nein\*       |
| `claude_args`       | CLI-Argumente, die an Claude Code übergeben werden                  | Nein         |
| `anthropic_api_key` | Claude API-Schlüssel                                                | Ja\*\*       |
| `github_token`      | GitHub-Token für API-Zugriff                                        | Nein         |
| `trigger_phrase`    | Benutzerdefinierte Trigger-Phrase (Standard: "@claude")             | Nein         |
| `use_bedrock`       | Verwenden Sie AWS Bedrock statt Claude API                          | Nein         |
| `use_vertex`        | Verwenden Sie Google Vertex AI statt Claude API                     | Nein         |

\*Prompt ist optional – wenn für Issue/PR-Kommentare weggelassen, antwortet Claude auf Trigger-Phrase\
\*\*Erforderlich für direkte Claude API, nicht für Bedrock/Vertex

#### Übergeben Sie CLI-Argumente

Der Parameter `claude_args` akzeptiert alle Claude Code CLI-Argumente:

```yaml theme={null}
claude_args: "--max-turns 5 --model claude-sonnet-4-6 --mcp-config /path/to/config.json"
```

Häufige Argumente:

* `--max-turns`: Maximale Gesprächs-Turns (Standard: 10)
* `--model`: Zu verwendendes Modell (zum Beispiel `claude-sonnet-4-6`)
* `--mcp-config`: Pfad zur MCP-Konfiguration
* `--allowedTools`: Komma-getrennte Liste zulässiger Tools. Der Alias `--allowed-tools` funktioniert auch.
* `--debug`: Debug-Ausgabe aktivieren

### Alternative Integrationsmethoden

Während der Befehl `/install-github-app` der empfohlene Ansatz ist, können Sie auch:

* **Benutzerdefinierte GitHub-App**: Für Organisationen, die Branded-Benutzernamen oder benutzerdefinierte Authentifizierungs-Flows benötigen. Erstellen Sie Ihre eigene GitHub-App mit erforderlichen Berechtigungen (Contents, Issues, Pull Requests) und verwenden Sie die actions/create-github-app-token-Action, um Token in Ihren Workflows zu generieren.
* **Manuelle GitHub Actions**: Direkte Workflow-Konfiguration für maximale Flexibilität
* **MCP-Konfiguration**: Dynamisches Laden von Model Context Protocol-Servern

Siehe die [Claude Code Action-Dokumentation](https://github.com/anthropics/claude-code-action/blob/main/docs) für detaillierte Leitfäden zu Authentifizierung, Sicherheit und erweiterte Konfiguration.

### Anpassung von Claudes Verhalten

Sie können Claudes Verhalten auf zwei Arten konfigurieren:

1. **CLAUDE.md**: Definieren Sie Coding-Standards, Review-Kriterien und projektspezifische Regeln in einer `CLAUDE.md`-Datei im Root-Verzeichnis Ihres Repositories. Claude wird diese Richtlinien beim Erstellen von PRs und Antworten auf Anfragen befolgen. Weitere Details finden Sie in unserer [Memory-Dokumentation](/de/memory).
2. **Benutzerdefinierte Prompts**: Verwenden Sie den Parameter `prompt` in der Workflow-Datei, um Workflow-spezifische Anweisungen bereitzustellen. Dies ermöglicht es Ihnen, Claudes Verhalten für verschiedene Workflows oder Aufgaben anzupassen.

Claude wird diese Richtlinien beim Erstellen von PRs und Antworten auf Anfragen befolgen.
