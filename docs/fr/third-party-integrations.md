> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Aperçu du déploiement en entreprise

> Découvrez comment Claude Code peut s'intégrer à divers services tiers et infrastructures pour répondre aux exigences de déploiement en entreprise.

Cette page fournit un aperçu des options de déploiement disponibles et vous aide à choisir la configuration appropriée pour votre organisation.

## Comparaison des fournisseurs

<table>
  <thead>
    <tr>
      <th>Fonctionnalité</th>
      <th>Anthropic</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Régions</td>
      <td>[Pays](https://www.anthropic.com/supported-countries) pris en charge</td>
      <td>Plusieurs [régions](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) AWS</td>
      <td>Plusieurs [régions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations) GCP</td>
      <td>Plusieurs [régions](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/) Azure</td>
    </tr>

    <tr>
      <td>Mise en cache des invites</td>
      <td>Activée par défaut</td>
      <td>Activée par défaut</td>
      <td>Activée par défaut</td>
      <td>Activée par défaut</td>
    </tr>

    <tr>
      <td>Authentification</td>
      <td>Clé API</td>
      <td>Clé API ou identifiants AWS</td>
      <td>Identifiants GCP</td>
      <td>Clé API ou Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>Suivi des coûts</td>
      <td>Tableau de bord</td>
      <td>AWS Cost Explorer</td>
      <td>Facturation GCP</td>
      <td>Gestion des coûts Azure</td>
    </tr>

    <tr>
      <td>Fonctionnalités d'entreprise</td>
      <td>Équipes, surveillance de l'utilisation</td>
      <td>Politiques IAM, CloudTrail</td>
      <td>Rôles IAM, Journaux d'audit cloud</td>
      <td>Politiques RBAC, Azure Monitor</td>
    </tr>
  </tbody>
</table>

## Fournisseurs de cloud

<CardGroup cols={3}>
  <Card title="Amazon Bedrock" icon="aws" href="/fr/amazon-bedrock">
    Utilisez les modèles Claude via l'infrastructure AWS avec authentification par clé API ou basée sur IAM et surveillance native AWS
  </Card>

  <Card title="Google Vertex AI" icon="google" href="/fr/google-vertex-ai">
    Accédez aux modèles Claude via Google Cloud Platform avec sécurité et conformité de niveau entreprise
  </Card>

  <Card title="Microsoft Foundry" icon="microsoft" href="/fr/microsoft-foundry">
    Accédez à Claude via Azure avec authentification par clé API ou Microsoft Entra ID et facturation Azure
  </Card>
</CardGroup>

## Infrastructure d'entreprise

<CardGroup cols={2}>
  <Card title="Réseau d'entreprise" icon="shield" href="/fr/network-config">
    Configurez Claude Code pour fonctionner avec les serveurs proxy de votre organisation et les exigences SSL/TLS
  </Card>

  <Card title="Passerelle LLM" icon="server" href="/fr/llm-gateway">
    Déployez un accès centralisé aux modèles avec suivi de l'utilisation, budgétisation et journalisation d'audit
  </Card>
</CardGroup>

## Aperçu de la configuration

Claude Code prend en charge des options de configuration flexibles qui vous permettent de combiner différents fournisseurs et infrastructures :

<Note>
  Comprenez la différence entre :

  * **Proxy d'entreprise** : Un proxy HTTP/HTTPS pour acheminer le trafic (défini via `HTTPS_PROXY` ou `HTTP_PROXY`)
  * **Passerelle LLM** : Un service qui gère l'authentification et fournit des points de terminaison compatibles avec le fournisseur (défini via `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL` ou `ANTHROPIC_VERTEX_BASE_URL`)

  Les deux configurations peuvent être utilisées ensemble.
</Note>

### Utilisation de Bedrock avec proxy d'entreprise

Acheminez le trafic Bedrock via un proxy HTTP/HTTPS d'entreprise :

```bash  theme={null}
# Activer Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

# Configurer le proxy d'entreprise
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Utilisation de Bedrock avec passerelle LLM

Utilisez un service de passerelle qui fournit des points de terminaison compatibles avec Bedrock :

```bash  theme={null}
# Activer Bedrock
export CLAUDE_CODE_USE_BEDROCK=1

# Configurer la passerelle LLM
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # Si la passerelle gère l'authentification AWS
```

### Utilisation de Foundry avec proxy d'entreprise

Acheminez le trafic Azure via un proxy HTTP/HTTPS d'entreprise :

```bash  theme={null}
# Activer Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1
export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # Ou omettez pour l'authentification Entra ID

# Configurer le proxy d'entreprise
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Utilisation de Foundry avec passerelle LLM

Utilisez un service de passerelle qui fournit des points de terminaison compatibles avec Azure :

```bash  theme={null}
# Activer Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# Configurer la passerelle LLM
export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # Si la passerelle gère l'authentification Azure
```

### Utilisation de Vertex AI avec proxy d'entreprise

Acheminez le trafic Vertex AI via un proxy HTTP/HTTPS d'entreprise :

```bash  theme={null}
# Activer Vertex
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

# Configurer le proxy d'entreprise
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Utilisation de Vertex AI avec passerelle LLM

Combinez les modèles Google Vertex AI avec une passerelle LLM pour une gestion centralisée :

```bash  theme={null}
# Activer Vertex
export CLAUDE_CODE_USE_VERTEX=1

# Configurer la passerelle LLM
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # Si la passerelle gère l'authentification GCP
```

### Configuration de l'authentification

Claude Code utilise `ANTHROPIC_AUTH_TOKEN` pour l'en-tête `Authorization` si nécessaire. Les drapeaux `SKIP_AUTH` (`CLAUDE_CODE_SKIP_BEDROCK_AUTH`, `CLAUDE_CODE_SKIP_VERTEX_AUTH`) sont utilisés dans les scénarios de passerelle LLM où la passerelle gère l'authentification du fournisseur.

## Choisir la bonne configuration de déploiement

Considérez ces facteurs lors de la sélection de votre approche de déploiement :

### Accès direct au fournisseur

Idéal pour les organisations qui :

* Veulent la configuration la plus simple
* Disposent d'une infrastructure AWS ou GCP existante
* Ont besoin de surveillance et de conformité natives du fournisseur

### Proxy d'entreprise

Idéal pour les organisations qui :

* Ont des exigences de proxy d'entreprise existantes
* Ont besoin de surveillance du trafic et de conformité
* Doivent acheminer tout le trafic via des chemins réseau spécifiques

### Passerelle LLM

Idéal pour les organisations qui :

* Ont besoin de suivi de l'utilisation entre les équipes
* Veulent basculer dynamiquement entre les modèles
* Nécessitent une limitation de débit personnalisée ou des budgets
* Ont besoin d'une gestion centralisée de l'authentification

## Débogage

Lors du débogage de votre déploiement :

* Utilisez la [commande slash](/fr/slash-commands) `claude /status`. Cette commande fournit une observabilité dans les paramètres d'authentification, de proxy et d'URL appliqués.
* Définissez la variable d'environnement `export ANTHROPIC_LOG=debug` pour enregistrer les requêtes.

## Meilleures pratiques pour les organisations

### 1. Investir dans la documentation et la mémoire

Nous recommandons vivement d'investir dans la documentation afin que Claude Code comprenne votre base de code. Les organisations peuvent déployer des fichiers CLAUDE.md à plusieurs niveaux :

* **À l'échelle de l'organisation** : Déployez dans les répertoires système comme `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) pour les normes à l'échelle de l'entreprise
* **Au niveau du référentiel** : Créez des fichiers `CLAUDE.md` dans les racines des référentiels contenant l'architecture du projet, les commandes de compilation et les directives de contribution. Archivez-les dans le contrôle de source afin que tous les utilisateurs en bénéficient

  [En savoir plus](/fr/memory).

### 2. Simplifier le déploiement

Si vous avez un environnement de développement personnalisé, nous constatons que créer un moyen « en un clic » d'installer Claude Code est essentiel pour augmenter l'adoption dans une organisation.

### 3. Commencer par une utilisation guidée

Encouragez les nouveaux utilisateurs à essayer Claude Code pour les questions sur la base de code, ou sur les corrections de bogues plus petites ou les demandes de fonctionnalités. Demandez à Claude Code de faire un plan. Vérifiez les suggestions de Claude et donnez un retour d'information si c'est hors piste. Au fil du temps, à mesure que les utilisateurs comprendront mieux ce nouveau paradigme, ils seront plus efficaces pour laisser Claude Code fonctionner de manière plus agentique.

### 4. Configurer les politiques de sécurité

Les équipes de sécurité peuvent configurer des autorisations gérées pour ce que Claude Code est et n'est pas autorisé à faire, ce qui ne peut pas être remplacé par la configuration locale. [En savoir plus](/fr/security).

### 5. Exploiter MCP pour les intégrations

MCP est un excellent moyen de donner à Claude Code plus d'informations, comme la connexion à des systèmes de gestion de tickets ou des journaux d'erreurs. Nous recommandons qu'une équipe centrale configure les serveurs MCP et archive une configuration `.mcp.json` dans la base de code afin que tous les utilisateurs en bénéficient. [En savoir plus](/fr/mcp).

Chez Anthropic, nous faisons confiance à Claude Code pour alimenter le développement dans chaque base de code Anthropic. Nous espérons que vous apprécierez d'utiliser Claude Code autant que nous.

## Étapes suivantes

* [Configurer Amazon Bedrock](/fr/amazon-bedrock) pour le déploiement natif AWS
* [Configurer Google Vertex AI](/fr/google-vertex-ai) pour le déploiement GCP
* [Configurer Microsoft Foundry](/fr/microsoft-foundry) pour le déploiement Azure
* [Configurer le réseau d'entreprise](/fr/network-config) pour les exigences réseau
* [Déployer la passerelle LLM](/fr/llm-gateway) pour la gestion en entreprise
* [Paramètres](/fr/settings) pour les options de configuration et les variables d'environnement
