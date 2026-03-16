> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Surveillance

> Découvrez comment activer et configurer OpenTelemetry pour Claude Code.

Claude Code prend en charge les métriques et événements OpenTelemetry (OTel) pour la surveillance et l'observabilité.

Toutes les métriques sont des données de séries chronologiques exportées via le protocole de métriques standard d'OpenTelemetry, et les événements sont exportés via le protocole de journaux/événements d'OpenTelemetry. Il est de la responsabilité de l'utilisateur de s'assurer que ses backends de métriques et de journaux sont correctement configurés et que la granularité d'agrégation répond à ses exigences de surveillance.

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
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.company.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer company-token"
  }
}
```

<Note>
  Les paramètres gérés peuvent être distribués via MDM (Mobile Device Management) ou d'autres solutions de gestion d'appareils. Les variables d'environnement définies dans le fichier de paramètres gérés ont une haute priorité et ne peuvent pas être remplacées par les utilisateurs.
</Note>

## Détails de la configuration

### Variables de configuration courantes

| Variable d'environnement                        | Description                                                                              | Exemples de valeurs                         |
| ----------------------------------------------- | ---------------------------------------------------------------------------------------- | ------------------------------------------- |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                  | Active la collecte de télémétrie (obligatoire)                                           | `1`                                         |
| `OTEL_METRICS_EXPORTER`                         | Type(s) d'exportateur de métriques (séparés par des virgules)                            | `console`, `otlp`, `prometheus`             |
| `OTEL_LOGS_EXPORTER`                            | Type(s) d'exportateur de journaux/événements (séparés par des virgules)                  | `console`, `otlp`                           |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                   | Protocole pour l'exportateur OTLP (tous les signaux)                                     | `grpc`, `http/json`, `http/protobuf`        |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                   | Point de terminaison du collecteur OTLP (tous les signaux)                               | `http://localhost:4317`                     |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`           | Protocole pour les métriques (remplace le général)                                       | `grpc`, `http/json`, `http/protobuf`        |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`           | Point de terminaison des métriques OTLP (remplace le général)                            | `http://localhost:4318/v1/metrics`          |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`              | Protocole pour les journaux (remplace le général)                                        | `grpc`, `http/json`, `http/protobuf`        |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`              | Point de terminaison des journaux OTLP (remplace le général)                             | `http://localhost:4318/v1/logs`             |
| `OTEL_EXPORTER_OTLP_HEADERS`                    | En-têtes d'authentification pour OTLP                                                    | `Authorization=Bearer token`                |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`         | Clé client pour l'authentification mTLS                                                  | Chemin vers le fichier de clé client        |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE` | Certificat client pour l'authentification mTLS                                           | Chemin vers le fichier de certificat client |
| `OTEL_METRIC_EXPORT_INTERVAL`                   | Intervalle d'export en millisecondes (par défaut : 60000)                                | `5000`, `60000`                             |
| `OTEL_LOGS_EXPORT_INTERVAL`                     | Intervalle d'export des journaux en millisecondes (par défaut : 5000)                    | `1000`, `10000`                             |
| `OTEL_LOG_USER_PROMPTS`                         | Activer la journalisation du contenu des invites utilisateur (par défaut : désactivé)    | `1` pour activer                            |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`   | Intervalle d'actualisation des en-têtes dynamiques (par défaut : 1740000ms / 29 minutes) | `900000`                                    |

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

  La variable d'environnement `OTEL_RESOURCE_ATTRIBUTES` suit la [spécification W3C Baggage](https://www.w3.org/TR/baggage/), qui a des exigences de formatage strictes :

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
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.company.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.company.com:4317

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

| Attribut            | Description                                                             | Contrôlé par                                            |
| ------------------- | ----------------------------------------------------------------------- | ------------------------------------------------------- |
| `session.id`        | Identifiant de session unique                                           | `OTEL_METRICS_INCLUDE_SESSION_ID` (par défaut : true)   |
| `app.version`       | Version actuelle de Claude Code                                         | `OTEL_METRICS_INCLUDE_VERSION` (par défaut : false)     |
| `organization.id`   | UUID de l'organisation (si authentifié)                                 | Toujours inclus si disponible                           |
| `user.account_uuid` | UUID du compte (si authentifié)                                         | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (par défaut : true) |
| `terminal.type`     | Type de terminal (par exemple, `iTerm.app`, `vscode`, `cursor`, `tmux`) | Toujours inclus si détecté                              |

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
* `model` : Identifiant du modèle (par exemple, "claude-sonnet-4-5-20250929")

#### Compteur de jetons

Incrémenté après chaque demande d'API.

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `type` : (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)
* `model` : Identifiant du modèle (par exemple, "claude-sonnet-4-5-20250929")

#### Compteur de décisions de l'outil d'édition de code

Incrémenté lorsque l'utilisateur accepte ou rejette l'utilisation de l'outil Edit, Write ou NotebookEdit.

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `tool` : Nom de l'outil (`"Edit"`, `"Write"`, `"NotebookEdit"`)
* `decision` : Décision de l'utilisateur (`"accept"`, `"reject"`)
* `language` : Langage de programmation du fichier édité (par exemple, `"TypeScript"`, `"Python"`, `"JavaScript"`, `"Markdown"`). Retourne `"unknown"` pour les extensions de fichier non reconnues.

#### Compteur de temps actif

Suit le temps réel passé à utiliser activement Claude Code (pas le temps d'inactivité). Cette métrique est incrémentée lors des interactions utilisateur telles que la saisie d'invites ou la réception de réponses.

**Attributs** :

* Tous les [attributs standard](#standard-attributes)

### Événements

Claude Code exporte les événements suivants via les journaux/événements OpenTelemetry (lorsque `OTEL_LOGS_EXPORTER` est configuré) :

#### Événement d'invite utilisateur

Enregistré lorsqu'un utilisateur soumet une invite.

**Nom de l'événement** : `claude_code.user_prompt`

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `event.name` : `"user_prompt"`
* `event.timestamp` : Horodatage ISO 8601
* `prompt_length` : Longueur de l'invite
* `prompt` : Contenu de l'invite (masqué par défaut, activez avec `OTEL_LOG_USER_PROMPTS=1`)

#### Événement de résultat d'outil

Enregistré lorsqu'un outil termine son exécution.

**Nom de l'événement** : `claude_code.tool_result`

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `event.name` : `"tool_result"`
* `event.timestamp` : Horodatage ISO 8601
* `tool_name` : Nom de l'outil
* `success` : `"true"` ou `"false"`
* `duration_ms` : Temps d'exécution en millisecondes
* `error` : Message d'erreur (en cas d'échec)
* `decision` : Soit `"accept"` soit `"reject"`
* `source` : Source de la décision - `"config"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, ou `"user_reject"`
* `tool_parameters` : Chaîne JSON contenant les paramètres spécifiques à l'outil (si disponible)
  * Pour l'outil Bash : inclut `bash_command`, `full_command`, `timeout`, `description`, `sandbox`

#### Événement de demande d'API

Enregistré pour chaque demande d'API à Claude.

**Nom de l'événement** : `claude_code.api_request`

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `event.name` : `"api_request"`
* `event.timestamp` : Horodatage ISO 8601
* `model` : Modèle utilisé (par exemple, "claude-sonnet-4-5-20250929")
* `cost_usd` : Coût estimé en USD
* `duration_ms` : Durée de la demande en millisecondes
* `input_tokens` : Nombre de jetons d'entrée
* `output_tokens` : Nombre de jetons de sortie
* `cache_read_tokens` : Nombre de jetons lus à partir du cache
* `cache_creation_tokens` : Nombre de jetons utilisés pour la création du cache

#### Événement d'erreur d'API

Enregistré lorsqu'une demande d'API à Claude échoue.

**Nom de l'événement** : `claude_code.api_error`

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `event.name` : `"api_error"`
* `event.timestamp` : Horodatage ISO 8601
* `model` : Modèle utilisé (par exemple, "claude-sonnet-4-5-20250929")
* `error` : Message d'erreur
* `status_code` : Code de statut HTTP (si applicable)
* `duration_ms` : Durée de la demande en millisecondes
* `attempt` : Numéro de tentative (pour les demandes réessayées)

#### Événement de décision d'outil

Enregistré lorsqu'une décision de permission d'outil est prise (accepter/rejeter).

**Nom de l'événement** : `claude_code.tool_decision`

**Attributs** :

* Tous les [attributs standard](#standard-attributes)
* `event.name` : `"tool_decision"`
* `event.timestamp` : Horodatage ISO 8601
* `tool_name` : Nom de l'outil (par exemple, "Read", "Edit", "Write", "NotebookEdit")
* `decision` : Soit `"accept"` soit `"reject"`
* `source` : Source de la décision - `"config"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"`, ou `"user_reject"`

## Interprétation des données de métriques et d'événements

Les métriques exportées par Claude Code fournissent des informations précieuses sur les modèles d'utilisation et la productivité. Voici quelques visualisations et analyses courantes que vous pouvez créer :

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

Toutes les métriques peuvent être segmentées par `user.account_uuid`, `organization.id`, `session.id`, `model` et `app.version`.

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

## Considérations de sécurité/confidentialité

* La télémétrie est opt-in et nécessite une configuration explicite
* Les informations sensibles comme les clés d'API ou le contenu des fichiers ne sont jamais incluses dans les métriques ou les événements
* Le contenu des invites utilisateur est masqué par défaut - seule la longueur de l'invite est enregistrée. Pour activer la journalisation des invites utilisateur, définissez `OTEL_LOG_USER_PROMPTS=1`

## Surveillance de Claude Code sur Amazon Bedrock

Pour des conseils détaillés sur la surveillance de l'utilisation de Claude Code pour Amazon Bedrock, consultez [Implémentation de la surveillance de Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md).
