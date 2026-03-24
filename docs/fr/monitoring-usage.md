> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Surveillance

> Découvrez comment activer et configurer OpenTelemetry pour Claude Code.

Suivez l'utilisation de Claude Code, les coûts et l'activité des outils dans votre organisation en exportant les données de télémétrie via OpenTelemetry (OTel). Claude Code exporte les métriques sous forme de données de séries chronologiques via le protocole de métriques standard, et les événements via le protocole de journaux/événements. Configurez vos backends de métriques et de journaux pour qu'ils correspondent à vos exigences de surveillance.

## Démarrage rapide

Configurez OpenTelemetry à l'aide de variables d'environnement :

```bash  theme={null}
# 1. Activer la télémétrie
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. Choisir les exportateurs (les deux sont facultatifs - configurez uniquement ce dont vous avez besoin)
export OTEL_METRICS_EXPORTER=otlp       # Options : otlp, prometheus, console
export OTEL_LOGS_EXPORTER=otlp          # Options : otlp, console

# 3. Configurer le point de terminaison OTLP (pour l'exportateur OTLP)
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. Définir l'authentification (si nécessaire)
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. Pour le débogage : réduire les intervalles d'export
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 secondes (par défaut : 60000ms)
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 secondes (par défaut : 5000ms)

# 6. Exécuter Claude Code
claude
```

<Note>
  Les intervalles d'export par défaut sont de 60 secondes pour les métriques et de 5 secondes pour les journaux. Lors de la configuration, vous pouvez utiliser des intervalles plus courts à des fins de débogage. N'oubliez pas de les réinitialiser pour une utilisation en production.
</Note>

Pour les options de configuration complètes, consultez la [spécification OpenTelemetry](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options).

## Configuration de l'administrateur

Les administrateurs peuvent configurer les paramètres OpenTelemetry pour tous les utilisateurs via le [fichier de paramètres gérés](/fr/settings#settings-files). Cela permet un contrôle centralisé des paramètres de télémétrie dans toute une organisation. Consultez la [précédence des paramètres](/fr/settings#settings-precedence) pour plus d'informations sur la façon dont les paramètres sont appliqués.

Exemple de configuration des paramètres gérés :

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer example-token"
  }
}
```

<Note>
  Les paramètres gérés peuvent être distribués via MDM (Mobile Device Management) ou d'autres solutions de gestion d'appareils. Les variables d'environnement définies dans le fichier de paramètres gérés ont une haute priorité et ne peuvent pas être remplacées par les utilisateurs.
</Note>

## Détails de la configuration

### Variables de configuration courantes

| Variable d'environnement                            | Description                                                                                                                                    | Exemples de valeurs                         |
| --------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------- |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                      | Active la collecte de télémétrie (obligatoire)                                                                                                 | `1`                                         |
| `OTEL_METRICS_EXPORTER`                             | Types d'exportateur de métriques, séparés par des virgules                                                                                     | `console`, `otlp`, `prometheus`             |
| `OTEL_LOGS_EXPORTER`                                | Types d'exportateur de journaux/événements, séparés par des virgules                                                                           | `console`, `otlp`                           |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                       | Protocole pour l'exportateur OTLP, s'applique à tous les signaux                                                                               | `grpc`, `http/json`, `http/protobuf`        |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                       | Point de terminaison du collecteur OTLP pour tous les signaux                                                                                  | `http://localhost:4317`                     |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`               | Protocole pour les métriques, remplace le paramètre général                                                                                    | `grpc`, `http/json`, `http/protobuf`        |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`               | Point de terminaison des métriques OTLP, remplace le paramètre général                                                                         | `http://localhost:4318/v1/metrics`          |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`                  | Protocole pour les journaux, remplace le paramètre général                                                                                     | `grpc`, `http/json`, `http/protobuf`        |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`                  | Point de terminaison des journaux OTLP, remplace le paramètre général                                                                          | `http://localhost:4318/v1/logs`             |
| `OTEL_EXPORTER_OTLP_HEADERS`                        | En-têtes d'authentification pour OTLP                                                                                                          | `Authorization=Bearer token`                |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`             | Clé client pour l'authentification mTLS                                                                                                        | Chemin vers le fichier de clé client        |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE`     | Certificat client pour l'authentification mTLS                                                                                                 | Chemin vers le fichier de certificat client |
| `OTEL_METRIC_EXPORT_INTERVAL`                       | Intervalle d'export en millisecondes (par défaut : 60000)                                                                                      | `5000`, `60000`                             |
| `OTEL_LOGS_EXPORT_INTERVAL`                         | Intervalle d'export des journaux en millisecondes (par défaut : 5000)                                                                          | `1000`, `10000`                             |
| `OTEL_LOG_USER_PROMPTS`                             | Activer la journalisation du contenu des invites utilisateur (par défaut : désactivé)                                                          | `1` pour activer                            |
| `OTEL_LOG_TOOL_DETAILS`                             | Activer la journalisation des noms de serveur MCP/outil et des noms de compétences dans les événements d'outil (par défaut : désactivé)        | `1` pour activer                            |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | Préférence de temporalité des métriques (par défaut : `delta`). Définissez sur `cumulative` si votre backend attend une temporalité cumulative | `delta`, `cumulative`                       |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`       | Intervalle d'actualisation des en-têtes dynamiques (par défaut : 1740000ms / 29 minutes)                                                       | `900000`                                    |

### Contrôle de la cardinalité des métriques

Les variables d'environnement suivantes contrôlent les attributs inclus dans les métriques pour gérer la cardinalité :

| Variable d'environnement            | Description                                              | Valeur par défaut | Exemple pour désactiver |
| ----------------------------------- | -------------------------------------------------------- | ----------------- | ----------------------- |
| `OTEL_METRICS_INCLUDE_SESSION_ID`   | Inclure l'attribut session.id dans les métriques         | `true`            | `false`                 |
| `OTEL_METRICS_INCLUDE_VERSION`      | Inclure l'attribut app.version dans les métriques        | `false`           | `true`                  |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | Inclure l'attribut user.account\_uuid dans les métriques | `true`            | `false`                 |

Ces variables aident à contrôler la cardinalité des métriques, ce qui affecte les exigences de stockage et les performances des requêtes dans votre backend de métriques. Une cardinalité plus faible signifie généralement de meilleures performances et des coûts de stockage plus bas, mais des données moins granulaires pour l'analyse.

### En-têtes dynamiques

Pour les environnements d'entreprise qui nécessitent une authentification dynamique, vous pouvez configurer un script pour générer des en-têtes dynamiquement :

#### Configuration des paramètres

Ajoutez à votre `.claude/settings.json` :

```json  theme={null}
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

#### Exigences du script

Le script doit générer du JSON valide avec des paires clé-valeur de chaînes représentant les en-têtes HTTP :

```bash  theme={null}
#!/bin/bash
# Exemple : plusieurs en-têtes
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

#### Comportement d'actualisation

Le script d'aide des en-têtes s'exécute au démarrage et périodiquement par la suite pour prendre en charge l'actualisation des jetons. Par défaut, le script s'exécute toutes les 29 minutes. Personnalisez l'intervalle avec la variable d'environnement `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`.

### Support des organisations multi-équipes

Les organisations avec plusieurs équipes ou départements peuvent ajouter des attributs personnalisés pour distinguer les différents groupes à l'aide de la variable d'environnement `OTEL_RESOURCE_ATTRIBUTES` :

```bash  theme={null}
# Ajouter des attributs personnalisés pour l'identification de l'équipe
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

Ces attributs personnalisés seront inclus dans toutes les métriques et tous les événements, ce qui vous permet de :

* Filtrer les métriques par équipe ou département
* Suivre les coûts par centre de coûts
* Créer des tableaux de bord spécifiques à l'équipe
* Configurer des alertes pour des équipes spécifiques

<Warning>
  **Exigences importantes de formatage pour OTEL\_RESOURCE\_ATTRIBUTES :**

  La variable d'environnement `OTEL_RESOURCE_ATTRIBUTES` utilise des paires clé=valeur séparées par des virgules avec des exigences de formatage strictes :

  * **Aucun espace autorisé** : Les valeurs ne peuvent pas contenir d'espaces. Par exemple, `user.organizationName=My Company` est invalide
  * **Format** : Doit être des paires clé=valeur séparées par des virgules : `key1=value1,key2=value2`
  * **Caractères autorisés** : Uniquement les caractères US-ASCII à l'exclusion des caractères de contrôle, des espaces, des guillemets doubles, des virgules, des points-virgules et des barres obliques inverses
  * **Caractères spéciaux** : Les caractères en dehors de la plage autorisée doivent être codés en pourcentage

  **Exemples :**

  ```bash  theme={null}
  # ❌ Invalide - contient des espaces
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John's Organization"

  # ✅ Valide - utiliser des traits de soulignement ou camelCase à la place
  export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"
  export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"

  # ✅ Valide - coder en pourcentage les caractères spéciaux si nécessaire
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"
  ```

  Remarque : entourer les valeurs de guillemets n'échappe pas aux espaces. Par exemple, `org.name="My Company"` donne la valeur littérale `"My Company"` (avec guillemets inclus), pas `My Company`.
</Warning>

### Exemples de configurations

Définissez ces variables d'environnement avant d'exécuter `claude`. Chaque bloc montre une configuration complète pour un exportateur ou un scénario de déploiement différent :

```bash  theme={null}
# Débogage de console (intervalles de 1 seconde)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000

# OTLP/gRPC
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus

# Plusieurs exportateurs
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json

# Points de terminaison/backends différents pour les métriques et les journaux
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.example.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.example.com:4317

# Métriques uniquement (pas d'événements/journaux)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Événements/journaux uniquement (pas de métriques)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## Métriques et événements disponibles

### Attributs standard

Toutes les métriques et tous les événements partagent ces attributs standard :

| Attribut            | Description                                                                         | Contrôlé par                                            |
| ------------------- | ----------------------------------------------------------------------------------- | ------------------------------------------------------- |
| `session.id`        | Identifiant de session unique                                                       | `OTEL_METRICS_INCLUDE_SESSION_ID` (par défaut : true)   |
| `app.version`       | Version actuelle de Claude Code                                                     | `OTEL_METRICS_INCLUDE_VERSION` (par défaut : false)     |
| `organization.id`   | UUID de l'organisation (si authentifié)                                             | Toujours inclus si disponible                           |
| `user.account_uuid` | UUID du compte (si authentifié)                                                     | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (par défaut : true) |
| `user.id`           | Identifiant anonyme d'appareil/installation, généré par installation de Claude Code | Toujours inclus                                         |
| `user.email`        | Adresse e-mail de l'utilisateur (si authentifié via OAuth)                          | Toujours inclus si disponible                           |
| `terminal.type`     | Type de terminal, tel que `iTerm.app`, `vscode`, `cursor`, ou `tmux`                | Toujours inclus si détecté                              |

### Métriques

Claude Code exporte les métriques suivantes :

| Nom de la métrique                    | Description                                                    | Unité  |
| ------------------------------------- | -------------------------------------------------------------- | ------ |
| `claude_code.session.count`           | Nombre de sessions CLI démarrées                               | count  |
| `claude_code.lines_of_code.count`     | Nombre de lignes de code modifiées                             | count  |
| `claude_code.pull_request.count`      | Nombre de demandes de tirage créées                            | count  |
| `claude_code.commit.count`            | Nombre de commits git créés                                    | count  |
| `claude_code.cost.usage`              | Coût de la session Claude Code                                 | USD    |
| `claude_code.token.usage`             | Nombre de jetons utilisés                                      | tokens |
| `claude_code.code_edit_tool.decision` | Nombre de décisions de permission de l'outil d'édition de code | count  |
| `claude_code.active_time.total`       | Temps actif total en secondes                                  | s      |

### Détails des métriques

Chaque métrique inclut les attributs standard listés ci-dessus. Les métriques avec des attributs supplémentaires spécifiques au contexte sont notées ci-dessous.

#### Compteur de sessions

Incrémenté au début de chaque session.

**Attributs** :

* Tous les [attributs standard](#standard-attributes)

#### Compteur de lignes de code

Incrémenté lorsque du code est ajouté ou supprimé.

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `type` : (`"added"`, `"removed"`)

#### Compteur de demandes de tirage

Incrémenté lors de la création de demandes de tirage via Claude Code.

**Attributs** :

* Tous les [attributs standard](#standard-attributes)

#### Compteur de commits

Incrémenté lors de la création de commits git via Claude Code.

**Attributs** :

* Tous les [attributs standard](#standard-attributes)

#### Compteur de coûts

Incrémenté après chaque demande d'API.

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `model` : Identifiant du modèle (par exemple, « claude-sonnet-4-6 »)

#### Compteur de jetons

Incrémenté après chaque demande d'API.

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `type` : (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)
* `model` : Identifiant du modèle (par exemple, « claude-sonnet-4-6 »)

#### Compteur de décisions de l'outil d'édition de code

Incrémenté lorsque l'utilisateur accepte ou rejette l'utilisation de l'outil Edit, Write ou NotebookEdit.

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `tool_name` : Nom de l'outil (`"Edit"`, `"Write"`, `"NotebookEdit"`)
* `decision` : Décision de l'utilisateur (`"accept"`, `"reject"`)
* `source` : Source de la décision - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, ou `"user_reject"`
* `language` : Langage de programmation du fichier édité, tel que `"TypeScript"`, `"Python"`, `"JavaScript"`, ou `"Markdown"`. Retourne `"unknown"` pour les extensions de fichier non reconnues.

#### Compteur de temps actif

Suit le temps réel passé à utiliser activement Claude Code, excluant le temps d'inactivité. Cette métrique est incrémentée lors des interactions utilisateur (saisie, lecture des réponses) et lors du traitement CLI (exécution d'outils, génération de réponses IA).

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `type` : `"user"` pour les interactions au clavier, `"cli"` pour l'exécution d'outils et les réponses IA

### Événements

Claude Code exporte les événements suivants via les journaux/événements OpenTelemetry (lorsque `OTEL_LOGS_EXPORTER` est configuré) :

#### Attributs de corrélation d'événements

Lorsqu'un utilisateur soumet une invite, Claude Code peut effectuer plusieurs appels d'API et exécuter plusieurs outils. L'attribut `prompt.id` vous permet de lier tous ces événements à l'invite unique qui les a déclenchés.

| Attribut    | Description                                                                                               |
| ----------- | --------------------------------------------------------------------------------------------------------- |
| `prompt.id` | Identifiant UUID v4 liant tous les événements produits lors du traitement d'une invite utilisateur unique |

Pour tracer toute l'activité déclenchée par une invite unique, filtrez vos événements par une valeur `prompt.id` spécifique. Cela retourne l'événement user\_prompt, tous les événements api\_request, et tous les événements tool\_result qui se sont produits lors du traitement de cette invite.

<Note>
  `prompt.id` est intentionnellement exclu des métriques car chaque invite génère un ID unique, ce qui créerait un nombre toujours croissant de séries chronologiques. Utilisez-le uniquement pour l'analyse au niveau des événements et les pistes d'audit.
</Note>

#### Événement d'invite utilisateur

Enregistré lorsqu'un utilisateur soumet une invite.

**Nom de l'événement** : `claude_code.user_prompt`

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `event.name` : `"user_prompt"`
* `event.timestamp` : Horodatage ISO 8601
* `event.sequence` : Compteur monotone croissant pour ordonner les événements au sein d'une session
* `prompt_length` : Longueur de l'invite
* `prompt` : Contenu de l'invite (masqué par défaut, activez avec `OTEL_LOG_USER_PROMPTS=1`)

#### Événement de résultat d'outil

Enregistré lorsqu'un outil termine son exécution.

**Nom de l'événement** : `claude_code.tool_result`

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `event.name` : `"tool_result"`
* `event.timestamp` : Horodatage ISO 8601
* `event.sequence` : Compteur monotone croissant pour ordonner les événements au sein d'une session
* `tool_name` : Nom de l'outil
* `success` : `"true"` ou `"false"`
* `duration_ms` : Temps d'exécution en millisecondes
* `error` : Message d'erreur (en cas d'échec)
* `decision_type` : Soit `"accept"` soit `"reject"`
* `decision_source` : Source de la décision - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, ou `"user_reject"`
* `tool_result_size_bytes` : Taille du résultat de l'outil en octets
* `mcp_server_scope` : Identifiant de portée du serveur MCP (pour les outils MCP)
* `tool_parameters` : Chaîne JSON contenant les paramètres spécifiques à l'outil (si disponible)
  * Pour l'outil Bash : inclut `bash_command`, `full_command`, `timeout`, `description`, `dangerouslyDisableSandbox`, et `git_commit_id` (le SHA du commit, lorsqu'une commande `git commit` réussit)
  * Pour les outils MCP (lorsque `OTEL_LOG_TOOL_DETAILS=1`) : inclut `mcp_server_name`, `mcp_tool_name`
  * Pour l'outil Skill (lorsque `OTEL_LOG_TOOL_DETAILS=1`) : inclut `skill_name`

#### Événement de demande d'API

Enregistré pour chaque demande d'API à Claude.

**Nom de l'événement** : `claude_code.api_request`

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `event.name` : `"api_request"`
* `event.timestamp` : Horodatage ISO 8601
* `event.sequence` : Compteur monotone croissant pour ordonner les événements au sein d'une session
* `model` : Modèle utilisé (par exemple, « claude-sonnet-4-6 »)
* `cost_usd` : Coût estimé en USD
* `duration_ms` : Durée de la demande en millisecondes
* `input_tokens` : Nombre de jetons d'entrée
* `output_tokens` : Nombre de jetons de sortie
* `cache_read_tokens` : Nombre de jetons lus à partir du cache
* `cache_creation_tokens` : Nombre de jetons utilisés pour la création du cache
* `speed` : `"fast"` ou `"normal"`, indiquant si le mode rapide était actif

#### Événement d'erreur d'API

Enregistré lorsqu'une demande d'API à Claude échoue.

**Nom de l'événement** : `claude_code.api_error`

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `event.name` : `"api_error"`
* `event.timestamp` : Horodatage ISO 8601
* `event.sequence` : Compteur monotone croissant pour ordonner les événements au sein d'une session
* `model` : Modèle utilisé (par exemple, « claude-sonnet-4-6 »)
* `error` : Message d'erreur
* `status_code` : Code de statut HTTP sous forme de chaîne, ou `"undefined"` pour les erreurs non-HTTP
* `duration_ms` : Durée de la demande en millisecondes
* `attempt` : Numéro de tentative (pour les demandes réessayées)
* `speed` : `"fast"` ou `"normal"`, indiquant si le mode rapide était actif

#### Événement de décision d'outil

Enregistré lorsqu'une décision de permission d'outil est prise (accepter/rejeter).

**Nom de l'événement** : `claude_code.tool_decision`

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `event.name` : `"tool_decision"`
* `event.timestamp` : Horodatage ISO 8601
* `event.sequence` : Compteur monotone croissant pour ordonner les événements au sein d'une session
* `tool_name` : Nom de l'outil (par exemple, « Read », « Edit », « Write », « NotebookEdit »)
* `decision` : Soit `"accept"` soit `"reject"`
* `source` : Source de la décision - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, ou `"user_reject"`

## Interpréter les données de métriques et d'événements

Les métriques et événements exportés prennent en charge une gamme d'analyses :

### Surveillance de l'utilisation

| Métrique                                                      | Opportunité d'analyse                                              |
| ------------------------------------------------------------- | ------------------------------------------------------------------ |
| `claude_code.token.usage`                                     | Ventiler par `type` (entrée/sortie), utilisateur, équipe ou modèle |
| `claude_code.session.count`                                   | Suivre l'adoption et l'engagement au fil du temps                  |
| `claude_code.lines_of_code.count`                             | Mesurer la productivité en suivant les ajouts/suppressions de code |
| `claude_code.commit.count` & `claude_code.pull_request.count` | Comprendre l'impact sur les flux de travail de développement       |

### Surveillance des coûts

La métrique `claude_code.cost.usage` aide à :

* Suivre les tendances d'utilisation entre les équipes ou les individus
* Identifier les sessions à utilisation élevée pour l'optimisation

<Note>
  Les métriques de coûts sont des approximations. Pour les données de facturation officielles, consultez votre fournisseur d'API (Claude Console, AWS Bedrock ou Google Cloud Vertex).
</Note>

### Alertes et segmentation

Les alertes courantes à considérer :

* Pics de coûts
* Consommation de jetons inhabituelle
* Volume de session élevé d'utilisateurs spécifiques

Toutes les métriques peuvent être segmentées par `user.account_uuid`, `organization.id`, `session.id`, `model`, et `app.version`.

### Analyse des événements

Les données d'événements fournissent des informations détaillées sur les interactions de Claude Code :

**Modèles d'utilisation des outils** : analyser les événements de résultat d'outil pour identifier :

* Les outils les plus fréquemment utilisés
* Les taux de réussite des outils
* Les temps d'exécution moyens des outils
* Les modèles d'erreur par type d'outil

**Surveillance des performances** : suivre les durées des demandes d'API et les temps d'exécution des outils pour identifier les goulots d'étranglement de performance.

## Considérations relatives aux backends

Votre choix de backends de métriques et de journaux détermine les types d'analyses que vous pouvez effectuer :

### Pour les métriques

* **Bases de données de séries chronologiques (par exemple, Prometheus)** : Calculs de taux, métriques agrégées
* **Magasins colonnaires (par exemple, ClickHouse)** : Requêtes complexes, analyse d'utilisateurs uniques
* **Plates-formes d'observabilité complètes (par exemple, Honeycomb, Datadog)** : Requêtes avancées, visualisation, alertes

### Pour les événements/journaux

* **Systèmes d'agrégation de journaux (par exemple, Elasticsearch, Loki)** : Recherche en texte intégral, analyse de journaux
* **Magasins colonnaires (par exemple, ClickHouse)** : Analyse d'événements structurés
* **Plates-formes d'observabilité complètes (par exemple, Honeycomb, Datadog)** : Corrélation entre les métriques et les événements

Pour les organisations nécessitant des métriques d'utilisateurs actifs quotidiens/hebdomadaires/mensuels (DAU/WAU/MAU), envisagez des backends qui prennent en charge les requêtes de valeurs uniques efficaces.

## Informations sur le service

Toutes les métriques et tous les événements sont exportés avec les attributs de ressource suivants :

* `service.name` : `claude-code`
* `service.version` : Version actuelle de Claude Code
* `os.type` : Type de système d'exploitation (par exemple, `linux`, `darwin`, `windows`)
* `os.version` : Chaîne de version du système d'exploitation
* `host.arch` : Architecture de l'hôte (par exemple, `amd64`, `arm64`)
* `wsl.version` : Numéro de version WSL (présent uniquement lors de l'exécution sur Windows Subsystem for Linux)
* Nom du compteur : `com.anthropic.claude_code`

## Ressources de mesure du ROI

Pour un guide complet sur la mesure du retour sur investissement pour Claude Code, y compris la configuration de la télémétrie, l'analyse des coûts, les métriques de productivité et les rapports automatisés, consultez le [Guide de mesure du ROI de Claude Code](https://github.com/anthropics/claude-code-monitoring-guide). Ce référentiel fournit des configurations Docker Compose prêtes à l'emploi, des configurations Prometheus et OpenTelemetry, et des modèles pour générer des rapports de productivité intégrés à des outils comme Linear.

## Sécurité et confidentialité

* La télémétrie est opt-in et nécessite une configuration explicite
* Les contenus de fichiers bruts et les extraits de code ne sont pas inclus dans les métriques ou les événements. Les événements d'exécution d'outils incluent les commandes bash et les chemins de fichiers dans le champ `tool_parameters`, qui peuvent contenir des valeurs sensibles. Si vos commandes peuvent inclure des secrets, configurez votre backend de télémétrie pour filtrer ou masquer `tool_parameters`
* Lorsqu'authentifié via OAuth, `user.email` est inclus dans les attributs de télémétrie. Si cela pose un problème pour votre organisation, travaillez avec votre backend de télémétrie pour filtrer ou masquer ce champ
* Le contenu des invites utilisateur n'est pas collecté par défaut. Seule la longueur de l'invite est enregistrée. Pour inclure le contenu de l'invite, définissez `OTEL_LOG_USER_PROMPTS=1`
* Les noms de serveur MCP/outil et les noms de compétences ne sont pas enregistrés par défaut car ils peuvent révéler des configurations spécifiques à l'utilisateur. Pour les inclure, définissez `OTEL_LOG_TOOL_DETAILS=1`

## Surveiller Claude Code sur Amazon Bedrock

Pour des conseils détaillés sur la surveillance de l'utilisation de Claude Code pour Amazon Bedrock, consultez [Implémentation de la surveillance de Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md).
