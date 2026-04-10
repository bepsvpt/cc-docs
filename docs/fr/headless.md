> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Exécuter Claude Code par programmation

> Utilisez l'Agent SDK pour exécuter Claude Code par programmation depuis la CLI, Python ou TypeScript.

L'[Agent SDK](https://platform.claude.com/docs/fr/agent-sdk/overview) vous donne accès aux mêmes outils, boucle d'agent et gestion du contexte qui alimentent Claude Code. Il est disponible en tant que CLI pour les scripts et CI/CD, ou en tant que packages [Python](https://platform.claude.com/docs/fr/agent-sdk/python) et [TypeScript](https://platform.claude.com/docs/fr/agent-sdk/typescript) pour un contrôle programmatique complet.

<Note>
  La CLI s'appelait auparavant « mode sans interface ». Le flag `-p` et toutes les options CLI fonctionnent de la même manière.
</Note>

Pour exécuter Claude Code par programmation depuis la CLI, passez `-p` avec votre prompt et toute [option CLI](/fr/cli-reference) :

```bash  theme={null}
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

Cette page couvre l'utilisation de l'Agent SDK via la CLI (`claude -p`). Pour les packages SDK Python et TypeScript avec sorties structurées, callbacks d'approbation d'outils et objets de message natifs, consultez la [documentation complète de l'Agent SDK](https://platform.claude.com/docs/fr/agent-sdk/overview).

## Utilisation basique

Ajoutez le flag `-p` (ou `--print`) à n'importe quelle commande `claude` pour l'exécuter de manière non-interactive. Toutes les [options CLI](/fr/cli-reference) fonctionnent avec `-p`, notamment :

* `--continue` pour [continuer les conversations](#continue-conversations)
* `--allowedTools` pour [approuver automatiquement les outils](#auto-approve-tools)
* `--output-format` pour [obtenir une sortie structurée](#get-structured-output)

Cet exemple pose une question à Claude sur votre base de code et affiche la réponse :

```bash  theme={null}
claude -p "What does the auth module do?"
```

## Exemples

Ces exemples mettent en évidence les modèles CLI courants.

### Obtenir une sortie structurée

Utilisez `--output-format` pour contrôler la façon dont les réponses sont retournées :

* `text` (par défaut) : sortie en texte brut
* `json` : JSON structuré avec résultat, ID de session et métadonnées
* `stream-json` : JSON délimité par des sauts de ligne pour le streaming en temps réel

Cet exemple retourne un résumé du projet au format JSON avec les métadonnées de session, avec le résultat textuel dans le champ `result` :

```bash  theme={null}
claude -p "Summarize this project" --output-format json
```

Pour obtenir une sortie conforme à un schéma spécifique, utilisez `--output-format json` avec `--json-schema` et une définition [JSON Schema](https://json-schema.org/). La réponse inclut les métadonnées sur la requête (ID de session, utilisation, etc.) avec la sortie structurée dans le champ `structured_output`.

Cet exemple extrait les noms de fonctions et les retourne sous forme de tableau de chaînes :

```bash  theme={null}
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

<Tip>
  Utilisez un outil comme [jq](https://jqlang.github.io/jq/) pour analyser la réponse et extraire des champs spécifiques :

  ```bash  theme={null}
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

```bash  theme={null}
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

L'exemple suivant utilise [jq](https://jqlang.github.io/jq/) pour filtrer les deltas de texte et afficher uniquement le texte en streaming. Le flag `-r` affiche les chaînes brutes (sans guillemets) et `-j` joint sans sauts de ligne pour que les tokens se diffusent en continu :

```bash  theme={null}
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

Pour le streaming programmatique avec callbacks et objets de message, consultez [Réponses en streaming en temps réel](https://platform.claude.com/docs/fr/agent-sdk/streaming-output) dans la documentation de l'Agent SDK.

### Approuver automatiquement les outils

Utilisez `--allowedTools` pour permettre à Claude d'utiliser certains outils sans demander. Cet exemple exécute une suite de tests et corrige les défaillances, permettant à Claude d'exécuter des commandes Bash et de lire/modifier des fichiers sans demander la permission :

```bash  theme={null}
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

### Créer un commit

Cet exemple examine les modifications mises en scène et crée un commit avec un message approprié :

```bash  theme={null}
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

Le flag `--allowedTools` utilise la [syntaxe des règles de permission](/fr/settings#permission-rule-syntax). L'espace ` *` à la fin active la correspondance de préfixe, donc `Bash(git diff *)` autorise n'importe quelle commande commençant par `git diff`. L'espace avant `*` est important : sans lui, `Bash(git diff*)` correspondrait également à `git diff-index`.

<Note>
  Les [skills](/fr/skills) invoquées par l'utilisateur comme `/commit` et les [commandes intégrées](/fr/commands) ne sont disponibles qu'en mode interactif. En mode `-p`, décrivez plutôt la tâche que vous souhaitez accomplir.
</Note>

### Personnaliser le prompt système

Utilisez `--append-system-prompt` pour ajouter des instructions tout en conservant le comportement par défaut de Claude Code. Cet exemple envoie un diff de PR à Claude et lui demande de vérifier les vulnérabilités de sécurité :

```bash  theme={null}
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

Consultez les [flags de prompt système](/fr/cli-reference#system-prompt-flags) pour plus d'options, notamment `--system-prompt` pour remplacer complètement le prompt par défaut.

### Continuer les conversations

Utilisez `--continue` pour continuer la conversation la plus récente, ou `--resume` avec un ID de session pour continuer une conversation spécifique. Cet exemple exécute un examen, puis envoie des prompts de suivi :

```bash  theme={null}
# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

Si vous exécutez plusieurs conversations, capturez l'ID de session pour reprendre une conversation spécifique :

```bash  theme={null}
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

## Étapes suivantes

* [Démarrage rapide de l'Agent SDK](https://platform.claude.com/docs/fr/agent-sdk/quickstart) : créez votre premier agent avec Python ou TypeScript
* [Référence CLI](/fr/cli-reference) : tous les flags et options CLI
* [GitHub Actions](/fr/github-actions) : utilisez l'Agent SDK dans les workflows GitHub
* [GitLab CI/CD](/fr/gitlab-ci-cd) : utilisez l'Agent SDK dans les pipelines GitLab
