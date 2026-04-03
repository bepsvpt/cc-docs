> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurer les autorisations

> Contrôlez ce que Claude Code peut accéder et faire avec des règles d'autorisation granulaires, des modes et des politiques gérées.

Claude Code prend en charge les autorisations granulaires afin que vous puissiez spécifier exactement ce que l'agent est autorisé à faire et ce qu'il ne peut pas faire. Les paramètres d'autorisation peuvent être archivés dans le contrôle de version et distribués à tous les développeurs de votre organisation, ainsi que personnalisés par les développeurs individuels.

## Système d'autorisation

Claude Code utilise un système d'autorisation à plusieurs niveaux pour équilibrer la puissance et la sécurité :

| Type d'outil            | Exemple                      | Approbation requise | Comportement « Oui, ne pas demander à nouveau » |
| :---------------------- | :--------------------------- | :------------------ | :---------------------------------------------- |
| Lecture seule           | Lectures de fichiers, Grep   | Non                 | S/O                                             |
| Commandes Bash          | Exécution shell              | Oui                 | Permanent par répertoire de projet et commande  |
| Modification de fichier | Édition/écriture de fichiers | Oui                 | Jusqu'à la fin de la session                    |

## Gérer les autorisations

Vous pouvez afficher et gérer les autorisations d'outils de Claude Code avec `/permissions`. Cette interface utilisateur répertorie toutes les règles d'autorisation et le fichier settings.json dont elles proviennent.

* Les règles **Allow** permettent à Claude Code d'utiliser l'outil spécifié sans approbation manuelle.
* Les règles **Ask** demandent une confirmation chaque fois que Claude Code essaie d'utiliser l'outil spécifié.
* Les règles **Deny** empêchent Claude Code d'utiliser l'outil spécifié.

Les règles sont évaluées dans l'ordre : **deny -> ask -> allow**. La première règle correspondante gagne, donc les règles de refus ont toujours la priorité.

## Modes d'autorisation

Claude Code prend en charge plusieurs modes d'autorisation qui contrôlent la façon dont les outils sont approuvés. Consultez [Modes d'autorisation](/fr/permission-modes) pour savoir quand utiliser chacun. Définissez le `defaultMode` dans vos [fichiers de paramètres](/fr/settings#settings-files) :

| Mode                | Description                                                                                                                                                                                      |
| :------------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Comportement standard : demande une autorisation à la première utilisation de chaque outil                                                                                                       |
| `acceptEdits`       | Accepte automatiquement les autorisations d'édition de fichiers pour la session, sauf les écritures dans les répertoires protégés                                                                |
| `plan`              | Plan Mode : Claude peut analyser mais pas modifier les fichiers ou exécuter les commandes                                                                                                        |
| `auto`              | Approuve automatiquement les appels d'outils avec des vérifications de sécurité en arrière-plan qui vérifient que les actions s'alignent avec votre demande. Actuellement un aperçu de recherche |
| `dontAsk`           | Refuse automatiquement les outils sauf s'ils sont pré-approuvés via `/permissions` ou les règles `permissions.allow`                                                                             |
| `bypassPermissions` | Ignore les invites d'autorisation sauf pour les écritures dans les répertoires protégés (voir l'avertissement ci-dessous)                                                                        |

<Warning>
  Le mode `bypassPermissions` ignore les invites d'autorisation. Les écritures dans les répertoires `.git`, `.claude`, `.vscode`, `.idea` et `.husky` demandent toujours une confirmation pour éviter la corruption accidentelle de l'état du référentiel, de la configuration de l'éditeur et des hooks git. Les écritures dans `.claude/commands`, `.claude/agents` et `.claude/skills` sont exemptées et ne demandent pas, car Claude écrit régulièrement là lors de la création de skills, de subagents et de commandes. Utilisez ce mode uniquement dans des environnements isolés comme les conteneurs ou les machines virtuelles où Claude Code ne peut pas causer de dommages. Les administrateurs peuvent empêcher ce mode en définissant `permissions.disableBypassPermissionsMode` sur `"disable"` dans les [paramètres gérés](#managed-settings).
</Warning>

Pour empêcher le mode `bypassPermissions` ou `auto` d'être utilisé, définissez `permissions.disableBypassPermissionsMode` ou `permissions.disableAutoMode` sur `"disable"` dans n'importe quel [fichier de paramètres](/fr/settings#settings-files). Ces paramètres sont particulièrement utiles dans les [paramètres gérés](#managed-settings) où ils ne peuvent pas être remplacés.

## Syntaxe des règles d'autorisation

Les règles d'autorisation suivent le format `Tool` ou `Tool(specifier)`.

### Correspondre à tous les usages d'un outil

Pour correspondre à tous les usages d'un outil, utilisez simplement le nom de l'outil sans parenthèses :

| Règle      | Effet                                                |
| :--------- | :--------------------------------------------------- |
| `Bash`     | Correspond à toutes les commandes Bash               |
| `WebFetch` | Correspond à toutes les demandes de récupération web |
| `Read`     | Correspond à toutes les lectures de fichiers         |

`Bash(*)` est équivalent à `Bash` et correspond à toutes les commandes Bash.

### Utiliser des spécificateurs pour un contrôle granulaire

Ajoutez un spécificateur entre parenthèses pour correspondre à des usages d'outils spécifiques :

| Règle                          | Effet                                                                |
| :----------------------------- | :------------------------------------------------------------------- |
| `Bash(npm run build)`          | Correspond à la commande exacte `npm run build`                      |
| `Read(./.env)`                 | Correspond à la lecture du fichier `.env` dans le répertoire courant |
| `WebFetch(domain:example.com)` | Correspond aux demandes de récupération vers example.com             |

### Modèles de caractères génériques

Les règles Bash prennent en charge les modèles glob avec `*`. Les caractères génériques peuvent apparaître à n'importe quelle position dans la commande. Cette configuration permet les commandes npm et git commit tout en bloquant git push :

```json  theme={null}
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)",
      "Bash(* --version)",
      "Bash(* --help *)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

L'espace avant `*` est important : `Bash(ls *)` correspond à `ls -la` mais pas à `lsof`, tandis que `Bash(ls*)` correspond aux deux. La syntaxe du suffixe `:*` hérité est équivalente à ` *` mais est dépréciée.

## Règles d'autorisation spécifiques aux outils

### Bash

Les règles d'autorisation Bash prennent en charge la correspondance de caractères génériques avec `*`. Les caractères génériques peuvent apparaître à n'importe quelle position dans la commande, y compris au début, au milieu ou à la fin :

* `Bash(npm run build)` correspond à la commande Bash exacte `npm run build`
* `Bash(npm run test *)` correspond aux commandes Bash commençant par `npm run test`
* `Bash(npm *)` correspond à toute commande commençant par `npm `
* `Bash(* install)` correspond à toute commande se terminant par ` install`
* `Bash(git * main)` correspond à des commandes comme `git checkout main`, `git merge main`

Lorsque `*` apparaît à la fin avec un espace avant (comme `Bash(ls *)`), il applique une limite de mot, exigeant que le préfixe soit suivi d'un espace ou de la fin de la chaîne. Par exemple, `Bash(ls *)` correspond à `ls -la` mais pas à `lsof`. En contraste, `Bash(ls*)` sans espace correspond aux deux `ls -la` et `lsof` car il n'y a pas de contrainte de limite de mot.

<Tip>
  Claude Code est conscient des opérateurs shell (comme `&&`) donc une règle de correspondance de préfixe comme `Bash(safe-cmd *)` ne lui donnera pas la permission d'exécuter la commande `safe-cmd && other-cmd`.
</Tip>

Lorsque vous approuvez une commande composée avec « Oui, ne pas demander à nouveau », Claude Code enregistre une règle séparée pour chaque sous-commande qui nécessite une approbation, plutôt qu'une seule règle pour la chaîne complète. Par exemple, approuver `git status && npm test` enregistre une règle pour `npm test`, donc les invocations futures de `npm test` sont reconnues indépendamment de ce qui précède le `&&`. Les sous-commandes comme `cd` dans un sous-répertoire génèrent leur propre règle Read pour ce chemin. Jusqu'à 5 règles peuvent être enregistrées pour une seule commande composée.

<Warning>
  Les modèles d'autorisation Bash qui tentent de contraindre les arguments de commande sont fragiles. Par exemple, `Bash(curl http://github.com/ *)` a l'intention de restreindre curl aux URL GitHub, mais ne correspondra pas aux variations comme :

  * Options avant l'URL : `curl -X GET http://github.com/...`
  * Protocole différent : `curl https://github.com/...`
  * Redirections : `curl -L http://bit.ly/xyz` (redirige vers github)
  * Variables : `URL=http://github.com && curl $URL`
  * Espaces supplémentaires : `curl  http://github.com`

  Pour un filtrage d'URL plus fiable, envisagez :

  * **Restreindre les outils réseau Bash** : utilisez les règles de refus pour bloquer `curl`, `wget` et les commandes similaires, puis utilisez l'outil WebFetch avec l'autorisation `WebFetch(domain:github.com)` pour les domaines autorisés
  * **Utiliser les hooks PreToolUse** : implémentez un hook qui valide les URL dans les commandes Bash et bloque les domaines non autorisés
  * Instruire Claude Code sur vos modèles curl autorisés via CLAUDE.md

  Notez que l'utilisation de WebFetch seul n'empêche pas l'accès au réseau. Si Bash est autorisé, Claude peut toujours utiliser `curl`, `wget` ou d'autres outils pour atteindre n'importe quelle URL.
</Warning>

### Read et Edit

Les règles `Edit` s'appliquent à tous les outils intégrés qui éditent les fichiers. Claude fait un effort raisonnable pour appliquer les règles `Read` à tous les outils intégrés qui lisent les fichiers comme Grep et Glob.

<Warning>
  Les règles de refus Read et Edit s'appliquent aux outils de fichiers intégrés de Claude, pas aux sous-processus Bash. Une règle de refus `Read(./.env)` bloque l'outil Read mais n'empêche pas `cat .env` dans Bash. Pour une application au niveau du système d'exploitation qui bloque tous les processus d'accéder à un chemin, [activez le sandbox](/fr/sandboxing).
</Warning>

Les règles Read et Edit suivent toutes deux la spécification [gitignore](https://git-scm.com/docs/gitignore) avec quatre types de modèles distincts :

| Modèle             | Signification                                                  | Exemple                          | Correspond                       |
| ------------------ | -------------------------------------------------------------- | -------------------------------- | -------------------------------- |
| `//path`           | Chemin **absolu** à partir de la racine du système de fichiers | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`        |
| `~/path`           | Chemin à partir du répertoire **home**                         | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf`   |
| `/path`            | Chemin **relatif à la racine du projet**                       | `Edit(/src/**/*.ts)`             | `<racine du projet>/src/**/*.ts` |
| `path` ou `./path` | Chemin **relatif au répertoire courant**                       | `Read(*.env)`                    | `<cwd>/*.env`                    |

<Warning>
  Un modèle comme `/Users/alice/file` n'est PAS un chemin absolu. Il est relatif à la racine du projet. Utilisez `//Users/alice/file` pour les chemins absolus.
</Warning>

Sur Windows, les chemins sont normalisés en forme POSIX avant la correspondance. `C:\Users\alice` devient `/c/Users/alice`, donc utilisez `//c/**/.env` pour correspondre aux fichiers `.env` n'importe où sur ce lecteur. Pour correspondre sur tous les lecteurs, utilisez `//**/.env`.

Exemples :

* `Edit(/docs/**)` : édite dans `<projet>/docs/` (PAS `/docs/` et PAS `<projet>/.claude/docs/`)
* `Read(~/.zshrc)` : lit le `.zshrc` de votre répertoire home
* `Edit(//tmp/scratch.txt)` : édite le chemin absolu `/tmp/scratch.txt`
* `Read(src/**)` : lit à partir de `<répertoire courant>/src/`

<Note>
  Dans les modèles gitignore, `*` correspond aux fichiers dans un seul répertoire tandis que `**` correspond récursivement dans les répertoires. Pour autoriser tous les accès aux fichiers, utilisez simplement le nom de l'outil sans parenthèses : `Read`, `Edit` ou `Write`.
</Note>

### WebFetch

* `WebFetch(domain:example.com)` correspond aux demandes de récupération vers example.com

### MCP

* `mcp__puppeteer` correspond à tout outil fourni par le serveur `puppeteer` (nom configuré dans Claude Code)
* `mcp__puppeteer__*` syntaxe de caractère générique qui correspond également à tous les outils du serveur `puppeteer`
* `mcp__puppeteer__puppeteer_navigate` correspond à l'outil `puppeteer_navigate` fourni par le serveur `puppeteer`

### Agent (subagents)

Utilisez les règles `Agent(AgentName)` pour contrôler quels [subagents](/fr/sub-agents) Claude peut utiliser :

* `Agent(Explore)` correspond au subagent Explore
* `Agent(Plan)` correspond au subagent Plan
* `Agent(my-custom-agent)` correspond à un subagent personnalisé nommé `my-custom-agent`

Ajoutez ces règles au tableau `deny` dans vos paramètres ou utilisez l'indicateur CLI `--disallowedTools` pour désactiver des agents spécifiques. Pour désactiver l'agent Explore :

```json  theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## Étendre les autorisations avec des hooks

Les [hooks Claude Code](/fr/hooks-guide) fournissent un moyen d'enregistrer des commandes shell personnalisées pour effectuer l'évaluation des autorisations à l'exécution. Lorsque Claude Code effectue un appel d'outil, les hooks PreToolUse s'exécutent avant l'invite d'autorisation. La sortie du hook peut refuser l'appel d'outil, forcer une invite ou ignorer l'invite pour laisser l'appel se poursuivre.

Ignorer l'invite ne contourne pas les règles d'autorisation. Les règles de refus et de demande sont toujours évaluées après qu'un hook retourne `"allow"`, donc une règle de refus correspondante bloque toujours l'appel. Cela préserve la précédence de refus en premier décrite dans [Gérer les autorisations](#manage-permissions), y compris les règles de refus définies dans les paramètres gérés.

Un hook de blocage prend également la priorité sur les règles d'autorisation. Un hook qui se termine avec le code 2 arrête l'appel d'outil avant que les règles d'autorisation ne soient évaluées, donc le blocage s'applique même lorsqu'une règle d'autorisation permettrait autrement l'appel. Pour exécuter toutes les commandes Bash sans invites sauf pour quelques-unes que vous voulez bloquer, ajoutez `"Bash"` à votre liste d'autorisation et enregistrez un hook PreToolUse qui rejette ces commandes spécifiques. Consultez [Bloquer les éditions des fichiers protégés](/fr/hooks-guide#block-edits-to-protected-files) pour un script de hook que vous pouvez adapter.

## Répertoires de travail

Par défaut, Claude a accès aux fichiers du répertoire où il a été lancé. Vous pouvez étendre cet accès :

* **Au démarrage** : utilisez l'argument CLI `--add-dir <path>`
* **Pendant la session** : utilisez la commande `/add-dir`
* **Configuration persistante** : ajoutez à `additionalDirectories` dans les [fichiers de paramètres](/fr/settings#settings-files)

Les fichiers dans les répertoires supplémentaires suivent les mêmes règles d'autorisation que le répertoire de travail d'origine : ils deviennent lisibles sans invites, et les autorisations d'édition de fichiers suivent le mode d'autorisation actuel.

### Les répertoires supplémentaires accordent l'accès aux fichiers, pas la configuration

L'ajout d'un répertoire étend l'endroit où Claude peut lire et éditer les fichiers. Cela ne fait pas de ce répertoire une racine de configuration complète : la plupart de la configuration `.claude/` n'est pas découverte à partir de répertoires supplémentaires, bien que quelques types soient chargés comme exceptions.

Les types de configuration suivants sont chargés à partir des répertoires `--add-dir` :

| Configuration                                        | Chargé à partir de `--add-dir`                                                 |
| :--------------------------------------------------- | :----------------------------------------------------------------------------- |
| [Skills](/fr/skills) dans `.claude/skills/`          | Oui, avec rechargement en direct                                               |
| Paramètres de plugin dans `.claude/settings.json`    | `enabledPlugins` et `extraKnownMarketplaces` uniquement                        |
| Fichiers [CLAUDE.md](/fr/memory) et `.claude/rules/` | Uniquement lorsque `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` est défini |

Tout le reste, y compris les subagents, les commandes, les styles de sortie, les hooks et d'autres paramètres, est découvert uniquement à partir du répertoire de travail actuel et de ses parents, de votre répertoire utilisateur à `~/.claude/` et des paramètres gérés. Pour partager cette configuration entre les projets, utilisez l'une de ces approches :

* **Configuration au niveau utilisateur** : placez les fichiers dans `~/.claude/agents/`, `~/.claude/output-styles/` ou `~/.claude/settings.json` pour les rendre disponibles dans chaque projet
* **Plugins** : empaquetez et distribuez la configuration en tant que [plugin](/fr/plugins) que les équipes peuvent installer
* **Lancer à partir du répertoire de configuration** : exécutez Claude Code à partir du répertoire contenant la configuration `.claude/` que vous souhaitez

## Comment les autorisations interagissent avec le sandboxing

Les autorisations et le [sandboxing](/fr/sandboxing) sont des couches de sécurité complémentaires :

* **Les autorisations** contrôlent quels outils Claude Code peut utiliser et quels fichiers ou domaines il peut accéder. Elles s'appliquent à tous les outils (Bash, Read, Edit, WebFetch, MCP et autres).
* **Le sandboxing** fournit une application au niveau du système d'exploitation qui restreint l'accès du système de fichiers et du réseau de l'outil Bash. Il s'applique uniquement aux commandes Bash et à leurs processus enfants.

Utilisez les deux pour une défense en profondeur :

* Les règles de refus d'autorisation empêchent Claude d'essayer même d'accéder aux ressources restreintes
* Les restrictions de sandbox empêchent les commandes Bash d'atteindre les ressources en dehors des limites définies, même si une injection de prompt contourne la prise de décision de Claude
* Les restrictions du système de fichiers dans le sandbox utilisent les règles de refus Read et Edit, pas une configuration de sandbox séparée
* Les restrictions réseau combinent les règles d'autorisation WebFetch avec la liste `allowedDomains` du sandbox

## Paramètres gérés

Pour les organisations qui ont besoin d'un contrôle centralisé sur la configuration de Claude Code, les administrateurs peuvent déployer des paramètres gérés qui ne peuvent pas être remplacés par les paramètres utilisateur ou projet. Ces paramètres de politique suivent le même format que les fichiers de paramètres réguliers et peuvent être livrés via des politiques MDM/au niveau du système d'exploitation, des fichiers de paramètres gérés ou des [paramètres gérés par le serveur](/fr/server-managed-settings). Consultez [fichiers de paramètres](/fr/settings#settings-files) pour les mécanismes de livraison et les emplacements de fichiers.

### Paramètres gérés uniquement

Les paramètres suivants ne sont efficaces que dans les paramètres gérés. Les placer dans les fichiers de paramètres utilisateur ou projet n'a aucun effet.

| Paramètre                                      | Description                                                                                                                                                                                                                                                                                              |
| :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowedChannelPlugins`                        | Liste blanche des plugins de canal qui peuvent envoyer des messages. Remplace la liste blanche Anthropic par défaut lorsqu'elle est définie. Nécessite `channelsEnabled: true`. Consultez [Restreindre les plugins de canal qui peuvent s'exécuter](/fr/channels#restrict-which-channel-plugins-can-run) |
| `allowManagedHooksOnly`                        | Lorsque `true`, empêche le chargement des hooks utilisateur, projet et plugin. Seuls les hooks gérés et les hooks SDK sont autorisés                                                                                                                                                                     |
| `allowManagedMcpServersOnly`                   | Lorsque `true`, seuls les `allowedMcpServers` des paramètres gérés sont respectés. `deniedMcpServers` fusionne toujours à partir de toutes les sources. Consultez [Configuration MCP gérée](/fr/mcp#managed-mcp-configuration)                                                                           |
| `allowManagedPermissionRulesOnly`              | Lorsque `true`, empêche les paramètres utilisateur et projet de définir les règles d'autorisation `allow`, `ask` ou `deny`. Seules les règles dans les paramètres gérés s'appliquent                                                                                                                     |
| `blockedMarketplaces`                          | Liste noire des sources de marketplace. Les sources bloquées sont vérifiées avant le téléchargement, elles ne touchent donc jamais le système de fichiers. Consultez [restrictions de marketplace gérées](/fr/plugin-marketplaces#managed-marketplace-restrictions)                                      |
| `channelsEnabled`                              | Autoriser les [canaux](/fr/channels) pour les utilisateurs Team et Enterprise. Non défini ou `false` bloque la livraison des messages de canal indépendamment de ce que les utilisateurs passent à `--channels`                                                                                          |
| `pluginTrustMessage`                           | Message personnalisé ajouté à l'avertissement de confiance du plugin affiché avant l'installation                                                                                                                                                                                                        |
| `sandbox.filesystem.allowManagedReadPathsOnly` | Lorsque `true`, seuls les chemins `filesystem.allowRead` des paramètres gérés sont respectés. `denyRead` fusionne toujours à partir de toutes les sources                                                                                                                                                |
| `sandbox.network.allowManagedDomainsOnly`      | Lorsque `true`, seuls les `allowedDomains` et les règles d'autorisation `WebFetch(domain:...)` des paramètres gérés sont respectés. Les domaines non autorisés sont bloqués automatiquement sans inviter l'utilisateur. Les domaines refusés fusionnent toujours à partir de toutes les sources          |
| `strictKnownMarketplaces`                      | Contrôle quels marketplaces de plugins les utilisateurs peuvent ajouter. Consultez [restrictions de marketplace gérées](/fr/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                        |

`disableBypassPermissionsMode` est généralement placé dans les paramètres gérés pour appliquer la politique organisationnelle, mais il fonctionne à partir de n'importe quelle portée. Un utilisateur peut le définir dans ses propres paramètres pour se verrouiller hors du mode de contournement.

<Note>
  L'accès à [Remote Control](/fr/remote-control) et aux [sessions web](/fr/claude-code-on-the-web) n'est pas contrôlé par une clé de paramètres gérés. Sur les plans Team et Enterprise, un administrateur active ou désactive ces fonctionnalités dans les [paramètres d'administration Claude Code](https://claude.ai/admin-settings/claude-code).
</Note>

## Examiner les refus du mode auto

Lorsque le [mode auto](/fr/permission-modes#eliminate-prompts-with-auto-mode) refuse un appel d'outil, une notification apparaît et l'action refusée est enregistrée dans `/permissions` sous l'onglet Récemment refusé. Appuyez sur `r` sur une action refusée pour la marquer pour réessai : lorsque vous quittez la boîte de dialogue, Claude Code envoie un message indiquant au modèle qu'il peut réessayer cet appel d'outil et reprend la conversation.

Pour réagir aux refus par programmation, utilisez le [hook `PermissionDenied`](/fr/hooks#permissiondenied).

## Configurer le classificateur du mode auto

Le [mode auto](/fr/permission-modes#eliminate-prompts-with-auto-mode) utilise un modèle de classificateur pour décider si chaque action est sûre à exécuter sans inviter. Par défaut, il ne fait confiance qu'au répertoire de travail et, s'il est présent, aux remotes du référentiel actuel. Les actions comme pousser vers l'organisation de contrôle de source de votre entreprise ou écrire dans un bucket cloud d'équipe seront bloquées comme exfiltration de données potentielle. Le bloc de paramètres `autoMode` vous permet de dire au classificateur quelle infrastructure votre organisation approuve.

Le classificateur lit `autoMode` à partir des paramètres utilisateur, `.claude/settings.local.json` et des paramètres gérés. Il ne lit pas à partir des paramètres de projet partagés dans `.claude/settings.json`, car un référentiel archivé pourrait autrement injecter ses propres règles d'autorisation.

| Portée                        | Fichier                       | Utiliser pour                                              |
| :---------------------------- | :---------------------------- | :--------------------------------------------------------- |
| Un développeur                | `~/.claude/settings.json`     | Infrastructure approuvée personnelle                       |
| Un projet, un développeur     | `.claude/settings.local.json` | Buckets ou services approuvés par projet, gitignored       |
| À l'échelle de l'organisation | Paramètres gérés              | Infrastructure approuvée appliquée à tous les développeurs |

Les entrées de chaque portée sont combinées. Un développeur peut étendre `environment`, `allow` et `soft_deny` avec des entrées personnelles mais ne peut pas supprimer les entrées que les paramètres gérés fournissent. Parce que les règles d'autorisation agissent comme des exceptions aux règles de blocage à l'intérieur du classificateur, une entrée `allow` ajoutée par un développeur peut remplacer une entrée `soft_deny` d'organisation : la combinaison est additive, pas une limite de politique dure. Si vous avez besoin d'une règle que les développeurs ne peuvent pas contourner, utilisez plutôt `permissions.deny` dans les paramètres gérés, qui bloque les actions avant que le classificateur ne soit consulté.

### Définir l'infrastructure approuvée

Pour la plupart des organisations, `autoMode.environment` est le seul champ que vous devez définir. Il dit au classificateur quels référentiels, buckets et domaines sont approuvés, sans toucher aux règles de blocage et d'autorisation intégrées. Le classificateur utilise `environment` pour décider ce que signifie « externe » : toute destination non listée est une cible d'exfiltration potentielle.

```json  theme={null}
{
  "autoMode": {
    "environment": [
      "Source control: github.example.com/acme-corp and all repos under it",
      "Trusted cloud buckets: s3://acme-build-artifacts, gs://acme-ml-datasets",
      "Trusted internal domains: *.corp.example.com, api.internal.example.com",
      "Key internal services: Jenkins at ci.example.com, Artifactory at artifacts.example.com"
    ]
  }
}
```

Les entrées sont en prose, pas en regex ou en modèles d'outils. Le classificateur les lit comme des règles en langage naturel. Écrivez-les comme vous décririez votre infrastructure à un nouvel ingénieur. Une section d'environnement approfondie couvre :

* **Organisation** : le nom de votre entreprise et ce pour quoi Claude Code est principalement utilisé, comme le développement logiciel, l'automatisation de l'infrastructure ou l'ingénierie des données
* **Contrôle de source** : chaque organisation GitHub, GitLab ou Bitbucket vers laquelle vos développeurs poussent
* **Fournisseurs cloud et buckets approuvés** : noms de buckets ou préfixes que Claude devrait pouvoir lire et écrire
* **Domaines internes approuvés** : noms d'hôtes pour les API, tableaux de bord et services à l'intérieur de votre réseau, comme `*.internal.example.com`
* **Services internes clés** : CI, registres d'artefacts, index de packages internes, outils d'incident
* **Contexte supplémentaire** : contraintes d'industrie réglementée, infrastructure multi-locataire ou exigences de conformité qui affectent ce que le classificateur devrait traiter comme risqué

Un modèle de démarrage utile : remplissez les champs entre crochets et supprimez les lignes qui ne s'appliquent pas :

```json  theme={null}
{
  "autoMode": {
    "environment": [
      "Organization: {COMPANY_NAME}. Primary use: {PRIMARY_USE_CASE, e.g. software development, infrastructure automation}",
      "Source control: {SOURCE_CONTROL, e.g. GitHub org github.example.com/acme-corp}",
      "Cloud provider(s): {CLOUD_PROVIDERS, e.g. AWS, GCP, Azure}",
      "Trusted cloud buckets: {TRUSTED_BUCKETS, e.g. s3://acme-builds, gs://acme-datasets}",
      "Trusted internal domains: {TRUSTED_DOMAINS, e.g. *.internal.example.com, api.example.com}",
      "Key internal services: {SERVICES, e.g. Jenkins at ci.example.com, Artifactory at artifacts.example.com}",
      "Additional context: {EXTRA, e.g. regulated industry, multi-tenant infrastructure, compliance requirements}"
    ]
  }
}
```

Plus le contexte spécifique que vous donnez, mieux le classificateur peut distinguer les opérations internes de routine des tentatives d'exfiltration.

Vous n'avez pas besoin de tout remplir à la fois. Un déploiement raisonnable : commencez par les paramètres par défaut et ajoutez votre organisation de contrôle de source et vos services internes clés, ce qui résout les faux positifs les plus courants comme pousser vers vos propres référentiels. Ajoutez ensuite les domaines approuvés et les buckets cloud. Remplissez le reste à mesure que les blocages se produisent.

### Remplacer les règles de blocage et d'autorisation

Deux champs supplémentaires vous permettent de remplacer les listes de règles intégrées du classificateur : `autoMode.soft_deny` contrôle ce qui est bloqué, et `autoMode.allow` contrôle quelles exceptions s'appliquent. Chacun est un tableau de descriptions en prose, lu comme des règles en langage naturel.

À l'intérieur du classificateur, la précédence est : les règles `soft_deny` bloquent d'abord, puis les règles `allow` remplacent comme exceptions, puis l'intention explicite de l'utilisateur remplace les deux. Si le message de l'utilisateur décrit directement et spécifiquement l'action exacte que Claude est sur le point d'entreprendre, le classificateur l'autorise même si une règle `soft_deny` correspond. Les demandes générales ne comptent pas : demander à Claude de « nettoyer le référentiel » n'autorise pas un force-push, mais demander à Claude de « force-push cette branche » le fait.

Pour assouplir : supprimez les règles de `soft_deny` lorsque les paramètres par défaut bloquent quelque chose que votre pipeline protège déjà avec l'examen des PR, CI ou les environnements de staging, ou ajoutez à `allow` lorsque le classificateur signale à plusieurs reprises un modèle de routine que les exceptions par défaut ne couvrent pas. Pour renforcer : ajoutez à `soft_deny` pour les risques spécifiques à votre environnement que les paramètres par défaut manquent, ou supprimez de `allow` pour maintenir une exception par défaut aux règles de blocage. Dans tous les cas, exécutez `claude auto-mode defaults` pour obtenir les listes par défaut complètes, puis copiez et modifiez : ne commencez jamais par une liste vide.

```json  theme={null}
{
  "autoMode": {
    "environment": [
      "Source control: github.example.com/acme-corp and all repos under it"
    ],
    "allow": [
      "Deploying to the staging namespace is allowed: staging is isolated from production and resets nightly",
      "Writing to s3://acme-scratch/ is allowed: ephemeral bucket with a 7-day lifecycle policy"
    ],
    "soft_deny": [
      "Never run database migrations outside the migrations CLI, even against dev databases",
      "Never modify files under infra/terraform/prod/: production infrastructure changes go through the review workflow",
      "...copy full default soft_deny list here first, then add your rules..."
    ]
  }
}
```

<Danger>
  Définir `allow` ou `soft_deny` remplace la liste par défaut entière pour cette section. Si vous définissez `soft_deny` avec une seule entrée, chaque règle de blocage intégrée est supprimée : force push, exfiltration de données, `curl | bash`, déploiements de production et toutes les autres règles de blocage par défaut deviennent autorisés. Pour personnaliser en toute sécurité, exécutez `claude auto-mode defaults` pour imprimer les règles intégrées, copiez-les dans votre fichier de paramètres, puis examinez chaque règle par rapport à votre propre pipeline et tolérance au risque. Supprimez uniquement les règles pour les risques que votre infrastructure atténue déjà.
</Danger>

Les trois sections sont évaluées indépendamment, donc définir `environment` seul laisse les listes `allow` et `soft_deny` par défaut intactes.

### Inspecter les paramètres par défaut et votre configuration effective

Parce que définir `allow` ou `soft_deny` remplace les paramètres par défaut, commencez toute personnalisation en copiant les listes par défaut complètes. Trois sous-commandes CLI vous aident à inspecter et valider :

```bash  theme={null}
claude auto-mode defaults  # the built-in environment, allow, and soft_deny rules
claude auto-mode config    # what the classifier actually uses: your settings where set, defaults otherwise
claude auto-mode critique  # get AI feedback on your custom allow and soft_deny rules
```

Enregistrez la sortie de `claude auto-mode defaults` dans un fichier, modifiez les listes pour correspondre à votre politique et collez le résultat dans votre fichier de paramètres. Après l'enregistrement, exécutez `claude auto-mode config` pour confirmer que les règles effectives sont ce que vous attendez. Si vous avez écrit des règles personnalisées, `claude auto-mode critique` les examine et signale les entrées qui sont ambiguës, redondantes ou susceptibles de causer des faux positifs.

## Précédence des paramètres

Les règles d'autorisation suivent la même [précédence des paramètres](/fr/settings#settings-precedence) que tous les autres paramètres de Claude Code :

1. **Paramètres gérés** : ne peuvent pas être remplacés par aucun autre niveau, y compris les arguments de ligne de commande
2. **Arguments de ligne de commande** : remplacements de session temporaires
3. **Paramètres de projet local** (`.claude/settings.local.json`)
4. **Paramètres de projet partagés** (`.claude/settings.json`)
5. **Paramètres utilisateur** (`~/.claude/settings.json`)

Si un outil est refusé à n'importe quel niveau, aucun autre niveau ne peut l'autoriser. Par exemple, un refus de paramètres gérés ne peut pas être remplacé par `--allowedTools`, et `--disallowedTools` peut ajouter des restrictions au-delà de ce que les paramètres gérés définissent.

Si une autorisation est autorisée dans les paramètres utilisateur mais refusée dans les paramètres de projet, le paramètre de projet prend la priorité et l'autorisation est bloquée.

## Exemples de configurations

Ce [référentiel](https://github.com/anthropics/claude-code/tree/main/examples/settings) inclut des configurations de paramètres de démarrage pour les scénarios de déploiement courants. Utilisez-les comme points de départ et ajustez-les pour répondre à vos besoins.

## Voir aussi

* [Paramètres](/fr/settings) : référence de configuration complète incluant le tableau des paramètres d'autorisation
* [Sandboxing](/fr/sandboxing) : isolation du système de fichiers et du réseau au niveau du système d'exploitation pour les commandes Bash
* [Authentification](/fr/authentication) : configurer l'accès utilisateur à Claude Code
* [Sécurité](/fr/security) : garanties de sécurité et meilleures pratiques
* [Hooks](/fr/hooks-guide) : automatiser les flux de travail et étendre l'évaluation des autorisations
