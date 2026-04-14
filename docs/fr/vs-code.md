> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Utiliser Claude Code dans VS Code

> Installez et configurez l'extension Claude Code pour VS Code. Obtenez une assistance de codage IA avec des diffs en ligne, des mentions @, un examen du plan et des raccourcis clavier.

<img src="https://mintcdn.com/claude-code/-YhHHmtSxwr7W8gy/images/vs-code-extension-interface.jpg?fit=max&auto=format&n=-YhHHmtSxwr7W8gy&q=85&s=300652d5678c63905e6b0ea9e50835f8" alt="Éditeur VS Code avec le panneau d'extension Claude Code ouvert sur le côté droit, montrant une conversation avec Claude" width="2500" height="1155" data-path="images/vs-code-extension-interface.jpg" />

L'extension VS Code fournit une interface graphique native pour Claude Code, intégrée directement dans votre IDE. C'est la façon recommandée d'utiliser Claude Code dans VS Code.

Avec l'extension, vous pouvez examiner et modifier les plans de Claude avant de les accepter, accepter automatiquement les modifications au fur et à mesure qu'elles sont apportées, mentionner des fichiers avec des plages de lignes spécifiques à partir de votre sélection, accéder à l'historique des conversations et ouvrir plusieurs conversations dans des onglets ou des fenêtres séparés.

## Prérequis

Avant d'installer, assurez-vous que vous avez :

* VS Code 1.98.0 ou supérieur
* Un compte Anthropic (vous vous connecterez lors de la première ouverture de l'extension). Si vous utilisez un fournisseur tiers comme Amazon Bedrock ou Google Vertex AI, consultez plutôt [Utiliser des fournisseurs tiers](#use-third-party-providers).

<Tip>
  L'extension inclut le CLI (interface de ligne de commande), auquel vous pouvez accéder à partir du terminal intégré de VS Code pour les fonctionnalités avancées. Consultez [Extension VS Code vs. CLI Claude Code](#vs-code-extension-vs-claude-code-cli) pour plus de détails.
</Tip>

## Installer l'extension

Cliquez sur le lien de votre IDE pour installer directement :

* [Installer pour VS Code](vscode:extension/anthropic.claude-code)
* [Installer pour Cursor](cursor:extension/anthropic.claude-code)

Ou dans VS Code, appuyez sur `Cmd+Shift+X` (Mac) ou `Ctrl+Shift+X` (Windows/Linux) pour ouvrir la vue Extensions, recherchez « Claude Code » et cliquez sur **Installer**.

<Note>Si l'extension n'apparaît pas après l'installation, redémarrez VS Code ou exécutez « Developer: Reload Window » à partir de la Palette de commandes.</Note>

## Commencer

Une fois installée, vous pouvez commencer à utiliser Claude Code via l'interface VS Code :

<Steps>
  <Step title="Ouvrir le panneau Claude Code">
    Dans VS Code, l'icône Spark indique Claude Code : <img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/vs-code-spark-icon.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=3ca45e00deadec8c8f4b4f807da94505" alt="Icône Spark" style={{display: "inline", height: "0.85em", verticalAlign: "middle"}} width="16" height="16" data-path="images/vs-code-spark-icon.svg" />

    Le moyen le plus rapide d'ouvrir Claude est de cliquer sur l'icône Spark dans la **Barre d'outils de l'éditeur** (coin supérieur droit de l'éditeur). L'icône n'apparaît que lorsque vous avez un fichier ouvert.

        <img src="https://mintcdn.com/claude-code/mfM-EyoZGnQv8JTc/images/vs-code-editor-icon.png?fit=max&auto=format&n=mfM-EyoZGnQv8JTc&q=85&s=eb4540325d94664c51776dbbfec4cf02" alt="Éditeur VS Code montrant l'icône Spark dans la Barre d'outils de l'éditeur" width="2796" height="734" data-path="images/vs-code-editor-icon.png" />

    Autres façons d'ouvrir Claude Code :

    * **Barre d'activité** : cliquez sur l'icône Spark dans la barre latérale gauche pour ouvrir la liste des sessions. Cliquez sur n'importe quelle session pour l'ouvrir en tant qu'onglet d'éditeur complet, ou démarrez-en une nouvelle. Cette icône est toujours visible dans la Barre d'activité.
    * **Palette de commandes** : `Cmd+Shift+P` (Mac) ou `Ctrl+Shift+P` (Windows/Linux), tapez « Claude Code » et sélectionnez une option comme « Ouvrir dans un nouvel onglet »
    * **Barre d'état** : cliquez sur **✱ Claude Code** dans le coin inférieur droit de la fenêtre. Cela fonctionne même quand aucun fichier n'est ouvert.

    Lorsque vous ouvrez le panneau pour la première fois, une liste de contrôle **Apprendre Claude Code** apparaît. Parcourez chaque élément en cliquant sur **Montrer-moi**, ou fermez-la avec le X. Pour la rouvrir plus tard, décochez **Masquer l'intégration** dans les paramètres VS Code sous Extensions → Claude Code.

    Vous pouvez faire glisser le panneau Claude pour le repositionner n'importe où dans VS Code. Consultez [Personnaliser votre flux de travail](#customize-your-workflow) pour plus de détails.
  </Step>

  <Step title="Envoyer une invite">
    Demandez à Claude de vous aider avec votre code ou vos fichiers, qu'il s'agisse d'expliquer comment quelque chose fonctionne, de déboguer un problème ou d'apporter des modifications.

    <Tip>Claude voit automatiquement votre texte sélectionné. Appuyez sur `Option+K` (Mac) / `Alt+K` (Windows/Linux) pour insérer également une référence de mention @ (comme `@file.ts#5-10`) dans votre invite.</Tip>

    Voici un exemple de question sur une ligne particulière dans un fichier :

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-send-prompt.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=ede3ed8d8d5f940e01c5de636d009cfd" alt="Éditeur VS Code avec les lignes 2-3 sélectionnées dans un fichier Python, et le panneau Claude Code montrant une question sur ces lignes avec une référence de mention @" width="3288" height="1876" data-path="images/vs-code-send-prompt.png" />
  </Step>

  <Step title="Examiner les modifications">
    Lorsque Claude souhaite modifier un fichier, il affiche une comparaison côte à côte de l'original et des modifications proposées, puis demande une permission. Vous pouvez accepter, rejeter ou dire à Claude ce qu'il faut faire à la place.

        <img src="https://mintcdn.com/claude-code/FVYz38sRY-VuoGHA/images/vs-code-edits.png?fit=max&auto=format&n=FVYz38sRY-VuoGHA&q=85&s=e005f9b41c541c5c7c59c082f7c4841c" alt="VS Code montrant un diff des modifications proposées par Claude avec une invite de permission demandant si vous souhaitez effectuer la modification" width="3292" height="1876" data-path="images/vs-code-edits.png" />
  </Step>
</Steps>

Pour plus d'idées sur ce que vous pouvez faire avec Claude Code, consultez [Flux de travail courants](/fr/common-workflows).

<Tip>
  Exécutez « Claude Code: Open Walkthrough » à partir de la Palette de commandes pour une visite guidée des bases.
</Tip>

## Utiliser la zone de saisie

La zone de saisie prend en charge plusieurs fonctionnalités :

* **Modes de permission** : cliquez sur l'indicateur de mode en bas de la zone de saisie pour changer de mode. En mode normal, Claude demande une permission avant chaque action. En Plan Mode, Claude décrit ce qu'il fera et attend l'approbation avant d'apporter des modifications. VS Code ouvre automatiquement le plan en tant que document markdown complet où vous pouvez ajouter des commentaires en ligne pour donner des commentaires avant que Claude ne commence. En mode acceptation automatique, Claude apporte des modifications sans demander. Définissez la valeur par défaut dans les paramètres VS Code sous `claudeCode.initialPermissionMode`.
* **Menu de commandes** : cliquez sur `/` ou tapez `/` pour ouvrir le menu de commandes. Les options incluent l'attachement de fichiers, le changement de modèles, l'activation de la réflexion étendue, l'affichage de l'utilisation du plan (`/usage`) et le démarrage d'une session [Remote Control](/fr/remote-control) (`/remote-control`). La section Personnaliser fournit l'accès aux serveurs MCP, hooks, mémoire, permissions et plugins. Les éléments avec une icône de terminal s'ouvrent dans le terminal intégré.
* **Indicateur de contexte** : la zone de saisie affiche la quantité de fenêtre de contexte de Claude que vous utilisez. Claude se compacte automatiquement si nécessaire, ou vous pouvez exécuter `/compact` manuellement.
* **Réflexion étendue** : permet à Claude de consacrer plus de temps à raisonner sur des problèmes complexes. Activez-la via le menu de commandes (`/`). Consultez [Réflexion étendue](/fr/common-workflows#use-extended-thinking-thinking-mode) pour plus de détails.
* **Entrée multiligne** : appuyez sur `Shift+Entrée` pour ajouter une nouvelle ligne sans envoyer. Cela fonctionne également dans l'entrée en texte libre « Autre » des dialogues de question.

### Référencer des fichiers et des dossiers

Utilisez les mentions @ pour donner à Claude du contexte sur des fichiers ou des dossiers spécifiques. Lorsque vous tapez `@` suivi d'un nom de fichier ou de dossier, Claude lit ce contenu et peut répondre à des questions à ce sujet ou y apporter des modifications. Claude Code prend en charge la correspondance floue, vous pouvez donc taper des noms partiels pour trouver ce dont vous avez besoin :

```text  theme={null}
> Explain the logic in @auth (fuzzy matches auth.js, AuthService.ts, etc.)
> What's in @src/components/ (include a trailing slash for folders)
```

Pour les grands PDF, vous pouvez demander à Claude de lire des pages spécifiques au lieu du fichier entier : une seule page, une plage comme les pages 1-10, ou une plage ouverte comme la page 3 et au-delà.

Lorsque vous sélectionnez du texte dans l'éditeur, Claude peut voir votre code en surbrillance automatiquement. Le pied de page de la zone de saisie affiche le nombre de lignes sélectionnées. Appuyez sur `Option+K` (Mac) / `Alt+K` (Windows/Linux) pour insérer une mention @ avec le chemin du fichier et les numéros de ligne (par exemple, `@app.ts#5-10`). Cliquez sur l'indicateur de sélection pour basculer si Claude peut voir votre texte en surbrillance - l'icône en forme de barre oblique signifie que la sélection est masquée à Claude.

Vous pouvez également maintenir `Shift` enfoncé tout en faisant glisser des fichiers dans la zone de saisie pour les ajouter en tant que pièces jointes. Cliquez sur le X sur n'importe quelle pièce jointe pour la supprimer du contexte.

### Reprendre les conversations passées

Cliquez sur la liste déroulante en haut du panneau Claude Code pour accéder à votre historique de conversations. Vous pouvez rechercher par mot-clé ou parcourir par heure (Aujourd'hui, Hier, 7 derniers jours, etc.). Cliquez sur n'importe quelle conversation pour la reprendre avec l'historique complet des messages. Les nouvelles sessions reçoivent des titres générés par l'IA en fonction de votre premier message. Survolez une session pour révéler les actions de renommage et de suppression : renommez pour lui donner un titre descriptif, ou supprimez pour la supprimer de la liste. Pour plus d'informations sur la reprise des sessions, consultez [Flux de travail courants](/fr/common-workflows#resume-previous-conversations).

### Reprendre les sessions distantes de Claude.ai

Si vous utilisez [Claude Code sur le web](/fr/claude-code-on-the-web), vous pouvez reprendre ces sessions distantes directement dans VS Code. Cela nécessite de se connecter avec **Claude.ai Subscription**, pas Anthropic Console.

<Steps>
  <Step title="Ouvrir les conversations passées">
    Cliquez sur la liste déroulante **Conversations passées** en haut du panneau Claude Code.
  </Step>

  <Step title="Sélectionner l'onglet Distant">
    Le dialogue affiche deux onglets : Local et Distant. Cliquez sur **Distant** pour voir les sessions de claude.ai.
  </Step>

  <Step title="Sélectionner une session à reprendre">
    Parcourez ou recherchez vos sessions distantes. Cliquez sur n'importe quelle session pour la télécharger et continuer la conversation localement.
  </Step>
</Steps>

<Note>
  Seules les sessions web démarrées avec un référentiel GitHub apparaissent dans l'onglet Distant. La reprise charge l'historique de la conversation localement ; les modifications ne sont pas resynchronisées vers claude.ai.
</Note>

## Personnaliser votre flux de travail

Une fois que vous êtes opérationnel, vous pouvez repositionner le panneau Claude, exécuter plusieurs sessions ou passer au mode terminal.

### Choisir où Claude se trouve

Vous pouvez faire glisser le panneau Claude pour le repositionner n'importe où dans VS Code. Saisissez l'onglet ou la barre de titre du panneau et faites-le glisser vers :

* **Barre latérale secondaire** : le côté droit de la fenêtre. Garde Claude visible pendant que vous codez.
* **Barre latérale principale** : la barre latérale gauche avec les icônes pour l'Explorateur, la Recherche, etc.
* **Zone d'éditeur** : ouvre Claude en tant qu'onglet à côté de vos fichiers. Utile pour les tâches secondaires.

<Tip>
  Utilisez la barre latérale pour votre session Claude principale et ouvrez des onglets supplémentaires pour les tâches secondaires. Claude se souvient de votre emplacement préféré. L'icône de la liste des sessions de la Barre d'activité est séparée du panneau Claude : la liste des sessions est toujours visible dans la Barre d'activité, tandis que l'icône du panneau Claude n'y apparaît que lorsque le panneau est ancré à la barre latérale gauche.
</Tip>

### Exécuter plusieurs conversations

Utilisez **Ouvrir dans un nouvel onglet** ou **Ouvrir dans une nouvelle fenêtre** à partir de la Palette de commandes pour démarrer des conversations supplémentaires. Chaque conversation maintient son propre historique et contexte, vous permettant de travailler sur différentes tâches en parallèle.

Lors de l'utilisation d'onglets, un petit point coloré sur l'icône spark indique l'état : bleu signifie qu'une demande de permission est en attente, orange signifie que Claude a terminé pendant que l'onglet était masqué.

### Passer au mode terminal

Par défaut, l'extension ouvre un panneau de chat graphique. Si vous préférez l'interface de style CLI, ouvrez le [paramètre Utiliser le terminal](vscode://settings/claudeCode.useTerminal) et cochez la case.

Vous pouvez également ouvrir les paramètres VS Code (`Cmd+,` sur Mac ou `Ctrl+,` sur Windows/Linux), aller à Extensions → Claude Code et cocher **Utiliser le terminal**.

## Gérer les plugins

L'extension VS Code inclut une interface graphique pour installer et gérer les [plugins](/fr/plugins). Tapez `/plugins` dans la zone de saisie pour ouvrir l'interface **Gérer les plugins**.

### Installer les plugins

Le dialogue des plugins affiche deux onglets : **Plugins** et **Marchés**.

Dans l'onglet Plugins :

* Les **plugins installés** apparaissent en haut avec des commutateurs pour les activer ou les désactiver
* Les **plugins disponibles** de vos marchés configurés apparaissent ci-dessous
* Recherchez pour filtrer les plugins par nom ou description
* Cliquez sur **Installer** sur n'importe quel plugin disponible

Lorsque vous installez un plugin, choisissez l'étendue de l'installation :

* **Installer pour vous** : disponible dans tous vos projets (étendue utilisateur)
* **Installer pour ce projet** : partagé avec les collaborateurs du projet (étendue du projet)
* **Installer localement** : uniquement pour vous, uniquement dans ce référentiel (étendue locale)

### Gérer les marchés

Basculez vers l'onglet **Marchés** pour ajouter ou supprimer des sources de plugins :

* Entrez un référentiel GitHub, une URL ou un chemin local pour ajouter un nouveau marché
* Cliquez sur l'icône d'actualisation pour mettre à jour la liste des plugins d'un marché
* Cliquez sur l'icône de corbeille pour supprimer un marché

Après avoir apporté des modifications, une bannière vous invite à redémarrer Claude Code pour appliquer les mises à jour.

<Note>
  La gestion des plugins dans VS Code utilise les mêmes commandes CLI sous le capot. Les plugins et les marchés que vous configurez dans l'extension sont également disponibles dans le CLI, et vice versa.
</Note>

Pour plus d'informations sur le système de plugins, consultez [Plugins](/fr/plugins) et [Marchés de plugins](/fr/plugin-marketplaces).

## Automatiser les tâches du navigateur avec Chrome

Connectez Claude à votre navigateur Chrome pour tester les applications web, déboguer avec les journaux de la console et automatiser les flux de travail du navigateur sans quitter VS Code. Cela nécessite l'extension [Claude in Chrome](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) version 1.0.36 ou supérieure.

Tapez `@browser` dans la zone de saisie suivi de ce que vous voulez que Claude fasse :

```text  theme={null}
@browser go to localhost:3000 and check the console for errors
```

Vous pouvez également ouvrir le menu des pièces jointes pour sélectionner des outils de navigateur spécifiques comme ouvrir un nouvel onglet ou lire le contenu de la page.

Claude ouvre de nouveaux onglets pour les tâches du navigateur et partage l'état de connexion de votre navigateur, il peut donc accéder à n'importe quel site auquel vous êtes déjà connecté.

Pour les instructions de configuration, la liste complète des capacités et le dépannage, consultez [Utiliser Claude Code avec Chrome](/fr/chrome).

## Commandes et raccourcis VS Code

Ouvrez la Palette de commandes (`Cmd+Shift+P` sur Mac ou `Ctrl+Shift+P` sur Windows/Linux) et tapez ' Claude Code ' pour voir toutes les commandes VS Code disponibles pour l'extension Claude Code.

Certains raccourcis dépendent du panneau qui est ' actif ' (recevant l'entrée au clavier). Lorsque votre curseur est dans un fichier de code, l'éditeur est actif. Lorsque votre curseur est dans la zone de saisie de Claude, Claude est actif. Utilisez `Cmd+Esc` / `Ctrl+Esc` pour basculer entre eux.

<Note>
  Ce sont des commandes VS Code pour contrôler l'extension. Toutes les commandes Claude Code intégrées ne sont pas disponibles dans l'extension. Consultez [Extension VS Code vs. CLI Claude Code](#vs-code-extension-vs-claude-code-cli) pour plus de détails.
</Note>

| Commande                   | Raccourci                                                | Description                                                                                    |
| -------------------------- | -------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Focus Input                | `Cmd+Esc` (Mac) / `Ctrl+Esc` (Windows/Linux)             | Basculer le focus entre l'éditeur et Claude                                                    |
| Open in Side Bar           | -                                                        | Ouvrir Claude dans la barre latérale gauche                                                    |
| Open in Terminal           | -                                                        | Ouvrir Claude en mode terminal                                                                 |
| Open in New Tab            | `Cmd+Shift+Esc` (Mac) / `Ctrl+Shift+Esc` (Windows/Linux) | Ouvrir une nouvelle conversation en tant qu'onglet d'éditeur                                   |
| Open in New Window         | -                                                        | Ouvrir une nouvelle conversation dans une fenêtre séparée                                      |
| New Conversation           | `Cmd+N` (Mac) / `Ctrl+N` (Windows/Linux)                 | Démarrer une nouvelle conversation (nécessite que Claude soit actif)                           |
| Insert @-Mention Reference | `Option+K` (Mac) / `Alt+K` (Windows/Linux)               | Insérer une référence au fichier actuel et à la sélection (nécessite que l'éditeur soit actif) |
| Show Logs                  | -                                                        | Afficher les journaux de débogage de l'extension                                               |
| Logout                     | -                                                        | Se déconnecter de votre compte Anthropic                                                       |

### Lancer un onglet VS Code à partir d'autres outils

L'extension enregistre un gestionnaire URI à `vscode://anthropic.claude-code/open`. Utilisez-le pour ouvrir un nouvel onglet Claude Code à partir de vos propres outils : un alias shell, un signet de navigateur ou tout script capable d'ouvrir une URL. Si VS Code n'est pas déjà en cours d'exécution, l'ouverture de l'URL le lance d'abord. Si VS Code est déjà en cours d'exécution, l'URL s'ouvre dans la fenêtre actuellement active.

Invoquez le gestionnaire avec l'ouvreur d'URL de votre système d'exploitation. Sur macOS :

```bash  theme={null}
open "vscode://anthropic.claude-code/open"
```

Utilisez `xdg-open` sur Linux ou `start` sur Windows.

Le gestionnaire accepte deux paramètres de requête optionnels :

| Paramètre | Description                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `prompt`  | Texte à pré-remplir dans la zone de saisie. Doit être codé en URL. L'invite est pré-remplie mais non soumise automatiquement.                                                                                                                                                                                                                                                                                                                       |
| `session` | Un ID de session à reprendre au lieu de démarrer une nouvelle conversation. La session doit appartenir à l'espace de travail actuellement ouvert dans VS Code. Si la session n'est pas trouvée, une conversation nouvelle commence à la place. Si la session est déjà ouverte dans un onglet, cet onglet est actif. Pour capturer un ID de session par programmation, consultez [Continuer les conversations](/fr/headless#continue-conversations). |

Par exemple, pour ouvrir un onglet pré-rempli avec « review my changes » :

```text  theme={null}
vscode://anthropic.claude-code/open?prompt=review%20my%20changes
```

## Configurer les paramètres

L'extension a deux types de paramètres :

* **Paramètres d'extension** dans VS Code : contrôlent le comportement de l'extension dans VS Code. Ouvrez avec `Cmd+,` (Mac) ou `Ctrl+,` (Windows/Linux), puis allez à Extensions → Claude Code. Vous pouvez également taper `/` et sélectionner **General Config** pour ouvrir les paramètres.
* **Paramètres Claude Code** dans `~/.claude/settings.json` : partagés entre l'extension et CLI. Utilisez pour les commandes autorisées, les variables d'environnement, les hooks et les serveurs MCP. Consultez [Paramètres](/fr/settings) pour plus de détails.

<Tip>
  Ajoutez `"$schema": "https://json.schemastore.org/claude-code-settings.json"` à votre `settings.json` pour obtenir l'autocomplétion et la validation en ligne pour tous les paramètres disponibles directement dans VS Code.
</Tip>

### Paramètres d'extension

| Paramètre                         | Par défaut | Description                                                                                                                                                                                                                                                                                                                                     |
| --------------------------------- | ---------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `selectedModel`                   | `default`  | Modèle pour les nouvelles conversations. Changez par session avec `/model`.                                                                                                                                                                                                                                                                     |
| `useTerminal`                     | `false`    | Lancer Claude en mode terminal au lieu du panneau graphique                                                                                                                                                                                                                                                                                     |
| `initialPermissionMode`           | `default`  | Contrôle les invites d'approbation pour les nouvelles conversations : `default`, `plan`, `acceptEdits`, `auto` ou `bypassPermissions`. Consultez [modes de permission](/fr/permission-modes).                                                                                                                                                   |
| `preferredLocation`               | `panel`    | Où Claude s'ouvre : `sidebar` (droite) ou `panel` (nouvel onglet)                                                                                                                                                                                                                                                                               |
| `autosave`                        | `true`     | Enregistrement automatique des fichiers avant que Claude ne les lise ou ne les écrive                                                                                                                                                                                                                                                           |
| `useCtrlEnterToSend`              | `false`    | Utiliser Ctrl/Cmd+Entrée au lieu d'Entrée pour envoyer les invites                                                                                                                                                                                                                                                                              |
| `enableNewConversationShortcut`   | `true`     | Activer Cmd/Ctrl+N pour démarrer une nouvelle conversation                                                                                                                                                                                                                                                                                      |
| `hideOnboarding`                  | `false`    | Masquer la liste de contrôle d'intégration (icône de chapeau de graduation)                                                                                                                                                                                                                                                                     |
| `respectGitIgnore`                | `true`     | Exclure les modèles .gitignore des recherches de fichiers                                                                                                                                                                                                                                                                                       |
| `environmentVariables`            | `[]`       | Définir les variables d'environnement pour le processus Claude. Utilisez plutôt les paramètres Claude Code pour la configuration partagée.                                                                                                                                                                                                      |
| `disableLoginPrompt`              | `false`    | Ignorer les invites d'authentification (pour les configurations de fournisseur tiers)                                                                                                                                                                                                                                                           |
| `allowDangerouslySkipPermissions` | `false`    | Ajoute les permissions [Auto](/fr/permission-modes#eliminate-prompts-with-auto-mode) et Bypass au sélecteur de mode. Auto nécessite un plan Team et Claude Sonnet 4.6 ou Opus 4.6, donc l'option peut rester indisponible même avec ce basculement activé. Utilisez les permissions Bypass uniquement dans les sandboxes sans accès à Internet. |
| `claudeProcessWrapper`            | -          | Chemin exécutable utilisé pour lancer le processus Claude                                                                                                                                                                                                                                                                                       |

## Extension VS Code vs. CLI Claude Code

Claude Code est disponible à la fois en tant qu'extension VS Code (panneau graphique) et en tant que CLI (interface de ligne de commande dans le terminal). Certaines fonctionnalités ne sont disponibles que dans le CLI. Si vous avez besoin d'une fonctionnalité CLI uniquement, exécutez `claude` dans le terminal intégré de VS Code.

| Fonctionnalité               | CLI                  | Extension VS Code                                                                                         |
| ---------------------------- | -------------------- | --------------------------------------------------------------------------------------------------------- |
| Commandes et skills          | [Tous](/fr/commands) | Sous-ensemble (tapez `/` pour voir les disponibles)                                                       |
| Configuration du serveur MCP | Oui                  | Partiel (ajouter des serveurs via CLI ; gérer les serveurs existants avec `/mcp` dans le panneau de chat) |
| Checkpoints                  | Oui                  | Oui                                                                                                       |
| Raccourci bash `!`           | Oui                  | Non                                                                                                       |
| Complément de tabulation     | Oui                  | Non                                                                                                       |

### Rembobiner avec les checkpoints

L'extension VS Code prend en charge les checkpoints, qui suivent les modifications de fichiers de Claude et vous permettent de rembobiner à un état précédent. Survolez n'importe quel message pour révéler le bouton de rembobinage, puis choisissez parmi trois options :

* **Créer une branche de conversation à partir d'ici** : démarrer une nouvelle branche de conversation à partir de ce message tout en conservant toutes les modifications de code
* **Rembobiner le code jusqu'ici** : annuler les modifications de fichiers jusqu'à ce point dans la conversation tout en conservant l'historique complet de la conversation
* **Créer une branche de conversation et rembobiner le code** : démarrer une nouvelle branche de conversation et annuler les modifications de fichiers jusqu'à ce point

Pour tous les détails sur le fonctionnement des checkpoints et leurs limitations, consultez [Checkpointing](/fr/checkpointing).

### Exécuter le CLI dans VS Code

Pour utiliser le CLI tout en restant dans VS Code, ouvrez le terminal intégré (`` Ctrl+` `` sur Windows/Linux ou `` Cmd+` `` sur Mac) et exécutez `claude`. Le CLI s'intègre automatiquement à votre IDE pour des fonctionnalités comme l'affichage des diffs et le partage des diagnostics.

Si vous utilisez un terminal externe, exécutez `/ide` dans Claude Code pour le connecter à VS Code.

### Basculer entre l'extension et le CLI

L'extension et le CLI partagent le même historique de conversations. Pour continuer une conversation d'extension dans le CLI, exécutez `claude --resume` dans le terminal. Cela ouvre un sélecteur interactif où vous pouvez rechercher et sélectionner votre conversation.

### Inclure la sortie du terminal dans les invites

Référencez la sortie du terminal dans vos invites en utilisant `@terminal:name` où `name` est le titre du terminal. Cela permet à Claude de voir la sortie de la commande, les messages d'erreur ou les journaux sans copier-coller.

### Surveiller les processus en arrière-plan

Lorsque Claude exécute des commandes longues, l'extension affiche la progression dans la barre d'état. Cependant, la visibilité des tâches en arrière-plan est limitée par rapport au CLI. Pour une meilleure visibilité, demandez à Claude de générer la commande afin que vous puissiez l'exécuter dans le terminal intégré de VS Code.

### Connecter à des outils externes avec MCP

Les serveurs MCP (Model Context Protocol) donnent à Claude accès à des outils externes, des bases de données et des API.

Pour ajouter un serveur MCP, ouvrez le terminal intégré (`` Ctrl+` `` ou `` Cmd+` ``) et exécutez :

```bash  theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Une fois configuré, demandez à Claude d'utiliser les outils (par exemple, « Review PR #456 »).

Pour gérer les serveurs MCP sans quitter VS Code, tapez `/mcp` dans le panneau de chat. Le dialogue de gestion MCP vous permet d'activer ou de désactiver les serveurs, de vous reconnecter à un serveur et de gérer l'authentification OAuth. Consultez la [documentation MCP](/fr/mcp) pour les serveurs disponibles.

## Travailler avec git

Claude Code s'intègre à git pour vous aider avec les flux de travail de contrôle de version directement dans VS Code. Demandez à Claude de valider les modifications, de créer des demandes de tirage ou de travailler sur plusieurs branches.

### Créer des commits et des demandes de tirage

Claude peut mettre en scène les modifications, écrire des messages de commit et créer des demandes de tirage en fonction de votre travail :

```text  theme={null}
> commit my changes with a descriptive message
> create a pr for this feature
> summarize the changes I've made to the auth module
```

Lors de la création de demandes de tirage, Claude génère des descriptions basées sur les modifications de code réelles et peut ajouter du contexte sur les tests ou les décisions de mise en œuvre.

### Utiliser les git worktrees pour les tâches parallèles

Utilisez l'indicateur `--worktree` (`-w`) pour démarrer Claude dans un worktree isolé avec ses propres fichiers et branche :

```bash  theme={null}
claude --worktree feature-auth
```

Chaque worktree maintient un état de fichier indépendant tout en partageant l'historique git. Cela empêche les instances de Claude d'interférer les unes avec les autres lorsqu'elles travaillent sur différentes tâches. Pour plus de détails, consultez [Exécuter des sessions Claude Code parallèles avec Git worktrees](/fr/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees).

## Utiliser des fournisseurs tiers

Par défaut, Claude Code se connecte directement à l'API d'Anthropic. Si votre organisation utilise Amazon Bedrock, Google Vertex AI ou Microsoft Foundry pour accéder à Claude, configurez l'extension pour utiliser votre fournisseur à la place :

<Steps>
  <Step title="Désactiver l'invite de connexion">
    Ouvrez le [paramètre Désactiver l'invite de connexion](vscode://settings/claudeCode.disableLoginPrompt) et cochez la case.

    Vous pouvez également ouvrir les paramètres VS Code (`Cmd+,` sur Mac ou `Ctrl+,` sur Windows/Linux), recherchez ' Claude Code login ' et cochez **Désactiver l'invite de connexion**.
  </Step>

  <Step title="Configurer votre fournisseur">
    Suivez le guide de configuration de votre fournisseur :

    * [Claude Code sur Amazon Bedrock](/fr/amazon-bedrock)
    * [Claude Code sur Google Vertex AI](/fr/google-vertex-ai)
    * [Claude Code sur Microsoft Foundry](/fr/microsoft-foundry)

    Ces guides couvrent la configuration de votre fournisseur dans `~/.claude/settings.json`, ce qui garantit que vos paramètres sont partagés entre l'extension VS Code et le CLI.
  </Step>
</Steps>

## Sécurité et confidentialité

Votre code reste privé. Claude Code traite votre code pour fournir une assistance mais ne l'utilise pas pour entraîner les modèles. Pour plus de détails sur la gestion des données et comment refuser la journalisation, consultez [Données et confidentialité](/fr/data-usage).

Avec les permissions d'édition automatique activées, Claude Code peut modifier les fichiers de configuration VS Code (comme `settings.json` ou `tasks.json`) que VS Code peut exécuter automatiquement. Pour réduire le risque lorsque vous travaillez avec du code non fiable :

* Activez le [Mode restreint VS Code](https://code.visualstudio.com/docs/editor/workspace-trust#_restricted-mode) pour les espaces de travail non fiables
* Utilisez le mode d'approbation manuelle au lieu de l'acceptation automatique pour les modifications
* Examinez attentivement les modifications avant de les accepter

### Le serveur MCP IDE intégré

Lorsque l'extension est active, elle exécute un serveur MCP local auquel le CLI se connecte automatiquement. C'est ainsi que le CLI ouvre les diffs dans la visionneuse de diffs native de VS Code, lit votre sélection actuelle pour les mentions `@` et — lorsque vous travaillez dans un notebook Jupyter — demande à VS Code d'exécuter les cellules.

Le serveur est nommé `ide` et est masqué de `/mcp` car il n'y a rien à configurer. Cependant, si votre organisation utilise un hook `PreToolUse` pour créer une liste blanche des outils MCP, vous devez savoir qu'il existe.

**Transport et authentification.** Le serveur se lie à `127.0.0.1` sur un port élevé aléatoire et n'est pas accessible à partir d'autres machines. Chaque activation d'extension génère un jeton d'authentification aléatoire frais que le CLI doit présenter pour se connecter. Le jeton est écrit dans un fichier de verrouillage sous `~/.claude/ide/` avec les permissions `0600` dans un répertoire `0700`, donc seul l'utilisateur exécutant VS Code peut le lire.

**Outils exposés au modèle.** Le serveur héberge une douzaine d'outils, mais seulement deux sont visibles au modèle. Le reste est un RPC interne que le CLI utilise pour sa propre interface utilisateur — ouvrir les diffs, lire les sélections, enregistrer les fichiers — et sont filtrés avant que la liste des outils n'atteigne Claude.

| Nom de l'outil (tel que vu par les hooks) | Ce qu'il fait                                                                                                                                             | Écrit ? |
| ----------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | ------- |
| `mcp__ide__getDiagnostics`                | Retourne les diagnostics du serveur de langage — les erreurs et avertissements dans le panneau Problèmes de VS Code. Optionnellement limité à un fichier. | Non     |
| `mcp__ide__executeCode`                   | Exécute le code Python dans le kernel du notebook Jupyter actif. Consultez le flux de confirmation ci-dessous.                                            | Oui     |

**L'exécution Jupyter demande toujours d'abord.** `mcp__ide__executeCode` ne peut rien exécuter silencieusement. À chaque appel, le code est inséré en tant que nouvelle cellule à la fin du notebook actif, VS Code le fait défiler dans la vue, et un Quick Pick natif vous demande d'**Exécuter** ou d'**Annuler**. L'annulation — ou le rejet du sélecteur avec `Esc` — retourne une erreur à Claude et rien ne s'exécute. L'outil refuse également catégoriquement lorsqu'il n'y a pas de notebook actif, lorsque l'extension Jupyter (`ms-toolsai.jupyter`) n'est pas installée, ou lorsque le kernel n'est pas Python.

<Note>
  Le Quick Pick de confirmation est séparé des hooks `PreToolUse`. Une entrée de liste blanche pour `mcp__ide__executeCode` permet à Claude de *proposer* d'exécuter une cellule ; le Quick Pick dans VS Code est ce qui lui permet de l'*exécuter réellement*.
</Note>

## Corriger les problèmes courants

### L'extension ne s'installe pas

* Assurez-vous que vous avez une version compatible de VS Code (1.98.0 ou ultérieure)
* Vérifiez que VS Code a la permission d'installer des extensions
* Essayez d'installer directement à partir de la [Place de marché VS Code](https://marketplace.visualstudio.com/items?itemName=anthropic.claude-code)

### L'icône Spark n'est pas visible

L'icône Spark apparaît dans la **Barre d'outils de l'éditeur** (coin supérieur droit de l'éditeur) lorsque vous avez un fichier ouvert. Si vous ne la voyez pas :

1. **Ouvrir un fichier** : L'icône nécessite qu'un fichier soit ouvert. Avoir juste un dossier ouvert ne suffit pas.
2. **Vérifier la version de VS Code** : Nécessite 1.98.0 ou supérieur (Aide → À propos)
3. **Redémarrer VS Code** : Exécutez « Developer: Reload Window » à partir de la Palette de commandes
4. **Désactiver les extensions conflictuelles** : Désactivez temporairement les autres extensions IA (Cline, Continue, etc.)
5. **Vérifier la confiance de l'espace de travail** : L'extension ne fonctionne pas en Mode restreint

Vous pouvez également cliquer sur « ✱ Claude Code » dans la **Barre d'état** (coin inférieur droit). Cela fonctionne même sans fichier ouvert. Vous pouvez également utiliser la **Palette de commandes** (`Cmd+Shift+P` / `Ctrl+Shift+P`) et taper « Claude Code ».

### Claude Code ne répond jamais

Si Claude Code ne répond pas à vos invites :

1. **Vérifier votre connexion Internet** : Assurez-vous que vous avez une connexion Internet stable
2. **Démarrer une nouvelle conversation** : Essayez de démarrer une nouvelle conversation pour voir si le problème persiste
3. **Essayer le CLI** : Exécutez `claude` à partir du terminal pour voir si vous obtenez des messages d'erreur plus détaillés

Si les problèmes persistent, [déposez un problème sur GitHub](https://github.com/anthropics/claude-code/issues) avec des détails sur l'erreur.

## Désinstaller l'extension

Pour désinstaller l'extension Claude Code :

1. Ouvrez la vue Extensions (`Cmd+Shift+X` sur Mac ou `Ctrl+Shift+X` sur Windows/Linux)
2. Recherchez « Claude Code »
3. Cliquez sur **Désinstaller**

Pour également supprimer les données d'extension et réinitialiser tous les paramètres :

```bash  theme={null}
rm -rf ~/.vscode/globalStorage/anthropic.claude-code
```

Pour une aide supplémentaire, consultez le [guide de dépannage](/fr/troubleshooting).

## Étapes suivantes

Maintenant que vous avez Claude Code configuré dans VS Code :

* [Explorez les flux de travail courants](/fr/common-workflows) pour tirer le meilleur parti de Claude Code
* [Configurez les serveurs MCP](/fr/mcp) pour étendre les capacités de Claude avec des outils externes. Ajoutez des serveurs en utilisant le CLI, puis gérez-les avec `/mcp` dans le panneau de chat.
* [Configurez les paramètres Claude Code](/fr/settings) pour personnaliser les commandes autorisées, les hooks et bien d'autres. Ces paramètres sont partagés entre l'extension et le CLI.
