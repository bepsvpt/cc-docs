> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Continuer les sessions locales depuis n'importe quel appareil avec Remote Control

> Continuez une session Claude Code locale depuis votre téléphone, tablette ou n'importe quel navigateur en utilisant Remote Control. Fonctionne avec claude.ai/code et l'application Claude mobile.

<Note>
  Remote Control est disponible sur tous les plans. Sur Team et Enterprise, il est désactivé par défaut jusqu'à ce qu'un administrateur active le bouton Remote Control dans les [paramètres d'administration Claude Code](https://claude.ai/admin-settings/claude-code).
</Note>

Remote Control connecte [claude.ai/code](https://claude.ai/code) ou l'application Claude pour [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) et [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) à une session Claude Code s'exécutant sur votre machine. Commencez une tâche à votre bureau, puis reprenez-la depuis votre téléphone sur le canapé ou un navigateur sur un autre ordinateur.

Lorsque vous démarrez une session Remote Control sur votre machine, Claude continue à s'exécuter localement à tout moment, donc rien ne se déplace vers le cloud. Avec Remote Control, vous pouvez :

* **Utiliser votre environnement local complet à distance** : votre système de fichiers, [serveurs MCP](/fr/mcp), outils et configuration de projet restent tous disponibles
* **Travailler depuis les deux surfaces à la fois** : la conversation reste synchronisée sur tous les appareils connectés, vous pouvez donc envoyer des messages depuis votre terminal, navigateur et téléphone de manière interchangeable
* **Survivre aux interruptions** : si votre ordinateur portable s'endort ou votre réseau tombe en panne, la session se reconnecte automatiquement lorsque votre machine revient en ligne

Contrairement à [Claude Code sur le web](/fr/claude-code-on-the-web), qui s'exécute sur l'infrastructure cloud, les sessions Remote Control s'exécutent directement sur votre machine et interagissent avec votre système de fichiers local. Les interfaces web et mobile ne sont qu'une fenêtre dans cette session locale.

<Note>
  Remote Control nécessite Claude Code v2.1.51 ou version ultérieure. Vérifiez votre version avec `claude --version`.
</Note>

Cette page couvre la configuration, comment démarrer et se connecter aux sessions, et comment Remote Control se compare à Claude Code sur le web.

## Conditions requises

Avant d'utiliser Remote Control, confirmez que votre environnement répond à ces conditions :

* **Abonnement** : disponible sur les plans Pro, Max, Team et Enterprise. Les clés API ne sont pas prises en charge. Sur Team et Enterprise, un administrateur doit d'abord activer le bouton Remote Control dans les [paramètres d'administration Claude Code](https://claude.ai/admin-settings/claude-code).
* **Authentification** : exécutez `claude` et utilisez `/login` pour vous connecter via claude.ai si vous ne l'avez pas déjà fait.
* **Confiance de l'espace de travail** : exécutez `claude` dans votre répertoire de projet au moins une fois pour accepter la boîte de dialogue de confiance de l'espace de travail.

## Démarrer une session Remote Control

Vous pouvez démarrer un serveur Remote Control dédié, démarrer une session interactive avec Remote Control activé, ou connecter une session déjà en cours d'exécution.

<Tabs>
  <Tab title="Mode serveur">
    Accédez à votre répertoire de projet et exécutez :

    ```bash  theme={null}
    claude remote-control
    ```

    Le processus reste en cours d'exécution dans votre terminal en mode serveur, en attente de connexions distantes. Il affiche une URL de session que vous pouvez utiliser pour [vous connecter depuis un autre appareil](#connect-from-another-device), et vous pouvez appuyer sur la barre d'espace pour afficher un code QR pour un accès rapide depuis votre téléphone. Pendant qu'une session distante est active, le terminal affiche l'état de la connexion et l'activité des outils.

    Drapeaux disponibles :

    | Drapeau                      | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
    | ---------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
    | `--name "My Project"`        | Définissez un titre de session personnalisé visible dans la liste des sessions sur claude.ai/code.                                                                                                                                                                                                                                                                                                                                                                 |
    | `--spawn <mode>`             | Comment les sessions concurrentes sont créées. Appuyez sur `w` à l'exécution pour basculer.<br />• `same-dir` (par défaut) : toutes les sessions partagent le répertoire de travail actuel, elles peuvent donc entrer en conflit si elles modifient les mêmes fichiers.<br />• `worktree` : chaque session à la demande obtient sa propre [git worktree](/fr/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees). Nécessite un référentiel git. |
    | `--capacity <N>`             | Nombre maximum de sessions concurrentes. La valeur par défaut est 32.                                                                                                                                                                                                                                                                                                                                                                                              |
    | `--verbose`                  | Afficher les journaux de connexion et de session détaillés.                                                                                                                                                                                                                                                                                                                                                                                                        |
    | `--sandbox` / `--no-sandbox` | Activer ou désactiver le [sandboxing](/fr/sandboxing) pour l'isolation du système de fichiers et du réseau. Désactivé par défaut.                                                                                                                                                                                                                                                                                                                                  |
  </Tab>

  <Tab title="Session interactive">
    Pour démarrer une session Claude Code interactive normale avec Remote Control activé, utilisez le drapeau `--remote-control` (ou `--rc`) :

    ```bash  theme={null}
    claude --remote-control
    ```

    Passez éventuellement un nom pour la session :

    ```bash  theme={null}
    claude --remote-control "My Project"
    ```

    Cela vous donne une session interactive complète dans votre terminal que vous pouvez également contrôler depuis claude.ai ou l'application Claude. Contrairement à `claude remote-control` (mode serveur), vous pouvez taper des messages localement tandis que la session est également disponible à distance.
  </Tab>

  <Tab title="À partir d'une session existante">
    Si vous êtes déjà dans une session Claude Code et que vous souhaitez la continuer à distance, utilisez la commande `/remote-control` (ou `/rc`) :

    ```text  theme={null}
    /remote-control
    ```

    Passez un nom comme argument pour définir un titre de session personnalisé :

    ```text  theme={null}
    /remote-control My Project
    ```

    Cela démarre une session Remote Control qui reprend votre historique de conversation actuel et affiche une URL de session et un code QR que vous pouvez utiliser pour [vous connecter depuis un autre appareil](#connect-from-another-device). Les drapeaux `--verbose`, `--sandbox` et `--no-sandbox` ne sont pas disponibles avec cette commande.
  </Tab>
</Tabs>

### Se connecter depuis un autre appareil

Une fois qu'une session Remote Control est active, vous avez plusieurs façons de vous connecter depuis un autre appareil :

* **Ouvrez l'URL de la session** dans n'importe quel navigateur pour accéder directement à la session sur [claude.ai/code](https://claude.ai/code). À la fois `claude remote-control` et `/remote-control` affichent cette URL dans le terminal.
* **Scannez le code QR** affiché à côté de l'URL de la session pour l'ouvrir directement dans l'application Claude. Avec `claude remote-control`, appuyez sur la barre d'espace pour basculer l'affichage du code QR.
* **Ouvrez [claude.ai/code](https://claude.ai/code) ou l'application Claude** et trouvez la session par nom dans la liste des sessions. Les sessions Remote Control affichent une icône d'ordinateur avec un point d'état vert lorsqu'elles sont en ligne.

Le titre de la session distante est choisi dans cet ordre :

1. Le nom que vous avez passé à `--name`, `--remote-control`, ou `/remote-control`
2. Le titre que vous avez défini avec `/rename`
3. Le dernier message significatif dans l'historique de conversation existant
4. Votre premier message une fois que vous en envoyez un

Si l'environnement a déjà une session active, vous serez invité à choisir si vous souhaitez la continuer ou en démarrer une nouvelle.

Si vous n'avez pas encore l'application Claude, utilisez la commande `/mobile` dans Claude Code pour afficher un code QR de téléchargement pour [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) ou [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).

### Activer Remote Control pour toutes les sessions

Par défaut, Remote Control ne s'active que lorsque vous exécutez explicitement `claude remote-control`, `claude --remote-control`, ou `/remote-control`. Pour l'activer automatiquement pour chaque session interactive, exécutez `/config` dans Claude Code et définissez **Enable Remote Control for all sessions** sur `true`. Définissez-le sur `false` pour le désactiver.

Avec ce paramètre activé, chaque processus Claude Code interactif enregistre une session distante. Si vous exécutez plusieurs instances, chacune obtient son propre environnement et sa propre session. Pour exécuter plusieurs sessions concurrentes à partir d'un seul processus, utilisez plutôt le mode serveur avec `--spawn`.

## Connexion et sécurité

Votre session Claude Code locale effectue uniquement des requêtes HTTPS sortantes et n'ouvre jamais de ports entrants sur votre machine. Lorsque vous démarrez Remote Control, il s'enregistre auprès de l'API Anthropic et interroge le travail. Lorsque vous vous connectez depuis un autre appareil, le serveur achemine les messages entre le client web ou mobile et votre session locale sur une connexion en continu.

Tout le trafic passe par l'API Anthropic sur TLS, le même transport de sécurité que n'importe quelle session Claude Code. La connexion utilise plusieurs identifiants de courte durée, chacun limité à un seul objectif et expirant indépendamment.

## Remote Control vs Claude Code sur le web

Remote Control et [Claude Code sur le web](/fr/claude-code-on-the-web) utilisent tous deux l'interface claude.ai/code. La différence clé est l'endroit où la session s'exécute : Remote Control s'exécute sur votre machine, donc vos serveurs MCP locaux, outils et configuration de projet restent disponibles. Claude Code sur le web s'exécute dans l'infrastructure cloud gérée par Anthropic.

Utilisez Remote Control lorsque vous êtes au milieu d'un travail local et que vous souhaitez continuer depuis un autre appareil. Utilisez Claude Code sur le web lorsque vous souhaitez lancer une tâche sans aucune configuration locale, travailler sur un référentiel que vous n'avez pas cloné, ou exécuter plusieurs tâches en parallèle.

## Limitations

* **Une session distante par processus interactif** : en dehors du mode serveur, chaque instance Claude Code prend en charge une session distante à la fois. Utilisez le mode serveur avec `--spawn` pour exécuter plusieurs sessions concurrentes à partir d'un seul processus.
* **Le terminal doit rester ouvert** : Remote Control s'exécute en tant que processus local. Si vous fermez le terminal ou arrêtez le processus `claude`, la session se termine. Exécutez `claude remote-control` à nouveau pour démarrer une nouvelle session.
* **Panne réseau prolongée** : si votre machine est allumée mais incapable d'atteindre le réseau pendant plus de dix minutes environ, la session expire et le processus se termine. Exécutez `claude remote-control` à nouveau pour démarrer une nouvelle session.

## Dépannage

### « Remote Control is not yet enabled for your account »

La vérification d'admissibilité peut échouer avec certaines variables d'environnement présentes :

* `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` ou `DISABLE_TELEMETRY` : désactivez-les et réessayez.
* `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX`, ou `CLAUDE_CODE_USE_FOUNDRY` : Remote Control nécessite l'authentification claude.ai et ne fonctionne pas avec les fournisseurs tiers.

Si aucun de ceux-ci n'est défini, exécutez `/logout` puis `/login` pour actualiser.

### « Remote Control is disabled by your organization's policy »

Cette erreur a trois causes distinctes. Exécutez d'abord `/status` pour voir quelle méthode de connexion et quel abonnement vous utilisez.

* **Vous êtes authentifié avec une clé API ou un compte Console** : Remote Control nécessite OAuth claude.ai. Exécutez `/login` et choisissez l'option claude.ai. Si `ANTHROPIC_API_KEY` est défini dans votre environnement, désactivez-le.
* **Votre administrateur Team ou Enterprise ne l'a pas activé** : Remote Control est désactivé par défaut sur ces plans. Un administrateur peut l'activer sur [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) en activant le bouton **Remote Control**. C'est un paramètre d'organisation côté serveur, pas une clé de [paramètres gérés](/fr/permissions#managed-only-settings).
* **Le bouton d'administration est grisé** : votre organisation a une configuration de rétention des données ou de conformité incompatible avec Remote Control. Cela ne peut pas être modifié à partir du panneau d'administration. Contactez le support Anthropic pour discuter des options.

### « Remote credentials fetch failed »

Claude Code n'a pas pu obtenir une accréditation de courte durée auprès de l'API Anthropic pour établir la connexion. Réexécutez avec `--verbose` pour voir l'erreur complète :

```bash  theme={null}
claude remote-control --verbose
```

Causes courantes :

* Non connecté : exécutez `claude` et utilisez `/login` pour vous authentifier avec votre compte claude.ai. L'authentification par clé API n'est pas prise en charge pour Remote Control.
* Problème de réseau ou de proxy : un pare-feu ou un proxy peut bloquer la requête HTTPS sortante. Remote Control nécessite l'accès à l'API Anthropic sur le port 443.
* Échec de la création de session : si vous voyez également `Session creation failed — see debug log`, l'échec s'est produit plus tôt dans la configuration. Vérifiez que votre abonnement est actif.

## Choisir la bonne approche

Claude Code offers several ways to work when you're not at your terminal. They differ in what triggers the work, where Claude runs, and how much you need to set up.

|                                                | Trigger                                                                                        | Claude runs on                                                                                                   | Setup                                                                                                                                | Best for                                                      |
| :--------------------------------------------- | :--------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------ |
| [Dispatch](/en/desktop#sessions-from-dispatch) | Message a task from the Claude mobile app                                                      | Your machine (Desktop)                                                                                           | [Pair the mobile app with Desktop](https://support.claude.com/en/articles/13947068)                                                  | Delegating work while you're away, minimal setup              |
| [Remote Control](/en/remote-control)           | Drive a running session from [claude.ai/code](https://claude.ai/code) or the Claude mobile app | Your machine (CLI or VS Code)                                                                                    | Run `claude remote-control`                                                                                                          | Steering in-progress work from another device                 |
| [Channels](/en/channels)                       | Push events from a chat app like Telegram or Discord, or your own server                       | Your machine (CLI)                                                                                               | [Install a channel plugin](/en/channels#quickstart) or [build your own](/en/channels-reference)                                      | Reacting to external events like CI failures or chat messages |
| [Slack](/en/slack)                             | Mention `@Claude` in a team channel                                                            | Anthropic cloud                                                                                                  | [Install the Slack app](/en/slack#setting-up-claude-code-in-slack) with [Claude Code on the web](/en/claude-code-on-the-web) enabled | PRs and reviews from team chat                                |
| [Scheduled tasks](/en/scheduled-tasks)         | Set a schedule                                                                                 | [CLI](/en/scheduled-tasks), [Desktop](/en/desktop#schedule-recurring-tasks), or [cloud](/en/web-scheduled-tasks) | Pick a frequency                                                                                                                     | Recurring automation like daily reviews                       |

## Ressources connexes

* [Claude Code sur le web](/fr/claude-code-on-the-web) : exécutez des sessions dans des environnements cloud gérés par Anthropic au lieu de sur votre machine
* [Canaux](/fr/channels) : transférez Telegram ou Discord dans une session afin que Claude réagisse aux messages pendant que vous êtes absent
* [Dispatch](/fr/desktop#sessions-from-dispatch) : envoyez un message avec une tâche depuis votre téléphone et il peut générer une session Desktop pour la gérer
* [Authentification](/fr/authentication) : configurez `/login` et gérez les identifiants pour claude.ai
* [Référence CLI](/fr/cli-reference) : liste complète des drapeaux et commandes incluant `claude remote-control`
* [Sécurité](/fr/security) : comment les sessions Remote Control s'intègrent dans le modèle de sécurité Claude Code
* [Utilisation des données](/fr/data-usage) : quelles données circulent via l'API Anthropic lors des sessions locales et distantes
