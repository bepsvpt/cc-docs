> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Aperçu de Claude Code

> Claude Code est un outil de codage agentique qui lit votre base de code, modifie les fichiers, exécute des commandes et s'intègre à vos outils de développement. Disponible dans votre terminal, IDE, application de bureau et navigateur.

Claude Code est un assistant de codage alimenté par l'IA qui vous aide à créer des fonctionnalités, corriger des bogues et automatiser les tâches de développement. Il comprend l'ensemble de votre base de code et peut travailler sur plusieurs fichiers et outils pour accomplir les tâches.

## Commencer

Choisissez votre environnement pour commencer. La plupart des surfaces nécessitent un [abonnement Claude](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_pricing) ou un compte [Anthropic Console](https://console.anthropic.com/). Le CLI Terminal et VS Code prennent également en charge les [fournisseurs tiers](/fr/third-party-integrations).

<Tabs>
  <Tab title="Terminal">
    Le CLI complet pour travailler avec Claude Code directement dans votre terminal. Modifiez les fichiers, exécutez des commandes et gérez l'ensemble de votre projet à partir de la ligne de commande.

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

        If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. Use the PowerShell command above instead. Your prompt shows `PS C:\` when you're in PowerShell.

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

    Ensuite, démarrez Claude Code dans n'importe quel projet :

    ```bash  theme={null}
    cd your-project
    claude
    ```

    Vous serez invité à vous connecter lors de la première utilisation. C'est tout ! [Continuez avec le Démarrage rapide →](/fr/quickstart)

    <Tip>
      Consultez la [configuration avancée](/fr/setup) pour les options d'installation, les mises à jour manuelles ou les instructions de désinstallation. Visitez la [résolution des problèmes](/fr/troubleshooting) si vous rencontrez des problèmes.
    </Tip>
  </Tab>

  <Tab title="VS Code">
    L'extension VS Code fournit des diffs en ligne, des mentions @, un examen du plan et l'historique des conversations directement dans votre éditeur.

    * [Installer pour VS Code](vscode:extension/anthropic.claude-code)
    * [Installer pour Cursor](cursor:extension/anthropic.claude-code)

    Ou recherchez « Claude Code » dans la vue Extensions (`Cmd+Shift+X` sur Mac, `Ctrl+Shift+X` sur Windows/Linux). Après l'installation, ouvrez la Palette de commandes (`Cmd+Shift+P` / `Ctrl+Shift+P`), tapez « Claude Code » et sélectionnez **Ouvrir dans un nouvel onglet**.

    [Commencer avec VS Code →](/fr/vs-code#get-started)
  </Tab>

  <Tab title="Application de bureau">
    Une application autonome pour exécuter Claude Code en dehors de votre IDE ou terminal. Examinez les diffs visuellement, exécutez plusieurs sessions côte à côte, planifiez des tâches récurrentes et lancez des sessions cloud.

    Téléchargez et installez :

    * [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) (Intel et Apple Silicon)
    * [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) (x64)
    * [Windows ARM64](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) (sessions distantes uniquement)

    Après l'installation, lancez Claude, connectez-vous et cliquez sur l'onglet **Code** pour commencer à coder. Un [abonnement payant](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=overview_desktop_pricing) est requis.

    [En savoir plus sur l'application de bureau →](/fr/desktop-quickstart)
  </Tab>

  <Tab title="Web">
    Exécutez Claude Code dans votre navigateur sans configuration locale. Lancez des tâches longues et revenez quand elles sont terminées, travaillez sur des dépôts que vous n'avez pas localement ou exécutez plusieurs tâches en parallèle. Disponible sur les navigateurs de bureau et l'application Claude iOS.

    Commencez à coder sur [claude.ai/code](https://claude.ai/code).

    [Commencer sur le web →](/fr/claude-code-on-the-web#getting-started)
  </Tab>

  <Tab title="JetBrains">
    Un plugin pour IntelliJ IDEA, PyCharm, WebStorm et autres IDE JetBrains avec visualisation interactive des diffs et partage du contexte de sélection.

    Installez le [plugin Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) depuis la Marketplace JetBrains et redémarrez votre IDE.

    [Commencer avec JetBrains →](/fr/jetbrains)
  </Tab>
</Tabs>

## Ce que vous pouvez faire

Voici quelques-unes des façons dont vous pouvez utiliser Claude Code :

<AccordionGroup>
  <Accordion title="Automatiser le travail que vous reprenez sans cesse" icon="wand-magic-sparkles">
    Claude Code gère les tâches fastidieuses qui vous prennent du temps : écrire des tests pour le code non testé, corriger les erreurs de lint dans un projet, résoudre les conflits de fusion, mettre à jour les dépendances et écrire les notes de version.

    ```bash  theme={null}
    claude "write tests for the auth module, run them, and fix any failures"
    ```
  </Accordion>

  <Accordion title="Créer des fonctionnalités et corriger des bogues" icon="hammer">
    Décrivez ce que vous voulez en langage naturel. Claude Code planifie l'approche, écrit le code sur plusieurs fichiers et vérifie qu'il fonctionne.

    Pour les bogues, collez un message d'erreur ou décrivez le symptôme. Claude Code trace le problème dans votre base de code, identifie la cause racine et implémente une correction. Consultez les [flux de travail courants](/fr/common-workflows) pour plus d'exemples.
  </Accordion>

  <Accordion title="Créer des commits et des demandes de tirage" icon="code-branch">
    Claude Code fonctionne directement avec git. Il prépare les modifications, écrit les messages de commit, crée des branches et ouvre des demandes de tirage.

    ```bash  theme={null}
    claude "commit my changes with a descriptive message"
    ```

    En CI, vous pouvez automatiser l'examen du code et le triage des problèmes avec [GitHub Actions](/fr/github-actions) ou [GitLab CI/CD](/fr/gitlab-ci-cd).
  </Accordion>

  <Accordion title="Connecter vos outils avec MCP" icon="plug">
    Le [Model Context Protocol (MCP)](/fr/mcp) est une norme ouverte pour connecter les outils d'IA aux sources de données externes. Avec MCP, Claude Code peut lire vos documents de conception dans Google Drive, mettre à jour les tickets dans Jira, extraire les données de Slack ou utiliser vos outils personnalisés.
  </Accordion>

  <Accordion title="Personnaliser avec des instructions, des skills et des hooks" icon="sliders">
    [`CLAUDE.md`](/fr/memory) est un fichier markdown que vous ajoutez à la racine de votre projet que Claude Code lit au début de chaque session. Utilisez-le pour définir les normes de codage, les décisions architecturales, les bibliothèques préférées et les listes de contrôle d'examen. Claude construit également une [mémoire automatique](/fr/memory#auto-memory) au fur et à mesure qu'il travaille, en sauvegardant les apprentissages comme les commandes de construction et les informations de débogage entre les sessions sans que vous ayez à écrire quoi que ce soit.

    Créez des [commandes personnalisées](/fr/skills) pour empaqueter les flux de travail répétables que votre équipe peut partager, comme `/review-pr` ou `/deploy-staging`.

    Les [hooks](/fr/hooks) vous permettent d'exécuter des commandes shell avant ou après les actions de Claude Code, comme le formatage automatique après chaque modification de fichier ou l'exécution de lint avant un commit.
  </Accordion>

  <Accordion title="Exécuter des équipes d'agents et créer des agents personnalisés" icon="users">
    Lancez [plusieurs agents Claude Code](/fr/sub-agents) qui travaillent sur différentes parties d'une tâche simultanément. Un agent principal coordonne le travail, assigne les sous-tâches et fusionne les résultats.

    Pour les flux de travail entièrement personnalisés, le [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) vous permet de créer vos propres agents alimentés par les outils et capacités de Claude Code, avec un contrôle total sur l'orchestration, l'accès aux outils et les permissions.
  </Accordion>

  <Accordion title="Piping, scripts et automatisation avec le CLI" icon="terminal">
    Claude Code est composable et suit la philosophie Unix. Canalisez les journaux dedans, exécutez-le en CI ou chaînez-le avec d'autres outils :

    ```bash  theme={null}
    # Analyser la sortie récente des journaux
    tail -200 app.log | claude -p "Slack me if you see any anomalies"

    # Automatiser les traductions en CI
    claude -p "translate new strings into French and raise a PR for review"

    # Opérations en masse sur les fichiers
    git diff main --name-only | claude -p "review these changed files for security issues"
    ```

    Consultez la [référence CLI](/fr/cli-reference) pour l'ensemble complet des commandes et des drapeaux.
  </Accordion>

  <Accordion title="Planifier des tâches récurrentes" icon="clock">
    Exécutez Claude selon un calendrier pour automatiser le travail qui se répète : examens de PR le matin, analyse des défaillances CI pendant la nuit, audits de dépendances hebdomadaires ou synchronisation des documents après la fusion des PR.

    * Les [tâches planifiées cloud](/fr/web-scheduled-tasks) s'exécutent sur l'infrastructure gérée par Anthropic, elles continuent donc à s'exécuter même quand votre ordinateur est éteint. Créez-les à partir du web, de l'application de bureau ou en exécutant `/schedule` dans le CLI.
    * Les [tâches planifiées de bureau](/fr/desktop#schedule-recurring-tasks) s'exécutent sur votre machine, avec un accès direct à vos fichiers et outils locaux
    * [`/loop`](/fr/scheduled-tasks) répète une invite dans une session CLI pour un sondage rapide
  </Accordion>

  <Accordion title="Travailler de n'importe où" icon="globe">
    Les sessions ne sont pas liées à une seule surface. Déplacez le travail entre les environnements à mesure que votre contexte change :

    * Éloignez-vous de votre bureau et continuez à travailler depuis votre téléphone ou n'importe quel navigateur avec [Contrôle à distance](/fr/remote-control)
    * Envoyez un message à [Dispatch](/fr/desktop#sessions-from-dispatch) une tâche depuis votre téléphone et ouvrez la session de bureau qu'il crée
    * Lancez une tâche longue sur le [web](/fr/claude-code-on-the-web) ou l'[application iOS](https://apps.apple.com/app/claude-by-anthropic/id6473753684), puis tirez-la dans votre terminal avec `/teleport`
    * Remettez une session de terminal à l'[application de bureau](/fr/desktop) avec `/desktop` pour un examen visuel des diffs
    * Acheminez les tâches depuis le chat d'équipe : mentionnez `@Claude` dans [Slack](/fr/slack) avec un rapport de bogue et récupérez une demande de tirage
  </Accordion>
</AccordionGroup>

## Utiliser Claude Code partout

Chaque surface se connecte au même moteur Claude Code sous-jacent, donc vos fichiers CLAUDE.md, paramètres et serveurs MCP fonctionnent sur tous.

Au-delà des environnements [Terminal](/fr/quickstart), [VS Code](/fr/vs-code), [JetBrains](/fr/jetbrains), [Desktop](/fr/desktop) et [Web](/fr/claude-code-on-the-web) ci-dessus, Claude Code s'intègre avec les flux de travail CI/CD, chat et navigateur :

| Je veux...                                                                           | Meilleure option                                                                                                           |
| ------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------- |
| Continuer une session locale depuis mon téléphone ou un autre appareil               | [Contrôle à distance](/fr/remote-control)                                                                                  |
| Envoyer des événements de Telegram, Discord ou mes propres webhooks dans une session | [Canaux](/fr/channels)                                                                                                     |
| Démarrer une tâche localement, continuer sur mobile                                  | [Web](/fr/claude-code-on-the-web) ou [application Claude iOS](https://apps.apple.com/app/claude-by-anthropic/id6473753684) |
| Exécuter Claude selon un calendrier récurrent                                        | [Tâches planifiées cloud](/fr/web-scheduled-tasks) ou [Tâches planifiées de bureau](/fr/desktop#schedule-recurring-tasks)  |
| Automatiser les examens de PR et le triage des problèmes                             | [GitHub Actions](/fr/github-actions) ou [GitLab CI/CD](/fr/gitlab-ci-cd)                                                   |
| Obtenir un examen automatique du code sur chaque PR                                  | [Examen du code GitHub](/fr/code-review)                                                                                   |
| Acheminer les rapports de bogues de Slack vers les demandes de tirage                | [Slack](/fr/slack)                                                                                                         |
| Déboguer les applications web en direct                                              | [Chrome](/fr/chrome)                                                                                                       |
| Créer des agents personnalisés pour vos propres flux de travail                      | [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)                                                        |

## Étapes suivantes

Une fois que vous avez installé Claude Code, ces guides vous aident à approfondir.

* [Démarrage rapide](/fr/quickstart) : parcourez votre première tâche réelle, de l'exploration d'une base de code à la validation d'une correction
* [Stocker les instructions et les mémoires](/fr/memory) : donnez à Claude des instructions persistantes avec les fichiers CLAUDE.md et la mémoire automatique
* [Flux de travail courants](/fr/common-workflows) et [meilleures pratiques](/fr/best-practices) : modèles pour tirer le meilleur parti de Claude Code
* [Paramètres](/fr/settings) : personnalisez Claude Code pour votre flux de travail
* [Résolution des problèmes](/fr/troubleshooting) : solutions pour les problèmes courants
* [code.claude.com](https://code.claude.com/) : démos, tarification et détails du produit
