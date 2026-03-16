> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Démarrage rapide

> Bienvenue dans Claude Code !

Ce guide de démarrage rapide vous permettra d'utiliser l'assistance au codage alimentée par l'IA en quelques minutes. À la fin, vous comprendrez comment utiliser Claude Code pour les tâches de développement courantes.

## Avant de commencer

Assurez-vous que vous avez :

* Un terminal ou une invite de commande ouvert
  * Si vous n'avez jamais utilisé le terminal auparavant, consultez le [guide du terminal](/fr/terminal-guide)
* Un projet de code avec lequel travailler
* Un [abonnement Claude](https://claude.com/pricing) (Pro, Max, Teams ou Enterprise), un compte [Claude Console](https://console.anthropic.com/), ou un accès via un [fournisseur cloud pris en charge](/fr/third-party-integrations)

<Note>
  Ce guide couvre le CLI du terminal. Claude Code est également disponible sur le [web](https://claude.ai/code), en tant qu'[application de bureau](/fr/desktop), dans [VS Code](/fr/vs-code) et [les IDE JetBrains](/fr/jetbrains), dans [Slack](/fr/slack), et en CI/CD avec [GitHub Actions](/fr/github-actions) et [GitLab](/fr/gitlab-ci-cd). Voir [toutes les interfaces](/fr/overview#use-claude-code-everywhere).
</Note>

## Étape 1 : Installer Claude Code

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell  theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

## Étape 2 : Se connecter à votre compte

Claude Code nécessite un compte pour être utilisé. Lorsque vous démarrez une session interactive avec la commande `claude`, vous devrez vous connecter :

```bash  theme={null}
claude
# Vous serez invité à vous connecter lors de la première utilisation
```

```bash  theme={null}
/login
# Suivez les invites pour vous connecter avec votre compte
```

Vous pouvez vous connecter en utilisant l'un de ces types de compte :

* [Claude Pro, Max, Teams ou Enterprise](https://claude.com/pricing) (recommandé)
* [Claude Console](https://console.anthropic.com/) (accès API avec crédits prépayés). Lors de la première connexion, un espace de travail « Claude Code » est automatiquement créé dans la Console pour un suivi centralisé des coûts.
* [Amazon Bedrock, Google Vertex AI ou Microsoft Foundry](/fr/third-party-integrations) (fournisseurs cloud d'entreprise)

Une fois connecté, vos identifiants sont stockés et vous n'aurez pas besoin de vous reconnecter. Pour changer de compte ultérieurement, utilisez la commande `/login`.

## Étape 3 : Démarrer votre première session

Ouvrez votre terminal dans n'importe quel répertoire de projet et démarrez Claude Code :

```bash  theme={null}
cd /path/to/your/project
claude
```

Vous verrez l'écran de bienvenue de Claude Code avec les informations de votre session, les conversations récentes et les dernières mises à jour. Tapez `/help` pour les commandes disponibles ou `/resume` pour continuer une conversation précédente.

<Tip>
  Après vous être connecté (Étape 2), vos identifiants sont stockés sur votre système. En savoir plus dans [Gestion des identifiants](/fr/authentication#credential-management).
</Tip>

## Étape 4 : Posez votre première question

Commençons par comprendre votre base de code. Essayez l'une de ces commandes :

```text  theme={null}
what does this project do?
```

Claude analysera vos fichiers et fournira un résumé. Vous pouvez également poser des questions plus spécifiques :

```text  theme={null}
what technologies does this project use?
```

```text  theme={null}
where is the main entry point?
```

```text  theme={null}
explain the folder structure
```

Vous pouvez également demander à Claude ses propres capacités :

```text  theme={null}
what can Claude Code do?
```

```text  theme={null}
how do I create custom skills in Claude Code?
```

```text  theme={null}
can Claude Code work with Docker?
```

<Note>
  Claude Code lit vos fichiers de projet selon les besoins. Vous n'avez pas à ajouter manuellement du contexte.
</Note>

## Étape 5 : Effectuez votre première modification de code

Maintenant, faisons en sorte que Claude Code fasse du vrai codage. Essayez une tâche simple :

```text  theme={null}
add a hello world function to the main file
```

Claude Code va :

1. Trouver le fichier approprié
2. Vous montrer les modifications proposées
3. Demander votre approbation
4. Effectuer la modification

<Note>
  Claude Code demande toujours la permission avant de modifier les fichiers. Vous pouvez approuver les modifications individuelles ou activer le mode « Accepter tout » pour une session.
</Note>

## Étape 6 : Utiliser Git avec Claude Code

Claude Code rend les opérations Git conversationnelles :

```text  theme={null}
what files have I changed?
```

```text  theme={null}
commit my changes with a descriptive message
```

Vous pouvez également demander des opérations Git plus complexes :

```text  theme={null}
create a new branch called feature/quickstart
```

```text  theme={null}
show me the last 5 commits
```

```text  theme={null}
help me resolve merge conflicts
```

## Étape 7 : Corriger un bug ou ajouter une fonctionnalité

Claude est compétent pour le débogage et l'implémentation de fonctionnalités.

Décrivez ce que vous voulez en langage naturel :

```text  theme={null}
add input validation to the user registration form
```

Ou corrigez les problèmes existants :

```text  theme={null}
there's a bug where users can submit empty forms - fix it
```

Claude Code va :

* Localiser le code pertinent
* Comprendre le contexte
* Implémenter une solution
* Exécuter les tests si disponibles

## Étape 8 : Testez d'autres flux de travail courants

Il existe plusieurs façons de travailler avec Claude :

**Refactoriser le code**

```text  theme={null}
refactor the authentication module to use async/await instead of callbacks
```

**Écrire des tests**

```text  theme={null}
write unit tests for the calculator functions
```

**Mettre à jour la documentation**

```text  theme={null}
update the README with installation instructions
```

**Révision de code**

```text  theme={null}
review my changes and suggest improvements
```

<Tip>
  Parlez à Claude comme vous le feriez avec un collègue utile. Décrivez ce que vous voulez réaliser, et il vous aidera à y parvenir.
</Tip>

## Commandes essentielles

Voici les commandes les plus importantes pour l'utilisation quotidienne :

| Commande            | Ce qu'elle fait                                                     | Exemple                             |
| ------------------- | ------------------------------------------------------------------- | ----------------------------------- |
| `claude`            | Démarrer le mode interactif                                         | `claude`                            |
| `claude "task"`     | Exécuter une tâche unique                                           | `claude "fix the build error"`      |
| `claude -p "query"` | Exécuter une requête unique, puis quitter                           | `claude -p "explain this function"` |
| `claude -c`         | Continuer la conversation la plus récente dans le répertoire actuel | `claude -c`                         |
| `claude -r`         | Reprendre une conversation précédente                               | `claude -r`                         |
| `claude commit`     | Créer un commit Git                                                 | `claude commit`                     |
| `/clear`            | Effacer l'historique des conversations                              | `/clear`                            |
| `/help`             | Afficher les commandes disponibles                                  | `/help`                             |
| `exit` ou Ctrl+C    | Quitter Claude Code                                                 | `exit`                              |

Voir la [référence CLI](/fr/cli-reference) pour une liste complète des commandes.

## Conseils professionnels pour les débutants

Pour plus d'informations, voir [les meilleures pratiques](/fr/best-practices) et [les flux de travail courants](/fr/common-workflows).

<AccordionGroup>
  <Accordion title="Soyez spécifique dans vos demandes">
    Au lieu de : ' corriger le bug '

    Essayez : ' corriger le bug de connexion où les utilisateurs voient un écran vide après avoir entré des identifiants incorrects '
  </Accordion>

  <Accordion title="Utilisez des instructions étape par étape">
    Divisez les tâches complexes en étapes :

    ```text  theme={null}
    1. create a new database table for user profiles
    2. create an API endpoint to get and update user profiles
    3. build a webpage that allows users to see and edit their information
    ```
  </Accordion>

  <Accordion title="Laissez Claude explorer d'abord">
    Avant de faire des modifications, laissez Claude comprendre votre code :

    ```text  theme={null}
    analyze the database schema
    ```

    ```text  theme={null}
    build a dashboard showing products that are most frequently returned by our UK customers
    ```
  </Accordion>

  <Accordion title="Gagnez du temps avec les raccourcis">
    * Appuyez sur `?` pour voir tous les raccourcis clavier disponibles
    * Utilisez Tab pour la complétion des commandes
    * Appuyez sur ↑ pour l'historique des commandes
    * Tapez `/` pour voir toutes les commandes et skills
  </Accordion>
</AccordionGroup>

## Prochaines étapes

Maintenant que vous avez appris les bases, explorez des fonctionnalités plus avancées :

<CardGroup cols={2}>
  <Card title="Comment fonctionne Claude Code" icon="microchip" href="/fr/how-claude-code-works">
    Comprendre la boucle agentique, les outils intégrés et comment Claude Code interagit avec votre projet
  </Card>

  <Card title="Meilleures pratiques" icon="star" href="/fr/best-practices">
    Obtenez de meilleurs résultats avec un prompting efficace et une configuration de projet appropriée
  </Card>

  <Card title="Flux de travail courants" icon="graduation-cap" href="/fr/common-workflows">
    Guides étape par étape pour les tâches courantes
  </Card>

  <Card title="Étendre Claude Code" icon="puzzle-piece" href="/fr/features-overview">
    Personnalisez avec CLAUDE.md, skills, hooks, MCP et bien plus
  </Card>
</CardGroup>

## Obtenir de l'aide

* **Dans Claude Code** : Tapez `/help` ou demandez « how do I... »
* **Documentation** : Vous êtes ici ! Parcourez les autres guides
* **Communauté** : Rejoignez notre [Discord](https://www.anthropic.com/discord) pour des conseils et du support
