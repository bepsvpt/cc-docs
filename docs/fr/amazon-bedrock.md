> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code sur Amazon Bedrock

> Découvrez comment configurer Claude Code via Amazon Bedrock, y compris la configuration, la configuration IAM et le dépannage.

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

export const Experiment = ({flag, treatment, children}) => {
  const VID_KEY = 'exp_vid';
  const CONSENT_COUNTRIES = new Set(['AT', 'BE', 'BG', 'HR', 'CY', 'CZ', 'DK', 'EE', 'FI', 'FR', 'DE', 'GR', 'HU', 'IE', 'IT', 'LV', 'LT', 'LU', 'MT', 'NL', 'PL', 'PT', 'RO', 'SK', 'SI', 'ES', 'SE', 'RE', 'GP', 'MQ', 'GF', 'YT', 'BL', 'MF', 'PM', 'WF', 'PF', 'NC', 'AW', 'CW', 'SX', 'FO', 'GL', 'AX', 'GB', 'UK', 'AI', 'BM', 'IO', 'VG', 'KY', 'FK', 'GI', 'MS', 'PN', 'SH', 'TC', 'GG', 'JE', 'IM', 'CA', 'BR', 'IN']);
  const fnv1a = s => {
    let h = 0x811c9dc5;
    for (let i = 0; i < s.length; i++) {
      h ^= s.charCodeAt(i);
      h += (h << 1) + (h << 4) + (h << 7) + (h << 8) + (h << 24);
    }
    return h >>> 0;
  };
  const bucket = (seed, vid) => fnv1a(fnv1a(seed + vid) + '') % 10000 < 5000 ? 'control' : 'treatment';
  const [decision] = useState(() => {
    const params = new URLSearchParams(location.search);
    const preBucketed = document.documentElement.dataset['gb_' + flag.replace(/-/g, '_')];
    const force = params.get('gb-force');
    if (force) {
      for (const p of force.split(',')) {
        const [k, v] = p.split(':');
        if (k === flag) return {
          variant: v || 'treatment',
          track: false
        };
      }
    }
    if (navigator.globalPrivacyControl) {
      return {
        variant: 'control',
        track: false
      };
    }
    const prefsMatch = document.cookie.match(/(?:^|; )anthropic-consent-preferences=([^;]+)/);
    if (prefsMatch) {
      try {
        if (JSON.parse(decodeURIComponent(prefsMatch[1])).analytics !== true) {
          return {
            variant: 'control',
            track: false
          };
        }
      } catch {
        return {
          variant: 'control',
          track: false
        };
      }
    } else {
      const country = params.get('country')?.toUpperCase() || (document.cookie.match(/(?:^|; )cf_geo=([A-Z]{2})/) || [])[1];
      if (!country || CONSENT_COUNTRIES.has(country)) {
        return {
          variant: 'control',
          track: false
        };
      }
    }
    let vid;
    try {
      const ajsMatch = document.cookie.match(/(?:^|; )ajs_anonymous_id=([^;]+)/);
      if (ajsMatch) {
        vid = decodeURIComponent(ajsMatch[1]).replace(/^"|"$/g, '');
      } else {
        vid = localStorage.getItem(VID_KEY);
        if (!vid) {
          vid = crypto.randomUUID();
        }
        document.cookie = `ajs_anonymous_id=${vid}; domain=.claude.com; path=/; Secure; SameSite=Lax; max-age=31536000`;
      }
      try {
        localStorage.setItem(VID_KEY, vid);
      } catch {}
    } catch {
      return {
        variant: 'control',
        track: false
      };
    }
    const variant = preBucketed === '1' ? 'treatment' : preBucketed === '0' ? 'control' : bucket(flag, vid);
    return {
      variant,
      track: true,
      vid
    };
  });
  useEffect(() => {
    if (!decision.track) return;
    fetch('https://api.anthropic.com/api/event_logging/v2/batch', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-service-name': 'claude_code_docs'
      },
      body: JSON.stringify({
        events: [{
          event_type: 'GrowthbookExperimentEvent',
          event_data: {
            device_id: decision.vid,
            anonymous_id: decision.vid,
            timestamp: new Date().toISOString(),
            experiment_id: flag,
            variation_id: decision.variant === 'treatment' ? 1 : 0,
            environment: 'production'
          }
        }]
      }),
      keepalive: true
    }).catch(() => {});
  }, []);
  return decision.variant === 'treatment' ? treatment : children;
};

<Experiment flag="docs-contact-sales-cta" treatment={<ContactSalesCard surface="bedrock" />} />

## Prérequis

Avant de configurer Claude Code avec Bedrock, assurez-vous que vous disposez de :

* Un compte AWS avec accès à Bedrock activé
* Accès aux modèles Claude souhaités (par exemple, Claude Sonnet 4.6) dans Bedrock
* AWS CLI installé et configuré (facultatif - nécessaire uniquement si vous n'avez pas d'autre mécanisme pour obtenir les identifiants)
* Autorisations IAM appropriées

Pour vous connecter avec vos propres identifiants Bedrock, suivez [Se connecter avec Bedrock](#sign-in-with-bedrock) ci-dessous. Pour déployer Claude Code dans une équipe, utilisez les étapes de [configuration manuelle](#set-up-manually) et [épinglez vos versions de modèle](#4-pin-model-versions) avant le déploiement.

## Se connecter avec Bedrock

Si vous disposez d'identifiants AWS et souhaitez commencer à utiliser Claude Code via Bedrock, l'assistant de connexion vous guide à travers le processus. Vous complétez les prérequis côté AWS une fois par compte ; l'assistant gère le côté Claude Code.

<Steps>
  <Step title="Activer les modèles Anthropic dans votre compte AWS">
    Dans la [console Amazon Bedrock](https://console.aws.amazon.com/bedrock/), ouvrez le catalogue de modèles, sélectionnez un modèle Anthropic et soumettez le formulaire de cas d'usage. L'accès est accordé immédiatement après la soumission. Voir [Soumettre les détails du cas d'usage](#1-submit-use-case-details) pour AWS Organizations et [Configuration IAM](#iam-configuration) pour les autorisations dont votre rôle a besoin.
  </Step>

  <Step title="Démarrer Claude Code et choisir Bedrock">
    Exécutez `claude`. À l'invite de connexion, sélectionnez **3rd-party platform**, puis **Amazon Bedrock**.
  </Step>

  <Step title="Suivre les invites de l'assistant">
    Choisissez comment vous vous authentifiez auprès d'AWS : un profil AWS détecté à partir de votre répertoire `~/.aws`, une clé API Bedrock, une clé d'accès et un secret, ou des identifiants déjà dans votre environnement. L'assistant récupère votre région, vérifie quels modèles Claude votre compte peut invoquer, et vous permet de les épingler. Il enregistre le résultat dans le bloc `env` de votre [fichier de paramètres utilisateur](/fr/settings), vous n'avez donc pas besoin d'exporter les variables d'environnement vous-même.
  </Step>
</Steps>

Après vous être connecté, exécutez `/setup-bedrock` à tout moment pour rouvrir l'assistant et modifier vos identifiants, votre région ou vos épingles de modèle.

## Configuration manuelle

Pour configurer Bedrock via des variables d'environnement au lieu de l'assistant, par exemple dans CI ou un déploiement d'entreprise scriptés, suivez les étapes ci-dessous.

### 1. Soumettre les détails du cas d'usage

Les utilisateurs pour la première fois des modèles Anthropic doivent soumettre les détails du cas d'usage avant d'invoquer un modèle. Ceci est fait une fois par compte AWS.

1. Assurez-vous que vous disposez des bonnes autorisations IAM décrites ci-dessous
2. Accédez à la [console Amazon Bedrock](https://console.aws.amazon.com/bedrock/)
3. Sélectionnez un modèle Anthropic dans le **catalogue de modèles**
4. Complétez le formulaire de cas d'usage. L'accès est accordé immédiatement après la soumission.

Si vous utilisez AWS Organizations, vous pouvez soumettre le formulaire une fois à partir du compte de gestion en utilisant l'[API `PutUseCaseForModelAccess`](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html). Cet appel nécessite l'autorisation IAM `bedrock:PutUseCaseForModelAccess`. L'approbation s'étend automatiquement aux comptes enfants.

### 2. Configurer les identifiants AWS

Claude Code utilise la chaîne d'identifiants par défaut du SDK AWS. Configurez vos identifiants en utilisant l'une de ces méthodes :

**Option A : Configuration AWS CLI**

```bash theme={null}
aws configure
```

**Option B : Variables d'environnement (clé d'accès)**

```bash theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**Option C : Variables d'environnement (profil SSO)**

```bash theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**Option D : Identifiants de la console de gestion AWS**

```bash theme={null}
aws login
```

[En savoir plus](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) sur `aws login`.

**Option E : Clés API Bedrock**

```bash theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Les clés API Bedrock offrent une méthode d'authentification plus simple sans avoir besoin d'identifiants AWS complets. [En savoir plus sur les clés API Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### Configuration avancée des identifiants

Claude Code prend en charge l'actualisation automatique des identifiants pour AWS SSO et les fournisseurs d'identité d'entreprise. Ajoutez ces paramètres à votre fichier de paramètres Claude Code (voir [Paramètres](/fr/settings) pour les emplacements des fichiers).

Lorsque Claude Code détecte que vos identifiants AWS ont expiré (soit localement en fonction de leur horodatage, soit lorsque Bedrock retourne une erreur d'identifiants), il exécutera automatiquement vos commandes `awsAuthRefresh` et/ou `awsCredentialExport` configurées pour obtenir de nouveaux identifiants avant de réessayer la demande.

##### Exemple de configuration

```json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### Paramètres de configuration expliqués

**`awsAuthRefresh`** : Utilisez ceci pour les commandes qui modifient le répertoire `.aws`, comme la mise à jour des identifiants, du cache SSO ou des fichiers de configuration. La sortie de la commande s'affiche à l'utilisateur, mais l'entrée interactive n'est pas prise en charge. Cela fonctionne bien pour les flux SSO basés sur un navigateur où l'interface de ligne de commande affiche une URL ou un code et vous complétez l'authentification dans le navigateur.

**`awsCredentialExport`** : Utilisez ceci uniquement si vous ne pouvez pas modifier `.aws` et devez retourner directement les identifiants. La sortie est capturée silencieusement et non affichée à l'utilisateur. La commande doit générer du JSON dans ce format :

```json theme={null}
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. Configurer Claude Code

Définissez les variables d'environnement suivantes pour activer Bedrock :

```bash theme={null}
# Enable Bedrock integration
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # or your preferred region

# Optional: Override the region for the small/fast model (Haiku).
# Also applies to Bedrock Mantle.
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2

# Optional: Override the Bedrock endpoint URL for custom endpoints or gateways
# export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

Lors de l'activation de Bedrock pour Claude Code, gardez à l'esprit les points suivants :

* `AWS_REGION` est une variable d'environnement requise. Claude Code ne lit pas à partir du fichier de configuration `.aws` pour ce paramètre.
* Lors de l'utilisation de Bedrock, les commandes `/login` et `/logout` sont désactivées car l'authentification est gérée via les identifiants AWS.
* Vous pouvez utiliser des fichiers de paramètres pour les variables d'environnement comme `AWS_PROFILE` que vous ne voulez pas divulguer à d'autres processus. Voir [Paramètres](/fr/settings) pour plus d'informations.

### 4. Épingler les versions de modèle

<Warning>
  Épinglez les versions de modèle spécifiques lors du déploiement pour plusieurs utilisateurs. Sans épinglage, les alias de modèle tels que `sonnet` et `opus` se résolvent à la dernière version, qui peut ne pas encore être disponible dans votre compte Bedrock lorsqu'Anthropic publie une mise à jour. Claude Code [revient](#startup-model-checks) à la version précédente au démarrage lorsque la dernière n'est pas disponible, mais l'épinglage vous permet de contrôler quand vos utilisateurs passent à un nouveau modèle.
</Warning>

Définissez ces variables d'environnement sur des ID de modèle Bedrock spécifiques.

Sans `ANTHROPIC_DEFAULT_OPUS_MODEL`, l'alias `opus` sur Bedrock se résout à Opus 4.6. Définissez-le sur l'ID Opus 4.7 pour utiliser le dernier modèle :

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

Ces variables utilisent des ID de profil d'inférence inter-régions (avec le préfixe `us.`). Si vous utilisez un préfixe de région différent ou des profils d'inférence d'application, ajustez en conséquence. Pour les ID de modèle actuels et hérités, voir [Aperçu des modèles](https://platform.claude.com/docs/en/about-claude/models/overview). Voir [Configuration du modèle](/fr/model-config#pin-models-for-third-party-deployments) pour la liste complète des variables d'environnement.

Claude Code utilise ces modèles par défaut lorsqu'aucune variable d'épinglage n'est définie :

| Type de modèle      | Valeur par défaut                              |
| :------------------ | :--------------------------------------------- |
| Modèle principal    | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Modèle petit/rapide | `us.anthropic.claude-haiku-4-5-20251001-v1:0`  |

Pour personnaliser davantage les modèles, utilisez l'une de ces méthodes :

```bash theme={null}
# Using inference profile ID
export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Using application inference profile ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1

# Optional: Request 1-hour prompt cache TTL instead of the 5-minute default
export ENABLE_PROMPT_CACHING_1H=1
```

<Note>[La mise en cache des invites](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) peut ne pas être disponible dans toutes les régions. Les écritures de cache avec un TTL d'une heure sont facturées à un taux plus élevé que les écritures de cinq minutes.</Note>

#### Mapper chaque version de modèle à un profil d'inférence

Les variables d'environnement `ANTHROPIC_DEFAULT_*_MODEL` configurent un profil d'inférence par famille de modèles. Si votre organisation doit exposer plusieurs versions de la même famille dans le sélecteur `/model`, chacune acheminée vers son propre ARN de profil d'inférence d'application, utilisez plutôt le paramètre `modelOverrides` dans votre [fichier de paramètres](/fr/settings#settings-files).

Cet exemple mappe quatre versions d'Opus à des ARN distincts afin que les utilisateurs puissent basculer entre elles sans contourner les profils d'inférence de votre organisation :

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

Lorsqu'un utilisateur sélectionne l'une de ces versions dans `/model`, Claude Code appelle Bedrock avec l'ARN mappé. Les versions sans remplacement reviennent à l'ID de modèle Bedrock intégré ou à tout profil d'inférence correspondant découvert au démarrage. Voir [Remplacer les ID de modèle par version](/fr/model-config#override-model-ids-per-version) pour plus de détails sur la façon dont les remplacements interagissent avec `availableModels` et d'autres paramètres de modèle.

## Vérifications du modèle au démarrage

Lorsque Claude Code démarre avec Bedrock configuré, il vérifie que les modèles qu'il a l'intention d'utiliser sont accessibles dans votre compte. Cette vérification nécessite Claude Code v2.1.94 ou version ultérieure.

Si vous avez épinglé une version de modèle plus ancienne que la valeur par défaut actuelle de Claude Code, et que votre compte peut invoquer la version plus récente, Claude Code vous invite à mettre à jour l'épingle. L'acceptation écrit le nouvel ID de modèle dans votre [fichier de paramètres utilisateur](/fr/settings) et redémarre Claude Code. Le refus est mémorisé jusqu'au prochain changement de version par défaut. Les épingles qui pointent vers un [ARN de profil d'inférence d'application](#map-each-model-version-to-an-inference-profile) sont ignorées, car celles-ci sont gérées par votre administrateur.

Si vous n'avez pas épinglé un modèle et que la valeur par défaut actuelle n'est pas disponible dans votre compte, Claude Code revient à la version précédente pour la session actuelle et affiche un avis. Le retour n'est pas persistant. Activez le modèle plus récent dans votre compte Bedrock ou [épinglez une version](#4-pin-model-versions) pour rendre le choix permanent.

## Configuration IAM

Créez une politique IAM avec les autorisations requises pour Claude Code :

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

Pour des autorisations plus restrictives, vous pouvez limiter la ressource à des ARN de profil d'inférence spécifiques.

Pour plus de détails, voir [Documentation IAM Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

<Note>
  Créez un compte AWS dédié pour Claude Code pour simplifier le suivi des coûts et le contrôle d'accès.
</Note>

## Fenêtre de contexte de 1M de jetons

Claude Opus 4.7, Opus 4.6 et Sonnet 4.6 prennent en charge la [fenêtre de contexte de 1M de jetons](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) sur Amazon Bedrock. Claude Code active automatiquement la fenêtre de contexte étendue lorsque vous sélectionnez une variante de modèle 1M.

L'[assistant de configuration](#sign-in-with-bedrock) offre une option de contexte 1M lorsqu'il épingle les modèles. Pour l'activer pour un modèle épinglé manuellement à la place, ajoutez `[1m]` à l'ID du modèle. Voir [Épingler les modèles pour les déploiements tiers](/fr/model-config#pin-models-for-third-party-deployments) pour plus de détails.

## Garde-fous AWS

[Les garde-fous Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) vous permettent de mettre en œuvre le filtrage du contenu pour Claude Code. Créez un garde-fou dans la [console Amazon Bedrock](https://console.aws.amazon.com/bedrock/), publiez une version, puis ajoutez les en-têtes du garde-fou à votre [fichier de paramètres](/fr/settings). Activez l'inférence inter-régions sur votre garde-fou si vous utilisez des profils d'inférence inter-régions.

Exemple de configuration :

```json theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

## Utiliser le point de terminaison Mantle

Mantle est un point de terminaison Amazon Bedrock qui sert les modèles Claude via la forme API Anthropic native plutôt que l'API Invoke Bedrock. Il utilise les mêmes identifiants AWS, autorisations IAM et configuration `awsAuthRefresh` décrites précédemment sur cette page.

<Note>
  Mantle nécessite Claude Code v2.1.94 ou version ultérieure. Exécutez `claude --version` pour vérifier.
</Note>

### Activer Mantle

Avec les identifiants AWS déjà configurés, définissez `CLAUDE_CODE_USE_MANTLE` pour acheminer les demandes vers le point de terminaison Mantle :

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export AWS_REGION=us-east-1
```

Claude Code construit l'URL du point de terminaison à partir de `AWS_REGION`. Pour la remplacer pour un point de terminaison personnalisé ou une passerelle, définissez `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`.

Exécutez `/status` dans Claude Code pour confirmer. La ligne du fournisseur affiche `Amazon Bedrock (Mantle)` lorsque Mantle est actif.

### Sélectionner un modèle Mantle

Mantle utilise des ID de modèle préfixés avec `anthropic.` et sans suffixe de version, par exemple `anthropic.claude-haiku-4-5`. Les modèles disponibles pour votre compte dépendent de ce que votre organisation a reçu ; les ID de modèle supplémentaires sont répertoriés dans vos documents d'intégration d'AWS. Contactez votre équipe de compte AWS pour demander l'accès aux modèles autorisés.

Définissez le modèle avec l'indicateur `--model` ou avec `/model` dans Claude Code :

```bash theme={null}
claude --model anthropic.claude-haiku-4-5
```

### Exécuter Mantle aux côtés de l'API Invoke

Les modèles disponibles pour vous sur Mantle peuvent ne pas inclure tous les modèles que vous utilisez aujourd'hui. La définition de `CLAUDE_CODE_USE_BEDROCK` et `CLAUDE_CODE_USE_MANTLE` permet à Claude Code d'appeler les deux points de terminaison à partir de la même session. Les ID de modèle qui correspondent au format Mantle sont acheminés vers Mantle, et tous les autres ID de modèle vont à l'API Invoke Bedrock.

```bash theme={null}
export CLAUDE_CODE_USE_BEDROCK=1
export CLAUDE_CODE_USE_MANTLE=1
```

Pour afficher un modèle Mantle dans le sélecteur `/model`, répertoriez son ID dans `availableModels` dans votre [fichier de paramètres](/fr/settings). Ce paramètre restreint également le sélecteur aux entrées répertoriées, donc incluez chaque alias que vous souhaitez garder disponible :

```json theme={null}
{
  "availableModels": ["opus", "sonnet", "haiku", "anthropic.claude-haiku-4-5"]
}
```

Les entrées avec le préfixe `anthropic.` sont ajoutées en tant qu'options de sélecteur personnalisées et acheminées vers Mantle. Remplacez `anthropic.claude-haiku-4-5` par l'ID de modèle que votre compte a reçu. Voir [Restreindre la sélection du modèle](/fr/model-config#restrict-model-selection) pour savoir comment `availableModels` interagit avec d'autres paramètres de modèle.

Lorsque les deux fournisseurs sont actifs, `/status` affiche `Amazon Bedrock + Amazon Bedrock (Mantle)`.

### Acheminer Mantle via une passerelle

Si votre organisation achemine le trafic du modèle via une [passerelle LLM](/fr/llm-gateway) centralisée qui injecte les identifiants AWS côté serveur, désactivez l'authentification côté client afin que Claude Code envoie les demandes sans signatures SigV4 ou en-têtes `x-api-key` :

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export CLAUDE_CODE_SKIP_MANTLE_AUTH=1
export ANTHROPIC_BEDROCK_MANTLE_BASE_URL=https://your-gateway.example.com
```

### Variables d'environnement Mantle

Ces variables sont spécifiques au point de terminaison Mantle. Voir [Variables d'environnement](/fr/env-vars) pour la liste complète.

| Variable                                | Objectif                                                                      |
| :-------------------------------------- | :---------------------------------------------------------------------------- |
| `CLAUDE_CODE_USE_MANTLE`                | Activer le point de terminaison Mantle. Définissez sur `1` ou `true`.         |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`     | Remplacer l'URL du point de terminaison Mantle par défaut                     |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH`          | Ignorer l'authentification côté client pour les configurations de proxy       |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | Remplacer la région AWS pour le modèle de classe Haiku (partagé avec Bedrock) |

## Dépannage

### Boucle d'authentification avec SSO et proxies d'entreprise

Si des onglets de navigateur s'ouvrent à plusieurs reprises lors de l'utilisation d'AWS SSO, supprimez le paramètre `awsAuthRefresh` de votre [fichier de paramètres](/fr/settings). Cela peut se produire lorsque les VPN d'entreprise ou les proxies d'inspection TLS interrompent le flux SSO du navigateur. Claude Code traite la connexion interrompue comme un échec d'authentification, réexécute `awsAuthRefresh` et boucle indéfiniment.

Si votre environnement réseau interfère avec les flux SSO automatiques basés sur un navigateur, utilisez `aws sso login` manuellement avant de démarrer Claude Code au lieu de vous fier à `awsAuthRefresh`.

### Problèmes de région

Si vous rencontrez des problèmes de région :

* Vérifiez la disponibilité du modèle : `aws bedrock list-inference-profiles --region your-region`
* Basculez vers une région prise en charge : `export AWS_REGION=us-east-1`
* Envisagez d'utiliser des profils d'inférence pour l'accès inter-régions

Si vous recevez une erreur « on-demand throughput isn't supported » :

* Spécifiez le modèle comme ID de [profil d'inférence](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)

Claude Code utilise l'API Bedrock [Invoke](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) et ne prend pas en charge l'API Converse.

### Erreurs du point de terminaison Mantle

Si `/status` n'affiche pas `Amazon Bedrock (Mantle)` après avoir défini `CLAUDE_CODE_USE_MANTLE`, la variable n'atteint pas le processus. Confirmez qu'elle est exportée dans le shell où vous avez lancé `claude`, ou définissez-la dans le bloc `env` de votre [fichier de paramètres](/fr/settings).

Un `403` du point de terminaison Mantle avec des identifiants valides signifie que votre compte AWS n'a pas reçu l'accès au modèle que vous avez demandé. Contactez votre équipe de compte AWS pour demander l'accès.

Un `400` qui nomme l'ID du modèle signifie que ce modèle n'est pas servi sur Mantle. Mantle a sa propre gamme de modèles distincte du catalogue Bedrock standard, donc les ID de profil d'inférence tels que `us.anthropic.claude-sonnet-4-6` ne fonctionneront pas. Utilisez un ID au format Mantle, ou activez [les deux points de terminaison](#run-mantle-alongside-the-invoke-api) afin que Claude Code achemine chaque demande vers le point de terminaison où le modèle est disponible.

## Ressources supplémentaires

* [Documentation Bedrock](https://docs.aws.amazon.com/bedrock/)
* [Tarification Bedrock](https://aws.amazon.com/bedrock/pricing/)
* [Profils d'inférence Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Quota de jetons Bedrock et réduction des jetons](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-token-burndown.html)
* [Claude Code sur Amazon Bedrock : Guide de configuration rapide](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Implémentation de la surveillance de Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
