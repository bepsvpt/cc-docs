> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Orchestrer des équipes de sessions Claude Code

> Coordonnez plusieurs instances Claude Code travaillant ensemble en tant qu'équipe, avec des tâches partagées, la messagerie inter-agents et la gestion centralisée.

<Warning>
  Les équipes d'agents sont expérimentales et désactivées par défaut. Activez-les en ajoutant `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` à votre [settings.json](/fr/settings) ou à votre environnement. Les équipes d'agents ont des [limitations connues](#limitations) concernant la reprise de session, la coordination des tâches et le comportement d'arrêt.
</Warning>

Les équipes d'agents vous permettent de coordonner plusieurs instances Claude Code travaillant ensemble. Une session agit comme chef d'équipe, coordonnant le travail, assignant des tâches et synthétisant les résultats. Les coéquipiers travaillent indépendamment, chacun dans sa propre fenêtre de contexte, et communiquent directement les uns avec les autres.

Contrairement aux [subagents](/fr/sub-agents), qui s'exécutent au sein d'une seule session et ne peuvent que rendre compte à l'agent principal, vous pouvez également interagir directement avec les coéquipiers individuels sans passer par le chef.

<Note>
  Les équipes d'agents nécessitent Claude Code v2.1.32 ou ultérieur. Vérifiez votre version avec `claude --version`.
</Note>

Cette page couvre :

* [Quand utiliser les équipes d'agents](#when-to-use-agent-teams), y compris les meilleurs cas d'usage et comment ils se comparent aux subagents
* [Démarrer une équipe](#start-your-first-agent-team)
* [Contrôler les coéquipiers](#control-your-agent-team), y compris les modes d'affichage, l'assignation de tâches et la délégation
* [Meilleures pratiques pour le travail parallèle](#best-practices)

## Quand utiliser les équipes d'agents

Les équipes d'agents sont les plus efficaces pour les tâches où l'exploration parallèle ajoute une réelle valeur. Consultez les [exemples de cas d'usage](#use-case-examples) pour des scénarios complets. Les cas d'usage les plus solides sont :

* **Recherche et examen** : plusieurs coéquipiers peuvent enquêter sur différents aspects d'un problème simultanément, puis partager et contester les conclusions les uns des autres
* **Nouveaux modules ou fonctionnalités** : les coéquipiers peuvent chacun posséder une partie distincte sans se marcher dessus
* **Débogage avec hypothèses concurrentes** : les coéquipiers testent différentes théories en parallèle et convergent vers la réponse plus rapidement
* **Coordination inter-couches** : les modifications qui s'étendent sur le frontend, le backend et les tests, chacun possédé par un coéquipier différent

Les équipes d'agents ajoutent une surcharge de coordination et utilisent considérablement plus de tokens qu'une seule session. Elles fonctionnent mieux lorsque les coéquipiers peuvent opérer indépendamment. Pour les tâches séquentielles, les modifications du même fichier ou le travail avec de nombreuses dépendances, une seule session ou les [subagents](/fr/sub-agents) sont plus efficaces.

### Comparer avec les subagents

Les équipes d'agents et les [subagents](/fr/sub-agents) vous permettent tous deux de paralléliser le travail, mais ils fonctionnent différemment. Choisissez en fonction de la nécessité pour vos travailleurs de communiquer les uns avec les autres :

<Frame caption="Les subagents ne rendent compte que des résultats à l'agent principal et ne se parlent jamais. Dans les équipes d'agents, les coéquipiers partagent une liste de tâches, revendiquent du travail et communiquent directement les uns avec les autres.">
  <img src="https://mintcdn.com/claude-code/nsvRFSDNfpSU5nT7/images/subagents-vs-agent-teams-light.png?fit=max&auto=format&n=nsvRFSDNfpSU5nT7&q=85&s=2f8db9b4f3705dd3ab931fbe2d96e42a" className="dark:hidden" alt="Diagramme comparant les architectures des subagents et des équipes d'agents. Les subagents sont générés par l'agent principal, font du travail et rendent compte des résultats. Les équipes d'agents se coordonnent via une liste de tâches partagée, avec les coéquipiers communiquant directement les uns avec les autres." width="4245" height="1615" data-path="images/subagents-vs-agent-teams-light.png" />

  <img src="https://mintcdn.com/claude-code/nsvRFSDNfpSU5nT7/images/subagents-vs-agent-teams-dark.png?fit=max&auto=format&n=nsvRFSDNfpSU5nT7&q=85&s=d573a037540f2ada6a9ae7d8285b46fd" className="hidden dark:block" alt="Diagramme comparant les architectures des subagents et des équipes d'agents. Les subagents sont générés par l'agent principal, font du travail et rendent compte des résultats. Les équipes d'agents se coordonnent via une liste de tâches partagée, avec les coéquipiers communiquant directement les uns avec les autres." width="4245" height="1615" data-path="images/subagents-vs-agent-teams-dark.png" />
</Frame>

|                    | Subagents                                                          | Équipes d'agents                                                |
| :----------------- | :----------------------------------------------------------------- | :-------------------------------------------------------------- |
| **Contexte**       | Fenêtre de contexte propre ; les résultats reviennent à l'appelant | Fenêtre de contexte propre ; complètement indépendant           |
| **Communication**  | Rendre compte uniquement à l'agent principal                       | Les coéquipiers se messagent directement                        |
| **Coordination**   | L'agent principal gère tout le travail                             | Liste de tâches partagée avec auto-coordination                 |
| **Meilleur pour**  | Les tâches ciblées où seul le résultat compte                      | Le travail complexe nécessitant discussion et collaboration     |
| **Coût en tokens** | Inférieur : les résultats sont résumés au contexte principal       | Supérieur : chaque coéquipier est une instance Claude distincte |

Utilisez les subagents lorsque vous avez besoin de travailleurs rapides et ciblés qui rendent compte. Utilisez les équipes d'agents lorsque les coéquipiers doivent partager les conclusions, se contester mutuellement et se coordonner de manière autonome.

## Activer les équipes d'agents

Les équipes d'agents sont désactivées par défaut. Activez-les en définissant la variable d'environnement `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` sur `1`, soit dans votre environnement shell, soit via [settings.json](/fr/settings) :

```json settings.json theme={null}
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

## Démarrer votre première équipe d'agents

Après avoir activé les équipes d'agents, demandez à Claude de créer une équipe d'agents et décrivez la tâche et la structure d'équipe que vous souhaitez en langage naturel. Claude crée l'équipe, génère les coéquipiers et coordonne le travail en fonction de votre prompt.

Cet exemple fonctionne bien car les trois rôles sont indépendants et peuvent explorer le problème sans attendre les uns les autres :

```text  theme={null}
Je conçois un outil CLI qui aide les développeurs à suivre les commentaires TODO dans
leur base de code. Créez une équipe d'agents pour explorer cela sous différents angles : un
coéquipier sur l'UX, un sur l'architecture technique, un jouant l'avocat du diable.
```

À partir de là, Claude crée une équipe avec une [liste de tâches partagée](/fr/interactive-mode#task-list), génère les coéquipiers pour chaque perspective, les fait explorer le problème, synthétise les conclusions et tente de [nettoyer l'équipe](#clean-up-the-team) une fois terminée.

Le terminal du chef liste tous les coéquipiers et sur quoi ils travaillent. Utilisez Maj+Bas pour parcourir les coéquipiers et leur envoyer un message directement. Après le dernier coéquipier, Maj+Bas revient au chef.

Si vous souhaitez que chaque coéquipier soit dans son propre volet divisé, consultez [Choisir un mode d'affichage](#choose-a-display-mode).

## Contrôler votre équipe d'agents

Dites au chef ce que vous voulez en langage naturel. Il gère la coordination d'équipe, l'assignation de tâches et la délégation en fonction de vos instructions.

### Choisir un mode d'affichage

Les équipes d'agents supportent deux modes d'affichage :

* **In-process** : tous les coéquipiers s'exécutent dans votre terminal principal. Utilisez Maj+Bas pour parcourir les coéquipiers et tapez pour leur envoyer un message directement. Fonctionne dans n'importe quel terminal, aucune configuration supplémentaire requise.
* **Volets divisés** : chaque coéquipier obtient son propre volet. Vous pouvez voir la sortie de tout le monde à la fois et cliquer dans un volet pour interagir directement. Nécessite tmux ou iTerm2.

<Note>
  `tmux` a des limitations connues sur certains systèmes d'exploitation et fonctionne traditionnellement mieux sur macOS. L'utilisation de `tmux -CC` dans iTerm2 est le point d'entrée suggéré dans `tmux`.
</Note>

La valeur par défaut est `"auto"`, qui utilise les volets divisés si vous êtes déjà en train de s'exécuter dans une session tmux, et in-process sinon. Le paramètre `"tmux"` active le mode volets divisés et détecte automatiquement s'il faut utiliser tmux ou iTerm2 en fonction de votre terminal. Pour remplacer, définissez `teammateMode` dans votre [configuration globale](/fr/settings#global-config-settings) à `~/.claude.json` :

```json  theme={null}
{
  "teammateMode": "in-process"
}
```

Pour forcer le mode in-process pour une seule session, passez-le en tant que drapeau :

```bash  theme={null}
claude --teammate-mode in-process
```

Le mode volets divisés nécessite soit [tmux](https://github.com/tmux/tmux/wiki) soit iTerm2 avec le CLI [`it2`](https://github.com/mkusaka/it2). Pour installer manuellement :

* **tmux** : installez via le gestionnaire de paquets de votre système. Consultez le [wiki tmux](https://github.com/tmux/tmux/wiki/Installing) pour les instructions spécifiques à la plateforme.
* **iTerm2** : installez le CLI [`it2`](https://github.com/mkusaka/it2), puis activez l'API Python dans **iTerm2 → Paramètres → Général → Magie → Activer l'API Python**.

### Spécifier les coéquipiers et les modèles

Claude décide du nombre de coéquipiers à générer en fonction de votre tâche, ou vous pouvez spécifier exactement ce que vous voulez :

```text  theme={null}
Créez une équipe avec 4 coéquipiers pour refactoriser ces modules en parallèle.
Utilisez Sonnet pour chaque coéquipier.
```

### Exiger l'approbation du plan pour les coéquipiers

Pour les tâches complexes ou risquées, vous pouvez exiger que les coéquipiers planifient avant de mettre en œuvre. Le coéquipier travaille en mode plan en lecture seule jusqu'à ce que le chef approuve son approche :

```text  theme={null}
Générez un coéquipier architecte pour refactoriser le module d'authentification.
Exigez l'approbation du plan avant qu'il ne fasse des modifications.
```

Lorsqu'un coéquipier termine la planification, il envoie une demande d'approbation du plan au chef. Le chef examine le plan et l'approuve ou le rejette avec des commentaires. S'il est rejeté, le coéquipier reste en mode plan, révise en fonction des commentaires et resoumis. Une fois approuvé, le coéquipier quitte le mode plan et commence la mise en œuvre.

Le chef prend les décisions d'approbation de manière autonome. Pour influencer le jugement du chef, donnez-lui des critères dans votre prompt, tels que « n'approuvez que les plans qui incluent la couverture de test » ou « rejetez les plans qui modifient le schéma de base de données ».

### Parler directement aux coéquipiers

Chaque coéquipier est une session Claude Code complète et indépendante. Vous pouvez envoyer un message à n'importe quel coéquipier directement pour donner des instructions supplémentaires, poser des questions de suivi ou rediriger son approche.

* **Mode in-process** : utilisez Maj+Bas pour parcourir les coéquipiers, puis tapez pour leur envoyer un message. Appuyez sur Entrée pour afficher la session d'un coéquipier, puis Échap pour interrompre son tour actuel. Appuyez sur Ctrl+T pour basculer la liste des tâches.
* **Mode volets divisés** : cliquez dans le volet d'un coéquipier pour interagir directement avec sa session. Chaque coéquipier a une vue complète de son propre terminal.

### Assigner et revendiquer des tâches

La liste de tâches partagée coordonne le travail dans l'équipe. Le chef crée des tâches et les coéquipiers les accomplissent. Les tâches ont trois états : en attente, en cours et terminées. Les tâches peuvent également dépendre d'autres tâches : une tâche en attente avec des dépendances non résolues ne peut pas être revendiquée jusqu'à ce que ces dépendances soient complétées.

Le chef peut assigner des tâches explicitement, ou les coéquipiers peuvent les revendiquer eux-mêmes :

* **Le chef assigne** : dites au chef quelle tâche donner à quel coéquipier
* **Auto-revendication** : après avoir terminé une tâche, un coéquipier choisit la prochaine tâche non assignée et non bloquée de sa propre initiative

La revendication de tâche utilise le verrouillage de fichiers pour prévenir les conditions de course lorsque plusieurs coéquipiers tentent de revendiquer la même tâche simultanément.

### Arrêter les coéquipiers

Pour terminer gracieusement la session d'un coéquipier :

```text  theme={null}
Demandez au coéquipier chercheur d'arrêter
```

Le chef envoie une demande d'arrêt. Le coéquipier peut approuver, quittant gracieusement, ou rejeter avec une explication.

### Nettoyer l'équipe

Lorsque vous avez terminé, demandez au chef de nettoyer :

```text  theme={null}
Nettoyez l'équipe
```

Cela supprime les ressources d'équipe partagées. Lorsque le chef exécute le nettoyage, il vérifie les coéquipiers actifs et échoue s'il y en a encore en cours d'exécution, alors arrêtez-les d'abord.

<Warning>
  Utilisez toujours le chef pour nettoyer. Les coéquipiers ne doivent pas exécuter le nettoyage car leur contexte d'équipe peut ne pas se résoudre correctement, laissant potentiellement les ressources dans un état incohérent.
</Warning>

### Appliquer des portes de qualité avec des hooks

Utilisez les [hooks](/fr/hooks) pour appliquer des règles lorsque les coéquipiers terminent le travail ou que les tâches sont créées ou complétées :

* [`TeammateIdle`](/fr/hooks#teammateidle) : s'exécute lorsqu'un coéquipier est sur le point de devenir inactif. Quittez avec le code 2 pour envoyer des commentaires et garder le coéquipier au travail.
* [`TaskCreated`](/fr/hooks#taskcreated) : s'exécute lorsqu'une tâche est en cours de création. Quittez avec le code 2 pour empêcher la création et envoyer des commentaires.
* [`TaskCompleted`](/fr/hooks#taskcompleted) : s'exécute lorsqu'une tâche est marquée comme complète. Quittez avec le code 2 pour empêcher la complétion et envoyer des commentaires.

## Comment fonctionnent les équipes d'agents

Cette section couvre l'architecture et la mécanique derrière les équipes d'agents. Si vous souhaitez commencer à les utiliser, consultez [Contrôler votre équipe d'agents](#control-your-agent-team) ci-dessus.

### Comment Claude démarre les équipes d'agents

Il y a deux façons de démarrer les équipes d'agents :

* **Vous demandez une équipe** : donnez à Claude une tâche qui bénéficie du travail parallèle et demandez explicitement une équipe d'agents. Claude en crée une en fonction de vos instructions.
* **Claude propose une équipe** : si Claude détermine que votre tâche bénéficierait du travail parallèle, il peut suggérer de créer une équipe. Vous confirmez avant qu'il ne procède.

Dans les deux cas, vous restez maître. Claude ne créera pas d'équipe sans votre approbation.

### Architecture

Une équipe d'agents se compose de :

| Composant             | Rôle                                                                                                |
| :-------------------- | :-------------------------------------------------------------------------------------------------- |
| **Chef d'équipe**     | La session Claude Code principale qui crée l'équipe, génère les coéquipiers et coordonne le travail |
| **Coéquipiers**       | Des instances Claude Code distinctes qui travaillent chacune sur des tâches assignées               |
| **Liste de tâches**   | Liste partagée d'éléments de travail que les coéquipiers revendiquent et complètent                 |
| **Boîte aux lettres** | Système de messagerie pour la communication entre agents                                            |

Consultez [Choisir un mode d'affichage](#choose-a-display-mode) pour les options de configuration d'affichage. Les messages des coéquipiers arrivent au chef automatiquement.

Le système gère automatiquement les dépendances de tâches. Lorsqu'un coéquipier complète une tâche dont d'autres tâches dépendent, les tâches bloquées se débloquent sans intervention manuelle.

Les équipes et les tâches sont stockées localement :

* **Configuration d'équipe** : `~/.claude/teams/{team-name}/config.json`
* **Liste de tâches** : `~/.claude/tasks/{team-name}/`

Claude Code génère automatiquement ces deux éléments lorsque vous créez une équipe et les met à jour à mesure que les coéquipiers rejoignent, deviennent inactifs ou partent. La configuration d'équipe contient l'état d'exécution tel que les ID de session et les ID de volet tmux, donc ne l'éditez pas à la main ou ne la pré-créez pas : vos modifications sont écrasées lors de la prochaine mise à jour d'état.

Pour définir des rôles de coéquipiers réutilisables, utilisez plutôt les [définitions de subagents](#use-subagent-definitions-for-teammates).

La configuration d'équipe contient un tableau `members` avec le nom de chaque coéquipier, l'ID d'agent et le type d'agent. Les coéquipiers peuvent lire ce fichier pour découvrir les autres membres de l'équipe.

Il n'y a pas d'équivalent au niveau du projet de la configuration d'équipe. Un fichier comme `.claude/teams/teams.json` dans votre répertoire de projet n'est pas reconnu comme configuration ; Claude le traite comme un fichier ordinaire.

### Utiliser les définitions de subagents pour les coéquipiers

Lors de la génération d'un coéquipier, vous pouvez référencer un type de [subagent](/fr/sub-agents) de n'importe quelle [portée de subagent](/fr/sub-agents#choose-the-subagent-scope) : projet, utilisateur, plugin ou défini par CLI. Le coéquipier hérite du système prompt, des outils et du modèle de ce subagent. Cela vous permet de définir un rôle une fois, comme un examinateur de sécurité ou un exécuteur de tests, et de le réutiliser à la fois comme subagent délégué et comme coéquipier d'équipe d'agents.

Pour utiliser une définition de subagent, mentionnez-la par nom lorsque vous demandez à Claude de générer le coéquipier :

```text  theme={null}
Générez un coéquipier utilisant le type d'agent security-reviewer pour auditer le module d'authentification.
```

### Permissions

Les coéquipiers commencent avec les paramètres de permission du chef. Si le chef s'exécute avec `--dangerously-skip-permissions`, tous les coéquipiers le font aussi. Après la génération, vous pouvez modifier les modes de coéquipiers individuels, mais vous ne pouvez pas définir les modes par coéquipier au moment de la génération.

### Contexte et communication

Chaque coéquipier a sa propre fenêtre de contexte. Lorsqu'il est généré, un coéquipier charge le même contexte de projet qu'une session régulière : CLAUDE.md, MCP servers et skills. Il reçoit également le prompt de génération du chef. L'historique de conversation du chef ne se transporte pas.

**Comment les coéquipiers partagent les informations :**

* **Livraison automatique de messages** : lorsque les coéquipiers envoient des messages, ils sont livrés automatiquement aux destinataires. Le chef n'a pas besoin d'interroger les mises à jour.
* **Notifications d'inactivité** : lorsqu'un coéquipier termine et s'arrête, il notifie automatiquement le chef.
* **Liste de tâches partagée** : tous les agents peuvent voir l'état des tâches et revendiquer le travail disponible.

**Messagerie des coéquipiers :**

* **message** : envoyer un message à un coéquipier spécifique
* **broadcast** : envoyer à tous les coéquipiers simultanément. À utiliser avec parcimonie, car les coûts augmentent avec la taille de l'équipe.

### Utilisation des tokens

Les équipes d'agents utilisent considérablement plus de tokens qu'une seule session. Chaque coéquipier a sa propre fenêtre de contexte, et l'utilisation des tokens augmente avec le nombre de coéquipiers actifs. Pour la recherche, l'examen et le travail sur les nouvelles fonctionnalités, les tokens supplémentaires en valent généralement la peine. Pour les tâches de routine, une seule session est plus rentable. Consultez les [coûts des tokens des équipes d'agents](/fr/costs#agent-team-token-costs) pour les conseils d'utilisation.

## Exemples de cas d'usage

Ces exemples montrent comment les équipes d'agents gèrent les tâches où l'exploration parallèle ajoute de la valeur.

### Exécuter un examen de code parallèle

Un seul examinateur tend à graviter vers un type de problème à la fois. Diviser les critères d'examen en domaines indépendants signifie que la sécurité, l'impact sur les performances et la couverture de test reçoivent tous une attention approfondie simultanément. Le prompt assigne à chaque coéquipier une lentille distincte pour qu'ils ne se chevauchent pas :

```text  theme={null}
Créez une équipe d'agents pour examiner la PR #142. Générez trois examinateurs :
- Un axé sur les implications de sécurité
- Un vérifiant l'impact sur les performances
- Un validant la couverture de test
Demandez-leur d'examiner et de signaler les conclusions.
```

Chaque examinateur travaille à partir de la même PR mais applique un filtre différent. Le chef synthétise les conclusions de tous les trois après qu'ils aient terminé.

### Enquêter avec des hypothèses concurrentes

Lorsque la cause première est peu claire, un seul agent tend à trouver une explication plausible et s'arrête. Le prompt combat cela en rendant les coéquipiers explicitement adversaires : le travail de chacun n'est pas seulement d'enquêter sur sa propre théorie mais de contester les autres.

```text  theme={null}
Les utilisateurs signalent que l'application se ferme après un message au lieu de rester connectée.
Générez 5 coéquipiers agents pour enquêter sur différentes hypothèses. Demandez-leur de se parler
pour essayer de réfuter les théories les uns des autres, comme un débat
scientifique. Mettez à jour le document des conclusions avec le consensus qui émerge.
```

La structure du débat est le mécanisme clé ici. L'enquête séquentielle souffre de l'ancrage : une fois qu'une théorie est explorée, l'enquête ultérieure est biaisée vers elle.

Avec plusieurs enquêteurs indépendants essayant activement de réfuter les uns les autres, la théorie qui survit est beaucoup plus susceptible d'être la cause première réelle.

## Meilleures pratiques

### Donner aux coéquipiers suffisamment de contexte

Les coéquipiers chargent automatiquement le contexte du projet, y compris CLAUDE.md, MCP servers et skills, mais ils n'héritent pas de l'historique de conversation du chef. Consultez [Contexte et communication](#context-and-communication) pour les détails. Incluez les détails spécifiques à la tâche dans le prompt de génération :

```text  theme={null}
Générez un coéquipier examinateur de sécurité avec le prompt : « Examinez le module d'authentification
à src/auth/ pour les vulnérabilités de sécurité. Concentrez-vous sur la gestion des tokens, la gestion
des sessions et la validation des entrées. L'application utilise des tokens JWT stockés dans
des cookies httpOnly. Signalez tout problème avec les évaluations de gravité. »
```

### Choisir une taille d'équipe appropriée

Il n'y a pas de limite stricte au nombre de coéquipiers, mais des contraintes pratiques s'appliquent :

* **Les coûts des tokens augmentent linéairement** : chaque coéquipier a sa propre fenêtre de contexte et consomme des tokens indépendamment. Consultez les [coûts des tokens des équipes d'agents](/fr/costs#agent-team-token-costs) pour les détails.
* **La surcharge de coordination augmente** : plus de coéquipiers signifie plus de communication, de coordination de tâches et de risques de conflits
* **Rendements décroissants** : au-delà d'un certain point, les coéquipiers supplémentaires n'accélèrent pas le travail proportionnellement

Commencez avec 3 à 5 coéquipiers pour la plupart des flux de travail. Cela équilibre le travail parallèle avec une coordination gérable. Les exemples de ce guide utilisent 3 à 5 coéquipiers car cette plage fonctionne bien dans différents types de tâches.

Avoir 5 à 6 [tâches](/fr/agent-teams#architecture) par coéquipier garde tout le monde productif sans changement de contexte excessif. Si vous avez 15 tâches indépendantes, 3 coéquipiers est un bon point de départ.

Augmentez l'échelle uniquement lorsque le travail bénéficie véritablement d'avoir des coéquipiers travaillant simultanément. Trois coéquipiers ciblés surpassent souvent cinq dispersés.

### Dimensionner les tâches de manière appropriée

* **Trop petites** : la surcharge de coordination dépasse le bénéfice
* **Trop grandes** : les coéquipiers travaillent trop longtemps sans points de contrôle, augmentant le risque d'effort gaspillé
* **Juste bien** : des unités autonomes qui produisent un livrable clair, comme une fonction, un fichier de test ou un examen

<Tip>
  Le chef divise le travail en tâches et les assigne aux coéquipiers automatiquement. S'il ne crée pas assez de tâches, demandez-lui de diviser le travail en morceaux plus petits. Avoir 5 à 6 tâches par coéquipier garde tout le monde productif et permet au chef de réassigner le travail si quelqu'un est bloqué.
</Tip>

### Attendre que les coéquipiers terminent

Parfois, le chef commence à mettre en œuvre des tâches lui-même au lieu d'attendre les coéquipiers. Si vous remarquez cela :

```text  theme={null}
Attendez que vos coéquipiers complètent leurs tâches avant de procéder
```

### Commencer par la recherche et l'examen

Si vous êtes nouveau aux équipes d'agents, commencez par des tâches qui ont des limites claires et ne nécessitent pas d'écrire du code : examiner une PR, rechercher une bibliothèque ou enquêter sur un bug. Ces tâches montrent la valeur de l'exploration parallèle sans les défis de coordination qui accompagnent la mise en œuvre parallèle.

### Éviter les conflits de fichiers

Deux coéquipiers éditant le même fichier entraîne des écrasements. Divisez le travail pour que chaque coéquipier possède un ensemble de fichiers différent.

### Surveiller et diriger

Vérifiez la progression des coéquipiers, redirigez les approches qui ne fonctionnent pas et synthétisez les conclusions au fur et à mesure qu'elles arrivent. Laisser une équipe s'exécuter sans surveillance pendant trop longtemps augmente le risque d'effort gaspillé.

## Dépannage

### Les coéquipiers n'apparaissent pas

Si les coéquipiers n'apparaissent pas après avoir demandé à Claude de créer une équipe :

* En mode in-process, les coéquipiers peuvent déjà être en cours d'exécution mais non visibles. Appuyez sur Maj+Bas pour parcourir les coéquipiers actifs.
* Vérifiez que la tâche que vous avez donnée à Claude était suffisamment complexe pour justifier une équipe. Claude décide s'il faut générer des coéquipiers en fonction de la tâche.
* Si vous avez explicitement demandé des volets divisés, assurez-vous que tmux est installé et disponible dans votre PATH :
  ```bash  theme={null}
  which tmux
  ```
* Pour iTerm2, vérifiez que le CLI `it2` est installé et que l'API Python est activée dans les préférences d'iTerm2.

### Trop de demandes de permission

Les demandes de permission des coéquipiers remontent au chef, ce qui peut créer des frictions. Pré-approuvez les opérations courantes dans vos [paramètres de permission](/fr/permissions) avant de générer les coéquipiers pour réduire les interruptions.

### Les coéquipiers s'arrêtent sur les erreurs

Les coéquipiers peuvent s'arrêter après avoir rencontré des erreurs au lieu de se rétablir. Vérifiez leur sortie en utilisant Maj+Bas en mode in-process ou en cliquant sur le volet en mode divisé, puis :

* Donnez-leur des instructions supplémentaires directement
* Générez un coéquipier de remplacement pour continuer le travail

### Le chef s'arrête avant que le travail ne soit terminé

Le chef peut décider que l'équipe est terminée avant que toutes les tâches ne soient réellement complètes. Si cela se produit, dites-lui de continuer. Vous pouvez également dire au chef d'attendre que les coéquipiers terminent avant de procéder s'il commence à faire du travail au lieu de déléguer.

### Sessions tmux orphelines

Si une session tmux persiste après la fin de l'équipe, elle peut ne pas avoir été complètement nettoyée. Listez les sessions et tuez celle créée par l'équipe :

```bash  theme={null}
tmux ls
tmux kill-session -t <session-name>
```

## Limitations

Les équipes d'agents sont expérimentales. Les limitations actuelles à connaître :

* **Pas de reprise de session avec les coéquipiers in-process** : `/resume` et `/rewind` ne restaurent pas les coéquipiers in-process. Après la reprise d'une session, le chef peut tenter de envoyer un message aux coéquipiers qui n'existent plus. Si cela se produit, dites au chef de générer de nouveaux coéquipiers.
* **L'état des tâches peut être en retard** : les coéquipiers échouent parfois à marquer les tâches comme complètes, ce qui bloque les tâches dépendantes. Si une tâche semble bloquée, vérifiez si le travail est réellement terminé et mettez à jour l'état de la tâche manuellement ou dites au chef de pousser le coéquipier.
* **L'arrêt peut être lent** : les coéquipiers terminent leur demande actuelle ou appel d'outil avant de s'arrêter, ce qui peut prendre du temps.
* **Une équipe par session** : un chef ne peut gérer qu'une seule équipe à la fois. Nettoyez l'équipe actuelle avant de démarrer une nouvelle.
* **Pas d'équipes imbriquées** : les coéquipiers ne peuvent pas générer leurs propres équipes ou coéquipiers. Seul le chef peut gérer l'équipe.
* **Le chef est fixe** : la session qui crée l'équipe est le chef pour sa durée de vie. Vous ne pouvez pas promouvoir un coéquipier en chef ou transférer le leadership.
* **Permissions définies au moment de la génération** : tous les coéquipiers commencent avec le mode de permission du chef. Vous pouvez modifier les modes de coéquipiers individuels après la génération, mais vous ne pouvez pas définir les modes par coéquipier au moment de la génération.
* **Les volets divisés nécessitent tmux ou iTerm2** : le mode in-process par défaut fonctionne dans n'importe quel terminal. Le mode volets divisés n'est pas supporté dans le terminal intégré de VS Code, Windows Terminal ou Ghostty.

<Tip>
  **`CLAUDE.md` fonctionne normalement** : les coéquipiers lisent les fichiers `CLAUDE.md` de leur répertoire de travail. Utilisez ceci pour fournir des conseils spécifiques au projet à tous les coéquipiers.
</Tip>

## Prochaines étapes

Explorez les approches connexes pour le travail parallèle et la délégation :

* **Délégation légère** : les [subagents](/fr/sub-agents) génèrent des agents auxiliaires pour la recherche ou la vérification au sein de votre session, mieux pour les tâches qui n'ont pas besoin de coordination inter-agents
* **Sessions parallèles manuelles** : les [Git worktrees](/fr/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) vous permettent d'exécuter plusieurs sessions Claude Code vous-même sans coordination d'équipe automatisée
* **Comparer les approches** : consultez la comparaison [subagent vs équipe d'agents](/fr/features-overview#compare-similar-features) pour une répartition côte à côte
