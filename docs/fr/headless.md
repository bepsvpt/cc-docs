> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Exécuter Claude Code par programmation

> Utilisez l'Agent SDK pour exécuter Claude Code par programmation depuis la CLI, Python ou TypeScript.

<Note>
  Starting June 15, 2026, Agent SDK and `claude -p` usage on subscription plans will draw from a new monthly Agent SDK credit, separate from your interactive usage limits. See [Use the Claude Agent SDK with your Claude plan](https://support.claude.com/en/articles/15036540-use-the-claude-agent-sdk-with-your-claude-plan) for details.
</Note>

L'[Agent SDK](/fr/agent-sdk/overview) vous donne accès aux mêmes outils, boucle d'agent et gestion du contexte qui alimentent Claude Code. Il est disponible en tant que CLI pour les scripts et CI/CD, ou en tant que packages [Python](/fr/agent-sdk/python) et [TypeScript](/fr/agent-sdk/typescript) pour un contrôle programmatique complet.

Pour exécuter Claude Code en mode non interactif, passez `-p` avec votre prompt et toute [option CLI](/fr/cli-reference) :

```bash theme={null}
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

Cette page couvre l'utilisation de l'Agent SDK via la CLI (`claude -p`). Pour les packages SDK Python et TypeScript avec sorties structurées, callbacks d'approbation d'outils et objets de message natifs, consultez la [documentation complète de l'Agent SDK](/fr/agent-sdk/overview).

## Utilisation basique

Ajoutez le flag `-p` (ou `--print`) à n'importe quelle commande `claude` pour l'exécuter de manière non-interactive. Toutes les [options CLI](/fr/cli-reference) fonctionnent avec `-p`, notamment :

* `--continue` pour [continuer les conversations](#continue-conversations)
* `--allowedTools` pour [approuver automatiquement les outils](#auto-approve-tools)
* `--output-format` pour [obtenir une sortie structurée](#get-structured-output)

Cet exemple pose une question à Claude sur votre base de code et affiche la réponse :

```bash theme={null}
claude -p "What does the auth module do?"
```

### Démarrer plus rapidement avec le mode bare

Ajoutez `--bare` pour réduire le temps de démarrage en ignorant la découverte automatique des hooks, skills, plugins, serveurs MCP, mémoire automatique et CLAUDE.md. Sans cela, `claude -p` charge le même [contexte](/fr/how-claude-code-works#the-context-window) qu'une session interactive, y compris tout ce qui est configuré dans le répertoire de travail ou `~/.claude`.

Le mode bare est utile pour CI et les scripts où vous avez besoin du même résultat sur chaque machine. Un hook dans le `~/.claude` d'un coéquipier ou un serveur MCP dans le `.mcp.json` du projet ne s'exécutera pas, car le mode bare ne les lit jamais. Seuls les flags que vous passez explicitement prennent effet.

Cet exemple exécute une tâche de résumé ponctuelle en mode bare et pré-approuve l'outil Read pour que l'appel se termine sans invite de permission :

```bash theme={null}
claude --bare -p "Summarize this file" --allowedTools "Read"
```

En mode bare, Claude a accès aux outils Bash, lecture de fichier et modification de fichier. Passez tout contexte dont vous avez besoin avec un flag :

| Pour charger             | Utilisez                                                |
| ------------------------ | ------------------------------------------------------- |
| Ajouts de prompt système | `--append-system-prompt`, `--append-system-prompt-file` |
| Paramètres               | `--settings <file-or-json>`                             |
| Serveurs MCP             | `--mcp-config <file-or-json>`                           |
| Agents personnalisés     | `--agents <json>`                                       |
| Un plugin                | `--plugin-dir <path>`, `--plugin-url <url>`             |

Le mode bare ignore OAuth et les lectures du trousseau. L'authentification Anthropic doit provenir de `ANTHROPIC_API_KEY` ou d'un `apiKeyHelper` dans le JSON passé à `--settings`. Bedrock, Vertex et Foundry utilisent leurs identifiants de fournisseur habituels.

<Note>
  `--bare` est le mode recommandé pour les appels scriptés et SDK, et deviendra le mode par défaut pour `-p` dans une version future.
</Note>

## Exemples

Ces exemples mettent en évidence les modèles CLI courants. Pour CI et autres appels scriptés, ajoutez [`--bare`](#start-faster-with-bare-mode) pour qu'ils ne reprennent pas ce qui se trouve configuré localement.

### Transmettre des données via Claude

Le mode non-interactif lit stdin, vous pouvez donc transmettre des données et rediriger la réponse comme n'importe quel autre outil en ligne de commande.

Cet exemple transmet un journal de compilation à Claude et écrit l'explication dans un fichier :

```bash theme={null}
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

Avec `--output-format json`, la charge utile de réponse inclut `total_cost_usd` et une ventilation des coûts par modèle, afin que les appelants scriptés puissent suivre les dépenses par invocation sans consulter le [tableau de bord d'utilisation](/fr/costs).

<Note>
  À partir de Claude Code v2.1.128, stdin transmis est limité à 10 Mo. Si vous dépassez la limite, Claude Code se ferme avec une erreur claire et un statut non nul. Pour travailler avec des entrées plus grandes, écrivez le contenu dans un fichier et référencez le chemin du fichier dans votre prompt au lieu de le transmettre.
</Note>

### Ajouter Claude à un script de compilation

Vous pouvez envelopper un appel non-interactif dans un script pour utiliser Claude comme linter ou examinateur spécifique au projet.

Ce script `package.json` transmet le diff par rapport à `main` à Claude et lui demande de signaler les fautes de frappe. Transmettre le diff signifie que Claude n'a pas besoin de permission Bash pour le lire, et les guillemets échappés gardent le script portable vers Windows :

```json theme={null}
{
  "scripts": {
    "lint:claude": "git diff main | claude -p \"you are a typo linter. for each typo in this diff, report filename:line on one line and the issue on the next. return nothing else.\""
  }
}
```

### Obtenir une sortie structurée

Utilisez `--output-format` pour contrôler la façon dont les réponses sont retournées :

* `text` (par défaut) : sortie en texte brut
* `json` : JSON structuré avec résultat, ID de session et métadonnées
* `stream-json` : JSON délimité par des sauts de ligne pour le streaming en temps réel

Cet exemple retourne un résumé du projet au format JSON avec les métadonnées de session, avec le résultat textuel dans le champ `result` :

```bash theme={null}
claude -p "Summarize this project" --output-format json
```

Pour obtenir une sortie conforme à un schéma spécifique, utilisez `--output-format json` avec `--json-schema` et une définition [JSON Schema](https://json-schema.org/). La réponse inclut les métadonnées sur la requête (ID de session, utilisation, etc.) avec la sortie structurée dans le champ `structured_output`.

Cet exemple extrait les noms de fonctions et les retourne sous forme de tableau de chaînes :

```bash theme={null}
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

<Tip>
  Utilisez un outil comme [jq](https://jqlang.github.io/jq/) pour analyser la réponse et extraire des champs spécifiques :

  ```bash theme={null}
  # Extract the text result
  claude -p "Summarize this project" --output-format json | jq -r '.result'

  # Extract structured output
  claude -p "Extract function names from auth.py" \
    --output-format json \
    --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
    | jq '.structured_output'
  ```
</Tip>

### Réponses en streaming

Utilisez `--output-format stream-json` avec `--verbose` et `--include-partial-messages` pour recevoir les tokens au fur et à mesure qu'ils sont générés. Chaque ligne est un objet JSON représentant un événement :

```bash theme={null}
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

L'exemple suivant utilise [jq](https://jqlang.github.io/jq/) pour filtrer les deltas de texte et afficher uniquement le texte en streaming. Le flag `-r` affiche les chaînes brutes (sans guillemets) et `-j` joint sans sauts de ligne pour que les tokens se diffusent en continu :

```bash theme={null}
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

Quand une requête API échoue avec une erreur réessayable, Claude Code émet un événement `system/api_retry` avant de réessayer. Vous pouvez l'utiliser pour afficher la progression des tentatives ou implémenter une logique de backoff personnalisée.

| Champ            | Type           | Description                                                                                                                                                                |
| ---------------- | -------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`           | `"system"`     | type de message                                                                                                                                                            |
| `subtype`        | `"api_retry"`  | identifie ceci comme un événement de tentative                                                                                                                             |
| `attempt`        | entier         | numéro de tentative actuel, commençant à 1                                                                                                                                 |
| `max_retries`    | entier         | nombre total de tentatives autorisées                                                                                                                                      |
| `retry_delay_ms` | entier         | millisecondes jusqu'à la prochaine tentative                                                                                                                               |
| `error_status`   | entier ou null | code de statut HTTP, ou `null` pour les erreurs de connexion sans réponse HTTP                                                                                             |
| `error`          | chaîne         | catégorie d'erreur : `authentication_failed`, `oauth_org_not_allowed`, `billing_error`, `rate_limit`, `invalid_request`, `server_error`, `max_output_tokens`, ou `unknown` |
| `uuid`           | chaîne         | identifiant d'événement unique                                                                                                                                             |
| `session_id`     | chaîne         | session à laquelle appartient l'événement                                                                                                                                  |

L'événement `system/init` rapporte les métadonnées de session, y compris le modèle, les outils, les serveurs MCP et les plugins chargés. C'est le premier événement du flux sauf si [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/fr/env-vars) est défini, auquel cas les événements `plugin_install` le précèdent. Utilisez les champs de plugin pour échouer CI quand un plugin n'a pas pu être chargé :

| Champ           | Type    | Description                                                                                                                                                                                                                                                                                                                                        |
| --------------- | ------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `plugins`       | tableau | plugins qui se sont chargés avec succès, chacun avec `name` et `path`                                                                                                                                                                                                                                                                              |
| `plugin_errors` | tableau | erreurs de chargement de plugin, chacune avec `plugin`, `type` et `message`. Inclut les versions de dépendance non satisfaites et les défaillances de chargement `--plugin-dir` telles qu'un chemin manquant ou une archive invalide. Les plugins affectés sont rétrogradés et absents de `plugins`. La clé est omise quand il n'y a pas d'erreurs |

Quand [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/fr/env-vars) est défini, Claude Code émet des événements `system/plugin_install` pendant que les plugins de marketplace s'installent avant le premier tour. Utilisez-les pour afficher la progression de l'installation dans votre propre interface utilisateur.

| Champ        | Type                                                     | Description                                                                                                                   |
| ------------ | -------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `type`       | `"system"`                                               | type de message                                                                                                               |
| `subtype`    | `"plugin_install"`                                       | identifie ceci comme un événement d'installation de plugin                                                                    |
| `status`     | `"started"`, `"installed"`, `"failed"`, ou `"completed"` | `started` et `completed` encadrent l'installation globale ; `installed` et `failed` rapportent les marketplaces individuelles |
| `name`       | chaîne, optionnel                                        | nom de la marketplace, présent sur `installed` et `failed`                                                                    |
| `error`      | chaîne, optionnel                                        | message d'échec, présent sur `failed`                                                                                         |
| `uuid`       | chaîne                                                   | identifiant d'événement unique                                                                                                |
| `session_id` | chaîne                                                   | session à laquelle appartient l'événement                                                                                     |

Pour le streaming programmatique avec callbacks et objets de message, consultez [Réponses en streaming en temps réel](/fr/agent-sdk/streaming-output) dans la documentation de l'Agent SDK.

### Approuver automatiquement les outils

Utilisez `--allowedTools` pour permettre à Claude d'utiliser certains outils sans demander. Cet exemple exécute une suite de tests et corrige les défaillances, permettant à Claude d'exécuter des commandes Bash et de lire/modifier des fichiers sans demander la permission :

```bash theme={null}
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

Pour définir une base de référence pour la session entière au lieu de lister les outils individuels, passez un [mode de permission](/fr/permission-modes). `dontAsk` refuse tout ce qui n'est pas dans vos règles `permissions.allow` ou l'[ensemble de commandes en lecture seule](/fr/permissions#read-only-commands), ce qui est utile pour les exécutions CI verrouillées. `acceptEdits` permet à Claude d'écrire des fichiers sans demander et approuve également automatiquement les commandes de système de fichiers courants telles que `mkdir`, `touch`, `mv` et `cp`. Les autres commandes shell et requêtes réseau ont toujours besoin d'une entrée `--allowedTools` ou d'une règle `permissions.allow`, sinon l'exécution s'arrête quand l'une d'elles est tentée :

```bash theme={null}
claude -p "Apply the lint fixes" --permission-mode acceptEdits
```

### Créer un commit

Cet exemple examine les modifications mises en scène et crée un commit avec un message approprié :

```bash theme={null}
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

Le flag `--allowedTools` utilise la [syntaxe des règles de permission](/fr/settings#permission-rule-syntax). L'espace ` *` à la fin active la correspondance de préfixe, donc `Bash(git diff *)` autorise n'importe quelle commande commençant par `git diff`. L'espace avant `*` est important : sans lui, `Bash(git diff*)` correspondrait également à `git diff-index`.

<Note>
  Les [skills](/fr/skills) invoquées par l'utilisateur comme `/commit` et les [commandes intégrées](/fr/commands) ne sont disponibles qu'en mode interactif. En mode `-p`, décrivez plutôt la tâche que vous souhaitez accomplir.
</Note>

### Personnaliser le prompt système

Utilisez `--append-system-prompt` pour ajouter des instructions tout en conservant le comportement par défaut de Claude Code. Cet exemple envoie un diff de PR à Claude et lui demande de vérifier les vulnérabilités de sécurité :

```bash theme={null}
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

Consultez les [flags de prompt système](/fr/cli-reference#system-prompt-flags) pour plus d'options, notamment `--system-prompt` pour remplacer complètement le prompt par défaut.

### Continuer les conversations

Utilisez `--continue` pour continuer la conversation la plus récente, ou `--resume` avec un ID de session pour continuer une conversation spécifique. Cet exemple exécute un examen, puis envoie des prompts de suivi :

```bash theme={null}
# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

Si vous exécutez plusieurs conversations, capturez l'ID de session pour reprendre une conversation spécifique :

```bash theme={null}
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

## Étapes suivantes

* [Démarrage rapide de l'Agent SDK](/fr/agent-sdk/quickstart) : créez votre premier agent avec Python ou TypeScript
* [Référence CLI](/fr/cli-reference) : tous les flags et options CLI
* [GitHub Actions](/fr/github-actions) : utilisez l'Agent SDK dans les workflows GitHub
* [GitLab CI/CD](/fr/gitlab-ci-cd) : utilisez l'Agent SDK dans les pipelines GitLab
