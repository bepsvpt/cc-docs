> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Référence des plugins

> Référence technique complète du système de plugins Claude Code, incluant les schémas, les commandes CLI et les spécifications des composants.

<Tip>
  Vous cherchez à installer des plugins ? Consultez [Découvrir et installer des plugins](/fr/discover-plugins). Pour créer des plugins, consultez [Plugins](/fr/plugins). Pour distribuer des plugins, consultez [Marketplaces de plugins](/fr/plugin-marketplaces).
</Tip>

Cette référence fournit les spécifications techniques complètes du système de plugins Claude Code, incluant les schémas de composants, les commandes CLI et les outils de développement.

Un **plugin** est un répertoire autonome de composants qui étend Claude Code avec des fonctionnalités personnalisées. Les composants de plugin incluent les skills, les agents, les hooks, les serveurs MCP et les serveurs LSP.

## Référence des composants de plugin

### Skills

Les plugins ajoutent des skills à Claude Code, créant des raccourcis `/name` que vous ou Claude pouvez invoquer.

**Emplacement** : répertoire `skills/` ou `commands/` à la racine du plugin

**Format de fichier** : Les skills sont des répertoires avec `SKILL.md` ; les commandes sont des fichiers markdown simples

**Structure des skills** :

```text  theme={null}
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (optionnel)
│   └── scripts/ (optionnel)
└── code-reviewer/
    └── SKILL.md
```

**Comportement d'intégration** :

* Les skills et les commandes sont découverts automatiquement lors de l'installation du plugin
* Claude peut les invoquer automatiquement en fonction du contexte de la tâche
* Les skills peuvent inclure des fichiers de support à côté de SKILL.md

Pour plus de détails, consultez [Skills](/fr/skills).

### Agents

Les plugins peuvent fournir des subagents spécialisés pour des tâches spécifiques que Claude peut invoquer automatiquement si approprié.

**Emplacement** : répertoire `agents/` à la racine du plugin

**Format de fichier** : Fichiers markdown décrivant les capacités de l'agent

**Structure de l'agent** :

```markdown  theme={null}
---
name: agent-name
description: Ce dans quoi cet agent se spécialise et quand Claude devrait l'invoquer
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Write, Edit
---

Invite système détaillée pour l'agent décrivant son rôle, son expertise et son comportement.
```

Les agents de plugin prennent en charge les champs frontmatter `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background` et `isolation`. La seule valeur `isolation` valide est `"worktree"`. Pour des raisons de sécurité, `hooks`, `mcpServers` et `permissionMode` ne sont pas pris en charge pour les agents fournis par les plugins.

**Points d'intégration** :

* Les agents apparaissent dans l'interface `/agents`
* Claude peut invoquer les agents automatiquement en fonction du contexte de la tâche
* Les agents peuvent être invoqués manuellement par les utilisateurs
* Les agents de plugin fonctionnent aux côtés des agents Claude intégrés

Pour plus de détails, consultez [Subagents](/fr/sub-agents).

### Hooks

Les plugins peuvent fournir des gestionnaires d'événements qui répondent automatiquement aux événements de Claude Code.

**Emplacement** : `hooks/hooks.json` à la racine du plugin, ou en ligne dans plugin.json

**Format** : Configuration JSON avec des correspondances d'événements et des actions

**Configuration des hooks** :

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

Les hooks de plugin répondent aux mêmes événements de cycle de vie que les [hooks définis par l'utilisateur](/fr/hooks) :

| Event                | When it fires                                                                                                                                          |
| :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                                       |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                                   |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`  | When a permission dialog appears                                                                                                                       |
| `PostToolUse`        | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure` | After a tool call fails                                                                                                                                |
| `Notification`       | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`      | When a subagent is spawned                                                                                                                             |
| `SubagentStop`       | When a subagent finishes                                                                                                                               |
| `Stop`               | When Claude finishes responding                                                                                                                        |
| `StopFailure`        | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                               |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`       | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`         | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`        | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`         | Before context compaction                                                                                                                              |
| `PostCompact`        | After context compaction completes                                                                                                                     |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`         | When a session terminates                                                                                                                              |

**Types de hooks** :

* `command` : exécuter des commandes shell ou des scripts
* `http` : envoyer l'événement JSON en tant que requête POST à une URL
* `prompt` : évaluer une invite avec un LLM (utilise l'espace réservé `$ARGUMENTS` pour le contexte)
* `agent` : exécuter un vérificateur agentic avec des outils pour les tâches de vérification complexes

### Serveurs MCP

Les plugins peuvent regrouper des serveurs Model Context Protocol (MCP) pour connecter Claude Code avec des outils et services externes.

**Emplacement** : `.mcp.json` à la racine du plugin, ou en ligne dans plugin.json

**Format** : Configuration standard du serveur MCP

**Configuration du serveur MCP** :

```json  theme={null}
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**Comportement d'intégration** :

* Les serveurs MCP de plugin démarrent automatiquement quand le plugin est activé
* Les serveurs apparaissent comme des outils MCP standard dans la boîte à outils de Claude
* Les capacités du serveur s'intègrent de manière transparente avec les outils existants de Claude
* Les serveurs de plugin peuvent être configurés indépendamment des serveurs MCP de l'utilisateur

### Serveurs LSP

<Tip>
  Vous cherchez à utiliser des plugins LSP ? Installez-les depuis la marketplace officielle : recherchez « lsp » dans l'onglet Découvrir de `/plugin`. Cette section documente comment créer des plugins LSP pour les langages non couverts par la marketplace officielle.
</Tip>

Les plugins peuvent fournir des serveurs [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) pour donner à Claude une intelligence de code en temps réel lors du travail sur votre base de code.

L'intégration LSP fournit :

* **Diagnostics instantanés** : Claude voit les erreurs et les avertissements immédiatement après chaque modification
* **Navigation de code** : aller à la définition, trouver les références et les informations au survol
* **Sensibilisation au langage** : informations de type et documentation pour les symboles de code

**Emplacement** : `.lsp.json` à la racine du plugin, ou en ligne dans `plugin.json`

**Format** : Configuration JSON mappant les noms des serveurs de langage à leurs configurations

**Format du fichier `.lsp.json`** :

```json  theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**En ligne dans `plugin.json`** :

```json  theme={null}
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**Champs obligatoires :**

| Champ                 | Description                                                 |
| :-------------------- | :---------------------------------------------------------- |
| `command`             | Le binaire LSP à exécuter (doit être dans PATH)             |
| `extensionToLanguage` | Mappe les extensions de fichier aux identifiants de langage |

**Champs optionnels :**

| Champ                   | Description                                                        |
| :---------------------- | :----------------------------------------------------------------- |
| `args`                  | Arguments de ligne de commande pour le serveur LSP                 |
| `transport`             | Transport de communication : `stdio` (par défaut) ou `socket`      |
| `env`                   | Variables d'environnement à définir au démarrage du serveur        |
| `initializationOptions` | Options transmises au serveur lors de l'initialisation             |
| `settings`              | Paramètres transmis via `workspace/didChangeConfiguration`         |
| `workspaceFolder`       | Chemin du dossier de l'espace de travail pour le serveur           |
| `startupTimeout`        | Temps maximum d'attente du démarrage du serveur (millisecondes)    |
| `shutdownTimeout`       | Temps maximum d'attente de l'arrêt gracieux (millisecondes)        |
| `restartOnCrash`        | S'il faut redémarrer automatiquement le serveur en cas de plantage |
| `maxRestarts`           | Nombre maximum de tentatives de redémarrage avant d'abandonner     |

<Warning>
  **Vous devez installer le binaire du serveur de langage séparément.** Les plugins LSP configurent comment Claude Code se connecte à un serveur de langage, mais ils n'incluent pas le serveur lui-même. Si vous voyez `Executable not found in $PATH` dans l'onglet Erreurs de `/plugin`, installez le binaire requis pour votre langage.
</Warning>

**Plugins LSP disponibles :**

| Plugin           | Serveur de langage         | Commande d'installation                                                                          |
| :--------------- | :------------------------- | :----------------------------------------------------------------------------------------------- |
| `pyright-lsp`    | Pyright (Python)           | `pip install pyright` ou `npm install -g pyright`                                                |
| `typescript-lsp` | TypeScript Language Server | `npm install -g typescript-language-server typescript`                                           |
| `rust-lsp`       | rust-analyzer              | [Voir l'installation de rust-analyzer](https://rust-analyzer.github.io/manual.html#installation) |

Installez d'abord le serveur de langage, puis installez le plugin depuis la marketplace.

***

## Portées d'installation des plugins

Quand vous installez un plugin, vous choisissez une **portée** qui détermine où le plugin est disponible et qui d'autre peut l'utiliser :

| Portée    | Fichier de paramètres                           | Cas d'usage                                                       |
| :-------- | :---------------------------------------------- | :---------------------------------------------------------------- |
| `user`    | `~/.claude/settings.json`                       | Plugins personnels disponibles dans tous les projets (par défaut) |
| `project` | `.claude/settings.json`                         | Plugins d'équipe partagés via le contrôle de version              |
| `local`   | `.claude/settings.local.json`                   | Plugins spécifiques au projet, ignorés par git                    |
| `managed` | [Paramètres gérés](/fr/settings#settings-files) | Plugins gérés (lecture seule, mise à jour uniquement)             |

Les plugins utilisent le même système de portée que les autres configurations de Claude Code. Pour les instructions d'installation et les drapeaux de portée, consultez [Installer des plugins](/fr/discover-plugins#install-plugins). Pour une explication complète des portées, consultez [Portées de configuration](/fr/settings#configuration-scopes).

***

## Schéma du manifeste du plugin

Le fichier `.claude-plugin/plugin.json` définit les métadonnées et la configuration de votre plugin. Cette section documente tous les champs et options pris en charge.

Le manifeste est optionnel. S'il est omis, Claude Code découvre automatiquement les composants dans les [emplacements par défaut](#file-locations-reference) et dérive le nom du plugin du nom du répertoire. Utilisez un manifeste quand vous devez fournir des métadonnées ou des chemins de composants personnalisés.

### Schéma complet

```json  theme={null}
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

### Champs obligatoires

Si vous incluez un manifeste, `name` est le seul champ obligatoire.

| Champ  | Type   | Description                                    | Exemple              |
| :----- | :----- | :--------------------------------------------- | :------------------- |
| `name` | string | Identifiant unique (kebab-case, pas d'espaces) | `"deployment-tools"` |

Ce nom est utilisé pour l'espace de noms des composants. Par exemple, dans l'interface utilisateur, l'agent `agent-creator` pour le plugin avec le nom `plugin-dev` apparaîtra comme `plugin-dev:agent-creator`.

### Champs de métadonnées

| Champ         | Type   | Description                                                                                                                                                                | Exemple                                            |
| :------------ | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `version`     | string | Version sémantique. Si elle est également définie dans l'entrée de la marketplace, `plugin.json` a la priorité. Vous n'avez besoin de la définir que dans un seul endroit. | `"2.1.0"`                                          |
| `description` | string | Explication brève de l'objectif du plugin                                                                                                                                  | `"Deployment automation tools"`                    |
| `author`      | object | Informations sur l'auteur                                                                                                                                                  | `{"name": "Dev Team", "email": "dev@company.com"}` |
| `homepage`    | string | URL de documentation                                                                                                                                                       | `"https://docs.example.com"`                       |
| `repository`  | string | URL du code source                                                                                                                                                         | `"https://github.com/user/plugin"`                 |
| `license`     | string | Identifiant de licence                                                                                                                                                     | `"MIT"`, `"Apache-2.0"`                            |
| `keywords`    | array  | Balises de découverte                                                                                                                                                      | `["deployment", "ci-cd"]`                          |

### Champs de chemin de composant

| Champ          | Type                  | Description                                                                                                                                                                        | Exemple                                |
| :------------- | :-------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------- |
| `commands`     | string\|array         | Fichiers/répertoires de commandes supplémentaires                                                                                                                                  | `"./custom/cmd.md"` ou `["./cmd1.md"]` |
| `agents`       | string\|array         | Fichiers d'agents supplémentaires                                                                                                                                                  | `"./custom/agents/reviewer.md"`        |
| `skills`       | string\|array         | Répertoires de skills supplémentaires                                                                                                                                              | `"./custom/skills/"`                   |
| `hooks`        | string\|array\|object | Chemins de configuration des hooks ou configuration en ligne                                                                                                                       | `"./my-extra-hooks.json"`              |
| `mcpServers`   | string\|array\|object | Chemins de configuration MCP ou configuration en ligne                                                                                                                             | `"./my-extra-mcp-config.json"`         |
| `outputStyles` | string\|array         | Fichiers/répertoires de styles de sortie supplémentaires                                                                                                                           | `"./styles/"`                          |
| `lspServers`   | string\|array\|object | Configurations [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) pour l'intelligence de code (aller à la définition, trouver les références, etc.) | `"./.lsp.json"`                        |
| `userConfig`   | object                | Valeurs configurables par l'utilisateur demandées au moment de l'activation. Consultez [Configuration utilisateur](#user-configuration)                                            | Voir ci-dessous                        |
| `channels`     | array                 | Déclarations de canaux pour l'injection de messages (style Telegram, Slack, Discord). Consultez [Canaux](#channels)                                                                | Voir ci-dessous                        |

### Configuration utilisateur

Le champ `userConfig` déclare les valeurs que Claude Code demande à l'utilisateur lors de l'activation du plugin. Utilisez ceci au lieu d'exiger que les utilisateurs modifient manuellement `settings.json`.

```json  theme={null}
{
  "userConfig": {
    "api_endpoint": {
      "description": "Le point de terminaison API de votre équipe",
      "sensitive": false
    },
    "api_token": {
      "description": "Jeton d'authentification API",
      "sensitive": true
    }
  }
}
```

Les clés doivent être des identifiants valides. Chaque valeur est disponible pour la substitution en tant que `${user_config.KEY}` dans les configurations de serveurs MCP et LSP, les commandes de hook, et (pour les valeurs non sensibles uniquement) le contenu des skills et des agents. Les valeurs sont également exportées vers les sous-processus du plugin en tant que variables d'environnement `CLAUDE_PLUGIN_OPTION_<KEY>`.

Les valeurs non sensibles sont stockées dans `settings.json` sous `pluginConfigs[<plugin-id>].options`. Les valeurs sensibles vont au trousseau système (ou `~/.claude/.credentials.json` où le trousseau n'est pas disponible). Le stockage du trousseau est partagé avec les jetons OAuth et a une limite totale d'environ 2 KB, donc gardez les valeurs sensibles petites.

### Canaux

Le champ `channels` permet à un plugin de déclarer un ou plusieurs canaux de messages qui injectent du contenu dans la conversation. Chaque canal se lie à un serveur MCP que le plugin fournit.

```json  theme={null}
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": { "description": "Jeton de bot Telegram", "sensitive": true },
        "owner_id": { "description": "Votre ID utilisateur Telegram", "sensitive": false }
      }
    }
  ]
}
```

Le champ `server` est obligatoire et doit correspondre à une clé dans les `mcpServers` du plugin. Le `userConfig` optionnel par canal utilise le même schéma que le champ de niveau supérieur, permettant au plugin de demander des jetons de bot ou des ID de propriétaire lors de l'activation du plugin.

### Règles de comportement des chemins

**Important** : Les chemins personnalisés complètent les répertoires par défaut - ils ne les remplacent pas.

* Si `commands/` existe, il est chargé en plus des chemins de commandes personnalisés
* Tous les chemins doivent être relatifs à la racine du plugin et commencer par `./`
* Les commandes des chemins personnalisés utilisent les mêmes règles de nommage et d'espace de noms
* Plusieurs chemins peuvent être spécifiés sous forme de tableaux pour plus de flexibilité

**Exemples de chemins** :

```json  theme={null}
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### Variables d'environnement

Claude Code fournit deux variables pour référencer les chemins des plugins. Les deux sont substituées en ligne partout où elles apparaissent dans le contenu des skills, le contenu des agents, les commandes de hook, et les configurations des serveurs MCP ou LSP. Les deux sont également exportées en tant que variables d'environnement vers les processus de hook et les sous-processus des serveurs MCP ou LSP.

**`${CLAUDE_PLUGIN_ROOT}`** : le chemin absolu du répertoire d'installation de votre plugin. Utilisez ceci pour référencer les scripts, les binaires et les fichiers de configuration fournis avec le plugin. Ce chemin change quand le plugin se met à jour, donc les fichiers que vous écrivez ici ne survivent pas à une mise à jour.

**`${CLAUDE_PLUGIN_DATA}`** : un répertoire persistant pour l'état du plugin qui survit aux mises à jour. Utilisez ceci pour les dépendances installées telles que `node_modules` ou les environnements virtuels Python, le code généré, les caches et tous les autres fichiers qui doivent persister entre les versions du plugin. Le répertoire est créé automatiquement la première fois que cette variable est référencée.

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

#### Répertoire de données persistantes

Le répertoire `${CLAUDE_PLUGIN_DATA}` se résout en `~/.claude/plugins/data/{id}/`, où `{id}` est l'identifiant du plugin avec les caractères en dehors de `a-z`, `A-Z`, `0-9`, `_` et `-` remplacés par `-`. Pour un plugin installé en tant que `formatter@my-marketplace`, le répertoire est `~/.claude/plugins/data/formatter-my-marketplace/`.

Un usage courant est d'installer les dépendances de langage une fois et de les réutiliser entre les sessions et les mises à jour du plugin. Parce que le répertoire de données survit à n'importe quelle version unique du plugin, une vérification de l'existence du répertoire seul ne peut pas détecter quand une mise à jour change le manifeste de dépendance du plugin. Le motif recommandé compare le manifeste fourni par rapport à une copie dans le répertoire de données et réinstalle quand ils diffèrent.

Ce hook `SessionStart` installe `node_modules` à la première exécution et à nouveau chaque fois qu'une mise à jour du plugin inclut un `package.json` modifié :

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

Le `diff` sort avec un code non nul quand la copie stockée est manquante ou diffère de celle fournie, couvrant à la fois la première exécution et les mises à jour changeant les dépendances. Si `npm install` échoue, le `rm` final supprime le manifeste copié pour que la session suivante réessaie.

Les scripts fournis dans `${CLAUDE_PLUGIN_ROOT}` peuvent ensuite s'exécuter contre les `node_modules` persistants :

```json  theme={null}
{
  "mcpServers": {
    "routines": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "NODE_PATH": "${CLAUDE_PLUGIN_DATA}/node_modules"
      }
    }
  }
}
```

Le répertoire de données est supprimé automatiquement quand vous désinstallez le plugin de la dernière portée où il est installé. L'interface `/plugin` affiche la taille du répertoire et demande une confirmation avant la suppression. La CLI supprime par défaut ; passez [`--keep-data`](#plugin-uninstall) pour le conserver.

***

## Mise en cache des plugins et résolution des fichiers

Les plugins sont spécifiés de deux façons :

* Via `claude --plugin-dir`, pour la durée d'une session.
* Via une marketplace, installés pour les sessions futures.

À des fins de sécurité et de vérification, Claude Code copie les plugins de *marketplace* dans le **cache de plugins** local de l'utilisateur (`~/.claude/plugins/cache`) plutôt que de les utiliser sur place. Comprendre ce comportement est important lors du développement de plugins qui référencent des fichiers externes.

### Limitations de traversée de répertoires

Les plugins installés ne peuvent pas référencer des fichiers en dehors de leur répertoire. Les chemins qui traversent en dehors de la racine du plugin (comme `../shared-utils`) ne fonctionneront pas après l'installation car ces fichiers externes ne sont pas copiés dans le cache.

### Travail avec les dépendances externes

Si votre plugin doit accéder à des fichiers en dehors de son répertoire, vous pouvez créer des liens symboliques vers des fichiers externes dans votre répertoire de plugin. Les liens symboliques sont honorés lors du processus de copie :

```bash  theme={null}
# À l'intérieur de votre répertoire de plugin
ln -s /path/to/shared-utils ./shared-utils
```

Le contenu lié symboliquement sera copié dans le cache de plugins. Cela offre de la flexibilité tout en maintenant les avantages de sécurité du système de mise en cache.

***

## Structure du répertoire des plugins

### Disposition standard des plugins

Un plugin complet suit cette structure :

```text  theme={null}
enterprise-plugin/
├── .claude-plugin/           # Répertoire de métadonnées (optionnel)
│   └── plugin.json             # manifeste du plugin
├── commands/                 # Emplacement de commande par défaut
│   ├── status.md
│   └── logs.md
├── agents/                   # Emplacement d'agent par défaut
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                   # Skills d'agent
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Configurations des hooks
│   ├── hooks.json           # Configuration principale des hooks
│   └── security-hooks.json  # Hooks supplémentaires
├── settings.json            # Paramètres par défaut pour le plugin
├── .mcp.json                # Définitions du serveur MCP
├── .lsp.json                # Configurations du serveur LSP
├── scripts/                 # Scripts de hooks et d'utilitaires
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # Fichier de licence
└── CHANGELOG.md             # Historique des versions
```

<Warning>
  Le répertoire `.claude-plugin/` contient le fichier `plugin.json`. Tous les autres répertoires (commands/, agents/, skills/, hooks/) doivent être à la racine du plugin, pas à l'intérieur de `.claude-plugin/`.
</Warning>

### Référence des emplacements de fichiers

| Composant        | Emplacement par défaut       | Objectif                                                                                                                                       |
| :--------------- | :--------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| **Manifeste**    | `.claude-plugin/plugin.json` | Métadonnées et configuration du plugin (optionnel)                                                                                             |
| **Commandes**    | `commands/`                  | Fichiers Markdown de skill (hérité ; utilisez `skills/` pour les nouveaux skills)                                                              |
| **Agents**       | `agents/`                    | Fichiers Markdown de subagent                                                                                                                  |
| **Skills**       | `skills/`                    | Skills avec structure `<name>/SKILL.md`                                                                                                        |
| **Hooks**        | `hooks/hooks.json`           | Configuration des hooks                                                                                                                        |
| **Serveurs MCP** | `.mcp.json`                  | Définitions du serveur MCP                                                                                                                     |
| **Serveurs LSP** | `.lsp.json`                  | Configurations du serveur de langage                                                                                                           |
| **Paramètres**   | `settings.json`              | Configuration par défaut appliquée quand le plugin est activé. Seuls les paramètres [`agent`](/fr/sub-agents) sont actuellement pris en charge |

***

## Référence des commandes CLI

Claude Code fournit des commandes CLI pour la gestion des plugins non interactive, utile pour les scripts et l'automatisation.

### plugin install

Installez un plugin à partir des marketplaces disponibles.

```bash  theme={null}
claude plugin install <plugin> [options]
```

**Arguments :**

* `<plugin>` : Nom du plugin ou `plugin-name@marketplace-name` pour une marketplace spécifique

**Options :**

| Option                | Description                                           | Par défaut |
| :-------------------- | :---------------------------------------------------- | :--------- |
| `-s, --scope <scope>` | Portée d'installation : `user`, `project`, ou `local` | `user`     |
| `-h, --help`          | Afficher l'aide pour la commande                      |            |

La portée détermine quel fichier de paramètres le plugin installé est ajouté. Par exemple, --scope project écrit dans `enabledPlugins` dans .claude/settings.json, rendant le plugin disponible à tous ceux qui clonent le référentiel du projet.

**Exemples :**

```bash  theme={null}
# Installer dans la portée utilisateur (par défaut)
claude plugin install formatter@my-marketplace

# Installer dans la portée du projet (partagé avec l'équipe)
claude plugin install formatter@my-marketplace --scope project

# Installer dans la portée locale (ignorée par git)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

Supprimez un plugin installé.

```bash  theme={null}
claude plugin uninstall <plugin> [options]
```

**Arguments :**

* `<plugin>` : Nom du plugin ou `plugin-name@marketplace-name`

**Options :**

| Option                | Description                                                                             | Par défaut |
| :-------------------- | :-------------------------------------------------------------------------------------- | :--------- |
| `-s, --scope <scope>` | Désinstaller de la portée : `user`, `project`, ou `local`                               | `user`     |
| `--keep-data`         | Conserver le [répertoire de données persistantes](#persistent-data-directory) du plugin |            |
| `-h, --help`          | Afficher l'aide pour la commande                                                        |            |

**Alias :** `remove`, `rm`

Par défaut, la désinstallation de la dernière portée restante supprime également le répertoire `${CLAUDE_PLUGIN_DATA}` du plugin. Utilisez `--keep-data` pour le conserver, par exemple lors de la réinstallation après le test d'une nouvelle version.

### plugin enable

Activez un plugin désactivé.

```bash  theme={null}
claude plugin enable <plugin> [options]
```

**Arguments :**

* `<plugin>` : Nom du plugin ou `plugin-name@marketplace-name`

**Options :**

| Option                | Description                                      | Par défaut |
| :-------------------- | :----------------------------------------------- | :--------- |
| `-s, --scope <scope>` | Portée à activer : `user`, `project`, ou `local` | `user`     |
| `-h, --help`          | Afficher l'aide pour la commande                 |            |

### plugin disable

Désactivez un plugin sans le désinstaller.

```bash  theme={null}
claude plugin disable <plugin> [options]
```

**Arguments :**

* `<plugin>` : Nom du plugin ou `plugin-name@marketplace-name`

**Options :**

| Option                | Description                                         | Par défaut |
| :-------------------- | :-------------------------------------------------- | :--------- |
| `-s, --scope <scope>` | Portée à désactiver : `user`, `project`, ou `local` | `user`     |
| `-h, --help`          | Afficher l'aide pour la commande                    |            |

### plugin update

Mettez à jour un plugin vers la dernière version.

```bash  theme={null}
claude plugin update <plugin> [options]
```

**Arguments :**

* `<plugin>` : Nom du plugin ou `plugin-name@marketplace-name`

**Options :**

| Option                | Description                                                       | Par défaut |
| :-------------------- | :---------------------------------------------------------------- | :--------- |
| `-s, --scope <scope>` | Portée à mettre à jour : `user`, `project`, `local`, ou `managed` | `user`     |
| `-h, --help`          | Afficher l'aide pour la commande                                  |            |

***

## Outils de débogage et de développement

### Commandes de débogage

Utilisez `claude --debug` pour voir les détails du chargement des plugins :

Cela affiche :

* Quels plugins sont en cours de chargement
* Toute erreur dans les manifestes de plugins
* Enregistrement des commandes, agents et hooks
* Initialisation du serveur MCP

### Problèmes courants

| Problème                            | Cause                              | Solution                                                                                                                                                                                       |
| :---------------------------------- | :--------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Plugin ne se charge pas             | `plugin.json` invalide             | Exécutez `claude plugin validate` ou `/plugin validate` pour vérifier `plugin.json`, le frontmatter des skills/agents/commandes et `hooks/hooks.json` pour les erreurs de syntaxe et de schéma |
| Les commandes n'apparaissent pas    | Structure de répertoire incorrecte | Assurez-vous que `commands/` est à la racine, pas dans `.claude-plugin/`                                                                                                                       |
| Les hooks ne se déclenchent pas     | Le script n'est pas exécutable     | Exécutez `chmod +x script.sh`                                                                                                                                                                  |
| Le serveur MCP échoue               | `${CLAUDE_PLUGIN_ROOT}` manquant   | Utilisez la variable pour tous les chemins de plugin                                                                                                                                           |
| Erreurs de chemin                   | Chemins absolus utilisés           | Tous les chemins doivent être relatifs et commencer par `./`                                                                                                                                   |
| LSP `Executable not found in $PATH` | Serveur de langage non installé    | Installez le binaire (par exemple, `npm install -g typescript-language-server typescript`)                                                                                                     |

### Exemples de messages d'erreur

**Erreurs de validation du manifeste** :

* `Invalid JSON syntax: Unexpected token } in JSON at position 142` : vérifiez les virgules manquantes, les virgules supplémentaires ou les chaînes non citées
* `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required` : un champ obligatoire est manquant
* `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...` : erreur de syntaxe JSON

**Erreurs de chargement du plugin** :

* `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.` : le chemin de commande existe mais ne contient aucun fichier de commande valide
* `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.` : le chemin `source` dans marketplace.json pointe vers un répertoire inexistant
* `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.` : supprimez les définitions de composants en double ou supprimez `strict: false` dans l'entrée de la marketplace

### Dépannage des hooks

**Le script du hook ne s'exécute pas** :

1. Vérifiez que le script est exécutable : `chmod +x ./scripts/your-script.sh`
2. Vérifiez la ligne shebang : La première ligne doit être `#!/bin/bash` ou `#!/usr/bin/env bash`
3. Vérifiez que le chemin utilise `${CLAUDE_PLUGIN_ROOT}` : `"command": "${CLAUDE_PLUGIN_ROOT}/scripts/your-script.sh"`
4. Testez le script manuellement : `./scripts/your-script.sh`

**Le hook ne se déclenche pas sur les événements attendus** :

1. Vérifiez que le nom de l'événement est correct (sensible à la casse) : `PostToolUse`, pas `postToolUse`
2. Vérifiez que le motif de correspondance correspond à vos outils : `"matcher": "Write|Edit"` pour les opérations de fichier
3. Confirmez que le type de hook est valide : `command`, `http`, `prompt`, ou `agent`

### Dépannage du serveur MCP

**Le serveur ne démarre pas** :

1. Vérifiez que la commande existe et est exécutable
2. Vérifiez que tous les chemins utilisent la variable `${CLAUDE_PLUGIN_ROOT}`
3. Vérifiez les journaux du serveur MCP : `claude --debug` affiche les erreurs d'initialisation
4. Testez le serveur manuellement en dehors de Claude Code

**Les outils du serveur n'apparaissent pas** :

1. Assurez-vous que le serveur est correctement configuré dans `.mcp.json` ou `plugin.json`
2. Vérifiez que le serveur implémente correctement le protocole MCP
3. Vérifiez les délais d'expiration de la connexion dans la sortie de débogage

### Erreurs de structure de répertoire

**Symptômes** : Le plugin se charge mais les composants (commandes, agents, hooks) sont manquants.

**Structure correcte** : Les composants doivent être à la racine du plugin, pas à l'intérieur de `.claude-plugin/`. Seul `plugin.json` appartient à `.claude-plugin/`.

```text  theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← Seul le manifeste ici
├── commands/            ← Au niveau racine
├── agents/              ← Au niveau racine
└── hooks/               ← Au niveau racine
```

Si vos composants sont à l'intérieur de `.claude-plugin/`, déplacez-les à la racine du plugin.

**Liste de contrôle de débogage** :

1. Exécutez `claude --debug` et recherchez les messages « loading plugin »
2. Vérifiez que chaque répertoire de composants est listé dans la sortie de débogage
3. Vérifiez que les permissions de fichier permettent de lire les fichiers du plugin

***

## Référence de distribution et de versioning

### Gestion des versions

Suivez le versioning sémantique pour les versions de plugin :

```json  theme={null}
{
  "name": "my-plugin",
  "version": "2.1.0"
}
```

**Format de version** : `MAJOR.MINOR.PATCH`

* **MAJOR** : Changements cassants (changements d'API incompatibles)
* **MINOR** : Nouvelles fonctionnalités (ajouts rétro-compatibles)
* **PATCH** : Corrections de bugs (corrections rétro-compatibles)

**Meilleures pratiques** :

* Commencez à `1.0.0` pour votre première version stable
* Mettez à jour la version dans `plugin.json` avant de distribuer les modifications
* Documentez les modifications dans un fichier `CHANGELOG.md`
* Utilisez des versions de pré-version comme `2.0.0-beta.1` pour les tests

<Warning>
  Claude Code utilise la version pour déterminer s'il faut mettre à jour votre plugin. Si vous modifiez le code de votre plugin mais ne mettez pas à jour la version dans `plugin.json`, les utilisateurs existants de votre plugin ne verront pas vos modifications en raison de la mise en cache.

  Si votre plugin se trouve dans un répertoire de [marketplace](/fr/plugin-marketplaces), vous pouvez gérer la version via `marketplace.json` à la place et omettre le champ `version` de `plugin.json`.
</Warning>

***

## Voir aussi

* [Plugins](/fr/plugins) - Tutoriels et utilisation pratique
* [Marketplaces de plugins](/fr/plugin-marketplaces) - Création et gestion des marketplaces
* [Skills](/fr/skills) - Détails du développement des skills
* [Subagents](/fr/sub-agents) - Configuration et capacités des agents
* [Hooks](/fr/hooks) - Gestion des événements et automatisation
* [MCP](/fr/mcp) - Intégration des outils externes
* [Paramètres](/fr/settings) - Options de configuration pour les plugins
