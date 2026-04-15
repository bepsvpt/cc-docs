> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code sur Amazon Bedrock

> Découvrez comment configurer Claude Code via Amazon Bedrock, y compris la configuration, la configuration IAM et le dépannage.

## Prérequis

Avant de configurer Claude Code avec Bedrock, assurez-vous que vous disposez de :

* Un compte AWS avec accès à Bedrock activé
* Accès aux modèles Claude souhaités (par exemple, Claude Sonnet 4.6) dans Bedrock
* AWS CLI installé et configuré (facultatif - nécessaire uniquement si vous n'avez pas d'autre mécanisme pour obtenir les identifiants)
* Autorisations IAM appropriées

<Note>
  Si vous déployez Claude Code pour plusieurs utilisateurs, [épinglez vos versions de modèle](#4-pin-model-versions) pour éviter les ruptures lors de la publication de nouveaux modèles par Anthropic.
</Note>

## Configuration

### 1. Soumettre les détails du cas d'usage

Les utilisateurs pour la première fois des modèles Anthropic doivent soumettre les détails du cas d'usage avant d'invoquer un modèle. Ceci est fait une fois par compte.

1. Assurez-vous que vous disposez des bonnes autorisations IAM (voir plus à ce sujet ci-dessous)
2. Accédez à la [console Amazon Bedrock](https://console.aws.amazon.com/bedrock/)
3. Sélectionnez **Chat/Text playground**
4. Choisissez n'importe quel modèle Anthropic et vous serez invité à remplir le formulaire de cas d'usage

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

# Optional: Override the region for the small/fast model (Haiku)
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
  Épinglez les versions de modèle spécifiques pour chaque déploiement. Si vous utilisez des alias de modèle (`sonnet`, `opus`, `haiku`) sans épinglage, Claude Code peut tenter d'utiliser une version de modèle plus récente qui n'est pas disponible dans votre compte Bedrock, ce qui casse les utilisateurs existants lors de la publication de mises à jour par Anthropic.
</Warning>

Définissez ces variables d'environnement sur des ID de modèle Bedrock spécifiques :

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'
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
```

<Note>[La mise en cache des invites](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) peut ne pas être disponible dans toutes les régions.</Note>

#### Mapper chaque version de modèle à un profil d'inférence

Les variables d'environnement `ANTHROPIC_DEFAULT_*_MODEL` configurent un profil d'inférence par famille de modèles. Si votre organisation doit exposer plusieurs versions de la même famille dans le sélecteur `/model`, chacune acheminée vers son propre ARN de profil d'inférence d'application, utilisez plutôt le paramètre `modelOverrides` dans votre [fichier de paramètres](/fr/settings#settings-files).

Cet exemple mappe trois versions d'Opus à des ARN distincts afin que les utilisateurs puissent basculer entre elles sans contourner les profils d'inférence de votre organisation :

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

Lorsqu'un utilisateur sélectionne l'une de ces versions dans `/model`, Claude Code appelle Bedrock avec l'ARN mappé. Les versions sans remplacement reviennent à l'ID de modèle Bedrock intégré ou à tout profil d'inférence correspondant découvert au démarrage. Voir [Remplacer les ID de modèle par version](/fr/model-config#override-model-ids-per-version) pour plus de détails sur la façon dont les remplacements interagissent avec `availableModels` et d'autres paramètres de modèle.

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

Claude Opus 4.6 et Sonnet 4.6 prennent en charge la [fenêtre de contexte de 1M de jetons](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) sur Amazon Bedrock. Claude Code active automatiquement la fenêtre de contexte étendue lorsque vous sélectionnez une variante de modèle 1M.

Pour activer la fenêtre de contexte 1M pour votre modèle épinglé, ajoutez `[1m]` à l'ID du modèle. Voir [Épingler les modèles pour les déploiements tiers](/fr/model-config#pin-models-for-third-party-deployments) pour plus de détails.

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

## Ressources supplémentaires

* [Documentation Bedrock](https://docs.aws.amazon.com/bedrock/)
* [Tarification Bedrock](https://aws.amazon.com/bedrock/pricing/)
* [Profils d'inférence Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Claude Code sur Amazon Bedrock : Guide de configuration rapide](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Implémentation de la surveillance de Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
