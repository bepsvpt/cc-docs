> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Aperçu du déploiement en entreprise

> Découvrez comment Claude Code peut s'intégrer à divers services tiers et infrastructures pour répondre aux exigences de déploiement en entreprise.

Les organisations peuvent déployer Claude Code directement via Anthropic ou via un fournisseur de cloud. Cette page vous aide à choisir la bonne configuration.

## Comparer les options de déploiement

Pour la plupart des organisations, Claude for Teams ou Claude for Enterprise offre la meilleure expérience. Les membres de l'équipe ont accès à la fois à Claude Code et à Claude sur le web avec un seul abonnement, une facturation centralisée et aucune configuration d'infrastructure requise.

**Claude for Teams** est en libre-service et inclut des fonctionnalités de collaboration, des outils d'administration et la gestion de la facturation. Idéal pour les petites équipes qui ont besoin de démarrer rapidement.

**Claude for Enterprise** ajoute SSO et la capture de domaine, les autorisations basées sur les rôles, l'accès à l'API de conformité et les paramètres de politique gérés pour déployer des configurations Claude Code à l'échelle de l'organisation. Idéal pour les grandes organisations ayant des exigences de sécurité et de conformité.

En savoir plus sur les [plans d'équipe](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) et les [plans d'entreprise](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan).

Si votre organisation a des exigences d'infrastructure spécifiques, comparez les options ci-dessous :

<table>
  <thead>
    <tr>
      <th>Fonctionnalité</th>
      <th>Claude for Teams/Enterprise</th>
      <th>Anthropic Console</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Idéal pour</td>
      <td>La plupart des organisations (recommandé)</td>
      <td>Développeurs individuels</td>
      <td>Déploiements natifs AWS</td>
      <td>Déploiements natifs GCP</td>
      <td>Déploiements natifs Azure</td>
    </tr>

    <tr>
      <td>Facturation</td>
      <td><strong>Teams :</strong> 150 \$/siège (Premium) avec PAYG disponible<br /><strong>Enterprise :</strong> <a href="https://claude.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=third_party_enterprise">Contacter les ventes</a></td>
      <td>PAYG</td>
      <td>PAYG via AWS</td>
      <td>PAYG via GCP</td>
      <td>PAYG via Azure</td>
    </tr>

    <tr>
      <td>Régions</td>
      <td>[Pays](https://www.anthropic.com/supported-countries) supportés</td>
      <td>[Pays](https://www.anthropic.com/supported-countries) supportés</td>
      <td>Plusieurs [régions](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html) AWS</td>
      <td>Plusieurs [régions](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations) GCP</td>
      <td>Plusieurs [régions](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/) Azure</td>
    </tr>

    <tr>
      <td>Prompt caching</td>
      <td>Activé par défaut</td>
      <td>Activé par défaut</td>
      <td>Activé par défaut</td>
      <td>Activé par défaut</td>
      <td>Activé par défaut</td>
    </tr>

    <tr>
      <td>Authentification</td>
      <td>Claude.ai SSO ou email</td>
      <td>Clé API</td>
      <td>Clé API ou identifiants AWS</td>
      <td>Identifiants GCP</td>
      <td>Clé API ou Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>Suivi des coûts</td>
      <td>Tableau de bord d'utilisation</td>
      <td>Tableau de bord d'utilisation</td>
      <td>AWS Cost Explorer</td>
      <td>Facturation GCP</td>
      <td>Gestion des coûts Azure</td>
    </tr>

    <tr>
      <td>Inclut Claude sur le web</td>
      <td>Oui</td>
      <td>Non</td>
      <td>Non</td>
      <td>Non</td>
      <td>Non</td>
    </tr>

    <tr>
      <td>Fonctionnalités d'entreprise</td>
      <td>Gestion d'équipe, SSO, surveillance de l'utilisation</td>
      <td>Aucune</td>
      <td>Politiques IAM, CloudTrail</td>
      <td>Rôles IAM, journaux d'audit cloud</td>
      <td>Politiques RBAC, Azure Monitor</td>
    </tr>
  </tbody>
</table>

Sélectionnez une option de déploiement pour afficher les instructions de configuration :

* [Claude for Teams ou Enterprise](/fr/authentication#claude-for-teams-or-enterprise)
* [Anthropic Console](/fr/authentication#claude-console-authentication)
* [Amazon Bedrock](/fr/amazon-bedrock)
* [Google Vertex AI](/fr/google-vertex-ai)
* [Microsoft Foundry](/fr/microsoft-foundry)

## Configurer les proxies et les passerelles

La plupart des organisations peuvent utiliser un fournisseur de cloud directement sans configuration supplémentaire. Cependant, vous devrez peut-être configurer un proxy d'entreprise ou une passerelle LLM si votre organisation a des exigences réseau ou de gestion spécifiques. Il s'agit de configurations différentes qui peuvent être utilisées ensemble :

* **Proxy d'entreprise** : Achemine le trafic via un proxy HTTP/HTTPS. Utilisez ceci si votre organisation exige que tout le trafic sortant passe par un serveur proxy pour la surveillance de la sécurité, la conformité ou l'application des politiques réseau. Configurez avec les variables d'environnement `HTTPS_PROXY` ou `HTTP_PROXY`. En savoir plus dans [Configuration du réseau d'entreprise](/fr/network-config).
* **Passerelle LLM** : Un service qui se situe entre Claude Code et le fournisseur de cloud pour gérer l'authentification et le routage. Utilisez ceci si vous avez besoin d'un suivi centralisé de l'utilisation entre les équipes, d'une limitation de débit personnalisée ou de budgets, ou d'une gestion centralisée de l'authentification. Configurez avec les variables d'environnement `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL` ou `ANTHROPIC_VERTEX_BASE_URL`. En savoir plus dans [Configuration de la passerelle LLM](/fr/llm-gateway).

Les exemples suivants montrent les variables d'environnement à définir dans votre shell ou profil shell (`.bashrc`, `.zshrc`). Voir [Paramètres](/fr/settings) pour d'autres méthodes de configuration.

### Amazon Bedrock

<Tabs>
  <Tab title="Proxy d'entreprise">
    Acheminez le trafic Bedrock via votre proxy d'entreprise en définissant les [variables d'environnement](/fr/env-vars) suivantes :

    ```bash  theme={null}
    # Enable Bedrock
    export CLAUDE_CODE_USE_BEDROCK=1
    export AWS_REGION=us-east-1

    # Configure corporate proxy
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="Passerelle LLM">
    Acheminez le trafic Bedrock via votre passerelle LLM en définissant les [variables d'environnement](/fr/env-vars) suivantes :

    ```bash  theme={null}
    # Enable Bedrock
    export CLAUDE_CODE_USE_BEDROCK=1

    # Configure LLM gateway
    export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
    export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # If gateway handles AWS auth
    ```
  </Tab>
</Tabs>

### Microsoft Foundry

<Tabs>
  <Tab title="Proxy d'entreprise">
    Acheminez le trafic Foundry via votre proxy d'entreprise en définissant les [variables d'environnement](/fr/env-vars) suivantes :

    ```bash  theme={null}
    # Enable Microsoft Foundry
    export CLAUDE_CODE_USE_FOUNDRY=1
    export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
    export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # Or omit for Entra ID auth

    # Configure corporate proxy
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="Passerelle LLM">
    Acheminez le trafic Foundry via votre passerelle LLM en définissant les [variables d'environnement](/fr/env-vars) suivantes :

    ```bash  theme={null}
    # Enable Microsoft Foundry
    export CLAUDE_CODE_USE_FOUNDRY=1

    # Configure LLM gateway
    export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
    export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # If gateway handles Azure auth
    ```
  </Tab>
</Tabs>

### Google Vertex AI

<Tabs>
  <Tab title="Proxy d'entreprise">
    Acheminez le trafic Vertex AI via votre proxy d'entreprise en définissant les [variables d'environnement](/fr/env-vars) suivantes :

    ```bash  theme={null}
    # Enable Vertex
    export CLAUDE_CODE_USE_VERTEX=1
    export CLOUD_ML_REGION=us-east5
    export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

    # Configure corporate proxy
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="Passerelle LLM">
    Acheminez le trafic Vertex AI via votre passerelle LLM en définissant les [variables d'environnement](/fr/env-vars) suivantes :

    ```bash  theme={null}
    # Enable Vertex
    export CLAUDE_CODE_USE_VERTEX=1

    # Configure LLM gateway
    export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
    export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # If gateway handles GCP auth
    ```
  </Tab>
</Tabs>

<Tip>
  Utilisez `/status` dans Claude Code pour vérifier que votre configuration de proxy et de passerelle est appliquée correctement.
</Tip>

## Meilleures pratiques pour les organisations

### Investir dans la documentation et la mémoire

Nous recommandons vivement d'investir dans la documentation afin que Claude Code comprenne votre base de code. Les organisations peuvent déployer des fichiers CLAUDE.md à plusieurs niveaux :

* **À l'échelle de l'organisation** : Déployez dans des répertoires système comme `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) pour les normes à l'échelle de l'entreprise
* **Au niveau du référentiel** : Créez des fichiers `CLAUDE.md` dans les racines de référentiel contenant l'architecture du projet, les commandes de compilation et les directives de contribution. Vérifiez-les dans le contrôle de source afin que tous les utilisateurs en bénéficient

En savoir plus dans [Mémoire et fichiers CLAUDE.md](/fr/memory).

### Simplifier le déploiement

Si vous avez un environnement de développement personnalisé, nous constatons que créer un moyen « en un clic » d'installer Claude Code est essentiel pour augmenter l'adoption dans une organisation.

### Commencer par une utilisation guidée

Encouragez les nouveaux utilisateurs à essayer Claude Code pour les questions sur la base de code, ou sur les corrections de bogues plus petites ou les demandes de fonctionnalités. Demandez à Claude Code de faire un plan. Vérifiez les suggestions de Claude et donnez des commentaires si c'est hors piste. Au fil du temps, à mesure que les utilisateurs comprendront mieux ce nouveau paradigme, ils seront plus efficaces pour laisser Claude Code fonctionner de manière plus agentique.

### Épingler les versions de modèle pour les fournisseurs de cloud

Si vous déployez via [Bedrock](/fr/amazon-bedrock), [Vertex AI](/fr/google-vertex-ai) ou [Foundry](/fr/microsoft-foundry), épinglez les versions de modèle spécifiques en utilisant `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` et `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Sans épinglage, les alias Claude Code se résolvent à la dernière version, ce qui peut casser les utilisateurs lorsqu'Anthropic publie un nouveau modèle qui n'est pas encore activé dans votre compte. Voir [Configuration du modèle](/fr/model-config#pin-models-for-third-party-deployments) pour plus de détails.

### Configurer les politiques de sécurité

Les équipes de sécurité peuvent configurer des autorisations gérées pour ce que Claude Code est et n'est pas autorisé à faire, ce qui ne peut pas être remplacé par la configuration locale. [En savoir plus](/fr/security).

### Tirer parti de MCP pour les intégrations

MCP est un excellent moyen de donner à Claude Code plus d'informations, comme la connexion à des systèmes de gestion de tickets ou des journaux d'erreurs. Nous recommandons qu'une équipe centrale configure les serveurs MCP et vérifie une configuration `.mcp.json` dans la base de code afin que tous les utilisateurs en bénéficient. [En savoir plus](/fr/mcp).

Chez Anthropic, nous faisons confiance à Claude Code pour alimenter le développement dans chaque base de code Anthropic. Nous espérons que vous apprécierez d'utiliser Claude Code autant que nous.

## Étapes suivantes

Une fois que vous avez choisi une option de déploiement et configuré l'accès pour votre équipe :

1. **Déployer auprès de votre équipe** : Partagez les instructions d'installation et demandez aux membres de l'équipe d'[installer Claude Code](/fr/setup) et de s'authentifier avec leurs identifiants.
2. **Configurer la configuration partagée** : Créez un [fichier CLAUDE.md](/fr/memory) dans vos référentiels pour aider Claude Code à comprendre votre base de code et vos normes de codage.
3. **Configurer les autorisations** : Consultez les [paramètres de sécurité](/fr/security) pour définir ce que Claude Code peut et ne peut pas faire dans votre environnement.
