> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code auf Amazon Bedrock

> Erfahren Sie, wie Sie Claude Code über Amazon Bedrock konfigurieren, einschließlich Setup, IAM-Konfiguration und Fehlerbehebung.

## Voraussetzungen

Bevor Sie Claude Code mit Bedrock konfigurieren, stellen Sie sicher, dass Sie über Folgendes verfügen:

* Ein AWS-Konto mit aktiviertem Bedrock-Zugriff
* Zugriff auf gewünschte Claude-Modelle (z. B. Claude Sonnet 4.6) in Bedrock
* AWS CLI installiert und konfiguriert (optional – nur erforderlich, wenn Sie keinen anderen Mechanismus zur Beschaffung von Anmeldedaten haben)
* Angemessene IAM-Berechtigungen

<Note>
  Wenn Sie Claude Code für mehrere Benutzer bereitstellen, [fixieren Sie Ihre Modellversionen](#4-pin-model-versions), um Fehler zu vermeiden, wenn Anthropic neue Modelle veröffentlicht.
</Note>

## Setup

### 1. Anwendungsfalldetails einreichen

Erstmalige Benutzer von Anthropic-Modellen müssen Anwendungsfalldetails einreichen, bevor sie ein Modell aufrufen. Dies wird einmal pro Konto durchgeführt.

1. Stellen Sie sicher, dass Sie die richtigen IAM-Berechtigungen haben (siehe unten für weitere Informationen)
2. Navigieren Sie zur [Amazon Bedrock-Konsole](https://console.aws.amazon.com/bedrock/)
3. Wählen Sie **Chat/Text playground**
4. Wählen Sie ein beliebiges Anthropic-Modell aus, und Sie werden aufgefordert, das Anwendungsfallformular auszufüllen

### 2. AWS-Anmeldedaten konfigurieren

Claude Code verwendet die Standard-AWS-SDK-Anmeldedatenkette. Richten Sie Ihre Anmeldedaten mit einer dieser Methoden ein:

**Option A: AWS CLI-Konfiguration**

```bash  theme={null}
aws configure
```

**Option B: Umgebungsvariablen (Zugriffsschlüssel)**

```bash  theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**Option C: Umgebungsvariablen (SSO-Profil)**

```bash  theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**Option D: AWS Management Console-Anmeldedaten**

```bash  theme={null}
aws login
```

[Erfahren Sie mehr](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) über `aws login`.

**Option E: Bedrock API-Schlüssel**

```bash  theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Bedrock API-Schlüssel bieten eine einfachere Authentifizierungsmethode ohne vollständige AWS-Anmeldedaten. [Erfahren Sie mehr über Bedrock API-Schlüssel](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### Erweiterte Anmeldedatenkonfiguration

Claude Code unterstützt die automatische Aktualisierung von Anmeldedaten für AWS SSO und Unternehmensidentitätsanbieter. Fügen Sie diese Einstellungen zu Ihrer Claude Code-Einstellungsdatei hinzu (siehe [Einstellungen](/de/settings) für Dateispeicherorte).

Wenn Claude Code erkennt, dass Ihre AWS-Anmeldedaten abgelaufen sind (entweder lokal basierend auf ihrem Zeitstempel oder wenn Bedrock einen Anmeldedatenfehler zurückgibt), führt es automatisch Ihre konfigurierten `awsAuthRefresh`- und/oder `awsCredentialExport`-Befehle aus, um neue Anmeldedaten zu erhalten, bevor die Anfrage erneut versucht wird.

##### Beispielkonfiguration

```json  theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### Erklärung der Konfigurationseinstellungen

**`awsAuthRefresh`**: Verwenden Sie dies für Befehle, die das `.aws`-Verzeichnis ändern, z. B. zum Aktualisieren von Anmeldedaten, SSO-Cache oder Konfigurationsdateien. Die Ausgabe des Befehls wird dem Benutzer angezeigt, aber interaktive Eingaben werden nicht unterstützt. Dies funktioniert gut für browserbasierte SSO-Flows, bei denen die CLI eine URL oder einen Code anzeigt und Sie die Authentifizierung im Browser abschließen.

**`awsCredentialExport`**: Verwenden Sie dies nur, wenn Sie das `.aws`-Verzeichnis nicht ändern können und Anmeldedaten direkt zurückgeben müssen. Die Ausgabe wird stillschweigend erfasst und nicht dem Benutzer angezeigt. Der Befehl muss JSON in diesem Format ausgeben:

```json  theme={null}
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. Claude Code konfigurieren

Legen Sie die folgenden Umgebungsvariablen fest, um Bedrock zu aktivieren:

```bash  theme={null}
# Bedrock-Integration aktivieren
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # oder Ihre bevorzugte Region

# Optional: Region für das kleine/schnelle Modell (Haiku) überschreiben
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2

# Optional: Bedrock-Endpunkt-URL für benutzerdefinierte Endpunkte oder Gateways überschreiben
# export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

Beachten Sie beim Aktivieren von Bedrock für Claude Code Folgendes:

* `AWS_REGION` ist eine erforderliche Umgebungsvariable. Claude Code liest diese Einstellung nicht aus der `.aws`-Konfigurationsdatei.
* Bei Verwendung von Bedrock sind die `/login`- und `/logout`-Befehle deaktiviert, da die Authentifizierung über AWS-Anmeldedaten erfolgt.
* Sie können Einstellungsdateien für Umgebungsvariablen wie `AWS_PROFILE` verwenden, die Sie nicht an andere Prozesse weitergeben möchten. Weitere Informationen finden Sie unter [Einstellungen](/de/settings).

### 4. Modellversionen fixieren

<Warning>
  Fixieren Sie spezifische Modellversionen für jede Bereitstellung. Wenn Sie Modellaliase (`sonnet`, `opus`, `haiku`) ohne Fixierung verwenden, versucht Claude Code möglicherweise, eine neuere Modellversion zu verwenden, die in Ihrem Bedrock-Konto nicht verfügbar ist, was bestehende Benutzer unterbricht, wenn Anthropic Updates veröffentlicht.
</Warning>

Legen Sie diese Umgebungsvariablen auf spezifische Bedrock-Modell-IDs fest:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

Diese Variablen verwenden Cross-Region-Inferenzprofil-IDs (mit dem `us.`-Präfix). Wenn Sie ein anderes Regionspräfix oder Anwendungsinferenzprofile verwenden, passen Sie entsprechend an. Aktuelle und ältere Modell-IDs finden Sie unter [Modellübersicht](https://platform.claude.com/docs/en/about-claude/models/overview). Siehe [Modellkonfiguration](/de/model-config#pin-models-for-third-party-deployments) für die vollständige Liste der Umgebungsvariablen.

Claude Code verwendet diese Standardmodelle, wenn keine Fixierungsvariablen gesetzt sind:

| Modelltyp                | Standardwert                                   |
| :----------------------- | :--------------------------------------------- |
| Primäres Modell          | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Kleines/schnelles Modell | `us.anthropic.claude-haiku-4-5-20251001-v1:0`  |

Um Modelle weiter anzupassen, verwenden Sie eine dieser Methoden:

```bash  theme={null}
# Verwendung der Inferenzprofil-ID
export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Verwendung des Anwendungsinferenzprofil-ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Optional: Prompt Caching deaktivieren, falls erforderlich
export DISABLE_PROMPT_CACHING=1
```

<Note>[Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) ist möglicherweise nicht in allen Regionen verfügbar.</Note>

#### Jede Modellversion einem Inferenzprofil zuordnen

Die Umgebungsvariablen `ANTHROPIC_DEFAULT_*_MODEL` konfigurieren ein Inferenzprofil pro Modellfamilie. Wenn Ihre Organisation mehrere Versionen derselben Familie in der `/model`-Auswahl verfügbar machen muss, die jeweils zu ihrem eigenen Anwendungsinferenzprofil-ARN weitergeleitet werden, verwenden Sie stattdessen die `modelOverrides`-Einstellung in Ihrer [Einstellungsdatei](/de/settings#settings-files).

Dieses Beispiel ordnet drei Opus-Versionen unterschiedlichen ARNs zu, damit Benutzer zwischen ihnen wechseln können, ohne die Inferenzprofile Ihrer Organisation zu umgehen:

```json  theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

Wenn ein Benutzer eine dieser Versionen in `/model` auswählt, ruft Claude Code Bedrock mit dem zugeordneten ARN auf. Versionen ohne Überschreibung fallen auf die integrierte Bedrock-Modell-ID oder ein beliebiges übereinstimmendes Inferenzprofil zurück, das beim Start erkannt wird. Siehe [Modell-IDs pro Version überschreiben](/de/model-config#override-model-ids-per-version) für Details, wie Überschreibungen mit `availableModels` und anderen Modelleinstellungen interagieren.

## IAM-Konfiguration

Erstellen Sie eine IAM-Richtlinie mit den erforderlichen Berechtigungen für Claude Code:

```json  theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelAndInferenceProfileAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*",
        "arn:aws:bedrock:*:*:foundation-model/*"
      ]
    },
    {
      "Sid": "AllowMarketplaceSubscription",
      "Effect": "Allow",
      "Action": [
        "aws-marketplace:ViewSubscriptions",
        "aws-marketplace:Subscribe"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:CalledViaLast": "bedrock.amazonaws.com"
        }
      }
    }
  ]
}
```

Für restriktivere Berechtigungen können Sie die Ressource auf spezifische Inferenzprofil-ARNs beschränken.

Weitere Details finden Sie in der [Bedrock IAM-Dokumentation](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

<Note>
  Erstellen Sie ein dediziertes AWS-Konto für Claude Code, um die Kostenverfolgung und Zugriffskontrolle zu vereinfachen.
</Note>

## 1M Token-Kontextfenster

Claude Opus 4.6 und Sonnet 4.6 unterstützen das [1M Token-Kontextfenster](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) auf Amazon Bedrock. Claude Code aktiviert automatisch das erweiterte Kontextfenster, wenn Sie eine 1M-Modellvariante auswählen.

Um das 1M-Kontextfenster für Ihr fixiertes Modell zu aktivieren, hängen Sie `[1m]` an die Modell-ID an. Siehe [Modelle für Drittanbieter-Bereitstellungen fixieren](/de/model-config#pin-models-for-third-party-deployments) für Details.

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) ermöglichen es Ihnen, Inhaltsfilterung für Claude Code zu implementieren. Erstellen Sie einen Guardrail in der [Amazon Bedrock-Konsole](https://console.aws.amazon.com/bedrock/), veröffentlichen Sie eine Version, und fügen Sie dann die Guardrail-Header zu Ihrer [Einstellungsdatei](/de/settings) hinzu. Aktivieren Sie Cross-Region-Inferenz auf Ihrem Guardrail, wenn Sie Cross-Region-Inferenzprofile verwenden.

Beispielkonfiguration:

```json  theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

## Fehlerbehebung

### Authentifizierungsschleife mit SSO und Unternehmens-Proxys

Wenn Browser-Registerkarten wiederholt geöffnet werden, wenn Sie AWS SSO verwenden, entfernen Sie die `awsAuthRefresh`-Einstellung aus Ihrer [Einstellungsdatei](/de/settings). Dies kann auftreten, wenn Unternehmens-VPNs oder TLS-Inspektions-Proxys den SSO-Browser-Flow unterbrechen. Claude Code behandelt die unterbrochene Verbindung als Authentifizierungsfehler, führt `awsAuthRefresh` erneut aus und schleift sich endlos.

Wenn Ihre Netzwerkumgebung automatische browserbasierte SSO-Flows beeinträchtigt, verwenden Sie `aws sso login` manuell, bevor Sie Claude Code starten, anstatt sich auf `awsAuthRefresh` zu verlassen.

### Regionsprobleme

Wenn Sie auf Regionsprobleme stoßen:

* Modellverfügbarkeit prüfen: `aws bedrock list-inference-profiles --region your-region`
* Zu einer unterstützten Region wechseln: `export AWS_REGION=us-east-1`
* Erwägen Sie die Verwendung von Inferenzprofilen für Cross-Region-Zugriff

Wenn Sie einen Fehler „on-demand throughput isn't supported" erhalten:

* Geben Sie das Modell als [Inferenzprofil](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)-ID an

Claude Code verwendet die Bedrock [Invoke API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) und unterstützt die Converse API nicht.

## Zusätzliche Ressourcen

* [Bedrock-Dokumentation](https://docs.aws.amazon.com/bedrock/)
* [Bedrock-Preisgestaltung](https://aws.amazon.com/bedrock/pricing/)
* [Bedrock-Inferenzprofile](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Claude Code auf Amazon Bedrock: Schnellstartanleitung](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Claude Code Monitoring Implementation (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
