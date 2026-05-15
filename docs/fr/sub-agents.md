> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Créer des sous-agents personnalisés

> Créez et utilisez des sous-agents IA spécialisés dans Claude Code pour des workflows spécifiques à des tâches et une meilleure gestion du contexte.

Les sous-agents sont des assistants IA spécialisés qui gèrent des types de tâches spécifiques. Utilisez-en un lorsqu'une tâche secondaire inonderait votre conversation principale avec des résultats de recherche, des journaux ou des contenus de fichiers que vous ne référencerez plus : le sous-agent effectue ce travail dans son propre contexte et retourne uniquement le résumé. Définissez un sous-agent personnalisé lorsque vous générez constamment le même type de travailleur avec les mêmes instructions.

Chaque sous-agent s'exécute dans sa propre fenêtre de contexte avec une invite système personnalisée, un accès à des outils spécifiques et des permissions indépendantes. Lorsque Claude rencontre une tâche qui correspond à la description d'un sous-agent, il délègue à ce sous-agent, qui fonctionne indépendamment et retourne les résultats. Pour voir les économies de contexte en pratique, la [visualisation de la fenêtre de contexte](/fr/context-window) vous guide à travers une session où un sous-agent gère la recherche dans sa propre fenêtre séparée.

<Note>
  Les sous-agents fonctionnent au sein d'une seule session. Pour exécuter de nombreuses sessions indépendantes en parallèle et les surveiller depuis un seul endroit, consultez [les agents en arrière-plan](/fr/agent-view). Pour les sessions qui communiquent entre elles, consultez [les équipes d'agents](/fr/agent-teams).
</Note>

Les sous-agents vous aident à :

* **Préserver le contexte** en gardant l'exploration et l'implémentation en dehors de votre conversation principale
* **Appliquer des contraintes** en limitant les outils qu'un sous-agent peut utiliser
* **Réutiliser les configurations** dans les projets avec des sous-agents au niveau utilisateur
* **Spécialiser le comportement** avec des invites système ciblées pour des domaines spécifiques
* **Contrôler les coûts** en acheminant les tâches vers des modèles plus rapides et moins chers comme Haiku

Claude utilise la description de chaque sous-agent pour décider quand déléguer les tâches. Lorsque vous créez un sous-agent, écrivez une description claire pour que Claude sache quand l'utiliser.

Claude Code inclut plusieurs sous-agents intégrés comme **Explore**, **Plan** et **general-purpose**. Vous pouvez également créer des sous-agents personnalisés pour gérer des tâches spécifiques. Cette page couvre :

* [Sous-agents intégrés](#built-in-subagents)
* [Comment créer les vôtres](#quickstart-create-your-first-subagent)
* [Options de configuration complètes](#configure-subagents)
* [Modèles de travail avec les sous-agents](#work-with-subagents)
* [Sous-agents dupliqués](#fork-the-current-conversation)
* [Exemples de sous-agents](#example-subagents)

## Sous-agents intégrés

Claude Code inclut des sous-agents intégrés que Claude utilise automatiquement le cas échéant. Chacun hérite des permissions de la conversation parent avec des restrictions d'outils supplémentaires.

<Tabs>
  <Tab title="Explore">
    Un agent rapide et en lecture seule optimisé pour la recherche et l'analyse de bases de code.

    * **Modèle** : Haiku (rapide, faible latence)
    * **Outils** : Outils en lecture seule (accès refusé aux outils Write et Edit)
    * **Objectif** : Découverte de fichiers, recherche de code, exploration de base de code

    Claude délègue à Explore lorsqu'il doit rechercher ou comprendre une base de code sans apporter de modifications. Cela garde les résultats d'exploration en dehors du contexte de votre conversation principale.

    Lors de l'invocation d'Explore, Claude spécifie un niveau de minutie : **quick** pour les recherches ciblées, **medium** pour l'exploration équilibrée, ou **very thorough** pour l'analyse complète.
  </Tab>

  <Tab title="Plan">
    Un agent de recherche utilisé pendant le [mode plan](/fr/permission-modes#analyze-before-you-edit-with-plan-mode) pour rassembler le contexte avant de présenter un plan.

    * **Modèle** : Hérité de la conversation principale
    * **Outils** : Outils en lecture seule (accès refusé aux outils Write et Edit)
    * **Objectif** : Recherche de base de code pour la planification

    Lorsque vous êtes en mode plan et que Claude doit comprendre votre base de code, il délègue la recherche au sous-agent Plan. Cela empêche l'imbrication infinie (les sous-agents ne peuvent pas générer d'autres sous-agents) tout en rassemblant le contexte nécessaire.
  </Tab>

  <Tab title="General-purpose">
    Un agent capable pour les tâches complexes et multi-étapes qui nécessitent à la fois l'exploration et l'action.

    * **Modèle** : Hérité de la conversation principale
    * **Outils** : Tous les outils
    * **Objectif** : Recherche complexe, opérations multi-étapes, modifications de code

    Claude délègue à general-purpose lorsque la tâche nécessite à la fois l'exploration et la modification, un raisonnement complexe pour interpréter les résultats, ou plusieurs étapes dépendantes.
  </Tab>

  <Tab title="Other">
    Claude Code inclut des agents d'assistance supplémentaires pour des tâches spécifiques. Ceux-ci sont généralement invoqués automatiquement, vous n'avez donc pas besoin de les utiliser directement.

    | Agent             | Modèle | Quand Claude l'utilise                                                  |
    | :---------------- | :----- | :---------------------------------------------------------------------- |
    | statusline-setup  | Sonnet | Lorsque vous exécutez `/statusline` pour configurer votre ligne d'état  |
    | claude-code-guide | Haiku  | Lorsque vous posez des questions sur les fonctionnalités de Claude Code |
  </Tab>
</Tabs>

Au-delà de ces sous-agents intégrés, vous pouvez créer les vôtres avec des invites personnalisées, des restrictions d'outils, des modes de permission, des hooks et des skills. Les sections suivantes montrent comment commencer et personnaliser les sous-agents.

## Démarrage rapide : créer votre premier sous-agent

Les sous-agents sont définis dans des fichiers Markdown avec du frontmatter YAML. Vous pouvez les [créer manuellement](#write-subagent-files) ou utiliser la commande `/agents`.

Cette procédure pas à pas vous guide dans la création d'un sous-agent au niveau utilisateur avec la commande `/agents`. Le sous-agent examine le code et suggère des améliorations pour la base de code.

<Steps>
  <Step title="Ouvrir l'interface des sous-agents">
    Dans Claude Code, exécutez :

    ```text theme={null}
    /agents
    ```
  </Step>

  <Step title="Choisir un emplacement">
    Basculez vers l'onglet **Library**, sélectionnez **Create new agent**, puis choisissez **Personal**. Cela enregistre le sous-agent dans `~/.claude/agents/` pour qu'il soit disponible dans tous vos projets.
  </Step>

  <Step title="Générer avec Claude">
    Sélectionnez **Generate with Claude**. Lorsque vous y êtes invité, décrivez le sous-agent :

    ```text theme={null}
    A code improvement agent that scans files and suggests improvements
    for readability, performance, and best practices. It should explain
    each issue, show the current code, and provide an improved version.
    ```

    Claude génère l'identifiant, la description et l'invite système pour vous.
  </Step>

  <Step title="Sélectionner les outils">
    Pour un examinateur en lecture seule, désélectionnez tout sauf **Read-only tools**. Si vous gardez tous les outils sélectionnés, le sous-agent hérite de tous les outils disponibles pour la conversation principale.
  </Step>

  <Step title="Sélectionner le modèle">
    Choisissez le modèle que le sous-agent utilise. Pour cet exemple d'agent, sélectionnez **Sonnet**, qui équilibre la capacité et la vitesse pour analyser les modèles de code.
  </Step>

  <Step title="Choisir une couleur">
    Choisissez une couleur de fond pour le sous-agent. Cela vous aide à identifier quel sous-agent s'exécute dans l'interface utilisateur.
  </Step>

  <Step title="Configurer la mémoire">
    Sélectionnez **User scope** pour donner au sous-agent un [répertoire de mémoire persistante](#enable-persistent-memory) à `~/.claude/agent-memory/`. Le sous-agent utilise ceci pour accumuler des insights dans les conversations, comme les modèles de base de code et les problèmes récurrents. Sélectionnez **None** si vous ne souhaitez pas que le sous-agent persiste les apprentissages.
  </Step>

  <Step title="Enregistrer et essayer">
    Examinez le résumé de la configuration. Appuyez sur `s` ou `Entrée` pour enregistrer, ou appuyez sur `e` pour enregistrer et modifier le fichier dans votre éditeur. Le sous-agent est disponible immédiatement. Essayez-le :

    ```text theme={null}
    Use the code-improver agent to suggest improvements in this project
    ```

    Claude délègue à votre nouveau sous-agent, qui analyse la base de code et retourne les suggestions d'amélioration.
  </Step>
</Steps>

Vous avez maintenant un sous-agent que vous pouvez utiliser dans n'importe quel projet sur votre machine pour analyser les bases de code et suggérer des améliorations.

Vous pouvez également créer des sous-agents manuellement en tant que fichiers Markdown, les définir via des drapeaux CLI ou les distribuer via des plugins. Les sections suivantes couvrent toutes les options de configuration.

## Configurer les sous-agents

### Utiliser la commande /agents

La commande `/agents` ouvre une interface à onglets pour gérer les sous-agents. L'onglet **Running** affiche les sous-agents en direct et vous permet de les ouvrir ou de les arrêter. L'onglet **Library** vous permet de :

* Afficher tous les sous-agents disponibles (intégrés, utilisateur, projet et plugin)
* Créer de nouveaux sous-agents avec une configuration guidée ou une génération Claude
* Modifier la configuration des sous-agents existants et l'accès aux outils
* Supprimer les sous-agents personnalisés
* Voir quels sous-agents sont actifs en cas de doublons

C'est la méthode recommandée pour créer et gérer les sous-agents. Pour la création manuelle ou l'automatisation, vous pouvez également ajouter des fichiers de sous-agent directement.

### Choisir la portée du sous-agent

Les sous-agents sont des fichiers Markdown avec du frontmatter YAML. Stockez-les dans différents emplacements selon la portée. Lorsque plusieurs sous-agents partagent le même nom, l'emplacement de priorité plus élevée gagne.

| Emplacement                    | Portée                        | Priorité           | Comment créer                                |
| :----------------------------- | :---------------------------- | :----------------- | :------------------------------------------- |
| Paramètres gérés               | À l'échelle de l'organisation | 1 (la plus élevée) | Déployé via [paramètres gérés](/fr/settings) |
| Drapeau CLI `--agents`         | Session actuelle              | 2                  | Passer JSON lors du lancement de Claude Code |
| `.claude/agents/`              | Projet actuel                 | 3                  | Interactif ou manuel                         |
| `~/.claude/agents/`            | Tous vos projets              | 4                  | Interactif ou manuel                         |
| Répertoire `agents/` du plugin | Où le plugin est activé       | 5 (la plus basse)  | Installé avec les [plugins](/fr/plugins)     |

**Les sous-agents de projet** (`.claude/agents/`) sont idéaux pour les sous-agents spécifiques à une base de code. Enregistrez-les dans le contrôle de version pour que votre équipe puisse les utiliser et les améliorer de manière collaborative.

Les sous-agents de projet sont découverts en remontant à partir du répertoire de travail actuel. Les répertoires ajoutés avec `--add-dir` [accordent uniquement l'accès aux fichiers](/fr/permissions#additional-directories-grant-file-access-not-configuration) et ne sont pas analysés pour les sous-agents. Pour partager les sous-agents entre les projets, utilisez `~/.claude/agents/` ou un [plugin](/fr/plugins).

**Les sous-agents utilisateur** (`~/.claude/agents/`) sont des sous-agents personnels disponibles dans tous vos projets.

Claude Code analyse `.claude/agents/` et `~/.claude/agents/` de manière récursive, vous pouvez donc organiser les définitions dans des sous-dossiers tels que `agents/review/` ou `agents/research/`. Le chemin du sous-répertoire n'affecte pas la façon dont un sous-agent est identifié ou invoqué, car l'identité provient uniquement du champ frontmatter `name`. Gardez les valeurs `name` uniques dans tout l'arborescence : si deux fichiers dans une même portée déclarent le même nom, Claude Code en conserve un et rejette l'autre sans avertissement.

Les répertoires `agents/` des plugins sont également analysés de manière récursive. Contrairement aux portées de projet et utilisateur, un sous-dossier à l'intérieur du répertoire `agents/` d'un plugin devient partie de l'[identifiant limité](#invoke-subagents-explicitly) : un fichier à `agents/review/security.md` dans le plugin `my-plugin` s'enregistre comme `my-plugin:review:security`.

**Les sous-agents définis par CLI** sont passés en JSON lors du lancement de Claude Code. Ils n'existent que pour cette session et ne sont pas enregistrés sur le disque, ce qui les rend utiles pour les tests rapides ou les scripts d'automatisation. Vous pouvez définir plusieurs sous-agents dans un seul appel `--agents` :

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    claude --agents '{
      "code-reviewer": {
        "description": "Expert code reviewer. Use proactively after code changes.",
        "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
        "model": "sonnet"
      },
      "debugger": {
        "description": "Debugging specialist for errors and test failures.",
        "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
      }
    }'
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    claude --agents @'
    {
      "code-reviewer": {
        "description": "Expert code reviewer. Use proactively after code changes.",
        "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
        "model": "sonnet"
      },
      "debugger": {
        "description": "Debugging specialist for errors and test failures.",
        "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
      }
    }
    '@
    ```
  </Tab>
</Tabs>

Le drapeau `--agents` accepte JSON avec les mêmes champs de [frontmatter](#supported-frontmatter-fields) que les sous-agents basés sur fichier : `description`, `prompt`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation` et `color`. Utilisez `prompt` pour l'invite système, équivalent au corps markdown dans les sous-agents basés sur fichier.

**Les sous-agents gérés** sont déployés par les administrateurs de l'organisation. Placez les fichiers markdown dans `.claude/agents/` à l'intérieur du [répertoire des paramètres gérés](/fr/settings#settings-files), en utilisant le même format de frontmatter que les sous-agents de projet et utilisateur. Les définitions gérées prennent précédence sur les sous-agents de projet et utilisateur portant le même nom.

**Les sous-agents de plugin** proviennent des [plugins](/fr/plugins) que vous avez installés. Ils apparaissent dans `/agents` aux côtés de vos sous-agents personnalisés. Consultez la [référence des composants de plugin](/fr/plugins-reference#agents) pour plus de détails sur la création de sous-agents de plugin.

<Note>
  Pour des raisons de sécurité, les sous-agents de plugin ne prennent pas en charge les champs frontmatter `hooks`, `mcpServers` ou `permissionMode`. Ces champs sont ignorés lors du chargement des agents à partir d'un plugin. Si vous en avez besoin, copiez le fichier d'agent dans `.claude/agents/` ou `~/.claude/agents/`. Vous pouvez également ajouter des règles à [`permissions.allow`](/fr/settings#permission-settings) dans `settings.json` ou `settings.local.json`, mais ces règles s'appliquent à l'ensemble de la session, pas seulement au sous-agent du plugin.
</Note>

Les définitions de sous-agent de l'une de ces portées sont également disponibles pour les [équipes d'agents](/fr/agent-teams#use-subagent-definitions-for-teammates) : lors du lancement d'un coéquipier, vous pouvez référencer un type de sous-agent et le coéquipier utilise ses `tools` et son `model`, avec le corps de la définition ajouté à l'invite système du coéquipier comme instructions supplémentaires. Consultez [équipes d'agents](/fr/agent-teams#use-subagent-definitions-for-teammates) pour voir quels champs de frontmatter s'appliquent sur ce chemin.

### Écrire des fichiers de sous-agent

Les fichiers de sous-agent utilisent du frontmatter YAML pour la configuration, suivi de l'invite système en Markdown :

<Note>
  Les sous-agents sont chargés au démarrage de la session. Si vous ajoutez ou modifiez un fichier de sous-agent directement sur le disque, redémarrez votre session pour le charger. Les sous-agents créés via l'interface `/agents` prennent effet immédiatement sans redémarrage.
</Note>

```markdown theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

Le frontmatter définit les métadonnées et la configuration du sous-agent. Le corps devient l'invite système qui guide le comportement du sous-agent. Les sous-agents reçoivent uniquement cette invite système (plus les détails d'environnement de base comme le répertoire de travail), pas l'invite système complète de Claude Code.

Un sous-agent démarre dans le répertoire de travail actuel de la conversation principale. Au sein d'un sous-agent, les commandes `cd` ne persistent pas entre les appels d'outils Bash ou PowerShell et n'affectent pas le répertoire de travail de la conversation principale. Pour donner au sous-agent une copie isolée du référentiel à la place, définissez [`isolation: worktree`](#supported-frontmatter-fields).

#### Champs de frontmatter pris en charge

Les champs suivants peuvent être utilisés dans le frontmatter YAML. Seuls `name` et `description` sont obligatoires.

| Champ             | Obligatoire | Description                                                                                                                                                                                                                                                                                                                                                                                    |
| :---------------- | :---------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | Oui         | Identifiant unique utilisant des lettres minuscules et des tirets. Les [Hooks](/fr/hooks#subagentstart) reçoivent cette valeur comme `agent_type`. Le nom du fichier n'a pas besoin de correspondre                                                                                                                                                                                            |
| `description`     | Oui         | Quand Claude doit déléguer à ce sous-agent                                                                                                                                                                                                                                                                                                                                                     |
| `tools`           | Non         | [Outils](#available-tools) que le sous-agent peut utiliser. Hérite de tous les outils s'il est omis. Pour précharger les Skills dans le contexte, utilisez le champ `skills` plutôt que de lister `Skill` ici                                                                                                                                                                                  |
| `disallowedTools` | Non         | Outils à refuser, supprimés de la liste héritée ou spécifiée                                                                                                                                                                                                                                                                                                                                   |
| `model`           | Non         | [Modèle](#choose-a-model) à utiliser : `sonnet`, `opus`, `haiku`, un ID de modèle complet (par exemple, `claude-opus-4-7`), ou `inherit`. Par défaut `inherit`                                                                                                                                                                                                                                 |
| `permissionMode`  | Non         | [Mode de permission](#permission-modes) : `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions` ou `plan`. Ignoré pour les [sous-agents de plugin](#choose-the-subagent-scope)                                                                                                                                                                                                      |
| `maxTurns`        | Non         | Nombre maximum de tours d'agent avant que le sous-agent s'arrête                                                                                                                                                                                                                                                                                                                               |
| `skills`          | Non         | [Skills](/fr/skills) à précharger dans le contexte du sous-agent au démarrage. Le contenu complet de la skill est injecté, pas seulement la description. Les sous-agents peuvent toujours invoquer les skills de projet, utilisateur et plugin non listées via l'outil Skill                                                                                                                   |
| `mcpServers`      | Non         | [Serveurs MCP](/fr/mcp) disponibles pour ce sous-agent. Chaque entrée est soit un nom de serveur référençant un serveur déjà configuré (par exemple, `"slack"`) soit une définition en ligne avec le nom du serveur comme clé et une [configuration de serveur MCP](/fr/mcp#installing-mcp-servers) complète comme valeur. Ignoré pour les [sous-agents de plugin](#choose-the-subagent-scope) |
| `hooks`           | Non         | [Hooks de cycle de vie](#define-hooks-for-subagents) limités à ce sous-agent. Ignoré pour les [sous-agents de plugin](#choose-the-subagent-scope)                                                                                                                                                                                                                                              |
| `memory`          | Non         | [Portée de la mémoire persistante](#enable-persistent-memory) : `user`, `project` ou `local`. Active l'apprentissage entre sessions                                                                                                                                                                                                                                                            |
| `background`      | Non         | Définir sur `true` pour toujours exécuter ce sous-agent en tant que [tâche d'arrière-plan](#run-subagents-in-foreground-or-background). Par défaut : `false`                                                                                                                                                                                                                                   |
| `effort`          | Non         | Niveau d'effort lorsque ce sous-agent est actif. Remplace le niveau d'effort de la session. Par défaut : hérite de la session. Options : `low`, `medium`, `high`, `xhigh`, `max` ; les niveaux disponibles dépendent du modèle                                                                                                                                                                 |
| `isolation`       | Non         | Définir sur `worktree` pour exécuter le sous-agent dans un [git worktree](/fr/worktrees) temporaire, ce qui lui donne une copie isolée du référentiel. Le worktree est automatiquement nettoyé si le sous-agent n'apporte aucune modification                                                                                                                                                  |
| `color`           | Non         | Couleur d'affichage pour le sous-agent dans la liste des tâches et la transcription. Accepte `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink` ou `cyan`                                                                                                                                                                                                                            |
| `initialPrompt`   | Non         | Auto-soumis comme le premier tour utilisateur lorsque cet agent s'exécute en tant qu'agent de session principal (via `--agent` ou le paramètre `agent`). Les [commandes](/fr/commands) et les [skills](/fr/skills) sont traitées. Préfixé à tout invite fourni par l'utilisateur                                                                                                               |

### Choisir un modèle

Le champ `model` contrôle quel [modèle IA](/fr/model-config) le sous-agent utilise :

* **Alias de modèle** : Utilisez l'un des alias disponibles : `sonnet`, `opus` ou `haiku`
* **ID de modèle complet** : Utilisez un ID de modèle complet tel que `claude-opus-4-7` ou `claude-sonnet-4-6`. Accepte les mêmes valeurs que le drapeau `--model`
* **inherit** : Utilisez le même modèle que la conversation principale
* **Omis** : S'il n'est pas spécifié, par défaut `inherit` (utilise le même modèle que la conversation principale)

Lorsque Claude invoque un sous-agent, il peut également passer un paramètre `model` pour cette invocation spécifique. Claude Code résout le modèle du sous-agent dans cet ordre :

1. La variable d'environnement [`CLAUDE_CODE_SUBAGENT_MODEL`](/fr/model-config#environment-variables), si elle est définie
2. Le paramètre `model` par invocation
3. Le frontmatter `model` de la définition du sous-agent
4. Le modèle de la conversation principale

### Contrôler les capacités des sous-agents

Vous pouvez contrôler ce que les sous-agents peuvent faire via l'accès aux outils, les modes de permission et les règles conditionnelles.

#### Outils disponibles

Les sous-agents peuvent utiliser n'importe lequel des [outils internes](/fr/tools-reference) de Claude Code. Par défaut, les sous-agents héritent de tous les outils de la conversation principale, y compris les outils MCP.

Pour restreindre les outils, utilisez soit le champ `tools` (liste blanche) soit le champ `disallowedTools` (liste noire). Cet exemple utilise `tools` pour autoriser exclusivement Read, Grep, Glob et Bash. Le sous-agent ne peut pas modifier les fichiers, écrire des fichiers ou utiliser des outils MCP :

```yaml theme={null}
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

Cet exemple utilise `disallowedTools` pour hériter de tous les outils de la conversation principale sauf Write et Edit. Le sous-agent conserve Bash, les outils MCP et tout le reste :

```yaml theme={null}
---
name: no-writes
description: Inherits every tool except file writes
disallowedTools: Write, Edit
---
```

Si les deux sont définis, `disallowedTools` est appliqué en premier, puis `tools` est résolu par rapport au pool restant. Un outil listé dans les deux est supprimé.

#### Restreindre les sous-agents qui peuvent être générés

Lorsqu'un agent s'exécute en tant que thread principal avec `claude --agent`, il peut générer des sous-agents à l'aide de l'outil Agent. Pour restreindre les types de sous-agents qu'il peut générer, utilisez la syntaxe `Agent(agent_type)` dans le champ `tools`.

<Note>Dans la version 2.1.63, l'outil Task a été renommé en Agent. Les références `Task(...)` existantes dans les paramètres et les définitions d'agent fonctionnent toujours comme des alias.</Note>

```yaml theme={null}
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

C'est une liste blanche : seuls les sous-agents `worker` et `researcher` peuvent être générés. Si l'agent essaie de générer un autre type, la demande échoue et l'agent ne voit que les types autorisés dans son invite. Pour bloquer des agents spécifiques tout en autorisant tous les autres, utilisez plutôt [`permissions.deny`](#disable-specific-subagents).

Pour autoriser la génération de n'importe quel sous-agent sans restrictions, utilisez `Agent` sans parenthèses :

```yaml theme={null}
tools: Agent, Read, Bash
```

Si `Agent` est complètement omis de la liste `tools`, l'agent ne peut générer aucun sous-agent. Cette restriction s'applique uniquement aux agents s'exécutant en tant que thread principal avec `claude --agent`. Les sous-agents ne peuvent pas générer d'autres sous-agents, donc `Agent(agent_type)` n'a aucun effet dans les définitions de sous-agent.

#### Limiter les serveurs MCP à un sous-agent

Utilisez le champ `mcpServers` pour donner à un sous-agent l'accès aux serveurs [MCP](/fr/mcp) qui ne sont pas disponibles dans la conversation principale. Les serveurs en ligne définis ici sont connectés au démarrage du sous-agent et déconnectés à la fin. Les références de chaîne partagent la connexion de la session parent.

<Note>
  Le champ `mcpServers` s'applique dans les deux contextes où un fichier d'agent peut s'exécuter :

  * En tant que sous-agent, généré via l'outil Agent ou une @-mention
  * En tant que session principale, lancée avec [`--agent`](#invoke-subagents-explicitly) ou le paramètre `agent`

  Lorsque l'agent est la session principale, les définitions de serveur en ligne se connectent au démarrage aux côtés des serveurs de [`.mcp.json`](/fr/mcp) et des fichiers de paramètres.
</Note>

Chaque entrée de la liste est soit une définition de serveur en ligne, soit une chaîne référençant un serveur MCP déjà configuré dans votre session :

```yaml theme={null}
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.
```

Les définitions en ligne utilisent le même schéma que les entrées de serveur `.mcp.json` (`stdio`, `http`, `sse`, `ws`), indexées par le nom du serveur.

Pour garder un serveur MCP en dehors de la conversation principale et éviter que ses descriptions d'outils ne consomment du contexte, définissez-le en ligne ici plutôt que dans `.mcp.json`. Le sous-agent obtient les outils ; la conversation parent ne les obtient pas.

#### Modes de permission

Le champ `permissionMode` contrôle comment le sous-agent gère les invites de permission. Les sous-agents héritent du contexte de permission de la conversation principale et peuvent remplacer le mode, sauf lorsque le mode parent prend précédence comme décrit ci-dessous.

| Mode                | Comportement                                                                                                                                                       |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Vérification de permission standard avec invites                                                                                                                   |
| `acceptEdits`       | Auto-accepter les modifications de fichiers et les commandes courantes du système de fichiers pour les chemins du répertoire de travail ou `additionalDirectories` |
| `auto`              | [Mode auto](/fr/permission-modes#eliminate-prompts-with-auto-mode) : un classificateur IA évalue chaque appel d'outil                                              |
| `dontAsk`           | Auto-refuser les invites de permission (les outils explicitement autorisés fonctionnent toujours)                                                                  |
| `bypassPermissions` | Ignorer les invites de permission                                                                                                                                  |
| `plan`              | Mode plan (exploration en lecture seule)                                                                                                                           |

<Warning>
  Utilisez `bypassPermissions` avec prudence. Il ignore les invites de permission, permettant au sous-agent d'exécuter des opérations sans approbation, y compris les écritures dans `.git`, `.claude`, `.vscode`, `.idea` et `.husky`. Les suppressions du répertoire racine et du répertoire personnel comme `rm -rf /` demandent toujours une confirmation en tant que disjoncteur. Consultez [modes de permission](/fr/permission-modes#skip-all-checks-with-bypasspermissions-mode) pour plus de détails.
</Warning>

Si le parent utilise `bypassPermissions` ou `acceptEdits`, cela prend précédence et ne peut pas être remplacé. Si le parent utilise le [mode auto](/fr/permission-modes#eliminate-prompts-with-auto-mode), le sous-agent hérite du mode auto et tout `permissionMode` dans son frontmatter est ignoré : le classificateur évalue les appels d'outils du sous-agent avec les mêmes règles de blocage et d'autorisation que la session parent.

#### Précharger les skills dans les sous-agents

Utilisez le champ `skills` pour injecter le contenu de la skill dans le contexte du sous-agent au démarrage. Cela donne au sous-agent des connaissances de domaine sans qu'il ait besoin de découvrir et charger les skills pendant l'exécution.

```yaml theme={null}
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

Le contenu complet de chaque skill listée est injecté dans le contexte du sous-agent au démarrage. Ce champ contrôle quelles skills sont préchargées, pas quelles skills le sous-agent peut accéder : sans lui, le sous-agent peut toujours découvrir et invoquer les skills de projet, utilisateur et plugin via l'outil Skill pendant l'exécution. Pour empêcher un sous-agent d'invoquer les skills entièrement, omettez `Skill` de la liste [`tools`](#available-tools) ou ajoutez-le à `disallowedTools`.

Vous ne pouvez pas précharger les skills qui définissent [`disable-model-invocation: true`](/fr/skills#control-who-invokes-a-skill), car le préchargement provient du même ensemble de skills que Claude peut invoquer. Si une skill listée est manquante ou désactivée, Claude Code la saute et enregistre un avertissement dans le journal de débogage.

<Note>
  C'est l'inverse de [l'exécution d'une skill dans un sous-agent](/fr/skills#run-skills-in-a-subagent). Avec `skills` dans un sous-agent, le sous-agent contrôle l'invite système et charge le contenu de la skill. Avec `context: fork` dans une skill, le contenu de la skill est injecté dans l'agent que vous spécifiez. Les deux utilisent le même système sous-jacent.
</Note>

#### Activer la mémoire persistante

Le champ `memory` donne au sous-agent un répertoire persistant qui survit aux conversations. Le sous-agent utilise ce répertoire pour accumuler des connaissances au fil du temps, comme les modèles de base de code, les insights de débogage et les décisions architecturales.

```yaml theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

Choisissez une portée en fonction de la largeur d'application de la mémoire :

| Portée    | Emplacement                                   | Utiliser quand                                                                                                               |
| :-------- | :-------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| `user`    | `~/.claude/agent-memory/<name-of-agent>/`     | le sous-agent doit se souvenir des apprentissages dans tous les projets                                                      |
| `project` | `.claude/agent-memory/<name-of-agent>/`       | les connaissances du sous-agent sont spécifiques au projet et partageables via le contrôle de version                        |
| `local`   | `.claude/agent-memory-local/<name-of-agent>/` | les connaissances du sous-agent sont spécifiques au projet mais ne doivent pas être enregistrées dans le contrôle de version |

Lorsque la mémoire est activée :

* L'invite système du sous-agent inclut des instructions pour lire et écrire dans le répertoire de mémoire.
* L'invite système du sous-agent inclut également les 200 premières lignes ou 25 KB de `MEMORY.md` dans le répertoire de mémoire, selon ce qui est le moins important, avec des instructions pour organiser `MEMORY.md` s'il dépasse cette limite.
* Les outils Read, Write et Edit sont automatiquement activés pour que le sous-agent puisse gérer ses fichiers de mémoire.

##### Conseils de mémoire persistante

* `project` est la portée par défaut recommandée. Elle rend les connaissances du sous-agent partageables via le contrôle de version. Utilisez `user` lorsque les connaissances du sous-agent sont largement applicables dans les projets, ou `local` lorsque les connaissances ne doivent pas être enregistrées dans le contrôle de version.
* Demandez au sous-agent de consulter sa mémoire avant de commencer le travail : « Examinez cette PR et consultez votre mémoire pour les modèles que vous avez vus auparavant. »
* Demandez au sous-agent de mettre à jour sa mémoire après avoir terminé une tâche : « Maintenant que vous avez terminé, enregistrez ce que vous avez appris dans votre mémoire. » Au fil du temps, cela crée une base de connaissances qui rend le sous-agent plus efficace.
* Incluez les instructions de mémoire directement dans le fichier markdown du sous-agent pour qu'il maintienne proactivement sa propre base de connaissances :

  ```markdown theme={null}
  Update your agent memory as you discover codepaths, patterns, library
  locations, and key architectural decisions. This builds up institutional
  knowledge across conversations. Write concise notes about what you found
  and where.
  ```

#### Règles conditionnelles avec hooks

Pour un contrôle plus dynamique de l'utilisation des outils, utilisez les hooks `PreToolUse` pour valider les opérations avant leur exécution. C'est utile lorsque vous devez autoriser certaines opérations d'un outil tout en en bloquer d'autres.

Cet exemple crée un sous-agent qui n'autorise que les requêtes de base de données en lecture seule. Le hook `PreToolUse` exécute le script spécifié dans `command` avant chaque commande Bash :

```yaml theme={null}
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

Claude Code [passe l'entrée du hook en JSON](/fr/hooks#pretooluse-input) via stdin aux commandes du hook. Le script de validation lit ce JSON, extrait la commande Bash et [quitte avec le code 2](/fr/hooks#exit-code-2-behavior-per-event) pour bloquer les opérations d'écriture :

```bash theme={null}
#!/bin/bash
# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

Consultez [Hook input](/fr/hooks#pretooluse-input) pour le schéma d'entrée complet et [exit codes](/fr/hooks#exit-code-output) pour savoir comment les codes de sortie affectent le comportement. Sur Windows, écrivez les scripts de hook en PowerShell et ajoutez `shell: powershell` à l'entrée du hook comme indiqué dans [exécution de hooks en PowerShell](/fr/hooks#windows-powershell-tool).

#### Désactiver des sous-agents spécifiques

Vous pouvez empêcher Claude d'utiliser des sous-agents spécifiques en les ajoutant au tableau `deny` dans vos [paramètres](/fr/settings#permission-settings). Utilisez le format `Agent(subagent-name)` où `subagent-name` correspond au champ name du sous-agent.

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

Cela fonctionne pour les sous-agents intégrés et personnalisés. Vous pouvez également utiliser le drapeau CLI `--disallowedTools` :

```bash theme={null}
claude --disallowedTools "Agent(Explore)"
```

Consultez la [documentation Permissions](/fr/permissions#tool-specific-permission-rules) pour plus de détails sur les règles de permission.

### Définir les hooks pour les sous-agents

Les sous-agents peuvent définir des [hooks](/fr/hooks) qui s'exécutent pendant le cycle de vie du sous-agent. Il y a deux façons de configurer les hooks :

1. **Dans le frontmatter du sous-agent** : Définir les hooks qui s'exécutent uniquement pendant que ce sous-agent spécifique est actif
2. **Dans `settings.json`** : Définir les hooks qui s'exécutent dans la session principale lorsque les sous-agents démarrent ou s'arrêtent

#### Hooks dans le frontmatter du sous-agent

Définissez les hooks directement dans le fichier markdown du sous-agent. Ces hooks s'exécutent uniquement pendant que ce sous-agent spécifique est actif et sont nettoyés à la fin.

<Note>
  Les hooks de frontmatter se déclenchent lorsque l'agent est généré en tant que sous-agent via l'outil Agent ou une @-mention, et lorsque l'agent s'exécute en tant que principal de session via [`--agent`](#invoke-subagents-explicitly) ou le paramètre `agent`. Dans le cas de la session principale, ils s'exécutent aux côtés de tous les hooks définis dans [`settings.json`](/fr/hooks).
</Note>

Tous les [événements de hook](/fr/hooks#hook-events) sont pris en charge. Les événements les plus courants pour les sous-agents sont :

| Événement     | Entrée du matcher | Quand il se déclenche                                                     |
| :------------ | :---------------- | :------------------------------------------------------------------------ |
| `PreToolUse`  | Nom de l'outil    | Avant que le sous-agent utilise un outil                                  |
| `PostToolUse` | Nom de l'outil    | Après que le sous-agent utilise un outil                                  |
| `Stop`        | (aucun)           | Quand le sous-agent se termine (converti en `SubagentStop` à l'exécution) |

Cet exemple valide les commandes Bash avec le hook `PreToolUse` et exécute un linter après les modifications de fichiers avec `PostToolUse` :

```yaml theme={null}
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

Lorsque l'agent est invoqué en tant que sous-agent, les hooks `Stop` dans le frontmatter sont automatiquement convertis en événements `SubagentStop`.

#### Hooks au niveau du projet pour les événements de sous-agent

Configurez les hooks dans `settings.json` qui répondent aux événements du cycle de vie du sous-agent dans la session principale.

| Événement       | Entrée du matcher   | Quand il se déclenche                    |
| :-------------- | :------------------ | :--------------------------------------- |
| `SubagentStart` | Nom du type d'agent | Quand un sous-agent commence l'exécution |
| `SubagentStop`  | Nom du type d'agent | Quand un sous-agent se termine           |

Les deux événements prennent en charge les matchers pour cibler des types d'agents spécifiques par nom. Cet exemple exécute un script de configuration uniquement lorsque le sous-agent `db-agent` démarre, et un script de nettoyage lorsque n'importe quel sous-agent s'arrête :

```json theme={null}
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

Consultez [Hooks](/fr/hooks) pour le format de configuration complet des hooks.

## Travailler avec les sous-agents

### Comprendre la délégation automatique

Claude délègue automatiquement les tâches en fonction de la description de la tâche dans votre demande, du champ `description` dans les configurations de sous-agent et du contexte actuel. Pour encourager la délégation proactive, incluez des phrases comme « use proactively » dans le champ description de votre sous-agent.

### Invoquer les sous-agents explicitement

Lorsque la délégation automatique ne suffit pas, vous pouvez demander un sous-agent vous-même. Trois modèles escaladent d'une suggestion ponctuelle à une valeur par défaut au niveau de la session :

* **Langage naturel** : nommez le sous-agent dans votre invite ; Claude décide s'il faut déléguer
* **@-mention** : garantit que le sous-agent s'exécute pour une tâche
* **Au niveau de la session** : la session entière utilise l'invite système, les restrictions d'outils et le modèle de ce sous-agent via le drapeau `--agent` ou le paramètre `agent`

Pour le langage naturel, il n'y a pas de syntaxe spéciale. Nommez le sous-agent et Claude délègue généralement :

```text theme={null}
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

**@-mentionnez le sous-agent.** Tapez `@` et choisissez le sous-agent dans la saisie semi-automatique, de la même manière que vous @-mentionnez les fichiers. Cela garantit que ce sous-agent spécifique s'exécute plutôt que de laisser le choix à Claude :

```text theme={null}
@"code-reviewer (agent)" look at the auth changes
```

Votre message complet va toujours à Claude, qui écrit l'invite de tâche du sous-agent en fonction de ce que vous avez demandé. La @-mention contrôle quel sous-agent Claude invoque, pas quelle invite il reçoit.

Les sous-agents fournis par un [plugin](/fr/plugins) activé apparaissent dans la saisie semi-automatique sous leur nom délimité, comme `my-plugin:code-reviewer` ou `my-plugin:review:security` lorsque le plugin [organise les agents dans des sous-dossiers](#choose-the-subagent-scope). Les sous-agents d'arrière-plan nommés actuellement en cours d'exécution dans la session apparaissent également dans la saisie semi-automatique, affichant leur statut à côté du nom. Vous pouvez également taper la mention manuellement sans utiliser le sélecteur : `@agent-<name>` pour les sous-agents locaux, ou `@agent-` suivi du nom délimité pour les sous-agents de plugin, par exemple `@agent-my-plugin:code-reviewer`.

**Exécutez la session entière en tant que sous-agent.** Passez [`--agent <name>`](/fr/cli-reference) pour démarrer une session où le thread principal lui-même prend l'invite système, les restrictions d'outils et le modèle de ce sous-agent :

```bash theme={null}
claude --agent code-reviewer
```

L'invite système du sous-agent remplace complètement l'invite système par défaut de Claude Code, de la même manière que [`--system-prompt`](/fr/cli-reference) le fait. Les fichiers `CLAUDE.md` et la mémoire du projet se chargent toujours via le flux de messages normal. Le nom de l'agent apparaît comme `@<name>` dans l'en-tête de démarrage pour que vous puissiez confirmer qu'il est actif.

Cela fonctionne avec les sous-agents intégrés et personnalisés, et le choix persiste lorsque vous reprenez la session.

Pour un sous-agent fourni par un plugin, passez le nom délimité : `claude --agent <plugin-name>:<agent-name>`. Si le plugin place l'agent dans un sous-dossier de son répertoire `agents/`, incluez le sous-dossier dans le nom délimité, par exemple `claude --agent my-plugin:review:security`.

Pour en faire la valeur par défaut pour chaque session dans un projet, définissez `agent` dans `.claude/settings.json` :

```json theme={null}
{
  "agent": "code-reviewer"
}
```

Le drapeau CLI remplace le paramètre si les deux sont présents.

### Exécuter les sous-agents au premier plan ou en arrière-plan

Les sous-agents peuvent s'exécuter au premier plan (bloquant) ou en arrière-plan (concurrent) :

* **Les sous-agents au premier plan** bloquent la conversation principale jusqu'à la fin. Les invites de permission vous sont transmises au fur et à mesure qu'elles se produisent.
* **Les sous-agents en arrière-plan** s'exécutent simultanément pendant que vous continuez à travailler. Ils s'exécutent avec les permissions déjà accordées dans la session et auto-refusent tout appel d'outil qui sinon demanderait une permission. Si un sous-agent en arrière-plan doit poser des questions de clarification, cet appel d'outil échoue mais le sous-agent continue.

Si un sous-agent en arrière-plan échoue en raison de permissions manquantes, vous pouvez démarrer un nouveau sous-agent au premier plan avec la même tâche pour réessayer avec des invites interactives.

Claude décide si les sous-agents s'exécutent au premier plan ou en arrière-plan en fonction de la tâche. Vous pouvez également :

* Demander à Claude de « run this in the background »
* Appuyer sur **Ctrl+B** pour mettre une tâche en arrière-plan

Pour désactiver toute la fonctionnalité de tâche en arrière-plan, définissez la variable d'environnement `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` sur `1`. Consultez [Variables d'environnement](/fr/env-vars).

Lorsque le [mode fork](#fork-the-current-conversation) est activé, chaque génération de sous-agent s'exécute en arrière-plan indépendamment du champ `background`. Les forks affichent toujours les invites de permission dans votre terminal au fur et à mesure qu'elles se produisent ; les sous-agents nommés auto-refusent tout ce qui sinon demanderait une permission, comme décrit ci-dessus.

### Modèles courants

#### Isoler les opérations à haut volume

L'une des utilisations les plus efficaces des sous-agents est l'isolation des opérations qui produisent de grandes quantités de résultats. L'exécution de tests, la récupération de documentation ou le traitement de fichiers journaux peuvent consommer un contexte important. En déléguant ces tâches à un sous-agent, la sortie détaillée reste dans le contexte du sous-agent tandis que seul le résumé pertinent revient à votre conversation principale.

```text theme={null}
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### Exécuter la recherche en parallèle

Pour les investigations indépendantes, générez plusieurs sous-agents pour travailler simultanément :

```text theme={null}
Research the authentication, database, and API modules in parallel using separate subagents
```

Chaque sous-agent explore son domaine indépendamment, puis Claude synthétise les résultats. Cela fonctionne mieux lorsque les chemins de recherche ne dépendent pas les uns des autres.

<Warning>
  Lorsque les sous-agents se terminent, leurs résultats reviennent à votre conversation principale. L'exécution de nombreux sous-agents qui retournent chacun des résultats détaillés peut consommer un contexte important.
</Warning>

Pour les tâches qui nécessitent un parallélisme soutenu ou qui dépassent votre fenêtre de contexte, les [équipes d'agents](/fr/agent-teams) donnent à chaque travailleur son propre contexte indépendant.

#### Chaîner les sous-agents

Pour les workflows multi-étapes, demandez à Claude d'utiliser les sous-agents en séquence. Chaque sous-agent termine sa tâche et retourne les résultats à Claude, qui transmet ensuite le contexte pertinent au sous-agent suivant.

```text theme={null}
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Choisir entre les sous-agents et la conversation principale

Utilisez la **conversation principale** quand :

* La tâche nécessite des allers-retours fréquents ou un raffinement itératif
* Plusieurs phases partagent un contexte important (planification → implémentation → test)
* Vous apportez une modification rapide et ciblée
* La latence est importante. Les sous-agents commencent à zéro et peuvent avoir besoin de temps pour rassembler le contexte

Utilisez les **sous-agents** quand :

* La tâche produit une sortie détaillée dont vous n'avez pas besoin dans votre contexte principal
* Vous souhaitez appliquer des restrictions d'outils ou des permissions spécifiques
* Le travail est autonome et peut retourner un résumé

Envisagez plutôt les [Skills](/fr/skills) lorsque vous souhaitez des invites ou des workflows réutilisables qui s'exécutent dans le contexte de la conversation principale plutôt que dans un contexte de sous-agent isolé.

Pour une question rapide sur quelque chose déjà dans votre conversation, utilisez [`/btw`](/fr/interactive-mode#side-questions-with-%2Fbtw) au lieu d'un sous-agent. Il voit votre contexte complet mais n'a pas d'accès aux outils, et la réponse est ignorée plutôt que d'être ajoutée à l'historique.

<Note>
  Les sous-agents ne peuvent pas générer d'autres sous-agents. Si votre workflow nécessite une délégation imbriquée, utilisez les [Skills](/fr/skills) ou [chaînez les sous-agents](#chain-subagents) à partir de la conversation principale.
</Note>

### Gérer le contexte du sous-agent

#### Reprendre les sous-agents

Chaque invocation de sous-agent crée une nouvelle instance avec un contexte frais. Pour continuer le travail d'un sous-agent existant au lieu de recommencer, demandez à Claude de le reprendre.

Les sous-agents repris conservent leur historique de conversation complet, y compris tous les appels d'outils précédents, les résultats et le raisonnement. Le sous-agent reprend exactement où il s'était arrêté plutôt que de recommencer à zéro.

Lorsqu'un sous-agent se termine, Claude reçoit son ID d'agent. Claude utilise l'outil `SendMessage` avec l'ID de l'agent comme champ `to` pour le reprendre. L'outil `SendMessage` n'est disponible que lorsque les [équipes d'agents](/fr/agent-teams) sont activées via `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

Pour reprendre un sous-agent, demandez à Claude de continuer le travail précédent :

```text theme={null}
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

Si un sous-agent arrêté reçoit un `SendMessage`, il se reprend automatiquement en arrière-plan sans nécessiter une nouvelle invocation `Agent`.

Vous pouvez également demander à Claude l'ID d'agent si vous souhaitez le référencer explicitement, ou trouver les ID dans les fichiers de transcription à `~/.claude/projects/{project}/{sessionId}/subagents/`. Chaque transcription est stockée sous la forme `agent-{agentId}.jsonl`.

Les transcriptions de sous-agent persistent indépendamment de la conversation principale :

* **Compaction de la conversation principale** : Lorsque la conversation principale se compacte, les transcriptions de sous-agent ne sont pas affectées. Elles sont stockées dans des fichiers séparés.
* **Persistance de session** : Les transcriptions de sous-agent persistent au sein de leur session. Vous pouvez [reprendre un sous-agent](#resume-subagents) après le redémarrage de Claude Code en reprenant la même session.
* **Nettoyage automatique** : Les transcriptions sont nettoyées en fonction du paramètre `cleanupPeriodDays` (par défaut : 30 jours).

#### Auto-compaction

Les sous-agents prennent en charge la compaction automatique en utilisant la même logique que la conversation principale. Par défaut, la compaction automatique se déclenche à environ 95 % de capacité. Pour déclencher la compaction plus tôt, définissez `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` sur un pourcentage inférieur (par exemple, `50`). Consultez [variables d'environnement](/fr/env-vars) pour plus de détails.

Les événements de compaction sont enregistrés dans les fichiers de transcription de sous-agent :

```json theme={null}
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}
```

La valeur `preTokens` indique le nombre de tokens utilisés avant la compaction.

## Dupliquer la conversation actuelle

<Note>
  Les sous-agents dupliqués sont expérimentaux et nécessitent Claude Code v2.1.117 ou version ultérieure. Le comportement et la configuration peuvent changer dans les versions futures. Activez-les en définissant la variable d'environnement [`CLAUDE_CODE_FORK_SUBAGENT`](/fr/env-vars) sur `1`. La variable est honorée en mode interactif et via le SDK ou `claude -p`.
</Note>

Un fork est un sous-agent qui hérite de l'intégralité de la conversation jusqu'à présent au lieu de commencer à zéro. Cela supprime l'isolation d'entrée que les sous-agents fournissent autrement : un fork voit la même invite système, les mêmes outils, le même modèle et l'historique des messages que la session principale, vous pouvez donc lui confier une tâche secondaire sans réexpliquer la situation. Les appels d'outils du fork restent en dehors de votre conversation et seul son résultat final revient, donc votre fenêtre de contexte principal reste propre. Utilisez un fork lorsqu'un sous-agent nommé aurait besoin de trop de contexte pour être utile, ou lorsque vous souhaitez essayer plusieurs approches en parallèle à partir du même point de départ.

L'activation du mode fork change Claude Code de trois façons :

* Claude génère un fork chaque fois qu'il utiliserait autrement le sous-agent [general-purpose](#built-in-subagents). Les sous-agents nommés tels que Explore se génèrent comme avant.
* Chaque génération de sous-agent s'exécute en [arrière-plan](#run-subagents-in-foreground-or-background), qu'il s'agisse d'un fork ou d'un sous-agent nommé. Définissez `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` sur `1` pour garder les générations synchrones.
* La commande `/fork` génère un fork au lieu d'agir comme un alias pour [`/branch`](/fr/commands).

Vous pouvez démarrer un fork vous-même avec `/fork` suivi d'une directive. Claude Code nomme le fork à partir des premiers mots de la directive. L'exemple suivant duplique la conversation pour rédiger des cas de test pendant que vous continuez avec l'implémentation dans la session principale :

```text theme={null}
/fork draft unit tests for the parser changes so far
```

Le fork apparaît dans un panneau sous votre invite et s'exécute en arrière-plan pendant que vous continuez à travailler. Lorsqu'il se termine, son résultat arrive sous forme de message dans votre conversation principale. La section suivante couvre les contrôles du panneau pour observer et diriger les forks pendant qu'ils s'exécutent.

### Observer et diriger les forks en cours d'exécution

Les forks en cours d'exécution apparaissent dans un panneau sous l'entrée d'invite, avec une ligne pour la session principale et une pour chaque fork. Utilisez ces touches pour interagir avec le panneau :

| Touche    | Action                                                                           |
| :-------- | :------------------------------------------------------------------------------- |
| `↑` / `↓` | Se déplacer entre les lignes                                                     |
| `Entrée`  | Ouvrir la transcription du fork sélectionné et lui envoyer des messages de suivi |
| `x`       | Ignorer un fork terminé ou arrêter un fork en cours d'exécution                  |
| `Échap`   | Retourner le focus à l'entrée d'invite                                           |

### Comment les forks diffèrent des sous-agents nommés

Un fork hérite de tout ce que la session principale a au moment où il se génère. Un sous-agent nommé démarre à partir de sa propre définition.

|                          | Fork                                        | Sous-agent nommé                                                                                |
| :----------------------- | :------------------------------------------ | :---------------------------------------------------------------------------------------------- |
| Contexte                 | Historique de conversation complet          | Contexte frais avec l'invite que vous transmettez                                               |
| Invite système et outils | Identique à la session principale           | À partir du [fichier de définition](#write-subagent-files) du sous-agent                        |
| Modèle                   | Identique à la session principale           | À partir du champ `model` du sous-agent                                                         |
| Permissions              | Les invites s'affichent dans votre terminal | [Auto-refusées](#run-subagents-in-foreground-or-background) lors de l'exécution en arrière-plan |
| Cache d'invite           | Partagé avec la session principale          | Cache séparé                                                                                    |

Parce que l'invite système d'un fork et les définitions d'outils sont identiques au parent, sa première demande réutilise le cache d'invite du parent. Cela rend le forking moins cher que la génération d'un sous-agent frais pour les tâches qui ont besoin du même contexte.

Lorsque Claude génère un fork via l'outil Agent, il peut passer `isolation: "worktree"` pour que les modifications de fichiers du fork soient écrites dans un git worktree séparé au lieu de votre extraction.

### Limitations

Le paramètre `CLAUDE_CODE_FORK_SUBAGENT=1` active le mode fork dans les sessions interactives, le [mode non-interactif](/fr/headless), et le SDK Agent. Un fork ne peut pas générer d'autres forks.

## Exemples de sous-agents

Ces exemples démontrent des modèles efficaces pour construire des sous-agents. Utilisez-les comme points de départ, ou générez une version personnalisée avec Claude.

<Tip>
  **Meilleures pratiques :**

  * **Concevoir des sous-agents ciblés :** chaque sous-agent doit exceller dans une tâche spécifique
  * **Écrire des descriptions détaillées :** Claude utilise la description pour décider quand déléguer
  * **Limiter l'accès aux outils :** accordez uniquement les permissions nécessaires pour la sécurité et la concentration
  * **Enregistrer dans le contrôle de version :** partagez les sous-agents de projet avec votre équipe
</Tip>

### Examinateur de code

Un sous-agent en lecture seule qui examine le code sans le modifier. Cet exemple montre comment concevoir un sous-agent ciblé avec un accès limité aux outils (pas d'Edit ou Write) et une invite détaillée qui spécifie exactement ce qu'il faut chercher et comment formater la sortie.

```markdown theme={null}
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### Débogueur

Un sous-agent qui peut à la fois analyser et corriger les problèmes. Contrairement à l'examinateur de code, celui-ci inclut Edit car corriger les bugs nécessite de modifier le code. L'invite fournit un workflow clair du diagnostic à la vérification.

```markdown theme={null}
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### Data scientist

Un sous-agent spécialisé dans le domaine pour le travail d'analyse de données. Cet exemple montre comment créer des sous-agents pour des workflows spécialisés en dehors des tâches de codage typiques. Il définit explicitement `model: sonnet` pour une analyse plus capable.

```markdown theme={null}
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

### Validateur de requête de base de données

Un sous-agent qui autorise l'accès à Bash mais valide les commandes pour n'autoriser que les requêtes SQL en lecture seule. Cet exemple montre comment utiliser les hooks `PreToolUse` pour la validation conditionnelle lorsque vous avez besoin d'un contrôle plus fin que le champ `tools` ne le permet.

```markdown theme={null}
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.
```

Claude Code [passe l'entrée du hook en JSON](/fr/hooks#pretooluse-input) via stdin aux commandes du hook. Le script de validation lit ce JSON, extrait la commande en cours d'exécution et la vérifie par rapport à une liste d'opérations d'écriture SQL. Si une opération d'écriture est détectée, le script [quitte avec le code 2](/fr/hooks#exit-code-2-behavior-per-event) pour bloquer l'exécution et retourne un message d'erreur à Claude via stderr.

Créez le script de validation n'importe où dans votre projet. Le chemin doit correspondre au champ `command` dans votre configuration de hook :

```bash theme={null}
#!/bin/bash
# Blocks SQL write operations, allows SELECT queries

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0
```

Sur macOS et Linux, rendez le script exécutable :

```bash theme={null}
chmod +x ./scripts/validate-readonly-query.sh
```

Sur Windows, écrivez le script de validation en PowerShell et ajoutez `shell: powershell` à l'entrée du hook. Consultez [exécution des hooks dans PowerShell](/fr/hooks#windows-powershell-tool).

Le hook reçoit JSON via stdin avec la commande Bash dans `tool_input.command`. Le code de sortie 2 bloque l'opération et renvoie le message d'erreur à Claude. Consultez [Hooks](/fr/hooks#exit-code-output) pour plus de détails sur les codes de sortie et [Hook input](/fr/hooks#pretooluse-input) pour le schéma d'entrée complet.

## Étapes suivantes

Maintenant que vous comprenez les sous-agents, explorez ces fonctionnalités connexes :

* [Distribuer les sous-agents avec les plugins](/fr/plugins) pour partager les sous-agents entre les équipes ou les projets
* [Exécuter Claude Code par programmation](/fr/headless) avec le SDK Agent pour CI/CD et l'automatisation
* [Utiliser les serveurs MCP](/fr/mcp) pour donner aux sous-agents l'accès aux outils et données externes
