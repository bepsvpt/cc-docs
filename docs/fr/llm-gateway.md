> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuration de la passerelle LLM

> Découvrez comment configurer Claude Code pour fonctionner avec des solutions de passerelle LLM. Couvre les exigences de la passerelle, la configuration de l'authentification, la sélection du modèle et la configuration des points de terminaison spécifiques aux fournisseurs.

Les passerelles LLM fournissent une couche proxy centralisée entre Claude Code et les fournisseurs de modèles, offrant souvent :

* **Authentification centralisée** - Point unique pour la gestion des clés API
* **Suivi de l'utilisation** - Surveiller l'utilisation entre les équipes et les projets
* **Contrôles des coûts** - Implémenter des budgets et des limites de débit
* **Journalisation d'audit** - Suivre toutes les interactions de modèle pour la conformité
* **Routage des modèles** - Basculer entre les fournisseurs sans modifications de code

## Exigences de la passerelle

Pour qu'une passerelle LLM fonctionne avec Claude Code, elle doit répondre aux exigences suivantes :

**Format API**

La passerelle doit exposer aux clients au moins l'un des formats API suivants :

1. **Anthropic Messages** : `/v1/messages`, `/v1/messages/count_tokens`
   * Doit transférer les en-têtes de requête : `anthropic-beta`, `anthropic-version`

2. **Bedrock InvokeModel** : `/invoke`, `/invoke-with-response-stream`
   * Doit préserver les champs du corps de la requête : `anthropic_beta`, `anthropic_version`

3. **Vertex rawPredict** : `:rawPredict`, `:streamRawPredict`, `/count-tokens:rawPredict`
   * Doit transférer les en-têtes de requête : `anthropic-beta`, `anthropic-version`

L'absence de transfert d'en-têtes ou la non-préservation des champs du corps peut entraîner une réduction des fonctionnalités ou l'impossibilité d'utiliser les fonctionnalités de Claude Code.

<Note>
  Claude Code détermine les fonctionnalités à activer en fonction du format API. Lors de l'utilisation du format Anthropic Messages avec Bedrock ou Vertex, vous devrez peut-être définir la variable d'environnement `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`.
</Note>

## Configuration

### Sélection du modèle

Par défaut, Claude Code utilisera les noms de modèles standard pour le format API sélectionné.

Si vous avez configuré des noms de modèles personnalisés dans votre passerelle, utilisez les variables d'environnement documentées dans [Configuration du modèle](/fr/model-config) pour correspondre à vos noms personnalisés.

## Configuration de LiteLLM

<Warning>
  Les versions PyPI de LiteLLM 1.82.7 et 1.82.8 ont été compromises avec un malware voleur d'identifiants. N'installez pas ces versions. Si vous les avez déjà installées :

  * Supprimez le paquet
  * Renouvelez tous les identifiants sur les systèmes affectés
  * Suivez les étapes de correction dans [BerriAI/litellm#24518](https://github.com/BerriAI/litellm/issues/24518)

  LiteLLM est un service proxy tiers. Anthropic n'approuve pas, ne maintient pas et n'audite pas la sécurité ou les fonctionnalités de LiteLLM. Ce guide est fourni à titre informatif et peut devenir obsolète. À utiliser à votre discrétion.
</Warning>

### Conditions préalables

* Claude Code mis à jour vers la dernière version
* Serveur proxy LiteLLM déployé et accessible
* Accès aux modèles Claude via votre fournisseur choisi

### Configuration de base de LiteLLM

**Configurer Claude Code** :

#### Méthodes d'authentification

##### Clé API statique

Méthode la plus simple utilisant une clé API fixe :

```bash  theme={null}
# Définir dans l'environnement
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# Ou dans les paramètres de Claude Code
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

Cette valeur sera envoyée en tant qu'en-tête `Authorization`.

##### Clé API dynamique avec assistant

Pour les clés rotatives ou l'authentification par utilisateur :

1. Créez un script d'assistant de clé API :

```bash  theme={null}
#!/bin/bash
# ~/bin/get-litellm-key.sh

# Exemple : Récupérer la clé du coffre-fort
vault kv get -field=api_key secret/litellm/claude-code

# Exemple : Générer un jeton JWT
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'
```

2. Configurez les paramètres de Claude Code pour utiliser l'assistant :

```json  theme={null}
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. Définissez l'intervalle d'actualisation du jeton :

```bash  theme={null}
# Actualiser toutes les heures (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

Cette valeur sera envoyée en tant qu'en-têtes `Authorization` et `X-Api-Key`. L'`apiKeyHelper` a une priorité inférieure à `ANTHROPIC_AUTH_TOKEN` ou `ANTHROPIC_API_KEY`.

#### Point de terminaison unifié (recommandé)

Utilisant le [point de terminaison au format Anthropic](https://docs.litellm.ai/docs/anthropic_unified) de LiteLLM :

```bash  theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**Avantages du point de terminaison unifié par rapport aux points de terminaison de transmission directe :**

* Équilibrage de charge
* Basculements
* Support cohérent du suivi des coûts et du suivi des utilisateurs finaux

#### Points de terminaison de transmission directe spécifiques aux fournisseurs (alternative)

##### API Claude via LiteLLM

Utilisant le [point de terminaison de transmission directe](https://docs.litellm.ai/docs/pass_through/anthropic_completion) :

```bash  theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### Amazon Bedrock via LiteLLM

Utilisant le [point de terminaison de transmission directe](https://docs.litellm.ai/docs/pass_through/bedrock) :

```bash  theme={null}
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### Google Vertex AI via LiteLLM

Utilisant le [point de terminaison de transmission directe](https://docs.litellm.ai/docs/pass_through/vertex_ai) :

```bash  theme={null}
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

Pour plus d'informations détaillées, consultez la [documentation de LiteLLM](https://docs.litellm.ai/).

## Ressources supplémentaires

* [Documentation de LiteLLM](https://docs.litellm.ai/)
* [Paramètres de Claude Code](/fr/settings)
* [Configuration du réseau d'entreprise](/fr/network-config)
* [Aperçu des intégrations tierces](/fr/third-party-integrations)
