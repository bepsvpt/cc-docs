> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Référence CLI

> Référence complète pour l'interface de ligne de commande Claude Code, incluant les commandes et les drapeaux.

## Commandes CLI

Vous pouvez démarrer des sessions, traiter du contenu, reprendre des conversations et gérer les mises à jour avec ces commandes :

| Commande                        | Description                                                                                                                                                                                                             | Exemple                                            |
| :------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `claude`                        | Démarrer une session interactive                                                                                                                                                                                        | `claude`                                           |
| `claude "query"`                | Démarrer une session interactive avec une invite initiale                                                                                                                                                               | `claude "explain this project"`                    |
| `claude -p "query"`             | Interroger via SDK, puis quitter                                                                                                                                                                                        | `claude -p "explain this function"`                |
| `cat file \| claude -p "query"` | Traiter le contenu canalisé                                                                                                                                                                                             | `cat logs.txt \| claude -p "explain"`              |
| `claude -c`                     | Continuer la conversation la plus récente dans le répertoire courant                                                                                                                                                    | `claude -c`                                        |
| `claude -c -p "query"`          | Continuer via SDK                                                                                                                                                                                                       | `claude -c -p "Check for type errors"`             |
| `claude -r "<session>" "query"` | Reprendre une session par ID ou nom                                                                                                                                                                                     | `claude -r "auth-refactor" "Finish this PR"`       |
| `claude update`                 | Mettre à jour vers la dernière version                                                                                                                                                                                  | `claude update`                                    |
| `claude auth login`             | Se connecter à votre compte Anthropic. Utilisez `--email` pour pré-remplir votre adresse e-mail et `--sso` pour forcer l'authentification SSO                                                                           | `claude auth login --email user@example.com --sso` |
| `claude auth logout`            | Se déconnecter de votre compte Anthropic                                                                                                                                                                                | `claude auth logout`                               |
| `claude auth status`            | Afficher l'état de l'authentification en JSON. Utilisez `--text` pour une sortie lisible par l'homme. Quitte avec le code 0 si connecté, 1 sinon                                                                        | `claude auth status`                               |
| `claude agents`                 | Lister tous les [subagents](/fr/sub-agents) configurés, groupés par source                                                                                                                                              | `claude agents`                                    |
| `claude mcp`                    | Configurer les serveurs Model Context Protocol (MCP)                                                                                                                                                                    | Voir la [documentation Claude Code MCP](/fr/mcp).  |
| `claude remote-control`         | Démarrer une [session Remote Control](/fr/remote-control) pour contrôler Claude Code depuis Claude.ai ou l'application Claude tout en exécutant localement. Voir [Remote Control](/fr/remote-control) pour les drapeaux | `claude remote-control`                            |

## Drapeaux CLI

Personnalisez le comportement de Claude Code avec ces drapeaux de ligne de commande :

| Drapeau                                | Description                                                                                                                                                                                                                                | Exemple                                                                                            |
| :------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `--add-dir`                            | Ajouter des répertoires de travail supplémentaires pour que Claude y accède (valide que chaque chemin existe en tant que répertoire)                                                                                                       | `claude --add-dir ../apps ../lib`                                                                  |
| `--agent`                              | Spécifier un agent pour la session actuelle (remplace le paramètre `agent`)                                                                                                                                                                | `claude --agent my-custom-agent`                                                                   |
| `--agents`                             | Définir des [subagents](/fr/sub-agents) personnalisés dynamiquement via JSON (voir ci-dessous pour le format)                                                                                                                              | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allow-dangerously-skip-permissions` | Activer le contournement des permissions en tant qu'option sans l'activer immédiatement. Permet de composer avec `--permission-mode` (à utiliser avec prudence)                                                                            | `claude --permission-mode plan --allow-dangerously-skip-permissions`                               |
| `--allowedTools`                       | Outils qui s'exécutent sans demander la permission. Voir [syntaxe des règles de permission](/fr/settings#permission-rule-syntax) pour la correspondance de motifs. Pour restreindre les outils disponibles, utilisez `--tools` à la place  | `"Bash(git log *)" "Bash(git diff *)" "Read"`                                                      |
| `--append-system-prompt`               | Ajouter du texte personnalisé à la fin de l'invite système par défaut                                                                                                                                                                      | `claude --append-system-prompt "Always use TypeScript"`                                            |
| `--append-system-prompt-file`          | Charger du texte d'invite système supplémentaire à partir d'un fichier et l'ajouter à l'invite par défaut                                                                                                                                  | `claude --append-system-prompt-file ./extra-rules.txt`                                             |
| `--betas`                              | En-têtes bêta à inclure dans les requêtes API (utilisateurs de clé API uniquement)                                                                                                                                                         | `claude --betas interleaved-thinking`                                                              |
| `--chrome`                             | Activer l'[intégration du navigateur Chrome](/fr/chrome) pour l'automatisation web et les tests                                                                                                                                            | `claude --chrome`                                                                                  |
| `--continue`, `-c`                     | Charger la conversation la plus récente dans le répertoire courant                                                                                                                                                                         | `claude --continue`                                                                                |
| `--dangerously-skip-permissions`       | Ignorer toutes les invites de permission (à utiliser avec prudence)                                                                                                                                                                        | `claude --dangerously-skip-permissions`                                                            |
| `--debug`                              | Activer le mode débogage avec filtrage de catégorie optionnel (par exemple, `"api,hooks"` ou `"!statsig,!file"`)                                                                                                                           | `claude --debug "api,mcp"`                                                                         |
| `--disable-slash-commands`             | Désactiver tous les skills et commandes pour cette session                                                                                                                                                                                 | `claude --disable-slash-commands`                                                                  |
| `--disallowedTools`                    | Outils qui sont supprimés du contexte du modèle et ne peuvent pas être utilisés                                                                                                                                                            | `"Bash(git log *)" "Bash(git diff *)" "Edit"`                                                      |
| `--fallback-model`                     | Activer le basculement automatique vers le modèle spécifié lorsque le modèle par défaut est surchargé (mode impression uniquement)                                                                                                         | `claude -p --fallback-model sonnet "query"`                                                        |
| `--fork-session`                       | Lors de la reprise, créer un nouvel ID de session au lieu de réutiliser l'original (à utiliser avec `--resume` ou `--continue`)                                                                                                            | `claude --resume abc123 --fork-session`                                                            |
| `--from-pr`                            | Reprendre les sessions liées à une PR GitHub spécifique. Accepte un numéro de PR ou une URL. Les sessions sont automatiquement liées lors de la création via `gh pr create`                                                                | `claude --from-pr 123`                                                                             |
| `--ide`                                | Se connecter automatiquement à l'IDE au démarrage s'il y a exactement un IDE valide disponible                                                                                                                                             | `claude --ide`                                                                                     |
| `--init`                               | Exécuter les hooks d'initialisation et démarrer le mode interactif                                                                                                                                                                         | `claude --init`                                                                                    |
| `--init-only`                          | Exécuter les hooks d'initialisation et quitter (pas de session interactive)                                                                                                                                                                | `claude --init-only`                                                                               |
| `--include-partial-messages`           | Inclure les événements de streaming partiels dans la sortie (nécessite `--print` et `--output-format=stream-json`)                                                                                                                         | `claude -p --output-format stream-json --include-partial-messages "query"`                         |
| `--input-format`                       | Spécifier le format d'entrée pour le mode impression (options : `text`, `stream-json`)                                                                                                                                                     | `claude -p --output-format json --input-format stream-json`                                        |
| `--json-schema`                        | Obtenir une sortie JSON validée correspondant à un JSON Schema après que l'agent ait terminé son flux de travail (mode impression uniquement, voir [structured outputs](https://platform.claude.com/docs/en/agent-sdk/structured-outputs)) | `claude -p --json-schema '{"type":"object","properties":{...}}' "query"`                           |
| `--maintenance`                        | Exécuter les hooks de maintenance et quitter                                                                                                                                                                                               | `claude --maintenance`                                                                             |
| `--max-budget-usd`                     | Montant en dollars maximum à dépenser pour les appels API avant d'arrêter (mode impression uniquement)                                                                                                                                     | `claude -p --max-budget-usd 5.00 "query"`                                                          |
| `--max-turns`                          | Limiter le nombre de tours agentiques (mode impression uniquement). Quitte avec une erreur lorsque la limite est atteinte. Pas de limite par défaut                                                                                        | `claude -p --max-turns 3 "query"`                                                                  |
| `--mcp-config`                         | Charger les serveurs MCP à partir de fichiers ou de chaînes JSON (séparés par des espaces)                                                                                                                                                 | `claude --mcp-config ./mcp.json`                                                                   |
| `--model`                              | Définit le modèle pour la session actuelle avec un alias pour le dernier modèle (`sonnet` ou `opus`) ou le nom complet d'un modèle                                                                                                         | `claude --model claude-sonnet-4-6`                                                                 |
| `--no-chrome`                          | Désactiver l'[intégration du navigateur Chrome](/fr/chrome) pour cette session                                                                                                                                                             | `claude --no-chrome`                                                                               |
| `--no-session-persistence`             | Désactiver la persistance de session afin que les sessions ne soient pas enregistrées sur le disque et ne puissent pas être reprises (mode impression uniquement)                                                                          | `claude -p --no-session-persistence "query"`                                                       |
| `--output-format`                      | Spécifier le format de sortie pour le mode impression (options : `text`, `json`, `stream-json`)                                                                                                                                            | `claude -p "query" --output-format json`                                                           |
| `--permission-mode`                    | Commencer dans un [mode de permission](/fr/permissions#permission-modes) spécifié                                                                                                                                                          | `claude --permission-mode plan`                                                                    |
| `--permission-prompt-tool`             | Spécifier un outil MCP pour gérer les invites de permission en mode non interactif                                                                                                                                                         | `claude -p --permission-prompt-tool mcp_auth_tool "query"`                                         |
| `--plugin-dir`                         | Charger les plugins à partir de répertoires pour cette session uniquement (répétable)                                                                                                                                                      | `claude --plugin-dir ./my-plugins`                                                                 |
| `--print`, `-p`                        | Imprimer la réponse sans mode interactif (voir la [documentation Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) pour les détails d'utilisation programmatique)                                                         | `claude -p "query"`                                                                                |
| `--remote`                             | Créer une nouvelle [session web](/fr/claude-code-on-the-web) sur claude.ai avec la description de tâche fournie                                                                                                                            | `claude --remote "Fix the login bug"`                                                              |
| `--resume`, `-r`                       | Reprendre une session spécifique par ID ou nom, ou afficher un sélecteur interactif pour choisir une session                                                                                                                               | `claude --resume auth-refactor`                                                                    |
| `--session-id`                         | Utiliser un ID de session spécifique pour la conversation (doit être un UUID valide)                                                                                                                                                       | `claude --session-id "550e8400-e29b-41d4-a716-446655440000"`                                       |
| `--setting-sources`                    | Liste séparée par des virgules des sources de paramètres à charger (`user`, `project`, `local`)                                                                                                                                            | `claude --setting-sources user,project`                                                            |
| `--settings`                           | Chemin vers un fichier JSON de paramètres ou une chaîne JSON pour charger des paramètres supplémentaires                                                                                                                                   | `claude --settings ./settings.json`                                                                |
| `--strict-mcp-config`                  | Utiliser uniquement les serveurs MCP de `--mcp-config`, en ignorant toutes les autres configurations MCP                                                                                                                                   | `claude --strict-mcp-config --mcp-config ./mcp.json`                                               |
| `--system-prompt`                      | Remplacer l'invite système entière par du texte personnalisé                                                                                                                                                                               | `claude --system-prompt "You are a Python expert"`                                                 |
| `--system-prompt-file`                 | Charger l'invite système à partir d'un fichier, remplaçant l'invite par défaut                                                                                                                                                             | `claude --system-prompt-file ./custom-prompt.txt`                                                  |
| `--teleport`                           | Reprendre une [session web](/fr/claude-code-on-the-web) dans votre terminal local                                                                                                                                                          | `claude --teleport`                                                                                |
| `--teammate-mode`                      | Définir comment les coéquipiers de l'[équipe d'agents](/fr/agent-teams) s'affichent : `auto` (par défaut), `in-process`, ou `tmux`. Voir [configurer les équipes d'agents](/fr/agent-teams#set-up-agent-teams)                             | `claude --teammate-mode in-process`                                                                |
| `--tools`                              | Restreindre les outils intégrés que Claude peut utiliser. Utilisez `""` pour désactiver tous, `"default"` pour tous, ou des noms d'outils comme `"Bash,Edit,Read"`                                                                         | `claude --tools "Bash,Edit,Read"`                                                                  |
| `--verbose`                            | Activer la journalisation détaillée, affiche la sortie complète tour par tour                                                                                                                                                              | `claude --verbose`                                                                                 |
| `--version`, `-v`                      | Afficher le numéro de version                                                                                                                                                                                                              | `claude -v`                                                                                        |
| `--worktree`, `-w`                     | Démarrer Claude dans un [git worktree](/fr/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) isolé à `<repo>/.claude/worktrees/<name>`. Si aucun nom n'est donné, un est généré automatiquement                       | `claude -w feature-auth`                                                                           |

<Tip>
  Le drapeau `--output-format json` est particulièrement utile pour les scripts et
  l'automatisation, vous permettant d'analyser les réponses de Claude par programmation.
</Tip>

### Format du drapeau agents

Le drapeau `--agents` accepte un objet JSON qui définit un ou plusieurs subagents personnalisés. Chaque subagent nécessite un nom unique (comme clé) et un objet de définition avec les champs suivants :

| Champ             | Requis | Description                                                                                                                                                                                                                                       |
| :---------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `description`     | Oui    | Description en langage naturel du moment où le subagent doit être invoqué                                                                                                                                                                         |
| `prompt`          | Oui    | L'invite système qui guide le comportement du subagent                                                                                                                                                                                            |
| `tools`           | Non    | Tableau des outils spécifiques que le subagent peut utiliser, par exemple `["Read", "Edit", "Bash"]`. S'il est omis, hérite de tous les outils. Supporte la syntaxe [`Agent(agent_type)`](/fr/sub-agents#restrict-which-subagents-can-be-spawned) |
| `disallowedTools` | Non    | Tableau des noms d'outils à explicitement refuser pour ce subagent                                                                                                                                                                                |
| `model`           | Non    | Alias de modèle à utiliser : `sonnet`, `opus`, `haiku`, ou `inherit`. S'il est omis, par défaut `inherit`                                                                                                                                         |
| `skills`          | Non    | Tableau des noms de [skill](/fr/skills) à précharger dans le contexte du subagent                                                                                                                                                                 |
| `mcpServers`      | Non    | Tableau des [serveurs MCP](/fr/mcp) pour ce subagent. Chaque entrée est une chaîne de nom de serveur ou un objet `{name: config}`                                                                                                                 |
| `maxTurns`        | Non    | Nombre maximum de tours agentiques avant que le subagent s'arrête                                                                                                                                                                                 |

Exemple :

```bash  theme={null}
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

Pour plus de détails sur la création et l'utilisation de subagents, voir la [documentation des subagents](/fr/sub-agents).

### Drapeaux d'invite système

Claude Code fournit quatre drapeaux pour personnaliser l'invite système. Les quatre fonctionnent à la fois en mode interactif et non interactif.

| Drapeau                       | Comportement                                           | Cas d'utilisation                                                                                       |
| :---------------------------- | :----------------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `--system-prompt`             | **Remplace** l'invite par défaut entière               | Contrôle complet sur le comportement et les instructions de Claude                                      |
| `--system-prompt-file`        | **Remplace** par le contenu du fichier                 | Charger les invites à partir de fichiers pour la reproductibilité et le contrôle de version             |
| `--append-system-prompt`      | **Ajoute** à l'invite par défaut                       | Ajouter des instructions spécifiques tout en conservant le comportement par défaut de Claude Code       |
| `--append-system-prompt-file` | **Ajoute** le contenu du fichier à l'invite par défaut | Charger des instructions supplémentaires à partir de fichiers tout en conservant les valeurs par défaut |

**Quand utiliser chacun :**

* **`--system-prompt`** : utilisez lorsque vous avez besoin d'un contrôle complet sur l'invite système de Claude. Cela supprime toutes les instructions Claude Code par défaut, vous donnant une ardoise vierge.
  ```bash  theme={null}
  claude --system-prompt "You are a Python expert who only writes type-annotated code"
  ```

* **`--system-prompt-file`** : utilisez lorsque vous souhaitez charger une invite personnalisée à partir d'un fichier, utile pour la cohérence d'équipe ou les modèles d'invite contrôlés par version.
  ```bash  theme={null}
  claude --system-prompt-file ./prompts/code-review.txt
  ```

* **`--append-system-prompt`** : utilisez lorsque vous souhaitez ajouter des instructions spécifiques tout en conservant les capacités par défaut de Claude Code. C'est l'option la plus sûre pour la plupart des cas d'utilisation.
  ```bash  theme={null}
  claude --append-system-prompt "Always use TypeScript and include JSDoc comments"
  ```

* **`--append-system-prompt-file`** : utilisez lorsque vous souhaitez ajouter des instructions à partir d'un fichier tout en conservant les valeurs par défaut de Claude Code. Utile pour les ajouts contrôlés par version.
  ```bash  theme={null}
  claude --append-system-prompt-file ./prompts/style-rules.txt
  ```

`--system-prompt` et `--system-prompt-file` s'excluent mutuellement. Les drapeaux d'ajout peuvent être utilisés ensemble avec l'un ou l'autre drapeau de remplacement.

Pour la plupart des cas d'utilisation, `--append-system-prompt` ou `--append-system-prompt-file` est recommandé car ils préservent les capacités intégrées de Claude Code tout en ajoutant vos exigences personnalisées. Utilisez `--system-prompt` ou `--system-prompt-file` uniquement lorsque vous avez besoin d'un contrôle complet sur l'invite système.

## Voir aussi

* [Extension Chrome](/fr/chrome) - Automatisation du navigateur et tests web
* [Mode interactif](/fr/interactive-mode) - Raccourcis, modes d'entrée et fonctionnalités interactives
* [Guide de démarrage rapide](/fr/quickstart) - Prise en main de Claude Code
* [Flux de travail courants](/fr/common-workflows) - Flux de travail et modèles avancés
* [Paramètres](/fr/settings) - Options de configuration
* [Documentation Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) - Utilisation programmatique et intégrations
