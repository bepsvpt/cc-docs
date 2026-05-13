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

<Note>
  Les règles d'autorisation sont appliquées par Claude Code, et non par le modèle. Les instructions dans votre prompt ou `CLAUDE.md` façonnent ce que Claude essaie de faire, mais elles ne changent pas ce que Claude Code autorise. Pour accorder ou révoquer l'accès, utilisez `/permissions`, les règles décrites ici, un [mode d'autorisation](/fr/permission-modes), ou un [hook PreToolUse](#extend-permissions-with-hooks).
</Note>

## Modes d'autorisation

Claude Code prend en charge plusieurs modes d'autorisation qui contrôlent la façon dont les outils sont approuvés. Consultez [Modes d'autorisation](/fr/permission-modes) pour savoir quand utiliser chacun. Définissez le `defaultMode` dans vos [fichiers de paramètres](/fr/settings#settings-files) :

| Mode                | Description                                                                                                                                                                                                    |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Comportement standard : demande une autorisation à la première utilisation de chaque outil                                                                                                                     |
| `acceptEdits`       | Accepte automatiquement les éditions de fichiers et les commandes courantes du système de fichiers (`mkdir`, `touch`, `mv`, `cp`, etc.) pour les chemins du répertoire de travail ou `additionalDirectories`   |
| `plan`              | Plan Mode : Claude lit les fichiers et exécute les commandes shell en lecture seule pour explorer mais n'édite pas vos fichiers source                                                                         |
| `auto`              | Approuve automatiquement les appels d'outils avec des vérifications de sécurité en arrière-plan qui vérifient que les actions s'alignent avec votre demande. Actuellement un aperçu de recherche               |
| `dontAsk`           | Refuse automatiquement les outils sauf s'ils sont pré-approuvés via `/permissions` ou les règles `permissions.allow`                                                                                           |
| `bypassPermissions` | Ignore tous les invites d'autorisation. Les suppressions ciblant la racine du système de fichiers ou le répertoire personnel, comme `rm -rf /` et `rm -rf ~`, demandent toujours comme disjoncteur de sécurité |

<Warning>
  Le mode `bypassPermissions` ignore tous les invites d'autorisation, y compris les écritures dans `.git`, `.claude`, `.vscode`, `.idea` et `.husky`. Les suppressions ciblant la racine du système de fichiers ou le répertoire personnel, comme `rm -rf /` et `rm -rf ~`, demandent toujours comme disjoncteur de sécurité contre l'erreur du modèle. Utilisez ce mode uniquement dans des environnements isolés comme les conteneurs ou les machines virtuelles où Claude Code ne peut pas causer de dommages. Les administrateurs peuvent empêcher ce mode en définissant `permissions.disableBypassPermissionsMode` sur `"disable"` dans les [paramètres gérés](#managed-settings).
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

```json theme={null}
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

L'espace avant `*` est important : `Bash(ls *)` correspond à `ls -la` mais pas à `lsof`, tandis que `Bash(ls*)` correspond aux deux. Le suffixe `:*` est une façon équivalente d'écrire un caractère générique de fin, donc `Bash(ls:*)` correspond aux mêmes commandes que `Bash(ls *)`.

La boîte de dialogue d'autorisation écrit la forme séparée par des espaces lorsque vous sélectionnez « Oui, ne pas demander à nouveau » pour un préfixe de commande. La forme `:*` n'est reconnue qu'à la fin d'un modèle. Dans un modèle comme `Bash(git:* push)`, le deux-points est traité comme un caractère littéral et ne correspondra pas aux commandes git.

## Règles d'autorisation spécifiques aux outils

### Bash

Les règles d'autorisation Bash prennent en charge la correspondance de caractères génériques avec `*`. Les caractères génériques peuvent apparaître à n'importe quelle position dans la commande, y compris au début, au milieu ou à la fin :

* `Bash(npm run build)` correspond à la commande Bash exacte `npm run build`
* `Bash(npm run test *)` correspond aux commandes Bash commençant par `npm run test`
* `Bash(npm *)` correspond à toute commande commençant par `npm `
* `Bash(* install)` correspond à toute commande se terminant par ` install`
* `Bash(git * main)` correspond à des commandes comme `git checkout main` et `git log --oneline main`

Un seul `*` correspond à n'importe quelle séquence de caractères, y compris les espaces, donc un caractère générique peut s'étendre sur plusieurs arguments. `Bash(git *)` correspond à `git log --oneline --all`, et `Bash(git * main)` correspond à `git push origin main` ainsi qu'à `git merge main`.

Lorsque `*` apparaît à la fin avec un espace avant (comme `Bash(ls *)`), il applique une limite de mot, exigeant que le préfixe soit suivi d'un espace ou de la fin de la chaîne. Par exemple, `Bash(ls *)` correspond à `ls -la` mais pas à `lsof`. En contraste, `Bash(ls*)` sans espace correspond aux deux `ls -la` et `lsof` car il n'y a pas de contrainte de limite de mot.

#### Commandes composées

<Tip>
  Claude Code est conscient des opérateurs shell, donc une règle comme `Bash(safe-cmd *)` ne lui donnera pas la permission d'exécuter la commande `safe-cmd && other-cmd`. Les séparateurs de commande reconnus sont `&&`, `||`, `;`, `|`, `|&`, `&` et les sauts de ligne. Une règle doit correspondre à chaque sous-commande indépendamment.
</Tip>

Lorsque vous approuvez une commande composée avec « Oui, ne pas demander à nouveau », Claude Code enregistre une règle séparée pour chaque sous-commande qui nécessite une approbation, plutôt qu'une seule règle pour la chaîne complète. Par exemple, approuver `git status && npm test` enregistre une règle pour `npm test`, donc les invocations futures de `npm test` sont reconnues indépendamment de ce qui précède le `&&`. Les sous-commandes comme `cd` dans un sous-répertoire génèrent leur propre règle Read pour ce chemin. Jusqu'à 5 règles peuvent être enregistrées pour une seule commande composée.

#### Wrappers de processus

Avant de correspondre aux règles Bash, Claude Code supprime un ensemble fixe de wrappers de processus afin qu'une règle comme `Bash(npm test *)` corresponde également à `timeout 30 npm test`. Les wrappers reconnus sont `timeout`, `time`, `nice`, `nohup` et `stdbuf`.

Le `xargs` nu est également supprimé, donc `Bash(grep *)` correspond à `xargs grep pattern`. La suppression s'applique uniquement lorsque `xargs` n'a pas de drapeaux : une invocation comme `xargs -n1 grep pattern` est mise en correspondance en tant que commande `xargs`, donc les règles écrites pour la commande interne ne la couvrent pas.

Cette liste de wrappers est intégrée et n'est pas configurable. Les exécuteurs d'environnement de développement tels que `direnv exec`, `devbox run`, `mise exec`, `npx` et `docker exec` ne figurent pas dans la liste. Parce que ces outils exécutent leurs arguments en tant que commande, une règle comme `Bash(devbox run *)` correspond à tout ce qui vient après `run`, y compris `devbox run rm -rf .`. Pour approuver le travail à l'intérieur d'un exécuteur d'environnement, écrivez une règle spécifique qui inclut à la fois l'exécuteur et la commande interne, comme `Bash(devbox run npm test)`. Ajoutez une règle par commande interne que vous souhaitez autoriser.

Les wrappers exec tels que `watch`, `setsid`, `ionice` et `flock` demandent toujours et ne peuvent pas être approuvés automatiquement par une règle de préfixe comme `Bash(watch *)`. Il en va de même pour `find` avec `-exec` ou `-delete` : une règle `Bash(find *)` ne couvre pas ces formes. Pour approuver une invocation spécifique, écrivez une règle de correspondance exacte pour la chaîne de commande complète.

#### Commandes en lecture seule

Claude Code reconnaît un ensemble intégré de commandes Bash comme étant en lecture seule et les exécute sans invite d'autorisation dans tous les modes. Ceux-ci incluent `ls`, `cat`, `echo`, `pwd`, `head`, `tail`, `grep`, `find`, `wc`, `which`, `diff`, `stat`, `du`, `cd` et les formes en lecture seule de `git`. L'ensemble n'est pas configurable ; pour exiger une invite pour l'une de ces commandes, ajoutez une règle `ask` ou `deny` pour celle-ci.

Les modèles glob non cités sont autorisés pour les commandes dont chaque drapeau est en lecture seule, donc `ls *.ts` et `wc -l src/*.py` s'exécutent sans invite. Les commandes avec des drapeaux capables d'écriture ou d'exécution, tels que `find`, `sort`, `sed` et `git`, demandent toujours lorsqu'un glob non cité est présent car le glob pourrait s'étendre à un drapeau comme `-delete`.

Un `cd` dans un chemin à l'intérieur de votre répertoire de travail ou d'un [répertoire supplémentaire](#working-directories) est également en lecture seule. Une commande composée comme `cd packages/api && ls` s'exécute sans invite lorsque chaque partie se qualifie seule. La combinaison de `cd` avec `git` dans une seule commande composée demande toujours, indépendamment du répertoire cible.

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
  * **Ajouter des conseils CLAUDE.md** : décrivez vos modèles curl autorisés dans `CLAUDE.md`. Cela façonne ce que Claude essaie mais n'applique pas une limite, donc associez-le à l'une des options ci-dessus

  Notez que l'utilisation de WebFetch seul n'empêche pas l'accès au réseau. Si Bash est autorisé, Claude peut toujours utiliser `curl`, `wget` ou d'autres outils pour atteindre n'importe quelle URL.
</Warning>

### PowerShell

Les règles d'autorisation PowerShell utilisent la même forme que les règles Bash. Les caractères génériques avec `*` correspondent à n'importe quelle position, le suffixe `:*` est équivalent à un ` *` de fin, et un `PowerShell` nu ou `PowerShell(*)` correspond à chaque commande. Cette configuration permet les commandes `Get-ChildItem` et `git commit` tout en bloquant `Remove-Item` :

```json theme={null}
{
  "permissions": {
    "allow": [
      "PowerShell(Get-ChildItem *)",
      "PowerShell(git commit *)"
    ],
    "deny": [
      "PowerShell(Remove-Item *)"
    ]
  }
}
```

Les alias courants sont canonicalisés avant la correspondance. Une règle écrite pour le nom de la cmdlet correspond également à ses alias, donc `PowerShell(Get-ChildItem *)` correspond à `gci`, `ls` et `dir` aussi. La correspondance est insensible à la casse.

Claude Code analyse l'AST PowerShell et vérifie chaque commande dans une commande composée indépendamment. Les opérateurs de pipeline `|`, les séparateurs d'instruction `;` et sur PowerShell 7+ les opérateurs de chaîne `&&` et `||` divisent une commande composée en sous-commandes. Une règle doit correspondre à chaque sous-commande pour que la commande composée soit autorisée.

### Read et Edit

Les règles `Edit` s'appliquent à tous les outils intégrés qui éditent les fichiers. Claude fait un effort raisonnable pour appliquer les règles `Read` à tous les outils intégrés qui lisent les fichiers comme Grep et Glob.

<Warning>
  Les règles de refus Read et Edit s'appliquent aux outils de fichiers intégrés de Claude et aux commandes de fichiers que Claude Code reconnaît dans Bash, tels que `cat`, `head`, `tail` et `sed`. Elles ne s'appliquent pas aux sous-processus arbitraires qui lisent ou écrivent des fichiers indirectement, comme un script Python ou Node qui ouvre des fichiers lui-même. Pour une application au niveau du système d'exploitation qui bloque tous les processus d'accéder à un chemin, [activez le sandbox](/fr/sandboxing).
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

Une règle ne correspond qu'aux fichiers sous son ancrage, donc l'ancrage détermine jusqu'où une règle de refus s'étend. Les noms de fichiers nus suivent la sémantique gitignore et correspondent à n'importe quelle profondeur, donc `Read(.env)` et `Read(**/.env)` sont équivalents :

| Règle de refus                  | Bloque                                              | Ne bloque pas                                                 |
| ------------------------------- | --------------------------------------------------- | ------------------------------------------------------------- |
| `Read(.env)` ou `Read(**/.env)` | tout `.env` au ou sous le répertoire courant        | `.env` dans un répertoire parent ou un autre projet           |
| `Read(//**/.env)`               | tout `.env` n'importe où sur le système de fichiers | rien ; la règle est ancrée à la racine du système de fichiers |

<Note>
  Dans les modèles gitignore, `*` correspond aux fichiers dans un seul répertoire tandis que `**` correspond récursivement dans les répertoires. Pour autoriser tous les accès aux fichiers, utilisez simplement le nom de l'outil sans parenthèses : `Read`, `Edit` ou `Write`.
</Note>

Lorsque Claude accède à un lien symbolique, les règles d'autorisation vérifient deux chemins : le lien symbolique lui-même et le fichier vers lequel il se résout. Les règles d'autorisation et de refus traitent cette paire différemment : les règles d'autorisation reviennent à vous inviter, tandis que les règles de refus bloquent carrément.

* **Règles d'autorisation** : s'appliquent uniquement lorsque le chemin du lien symbolique et sa cible correspondent tous les deux. Un lien symbolique à l'intérieur d'un répertoire autorisé qui pointe vers l'extérieur vous invite toujours.
* **Règles de refus** : s'appliquent lorsque le chemin du lien symbolique ou sa cible correspond. Un lien symbolique qui pointe vers un fichier refusé est lui-même refusé.

Par exemple, avec `Read(./project/**)` autorisé et `Read(~/.ssh/**)` refusé, un lien symbolique à `./project/key` pointant vers `~/.ssh/id_rsa` est bloqué : la cible échoue à la règle d'autorisation et correspond à la règle de refus.

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

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## Étendre les autorisations avec des hooks

Les [hooks Claude Code](/fr/hooks-guide) fournissent un moyen d'enregistrer des commandes shell personnalisées pour effectuer l'évaluation des autorisations à l'exécution. Lorsque Claude Code effectue un appel d'outil, les hooks PreToolUse s'exécutent avant l'invite d'autorisation. La sortie du hook peut refuser l'appel d'outil, forcer une invite ou ignorer l'invite pour laisser l'appel se poursuivre.

Les décisions du hook ne contournent pas les règles d'autorisation. Les règles de refus et de demande sont évaluées indépendamment de ce qu'un hook PreToolUse retourne, donc une règle de refus correspondante bloque l'appel et une règle de demande correspondante demande toujours même lorsque le hook a retourné `"allow"` ou `"ask"`. Cela préserve la précédence de refus en premier décrite dans [Gérer les autorisations](#manage-permissions), y compris les règles de refus définies dans les paramètres gérés.

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

| Configuration                                                           | Chargé à partir de `--add-dir`                                                                                                                                        |
| :---------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Skills](/fr/skills) dans `.claude/skills/`                             | Oui, avec rechargement en direct                                                                                                                                      |
| Paramètres de plugin dans `.claude/settings.json`                       | `enabledPlugins` et `extraKnownMarketplaces` uniquement                                                                                                               |
| Fichiers [CLAUDE.md](/fr/memory), `.claude/rules/` et `CLAUDE.local.md` | Uniquement lorsque `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` est défini. `CLAUDE.local.md` nécessite également le paramètre `local`, qui est activé par défaut |

Les subagents, les commandes et les styles de sortie sont découverts à partir du répertoire de travail actuel et de ses parents, de votre répertoire utilisateur à `~/.claude/` et des paramètres gérés. Les hooks et d'autres clés `settings.json` se chargent à partir du dossier `.claude/` du répertoire de travail actuel sans secours au répertoire parent, aux côtés de votre `~/.claude/settings.json` utilisateur et des paramètres gérés. Pour partager cette configuration entre les projets, utilisez l'une de ces approches :

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
* Les restrictions du système de fichiers dans le sandbox combinent les paramètres [`sandbox.filesystem`](/fr/sandboxing) avec les règles de refus Read et Edit ; les deux sont fusionnées dans la limite finale du sandbox
* Les restrictions réseau combinent les règles d'autorisation WebFetch avec les listes `allowedDomains` et `deniedDomains` du sandbox

Lorsque le sandboxing est activé avec `autoAllowBashIfSandboxed: true`, qui est la valeur par défaut, les commandes Bash en sandbox s'exécutent sans invite même si vos autorisations incluent `ask: Bash(*)`. La limite du sandbox remplace l'invite par commande. Les règles de refus explicites s'appliquent toujours, et les commandes `rm` ou `rmdir` qui ciblent `/`, votre répertoire personnel ou d'autres chemins système critiques déclenchent toujours une invite. Consultez [modes sandbox](/fr/sandboxing#sandbox-modes) pour modifier ce comportement.

## Paramètres gérés

Pour les organisations qui ont besoin d'un contrôle centralisé sur la configuration de Claude Code, les administrateurs peuvent déployer des paramètres gérés qui ne peuvent pas être remplacés par les paramètres utilisateur ou projet. Ces paramètres de politique suivent le même format que les fichiers de paramètres réguliers et peuvent être livrés via des politiques MDM/au niveau du système d'exploitation, des fichiers de paramètres gérés ou des [paramètres gérés par le serveur](/fr/server-managed-settings). Consultez [fichiers de paramètres](/fr/settings#settings-files) pour les mécanismes de livraison et les emplacements de fichiers.

### Paramètres gérés uniquement

Les paramètres suivants ne sont efficaces que dans les paramètres gérés. Les placer dans les fichiers de paramètres utilisateur ou projet n'a aucun effet.

| Paramètre                                      | Description                                                                                                                                                                                                                                                                                              |
| :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowedChannelPlugins`                        | Liste blanche des plugins de canal qui peuvent envoyer des messages. Remplace la liste blanche Anthropic par défaut lorsqu'elle est définie. Nécessite `channelsEnabled: true`. Consultez [Restreindre les plugins de canal qui peuvent s'exécuter](/fr/channels#restrict-which-channel-plugins-can-run) |
| `allowManagedHooksOnly`                        | Lorsque `true`, seuls les hooks gérés, les hooks SDK et les hooks des plugins activés de force dans les paramètres gérés `enabledPlugins` sont chargés. Les hooks utilisateur, projet et tous les autres hooks de plugin sont bloqués                                                                    |
| `allowManagedMcpServersOnly`                   | Lorsque `true`, seuls les `allowedMcpServers` des paramètres gérés sont respectés. `deniedMcpServers` fusionne toujours à partir de toutes les sources. Consultez [Configuration MCP gérée](/fr/mcp#managed-mcp-configuration)                                                                           |
| `allowManagedPermissionRulesOnly`              | Lorsque `true`, empêche les paramètres utilisateur et projet de définir les règles d'autorisation `allow`, `ask` ou `deny`. Seules les règles dans les paramètres gérés s'appliquent                                                                                                                     |
| `blockedMarketplaces`                          | Liste noire des sources de marketplace. Les sources bloquées sont vérifiées avant le téléchargement, elles ne touchent donc jamais le système de fichiers. Consultez [restrictions de marketplace gérées](/fr/plugin-marketplaces#managed-marketplace-restrictions)                                      |
| `channelsEnabled`                              | Autoriser les [canaux](/fr/channels) pour l'organisation. Consultez [contrôles d'entreprise](/fr/channels#enterprise-controls) pour la valeur par défaut sur chaque plan                                                                                                                                 |
| `forceRemoteSettingsRefresh`                   | Lorsque `true`, bloque le démarrage de la CLI jusqu'à ce que les paramètres gérés distants soient fraîchement récupérés et se termine si la récupération échoue. Consultez [application fail-closed](/fr/server-managed-settings#enforce-fail-closed-startup)                                            |
| `pluginTrustMessage`                           | Message personnalisé ajouté à l'avertissement de confiance du plugin affiché avant l'installation                                                                                                                                                                                                        |
| `sandbox.filesystem.allowManagedReadPathsOnly` | Lorsque `true`, seuls les chemins `filesystem.allowRead` des paramètres gérés sont respectés. `denyRead` fusionne toujours à partir de toutes les sources                                                                                                                                                |
| `sandbox.network.allowManagedDomainsOnly`      | Lorsque `true`, seuls les `allowedDomains` et les règles d'autorisation `WebFetch(domain:...)` des paramètres gérés sont respectés. Les domaines non autorisés sont bloqués automatiquement sans inviter l'utilisateur. Les domaines refusés fusionnent toujours à partir de toutes les sources          |
| `strictKnownMarketplaces`                      | Contrôle quels marketplaces de plugins les utilisateurs peuvent ajouter et installer des plugins à partir de. Consultez [restrictions de marketplace gérées](/fr/plugin-marketplaces#managed-marketplace-restrictions)                                                                                   |
| `wslInheritsWindowsSettings`                   | Lorsque `true` dans la clé de registre Windows HKLM ou `C:\Program Files\ClaudeCode\managed-settings.json`, WSL lit les paramètres gérés à partir de la chaîne de politique Windows en plus de `/etc/claude-code`. Consultez [Fichiers de paramètres](/fr/settings#settings-files)                       |

`disableBypassPermissionsMode` est généralement placé dans les paramètres gérés pour appliquer la politique organisationnelle, mais il fonctionne à partir de n'importe quelle portée. Un utilisateur peut le définir dans ses propres paramètres pour se verrouiller hors du mode de contournement.

<Note>
  Sur les plans Team et Enterprise, un administrateur active ou désactive [Remote Control](/fr/remote-control) et les [sessions web](/fr/claude-code-on-the-web) à l'échelle de l'organisation dans les [paramètres d'administration Claude Code](https://claude.ai/admin-settings/claude-code). Remote Control peut également être désactivé par appareil avec le paramètre géré [`disableRemoteControl`](/fr/settings#available-settings). Les sessions web n'ont pas de clé de paramètres gérés par appareil.
</Note>

## Précédence des paramètres

Les règles d'autorisation suivent la même [précédence des paramètres](/fr/settings#settings-precedence) que tous les autres paramètres de Claude Code :

1. **Paramètres gérés** : ne peuvent pas être remplacés par aucun autre niveau, y compris les arguments de ligne de commande
2. **Arguments de ligne de commande** : remplacements de session temporaires
3. **Paramètres de projet local** (`.claude/settings.local.json`)
4. **Paramètres de projet partagés** (`.claude/settings.json`)
5. **Paramètres utilisateur** (`~/.claude/settings.json`)

Si un outil est refusé à n'importe quel niveau, aucun autre niveau ne peut l'autoriser. Par exemple, un refus de paramètres gérés ne peut pas être remplacé par `--allowedTools`, et `--disallowedTools` peut ajouter des restrictions au-delà de ce que les paramètres gérés définissent.

Les hôtes d'intégration peuvent fournir une politique gérée supplémentaire via l'option SDK `managedSettings` lorsque [`parentSettingsBehavior`](/fr/settings#settings-precedence) est défini sur `"merge"` ; les valeurs de l'intégrateur peuvent renforcer la politique mais pas l'assouplir.

Si une autorisation est autorisée dans les paramètres utilisateur mais refusée dans les paramètres de projet, le paramètre de projet prend la priorité et l'autorisation est bloquée.

## Exemples de configurations

Ce [référentiel](https://github.com/anthropics/claude-code/tree/main/examples/settings) inclut des configurations de paramètres de démarrage pour les scénarios de déploiement courants. Utilisez-les comme points de départ et ajustez-les pour répondre à vos besoins.

## Voir aussi

* [Paramètres](/fr/settings) : référence de configuration complète incluant le tableau des paramètres d'autorisation
* [Configurer le mode auto](/fr/auto-mode-config) : dites au classificateur du mode auto quelle infrastructure votre organisation approuve
* [Sandboxing](/fr/sandboxing) : isolation du système de fichiers et du réseau au niveau du système d'exploitation pour les commandes Bash
* [Authentification](/fr/authentication) : configurer l'accès utilisateur à Claude Code
* [Sécurité](/fr/security) : garanties de sécurité et meilleures pratiques
* [Hooks](/fr/hooks-guide) : automatiser les flux de travail et étendre l'évaluation des autorisations
