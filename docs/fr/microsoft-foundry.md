> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code sur Microsoft Foundry

> Découvrez comment configurer Claude Code via Microsoft Foundry, y compris la configuration, les paramètres et la résolution des problèmes.

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

<ContactSalesCard surface="foundry" />

## Conditions préalables

Avant de configurer Claude Code avec Microsoft Foundry, assurez-vous que vous disposez de :

* Un abonnement Azure avec accès à Microsoft Foundry
* Des autorisations RBAC pour créer des ressources et des déploiements Microsoft Foundry
* Azure CLI installé et configuré (facultatif - nécessaire uniquement si vous n'avez pas d'autre mécanisme pour obtenir les identifiants)

<Note>
  Si vous déployez Claude Code pour plusieurs utilisateurs, [épinglez vos versions de modèle](#4-pin-model-versions) pour éviter les ruptures lorsqu'Anthropic publie de nouveaux modèles.
</Note>

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

```bash theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**Option B : Authentification Microsoft Entra ID**

Lorsque `ANTHROPIC_FOUNDRY_API_KEY` n'est pas défini, Claude Code utilise automatiquement la [chaîne d'identifiants par défaut](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview) du SDK Azure.
Cela prend en charge une variété de méthodes pour authentifier les charges de travail locales et distantes.

Dans les environnements locaux, vous pouvez généralement utiliser Azure CLI :

```bash theme={null}
az login
```

<Note>
  Lors de l'utilisation de Microsoft Foundry, les commandes `/login` et `/logout` sont désactivées car l'authentification est gérée via les identifiants Azure.
</Note>

### 3. Configurer Claude Code

Définissez les variables d'environnement suivantes pour activer Microsoft Foundry :

```bash theme={null}
# Activer l'intégration Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# Nom de la ressource Azure (remplacez {resource} par le nom de votre ressource)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Ou fournissez l'URL de base complète :
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic
```

### 4. Épingler les versions de modèle

<Warning>
  Épinglez des versions de modèle spécifiques pour chaque déploiement. Si vous utilisez des alias de modèle (`sonnet`, `opus`, `haiku`) sans épingler, Claude Code peut tenter d'utiliser une version de modèle plus récente qui n'est pas disponible dans votre compte Foundry, ce qui casse les utilisateurs existants lorsqu'Anthropic publie des mises à jour. Lorsque vous créez des déploiements Azure, sélectionnez une version de modèle spécifique plutôt que « mise à jour automatique vers la dernière version ».
</Warning>

Définissez les variables de modèle pour correspondre aux noms de déploiement que vous avez créés à l'étape 1.

Sans `ANTHROPIC_DEFAULT_OPUS_MODEL`, l'alias `opus` sur Foundry se résout en Opus 4.6. Définissez-le sur l'ID Opus 4.7 pour utiliser le modèle le plus récent :

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
```

Les tâches en arrière-plan telles que la génération de titres de session utilisent le modèle petit/rapide, normalement un modèle de classe Haiku. Sur Foundry, Claude Code utilise par défaut le modèle principal car tous les comptes n'ont pas de déploiement Haiku. Pour utiliser Haiku pour les tâches en arrière-plan, définissez `ANTHROPIC_DEFAULT_HAIKU_MODEL` sur un déploiement Haiku disponible dans votre compte, comme indiqué ci-dessus.

Pour les ID de modèle actuels et hérités, consultez [Aperçu des modèles](https://platform.claude.com/docs/en/about-claude/models/overview). Consultez [Configuration des modèles](/fr/model-config#pin-models-for-third-party-deployments) pour la liste complète des variables d'environnement.

[Le cache des invites](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) est activé automatiquement. Pour demander un TTL de cache d'une heure au lieu de la valeur par défaut de 5 minutes, définissez la variable suivante ; les écritures de cache avec un TTL d'une heure sont facturées à un taux plus élevé :

```bash theme={null}
export ENABLE_PROMPT_CACHING_1H=1
```

## Configuration Azure RBAC

Les rôles par défaut `Azure AI User` et `Cognitive Services User` incluent toutes les autorisations requises pour invoquer les modèles Claude.

Pour des autorisations plus restrictives, créez un rôle personnalisé avec les éléments suivants :

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

Pour plus de détails, consultez la [documentation RBAC de Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

## Résolution des problèmes

Si vous recevez une erreur « Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed » :

* Configurez Entra ID sur l'environnement, ou définissez `ANTHROPIC_FOUNDRY_API_KEY`.

## Ressources supplémentaires

* [Documentation Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Modèles Microsoft Foundry](https://ai.azure.com/explore/models)
* [Tarification Microsoft Foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
