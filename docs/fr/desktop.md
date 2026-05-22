> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Application de bureau

> Tirez le meilleur parti de Claude Code Desktop : sessions parallèles avec isolation Git, disposition des volets par glisser-déposer, terminal intégré et éditeur de fichiers, chats latéraux, utilisation informatique, sessions Dispatch depuis votre téléphone, examen visuel des différences, aperçus d'applications, surveillance des PR, connecteurs et configuration d'entreprise.

L'application Claude Desktop a trois onglets : **Chat** pour les conversations, **Cowork** pour [Dispatch et les travaux agentiques plus longs](https://claude.com/product/cowork), et **Code** pour le développement logiciel. Cette page est la référence pour l'onglet Code.

<CardGroup cols={2}>
  <Card title="Download for macOS" icon="apple" href="https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs">
    Universal build for Intel and Apple Silicon
  </Card>

  <Card title="Download for Windows" icon="windows" href="https://claude.ai/api/desktop/win32/x64/setup/latest/redirect?utm_source=claude_code&utm_medium=docs">
    For x64 processors
  </Card>
</CardGroup>

For Windows ARM64, download the [ARM64 installer](https://claude.ai/api/desktop/win32/arm64/setup/latest/redirect?utm_source=claude_code\&utm_medium=docs). The desktop app is not available on Linux; use the [CLI](/en/quickstart) instead.

Après l'installation, lancez Claude, connectez-vous et cliquez sur l'onglet **Code**. La première fois que vous l'ouvrez sur Windows, vous devez avoir [Git for Windows](https://git-scm.com/downloads/win) installé ; redémarrez l'application après l'installation. Pour une présentation de votre première session, consultez le [guide Démarrer](/fr/desktop-quickstart).

Dans l'onglet Code, chaque conversation est une **session** : elle a son propre historique de chat, dossier de projet et modifications de code, indépendants de toute autre session. La barre latérale répertorie vos sessions et vous permet d'en exécuter plusieurs en parallèle. Au sein d'une session, vous pouvez :

* [Examiner et commenter les différences](#review-changes-with-diff-view), puis [surveiller la PR résultante via CI](#monitor-pull-request-status)
* [Prévisualiser votre application en cours d'exécution](#preview-your-app) dans un navigateur intégré tandis que Claude vérifie ses propres modifications
* [Arranger les volets](#arrange-your-workspace) pour le chat, la différence, l'aperçu, le terminal et l'éditeur de fichiers côte à côte
* Poser une [question latérale](#ask-a-side-question-without-derailing-the-session) qui utilise le contexte de la session sans la dérailler
* [Connecter des outils externes](#connect-external-tools) comme GitHub, Slack et Linear
* Laisser Claude [ouvrir des applications et contrôler votre écran](#let-claude-use-your-computer)
* Exécuter sur votre machine, dans le [cloud](#run-long-running-tasks-remotely), ou via [SSH](#ssh-sessions)

Pour [les travaux récurrents planifiés](/fr/desktop-scheduled-tasks), [les raccourcis clavier](#keyboard-shortcuts), ou [l'envoi de tâches depuis votre téléphone](#sessions-from-dispatch), consultez les pages et sections liées. Si vous utilisez déjà le CLI basé sur le terminal, consultez la [comparaison CLI](#coming-from-the-cli) pour voir ce qui est transféré.

## Démarrer une session

Avant d'envoyer votre premier message, configurez quatre choses dans la zone de prompt :

* **Environnement** : choisissez où Claude s'exécute. Sélectionnez **Local** pour votre machine, **Remote** pour les sessions cloud hébergées par Anthropic, ou une [**connexion SSH**](#ssh-sessions) pour une machine distante que vous gérez. Voir [configuration de l'environnement](#environment-configuration).
* **Dossier du projet** : sélectionnez le dossier ou le référentiel dans lequel Claude travaille. Pour les sessions distantes, vous pouvez ajouter [plusieurs référentiels](#run-long-running-tasks-remotely).
* **Modèle** : choisissez un [modèle](/fr/model-config#available-models) dans la liste déroulante à côté du bouton d'envoi. Vous pouvez modifier ceci pendant la session.
* **Mode de permission** : choisissez le niveau d'autonomie de Claude à partir du [sélecteur de mode](#choose-a-permission-mode). Vous pouvez modifier ceci pendant la session.

Tapez votre tâche et appuyez sur **Entrée** pour démarrer. Chaque session suit son propre contexte et les modifications indépendamment.

## Travailler avec le code

Donnez à Claude le bon contexte, contrôlez le volume de travail qu'il effectue seul et examinez ce qu'il a modifié.

### Utiliser la zone de prompt

Tapez ce que vous voulez que Claude fasse et appuyez sur **Entrée** pour envoyer. Claude lit vos fichiers de projet, effectue des modifications et exécute des commandes en fonction de votre [mode de permission](#choose-a-permission-mode). Vous pouvez rediriger Claude à tout moment : cliquez sur le bouton d'arrêt pour interrompre immédiatement, ou tapez une correction et appuyez sur **Entrée** pour l'envoyer sans arrêter l'action en cours. Claude lit la correction dès que l'action actuelle se termine et s'ajuste avant son étape suivante.

Le bouton **+** à côté de la zone de prompt vous donne accès aux pièces jointes de fichiers, [skills](#use-skills), [connecteurs](#connect-external-tools) et [plugins](#install-plugins).

### Ajouter des fichiers et du contexte aux prompts

La zone de prompt supporte deux façons d'apporter du contexte externe :

* **Fichiers @mention** : tapez `@` suivi d'un nom de fichier pour ajouter un fichier au contexte de la conversation. Claude peut alors lire et référencer ce fichier. @mention n'est pas disponible dans les sessions distantes.
* **Joindre des fichiers** : joignez des images, des PDF et d'autres fichiers à votre prompt en utilisant le bouton de pièce jointe, ou glissez-déposez les fichiers directement dans le prompt. Ceci est utile pour partager des captures d'écran de bugs, des maquettes de conception ou des documents de référence.

### Choisir un mode de permission

Les modes de permission contrôlent le niveau d'autonomie de Claude pendant une session : s'il demande avant de modifier des fichiers, d'exécuter des commandes ou les deux. Vous pouvez changer de mode à tout moment en utilisant le sélecteur de mode à côté du bouton d'envoi. Commencez par Demander les permissions pour voir exactement ce que Claude fait, puis passez à Accepter automatiquement les modifications ou Plan mode à mesure que vous vous sentez à l'aise.

| Mode                                           | Clé de paramètres   | Comportement                                                                                                                                                                                                                                                                                                                                                         |
| ---------------------------------------------- | ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Demander les permissions**                   | `default`           | Claude demande avant de modifier des fichiers ou d'exécuter des commandes. Vous voyez une différence et pouvez accepter ou rejeter chaque modification. Recommandé pour les nouveaux utilisateurs.                                                                                                                                                                   |
| **Accepter automatiquement les modifications** | `acceptEdits`       | Claude accepte automatiquement les modifications de fichiers et les commandes courantes du système de fichiers comme `mkdir`, `touch` et `mv`, mais demande toujours avant d'exécuter les autres commandes du terminal. Utilisez ceci quand vous faites confiance aux modifications de fichiers et voulez une itération plus rapide.                                 |
| **Plan mode**                                  | `plan`              | Claude lit les fichiers et exécute les commandes pour explorer, puis propose un plan sans modifier votre code source. Bon pour les tâches complexes où vous voulez examiner l'approche en premier.                                                                                                                                                                   |
| **Auto**                                       | `auto`              | Claude exécute toutes les actions avec des vérifications de sécurité en arrière-plan qui vérifient l'alignement avec votre demande. Réduit les invites de permission tout en maintenant la surveillance. Activez dans vos Paramètres → Claude Code. Voir [conditions de disponibilité](#auto-mode-availability) ci-dessous.                                          |
| **Contourner les permissions**                 | `bypassPermissions` | Claude s'exécute sans aucune invite de permission, équivalent à `--dangerously-skip-permissions` dans la CLI. Activez dans vos Paramètres → Claude Code sous « Autoriser le mode de contournement des permissions ». Utilisez uniquement dans les conteneurs sandboxés ou les machines virtuelles. Les administrateurs d'entreprise peuvent désactiver cette option. |

Le mode de permission `dontAsk` est disponible uniquement dans la [CLI](/fr/permission-modes#allow-only-pre-approved-tools-with-dontask-mode).

<span id="auto-mode-availability" />

Auto mode est un aperçu de recherche disponible à tous les utilisateurs sur l'API Anthropic. Il n'est pas disponible sur les fournisseurs tiers. Il nécessite Claude Sonnet 4.6, Opus 4.6 ou Opus 4.7.

<Tip title="Bonne pratique">
  Commencez les tâches complexes en Plan mode pour que Claude trace une approche avant de faire des modifications. Une fois que vous approuvez le plan, passez à Accepter automatiquement les modifications ou Demander les permissions pour l'exécuter. Voir [explorer d'abord, puis planifier, puis coder](/fr/best-practices#explore-first-then-plan-then-code) pour plus d'informations sur ce flux de travail.
</Tip>

Les sessions distantes supportent Accepter automatiquement les modifications et Plan mode. Demander les permissions n'est pas disponible car les sessions distantes acceptent automatiquement les modifications de fichiers par défaut, et Contourner les permissions n'est pas disponible car l'environnement distant est déjà sandboxé.

Les administrateurs d'entreprise peuvent restreindre les modes de permission disponibles. Voir [configuration d'entreprise](#enterprise-configuration) pour les détails.

### Aperçu de votre application

Claude peut démarrer un serveur de développement et ouvrir un navigateur intégré pour vérifier ses modifications. Ceci fonctionne pour les applications web frontend ainsi que les serveurs backend : Claude peut tester les points de terminaison API, afficher les journaux du serveur et itérer sur les problèmes qu'il trouve. Dans la plupart des cas, Claude démarre le serveur automatiquement après la modification des fichiers du projet. Vous pouvez également demander à Claude de prévisualiser à tout moment. Par défaut, Claude [vérifie automatiquement](#auto-verify-changes) les modifications après chaque modification.

Le volet d'aperçu peut également ouvrir des fichiers HTML statiques, des PDF, des images et des vidéos de votre projet. Cliquez sur un chemin HTML, PDF, image ou vidéo dans le chat pour l'ouvrir dans l'aperçu.

À partir du volet d'aperçu, vous pouvez :

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

Utilisez les bascules **Correction automatique** et **Fusion automatique** dans la barre d'état CI pour activer l'une ou l'autre option. Claude Code envoie également une notification de bureau quand CI se termine. Pour archiver la session automatiquement une fois que la PR fusionne ou se ferme, activez [auto-archive](#work-in-parallel-with-sessions) dans Paramètres → Claude Code.

<Note>
  La surveillance des PR nécessite que la [CLI GitHub (`gh`)](https://cli.github.com/) soit installée et authentifiée sur votre machine. Si `gh` n'est pas installée, Desktop vous invite à l'installer la première fois que vous essayez de créer une PR.
</Note>

## Arranger votre espace de travail

L'onglet Code est construit autour de volets que vous pouvez arranger dans n'importe quelle disposition : chat, différence, aperçu, terminal, fichier, plan, tâches et sous-agent. Glissez un volet par son en-tête pour le repositionner, ou glissez un bord de volet pour le redimensionner. Appuyez sur **Cmd+\\** sur macOS ou **Ctrl+\\** sur Windows pour fermer le volet actif. Ouvrez des volets supplémentaires à partir du menu **Vues** dans la barre d'outils de la session.

<Note>
  La disposition des volets, le terminal, l'éditeur de fichiers et les modes d'affichage dans cette section nécessitent Claude Desktop v1.2581.0 ou une version ultérieure. Ouvrez **Claude → Vérifier les mises à jour** sur macOS ou **Aide → Vérifier les mises à jour** sur Windows pour mettre à jour.
</Note>

### Exécuter les commandes dans le terminal

Le terminal intégré vous permet d'exécuter les commandes aux côtés de votre session sans basculer vers une autre application. Ouvrez-le à partir du menu **Vues** ou appuyez sur **Ctrl+\`** sur macOS ou Windows. Le terminal s'ouvre dans le répertoire de travail de votre session et partage le même environnement que Claude, donc les commandes comme `npm test` ou `git status` voient les mêmes fichiers que Claude édite. Pour ouvrir un deuxième onglet de terminal, cliquez sur **+** dans l'en-tête du volet de terminal ou cliquez avec le bouton droit sur un dossier dans le chat pour choisir **Ouvrir dans le terminal**. Le terminal est disponible dans les sessions locales uniquement.

### Ouvrir et modifier les fichiers

Cliquez sur un chemin de fichier dans le chat ou la visionneuse de différences pour l'ouvrir dans le volet de fichier. Les chemins HTML, PDF, image et vidéo s'ouvrent dans le [volet d'aperçu](#preview-your-app) à la place. Effectuez des modifications ponctuelles et cliquez sur **Enregistrer** pour les écrire. Si le fichier a changé sur le disque depuis que vous l'avez ouvert, le volet vous avertit et vous permet de remplacer ou d'abandonner. Cliquez sur **Abandonner** pour annuler vos modifications, ou cliquez sur le chemin dans l'en-tête du volet pour copier le chemin absolu.

Le volet de fichier est disponible dans les sessions locales et SSH. Pour les sessions distantes, demandez à Claude de faire la modification.

### Ouvrir les fichiers dans d'autres applications

Cliquez avec le bouton droit sur n'importe quel chemin de fichier dans le chat, la visionneuse de différences ou le volet de fichier pour ouvrir un menu contextuel :

* **Joindre comme contexte** : ajouter le fichier à votre prochain prompt
* **Ouvrir dans** : ouvrir le fichier dans un éditeur installé comme VS Code, Cursor ou Zed
* **Afficher dans le Finder** sur macOS, **Afficher dans l'Explorateur** sur Windows : ouvrir le dossier contenant
* **Copier le chemin** : copier le chemin absolu dans votre presse-papiers

### Changer les modes d'affichage

Les modes d'affichage contrôlent le niveau de détail qui apparaît dans la transcription du chat. Changez les modes à partir de la liste déroulante **Vue de la transcription** à côté du bouton d'envoi, ou appuyez sur **Ctrl+O** sur macOS ou Windows pour les parcourir.

| Mode        | Ce qu'il affiche                                                                 |
| ----------- | -------------------------------------------------------------------------------- |
| **Normal**  | Les appels d'outils réduits en résumés, avec les réponses texte complètes        |
| **Verbose** | Chaque appel d'outil, lecture de fichier et étape intermédiaire que Claude prend |
| **Résumé**  | Uniquement les réponses finales de Claude et les modifications qu'il a apportées |

Utilisez Verbose lors du débogage pour savoir pourquoi Claude a pris une action particulière. Utilisez Résumé quand vous exécutez plusieurs sessions et voulez scanner les résultats rapidement.

### Raccourcis clavier

Appuyez sur **Cmd+/** sur macOS ou **Ctrl+/** sur Windows pour voir tous les raccourcis disponibles dans l'onglet Code. Sur Windows, utilisez **Ctrl** à la place de **Cmd** pour les raccourcis ci-dessous. Le cycle des sessions, le basculement du terminal et le basculement du mode d'affichage utilisent **Ctrl** sur chaque plateforme.

| Raccourci                             | Action                                      |
| ------------------------------------- | ------------------------------------------- |
| `Cmd` `/`                             | Afficher les raccourcis clavier             |
| `Cmd` `N`                             | Nouvelle session                            |
| `Cmd` `W`                             | Fermer la session                           |
| `Ctrl` `Tab` / `Ctrl` `Shift` `Tab`   | Session suivante ou précédente              |
| `Cmd` `Shift` `]` / `Cmd` `Shift` `[` | Session suivante ou précédente              |
| `Esc`                                 | Arrêter la réponse de Claude                |
| `Cmd` `Shift` `D`                     | Basculer le volet de différence             |
| `Cmd` `Shift` `P`                     | Basculer le volet d'aperçu                  |
| `Cmd` `Shift` `S`                     | Sélectionner un élément dans l'aperçu       |
| `Ctrl` `` ` ``                        | Basculer le volet de terminal               |
| `Cmd` `\`                             | Fermer le volet actif                       |
| `Cmd` `;`                             | Ouvrir le chat latéral                      |
| `Ctrl` `O`                            | Parcourir les modes d'affichage             |
| `Cmd` `Shift` `M`                     | Ouvrir le menu du mode de permission        |
| `Cmd` `Shift` `I`                     | Ouvrir le menu du modèle                    |
| `Cmd` `Shift` `E`                     | Ouvrir le menu d'effort                     |
| `1`–`9`                               | Sélectionner un élément dans un menu ouvert |

Ces raccourcis s'appliquent uniquement à l'onglet Code. Les raccourcis du [mode interactif](/fr/interactive-mode#keyboard-shortcuts) basés sur le terminal, comme `Shift+Tab` pour parcourir les modes, ne s'appliquent pas dans Desktop.

### Vérifier l'utilisation

Cliquez sur l'anneau d'utilisation à côté du sélecteur de modèle pour voir votre utilisation actuelle de la fenêtre de contexte et votre utilisation du plan pour la période. L'utilisation du contexte est par session ; l'utilisation du plan est partagée sur toutes vos surfaces Claude Code.

## Laisser Claude utiliser votre ordinateur

L'utilisation informatique permet à Claude d'ouvrir vos applications, de contrôler votre écran et de travailler directement sur votre machine comme vous le feriez. Demandez à Claude de tester une application native dans un simulateur mobile, d'interagir avec un outil de bureau qui n'a pas de CLI, ou d'automatiser quelque chose qui ne fonctionne que via une GUI.

<Note>
  L'utilisation informatique est un aperçu de recherche sur macOS et Windows qui nécessite un plan Pro ou Max. Elle n'est pas disponible sur les plans Team ou Enterprise. L'application Claude Desktop doit être en cours d'exécution.
</Note>

L'utilisation informatique est désactivée par défaut. [Activez-la dans Paramètres](#enable-computer-use) avant que Claude puisse contrôler votre écran. Sur macOS, vous devez également accorder les permissions d'Accessibilité et d'Enregistrement d'écran.

<Warning>
  Contrairement à l'[outil Bash sandboxé](/fr/sandboxing), l'utilisation informatique s'exécute sur votre vrai bureau avec accès à tout ce que vous approuvez. Claude vérifie chaque action et signale les injections de prompt potentielles du contenu à l'écran, mais la limite de confiance est différente. Voir le [guide de sécurité de l'utilisation informatique](https://support.claude.com/en/articles/14128542) pour les meilleures pratiques.
</Warning>

### Quand l'utilisation informatique s'applique

Claude a plusieurs façons d'interagir avec une application ou un service, et l'utilisation informatique est la plus large et la plus lente. Il essaie d'abord l'outil le plus précis :

* Si vous avez un [connecteur](#connect-external-tools) pour un service, Claude utilise le connecteur.
* Si la tâche est une commande shell, Claude utilise Bash.
* Si la tâche est du travail de navigateur et que vous avez [Claude dans Chrome](/fr/chrome) configuré, Claude utilise cela.
* Si aucun de ceux-ci ne s'applique, Claude utilise l'utilisation informatique.

Les [niveaux d'accès par application](#app-permissions) renforcent ceci : les navigateurs sont limités à la lecture seule, et les terminaux et IDE à clic uniquement, guidant Claude vers l'outil dédié même quand l'utilisation informatique est active. Le contrôle d'écran est réservé aux choses que rien d'autre ne peut atteindre, comme les applications natives, les panneaux de contrôle matériel, les simulateurs mobiles ou les outils propriétaires sans API.

### Activer l'utilisation informatique

L'utilisation informatique est désactivée par défaut. Si vous demandez à Claude de faire quelque chose qui en a besoin alors qu'elle est désactivée, Claude vous dit qu'il pourrait faire la tâche si vous activez l'utilisation informatique dans Paramètres.

<Steps>
  <Step title="Mettre à jour l'application de bureau">
    Assurez-vous que vous avez la dernière version de Claude Desktop. Téléchargez ou mettez à jour sur [claude.com/download](https://claude.com/download), puis redémarrez l'application.
  </Step>

  <Step title="Activer le basculement">
    Dans l'application de bureau, allez à **Paramètres > Général** (sous **Application de bureau**). Trouvez le basculement **Utilisation informatique** et activez-le. Sur Windows, le basculement prend effet immédiatement et la configuration est complète. Sur macOS, continuez à l'étape suivante.

    Si vous ne voyez pas le basculement, confirmez que vous êtes sur macOS ou Windows avec un plan Pro ou Max, puis mettez à jour et redémarrez l'application.
  </Step>

  <Step title="Accorder les permissions macOS">
    Sur macOS, accordez deux permissions système avant que le basculement prenne effet :

    * **Accessibilité** : permet à Claude de cliquer, taper et faire défiler
    * **Enregistrement d'écran** : permet à Claude de voir ce qui est sur votre écran

    La page Paramètres affiche l'état actuel de chaque permission. Si l'une est refusée, cliquez sur le badge pour ouvrir le volet Paramètres système pertinent.
  </Step>
</Steps>

### Permissions d'application

La première fois que Claude doit utiliser une application, une invite apparaît dans votre session. Cliquez sur **Autoriser pour cette session** ou **Refuser**. Les approbations durent pour la session actuelle, ou 30 minutes dans les [sessions générées par Dispatch](#sessions-from-dispatch).

L'invite affiche également quel niveau de contrôle Claude obtient pour cette application. Ces niveaux sont fixés par catégorie d'application et ne peuvent pas être modifiés :

| Niveau           | Ce que Claude peut faire                                                    | S'applique à                        |
| :--------------- | :-------------------------------------------------------------------------- | :---------------------------------- |
| Lecture seule    | Voir l'application dans les captures d'écran                                | Navigateurs, plateformes de trading |
| Clic uniquement  | Cliquer et faire défiler, mais pas taper ou utiliser les raccourcis clavier | Terminaux, IDE                      |
| Contrôle complet | Cliquer, taper, glisser et utiliser les raccourcis clavier                  | Tout le reste                       |

Les applications avec une large portée, comme les terminaux, Finder ou Explorateur de fichiers, et Paramètres système ou Paramètres, affichent un avertissement supplémentaire dans l'invite pour que vous sachiez ce que l'approbation accorde.

Vous pouvez configurer deux paramètres dans **Paramètres > Général** (sous **Application de bureau**) :

* **Applications refusées** : ajoutez des applications ici pour les rejeter sans demander. Claude peut toujours affecter une application refusée indirectement via des actions dans une application autorisée, mais il ne peut pas interagir directement avec l'application refusée.
* **Afficher les applications quand Claude a terminé** : tandis que Claude travaille, vos autres fenêtres sont masquées pour qu'il n'interagisse qu'avec l'application approuvée. Quand Claude a terminé, les fenêtres masquées sont restaurées sauf si vous désactivez ce paramètre.

## Gérer les sessions

Chaque session est une conversation indépendante avec son propre contexte et ses propres modifications. Vous pouvez exécuter plusieurs sessions en parallèle, créer des chats latéraux, envoyer du travail vers le cloud ou laisser Dispatch démarrer des sessions pour vous depuis votre téléphone.

### Travailler en parallèle avec les sessions

Cliquez sur **+ Nouvelle session** dans la barre latérale, ou appuyez sur **Cmd+N** sur macOS ou **Ctrl+N** sur Windows, pour travailler sur plusieurs tâches en parallèle. Appuyez sur **Ctrl+Tab** et **Ctrl+Shift+Tab** pour parcourir les sessions dans la barre latérale. Pour les référentiels Git, chaque session obtient sa propre copie isolée de votre projet en utilisant [Git worktrees](/fr/worktrees), donc les modifications dans une session n'affectent pas les autres sessions jusqu'à ce que vous les validiez.

Pour afficher deux sessions à la fois, maintenez **Cmd** sur macOS ou **Ctrl** sur Windows et cliquez sur une session dans la barre latérale. La session s'ouvre dans un deuxième volet à côté de celui que vous avez déjà ouvert. Pendant que la division est active, cliquer sur une autre session de la barre latérale remplace le volet qui a le focus. Appuyez sur **Cmd+\\** sur macOS ou **Ctrl+\\** sur Windows pour fermer le volet actif et revenir à une seule session.

Les worktrees sont stockés dans `<project-root>/.claude/worktrees/` par défaut. Vous pouvez modifier ceci en un répertoire personnalisé dans Paramètres → Claude Code sous « Emplacement du worktree ». Vous pouvez également définir un préfixe de branche qui est ajouté au début de chaque nom de branche worktree, ce qui est utile pour garder les branches créées par Claude organisées. Pour supprimer un worktree quand vous avez terminé, survolez la session dans la barre latérale et cliquez sur l'icône d'archive. Pour avoir les sessions s'archiver elles-mêmes quand leur demande de tirage fusionne ou se ferme, activez **Auto-archive après fusion ou fermeture de PR** dans Paramètres → Claude Code. L'auto-archive s'applique uniquement aux sessions locales qui ont terminé l'exécution.

Pour inclure les fichiers ignorés par git comme `.env` dans les nouveaux worktrees, créez un [fichier `.worktreeinclude`](/fr/worktrees#copy-gitignored-files-into-worktrees) à la racine de votre projet.

<Note>
  L'isolation des sessions nécessite [Git](https://git-scm.com/downloads). La plupart des Macs incluent Git par défaut. Exécutez `git --version` dans Terminal pour vérifier. Sur Windows, Git est requis pour que l'onglet Code fonctionne : [téléchargez Git pour Windows](https://git-scm.com/downloads/win), installez-le et redémarrez l'application. Si vous rencontrez des erreurs Git, demandez à Claude dans l'[onglet Cowork](https://claude.com/product/cowork) de vous aider à dépanner votre configuration.
</Note>

Utilisez les contrôles en haut de la barre latérale pour filtrer les sessions par statut, projet ou environnement, et pour grouper les sessions par projet. Pour renommer une session, cliquez sur le titre de la session dans la barre d'outils en haut de la session active. Pour vérifier l'utilisation du contexte, voir [Vérifier l'utilisation](#check-usage). Quand le contexte se remplit, Claude résume automatiquement la conversation et continue de travailler. Vous pouvez également taper `/compact` pour déclencher la compaction plus tôt et libérer de l'espace de contexte. Voir [la fenêtre de contexte](/fr/how-claude-code-works#the-context-window) pour les détails sur le fonctionnement de la compaction.

L'application de bureau envoie une notification du système d'exploitation quand une session Code termine une tâche et que vous ne visualisez pas actuellement cette session.

### Poser une question latérale sans dérailler la session

Un chat latéral vous permet de poser une question à Claude qui utilise le contexte de votre session mais n'ajoute rien à la conversation principale. Utilisez-le quand vous voulez comprendre un morceau de code, vérifier une hypothèse ou explorer une idée sans détourner la session de son cours.

Appuyez sur **Cmd+;** sur macOS ou **Ctrl+;** sur Windows pour ouvrir un chat latéral, ou tapez `/btw` dans la zone de prompt. Le chat latéral peut lire tout ce qui se trouve dans le fil principal jusqu'à ce point. Quand vous avez terminé, fermez le chat latéral et continuez la session principale où vous l'aviez laissée. Les chats latéraux sont disponibles dans les sessions locales et SSH.

### Regarder les tâches en arrière-plan

Le volet des tâches affiche le travail en arrière-plan s'exécutant dans la session actuelle : sous-agents, commandes shell en arrière-plan et flux de travail. Ouvrez-le à partir du menu **Vues** ou glissez-le dans votre disposition.

Cliquez sur n'importe quelle entrée pour voir sa sortie dans le volet du sous-agent ou l'arrêter. Pour voir ce que font les autres sessions, utilisez la [barre latérale](#work-in-parallel-with-sessions).

### Exécuter les tâches longues à distance

Pour les refactorisations importantes, les suites de tests, les migrations ou autres tâches longues, sélectionnez **Remote** au lieu de **Local** au démarrage d'une session. Les sessions distantes s'exécutent sur l'infrastructure cloud d'Anthropic et continuent même si vous fermez l'application ou arrêtez votre ordinateur. Revenez à tout moment pour voir la progression ou orienter Claude dans une direction différente. Vous pouvez également surveiller les sessions distantes à partir de [claude.ai/code](https://claude.ai/code) ou de l'application Claude iOS.

Les sessions distantes supportent également plusieurs référentiels. Après avoir sélectionné un environnement cloud, cliquez sur le bouton **+** à côté de la pilule de référentiel pour ajouter des référentiels supplémentaires à la session. Chaque référentiel obtient son propre sélecteur de branche. Ceci est utile pour les tâches qui s'étendent sur plusieurs bases de code, comme la mise à jour d'une bibliothèque partagée et ses consommateurs.

Voir [Claude Code sur le web](/fr/claude-code-on-the-web) pour plus d'informations sur le fonctionnement des sessions distantes.

### Continuer sur une autre surface

Le menu **Continuer dans**, accessible à partir de l'icône VS Code en bas à droite de la barre d'outils de la session, vous permet de déplacer votre session vers une autre surface :

* **Claude Code sur le Web** : envoie votre session locale pour continuer à s'exécuter à distance. Desktop pousse votre branche, génère un résumé de la conversation et crée une nouvelle session distante avec le contexte complet. Vous pouvez ensuite choisir d'archiver la session locale ou de la conserver. Ceci nécessite un arbre de travail propre et n'est pas disponible pour les sessions SSH.
* **Votre IDE** : ouvre votre projet dans un IDE supporté au répertoire de travail actuel.

### Sessions depuis Dispatch

[Dispatch](https://support.claude.com/en/articles/13947068) est une conversation persistante avec Claude qui vit dans l'onglet [Cowork](https://claude.com/product/cowork#dispatch-and-computer-use). Vous envoyez un message à Dispatch avec une tâche, et il décide comment la gérer.

Une tâche peut devenir une session Code de deux façons : vous en demandez une directement, comme « ouvrir une session Claude Code et corriger le bug de connexion », ou Dispatch décide que la tâche est du travail de développement et en génère une automatiquement. Les tâches qui routent généralement vers Code incluent la correction de bugs, la mise à jour des dépendances, l'exécution de tests ou l'ouverture de demandes de tirage. La recherche, l'édition de documents et le travail sur feuille de calcul restent dans Cowork.

De toute façon, la session Code apparaît dans la barre latérale de l'onglet Code avec un badge **Dispatch**. Vous recevez une notification push sur votre téléphone quand elle se termine ou a besoin de votre approbation.

Si vous avez [l'utilisation informatique](#let-claude-use-your-computer) activée, les sessions Code générées par Dispatch peuvent l'utiliser aussi. Les approbations d'application dans ces sessions expirent après 30 minutes et re-demandent, plutôt que de durer la session complète comme les sessions Code régulières.

Pour la configuration, l'appairage et les paramètres Dispatch, voir l'[article d'aide Dispatch](https://support.claude.com/en/articles/13947068). Dispatch nécessite un plan Pro ou Max et n'est pas disponible sur les plans Team ou Enterprise.

Dispatch est l'une de plusieurs façons de travailler avec Claude quand vous êtes loin de votre terminal. Voir [Plateformes et intégrations](/fr/platforms#work-when-you-are-away-from-your-terminal) pour le comparer avec Remote Control, Channels, Slack et les tâches planifiées.

## Étendre Claude Code

Connectez les services externes, ajoutez des flux de travail réutilisables, personnalisez le comportement de Claude et configurez les serveurs d'aperçu. Pour gérer les connecteurs, les skills et les plugins au même endroit, cliquez sur **Personnaliser** dans la barre latérale.

### Connecter les outils externes

Pour les sessions locales et [SSH](#ssh-sessions), cliquez sur le bouton **+** à côté de la zone de prompt et sélectionnez **Connecteurs** pour ajouter des intégrations comme Google Calendar, Slack, GitHub, Linear, Notion et bien d'autres. Vous pouvez ajouter des connecteurs avant ou pendant une session. Le bouton **+** n'est pas disponible dans les sessions distantes, mais les [routines](/fr/routines) configurent les connecteurs au moment de la création de la routine.

Pour gérer ou déconnecter les connecteurs, allez à Paramètres → Connecteurs dans l'application de bureau, ou sélectionnez **Gérer les connecteurs** à partir du menu Connecteurs dans la zone de prompt.

Une fois connecté, Claude peut lire votre calendrier, envoyer des messages, créer des problèmes et interagir avec vos outils directement. Vous pouvez demander à Claude quels connecteurs sont configurés dans votre session.

Les connecteurs sont [des serveurs MCP](/fr/mcp) avec un flux de configuration graphique. Utilisez-les pour une intégration rapide avec les services supportés. Pour les intégrations non listées dans Connecteurs, ajoutez les serveurs MCP manuellement via [fichiers de paramètres](/fr/mcp#installing-mcp-servers). Vous pouvez également [créer des connecteurs personnalisés](https://support.claude.com/en/articles/11175166-getting-started-with-custom-connectors-using-remote-mcp).

### Utiliser les skills

[Les skills](/fr/skills) étendent ce que Claude peut faire. Claude les charge automatiquement quand ils sont pertinents, ou vous pouvez en invoquer un directement : tapez `/` dans la zone de prompt ou cliquez sur le bouton **+** et sélectionnez **Slash commands** pour parcourir ce qui est disponible. Ceci inclut [les commandes intégrées](/fr/commands), vos [skills personnalisés](/fr/skills#create-your-first-skill), les skills du projet à partir de votre base de code et les skills de tout [plugin installé](/fr/plugins). Sélectionnez-en un et il apparaît en surbrillance dans le champ d'entrée. Tapez votre tâche après et envoyez comme d'habitude.

### Installer les plugins

[Les plugins](/fr/plugins) sont des packages réutilisables qui ajoutent des skills, des agents, des hooks, des serveurs MCP et des configurations LSP à Claude Code. Vous pouvez installer les plugins à partir de l'application de bureau sans utiliser le terminal.

Pour les sessions locales et [SSH](#ssh-sessions), cliquez sur le bouton **+** à côté de la zone de prompt et sélectionnez **Plugins** pour voir vos plugins installés et leurs skills. Pour ajouter un plugin, sélectionnez **Ajouter un plugin** à partir du sous-menu pour ouvrir le navigateur de plugins, qui affiche les plugins disponibles à partir de vos [marketplaces](/fr/plugin-marketplaces) configurés, y compris le marketplace officiel d'Anthropic. Sélectionnez **Gérer les plugins** pour activer, désactiver ou désinstaller les plugins.

Les plugins peuvent être limités à votre compte utilisateur, un projet spécifique ou local uniquement. Si votre organisation gère les plugins de manière centralisée, ces plugins sont disponibles dans les sessions de bureau de la même manière qu'ils le sont dans la CLI. Les plugins ne sont pas disponibles pour les sessions distantes. Pour la référence complète des plugins, y compris la création de vos propres plugins, voir [plugins](/fr/plugins).

### Configurer les serveurs d'aperçu

Claude détecte automatiquement votre configuration de serveur de développement et stocke la configuration dans `.claude/launch.json` à la racine du dossier que vous avez sélectionné au démarrage de la session. L'aperçu utilise ce dossier comme répertoire de travail, donc si vous avez sélectionné un dossier parent, les sous-dossiers avec leurs propres serveurs de développement ne seront pas détectés automatiquement. Pour travailler avec le serveur d'un sous-dossier, soit démarrez une session dans ce dossier directement, soit ajoutez une configuration manuellement.

Pour personnaliser le démarrage de votre serveur, par exemple pour utiliser `yarn dev` au lieu de `npm run dev` ou pour modifier le port, modifiez le fichier manuellement ou cliquez sur **Modifier la configuration** dans la liste déroulante Aperçu pour l'ouvrir dans votre éditeur de code. Le fichier supporte JSON avec commentaires.

```json theme={null}
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

```json theme={null}
{
  "version": "0.0.1",
  "autoVerify": false,
  "configurations": [...]
}
```

Quand désactivée, les outils d'aperçu sont toujours disponibles et vous pouvez demander à Claude de vérifier à tout moment. La vérification automatique la rend automatique après chaque modification.

#### Champs de configuration

Chaque entrée dans le tableau `configurations` accepte les champs suivants :

| Champ               | Type      | Description                                                                                                                                                                                                                                                                                                                           |
| ------------------- | --------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`              | string    | Un identifiant unique pour ce serveur                                                                                                                                                                                                                                                                                                 |
| `runtimeExecutable` | string    | La commande à exécuter, comme `npm`, `yarn` ou `node`                                                                                                                                                                                                                                                                                 |
| `runtimeArgs`       | string\[] | Arguments passés à `runtimeExecutable`, comme `["run", "dev"]`                                                                                                                                                                                                                                                                        |
| `port`              | number    | Le port sur lequel votre serveur écoute. Par défaut 3000                                                                                                                                                                                                                                                                              |
| `cwd`               | string    | Répertoire de travail relatif à la racine de votre projet. Par défaut la racine du projet. Utilisez `${workspaceFolder}` pour référencer la racine du projet explicitement                                                                                                                                                            |
| `env`               | object    | Variables d'environnement supplémentaires comme paires clé-valeur, comme `{ "NODE_ENV": "development" }`. Ne mettez pas de secrets ici car ce fichier est validé dans votre référentiel. Pour passer les secrets à votre serveur de développement, définissez-les dans l'[éditeur d'environnement local](#local-sessions) à la place. |
| `autoPort`          | boolean   | Comment gérer les conflits de port. Voir ci-dessous                                                                                                                                                                                                                                                                                   |
| `program`           | string    | Un script à exécuter avec `node`. Voir [quand utiliser `program` vs `runtimeExecutable`](#when-to-use-program-vs-runtimeexecutable)                                                                                                                                                                                                   |
| `args`              | string\[] | Arguments passés à `program`. Utilisé uniquement quand `program` est défini                                                                                                                                                                                                                                                           |

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

    ```json theme={null}
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

    ```json theme={null}
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

    ```json theme={null}
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

## Configuration de l'environnement

L'environnement que vous choisissez au [démarrage d'une session](#start-a-session) détermine où Claude s'exécute et comment vous vous connectez :

* **Local** : s'exécute sur votre machine avec accès direct à vos fichiers
* **Remote** : s'exécute sur l'infrastructure cloud d'Anthropic. Les sessions continuent même si vous fermez l'application.
* **SSH** : s'exécute sur une machine distante à laquelle vous vous connectez via SSH, comme vos propres serveurs, des machines virtuelles cloud ou des conteneurs de développement

### Sessions locales

L'application de bureau n'hérite pas toujours de votre environnement shell complet. Sur macOS, quand vous lancez l'application à partir du Dock ou du Finder, elle lit votre profil shell, comme `~/.zshrc` ou `~/.bashrc`, pour extraire `PATH` et un ensemble fixe de variables Claude Code, mais les autres variables que vous exportez là ne sont pas récupérées. Sur Windows, l'application hérite des variables d'environnement utilisateur et système mais ne lit pas les profils PowerShell.

Pour définir les variables d'environnement pour les sessions locales et les serveurs de développement sur n'importe quelle plateforme, ouvrez la liste déroulante d'environnement dans la zone de prompt, survolez **Local** et cliquez sur l'icône d'engrenage pour ouvrir l'éditeur d'environnement local. Les variables que vous enregistrez ici sont stockées chiffrées sur votre machine et s'appliquent à chaque session locale et serveur d'aperçu que vous démarrez. Vous pouvez également ajouter des variables à la clé `env` dans votre fichier `~/.claude/settings.json`, bien que celles-ci n'atteignent que les sessions Claude et non les serveurs de développement. Voir [variables d'environnement](/fr/env-vars) pour la liste complète des variables supportées.

[La réflexion étendue](/fr/model-config#extended-thinking) est activée par défaut, ce qui améliore les performances sur les tâches de raisonnement complexe mais utilise des tokens supplémentaires. Pour désactiver complètement la réflexion, définissez `MAX_THINKING_TOKENS` à `0` dans l'éditeur d'environnement local. Sur les modèles avec [raisonnement adaptatif](/fr/model-config#adjust-effort-level), toute autre valeur `MAX_THINKING_TOKENS` est ignorée car le raisonnement adaptatif contrôle la profondeur de la réflexion à la place. Sur Opus 4.6 et Sonnet 4.6, définissez `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` à `1` pour utiliser un budget de réflexion fixe ; Opus 4.7 utilise toujours le raisonnement adaptatif et n'a pas de mode de budget fixe.

### Sessions distantes

Les sessions distantes continuent en arrière-plan même si vous fermez l'application. L'utilisation compte vers les limites de votre [plan d'abonnement](/fr/costs) sans frais de calcul séparés.

Vous pouvez créer des environnements cloud personnalisés avec différents niveaux d'accès réseau et variables d'environnement. Sélectionnez la liste déroulante d'environnement au démarrage d'une session distante et choisissez **Ajouter un environnement**. Voir [l'environnement cloud](/fr/claude-code-on-the-web#the-cloud-environment) pour les détails sur la configuration de l'accès réseau et des variables d'environnement.

### Sessions SSH

Les sessions SSH vous permettent d'exécuter Claude Code sur une machine distante tout en utilisant l'application de bureau comme votre interface. Ceci est utile pour travailler avec des bases de code qui vivent sur des machines virtuelles cloud, des conteneurs de développement ou des serveurs avec du matériel ou des dépendances spécifiques.

Pour ajouter une connexion SSH, cliquez sur la liste déroulante d'environnement avant de démarrer une session et sélectionnez **+ Ajouter une connexion SSH**. La boîte de dialogue demande :

* **Nom** : une étiquette conviviale pour cette connexion
* **Hôte SSH** : `user@hostname` ou un hôte défini dans `~/.ssh/config`
* **Port SSH** : par défaut 22 s'il est laissé vide, ou utilise le port de votre configuration SSH
* **Fichier d'identité** : chemin vers votre clé privée, comme `~/.ssh/id_rsa`. Laissez vide pour utiliser la clé par défaut ou votre configuration SSH.

Une fois ajoutée, la connexion apparaît dans la liste déroulante d'environnement. Sélectionnez-la pour démarrer une session sur cette machine. Claude s'exécute sur la machine distante avec accès à ses fichiers et outils.

La machine distante doit exécuter Linux ou macOS. L'application de bureau installe Claude Code sur la machine distante automatiquement la première fois que vous vous connectez. Une fois connecté, les sessions SSH supportent les modes de permission, les connecteurs, les plugins et les serveurs MCP.

#### Pré-configurer les connexions SSH pour votre équipe

Les administrateurs peuvent distribuer les connexions SSH aux membres de l'équipe en ajoutant `sshConfigs` à un fichier de [paramètres gérés](/fr/settings#settings-precedence). Les connexions définies de cette manière apparaissent dans la liste déroulante d'environnement de chaque utilisateur automatiquement et sont affichées comme gérées, de sorte que les utilisateurs peuvent les sélectionner mais ne peuvent pas les modifier ou les supprimer dans l'application.

L'exemple suivant pré-configure une seule connexion qui s'ouvre dans `~/projects` sur l'hôte distant :

```json theme={null}
{
  "sshConfigs": [
    {
      "id": "shared-dev-vm",
      "name": "Shared Dev VM",
      "sshHost": "user@dev.example.com",
      "sshPort": 22,
      "sshIdentityFile": "~/.ssh/id_ed25519",
      "startDirectory": "~/projects"
    }
  ]
}
```

Chaque entrée nécessite `id`, `name` et `sshHost`. Les champs `sshPort`, `sshIdentityFile` et `startDirectory` sont optionnels. Les utilisateurs peuvent également ajouter `sshConfigs` à leur propre `~/.claude/settings.json`, qui est l'endroit où les connexions ajoutées via la boîte de dialogue sont stockées.

#### Restreindre les hôtes SSH auxquels les utilisateurs peuvent se connecter

Les administrateurs peuvent limiter les sessions SSH de Desktop à un ensemble approuvé d'hôtes en ajoutant `sshHostAllowlist` à un fichier de [paramètres gérés](/fr/settings#settings-precedence). Lorsqu'il est défini, les utilisateurs ne peuvent se connecter qu'à des hôtes dont le nom d'hôte résolu correspond à l'un des modèles. Définissez-le sur un tableau vide pour désactiver complètement les sessions SSH.

L'exemple suivant autorise les connexions à n'importe quel hôte sous `devboxes.example.com` et à un seul hôte bastion nommé :

```json theme={null}
{
  "sshHostAllowlist": ["*.devboxes.example.com", "bastion.example.com"]
}
```

Les modèles sont insensibles à la casse. `*` correspond à n'importe quel hôte, et `*.example.com` correspond à `example.com` et à n'importe quel sous-domaine. Tout le reste est une correspondance exacte. La vérification s'exécute sur le nom d'hôte après la résolution `~/.ssh/config` via `ssh -G`, de sorte que les alias `Host` et les entrées `ProxyCommand`/`ProxyJump` sont autorisés tant que le `HostName` résolu correspond.

`sshHostAllowlist` est lu uniquement à partir des paramètres gérés ; les valeurs dans les paramètres utilisateur ou projet sont ignorées. Seule l'application Claude Desktop honore ce paramètre ; la CLI Claude Code et les extensions IDE ne le lisent pas, et il ne restreint pas les commandes `ssh` exécutées via l'outil Bash. Il gouverne les hôtes auxquels l'application Desktop se connecte, pas la sortie réseau, donc associez-le aux contrôles réseau ou zero-trust de votre organisation si vous avez besoin d'une limite stricte.

## Configuration d'entreprise

Les organisations sur les plans Team ou Enterprise peuvent gérer le comportement de l'application de bureau via les contrôles de la console d'administration, les fichiers de paramètres gérés et les politiques de gestion des appareils.

### Contrôles de la console d'administration

Ces paramètres sont configurés via la [console de paramètres d'administration](https://claude.ai/admin-settings/claude-code) :

* **Code dans le bureau** : contrôlez si les utilisateurs de votre organisation peuvent accéder à Claude Code dans l'application de bureau
* **Code sur le web** : activez ou désactivez les [sessions web](/fr/claude-code-on-the-web) pour votre organisation
* **Remote Control** : activez ou désactivez [Remote Control](/fr/remote-control) pour votre organisation
* **Désactiver le mode Contourner les permissions** : empêchez les utilisateurs de votre organisation d'activer le mode de contournement des permissions

### Paramètres gérés

Les paramètres gérés remplacent les paramètres du projet et de l'utilisateur et s'appliquent quand Desktop génère des sessions CLI. Vous pouvez définir ces clés dans le fichier [paramètres gérés](/fr/settings#settings-precedence) de votre organisation ou les pousser à distance via la console d'administration.

| Clé                                        | Description                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `permissions.disableBypassPermissionsMode` | définissez sur `"disable"` pour empêcher les utilisateurs d'activer le mode de contournement des permissions.                                                                                                                                                                                                                                                                        |
| `disableAutoMode`                          | définissez sur `"disable"` pour empêcher les utilisateurs d'activer le mode [Auto](/fr/permission-modes#eliminate-prompts-with-auto-mode). Supprime Auto du sélecteur de mode. Également accepté sous `permissions`.                                                                                                                                                                 |
| `autoMode`                                 | personnalisez ce que le classificateur du mode auto fait confiance et bloque dans votre organisation. Voir [Configurer le mode auto](/fr/auto-mode-config).                                                                                                                                                                                                                          |
| `sshConfigs`                               | pré-configurez les [connexions SSH](#pre-configure-ssh-connections-for-your-team) qui apparaissent dans la liste déroulante de l'environnement. Les utilisateurs ne peuvent pas modifier ou supprimer les connexions gérées.                                                                                                                                                         |
| `sshHostAllowlist`                         | restreignez les [sessions SSH](#restrict-which-ssh-hosts-users-can-connect-to) aux hôtes dont le nom d'hôte résolu correspond à l'un de ces modèles. Un tableau vide désactive les sessions SSH. Lecture à partir des paramètres gérés uniquement.                                                                                                                                   |
| `managedMcpServers`                        | poussez les configurations du serveur MCP à tous les utilisateurs dans un déploiement tiers. Chaque entrée spécifie un transport de `"http"`, `"sse"` ou `"stdio"`, les détails de connexion et optionnellement une carte `toolPolicy` qui restreint les outils de ce serveur que les utilisateurs peuvent invoquer. Disponible dans les déploiements Desktop tiers (3P) uniquement. |

Un fichier de paramètres gérés déployé sur le disque de chaque machine s'applique aux sessions Desktop. Les paramètres gérés poussés à distance via la console d'administration atteignent actuellement uniquement les sessions CLI et IDE, donc pour les déploiements Desktop, distribuez le fichier via MDM ou utilisez les [contrôles de la console d'administration](#admin-console-controls) ci-dessus.

`permissions.disableBypassPermissionsMode` et `disableAutoMode` fonctionnent également dans les paramètres utilisateur et projet, mais les placer dans les paramètres gérés empêche les utilisateurs de les remplacer. `autoMode` est lu à partir des paramètres utilisateur, `.claude/settings.local.json` et des paramètres gérés, mais pas à partir du `.claude/settings.json` coché : un référentiel cloné ne peut pas injecter ses propres règles de classificateur. Pour la liste complète des paramètres gérés uniquement, y compris `allowManagedPermissionRulesOnly` et `allowManagedHooksOnly`, voir [paramètres gérés uniquement](/fr/permissions#managed-only-settings).

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

Pour déplacer une session CLI dans Desktop, exécutez `/desktop` dans le terminal. Claude enregistre votre session et l'ouvre dans l'application de bureau, puis quitte la CLI. Cette commande est disponible sur macOS et Windows quand vous êtes connecté avec un abonnement Claude. Elle n'est pas disponible avec l'authentification par clé API ou sur Bedrock, Vertex ou Foundry.

<Tip>
  Quand utiliser Desktop vs CLI : utilisez Desktop quand vous voulez gérer les sessions parallèles dans une fenêtre, arranger les volets côte à côte ou examiner les modifications visuellement. Utilisez la CLI quand vous avez besoin de scripts, d'automatisation ou préférez un flux de travail terminal.
</Tip>

### Équivalents des drapeaux CLI

Ce tableau montre l'équivalent de l'application de bureau pour les drapeaux CLI courants. Les drapeaux non listés n'ont pas d'équivalent de bureau car ils sont conçus pour les scripts ou l'automatisation.

| CLI                                            | Équivalent de bureau                                                                                                                                                                               |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--model sonnet`                               | Liste déroulante de modèle à côté du bouton d'envoi                                                                                                                                                |
| `--resume`, `--continue`                       | Cliquez sur une session dans la barre latérale                                                                                                                                                     |
| `--permission-mode`                            | Sélecteur de mode à côté du bouton d'envoi                                                                                                                                                         |
| `--dangerously-skip-permissions`               | Mode Contourner les permissions. Activez dans Paramètres → Claude Code → « Autoriser le mode de contournement des permissions ». Les administrateurs d'entreprise peuvent désactiver ce paramètre. |
| `--add-dir`                                    | Ajouter plusieurs référentiels avec le bouton **+** dans les sessions distantes                                                                                                                    |
| `--allowedTools`, `--disallowedTools`          | Aucun équivalent par session. Les règles de permission dans les [fichiers de paramètres](/fr/settings) s'appliquent toujours.                                                                      |
| `--verbose`                                    | Mode d'affichage [Verbose](#switch-view-modes) dans la liste déroulante Vue de la transcription                                                                                                    |
| `--print`, `--output-format`                   | Non disponible. Desktop est interactif uniquement.                                                                                                                                                 |
| Variable d'environnement `ANTHROPIC_MODEL`     | Liste déroulante de modèle à côté du bouton d'envoi                                                                                                                                                |
| Variable d'environnement `MAX_THINKING_TOKENS` | Définissez dans l'éditeur d'environnement local. Voir [configuration de l'environnement](#environment-configuration).                                                                              |

### Configuration partagée

Desktop et CLI lisent les mêmes fichiers de configuration, donc votre configuration se transfère :

* Les fichiers **[CLAUDE.md](/fr/memory)** et `CLAUDE.local.md` dans votre projet sont utilisés par les deux
* Les **[serveurs MCP](/fr/mcp)** configurés dans `~/.claude.json` ou `.mcp.json` fonctionnent dans les deux
* Les **[hooks](/fr/hooks)** et **[skills](/fr/skills)** définis dans les paramètres s'appliquent aux deux
* Les **[paramètres](/fr/settings)** dans `~/.claude.json` et `~/.claude/settings.json` sont partagés. Les règles de permission, les outils autorisés et d'autres paramètres dans `settings.json` s'appliquent aux sessions Desktop.
* **Modèles** : Sonnet, Opus et Haiku sont disponibles dans les deux. Dans Desktop, sélectionnez le modèle à partir de la liste déroulante à côté du bouton d'envoi. Vous pouvez modifier le modèle pendant la session à partir de la même liste déroulante.

<Note>
  **Serveurs MCP : application de chat de bureau vs Claude Code** : les serveurs MCP configurés pour l'application de chat Claude Desktop dans `claude_desktop_config.json` sont séparés de Claude Code et n'apparaîtront pas dans l'onglet Code. Pour utiliser les serveurs MCP dans Claude Code, configurez-les dans `~/.claude.json` ou le fichier `.mcp.json` de votre projet. Voir [configuration MCP](/fr/mcp#installing-mcp-servers) pour les détails.
</Note>

### Comparaison des fonctionnalités

Ce tableau compare les capacités principales entre la CLI et Desktop. Pour une liste complète des drapeaux CLI, voir la [référence CLI](/fr/cli-reference).

| Fonctionnalité                                     | CLI                                                       | Desktop                                                                                                                                                                                                                                            |
| -------------------------------------------------- | --------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Modes de permission                                | Tous les modes y compris `dontAsk`                        | Demander les permissions, Accepter automatiquement les modifications, Plan mode, Auto et Contourner les permissions via Paramètres                                                                                                                 |
| `--dangerously-skip-permissions`                   | Drapeau CLI                                               | Mode Contourner les permissions. Activez dans Paramètres → Claude Code → « Autoriser le mode de contournement des permissions »                                                                                                                    |
| [Fournisseurs tiers](/fr/third-party-integrations) | Bedrock, Vertex, Foundry                                  | API d'Anthropic par défaut. Les déploiements d'entreprise peuvent configurer Vertex AI et les fournisseurs de passerelle. Voir le [guide de configuration d'entreprise](https://support.claude.com/en/articles/12622667-enterprise-configuration). |
| [Serveurs MCP](/fr/mcp)                            | Configurer dans les fichiers de paramètres                | Interface utilisateur Connecteurs pour les sessions locales et SSH, ou fichiers de paramètres                                                                                                                                                      |
| [Plugins](/fr/plugins)                             | Commande `/plugin`                                        | Interface utilisateur du gestionnaire de plugins                                                                                                                                                                                                   |
| Fichiers @mention                                  | Basé sur le texte                                         | Avec autocomplétion ; sessions locales et SSH uniquement                                                                                                                                                                                           |
| Pièces jointes de fichiers                         | Non disponible                                            | Images, PDF                                                                                                                                                                                                                                        |
| Isolation des sessions                             | Drapeau [`--worktree`](/fr/cli-reference)                 | Worktrees automatiques                                                                                                                                                                                                                             |
| Sessions multiples                                 | Terminaux séparés                                         | Onglets de barre latérale                                                                                                                                                                                                                          |
| Tâches récurrentes                                 | Tâches cron, pipelines CI                                 | [Tâches planifiées](/fr/desktop-scheduled-tasks)                                                                                                                                                                                                   |
| Utilisation informatique                           | [Activer via `/mcp`](/fr/computer-use) sur macOS          | [Contrôle d'application et d'écran](#let-claude-use-your-computer) sur macOS et Windows                                                                                                                                                            |
| Intégration Dispatch                               | Non disponible                                            | [Sessions Dispatch](#sessions-from-dispatch) dans la barre latérale                                                                                                                                                                                |
| Scripts et automatisation                          | [`--print`](/fr/cli-reference), [Agent SDK](/fr/headless) | Non disponible                                                                                                                                                                                                                                     |

### Ce qui n'est pas disponible dans Desktop

Les fonctionnalités suivantes sont disponibles uniquement dans la CLI ou l'extension VS Code :

* **Fournisseurs tiers** : Desktop se connecte à l'API d'Anthropic par défaut. Les déploiements d'entreprise peuvent configurer Vertex AI et les fournisseurs de passerelle via [paramètres gérés](https://support.claude.com/en/articles/12622667-enterprise-configuration). Pour Bedrock ou Foundry, utilisez la [CLI](/fr/quickstart).
* **Linux** : l'application de bureau est disponible sur macOS et Windows uniquement. Sur Linux, utilisez la [CLI](/fr/quickstart).
* **Suggestions de code en ligne** : Desktop ne fournit pas de suggestions de style autocomplétion. Il fonctionne via des prompts conversationnels et des modifications de code explicites.
* **Équipes d'agents** : l'orchestration multi-agents est disponible via la [CLI](/fr/agent-teams) et [Agent SDK](/fr/headless), pas dans Desktop.
* **Commandes de dialogue terminal** : les commandes intégrées qui ouvrent un panneau interactif dans le terminal, telles que `/permissions`, `/config`, `/agents` et `/doctor`, ne sont pas disponibles dans l'onglet Code et répondent avec `n'est pas disponible dans cet environnement`. Modifiez les [fichiers de paramètres](/fr/settings) directement pour gérer les règles de permission et la configuration, ou exécutez la commande à partir de la CLI autonome.

## Dépannage

Les sections ci-dessous couvrent les problèmes spécifiques à l'application de bureau. Pour les erreurs API d'exécution qui apparaissent dans le chat comme `API Error: 500`, `529 Overloaded`, `429` ou `Prompt is too long`, voir la [référence des erreurs](/fr/errors). Ces erreurs et leurs correctifs sont les mêmes sur la CLI, le bureau et le web.

### Vérifier votre version

Pour voir quelle version de l'application de bureau vous exécutez :

* **macOS** : cliquez sur **Claude** dans la barre de menu, puis **À propos de Claude**
* **Windows** : cliquez sur **Aide**, puis **À propos**

Cliquez sur le numéro de version pour le copier dans votre presse-papiers.

### Erreurs 403 ou d'authentification dans l'onglet Code

Si vous voyez `Error 403: Forbidden` ou d'autres défaillances d'authentification lors de l'utilisation de l'onglet Code :

1. Déconnectez-vous et reconnectez-vous à partir du menu de l'application. C'est le correctif le plus courant.
2. Vérifiez que vous avez un abonnement payant actif : Pro, Max, Team ou Enterprise.
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

### « La branche n'existe pas encore » lors de l'ouverture dans la CLI

Les sessions distantes peuvent créer des branches qui n'existent pas sur votre machine locale. Cliquez sur le nom de la branche dans la barre d'outils de la session pour le copier, puis récupérez-le localement :

```bash theme={null}
git fetch origin <branch-name>
git checkout <branch-name>
```

### Toujours bloqué ?

* Recherchez ou signalez un bug sur [GitHub Issues](https://github.com/anthropics/claude-code/issues)
* Visitez le [centre de support Claude](https://support.claude.com/)

Lors du signalement d'un bug, incluez la version de votre application de bureau, votre système d'exploitation, le message d'erreur exact et les journaux pertinents. Sur macOS, vérifiez Console.app. Sur Windows, vérifiez Observateur d'événements → Journaux Windows → Application.
