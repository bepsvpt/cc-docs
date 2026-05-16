> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code auf Google Vertex AI

> Erfahren Sie, wie Sie Claude Code über Google Vertex AI konfigurieren, einschließlich Setup, IAM-Konfiguration und Fehlerbehebung.

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

<ContactSalesCard surface="vertex" />

## Voraussetzungen

Bevor Sie Claude Code mit Vertex AI konfigurieren, stellen Sie sicher, dass Sie über Folgendes verfügen:

* Ein Google Cloud Platform (GCP)-Konto mit aktivierter Abrechnung
* Ein GCP-Projekt mit aktivierter Vertex AI API
* Zugriff auf gewünschte Claude-Modelle (z. B. Claude Sonnet 4.6)
* Google Cloud SDK (`gcloud`) installiert und konfiguriert
* Kontingent im gewünschten GCP-Bereich zugewiesen

Um sich mit Ihren eigenen Vertex AI-Anmeldedaten anzumelden, folgen Sie [Anmelden mit Vertex AI](#sign-in-with-vertex-ai) unten. Um Claude Code in einem Team bereitzustellen, verwenden Sie die Schritte zum [manuellen Setup](#set-up-manually) und [fixieren Sie Ihre Modellversionen](#5-pin-model-versions), bevor Sie ausrollen.

## Anmelden mit Vertex AI

Wenn Sie Google Cloud-Anmeldedaten haben und Claude Code über Vertex AI verwenden möchten, führt Sie der Anmeldeasistent durch den Prozess. Sie führen die GCP-seitigen Voraussetzungen einmal pro Projekt durch; der Assistent kümmert sich um die Claude Code-Seite.

<Note>
  Der Vertex AI-Setup-Assistent erfordert Claude Code v2.1.98 oder später. Führen Sie `claude --version` aus, um dies zu überprüfen.
</Note>

<Steps>
  <Step title="Aktivieren Sie Claude-Modelle in Ihrem GCP-Projekt">
    [Aktivieren Sie die Vertex AI API](#1-enable-vertex-ai-api) für Ihr Projekt, und fordern Sie dann Zugriff auf die Claude-Modelle an, die Sie im [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) möchten. Siehe [IAM-Konfiguration](#iam-configuration) für die Berechtigungen, die Ihr Konto benötigt.
  </Step>

  <Step title="Starten Sie Claude Code und wählen Sie Vertex AI">
    Führen Sie `claude` aus. Wählen Sie bei der Anmeldeeingabeaufforderung **3rd-party platform** und dann **Google Vertex AI**.
  </Step>

  <Step title="Folgen Sie den Eingabeaufforderungen des Assistenten">
    Wählen Sie, wie Sie sich bei Google Cloud authentifizieren: Application Default Credentials von `gcloud`, eine Service-Account-Schlüsseldatei oder Anmeldedaten, die bereits in Ihrer Umgebung vorhanden sind. Der Assistent erkennt Ihr Projekt und Ihre Region, überprüft, welche Claude-Modelle Ihr Projekt aufrufen kann, und ermöglicht es Ihnen, diese zu fixieren. Das Ergebnis wird im `env`-Block Ihrer [Benutzereinstellungsdatei](/de/settings) gespeichert, sodass Sie Umgebungsvariablen nicht selbst exportieren müssen.
  </Step>
</Steps>

Nachdem Sie sich angemeldet haben, führen Sie `/setup-vertex` jederzeit aus, um den Assistenten erneut zu öffnen und Ihre Anmeldedaten, Ihr Projekt, Ihre Region oder Ihre Modellpins zu ändern.

## Regionskonfiguration

Claude Code unterstützt Vertex AI [globale](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai), Multi-Region- und regionale Endpunkte. Legen Sie `CLOUD_ML_REGION` auf `global`, einen Multi-Region-Standort wie `eu` oder `us` oder eine bestimmte Region wie `us-east5` fest. Claude Code wählt den korrekten Vertex AI-Hostnamen für jedes Formular aus, einschließlich der Hosts `aiplatform.eu.rep.googleapis.com` und `aiplatform.us.rep.googleapis.com` für Multi-Region-Standorte.

<Note>
  Vertex AI unterstützt möglicherweise die Claude Code-Standardmodelle nicht auf jedem Endpunkttyp. Die Modellverfügbarkeit variiert je nach [spezifischen Regionen](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models), Multi-Region-Standorten und [globalen Endpunkten](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models). Möglicherweise müssen Sie zu einem unterstützten Standort wechseln oder ein unterstütztes Modell angeben.
</Note>

## Manuelles Setup

Um Vertex AI über Umgebungsvariablen statt über den Assistenten zu konfigurieren, z. B. in CI oder einem skriptgesteuerten Enterprise-Rollout, folgen Sie den folgenden Schritten.

### 1. Aktivieren Sie die Vertex AI API

Aktivieren Sie die Vertex AI API in Ihrem GCP-Projekt:

```bash theme={null}
# Legen Sie Ihre Projekt-ID fest
gcloud config set project YOUR-PROJECT-ID

# Aktivieren Sie die Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

### 2. Fordern Sie Modellzugriff an

Fordern Sie Zugriff auf Claude-Modelle in Vertex AI an:

1. Navigieren Sie zum [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Suchen Sie nach 'Claude"-Modellen
3. Fordern Sie Zugriff auf gewünschte Claude-Modelle an (z. B. Claude Sonnet 4.6)
4. Warten Sie auf Genehmigung (kann 24–48 Stunden dauern)

### 3. Konfigurieren Sie GCP-Anmeldedaten

Claude Code verwendet die standardmäßige Google Cloud-Authentifizierung.

Weitere Informationen finden Sie in der [Google Cloud-Authentifizierungsdokumentation](https://cloud.google.com/docs/authentication).

Claude Code v2.1.121 oder später unterstützt [X.509-zertifikatbasierte Workload Identity Federation](https://cloud.google.com/iam/docs/workload-identity-federation-with-x509-certificates) über die gleiche Application Default Credentials-Kette. Legen Sie `GOOGLE_APPLICATION_CREDENTIALS` auf den Pfad Ihrer Anmeldedaten-Konfigurationsdatei fest.

<Note>
  Claude Code verwendet `ANTHROPIC_VERTEX_PROJECT_ID` als die Projekt-ID für Vertex AI-Anfragen. Die Umgebungsvariablen `GCLOUD_PROJECT` und `GOOGLE_CLOUD_PROJECT` sowie die Anmeldedatei, auf die `GOOGLE_APPLICATION_CREDENTIALS` verweist, haben Vorrang vor ihr. Wenn keine dieser Optionen gesetzt sind, wird die Projekt-ID aus Ihrer `gcloud`-Konfiguration oder dem angehängten Service-Konto aufgelöst.
</Note>

#### Erweiterte Anmeldedaten-Konfiguration

Claude Code unterstützt die automatische Aktualisierung von Anmeldedaten für GCP über die Einstellung `gcpAuthRefresh`. Wenn Claude Code erkennt, dass Ihre GCP-Anmeldedaten abgelaufen sind oder nicht geladen werden können, führt es den konfigurierten Befehl aus, um neue Anmeldedaten zu erhalten, bevor die Anfrage erneut versucht wird.

```json theme={null}
{
  "gcpAuthRefresh": "gcloud auth application-default login",
  "env": {
    "ANTHROPIC_VERTEX_PROJECT_ID": "your-project-id"
  }
}
```

Die Ausgabe des Befehls wird dem Benutzer angezeigt, aber interaktive Eingaben werden nicht unterstützt. Dies funktioniert gut für browserbasierte Authentifizierungsabläufe, bei denen die CLI eine URL anzeigt und Sie die Authentifizierung im Browser abschließen. Der Aktualisierungsbefehl läuft nach drei Minuten ab, wenn die Authentifizierung nicht abgeschlossen ist. Wenn Sie `gcpAuthRefresh` in Projekteinstellungen wie `.claude/settings.json` festlegen, wird der Befehl nur ausgeführt, nachdem Sie die Workspace-Vertrauensaufforderung akzeptiert haben.

### 4. Konfigurieren Sie Claude Code

Legen Sie die folgenden Umgebungsvariablen fest:

```bash theme={null}
# Aktivieren Sie die Vertex AI-Integration
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Optional: Überschreiben Sie die Vertex-Endpunkt-URL für benutzerdefinierte Endpunkte oder Gateways
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# Optional: Deaktivieren Sie Prompt Caching bei Bedarf
export DISABLE_PROMPT_CACHING=1

# Optional: Fordern Sie eine 1-Stunden-Prompt-Cache-TTL statt des 5-Minuten-Standards an
export ENABLE_PROMPT_CACHING_1H=1

# Wenn CLOUD_ML_REGION=global, überschreiben Sie die Region für Modelle, die keine globalen Endpunkte unterstützen
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

Die meisten Modellversionen haben eine entsprechende `VERTEX_REGION_CLAUDE_*`-Variable. Siehe die [Referenz für Umgebungsvariablen](/de/env-vars) für die vollständige Liste. Überprüfen Sie [Vertex Model Garden](https://console.cloud.google.com/vertex-ai/model-garden), um zu bestimmen, welche Modelle globale Endpunkte versus nur regionale Endpunkte unterstützen.

[Prompt Caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) wird automatisch aktiviert. Um es zu deaktivieren, legen Sie `DISABLE_PROMPT_CACHING=1` fest. Um eine 1-Stunden-Cache-TTL statt des 5-Minuten-Standards anzufordern, legen Sie `ENABLE_PROMPT_CACHING_1H=1` fest; Cache-Schreibvorgänge mit einer 1-Stunden-TTL werden mit einem höheren Satz abgerechnet. Für erhöhte Ratenlimits wenden Sie sich an den Google Cloud-Support. Bei Verwendung von Vertex AI sind die Befehle `/login` und `/logout` deaktiviert, da die Authentifizierung über Google Cloud-Anmeldedaten erfolgt.

Claude Code deaktiviert [MCP-Toolsuche](/de/mcp#scale-with-mcp-tool-search) standardmäßig auf Vertex AI, sodass MCP-Tool-Definitionen beim Start geladen werden. Vertex AI unterstützt Toolsuche für Claude Sonnet 4.5 und später sowie Claude Opus 4.5 und später. Legen Sie `ENABLE_TOOL_SEARCH=true` fest, um sie auf diesen Modellen zu aktivieren. Frühere Modelle auf Vertex AI akzeptieren den erforderlichen Beta-Header nicht, und Anfragen schlagen fehl, wenn Sie die Toolsuche mit ihnen aktivieren.

### 5. Fixieren Sie Modellversionen

<Warning>
  Fixieren Sie spezifische Modellversionen bei der Bereitstellung für mehrere Benutzer. Ohne Fixierung werden Modellaliase wie `sonnet` und `opus` zur neuesten Version aufgelöst, die möglicherweise noch nicht in Ihrem Vertex AI-Projekt aktiviert ist, wenn Anthropic ein Update veröffentlicht. Claude Code [fällt zurück](#startup-model-checks) beim Start zur vorherigen Version zurück, wenn die neueste nicht verfügbar ist, aber das Fixieren ermöglicht es Ihnen, zu kontrollieren, wann Ihre Benutzer zu einem neuen Modell wechseln.
</Warning>

Legen Sie diese Umgebungsvariablen auf spezifische Vertex AI-Modell-IDs fest.

Ohne `ANTHROPIC_DEFAULT_OPUS_MODEL` wird der `opus`-Alias auf Vertex zu Opus 4.6 aufgelöst. Legen Sie ihn auf die Opus 4.7-ID fest, um das neueste Modell zu verwenden:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

Aktuelle und ältere Modell-IDs finden Sie unter [Modellübersicht](https://platform.claude.com/docs/en/about-claude/models/overview). Siehe [Modellkonfiguration](/de/model-config#pin-models-for-third-party-deployments) für die vollständige Liste der Umgebungsvariablen.

Claude Code verwendet diese Standardmodelle, wenn keine Fixierungsvariablen gesetzt sind:

| Modelltyp                | Standardwert                 |
| :----------------------- | :--------------------------- |
| Primäres Modell          | `claude-sonnet-4-5@20250929` |
| Kleines/schnelles Modell | Gleich wie primäres Modell   |

Hintergrundaufgaben wie die Generierung von Sitzungstiteln verwenden das kleine/schnelle Modell, normalerweise ein Haiku-Klasse-Modell. Auf Vertex AI setzt Claude Code dies standardmäßig auf das primäre Modell, da Haiku möglicherweise nicht in jedem Projekt oder jeder Region aktiviert ist. Um Haiku für Hintergrundaufgaben zu verwenden, legen Sie `ANTHROPIC_DEFAULT_HAIKU_MODEL` auf eine Modell-ID fest, die in Ihrem Projekt verfügbar ist.

Um Modelle weiter anzupassen:

```bash theme={null}
export ANTHROPIC_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

## Startmodellprüfungen

Wenn Claude Code mit konfiguriertem Vertex AI startet, überprüft es, dass die Modelle, die es verwenden möchte, in Ihrem Projekt zugänglich sind. Diese Prüfung erfordert Claude Code v2.1.98 oder später.

Wenn Sie eine Modellversion fixiert haben, die älter als der aktuelle Claude Code-Standard ist, und Ihr Projekt die neuere Version aufrufen kann, fordert Claude Code Sie auf, die Fixierung zu aktualisieren. Das Akzeptieren schreibt die neue Modell-ID in Ihre [Benutzereinstellungsdatei](/de/settings) und startet Claude Code neu. Das Ablehnen wird bis zur nächsten Standardversionänderung beibehalten.

Wenn Sie ein Modell nicht fixiert haben und der aktuelle Standard in Ihrem Projekt nicht verfügbar ist, fällt Claude Code für die aktuelle Sitzung zur vorherigen Version zurück und zeigt einen Hinweis an. Das Fallback wird nicht beibehalten. Aktivieren Sie das neuere Modell im [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) oder [fixieren Sie eine Version](#5-pin-model-versions), um die Auswahl dauerhaft zu machen.

## IAM-Konfiguration

Weisen Sie die erforderlichen IAM-Berechtigungen zu:

Die Rolle `roles/aiplatform.user` umfasst die erforderlichen Berechtigungen:

* `aiplatform.endpoints.predict` - Erforderlich für Modellaufrufe und Token-Zählung

Für restriktivere Berechtigungen erstellen Sie eine benutzerdefinierte Rolle nur mit den oben genannten Berechtigungen.

Weitere Informationen finden Sie in der [Vertex IAM-Dokumentation](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Erstellen Sie ein dediziertes GCP-Projekt für Claude Code, um die Kostenverfolgung und Zugriffskontrolle zu vereinfachen.
</Note>

## 1M-Token-Kontextfenster

Claude Opus 4.7, Opus 4.6 und Sonnet 4.6 unterstützen das [1M-Token-Kontextfenster](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) auf Vertex AI. Claude Code aktiviert automatisch das erweiterte Kontextfenster, wenn Sie eine 1M-Modellvariante auswählen.

Der [Setup-Assistent](#sign-in-with-vertex-ai) bietet eine 1M-Kontextoption an, wenn er Modelle fixiert. Um es stattdessen für ein manuell fixiertes Modell zu aktivieren, hängen Sie `[1m]` an die Modell-ID an. Siehe [Modelle für Drittanbieter-Bereitstellungen fixieren](/de/model-config#pin-models-for-third-party-deployments) für Details.

## Fehlerbehebung

Wenn Sie auf Fehler „Could not load the default credentials" stoßen:

* Führen Sie `gcloud auth application-default login` aus, um Application Default Credentials einzurichten
* Setzen Sie `GOOGLE_APPLICATION_CREDENTIALS` auf einen Pfad zu einer Service-Account-Schlüsseldatei
* Siehe [GCP-Anmeldedaten konfigurieren](#3-configure-gcp-credentials) für alle Optionen

Wenn Sie auf Kontingentprobleme stoßen:

* Überprüfen Sie aktuelle Kontingente oder fordern Sie eine Kontingenterhöhung über die [Cloud Console](https://cloud.google.com/docs/quotas/view-manage) an

Wenn Sie auf Fehler „Modell nicht gefunden" 404 stoßen:

* Bestätigen Sie, dass das Modell im [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) aktiviert ist
* Überprüfen Sie, dass das Modell am angegebenen Standort verfügbar ist. Einige Modelle werden nur auf `global` oder Multi-Region-Standorten wie `eu` und `us` angeboten, nicht in spezifischen Regionen
* Wenn Sie `CLOUD_ML_REGION=global` verwenden, überprüfen Sie, dass Ihre Modelle globale Endpunkte im [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) unter „Unterstützte Funktionen" unterstützen. Für Modelle, die globale Endpunkte nicht unterstützen, können Sie entweder:
  * Ein unterstütztes Modell über `ANTHROPIC_MODEL` oder `ANTHROPIC_DEFAULT_HAIKU_MODEL` angeben, oder
  * Einen regionalen oder Multi-Region-Standort mit `VERTEX_REGION_<MODEL_NAME>`-Umgebungsvariablen festlegen

Wenn Sie auf 429-Fehler stoßen:

* Stellen Sie für regionale Endpunkte sicher, dass das primäre Modell und das kleine/schnelle Modell in Ihrer ausgewählten Region unterstützt werden
* Erwägen Sie, zu `CLOUD_ML_REGION=global` zu wechseln, um bessere Verfügbarkeit zu erreichen

## Zusätzliche Ressourcen

* [Vertex AI-Dokumentation](https://cloud.google.com/vertex-ai/docs)
* [Vertex AI-Preisgestaltung](https://cloud.google.com/vertex-ai/pricing)
* [Vertex AI-Kontingente und -Limits](https://cloud.google.com/vertex-ai/docs/quotas)
