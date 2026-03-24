> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Créer et distribuer une place de marché de plugins

> Créez et hébergez des places de marché de plugins pour distribuer les extensions Claude Code dans vos équipes et communautés.

Une **place de marché de plugins** est un catalogue qui vous permet de distribuer des plugins à d'autres. Les places de marché offrent une découverte centralisée, un suivi des versions, des mises à jour automatiques et la prise en charge de plusieurs types de sources (dépôts git, chemins locaux, etc.). Ce guide vous montre comment créer votre propre place de marché pour partager des plugins avec votre équipe ou votre communauté.

Vous cherchez à installer des plugins à partir d'une place de marché existante ? Consultez [Découvrir et installer des plugins préconfigurés](/fr/discover-plugins).

## Aperçu

La création et la distribution d'une place de marché impliquent :

1. **Créer des plugins** : créez un ou plusieurs plugins avec des commandes, des agents, des hooks, des serveurs MCP ou des serveurs LSP. Ce guide suppose que vous avez déjà des plugins à distribuer ; consultez [Créer des plugins](/fr/plugins) pour plus de détails sur la création de plugins.
2. **Créer un fichier de place de marché** : définissez un `marketplace.json` qui répertorie vos plugins et où les trouver (voir [Créer le fichier de place de marché](#create-the-marketplace-file)).
3. **Héberger la place de marché** : poussez vers GitHub, GitLab ou un autre hôte git (voir [Héberger et distribuer les places de marché](#host-and-distribute-marketplaces)).
4. **Partager avec les utilisateurs** : les utilisateurs ajoutent votre place de marché avec `/plugin marketplace add` et installent des plugins individuels (voir [Découvrir et installer des plugins](/fr/discover-plugins)).

Une fois votre place de marché en ligne, vous pouvez la mettre à jour en poussant les modifications vers votre dépôt. Les utilisateurs actualisent leur copie locale avec `/plugin marketplace update`.

## Procédure pas à pas : créer une place de marché locale

Cet exemple crée une place de marché avec un plugin : une compétence `/quality-review` pour les révisions de code. Vous allez créer la structure de répertoires, ajouter une compétence, créer le manifeste du plugin et le catalogue de la place de marché, puis l'installer et la tester.

<Steps>
  <Step title="Créer la structure de répertoires">
    ```bash  theme={null}
    mkdir -p my-marketplace/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/skills/quality-review
    ```
  </Step>

  <Step title="Créer la compétence">
    Créez un fichier `SKILL.md` qui définit ce que fait la compétence `/quality-review`.

    ```markdown my-marketplace/plugins/quality-review-plugin/skills/quality-review/SKILL.md theme={null}
    ---
    description: Review code for bugs, security, and performance
    disable-model-invocation: true
    ---

    Review the code I've selected or the recent changes for:
    - Potential bugs or edge cases
    - Security concerns
    - Performance issues
    - Readability improvements

    Be concise and actionable.
    ```
  </Step>

  <Step title="Créer le manifeste du plugin">
    Créez un fichier `plugin.json` qui décrit le plugin. Le manifeste se trouve dans le répertoire `.claude-plugin/`.

    ```json my-marketplace/plugins/quality-review-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "quality-review-plugin",
      "description": "Adds a /quality-review skill for quick code reviews",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Créer le fichier de place de marché">
    Créez le catalogue de la place de marché qui répertorie votre plugin.

    ```json my-marketplace/.claude-plugin/marketplace.json theme={null}
    {
      "name": "my-plugins",
      "owner": {
        "name": "Your Name"
      },
      "plugins": [
        {
          "name": "quality-review-plugin",
          "source": "./plugins/quality-review-plugin",
          "description": "Adds a /quality-review skill for quick code reviews"
        }
      ]
    }
    ```
  </Step>

  <Step title="Ajouter et installer">
    Ajoutez la place de marché et installez le plugin.

    ```shell  theme={null}
    /plugin marketplace add ./my-marketplace
    /plugin install quality-review-plugin@my-plugins
    ```
  </Step>

  <Step title="Essayer">
    Sélectionnez du code dans votre éditeur et exécutez votre nouvelle commande.

    ```shell  theme={null}
    /review
    ```
  </Step>
</Steps>

Pour en savoir plus sur ce que les plugins peuvent faire, notamment les hooks, les agents, les serveurs MCP et les serveurs LSP, consultez [Plugins](/fr/plugins).

<Note>
  **Comment les plugins sont installés** : Lorsque les utilisateurs installent un plugin, Claude Code copie le répertoire du plugin vers un emplacement de cache. Cela signifie que les plugins ne peuvent pas référencer des fichiers en dehors de leur répertoire en utilisant des chemins comme `../shared-utils`, car ces fichiers ne seront pas copiés.

  Si vous devez partager des fichiers entre les plugins, utilisez des symlinks (qui sont suivis lors de la copie). Consultez [Plugin caching and file resolution](/fr/plugins-reference#plugin-caching-and-file-resolution) pour plus de détails.
</Note>

## Créer le fichier de place de marché

Créez `.claude-plugin/marketplace.json` à la racine de votre dépôt. Ce fichier définit le nom de votre place de marché, les informations du propriétaire et une liste de plugins avec leurs sources.

Chaque entrée de plugin a besoin au minimum d'un `name` et d'une `source` (où la récupérer). Consultez le [schéma complet](#marketplace-schema) ci-dessous pour tous les champs disponibles.

```json  theme={null}
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Automatic code formatting on save",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      }
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Deployment automation tools"
    }
  ]
}
```

## Schéma de la place de marché

### Champs obligatoires

| Champ     | Type   | Description                                                                                                                                                                                                     | Exemple         |
| :-------- | :----- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------- |
| `name`    | string | Identifiant de la place de marché (kebab-case, sans espaces). C'est un élément public : les utilisateurs le voient lors de l'installation de plugins (par exemple, `/plugin install my-tool@your-marketplace`). | `"acme-tools"`  |
| `owner`   | object | Informations du responsable de la place de marché ([voir les champs ci-dessous](#owner-fields))                                                                                                                 |                 |
| `plugins` | array  | Liste des plugins disponibles                                                                                                                                                                                   | Voir ci-dessous |

<Note>
  **Noms réservés** : Les noms de place de marché suivants sont réservés à l'usage officiel d'Anthropic et ne peuvent pas être utilisés par les places de marché tierces : `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `life-sciences`. Les noms qui usurpent l'identité de places de marché officielles (comme `official-claude-plugins` ou `anthropic-tools-v2`) sont également bloqués.
</Note>

### Champs du propriétaire

| Champ   | Type   | Obligatoire | Description                              |
| :------ | :----- | :---------- | :--------------------------------------- |
| `name`  | string | Oui         | Nom du responsable ou de l'équipe        |
| `email` | string | Non         | Adresse e-mail de contact du responsable |

### Métadonnées optionnelles

| Champ                  | Type   | Description                                                                                                                                                                               |
| :--------------------- | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `metadata.description` | string | Brève description de la place de marché                                                                                                                                                   |
| `metadata.version`     | string | Version de la place de marché                                                                                                                                                             |
| `metadata.pluginRoot`  | string | Répertoire de base ajouté aux chemins de source de plugin relatifs (par exemple, `"./plugins"` vous permet d'écrire `"source": "formatter"` au lieu de `"source": "./plugins/formatter"`) |

## Entrées de plugin

Chaque entrée de plugin dans le tableau `plugins` décrit un plugin et où le trouver. Vous pouvez inclure n'importe quel champ du [schéma du manifeste du plugin](/fr/plugins-reference#plugin-manifest-schema) (comme `description`, `version`, `author`, `commands`, `hooks`, etc.), plus ces champs spécifiques à la place de marché : `source`, `category`, `tags` et `strict`.

### Champs obligatoires

| Champ    | Type           | Description                                                                                                                                                                           |
| :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`   | string         | Identifiant du plugin (kebab-case, sans espaces). C'est un élément public : les utilisateurs le voient lors de l'installation (par exemple, `/plugin install my-plugin@marketplace`). |
| `source` | string\|object | Où récupérer le plugin (voir [Sources de plugin](#plugin-sources) ci-dessous)                                                                                                         |

### Champs de plugin optionnels

**Champs de métadonnées standard :**

| Champ         | Type    | Description                                                                                                                                   |
| :------------ | :------ | :-------------------------------------------------------------------------------------------------------------------------------------------- |
| `description` | string  | Brève description du plugin                                                                                                                   |
| `version`     | string  | Version du plugin                                                                                                                             |
| `author`      | object  | Informations sur l'auteur du plugin (`name` obligatoire, `email` optionnel)                                                                   |
| `homepage`    | string  | URL de la page d'accueil ou de la documentation du plugin                                                                                     |
| `repository`  | string  | URL du dépôt du code source                                                                                                                   |
| `license`     | string  | Identifiant de licence SPDX (par exemple, MIT, Apache-2.0)                                                                                    |
| `keywords`    | array   | Balises pour la découverte et la catégorisation des plugins                                                                                   |
| `category`    | string  | Catégorie du plugin pour l'organisation                                                                                                       |
| `tags`        | array   | Balises pour la recherche                                                                                                                     |
| `strict`      | boolean | Contrôle si `plugin.json` est l'autorité pour les définitions de composants (par défaut : true). Voir [Mode strict](#strict-mode) ci-dessous. |

**Champs de configuration des composants :**

| Champ        | Type           | Description                                                               |
| :----------- | :------------- | :------------------------------------------------------------------------ |
| `commands`   | string\|array  | Chemins personnalisés vers les fichiers ou répertoires de commandes       |
| `agents`     | string\|array  | Chemins personnalisés vers les fichiers d'agents                          |
| `hooks`      | string\|object | Configuration personnalisée des hooks ou chemin vers le fichier des hooks |
| `mcpServers` | string\|object | Configurations du serveur MCP ou chemin vers la configuration MCP         |
| `lspServers` | string\|object | Configurations du serveur LSP ou chemin vers la configuration LSP         |

## Sources de plugin

Les sources de plugin indiquent à Claude Code où récupérer chaque plugin individuel répertorié dans votre place de marché. Elles sont définies dans le champ `source` de chaque entrée de plugin dans `marketplace.json`.

Une fois qu'un plugin est cloné ou copié sur la machine locale, il est copié dans le cache de plugin local versionné à `~/.claude/plugins/cache`.

| Source         | Type                                   | Champs                                            | Notes                                                                                                       |
| -------------- | -------------------------------------- | ------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| Chemin relatif | `string` (par exemple `"./my-plugin"`) | —                                                 | Répertoire local dans le dépôt de la place de marché. Doit commencer par `./`                               |
| `github`       | object                                 | `repo`, `ref?`, `sha?`                            |                                                                                                             |
| `url`          | object                                 | `url` (doit se terminer par .git), `ref?`, `sha?` | Source d'URL Git                                                                                            |
| `git-subdir`   | object                                 | `url`, `path`, `ref?`, `sha?`                     | Sous-répertoire dans un dépôt git. Clone partiellement pour minimiser la bande passante pour les monodépôts |
| `npm`          | object                                 | `package`, `version?`, `registry?`                | Installé via `npm install`                                                                                  |
| `pip`          | object                                 | `package`, `version?`, `registry?`                | Installé via pip                                                                                            |

<Note>
  **Sources de place de marché vs sources de plugin** : Ce sont des concepts différents qui contrôlent des choses différentes.

  * **Source de place de marché** — où récupérer le catalogue `marketplace.json` lui-même. Défini lorsque les utilisateurs exécutent `/plugin marketplace add` ou dans les paramètres `extraKnownMarketplaces`. Prend en charge `ref` (branche/tag) mais pas `sha`.
  * **Source de plugin** — où récupérer un plugin individuel répertorié dans la place de marché. Défini dans le champ `source` de chaque entrée de plugin dans `marketplace.json`. Prend en charge à la fois `ref` (branche/tag) et `sha` (commit exact).

  Par exemple, une place de marché hébergée à `acme-corp/plugin-catalog` (source de place de marché) peut répertorier un plugin récupéré à partir de `acme-corp/code-formatter` (source de plugin). La source de place de marché et la source de plugin pointent vers des dépôts différents et sont épinglées indépendamment.
</Note>

### Chemins relatifs

Pour les plugins dans le même dépôt, utilisez un chemin commençant par `./` :

```json  theme={null}
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

Les chemins se résolvent par rapport à la racine de la place de marché, qui est le répertoire contenant `.claude-plugin/`. Dans l'exemple ci-dessus, `./plugins/my-plugin` pointe vers `<repo>/plugins/my-plugin`, même si `marketplace.json` se trouve à `<repo>/.claude-plugin/marketplace.json`. N'utilisez pas `../` pour sortir de `.claude-plugin/`.

<Note>
  Les chemins relatifs ne fonctionnent que lorsque les utilisateurs ajoutent votre place de marché via Git (GitHub, GitLab ou URL git). Si les utilisateurs ajoutent votre place de marché via une URL directe vers le fichier `marketplace.json`, les chemins relatifs ne se résoudront pas correctement. Pour la distribution basée sur les URL, utilisez plutôt les sources GitHub, npm ou URL git. Consultez [Dépannage](#plugins-with-relative-paths-fail-in-url-based-marketplaces) pour plus de détails.
</Note>

### Dépôts GitHub

```json  theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

Vous pouvez épingler à une branche, un tag ou un commit spécifique :

```json  theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Champ  | Type   | Description                                                                              |
| :----- | :----- | :--------------------------------------------------------------------------------------- |
| `repo` | string | Obligatoire. Dépôt GitHub au format `owner/repo`                                         |
| `ref`  | string | Optionnel. Branche ou tag Git (par défaut la branche par défaut du dépôt)                |
| `sha`  | string | Optionnel. SHA de commit git complet de 40 caractères pour épingler à une version exacte |

### Dépôts Git

```json  theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

Vous pouvez épingler à une branche, un tag ou un commit spécifique :

```json  theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Champ | Type   | Description                                                                                                                                                              |
| :---- | :----- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url` | string | Obligatoire. URL complète du dépôt git (`https://` ou `git@`). Le suffixe `.git` est optionnel, donc les URL Azure DevOps et AWS CodeCommit sans le suffixe fonctionnent |
| `ref` | string | Optionnel. Branche ou tag Git (par défaut la branche par défaut du dépôt)                                                                                                |
| `sha` | string | Optionnel. SHA de commit git complet de 40 caractères pour épingler à une version exacte                                                                                 |

### Sous-répertoires Git

Utilisez `git-subdir` pour pointer vers un plugin qui se trouve dans un sous-répertoire d'un dépôt git. Claude Code utilise un clone partiel et clairsemé pour récupérer uniquement le sous-répertoire, minimisant la bande passante pour les grands monodépôts.

```json  theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin"
  }
}
```

Vous pouvez épingler à une branche, un tag ou un commit spécifique :

```json  theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

Le champ `url` accepte également un raccourci GitHub (`owner/repo`) ou des URL SSH (`git@github.com:owner/repo.git`).

| Champ  | Type   | Description                                                                                                     |
| :----- | :----- | :-------------------------------------------------------------------------------------------------------------- |
| `url`  | string | Obligatoire. URL du dépôt Git, raccourci GitHub `owner/repo` ou URL SSH                                         |
| `path` | string | Obligatoire. Chemin du sous-répertoire dans le dépôt contenant le plugin (par exemple, `"tools/claude-plugin"`) |
| `ref`  | string | Optionnel. Branche ou tag Git (par défaut la branche par défaut du dépôt)                                       |
| `sha`  | string | Optionnel. SHA de commit git complet de 40 caractères pour épingler à une version exacte                        |

### Paquets npm

Les plugins distribués en tant que paquets npm sont installés à l'aide de `npm install`. Cela fonctionne avec n'importe quel paquet du registre npm public ou d'un registre privé que votre équipe héberge.

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin"
  }
}
```

Pour épingler à une version spécifique, ajoutez le champ `version` :

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "2.1.0"
  }
}
```

Pour installer à partir d'un registre privé ou interne, ajoutez le champ `registry` :

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

| Champ      | Type   | Description                                                                                                 |
| :--------- | :----- | :---------------------------------------------------------------------------------------------------------- |
| `package`  | string | Obligatoire. Nom du paquet ou paquet scopé (par exemple, `@org/plugin`)                                     |
| `version`  | string | Optionnel. Version ou plage de version (par exemple, `2.1.0`, `^2.0.0`, `~1.5.0`)                           |
| `registry` | string | Optionnel. URL du registre npm personnalisé. Par défaut le registre npm du système (généralement npmjs.org) |

### Entrées de plugin avancées

Cet exemple montre une entrée de plugin utilisant de nombreux champs optionnels, notamment des chemins personnalisés pour les commandes, les agents, les hooks et les serveurs MCP :

```json  theme={null}
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Enterprise workflow automation tools",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "enterprise@example.com"
  },
  "homepage": "https://docs.example.com/plugins/enterprise-tools",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity",
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": ["./agents/security-reviewer.md", "./agents/compliance-checker.md"],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "enterprise-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  },
  "strict": false
}
```

Points clés à noter :

* **`commands` et `agents`** : Vous pouvez spécifier plusieurs répertoires ou fichiers individuels. Les chemins sont relatifs à la racine du plugin.
* **`${CLAUDE_PLUGIN_ROOT}`** : Utilisez cette variable dans les hooks et les configurations du serveur MCP pour référencer les fichiers dans le répertoire d'installation du plugin. C'est nécessaire car les plugins sont copiés vers un emplacement de cache lors de l'installation.
* **`strict: false`** : Puisque ceci est défini sur false, le plugin n'a pas besoin de son propre `plugin.json`. L'entrée de la place de marché définit tout. Voir [Mode strict](#strict-mode) ci-dessous.

### Mode strict

Le champ `strict` contrôle si `plugin.json` est l'autorité pour les définitions de composants (commandes, agents, hooks, compétences, serveurs MCP, styles de sortie).

| Valeur              | Comportement                                                                                                                                                                     |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `true` (par défaut) | `plugin.json` est l'autorité. L'entrée de la place de marché peut la compléter avec des composants supplémentaires, et les deux sources sont fusionnées.                         |
| `false`             | L'entrée de la place de marché est la définition complète. Si le plugin a également un `plugin.json` qui déclare des composants, c'est un conflit et le plugin ne se charge pas. |

**Quand utiliser chaque mode :**

* **`strict: true`** : le plugin a son propre `plugin.json` et gère ses propres composants. L'entrée de la place de marché peut ajouter des commandes ou des hooks supplémentaires par-dessus. C'est la valeur par défaut et fonctionne pour la plupart des plugins.
* **`strict: false`** : l'opérateur de la place de marché veut le contrôle total. Le dépôt du plugin fournit des fichiers bruts, et l'entrée de la place de marché définit lesquels de ces fichiers sont exposés en tant que commandes, agents, hooks, etc. Utile lorsque la place de marché restructure ou sélectionne les composants d'un plugin différemment de ce que l'auteur du plugin avait prévu.

## Héberger et distribuer les places de marché

### Héberger sur GitHub (recommandé)

GitHub offre la méthode de distribution la plus facile :

1. **Créer un dépôt** : Configurez un nouveau dépôt pour votre place de marché
2. **Ajouter le fichier de place de marché** : Créez `.claude-plugin/marketplace.json` avec vos définitions de plugins
3. **Partager avec les équipes** : Les utilisateurs ajoutent votre place de marché avec `/plugin marketplace add owner/repo`

**Avantages** : Contrôle de version intégré, suivi des problèmes et fonctionnalités de collaboration d'équipe.

### Héberger sur d'autres services git

N'importe quel service d'hébergement git fonctionne, comme GitLab, Bitbucket et les serveurs auto-hébergés. Les utilisateurs ajoutent avec l'URL complète du dépôt :

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### Dépôts privés

Claude Code prend en charge l'installation de plugins à partir de dépôts privés. Pour l'installation manuelle et les mises à jour, Claude Code utilise vos assistants de credentials git existants. Si `git clone` fonctionne pour un dépôt privé dans votre terminal, cela fonctionne aussi dans Claude Code. Les assistants de credentials courants incluent `gh auth login` pour GitHub, Keychain macOS et `git-credential-store`.

Les mises à jour automatiques en arrière-plan s'exécutent au démarrage sans assistants de credentials, car les invites interactives bloqueraient le démarrage de Claude Code. Pour activer les mises à jour automatiques pour les places de marché privées, définissez le jeton d'authentification approprié dans votre environnement :

| Fournisseur | Variables d'environnement    | Notes                                                |
| :---------- | :--------------------------- | :--------------------------------------------------- |
| GitHub      | `GITHUB_TOKEN` ou `GH_TOKEN` | Jeton d'accès personnel ou jeton GitHub App          |
| GitLab      | `GITLAB_TOKEN` ou `GL_TOKEN` | Jeton d'accès personnel ou jeton de projet           |
| Bitbucket   | `BITBUCKET_TOKEN`            | Mot de passe d'application ou jeton d'accès au dépôt |

Définissez le jeton dans votre configuration de shell (par exemple, `.bashrc`, `.zshrc`) ou passez-le lors de l'exécution de Claude Code :

```bash  theme={null}
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

<Note>
  Pour les environnements CI/CD, configurez le jeton en tant que variable d'environnement secrète. GitHub Actions fournit automatiquement `GITHUB_TOKEN` pour les dépôts de la même organisation.
</Note>

### Tester localement avant la distribution

Testez votre place de marché localement avant de la partager :

```shell  theme={null}
/plugin marketplace add ./my-local-marketplace
/plugin install test-plugin@my-local-marketplace
```

Pour la gamme complète de commandes add (GitHub, URL Git, chemins locaux, URL distantes), consultez [Ajouter des places de marché](/fr/discover-plugins#add-marketplaces).

### Exiger des places de marché pour votre équipe

Vous pouvez configurer votre dépôt pour que les membres de l'équipe soient automatiquement invités à installer votre place de marché lorsqu'ils font confiance au dossier du projet. Ajoutez votre place de marché à `.claude/settings.json` :

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

Vous pouvez également spécifier quels plugins doivent être activés par défaut :

```json  theme={null}
{
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

Pour les options de configuration complètes, consultez [Paramètres des plugins](/fr/settings#plugin-settings).

### Restrictions des places de marché gérées

Pour les organisations nécessitant un contrôle strict sur les sources de plugins, les administrateurs peuvent restreindre les places de marché de plugins que les utilisateurs sont autorisés à ajouter en utilisant le paramètre [`strictKnownMarketplaces`](/fr/settings#strictknownmarketplaces) dans les paramètres gérés.

Lorsque `strictKnownMarketplaces` est configuré dans les paramètres gérés, le comportement de restriction dépend de la valeur :

| Valeur                  | Comportement                                                                                                        |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------- |
| Non défini (par défaut) | Aucune restriction. Les utilisateurs peuvent ajouter n'importe quelle place de marché                               |
| Tableau vide `[]`       | Verrouillage complet. Les utilisateurs ne peuvent pas ajouter de nouvelles places de marché                         |
| Liste de sources        | Les utilisateurs ne peuvent ajouter que les places de marché qui correspondent exactement à la liste d'autorisation |

#### Configurations courantes

Désactiver tous les ajouts de place de marché :

```json  theme={null}
{
  "strictKnownMarketplaces": []
}
```

Autoriser uniquement les places de marché spécifiques :

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    }
  ]
}
```

Autoriser toutes les places de marché d'un serveur git interne en utilisant la correspondance de motif regex sur l'hôte :

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

Autoriser les places de marché basées sur le système de fichiers à partir d'un répertoire spécifique en utilisant la correspondance de motif regex sur le chemin :

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "pathPattern",
      "pathPattern": "^/opt/approved/"
    }
  ]
}
```

Utilisez `".*"` comme `pathPattern` pour autoriser n'importe quel chemin du système de fichiers tout en contrôlant les sources réseau avec `hostPattern`.

<Note>
  `strictKnownMarketplaces` restreint ce que les utilisateurs peuvent ajouter, mais n'enregistre pas les places de marché par lui-même. Pour rendre les places de marché autorisées disponibles automatiquement sans que les utilisateurs exécutent `/plugin marketplace add`, associez-le à [`extraKnownMarketplaces`](/fr/settings#extraknownmarketplaces) dans le même `managed-settings.json`. Voir [Utiliser les deux ensemble](/fr/settings#strictknownmarketplaces).
</Note>

#### Comment fonctionnent les restrictions

Les restrictions sont validées tôt dans le processus d'installation du plugin, avant toute demande réseau ou opération du système de fichiers. Cela empêche les tentatives d'accès non autorisé à la place de marché.

La liste d'autorisation utilise la correspondance exacte pour la plupart des types de sources. Pour qu'une place de marché soit autorisée, tous les champs spécifiés doivent correspondre exactement :

* Pour les sources GitHub : `repo` est obligatoire, et `ref` ou `path` doivent également correspondre s'ils sont spécifiés dans la liste d'autorisation
* Pour les sources URL : l'URL complète doit correspondre exactement
* Pour les sources `hostPattern` : l'hôte de la place de marché est comparé au motif regex
* Pour les sources `pathPattern` : le chemin du système de fichiers de la place de marché est comparé au motif regex

Parce que `strictKnownMarketplaces` est défini dans les [paramètres gérés](/fr/settings#settings-files), les configurations individuelles des utilisateurs et des projets ne peuvent pas contourner ces restrictions.

Pour les détails de configuration complets, y compris tous les types de sources pris en charge et la comparaison avec `extraKnownMarketplaces`, consultez la [référence strictKnownMarketplaces](/fr/settings#strictknownmarketplaces).

### Résolution des versions et canaux de publication

Les versions des plugins déterminent les chemins du cache et la détection des mises à jour. Vous pouvez spécifier la version dans le manifeste du plugin (`plugin.json`) ou dans l'entrée de la place de marché (`marketplace.json`).

<Warning>
  Lorsque c'est possible, évitez de définir la version aux deux endroits. Le manifeste du plugin gagne toujours silencieusement, ce qui peut faire que la version de la place de marché soit ignorée. Pour les plugins avec chemins relatifs, définissez la version dans l'entrée de la place de marché. Pour toutes les autres sources de plugins, définissez-la dans le manifeste du plugin.
</Warning>

#### Configurer les canaux de publication

Pour prendre en charge les canaux de publication « stable » et « latest » pour vos plugins, vous pouvez configurer deux places de marché qui pointent vers différentes refs ou SHAs du même dépôt. Vous pouvez ensuite assigner les deux places de marché à différents groupes d'utilisateurs via les [paramètres gérés](/fr/settings#settings-files).

<Warning>
  Le `plugin.json` du plugin doit déclarer une `version` différente à chaque ref ou commit épinglé. Si deux refs ou commits ont la même version de manifeste, Claude Code les traite comme identiques et ignore la mise à jour.
</Warning>

##### Exemple

```json  theme={null}
{
  "name": "stable-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "stable"
      }
    }
  ]
}
```

```json  theme={null}
{
  "name": "latest-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "latest"
      }
    }
  ]
}
```

##### Assigner les canaux aux groupes d'utilisateurs

Assignez chaque place de marché au groupe d'utilisateurs approprié via les paramètres gérés. Par exemple, le groupe stable reçoit :

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "stable-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/stable-tools"
      }
    }
  }
}
```

Le groupe early-access reçoit `latest-tools` à la place :

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "latest-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/latest-tools"
      }
    }
  }
}
```

## Validation et test

Testez votre place de marché avant de la partager.

Validez la syntaxe JSON de votre place de marché :

```bash  theme={null}
claude plugin validate .
```

Ou depuis Claude Code :

```shell  theme={null}
/plugin validate .
```

Ajoutez la place de marché pour le test :

```shell  theme={null}
/plugin marketplace add ./path/to/marketplace
```

Installez un plugin de test pour vérifier que tout fonctionne :

```shell  theme={null}
/plugin install test-plugin@marketplace-name
```

Pour les flux de travail complets de test de plugins, consultez [Tester vos plugins localement](/fr/plugins#test-your-plugins-locally). Pour le dépannage technique, consultez [Référence des plugins](/fr/plugins-reference).

## Dépannage

### La place de marché ne se charge pas

**Symptômes** : Impossible d'ajouter la place de marché ou de voir les plugins qu'elle contient

**Solutions** :

* Vérifiez que l'URL de la place de marché est accessible
* Vérifiez que `.claude-plugin/marketplace.json` existe au chemin spécifié
* Assurez-vous que la syntaxe JSON est valide en utilisant `claude plugin validate` ou `/plugin validate`
* Pour les dépôts privés, confirmez que vous avez les permissions d'accès

### Erreurs de validation de la place de marché

Exécutez `claude plugin validate .` ou `/plugin validate .` à partir de votre répertoire de place de marché pour vérifier les problèmes. Erreurs courantes :

| Erreur                                            | Cause                              | Solution                                                                                 |
| :------------------------------------------------ | :--------------------------------- | :--------------------------------------------------------------------------------------- |
| `File not found: .claude-plugin/marketplace.json` | Manifeste manquant                 | Créez `.claude-plugin/marketplace.json` avec les champs obligatoires                     |
| `Invalid JSON syntax: Unexpected token...`        | Erreur de syntaxe JSON             | Vérifiez les virgules manquantes, les virgules supplémentaires ou les chaînes non citées |
| `Duplicate plugin name "x" found in marketplace`  | Deux plugins partagent le même nom | Donnez à chaque plugin une valeur `name` unique                                          |
| `plugins[0].source: Path traversal not allowed`   | Le chemin source contient `..`     | Utilisez des chemins relatifs à la racine de la place de marché sans `..`                |

**Avertissements** (non bloquants) :

* `Marketplace has no plugins defined` : ajoutez au moins un plugin au tableau `plugins`
* `No marketplace description provided` : ajoutez `metadata.description` pour aider les utilisateurs à comprendre votre place de marché

### Échecs d'installation de plugins

**Symptômes** : La place de marché apparaît mais l'installation du plugin échoue

**Solutions** :

* Vérifiez que les URL sources des plugins sont accessibles
* Vérifiez que les répertoires des plugins contiennent les fichiers requis
* Pour les sources GitHub, assurez-vous que les dépôts sont publics ou que vous avez accès
* Testez manuellement les sources de plugins en les clonant/téléchargeant

### L'authentification du dépôt privé échoue

**Symptômes** : Erreurs d'authentification lors de l'installation de plugins à partir de dépôts privés

**Solutions** :

Pour l'installation manuelle et les mises à jour :

* Vérifiez que vous êtes authentifié auprès de votre fournisseur git (par exemple, exécutez `gh auth status` pour GitHub)
* Vérifiez que votre assistant de credentials est configuré correctement : `git config --global credential.helper`
* Essayez de cloner le dépôt manuellement pour vérifier que vos credentials fonctionnent

Pour les mises à jour automatiques en arrière-plan :

* Définissez le jeton approprié dans votre environnement : `echo $GITHUB_TOKEN`
* Vérifiez que le jeton a les permissions requises (accès en lecture au dépôt)
* Pour GitHub, assurez-vous que le jeton a la portée `repo` pour les dépôts privés
* Pour GitLab, assurez-vous que le jeton a au moins la portée `read_repository`
* Vérifiez que le jeton n'a pas expiré

### Les opérations Git expirent

**Symptômes** : L'installation du plugin ou les mises à jour de la place de marché échouent avec une erreur de délai d'expiration comme « Git clone timed out after 120s » ou « Git pull timed out after 120s ».

**Cause** : Claude Code utilise un délai d'expiration de 120 secondes pour toutes les opérations git, y compris le clonage des dépôts de plugins et l'extraction des mises à jour de la place de marché. Les grands dépôts ou les connexions réseau lentes peuvent dépasser cette limite.

**Solution** : Augmentez le délai d'expiration en utilisant la variable d'environnement `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`. La valeur est en millisecondes :

```bash  theme={null}
export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000  # 5 minutes
```

### Les plugins avec chemins relatifs échouent dans les places de marché basées sur les URL

**Symptômes** : Vous avez ajouté une place de marché via URL (comme `https://example.com/marketplace.json`), mais les plugins avec des sources de chemin relatif comme `"./plugins/my-plugin"` échouent à installer avec des erreurs « path not found ».

**Cause** : Les places de marché basées sur les URL téléchargent uniquement le fichier `marketplace.json` lui-même. Elles ne téléchargent pas les fichiers de plugins du serveur. Les chemins relatifs dans l'entrée de la place de marché référencent des fichiers sur le serveur distant qui n'ont pas été téléchargés.

**Solutions** :

* **Utiliser des sources externes** : Changez les entrées de plugins pour utiliser les sources GitHub, npm ou URL git au lieu des chemins relatifs :
  ```json  theme={null}
  { "name": "my-plugin", "source": { "source": "github", "repo": "owner/repo" } }
  ```
* **Utiliser une place de marché basée sur Git** : Hébergez votre place de marché dans un dépôt Git et ajoutez-la avec l'URL git. Les places de marché basées sur Git clonent le dépôt entier, ce qui rend les chemins relatifs fonctionnels.

### Fichiers non trouvés après l'installation

**Symptômes** : Le plugin s'installe mais les références aux fichiers échouent, en particulier les fichiers en dehors du répertoire du plugin

**Cause** : Les plugins sont copiés vers un répertoire de cache plutôt que d'être utilisés sur place. Les chemins qui référencent des fichiers en dehors du répertoire du plugin (comme `../shared-utils`) ne fonctionneront pas car ces fichiers ne sont pas copiés.

**Solutions** : Consultez [Plugin caching and file resolution](/fr/plugins-reference#plugin-caching-and-file-resolution) pour les solutions de contournement, y compris les symlinks et la restructuration des répertoires.

Pour des outils de débogage supplémentaires et des problèmes courants, consultez [Debugging and development tools](/fr/plugins-reference#debugging-and-development-tools).

## Voir aussi

* [Découvrir et installer des plugins préconfigurés](/fr/discover-plugins) - Installation de plugins à partir de places de marché existantes
* [Plugins](/fr/plugins) - Création de vos propres plugins
* [Référence des plugins](/fr/plugins-reference) - Spécifications techniques complètes et schémas
* [Paramètres des plugins](/fr/settings#plugin-settings) - Options de configuration des plugins
* [Référence strictKnownMarketplaces](/fr/settings#strictknownmarketplaces) - Restrictions des places de marché gérées
