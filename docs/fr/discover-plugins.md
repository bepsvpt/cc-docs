> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Découvrir et installer des plugins prédéfinis via les marketplaces

> Trouvez et installez des plugins depuis les marketplaces pour étendre Claude Code avec de nouvelles commandes, agents et capacités.

Les plugins étendent Claude Code avec des skills, des agents, des hooks et des MCP servers. Les marketplaces de plugins sont des catalogues qui vous aident à découvrir et installer ces extensions sans les construire vous-même.

Vous cherchez à créer et distribuer votre propre marketplace ? Consultez [Créer et distribuer une marketplace de plugins](/fr/plugin-marketplaces).

## Comment fonctionnent les marketplaces

Une marketplace est un catalogue de plugins que quelqu'un d'autre a créé et partagé. L'utilisation d'une marketplace est un processus en deux étapes :

<Steps>
  <Step title="Ajouter la marketplace">
    Cela enregistre le catalogue avec Claude Code pour que vous puissiez parcourir ce qui est disponible. Aucun plugin n'est installé pour le moment.
  </Step>

  <Step title="Installer des plugins individuels">
    Parcourez le catalogue et installez les plugins que vous souhaitez.
  </Step>
</Steps>

Pensez-y comme ajouter un app store : ajouter le store vous donne accès pour parcourir sa collection, mais vous choisissez toujours quelles applications télécharger individuellement.

## Marketplace officielle Anthropic

La marketplace officielle Anthropic (`claude-plugins-official`) est automatiquement disponible quand vous démarrez Claude Code. Exécutez `/plugin` et allez à l'onglet **Discover** pour parcourir ce qui est disponible, ou consultez le catalogue sur [claude.com/plugins](https://claude.com/plugins).

Pour installer un plugin depuis la marketplace officielle, utilisez `/plugin install <name>@claude-plugins-official`. Par exemple, pour installer l'intégration GitHub :

```shell theme={null}
/plugin install github@claude-plugins-official
```

<Note>
  La marketplace officielle est maintenue par Anthropic. Pour soumettre un plugin à la marketplace officielle, utilisez l'un des formulaires de soumission intégrés à l'application :

  * **Claude.ai** : [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
  * **Console** : [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

  Pour distribuer des plugins indépendamment, [créez votre propre marketplace](/fr/plugin-marketplaces) et partagez-la avec les utilisateurs.
</Note>

La marketplace officielle inclut plusieurs catégories de plugins :

### Code intelligence

Les plugins de code intelligence activent l'outil LSP intégré de Claude Code, donnant à Claude la capacité de sauter aux définitions, trouver les références et voir les erreurs de type immédiatement après les modifications. Ces plugins configurent les connexions [Language Server Protocol](https://microsoft.github.io/language-server-protocol/), la même technologie qui alimente la code intelligence de VS Code.

Ces plugins nécessitent que le binaire du serveur de langage soit installé sur votre système. Si vous avez déjà un serveur de langage installé, Claude peut vous inviter à installer le plugin correspondant quand vous ouvrez un projet.

| Langage    | Plugin              | Binaire requis               |
| :--------- | :------------------ | :--------------------------- |
| C/C++      | `clangd-lsp`        | `clangd`                     |
| C#         | `csharp-lsp`        | `csharp-ls`                  |
| Go         | `gopls-lsp`         | `gopls`                      |
| Java       | `jdtls-lsp`         | `jdtls`                      |
| Kotlin     | `kotlin-lsp`        | `kotlin-language-server`     |
| Lua        | `lua-lsp`           | `lua-language-server`        |
| PHP        | `php-lsp`           | `intelephense`               |
| Python     | `pyright-lsp`       | `pyright-langserver`         |
| Rust       | `rust-analyzer-lsp` | `rust-analyzer`              |
| Swift      | `swift-lsp`         | `sourcekit-lsp`              |
| TypeScript | `typescript-lsp`    | `typescript-language-server` |

Vous pouvez également [créer votre propre plugin LSP](/fr/plugins-reference#lsp-servers) pour d'autres langages.

<Note>
  Si vous voyez `Executable not found in $PATH` dans l'onglet `/plugin` Errors après avoir installé un plugin, installez le binaire requis du tableau ci-dessus.
</Note>

#### Ce que Claude gagne des plugins de code intelligence

Une fois qu'un plugin de code intelligence est installé et que son binaire de serveur de langage est disponible, Claude gagne deux capacités :

* **Diagnostics automatiques** : après chaque modification de fichier que Claude effectue, le serveur de langage analyse les modifications et signale les erreurs et avertissements automatiquement. Claude voit les erreurs de type, les imports manquants et les problèmes de syntaxe sans avoir besoin d'exécuter un compilateur ou un linter. Si Claude introduit une erreur, il la remarque et la corrige dans le même tour. Cela ne nécessite aucune configuration au-delà de l'installation du plugin. Vous pouvez voir les diagnostics en ligne en appuyant sur **Ctrl+O** quand l'indicateur « diagnostics found » apparaît.
* **Navigation de code** : Claude peut utiliser le serveur de langage pour sauter aux définitions, trouver les références, obtenir les informations de type au survol, lister les symboles, trouver les implémentations et tracer les hiérarchies d'appels. Ces opérations donnent à Claude une navigation plus précise que la recherche basée sur grep, bien que la disponibilité puisse varier selon le langage et l'environnement.

Si vous rencontrez des problèmes, consultez [Dépannage de la code intelligence](#code-intelligence-issues).

### Intégrations externes

Ces plugins regroupent des [MCP servers](/fr/mcp) préconfigurés pour que vous puissiez connecter Claude à des services externes sans configuration manuelle :

* **Contrôle de source** : `github`, `gitlab`
* **Gestion de projet** : `atlassian` (Jira/Confluence), `asana`, `linear`, `notion`
* **Design** : `figma`
* **Infrastructure** : `vercel`, `firebase`, `supabase`
* **Communication** : `slack`
* **Monitoring** : `sentry`

### Workflows de développement

Plugins qui ajoutent des commandes et des agents pour les tâches de développement courantes :

* **commit-commands** : Workflows de commit Git incluant commit, push et création de PR
* **pr-review-toolkit** : Agents spécialisés pour examiner les pull requests
* **agent-sdk-dev** : Outils pour construire avec le Claude Agent SDK
* **plugin-dev** : Toolkit pour créer vos propres plugins

### Styles de sortie

Personnalisez comment Claude répond :

* **explanatory-output-style** : Insights éducatifs sur les choix d'implémentation
* **learning-output-style** : Mode d'apprentissage interactif pour la construction de compétences

## Essayez : ajouter la marketplace de démonstration

Anthropic maintient également une [marketplace de plugins de démonstration](https://github.com/anthropics/claude-code/tree/main/plugins) (`claude-code-plugins`) avec des plugins d'exemple qui montrent ce qui est possible avec le système de plugins. Contrairement à la marketplace officielle, vous devez ajouter celle-ci manuellement.

<Steps>
  <Step title="Ajouter la marketplace">
    Depuis Claude Code, exécutez la commande `plugin marketplace add` pour la marketplace `anthropics/claude-code` :

    ```shell theme={null}
    /plugin marketplace add anthropics/claude-code
    ```

    Cela télécharge le catalogue de la marketplace et rend ses plugins disponibles pour vous.
  </Step>

  <Step title="Parcourir les plugins disponibles">
    Exécutez `/plugin` pour ouvrir le gestionnaire de plugins. Cela ouvre une interface à onglets avec quatre onglets que vous pouvez parcourir en utilisant **Tab** (ou **Shift+Tab** pour aller en arrière) :

    * **Discover** : parcourez les plugins disponibles de toutes vos marketplaces
    * **Installed** : visualisez et gérez vos plugins installés
    * **Marketplaces** : ajoutez, supprimez ou mettez à jour vos marketplaces ajoutées
    * **Errors** : visualisez les erreurs de chargement de plugins

    Allez à l'onglet **Discover** pour voir les plugins de la marketplace que vous venez d'ajouter.
  </Step>

  <Step title="Installer un plugin">
    Sélectionnez un plugin pour voir ses détails, puis choisissez une portée d'installation :

    * **User scope** : installez pour vous-même dans tous les projets
    * **Project scope** : installez pour tous les collaborateurs sur ce référentiel
    * **Local scope** : installez pour vous-même dans ce référentiel uniquement

    Par exemple, sélectionnez **commit-commands** (un plugin qui ajoute des commandes de workflow git) et installez-le à votre portée utilisateur.

    Vous pouvez également installer directement depuis la ligne de commande :

    ```shell theme={null}
    /plugin install commit-commands@anthropics-claude-code
    ```

    Consultez [Configuration scopes](/fr/settings#configuration-scopes) pour en savoir plus sur les portées.
  </Step>

  <Step title="Utiliser votre nouveau plugin">
    Après l'installation, exécutez `/reload-plugins` pour activer le plugin. Les commandes de plugin sont espacées par le nom du plugin, donc **commit-commands** fournit des commandes comme `/commit-commands:commit`.

    Essayez en effectuant une modification à un fichier et en exécutant :

    ```shell theme={null}
    /commit-commands:commit
    ```

    Cela prépare vos modifications, génère un message de commit et crée le commit.

    Chaque plugin fonctionne différemment. Consultez la description du plugin dans l'onglet **Discover** ou sa page d'accueil pour apprendre quelles commandes et capacités il fournit.
  </Step>
</Steps>

Le reste de ce guide couvre tous les moyens d'ajouter des marketplaces, installer des plugins et gérer votre configuration.

## Ajouter des marketplaces

Utilisez la commande `/plugin marketplace add` pour ajouter des marketplaces de différentes sources.

<Tip>
  **Raccourcis** : Vous pouvez utiliser `/plugin market` au lieu de `/plugin marketplace`, et `rm` au lieu de `remove`.
</Tip>

* **Référentiels GitHub** : format `owner/repo` (par exemple, `anthropics/claude-code`)
* **URLs Git** : n'importe quelle URL de référentiel git (GitLab, Bitbucket, auto-hébergé)
* **Chemins locaux** : répertoires ou chemins directs vers les fichiers `marketplace.json`
* **URLs distantes** : URLs directs vers les fichiers `marketplace.json` hébergés

### Ajouter depuis GitHub

Ajoutez un référentiel GitHub qui contient un fichier `.claude-plugin/marketplace.json` en utilisant le format `owner/repo`—où `owner` est le nom d'utilisateur ou l'organisation GitHub et `repo` est le nom du référentiel.

Par exemple, `anthropics/claude-code` fait référence au référentiel `claude-code` appartenant à `anthropics` :

```shell theme={null}
/plugin marketplace add anthropics/claude-code
```

### Ajouter depuis d'autres hôtes Git

Ajoutez n'importe quel référentiel git en fournissant l'URL complète. Cela fonctionne avec n'importe quel hôte Git, y compris GitLab, Bitbucket et les serveurs auto-hébergés :

Utilisation de HTTPS :

```shell theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

Utilisation de SSH :

```shell theme={null}
/plugin marketplace add git@gitlab.com:company/plugins.git
```

Pour ajouter une branche ou un tag spécifique, ajoutez `#` suivi de la ref :

```shell theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

### Ajouter depuis des chemins locaux

Ajoutez un répertoire local qui contient un fichier `.claude-plugin/marketplace.json` :

```shell theme={null}
/plugin marketplace add ./my-marketplace
```

Vous pouvez également ajouter un chemin direct vers un fichier `marketplace.json` :

```shell theme={null}
/plugin marketplace add ./path/to/marketplace.json
```

### Ajouter depuis des URLs distantes

Ajoutez un fichier `marketplace.json` distant via URL :

```shell theme={null}
/plugin marketplace add https://example.com/marketplace.json
```

<Note>
  Les marketplaces basées sur URL ont certaines limitations par rapport aux marketplaces basées sur Git. Si vous rencontrez des erreurs « path not found » lors de l'installation de plugins, consultez [Dépannage](/fr/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces).
</Note>

## Installer des plugins

Une fois que vous avez ajouté des marketplaces, vous pouvez installer des plugins directement (installe à la portée utilisateur par défaut) :

```shell theme={null}
/plugin install plugin-name@marketplace-name
```

Pour choisir une [portée d'installation](/fr/settings#configuration-scopes) différente, utilisez l'interface interactive : exécutez `/plugin`, allez à l'onglet **Discover** et appuyez sur **Enter** sur un plugin. Vous verrez les options pour :

* **User scope** (par défaut) : installez pour vous-même dans tous les projets
* **Project scope** : installez pour tous les collaborateurs sur ce référentiel (ajoute à `.claude/settings.json`)
* **Local scope** : installez pour vous-même dans ce référentiel uniquement (non partagé avec les collaborateurs)

Vous pouvez également voir des plugins avec la portée **managed**—ceux-ci sont installés par les administrateurs via [managed settings](/fr/settings#settings-files) et ne peuvent pas être modifiés.

Exécutez `/plugin` et allez à l'onglet **Installed** pour voir vos plugins groupés par portée.

<Warning>
  Assurez-vous de faire confiance à un plugin avant de l'installer. Anthropic ne contrôle pas quels MCP servers, fichiers ou autres logiciels sont inclus dans les plugins et ne peut pas vérifier qu'ils fonctionnent comme prévu. Consultez la page d'accueil de chaque plugin pour plus d'informations.
</Warning>

## Gérer les plugins installés

Exécutez `/plugin` et allez à l'onglet **Installed** pour visualiser, activer, désactiver ou désinstaller vos plugins. Tapez pour filtrer la liste par nom ou description du plugin.

Vous pouvez également gérer les plugins avec des commandes directes.

Désactiver un plugin sans le désinstaller :

```shell theme={null}
/plugin disable plugin-name@marketplace-name
```

Réactiver un plugin désactivé :

```shell theme={null}
/plugin enable plugin-name@marketplace-name
```

Supprimer complètement un plugin :

```shell theme={null}
/plugin uninstall plugin-name@marketplace-name
```

L'option `--scope` vous permet de cibler une portée spécifique avec les commandes CLI :

```shell theme={null}
claude plugin install formatter@your-org --scope project
claude plugin uninstall formatter@your-org --scope project
```

### Appliquer les modifications de plugin sans redémarrer

Quand vous installez, activez ou désactivez des plugins pendant une session, exécutez `/reload-plugins` pour récupérer toutes les modifications sans redémarrer :

```shell theme={null}
/reload-plugins
```

Claude Code recharge tous les plugins actifs et affiche les comptages pour les plugins, les skills, les agents, les hooks, les MCP servers de plugin et les serveurs LSP de plugin.

## Gérer les marketplaces

Vous pouvez gérer les marketplaces via l'interface interactive `/plugin` ou avec des commandes CLI.

### Utiliser l'interface interactive

Exécutez `/plugin` et allez à l'onglet **Marketplaces** pour :

* Visualiser toutes vos marketplaces ajoutées avec leurs sources et statut
* Ajouter de nouvelles marketplaces
* Mettre à jour les listes de marketplace pour récupérer les derniers plugins
* Supprimer les marketplaces dont vous n'avez plus besoin

### Utiliser les commandes CLI

Vous pouvez également gérer les marketplaces avec des commandes directes.

Lister toutes les marketplaces configurées :

```shell theme={null}
/plugin marketplace list
```

Actualiser les listes de plugins d'une marketplace :

```shell theme={null}
/plugin marketplace update marketplace-name
```

Supprimer une marketplace :

```shell theme={null}
/plugin marketplace remove marketplace-name
```

<Warning>
  La suppression d'une marketplace désinstallera tous les plugins que vous avez installés à partir de celle-ci.
</Warning>

### Configurer les mises à jour automatiques

Claude Code peut automatiquement mettre à jour les marketplaces et leurs plugins installés au démarrage. Quand la mise à jour automatique est activée pour une marketplace, Claude Code actualise les données de la marketplace et met à jour les plugins installés vers leurs dernières versions. Si des plugins ont été mis à jour, vous verrez une notification vous invitant à exécuter `/reload-plugins`.

Basculez la mise à jour automatique pour les marketplaces individuelles via l'interface utilisateur :

1. Exécutez `/plugin` pour ouvrir le gestionnaire de plugins
2. Sélectionnez **Marketplaces**
3. Choisissez une marketplace dans la liste
4. Sélectionnez **Enable auto-update** ou **Disable auto-update**

Les marketplaces officielles Anthropic ont la mise à jour automatique activée par défaut. Les marketplaces tierces et de développement local ont la mise à jour automatique désactivée par défaut.

Pour désactiver complètement toutes les mises à jour automatiques pour Claude Code et tous les plugins, définissez la variable d'environnement `DISABLE_AUTOUPDATER`. Consultez [Auto updates](/fr/setup#auto-updates) pour plus de détails.

Pour garder les mises à jour automatiques des plugins activées tout en désactivant les mises à jour automatiques de Claude Code, définissez `FORCE_AUTOUPDATE_PLUGINS=1` avec `DISABLE_AUTOUPDATER` :

```bash theme={null}
export DISABLE_AUTOUPDATER=1
export FORCE_AUTOUPDATE_PLUGINS=1
```

Cela est utile quand vous voulez gérer les mises à jour de Claude Code manuellement mais recevoir toujours les mises à jour automatiques des plugins.

## Configurer les marketplaces d'équipe

Les administrateurs d'équipe peuvent configurer l'installation automatique de marketplace pour les projets en ajoutant la configuration de marketplace à `.claude/settings.json`. Quand les membres de l'équipe font confiance au dossier du référentiel, Claude Code les invite à installer ces marketplaces et plugins.

Ajoutez `extraKnownMarketplaces` au `.claude/settings.json` de votre projet :

```json theme={null}
{
  "extraKnownMarketplaces": {
    "my-team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

Pour les options de configuration complètes incluant `extraKnownMarketplaces` et `enabledPlugins`, consultez [Plugin settings](/fr/settings#plugin-settings).

## Sécurité

Les plugins et les marketplaces sont des composants hautement fiables qui peuvent exécuter du code arbitraire sur votre machine avec vos privilèges utilisateur. Installez uniquement les plugins et ajoutez les marketplaces à partir de sources auxquelles vous faites confiance. Les organisations peuvent restreindre quelles marketplaces les utilisateurs sont autorisés à ajouter en utilisant [managed marketplace restrictions](/fr/plugin-marketplaces#managed-marketplace-restrictions).

## Dépannage

### Commande /plugin non reconnue

Si vous voyez « unknown command » ou la commande `/plugin` n'apparaît pas :

1. **Vérifiez votre version** : Exécutez `claude --version` pour voir ce qui est installé.
2. **Mettez à jour Claude Code** :
   * **Homebrew** : `brew upgrade claude-code`
   * **npm** : `npm update -g @anthropic-ai/claude-code`
   * **Native installer** : Réexécutez la commande d'installation depuis [Setup](/fr/setup)
3. **Redémarrez Claude Code** : Après la mise à jour, redémarrez votre terminal et exécutez `claude` à nouveau.

### Problèmes courants

* **Marketplace ne se charge pas** : Vérifiez que l'URL est accessible et que `.claude-plugin/marketplace.json` existe au chemin
* **Échecs d'installation de plugin** : Vérifiez que les URLs sources du plugin sont accessibles et que les référentiels sont publics (ou vous avez accès)
* **Fichiers non trouvés après l'installation** : Les plugins sont copiés dans un cache, donc les chemins référençant des fichiers en dehors du répertoire du plugin ne fonctionneront pas
* **Les skills du plugin n'apparaissent pas** : Effacez le cache avec `rm -rf ~/.claude/plugins/cache`, redémarrez Claude Code et réinstallez le plugin.

Pour un dépannage détaillé avec des solutions, consultez [Dépannage](/fr/plugin-marketplaces#troubleshooting) dans le guide de la marketplace. Pour les outils de débogage, consultez [Debugging and development tools](/fr/plugins-reference#debugging-and-development-tools).

### Problèmes de code intelligence

* **Le serveur de langage ne démarre pas** : vérifiez que le binaire est installé et disponible dans votre `$PATH`. Consultez l'onglet `/plugin` Errors pour plus de détails.
* **Utilisation élevée de la mémoire** : les serveurs de langage comme `rust-analyzer` et `pyright` peuvent consommer une mémoire importante sur les grands projets. Si vous rencontrez des problèmes de mémoire, désactivez le plugin avec `/plugin disable <plugin-name>` et fiez-vous aux outils de recherche intégrés de Claude à la place.
* **Diagnostics faux positifs dans les monorepos** : les serveurs de langage peuvent signaler des erreurs d'import non résolues pour les packages internes si l'espace de travail n'est pas configuré correctement. Ceux-ci n'affectent pas la capacité de Claude à modifier le code.

## Prochaines étapes

* **Construisez vos propres plugins** : Consultez [Plugins](/fr/plugins) pour créer des skills, des agents et des hooks
* **Créez une marketplace** : Consultez [Créer une marketplace de plugins](/fr/plugin-marketplaces) pour distribuer des plugins à votre équipe ou communauté
* **Référence technique** : Consultez [Plugins reference](/fr/plugins-reference) pour les spécifications complètes
