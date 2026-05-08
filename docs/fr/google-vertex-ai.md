> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code sur Google Vertex AI

> Découvrez comment configurer Claude Code via Google Vertex AI, y compris la configuration, la configuration IAM et la résolution des problèmes.

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

## Conditions préalables

Avant de configurer Claude Code avec Vertex AI, assurez-vous que vous disposez de :

* Un compte Google Cloud Platform (GCP) avec facturation activée
* Un projet GCP avec l'API Vertex AI activée
* Accès aux modèles Claude souhaités (par exemple, Claude Sonnet 4.6)
* Google Cloud SDK (`gcloud`) installé et configuré
* Quota alloué dans la région GCP souhaitée

Pour vous connecter avec vos propres identifiants Vertex AI, suivez [Se connecter avec Vertex AI](#sign-in-with-vertex-ai) ci-dessous. Pour déployer Claude Code dans une équipe, utilisez les étapes de [configuration manuelle](#set-up-manually) et [épinglez vos versions de modèle](#5-pin-model-versions) avant le déploiement.

## Se connecter avec Vertex AI

Si vous disposez d'identifiants Google Cloud et souhaitez commencer à utiliser Claude Code via Vertex AI, l'assistant de connexion vous guide à travers le processus. Vous complétez les conditions préalables du côté GCP une fois par projet ; l'assistant gère le côté Claude Code.

<Note>
  L'assistant de configuration Vertex AI nécessite Claude Code v2.1.98 ou version ultérieure. Exécutez `claude --version` pour vérifier.
</Note>

<Steps>
  <Step title="Activer les modèles Claude dans votre projet GCP">
    [Activez l'API Vertex AI](#1-enable-vertex-ai-api) pour votre projet, puis demandez l'accès aux modèles Claude que vous souhaitez dans le [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden). Consultez [Configuration IAM](#iam-configuration) pour les autorisations dont votre compte a besoin.
  </Step>

  <Step title="Démarrer Claude Code et choisir Vertex AI">
    Exécutez `claude`. À l'invite de connexion, sélectionnez **plateforme tierce**, puis **Google Vertex AI**.
  </Step>

  <Step title="Suivre les invites de l'assistant">
    Choisissez comment vous vous authentifiez auprès de Google Cloud : identifiants par défaut de l'application à partir de `gcloud`, fichier de clé de compte de service, ou identifiants déjà dans votre environnement. L'assistant détecte votre projet et votre région, vérifie quels modèles Claude votre projet peut invoquer, et vous permet de les épingler. Il enregistre le résultat dans le bloc `env` de votre [fichier de paramètres utilisateur](/fr/settings), vous n'avez donc pas besoin d'exporter les variables d'environnement vous-même.
  </Step>
</Steps>

Après vous être connecté, exécutez `/setup-vertex` à tout moment pour rouvrir l'assistant et modifier vos identifiants, votre projet, votre région ou vos épingles de modèle.

## Configuration de la région

Claude Code prend en charge les points de terminaison Vertex AI [globaux](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai), multi-régions et régionaux. Définissez `CLOUD_ML_REGION` sur `global`, un emplacement multi-région tel que `eu` ou `us`, ou une région spécifique telle que `us-east5`. Claude Code sélectionne le nom d'hôte Vertex AI correct pour chaque formulaire, y compris les hôtes `aiplatform.eu.rep.googleapis.com` et `aiplatform.us.rep.googleapis.com` pour les emplacements multi-régions.

<Note>
  Vertex AI peut ne pas prendre en charge les modèles par défaut de Claude Code sur tous les types de points de terminaison. La disponibilité des modèles varie selon les [régions spécifiques](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models), les emplacements multi-régions et les [points de terminaison globaux](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models). Vous devrez peut-être basculer vers un emplacement pris en charge ou spécifier un modèle pris en charge.
</Note>

## Configuration manuelle

Pour configurer Vertex AI via des variables d'environnement au lieu de l'assistant, par exemple dans CI ou un déploiement d'entreprise scriptée, suivez les étapes ci-dessous.

### 1. Activer l'API Vertex AI

Activez l'API Vertex AI dans votre projet GCP :

```bash theme={null}
# Définissez votre ID de projet
gcloud config set project YOUR-PROJECT-ID

# Activez l'API Vertex AI
gcloud services enable aiplatform.googleapis.com
```

### 2. Demander l'accès au modèle

Demandez l'accès aux modèles Claude dans Vertex AI :

1. Accédez au [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Recherchez les modèles ' Claude '
3. Demandez l'accès aux modèles Claude souhaités (par exemple, Claude Sonnet 4.6)
4. Attendez l'approbation (peut prendre 24 à 48 heures)

### 3. Configurer les identifiants GCP

Claude Code utilise l'authentification Google Cloud standard.

Pour plus d'informations, consultez la [documentation d'authentification Google Cloud](https://cloud.google.com/docs/authentication).

Claude Code v2.1.121 ou version ultérieure prend en charge la [Fédération d'identité de charge de travail basée sur certificat X.509](https://cloud.google.com/iam/docs/workload-identity-federation-with-x509-certificates) via la même chaîne Application Default Credentials. Définissez `GOOGLE_APPLICATION_CREDENTIALS` sur le chemin de votre fichier de configuration des identifiants.

<Note>
  Claude Code utilise `ANTHROPIC_VERTEX_PROJECT_ID` comme ID de projet pour les demandes Vertex AI. Les variables d'environnement `GCLOUD_PROJECT` et `GOOGLE_CLOUD_PROJECT` et le fichier d'identifiants référencé par `GOOGLE_APPLICATION_CREDENTIALS` ont la priorité sur celui-ci. Si aucun de ces éléments n'est défini, l'ID de projet est résolu à partir de votre configuration `gcloud` ou du compte de service attaché.
</Note>

#### Configuration avancée des identifiants

Claude Code prend en charge l'actualisation automatique des identifiants GCP via le paramètre `gcpAuthRefresh`. Lorsque Claude Code détecte que vos identifiants GCP ont expiré ou ne peuvent pas être chargés, il exécute la commande configurée pour obtenir de nouveaux identifiants avant de réessayer la demande.

```json theme={null}
{
  "gcpAuthRefresh": "gcloud auth application-default login",
  "env": {
    "ANTHROPIC_VERTEX_PROJECT_ID": "your-project-id"
  }
}
```

La sortie de la commande s'affiche à l'utilisateur, mais l'entrée interactive n'est pas prise en charge. Cela fonctionne bien pour les flux d'authentification basés sur navigateur où l'interface de ligne de commande affiche une URL et vous complétez l'authentification dans le navigateur. La commande d'actualisation expire après trois minutes si l'authentification ne se termine pas. Si vous définissez `gcpAuthRefresh` dans les paramètres du projet tels que `.claude/settings.json`, la commande s'exécute uniquement après que vous ayez accepté l'invite de confiance de l'espace de travail.

### 4. Configurer Claude Code

Définissez les variables d'environnement suivantes :

```bash theme={null}
# Activez l'intégration Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Optionnel : Remplacez l'URL du point de terminaison Vertex pour les points de terminaison personnalisés ou les passerelles
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# Optionnel : Désactivez la mise en cache des invites si nécessaire
export DISABLE_PROMPT_CACHING=1

# Optionnel : Demandez une TTL de cache d'invites d'1 heure au lieu de la valeur par défaut de 5 minutes
export ENABLE_PROMPT_CACHING_1H=1

# Quand CLOUD_ML_REGION=global, remplacez la région pour les modèles qui ne prennent pas en charge les points de terminaison globaux
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

La plupart des versions de modèle ont une variable `VERTEX_REGION_CLAUDE_*` correspondante. Consultez la [référence des variables d'environnement](/fr/env-vars) pour la liste complète. Vérifiez [Vertex Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) pour déterminer quels modèles prennent en charge les points de terminaison globaux par rapport aux points de terminaison régionaux uniquement.

[La mise en cache des invites](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) est activée automatiquement. Pour la désactiver, définissez `DISABLE_PROMPT_CACHING=1`. Pour demander une TTL de cache d'1 heure au lieu de la valeur par défaut de 5 minutes, définissez `ENABLE_PROMPT_CACHING_1H=1` ; les écritures de cache avec une TTL d'1 heure sont facturées à un taux plus élevé. Pour des limites de débit accrues, contactez le support Google Cloud. Lors de l'utilisation de Vertex AI, les commandes `/login` et `/logout` sont désactivées car l'authentification est gérée via les identifiants Google Cloud.

[La recherche d'outils MCP](/fr/mcp#scale-with-mcp-tool-search) est désactivée par défaut sur Vertex AI car le point de terminaison n'accepte pas l'en-tête bêta requis. Toutes les définitions d'outils MCP se chargent à l'avance à la place. Pour participer, définissez `ENABLE_TOOL_SEARCH=true`.

### 5. Épingler les versions de modèle

<Warning>
  Épinglez les versions de modèle spécifiques lors du déploiement pour plusieurs utilisateurs. Sans épinglage, les alias de modèle tels que `sonnet` et `opus` se résolvent à la dernière version, qui peut ne pas encore être activée dans votre projet Vertex AI lorsqu'Anthropic publie une mise à jour. Claude Code [revient](#startup-model-checks) à la version précédente au démarrage lorsque la dernière n'est pas disponible, mais l'épinglage vous permet de contrôler quand vos utilisateurs passent à un nouveau modèle.
</Warning>

Définissez ces variables d'environnement sur des ID de modèle Vertex AI spécifiques.

Sans `ANTHROPIC_DEFAULT_OPUS_MODEL`, l'alias `opus` sur Vertex se résout à Opus 4.6. Définissez-le sur l'ID Opus 4.7 pour utiliser le dernier modèle :

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

Pour les ID de modèle actuels et hérités, consultez [Aperçu des modèles](https://platform.claude.com/docs/en/about-claude/models/overview). Consultez [Configuration du modèle](/fr/model-config#pin-models-for-third-party-deployments) pour la liste complète des variables d'environnement.

Claude Code utilise ces modèles par défaut lorsqu'aucune variable d'épinglage n'est définie :

| Type de modèle      | Valeur par défaut            |
| :------------------ | :--------------------------- |
| Modèle principal    | `claude-sonnet-4-5@20250929` |
| Modèle petit/rapide | `claude-haiku-4-5@20251001`  |

Pour personnaliser davantage les modèles :

```bash theme={null}
export ANTHROPIC_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

## Vérifications du modèle au démarrage

Lorsque Claude Code démarre avec Vertex AI configuré, il vérifie que les modèles qu'il a l'intention d'utiliser sont accessibles dans votre projet. Cette vérification nécessite Claude Code v2.1.98 ou version ultérieure.

Si vous avez épinglé une version de modèle plus ancienne que la valeur par défaut actuelle de Claude Code, et que votre projet peut invoquer la version plus récente, Claude Code vous invite à mettre à jour l'épingle. L'acceptation écrit le nouvel ID de modèle dans votre [fichier de paramètres utilisateur](/fr/settings) et redémarre Claude Code. Le refus est mémorisé jusqu'au prochain changement de version par défaut.

Si vous n'avez pas épinglé un modèle et que la valeur par défaut actuelle n'est pas disponible dans votre projet, Claude Code revient à la version précédente pour la session actuelle et affiche un avis. Le retour n'est pas persistant. Activez le modèle plus récent dans [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) ou [épinglez une version](#5-pin-model-versions) pour rendre le choix permanent.

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

Claude Opus 4.7, Opus 4.6 et Sonnet 4.6 prennent en charge la [fenêtre de contexte de 1M de jetons](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) sur Vertex AI. Claude Code active automatiquement la fenêtre de contexte étendue lorsque vous sélectionnez une variante de modèle 1M.

L'[assistant de configuration](#sign-in-with-vertex-ai) offre une option de contexte 1M lorsqu'il épingle les modèles. Pour l'activer pour un modèle épinglé manuellement à la place, ajoutez `[1m]` à l'ID du modèle. Consultez [Épingler les modèles pour les déploiements tiers](/fr/model-config#pin-models-for-third-party-deployments) pour plus de détails.

## Résolution des problèmes

Si vous rencontrez des erreurs « Impossible de charger les identifiants par défaut » :

* Exécutez `gcloud auth application-default login` pour configurer les identifiants par défaut de l'application
* Définissez `GOOGLE_APPLICATION_CREDENTIALS` sur le chemin d'un fichier de clé de compte de service
* Consultez [Configurer les identifiants GCP](#3-configure-gcp-credentials) pour toutes les options

Si vous rencontrez des problèmes de quota :

* Vérifiez les quotas actuels ou demandez une augmentation de quota via la [Console Cloud](https://cloud.google.com/docs/quotas/view-manage)

Si vous rencontrez des erreurs « modèle non trouvé » 404 :

* Confirmez que le modèle est activé dans [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Vérifiez que le modèle est disponible dans l'emplacement que vous avez spécifié. Certains modèles ne sont proposés que sur les emplacements `global` ou multi-régions tels que `eu` et `us`, pas dans les régions spécifiques
* Si vous utilisez `CLOUD_ML_REGION=global`, vérifiez que vos modèles prennent en charge les points de terminaison globaux dans [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) sous « Fonctionnalités prises en charge ». Pour les modèles qui ne prennent pas en charge les points de terminaison globaux, soit :
  * Spécifiez un modèle pris en charge via `ANTHROPIC_MODEL` ou `ANTHROPIC_DEFAULT_HAIKU_MODEL`, soit
  * Définissez une région ou un emplacement multi-région à l'aide des variables d'environnement `VERTEX_REGION_<MODEL_NAME>`

Si vous rencontrez des erreurs 429 :

* Pour les points de terminaison régionaux, assurez-vous que le modèle principal et le modèle petit/rapide sont pris en charge dans votre région sélectionnée
* Envisagez de basculer vers `CLOUD_ML_REGION=global` pour une meilleure disponibilité

## Ressources supplémentaires

* [Documentation Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Tarification Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Quotas et limites Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
