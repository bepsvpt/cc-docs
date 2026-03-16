> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code auf Microsoft Foundry

> Erfahren Sie, wie Sie Claude Code über Microsoft Foundry konfigurieren, einschließlich Setup, Konfiguration und Fehlerbehebung.

## Voraussetzungen

Bevor Sie Claude Code mit Microsoft Foundry konfigurieren, stellen Sie sicher, dass Sie über Folgendes verfügen:

* Ein Azure-Abonnement mit Zugriff auf Microsoft Foundry
* RBAC-Berechtigungen zum Erstellen von Microsoft Foundry-Ressourcen und Bereitstellungen
* Azure CLI installiert und konfiguriert (optional - nur erforderlich, wenn Sie keinen anderen Mechanismus zum Abrufen von Anmeldedaten haben)

## Setup

### 1. Microsoft Foundry-Ressource bereitstellen

Erstellen Sie zunächst eine Claude-Ressource in Azure:

1. Navigieren Sie zum [Microsoft Foundry-Portal](https://ai.azure.com/)
2. Erstellen Sie eine neue Ressource und notieren Sie sich Ihren Ressourcennamen
3. Erstellen Sie Bereitstellungen für die Claude-Modelle:
   * Claude Opus
   * Claude Sonnet
   * Claude Haiku

### 2. Azure-Anmeldedaten konfigurieren

Claude Code unterstützt zwei Authentifizierungsmethoden für Microsoft Foundry. Wählen Sie die Methode, die Ihren Sicherheitsanforderungen am besten entspricht.

**Option A: API-Schlüssel-Authentifizierung**

1. Navigieren Sie zu Ihrer Ressource im Microsoft Foundry-Portal
2. Gehen Sie zum Abschnitt **Endpunkte und Schlüssel**
3. Kopieren Sie **API-Schlüssel**
4. Legen Sie die Umgebungsvariable fest:

```bash  theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**Option B: Microsoft Entra ID-Authentifizierung**

Wenn `ANTHROPIC_FOUNDRY_API_KEY` nicht gesetzt ist, verwendet Claude Code automatisch die Azure SDK [Standard-Anmeldekette](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview).
Dies unterstützt eine Vielzahl von Methoden zur Authentifizierung lokaler und Remote-Workloads.

In lokalen Umgebungen können Sie häufig die Azure CLI verwenden:

```bash  theme={null}
az login
```

<Note>
  Bei Verwendung von Microsoft Foundry sind die Befehle `/login` und `/logout` deaktiviert, da die Authentifizierung über Azure-Anmeldedaten erfolgt.
</Note>

### 3. Claude Code konfigurieren

Legen Sie die folgenden Umgebungsvariablen fest, um Microsoft Foundry zu aktivieren. Beachten Sie, dass die Namen Ihrer Bereitstellungen als Modellbezeichner in Claude Code festgelegt sind (möglicherweise optional, wenn Sie die vorgeschlagenen Bereitstellungsnamen verwenden).

```bash  theme={null}
# Microsoft Foundry-Integration aktivieren
export CLAUDE_CODE_USE_FOUNDRY=1

# Azure-Ressourcenname (ersetzen Sie {resource} durch Ihren Ressourcennamen)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Oder geben Sie die vollständige Basis-URL an:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com

# Legen Sie Modelle auf die Bereitstellungsnamen Ihrer Ressource fest
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-5'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-1'
```

Weitere Informationen zu Modellkonfigurationsoptionen finden Sie unter [Modellkonfiguration](/de/model-config).

## Azure RBAC-Konfiguration

Die Standardrollen `Azure AI User` und `Cognitive Services User` enthalten alle erforderlichen Berechtigungen zum Aufrufen von Claude-Modellen.

Für restriktivere Berechtigungen erstellen Sie eine benutzerdefinierte Rolle mit Folgendem:

```json  theme={null}
{
  "permissions": [
    {
      "dataActions": [
        "Microsoft.CognitiveServices/accounts/providers/*"
      ]
    }
  ]
}
```

Weitere Informationen finden Sie in der [Microsoft Foundry RBAC-Dokumentation](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

## Fehlerbehebung

Wenn Sie einen Fehler erhalten "Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed":

* Konfigurieren Sie Entra ID in der Umgebung, oder legen Sie `ANTHROPIC_FOUNDRY_API_KEY` fest.

## Zusätzliche Ressourcen

* [Microsoft Foundry-Dokumentation](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Microsoft Foundry-Modelle](https://ai.azure.com/explore/models)
* [Microsoft Foundry-Preise](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
