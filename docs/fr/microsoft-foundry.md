> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code sur Microsoft Foundry

> Découvrez comment configurer Claude Code via Microsoft Foundry, y compris la configuration, les paramètres et la résolution des problèmes.

## Conditions préalables

Avant de configurer Claude Code avec Microsoft Foundry, assurez-vous que vous disposez de :

* Un abonnement Azure avec accès à Microsoft Foundry
* Des autorisations RBAC pour créer des ressources et des déploiements Microsoft Foundry
* Azure CLI installé et configuré (facultatif - nécessaire uniquement si vous n'avez pas d'autre mécanisme pour obtenir les identifiants)

## Configuration

### 1. Provisionner la ressource Microsoft Foundry

Tout d'abord, créez une ressource Claude dans Azure :

1. Accédez au [portail Microsoft Foundry](https://ai.azure.com/)
2. Créez une nouvelle ressource, en notant le nom de votre ressource
3. Créez des déploiements pour les modèles Claude :
   * Claude Opus
   * Claude Sonnet
   * Claude Haiku

### 2. Configurer les identifiants Azure

Claude Code prend en charge deux méthodes d'authentification pour Microsoft Foundry. Choisissez la méthode qui correspond le mieux à vos exigences de sécurité.

**Option A : Authentification par clé API**

1. Accédez à votre ressource dans le portail Microsoft Foundry
2. Allez à la section **Points de terminaison et clés**
3. Copiez la **Clé API**
4. Définissez la variable d'environnement :

```bash  theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**Option B : Authentification Microsoft Entra ID**

Lorsque `ANTHROPIC_FOUNDRY_API_KEY` n'est pas défini, Claude Code utilise automatiquement la [chaîne d'identifiants par défaut](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview) du SDK Azure.
Cela prend en charge une variété de méthodes pour authentifier les charges de travail locales et distantes.

Dans les environnements locaux, vous pouvez généralement utiliser Azure CLI :

```bash  theme={null}
az login
```

<Note>
  Lors de l'utilisation de Microsoft Foundry, les commandes `/login` et `/logout` sont désactivées car l'authentification est gérée via les identifiants Azure.
</Note>

### 3. Configurer Claude Code

Définissez les variables d'environnement suivantes pour activer Microsoft Foundry. Notez que les noms de vos déploiements sont définis comme identifiants de modèle dans Claude Code (peut être facultatif si vous utilisez les noms de déploiement suggérés).

```bash  theme={null}
# Activer l'intégration Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# Nom de la ressource Azure (remplacez {resource} par le nom de votre ressource)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Ou fournissez l'URL de base complète :
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com

# Définissez les modèles sur les noms de déploiement de votre ressource
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-5'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-1'
```

Pour plus de détails sur les options de configuration des modèles, consultez [Configuration des modèles](/fr/model-config).

## Configuration Azure RBAC

Les rôles par défaut `Azure AI User` et `Cognitive Services User` incluent toutes les autorisations requises pour invoquer les modèles Claude.

Pour des autorisations plus restrictives, créez un rôle personnalisé avec les éléments suivants :

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

Pour plus de détails, consultez la [documentation RBAC de Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

## Résolution des problèmes

Si vous recevez une erreur « Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed » :

* Configurez Entra ID sur l'environnement, ou définissez `ANTHROPIC_FOUNDRY_API_KEY`.

## Ressources supplémentaires

* [Documentation Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Modèles Microsoft Foundry](https://ai.azure.com/explore/models)
* [Tarification Microsoft Foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
