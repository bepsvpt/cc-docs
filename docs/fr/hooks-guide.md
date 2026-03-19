> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Automatiser les workflows avec les hooks

> Exécutez automatiquement des commandes shell lorsque Claude Code modifie des fichiers, termine des tâches ou a besoin d'une entrée. Formatez le code, envoyez des notifications, validez les commandes et appliquez les règles du projet.

Les hooks sont des commandes shell définies par l'utilisateur qui s'exécutent à des points spécifiques du cycle de vie de Claude Code. Ils fournissent un contrôle déterministe du comportement de Claude Code, en garantissant que certaines actions se produisent toujours plutôt que de compter sur le LLM pour choisir de les exécuter. Utilisez les hooks pour appliquer les règles du projet, automatiser les tâches répétitives et intégrer Claude Code avec vos outils existants.

Pour les décisions qui nécessitent un jugement plutôt que des règles déterministes, vous pouvez également utiliser des [hooks basés sur des invites](#prompt-based-hooks) ou des [hooks basés sur des agents](#agent-based-hooks) qui utilisent un modèle Claude pour évaluer les conditions.

Pour d'autres façons d'étendre Claude Code, consultez [skills](/fr/skills) pour donner à Claude des instructions supplémentaires et des commandes exécutables, [subagents](/fr/sub-agents) pour exécuter des tâches dans des contextes isolés, et [plugins](/fr/plugins) pour empaqueter les extensions à partager entre les projets.

<Tip>
  Ce guide couvre les cas d'usage courants et comment commencer. Pour les schémas d'événements complets, les formats d'entrée/sortie JSON et les fonctionnalités avancées comme les hooks asynchrones et les hooks d'outils MCP, consultez la [référence des Hooks](/fr/hooks).
</Tip>

## Configurer votre premier hook

Le moyen le plus rapide de créer un hook est via le menu interactif `/hooks` dans Claude Code. Cette procédure pas à pas crée un hook de notification de bureau, afin que vous soyez alerté chaque fois que Claude attend votre entrée au lieu de regarder le terminal.

<Steps>
  <Step title="Ouvrir le menu des hooks">
    Tapez `/hooks` dans le CLI de Claude Code. Vous verrez une liste de tous les événements de hook disponibles, plus une option pour désactiver tous les hooks. Chaque événement correspond à un point du cycle de vie de Claude où vous pouvez exécuter du code personnalisé. Sélectionnez `Notification` pour créer un hook qui se déclenche lorsque Claude a besoin de votre attention.
  </Step>

  <Step title="Configurer le matcher">
    Le menu affiche une liste de matchers, qui filtrent le moment où le hook se déclenche. Définissez le matcher sur `*` pour se déclencher sur tous les types de notifications. Vous pouvez l'affiner plus tard en changeant le matcher en une valeur spécifique comme `permission_prompt` ou `idle_prompt`.
  </Step>

  <Step title="Ajouter votre commande">
    Sélectionnez `+ Add new hook…`. Le menu vous demande une commande shell à exécuter lorsque l'événement se déclenche. Les hooks exécutent n'importe quelle commande shell que vous fournissez, vous pouvez donc utiliser l'outil de notification intégré de votre plateforme. Copiez la commande pour votre système d'exploitation :

    <Tabs>
      <Tab title="macOS">
        Utilise [`osascript`](https://ss64.com/mac/osascript.html) pour déclencher une notification macOS native via AppleScript :

        ```bash  theme={null}
        osascript -e 'display notification "Claude Code needs your attention" with title "Claude Code"'
        ```
      </Tab>

      <Tab title="Linux">
        Utilise `notify-send`, qui est pré-installé sur la plupart des bureaux Linux avec un démon de notification :

        ```bash  theme={null}
        notify-send 'Claude Code' 'Claude Code needs your attention'
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        Utilise PowerShell pour afficher une boîte de message native via Windows Forms de .NET :

        ```powershell  theme={null}
        powershell.exe -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')"
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Choisir un emplacement de stockage">
    Le menu vous demande où enregistrer la configuration du hook. Sélectionnez `User settings` pour la stocker dans `~/.claude/settings.json`, ce qui applique le hook à tous vos projets. Vous pouvez également choisir `Project settings` pour le limiter au projet actuel. Consultez [Configurer l'emplacement du hook](#configure-hook-location) pour tous les périmètres disponibles.
  </Step>

  <Step title="Tester le hook">
    Appuyez sur `Esc` pour revenir au CLI. Demandez à Claude de faire quelque chose qui nécessite une permission, puis quittez le terminal. Vous devriez recevoir une notification de bureau.
  </Step>
</Steps>

## Ce que vous pouvez automatiser

Les hooks vous permettent d'exécuter du code à des points clés du cycle de vie de Claude Code : formater les fichiers après les modifications, bloquer les commandes avant leur exécution, envoyer des notifications lorsque Claude a besoin d'une entrée, injecter du contexte au démarrage de la session, et bien plus. Pour la liste complète des événements de hook, consultez la [référence des Hooks](/fr/hooks#hook-lifecycle).

Chaque exemple inclut un bloc de configuration prêt à l'emploi que vous ajoutez à un [fichier de paramètres](#configure-hook-location). Les modèles les plus courants :

* [Être notifié lorsque Claude a besoin d'une entrée](#get-notified-when-claude-needs-input)
* [Formater automatiquement le code après les modifications](#auto-format-code-after-edits)
* [Bloquer les modifications des fichiers protégés](#block-edits-to-protected-files)
* [Réinjecter le contexte après compaction](#re-inject-context-after-compaction)
* [Auditer les modifications de configuration](#audit-configuration-changes)

### Être notifié lorsque Claude a besoin d'une entrée

Recevez une notification de bureau chaque fois que Claude termine son travail et a besoin de votre entrée, afin que vous puissiez passer à d'autres tâches sans vérifier le terminal.

Ce hook utilise l'événement `Notification`, qui se déclenche lorsque Claude attend une entrée ou une permission. Chaque onglet ci-dessous utilise la commande de notification native de la plateforme. Ajoutez ceci à `~/.claude/settings.json`, ou utilisez la [procédure pas à pas interactive](#set-up-your-first-hook) ci-dessus pour le configurer avec `/hooks` :

<Tabs>
  <Tab title="macOS">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Linux">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Windows (PowerShell)">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

### Formater automatiquement le code après les modifications

Exécutez automatiquement [Prettier](https://prettier.io/) sur chaque fichier que Claude modifie, afin que le formatage reste cohérent sans intervention manuelle.

Ce hook utilise l'événement `PostToolUse` avec un matcher `Edit|Write`, il s'exécute donc uniquement après les outils d'édition de fichiers. La commande extrait le chemin du fichier modifié avec [`jq`](https://jqlang.github.io/jq/) et le transmet à Prettier. Ajoutez ceci à `.claude/settings.json` dans la racine de votre projet :

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

<Note>
  Les exemples Bash sur cette page utilisent `jq` pour l'analyse JSON. Installez-le avec `brew install jq` (macOS), `apt-get install jq` (Debian/Ubuntu), ou consultez les [téléchargements de `jq`](https://jqlang.github.io/jq/download/).
</Note>

### Bloquer les modifications des fichiers protégés

Empêchez Claude de modifier les fichiers sensibles comme `.env`, `package-lock.json`, ou n'importe quoi dans `.git/`. Claude reçoit un retour d'information expliquant pourquoi la modification a été bloquée, afin qu'il puisse ajuster son approche.

Cet exemple utilise un fichier de script séparé que le hook appelle. Le script vérifie le chemin du fichier cible par rapport à une liste de modèles protégés et quitte avec le code 2 pour bloquer la modification.

<Steps>
  <Step title="Créer le script du hook">
    Enregistrez ceci dans `.claude/hooks/protect-files.sh` :

    ```bash  theme={null}
    #!/bin/bash
    # protect-files.sh

    INPUT=$(cat)
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

    PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

    for pattern in "${PROTECTED_PATTERNS[@]}"; do
      if [[ "$FILE_PATH" == *"$pattern"* ]]; then
        echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
        exit 2
      fi
    done

    exit 0
    ```
  </Step>

  <Step title="Rendre le script exécutable (macOS/Linux)">
    Les scripts de hook doivent être exécutables pour que Claude Code les exécute :

    ```bash  theme={null}
    chmod +x .claude/hooks/protect-files.sh
    ```
  </Step>

  <Step title="Enregistrer le hook">
    Ajoutez un hook `PreToolUse` à `.claude/settings.json` qui exécute le script avant tout appel d'outil `Edit` ou `Write` :

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Step>
</Steps>

### Réinjecter le contexte après compaction

Lorsque la fenêtre de contexte de Claude se remplit, la compaction résume la conversation pour libérer de l'espace. Cela peut perdre des détails importants. Utilisez un hook `SessionStart` avec un matcher `compact` pour réinjecter le contexte critique après chaque compaction.

Tout texte que votre commande écrit sur stdout est ajouté au contexte de Claude. Cet exemple rappelle à Claude les conventions du projet et le travail récent. Ajoutez ceci à `.claude/settings.json` dans la racine de votre projet :

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
          }
        ]
      }
    ]
  }
}
```

Vous pouvez remplacer `echo` par n'importe quelle commande qui produit une sortie dynamique, comme `git log --oneline -5` pour afficher les commits récents. Pour injecter du contexte au démarrage de chaque session, envisagez d'utiliser [CLAUDE.md](/fr/memory) à la place. Pour les variables d'environnement, consultez [`CLAUDE_ENV_FILE`](/fr/hooks#persist-environment-variables) dans la référence.

### Auditer les modifications de configuration

Suivez les modifications des fichiers de paramètres ou de skills pendant une session. L'événement `ConfigChange` se déclenche lorsqu'un processus externe ou un éditeur modifie un fichier de configuration, afin que vous puissiez enregistrer les modifications pour la conformité ou bloquer les modifications non autorisées.

Cet exemple ajoute chaque modification à un journal d'audit. Ajoutez ceci à `~/.claude/settings.json` :

```json  theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> ~/claude-config-audit.log"
          }
        ]
      }
    ]
  }
}
```

Le matcher filtre par type de configuration : `user_settings`, `project_settings`, `local_settings`, `policy_settings`, ou `skills`. Pour bloquer une modification de prendre effet, quittez avec le code 2 ou retournez `{"decision": "block"}`. Consultez la [référence ConfigChange](/fr/hooks#configchange) pour le schéma d'entrée complet.

## Comment fonctionnent les hooks

Les événements de hook se déclenchent à des points spécifiques du cycle de vie de Claude Code. Lorsqu'un événement se déclenche, tous les hooks correspondants s'exécutent en parallèle, et les commandes de hook identiques sont automatiquement dédupliquées. Le tableau ci-dessous montre chaque événement et quand il se déclenche :

| Event                | When it fires                                                                                                                                  |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                               |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                           |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                      |
| `PermissionRequest`  | When a permission dialog appears                                                                                                               |
| `PostToolUse`        | After a tool call succeeds                                                                                                                     |
| `PostToolUseFailure` | After a tool call fails                                                                                                                        |
| `Notification`       | When Claude Code sends a notification                                                                                                          |
| `SubagentStart`      | When a subagent is spawned                                                                                                                     |
| `SubagentStop`       | When a subagent finishes                                                                                                                       |
| `Stop`               | When Claude finishes responding                                                                                                                |
| `StopFailure`        | When the turn ends due to an API error. Output and exit code are ignored                                                                       |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                             |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                       |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session |
| `ConfigChange`       | When a configuration file changes during a session                                                                                             |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                    |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                           |
| `PreCompact`         | Before context compaction                                                                                                                      |
| `PostCompact`        | After context compaction completes                                                                                                             |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                      |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                    |
| `SessionEnd`         | When a session terminates                                                                                                                      |

Chaque hook a un `type` qui détermine comment il s'exécute. La plupart des hooks utilisent `"type": "command"`, qui exécute une commande shell. Trois autres types sont disponibles :

* `"type": "http"` : POST les données d'événement vers une URL. Consultez [HTTP hooks](#http-hooks).
* `"type": "prompt"` : évaluation LLM à un seul tour. Consultez [Hooks basés sur des invites](#prompt-based-hooks).
* `"type": "agent"` : vérification multi-tour avec accès aux outils. Consultez [Hooks basés sur des agents](#agent-based-hooks).

### Lire l'entrée et retourner la sortie

Les hooks communiquent avec Claude Code via stdin, stdout, stderr et les codes de sortie. Lorsqu'un événement se déclenche, Claude Code transmet les données spécifiques à l'événement en JSON à stdin de votre script. Votre script lit ces données, fait son travail, et dit à Claude Code quoi faire ensuite via le code de sortie.

#### Entrée du hook

Chaque événement inclut des champs communs comme `session_id` et `cwd`, mais chaque type d'événement ajoute des données différentes. Par exemple, lorsque Claude exécute une commande Bash, un hook `PreToolUse` reçoit quelque chose comme ceci sur stdin :

```json  theme={null}
{
  "session_id": "abc123",          // unique ID for this session
  "cwd": "/Users/sarah/myproject", // working directory when the event fired
  "hook_event_name": "PreToolUse", // which event triggered this hook
  "tool_name": "Bash",             // the tool Claude is about to use
  "tool_input": {                  // the arguments Claude passed to the tool
    "command": "npm test"          // for Bash, this is the shell command
  }
}
```

Votre script peut analyser ce JSON et agir sur n'importe lequel de ces champs. Les hooks `UserPromptSubmit` obtiennent le texte `prompt` à la place, les hooks `SessionStart` obtiennent la `source` (startup, resume, clear, compact), et ainsi de suite. Consultez [Champs d'entrée communs](/fr/hooks#common-input-fields) dans la référence pour les champs partagés, et la section de chaque événement pour les schémas spécifiques à l'événement.

#### Sortie du hook

Votre script dit à Claude Code quoi faire ensuite en écrivant sur stdout ou stderr et en quittant avec un code spécifique. Par exemple, un hook `PreToolUse` qui veut bloquer une commande :

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q "drop table"; then
  echo "Blocked: dropping tables is not allowed" >&2  # stderr becomes Claude's feedback
  exit 2 # exit 2 = block the action
fi

exit 0  # exit 0 = let it proceed
```

Le code de sortie détermine ce qui se passe ensuite :

* **Exit 0** : l'action se poursuit. Pour les hooks `UserPromptSubmit` et `SessionStart`, tout ce que vous écrivez sur stdout est ajouté au contexte de Claude.
* **Exit 2** : l'action est bloquée. Écrivez une raison sur stderr, et Claude la reçoit comme retour d'information afin qu'il puisse s'ajuster.
* **Tout autre code de sortie** : l'action se poursuit. Stderr est enregistré mais non affiché à Claude. Basculez le mode verbeux avec `Ctrl+O` pour voir ces messages dans la transcription.

#### Sortie JSON structurée

Les codes de sortie vous donnent deux options : autoriser ou bloquer. Pour plus de contrôle, quittez 0 et imprimez un objet JSON sur stdout à la place.

<Note>
  Utilisez exit 2 pour bloquer avec un message stderr, ou exit 0 avec JSON pour un contrôle structuré. Ne les mélangez pas : Claude Code ignore JSON lorsque vous quittez 2.
</Note>

Par exemple, un hook `PreToolUse` peut refuser un appel d'outil et dire à Claude pourquoi, ou l'escalader à l'utilisateur pour approbation :

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep for better performance"
  }
}
```

Claude Code lit `permissionDecision` et annule l'appel d'outil, puis renvoie `permissionDecisionReason` à Claude comme retour d'information. Ces trois options sont spécifiques à `PreToolUse` :

* `"allow"` : procéder sans afficher une invite de permission
* `"deny"` : annuler l'appel d'outil et envoyer la raison à Claude
* `"ask"` : afficher l'invite de permission à l'utilisateur comme d'habitude

D'autres événements utilisent des modèles de décision différents. Par exemple, les hooks `PostToolUse` et `Stop` utilisent un champ `decision: "block"` au niveau supérieur, tandis que `PermissionRequest` utilise `hookSpecificOutput.decision.behavior`. Consultez le [tableau récapitulatif](/fr/hooks#decision-control) dans la référence pour une ventilation complète par événement.

Pour les hooks `UserPromptSubmit`, utilisez `additionalContext` à la place pour injecter du texte dans le contexte de Claude. Les hooks basés sur des invites (`type: "prompt"`) gèrent la sortie différemment : consultez [Hooks basés sur des invites](#prompt-based-hooks).

### Filtrer les hooks avec des matchers

Sans matcher, un hook se déclenche à chaque occurrence de son événement. Les matchers vous permettent de réduire cela. Par exemple, si vous voulez exécuter un formateur uniquement après les modifications de fichiers (pas après chaque appel d'outil), ajoutez un matcher à votre hook `PostToolUse` :

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "prettier --write ..." }
        ]
      }
    ]
  }
}
```

Le matcher `"Edit|Write"` est un modèle regex qui correspond au nom de l'outil. Le hook ne se déclenche que lorsque Claude utilise l'outil `Edit` ou `Write`, pas lorsqu'il utilise `Bash`, `Read`, ou tout autre outil.

Chaque type d'événement correspond à un champ spécifique. Les matchers supportent les chaînes exactes et les modèles regex :

| Événement                                                                                       | Ce que le matcher filtre           | Exemples de valeurs de matcher                                                     |
| :---------------------------------------------------------------------------------------------- | :--------------------------------- | :--------------------------------------------------------------------------------- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`                          | nom de l'outil                     | `Bash`, `Edit\|Write`, `mcp__.*`                                                   |
| `SessionStart`                                                                                  | comment la session a démarré       | `startup`, `resume`, `clear`, `compact`                                            |
| `SessionEnd`                                                                                    | pourquoi la session s'est terminée | `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`     |
| `Notification`                                                                                  | type de notification               | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`           |
| `SubagentStart`                                                                                 | type d'agent                       | `Bash`, `Explore`, `Plan`, ou noms d'agents personnalisés                          |
| `PreCompact`                                                                                    | ce qui a déclenché la compaction   | `manual`, `auto`                                                                   |
| `SubagentStop`                                                                                  | type d'agent                       | mêmes valeurs que `SubagentStart`                                                  |
| `ConfigChange`                                                                                  | source de configuration            | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | pas de support de matcher          | se déclenche toujours à chaque occurrence                                          |

Quelques autres exemples montrant des matchers sur différents types d'événements :

<Tabs>
  <Tab title="Enregistrer chaque commande Bash">
    Correspond uniquement aux appels d'outil `Bash` et enregistre chaque commande dans un fichier. L'événement `PostToolUse` se déclenche après la fin de la commande, donc `tool_input.command` contient ce qui a été exécuté. Le hook reçoit les données d'événement en JSON sur stdin, et `jq -r '.tool_input.command'` extrait juste la chaîne de commande, que `>>` ajoute au fichier journal :

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Correspondre aux outils MCP">
    Les outils MCP utilisent une convention de nommage différente des outils intégrés : `mcp__<server>__<tool>`, où `<server>` est le nom du serveur MCP et `<tool>` est l'outil qu'il fournit. Par exemple, `mcp__github__search_repositories` ou `mcp__filesystem__read_file`. Utilisez un matcher regex pour cibler tous les outils d'un serveur spécifique, ou correspondre entre les serveurs avec un modèle comme `mcp__.*__write.*`. Consultez [Correspondre aux outils MCP](/fr/hooks#match-mcp-tools) dans la référence pour la liste complète des exemples.

    La commande ci-dessous extrait le nom de l'outil de l'entrée JSON du hook avec `jq` et l'écrit sur stderr, où il apparaît en mode verbeux (`Ctrl+O`) :

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "mcp__github__.*",
            "hooks": [
              {
                "type": "command",
                "command": "echo \"GitHub tool called: $(jq -r '.tool_name')\" >&2"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Nettoyer à la fin de la session">
    L'événement `SessionEnd` supporte les matchers sur la raison de la fin de la session. Ce hook ne se déclenche que sur `clear` (lorsque vous exécutez `/clear`), pas sur les sorties normales :

    ```json  theme={null}
    {
      "hooks": {
        "SessionEnd": [
          {
            "matcher": "clear",
            "hooks": [
              {
                "type": "command",
                "command": "rm -f /tmp/claude-scratch-*.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

Pour la syntaxe complète du matcher, consultez la [référence des Hooks](/fr/hooks#configuration).

### Configurer l'emplacement du hook

L'endroit où vous ajoutez un hook détermine son périmètre :

| Emplacement                                                | Périmètre                                 | Partageable                              |
| :--------------------------------------------------------- | :---------------------------------------- | :--------------------------------------- |
| `~/.claude/settings.json`                                  | Tous vos projets                          | Non, local à votre machine               |
| `.claude/settings.json`                                    | Projet unique                             | Oui, peut être commité dans le repo      |
| `.claude/settings.local.json`                              | Projet unique                             | Non, gitignored                          |
| Paramètres de politique gérés                              | À l'échelle de l'organisation             | Oui, contrôlé par l'administrateur       |
| [Plugin](/fr/plugins) `hooks/hooks.json`                   | Lorsque le plugin est activé              | Oui, fourni avec le plugin               |
| [Skill](/fr/skills) ou [agent](/fr/sub-agents) frontmatter | Pendant que le skill ou l'agent est actif | Oui, défini dans le fichier du composant |

Vous pouvez également utiliser le menu [`/hooks`](/fr/hooks#the-hooks-menu) dans Claude Code pour ajouter, supprimer et afficher les hooks de manière interactive. Pour désactiver tous les hooks à la fois, utilisez le bouton bascule en bas du menu `/hooks` ou définissez `"disableAllHooks": true` dans votre fichier de paramètres.

Les hooks ajoutés via le menu `/hooks` prennent effet immédiatement. Si vous modifiez les fichiers de paramètres directement pendant que Claude Code s'exécute, les modifications ne prendront effet que lorsque vous les examinerez dans le menu `/hooks` ou que vous redémarrerez votre session.

## Hooks basés sur des invites

Pour les décisions qui nécessitent un jugement plutôt que des règles déterministes, utilisez les hooks `type: "prompt"`. Au lieu d'exécuter une commande shell, Claude Code envoie votre invite et les données d'entrée du hook à un modèle Claude (Haiku par défaut) pour prendre la décision. Vous pouvez spécifier un modèle différent avec le champ `model` si vous avez besoin de plus de capacité.

Le seul travail du modèle est de retourner une décision oui/non en JSON :

* `"ok": true` : l'action se poursuit
* `"ok": false` : l'action est bloquée. La `"reason"` du modèle est renvoyée à Claude afin qu'il puisse s'ajuster.

Cet exemple utilise un hook `Stop` pour demander au modèle si toutes les tâches demandées sont complètes. Si le modèle retourne `"ok": false`, Claude continue à travailler et utilise la `reason` comme sa prochaine instruction :

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
          }
        ]
      }
    ]
  }
}
```

Pour les options de configuration complètes, consultez [Hooks basés sur des invites](/fr/hooks#prompt-based-hooks) dans la référence.

## Hooks basés sur des agents

Lorsque la vérification nécessite d'inspecter des fichiers ou d'exécuter des commandes, utilisez les hooks `type: "agent"`. Contrairement aux hooks d'invite qui font un seul appel LLM, les hooks d'agent génèrent un subagent qui peut lire des fichiers, rechercher du code et utiliser d'autres outils pour vérifier les conditions avant de retourner une décision.

Les hooks d'agent utilisent le même format de réponse `"ok"` / `"reason"` que les hooks d'invite, mais avec un délai d'expiration par défaut plus long de 60 secondes et jusqu'à 50 tours d'utilisation d'outils.

Cet exemple vérifie que les tests réussissent avant de permettre à Claude de s'arrêter :

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

Utilisez les hooks d'invite lorsque les données d'entrée du hook seules suffisent pour prendre une décision. Utilisez les hooks d'agent lorsque vous avez besoin de vérifier quelque chose par rapport à l'état réel de la base de code.

Pour les options de configuration complètes, consultez [Hooks basés sur des agents](/fr/hooks#agent-based-hooks) dans la référence.

## HTTP hooks

Utilisez les hooks `type: "http"` pour POST les données d'événement vers un point de terminaison HTTP au lieu d'exécuter une commande shell. Le point de terminaison reçoit le même JSON qu'un hook de commande recevrait sur stdin, et retourne les résultats via le corps de la réponse HTTP en utilisant le même format JSON.

Les HTTP hooks sont utiles lorsque vous voulez qu'un serveur web, une fonction cloud ou un service externe gère la logique du hook : par exemple, un service d'audit partagé qui enregistre les événements d'utilisation d'outils dans une équipe.

Cet exemple poste chaque utilisation d'outil vers un service de journalisation local :

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/tool-use",
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

Le point de terminaison doit retourner un corps de réponse JSON en utilisant le même [format de sortie](/fr/hooks#json-output) que les hooks de commande. Pour bloquer un appel d'outil, retournez une réponse 2xx avec les champs `hookSpecificOutput` appropriés. Les codes de statut HTTP seuls ne peuvent pas bloquer les actions.

Les valeurs d'en-tête supportent l'interpolation de variables d'environnement en utilisant la syntaxe `$VAR_NAME` ou `${VAR_NAME}`. Seules les variables listées dans le tableau `allowedEnvVars` sont résolues ; toutes les autres références `$VAR` restent vides.

<Note>
  Les HTTP hooks doivent être configurés en modifiant directement votre JSON de paramètres. Le menu interactif `/hooks` ne supporte que l'ajout de hooks de commande.
</Note>

Pour les options de configuration complètes et la gestion des réponses, consultez [HTTP hooks](/fr/hooks#http-hook-fields) dans la référence.

## Limitations et dépannage

### Limitations

* Les hooks de commande communiquent uniquement via stdout, stderr et les codes de sortie. Ils ne peuvent pas déclencher directement des commandes ou des appels d'outils. Les HTTP hooks communiquent via le corps de la réponse à la place.
* Le délai d'expiration du hook est de 10 minutes par défaut, configurable par hook avec le champ `timeout` (en secondes).
* Les hooks `PostToolUse` ne peuvent pas annuler les actions puisque l'outil a déjà été exécuté.
* Les hooks `PermissionRequest` ne se déclenchent pas en [mode non-interactif](/fr/headless) (`-p`). Utilisez les hooks `PreToolUse` pour les décisions de permission automatisées.
* Les hooks `Stop` se déclenchent chaque fois que Claude termine sa réponse, pas seulement à la fin de la tâche. Ils ne se déclenchent pas sur les interruptions de l'utilisateur.

### Hook ne se déclenche pas

Le hook est configuré mais ne s'exécute jamais.

* Exécutez `/hooks` et confirmez que le hook apparaît sous l'événement correct
* Vérifiez que le modèle de matcher correspond exactement au nom de l'outil (les matchers sont sensibles à la casse)
* Vérifiez que vous déclenchez le bon type d'événement (par exemple, `PreToolUse` se déclenche avant l'exécution de l'outil, `PostToolUse` se déclenche après)
* Si vous utilisez des hooks `PermissionRequest` en mode non-interactif (`-p`), passez à `PreToolUse` à la place

### Erreur du hook dans la sortie

Vous voyez un message comme « PreToolUse hook error : ... » dans la transcription.

* Votre script a quitté avec un code non-zéro de manière inattendue. Testez-le manuellement en piping du JSON d'exemple :
  ```bash  theme={null}
  echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
  echo $?  # Check the exit code
  ```
* Si vous voyez « command not found », utilisez des chemins absolus ou `$CLAUDE_PROJECT_DIR` pour référencer les scripts
* Si vous voyez « jq: command not found », installez `jq` ou utilisez Python/Node.js pour l'analyse JSON
* Si le script ne s'exécute pas du tout, rendez-le exécutable : `chmod +x ./my-hook.sh`

### `/hooks` n'affiche aucun hook configuré

Vous avez modifié un fichier de paramètres mais les hooks n'apparaissent pas dans le menu.

* Redémarrez votre session ou ouvrez `/hooks` pour recharger. Les hooks ajoutés via le menu `/hooks` prennent effet immédiatement, mais les modifications manuelles des fichiers nécessitent un rechargement.
* Vérifiez que votre JSON est valide (les virgules finales et les commentaires ne sont pas autorisés)
* Confirmez que le fichier de paramètres est au bon emplacement : `.claude/settings.json` pour les hooks de projet, `~/.claude/settings.json` pour les hooks globaux

### Le hook Stop s'exécute indéfiniment

Claude continue à travailler dans une boucle infinie au lieu de s'arrêter.

Votre script de hook Stop doit vérifier s'il a déjà déclenché une continuation. Analysez le champ `stop_hook_active` de l'entrée JSON et quittez tôt s'il est `true` :

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # Allow Claude to stop
fi
# ... rest of your hook logic
```

### Validation JSON échouée

Claude Code affiche une erreur d'analyse JSON même si votre script de hook produit du JSON valide.

Lorsque Claude Code exécute un hook, il génère un shell qui source votre profil (`~/.zshrc` ou `~/.bashrc`). Si votre profil contient des instructions `echo` inconditionnelles, cette sortie est ajoutée au début de votre JSON du hook :

```text  theme={null}
Shell ready on arm64
{"decision": "block", "reason": "Not allowed"}
```

Claude Code essaie d'analyser ceci en JSON et échoue. Pour corriger cela, enveloppez les instructions echo dans votre profil shell afin qu'elles ne s'exécutent que dans les shells interactifs :

```bash  theme={null}
# In ~/.zshrc or ~/.bashrc
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

La variable `$-` contient les drapeaux du shell, et `i` signifie interactif. Les hooks s'exécutent dans des shells non-interactifs, donc l'echo est ignoré.

### Techniques de débogage

Basculez le mode verbeux avec `Ctrl+O` pour voir la sortie du hook dans la transcription, ou exécutez `claude --debug` pour les détails d'exécution complets, y compris les hooks qui ont correspondu et leurs codes de sortie.

## En savoir plus

* [Référence des Hooks](/fr/hooks) : schémas d'événements complets, format de sortie JSON, hooks asynchrones et hooks d'outils MCP
* [Considérations de sécurité](/fr/hooks#security-considerations) : examinez avant de déployer les hooks dans des environnements partagés ou de production
* [Exemple de validateur de commande Bash](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py) : implémentation de référence complète
