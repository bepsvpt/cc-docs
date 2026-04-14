> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Comment fonctionne Claude Code

> Comprenez la boucle agentive, les outils intégrés et comment Claude Code interagit avec votre projet.

Claude Code est un assistant agentif qui s'exécute dans votre terminal. Bien qu'il excelle dans la programmation, il peut vous aider pour tout ce que vous pouvez faire à partir de la ligne de commande : rédiger de la documentation, exécuter des builds, rechercher des fichiers, faire des recherches sur des sujets, et bien plus.

Ce guide couvre l'architecture centrale, les capacités intégrées, et [des conseils pour travailler efficacement avec Claude Code](#work-effectively-with-claude-code). Pour des procédures pas à pas, consultez [Workflows courants](/fr/common-workflows). Pour les fonctionnalités d'extensibilité comme les skills, MCP et hooks, consultez [Étendre Claude Code](/fr/features-overview).

## La boucle agentive

Lorsque vous donnez une tâche à Claude, il travaille à travers trois phases : **rassembler le contexte**, **agir**, et **vérifier les résultats**. Ces phases se mélangent ensemble. Claude utilise des outils tout au long du processus, qu'il s'agisse de rechercher des fichiers pour comprendre votre code, d'éditer pour apporter des modifications, ou d'exécuter des tests pour vérifier son travail.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/agentic-loop.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=5f1827dec8539f38adee90ead3a85a38" alt="La boucle agentive : Votre prompt conduit Claude à rassembler le contexte, agir, vérifier les résultats, et répéter jusqu'à ce que la tâche soit terminée. Vous pouvez interrompre à tout moment." width="720" height="280" data-path="images/agentic-loop.svg" />

La boucle s'adapte à ce que vous demandez. Une question sur votre base de code pourrait nécessiter uniquement la collecte de contexte. Une correction de bug parcourt les trois phases à plusieurs reprises. Une refactorisation pourrait impliquer une vérification extensive. Claude décide ce que chaque étape nécessite en fonction de ce qu'il a appris à l'étape précédente, en enchaînant des dizaines d'actions ensemble et en se corrigeant en cours de route.

Vous faites également partie de cette boucle. Vous pouvez interrompre à tout moment pour orienter Claude dans une direction différente, fournir un contexte supplémentaire, ou lui demander d'essayer une approche différente. Claude fonctionne de manière autonome mais reste réactif à votre contribution.

La boucle agentive est alimentée par deux composants : [les modèles](#models) qui raisonnent et [les outils](#tools) qui agissent. Claude Code sert de **harnais agentif** autour de Claude : il fournit les outils, la gestion du contexte, et l'environnement d'exécution qui transforment un modèle de langage en un agent de codage capable.

### Modèles

Claude Code utilise les modèles Claude pour comprendre votre code et raisonner sur les tâches. Claude peut lire du code dans n'importe quel langage, comprendre comment les composants se connectent, et déterminer ce qui doit changer pour accomplir votre objectif. Pour les tâches complexes, il divise le travail en étapes, les exécute, et s'ajuste en fonction de ce qu'il apprend.

[Plusieurs modèles](/fr/model-config) sont disponibles avec des compromis différents. Sonnet gère bien la plupart des tâches de codage. Opus fournit un raisonnement plus fort pour les décisions architecturales complexes. Basculez avec `/model` pendant une session ou commencez avec `claude --model <name>`.

Lorsque ce guide dit « Claude choisit » ou « Claude décide », c'est le modèle qui effectue le raisonnement.

### Outils

Les outils sont ce qui rend Claude Code agentif. Sans outils, Claude ne peut que répondre avec du texte. Avec les outils, Claude peut agir : lire votre code, éditer des fichiers, exécuter des commandes, rechercher sur le web, et interagir avec des services externes. Chaque utilisation d'outil retourne des informations qui se réintègrent dans la boucle, informant la décision suivante de Claude.

Les outils intégrés se divisent généralement en cinq catégories, chacune représentant un type d'agentivité différent.

| Catégorie                       | Ce que Claude peut faire                                                                                                                                                                                    |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Opérations sur les fichiers** | Lire des fichiers, éditer du code, créer de nouveaux fichiers, renommer et réorganiser                                                                                                                      |
| **Recherche**                   | Trouver des fichiers par motif, rechercher du contenu avec regex, explorer les bases de code                                                                                                                |
| **Exécution**                   | Exécuter des commandes shell, démarrer des serveurs, exécuter des tests, utiliser git                                                                                                                       |
| **Web**                         | Rechercher sur le web, récupérer de la documentation, rechercher des messages d'erreur                                                                                                                      |
| **Intelligence du code**        | Voir les erreurs de type et les avertissements après les éditions, accéder aux définitions, trouver les références (nécessite [les plugins d'intelligence du code](/fr/discover-plugins#code-intelligence)) |

Ce sont les capacités principales. Claude dispose également d'outils pour générer des subagents, vous poser des questions, et d'autres tâches d'orchestration. Consultez [Outils disponibles pour Claude](/fr/tools-reference) pour la liste complète.

Claude choisit les outils à utiliser en fonction de votre prompt et de ce qu'il apprend en cours de route. Lorsque vous dites « corriger les tests qui échouent », Claude pourrait :

1. Exécuter la suite de tests pour voir ce qui échoue
2. Lire la sortie d'erreur
3. Rechercher les fichiers source pertinents
4. Lire ces fichiers pour comprendre le code
5. Éditer les fichiers pour corriger le problème
6. Exécuter les tests à nouveau pour vérifier

Chaque utilisation d'outil donne à Claude de nouvelles informations qui informent l'étape suivante. C'est la boucle agentive en action.

**Étendre les capacités de base :** Les outils intégrés sont la fondation. Vous pouvez étendre ce que Claude sait avec [les skills](/fr/skills), vous connecter à des services externes avec [MCP](/fr/mcp), automatiser les workflows avec [hooks](/fr/hooks), et déléguer des tâches à [des subagents](/fr/sub-agents). Ces extensions forment une couche au-dessus de la boucle agentive principale. Consultez [Étendre Claude Code](/fr/features-overview) pour des conseils sur le choix de la bonne extension pour vos besoins.

## Ce que Claude peut accéder

Ce guide se concentre sur le terminal. Claude Code s'exécute également dans [VS Code](/fr/vs-code), [les IDEs JetBrains](/fr/jetbrains), et d'autres environnements.

Lorsque vous exécutez `claude` dans un répertoire, Claude Code accède à :

* **Votre projet.** Les fichiers de votre répertoire et sous-répertoires, plus les fichiers ailleurs avec votre permission.
* **Votre terminal.** N'importe quelle commande que vous pourriez exécuter : outils de build, git, gestionnaires de paquets, utilitaires système, scripts. Si vous pouvez le faire à partir de la ligne de commande, Claude aussi.
* **Votre état git.** La branche actuelle, les modifications non validées, et l'historique récent des commits.
* **Votre [CLAUDE.md](/fr/memory).** Un fichier markdown où vous stockez les instructions spécifiques au projet, les conventions, et le contexte que Claude devrait connaître à chaque session.
* **[Mémoire automatique](/fr/memory#auto-memory).** Les apprentissages que Claude sauvegarde automatiquement au fur et à mesure que vous travaillez, comme les motifs de projet et vos préférences. Les 200 premières lignes ou 25 KB de MEMORY.md, selon ce qui vient en premier, se chargent au début de chaque session.
* **Les extensions que vous configurez.** [Les serveurs MCP](/fr/mcp) pour les services externes, [les skills](/fr/skills) pour les workflows, [les subagents](/fr/sub-agents) pour le travail délégué, et [Claude dans Chrome](/fr/chrome) pour l'interaction avec le navigateur.

Parce que Claude voit votre projet entier, il peut travailler à travers celui-ci. Lorsque vous demandez à Claude de « corriger le bug d'authentification », il recherche les fichiers pertinents, lit plusieurs fichiers pour comprendre le contexte, effectue des éditions coordonnées à travers eux, exécute des tests pour vérifier la correction, et valide les modifications si vous le demandez. C'est différent des assistants de code en ligne qui ne voient que le fichier actuel.

## Environnements et interfaces

La boucle agentive, les outils, et les capacités décrites ci-dessus sont les mêmes partout où vous utilisez Claude Code. Ce qui change, c'est où le code s'exécute et comment vous interagissez avec lui.

### Environnements d'exécution

Claude Code s'exécute dans trois environnements, chacun avec des compromis différents pour l'endroit où votre code s'exécute.

| Environnement           | Où le code s'exécute                              | Cas d'usage                                                                  |
| ----------------------- | ------------------------------------------------- | ---------------------------------------------------------------------------- |
| **Local**               | Votre machine                                     | Par défaut. Accès complet à vos fichiers, outils, et environnement           |
| **Cloud**               | VMs gérées par Anthropic                          | Déléguer des tâches, travailler sur des repos que vous n'avez pas localement |
| **Contrôle à distance** | Votre machine, contrôlée à partir d'un navigateur | Utiliser l'interface web tout en gardant tout local                          |

### Interfaces

Vous pouvez accéder à Claude Code via le terminal, l'[application de bureau](/fr/desktop), [les extensions IDE](/fr/vs-code), [claude.ai/code](https://claude.ai/code), [Contrôle à distance](/fr/remote-control), [Slack](/fr/slack), et [les pipelines CI/CD](/fr/github-actions). L'interface détermine comment vous voyez et interagissez avec Claude, mais la boucle agentive sous-jacente est identique. Consultez [Utiliser Claude Code partout](/fr/overview#use-claude-code-everywhere) pour la liste complète.

## Travailler avec les sessions

Claude Code sauvegarde votre conversation localement au fur et à mesure que vous travaillez. Chaque message, utilisation d'outil, et résultat est stocké, ce qui permet [de revenir en arrière](#undo-changes-with-checkpoints), [de reprendre et de forker](#resume-or-fork-sessions) les sessions. Avant que Claude ne fasse des modifications de code, il prend également un snapshot des fichiers affectés afin que vous puissiez revenir en arrière si nécessaire.

**Les sessions sont indépendantes.** Chaque nouvelle session commence avec une fenêtre de contexte fraîche, sans l'historique de conversation des sessions précédentes. Claude peut persister les apprentissages à travers les sessions en utilisant [la mémoire automatique](/fr/memory#auto-memory), et vous pouvez ajouter vos propres instructions persistantes dans [CLAUDE.md](/fr/memory).

### Travailler à travers les branches

Chaque conversation Claude Code est une session liée à votre répertoire actuel. Lorsque vous reprenez, vous ne voyez que les sessions de ce répertoire.

Claude voit les fichiers de votre branche actuelle. Lorsque vous changez de branche, Claude voit les fichiers de la nouvelle branche, mais votre historique de conversation reste le même. Claude se souvient de ce que vous avez discuté même après avoir changé de branche.

Puisque les sessions sont liées aux répertoires, vous pouvez exécuter des sessions Claude parallèles en utilisant [git worktrees](/fr/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), qui créent des répertoires séparés pour les branches individuelles.

### Reprendre ou forker les sessions

Lorsque vous reprenez une session avec `claude --continue` ou `claude --resume`, vous reprenez là où vous vous étiez arrêté en utilisant le même ID de session. Les nouveaux messages s'ajoutent à la conversation existante. Votre historique de conversation complet est restauré, mais les permissions scoped à la session ne le sont pas. Vous devrez les réapprouver.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/session-continuity.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=fa41d12bfb57579cabfeece907151d30" alt="Continuité de session : reprendre continue la même session, forker crée une nouvelle branche avec un nouvel ID." width="560" height="280" data-path="images/session-continuity.svg" />

Pour créer une branche et essayer une approche différente sans affecter la session d'origine, utilisez le flag `--fork-session` :

```bash  theme={null}
claude --continue --fork-session
```

Cela crée un nouvel ID de session tout en préservant l'historique de conversation jusqu'à ce point. La session d'origine reste inchangée. Comme pour reprendre, les sessions forkées n'héritent pas des permissions scoped à la session.

**Même session dans plusieurs terminaux** : Si vous reprenez la même session dans plusieurs terminaux, les deux terminaux écrivent dans le même fichier de session. Les messages des deux sont entrelacés, comme deux personnes écrivant dans le même carnet. Rien ne se corrompt, mais la conversation devient confuse. Chaque terminal ne voit que ses propres messages pendant la session, mais si vous reprenez cette session plus tard, vous verrez tout entrelacé. Pour le travail parallèle à partir du même point de départ, utilisez `--fork-session` pour donner à chaque terminal sa propre session propre.

### La fenêtre de contexte

La fenêtre de contexte de Claude contient votre historique de conversation, le contenu des fichiers, les sorties de commande, [CLAUDE.md](/fr/memory), [la mémoire automatique](/fr/memory#auto-memory), les skills chargés, et les instructions système. Au fur et à mesure que vous travaillez, le contexte se remplit. Claude compacte automatiquement, mais les instructions du début de la conversation peuvent être perdues. Mettez les règles persistantes dans CLAUDE.md, et exécutez `/context` pour voir ce qui utilise l'espace.

Pour une procédure interactive d'exploration de ce qui se charge et quand, consultez [Explorer la fenêtre de contexte](/fr/context-window).

#### Lorsque le contexte se remplit

Claude Code gère le contexte automatiquement à mesure que vous approchez de la limite. Il efface d'abord les sorties d'outils plus anciennes, puis résume la conversation si nécessaire. Vos demandes et les extraits de code clés sont préservés ; les instructions détaillées du début de la conversation peuvent être perdues. Mettez les règles persistantes dans CLAUDE.md plutôt que de compter sur l'historique de conversation.

Pour contrôler ce qui est préservé pendant la compaction, ajoutez une section « Compact Instructions » à CLAUDE.md ou exécutez `/compact` avec un focus (comme `/compact focus on the API changes`).

Exécutez `/context` pour voir ce qui utilise l'espace. Les définitions d'outils MCP sont différées par défaut et chargées à la demande via [la recherche d'outils](/fr/mcp#scale-with-mcp-tool-search), donc seuls les noms d'outils consomment du contexte jusqu'à ce que Claude utilise un outil spécifique. Exécutez `/mcp` pour vérifier les coûts par serveur.

#### Gérer le contexte avec les skills et les subagents

Au-delà de la compaction, vous pouvez utiliser d'autres fonctionnalités pour contrôler ce qui se charge dans le contexte.

[Les skills](/fr/skills) se chargent à la demande. Claude voit les descriptions des skills au démarrage de la session, mais le contenu complet ne se charge que lorsqu'un skill est utilisé. Pour les skills que vous invoquez manuellement, définissez `disable-model-invocation: true` pour garder les descriptions hors du contexte jusqu'à ce que vous en ayez besoin.

[Les subagents](/fr/sub-agents) obtiennent leur propre contexte frais, complètement séparé de votre conversation principale. Leur travail ne gonfle pas votre contexte. Une fois terminés, ils retournent un résumé. Cet isolement est pourquoi les subagents aident avec les sessions longues.

Consultez [les coûts de contexte](/fr/features-overview#understand-context-costs) pour ce que chaque fonctionnalité coûte, et [réduire l'utilisation des tokens](/fr/costs#reduce-token-usage) pour des conseils sur la gestion du contexte.

## Rester en sécurité avec les checkpoints et les permissions

Claude dispose de deux mécanismes de sécurité : les checkpoints vous permettent d'annuler les modifications de fichiers, et les permissions contrôlent ce que Claude peut faire sans demander.

### Annuler les modifications avec les checkpoints

**Chaque édition de fichier est réversible.** Avant que Claude n'édite un fichier, il prend un snapshot du contenu actuel. Si quelque chose se passe mal, appuyez deux fois sur `Esc` pour revenir à un état précédent, ou demandez à Claude d'annuler.

Les checkpoints sont locaux à votre session, séparés de git. Ils ne couvrent que les modifications de fichiers. Les actions qui affectent les systèmes distants (bases de données, APIs, déploiements) ne peuvent pas être checkpointées, c'est pourquoi Claude demande avant d'exécuter des commandes avec des effets secondaires externes.

### Contrôler ce que Claude peut faire

Appuyez sur `Shift+Tab` pour parcourir les modes de permission :

* **Par défaut** : Claude demande avant les éditions de fichiers et les commandes shell
* **Auto-accepter les éditions** : Claude édite les fichiers sans demander, demande toujours pour les commandes
* **Plan Mode** : Claude utilise uniquement les outils en lecture seule, créant un plan que vous pouvez approuver avant l'exécution
* **Mode Auto** : Claude évalue toutes les actions avec des vérifications de sécurité en arrière-plan. Actuellement une préversion de recherche

Vous pouvez également autoriser des commandes spécifiques dans `.claude/settings.json` afin que Claude ne demande pas à chaque fois. C'est utile pour les commandes de confiance comme `npm test` ou `git status`. Les paramètres peuvent être scoped à partir des politiques à l'échelle de l'organisation jusqu'aux préférences personnelles. Consultez [Permissions](/fr/permissions) pour plus de détails.

***

## Travailler efficacement avec Claude Code

Ces conseils vous aident à obtenir de meilleurs résultats avec Claude Code.

### Demander de l'aide à Claude Code

Claude Code peut vous enseigner comment l'utiliser. Posez des questions comme « comment configurer les hooks ? » ou « quelle est la meilleure façon de structurer mon CLAUDE.md ? » et Claude expliquera.

Les commandes intégrées vous guident également à travers la configuration :

* `/init` vous guide à travers la création d'un CLAUDE.md pour votre projet
* `/agents` vous aide à configurer des subagents personnalisés
* `/doctor` diagnostique les problèmes courants avec votre installation

### C'est une conversation

Claude Code est conversationnel. Vous n'avez pas besoin de prompts parfaits. Commencez par ce que vous voulez, puis affinez :

```text  theme={null}
Corriger le bug de connexion
```

\[Claude enquête, essaie quelque chose]

```text  theme={null}
Ce n'est pas tout à fait correct. Le problème est dans la gestion de session.
```

\[Claude ajuste son approche]

Lorsque la première tentative n'est pas correcte, vous ne recommencez pas. Vous itérez.

#### Interrompre et orienter

Vous pouvez interrompre Claude à tout moment. S'il va dans la mauvaise direction, tapez simplement votre correction et appuyez sur Entrée. Claude arrêtera ce qu'il fait et ajustera son approche en fonction de votre contribution. Vous n'avez pas à attendre qu'il finisse ou à recommencer.

### Être spécifique dès le départ

Plus votre prompt initial est précis, moins de corrections vous aurez besoin. Référencez des fichiers spécifiques, mentionnez les contraintes, et pointez vers des motifs d'exemple.

```text  theme={null}
Le flux de paiement est cassé pour les utilisateurs avec des cartes expirées.
Vérifiez src/payments/ pour le problème, en particulier l'actualisation des tokens.
Écrivez d'abord un test qui échoue, puis corrigez-le.
```

Les prompts vagues fonctionnent, mais vous passerez plus de temps à orienter. Les prompts spécifiques comme celui ci-dessus réussissent souvent à la première tentative.

### Donner à Claude quelque chose à vérifier

Claude fonctionne mieux lorsqu'il peut vérifier son propre travail. Incluez des cas de test, collez des captures d'écran de l'interface utilisateur attendue, ou définissez la sortie que vous voulez.

```text  theme={null}
Implémenter validateEmail. Cas de test : 'user@example.com' → true,
'invalid' → false, 'user@.com' → false. Exécutez les tests après.
```

Pour le travail visuel, collez une capture d'écran de la conception et demandez à Claude de comparer son implémentation avec celle-ci.

### Explorer avant d'implémenter

Pour les problèmes complexes, séparez la recherche du codage. Utilisez le plan mode (`Shift+Tab` deux fois) pour analyser d'abord la base de code :

```text  theme={null}
Lire src/auth/ et comprendre comment nous gérons les sessions.
Ensuite, créer un plan pour ajouter le support OAuth.
```

Examinez le plan, affinez-le à travers la conversation, puis laissez Claude implémenter. Cette approche en deux phases produit de meilleurs résultats que de sauter directement au code.

### Déléguer, ne pas dicter

Pensez à déléguer à un collègue capable. Donnez le contexte et la direction, puis faites confiance à Claude pour déterminer les détails :

```text  theme={null}
Le flux de paiement est cassé pour les utilisateurs avec des cartes expirées.
Le code pertinent est dans src/payments/. Pouvez-vous enquêter et corriger ?
```

Vous n'avez pas besoin de spécifier quels fichiers lire ou quelles commandes exécuter. Claude le détermine.

## Prochaines étapes

<CardGroup cols={2}>
  <Card title="Étendre avec des fonctionnalités" icon="puzzle-piece" href="/fr/features-overview">
    Ajouter des Skills, des connexions MCP, et des commandes personnalisées
  </Card>

  <Card title="Workflows courants" icon="graduation-cap" href="/fr/common-workflows">
    Guides pas à pas pour les tâches typiques
  </Card>
</CardGroup>
