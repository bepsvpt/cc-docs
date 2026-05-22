> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurer l'outil Bash en sandbox

> Découvrez comment l'outil Bash en sandbox de Claude Code fournit une isolation du système de fichiers et du réseau pour une exécution d'agent plus sûre et plus autonome.

Le sandbox Bash permet à Claude d'exécuter la plupart des commandes shell sans s'arrêter pour demander une permission. Au lieu d'approuver chaque commande, vous définissez quels fichiers et domaines réseau les commandes peuvent toucher, et le système d'exploitation applique cette limite pour chaque commande Bash et ses processus enfants.

Cette page couvre comment :

* [Activer le sandbox](#get-started) et choisir comment les commandes sandboxées sont approuvées
* [Configurer](#configure-sandboxing) quels chemins et domaines réseau les commandes peuvent atteindre
* [Combiner le sandboxing avec les règles de permission et les modes de permission](#how-sandboxing-relates-to-permissions-and-permission-modes)
* [Appliquer le sandboxing dans toute une organisation](#configure-the-sandbox-for-your-organization) avec les paramètres gérés

<Note>
  Pour comparer d'autres approches d'isolation telles que les dev containers, les conteneurs personnalisés et les machines virtuelles, consultez [Environnements sandbox](/fr/sandbox-environments). Pour réduire les invites de permission pour les outils autres que Bash, consultez [modes de permission](/fr/permission-modes).
</Note>

## Démarrage

Le sandbox est intégré à Claude Code et s'exécute sur macOS, Linux et WSL2. Windows natif n'est pas supporté. Sur Windows, exécutez Claude Code à l'intérieur d'une distribution WSL2.

Sur macOS, il n'y a rien à installer : le sandboxing utilise le framework Seatbelt intégré. Sur Linux et WSL2, le sandbox dépend de deux packages, couverts dans [Configurer Linux et WSL2](#set-up-linux-and-wsl2). Même si vous ne les avez pas encore installés, vous pouvez commencer avec `/sandbox`, car son panneau montre si quelque chose manque.

<Steps>
  <Step title="Exécuter /sandbox">
    Démarrez une session Claude Code et exécutez la commande `/sandbox` :

    ```text theme={null}
    /sandbox
    ```

    Cela ouvre le panneau sandbox avec trois onglets :

    * **Mode** : choisissez comment les commandes sandboxées sont approuvées, couvert à l'étape suivante
    * **Overrides** : choisissez si les commandes qui échouent sous le sandbox peuvent revenir à une exécution non sandboxée. C'est le paramètre [`allowUnsandboxedCommands`](/fr/settings#sandbox-settings)
    * **Config** : affichage les paramètres de sandbox résolus

    Si le panneau affiche uniquement un onglet Dependencies, un package requis manque. Installez-le comme décrit dans [Configurer Linux et WSL2](#set-up-linux-and-wsl2), redémarrez Claude Code et exécutez `/sandbox` à nouveau.
  </Step>

  <Step title="Choisir un mode">
    Sur l'onglet Mode, sélectionnez auto-allow ou permissions régulières. Auto-allow exécute les commandes sandboxées sans invite, et les permissions régulières conservent les invites de permission régulières même lorsque les commandes sont sandboxées. Consultez [Modes sandbox](#sandbox-modes) pour voir quelles commandes invitent toujours en mode auto-allow.
  </Step>

  <Step title="Exécuter une commande Bash">
    Demandez à Claude d'exécuter une commande, comme une compilation ou une suite de tests. Par défaut, les commandes à l'intérieur du sandbox ne peuvent écrire que dans le répertoire de travail. La première fois qu'une commande a besoin d'un nouveau domaine réseau, Claude Code demande une approbation.

    Les commandes qui ne peuvent pas s'exécuter sandboxées reviennent au flux de permission régulier. Pour élargir ou réduire ces limites, consultez [Configurer le sandboxing](#configure-sandboxing).
  </Step>
</Steps>

La sélection d'un mode dans le panneau écrit dans les paramètres locaux de votre projet à `.claude/settings.local.json`, qui s'appliquent au projet actuel et ne sont pas vérifiés dans git. Pour activer le sandbox dans tous vos projets, définissez [`sandbox.enabled`](/fr/settings#sandbox-settings) sur `true` dans vos paramètres utilisateur à `~/.claude/settings.json`. Pour appliquer le sandboxing pour chaque développeur dans une organisation, utilisez [paramètres gérés](#enforce-sandboxing-with-managed-settings).

<Warning>
  Par défaut, si le sandbox ne peut pas démarrer parce que les dépendances manquent ou que la plateforme n'est pas supportée, Claude Code affiche un avertissement et exécute les commandes sans sandboxing. Pour en faire un échec dur à la place, définissez [`sandbox.failIfUnavailable`](/fr/settings#sandbox-settings) sur `true`. Ceci est destiné aux déploiements gérés qui nécessitent le sandboxing comme porte de sécurité.
</Warning>

### Configurer Linux et WSL2

Sur Linux et WSL2, le sandbox dépend de deux packages :

* [`bubblewrap`](https://github.com/containers/bubblewrap) : l'outil de sandboxing sans privilèges qui applique l'isolation du système de fichiers
* [`socat`](http://www.dest-unreach.org/socat/) : le relais utilisé pour acheminer le trafic réseau via le proxy sandbox

Installez-les avec le gestionnaire de packages de votre distribution :

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

Après l'installation, l'onglet Dependencies dans `/sandbox` montre si `ripgrep`, `bubblewrap`, `socat` et le filtre seccomp sont disponibles sur votre plateforme. Ripgrep est fourni avec le binaire natif Claude Code. Le filtre seccomp est optionnel et ajoute le blocage des sockets de domaine Unix. Installez-le avec `npm install -g @anthropic-ai/sandbox-runtime` s'il manque.

Lorsqu'une dépendance requise manque, l'onglet Dependencies est le seul onglet affiché jusqu'à ce que vous l'installiez. La vérification des dépendances s'exécute au démarrage, donc redémarrez Claude Code après l'installation des packages pour que `/sandbox` les détecte.

<AccordionGroup>
  <Accordion title="Ubuntu 24.04 et versions ultérieures : autoriser bubblewrap à créer des espaces de noms utilisateur">
    Sur Ubuntu 24.04 et versions ultérieures, la politique AppArmor par défaut empêche bubblewrap de créer les espaces de noms utilisateur dont il a besoin pour l'isolation.

    Pour vérifier si votre environnement applique cette restriction, y compris à l'intérieur de WSL2, exécutez `sysctl kernel.apparmor_restrict_unprivileged_userns`. Si la clé n'existe pas ou retourne `0`, ignorez cette étape. Si elle retourne `1`, ajoutez un profil AppArmor qui accorde à `bwrap` cette capacité :

    ```bash theme={null}
    sudo tee /etc/apparmor.d/bwrap > /dev/null <<'EOF'
    abi <abi/4.0>,
    include <tunables/global>

    profile bwrap /usr/bin/bwrap flags=(unconfined) {
      userns,
      include if exists <local/bwrap>
    }
    EOF
    ```

    Le profil s'applique uniquement à `bwrap` lui-même, pas aux commandes qu'il exécute à l'intérieur du sandbox. Rechargez AppArmor pour l'appliquer :

    ```bash theme={null}
    sudo systemctl reload apparmor
    ```
  </Accordion>

  <Accordion title="Notes WSL2">
    Vérifiez votre version WSL avec `wsl -l -v` à partir de PowerShell. Si vous voyez `Sandboxing requires WSL2`, votre distribution exécute WSL1. Mettez-la à niveau vers WSL2 ou exécutez Claude Code sans sandboxing.

    Sur WSL2, les commandes sandboxées ne peuvent pas lancer les binaires Windows tels que `cmd.exe`, `powershell.exe`, ou quoi que ce soit sous `/mnt/c/`. WSL les transmet à l'hôte Windows via un socket Unix, que le sandbox bloque. Si une commande doit invoquer un binaire Windows, ajoutez-la à [`excludedCommands`](/fr/settings#sandbox-settings) pour qu'elle s'exécute en dehors du sandbox.
  </Accordion>
</AccordionGroup>

### Modes sandbox

Claude Code offre deux modes sandbox :

**Mode auto-allow** : Les commandes Bash tenteront de s'exécuter à l'intérieur du sandbox et sont automatiquement autorisées sans nécessiter de permission. Les commandes qui ne peuvent pas être sandboxées, comme celles nécessitant un accès réseau à des hôtes non autorisés, reviennent au flux de permission régulier, où Claude Code vérifie vos [règles de permission](/fr/permissions) et vous demande pour toute commande que ces règles n'autorisent pas déjà.

Même en mode auto-allow, les éléments suivants s'appliquent toujours :

* Les [règles de refus](/fr/permissions) explicites sont toujours respectées
* Les commandes `rm` ou `rmdir` qui ciblent `/`, votre répertoire personnel ou d'autres chemins système critiques déclenchent toujours une invite de permission
* Les [règles Ask](/fr/permissions) s'appliquent aux commandes qui reviennent au flux de permission régulier

**Mode permissions régulières** : Toutes les commandes Bash passent par le flux de permission régulier, même lorsqu'elles sont sandboxées. Cela offre plus de contrôle mais nécessite plus d'approbations.

Dans les deux modes, le sandbox applique les mêmes restrictions de système de fichiers et de réseau. La différence réside uniquement dans le fait que les commandes sandboxées sont auto-approuvées ou nécessitent une permission explicite.

Certaines commandes ne peuvent pas s'exécuter à l'intérieur du sandbox du tout, comme les outils qui sont incompatibles avec lui ou qui ont besoin d'un hôte que vous n'avez pas autorisé. Plutôt que d'échouer la tâche ou de vous demander d'éteindre le sandboxing, Claude Code inclut une trappe d'échappement : lorsqu'une commande échoue en raison des restrictions du sandbox, Claude analyse l'échec et peut réessayer la commande avec le paramètre `dangerouslyDisableSandbox`. La commande réessayée s'exécute en dehors du sandbox, elle passe donc par le flux de permission régulier et nécessite votre approbation.

Vous pouvez désactiver cette trappe d'échappement en définissant `"allowUnsandboxedCommands": false` dans vos [paramètres de sandbox](/fr/settings#sandbox-settings). Lorsqu'elle est désactivée, ce que l'onglet Overrides de `/sandbox` affiche comme **Mode sandbox strict**, le paramètre `dangerouslyDisableSandbox` est complètement ignoré et toutes les commandes doivent s'exécuter sandboxées ou être explicitement listées dans `excludedCommands`.

<Info>
  Le mode auto-allow fonctionne indépendamment de votre paramètre de mode de permission. Même si vous n'êtes pas en mode « accepter les modifications », les commandes Bash sandboxées s'exécuteront automatiquement lorsque l'auto-allow est activé. Cela signifie que les commandes Bash qui modifient les fichiers dans les limites du sandbox s'exécuteront sans invite, même lorsque les outils de modification de fichiers nécessiteraient normalement une approbation.
</Info>

## Configurer le sandboxing

Personnalisez le comportement du sandbox via votre fichier `settings.json`. Consultez [Paramètres](/fr/settings#sandbox-settings) pour la référence de configuration complète.

Par défaut, les commandes sandboxées ne peuvent écrire que dans le répertoire de travail actuel. Si les commandes de sous-processus comme `kubectl`, `terraform` ou `npm` doivent écrire en dehors du répertoire du projet, utilisez `sandbox.filesystem.allowWrite` pour accorder l'accès à des chemins spécifiques :

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowWrite": ["~/.kube", "/tmp/build"]
    }
  }
}
```

Ces chemins sont appliqués au niveau du système d'exploitation, donc toutes les commandes s'exécutant à l'intérieur du sandbox, y compris leurs processus enfants, les respectent. C'est l'approche recommandée lorsqu'un outil a besoin d'un accès en écriture à un emplacement spécifique, plutôt que d'exclure complètement l'outil du sandbox avec `excludedCommands`.

Lorsque le même tableau de système de fichiers est défini dans plusieurs [portées de paramètres](/fr/settings#settings-precedence), les tableaux sont fusionnés : les chemins de chaque portée sont combinés, non remplacés.

Les préfixes de chemin contrôlent la façon dont les chemins sont résolus :

| Préfixe                | Signification                                                                                                 | Exemple                                                                      |
| :--------------------- | :------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------- |
| `/`                    | Chemin absolu à partir de la racine du système de fichiers                                                    | `/tmp/build` reste `/tmp/build`                                              |
| `~/`                   | Relatif au répertoire personnel                                                                               | `~/.kube` devient `$HOME/.kube`                                              |
| `./` ou pas de préfixe | Relatif à la racine du projet pour les paramètres du projet, ou à `~/.claude` pour les paramètres utilisateur | `./output` dans `.claude/settings.json` se résout en `<project-root>/output` |

Cette syntaxe diffère des [règles de permission Read et Edit](/fr/permissions#read-and-edit), qui utilisent `//path` pour absolu et `/path` pour relatif au projet. Les chemins du système de fichiers du sandbox utilisent les conventions standard : `/tmp/build` est absolu.

Vous pouvez également refuser l'accès en écriture ou en lecture en utilisant `sandbox.filesystem.denyWrite` et `sandbox.filesystem.denyRead`, et réautoriser des chemins spécifiques dans une région refusée en utilisant `sandbox.filesystem.allowRead`.

L'exemple ci-dessous bloque la lecture de l'ensemble du répertoire personnel tout en autorisant toujours les lectures du projet actuel. Placez-le dans le `.claude/settings.json` de votre projet, car le chemin relatif `.` se résout à la racine du projet uniquement lorsque la configuration se trouve dans les paramètres du projet :

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["."]
    }
  }
}
```

Le `.` dans `allowRead` se résout à la racine du projet car cette configuration se trouve dans les paramètres du projet. Si vous aviez placé la même configuration dans `~/.claude/settings.json`, `.` se résoudrait à `~/.claude` à la place, et les fichiers du projet resteraient bloqués par la règle `denyRead`.

## Comment fonctionne le sandboxing

### Isolation du système de fichiers

L'outil Bash en sandbox restreint l'accès au système de fichiers à des répertoires spécifiques :

* **Comportement d'écriture par défaut** : accès en lecture et écriture au répertoire de travail actuel et à ses sous-répertoires
* **Comportement de lecture par défaut** : accès en lecture à l'ensemble de l'ordinateur, sauf certains répertoires refusés. Notez que ce comportement par défaut permet toujours de lire les fichiers d'identifiants tels que `~/.aws/credentials` et `~/.ssh/`. Ajoutez-les à `denyRead` pour les bloquer.
* **Accès bloqué** : impossible de modifier les fichiers en dehors du répertoire de travail actuel sans permission explicite, y compris les fichiers de configuration shell tels que `~/.bashrc` et les binaires système dans `/bin/`
* **Configurable** : définissez des chemins autorisés et refusés personnalisés via les paramètres

Vous pouvez accorder l'accès en écriture à des chemins supplémentaires en utilisant `sandbox.filesystem.allowWrite` dans vos paramètres. Ces restrictions sont appliquées au niveau du système d'exploitation, elles s'appliquent donc à toutes les commandes de sous-processus, y compris les outils comme `kubectl`, `terraform` et `npm`, pas seulement aux outils de fichiers de Claude.

### Isolation réseau

L'accès réseau est contrôlé via un serveur proxy s'exécutant en dehors du sandbox :

* **Restrictions de domaine** : aucun domaine n'est pré-autorisé. La première fois qu'une commande a besoin d'un nouveau domaine, Claude Code demande une approbation. Pré-autorisez les domaines avec [`allowedDomains`](/fr/settings#sandbox-settings) pour éviter l'invite.
* **Verrouillage géré** : si [`allowManagedDomainsOnly`](/fr/settings#sandbox-settings) est défini dans les paramètres gérés, les domaines non autorisés sont bloqués automatiquement au lieu de demander, et seuls les `allowedDomains` des paramètres gérés sont honorés.
* **Support de proxy personnalisé** : les utilisateurs avancés peuvent implémenter des règles personnalisées sur le trafic sortant
* **Couverture complète** : les restrictions s'appliquent à tous les scripts, programmes et sous-processus générés par les commandes

<Note>
  Le proxy intégré applique la liste d'autorisation en fonction du nom d'hôte demandé et ne termine pas ou n'inspecte pas le trafic TLS. Consultez [Limitations de sécurité](#security-limitations) pour les implications de cette conception, et [Configuration de proxy personnalisée](#custom-proxy-configuration) si votre modèle de menace nécessite l'inspection TLS.
</Note>

### Application au niveau du système d'exploitation

L'outil Bash en sandbox exploite les primitives de sécurité du système d'exploitation :

* **macOS** : utilise Seatbelt pour l'application du sandbox
* **Linux** : utilise [bubblewrap](https://github.com/containers/bubblewrap) pour l'isolation
* **WSL2** : utilise bubblewrap, comme Linux

WSL1 n'est pas supporté car bubblewrap nécessite des fonctionnalités du noyau uniquement disponibles dans WSL2. Ces restrictions au niveau du système d'exploitation garantissent que tous les processus enfants générés par les commandes de Claude Code héritent des mêmes limites de sécurité.

Ces mêmes primitives sont disponibles en tant que package autonome [`@anthropic-ai/sandbox-runtime`](https://github.com/anthropic-experimental/sandbox-runtime), que la page [Environnements sandbox](/fr/sandbox-environments#sandbox-runtime) couvre comme une approche distincte pour envelopper l'ensemble du processus Claude Code.

## Comment le sandboxing se rapporte aux permissions et aux modes de permission

Le sandboxing, les [règles de permission](/fr/permissions) et les [modes de permission](/fr/permission-modes) sont des couches complémentaires. Les sections ci-dessous couvrent comment le sandbox interagit avec chacun.

### Règles de permission

Les règles de permission et le sandboxing contrôlent des choses différentes :

* **Les règles de permission** contrôlent quels outils Claude Code peut utiliser et sont évaluées avant l'exécution de tout outil. Elles s'appliquent à tous les outils : Bash, Read, Edit, WebFetch, MCP et autres.
* **Le sandboxing** fournit une application au niveau du système d'exploitation qui restreint ce que les commandes Bash peuvent accéder au niveau du système de fichiers et du réseau. Il s'applique uniquement aux commandes Bash et à leurs processus enfants.

Les deux couches diffèrent également dans la façon dont elles sont appliquées. Claude Code évalue les décisions de permission avant l'exécution d'une commande, en fonction de la chaîne de commande et, en mode auto, du jugement d'un classificateur distinct sur la sécurité de la commande. Le système d'exploitation applique la limite du sandbox sur le processus en cours d'exécution, elle tient donc indépendamment de ce que le modèle a choisi d'exécuter et même si une commande autorisée fait plus que son nom ne le suggère.

Les restrictions du système de fichiers et du réseau sont configurées via les paramètres de sandbox et les règles de permission :

| Paramètre ou règle                                              | Ce qu'il fait                                                                                                   |
| :-------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------- |
| `sandbox.filesystem.allowWrite`                                 | Accorde l'accès en écriture des sous-processus à des chemins en dehors du répertoire de travail                 |
| `sandbox.filesystem.denyWrite` et `sandbox.filesystem.denyRead` | Bloque l'accès des sous-processus à des chemins spécifiques                                                     |
| `sandbox.filesystem.allowRead`                                  | Réautorise la lecture de chemins spécifiques dans une région `denyRead`                                         |
| Règles d'autorisation `Edit`                                    | Accordent l'accès en écriture à des chemins spécifiques, de la même manière que `sandbox.filesystem.allowWrite` |
| Règles de refus `Read` et `Edit`                                | Bloquent l'accès à des fichiers ou répertoires spécifiques                                                      |
| Règles d'autorisation et de refus `WebFetch`                    | Contrôlent l'accès au domaine                                                                                   |
| `allowedDomains` du sandbox                                     | Contrôle quels domaines les commandes Bash peuvent atteindre                                                    |
| `deniedDomains` du sandbox                                      | Bloque des domaines spécifiques même lorsqu'un wildcard `allowedDomains` plus large les autoriserait autrement  |

Les chemins des paramètres `sandbox.filesystem` et des règles de permission sont fusionnés dans la configuration finale du sandbox.

Le [répertoire d'exemples du référentiel claude-code](https://github.com/anthropics/claude-code/tree/main/examples/settings) inclut des configurations de paramètres de démarrage pour les scénarios de déploiement courants, y compris des exemples spécifiques au sandbox. Utilisez-les comme points de départ et ajustez-les selon vos besoins.

### Modes de permission

`/sandbox` n'est pas un [mode de permission](/fr/permission-modes). Les modes de permission décident si un appel d'outil s'exécute et si vous êtes invité en premier, tandis que le sandbox restreint ce qu'une commande Bash peut accéder une fois qu'elle s'exécute. Ils diffèrent dans ce qu'ils contrôlent et ce qui remplace l'invite par action :

|                                                                    | Ce qu'il contrôle                                               | Ce qui remplace l'invite                                                                                                                                                            |
| :----------------------------------------------------------------- | :-------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/sandbox`                                                         | Ce qu'une commande Bash peut accéder une fois qu'elle s'exécute | La limite du sandbox elle-même, en [mode auto-allow](#sandbox-modes)                                                                                                                |
| [Mode auto](/fr/permission-modes#eliminate-prompts-with-auto-mode) | Si chaque appel d'outil s'exécute                               | Un classificateur qui examine les actions                                                                                                                                           |
| `--dangerously-skip-permissions`                                   | Si chaque appel d'outil s'exécute                               | Rien. Les vérifications de [chemin protégé](/fr/permission-modes#protected-paths) sont également ignorées ; seul le retrait de `/` ou de votre répertoire personnel invite toujours |

Le [mode auto-allow](#sandbox-modes) du sandbox est distinct du [mode auto](/fr/permission-modes#eliminate-prompts-with-auto-mode) : l'auto-allow approuve les commandes Bash parce que la limite du sandbox les contient, tandis que le mode auto utilise un classificateur pour examiner les actions. Les deux fonctionnent indépendamment et peuvent être combinés. Pour choisir une limite d'isolation pour les exécutions sans surveillance, consultez [Environnements sandbox](/fr/sandbox-environments#how-isolation-relates-to-permission-modes).

## Configurer le sandbox pour votre organisation

Les administrateurs peuvent exiger le sandboxing pour chaque utilisateur, empêcher les développeurs d'élargir la politique et acheminer le trafic sandbox via un proxy d'entreprise.

### Appliquer le sandboxing avec les paramètres gérés

Pour exiger le sandbox pour chaque développeur, livrez les clés `sandbox` via [paramètres gérés](/fr/settings#settings-files), soit en tant que fichier géré par votre MDM, soit via [paramètres gérés par serveur](/fr/server-managed-settings) sur Claude.ai.

La configuration de paramètres gérés suivante active le sandbox, refuse de démarrer Claude Code si le sandbox ne peut pas s'initialiser et empêche le modèle de réessayer les commandes en dehors du sandbox :

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true,
    "allowUnsandboxedCommands": false
  }
}
```

Les deux clés au-delà de `enabled` contrôlent ce qui se passe lorsque le sandbox ne peut pas exécuter une commande :

* **`failIfUnavailable`** : une dépendance manquante telle que bubblewrap sur Linux empêche Claude Code de démarrer plutôt que d'afficher un avertissement et de revenir à une exécution non sandboxée
* **`allowUnsandboxedCommands: false`** : la trappe d'échappement `dangerouslyDisableSandbox` est ignorée, les commandes qui échouent sous le sandbox ne peuvent donc pas être réessayées en dehors de celui-ci

Deux ajouts valent la peine d'être envisagés aux côtés d'eux. Ajoutez `excludedCommands` pour tous les outils approuvés par l'organisation qui doivent s'exécuter sans isolation. Ajoutez des entrées [`denyRead`](#filesystem-isolation) pour les répertoires d'identifiants tels que `~/.aws` et `~/.ssh`, que la politique de lecture par défaut autorise toujours.

Le sandbox ne s'exécute pas sur Windows natif, donc si votre flotte inclut des hôtes Windows, limitez cette configuration à macOS et Linux ou demandez à ces utilisateurs d'exécuter Claude Code à l'intérieur de WSL2 ou d'un conteneur.

### Empêcher les développeurs d'élargir la politique

Pour les clés booléennes telles que `enabled` et `failIfUnavailable`, Claude Code utilise la valeur gérée et ignore tout ce qu'un développeur définit localement. Pour les clés de tableau telles que `excludedCommands` et `allowRead`, Claude Code fusionne les entrées de chaque portée, un développeur peut donc ajouter des entrées qui élargissent la politique.

Définissez `allowManagedReadPathsOnly` sur `true` dans les paramètres gérés pour que seules les entrées `allowRead` des paramètres gérés soient honorées. Les entrées `allowRead` utilisateur, projet et local sont ignorées. Cela empêche les développeurs d'élargir l'accès en lecture au-delà des chemins approuvés par l'organisation. Pour verrouiller les domaines réseau aux valeurs gérées de la même manière, définissez [`allowManagedDomainsOnly`](/fr/settings#sandbox-settings).

`excludedCommands` n'a pas d'équivalent de verrouillage géré uniquement, un développeur peut donc toujours ajouter des entrées qui exécutent des commandes supplémentaires en dehors du sandbox. Gardez la liste gérée étroite.

### Configuration de proxy personnalisée

Pour les organisations nécessitant une sécurité réseau avancée, vous pouvez implémenter un proxy personnalisé pour :

* Déchiffrer et inspecter le trafic HTTPS
* Appliquer des règles de filtrage personnalisées
* Enregistrer toutes les demandes réseau
* Intégrer avec l'infrastructure de sécurité existante

Pour pointer Claude Code vers votre proxy, définissez les ports proxy dans [paramètres de sandbox](/fr/settings#sandbox-settings) :

```json theme={null}
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

## Dépannage

Certaines commandes échouent à l'intérieur du sandbox même si elles fonctionnent en dehors. Les correctifs ci-dessous couvrent les cas les plus courants.

* **Les commandes échouent avec une erreur host-not-allowed** : de nombreux outils CLI doivent atteindre des hôtes spécifiques. Accorder la permission lorsque vous y êtes invité ajoute l'hôte à votre liste autorisée pour que l'outil s'exécute à l'intérieur du sandbox à l'avenir.
* **`jest` se bloque ou échoue** : `watchman` est incompatible avec le sandbox. Exécutez `jest --no-watchman` à la place.
* **Les CLI basés sur Go échouent la vérification TLS sur macOS** : les outils tels que `gh`, `gcloud` et `terraform` peuvent échouer la vérification TLS sous Seatbelt. Listez ces outils dans `excludedCommands` pour les exécuter en dehors du sandbox. Si vous utilisez `httpProxyPort` avec un proxy MITM et une CA personnalisée, définissez [`enableWeakerNetworkIsolation`](/fr/settings#sandbox-settings) sur `true` à la place.
* **Les commandes `docker` échouent** : `docker` est incompatible avec le sandbox. Ajoutez `docker *` à `excludedCommands` pour l'exécuter en dehors du sandbox.
* **Bubblewrap échoue à démarrer à l'intérieur d'un conteneur** : dans un conteneur sans privilèges, bubblewrap ne peut pas monter un système de fichiers `/proc` frais. Définissez [`enableWeakerNestedSandbox`](/fr/settings#sandbox-settings) sur `true` pour que le sandbox interne bind-monte le `/proc` existant du conteneur à la place. Utilisez ce paramètre uniquement lorsque le conteneur externe fournit déjà la limite d'isolation dont vous avez besoin, car il expose les informations de processus aux commandes sandboxées qu'un montage `/proc` frais cacherait.
* **Filtre seccomp sur Linux** : le filtre seccomp est requis pour bloquer les sockets de domaine Unix. L'onglet Dependencies dans `/sandbox` montre s'il est disponible. S'il manque, exécutez `npm install -g @anthropic-ai/sandbox-runtime` pour installer l'assistant.
* **`--dangerously-skip-permissions` échoue en tant que root** : cet indicateur est bloqué lors de l'exécution en tant que root ou via sudo sur Linux et macOS, car l'accès root combiné à aucune invite de permission peut modifier n'importe quel fichier ou service sur le système. La vérification est ignorée automatiquement à l'intérieur d'un sandbox reconnu. Pour exécuter de manière autonome dans un conteneur, utilisez la configuration [dev container](/fr/devcontainer), qui exécute Claude Code en tant qu'utilisateur non-root.

## Limitations

Le sandboxing réduit le risque mais n'est pas une limite d'isolation complète. Examinez les limitations ci-dessous avant de vous y fier comme contrôle de sécurité dur.

### Limitations de sécurité

* **Filtrage réseau** : le système de filtrage réseau fonctionne en restreignant les domaines auxquels les processus sont autorisés à se connecter. Le proxy intégré ne termine pas ou n'effectue pas l'inspection TLS sur le trafic sortant, le contenu des connexions chiffrées n'est donc pas examiné. Vous êtes responsable de vous assurer que seuls les domaines de confiance sont autorisés dans votre politique.

<Warning>
  Autoriser des domaines larges tels que `github.com` peut créer des chemins pour l'exfiltration de données. Parce que le proxy prend sa décision d'autorisation à partir du nom d'hôte fourni par le client sans inspecter TLS, le code s'exécutant à l'intérieur du sandbox peut potentiellement utiliser [domain fronting](https://en.wikipedia.org/wiki/Domain_fronting) ou des techniques similaires pour atteindre des hôtes en dehors de la liste d'autorisation. Si votre modèle de menace nécessite des garanties plus fortes, configurez un [proxy personnalisé](#custom-proxy-configuration) qui termine TLS et inspecte le trafic, et installez son certificat CA à l'intérieur du sandbox. L'isolation réseau plus forte consciente de TLS est un domaine actif de développement.
</Warning>

* **Escalade de privilèges via les sockets de domaine Unix** : la configuration `allowUnixSockets` peut accorder involontairement l'accès à des services système puissants qui pourraient entraîner des contournements du sandbox. Par exemple, autoriser l'accès à `/var/run/docker.sock` accorde effectivement l'accès au système hôte via le socket Docker. Considérez attentivement tous les sockets Unix que vous autorisez via le sandbox.
* **Escalade de permissions du système de fichiers** : les permissions d'écriture du système de fichiers trop larges peuvent permettre des attaques d'escalade de privilèges. Autoriser les écritures dans les répertoires contenant des exécutables dans `$PATH`, les répertoires de configuration système ou les fichiers de configuration shell utilisateur tels que `.bashrc` ou `.zshrc` peut entraîner l'exécution de code dans différents contextes de sécurité lorsque d'autres utilisateurs ou processus système accèdent à ces fichiers.
* **Force du sandbox Linux** : l'implémentation Linux fournit une isolation forte du système de fichiers et du réseau mais inclut un mode `enableWeakerNestedSandbox` qui lui permet de fonctionner à l'intérieur des environnements Docker sans espaces de noms privilégiés, ou sur les hôtes Linux où les espaces de noms utilisateur sans privilèges sont désactivés par sysctl. Cette option affaiblit considérablement la sécurité et ne doit être utilisée que lorsqu'une isolation supplémentaire est autrement appliquée.
* **Fichiers de paramètres protégés** : le sandbox refuse automatiquement l'accès en écriture aux fichiers `settings.json` de Claude Code à chaque portée et au répertoire des paramètres gérés, une commande sandboxée ne peut donc pas modifier sa propre politique.

### Compatibilité de plateforme et d'outil

* **Support de plateforme** : supporte macOS, Linux et WSL2. WSL1 et Windows natif ne sont pas supportés.
* **Surcharge de performance** : minimale, mais certaines opérations du système de fichiers peuvent être légèrement plus lentes.
* **Compatibilité d'outil** : certains outils qui nécessitent des modèles d'accès système spécifiques peuvent nécessiter des ajustements de configuration, ou peuvent avoir besoin d'être exécutés en dehors du sandbox.

### Portée

Le sandbox isole les sous-processus Bash. Les autres outils fonctionnent sous des limites différentes :

* **Outils de fichiers intégrés** : Read, Edit et Write utilisent le système de permissions directement plutôt que de s'exécuter via le sandbox. Consultez [permissions](/fr/permissions).
* **Utilisation de l'ordinateur** : lorsque Claude ouvre des applications et contrôle votre écran, il s'exécute sur votre bureau réel plutôt que dans un environnement isolé. Les invites de permission par application contrôlent chaque application. Consultez [utilisation de l'ordinateur dans la CLI](/fr/computer-use) ou [utilisation de l'ordinateur dans Desktop](/fr/desktop#let-claude-use-your-computer).
* **Variables d'environnement** : les commandes Bash sandboxées héritent de l'environnement du processus parent par défaut, y compris les identifiants définis là-bas. Pour supprimer les identifiants Anthropic et du fournisseur cloud des sous-processus, définissez [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](/fr/env-vars).
* **Sous-agents** : les [sous-agents](/fr/sub-agents) s'exécutent dans le même processus que la session parent et utilisent la même configuration de sandbox. Les commandes Bash à l'intérieur d'un sous-agent sont sandboxées lorsque le sandboxing est activé dans la session parent.

<Warning>
  Un sandboxing efficace nécessite **à la fois** l'isolation du système de fichiers et du réseau. Sans isolation réseau, un agent compromis pourrait exfiltrer des fichiers sensibles comme les clés SSH. Sans isolation du système de fichiers, un agent compromis pourrait installer une porte dérobée sur les ressources système pour accéder au réseau. Lorsque vous élargissez les valeurs par défaut, vérifiez qu'un chemin `allowWrite`, une entrée `allowedDomains` large ou une exception `excludedCommands` ne défait pas une restriction de l'autre côté.
</Warning>

## Voir aussi

* [Environnements sandbox](/fr/sandbox-environments) : comparez le sandbox intégré avec les dev containers, les conteneurs et les machines virtuelles
* [Sécurité](/fr/security) : fonctionnalités de sécurité complètes et meilleures pratiques
* [Permissions](/fr/permissions) : configuration des permissions et contrôle d'accès
* [Paramètres](/fr/settings) : référence de configuration complète
* [Référence CLI](/fr/cli-reference) : options de ligne de commande
