> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Utiliser Claude Code sur le web

> Configurez les environnements cloud, les scripts de configuration, l'accès réseau et Docker dans le sandbox d'Anthropic. Déplacez les sessions entre le web et le terminal avec `--remote` et `--teleport`.

<Note>
  Claude Code sur le web est en aperçu de recherche pour les utilisateurs Pro, Max et Team, ainsi que pour les utilisateurs Enterprise disposant de sièges premium ou de sièges Chat + Claude Code.
</Note>

Claude Code sur le web exécute les tâches sur l'infrastructure cloud gérée par Anthropic à [claude.ai/code](https://claude.ai/code). Les sessions persistent même si vous fermez votre navigateur, et vous pouvez les surveiller depuis l'application mobile Claude.

<Tip>
  Nouveau sur Claude Code sur le web ? Commencez par [Démarrer](/fr/web-quickstart) pour connecter votre compte GitHub et soumettre votre première tâche.
</Tip>

Cette page couvre :

* [Options d'authentification GitHub](#github-authentication-options) : deux façons de connecter GitHub
* [L'environnement cloud](#the-cloud-environment) : quelle configuration est transférée, quels outils sont installés et comment configurer les environnements
* [Scripts de configuration](#setup-scripts) et gestion des dépendances
* [Accès réseau](#network-access) : niveaux, proxies et liste d'autorisation par défaut
* [Déplacer les tâches entre le web et le terminal](#move-tasks-between-web-and-terminal) avec `--remote` et `--teleport`
* [Travailler avec les sessions](#work-with-sessions) : examiner, partager, archiver, supprimer
* [Correction automatique des demandes de tirage](#auto-fix-pull-requests) : répondre automatiquement aux défaillances CI et aux commentaires d'examen
* [Sécurité et isolation](#security-and-isolation) : comment les sessions sont isolées
* [Limitations](#limitations) : limites de débit et restrictions de plateforme

## Options d'authentification GitHub

Les sessions cloud ont besoin d'accès à vos référentiels GitHub pour cloner le code et pousser les branches. Vous pouvez accorder l'accès de deux façons :

| Méthode                | Comment ça marche                                                                                                                                                        | Idéal pour                                                         |
| :--------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------- |
| **Application GitHub** | Installez l'application Claude GitHub sur des référentiels spécifiques lors de [l'intégration web](/fr/web-quickstart). L'accès est limité par référentiel.              | Les équipes qui veulent une autorisation explicite par référentiel |
| **`/web-setup`**       | Exécutez `/web-setup` dans votre terminal pour synchroniser votre jeton CLI `gh` local vers votre compte Claude. L'accès correspond à ce que votre jeton `gh` peut voir. | Les développeurs individuels qui utilisent déjà `gh`               |

L'une ou l'autre méthode fonctionne. [`/schedule`](/fr/routines) vérifie l'une ou l'autre forme d'accès et vous invite à exécuter `/web-setup` si aucune n'est configurée. Consultez [Connecter depuis votre terminal](/fr/web-quickstart#connect-from-your-terminal) pour la procédure pas à pas de `/web-setup`.

L'application GitHub est requise pour [Auto-fix](#auto-fix-pull-requests), qui utilise l'application pour recevoir les webhooks PR. Si vous vous connectez avec `/web-setup` et souhaitez ultérieurement Auto-fix, installez l'application sur ces référentiels.

Les administrateurs Team et Enterprise peuvent désactiver `/web-setup` avec le bouton bascule Quick web setup sur [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code).

<Note>
  Les organisations avec [Zéro rétention de données](/fr/zero-data-retention) activée ne peuvent pas utiliser `/web-setup` ou d'autres fonctionnalités de session cloud.
</Note>

## L'environnement cloud

Chaque session s'exécute dans une VM fraîche gérée par Anthropic avec votre référentiel cloné. Cette section couvre ce qui est disponible au démarrage d'une session et comment la personnaliser.

### Ce qui est disponible dans les sessions cloud

Les sessions cloud commencent par un clone frais de votre référentiel. Tout ce qui est validé dans le référentiel est disponible. Tout ce que vous avez installé ou configuré uniquement sur votre propre machine ne l'est pas.

|                                                                                | Disponible dans les sessions cloud | Pourquoi                                                                                                                                                                                |
| :----------------------------------------------------------------------------- | :--------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Votre `CLAUDE.md` du référentiel                                               | Oui                                | Fait partie du clone                                                                                                                                                                    |
| Vos hooks `.claude/settings.json` du référentiel                               | Oui                                | Fait partie du clone                                                                                                                                                                    |
| Vos serveurs MCP `.mcp.json` du référentiel                                    | Oui                                | Fait partie du clone                                                                                                                                                                    |
| Votre `.claude/rules/` du référentiel                                          | Oui                                | Fait partie du clone                                                                                                                                                                    |
| Votre `.claude/skills/`, `.claude/agents/`, `.claude/commands/` du référentiel | Oui                                | Fait partie du clone                                                                                                                                                                    |
| Plugins déclarés dans `.claude/settings.json`                                  | Oui                                | Installés au démarrage de la session à partir de la [marketplace](/fr/plugin-marketplaces) que vous avez déclarée. Nécessite un accès réseau pour atteindre la source de la marketplace |
| Votre `~/.claude/CLAUDE.md` utilisateur                                        | Non                                | Vit sur votre machine, pas dans le référentiel                                                                                                                                          |
| Plugins activés uniquement dans vos paramètres utilisateur                     | Non                                | Les `enabledPlugins` limités à l'utilisateur vivent dans `~/.claude/settings.json`. Déclarez-les plutôt dans le `.claude/settings.json` du référentiel                                  |
| Serveurs MCP que vous avez ajoutés avec `claude mcp add`                       | Non                                | Ceux-ci écrivent dans votre configuration utilisateur locale, pas dans le référentiel. Déclarez le serveur dans [`.mcp.json`](/fr/mcp#project-scope) à la place                         |
| Jetons API statiques et identifiants                                           | Non                                | Aucun magasin de secrets dédié n'existe encore. Voir ci-dessous                                                                                                                         |
| Authentification interactive comme AWS SSO                                     | Non                                | Non pris en charge. SSO nécessite une connexion basée sur le navigateur qui ne peut pas s'exécuter dans une session cloud                                                               |

Pour rendre la configuration disponible dans les sessions cloud, validez-la dans le référentiel. Un magasin de secrets dédié n'est pas encore disponible. Les variables d'environnement et les scripts de configuration sont stockés dans la configuration de l'environnement, visibles à quiconque peut modifier cet environnement. Si vous avez besoin de secrets dans une session cloud, ajoutez-les comme variables d'environnement en gardant cette visibilité à l'esprit.

### Outils installés

Les sessions cloud sont livrées avec des runtimes de langage courants, des outils de construction et des bases de données pré-installés. Le tableau ci-dessous résume ce qui est inclus par catégorie.

| Catégorie            | Inclus                                                                           |
| :------------------- | :------------------------------------------------------------------------------- |
| **Python**           | Python 3.x avec pip, poetry, uv, black, mypy, pytest, ruff                       |
| **Node.js**          | 20, 21 et 22 via nvm, avec npm, yarn, pnpm, bun¹, eslint, prettier, chromedriver |
| **Ruby**             | 3.1, 3.2, 3.3 avec gem, bundler, rbenv                                           |
| **PHP**              | 8.4 avec Composer                                                                |
| **Java**             | OpenJDK 21 avec Maven et Gradle                                                  |
| **Go**               | dernière version stable avec support des modules                                 |
| **Rust**             | rustc et cargo                                                                   |
| **C/C++**            | GCC, Clang, cmake, ninja, conan                                                  |
| **Docker**           | docker, dockerd, docker compose                                                  |
| **Bases de données** | PostgreSQL 16, Redis 7.0                                                         |
| **Utilitaires**      | git, jq, yq, ripgrep, tmux, vim, nano                                            |

¹ Bun est installé mais a des [problèmes de compatibilité proxy](#install-dependencies-with-a-sessionstart-hook) connus pour la récupération de paquets.

Pour les versions exactes, demandez à Claude d'exécuter `check-tools` dans une session cloud. Cette commande n'existe que dans les sessions cloud.

### Travailler avec les problèmes et demandes de tirage GitHub

Les sessions cloud incluent des outils GitHub intégrés qui permettent à Claude de lire les problèmes, de lister les demandes de tirage, de récupérer les diffs et de publier des commentaires sans aucune configuration. Ces outils s'authentifient via le [proxy GitHub](#github-proxy) en utilisant la méthode que vous avez configurée sous [Options d'authentification GitHub](#github-authentication-options), donc votre jeton n'entre jamais dans le conteneur.

Le CLI `gh` n'est pas pré-installé. Si vous avez besoin d'une commande `gh` que les outils intégrés ne couvrent pas, comme `gh release` ou `gh workflow run`, installez et authentifiez-la vous-même :

<Steps>
  <Step title="Installer gh dans votre script de configuration">
    Ajoutez `apt update && apt install -y gh` à votre [script de configuration](#setup-scripts).
  </Step>

  <Step title="Fournir un jeton">
    Ajoutez une variable d'environnement `GH_TOKEN` à vos [paramètres d'environnement](#configure-your-environment) avec un jeton d'accès personnel GitHub. `gh` lit `GH_TOKEN` automatiquement, donc aucune étape `gh auth login` n'est nécessaire.
  </Step>
</Steps>

### Lier les artefacts à la session

Chaque session cloud a une URL de transcription sur claude.ai, et la session peut lire son propre ID à partir de la variable d'environnement `CLAUDE_CODE_REMOTE_SESSION_ID`. Utilisez ceci pour mettre un lien traçable dans les corps PR, les messages de commit, les publications Slack ou les rapports générés afin qu'un examinateur puisse ouvrir l'exécution qui les a produits.

Demandez à Claude de construire le lien à partir de la variable d'environnement. La commande suivante imprime l'URL :

```bash theme={null}
echo "https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID}"
```

### Exécuter les tests, démarrer les services et ajouter des paquets

Claude exécute les tests dans le cadre du travail sur une tâche. Demandez-le dans votre invite, comme « corriger les tests échoués dans `tests/` » ou « exécuter pytest après chaque modification ». Les exécuteurs de tests comme pytest, jest et cargo test fonctionnent directement puisqu'ils sont pré-installés.

PostgreSQL et Redis sont pré-installés mais ne s'exécutent pas par défaut. Demandez à Claude de démarrer chacun pendant la session :

```bash theme={null}
service postgresql start
```

```bash theme={null}
service redis-server start
```

Docker est disponible pour exécuter les services conteneurisés. Demandez à Claude d'exécuter `docker compose up` pour démarrer les services de votre projet. L'accès réseau pour extraire les images suit le [niveau d'accès](#access-levels) de votre environnement, et les [valeurs par défaut de confiance](#default-allowed-domains) incluent Docker Hub et d'autres registres courants.

Si vos images sont volumineuses ou lentes à extraire, ajoutez `docker compose pull` ou `docker compose build` à votre [script de configuration](#setup-scripts). Les images extraites sont sauvegardées dans l'[environnement en cache](#environment-caching), donc chaque nouvelle session les a sur le disque. Le cache stocke uniquement les fichiers, pas les processus en cours d'exécution, donc Claude démarre toujours les conteneurs à chaque session.

Pour ajouter des paquets qui ne sont pas pré-installés, utilisez un [script de configuration](#setup-scripts). La sortie du script est [mise en cache](#environment-caching), donc les paquets que vous installez là sont disponibles au démarrage de chaque session sans réinstallation à chaque fois. Vous pouvez également demander à Claude d'installer des paquets pendant la session, mais ces installations ne persistent pas entre les sessions.

### Limites de ressources

Les sessions cloud s'exécutent avec des plafonds de ressources approximatifs qui peuvent changer au fil du temps :

* 4 vCPU
* 16 Go de RAM
* 30 Go de disque

Les tâches nécessitant beaucoup plus de mémoire, comme les gros travaux de construction ou les tests gourmands en mémoire, peuvent échouer ou être terminées. Pour les charges de travail au-delà de ces limites, utilisez [Contrôle à distance](/fr/remote-control) pour exécuter Claude Code sur votre propre matériel.

### Configurer votre environnement

Les environnements contrôlent [l'accès réseau](#network-access), les variables d'environnement et le [script de configuration](#setup-scripts) qui s'exécute avant le démarrage d'une session. Consultez [Outils installés](#installed-tools) pour ce qui est disponible sans aucune configuration. Vous pouvez gérer les environnements à partir de l'interface web ou du terminal :

| Action                                       | Comment                                                                                                                                                                                                                                                                        |
| :------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Ajouter un environnement                     | Sélectionnez l'environnement actuel pour ouvrir le sélecteur, puis sélectionnez **Ajouter un environnement**. La boîte de dialogue inclut le nom, le niveau d'accès réseau, les variables d'environnement et le script de configuration.                                       |
| Modifier un environnement                    | Sélectionnez l'icône des paramètres à droite du nom de l'environnement.                                                                                                                                                                                                        |
| Archiver un environnement                    | Ouvrez l'environnement pour le modifier et sélectionnez **Archiver**. Les environnements archivés sont masqués du sélecteur mais les sessions existantes continuent de s'exécuter.                                                                                             |
| Définir la valeur par défaut pour `--remote` | Exécutez `/remote-env` dans votre terminal. Si vous avez un seul environnement, cette commande affiche votre configuration actuelle. `/remote-env` sélectionne uniquement la valeur par défaut ; ajoutez, modifiez et archivez les environnements à partir de l'interface web. |

Les variables d'environnement utilisent le format `.env` avec une paire `KEY=value` par ligne. N'enveloppez pas les valeurs entre guillemets, car les guillemets sont stockés comme faisant partie de la valeur.

```text theme={null}
NODE_ENV=development
LOG_LEVEL=debug
DATABASE_URL=postgres://localhost:5432/myapp
```

## Scripts de configuration

Un script de configuration est un script Bash qui s'exécute au démarrage d'une nouvelle session cloud, avant le lancement de Claude Code. Utilisez les scripts de configuration pour installer les dépendances, configurer les outils ou récupérer tout ce dont la session a besoin et qui n'est pas pré-installé.

Les scripts s'exécutent en tant que root sur Ubuntu 24.04, donc `apt install` et la plupart des gestionnaires de paquets de langage fonctionnent.

Pour ajouter un script de configuration, ouvrez la boîte de dialogue des paramètres d'environnement et entrez votre script dans le champ **Script de configuration**.

Cet exemple installe le CLI `gh`, qui n'est pas pré-installé :

```bash theme={null}
#!/bin/bash
apt update && apt install -y gh
```

Si le script se termine avec un code non nul, la session ne démarre pas. Ajoutez `|| true` aux commandes non critiques pour éviter de bloquer la session sur une défaillance d'installation intermittente.

<Note>
  Les scripts de configuration qui installent des paquets ont besoin d'un accès réseau pour atteindre les registres. L'accès réseau **Trusted** par défaut permet les connexions aux [domaines de paquets courants](#default-allowed-domains) y compris npm, PyPI, RubyGems et crates.io. Les scripts échoueront à installer les paquets si votre environnement utilise l'accès réseau **None**.
</Note>

### Mise en cache de l'environnement

Le script de configuration s'exécute la première fois que vous démarrez une session dans un environnement. Après son achèvement, Anthropic crée un snapshot du système de fichiers et réutilise ce snapshot comme point de départ pour les sessions ultérieures. Les nouvelles sessions commencent avec vos dépendances, outils et images Docker déjà sur le disque, et l'étape du script de configuration est ignorée. Cela maintient le démarrage rapide même lorsque le script installe de grandes chaînes d'outils ou extrait des images de conteneur.

Le cache capture les fichiers, pas les processus en cours d'exécution. Tout ce que le script de configuration écrit sur le disque est transféré. Les services ou conteneurs qu'il démarre ne le sont pas, donc démarrez-les par session en demandant à Claude ou avec un [hook SessionStart](#setup-scripts-vs-sessionstart-hooks).

Le script de configuration s'exécute à nouveau pour reconstruire le cache lorsque vous modifiez le script de configuration de l'environnement ou les hôtes réseau autorisés, et lorsque le cache atteint son expiration après environ sept jours. La reprise d'une session existante ne réexécute jamais le script de configuration.

Vous n'avez pas besoin d'activer la mise en cache ou de gérer les snapshots vous-même.

### Scripts de configuration vs. hooks SessionStart

Utilisez un script de configuration pour installer les choses dont le cloud a besoin mais que votre ordinateur portable a déjà, comme un runtime de langage ou un outil CLI. Utilisez un hook [SessionStart](/fr/hooks#sessionstart) pour la configuration du projet qui devrait s'exécuter partout, cloud et local, comme `npm install`.

Les deux s'exécutent au démarrage d'une session, mais ils appartiennent à des endroits différents :

|                | Scripts de configuration                                                                                        | Hooks SessionStart                                                                    |
| -------------- | --------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| Attaché à      | L'environnement cloud                                                                                           | Votre référentiel                                                                     |
| Configuré dans | Interface utilisateur de l'environnement cloud                                                                  | `.claude/settings.json` dans votre référentiel                                        |
| S'exécute      | Avant le lancement de Claude Code, lorsqu'aucun [environnement en cache](#environment-caching) n'est disponible | Après le lancement de Claude Code, sur chaque session y compris les sessions reprises |
| Portée         | Environnements cloud uniquement                                                                                 | Local et cloud                                                                        |

Les hooks SessionStart peuvent également être définis dans votre `~/.claude/settings.json` au niveau de l'utilisateur localement, mais les paramètres au niveau de l'utilisateur ne sont pas transférés aux sessions cloud. Dans le cloud, seuls les hooks validés dans le référentiel s'exécutent.

### Installer les dépendances avec un hook SessionStart

Pour installer les dépendances uniquement dans les sessions cloud, ajoutez un hook SessionStart au `.claude/settings.json` de votre référentiel :

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

Créez le script à `scripts/install_pkgs.sh` et rendez-le exécutable avec `chmod +x`. La variable d'environnement `CLAUDE_CODE_REMOTE` est définie sur `true` dans les sessions cloud, vous pouvez donc l'utiliser pour ignorer l'exécution locale :

```bash theme={null}
#!/bin/bash

if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

Les hooks SessionStart ont certaines limitations dans les sessions cloud :

* **Pas de portée cloud uniquement** : les hooks s'exécutent dans les sessions locales et cloud. Pour ignorer l'exécution locale, vérifiez la variable d'environnement `CLAUDE_CODE_REMOTE` comme indiqué ci-dessus.
* **Nécessite un accès réseau** : les commandes d'installation ont besoin d'atteindre les registres de paquets. Si votre environnement utilise l'accès réseau **None**, ces hooks échouent. La [liste d'autorisation par défaut](#default-allowed-domains) sous **Trusted** couvre npm, PyPI, RubyGems et crates.io.
* **Compatibilité du proxy** : tout le trafic sortant passe par un [proxy de sécurité](#security-proxy). Certains gestionnaires de paquets ne fonctionnent pas correctement avec ce proxy. Bun est un exemple connu.
* **Ajoute une latence de démarrage** : les hooks s'exécutent chaque fois qu'une session démarre ou reprend, contrairement aux scripts de configuration qui bénéficient de la [mise en cache de l'environnement](#environment-caching). Gardez les scripts d'installation rapides en vérifiant si les dépendances sont déjà présentes avant de les réinstaller.

Pour persister les variables d'environnement pour les commandes Bash suivantes, écrivez dans le fichier à `$CLAUDE_ENV_FILE`. Consultez [Hooks SessionStart](/fr/hooks#sessionstart) pour plus de détails.

Remplacer l'image de base par votre propre image Docker n'est pas encore pris en charge. Utilisez un script de configuration pour installer ce dont vous avez besoin en haut de l'[image fournie](#installed-tools), ou exécutez votre image en tant que conteneur aux côtés de Claude avec `docker compose`.

## Accès réseau

L'accès réseau contrôle les connexions sortantes de l'environnement cloud. Chaque environnement spécifie un niveau d'accès, et vous pouvez l'étendre avec des domaines autorisés personnalisés. La valeur par défaut est **Trusted**, qui permet les registres de paquets et autres [domaines autorisés](#default-allowed-domains).

### Niveaux d'accès

Choisissez un niveau d'accès lorsque vous créez ou modifiez un environnement :

| Niveau      | Connexions sortantes                                                                                |
| :---------- | :-------------------------------------------------------------------------------------------------- |
| **None**    | Aucun accès réseau sortant                                                                          |
| **Trusted** | [Domaines autorisés](#default-allowed-domains) uniquement : registres de paquets, GitHub, SDK cloud |
| **Full**    | N'importe quel domaine                                                                              |
| **Custom**  | Votre propre liste d'autorisation, incluant optionnellement les valeurs par défaut                  |

Les opérations GitHub utilisent un [proxy séparé](#github-proxy) qui est indépendant de ce paramètre.

### Autoriser des domaines spécifiques

Pour autoriser les domaines qui ne figurent pas dans la liste Trusted, sélectionnez **Custom** dans les paramètres d'accès réseau de l'environnement. Un champ **Allowed domains** apparaît. Entrez un domaine par ligne :

```text theme={null}
api.example.com
*.internal.example.com
registry.example.com
```

Utilisez `*.` pour la correspondance de sous-domaine générique. Cochez **Also include default list of common package managers** pour conserver les [domaines Trusted](#default-allowed-domains) aux côtés de vos entrées personnalisées, ou laissez-le décoché pour autoriser uniquement ce que vous listez.

### Proxy GitHub

Pour la sécurité, toutes les opérations GitHub passent par un service proxy dédié qui gère de manière transparente toutes les interactions git. À l'intérieur du sandbox, le client git s'authentifie à l'aide d'une identité personnalisée limitée. Ce proxy :

* Gère l'authentification GitHub de manière sécurisée : le client git utilise une identité limitée à l'intérieur du sandbox, que le proxy vérifie et traduit en votre jeton d'authentification GitHub réel
* Restreint les opérations de poussée git à la branche de travail actuelle pour la sécurité
* Permet le clonage, la récupération et les opérations PR tout en maintenant les limites de sécurité

### Proxy de sécurité

Les environnements s'exécutent derrière un proxy réseau HTTP/HTTPS pour la sécurité et la prévention des abus. Tout le trafic Internet sortant passe par ce proxy, qui fournit :

* Protection contre les demandes malveillantes
* Limitation de débit et prévention des abus
* Filtrage de contenu pour une sécurité renforcée

### Domaines autorisés par défaut

Lors de l'utilisation de l'accès réseau **Trusted**, les domaines suivants sont autorisés par défaut. Les domaines marqués avec `*` indiquent une correspondance de sous-domaine générique, donc `*.gcr.io` autorise n'importe quel sous-domaine de `gcr.io`.

<AccordionGroup>
  <Accordion title="Services Anthropic">
    * api.anthropic.com
    * statsig.anthropic.com
    * docs.claude.com
    * platform.claude.com
    * code.claude.com
    * claude.ai
  </Accordion>

  <Accordion title="Contrôle de version">
    * github.com
    * [www.github.com](http://www.github.com)
    * api.github.com
    * npm.pkg.github.com
    * raw\.githubusercontent.com
    * pkg-npm.githubusercontent.com
    * objects.githubusercontent.com
    * release-assets.githubusercontent.com
    * codeload.github.com
    * avatars.githubusercontent.com
    * camo.githubusercontent.com
    * gist.github.com
    * gitlab.com
    * [www.gitlab.com](http://www.gitlab.com)
    * registry.gitlab.com
    * bitbucket.org
    * [www.bitbucket.org](http://www.bitbucket.org)
    * api.bitbucket.org
  </Accordion>

  <Accordion title="Registres de conteneurs">
    * registry-1.docker.io
    * auth.docker.io
    * index.docker.io
    * hub.docker.com
    * [www.docker.com](http://www.docker.com)
    * production.cloudflare.docker.com
    * download.docker.com
    * gcr.io
    * \*.gcr.io
    * ghcr.io
    * mcr.microsoft.com
    * \*.data.mcr.microsoft.com
    * public.ecr.aws
  </Accordion>

  <Accordion title="Plateformes cloud">
    * cloud.google.com
    * accounts.google.com
    * gcloud.google.com
    * \*.googleapis.com
    * storage.googleapis.com
    * compute.googleapis.com
    * container.googleapis.com
    * azure.com
    * portal.azure.com
    * microsoft.com
    * [www.microsoft.com](http://www.microsoft.com)
    * \*.microsoftonline.com
    * packages.microsoft.com
    * dotnet.microsoft.com
    * dot.net
    * visualstudio.com
    * dev.azure.com
    * \*.amazonaws.com
    * \*.api.aws
    * oracle.com
    * [www.oracle.com](http://www.oracle.com)
    * java.com
    * [www.java.com](http://www.java.com)
    * java.net
    * [www.java.net](http://www.java.net)
    * download.oracle.com
    * yum.oracle.com
  </Accordion>

  <Accordion title="Gestionnaires de paquets JavaScript et Node">
    * registry.npmjs.org
    * [www.npmjs.com](http://www.npmjs.com)
    * [www.npmjs.org](http://www.npmjs.org)
    * npmjs.com
    * npmjs.org
    * yarnpkg.com
    * registry.yarnpkg.com
  </Accordion>

  <Accordion title="Gestionnaires de paquets Python">
    * pypi.org
    * [www.pypi.org](http://www.pypi.org)
    * files.pythonhosted.org
    * pythonhosted.org
    * test.pypi.org
    * pypi.python.org
    * pypa.io
    * [www.pypa.io](http://www.pypa.io)
  </Accordion>

  <Accordion title="Gestionnaires de paquets Ruby">
    * rubygems.org
    * [www.rubygems.org](http://www.rubygems.org)
    * api.rubygems.org
    * index.rubygems.org
    * ruby-lang.org
    * [www.ruby-lang.org](http://www.ruby-lang.org)
    * rubyforge.org
    * [www.rubyforge.org](http://www.rubyforge.org)
    * rubyonrails.org
    * [www.rubyonrails.org](http://www.rubyonrails.org)
    * rvm.io
    * get.rvm.io
  </Accordion>

  <Accordion title="Gestionnaires de paquets Rust">
    * crates.io
    * [www.crates.io](http://www.crates.io)
    * index.crates.io
    * static.crates.io
    * rustup.rs
    * static.rust-lang.org
    * [www.rust-lang.org](http://www.rust-lang.org)
  </Accordion>

  <Accordion title="Gestionnaires de paquets Go">
    * proxy.golang.org
    * sum.golang.org
    * index.golang.org
    * golang.org
    * [www.golang.org](http://www.golang.org)
    * goproxy.io
    * pkg.go.dev
  </Accordion>

  <Accordion title="Gestionnaires de paquets JVM">
    * maven.org
    * repo.maven.org
    * central.maven.org
    * repo1.maven.org
    * repo.maven.apache.org
    * jcenter.bintray.com
    * gradle.org
    * [www.gradle.org](http://www.gradle.org)
    * services.gradle.org
    * plugins.gradle.org
    * kotlinlang.org
    * [www.kotlinlang.org](http://www.kotlinlang.org)
    * spring.io
    * repo.spring.io
  </Accordion>

  <Accordion title="Autres gestionnaires de paquets">
    * packagist.org (PHP Composer)
    * [www.packagist.org](http://www.packagist.org)
    * repo.packagist.org
    * nuget.org (.NET NuGet)
    * [www.nuget.org](http://www.nuget.org)
    * api.nuget.org
    * pub.dev (Dart/Flutter)
    * api.pub.dev
    * hex.pm (Elixir/Erlang)
    * [www.hex.pm](http://www.hex.pm)
    * cpan.org (Perl CPAN)
    * [www.cpan.org](http://www.cpan.org)
    * metacpan.org
    * [www.metacpan.org](http://www.metacpan.org)
    * api.metacpan.org
    * cocoapods.org (iOS/macOS)
    * [www.cocoapods.org](http://www.cocoapods.org)
    * cdn.cocoapods.org
    * haskell.org
    * [www.haskell.org](http://www.haskell.org)
    * hackage.haskell.org
    * swift.org
    * [www.swift.org](http://www.swift.org)
  </Accordion>

  <Accordion title="Distributions Linux">
    * archive.ubuntu.com
    * security.ubuntu.com
    * ubuntu.com
    * [www.ubuntu.com](http://www.ubuntu.com)
    * \*.ubuntu.com
    * ppa.launchpad.net
    * launchpad.net
    * [www.launchpad.net](http://www.launchpad.net)
    * \*.nixos.org
  </Accordion>

  <Accordion title="Outils de développement et plateformes">
    * dl.k8s.io (Kubernetes)
    * pkgs.k8s.io
    * k8s.io
    * [www.k8s.io](http://www.k8s.io)
    * releases.hashicorp.com (HashiCorp)
    * apt.releases.hashicorp.com
    * rpm.releases.hashicorp.com
    * archive.releases.hashicorp.com
    * hashicorp.com
    * [www.hashicorp.com](http://www.hashicorp.com)
    * repo.anaconda.com (Anaconda/Conda)
    * conda.anaconda.org
    * anaconda.org
    * [www.anaconda.com](http://www.anaconda.com)
    * anaconda.com
    * continuum.io
    * apache.org (Apache)
    * [www.apache.org](http://www.apache.org)
    * archive.apache.org
    * downloads.apache.org
    * eclipse.org (Eclipse)
    * [www.eclipse.org](http://www.eclipse.org)
    * download.eclipse.org
    * nodejs.org (Node.js)
    * [www.nodejs.org](http://www.nodejs.org)
    * developer.apple.com
    * developer.android.com
    * pkg.stainless.com
    * binaries.prisma.sh
  </Accordion>

  <Accordion title="Services cloud et surveillance">
    * statsig.com
    * [www.statsig.com](http://www.statsig.com)
    * api.statsig.com
    * sentry.io
    * \*.sentry.io
    * downloads.sentry-cdn.com
    * http-intake.logs.datadoghq.com
    * \*.datadoghq.com
    * \*.datadoghq.eu
    * api.honeycomb.io
  </Accordion>

  <Accordion title="Livraison de contenu et miroirs">
    * sourceforge.net
    * \*.sourceforge.net
    * packagecloud.io
    * \*.packagecloud.io
    * fonts.googleapis.com
    * fonts.gstatic.com
  </Accordion>

  <Accordion title="Schéma et configuration">
    * json-schema.org
    * [www.json-schema.org](http://www.json-schema.org)
    * json.schemastore.org
    * [www.schemastore.org](http://www.schemastore.org)
  </Accordion>

  <Accordion title="Model Context Protocol">
    * \*.modelcontextprotocol.io
  </Accordion>
</AccordionGroup>

## Déplacer les tâches entre le web et le terminal

Ces flux de travail nécessitent le [CLI Claude Code](/fr/quickstart) connecté au même compte claude.ai. Vous pouvez démarrer de nouvelles sessions cloud à partir de votre terminal, ou extraire les sessions cloud dans votre terminal pour continuer localement. Les sessions cloud persistent même si vous fermez votre ordinateur portable, et vous pouvez les surveiller de n'importe où, y compris depuis l'application mobile Claude.

<Note>
  À partir du CLI, le transfert de session est unidirectionnel : vous pouvez extraire les sessions cloud dans votre terminal avec `--teleport`, mais vous ne pouvez pas pousser une session de terminal existante vers le web. L'indicateur `--remote` crée une nouvelle session cloud pour votre référentiel actuel. L'[application Desktop](/fr/desktop#continue-in-another-surface) fournit un menu Continue in qui peut envoyer une session locale vers le web.
</Note>

### Du terminal au web

Démarrez une session cloud à partir de la ligne de commande avec l'indicateur `--remote` :

```bash theme={null}
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

Cela crée une nouvelle session cloud sur claude.ai. La session clone votre répertoire courant du serveur distant GitHub à votre branche actuelle, donc poussez d'abord si vous avez des commits locaux, puisque la VM clone depuis GitHub plutôt que depuis votre machine. `--remote` fonctionne avec un seul référentiel à la fois. La tâche s'exécute dans le cloud tandis que vous continuez à travailler localement.

<Note>
  `--remote` crée des sessions cloud. `--remote-control` n'est pas lié : il expose une session CLI locale pour la surveillance depuis le web. Consultez [Contrôle à distance](/fr/remote-control).
</Note>

Utilisez `/tasks` dans le CLI Claude Code pour vérifier la progression, ou ouvrez la session sur claude.ai ou l'application mobile Claude pour interagir directement. De là, vous pouvez diriger Claude, fournir des commentaires ou répondre à des questions comme dans n'importe quelle autre conversation.

#### Conseils pour les tâches cloud

**Planifiez localement, exécutez à distance** : pour les tâches complexes, démarrez Claude en mode plan pour collaborer sur l'approche, puis envoyez le travail vers le cloud :

```bash theme={null}
claude --permission-mode plan
```

En mode plan, Claude lit les fichiers, exécute les commandes pour explorer et propose un plan sans modifier le code source. Une fois que vous êtes satisfait, enregistrez le plan dans le référentiel, validez et poussez afin que la VM cloud puisse le cloner. Ensuite, démarrez une session cloud pour l'exécution autonome :

```bash theme={null}
claude --remote "Execute the migration plan in docs/migration-plan.md"
```

Ce modèle vous donne le contrôle sur la stratégie tout en permettant à Claude d'exécuter de manière autonome dans le cloud.

**Planifiez dans le cloud avec ultraplan** : pour rédiger et examiner le plan lui-même dans une session web, utilisez [ultraplan](/fr/ultraplan). Claude génère le plan sur Claude Code sur le web tandis que vous continuez à travailler, puis vous commentez les sections dans votre navigateur et choisissez d'exécuter à distance ou d'envoyer le plan vers votre terminal.

**Exécutez les tâches en parallèle** : chaque commande `--remote` crée sa propre session cloud qui s'exécute indépendamment. Vous pouvez lancer plusieurs tâches et elles s'exécuteront toutes simultanément dans des sessions séparées :

```bash theme={null}
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

Surveillez toutes les sessions avec `/tasks` dans le CLI Claude Code. Lorsqu'une session se termine, vous pouvez créer une PR à partir de l'interface web ou [téléporter](#from-web-to-terminal) la session vers votre terminal pour continuer à travailler.

#### Envoyer les référentiels locaux sans GitHub

Lorsque vous exécutez `claude --remote` à partir d'un référentiel qui n'est pas connecté à GitHub, Claude Code regroupe votre référentiel local et le télécharge directement vers la session cloud. Le paquet inclut votre historique de référentiel complet sur toutes les branches, plus toute modification non validée des fichiers suivis.

Ce repli s'active automatiquement lorsque l'accès à GitHub n'est pas disponible. Pour le forcer même lorsque GitHub est connecté, définissez `CCR_FORCE_BUNDLE=1` :

```bash theme={null}
CCR_FORCE_BUNDLE=1 claude --remote "Run the test suite and fix any failures"
```

Les référentiels regroupés doivent respecter ces limites :

* Le répertoire doit être un référentiel git avec au moins un commit
* Le référentiel regroupé doit être inférieur à 100 Mo. Les référentiels plus grands reviennent à regrouper uniquement la branche actuelle, puis à un snapshot unique aplati de l'arborescence de travail, et échouent uniquement si le snapshot est toujours trop volumineux
* Les fichiers non suivis ne sont pas inclus ; exécutez `git add` sur les fichiers que vous souhaitez que la session cloud voie
* Les sessions créées à partir d'un paquet ne peuvent pas pousser vers un serveur distant à moins que vous ayez également [authentification GitHub](#github-authentication-options) configurée

### Du web au terminal

Extrayez une session cloud dans votre terminal en utilisant l'une de ces options :

* **Utilisation de `--teleport`** : à partir de la ligne de commande, exécutez `claude --teleport` pour un sélecteur de session interactif, ou `claude --teleport <session-id>` pour reprendre une session spécifique directement. Si vous avez des modifications non validées, vous serez invité à les ranger d'abord.
* **Utilisation de `/teleport`** : à l'intérieur d'une session CLI existante, exécutez `/teleport` (ou `/tp`) pour ouvrir le même sélecteur de session sans redémarrer Claude Code.
* **À partir de `/tasks`** : exécutez `/tasks` pour voir vos sessions en arrière-plan, puis appuyez sur `t` pour vous téléporter dans l'une d'elles
* **À partir de l'interface web** : sélectionnez **Open in CLI** pour copier une commande que vous pouvez coller dans votre terminal

Lorsque vous téléportez une session, Claude vérifie que vous êtes dans le bon référentiel, récupère et extrait la branche de la session cloud, et charge l'historique complet de la conversation dans votre terminal.

`--teleport` est distinct de `--resume`. `--resume` rouvre une conversation à partir de l'historique local de cette machine et ne liste pas les sessions cloud ; `--teleport` extrait une session cloud et sa branche.

#### Exigences de téléportation

La téléportation vérifie ces exigences avant de reprendre une session. Si une exigence n'est pas satisfaite, vous verrez une erreur ou vous serez invité à résoudre le problème.

| Exigence            | Détails                                                                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| État git propre     | Votre répertoire de travail ne doit avoir aucune modification non validée. La téléportation vous invite à ranger les modifications si nécessaire. |
| Référentiel correct | Vous devez exécuter `--teleport` à partir d'une extraction du même référentiel, pas d'une fourche.                                                |
| Branche disponible  | La branche de la session cloud doit avoir été poussée vers le serveur distant. La téléportation la récupère et l'extrait automatiquement.         |
| Même compte         | Vous devez être authentifié au même compte claude.ai utilisé dans la session cloud.                                                               |

#### `--teleport` n'est pas disponible

La téléportation nécessite l'authentification par abonnement claude.ai. Si vous êtes authentifié via clé API, Bedrock, Vertex AI ou Microsoft Foundry, exécutez `/login` pour vous connecter avec votre compte claude.ai à la place. Si vous êtes déjà connecté via claude.ai et `--teleport` n'est toujours pas disponible, votre organisation a peut-être désactivé les sessions cloud.

## Travailler avec les sessions

Les sessions apparaissent dans la barre latérale à claude.ai/code. De là, vous pouvez examiner les modifications, partager avec les coéquipiers, archiver le travail terminé ou supprimer les sessions définitivement.

### Gérer le contexte

Les sessions cloud prennent en charge les [commandes intégrées](/fr/commands) qui produisent une sortie textuelle. Les commandes qui ouvrent un sélecteur de terminal interactif, comme `/model` ou `/config`, ne sont pas disponibles.

Pour la gestion du contexte spécifiquement :

| Commande   | Fonctionne dans les sessions cloud | Notes                                                                                                                                 |
| :--------- | :--------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------ |
| `/compact` | Oui                                | Résume la conversation pour libérer du contexte. Accepte les instructions de focus optionnelles comme `/compact keep the test output` |
| `/context` | Oui                                | Affiche ce qui est actuellement dans la fenêtre de contexte                                                                           |
| `/clear`   | Non                                | Démarrez une nouvelle session à partir de la barre latérale à la place                                                                |

La compaction automatique s'exécute automatiquement lorsque la fenêtre de contexte approche de la capacité, comme dans le CLI. Pour la déclencher plus tôt, définissez [`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`](/fr/env-vars) dans vos [variables d'environnement](#configure-your-environment). Par exemple, `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE=70` compacte à 70 % de capacité au lieu de la valeur par défaut \~95 %. Pour modifier la taille de fenêtre effective pour les calculs de compaction, utilisez [`CLAUDE_CODE_AUTO_COMPACT_WINDOW`](/fr/env-vars).

Les [sous-agents](/fr/sub-agents) fonctionnent de la même manière qu'en local. Claude peut les générer avec l'outil Task pour décharger la recherche ou le travail parallèle dans une fenêtre de contexte séparée, gardant la conversation principale plus légère. Les sous-agents définis dans votre `.claude/agents/` du référentiel sont récupérés automatiquement. Les [équipes d'agents](/fr/agent-teams) sont désactivées par défaut mais peuvent être activées en ajoutant `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` à vos [variables d'environnement](#configure-your-environment).

### Examiner les modifications

Chaque session affiche un indicateur de diff avec les lignes ajoutées et supprimées, comme `+42 -18`. Sélectionnez-le pour ouvrir la vue diff, laissez des commentaires en ligne sur des lignes spécifiques et envoyez-les à Claude avec votre message suivant. Consultez [Examiner et itérer](/fr/web-quickstart#review-and-iterate) pour la procédure pas à pas complète incluant la création de PR. Pour que Claude surveille la PR pour les défaillances CI et les commentaires d'examen automatiquement, consultez [Correction automatique des demandes de tirage](#auto-fix-pull-requests).

### Partager les sessions

Pour partager une session, basculez sa visibilité selon les types de compte ci-dessous. Après cela, partagez le lien de session tel quel. Les destinataires voient l'état le plus récent lorsqu'ils ouvrent le lien, mais leur vue ne se met pas à jour en temps réel.

#### Partage à partir d'un compte Enterprise ou Team

Pour les comptes Enterprise et Team, les deux options de visibilité sont **Private** et **Team**. La visibilité Team rend la session visible aux autres membres de votre organisation claude.ai. La vérification de l'accès au référentiel est activée par défaut, en fonction du compte GitHub connecté au compte du destinataire. Le nom d'affichage de votre compte est visible à tous les destinataires ayant accès. Les sessions [Claude dans Slack](/fr/slack) sont automatiquement partagées avec la visibilité Team.

#### Partage à partir d'un compte Max ou Pro

Pour les comptes Max et Pro, les deux options de visibilité sont **Private** et **Public**. La visibilité Public rend la session visible à tout utilisateur connecté à claude.ai.

Vérifiez votre session pour le contenu sensible avant de la partager. Les sessions peuvent contenir du code et des identifiants provenant de référentiels GitHub privés. La vérification de l'accès au référentiel n'est pas activée par défaut.

Pour exiger que les destinataires aient accès au référentiel, ou pour masquer votre nom des sessions partagées, allez à Paramètres > Claude Code > Paramètres de partage.

### Archiver les sessions

Vous pouvez archiver les sessions pour garder votre liste de sessions organisée. Les sessions archivées sont masquées de la liste de sessions par défaut mais peuvent être affichées en filtrant les sessions archivées.

Pour archiver une session, survolez la session dans la barre latérale et sélectionnez l'icône d'archivage.

### Supprimer les sessions

La suppression d'une session supprime définitivement la session et ses données. Cette action ne peut pas être annulée. Vous pouvez supprimer une session de deux façons :

* **À partir de la barre latérale** : filtrez les sessions archivées, puis survolez la session que vous souhaitez supprimer et sélectionnez l'icône de suppression
* **À partir du menu de session** : ouvrez une session, sélectionnez la liste déroulante à côté du titre de la session et sélectionnez **Delete**

Vous serez invité à confirmer avant la suppression d'une session.

## Correction automatique des demandes de tirage

Claude peut surveiller une demande de tirage et répondre automatiquement aux défaillances CI et aux commentaires d'examen. Claude s'abonne aux événements GitHub sur la PR, et lorsqu'une vérification échoue ou qu'un examinateur laisse un commentaire, Claude enquête et pousse une correction si elle est claire.

<Note>
  Auto-fix nécessite que l'application Claude GitHub soit installée sur votre référentiel. Si vous ne l'avez pas déjà fait, installez-la à partir de la [page de l'application GitHub](https://github.com/apps/claude) ou lorsque vous y êtes invité lors de la [configuration](/fr/web-quickstart#connect-github-and-create-an-environment).
</Note>

Il existe plusieurs façons d'activer auto-fix selon d'où provient la PR et quel appareil vous utilisez :

* **PR créées dans Claude Code sur le web** : ouvrez la barre d'état CI et sélectionnez **Auto-fix**
* **À partir de votre terminal** : exécutez [`/autofix-pr`](/fr/commands) sur la branche de la PR. Claude Code détecte la PR ouverte avec `gh`, génère une session web et active auto-fix en une seule étape
* **À partir de l'application mobile** : dites à Claude de corriger automatiquement la PR, par exemple « regardez cette PR et corrigez les défaillances CI ou les commentaires d'examen »
* **N'importe quelle PR existante** : collez l'URL de la PR dans une session et dites à Claude de la corriger automatiquement

### Comment Claude répond à l'activité PR

Lorsque auto-fix est actif, Claude reçoit les événements GitHub pour la PR, y compris les nouveaux commentaires d'examen et les défaillances de vérification CI. Pour chaque événement, Claude enquête et décide comment procéder :

* **Corrections claires** : si Claude est confiant dans une correction et qu'elle n'entre pas en conflit avec les instructions antérieures, Claude apporte la modification, la pousse et explique ce qui a été fait dans la session
* **Demandes ambiguës** : si le commentaire d'un examinateur peut être interprété de plusieurs façons ou implique quelque chose d'architecturalement significatif, Claude vous demande avant d'agir
* **Événements en double ou sans action** : si un événement est un doublon ou ne nécessite aucune modification, Claude le note dans la session et continue

Claude peut répondre aux fils de commentaires d'examen sur GitHub dans le cadre de leur résolution. Ces réponses sont publiées en utilisant votre compte GitHub, elles apparaissent donc sous votre nom d'utilisateur, mais chaque réponse est étiquetée comme provenant de Claude Code pour que les examinateurs sachent qu'elle a été écrite par l'agent et non par vous directement.

<Warning>
  Si votre référentiel utilise une automatisation déclenchée par commentaire comme Atlantis, Terraform Cloud ou des GitHub Actions personnalisées qui s'exécutent sur les événements `issue_comment`, sachez que Claude peut répondre en votre nom, ce qui peut déclencher ces flux de travail. Examinez l'automatisation de votre référentiel avant d'activer auto-fix et envisagez de désactiver auto-fix pour les référentiels où un commentaire PR peut déployer une infrastructure ou exécuter des opérations privilégiées.
</Warning>

## Sécurité et isolation

Chaque session cloud est séparée de votre machine et des autres sessions par plusieurs couches :

* **Machines virtuelles isolées** : chaque session s'exécute dans une VM isolée gérée par Anthropic
* **Contrôles d'accès réseau** : l'accès réseau est limité par défaut et peut être désactivé. Lors de l'exécution avec l'accès réseau désactivé, Claude Code peut toujours communiquer avec l'API Anthropic, ce qui peut permettre aux données de quitter la VM.
* **Protection des identifiants** : les identifiants sensibles tels que les identifiants git ou les clés de signature ne sont jamais à l'intérieur du sandbox avec Claude Code. L'authentification est gérée via un proxy sécurisé utilisant des identifiants limités.
* **Analyse sécurisée** : le code est analysé et modifié dans des VM isolées avant la création de PR

## Limitations

Avant de compter sur les sessions cloud pour un flux de travail, tenez compte de ces contraintes :

* **Limites de débit** : Claude Code sur le web partage les limites de débit avec tous les autres usages de Claude et Claude Code au sein de votre compte. L'exécution de plusieurs tâches en parallèle consomme proportionnellement plus de limites de débit. Il n'y a pas de frais de calcul séparé pour la VM cloud.
* **Authentification du référentiel** : vous ne pouvez déplacer les sessions du web vers le local que lorsque vous êtes authentifié au même compte
* **Restrictions de plateforme** : le clonage du référentiel et la création de demandes de tirage nécessitent GitHub. Les instances [GitHub Enterprise Server](/fr/github-enterprise-server) auto-hébergées sont prises en charge pour les plans Team et Enterprise. GitLab, Bitbucket et les autres référentiels non-GitHub peuvent être envoyés aux sessions cloud en tant que [paquet local](#send-local-repositories-without-github), mais la session ne peut pas pousser les résultats vers le serveur distant

## Ressources connexes

* [Ultraplan](/fr/ultraplan) : rédigez un plan dans une session cloud et examinez-le dans votre navigateur
* [Ultrareview](/fr/ultrareview) : exécutez un examen de code multi-agent approfondi dans un sandbox cloud
* [Routines](/fr/routines) : automatisez le travail selon un calendrier, via un appel API ou en réponse aux événements GitHub
* [Configuration des hooks](/fr/hooks) : exécutez les scripts aux événements du cycle de vie de la session
* [Référence des paramètres](/fr/settings) : toutes les options de configuration
* [Sécurité](/fr/security) : garanties d'isolation et gestion des données
* [Utilisation des données](/fr/data-usage) : ce qu'Anthropic conserve des sessions cloud
