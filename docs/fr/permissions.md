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

Claude Code prend en charge plusieurs modes d'autorisation qui contrôlent la façon dont les outils sont approuvés. Définissez le `defaultMode` dans vos [fichiers de paramètres](/fr/settings#settings-files) :

| Mode                | Description                                                                                                          |
| :------------------ | :------------------------------------------------------------------------------------------------------------------- |
| `default`           | Comportement standard : demande une autorisation à la première utilisation de chaque outil                           |
| `acceptEdits`       | Accepte automatiquement les autorisations d'édition de fichiers pour la session                                      |
| `plan`              | Plan Mode : Claude peut analyser mais pas modifier les fichiers ou exécuter les commandes                            |
| `dontAsk`           | Refuse automatiquement les outils sauf s'ils sont pré-approuvés via `/permissions` ou les règles `permissions.allow` |
| `bypassPermissions` | Ignore tous les invites d'autorisation (nécessite un environnement sûr, voir l'avertissement ci-dessous)             |

<Warning>
  Le mode `bypassPermissions` désactive tous les contrôles d'autorisation. Utilisez-le uniquement dans des environnements isolés comme les conteneurs ou les machines virtuelles où Claude Code ne peut pas causer de dommages. Les administrateurs peuvent empêcher ce mode en définissant `disableBypassPermissionsMode` sur `"disable"` dans les [paramètres gérés](#managed-settings).
</Warning>

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

Les [hooks Claude Code](/fr/hooks-guide) fournissent un moyen d'enregistrer des commandes shell personnalisées pour effectuer l'évaluation des autorisations à l'exécution. Lorsque Claude Code effectue un appel d'outil, les hooks PreToolUse s'exécutent avant le système d'autorisation, et la sortie du hook peut déterminer s'il faut approuver ou refuser l'appel d'outil à la place du système d'autorisation.

## Répertoires de travail

Par défaut, Claude a accès aux fichiers du répertoire où il a été lancé. Vous pouvez étendre cet accès :

* **Au démarrage** : utilisez l'argument CLI `--add-dir <path>`
* **Pendant la session** : utilisez la commande `/add-dir`
* **Configuration persistante** : ajoutez à `additionalDirectories` dans les [fichiers de paramètres](/fr/settings#settings-files)

Les fichiers dans les répertoires supplémentaires suivent les mêmes règles d'autorisation que le répertoire de travail d'origine : ils deviennent lisibles sans invites, et les autorisations d'édition de fichiers suivent le mode d'autorisation actuel.

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

Pour les organisations qui ont besoin d'un contrôle centralisé sur la configuration de Claude Code, les administrateurs peuvent déployer des paramètres gérés qui ne peuvent pas être remplacés par les paramètres utilisateur ou projet. Ces paramètres de politique suivent le même format que les fichiers de paramètres réguliers et peuvent être livrés via des politiques MDM/au niveau du système d'exploitation, des fichiers de paramètres gérés ou des [paramètres gérés par le serveur](/fr/server-managed-settings). Voir [fichiers de paramètres](/fr/settings#settings-files) pour les mécanismes de livraison et les emplacements de fichiers.

### Paramètres gérés uniquement

Certains paramètres ne sont efficaces que dans les paramètres gérés :

| Paramètre                                 | Description                                                                                                                                                                                                                                                                                     |
| :---------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode`            | Définissez sur `"disable"` pour empêcher le mode `bypassPermissions` et l'indicateur `--dangerously-skip-permissions`                                                                                                                                                                           |
| `allowManagedPermissionRulesOnly`         | Lorsque `true`, empêche les paramètres utilisateur et projet de définir les règles d'autorisation `allow`, `ask` ou `deny`. Seules les règles dans les paramètres gérés s'appliquent                                                                                                            |
| `allowManagedHooksOnly`                   | Lorsque `true`, empêche le chargement des hooks utilisateur, projet et plugin. Seuls les hooks gérés et les hooks SDK sont autorisés                                                                                                                                                            |
| `allowManagedMcpServersOnly`              | Lorsque `true`, seuls les `allowedMcpServers` des paramètres gérés sont respectés. `deniedMcpServers` fusionne toujours à partir de toutes les sources. Voir [Configuration MCP gérée](/fr/mcp#managed-mcp-configuration)                                                                       |
| `blockedMarketplaces`                     | Liste de blocage des sources de marketplace. Les sources bloquées sont vérifiées avant le téléchargement, elles ne touchent donc jamais le système de fichiers. Voir [restrictions de marketplace gérées](/fr/plugin-marketplaces#managed-marketplace-restrictions)                             |
| `sandbox.network.allowManagedDomainsOnly` | Lorsque `true`, seuls les `allowedDomains` et les règles d'autorisation `WebFetch(domain:...)` des paramètres gérés sont respectés. Les domaines non autorisés sont bloqués automatiquement sans inviter l'utilisateur. Les domaines refusés fusionnent toujours à partir de toutes les sources |
| `strictKnownMarketplaces`                 | Contrôle quels marketplaces de plugins les utilisateurs peuvent ajouter. Voir [restrictions de marketplace gérées](/fr/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                    |
| `allow_remote_sessions`                   | Lorsque `true`, permet aux utilisateurs de démarrer [Remote Control](/fr/remote-control) et les [sessions web](/fr/claude-code-on-the-web). Par défaut `true`. Définissez sur `false` pour empêcher l'accès aux sessions distantes                                                              |

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
