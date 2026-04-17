> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Exécuter des prompts selon un calendrier

> Utilisez /loop et les outils de planification cron pour exécuter des prompts de manière répétée, interroger l'état ou définir des rappels ponctuels dans une session Claude Code.

<Note>
  Les tâches planifiées nécessitent Claude Code v2.1.72 ou version ultérieure. Vérifiez votre version avec `claude --version`.
</Note>

Les tâches planifiées permettent à Claude de réexécuter automatiquement un prompt à intervalles réguliers. Utilisez-les pour interroger un déploiement, surveiller une PR, vérifier une compilation longue ou vous rappeler de faire quelque chose plus tard dans la session. Pour réagir aux événements au fur et à mesure qu'ils se produisent au lieu d'interroger, consultez [Channels](/fr/channels) : votre CI peut pousser l'échec directement dans la session.

Les tâches sont limitées à la session : elles vivent dans le processus Claude Code actuel et disparaissent lorsque vous quittez. Pour une planification durable qui survit aux redémarrages, utilisez [Routines](/fr/routines), [Tâches planifiées sur le bureau](/fr/desktop-scheduled-tasks) ou [GitHub Actions](/fr/github-actions).

## Comparer les options de planification

Claude Code offers three ways to schedule recurring work:

|                            | [Cloud](/en/routines)          | [Desktop](/en/desktop-scheduled-tasks) | [`/loop`](/en/scheduled-tasks)      |
| :------------------------- | :----------------------------- | :------------------------------------- | :---------------------------------- |
| Runs on                    | Anthropic cloud                | Your machine                           | Your machine                        |
| Requires machine on        | No                             | Yes                                    | Yes                                 |
| Requires open session      | No                             | No                                     | Yes                                 |
| Persistent across restarts | Yes                            | Yes                                    | Restored on `--resume` if unexpired |
| Access to local files      | No (fresh clone)               | Yes                                    | Yes                                 |
| MCP servers                | Connectors configured per task | [Config files](/en/mcp) and connectors | Inherits from session               |
| Permission prompts         | No (runs autonomously)         | Configurable per task                  | Inherits from session               |
| Customizable schedule      | Via `/schedule` in the CLI     | Yes                                    | Yes                                 |
| Minimum interval           | 1 hour                         | 1 minute                               | 1 minute                            |

<Tip>
  Use **cloud tasks** for work that should run reliably without your machine. Use **Desktop tasks** when you need access to local files and tools. Use **`/loop`** for quick polling during a session.
</Tip>

## Exécuter un prompt de manière répétée avec /loop

La [compétence groupée](/fr/commands) `/loop` est le moyen le plus rapide d'exécuter un prompt de manière répétée pendant que la session reste ouverte. L'intervalle et le prompt sont tous deux optionnels, et ce que vous fournissez détermine le comportement de la boucle.

| Ce que vous fournissez         | Exemple                     | Ce qui se passe                                                                                                          |
| :----------------------------- | :-------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| Intervalle et prompt           | `/loop 5m check the deploy` | Votre prompt s'exécute selon un [calendrier fixe](#run-on-a-fixed-interval)                                              |
| Prompt uniquement              | `/loop check the deploy`    | Votre prompt s'exécute à un [intervalle choisi par Claude](#let-claude-choose-the-interval) à chaque itération           |
| Intervalle uniquement, ou rien | `/loop`                     | Le [prompt de maintenance intégré](#run-the-built-in-maintenance-prompt) s'exécute, ou votre `loop.md` s'il en existe un |

Vous pouvez également passer une autre commande en tant que prompt, par exemple `/loop 20m /review-pr 1234`, pour réexécuter un flux de travail empaqueté à chaque itération.

### Exécuter selon un intervalle fixe

Lorsque vous fournissez un intervalle, Claude le convertit en expression cron, planifie la tâche et confirme la cadence et l'ID de la tâche.

```text theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

L'intervalle peut précéder le prompt en tant que jeton nu comme `30m`, ou le suivre en tant que clause comme `every 2 hours`. Les unités prises en charge sont `s` pour les secondes, `m` pour les minutes, `h` pour les heures et `d` pour les jours.

Les secondes sont arrondies à la minute la plus proche puisque cron a une granularité d'une minute. Les intervalles qui ne correspondent pas à une étape cron propre, comme `7m` ou `90m`, sont arrondis à l'intervalle le plus proche et Claude vous indique ce qu'il a choisi.

### Laisser Claude choisir l'intervalle

Lorsque vous omettez l'intervalle, Claude en choisit un dynamiquement au lieu de s'exécuter selon un calendrier cron fixe. Après chaque itération, il choisit un délai entre une minute et une heure en fonction de ce qu'il a observé : des attentes courtes pendant qu'une compilation se termine ou qu'une PR est active, des attentes plus longues quand rien n'est en attente. Le délai choisi et la raison de ce choix sont imprimés à la fin de chaque itération.

L'exemple ci-dessous vérifie CI et les commentaires d'examen, Claude attendant plus longtemps entre les itérations une fois que la PR devient silencieuse :

```text theme={null}
/loop check whether CI passed and address any review comments
```

Lorsque vous demandez un calendrier `/loop` dynamique, Claude peut utiliser l'[outil Monitor](/fr/tools-reference#monitor-tool) directement. Monitor exécute un script en arrière-plan et diffuse chaque ligne de sortie, ce qui évite complètement l'interrogation et est souvent plus efficace en termes de jetons et plus réactif que de réexécuter un prompt à intervalles réguliers.

Une boucle planifiée dynamiquement apparaît dans votre [liste de tâches planifiées](#manage-scheduled-tasks) comme n'importe quelle autre tâche, vous pouvez donc la lister ou l'annuler de la même manière. Les [règles de gigue](#jitter) ne s'appliquent pas à elle, mais l'[expiration de sept jours](#seven-day-expiry) s'applique : la boucle se termine automatiquement sept jours après son démarrage.

<Note>
  Sur Bedrock, Vertex AI et Microsoft Foundry, un prompt sans intervalle s'exécute selon un calendrier fixe de 10 minutes à la place.
</Note>

### Exécuter le prompt de maintenance intégré

Lorsque vous omettez le prompt, Claude utilise un prompt de maintenance intégré au lieu d'un que vous fournissez. À chaque itération, il travaille sur les éléments suivants, dans l'ordre :

* continuer tout travail inachevé de la conversation
* s'occuper de la demande de fusion de la branche actuelle : examiner les commentaires, les exécutions CI échouées, les conflits de fusion
* exécuter des passes de nettoyage telles que la chasse aux bogues ou la simplification quand rien d'autre n'est en attente

Claude ne lance pas de nouvelles initiatives en dehors de cette portée, et les actions irréversibles telles que pousser ou supprimer ne procèdent que lorsqu'elles continuent quelque chose que la transcription a déjà autorisé.

```text theme={null}
/loop
```

Un `/loop` nu exécute ce prompt à un [intervalle choisi dynamiquement](#let-claude-choose-the-interval). Ajoutez un intervalle, par exemple `/loop 15m`, pour l'exécuter selon un calendrier fixe à la place. Pour remplacer le prompt intégré par le vôtre, consultez [Personnaliser le prompt par défaut avec loop.md](#customize-the-default-prompt-with-loop-md).

<Note>
  Sur Bedrock, Vertex AI et Microsoft Foundry, `/loop` sans prompt imprime le message d'utilisation au lieu de démarrer la boucle de maintenance.
</Note>

### Personnaliser le prompt par défaut avec loop.md

Un fichier `loop.md` remplace le prompt de maintenance intégré par vos propres instructions. Il définit un seul prompt par défaut pour un `/loop` nu, pas une liste de tâches planifiées séparées, et est ignoré chaque fois que vous fournissez un prompt sur la ligne de commande. Pour planifier des prompts supplémentaires à côté de celui-ci, utilisez `/loop <prompt>` ou [demandez directement à Claude](#manage-scheduled-tasks).

Claude recherche le fichier dans deux emplacements et utilise le premier qu'il trouve.

| Chemin              | Portée                                                                              |
| :------------------ | :---------------------------------------------------------------------------------- |
| `.claude/loop.md`   | Au niveau du projet. Prend la priorité quand les deux fichiers existent.            |
| `~/.claude/loop.md` | Au niveau de l'utilisateur. S'applique dans tout projet qui ne définit pas le sien. |

Le fichier est du Markdown simple sans structure requise. Écrivez-le comme si vous tapiez le prompt `/loop` directement. L'exemple suivant maintient une branche de version saine :

```markdown title=".claude/loop.md" theme={null}
Check the `release/next` PR. If CI is red, pull the failing job log,
diagnose, and push a minimal fix. If new review comments have arrived,
address each one and resolve the thread. If everything is green and
quiet, say so in one line.
```

Les modifications apportées à `loop.md` prennent effet à la prochaine itération, vous pouvez donc affiner les instructions pendant qu'une boucle s'exécute. Quand aucun `loop.md` n'existe dans l'un ou l'autre emplacement, la boucle revient au prompt de maintenance intégré. Gardez le fichier concis : le contenu au-delà de 25 000 octets est tronqué.

## Définir un rappel ponctuel

Pour les rappels ponctuels, décrivez ce que vous voulez en langage naturel au lieu d'utiliser `/loop`. Claude planifie une tâche à usage unique qui se supprime après son exécution.

```text theme={null}
remind me at 3pm to push the release branch
```

```text theme={null}
in 45 minutes, check whether the integration tests passed
```

Claude épingle l'heure d'exécution à une minute et une heure spécifiques en utilisant une expression cron et confirme quand elle s'exécutera.

## Gérer les tâches planifiées

Demandez à Claude en langage naturel de lister ou d'annuler les tâches, ou référencez directement les outils sous-jacents.

```text theme={null}
what scheduled tasks do I have?
```

```text theme={null}
cancel the deploy check job
```

Sous le capot, Claude utilise ces outils :

| Outil        | Objectif                                                                                                                                          |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------ |
| `CronCreate` | Planifier une nouvelle tâche. Accepte une expression cron à 5 champs, le prompt à exécuter et si elle est récurrente ou s'exécute une seule fois. |
| `CronList`   | Lister toutes les tâches planifiées avec leurs ID, leurs calendriers et leurs prompts.                                                            |
| `CronDelete` | Annuler une tâche par ID.                                                                                                                         |

Chaque tâche planifiée a un ID de 8 caractères que vous pouvez passer à `CronDelete`. Une session peut contenir jusqu'à 50 tâches planifiées à la fois.

## Comment les tâches planifiées s'exécutent

Le planificateur vérifie chaque seconde les tâches dues et les met en file d'attente à faible priorité. Un prompt planifié s'exécute entre vos tours, pas pendant que Claude répond. Si Claude est occupé quand une tâche arrive à échéance, le prompt attend la fin du tour actuel.

Tous les horaires sont interprétés dans votre fuseau horaire local. Une expression cron comme `0 9 * * *` signifie 9h là où vous exécutez Claude Code, pas UTC.

### Gigue

Pour éviter que chaque session ne frappe l'API au même moment mural, le planificateur ajoute un petit décalage déterministe aux heures d'exécution :

* Les tâches récurrentes s'exécutent jusqu'à 10 % de leur période en retard, plafonnées à 15 minutes. Une tâche horaire peut s'exécuter n'importe où de `:00` à `:06`.
* Les tâches ponctuelles planifiées pour le haut ou le bas de l'heure s'exécutent jusqu'à 90 secondes plus tôt.

Le décalage est dérivé de l'ID de la tâche, donc la même tâche obtient toujours le même décalage. Si le timing exact est important, choisissez une minute qui n'est pas `:00` ou `:30`, par exemple `3 9 * * *` au lieu de `0 9 * * *`, et la gigue ponctuelle ne s'appliquera pas.

### Expiration de sept jours

Les tâches récurrentes expirent automatiquement 7 jours après leur création. La tâche s'exécute une dernière fois, puis se supprime. Cela limite la durée pendant laquelle une boucle oubliée peut s'exécuter. Si vous avez besoin qu'une tâche récurrente dure plus longtemps, annulez et recréez-la avant son expiration, ou utilisez [Routines](/fr/routines) ou [Tâches planifiées sur le bureau](/fr/desktop-scheduled-tasks) pour une planification durable.

## Référence d'expression cron

`CronCreate` accepte les expressions cron standard à 5 champs : `minute heure jour-du-mois mois jour-de-la-semaine`. Tous les champs prennent en charge les caractères génériques (`*`), les valeurs uniques (`5`), les étapes (`*/15`), les plages (`1-5`) et les listes séparées par des virgules (`1,15,30`).

| Exemple        | Signification                    |
| :------------- | :------------------------------- |
| `*/5 * * * *`  | Toutes les 5 minutes             |
| `0 * * * *`    | Chaque heure à l'heure pile      |
| `7 * * * *`    | Chaque heure à 7 minutes passées |
| `0 9 * * *`    | Chaque jour à 9h local           |
| `0 9 * * 1-5`  | Jours de semaine à 9h local      |
| `30 14 15 3 *` | 15 mars à 14h30 local            |

Le jour de la semaine utilise `0` ou `7` pour dimanche jusqu'à `6` pour samedi. La syntaxe étendue comme `L`, `W`, `?` et les alias de noms tels que `MON` ou `JAN` ne sont pas pris en charge.

Lorsque le jour du mois et le jour de la semaine sont tous deux contraints, une date correspond si l'un ou l'autre champ correspond. Cela suit la sémantique standard de vixie-cron.

## Désactiver les tâches planifiées

Définissez `CLAUDE_CODE_DISABLE_CRON=1` dans votre environnement pour désactiver complètement le planificateur. Les outils cron et `/loop` deviennent indisponibles, et toutes les tâches déjà planifiées cessent de s'exécuter. Consultez [Variables d'environnement](/fr/env-vars) pour la liste complète des drapeaux de désactivation.

## Limitations

La planification limitée à la session a des contraintes inhérentes :

* Les tâches ne s'exécutent que pendant que Claude Code s'exécute et est inactif. Fermer le terminal ou laisser la session se terminer annule tout.
* Pas de rattrapage pour les exécutions manquées. Si l'heure planifiée d'une tâche passe pendant que Claude est occupé par une demande longue, elle s'exécute une fois quand Claude devient inactif, pas une fois par intervalle manqué.
* Pas de persistance entre les redémarrages. Le redémarrage de Claude Code efface toutes les tâches limitées à la session.

Pour l'automatisation pilotée par cron qui doit s'exécuter sans surveillance :

* [Routines](/fr/routines) : s'exécutent sur l'infrastructure gérée par Anthropic selon un calendrier, via un appel API ou sur des événements GitHub
* [GitHub Actions](/fr/github-actions) : utilisez un déclencheur `schedule` dans CI
* [Tâches planifiées sur le bureau](/fr/desktop-scheduled-tasks) : s'exécutent localement sur votre machine
