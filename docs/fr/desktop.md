> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Utiliser Claude Code Desktop

> Tirez le meilleur parti de Claude Code Desktop : sessions parallèles avec isolation Git, examen visuel des différences, aperçus d'applications, surveillance des PR, modes de permission, connecteurs et configuration d'entreprise.

L'onglet Code dans l'application Claude Desktop vous permet d'utiliser Claude Code via une interface graphique au lieu du terminal.

Desktop ajoute ces capacités à l'expérience standard de Claude Code :

* [Examen visuel des différences](#review-changes-with-diff-view) avec commentaires en ligne
* [Aperçu d'application en direct](#preview-your-app) avec serveurs de développement
* [Surveillance des PR GitHub](#monitor-pull-request-status) avec correction automatique et fusion automatique
* [Sessions parallèles](#work-in-parallel-with-sessions) avec isolation automatique des Git worktrees
* [Tâches planifiées](#schedule-recurring-tasks) qui exécutent Claude selon un calendrier récurrent
* [Connecteurs](#connect-external-tools) pour GitHub, Slack, Linear et bien d'autres
* Environnements locaux, [SSH](#ssh-sessions) et [cloud](#run-long-running-tasks-remotely)

<Tip>
  Nouveau sur Desktop ? Commencez par [Démarrer](/fr/desktop-quickstart) pour installer l'application et effectuer votre première modification.
</Tip>

Cette page couvre [travailler avec le code](#work-with-code), [gérer les sessions](#manage-sessions), [étendre Claude Code](#extend-claude-code), [tâches planifiées](#schedule-recurring-tasks) et [configuration](#environment-configuration). Elle inclut également une [comparaison CLI](#coming-from-the-cli) et [dépannage](#troubleshooting).

## Démarrer une session

Avant d'envoyer votre premier message, configurez quatre choses dans la zone de prompt :

* **Environnement** : choisissez où Claude s'exécute. Sélectionnez **Local** pour votre machine, **Remote** pour les sessions cloud hébergées par Anthropic, ou une [**connexion SSH**](#ssh-sessions) pour une machine distante que vous gérez. Voir [configuration de l'environnement](#environment-configuration).
* **Dossier du projet** : sélectionnez le dossier ou le référentiel dans lequel Claude travaille. Pour les sessions distantes, vous pouvez ajouter [plusieurs référentiels](#run-long-running-tasks-remotely).
* **Modèle** : choisissez un [modèle](/fr/model-config#available-models) dans la liste déroulante à côté du bouton d'envoi. Le modèle est verrouillé une fois la session démarrée.
* **Mode de permission** : choisissez le niveau d'autonomie de Claude à partir du [sélecteur de mode](#choose-a-permission-mode). Vous pouvez modifier ceci pendant la session.

Tapez votre tâche et appuyez sur **Entrée** pour démarrer. Chaque session suit son propre contexte et les modifications indépendamment.

## Travailler avec le code

Donnez à Claude le bon contexte, contrôlez le volume de travail qu'il effectue seul et examinez ce qu'il a modifié.

### Utiliser la zone de prompt

Tapez ce que vous voulez que Claude fasse et appuyez sur **Entrée** pour envoyer. Claude lit vos fichiers de projet, effectue des modifications et exécute des commandes en fonction de votre [mode de permission](#choose-a-permission-mode). Vous pouvez interrompre Claude à tout moment : cliquez sur le bouton d'arrêt ou tapez votre correction et appuyez sur **Entrée**. Claude arrête ce qu'il fait et s'ajuste en fonction de votre entrée.

Le bouton **+** à côté de la zone de prompt vous donne accès aux pièces jointes de fichiers, [skills](#use-skills), [connecteurs](#connect-external-tools) et [plugins](#install-plugins).

### Ajouter des fichiers et du contexte aux prompts

La zone de prompt supporte deux façons d'apporter du contexte externe :

* **Fichiers @mention** : tapez `@` suivi d'un nom de fichier pour ajouter un fichier au contexte de la conversation. Claude peut alors lire et référencer ce fichier.
* **Joindre des fichiers** : joignez des images, des PDF et d'autres fichiers à votre prompt en utilisant le bouton de pièce jointe, ou glissez-déposez les fichiers directement dans le prompt. Ceci est utile pour partager des captures d'écran de bugs, des maquettes de conception ou des documents de référence.

### Choisir un mode de permission

Les modes de permission contrôlent le niveau d'autonomie de Claude pendant une session : s'il demande avant de modifier des fichiers, d'exécuter des commandes ou les deux. Vous pouvez changer de mode à tout moment en utilisant le sélecteur de mode à côté du bouton d'envoi. Commencez par Demander les permissions pour voir exactement ce que Claude fait, puis passez à Accepter automatiquement les modifications ou Plan mode à mesure que vous vous sentez à l'aise.

| Mode                                           | Clé de paramètres   | Comportement                                                                                                                                                                                                                                                                                                                                                         |
| ---------------------------------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Demander les permissions**                   | `default`           | Claude demande avant de modifier des fichiers ou d'exécuter des commandes. Vous voyez une différence et pouvez accepter ou rejeter chaque modification. Recommandé pour les nouveaux utilisateurs.                                                                                                                                                                   |
| **Accepter automatiquement les modifications** | `acceptEdits`       | Claude accepte automatiquement les modifications de fichiers mais demande toujours avant d'exécuter les commandes du terminal. Utilisez ceci quand vous faites confiance aux modifications de fichiers et voulez une itération plus rapide.                                                                                                                          |
| **Plan mode**                                  | `plan`              | Claude analyse votre code et crée un plan sans modifier les fichiers ou exécuter les commandes. Bon pour les tâches complexes où vous voulez examiner l'approche en premier.                                                                                                                                                                                         |
| **Contourner les permissions**                 | `bypassPermissions` | Claude s'exécute sans aucune invite de permission, équivalent à `--dangerously-skip-permissions` dans la CLI. Activez dans vos Paramètres → Claude Code sous « Autoriser le mode de contournement des permissions ». Utilisez uniquement dans les conteneurs sandboxés ou les machines virtuelles. Les administrateurs d'entreprise peuvent désactiver cette option. |

Le mode de permission `dontAsk` est disponible uniquement dans la [CLI](/fr/permissions#permission-modes).

<Tip title="Bonne pratique">
  Commencez les tâches complexes en Plan mode pour que Claude trace une approche avant de faire des modifications. Une fois que vous approuvez le plan, passez à Accepter automatiquement les modifications ou Demander les permissions pour l'exécuter. Voir [explorer d'abord, puis planifier, puis coder](/fr/best-practices#explore-first-then-plan-then-code) pour plus d'informations sur ce flux de travail.
</Tip>

Les sessions distantes supportent Accepter automatiquement les modifications et Plan mode. Demander les permissions n'est pas disponible car les sessions distantes acceptent automatiquement les modifications de fichiers par défaut, et Contourner les permissions n'est pas disponible car l'environnement distant est déjà sandboxé.

Les administrateurs d'entreprise peuvent restreindre les modes de permission disponibles. Voir [configuration d'entreprise](#enterprise-configuration) pour les détails.

### Aperçu de votre application

Claude peut démarrer un serveur de développement et ouvrir un navigateur intégré pour vérifier ses modifications. Ceci fonctionne pour les applications web frontend ainsi que les serveurs backend : Claude peut tester les points de terminaison API, afficher les journaux du serveur et itérer sur les problèmes qu'il trouve. Dans la plupart des cas, Claude démarre le serveur automatiquement après la modification des fichiers du projet. Vous pouvez également demander à Claude de prévisualiser à tout moment. Par défaut, Claude [vérifie automatiquement](#auto-verify-changes) les modifications après chaque modification.

À partir du panneau d'aperçu, vous pouvez :

* Interagir avec votre application en cours d'exécution directement dans le navigateur intégré
* Regarder Claude vérifier ses propres modifications automatiquement : il prend des captures d'écran, inspecte le DOM, clique sur les éléments, remplit les formulaires et corrige les problèmes qu'il trouve
* Démarrer ou arrêter les serveurs à partir de la liste déroulante **Aperçu** dans la barre d'outils de la session
* Conserver les cookies et le stockage local entre les redémarrages du serveur en sélectionnant **Conserver les sessions** dans la liste déroulante, afin que vous n'ayez pas à vous reconnecter pendant le développement
* Modifier la configuration du serveur ou arrêter tous les serveurs à la fois

Claude crée la configuration initiale du serveur en fonction de votre projet. Si votre application utilise une commande de développement personnalisée, modifiez `.claude/launch.json` pour correspondre à votre configuration. Voir [Configurer les serveurs d'aperçu](#configure-preview-servers) pour la référence complète.

Pour effacer les données de session enregistrées, basculez **Conserver les sessions d'aperçu** sur Désactivé dans Paramètres → Claude Code. Pour désactiver complètement l'aperçu, basculez **Aperçu** sur Désactivé dans Paramètres → Claude Code.

### Examiner les modifications avec la vue de différence

Après que Claude ait modifié votre code, la vue de différence vous permet d'examiner les modifications fichier par fichier avant de créer une demande de tirage.

Quand Claude modifie des fichiers, un indicateur de statistiques de différence apparaît montrant le nombre de lignes ajoutées et supprimées, comme `+12 -1`. Cliquez sur cet indicateur pour ouvrir la visionneuse de différences, qui affiche une liste de fichiers à gauche et les modifications pour chaque fichier à droite.

Pour commenter des lignes spécifiques, cliquez sur n'importe quelle ligne dans la différence pour ouvrir une boîte de commentaire. Tapez votre retour et appuyez sur **Entrée** pour ajouter le commentaire. Après avoir ajouté des commentaires à plusieurs lignes, soumettez tous les commentaires à la fois :

* **macOS** : appuyez sur **Cmd+Entrée**
* **Windows** : appuyez sur **Ctrl+Entrée**

Claude lit vos commentaires et effectue les modifications demandées, qui apparaissent comme une nouvelle différence que vous pouvez examiner.

### Examiner votre code

Dans la vue de différence, cliquez sur **Examiner le code** dans la barre d'outils en haut à droite pour demander à Claude d'évaluer les modifications avant de les valider. Claude examine les différences actuelles et laisse des commentaires directement dans la vue de différence. Vous pouvez répondre à n'importe quel commentaire ou demander à Claude de réviser.

L'examen se concentre sur les problèmes à haut signal : erreurs de compilation, erreurs logiques définies, vulnérabilités de sécurité et bugs évidents. Il ne signale pas le style, le formatage, les problèmes préexistants ou quoi que ce soit qu'un linter attraperait.

### Surveiller l'état de la demande de tirage

Après avoir ouvert une demande de tirage, une barre d'état CI apparaît dans la session. Claude Code utilise la CLI GitHub pour interroger les résultats des vérifications et afficher les défaillances.

* **Correction automatique** : quand activée, Claude tente automatiquement de corriger les vérifications CI défaillantes en lisant la sortie de défaillance et en itérant.
* **Fusion automatique** : quand activée, Claude fusionne la PR une fois que toutes les vérifications réussissent. La méthode de fusion est squash. La fusion automatique doit être [activée dans les paramètres de votre référentiel GitHub](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/configuring-pull-request-merges/managing-auto-merge-for-pull-requests-in-your-repository) pour que cela fonctionne.

Utilisez les bascules **Correction automatique** et **Fusion automatique** dans la barre d'état CI pour activer l'une ou l'autre option. Claude Code envoie également une notification de bureau quand CI se termine.

<Note>
  La surveillance des PR nécessite que la [CLI GitHub (`gh`)](https://cli.github.com/) soit installée et authentifiée sur votre machine. Si `gh` n'est pas installée, Desktop vous invite à l'installer la première fois que vous essayez de créer une PR.
</Note>

## Gérer les sessions

Chaque session est une conversation indépendante avec son propre contexte et ses propres modifications. Vous pouvez exécuter plusieurs sessions en parallèle ou envoyer du travail vers le cloud.

### Travailler en parallèle avec les sessions

Cliquez sur **+ Nouvelle session** dans la barre latérale pour travailler sur plusieurs tâches en parallèle. Pour les référentiels Git, chaque session obtient sa propre copie isolée de votre projet en utilisant [Git worktrees](/fr/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), donc les modifications dans une session n'affectent pas les autres sessions jusqu'à ce que vous les validiez.

Les worktrees sont stockés dans `<project-root>/.claude/worktrees/` par défaut. Vous pouvez modifier ceci en un répertoire personnalisé dans Paramètres → Claude Code sous ' Emplacement du worktree '. Vous pouvez également définir un préfixe de branche qui est ajouté au début de chaque nom de branche worktree, ce qui est utile pour garder les branches créées par Claude organisées. Pour supprimer un worktree quand vous avez terminé, survolez la session dans la barre latérale et cliquez sur l'icône d'archive.

<Note>
  L'isolation des sessions nécessite [Git](https://git-scm.com/downloads). La plupart des Macs incluent Git par défaut. Exécutez `git --version` dans Terminal pour vérifier. Sur Windows, Git est requis pour que l'onglet Code fonctionne : [téléchargez Git pour Windows](https://git-scm.com/downloads/win), installez-le et redémarrez l'application. Si vous rencontrez des erreurs Git, essayez une session Cowork pour aider à dépanner votre configuration.
</Note>

Utilisez l'icône de filtre en haut de la barre latérale pour filtrer les sessions par statut (Actif, Archivé) et environnement (Local, Cloud). Pour renommer une session ou vérifier l'utilisation du contexte, cliquez sur le titre de la session dans la barre d'outils en haut de la session active. Quand le contexte se remplit, Claude résume automatiquement la conversation et continue de travailler. Vous pouvez également taper `/compact` pour déclencher la compaction plus tôt et libérer de l'espace de contexte. Voir [la fenêtre de contexte](/fr/how-claude-code-works#the-context-window) pour les détails sur le fonctionnement de la compaction.

### Exécuter des tâches longues à distance

Pour les refactorisations importantes, les suites de tests, les migrations ou autres tâches longues, sélectionnez **Remote** au lieu de **Local** au démarrage d'une session. Les sessions distantes s'exécutent sur l'infrastructure cloud d'Anthropic et continuent même si vous fermez l'application ou arrêtez votre ordinateur. Revenez à tout moment pour voir la progression ou orienter Claude dans une direction différente. Vous pouvez également surveiller les sessions distantes à partir de [claude.ai/code](https://claude.ai/code) ou de l'application Claude iOS.

Les sessions distantes supportent également plusieurs référentiels. Après avoir sélectionné un environnement cloud, cliquez sur le bouton **+** à côté de la pilule de référentiel pour ajouter des référentiels supplémentaires à la session. Chaque référentiel obtient son propre sélecteur de branche. Ceci est utile pour les tâches qui s'étendent sur plusieurs bases de code, comme la mise à jour d'une bibliothèque partagée et ses consommateurs.

Voir [Claude Code sur le web](/fr/claude-code-on-the-web) pour plus d'informations sur le fonctionnement des sessions distantes.

### Continuer sur une autre surface

Le menu **Continuer dans**, accessible à partir de l'icône VS Code en bas à droite de la barre d'outils de la session, vous permet de déplacer votre session vers une autre surface :

* **Claude Code sur le Web** : envoie votre session locale pour continuer à s'exécuter à distance. Desktop pousse votre branche, génère un résumé de la conversation et crée une nouvelle session distante avec le contexte complet. Vous pouvez ensuite choisir d'archiver la session locale ou de la conserver. Ceci nécessite un arbre de travail propre et n'est pas disponible pour les sessions SSH.
* **Votre IDE** : ouvre votre projet dans un IDE supporté au répertoire de travail actuel.

## Étendre Claude Code

Connectez les services externes, ajoutez des flux de travail réutilisables, personnalisez le comportement de Claude et configurez les serveurs d'aperçu.

### Connecter les outils externes

Pour les sessions locales et [SSH](#ssh-sessions), cliquez sur le bouton **+** à côté de la zone de prompt et sélectionnez **Connecteurs** pour ajouter des intégrations comme Google Calendar, Slack, GitHub, Linear, Notion et bien d'autres. Vous pouvez ajouter des connecteurs avant ou pendant une session. Les connecteurs ne sont pas disponibles pour les sessions distantes.

Pour gérer ou déconnecter les connecteurs, allez à Paramètres → Connecteurs dans l'application de bureau, ou sélectionnez **Gérer les connecteurs** à partir du menu Connecteurs dans la zone de prompt.

Une fois connecté, Claude peut lire votre calendrier, envoyer des messages, créer des problèmes et interagir avec vos outils directement. Vous pouvez demander à Claude quels connecteurs sont configurés dans votre session.

Les connecteurs sont [des serveurs MCP](/fr/mcp) avec un flux de configuration graphique. Utilisez-les pour une intégration rapide avec les services supportés. Pour les intégrations non listées dans Connecteurs, ajoutez les serveurs MCP manuellement via [fichiers de paramètres](/fr/mcp#installing-mcp-servers). Vous pouvez également [créer des connecteurs personnalisés](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

### Utiliser les skills

[Les skills](/fr/skills) étendent ce que Claude peut faire. Claude les charge automatiquement quand ils sont pertinents, ou vous pouvez en invoquer un directement : tapez `/` dans la zone de prompt ou cliquez sur le bouton **+** et sélectionnez **Slash commands** pour parcourir ce qui est disponible. Ceci inclut [les commandes intégrées](/fr/commands), vos [skills personnalisés](/fr/skills#create-custom-skills), les skills du projet à partir de votre base de code et les skills de tout [plugin installé](/fr/plugins). Sélectionnez-en un et il apparaît en surbrillance dans le champ d'entrée. Tapez votre tâche après et envoyez comme d'habitude.

### Installer les plugins

[Les plugins](/fr/plugins) sont des packages réutilisables qui ajoutent des skills, des agents, des hooks, des serveurs MCP et des configurations LSP à Claude Code. Vous pouvez installer les plugins à partir de l'application de bureau sans utiliser le terminal.

Pour les sessions locales et [SSH](#ssh-sessions), cliquez sur le bouton **+** à côté de la zone de prompt et sélectionnez **Plugins** pour voir vos plugins installés et leurs commandes. Pour ajouter un plugin, sélectionnez **Ajouter un plugin** à partir du sous-menu pour ouvrir le navigateur de plugins, qui affiche les plugins disponibles à partir de vos [marketplaces](/fr/plugin-marketplaces) configurés, y compris le marketplace officiel d'Anthropic. Sélectionnez **Gérer les plugins** pour activer, désactiver ou désinstaller les plugins.

Les plugins peuvent être limités à votre compte utilisateur, un projet spécifique ou local uniquement. Les plugins ne sont pas disponibles pour les sessions distantes. Pour la référence complète des plugins, y compris la création de vos propres plugins, voir [plugins](/fr/plugins).

### Configurer les serveurs d'aperçu

Claude détecte automatiquement votre configuration de serveur de développement et stocke la configuration dans `.claude/launch.json` à la racine du dossier que vous avez sélectionné au démarrage de la session. L'aperçu utilise ce dossier comme répertoire de travail, donc si vous avez sélectionné un dossier parent, les sous-dossiers avec leurs propres serveurs de développement ne seront pas détectés automatiquement. Pour travailler avec le serveur d'un sous-dossier, soit démarrez une session dans ce dossier directement, soit ajoutez une configuration manuellement.

Pour personnaliser le démarrage de votre serveur, par exemple pour utiliser `yarn dev` au lieu de `npm run dev` ou pour modifier le port, modifiez le fichier manuellement ou cliquez sur **Modifier la configuration** dans la liste déroulante Aperçu pour l'ouvrir dans votre éditeur de code. Le fichier supporte JSON avec commentaires.

```json  theme={null}
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "my-app",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

Vous pouvez définir plusieurs configurations pour exécuter différents serveurs à partir du même projet, comme un frontend et une API. Voir les [exemples](#examples) ci-dessous.

#### Vérification automatique des modifications

Quand `autoVerify` est activé, Claude vérifie automatiquement les modifications de code après la modification des fichiers. Il prend des captures d'écran, vérifie les erreurs et confirme que les modifications fonctionnent avant de terminer sa réponse.

La vérification automatique est activée par défaut. Désactivez-la par projet en ajoutant `"autoVerify": false` à `.claude/launch.json`, ou basculez-la à partir du menu déroulant **Aperçu**.

```json  theme={null}
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [...]
}
```

Quand désactivée, les outils d'aperçu sont toujours disponibles et vous pouvez demander à Claude de vérifier à tout moment. La vérification automatique la rend automatique après chaque modification.

#### Champs de configuration

Chaque entrée dans le tableau `configurations` accepte les champs suivants :

| Champ               | Type      | Description                                                                                                                                                                                                                                                        |
| ------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`              | string    | Un identifiant unique pour ce serveur                                                                                                                                                                                                                              |
| `runtimeExecutable` | string    | La commande à exécuter, comme `npm`, `yarn` ou `node`                                                                                                                                                                                                              |
| `runtimeArgs`       | string\[] | Arguments passés à `runtimeExecutable`, comme `["run", "dev"]`                                                                                                                                                                                                     |
| `port`              | number    | Le port sur lequel votre serveur écoute. Par défaut 3000                                                                                                                                                                                                           |
| `cwd`               | string    | Répertoire de travail relatif à la racine de votre projet. Par défaut la racine du projet. Utilisez `${workspaceFolder}` pour référencer la racine du projet explicitement                                                                                         |
| `env`               | object    | Variables d'environnement supplémentaires comme paires clé-valeur, comme `{ "NODE_ENV": "development" }`. Ne mettez pas de secrets ici car ce fichier est validé dans votre référentiel. Les secrets définis dans votre profil shell sont hérités automatiquement. |
| `autoPort`          | boolean   | Comment gérer les conflits de port. Voir ci-dessous                                                                                                                                                                                                                |
| `program`           | string    | Un script à exécuter avec `node`. Voir [quand utiliser `program` vs `runtimeExecutable`](#when-to-use-program-vs-runtimeexecutable)                                                                                                                                |
| `args`              | string\[] | Arguments passés à `program`. Utilisé uniquement quand `program` est défini                                                                                                                                                                                        |

##### Quand utiliser `program` vs `runtimeExecutable`

Utilisez `runtimeExecutable` avec `runtimeArgs` pour démarrer un serveur de développement via un gestionnaire de packages. Par exemple, `"runtimeExecutable": "npm"` avec `"runtimeArgs": ["run", "dev"]` exécute `npm run dev`.

Utilisez `program` quand vous avez un script autonome que vous voulez exécuter avec `node` directement. Par exemple, `"program": "server.js"` exécute `node server.js`. Passez des drapeaux supplémentaires avec `args`.

#### Conflits de port

Le champ `autoPort` contrôle ce qui se passe quand votre port préféré est déjà utilisé :

* **`true`** : Claude trouve et utilise un port libre automatiquement. Approprié pour la plupart des serveurs de développement.
* **`false`** : Claude échoue avec une erreur. Utilisez ceci quand votre serveur doit utiliser un port spécifique, comme pour les rappels OAuth ou les listes blanches CORS.
* **Non défini (par défaut)** : Claude demande si le serveur a besoin de ce port exact, puis enregistre votre réponse.

Quand Claude choisit un port différent, il passe le port assigné à votre serveur via la variable d'environnement `PORT`.

#### Exemples

Ces configurations montrent les configurations courantes pour différents types de projets :

<Tabs>
  <Tab title="Next.js">
    Cette configuration exécute une application Next.js en utilisant Yarn sur le port 3000 :

    ```json  theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "web",
          "runtimeExecutable": "yarn",
          "runtimeArgs": ["dev"],
          "port": 3000
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Plusieurs serveurs">
    Pour un monorepo avec un serveur frontend et API, définissez plusieurs configurations. Le frontend utilise `autoPort: true` pour qu'il choisisse un port libre si 3000 est pris, tandis que le serveur API nécessite le port 8080 exactement :

    ```json  theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "frontend",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "dev"],
          "cwd": "apps/web",
          "port": 3000,
          "autoPort": true
        },
        {
          "name": "api",
          "runtimeExecutable": "npm",
          "runtimeArgs": ["run", "start"],
          "cwd": "server",
          "port": 8080,
          "env": { "NODE_ENV": "development" },
          "autoPort": false
        }
      ]
    }
    ```
  </Tab>

  <Tab title="Script Node.js">
    Pour exécuter un script Node.js directement au lieu d'utiliser une commande du gestionnaire de packages, utilisez le champ `program` :

    ```json  theme={null}
    {
      "version": "0.0.1",
      "configurations": [
        {
          "name": "server",
          "program": "server.js",
          "args": ["--verbose"],
          "port": 4000
        }
      ]
    }
    ```
  </Tab>
</Tabs>

## Planifier les tâches récurrentes

Les tâches planifiées démarrent une nouvelle session locale automatiquement à une heure et une fréquence que vous choisissez. Utilisez-les pour le travail récurrent comme les examens de code quotidiens, les vérifications de mise à jour des dépendances ou les briefings matinaux qui tirent de votre calendrier et de votre boîte de réception.

Les tâches s'exécutent sur votre machine, donc l'application de bureau doit être ouverte et votre ordinateur éveillé pour qu'elles se déclenchent. Voir [Comment les tâches planifiées s'exécutent](#how-scheduled-tasks-run) pour les détails sur les exécutions manquées et le comportement de rattrapage.

<Note>
  Par défaut, les tâches planifiées s'exécutent contre l'état dans lequel se trouve votre répertoire de travail, y compris les modifications non validées. Activez le basculement worktree dans l'entrée de prompt pour donner à chaque exécution son propre Git worktree isolé, de la même manière que [les sessions parallèles](#work-in-parallel-with-sessions) fonctionnent.
</Note>

Pour créer une tâche planifiée, cliquez sur **Planifier** dans la barre latérale, puis **+ Nouvelle tâche**. Configurez ces champs :

| Champ       | Description                                                                                                                                                                                                                                                                                  |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Nom         | Identifiant pour la tâche. Converti en kebab-case minuscule et utilisé comme nom de dossier sur le disque. Doit être unique parmi vos tâches.                                                                                                                                                |
| Description | Résumé court affiché dans la liste des tâches.                                                                                                                                                                                                                                               |
| Prompt      | Les instructions envoyées à Claude quand la tâche s'exécute. Écrivez ceci de la même manière que vous écririez n'importe quel message dans la zone de prompt. L'entrée de prompt inclut également les contrôles pour le modèle, le mode de permission, le dossier de travail et le worktree. |
| Fréquence   | La fréquence à laquelle la tâche s'exécute. Voir [options de fréquence](#frequency-options) ci-dessous.                                                                                                                                                                                      |

Vous pouvez également créer une tâche en décrivant ce que vous voulez dans n'importe quelle session. Par exemple, « configurer un examen de code quotidien qui s'exécute chaque matin à 9h ».

### Options de fréquence

* **Manuel** : pas de calendrier, s'exécute uniquement quand vous cliquez sur **Exécuter maintenant**. Utile pour enregistrer un prompt que vous déclenchez à la demande
* **Horaire** : s'exécute chaque heure. Chaque tâche obtient un décalage fixe de jusqu'à 10 minutes à partir du sommet de l'heure pour échelonner le trafic API
* **Quotidien** : affiche un sélecteur d'heure, par défaut 9h00 heure locale
* **Jours de semaine** : identique à Quotidien mais saute samedi et dimanche
* **Hebdomadaire** : affiche un sélecteur d'heure et un sélecteur de jour

Pour les intervalles que le sélecteur n'offre pas (toutes les 15 minutes, premier de chaque mois, etc.), demandez à Claude dans n'importe quelle session Desktop de définir le calendrier. Utilisez le langage naturel ; par exemple, « planifier une tâche pour exécuter tous les tests toutes les 6 heures ».

### Comment les tâches planifiées s'exécutent

Les tâches planifiées s'exécutent localement sur votre machine. Desktop vérifie le calendrier chaque minute tandis que l'application est ouverte et démarre une session fraîche quand une tâche est due, indépendamment de toute session manuelle que vous avez ouverte. Chaque tâche obtient un délai fixe de jusqu'à 10 minutes après l'heure planifiée pour échelonner le trafic API. Le délai est déterministe : la même tâche démarre toujours au même décalage.

Quand une tâche se déclenche, vous recevez une notification de bureau et une nouvelle session apparaît sous une section **Planifiée** dans la barre latérale. Ouvrez-la pour voir ce que Claude a fait, examiner les modifications ou répondre aux invites de permission. La session fonctionne comme n'importe quelle autre : Claude peut modifier des fichiers, exécuter des commandes, créer des validations et ouvrir des demandes de tirage.

Les tâches s'exécutent uniquement tandis que l'application de bureau est en cours d'exécution et votre ordinateur est éveillé. Si votre ordinateur dort pendant une heure planifiée, l'exécution est ignorée. Pour empêcher le sommeil inactif, activez **Garder l'ordinateur éveillé** dans Paramètres sous **Application de bureau → Général**. Fermer le couvercle de l'ordinateur portable le met toujours en sommeil.

### Exécutions manquées

Quand l'application démarre ou votre ordinateur se réveille, Desktop vérifie si chaque tâche a manqué des exécutions au cours des sept derniers jours. Si c'est le cas, Desktop démarre exactement une exécution de rattrapage pour l'heure la plus récemment manquée et rejette tout ce qui est plus ancien. Une tâche quotidienne qui a manqué six jours s'exécute une fois au réveil. Desktop affiche une notification quand une exécution de rattrapage démarre.

Gardez ceci à l'esprit quand vous écrivez des prompts. Une tâche planifiée pour 9h pourrait s'exécuter à 23h si votre ordinateur a dormi toute la journée. Si le timing importe, ajoutez des garde-fous au prompt lui-même, par exemple : « Examinez uniquement les validations d'aujourd'hui. S'il est après 17h, ignorez l'examen et publiez simplement un résumé de ce qui a été manqué ».

### Permissions pour les tâches planifiées

Chaque tâche a son propre mode de permission, que vous définissez lors de la création ou de la modification de la tâche. Les règles d'autorisation de `~/.claude/settings.json` s'appliquent également aux sessions de tâches planifiées. Si une tâche s'exécute en mode Ask et doit exécuter un outil pour lequel elle n'a pas de permission, l'exécution s'arrête jusqu'à ce que vous l'approuviez. La session reste ouverte dans la barre latérale pour que vous puissiez répondre plus tard.

Pour éviter les arrêts, cliquez sur **Exécuter maintenant** après avoir créé une tâche, regardez les invites de permission et sélectionnez « toujours autoriser » pour chacune. Les exécutions futures de cette tâche approuvent automatiquement les mêmes outils sans demander. Vous pouvez examiner et révoquer ces approbations à partir de la page de détail de la tâche.

### Gérer les tâches planifiées

Cliquez sur une tâche dans la liste **Planifier** pour ouvrir sa page de détail. À partir d'ici, vous pouvez :

* **Exécuter maintenant** : démarrer la tâche immédiatement sans attendre l'heure planifiée suivante
* **Basculer les répétitions** : mettre en pause ou reprendre les exécutions planifiées sans supprimer la tâche
* **Modifier** : modifier le prompt, la fréquence, le dossier ou d'autres paramètres
* **Examiner l'historique** : voir chaque exécution passée, y compris celles qui ont été ignorées parce que votre ordinateur dormait
* **Examiner les permissions autorisées** : voir et révoquer les approbations d'outils enregistrées pour cette tâche à partir du panneau **Toujours autorisé**
* **Supprimer** : supprimer la tâche et archiver toutes les sessions qu'elle a créées

Vous pouvez également gérer les tâches en demandant à Claude dans n'importe quelle session Desktop. Par exemple, « mettre en pause ma tâche de dépendance-audit », « supprimer la tâche de préparation-standup » ou « afficher mes tâches planifiées ».

Pour modifier le prompt d'une tâche sur le disque, ouvrez `~/.claude/scheduled-tasks/<task-name>/SKILL.md` (ou sous [`CLAUDE_CONFIG_DIR`](/fr/env-vars) si défini). Le fichier utilise le frontmatter YAML pour `name` et `description`, avec le prompt comme corps. Les modifications prennent effet à la prochaine exécution. Le calendrier, le dossier, le modèle et l'état activé ne sont pas dans ce fichier : modifiez-les via le formulaire Modifier ou demandez à Claude.

## Configuration de l'environnement

L'environnement que vous choisissez au [démarrage d'une session](#start-a-session) détermine où Claude s'exécute et comment vous vous connectez :

* **Local** : s'exécute sur votre machine avec accès direct à vos fichiers
* **Remote** : s'exécute sur l'infrastructure cloud d'Anthropic. Les sessions continuent même si vous fermez l'application.
* **SSH** : s'exécute sur une machine distante à laquelle vous vous connectez via SSH, comme vos propres serveurs, des machines virtuelles cloud ou des conteneurs de développement

### Sessions locales

Les sessions locales héritent des variables d'environnement de votre shell. Si vous avez besoin de variables supplémentaires, définissez-les dans votre profil shell, comme `~/.zshrc` ou `~/.bashrc`, et redémarrez l'application de bureau. Voir [variables d'environnement](/fr/env-vars) pour la liste complète des variables supportées.

[La réflexion étendue](/fr/common-workflows#use-extended-thinking-thinking-mode) est activée par défaut, ce qui améliore les performances sur les tâches de raisonnement complexe mais utilise des tokens supplémentaires. Pour désactiver complètement la réflexion, définissez `MAX_THINKING_TOKENS=0` dans votre profil shell. Sur Opus, `MAX_THINKING_TOKENS` est ignoré sauf pour `0` car le raisonnement adaptatif contrôle la profondeur de la réflexion à la place.

### Sessions distantes

Les sessions distantes continuent en arrière-plan même si vous fermez l'application. L'utilisation compte vers les limites de votre [plan d'abonnement](/fr/costs) sans frais de calcul séparés.

Vous pouvez créer des environnements cloud personnalisés avec différents niveaux d'accès réseau et variables d'environnement. Sélectionnez la liste déroulante d'environnement au démarrage d'une session distante et choisissez **Ajouter un environnement**. Voir [environnements cloud](/fr/claude-code-on-the-web#cloud-environment) pour les détails sur la configuration de l'accès réseau et des variables d'environnement.

### Sessions SSH

Les sessions SSH vous permettent d'exécuter Claude Code sur une machine distante tout en utilisant l'application de bureau comme votre interface. Ceci est utile pour travailler avec des bases de code qui vivent sur des machines virtuelles cloud, des conteneurs de développement ou des serveurs avec du matériel ou des dépendances spécifiques.

Pour ajouter une connexion SSH, cliquez sur la liste déroulante d'environnement avant de démarrer une session et sélectionnez **+ Ajouter une connexion SSH**. La boîte de dialogue demande :

* **Nom** : une étiquette conviviale pour cette connexion
* **Hôte SSH** : `user@hostname` ou un hôte défini dans `~/.ssh/config`
* **Port SSH** : par défaut 22 s'il est laissé vide, ou utilise le port de votre configuration SSH
* **Fichier d'identité** : chemin vers votre clé privée, comme `~/.ssh/id_rsa`. Laissez vide pour utiliser la clé par défaut ou votre configuration SSH.

Une fois ajoutée, la connexion apparaît dans la liste déroulante d'environnement. Sélectionnez-la pour démarrer une session sur cette machine. Claude s'exécute sur la machine distante avec accès à ses fichiers et outils.

Claude Code doit être installé sur la machine distante. Une fois connecté, les sessions SSH supportent les modes de permission, les connecteurs, les plugins et les serveurs MCP.

## Configuration d'entreprise

Les organisations sur les plans Teams ou Enterprise peuvent gérer le comportement de l'application de bureau via les contrôles de la console d'administration, les fichiers de paramètres gérés et les politiques de gestion des appareils.

### Contrôles de la console d'administration

Ces paramètres sont configurés via la [console de paramètres d'administration](https://claude.ai/admin-settings/claude-code) :

* **Activer ou désactiver l'onglet Code** : contrôlez si les utilisateurs de votre organisation peuvent accéder à Claude Code dans l'application de bureau
* **Désactiver le mode Contourner les permissions** : empêchez les utilisateurs de votre organisation d'activer le mode de contournement des permissions
* **Désactiver Claude Code sur le web** : activez ou désactivez les sessions distantes pour votre organisation

### Paramètres gérés

Les paramètres gérés remplacent les paramètres du projet et de l'utilisateur et s'appliquent quand Desktop génère des sessions CLI. Vous pouvez définir ces clés dans le fichier [paramètres gérés](/fr/settings#settings-precedence) de votre organisation ou les pousser à distance via la console d'administration.

| Clé                            | Description                                                                                                                                                                              |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode` | définissez sur `"disable"` pour empêcher les utilisateurs d'activer le mode de contournement des permissions. Voir [paramètres gérés uniquement](/fr/permissions#managed-only-settings). |

Pour la liste complète des paramètres gérés uniquement, y compris `allowManagedPermissionRulesOnly` et `allowManagedHooksOnly`, voir [paramètres gérés uniquement](/fr/permissions#managed-only-settings).

Les paramètres gérés distants téléchargés via la console d'administration s'appliquent actuellement uniquement aux sessions CLI et IDE. Pour les restrictions spécifiques à Desktop, utilisez les contrôles de la console d'administration ci-dessus.

### Politiques de gestion des appareils

Les équipes informatiques peuvent gérer l'application de bureau via MDM sur macOS ou la politique de groupe sur Windows. Les politiques disponibles incluent l'activation ou la désactivation de la fonctionnalité Claude Code, le contrôle des mises à jour automatiques et la définition d'une URL de déploiement personnalisée.

* **macOS** : configurez via le domaine de préférence `com.anthropic.Claude` en utilisant des outils comme Jamf ou Kandji
* **Windows** : configurez via le registre à `SOFTWARE\Policies\Claude`

### Authentification et SSO

Les organisations d'entreprise peuvent exiger SSO pour tous les utilisateurs. Voir [authentification](/fr/authentication) pour les détails au niveau du plan et [Configuration de SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso) pour la configuration SAML et OIDC.

### Gestion des données

Claude Code traite votre code localement dans les sessions locales ou sur l'infrastructure cloud d'Anthropic dans les sessions distantes. Les conversations et le contexte du code sont envoyés à l'API d'Anthropic pour le traitement. Voir [gestion des données](/fr/data-usage) pour les détails sur la rétention des données, la confidentialité et la conformité.

### Déploiement

Desktop peut être distribué via les outils de déploiement d'entreprise :

* **macOS** : distribuez via MDM comme Jamf ou Kandji en utilisant l'installateur `.dmg`
* **Windows** : déployez via le package MSIX ou l'installateur `.exe`. Voir [Déployer Claude Desktop pour Windows](https://support.claude.com/en/articles/12622703-deploy-claude-desktop-for-windows) pour les options de déploiement d'entreprise, y compris l'installation silencieuse

Pour la configuration réseau comme les paramètres de proxy, l'ajout à la liste blanche du pare-feu et les passerelles LLM, voir [configuration réseau](/fr/network-config).

Pour la référence complète de la configuration d'entreprise, voir le [guide de configuration d'entreprise](https://support.claude.com/en/articles/12622667-enterprise-configuration).

## Venant de la CLI ?

Si vous utilisez déjà la CLI Claude Code, Desktop exécute le même moteur sous-jacent avec une interface graphique. Vous pouvez exécuter les deux simultanément sur la même machine, même sur le même projet. Chacun maintient un historique de session séparé, mais ils partagent la configuration et la mémoire du projet via les fichiers CLAUDE.md.

Pour déplacer une session CLI dans Desktop, exécutez `/desktop` dans le terminal. Claude enregistre votre session et l'ouvre dans l'application de bureau, puis quitte la CLI. Cette commande est disponible sur macOS et Windows uniquement.

<Tip>
  Quand utiliser Desktop vs CLI : utilisez Desktop quand vous voulez l'examen visuel des différences, les pièces jointes de fichiers ou la gestion des sessions dans une barre latérale. Utilisez la CLI quand vous avez besoin de scripts, d'automatisation, de fournisseurs tiers ou préférez un flux de travail terminal.
</Tip>

### Équivalents des drapeaux CLI

Ce tableau montre l'équivalent de l'application de bureau pour les drapeaux CLI courants. Les drapeaux non listés n'ont pas d'équivalent de bureau car ils sont conçus pour les scripts ou l'automatisation.

| CLI                                            | Équivalent de bureau                                                                                                                                                                               |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--model sonnet`                               | liste déroulante de modèle à côté du bouton d'envoi, avant de démarrer une session                                                                                                                 |
| `--resume`, `--continue`                       | cliquez sur une session dans la barre latérale                                                                                                                                                     |
| `--permission-mode`                            | sélecteur de mode à côté du bouton d'envoi                                                                                                                                                         |
| `--dangerously-skip-permissions`               | Mode Contourner les permissions. Activez dans Paramètres → Claude Code → « Autoriser le mode de contournement des permissions ». Les administrateurs d'entreprise peuvent désactiver ce paramètre. |
| `--add-dir`                                    | ajouter plusieurs référentiels avec le bouton **+** dans les sessions distantes                                                                                                                    |
| `--allowedTools`, `--disallowedTools`          | non disponible dans Desktop                                                                                                                                                                        |
| `--verbose`                                    | non disponible. Vérifiez les journaux système : Console.app sur macOS, Observateur d'événements → Journaux Windows → Application sur Windows                                                       |
| `--print`, `--output-format`                   | non disponible. Desktop est interactif uniquement.                                                                                                                                                 |
| Variable d'environnement `ANTHROPIC_MODEL`     | liste déroulante de modèle à côté du bouton d'envoi                                                                                                                                                |
| Variable d'environnement `MAX_THINKING_TOKENS` | définissez dans le profil shell ; s'applique aux sessions locales. Voir [configuration de l'environnement](#environment-configuration).                                                            |

### Configuration partagée

Desktop et CLI lisent les mêmes fichiers de configuration, donc votre configuration se transfère :

* Les fichiers **[CLAUDE.md](/fr/memory)** dans votre projet sont utilisés par les deux
* Les **[serveurs MCP](/fr/mcp)** configurés dans `~/.claude.json` ou `.mcp.json` fonctionnent dans les deux
* Les **[hooks](/fr/hooks)** et **[skills](/fr/skills)** définis dans les paramètres s'appliquent aux deux
* Les **[paramètres](/fr/settings)** dans `~/.claude.json` et `~/.claude/settings.json` sont partagés. Les règles de permission, les outils autorisés et d'autres paramètres dans `settings.json` s'appliquent aux sessions Desktop.
* **Modèles** : Sonnet, Opus et Haiku sont disponibles dans les deux. Dans Desktop, sélectionnez le modèle à partir de la liste déroulante à côté du bouton d'envoi avant de démarrer une session. Vous ne pouvez pas modifier le modèle pendant une session active.

<Note>
  **Serveurs MCP : application de chat de bureau vs Claude Code** : les serveurs MCP configurés pour l'application de chat Claude Desktop dans `claude_desktop_config.json` sont séparés de Claude Code et n'apparaîtront pas dans l'onglet Code. Pour utiliser les serveurs MCP dans Claude Code, configurez-les dans `~/.claude.json` ou le fichier `.mcp.json` de votre projet. Voir [configuration MCP](/fr/mcp#installing-mcp-servers) pour les détails.
</Note>

### Comparaison des fonctionnalités

Ce tableau compare les capacités principales entre la CLI et Desktop. Pour une liste complète des drapeaux CLI, voir la [référence CLI](/fr/cli-reference).

| Fonctionnalité                                     | CLI                                                       | Desktop                                                                                                                         |
| -------------------------------------------------- | --------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| Modes de permission                                | tous les modes y compris `dontAsk`                        | Demander les permissions, Accepter automatiquement les modifications, Plan mode et Contourner les permissions via Paramètres    |
| `--dangerously-skip-permissions`                   | Drapeau CLI                                               | Mode Contourner les permissions. Activez dans Paramètres → Claude Code → « Autoriser le mode de contournement des permissions » |
| [Fournisseurs tiers](/fr/third-party-integrations) | Bedrock, Vertex, Foundry                                  | non disponible. Desktop se connecte directement à l'API d'Anthropic.                                                            |
| [Serveurs MCP](/fr/mcp)                            | configurer dans les fichiers de paramètres                | Interface utilisateur Connecteurs pour les sessions locales et SSH, ou fichiers de paramètres                                   |
| [Plugins](/fr/plugins)                             | Commande `/plugin`                                        | Interface utilisateur du gestionnaire de plugins                                                                                |
| Fichiers @mention                                  | basé sur le texte                                         | avec autocomplétion                                                                                                             |
| Pièces jointes de fichiers                         | non disponible                                            | images, PDF                                                                                                                     |
| Isolation des sessions                             | Drapeau [`--worktree`](/fr/cli-reference)                 | worktrees automatiques                                                                                                          |
| Sessions multiples                                 | terminaux séparés                                         | onglets de barre latérale                                                                                                       |
| Tâches récurrentes                                 | tâches cron, pipelines CI                                 | [tâches planifiées](#schedule-recurring-tasks)                                                                                  |
| Scripts et automatisation                          | [`--print`](/fr/cli-reference), [Agent SDK](/fr/headless) | non disponible                                                                                                                  |

### Ce qui n'est pas disponible dans Desktop

Les fonctionnalités suivantes sont disponibles uniquement dans la CLI ou l'extension VS Code :

* **Fournisseurs tiers** : Desktop se connecte directement à l'API d'Anthropic. Utilisez la [CLI](/fr/quickstart) avec Bedrock, Vertex ou Foundry à la place.
* **Linux** : l'application de bureau est disponible sur macOS et Windows uniquement.
* **Suggestions de code en ligne** : Desktop ne fournit pas de suggestions de style autocomplétion. Il fonctionne via des prompts conversationnels et des modifications de code explicites.
* **Équipes d'agents** : l'orchestration multi-agents est disponible via la [CLI](/fr/agent-teams) et [Agent SDK](/fr/headless), pas dans Desktop.

## Dépannage

### Vérifier votre version

Pour voir quelle version de l'application de bureau vous exécutez :

* **macOS** : cliquez sur **Claude** dans la barre de menu, puis **À propos de Claude**
* **Windows** : cliquez sur **Aide**, puis **À propos**

Cliquez sur le numéro de version pour le copier dans votre presse-papiers.

### Erreurs 403 ou d'authentification dans l'onglet Code

Si vous voyez `Error 403: Forbidden` ou d'autres défaillances d'authentification lors de l'utilisation de l'onglet Code :

1. Déconnectez-vous et reconnectez-vous à partir du menu de l'application. C'est le correctif le plus courant.
2. Vérifiez que vous avez un abonnement payant actif : Pro, Max, Teams ou Enterprise.
3. Si la CLI fonctionne mais Desktop ne fonctionne pas, quittez complètement l'application de bureau, pas seulement fermez la fenêtre, puis rouvrez et reconnectez-vous.
4. Vérifiez votre connexion Internet et vos paramètres de proxy.

### Écran blanc ou bloqué au lancement

Si l'application s'ouvre mais affiche un écran blanc ou ne répond pas :

1. Redémarrez l'application.
2. Vérifiez les mises à jour en attente. L'application se met à jour automatiquement au lancement.
3. Sur Windows, vérifiez l'Observateur d'événements pour les journaux de crash sous **Journaux Windows → Application**.

### « Impossible de charger la session »

Si vous voyez `Failed to load session`, le dossier sélectionné peut ne plus exister, un référentiel Git peut nécessiter Git LFS qui n'est pas installé, ou les permissions de fichier peuvent empêcher l'accès. Essayez de sélectionner un dossier différent ou redémarrez l'application.

### Session ne trouvant pas les outils installés

Si Claude ne peut pas trouver des outils comme `npm`, `node` ou d'autres commandes CLI, vérifiez que les outils fonctionnent dans votre terminal régulier, vérifiez que votre profil shell configure correctement PATH et redémarrez l'application de bureau pour recharger les variables d'environnement.

### Erreurs Git et Git LFS

Sur Windows, Git est requis pour que l'onglet Code démarre les sessions locales. Si vous voyez « Git is required », installez [Git pour Windows](https://git-scm.com/downloads/win) et redémarrez l'application.

Si vous voyez « Git LFS is required by this repository but is not installed », installez Git LFS à partir de [git-lfs.com](https://git-lfs.com/), exécutez `git lfs install` et redémarrez l'application.

### Les serveurs MCP ne fonctionnent pas sur Windows

Si les bascules du serveur MCP ne répondent pas ou que les serveurs ne se connectent pas sur Windows, vérifiez que le serveur est correctement configuré dans vos paramètres, redémarrez l'application, vérifiez que le processus du serveur s'exécute dans le Gestionnaire des tâches et examinez les journaux du serveur pour les erreurs de connexion.

### L'application ne veut pas quitter

* **macOS** : appuyez sur Cmd+Q. Si l'application ne répond pas, utilisez Forcer à quitter avec Cmd+Option+Esc, sélectionnez Claude et cliquez sur Forcer à quitter.
* **Windows** : utilisez le Gestionnaire des tâches avec Ctrl+Maj+Esc pour terminer le processus Claude.

### Problèmes spécifiques à Windows

* **PATH non mis à jour après l'installation** : ouvrez une nouvelle fenêtre de terminal. Les mises à jour PATH s'appliquent uniquement aux nouvelles sessions de terminal.
* **Erreur d'installation simultanée** : si vous voyez une erreur concernant une autre installation en cours mais qu'il n'y en a pas, essayez d'exécuter l'installateur en tant qu'administrateur.
* **ARM64** : les appareils Windows ARM64 sont entièrement supportés.

### Onglet Cowork indisponible sur les Macs Intel

L'onglet Cowork nécessite Apple Silicon (M1 ou ultérieur) sur macOS. Sur Windows, Cowork est disponible sur tout le matériel supporté. Les onglets Chat et Code fonctionnent normalement sur les Macs Intel.

### « La branche n'existe pas encore » lors de l'ouverture dans la CLI

Les sessions distantes peuvent créer des branches qui n'existent pas sur votre machine locale. Cliquez sur le nom de la branche dans la barre d'outils de la session pour le copier, puis récupérez-le localement :

```bash  theme={null}
git fetch origin <branch-name>
git checkout <branch-name>
```

### Toujours bloqué ?

* Recherchez ou signalez un bug sur [GitHub Issues](https://github.com/anthropics/claude-code/issues)
* Visitez le [centre de support Claude](https://support.claude.com/)

Lors du signalement d'un bug, incluez la version de votre application de bureau, votre système d'exploitation, le message d'erreur exact et les journaux pertinents. Sur macOS, vérifiez Console.app. Sur Windows, vérifiez Observateur d'événements → Journaux Windows → Application.
