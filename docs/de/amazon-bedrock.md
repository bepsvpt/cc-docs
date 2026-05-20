> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code auf Amazon Bedrock

> Erfahren Sie, wie Sie Claude Code über Amazon Bedrock konfigurieren, einschließlich Setup, IAM-Konfiguration und Fehlerbehebung.

export const ContactSalesCard = ({surface}) => {
  const utm = content => `utm_source=claude_code&utm_medium=docs&utm_content=${surface}_${content}`;
  const iconArrowRight = (size = 13) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>;
  const STYLES = `
.cc-cs {
  --cs-slate: #141413;
  --cs-clay: #d97757;
  --cs-clay-deep: #c6613f;
  --cs-gray-000: #ffffff;
  --cs-gray-700: #3d3d3a;
  --cs-border-default: rgba(31, 30, 29, 0.15);
  font-family: inherit;
}
.dark .cc-cs {
  --cs-slate: #f0eee6;
  --cs-gray-000: #262624;
  --cs-gray-700: #bfbdb4;
  --cs-border-default: rgba(240, 238, 230, 0.14);
}
.cc-cs-card {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; padding: 14px 16px; margin: 0;
  background: var(--cs-gray-000); border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; flex-wrap: wrap;
}
.cc-cs-text { font-size: 13px; color: var(--cs-gray-700); line-height: 1.5; flex: 1; min-width: 240px; }
.cc-cs-text strong { font-weight: 550; color: var(--cs-slate); }
.cc-cs-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.cc-cs-btn-clay {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--cs-clay-deep); color: #fff; border: none;
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
  transition: background-color 0.15s; white-space: nowrap;
}
.cc-cs-btn-clay:hover { background: var(--cs-clay); }
.cc-cs-btn-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; color: var(--cs-gray-700);
  border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
}
.cc-cs-btn-ghost:hover { background: rgba(0, 0, 0, 0.04); }
.dark .cc-cs-btn-ghost:hover { background: rgba(255, 255, 255, 0.04); }
@media (max-width: 720px) {
  .cc-cs-actions { width: 100%; }
}
`;
  return <div className="cc-cs not-prose">
      <style>{STYLES}</style>
      <div className="cc-cs-card">
        <div className="cc-cs-text">
          <strong>Deploying Claude Code across your organization?</strong> Talk to sales about enterprise plans, SSO, and centralized billing.
        </div>
        <div className="cc-cs-actions">
          <a href={`https://claude.com/pricing?${utm('view_plans')}#plans-business`} className="cc-cs-btn-ghost">
            View plans
          </a>
          <a href={`https://claude.com/contact-sales?${utm('contact_sales')}`} className="cc-cs-btn-clay">
            Contact sales {iconArrowRight()}
          </a>
        </div>
      </div>
    </div>;
};

<ContactSalesCard surface="bedrock" />

## Voraussetzungen

Bevor Sie Claude Code mit Bedrock konfigurieren, stellen Sie sicher, dass Sie über Folgendes verfügen:

* Ein AWS-Konto mit aktiviertem Bedrock-Zugriff
* Zugriff auf gewünschte Claude-Modelle (z. B. Claude Sonnet 4.6) in Bedrock
* AWS CLI installiert und konfiguriert (optional – nur erforderlich, wenn Sie keinen anderen Mechanismus zur Beschaffung von Anmeldedaten haben)
* Angemessene IAM-Berechtigungen

Um sich mit Ihren eigenen Bedrock-Anmeldedaten anzumelden, folgen Sie [Mit Bedrock anmelden](#sign-in-with-bedrock) unten. Um Claude Code in einem Team bereitzustellen, verwenden Sie die Schritte zum [manuellen Setup](#set-up-manually) und [fixieren Sie Ihre Modellversionen](#4-pin-model-versions), bevor Sie ausrollen.

## Mit Bedrock anmelden

Wenn Sie AWS-Anmeldedaten haben und Claude Code über Bedrock verwenden möchten, führt Sie der Anmelde-Assistent durch den Prozess. Sie führen die AWS-seitigen Voraussetzungen einmal pro Konto durch; der Assistent kümmert sich um die Claude Code-Seite.

<Steps>
  <Step title="Aktivieren Sie Anthropic-Modelle in Ihrem AWS-Konto">
    Öffnen Sie in der [Amazon Bedrock-Konsole](https://console.aws.amazon.com/bedrock/) den Modellkatalog, wählen Sie ein Anthropic-Modell aus und reichen Sie das Anwendungsfallformular ein. Der Zugriff wird unmittelbar nach der Einreichung gewährt. Siehe [Anwendungsfalldetails einreichen](#1-submit-use-case-details) für AWS Organizations und [IAM-Konfiguration](#iam-configuration) für die Berechtigungen, die Ihre Rolle benötigt.
  </Step>

  <Step title="Starten Sie Claude Code und wählen Sie Bedrock">
    Führen Sie `claude` aus. Wählen Sie bei der Anmeldeeingabeaufforderung **3rd-party platform** und dann **Amazon Bedrock**.
  </Step>

  <Step title="Folgen Sie den Assistent-Eingabeaufforderungen">
    Wählen Sie, wie Sie sich bei AWS authentifizieren: ein AWS-Profil, das aus Ihrem `~/.aws`-Verzeichnis erkannt wird, ein Bedrock API-Schlüssel, ein Zugriffsschlüssel und Geheimnis oder Anmeldedaten, die bereits in Ihrer Umgebung vorhanden sind. Der Assistent erkennt Ihre Region, überprüft, welche Claude-Modelle Ihr Konto aufrufen kann, und ermöglicht es Ihnen, diese zu fixieren. Das Ergebnis wird im `env`-Block Ihrer [Benutzereinstellungsdatei](/de/settings) gespeichert, sodass Sie Umgebungsvariablen nicht selbst exportieren müssen.
  </Step>
</Steps>

Nachdem Sie sich angemeldet haben, führen Sie `/setup-bedrock` jederzeit aus, um den Assistenten erneut zu öffnen und Ihre Anmeldedaten, Region oder Modellpins zu ändern.

## Manuelles Setup

Um Bedrock über Umgebungsvariablen statt über den Assistenten zu konfigurieren, z. B. in CI oder einem skriptgesteuerten Enterprise-Rollout, folgen Sie den folgenden Schritten.

### 1. Anwendungsfalldetails einreichen

Erstmalige Benutzer von Anthropic-Modellen müssen Anwendungsfalldetails einreichen, bevor sie ein Modell aufrufen. Dies wird einmal pro AWS-Konto durchgeführt.

1. Stellen Sie sicher, dass Sie die unten beschriebenen richtigen IAM-Berechtigungen haben
2. Navigieren Sie zur [Amazon Bedrock-Konsole](https://console.aws.amazon.com/bedrock/)
3. Wählen Sie ein Anthropic-Modell aus dem **Modellkatalog**
4. Füllen Sie das Anwendungsfallformular aus. Der Zugriff wird unmittelbar nach der Einreichung gewährt.

Wenn Sie AWS Organizations verwenden, können Sie das Formular einmal vom Verwaltungskonto aus mit der [`PutUseCaseForModelAccess` API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html) einreichen. Dieser Aufruf erfordert die `bedrock:PutUseCaseForModelAccess` IAM-Berechtigung. Die Genehmigung erstreckt sich automatisch auf untergeordnete Konten.

### 2. AWS-Anmeldedaten konfigurieren

Claude Code verwendet die Standard-AWS-SDK-Anmeldedatenkette. Richten Sie Ihre Anmeldedaten mit einer dieser Methoden ein:

**Option A: AWS CLI-Konfiguration**

```bash theme={null}
aws configure
```

**Option B: Umgebungsvariablen (Zugriffsschlüssel)**

```bash theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**Option C: Umgebungsvariablen (SSO-Profil)**

```bash theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**Option D: AWS Management Console-Anmeldedaten**

```bash theme={null}
aws login
```

[Erfahren Sie mehr](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) über `aws login`.

**Option E: Bedrock API-Schlüssel**

```bash theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Bedrock API-Schlüssel bieten eine einfachere Authentifizierungsmethode ohne vollständige AWS-Anmeldedaten. [Erfahren Sie mehr über Bedrock API-Schlüssel](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### Erweiterte Anmeldedatenkonfiguration

Claude Code unterstützt die automatische Aktualisierung von Anmeldedaten für AWS SSO und Unternehmensidentitätsanbieter. Fügen Sie diese Einstellungen zu Ihrer Claude Code-Einstellungsdatei hinzu (siehe [Einstellungen](/de/settings) für Dateispeicherorte).

Diese zwei Einstellungen haben unterschiedliche Auslösebedingungen:

* **`awsAuthRefresh`**: wird nur ausgeführt, wenn Claude Code erkennt, dass Ihre AWS-Anmeldedaten abgelaufen sind, entweder lokal basierend auf ihrem Zeitstempel oder wenn Bedrock einen Anmeldedatenfehler zurückgibt, und versucht dann die Anfrage mit aktualisierten Anmeldedaten erneut.
* **`awsCredentialExport`**: wird beim Sitzungsstart und bei jeder Anmeldedatenaktualisierung ausgeführt, auch wenn die Anmeldedaten in Ihrer AWS-Standard-Anmeldedatenkette noch gültig sind. Verwenden Sie dies, wenn Ihr Bedrock-Konto Cross-Account-Anmeldedaten erfordert, die sich von denen unterscheiden, die die Standard-Anmeldedatenkette auflösen würde.

##### Beispielkonfiguration

```json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### Erklärung der Konfigurationseinstellungen

**`awsAuthRefresh`**: Verwenden Sie dies für Befehle, die das `.aws`-Verzeichnis ändern, z. B. zum Aktualisieren von Anmeldedaten, SSO-Cache oder Konfigurationsdateien. Die Ausgabe des Befehls wird dem Benutzer angezeigt, aber interaktive Eingaben werden nicht unterstützt. Dies funktioniert gut für browserbasierte SSO-Flows, bei denen die CLI eine URL oder einen Code anzeigt und Sie die Authentifizierung im Browser abschließen.

**`awsCredentialExport`**: Verwenden Sie dies nur, wenn Sie das `.aws`-Verzeichnis nicht ändern können und Anmeldedaten direkt zurückgeben müssen. Dieser Befehl wird ausgeführt, wenn Anmeldedaten aktualisiert werden müssen, nicht nur wenn Anmeldedaten abgelaufen sind. Die Ausgabe wird stillschweigend erfasst und nicht dem Benutzer angezeigt. Der Befehl muss JSON in diesem Format ausgeben:

```json theme={null}
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

```bash theme={null}
# Bedrock-Integration aktivieren
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # oder Ihre bevorzugte Region

# Optional: Region für das kleine/schnelle Modell (Bedrock und Mantle) überschreiben.
# Auf Bedrock hat dies keine Auswirkung ohne ANTHROPIC_DEFAULT_HAIKU_MODEL
# oder das veraltete ANTHROPIC_SMALL_FAST_MODEL gesetzt.
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
  Fixieren Sie spezifische Modellversionen bei der Bereitstellung für mehrere Benutzer. Ohne Fixierung werden Modellaliase wie `sonnet` und `opus` zur neuesten Version aufgelöst, die möglicherweise noch nicht in Ihrem Bedrock-Konto verfügbar ist, wenn Anthropic ein Update veröffentlicht. Claude Code [fällt beim Start](#startup-model-checks) auf die vorherige Version zurück, wenn die neueste nicht verfügbar ist, aber die Fixierung ermöglicht es Ihnen, zu kontrollieren, wann Ihre Benutzer zu einem neuen Modell wechseln.
</Warning>

Legen Sie diese Umgebungsvariablen auf spezifische Bedrock-Modell-IDs fest.

Ohne `ANTHROPIC_DEFAULT_OPUS_MODEL` wird der `opus`-Alias auf Bedrock zu Opus 4.6 aufgelöst. Legen Sie ihn auf die Opus 4.7-ID fest, um das neueste Modell zu verwenden:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

Diese Variablen verwenden Cross-Region-Inferenzprofil-IDs (mit dem `us.`-Präfix). Wenn Sie ein anderes Regionspräfix oder Anwendungsinferenzprofile verwenden, passen Sie entsprechend an. Aktuelle und ältere Modell-IDs finden Sie unter [Modellübersicht](https://platform.claude.com/docs/en/about-claude/models/overview). Siehe [Modellkonfiguration](/de/model-config#pin-models-for-third-party-deployments) für die vollständige Liste der Umgebungsvariablen.

Claude Code verwendet diese Standardmodelle, wenn keine Fixierungsvariablen gesetzt sind:

| Modelltyp                | Standardwert                                   |
| :----------------------- | :--------------------------------------------- |
| Primäres Modell          | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Kleines/schnelles Modell | Gleich wie primäres Modell                     |

Hintergrundaufgaben wie die Generierung von Sitzungstiteln verwenden das kleine/schnelle Modell, normalerweise ein Haiku-Klasse-Modell. Auf Bedrock setzt Claude Code dies standardmäßig auf das primäre Modell, da Haiku möglicherweise nicht in jedem Konto oder jeder Region aktiviert ist. Um Haiku für Hintergrundaufgaben zu verwenden, legen Sie `ANTHROPIC_DEFAULT_HAIKU_MODEL` auf eine Modell-ID fest, die in Ihrem Konto verfügbar ist.

Um Modelle weiter anzupassen, verwenden Sie eine dieser Methoden:

```bash theme={null}
# Verwendung der Inferenzprofil-ID
export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Verwendung des Anwendungsinferenzprofil-ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Optional: Prompt Caching deaktivieren, falls erforderlich
export DISABLE_PROMPT_CACHING=1

# Optional: 1-Stunden-Prompt-Cache-TTL statt der 5-Minuten-Standard anfordern
export ENABLE_PROMPT_CACHING_1H=1
```

Die 1-Stunden-Cache-TTL wird mit einer höheren Rate als die 5-Minuten-Standard abgerechnet. Siehe [Cache-Lebensdauer](/de/prompt-caching#cache-lifetime).

<Note>Prompt Caching ist möglicherweise nicht in allen Bedrock-Regionen verfügbar. Wenn die Cache-Token-Zählungen bei Null bleiben, überprüfen Sie [unterstützte Modelle, Regionen und Limits](https://docs.aws.amazon.com/bedrock/latest/userguide/prompt-caching.html#prompt-caching-models) in der Bedrock-Dokumentation.</Note>

#### Jede Modellversion einem Inferenzprofil zuordnen

Die Umgebungsvariablen `ANTHROPIC_DEFAULT_*_MODEL` konfigurieren ein Inferenzprofil pro Modellfamilie. Wenn Ihre Organisation mehrere Versionen derselben Familie in der `/model`-Auswahl verfügbar machen muss, die jeweils zu ihrem eigenen Anwendungsinferenzprofil-ARN weitergeleitet werden, verwenden Sie stattdessen die `modelOverrides`-Einstellung in Ihrer [Einstellungsdatei](/de/settings#settings-files).

Dieses Beispiel ordnet vier Opus-Versionen unterschiedlichen ARNs zu, damit Benutzer zwischen ihnen wechseln können, ohne die Inferenzprofile Ihrer Organisation zu umgehen:

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-47-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

Wenn ein Benutzer eine dieser Versionen in `/model` auswählt, ruft Claude Code Bedrock mit dem zugeordneten ARN auf. Versionen ohne Überschreibung fallen auf die integrierte Bedrock-Modell-ID oder ein beliebiges übereinstimmendes Inferenzprofil zurück, das beim Start erkannt wird. Siehe [Modell-IDs pro Version überschreiben](/de/model-config#override-model-ids-per-version) für Details, wie Überschreibungen mit `availableModels` und anderen Modelleinstellungen interagieren.

## Startup-Modellprüfungen

Wenn Claude Code mit konfiguriertem Bedrock startet, überprüft es, dass die Modelle, die es verwenden möchte, in Ihrem Konto zugänglich sind. Diese Prüfung erfordert Claude Code v2.1.94 oder später.

Wenn Sie eine Modellversion fixiert haben, die älter ist als der aktuelle Claude Code-Standard, und Ihr Konto die neuere Version aufrufen kann, fordert Claude Code Sie auf, die Fixierung zu aktualisieren. Das Akzeptieren schreibt die neue Modell-ID in Ihre [Benutzereinstellungsdatei](/de/settings) und startet Claude Code neu. Das Ablehnen wird bis zur nächsten Standardversionänderung beibehalten. Fixierungen, die auf einen [Anwendungsinferenzprofil-ARN](#map-each-model-version-to-an-inference-profile) verweisen, werden übersprungen, da diese von Ihrem Administrator verwaltet werden.

Wenn Sie ein Modell nicht fixiert haben und der aktuelle Standard in Ihrem Konto nicht verfügbar ist, fällt Claude Code für die aktuelle Sitzung auf die vorherige Version zurück und zeigt einen Hinweis an. Das Fallback wird nicht beibehalten. Aktivieren Sie das neuere Modell in Ihrem Bedrock-Konto oder [fixieren Sie eine Version](#4-pin-model-versions), um die Auswahl dauerhaft zu machen.

## IAM-Konfiguration

Erstellen Sie eine IAM-Richtlinie mit den erforderlichen Berechtigungen für Claude Code:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelAndInferenceProfileAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles",
        "bedrock:GetInferenceProfile"
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

`bedrock:GetInferenceProfile` ermöglicht es Claude Code, eine [Anwendungs-Inferenzprofil-ARN](#map-each-model-version-to-an-inference-profile) in ihr zugrunde liegendes Foundation-Modell aufzulösen, das verwendet wird, um die richtige Anforderungsform für dieses Modell auszuwählen.

Wenn dem Token diese Berechtigung fehlt, wird Claude Code automatisch wiederhergestellt, indem es einmal mit der alternativen Form erneut versucht wird, sodass Anfragen weiterhin erfolgreich sind, aber jedes neue Modell einen zusätzlichen Roundtrip hinzufügt. Die Gewährung der Berechtigung vermeidet den Wiederholungsversuch. Dies gilt am häufigsten für `AWS_BEARER_TOKEN_BEDROCK`-Bereitstellungen, bei denen die Richtlinie des Tokens typischerweise enger ist als eine vollständige IAM-Rolle.

Weitere Details finden Sie in der [Bedrock IAM-Dokumentation](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

<Note>
  Erstellen Sie ein dediziertes AWS-Konto für Claude Code, um die Kostenverfolgung und Zugriffskontrolle zu vereinfachen.
</Note>

## 1M Token-Kontextfenster

Claude Opus 4.7, Opus 4.6 und Sonnet 4.6 unterstützen das [1M Token-Kontextfenster](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) auf Amazon Bedrock. Claude Code aktiviert automatisch das erweiterte Kontextfenster, wenn Sie eine 1M-Modellvariante auswählen.

Der [Setup-Assistent](#sign-in-with-bedrock) bietet eine 1M-Kontextoption, wenn er Modelle fixiert. Um es stattdessen für ein manuell fixiertes Modell zu aktivieren, hängen Sie `[1m]` an die Modell-ID an. Siehe [Modelle für Drittanbieter-Bereitstellungen fixieren](/de/model-config#pin-models-for-third-party-deployments) für Details.

## Service-Tiers

[Amazon Bedrock Service-Tiers](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html) ermöglichen es Ihnen, Kosten gegen Latenz abzuwägen. Legen Sie `ANTHROPIC_BEDROCK_SERVICE_TIER` auf `default`, `flex` oder `priority` fest:

```bash theme={null}
export ANTHROPIC_BEDROCK_SERVICE_TIER=priority
```

Claude Code sendet dies als `X-Amzn-Bedrock-Service-Tier`-Header bei jeder Anfrage. Die Tier-Verfügbarkeit variiert je nach Modell und Region. Reservierte Kapazität verwendet einen [bereitgestellten Durchsatz](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html)-ARN als Modell-ID statt dieser Einstellung.

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) ermöglichen es Ihnen, Inhaltsfilterung für Claude Code zu implementieren. Erstellen Sie einen Guardrail in der [Amazon Bedrock-Konsole](https://console.aws.amazon.com/bedrock/), veröffentlichen Sie eine Version, und fügen Sie dann die Guardrail-Header zu Ihrer [Einstellungsdatei](/de/settings) hinzu. Aktivieren Sie Cross-Region-Inferenz auf Ihrem Guardrail, wenn Sie Cross-Region-Inferenzprofile verwenden.

Beispielkonfiguration:

```json theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

## Verwenden Sie den Mantle-Endpunkt

Mantle ist ein Amazon Bedrock-Endpunkt, der Claude-Modelle über die native Anthropic API-Form statt über die Bedrock Invoke API bereitstellt. Er verwendet die gleichen AWS-Anmeldedaten, IAM-Berechtigungen und `awsAuthRefresh`-Konfiguration, die weiter oben auf dieser Seite beschrieben sind.

<Note>
  Mantle erfordert Claude Code v2.1.94 oder später. Führen Sie `claude --version` aus, um zu überprüfen.
</Note>

### Aktivieren Sie Mantle

Mit bereits konfigurierten AWS-Anmeldedaten legen Sie `CLAUDE_CODE_USE_MANTLE` fest, um Anfragen zum Mantle-Endpunkt weiterzuleiten:

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export AWS_REGION=us-east-1
```

Claude Code erstellt die Endpunkt-URL aus `AWS_REGION`. Um sie für einen benutzerdefinierten Endpunkt oder ein Gateway zu überschreiben, legen Sie `ANTHROPIC_BEDROCK_MANTLE_BASE_URL` fest.

Führen Sie `/status` in Claude Code aus, um zu bestätigen. Die Provider-Zeile zeigt `Amazon Bedrock (Mantle)`, wenn Mantle aktiv ist.

### Wählen Sie ein Mantle-Modell

Mantle verwendet Modell-IDs mit dem Präfix `anthropic.` und ohne Versionssuffix, z. B. `anthropic.claude-haiku-4-5`. Die Modelle, die Ihrem Konto zur Verfügung stehen, hängen davon ab, was Ihre Organisation erhalten hat; zusätzliche Modell-IDs sind in Ihren Onboarding-Materialien von AWS aufgeführt. Wenden Sie sich an Ihr AWS-Kontoteam, um Zugriff auf zulässige Modelle anzufordern.

Legen Sie das Modell mit dem `--model`-Flag oder mit `/model` in Claude Code fest:

```bash theme={null}
claude --model anthropic.claude-haiku-4-5
```

### Führen Sie Mantle neben der Invoke API aus

Die Modelle, die Ihnen auf Mantle zur Verfügung stehen, enthalten möglicherweise nicht alle Modelle, die Sie heute verwenden. Das Setzen von `CLAUDE_CODE_USE_BEDROCK` und `CLAUDE_CODE_USE_MANTLE` ermöglicht es Claude Code, beide Endpunkte aus derselben Sitzung aufzurufen. Modell-IDs, die dem Mantle-Format entsprechen, werden zu Mantle weitergeleitet, und alle anderen Modell-IDs gehen zur Bedrock Invoke API.

```bash theme={null}
export CLAUDE_CODE_USE_BEDROCK=1
export CLAUDE_CODE_USE_MANTLE=1
```

Um ein Mantle-Modell in der `/model`-Auswahl anzuzeigen, listen Sie seine ID in `availableModels` in Ihrer [Einstellungsdatei](/de/settings) auf. Diese Einstellung beschränkt die Auswahl auch auf die aufgelisteten Einträge, daher sollten Sie jeden Alias einschließen, den Sie verfügbar halten möchten:

```json theme={null}
{
  "availableModels": ["opus", "sonnet", "haiku", "anthropic.claude-haiku-4-5"]
}
```

Einträge mit dem `anthropic.`-Präfix werden als benutzerdefinierte Auswahl-Optionen hinzugefügt und zu Mantle weitergeleitet. Ersetzen Sie `anthropic.claude-haiku-4-5` durch die Modell-ID, die Ihr Konto erhalten hat. Siehe [Modellauswahl einschränken](/de/model-config#restrict-model-selection) für Details, wie `availableModels` mit anderen Modelleinstellungen interagiert.

Wenn beide Provider aktiv sind, zeigt `/status` `Amazon Bedrock + Amazon Bedrock (Mantle)` an.

### Leiten Sie Mantle durch ein Gateway weiter

Wenn Ihre Organisation Modellverkehr durch ein zentralisiertes [LLM-Gateway](/de/llm-gateway) leitet, das AWS-Anmeldedaten serverseitig injiziert, deaktivieren Sie die clientseitige Authentifizierung, damit Claude Code Anfragen ohne SigV4-Signaturen oder `x-api-key`-Header sendet:

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export CLAUDE_CODE_SKIP_MANTLE_AUTH=1
export ANTHROPIC_BEDROCK_MANTLE_BASE_URL=https://your-gateway.example.com
```

### Mantle-Umgebungsvariablen

Diese Variablen sind spezifisch für den Mantle-Endpunkt. Siehe [Umgebungsvariablen](/de/env-vars) für die vollständige Liste.

| Variable                                | Zweck                                                                                |
| :-------------------------------------- | :----------------------------------------------------------------------------------- |
| `CLAUDE_CODE_USE_MANTLE`                | Aktivieren Sie den Mantle-Endpunkt. Legen Sie auf `1` oder `true` fest.              |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`     | Überschreiben Sie die Standard-Mantle-Endpunkt-URL                                   |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH`          | Überspringen Sie die clientseitige Authentifizierung für Proxy-Setups                |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | Überschreiben Sie die AWS-Region für das Haiku-Klasse-Modell (gemeinsam mit Bedrock) |

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

### Mantle-Endpunkt-Fehler

Wenn `/status` nach dem Setzen von `CLAUDE_CODE_USE_MANTLE` nicht `Amazon Bedrock (Mantle)` anzeigt, erreicht die Variable den Prozess nicht. Bestätigen Sie, dass sie in der Shell exportiert wird, in der Sie `claude` gestartet haben, oder legen Sie sie im `env`-Block Ihrer [Einstellungsdatei](/de/settings) fest.

Ein `403` vom Mantle-Endpunkt mit gültigen Anmeldedaten bedeutet, dass Ihrem AWS-Konto kein Zugriff auf das angeforderte Modell gewährt wurde. Wenden Sie sich an Ihr AWS-Kontoteam, um Zugriff anzufordern.

Ein `400`, das die Modell-ID nennt, bedeutet, dass dieses Modell nicht auf Mantle bereitgestellt wird. Mantle hat sein eigenes Modell-Lineup, das vom Standard-Bedrock-Katalog getrennt ist, daher funktionieren Inferenzprofil-IDs wie `us.anthropic.claude-sonnet-4-6` nicht. Verwenden Sie eine Mantle-Format-ID, oder aktivieren Sie [beide Endpunkte](#run-mantle-alongside-the-invoke-api), damit Claude Code jede Anfrage zum Endpunkt weiterleitet, wo das Modell verfügbar ist.

## Zusätzliche Ressourcen

* [Bedrock-Dokumentation](https://docs.aws.amazon.com/bedrock/)
* [Bedrock-Preisgestaltung](https://aws.amazon.com/bedrock/pricing/)
* [Bedrock-Inferenzprofile](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Bedrock-Token-Burndown und Kontingente](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-token-burndown.html)
* [Claude Code auf Amazon Bedrock: Schnellstartanleitung](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Claude Code Monitoring Implementation (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
