> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Mode interactif

> Référence complète des raccourcis clavier, modes d'entrée et fonctionnalités interactives dans les sessions Claude Code.

## Raccourcis clavier

<Note>
  Les raccourcis clavier peuvent varier selon la plateforme et le terminal. Appuyez sur `?` pour voir les raccourcis disponibles dans votre environnement.

  **Utilisateurs macOS** : les raccourcis avec la touche Option/Alt (`Alt+B`, `Alt+F`, `Alt+Y`, `Alt+M`, `Alt+P`) nécessitent de configurer Option comme Meta dans votre terminal :

  * **iTerm2** : paramètres → Profils → Touches → définir la touche Option gauche/droite sur « Esc+ »
  * **Terminal.app** : paramètres → Profils → Clavier → cocher « Utiliser Option comme touche Meta »
  * **VS Code** : paramètres → Profils → Touches → définir la touche Option gauche/droite sur « Esc+ »

  Consultez [Configuration du terminal](/fr/terminal-config) pour plus de détails.
</Note>

### Contrôles généraux

| Raccourci                                         | Description                                                                                   | Contexte                                                                                                         |
| :------------------------------------------------ | :-------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- |
| `Ctrl+C`                                          | Annuler l'entrée ou la génération actuelle                                                    | Interruption standard                                                                                            |
| `Ctrl+F`                                          | Arrêter tous les agents en arrière-plan. Appuyez deux fois dans les 3 secondes pour confirmer | Contrôle des agents en arrière-plan                                                                              |
| `Ctrl+D`                                          | Quitter la session Claude Code                                                                | Signal EOF                                                                                                       |
| `Ctrl+G`                                          | Ouvrir dans l'éditeur de texte par défaut                                                     | Modifiez votre invite ou réponse personnalisée dans votre éditeur de texte par défaut                            |
| `Ctrl+L`                                          | Effacer l'écran du terminal                                                                   | Conserve l'historique de conversation                                                                            |
| `Ctrl+O`                                          | Basculer la sortie détaillée                                                                  | Affiche l'utilisation détaillée des outils et l'exécution                                                        |
| `Ctrl+R`                                          | Recherche inversée dans l'historique des commandes                                            | Rechercher dans les commandes précédentes de manière interactive                                                 |
| `Ctrl+V` ou `Cmd+V` (iTerm2) ou `Alt+V` (Windows) | Coller une image du presse-papiers                                                            | Colle une image ou un chemin vers un fichier image                                                               |
| `Ctrl+B`                                          | Tâches en arrière-plan                                                                        | Met en arrière-plan les commandes bash et les agents. Les utilisateurs Tmux appuyez deux fois                    |
| `Ctrl+T`                                          | Basculer la liste des tâches                                                                  | Afficher ou masquer la [liste des tâches](#task-list) dans la zone d'état du terminal                            |
| `Flèches gauche/droite`                           | Parcourir les onglets de dialogue                                                             | Naviguer entre les onglets dans les dialogues de permission et les menus                                         |
| `Flèches haut/bas`                                | Naviguer dans l'historique des commandes                                                      | Rappeler les entrées précédentes                                                                                 |
| `Esc` + `Esc`                                     | Rembobiner ou résumer                                                                         | Restaurer le code et/ou la conversation à un point antérieur, ou résumer à partir d'un message sélectionné       |
| `Shift+Tab` ou `Alt+M` (certaines configurations) | Basculer les modes de permission                                                              | Basculer entre le mode Auto-Accept, Plan Mode et le mode normal.                                                 |
| `Option+P` (macOS) ou `Alt+P` (Windows/Linux)     | Changer de modèle                                                                             | Changer de modèles sans effacer votre invite                                                                     |
| `Option+T` (macOS) ou `Alt+T` (Windows/Linux)     | Basculer la réflexion étendue                                                                 | Activer ou désactiver le mode de réflexion étendue. Exécutez d'abord `/terminal-setup` pour activer ce raccourci |

### Édition de texte

| Raccourci                | Description                             | Contexte                                                                                                                 |
| :----------------------- | :-------------------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+K`                 | Supprimer jusqu'à la fin de la ligne    | Stocke le texte supprimé pour le collage                                                                                 |
| `Ctrl+U`                 | Supprimer la ligne entière              | Stocke le texte supprimé pour le collage                                                                                 |
| `Ctrl+Y`                 | Coller le texte supprimé                | Coller le texte supprimé avec `Ctrl+K` ou `Ctrl+U`                                                                       |
| `Alt+Y` (après `Ctrl+Y`) | Parcourir l'historique du collage       | Après le collage, parcourir le texte précédemment supprimé. Nécessite [Option comme Meta](#keyboard-shortcuts) sur macOS |
| `Alt+B`                  | Déplacer le curseur d'un mot en arrière | Navigation par mot. Nécessite [Option comme Meta](#keyboard-shortcuts) sur macOS                                         |
| `Alt+F`                  | Déplacer le curseur d'un mot en avant   | Navigation par mot. Nécessite [Option comme Meta](#keyboard-shortcuts) sur macOS                                         |

### Thème et affichage

| Raccourci | Description                                              | Contexte                                                                                                                                   |
| :-------- | :------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------- |
| `Ctrl+T`  | Basculer la coloration syntaxique pour les blocs de code | Fonctionne uniquement dans le menu du sélecteur `/theme`. Contrôle si le code dans les réponses de Claude utilise la coloration syntaxique |

<Note>
  La coloration syntaxique n'est disponible que dans la version native de Claude Code.
</Note>

### Entrée multiligne

| Méthode              | Raccourci          | Contexte                                                    |
| :------------------- | :----------------- | :---------------------------------------------------------- |
| Échappement rapide   | `\` + `Entrée`     | Fonctionne dans tous les terminaux                          |
| Par défaut macOS     | `Option+Entrée`    | Par défaut sur macOS                                        |
| Shift+Entrée         | `Shift+Entrée`     | Fonctionne directement dans iTerm2, WezTerm, Ghostty, Kitty |
| Séquence de contrôle | `Ctrl+J`           | Caractère de saut de ligne pour multiligne                  |
| Mode collage         | Coller directement | Pour les blocs de code, les journaux                        |

<Tip>
  Shift+Entrée fonctionne sans configuration dans iTerm2, WezTerm, Ghostty et Kitty. Pour les autres terminaux (VS Code, Alacritty, Zed, Warp), exécutez `/terminal-setup` pour installer la liaison.
</Tip>

### Commandes rapides

| Raccourci    | Description                  | Notes                                                                            |
| :----------- | :--------------------------- | :------------------------------------------------------------------------------- |
| `/` au début | Commande ou skill            | Consultez [commandes intégrées](#built-in-commands) et [skills](/fr/skills)      |
| `!` au début | Mode Bash                    | Exécuter les commandes directement et ajouter la sortie d'exécution à la session |
| `@`          | Mention de chemin de fichier | Déclencher l'autocomplétion du chemin de fichier                                 |

## Commandes intégrées

Tapez `/` dans Claude Code pour voir toutes les commandes disponibles, ou tapez `/` suivi de n'importe quelles lettres pour filtrer. Toutes les commandes ne sont pas visibles pour tous les utilisateurs. Certaines dépendent de votre plateforme, plan ou environnement. Par exemple, `/desktop` n'apparaît que sur macOS et Windows, `/upgrade` et `/privacy-settings` ne sont disponibles que pour les plans Pro et Max, et `/terminal-setup` est masqué lorsque votre terminal supporte nativement ses liaisons de touches.

Claude Code est également livré avec des [skills groupés](/fr/skills#bundled-skills) comme `/simplify`, `/batch` et `/debug` qui apparaissent aux côtés des commandes intégrées lorsque vous tapez `/`. Pour créer vos propres commandes, consultez [skills](/fr/skills).

Dans le tableau ci-dessous, `<arg>` indique un argument obligatoire et `[arg]` indique un argument facultatif.

| Commande                  | Objectif                                                                                                                                                                                                                                                                  |
| :------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `/add-dir <path>`         | Ajouter un nouveau répertoire de travail à la session actuelle                                                                                                                                                                                                            |
| `/agents`                 | Gérer les configurations d'[agent](/fr/sub-agents)                                                                                                                                                                                                                        |
| `/btw <question>`         | Poser une [question rapide](#side-questions-with-%2Fbtw) sans l'ajouter à la conversation                                                                                                                                                                                 |
| `/chrome`                 | Configurer les paramètres de [Claude dans Chrome](/fr/chrome)                                                                                                                                                                                                             |
| `/clear`                  | Effacer l'historique de conversation et libérer du contexte. Alias : `/reset`, `/new`                                                                                                                                                                                     |
| `/compact [instructions]` | Compacter la conversation avec des instructions de focus optionnelles                                                                                                                                                                                                     |
| `/config`                 | Ouvrir l'interface [Paramètres](/fr/settings) pour ajuster le thème, le modèle, [style de sortie](/fr/output-styles) et autres préférences. Alias : `/settings`                                                                                                           |
| `/context`                | Visualiser l'utilisation actuelle du contexte sous forme de grille colorée                                                                                                                                                                                                |
| `/copy`                   | Copier la dernière réponse de l'assistant dans le presse-papiers. Lorsque des blocs de code sont présents, affiche un sélecteur interactif pour sélectionner des blocs individuels ou la réponse complète                                                                 |
| `/cost`                   | Afficher les statistiques d'utilisation des tokens. Consultez le [guide de suivi des coûts](/fr/costs#using-the-cost-command) pour les détails spécifiques à l'abonnement                                                                                                 |
| `/desktop`                | Continuer la session actuelle dans l'application Claude Code Desktop. macOS et Windows uniquement. Alias : `/app`                                                                                                                                                         |
| `/diff`                   | Ouvrir une visionneuse de diff interactive affichant les modifications non validées et les diffs par tour. Utilisez les flèches gauche/droite pour basculer entre le diff git actuel et les tours Claude individuels, et haut/bas pour parcourir les fichiers             |
| `/doctor`                 | Diagnostiquer et vérifier votre installation et vos paramètres Claude Code                                                                                                                                                                                                |
| `/exit`                   | Quitter le CLI. Alias : `/quit`                                                                                                                                                                                                                                           |
| `/export [filename]`      | Exporter la conversation actuelle en texte brut. Avec un nom de fichier, écrit directement dans ce fichier. Sans, ouvre un dialogue pour copier dans le presse-papiers ou enregistrer dans un fichier                                                                     |
| `/extra-usage`            | Configurer l'utilisation supplémentaire pour continuer à travailler lorsque les limites de débit sont atteintes                                                                                                                                                           |
| `/fast [on\|off]`         | Basculer le [mode rapide](/fr/fast-mode) activé ou désactivé                                                                                                                                                                                                              |
| `/feedback [report]`      | Soumettre des commentaires sur Claude Code. Alias : `/bug`                                                                                                                                                                                                                |
| `/fork [name]`            | Créer une fourche de la conversation actuelle à ce stade                                                                                                                                                                                                                  |
| `/help`                   | Afficher l'aide et les commandes disponibles                                                                                                                                                                                                                              |
| `/hooks`                  | Gérer les configurations de [hook](/fr/hooks) pour les événements d'outils                                                                                                                                                                                                |
| `/ide`                    | Gérer les intégrations IDE et afficher l'état                                                                                                                                                                                                                             |
| `/init`                   | Initialiser le projet avec le guide `CLAUDE.md`                                                                                                                                                                                                                           |
| `/insights`               | Générer un rapport analysant vos sessions Claude Code, y compris les domaines de projet, les modèles d'interaction et les points de friction                                                                                                                              |
| `/install-github-app`     | Configurer l'application [Claude GitHub Actions](/fr/github-actions) pour un référentiel. Vous guide dans la sélection d'un référentiel et la configuration de l'intégration                                                                                              |
| `/install-slack-app`      | Installer l'application Claude Slack. Ouvre un navigateur pour terminer le flux OAuth                                                                                                                                                                                     |
| `/keybindings`            | Ouvrir ou créer votre fichier de configuration des liaisons de touches                                                                                                                                                                                                    |
| `/login`                  | Se connecter à votre compte Anthropic                                                                                                                                                                                                                                     |
| `/logout`                 | Se déconnecter de votre compte Anthropic                                                                                                                                                                                                                                  |
| `/mcp`                    | Gérer les connexions de serveur MCP et l'authentification OAuth                                                                                                                                                                                                           |
| `/memory`                 | Modifier les fichiers de mémoire `CLAUDE.md`, activer ou désactiver la [mémoire automatique](/fr/memory#auto-memory) et afficher les entrées de mémoire automatique                                                                                                       |
| `/mobile`                 | Afficher le code QR pour télécharger l'application mobile Claude. Alias : `/ios`, `/android`                                                                                                                                                                              |
| `/model [model]`          | Sélectionner ou changer le modèle IA. Pour les modèles qui le supportent, utilisez les flèches gauche/droite pour [ajuster le niveau d'effort](/fr/model-config#adjust-effort-level). Le changement prend effet immédiatement sans attendre la fin de la réponse actuelle |
| `/passes`                 | Partager une semaine gratuite de Claude Code avec des amis. Visible uniquement si votre compte est éligible                                                                                                                                                               |
| `/permissions`            | Afficher ou mettre à jour les [permissions](/fr/permissions#manage-permissions). Alias : `/allowed-tools`                                                                                                                                                                 |
| `/plan`                   | Entrer directement en mode plan à partir de l'invite                                                                                                                                                                                                                      |
| `/plugin`                 | Gérer les [plugins](/fr/plugins) Claude Code                                                                                                                                                                                                                              |
| `/pr-comments [PR]`       | Récupérer et afficher les commentaires d'une demande de tirage GitHub. Détecte automatiquement la PR pour la branche actuelle, ou passez une URL ou un numéro de PR. Nécessite le CLI `gh`                                                                                |
| `/privacy-settings`       | Afficher et mettre à jour vos paramètres de confidentialité. Disponible uniquement pour les abonnés aux plans Pro et Max                                                                                                                                                  |
| `/release-notes`          | Afficher le journal des modifications complet, avec la version la plus récente la plus proche de votre invite                                                                                                                                                             |
| `/reload-plugins`         | Recharger tous les [plugins](/fr/plugins) actifs pour appliquer les modifications en attente sans redémarrer. Signale ce qui a été chargé et note les modifications qui nécessitent un redémarrage                                                                        |
| `/remote-control`         | Rendre cette session disponible pour le [contrôle à distance](/fr/remote-control) depuis claude.ai. Alias : `/rc`                                                                                                                                                         |
| `/remote-env`             | Configurer l'environnement distant par défaut pour les [sessions de téléportation](/fr/claude-code-on-the-web#teleport-a-web-session-to-your-terminal)                                                                                                                    |
| `/rename [name]`          | Renommer la session actuelle. Sans nom, en génère automatiquement un à partir de l'historique de conversation                                                                                                                                                             |
| `/resume [session]`       | Reprendre une conversation par ID ou nom, ou ouvrir le sélecteur de session. Alias : `/continue`                                                                                                                                                                          |
| `/review`                 | Déprécié. Installez plutôt le [plugin `code-review`](https://github.com/anthropics/claude-code-marketplace/blob/main/code-review/README.md) : `claude plugin install code-review@claude-code-marketplace`                                                                 |
| `/rewind`                 | Rembobiner la conversation et/ou le code à un point antérieur, ou résumer à partir d'un message sélectionné. Consultez [checkpointing](/fr/checkpointing). Alias : `/checkpoint`                                                                                          |
| `/sandbox`                | Basculer le [mode sandbox](/fr/sandboxing). Disponible uniquement sur les plateformes supportées                                                                                                                                                                          |
| `/security-review`        | Analyser les modifications en attente sur la branche actuelle pour les vulnérabilités de sécurité. Examine le diff git et identifie les risques comme l'injection, les problèmes d'authentification et l'exposition de données                                            |
| `/skills`                 | Lister les [skills](/fr/skills) disponibles                                                                                                                                                                                                                               |
| `/stats`                  | Visualiser l'utilisation quotidienne, l'historique des sessions, les séries et les préférences de modèle                                                                                                                                                                  |
| `/status`                 | Ouvrir l'interface Paramètres (onglet Statut) affichant la version, le modèle, le compte et la connectivité                                                                                                                                                               |
| `/statusline`             | Configurer la [ligne d'état](/fr/statusline) de Claude Code. Décrivez ce que vous voulez, ou exécutez sans arguments pour auto-configurer à partir de votre invite shell                                                                                                  |
| `/stickers`               | Commander des autocollants Claude Code                                                                                                                                                                                                                                    |
| `/tasks`                  | Lister et gérer les tâches en arrière-plan                                                                                                                                                                                                                                |
| `/terminal-setup`         | Configurer les liaisons de touches du terminal pour Shift+Entrée et d'autres raccourcis. Visible uniquement dans les terminaux qui en ont besoin, comme VS Code, Alacritty ou Warp                                                                                        |
| `/theme`                  | Changer le thème de couleur. Inclut les variantes claires et sombres, les thèmes accessibles aux daltoniens (daltonisés) et les thèmes ANSI qui utilisent la palette de couleurs de votre terminal                                                                        |
| `/upgrade`                | Ouvrir la page de mise à niveau pour passer à un niveau de plan supérieur                                                                                                                                                                                                 |
| `/usage`                  | Afficher les limites d'utilisation du plan et l'état de la limite de débit                                                                                                                                                                                                |
| `/vim`                    | Basculer entre les modes d'édition Vim et Normal                                                                                                                                                                                                                          |

### Invites MCP

Les serveurs MCP peuvent exposer des invites qui apparaissent comme des commandes. Celles-ci utilisent le format `/mcp__<server>__<prompt>` et sont découvertes dynamiquement à partir des serveurs connectés. Consultez [Invites MCP](/fr/mcp#use-mcp-prompts-as-commands) pour plus de détails.

## Mode éditeur Vim

Activer l'édition de style vim avec la commande `/vim` ou configurer de manière permanente via `/config`.

### Basculement de mode

| Commande | Action                       | Du mode |
| :------- | :--------------------------- | :------ |
| `Esc`    | Entrer en mode NORMAL        | INSERT  |
| `i`      | Insérer avant le curseur     | NORMAL  |
| `I`      | Insérer au début de la ligne | NORMAL  |
| `a`      | Insérer après le curseur     | NORMAL  |
| `A`      | Insérer à la fin de la ligne | NORMAL  |
| `o`      | Ouvrir une ligne en dessous  | NORMAL  |
| `O`      | Ouvrir une ligne au-dessus   | NORMAL  |

### Navigation (mode NORMAL)

| Commande        | Action                                                  |
| :-------------- | :------------------------------------------------------ |
| `h`/`j`/`k`/`l` | Déplacer gauche/bas/haut/droite                         |
| `w`             | Mot suivant                                             |
| `e`             | Fin du mot                                              |
| `b`             | Mot précédent                                           |
| `0`             | Début de la ligne                                       |
| `$`             | Fin de la ligne                                         |
| `^`             | Premier caractère non vide                              |
| `gg`            | Début de l'entrée                                       |
| `G`             | Fin de l'entrée                                         |
| `f{char}`       | Sauter à la prochaine occurrence du caractère           |
| `F{char}`       | Sauter à l'occurrence précédente du caractère           |
| `t{char}`       | Sauter juste avant la prochaine occurrence du caractère |
| `T{char}`       | Sauter juste après l'occurrence précédente du caractère |
| `;`             | Répéter le dernier mouvement f/F/t/T                    |
| `,`             | Répéter le dernier mouvement f/F/t/T en sens inverse    |

<Note>
  En mode normal vim, si le curseur est au début ou à la fin de l'entrée et ne peut pas se déplacer davantage, les touches fléchées naviguent dans l'historique des commandes à la place.
</Note>

### Édition (mode NORMAL)

| Commande       | Action                                  |
| :------------- | :-------------------------------------- |
| `x`            | Supprimer le caractère                  |
| `dd`           | Supprimer la ligne                      |
| `D`            | Supprimer jusqu'à la fin de la ligne    |
| `dw`/`de`/`db` | Supprimer mot/jusqu'à la fin/en arrière |
| `cc`           | Changer la ligne                        |
| `C`            | Changer jusqu'à la fin de la ligne      |
| `cw`/`ce`/`cb` | Changer mot/jusqu'à la fin/en arrière   |
| `yy`/`Y`       | Copier la ligne                         |
| `yw`/`ye`/`yb` | Copier mot/jusqu'à la fin/en arrière    |
| `p`            | Coller après le curseur                 |
| `P`            | Coller avant le curseur                 |
| `>>`           | Indenter la ligne                       |
| `<<`           | Dédenter la ligne                       |
| `J`            | Joindre les lignes                      |
| `.`            | Répéter la dernière modification        |

### Objets texte (mode NORMAL)

Les objets texte fonctionnent avec les opérateurs comme `d`, `c` et `y` :

| Commande  | Action                                     |
| :-------- | :----------------------------------------- |
| `iw`/`aw` | Mot intérieur/autour                       |
| `iW`/`aW` | MOT intérieur/autour (délimité par espace) |
| `i"`/`a"` | Guillemets doubles intérieurs/autour       |
| `i'`/`a'` | Guillemets simples intérieurs/autour       |
| `i(`/`a(` | Parenthèses intérieures/autour             |
| `i[`/`a[` | Crochets intérieurs/autour                 |
| `i{`/`a{` | Accolades intérieures/autour               |

## Historique des commandes

Claude Code maintient l'historique des commandes pour la session actuelle :

* L'historique d'entrée est stocké par répertoire de travail
* L'historique d'entrée se réinitialise lorsque vous exécutez `/clear` pour démarrer une nouvelle session. La conversation de la session précédente est conservée et peut être reprise.
* Utilisez les flèches haut/bas pour naviguer (voir les raccourcis clavier ci-dessus)
* **Remarque** : l'expansion d'historique (`!`) est désactivée par défaut

### Recherche inversée avec Ctrl+R

Appuyez sur `Ctrl+R` pour rechercher de manière interactive dans votre historique de commandes :

1. **Démarrer la recherche** : appuyez sur `Ctrl+R` pour activer la recherche d'historique inversée
2. **Tapez la requête** : entrez le texte à rechercher dans les commandes précédentes. Le terme de recherche est mis en évidence dans les résultats correspondants
3. **Naviguer dans les correspondances** : appuyez à nouveau sur `Ctrl+R` pour parcourir les correspondances plus anciennes
4. **Accepter la correspondance** :
   * Appuyez sur `Tab` ou `Esc` pour accepter la correspondance actuelle et continuer l'édition
   * Appuyez sur `Entrée` pour accepter et exécuter la commande immédiatement
5. **Annuler la recherche** :
   * Appuyez sur `Ctrl+C` pour annuler et restaurer votre entrée d'origine
   * Appuyez sur `Retour arrière` sur une recherche vide pour annuler

La recherche affiche les commandes correspondantes avec le terme de recherche mis en évidence, afin que vous puissiez trouver et réutiliser les entrées précédentes.

## Commandes bash en arrière-plan

Claude Code supporte l'exécution de commandes bash en arrière-plan, vous permettant de continuer à travailler pendant que les processus de longue durée s'exécutent.

### Comment fonctionne la mise en arrière-plan

Lorsque Claude Code exécute une commande en arrière-plan, il exécute la commande de manière asynchrone et retourne immédiatement un ID de tâche en arrière-plan. Claude Code peut répondre à de nouvelles invites pendant que la commande continue à s'exécuter en arrière-plan.

Pour exécuter les commandes en arrière-plan, vous pouvez soit :

* Inviter Claude Code à exécuter une commande en arrière-plan
* Appuyez sur Ctrl+B pour déplacer une invocation d'outil Bash régulière en arrière-plan. (Les utilisateurs Tmux doivent appuyer sur Ctrl+B deux fois en raison de la touche de préfixe de tmux.)

**Caractéristiques clés :**

* La sortie est mise en mémoire tampon et Claude peut la récupérer à l'aide de l'outil TaskOutput
* Les tâches en arrière-plan ont des ID uniques pour le suivi et la récupération de la sortie
* Les tâches en arrière-plan sont automatiquement nettoyées lorsque Claude Code se ferme

Pour désactiver toute la fonctionnalité de tâche en arrière-plan, définissez la variable d'environnement `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` sur `1`. Consultez [Variables d'environnement](/fr/settings#environment-variables) pour plus de détails.

**Commandes couramment mises en arrière-plan :**

* Outils de construction (webpack, vite, make)
* Gestionnaires de paquets (npm, yarn, pnpm)
* Exécuteurs de tests (jest, pytest)
* Serveurs de développement
* Processus de longue durée (docker, terraform)

### Mode Bash avec le préfixe `!`

Exécutez les commandes bash directement sans passer par Claude en préfixant votre entrée avec `!` :

```bash  theme={null}
! npm test
! git status
! ls -la
```

Mode Bash :

* Ajoute la commande et sa sortie au contexte de conversation
* Affiche la progression et la sortie en temps réel
* Supporte la même mise en arrière-plan `Ctrl+B` pour les commandes de longue durée
* Ne nécessite pas que Claude interprète ou approuve la commande
* Supporte l'autocomplétion basée sur l'historique : tapez une commande partielle et appuyez sur **Tab** pour compléter à partir des commandes `!` précédentes du projet actuel
* Quitter avec `Échap`, `Retour arrière` ou `Ctrl+U` sur une invite vide

Ceci est utile pour les opérations shell rapides tout en maintenant le contexte de conversation.

## Suggestions d'invite

Lorsque vous ouvrez d'abord une session, une commande d'exemple grisée apparaît dans l'entrée d'invite pour vous aider à démarrer. Claude Code choisit ceci à partir de l'historique git de votre projet, il reflète donc les fichiers sur lesquels vous avez travaillé récemment.

Après que Claude réponde, les suggestions continuent à apparaître en fonction de votre historique de conversation, comme une étape de suivi d'une demande en plusieurs parties ou une continuation naturelle de votre flux de travail.

* Appuyez sur **Tab** pour accepter la suggestion, ou appuyez sur **Entrée** pour accepter et soumettre
* Commencez à taper pour la rejeter

La suggestion s'exécute comme une demande en arrière-plan qui réutilise le cache d'invite de la conversation parent, le coût supplémentaire est donc minimal. Claude Code ignore la génération de suggestions lorsque le cache est froid pour éviter les coûts inutiles.

Les suggestions sont automatiquement ignorées après le premier tour d'une conversation, en mode non interactif et en mode plan.

Pour désactiver complètement les suggestions d'invite, définissez la variable d'environnement ou basculez le paramètre dans `/config` :

```bash  theme={null}
export CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=false
```

## Questions rapides avec /btw

Utilisez `/btw` pour poser une question rapide sur votre travail actuel sans l'ajouter à l'historique de conversation. Ceci est utile lorsque vous voulez une réponse rapide mais ne voulez pas encombrer le contexte principal ou détourner Claude d'une tâche de longue durée.

```
/btw what was the name of that config file again?
```

Les questions rapides ont une visibilité complète sur la conversation actuelle, vous pouvez donc poser des questions sur le code que Claude a déjà lu, les décisions qu'il a prises plus tôt, ou n'importe quoi d'autre de la session. La question et la réponse sont éphémères : elles apparaissent dans une superposition rejetable et n'entrent jamais dans l'historique de conversation.

* **Disponible pendant que Claude travaille** : vous pouvez exécuter `/btw` même pendant que Claude traite une réponse. La question rapide s'exécute indépendamment et n'interrompt pas le tour principal.
* **Pas d'accès aux outils** : les questions rapides répondent uniquement à partir de ce qui est déjà en contexte. Claude ne peut pas lire les fichiers, exécuter les commandes ou rechercher lors de la réponse à une question rapide.
* **Réponse unique** : il n'y a pas de tours de suivi. Si vous avez besoin d'un aller-retour, utilisez une invite normale à la place.
* **Coût faible** : la question rapide réutilise le cache d'invite de la conversation parent, le coût supplémentaire est donc minimal.

Appuyez sur **Espace**, **Entrée** ou **Échap** pour rejeter la réponse et revenir à l'invite.

`/btw` est l'inverse d'un [subagent](/fr/sub-agents) : il voit votre conversation complète mais n'a pas d'outils, tandis qu'un subagent a tous les outils mais commence avec un contexte vide. Utilisez `/btw` pour poser des questions sur ce que Claude sait déjà de cette session ; utilisez un subagent pour aller découvrir quelque chose de nouveau.

## Liste des tâches

Lorsque vous travaillez sur un travail complexe en plusieurs étapes, Claude crée une liste de tâches pour suivre la progression. Les tâches apparaissent dans la zone d'état de votre terminal avec des indicateurs montrant ce qui est en attente, en cours ou terminé.

* Appuyez sur `Ctrl+T` pour basculer l'affichage de la liste des tâches. L'affichage montre jusqu'à 10 tâches à la fois
* Pour voir toutes les tâches ou les effacer, demandez directement à Claude : « show me all tasks » ou « clear all tasks »
* Les tâches persistent à travers les compactions de contexte, aidant Claude à rester organisé sur les projets plus importants
* Pour partager une liste de tâches entre les sessions, définissez `CLAUDE_CODE_TASK_LIST_ID` pour utiliser un répertoire nommé dans `~/.claude/tasks/` : `CLAUDE_CODE_TASK_LIST_ID=my-project claude`
* Pour revenir à la liste TODO précédente, définissez `CLAUDE_CODE_ENABLE_TASKS=false`.

## Statut de révision PR

Lorsque vous travaillez sur une branche avec une demande de tirage ouverte, Claude Code affiche un lien PR cliquable dans le pied de page (par exemple, « PR #446 »). Le lien a un soulignement coloré indiquant l'état de révision :

* Vert : approuvé
* Jaune : révision en attente
* Rouge : modifications demandées
* Gris : brouillon
* Violet : fusionné

`Cmd+clic` (Mac) ou `Ctrl+clic` (Windows/Linux) sur le lien pour ouvrir la demande de tirage dans votre navigateur. L'état se met à jour automatiquement toutes les 60 secondes.

<Note>
  Le statut PR nécessite que le CLI `gh` soit installé et authentifié (`gh auth login`).
</Note>

## Voir aussi

* [Skills](/fr/skills) - Invites personnalisées et flux de travail
* [Checkpointing](/fr/checkpointing) - Rembobiner les modifications de Claude et restaurer les états précédents
* [Référence CLI](/fr/cli-reference) - Drapeaux et options de ligne de commande
* [Paramètres](/fr/settings) - Options de configuration
* [Gestion de la mémoire](/fr/memory) - Gestion des fichiers CLAUDE.md
