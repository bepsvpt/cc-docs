> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Connecter Claude Code aux outils via MCP

> Découvrez comment connecter Claude Code à vos outils avec le Model Context Protocol.

Claude Code peut se connecter à des centaines d'outils externes et de sources de données via le [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), une norme open source pour les intégrations IA-outils. Les serveurs MCP donnent à Claude Code accès à vos outils, bases de données et API.

Connectez un serveur lorsque vous vous trouvez à copier des données dans le chat à partir d'un autre outil, comme un suivi de problèmes ou un tableau de bord de surveillance. Une fois connecté, Claude peut lire et agir sur ce système directement au lieu de travailler à partir de ce que vous collez.

## Ce que vous pouvez faire avec MCP

Avec les serveurs MCP connectés, vous pouvez demander à Claude Code de :

* **Implémenter des fonctionnalités à partir de suivi de problèmes** : « Ajouter la fonctionnalité décrite dans le problème JIRA ENG-4521 et créer une PR sur GitHub. »
* **Analyser les données de surveillance** : « Vérifier Sentry et Statsig pour vérifier l'utilisation de la fonctionnalité décrite dans ENG-4521. »
* **Interroger les bases de données** : « Trouver les e-mails de 10 utilisateurs aléatoires qui ont utilisé la fonctionnalité ENG-4521, en fonction de notre base de données PostgreSQL. »
* **Intégrer les conceptions** : « Mettre à jour notre modèle d'e-mail standard en fonction des nouvelles conceptions Figma qui ont été publiées sur Slack »
* **Automatiser les flux de travail** : « Créer des brouillons Gmail invitant ces 10 utilisateurs à une session de rétroaction sur la nouvelle fonctionnalité. »
* **Réagir aux événements externes** : Un serveur MCP peut également agir comme un [canal](/fr/channels) qui pousse des messages dans votre session, afin que Claude réagisse aux messages Telegram, aux discussions Discord ou aux événements webhook pendant que vous êtes absent.

## Trouver et créer des serveurs MCP

Parcourez les connecteurs vérifiés dans le [Répertoire Anthropic](https://claude.ai/directory). Les connecteurs du répertoire utilisent la même infrastructure MCP que Claude Code, vous pouvez donc ajouter n'importe quel serveur distant répertorié avec `claude mcp add`.

<Warning>
  Vérifiez que vous faites confiance à chaque serveur avant de le connecter. Les serveurs qui récupèrent du contenu externe peuvent vous exposer à un [risque d'injection de prompt](/fr/security#protect-against-prompt-injection).
</Warning>

Pour créer votre propre serveur, consultez le [guide du serveur MCP](https://modelcontextprotocol.io/docs/develop/build-server) pour les principes fondamentaux du protocole et la [documentation de création de connecteurs Claude](https://claude.com/docs/connectors/building) pour l'authentification, les tests et la soumission au répertoire.

Vous pouvez également faire en sorte que Claude crée un serveur pour vous avec le plugin officiel [`mcp-server-dev`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/mcp-server-dev).

<Steps>
  <Step title="Installer le plugin">
    Dans une session Claude Code, exécutez :

    ```
    /plugin install mcp-server-dev@claude-plugins-official
    ```

    Ensuite, exécutez `/reload-plugins` pour l'activer dans la session actuelle.
  </Step>

  <Step title="Exécuter la compétence de création">
    ```
    /mcp-server-dev:build-mcp-server
    ```

    Claude vous pose des questions sur votre cas d'usage et crée un serveur HTTP distant ou un serveur stdio local.
  </Step>
</Steps>

## Installation des serveurs MCP

Les serveurs MCP peuvent être configurés de trois façons différentes selon vos besoins :

### Option 1 : Ajouter un serveur HTTP distant

Les serveurs HTTP sont l'option recommandée pour se connecter aux serveurs MCP distants. C'est le transport le plus largement supporté pour les services basés sur le cloud.

```bash theme={null}
# Syntaxe de base
claude mcp add --transport http <name> <url>

# Exemple réel : Se connecter à Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Exemple avec jeton Bearer
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

Lors de la configuration des serveurs MCP via JSON dans `.mcp.json`, `~/.claude.json`, ou `claude mcp add-json`, le champ `type` accepte `streamable-http` comme alias pour `http`. La spécification MCP utilise le nom `streamable-http` pour ce transport, donc les configurations copiées à partir de la documentation du serveur fonctionnent sans modification.

### Option 2 : Ajouter un serveur SSE distant

<Warning>
  Le transport SSE (Server-Sent Events) est déprécié. Utilisez plutôt les serveurs HTTP, si disponibles.
</Warning>

```bash theme={null}
# Syntaxe de base
claude mcp add --transport sse <name> <url>

# Exemple réel : Se connecter à Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Exemple avec en-tête d'authentification
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

### Option 3 : Ajouter un serveur stdio local

Les serveurs Stdio s'exécutent en tant que processus locaux sur votre machine. Ils sont idéaux pour les outils qui ont besoin d'un accès direct au système ou de scripts personnalisés.

Claude Code définit `CLAUDE_PROJECT_DIR` dans l'environnement du serveur généré à la racine du projet, afin que votre serveur puisse résoudre les chemins relatifs au projet sans dépendre du répertoire de travail. C'est le même répertoire que les hooks reçoivent dans leur variable `CLAUDE_PROJECT_DIR`. Lisez-le depuis l'intérieur de votre processus serveur, par exemple `process.env.CLAUDE_PROJECT_DIR` en Node ou `os.environ["CLAUDE_PROJECT_DIR"]` en Python. Votre serveur peut également appeler la demande MCP `roots/list`, qui retourne le répertoire à partir duquel Claude Code a été lancé.

Cette variable est définie dans l'environnement du serveur, pas dans l'environnement propre de Claude Code, donc la référencer via l'expansion `${VAR}` dans un fichier `.mcp.json` de portée projet ou utilisateur `command` ou `args` nécessite une valeur par défaut telle que `${CLAUDE_PROJECT_DIR:-.}`. Les configurations MCP fournies par les plugins remplacent `${CLAUDE_PROJECT_DIR}` directement et n'ont pas besoin de la valeur par défaut.

```bash theme={null}
# Syntaxe de base
claude mcp add [options] <name> -- <command> [args...]

# Exemple réel : Ajouter un serveur Airtable
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server
```

<Note>
  **Important : Ordre des options**

  Toutes les options (`--transport`, `--env`, `--scope`, `--header`) doivent venir **avant** le nom du serveur. Le `--` (double tiret) sépare ensuite le nom du serveur de la commande et des arguments qui sont passés au serveur MCP.

  Par exemple :

  * `claude mcp add --transport stdio myserver -- npx server` → exécute `npx server`
  * `claude mcp add --transport stdio --env KEY=value myserver -- python server.py --port 8080` → exécute `python server.py --port 8080` avec `KEY=value` dans l'environnement

  Cela évite les conflits entre les drapeaux de Claude et les drapeaux du serveur.
</Note>

### Gestion de vos serveurs

Une fois configurés, vous pouvez gérer vos serveurs MCP avec ces commandes :

```bash theme={null}
# Lister tous les serveurs configurés
claude mcp list

# Obtenir les détails d'un serveur spécifique
claude mcp get github

# Supprimer un serveur
claude mcp remove github

# (dans Claude Code) Vérifier l'état du serveur
/mcp
```

Le panneau `/mcp` affiche le nombre d'outils à côté de chaque serveur connecté et signale les serveurs qui annoncent la capacité des outils mais n'exposent aucun outil.

Si votre demande a besoin d'outils d'un serveur qui se connecte toujours en arrière-plan, Claude attend que ce serveur se connecte avant de continuer. Avec la [recherche d'outils](#scale-with-mcp-tool-search) activée, qui est l'option par défaut, l'attente se produit à l'intérieur de l'appel `ToolSearch`. Dans les configurations sans recherche d'outils, telles que Vertex AI, une `ANTHROPIC_BASE_URL` personnalisée, ou `ENABLE_TOOL_SEARCH=false`, Claude utilise plutôt l'outil `WaitForMcpServers`.

Le nom du serveur `workspace` est réservé à un usage interne. Si votre configuration définit un serveur avec ce nom, Claude Code le saute au chargement et affiche un avertissement vous demandant de le renommer.

### Mises à jour dynamiques des outils

Claude Code supporte les notifications MCP `list_changed`, permettant aux serveurs MCP de mettre à jour dynamiquement leurs outils, prompts et ressources disponibles sans vous obliger à vous déconnecter et reconnecter. Lorsqu'un serveur MCP envoie une notification `list_changed`, Claude Code actualise automatiquement les capacités disponibles de ce serveur.

### Reconnexion automatique

Si un serveur HTTP ou SSE se déconnecte en cours de session, Claude Code se reconnecte automatiquement avec un backoff exponentiel : jusqu'à cinq tentatives, en commençant par un délai d'une seconde et en doublant à chaque fois. Le serveur apparaît comme en attente dans `/mcp` pendant que la reconnexion est en cours. Après cinq tentatives échouées, le serveur est marqué comme échoué et vous pouvez réessayer manuellement à partir de `/mcp`. Les serveurs Stdio sont des processus locaux et ne sont pas reconnectés automatiquement.

Le même backoff s'applique lorsqu'un serveur HTTP ou SSE échoue sa connexion initiale au démarrage. À partir de la v2.1.121, Claude Code réessaie la connexion initiale jusqu'à trois fois sur les erreurs transitoires telles qu'une réponse 5xx, une connexion refusée ou un délai d'expiration, puis marque le serveur comme échoué s'il ne peut toujours pas se connecter. Les erreurs d'authentification et les erreurs de non-trouvé ne sont pas réessayées car elles nécessitent une modification de la configuration pour être résolues.

### Pousser des messages avec des canaux

Un serveur MCP peut également pousser des messages directement dans votre session afin que Claude puisse réagir aux événements externes comme les résultats CI, les alertes de surveillance ou les messages de chat. Pour activer cela, votre serveur déclare la capacité `claude/channel` et vous l'activez avec le drapeau `--channels` au démarrage. Consultez [Canaux](/fr/channels) pour utiliser un canal officiellement supporté, ou [Référence des canaux](/fr/channels-reference) pour créer le vôtre.

<Tip>
  Conseils :

  * Utilisez le drapeau `--scope` pour spécifier où la configuration est stockée :
    * `local` (par défaut) : Disponible uniquement pour vous dans le projet actuel (appelé `project` dans les versions antérieures)
    * `project` : Partagé avec tous les membres du projet via le fichier `.mcp.json`
    * `user` : Disponible pour vous dans tous les projets (appelé `global` dans les versions antérieures)
  * Définissez les variables d'environnement avec les drapeaux `--env` (par exemple, `--env KEY=value`)
  * Configurez le délai d'expiration du démarrage du serveur MCP en utilisant la variable d'environnement MCP\_TIMEOUT (par exemple, `MCP_TIMEOUT=10000 claude` définit un délai d'expiration de 10 secondes)
  * Claude Code affichera un avertissement lorsque la sortie de l'outil MCP dépasse 10 000 jetons. Pour augmenter cette limite, définissez la variable d'environnement `MAX_MCP_OUTPUT_TOKENS` (par exemple, `MAX_MCP_OUTPUT_TOKENS=50000`)
  * Utilisez `/mcp` pour vous authentifier auprès des serveurs distants qui nécessitent une authentification OAuth 2.0
</Tip>

### Serveurs MCP fournis par les plugins

Les [plugins](/fr/plugins) peuvent regrouper des serveurs MCP, fournissant automatiquement des outils et des intégrations lorsque le plugin est activé. Les serveurs MCP des plugins fonctionnent de manière identique aux serveurs configurés par l'utilisateur.

**Comment fonctionnent les serveurs MCP des plugins** :

* Les plugins définissent les serveurs MCP dans `.mcp.json` à la racine du plugin ou en ligne dans `plugin.json`
* Lorsqu'un plugin est activé, ses serveurs MCP démarrent automatiquement
* Les outils MCP des plugins apparaissent aux côtés des outils MCP configurés manuellement
* Les serveurs des plugins sont gérés via l'installation du plugin (pas via les commandes `/mcp`)

**Exemple de configuration MCP du plugin** :

Dans `.mcp.json` à la racine du plugin :

```json theme={null}
{
  "mcpServers": {
    "database-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_URL": "${DB_URL}"
      }
    }
  }
}
```

Ou en ligne dans `plugin.json` :

```json theme={null}
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

**Fonctionnalités MCP du plugin** :

* **Cycle de vie automatique** : Au démarrage de la session, les serveurs des plugins activés se connectent automatiquement. Si vous activez ou désactivez un plugin pendant une session, exécutez `/reload-plugins` pour connecter ou déconnecter ses serveurs MCP
* **Variables d'environnement** : utilisez `${CLAUDE_PLUGIN_ROOT}` pour les fichiers du plugin groupés, `${CLAUDE_PLUGIN_DATA}` pour l'[état persistant](/fr/plugins-reference#persistent-data-directory) qui survit aux mises à jour du plugin, et `${CLAUDE_PROJECT_DIR}` pour la racine du projet stable
* **Accès aux variables d'environnement utilisateur** : Accès aux mêmes variables d'environnement que les serveurs configurés manuellement
* **Types de transport multiples** : Support des transports stdio, SSE et HTTP (le support des transports peut varier selon le serveur)

**Affichage des serveurs MCP du plugin** :

```bash theme={null}
# Dans Claude Code, voir tous les serveurs MCP y compris ceux du plugin
/mcp
```

Les serveurs des plugins apparaissent dans la liste avec des indicateurs montrant qu'ils proviennent des plugins.

**Avantages des serveurs MCP du plugin** :

* **Distribution groupée** : Outils et serveurs emballés ensemble
* **Configuration automatique** : Aucune configuration MCP manuelle nécessaire
* **Cohérence d'équipe** : Tout le monde obtient les mêmes outils lorsque le plugin est installé

Consultez la [référence des composants du plugin](/fr/plugins-reference#mcp-servers) pour plus de détails sur le regroupement des serveurs MCP avec les plugins.

## Portées d'installation MCP

Les serveurs MCP peuvent être configurés à trois portées différentes. La portée que vous choisissez contrôle les projets dans lesquels le serveur se charge et si la configuration est partagée avec votre équipe. Les administrateurs peuvent également déployer des serveurs au niveau de l'entreprise via la [configuration gérée](#managed-mcp-configuration).

| Portée                     | Se charge dans           | Partagé avec l'équipe           | Stocké dans                       |
| -------------------------- | ------------------------ | ------------------------------- | --------------------------------- |
| [Local](#local-scope)      | Projet actuel uniquement | Non                             | `~/.claude.json`                  |
| [Projet](#project-scope)   | Projet actuel uniquement | Oui, via le contrôle de version | `.mcp.json` à la racine du projet |
| [Utilisateur](#user-scope) | Tous vos projets         | Non                             | `~/.claude.json`                  |

### Portée locale

La portée locale est la portée par défaut. Un serveur à portée locale se charge uniquement dans le projet où vous l'avez ajouté et reste privé pour vous. Claude Code le stocke dans `~/.claude.json` sous le chemin de ce projet, donc le même serveur n'apparaîtra pas dans vos autres projets. Utilisez la portée locale pour les serveurs de développement personnels, les configurations expérimentales ou les serveurs avec des identifiants que vous ne voulez pas dans le contrôle de version.

<Note>
  Le terme « portée locale » pour les serveurs MCP diffère des paramètres locaux généraux. Les serveurs MCP à portée locale sont stockés dans `~/.claude.json` (votre répertoire personnel), tandis que les paramètres locaux généraux utilisent `.claude/settings.local.json` (dans le répertoire du projet). Consultez [Paramètres](/fr/settings#settings-files) pour plus de détails sur les emplacements des fichiers de paramètres.
</Note>

```bash theme={null}
# Ajouter un serveur à portée locale (par défaut)
claude mcp add --transport http stripe https://mcp.stripe.com

# Spécifier explicitement la portée locale
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

La commande écrit le serveur dans l'entrée de votre projet actuel dans `~/.claude.json`. L'exemple ci-dessous montre le résultat lorsque vous l'exécutez à partir de `/path/to/your/project` :

```json theme={null}
{
  "projects": {
    "/path/to/your/project": {
      "mcpServers": {
        "stripe": {
          "type": "http",
          "url": "https://mcp.stripe.com"
        }
      }
    }
  }
}
```

### Portée du projet

Les serveurs à portée de projet permettent la collaboration d'équipe en stockant les configurations dans un fichier `.mcp.json` à la racine de votre projet. Ce fichier est conçu pour être archivé dans le contrôle de version, garantissant que tous les membres de l'équipe ont accès aux mêmes outils et services MCP. Lorsque vous ajoutez un serveur à portée de projet, Claude Code crée ou met à jour automatiquement ce fichier avec la structure de configuration appropriée.

```bash theme={null}
# Ajouter un serveur à portée de projet
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

Le fichier `.mcp.json` résultant suit un format standardisé :

```json theme={null}
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

Pour des raisons de sécurité, Claude Code demande une approbation avant d'utiliser les serveurs à portée de projet à partir des fichiers `.mcp.json`. Si vous devez réinitialiser ces choix d'approbation, utilisez la commande `claude mcp reset-project-choices`.

### Portée utilisateur

Les serveurs à portée utilisateur sont stockés dans `~/.claude.json` et offrent une accessibilité inter-projets, les rendant disponibles dans tous les projets de votre machine tout en restant privés pour votre compte utilisateur. Cette portée fonctionne bien pour les serveurs utilitaires personnels, les outils de développement ou les services que vous utilisez fréquemment dans différents projets.

```bash theme={null}
# Ajouter un serveur utilisateur
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### Hiérarchie de portée et précédence

Lorsque le même serveur est défini à plus d'un endroit, Claude Code s'y connecte une fois, en utilisant la définition de la source avec la plus haute priorité :

1. Portée locale
2. Portée du projet
3. Portée utilisateur
4. [Serveurs fournis par les plugins](/fr/plugins)
5. [Connecteurs claude.ai](#use-mcp-servers-from-claude-ai)

Les trois portées correspondent aux doublons par nom. Les plugins et les connecteurs correspondent par point de terminaison, donc celui qui pointe vers la même URL ou commande qu'un serveur ci-dessus est traité comme un doublon.

### Expansion des variables d'environnement dans `.mcp.json`

Claude Code supporte l'expansion des variables d'environnement dans les fichiers `.mcp.json`, permettant aux équipes de partager des configurations tout en maintenant la flexibilité pour les chemins spécifiques à la machine et les valeurs sensibles comme les clés API.

**Syntaxe supportée :**

* `${VAR}` - Se développe à la valeur de la variable d'environnement `VAR`
* `${VAR:-default}` - Se développe à `VAR` si défini, sinon utilise `default`

**Emplacements d'expansion :**
Les variables d'environnement peuvent être développées dans :

* `command` - Le chemin de l'exécutable du serveur
* `args` - Arguments de la ligne de commande
* `env` - Variables d'environnement passées au serveur
* `url` - Pour les types de serveur HTTP
* `headers` - Pour l'authentification du serveur HTTP

**Exemple avec expansion de variable :**

```json theme={null}
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

Si une variable d'environnement requise n'est pas définie et n'a pas de valeur par défaut, Claude Code ne pourra pas analyser la configuration.

## Exemples pratiques

{/* ### Exemple : Automatiser les tests de navigateur avec Playwright

```bash
claude mcp add --transport stdio playwright -- npx -y @playwright/mcp@latest
```

Ensuite, écrivez et exécutez des tests de navigateur :

```text
Test si le flux de connexion fonctionne avec test@example.com
```
```text
Prendre une capture d'écran de la page de paiement sur mobile
```
```text
Vérifier que la fonction de recherche retourne des résultats
``` */}

### Exemple : Surveiller les erreurs avec Sentry

```bash theme={null}
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

Authentifiez-vous avec votre compte Sentry :

```text theme={null}
/mcp
```

Ensuite, déboguez les problèmes de production :

```text theme={null}
Quelles sont les erreurs les plus courantes au cours des 24 dernières heures ?
```

```text theme={null}
Montrez-moi la trace de pile pour l'erreur ID abc123
```

```text theme={null}
Quel déploiement a introduit ces nouvelles erreurs ?
```

### Exemple : Se connecter à GitHub pour les révisions de code

Le serveur MCP distant de GitHub s'authentifie avec un jeton d'accès personnel GitHub transmis en tant qu'en-tête. Pour en obtenir un, ouvrez vos [paramètres de jeton GitHub](https://github.com/settings/personal-access-tokens), générez un nouveau jeton à granularité fine avec accès aux référentiels avec lesquels vous souhaitez que Claude travaille, puis ajoutez le serveur :

```bash theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

Ensuite, travaillez avec GitHub :

```text theme={null}
Examinez la PR #456 et suggérez des améliorations
```

```text theme={null}
Créer un nouveau problème pour le bogue que nous venons de trouver
```

```text theme={null}
Montrez-moi toutes les PR ouvertes qui me sont assignées
```

### Exemple : Interroger votre base de données PostgreSQL

```bash theme={null}
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"
```

Ensuite, interrogez votre base de données naturellement :

```text theme={null}
Quel est notre revenu total ce mois-ci ?
```

```text theme={null}
Montrez-moi le schéma de la table des commandes
```

```text theme={null}
Trouver les clients qui n'ont pas effectué d'achat depuis 90 jours
```

## S'authentifier auprès des serveurs MCP distants

De nombreux serveurs MCP basés sur le cloud nécessitent une authentification. Claude Code supporte OAuth 2.0 pour les connexions sécurisées.

Claude Code marque un serveur distant comme nécessitant une authentification lorsque le serveur répond avec `401 Unauthorized` ou `403 Forbidden`. L'un ou l'autre code de statut signale le serveur dans `/mcp` afin que vous puissiez compléter le flux OAuth. Un serveur personnalisé qui retourne un en-tête `WWW-Authenticate` pointant vers son serveur d'autorisation obtient la même découverte automatique que tout autre serveur distant.

<Steps>
  <Step title="Ajouter le serveur qui nécessite une authentification">
    Par exemple :

    ```bash theme={null}
    claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
    ```
  </Step>

  <Step title="Utiliser la commande /mcp dans Claude Code">
    Dans Claude Code, utilisez la commande :

    ```text theme={null}
    /mcp
    ```

    Ensuite, suivez les étapes dans votre navigateur pour vous connecter.
  </Step>
</Steps>

<Tip>
  Conseils :

  * Les jetons d'authentification sont stockés de manière sécurisée et actualisés automatiquement
  * Utilisez « Clear authentication » dans le menu `/mcp` pour révoquer l'accès
  * Si votre navigateur ne s'ouvre pas automatiquement, copiez l'URL fournie et ouvrez-la manuellement
  * Si la redirection du navigateur échoue avec une erreur de connexion après l'authentification, collez l'URL de rappel complète de la barre d'adresse de votre navigateur dans l'invite d'URL qui apparaît dans Claude Code
  * L'authentification OAuth fonctionne avec les serveurs HTTP
</Tip>

### Utiliser un port de rappel OAuth fixe

Certains serveurs MCP nécessitent un URI de redirection spécifique enregistré à l'avance. Par défaut, Claude Code choisit un port disponible aléatoire pour le rappel OAuth. Utilisez `--callback-port` pour fixer le port afin qu'il corresponde à un URI de redirection pré-enregistré de la forme `http://localhost:PORT/callback`.

Vous pouvez utiliser `--callback-port` seul (avec l'enregistrement dynamique du client) ou ensemble avec `--client-id` (avec les identifiants pré-configurés).

```bash theme={null}
# Port de rappel fixe avec enregistrement dynamique du client
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

### Utiliser les identifiants OAuth pré-configurés

Certains serveurs MCP ne supportent pas la configuration OAuth automatique via l'enregistrement dynamique du client. Si vous voyez une erreur comme « Incompatible auth server: does not support dynamic client registration », le serveur nécessite des identifiants pré-configurés. Claude Code supporte également les serveurs qui utilisent un document de métadonnées d'ID client (CIMD) au lieu de l'enregistrement dynamique du client, et les découvre automatiquement. Si la découverte automatique échoue, enregistrez d'abord une application OAuth via le portail des développeurs du serveur, puis fournissez les identifiants lors de l'ajout du serveur.

<Steps>
  <Step title="Enregistrer une application OAuth auprès du serveur">
    Créez une application via le portail des développeurs du serveur et notez votre ID client et votre secret client.

    De nombreux serveurs nécessitent également un URI de redirection. Si c'est le cas, choisissez un port et enregistrez un URI de redirection au format `http://localhost:PORT/callback`. Utilisez ce même port avec `--callback-port` à l'étape suivante.
  </Step>

  <Step title="Ajouter le serveur avec vos identifiants">
    Choisissez l'une des méthodes suivantes. Le port utilisé pour `--callback-port` peut être n'importe quel port disponible. Il doit simplement correspondre à l'URI de redirection que vous avez enregistré à l'étape précédente.

    <Tabs>
      <Tab title="claude mcp add">
        Utilisez `--client-id` pour passer l'ID client de votre application. Le drapeau `--client-secret` demande le secret avec une entrée masquée :

        ```bash theme={null}
        claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>

      <Tab title="claude mcp add-json">
        Incluez l'objet `oauth` dans la configuration JSON et passez `--client-secret` comme drapeau séparé :

        ```bash theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' \
          --client-secret
        ```
      </Tab>

      <Tab title="claude mcp add-json (port de rappel uniquement)">
        Utilisez `--callback-port` sans ID client pour fixer le port tout en utilisant l'enregistrement dynamique du client :

        ```bash theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"callbackPort":8080}}'
        ```
      </Tab>

      <Tab title="CI / variable d'environnement">
        Définissez le secret via une variable d'environnement pour ignorer l'invite interactive :

        ```bash theme={null}
        MCP_CLIENT_SECRET=your-secret claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="S'authentifier dans Claude Code">
    Exécutez `/mcp` dans Claude Code et suivez le flux de connexion du navigateur.
  </Step>
</Steps>

<Tip>
  Conseils :

  * Le secret client est stocké de manière sécurisée dans votre trousseau système (macOS) ou un fichier d'identifiants, pas dans votre configuration
  * Si le serveur utilise un client OAuth public sans secret, utilisez uniquement `--client-id` sans `--client-secret`
  * `--callback-port` peut être utilisé avec ou sans `--client-id`
  * Ces drapeaux s'appliquent uniquement aux transports HTTP et SSE. Ils n'ont aucun effet sur les serveurs stdio
  * Utilisez `claude mcp get <name>` pour vérifier que les identifiants OAuth sont configurés pour un serveur
</Tip>

### Remplacer la découverte des métadonnées OAuth

Pointez Claude Code vers une URL de métadonnées spécifique du serveur d'autorisation OAuth pour contourner la chaîne de découverte par défaut. Définissez `authServerMetadataUrl` lorsque les points de terminaison standard du serveur MCP génèrent des erreurs, ou lorsque vous souhaitez acheminer la découverte via un proxy interne. Par défaut, Claude Code vérifie d'abord les métadonnées de ressource protégée RFC 9728 à `/.well-known/oauth-protected-resource`, puis revient aux métadonnées du serveur d'autorisation RFC 8414 à `/.well-known/oauth-authorization-server`.

Définissez `authServerMetadataUrl` dans l'objet `oauth` de la configuration de votre serveur dans `.mcp.json` :

```json theme={null}
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

L'URL doit utiliser `https://`. `authServerMetadataUrl` nécessite Claude Code v2.1.64 ou ultérieur. Les `scopes_supported` de l'URL des métadonnées remplacent les portées que le serveur en amont annonce.

### Restreindre les portées OAuth

Définissez `oauth.scopes` pour épingler les portées que Claude Code demande pendant le flux d'autorisation. C'est la façon supportée de restreindre un serveur MCP à un sous-ensemble approuvé par l'équipe de sécurité lorsque le serveur d'autorisation en amont annonce plus de portées que vous ne souhaitez accorder. La valeur est une seule chaîne séparée par des espaces, correspondant au format du paramètre `scope` dans RFC 6749 §3.3.

```json theme={null}
{
  "mcpServers": {
    "slack": {
      "type": "http",
      "url": "https://mcp.slack.com/mcp",
      "oauth": {
        "scopes": "channels:read chat:write search:read"
      }
    }
  }
}
```

`oauth.scopes` a la priorité sur `authServerMetadataUrl` et les portées que le serveur découvre à `/.well-known`. Laissez-le non défini pour laisser le serveur MCP déterminer l'ensemble de portées demandées.

Si le serveur d'autorisation annonce `offline_access` dans `scopes_supported`, Claude Code l'ajoute aux portées épinglées afin que le jeton d'accès puisse être actualisé sans une nouvelle connexion au navigateur.

Si le serveur retourne ultérieurement un 403 `insufficient_scope` pour un appel d'outil, Claude Code se réauthentifie avec les mêmes portées épinglées. Élargissez `oauth.scopes` lorsqu'un outil dont vous avez besoin nécessite une portée en dehors de l'épingle.

### Utiliser des en-têtes dynamiques pour l'authentification personnalisée

Si votre serveur MCP utilise un schéma d'authentification autre que OAuth (tel que Kerberos, jetons de courte durée ou un SSO interne), utilisez `headersHelper` pour générer des en-têtes de requête au moment de la connexion. Claude Code exécute la commande et fusionne sa sortie dans les en-têtes de connexion.

```json theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "/opt/bin/get-mcp-auth-headers.sh"
    }
  }
}
```

La commande peut également être en ligne :

```json theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "echo '{\"Authorization\": \"Bearer '\"$(get-token)\"'\"}'"
    }
  }
}
```

**Exigences :**

* La commande doit écrire un objet JSON de paires clé-valeur de chaîne sur stdout
* La commande s'exécute dans un shell avec un délai d'expiration de 10 secondes
* Les en-têtes dynamiques remplacent tous les `headers` statiques portant le même nom

L'assistant s'exécute à nouveau à chaque connexion (au démarrage de la session et à la reconnexion). Il n'y a pas de mise en cache, donc votre script est responsable de toute réutilisation de jetons.

Claude Code définit ces variables d'environnement lors de l'exécution de l'assistant :

| Variable                      | Valeur                |
| :---------------------------- | :-------------------- |
| `CLAUDE_CODE_MCP_SERVER_NAME` | le nom du serveur MCP |
| `CLAUDE_CODE_MCP_SERVER_URL`  | l'URL du serveur MCP  |

Utilisez-les pour écrire un script d'assistant unique qui sert plusieurs serveurs MCP.

<Note>
  `headersHelper` exécute des commandes shell arbitraires. Lorsqu'il est défini à portée de projet ou locale, il ne s'exécute qu'après que vous ayez accepté la boîte de dialogue de confiance de l'espace de travail.
</Note>

## Ajouter des serveurs MCP à partir de la configuration JSON

Si vous avez une configuration JSON pour un serveur MCP, vous pouvez l'ajouter directement :

<Steps>
  <Step title="Ajouter un serveur MCP à partir de JSON">
    ```bash theme={null}
    # Syntaxe de base
    claude mcp add-json <name> '<json>'

    # Exemple : Ajouter un serveur HTTP avec configuration JSON
    claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'

    # Exemple : Ajouter un serveur stdio avec configuration JSON
    claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'

    # Exemple : Ajouter un serveur HTTP avec identifiants OAuth pré-configurés
    claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' --client-secret
    ```
  </Step>

  <Step title="Vérifier que le serveur a été ajouté">
    ```bash theme={null}
    claude mcp get weather-api
    ```
  </Step>
</Steps>

<Tip>
  Conseils :

  * Assurez-vous que le JSON est correctement échappé dans votre shell
  * Le JSON doit se conformer au schéma de configuration du serveur MCP
  * Vous pouvez utiliser `--scope user` pour ajouter le serveur à votre configuration utilisateur au lieu de celle spécifique au projet
</Tip>

## Importer les serveurs MCP à partir de Claude Desktop

Si vous avez déjà configuré des serveurs MCP dans Claude Desktop, vous pouvez les importer :

<Steps>
  <Step title="Importer les serveurs à partir de Claude Desktop">
    ```bash theme={null}
    # Syntaxe de base 
    claude mcp add-from-claude-desktop 
    ```
  </Step>

  <Step title="Sélectionner les serveurs à importer">
    Après avoir exécuté la commande, vous verrez une boîte de dialogue interactive qui vous permet de sélectionner les serveurs que vous souhaitez importer.
  </Step>

  <Step title="Vérifier que les serveurs ont été importés">
    ```bash theme={null}
    claude mcp list 
    ```
  </Step>
</Steps>

<Tip>
  Conseils :

  * Cette fonctionnalité ne fonctionne que sur macOS et Windows Subsystem for Linux (WSL)
  * Elle lit le fichier de configuration de Claude Desktop à partir de son emplacement standard sur ces plates-formes
  * Utilisez le drapeau `--scope user` pour ajouter les serveurs à votre configuration utilisateur
  * Les serveurs importés auront les mêmes noms que dans Claude Desktop
  * Si des serveurs portant les mêmes noms existent déjà, ils recevront un suffixe numérique (par exemple, `server_1`)
</Tip>

## Utiliser les serveurs MCP à partir de Claude.ai

Si vous vous êtes connecté à Claude Code avec un compte [Claude.ai](https://claude.ai), les serveurs MCP que vous avez ajoutés dans Claude.ai sont automatiquement disponibles dans Claude Code :

<Steps>
  <Step title="Configurer les serveurs MCP dans Claude.ai">
    Ajoutez les serveurs à [claude.ai/customize/connectors](https://claude.ai/customize/connectors). Sur les plans Team et Enterprise, seuls les administrateurs peuvent ajouter des serveurs.
  </Step>

  <Step title="Authentifier le serveur MCP">
    Complétez les étapes d'authentification requises dans Claude.ai.
  </Step>

  <Step title="Afficher et gérer les serveurs dans Claude Code">
    Dans Claude Code, utilisez la commande :

    ```text theme={null}
    /mcp
    ```

    Les serveurs Claude.ai apparaissent dans la liste avec des indicateurs montrant qu'ils proviennent de Claude.ai.
  </Step>
</Steps>

Les connecteurs Claude.ai sont récupérés uniquement lorsque votre [méthode d'authentification](/fr/authentication#authentication-precedence) active est votre abonnement Claude.ai. Ils ne sont pas chargés lorsque `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `apiKeyHelper`, ou un fournisseur tiers tel que Bedrock ou Vertex est actif, même si vous avez précédemment exécuté `/login`. Si `/mcp` ne répertorie pas un connecteur que vous avez ajouté, exécutez `/status` pour confirmer quelle méthode d'authentification est active, désactivez cette variable d'environnement ou supprimez le paramètre `apiKeyHelper`, puis exécutez `/login` pour sélectionner votre compte Claude.ai.

Un serveur que vous avez ajouté dans Claude Code prend [précédence](#scope-hierarchy-and-precedence) sur un connecteur claude.ai qui pointe vers la même URL. Quand cela se produit, `/mcp` répertorie le connecteur comme masqué et montre comment supprimer le doublon si vous préférez utiliser le connecteur.

Pour désactiver les serveurs MCP de Claude.ai dans Claude Code, définissez la variable d'environnement `ENABLE_CLAUDEAI_MCP_SERVERS` sur `false` :

```bash theme={null}
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

## Utiliser Claude Code comme serveur MCP

Vous pouvez utiliser Claude Code lui-même comme serveur MCP auquel d'autres applications peuvent se connecter :

```bash theme={null}
# Démarrer Claude en tant que serveur MCP stdio
claude mcp serve
```

Vous pouvez l'utiliser dans Claude Desktop en ajoutant cette configuration à claude\_desktop\_config.json :

```json theme={null}
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

<Warning>
  **Configuration du chemin de l'exécutable** : Le champ `command` doit référencer l'exécutable Claude Code. Si la commande `claude` n'est pas dans le PATH de votre système, vous devrez spécifier le chemin complet de l'exécutable.

  Pour trouver le chemin complet :

  ```bash theme={null}
  which claude
  ```

  Ensuite, utilisez le chemin complet dans votre configuration :

  ```json theme={null}
  {
    "mcpServers": {
      "claude-code": {
        "type": "stdio",
        "command": "/full/path/to/claude",
        "args": ["mcp", "serve"],
        "env": {}
      }
    }
  }
  ```

  Sans le chemin d'exécutable correct, vous rencontrerez des erreurs comme `spawn claude ENOENT`.
</Warning>

<Tip>
  Conseils :

  * Le serveur fournit l'accès aux outils de Claude comme View, Edit, LS, etc.
  * Dans Claude Desktop, essayez de demander à Claude de lire les fichiers dans un répertoire, de faire des modifications, et plus encore.
  * Notez que ce serveur MCP expose uniquement les outils de Claude Code à votre client MCP, donc votre propre client est responsable de l'implémentation de la confirmation de l'utilisateur pour les appels d'outils individuels.
</Tip>

## Limites de sortie MCP et avertissements

Lorsque les outils MCP produisent de grandes sorties, Claude Code aide à gérer l'utilisation des jetons pour éviter de surcharger votre contexte de conversation :

* **Seuil d'avertissement de sortie** : Claude Code affiche un avertissement lorsque la sortie de tout outil MCP dépasse 10 000 jetons
* **Limite configurable** : vous pouvez ajuster le nombre maximum de jetons de sortie MCP autorisés en utilisant la variable d'environnement `MAX_MCP_OUTPUT_TOKENS`
* **Limite par défaut** : la limite maximale par défaut est de 25 000 jetons
* **Portée** : la variable d'environnement s'applique aux outils qui ne déclarent pas leur propre limite. Les outils qui définissent [`anthropic/maxResultSizeChars`](#raise-the-limit-for-a-specific-tool) utilisent cette valeur à la place pour le contenu texte, indépendamment de ce que `MAX_MCP_OUTPUT_TOKENS` est défini. Les outils qui retournent des données d'image sont toujours soumis à `MAX_MCP_OUTPUT_TOKENS`

Pour augmenter la limite pour les outils qui produisent de grandes sorties :

```bash theme={null}
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

Ceci est particulièrement utile lorsque vous travaillez avec des serveurs MCP qui :

* Interrogent de grands ensembles de données ou des bases de données
* Génèrent des rapports ou des documentations détaillés
* Traitent des fichiers journaux ou des informations de débogage étendus

### Augmenter la limite pour un outil spécifique

Si vous créez un serveur MCP, vous pouvez permettre aux outils individuels de retourner des résultats plus grands que le seuil par défaut de persistance sur disque en définissant `_meta["anthropic/maxResultSizeChars"]` dans l'entrée de l'outil dans la réponse `tools/list`. Claude Code augmente le seuil de cet outil à la valeur annotée, jusqu'à un plafond dur de 500 000 caractères.

Ceci est utile pour les outils qui retournent des sorties intrinsèquement grandes mais nécessaires, telles que les schémas de base de données ou les arbres de fichiers complets. Sans l'annotation, les résultats qui dépassent le seuil par défaut sont persistés sur disque et remplacés par une référence de fichier dans la conversation.

```json theme={null}
{
  "name": "get_schema",
  "description": "Returns the full database schema",
  "_meta": {
    "anthropic/maxResultSizeChars": 200000
  }
}
```

L'annotation s'applique indépendamment de `MAX_MCP_OUTPUT_TOKENS` pour le contenu texte, donc les utilisateurs n'ont pas besoin d'augmenter la variable d'environnement pour les outils qui la déclarent. Les outils qui retournent des données d'image sont toujours soumis à la limite de jetons.

<Warning>
  Si vous rencontrez fréquemment des avertissements de sortie avec des serveurs MCP spécifiques que vous ne contrôlez pas, envisagez d'augmenter la limite `MAX_MCP_OUTPUT_TOKENS`. Vous pouvez également demander à l'auteur du serveur d'ajouter l'annotation `anthropic/maxResultSizeChars` ou de paginer ses réponses. L'annotation n'a aucun effet sur les outils qui retournent du contenu d'image ; pour ceux-ci, augmenter `MAX_MCP_OUTPUT_TOKENS` est la seule option.
</Warning>

## Répondre aux demandes d'élicitation MCP

Les serveurs MCP peuvent demander une entrée structurée de votre part au cours d'une tâche en utilisant l'élicitation. Lorsqu'un serveur a besoin d'informations qu'il ne peut pas obtenir par lui-même, Claude Code affiche une boîte de dialogue interactive et transmet votre réponse au serveur. Aucune configuration n'est requise de votre côté : les boîtes de dialogue d'élicitation apparaissent automatiquement lorsqu'un serveur les demande.

Les serveurs peuvent demander une entrée de deux façons :

* **Mode formulaire** : Claude Code affiche une boîte de dialogue avec des champs de formulaire définis par le serveur (par exemple, une invite de nom d'utilisateur et de mot de passe). Remplissez les champs et soumettez.
* **Mode URL** : Claude Code ouvre une URL de navigateur pour l'authentification ou l'approbation. Complétez le flux dans le navigateur, puis confirmez dans l'interface de ligne de commande.

Pour répondre automatiquement aux demandes d'élicitation sans afficher de boîte de dialogue, utilisez le [hook `Elicitation`](/fr/hooks#Elicitation).

Si vous créez un serveur MCP qui utilise l'élicitation, consultez la [spécification d'élicitation MCP](https://modelcontextprotocol.io/docs/learn/client-concepts#elicitation) pour les détails du protocole et les exemples de schéma.

## Utiliser les ressources MCP

Les serveurs MCP peuvent exposer des ressources que vous pouvez référencer en utilisant des mentions @, similaire à la façon dont vous référencez les fichiers.

### Référencer les ressources MCP

<Steps>
  <Step title="Lister les ressources disponibles">
    Tapez `@` dans votre prompt pour voir les ressources disponibles de tous les serveurs MCP connectés. Les ressources apparaissent aux côtés des fichiers dans le menu d'autocomplétion.
  </Step>

  <Step title="Référencer une ressource spécifique">
    Utilisez le format `@server:protocol://resource/path` pour référencer une ressource :

    ```text theme={null}
    Pouvez-vous analyser @github:issue://123 et suggérer un correctif ?
    ```

    ```text theme={null}
    Veuillez examiner la documentation API à @docs:file://api/authentication
    ```
  </Step>

  <Step title="Références de ressources multiples">
    Vous pouvez référencer plusieurs ressources dans un seul prompt :

    ```text theme={null}
    Comparez @postgres:schema://users avec @docs:file://database/user-model
    ```
  </Step>
</Steps>

<Tip>
  Conseils :

  * Les ressources sont automatiquement récupérées et incluses en tant que pièces jointes lorsqu'elles sont référencées
  * Les chemins des ressources sont recherchables par correspondance floue dans l'autocomplétion de mention @
  * Claude Code fournit automatiquement des outils pour lister et lire les ressources MCP lorsque les serveurs les supportent
  * Les ressources peuvent contenir n'importe quel type de contenu fourni par le serveur MCP (texte, JSON, données structurées, etc.)
</Tip>

## Mettre à l'échelle avec la recherche d'outils MCP

La recherche d'outils maintient l'utilisation du contexte MCP faible en différant les définitions d'outils jusqu'à ce que Claude en ait besoin. Seuls les noms d'outils se chargent au démarrage de la session, donc l'ajout de plus de serveurs MCP a un impact minimal sur votre fenêtre de contexte.

### Comment cela fonctionne

La recherche d'outils est activée par défaut. Les outils MCP sont différés plutôt que chargés dans le contexte à l'avance, et Claude utilise un outil de recherche pour découvrir les outils pertinents lorsqu'une tâche en a besoin. Seuls les outils que Claude utilise réellement entrent dans le contexte. De votre point de vue, les outils MCP fonctionnent exactement comme avant.

Si vous préférez le chargement basé sur un seuil, définissez `ENABLE_TOOL_SEARCH=auto` pour charger les schémas à l'avance lorsqu'ils s'ajustent dans 10 % de la fenêtre de contexte et différer uniquement le débordement. Consultez [Configurer la recherche d'outils](#configure-tool-search) pour toutes les options.

### Pour les auteurs de serveurs MCP

Si vous créez un serveur MCP, le champ des instructions du serveur devient plus utile avec la recherche d'outils activée. Les instructions du serveur aident Claude à comprendre quand rechercher vos outils, similaire à la façon dont les [skills](/fr/skills) fonctionnent.

Ajoutez des instructions de serveur claires et descriptives qui expliquent :

* Quelle catégorie de tâches vos outils gèrent
* Quand Claude doit rechercher vos outils
* Les capacités clés de votre serveur

Claude Code tronque les descriptions d'outils et les instructions du serveur à 2 Ko chacune. Gardez-les concis pour éviter la troncature, et mettez les détails critiques près du début.

### Configurer la recherche d'outils

La recherche d'outils est activée par défaut : les outils MCP sont différés et découverts à la demande. Claude Code la désactive par défaut sur Vertex AI. Elle est également désactivée lorsque `ANTHROPIC_BASE_URL` pointe vers un hôte non-propriétaire, car la plupart des proxies ne transfèrent pas les blocs `tool_reference`. Définissez `ENABLE_TOOL_SEARCH` explicitement pour remplacer l'un ou l'autre des mécanismes de secours.

La recherche d'outils nécessite un modèle qui supporte les blocs `tool_reference` : Sonnet 4 et ultérieur, ou Opus 4 et ultérieur. Les modèles Haiku ne le supportent pas. Sur Vertex AI, la recherche d'outils est supportée pour Claude Sonnet 4.5 et ultérieur et Claude Opus 4.5 et ultérieur.

Contrôlez le comportement de la recherche d'outils avec la variable d'environnement `ENABLE_TOOL_SEARCH` :

| Valeur       | Comportement                                                                                                                                                                                                                                                    |
| :----------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| (non défini) | Tous les outils MCP différés et chargés à la demande. Revient au chargement à l'avance sur Vertex AI ou lorsque `ANTHROPIC_BASE_URL` est un hôte non-propriétaire                                                                                               |
| `true`       | Tous les outils MCP différés. Claude Code envoie l'en-tête bêta même sur Vertex AI et via les proxies. Les demandes échouent sur les modèles Vertex AI antérieurs à Sonnet 4.5 ou Opus 4.5, ou sur les proxies qui ne supportent pas les blocs `tool_reference` |
| `auto`       | Mode seuil : les outils se chargent à l'avance s'ils s'ajustent dans 10 % de la fenêtre de contexte, différés sinon                                                                                                                                             |
| `auto:N`     | Mode seuil avec un pourcentage personnalisé, où `N` est 0-100. Par exemple, `auto:5` pour 5 %                                                                                                                                                                   |
| `false`      | Tous les outils MCP chargés à l'avance, pas de différé                                                                                                                                                                                                          |

```bash theme={null}
# Utiliser un seuil personnalisé de 5 %
ENABLE_TOOL_SEARCH=auto:5 claude

# Désactiver complètement la recherche d'outils
ENABLE_TOOL_SEARCH=false claude
```

Ou définissez la valeur dans le champ `env` de votre [settings.json](/fr/settings#available-settings).

Vous pouvez également désactiver l'outil `ToolSearch` spécifiquement :

```json theme={null}
{
  "permissions": {
    "deny": ["ToolSearch"]
  }
}
```

### Exempter un serveur du différé

Si les outils d'un serveur doivent toujours être visibles pour Claude sans une étape de recherche, définissez `alwaysLoad` à `true` dans la configuration de ce serveur. Chaque outil de ce serveur se charge alors dans le contexte au démarrage de la session indépendamment du paramètre `ENABLE_TOOL_SEARCH`. Utilisez ceci pour un petit nombre d'outils que Claude doit utiliser à chaque tour, car chaque outil à l'avance consomme du contexte qui serait autrement disponible pour votre conversation.

L'entrée `.mcp.json` suivante exempte un serveur HTTP tout en laissant les autres serveurs différés :

```json theme={null}
{
  "mcpServers": {
    "core-tools": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "alwaysLoad": true
    }
  }
}
```

Le champ `alwaysLoad` est disponible sur tous les types de serveurs et nécessite Claude Code v2.1.121 ou ultérieur. Un serveur MCP peut également marquer les outils individuels comme toujours chargés en incluant `"anthropic/alwaysLoad": true` dans l'objet `_meta` de l'outil, ce qui a le même effet pour cet outil uniquement.

La définition de `alwaysLoad: true` bloque également le démarrage jusqu'à ce que le serveur se connecte, limité au délai d'expiration de connexion standard de 5 secondes. Cela s'applique même lorsque MCP startup est autrement [non-bloquant par défaut](/fr/env-vars), car les outils doivent être présents lors de la construction de la première invite. Les autres serveurs continuent à se connecter en arrière-plan.

## Utiliser les prompts MCP comme commandes

Les serveurs MCP peuvent exposer des prompts qui deviennent disponibles en tant que commandes dans Claude Code.

### Exécuter les prompts MCP

<Steps>
  <Step title="Découvrir les prompts disponibles">
    Tapez `/` pour voir toutes les commandes disponibles, y compris celles des serveurs MCP. Les prompts MCP apparaissent au format `/mcp__servername__promptname`.
  </Step>

  <Step title="Exécuter un prompt sans arguments">
    ```text theme={null}
    /mcp__github__list_prs
    ```
  </Step>

  <Step title="Exécuter un prompt avec des arguments">
    De nombreux prompts acceptent des arguments. Passez-les séparés par des espaces après la commande :

    ```text theme={null}
    /mcp__github__pr_review 456
    ```

    ```text theme={null}
    /mcp__jira__create_issue "Bug in login flow" high
    ```
  </Step>
</Steps>

<Tip>
  Conseils :

  * Les prompts MCP sont découverts dynamiquement à partir des serveurs connectés
  * Les arguments sont analysés en fonction des paramètres définis du prompt
  * Les résultats du prompt sont injectés directement dans la conversation
  * Les noms de serveur et de prompt sont normalisés (les espaces deviennent des traits de soulignement)
</Tip>

## Configuration MCP gérée

Pour les organisations qui ont besoin d'un contrôle centralisé sur les serveurs MCP, Claude Code supporte deux options de configuration :

1. **Contrôle exclusif avec `managed-mcp.json`** : Déployer un ensemble fixe de serveurs MCP que les utilisateurs ne peuvent pas modifier ou étendre
2. **Contrôle basé sur les politiques avec listes blanches/noires** : Permettre aux utilisateurs d'ajouter leurs propres serveurs, mais restreindre lesquels sont autorisés

Ces options permettent aux administrateurs informatiques de :

* **Contrôler les serveurs MCP auxquels les employés peuvent accéder** : Déployer un ensemble standardisé de serveurs MCP approuvés dans toute l'organisation
* **Empêcher les serveurs MCP non autorisés** : Restreindre les utilisateurs d'ajouter des serveurs MCP non approuvés
* **Désactiver complètement MCP** : Supprimer complètement la fonctionnalité MCP si nécessaire

### Option 1 : Contrôle exclusif avec managed-mcp.json

Lorsque vous déployez un fichier `managed-mcp.json`, il prend le **contrôle exclusif** de tous les serveurs MCP. Les utilisateurs ne peuvent pas ajouter, modifier ou utiliser d'autres serveurs MCP que ceux définis dans ce fichier. C'est l'approche la plus simple pour les organisations qui veulent un contrôle complet.

Les administrateurs système déploient le fichier de configuration dans un répertoire à l'échelle du système :

* macOS : `/Library/Application Support/ClaudeCode/managed-mcp.json`
* Linux et WSL : `/etc/claude-code/managed-mcp.json`
* Windows : `C:\Program Files\ClaudeCode\managed-mcp.json`

<Note>
  Ce sont des chemins à l'échelle du système (pas des répertoires personnels comme `~/Library/...`) qui nécessitent des privilèges d'administrateur. Ils sont conçus pour être déployés par les administrateurs informatiques.
</Note>

Le fichier `managed-mcp.json` utilise le même format qu'un fichier `.mcp.json` standard :

```json theme={null}
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.company.com"
      }
    }
  }
}
```

### Option 2 : Contrôle basé sur les politiques avec listes blanches et noires

Au lieu de prendre le contrôle exclusif, les administrateurs peuvent permettre aux utilisateurs de configurer leurs propres serveurs MCP tout en appliquant des restrictions sur les serveurs autorisés. Cette approche utilise `allowedMcpServers` et `deniedMcpServers` dans le [fichier de paramètres gérés](/fr/settings#settings-files).

<Note>
  **Choisir entre les options** : Utilisez l'option 1 (`managed-mcp.json`) lorsque vous souhaitez déployer un ensemble fixe de serveurs sans personnalisation utilisateur. Utilisez l'option 2 (listes blanches/noires) lorsque vous souhaitez permettre aux utilisateurs d'ajouter leurs propres serveurs dans le respect des contraintes de politique.
</Note>

#### Options de restriction

Chaque entrée dans la liste blanche ou noire peut restreindre les serveurs de trois façons :

1. **Par nom de serveur** (`serverName`) : Correspond au nom configuré du serveur
2. **Par commande** (`serverCommand`) : Correspond à la commande exacte et aux arguments utilisés pour démarrer les serveurs stdio
3. **Par modèle d'URL** (`serverUrl`) : Correspond aux URL des serveurs distants avec support des caractères génériques

**Important** : Chaque entrée doit avoir exactement un de `serverName`, `serverCommand` ou `serverUrl`.

#### Exemple de configuration

```json theme={null}
{
  "allowedMcpServers": [
    // Autoriser par nom de serveur
    { "serverName": "github" },
    { "serverName": "sentry" },

    // Autoriser par commande exacte (pour les serveurs stdio)
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] },
    { "serverCommand": ["python", "/usr/local/bin/approved-server.py"] },

    // Autoriser par modèle d'URL (pour les serveurs distants)
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverUrl": "https://*.internal.corp/*" }
  ],
  "deniedMcpServers": [
    // Bloquer par nom de serveur
    { "serverName": "dangerous-server" },

    // Bloquer par commande exacte (pour les serveurs stdio)
    { "serverCommand": ["npx", "-y", "unapproved-package"] },

    // Bloquer par modèle d'URL (pour les serveurs distants)
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

#### Comment fonctionnent les restrictions basées sur les commandes

**Correspondance exacte** :

* Les tableaux de commandes doivent correspondre **exactement** - à la fois la commande et tous les arguments dans le bon ordre
* Exemple : `["npx", "-y", "server"]` ne correspondra PAS à `["npx", "server"]` ou `["npx", "-y", "server", "--flag"]`

**Comportement du serveur stdio** :

* Lorsque la liste blanche contient **n'importe quelle** entrée `serverCommand`, les serveurs stdio **doivent** correspondre à l'une de ces commandes
* Les serveurs stdio ne peuvent pas passer par le nom seul lorsque des restrictions de commande sont présentes
* Cela garantit que les administrateurs peuvent appliquer les commandes autorisées à s'exécuter

**Comportement du serveur non-stdio** :

* Les serveurs distants (HTTP, SSE, WebSocket) utilisent la correspondance basée sur l'URL lorsque des entrées `serverUrl` existent dans la liste blanche
* Si aucune entrée d'URL n'existe, les serveurs distants reviennent à la correspondance basée sur le nom
* Les restrictions de commande ne s'appliquent pas aux serveurs distants

#### Comment fonctionnent les restrictions basées sur l'URL

Les modèles d'URL supportent les caractères génériques en utilisant `*` pour correspondre à n'importe quelle séquence de caractères. Ceci est utile pour autoriser des domaines ou des sous-domaines entiers.

**Exemples de caractères génériques** :

* `https://mcp.company.com/*` - Autoriser tous les chemins sur un domaine spécifique
* `https://*.example.com/*` - Autoriser n'importe quel sous-domaine de example.com
* `http://localhost:*/*` - Autoriser n'importe quel port sur localhost

La correspondance du nom d'hôte est insensible à la casse et ignore un point FQDN final, en correspondant à la sémantique DNS. Un modèle comme `*://Mcp.Example.com/*` correspond à `https://mcp.example.com/api`, et `https://mcp.example.com.` est traité de la même manière que `https://mcp.example.com`. Les schémas et les chemins restent sensibles à la casse.

**Comportement du serveur distant** :

* Lorsque la liste blanche contient **n'importe quelle** entrée `serverUrl`, les serveurs distants **doivent** correspondre à l'un de ces modèles d'URL
* Les serveurs distants ne peuvent pas passer par le nom seul lorsque des restrictions d'URL sont présentes
* Cela garantit que les administrateurs peuvent appliquer les points de terminaison distants autorisés

<Accordion title="Exemple : Liste blanche URL uniquement">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverUrl": "https://mcp.company.com/*" },
      { "serverUrl": "https://*.internal.corp/*" }
    ]
  }
  ```

  **Résultat** :

  * Serveur HTTP à `https://mcp.company.com/api` : ✅ Autorisé (correspond au modèle d'URL)
  * Serveur HTTP à `https://api.internal.corp/mcp` : ✅ Autorisé (correspond au sous-domaine générique)
  * Serveur HTTP à `https://external.com/mcp` : ❌ Bloqué (ne correspond à aucun modèle d'URL)
  * Serveur stdio avec n'importe quelle commande : ❌ Bloqué (aucune entrée de nom ou de commande à correspondre)
</Accordion>

<Accordion title="Exemple : Liste blanche commande uniquement">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverCommand": ["npx", "-y", "approved-package"] }
    ]
  }
  ```

  **Résultat** :

  * Serveur stdio avec `["npx", "-y", "approved-package"]` : ✅ Autorisé (correspond à la commande)
  * Serveur stdio avec `["node", "server.js"]` : ❌ Bloqué (ne correspond pas à la commande)
  * Serveur HTTP nommé « my-api » : ❌ Bloqué (aucune entrée de nom à correspondre)
</Accordion>

<Accordion title="Exemple : Liste blanche mixte nom et commande">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverName": "github" },
      { "serverCommand": ["npx", "-y", "approved-package"] }
    ]
  }
  ```

  **Résultat** :

  * Serveur stdio nommé « local-tool » avec `["npx", "-y", "approved-package"]` : ✅ Autorisé (correspond à la commande)
  * Serveur stdio nommé « local-tool » avec `["node", "server.js"]` : ❌ Bloqué (les entrées de commande existent mais ne correspondent pas)
  * Serveur stdio nommé « github » avec `["node", "server.js"]` : ❌ Bloqué (les serveurs stdio doivent correspondre aux commandes lorsque les entrées de commande existent)
  * Serveur HTTP nommé « github » : ✅ Autorisé (correspond au nom)
  * Serveur HTTP nommé « other-api » : ❌ Bloqué (le nom ne correspond pas)
</Accordion>

<Accordion title="Exemple : Liste blanche nom uniquement">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverName": "github" },
      { "serverName": "internal-tool" }
    ]
  }
  ```

  **Résultat** :

  * Serveur stdio nommé « github » avec n'importe quelle commande : ✅ Autorisé (aucune restriction de commande)
  * Serveur stdio nommé « internal-tool » avec n'importe quelle commande : ✅ Autorisé (aucune restriction de commande)
  * Serveur HTTP nommé « github » : ✅ Autorisé (correspond au nom)
  * N'importe quel serveur nommé « other » : ❌ Bloqué (le nom ne correspond pas)
</Accordion>

#### Comportement de la liste blanche (`allowedMcpServers`)

* `undefined` (par défaut) : Aucune restriction - les utilisateurs peuvent configurer n'importe quel serveur MCP
* Tableau vide `[]` : Verrouillage complet - les utilisateurs ne peuvent configurer aucun serveur MCP
* Liste d'entrées : Les utilisateurs ne peuvent configurer que les serveurs qui correspondent par nom, commande ou modèle d'URL

#### Comportement de la liste noire (`deniedMcpServers`)

* `undefined` (par défaut) : Aucun serveur n'est bloqué
* Tableau vide `[]` : Aucun serveur n'est bloqué
* Liste d'entrées : Les serveurs spécifiés sont explicitement bloqués dans toutes les portées

#### Notes importantes

* **L'option 1 et l'option 2 peuvent être combinées** : Si `managed-mcp.json` existe, il a le contrôle exclusif et les utilisateurs ne peuvent pas ajouter de serveurs. Les listes blanches/noires s'appliquent toujours aux serveurs gérés eux-mêmes.
* **La liste noire a une précédence absolue** : Si un serveur correspond à une entrée de liste noire (par nom, commande ou URL), il sera bloqué même s'il est sur la liste blanche
* **Les restrictions basées sur le nom, la commande et l'URL fonctionnent ensemble** : un serveur passe s'il correspond à **soit** une entrée de nom, une entrée de commande, ou un modèle d'URL (sauf s'il est bloqué par la liste noire)

<Note>
  **Lors de l'utilisation de `managed-mcp.json`** : Les utilisateurs ne peuvent pas ajouter de serveurs MCP via `claude mcp add` ou les fichiers de configuration. Les paramètres `allowedMcpServers` et `deniedMcpServers` s'appliquent toujours pour filtrer les serveurs gérés qui sont réellement chargés.
</Note>
