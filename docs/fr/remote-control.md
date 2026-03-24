> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Continuer les sessions locales depuis n'importe quel appareil avec Remote Control

> Continuez une session Claude Code locale depuis votre téléphone, tablette ou n'importe quel navigateur en utilisant Remote Control. Fonctionne avec claude.ai/code et l'application Claude mobile.

<Note>
  Remote Control est disponible sur tous les plans. Les administrateurs Team et Enterprise doivent d'abord activer Claude Code dans les [paramètres d'administration](https://claude.ai/admin-settings/claude-code).
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

* **Abonnement** : disponible sur les plans Pro, Max, Team et Enterprise. Les administrateurs Team et Enterprise doivent d'abord activer Claude Code dans les [paramètres d'administration](https://claude.ai/admin-settings/claude-code). Les clés API ne sont pas prises en charge.
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

La session distante prend son nom à partir de l'argument `--name` (ou du nom passé à `/remote-control`), votre dernier message, votre valeur `/rename`, ou « Remote Control session » s'il n'y a pas d'historique de conversation. Si l'environnement a déjà une session active, vous serez invité à choisir si vous souhaitez la continuer ou en démarrer une nouvelle.

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

## Ressources connexes

* [Claude Code sur le web](/fr/claude-code-on-the-web) : exécutez des sessions dans des environnements cloud gérés par Anthropic au lieu de sur votre machine
* [Authentification](/fr/authentication) : configurez `/login` et gérez les identifiants pour claude.ai
* [Référence CLI](/fr/cli-reference) : liste complète des drapeaux et commandes incluant `claude remote-control`
* [Sécurité](/fr/security) : comment les sessions Remote Control s'intègrent dans le modèle de sécurité Claude Code
* [Utilisation des données](/fr/data-usage) : quelles données circulent via l'API Anthropic lors des sessions locales et distantes
