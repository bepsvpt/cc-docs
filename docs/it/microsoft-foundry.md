> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code su Microsoft Foundry

> Scopri come configurare Claude Code tramite Microsoft Foundry, inclusi setup, configurazione e risoluzione dei problemi.

## Prerequisiti

Prima di configurare Claude Code con Microsoft Foundry, assicurati di avere:

* Un abbonamento Azure con accesso a Microsoft Foundry
* Autorizzazioni RBAC per creare risorse e distribuzioni di Microsoft Foundry
* Azure CLI installato e configurato (facoltativo - necessario solo se non hai un altro meccanismo per ottenere le credenziali)

## Setup

### 1. Provisioning della risorsa Microsoft Foundry

Per prima cosa, crea una risorsa Claude in Azure:

1. Accedi al [portale Microsoft Foundry](https://ai.azure.com/)
2. Crea una nuova risorsa, annotando il nome della risorsa
3. Crea distribuzioni per i modelli Claude:
   * Claude Opus
   * Claude Sonnet
   * Claude Haiku

### 2. Configurare le credenziali Azure

Claude Code supporta due metodi di autenticazione per Microsoft Foundry. Scegli il metodo che meglio si adatta ai tuoi requisiti di sicurezza.

**Opzione A: Autenticazione tramite chiave API**

1. Accedi alla tua risorsa nel portale Microsoft Foundry
2. Vai alla sezione **Endpoint e chiavi**
3. Copia **Chiave API**
4. Imposta la variabile di ambiente:

```bash theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**Opzione B: Autenticazione Microsoft Entra ID**

Quando `ANTHROPIC_FOUNDRY_API_KEY` non è impostato, Claude Code utilizza automaticamente la [catena di credenziali predefinita](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview) di Azure SDK.
Questo supporta una varietà di metodi per autenticare carichi di lavoro locali e remoti.

Negli ambienti locali, puoi comunemente utilizzare Azure CLI:

```bash theme={null}
az login
```

<Note>
  Quando si utilizza Microsoft Foundry, i comandi `/login` e `/logout` sono disabilitati poiché l'autenticazione viene gestita tramite le credenziali Azure.
</Note>

### 3. Configurare Claude Code

Imposta le seguenti variabili di ambiente per abilitare Microsoft Foundry. Nota che i nomi delle tue distribuzioni sono impostati come identificatori di modello in Claude Code (potrebbe essere facoltativo se si utilizzano i nomi di distribuzione suggeriti).

```bash theme={null}
# Abilita l'integrazione Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# Nome della risorsa Azure (sostituisci {resource} con il nome della tua risorsa)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Oppure fornisci l'URL di base completo:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com

# Imposta i modelli sui nomi di distribuzione della tua risorsa
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-5'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-1'
```

Per ulteriori dettagli sulle opzioni di configurazione del modello, vedi [Configurazione del modello](/it/model-config).

## Configurazione RBAC di Azure

I ruoli predefiniti `Azure AI User` e `Cognitive Services User` includono tutte le autorizzazioni necessarie per invocare i modelli Claude.

Per autorizzazioni più restrittive, crea un ruolo personalizzato con quanto segue:

```json theme={null}
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

Per i dettagli, vedi [Documentazione RBAC di Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

## Risoluzione dei problemi

Se ricevi un errore "Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed":

* Configura Entra ID nell'ambiente, oppure imposta `ANTHROPIC_FOUNDRY_API_KEY`.

## Risorse aggiuntive

* [Documentazione di Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Modelli di Microsoft Foundry](https://ai.azure.com/explore/models)
* [Prezzi di Microsoft Foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
