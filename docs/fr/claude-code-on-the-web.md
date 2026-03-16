> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code sur le web

> Exécutez les tâches Claude Code de manière asynchrone sur une infrastructure cloud sécurisée

<Note>
  Claude Code sur le web est actuellement en aperçu de recherche.
</Note>

## Qu'est-ce que Claude Code sur le web ?

Claude Code sur le web permet aux développeurs de lancer Claude Code depuis l'application Claude. C'est parfait pour :

* **Répondre à des questions** : Posez des questions sur l'architecture du code et la façon dont les fonctionnalités sont implémentées
* **Corrections de bugs et tâches de routine** : Tâches bien définies qui ne nécessitent pas de direction fréquente
* **Travail en parallèle** : Abordez plusieurs corrections de bugs en parallèle
* **Référentiels non sur votre machine locale** : Travaillez sur du code que vous n'avez pas extrait localement
* **Modifications du backend** : Où Claude Code peut écrire des tests puis écrire du code pour passer ces tests

Claude Code est également disponible sur l'application Claude pour [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) et [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) pour lancer des tâches en déplacement et surveiller le travail en cours.

Vous pouvez [lancer de nouvelles tâches sur le web depuis votre terminal](#from-terminal-to-web) avec `--remote`, ou [téléporter les sessions web vers votre terminal](#from-web-to-terminal) pour continuer localement. Pour utiliser l'interface web tout en exécutant Claude Code sur votre propre machine au lieu de l'infrastructure cloud, consultez [Contrôle à distance](/fr/remote-control).

## Qui peut utiliser Claude Code sur le web ?

Claude Code sur le web est disponible en aperçu de recherche pour :

* **Les utilisateurs Pro**
* **Les utilisateurs Max**
* **Les utilisateurs Team**
* **Les utilisateurs Enterprise** avec des sièges premium ou des sièges Chat + Claude Code

## Démarrage

1. Visitez [claude.ai/code](https://claude.ai/code)
2. Connectez votre compte GitHub
3. Installez l'application Claude GitHub dans vos référentiels
4. Sélectionnez votre environnement par défaut
5. Soumettez votre tâche de codage
6. Examinez les modifications en vue diff, itérez avec des commentaires, puis créez une demande de tirage

## Comment ça marche

Lorsque vous démarrez une tâche sur Claude Code sur le web :

1. **Clonage du référentiel** : Votre référentiel est cloné sur une machine virtuelle gérée par Anthropic
2. **Configuration de l'environnement** : Claude prépare un environnement cloud sécurisé avec votre code, puis exécute votre [script de configuration](#setup-scripts) s'il est configuré
3. **Configuration du réseau** : L'accès à Internet est configuré en fonction de vos paramètres
4. **Exécution de la tâche** : Claude analyse le code, apporte des modifications, exécute des tests et vérifie son travail
5. **Achèvement** : Vous êtes notifié lorsque c'est terminé et vous pouvez créer une PR avec les modifications
6. **Résultats** : Les modifications sont poussées vers une branche, prêtes pour la création d'une demande de tirage

## Examinez les modifications avec la vue diff

La vue diff vous permet de voir exactement ce que Claude a modifié avant de créer une demande de tirage. Au lieu de cliquer sur « Créer une PR » pour examiner les modifications dans GitHub, affichez le diff directement dans l'application et itérez avec Claude jusqu'à ce que les modifications soient prêtes.

Lorsque Claude apporte des modifications aux fichiers, un indicateur de statistiques diff apparaît indiquant le nombre de lignes ajoutées et supprimées (par exemple, `+12 -1`). Sélectionnez cet indicateur pour ouvrir la visionneuse diff, qui affiche une liste de fichiers à gauche et les modifications pour chaque fichier à droite.

À partir de la vue diff, vous pouvez :

* Examiner les modifications fichier par fichier
* Commenter des modifications spécifiques pour demander des modifications
* Continuer à itérer avec Claude en fonction de ce que vous voyez

Cela vous permet d'affiner les modifications à travers plusieurs cycles de rétroaction sans créer de PR de brouillon ni basculer vers GitHub.

## Déplacer les tâches entre le web et le terminal

Vous pouvez démarrer de nouvelles tâches sur le web depuis votre terminal, ou extraire les sessions web dans votre terminal pour continuer localement. Les sessions web persistent même si vous fermez votre ordinateur portable, et vous pouvez les surveiller de n'importe où, y compris depuis l'application mobile Claude.

<Note>
  Le transfert de session est unidirectionnel : vous pouvez extraire les sessions web dans votre terminal, mais vous ne pouvez pas pousser une session de terminal existante vers le web. L'indicateur `--remote` crée une *nouvelle* session web pour votre référentiel actuel.
</Note>

### Du terminal au web

Démarrez une session web à partir de la ligne de commande avec l'indicateur `--remote` :

```bash  theme={null}
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

Cela crée une nouvelle session web sur claude.ai. La tâche s'exécute dans le cloud tandis que vous continuez à travailler localement. Utilisez `/tasks` pour vérifier la progression, ou ouvrez la session sur claude.ai ou l'application mobile Claude pour interagir directement. De là, vous pouvez diriger Claude, fournir des commentaires ou répondre à des questions comme dans n'importe quelle autre conversation.

#### Conseils pour les tâches distantes

**Planifiez localement, exécutez à distance** : Pour les tâches complexes, démarrez Claude en mode plan pour collaborer sur l'approche, puis envoyez le travail sur le web :

```bash  theme={null}
claude --permission-mode plan
```

En mode plan, Claude ne peut que lire les fichiers et explorer la base de code. Une fois que vous êtes satisfait du plan, démarrez une session distante pour une exécution autonome :

```bash  theme={null}
claude --remote "Execute the migration plan in docs/migration-plan.md"
```

Ce modèle vous donne le contrôle sur la stratégie tout en permettant à Claude d'exécuter de manière autonome dans le cloud.

**Exécutez les tâches en parallèle** : Chaque commande `--remote` crée sa propre session web qui s'exécute indépendamment. Vous pouvez lancer plusieurs tâches et elles s'exécuteront toutes simultanément dans des sessions séparées :

```bash  theme={null}
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

Surveillez toutes les sessions avec `/tasks`. Lorsqu'une session se termine, vous pouvez créer une PR à partir de l'interface web ou [téléporter](#from-web-to-terminal) la session vers votre terminal pour continuer à travailler.

### Du web au terminal

Il existe plusieurs façons d'extraire une session web dans votre terminal :

* **Utilisation de `/teleport`** : Depuis Claude Code, exécutez `/teleport` (ou `/tp`) pour voir un sélecteur interactif de vos sessions web. Si vous avez des modifications non validées, vous serez invité à les ranger d'abord.
* **Utilisation de `--teleport`** : À partir de la ligne de commande, exécutez `claude --teleport` pour un sélecteur de session interactif, ou `claude --teleport <session-id>` pour reprendre une session spécifique directement.
* **À partir de `/tasks`** : Exécutez `/tasks` pour voir vos sessions en arrière-plan, puis appuyez sur `t` pour vous téléporter dans l'une d'elles
* **À partir de l'interface web** : Cliquez sur « Ouvrir dans CLI » pour copier une commande que vous pouvez coller dans votre terminal

Lorsque vous téléportez une session, Claude vérifie que vous êtes dans le bon référentiel, récupère et extrait la branche de la session distante, et charge l'historique complet de la conversation dans votre terminal.

#### Exigences pour la téléportation

La téléportation vérifie ces exigences avant de reprendre une session. Si une exigence n'est pas satisfaite, vous verrez une erreur ou vous serez invité à résoudre le problème.

| Exigence            | Détails                                                                                                                                           |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| État git propre     | Votre répertoire de travail ne doit avoir aucune modification non validée. La téléportation vous invite à ranger les modifications si nécessaire. |
| Référentiel correct | Vous devez exécuter `--teleport` à partir d'une extraction du même référentiel, pas d'une fourche.                                                |
| Branche disponible  | La branche de la session web doit avoir été poussée vers le serveur distant. La téléportation la récupère et l'extrait automatiquement.           |
| Même compte         | Vous devez être authentifié au même compte Claude.ai utilisé dans la session web.                                                                 |

### Partage de sessions

Pour partager une session, basculez sa visibilité selon les types de compte ci-dessous. Après cela, partagez le lien de session tel quel. Les destinataires qui ouvrent votre session partagée verront l'état le plus récent de la session au chargement, mais la page du destinataire ne se mettra pas à jour en temps réel.

#### Partage à partir d'un compte Enterprise ou Teams

Pour les comptes Enterprise et Teams, les deux options de visibilité sont **Privé** et **Team**. La visibilité Team rend la session visible aux autres membres de votre organisation Claude.ai. La vérification de l'accès au référentiel est activée par défaut, en fonction du compte GitHub connecté au compte du destinataire. Le nom d'affichage de votre compte est visible à tous les destinataires ayant accès. Les sessions [Claude dans Slack](/fr/slack) sont automatiquement partagées avec la visibilité Team.

#### Partage à partir d'un compte Max ou Pro

Pour les comptes Max et Pro, les deux options de visibilité sont **Privé** et **Public**. La visibilité publique rend la session visible à tout utilisateur connecté à claude.ai.

Vérifiez votre session pour le contenu sensible avant de la partager. Les sessions peuvent contenir du code et des identifiants provenant de référentiels GitHub privés. La vérification de l'accès au référentiel n'est pas activée par défaut.

Activez la vérification de l'accès au référentiel et/ou retenez votre nom de vos sessions partagées en accédant à Paramètres > Claude Code > Paramètres de partage.

## Gestion des sessions

### Archivage des sessions

Vous pouvez archiver les sessions pour garder votre liste de sessions organisée. Les sessions archivées sont masquées de la liste de sessions par défaut mais peuvent être affichées en filtrant les sessions archivées.

Pour archiver une session, survolez la session dans la barre latérale et cliquez sur l'icône d'archivage.

### Suppression de sessions

La suppression d'une session supprime définitivement la session et ses données. Cette action ne peut pas être annulée. Vous pouvez supprimer une session de deux façons :

* **À partir de la barre latérale** : Filtrez les sessions archivées, puis survolez la session que vous souhaitez supprimer et cliquez sur l'icône de suppression
* **À partir du menu de session** : Ouvrez une session, cliquez sur la liste déroulante à côté du titre de la session, et sélectionnez **Supprimer**

Vous serez invité à confirmer avant la suppression d'une session.

## Environnement cloud

### Image par défaut

Nous construisons et maintenons une image universelle avec des chaînes d'outils courantes et des écosystèmes de langage pré-installés. Cette image inclut :

* Langages de programmation et runtimes populaires
* Outils de construction courants et gestionnaires de paquets
* Frameworks de test et linters

#### Vérification des outils disponibles

Pour voir ce qui est pré-installé dans votre environnement, demandez à Claude Code d'exécuter :

```bash  theme={null}
check-tools
```

Cette commande affiche :

* Langages de programmation et leurs versions
* Gestionnaires de paquets disponibles
* Outils de développement installés

#### Configurations spécifiques au langage

L'image universelle inclut des environnements pré-configurés pour :

* **Python** : Python 3.x avec pip, poetry et des bibliothèques scientifiques courantes
* **Node.js** : Dernières versions LTS avec npm, yarn, pnpm et bun
* **Ruby** : Versions 3.1.6, 3.2.6, 3.3.6 (par défaut : 3.3.6) avec gem, bundler et rbenv pour la gestion des versions
* **PHP** : Version 8.4.14
* **Java** : OpenJDK avec Maven et Gradle
* **Go** : Dernière version stable avec support des modules
* **Rust** : Chaîne d'outils Rust avec cargo
* **C++** : Compilateurs GCC et Clang

#### Bases de données

L'image universelle inclut les bases de données suivantes :

* **PostgreSQL** : Version 16
* **Redis** : Version 7.0

### Configuration de l'environnement

Lorsque vous démarrez une session dans Claude Code sur le web, voici ce qui se passe en coulisse :

1. **Préparation de l'environnement** : Nous clonons votre référentiel et exécutons tout [script de configuration](#setup-scripts) configuré. Le référentiel sera cloné avec la branche par défaut de votre référentiel GitHub. Si vous souhaitez extraire une branche spécifique, vous pouvez la spécifier dans l'invite.

2. **Configuration du réseau** : Nous configurons l'accès à Internet pour l'agent. L'accès à Internet est limité par défaut, mais vous pouvez configurer l'environnement pour n'avoir aucun accès à Internet ou un accès Internet complet en fonction de vos besoins.

3. **Exécution de Claude Code** : Claude Code s'exécute pour accomplir votre tâche, en écrivant du code, en exécutant des tests et en vérifiant son travail. Vous pouvez guider et diriger Claude tout au long de la session via l'interface web. Claude respecte le contexte que vous avez défini dans votre `CLAUDE.md`.

4. **Résultat** : Lorsque Claude termine son travail, il poussera la branche vers le serveur distant. Vous pourrez créer une PR pour la branche.

<Note>
  Claude opère entièrement via le terminal et les outils CLI disponibles dans l'environnement. Il utilise les outils pré-installés dans l'image universelle et tous les outils supplémentaires que vous installez via des hooks ou la gestion des dépendances.
</Note>

**Pour ajouter un nouvel environnement :** Sélectionnez l'environnement actuel pour ouvrir le sélecteur d'environnement, puis sélectionnez « Ajouter un environnement ». Cela ouvrira une boîte de dialogue où vous pouvez spécifier le nom de l'environnement, le niveau d'accès réseau, les variables d'environnement et un [script de configuration](#setup-scripts).

**Pour mettre à jour un environnement existant :** Sélectionnez l'environnement actuel, à droite du nom de l'environnement, et sélectionnez le bouton des paramètres. Cela ouvrira une boîte de dialogue où vous pouvez mettre à jour le nom de l'environnement, l'accès réseau, les variables d'environnement et le script de configuration.

**Pour sélectionner votre environnement par défaut à partir du terminal :** Si vous avez plusieurs environnements configurés, exécutez `/remote-env` pour choisir celui à utiliser lors du démarrage de sessions web à partir de votre terminal avec `--remote`. Avec un seul environnement, cette commande affiche votre configuration actuelle.

<Note>
  Les variables d'environnement doivent être spécifiées sous forme de paires clé-valeur, au [format `.env`](https://www.dotenv.org/). Par exemple :

  ```text  theme={null}
  API_KEY=your_api_key
  DEBUG=true
  ```
</Note>

### Scripts de configuration

Un script de configuration est un script Bash qui s'exécute au démarrage d'une nouvelle session cloud, avant le lancement de Claude Code. Utilisez les scripts de configuration pour installer des dépendances, configurer des outils ou préparer tout ce dont l'environnement cloud a besoin et qui ne figure pas dans l'[image par défaut](#default-image).

Les scripts s'exécutent en tant que root sur Ubuntu 24.04, donc `apt install` et la plupart des gestionnaires de paquets de langage fonctionnent.

<Tip>
  Pour vérifier ce qui est déjà installé avant de l'ajouter à votre script, demandez à Claude d'exécuter `check-tools` dans une session cloud.
</Tip>

Pour ajouter un script de configuration, ouvrez la boîte de dialogue des paramètres d'environnement et entrez votre script dans le champ **Script de configuration**.

Cet exemple installe le CLI `gh`, qui ne figure pas dans l'image par défaut :

```bash  theme={null}
#!/bin/bash
apt update && apt install -y gh
```

Les scripts de configuration s'exécutent uniquement lors de la création d'une nouvelle session. Ils sont ignorés lors de la reprise d'une session existante.

Si le script se termine avec un code non nul, la session ne démarre pas. Ajoutez `|| true` aux commandes non critiques pour éviter de bloquer la session sur une installation instable.

<Note>
  Les scripts de configuration qui installent des paquets ont besoin d'un accès réseau pour atteindre les registres. L'accès réseau par défaut permet les connexions aux [registres de paquets courants](#default-allowed-domains) y compris npm, PyPI, RubyGems et crates.io. Les scripts échoueront à installer les paquets si votre environnement a l'accès réseau désactivé.
</Note>

#### Scripts de configuration vs. hooks SessionStart

Utilisez un script de configuration pour installer les choses dont le cloud a besoin mais que votre ordinateur portable a déjà, comme un runtime de langage ou un outil CLI. Utilisez un hook [SessionStart](/fr/hooks#sessionstart) pour la configuration du projet qui devrait s'exécuter partout, cloud et local, comme `npm install`.

Les deux s'exécutent au démarrage d'une session, mais ils appartiennent à des endroits différents :

|                | Scripts de configuration                                                 | Hooks SessionStart                                                                    |
| -------------- | ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------- |
| Attaché à      | L'environnement cloud                                                    | Votre référentiel                                                                     |
| Configuré dans | Interface utilisateur de l'environnement cloud                           | `.claude/settings.json` dans votre référentiel                                        |
| S'exécute      | Avant le lancement de Claude Code, sur les nouvelles sessions uniquement | Après le lancement de Claude Code, sur chaque session y compris les sessions reprises |
| Portée         | Environnements cloud uniquement                                          | Local et cloud                                                                        |

Les hooks SessionStart peuvent également être définis dans votre `~/.claude/settings.json` au niveau de l'utilisateur localement, mais les paramètres au niveau de l'utilisateur ne sont pas transférés aux sessions cloud. Dans le cloud, seuls les hooks validés dans le référentiel s'exécutent.

### Gestion des dépendances

Les images d'environnement personnalisées et les snapshots ne sont pas encore pris en charge. Utilisez les [scripts de configuration](#setup-scripts) pour installer les paquets au démarrage d'une session, ou les [hooks SessionStart](/fr/hooks#sessionstart) pour l'installation de dépendances qui devrait également s'exécuter dans les environnements locaux. Les hooks SessionStart ont des [limitations connues](#dependency-management-limitations).

Pour configurer l'installation automatique des dépendances avec un script de configuration, ouvrez vos paramètres d'environnement et ajoutez un script :

```bash  theme={null}
#!/bin/bash
npm install
pip install -r requirements.txt
```

Vous pouvez également utiliser les hooks SessionStart dans le fichier `.claude/settings.json` de votre référentiel pour l'installation de dépendances qui devrait également s'exécuter dans les environnements locaux :

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
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

Créez le script correspondant à `scripts/install_pkgs.sh` :

```bash  theme={null}
#!/bin/bash

# Only run in remote environments
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

Rendez-le exécutable : `chmod +x scripts/install_pkgs.sh`

#### Persister les variables d'environnement

Les hooks SessionStart peuvent persister les variables d'environnement pour les commandes Bash suivantes en écrivant dans le fichier spécifié dans la variable d'environnement `CLAUDE_ENV_FILE`. Pour plus de détails, consultez les [hooks SessionStart](/fr/hooks#sessionstart) dans la référence des hooks.

#### Limitations de la gestion des dépendances

* **Les hooks se déclenchent pour toutes les sessions** : Les hooks SessionStart s'exécutent dans les environnements locaux et distants. Il n'y a pas de configuration de hook pour limiter un hook aux sessions distantes uniquement. Pour ignorer l'exécution locale, vérifiez la variable d'environnement `CLAUDE_CODE_REMOTE` dans votre script comme indiqué ci-dessus.
* **Nécessite un accès réseau** : Les commandes d'installation ont besoin d'un accès réseau pour atteindre les registres de paquets. Si votre environnement est configuré avec un accès « Pas d'Internet », ces hooks échoueront. Utilisez l'accès réseau « Limité » (par défaut) ou « Complet ». La [liste d'autorisation par défaut](#default-allowed-domains) inclut les registres courants comme npm, PyPI, RubyGems et crates.io.
* **Compatibilité du proxy** : Tout le trafic sortant dans les environnements distants passe par un [proxy de sécurité](#security-proxy). Certains gestionnaires de paquets ne fonctionnent pas correctement avec ce proxy. Bun est un exemple connu.
* **S'exécute à chaque démarrage de session** : Les hooks s'exécutent chaque fois qu'une session démarre ou reprend, ajoutant une latence de démarrage. Gardez les scripts d'installation rapides en vérifiant si les dépendances sont déjà présentes avant de les réinstaller.

## Accès réseau et sécurité

### Politique réseau

#### Proxy GitHub

Pour la sécurité, toutes les opérations GitHub passent par un service proxy dédié qui gère de manière transparente toutes les interactions git. À l'intérieur du sandbox, le client git s'authentifie à l'aide d'une identité personnalisée limitée. Ce proxy :

* Gère l'authentification GitHub de manière sécurisée - le client git utilise une identité limitée à l'intérieur du sandbox, que le proxy vérifie et traduit en votre jeton d'authentification GitHub réel
* Restreint les opérations de poussée git à la branche de travail actuelle pour la sécurité
* Permet le clonage, la récupération et les opérations PR transparentes tout en maintenant les limites de sécurité

#### Proxy de sécurité

Les environnements s'exécutent derrière un proxy réseau HTTP/HTTPS pour la sécurité et la prévention des abus. Tout le trafic Internet sortant passe par ce proxy, qui fournit :

* Protection contre les demandes malveillantes
* Limitation de débit et prévention des abus
* Filtrage de contenu pour une sécurité renforcée

### Niveaux d'accès

Par défaut, l'accès réseau est limité aux [domaines autorisés](#default-allowed-domains).

Vous pouvez configurer un accès réseau personnalisé, y compris la désactivation de l'accès réseau.

### Domaines autorisés par défaut

Lors de l'utilisation de l'accès réseau « Limité », les domaines suivants sont autorisés par défaut :

#### Services Anthropic

* api.anthropic.com
* statsig.anthropic.com
* platform.claude.com
* code.claude.com
* claude.ai

#### Contrôle de version

* github.com
* [www.github.com](http://www.github.com)
* api.github.com
* npm.pkg.github.com
* raw\.githubusercontent.com
* pkg-npm.githubusercontent.com
* objects.githubusercontent.com
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

#### Registres de conteneurs

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

#### Plateformes cloud

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

#### Gestionnaires de paquets - JavaScript/Node

* registry.npmjs.org
* [www.npmjs.com](http://www.npmjs.com)
* [www.npmjs.org](http://www.npmjs.org)
* npmjs.com
* npmjs.org
* yarnpkg.com
* registry.yarnpkg.com

#### Gestionnaires de paquets - Python

* pypi.org
* [www.pypi.org](http://www.pypi.org)
* files.pythonhosted.org
* pythonhosted.org
* test.pypi.org
* pypi.python.org
* pypa.io
* [www.pypa.io](http://www.pypa.io)

#### Gestionnaires de paquets - Ruby

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

#### Gestionnaires de paquets - Rust

* crates.io
* [www.crates.io](http://www.crates.io)
* index.crates.io
* static.crates.io
* rustup.rs
* static.rust-lang.org
* [www.rust-lang.org](http://www.rust-lang.org)

#### Gestionnaires de paquets - Go

* proxy.golang.org
* sum.golang.org
* index.golang.org
* golang.org
* [www.golang.org](http://www.golang.org)
* goproxy.io
* pkg.go.dev

#### Gestionnaires de paquets - JVM

* maven.org
* repo.maven.org
* central.maven.org
* repo1.maven.org
* jcenter.bintray.com
* gradle.org
* [www.gradle.org](http://www.gradle.org)
* services.gradle.org
* plugins.gradle.org
* kotlin.org
* [www.kotlin.org](http://www.kotlin.org)
* spring.io
* repo.spring.io

#### Gestionnaires de paquets - Autres langages

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

#### Distributions Linux

* archive.ubuntu.com
* security.ubuntu.com
* ubuntu.com
* [www.ubuntu.com](http://www.ubuntu.com)
* \*.ubuntu.com
* ppa.launchpad.net
* launchpad.net
* [www.launchpad.net](http://www.launchpad.net)

#### Outils de développement et plateformes

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

#### Services cloud et surveillance

* statsig.com
* [www.statsig.com](http://www.statsig.com)
* api.statsig.com
* sentry.io
* \*.sentry.io
* http-intake.logs.datadoghq.com
* \*.datadoghq.com
* \*.datadoghq.eu

#### Livraison de contenu et miroirs

* sourceforge.net
* \*.sourceforge.net
* packagecloud.io
* \*.packagecloud.io

#### Schéma et configuration

* json-schema.org
* [www.json-schema.org](http://www.json-schema.org)
* json.schemastore.org
* [www.schemastore.org](http://www.schemastore.org)

#### Model Context Protocol

* \*.modelcontextprotocol.io

<Note>
  Les domaines marqués avec `*` indiquent une correspondance de sous-domaine générique. Par exemple, `*.gcr.io` permet l'accès à n'importe quel sous-domaine de `gcr.io`.
</Note>

### Meilleures pratiques de sécurité pour l'accès réseau personnalisé

1. **Principe du moindre privilège** : N'activez que l'accès réseau minimum requis
2. **Auditez régulièrement** : Examinez les domaines autorisés périodiquement
3. **Utilisez HTTPS** : Préférez toujours les points de terminaison HTTPS à HTTP

## Sécurité et isolation

Claude Code sur le web fournit des garanties de sécurité fortes :

* **Machines virtuelles isolées** : Chaque session s'exécute dans une VM isolée gérée par Anthropic
* **Contrôles d'accès réseau** : L'accès réseau est limité par défaut et peut être désactivé

<Note>
  Lors de l'exécution avec l'accès réseau désactivé, Claude Code est autorisé à communiquer avec l'API Anthropic, ce qui peut toujours permettre aux données de quitter la VM Claude Code isolée.
</Note>

* **Protection des identifiants** : Les identifiants sensibles (tels que les identifiants git ou les clés de signature) ne sont jamais à l'intérieur du sandbox avec Claude Code. L'authentification est gérée via un proxy sécurisé utilisant des identifiants limités
* **Analyse sécurisée** : Le code est analysé et modifié dans des VM isolées avant la création de PR

## Tarification et limites de débit

Claude Code sur le web partage les limites de débit avec tous les autres usages de Claude et Claude Code au sein de votre compte. L'exécution de plusieurs tâches en parallèle consommera proportionnellement plus de limites de débit.

## Limitations

* **Authentification du référentiel** : Vous ne pouvez déplacer les sessions du web vers le local que lorsque vous êtes authentifié au même compte
* **Restrictions de plateforme** : Claude Code sur le web ne fonctionne qu'avec le code hébergé sur GitHub. Les référentiels non-GitHub comme GitLab ne peuvent pas être utilisés avec les sessions cloud

## Meilleures pratiques

1. **Automatisez la configuration de l'environnement** : Utilisez les [scripts de configuration](#setup-scripts) pour installer les dépendances et configurer les outils avant le lancement de Claude Code. Pour les scénarios plus avancés, configurez les [hooks SessionStart](/fr/hooks#sessionstart).
2. **Documentez les exigences** : Spécifiez clairement les dépendances et les commandes dans votre fichier `CLAUDE.md`. Si vous avez un fichier `AGENTS.md`, vous pouvez le sourcer dans votre `CLAUDE.md` en utilisant `@AGENTS.md` pour maintenir une source unique de vérité.

## Ressources connexes

* [Configuration des hooks](/fr/hooks)
* [Référence des paramètres](/fr/settings)
* [Sécurité](/fr/security)
* [Utilisation des données](/fr/data-usage)
