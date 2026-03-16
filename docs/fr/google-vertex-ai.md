> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code sur Google Vertex AI

> Découvrez comment configurer Claude Code via Google Vertex AI, y compris la configuration, la configuration IAM et le dépannage.

## Prérequis

Avant de configurer Claude Code avec Vertex AI, assurez-vous que vous disposez de :

* Un compte Google Cloud Platform (GCP) avec facturation activée
* Un projet GCP avec l'API Vertex AI activée
* Accès aux modèles Claude souhaités (par exemple, Claude Sonnet 4.5)
* Google Cloud SDK (`gcloud`) installé et configuré
* Quota alloué dans la région GCP souhaitée

## Configuration de la région

Claude Code peut être utilisé avec les points de terminaison Vertex AI [globaux](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai) et régionaux.

<Note>
  Vertex AI peut ne pas supporter les modèles par défaut de Claude Code dans toutes les régions. Vous devrez peut-être basculer vers une [région ou un modèle supporté](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models).
</Note>

<Note>
  Vertex AI peut ne pas supporter les modèles par défaut de Claude Code sur les points de terminaison globaux. Vous devrez peut-être basculer vers un point de terminaison régional ou un [modèle supporté](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models).
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
3. Demandez l'accès aux modèles Claude souhaités (par exemple, Claude Sonnet 4.5)
4. Attendez l'approbation (peut prendre 24 à 48 heures)

### 3. Configurer les identifiants GCP

Claude Code utilise l'authentification Google Cloud standard.

Pour plus d'informations, consultez la [documentation d'authentification Google Cloud](https://cloud.google.com/docs/authentication).

<Note>
  Lors de l'authentification, Claude Code utilisera automatiquement l'ID de projet de la variable d'environnement `ANTHROPIC_VERTEX_PROJECT_ID`. Pour remplacer cela, définissez l'une de ces variables d'environnement : `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT`, ou `GOOGLE_APPLICATION_CREDENTIALS`.
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

# Quand CLOUD_ML_REGION=global, remplacez la région pour les modèles non supportés
export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-east5

# Optionnel : Remplacez les régions pour d'autres modèles spécifiques
export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5
export VERTEX_REGION_CLAUDE_3_7_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west1
export VERTEX_REGION_CLAUDE_4_0_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_1_OPUS=europe-west1
```

<Note>
  La [mise en cache des invites](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) est automatiquement supportée lorsque vous spécifiez l'indicateur éphémère `cache_control`. Pour la désactiver, définissez `DISABLE_PROMPT_CACHING=1`. Pour des limites de débit accrues, contactez le support Google Cloud.
</Note>

<Note>
  Lors de l'utilisation de Vertex AI, les commandes `/login` et `/logout` sont désactivées puisque l'authentification est gérée via les identifiants Google Cloud.
</Note>

### 5. Configuration du modèle

Claude Code utilise ces modèles par défaut pour Vertex AI :

| Type de modèle      | Valeur par défaut            |
| :------------------ | :--------------------------- |
| Modèle principal    | `claude-sonnet-4-5@20250929` |
| Modèle petit/rapide | `claude-haiku-4-5@20251001`  |

<Note>
  Pour les utilisateurs de Vertex AI, Claude Code ne sera pas automatiquement mis à niveau de Haiku 3.5 vers Haiku 4.5. Pour basculer manuellement vers un modèle Haiku plus récent, définissez la variable d'environnement `ANTHROPIC_DEFAULT_HAIKU_MODEL` avec le nom complet du modèle (par exemple, `claude-haiku-4-5@20251001`).
</Note>

Pour personnaliser les modèles :

```bash  theme={null}
export ANTHROPIC_MODEL='claude-opus-4-1@20250805'
export ANTHROPIC_SMALL_FAST_MODEL='claude-haiku-4-5@20251001'
```

## Configuration IAM

Attribuez les autorisations IAM requises :

Le rôle `roles/aiplatform.user` inclut les autorisations requises :

* `aiplatform.endpoints.predict` - Requis pour l'invocation de modèle et le comptage de jetons

Pour des autorisations plus restrictives, créez un rôle personnalisé avec uniquement les autorisations ci-dessus.

Pour plus de détails, consultez la [documentation IAM de Vertex](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Nous recommandons de créer un projet GCP dédié pour Claude Code afin de simplifier le suivi des coûts et le contrôle d'accès.
</Note>

## Fenêtre de contexte de 1 million de jetons

Claude Sonnet 4 et Sonnet 4.5 supportent la [fenêtre de contexte de 1 million de jetons](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) sur Vertex AI.

<Note>
  La fenêtre de contexte de 1 million de jetons est actuellement en version bêta. Pour utiliser la fenêtre de contexte étendue, incluez l'en-tête bêta `context-1m-2025-08-07` dans vos demandes Vertex AI.
</Note>

## Dépannage

Si vous rencontrez des problèmes de quota :

* Vérifiez les quotas actuels ou demandez une augmentation de quota via la [Console Cloud](https://cloud.google.com/docs/quotas/view-manage)

Si vous rencontrez des erreurs « modèle non trouvé » 404 :

* Confirmez que le modèle est activé dans [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Vérifiez que vous avez accès à la région spécifiée
* Si vous utilisez `CLOUD_ML_REGION=global`, vérifiez que vos modèles supportent les points de terminaison globaux dans [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) sous « Fonctionnalités supportées ». Pour les modèles qui ne supportent pas les points de terminaison globaux, soit :
  * Spécifiez un modèle supporté via `ANTHROPIC_MODEL` ou `ANTHROPIC_SMALL_FAST_MODEL`, soit
  * Définissez un point de terminaison régional en utilisant les variables d'environnement `VERTEX_REGION_<MODEL_NAME>`

Si vous rencontrez des erreurs 429 :

* Pour les points de terminaison régionaux, assurez-vous que le modèle principal et le modèle petit/rapide sont supportés dans votre région sélectionnée
* Envisagez de basculer vers `CLOUD_ML_REGION=global` pour une meilleure disponibilité

## Ressources supplémentaires

* [Documentation Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Tarification Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Quotas et limites Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
