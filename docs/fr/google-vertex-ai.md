> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code sur Google Vertex AI

> Découvrez comment configurer Claude Code via Google Vertex AI, y compris la configuration, la configuration IAM et la résolution des problèmes.

## Conditions préalables

Avant de configurer Claude Code avec Vertex AI, assurez-vous que vous disposez de :

* Un compte Google Cloud Platform (GCP) avec facturation activée
* Un projet GCP avec l'API Vertex AI activée
* Accès aux modèles Claude souhaités (par exemple, Claude Sonnet 4.6)
* Google Cloud SDK (`gcloud`) installé et configuré
* Quota alloué dans la région GCP souhaitée

<Note>
  Si vous déployez Claude Code pour plusieurs utilisateurs, [épinglez vos versions de modèle](#5-pin-model-versions) pour éviter les ruptures lorsqu'Anthropic publie de nouveaux modèles.
</Note>

## Configuration de la région

Claude Code peut être utilisé avec les points de terminaison Vertex AI [globaux](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai) et régionaux.

<Note>
  Vertex AI peut ne pas supporter les modèles par défaut de Claude Code dans toutes les [régions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models) ou sur les [points de terminaison globaux](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models). Vous devrez peut-être basculer vers une région prise en charge, utiliser un point de terminaison régional ou spécifier un modèle pris en charge.
</Note>

## Configuration

### 1. Activer l'API Vertex AI

Activez l'API Vertex AI dans votre projet GCP :

```bash  theme={null}
# Définissez votre ID de projet
gcloud config set project YOUR-PROJECT-ID

# Activez l'API Vertex AI
gcloud services enable aiplatform.googleapis.com
```

### 2. Demander l'accès au modèle

Demandez l'accès aux modèles Claude dans Vertex AI :

1. Accédez au [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Recherchez les modèles « Claude »
3. Demandez l'accès aux modèles Claude souhaités (par exemple, Claude Sonnet 4.6)
4. Attendez l'approbation (peut prendre 24 à 48 heures)

### 3. Configurer les identifiants GCP

Claude Code utilise l'authentification Google Cloud standard.

Pour plus d'informations, consultez la [documentation d'authentification Google Cloud](https://cloud.google.com/docs/authentication).

<Note>
  Lors de l'authentification, Claude Code utilisera automatiquement l'ID de projet de la variable d'environnement `ANTHROPIC_VERTEX_PROJECT_ID`. Pour remplacer cela, définissez l'une de ces variables d'environnement : `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT` ou `GOOGLE_APPLICATION_CREDENTIALS`.
</Note>

### 4. Configurer Claude Code

Définissez les variables d'environnement suivantes :

```bash  theme={null}
# Activez l'intégration Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Optionnel : Désactivez la mise en cache des invites si nécessaire
export DISABLE_PROMPT_CACHING=1

# Quand CLOUD_ML_REGION=global, remplacez la région pour les modèles non pris en charge
export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-east5

# Optionnel : Remplacez les régions pour d'autres modèles spécifiques
export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5
export VERTEX_REGION_CLAUDE_3_7_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west1
export VERTEX_REGION_CLAUDE_4_0_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_1_OPUS=europe-west1
```

[La mise en cache des invites](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) est automatiquement prise en charge lorsque vous spécifiez l'indicateur éphémère `cache_control`. Pour la désactiver, définissez `DISABLE_PROMPT_CACHING=1`. Pour des limites de débit accrues, contactez le support Google Cloud. Lors de l'utilisation de Vertex AI, les commandes `/login` et `/logout` sont désactivées car l'authentification est gérée via les identifiants Google Cloud.

### 5. Épingler les versions de modèle

<Warning>
  Épinglez les versions de modèle spécifiques pour chaque déploiement. Si vous utilisez des alias de modèle (`sonnet`, `opus`, `haiku`) sans épinglage, Claude Code peut tenter d'utiliser une version de modèle plus récente qui n'est pas activée dans votre projet Vertex AI, ce qui cassera les utilisateurs existants lorsqu'Anthropic publie des mises à jour.
</Warning>

Définissez ces variables d'environnement sur des ID de modèle Vertex AI spécifiques :

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

Pour les ID de modèle actuels et hérités, consultez [Aperçu des modèles](https://platform.claude.com/docs/en/about-claude/models/overview). Consultez [Configuration du modèle](/fr/model-config#pin-models-for-third-party-deployments) pour la liste complète des variables d'environnement.

Claude Code utilise ces modèles par défaut lorsqu'aucune variable d'épinglage n'est définie :

| Type de modèle      | Valeur par défaut           |
| :------------------ | :-------------------------- |
| Modèle principal    | `claude-sonnet-4-6`         |
| Modèle petit/rapide | `claude-haiku-4-5@20251001` |

Pour personnaliser davantage les modèles :

```bash  theme={null}
export ANTHROPIC_MODEL='claude-opus-4-6'
export ANTHROPIC_SMALL_FAST_MODEL='claude-haiku-4-5@20251001'
```

## Configuration IAM

Attribuez les autorisations IAM requises :

Le rôle `roles/aiplatform.user` inclut les autorisations requises :

* `aiplatform.endpoints.predict` - Requis pour l'invocation de modèle et le comptage des jetons

Pour des autorisations plus restrictives, créez un rôle personnalisé avec uniquement les autorisations ci-dessus.

Pour plus de détails, consultez la [documentation IAM de Vertex](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Créez un projet GCP dédié pour Claude Code pour simplifier le suivi des coûts et le contrôle d'accès.
</Note>

## Fenêtre de contexte de 1M de jetons

Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5 et Sonnet 4 prennent en charge la [fenêtre de contexte de 1M de jetons](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) sur Vertex AI. Claude Code active automatiquement la fenêtre de contexte étendue lorsque vous sélectionnez une variante de modèle 1M.

Pour activer la fenêtre de contexte de 1M pour votre modèle épinglé, ajoutez `[1m]` à l'ID du modèle. Consultez [Épingler les modèles pour les déploiements tiers](/fr/model-config#pin-models-for-third-party-deployments) pour plus de détails.

## Résolution des problèmes

Si vous rencontrez des problèmes de quota :

* Vérifiez les quotas actuels ou demandez une augmentation de quota via la [Console Cloud](https://cloud.google.com/docs/quotas/view-manage)

Si vous rencontrez des erreurs « modèle non trouvé » 404 :

* Confirmez que le modèle est activé dans [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Vérifiez que vous avez accès à la région spécifiée
* Si vous utilisez `CLOUD_ML_REGION=global`, vérifiez que vos modèles prennent en charge les points de terminaison globaux dans [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) sous « Fonctionnalités prises en charge ». Pour les modèles qui ne prennent pas en charge les points de terminaison globaux, soit :
  * Spécifiez un modèle pris en charge via `ANTHROPIC_MODEL` ou `ANTHROPIC_SMALL_FAST_MODEL`, soit
  * Définissez un point de terminaison régional à l'aide des variables d'environnement `VERTEX_REGION_<MODEL_NAME>`

Si vous rencontrez des erreurs 429 :

* Pour les points de terminaison régionaux, assurez-vous que le modèle principal et le modèle petit/rapide sont pris en charge dans votre région sélectionnée
* Envisagez de basculer vers `CLOUD_ML_REGION=global` pour une meilleure disponibilité

## Ressources supplémentaires

* [Documentation Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Tarification Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Quotas et limites Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
