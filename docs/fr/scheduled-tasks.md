> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Exécuter des prompts selon un calendrier

> Utilisez /loop et les outils de planification cron pour exécuter des prompts de manière répétée, interroger l'état ou définir des rappels ponctuels dans une session Claude Code.

<Note>
  Les tâches planifiées nécessitent Claude Code v2.1.72 ou version ultérieure. Vérifiez votre version avec `claude --version`.
</Note>

Les tâches planifiées permettent à Claude de réexécuter automatiquement un prompt à intervalles réguliers. Utilisez-les pour interroger un déploiement, surveiller une PR, vérifier une compilation longue ou vous rappeler de faire quelque chose plus tard dans la session. Pour réagir aux événements au fur et à mesure qu'ils se produisent au lieu d'interroger, consultez [Channels](/fr/channels) : votre CI peut pousser l'échec directement dans la session.

Les tâches sont limitées à la session : elles vivent dans le processus Claude Code actuel et disparaissent lorsque vous quittez. Pour une planification durable qui survit aux redémarrages, utilisez les tâches planifiées [Cloud](/fr/web-scheduled-tasks) ou [Desktop](/fr/desktop#schedule-recurring-tasks), ou [GitHub Actions](/fr/github-actions).

## Comparer les options de planification

Claude Code offers three ways to schedule recurring work:

|                            | [Cloud](/en/web-scheduled-tasks) | [Desktop](/en/desktop-scheduled-tasks) | [`/loop`](/en/scheduled-tasks) |
| :------------------------- | :------------------------------- | :------------------------------------- | :----------------------------- |
| Runs on                    | Anthropic cloud                  | Your machine                           | Your machine                   |
| Requires machine on        | No                               | Yes                                    | Yes                            |
| Requires open session      | No                               | No                                     | Yes                            |
| Persistent across restarts | Yes                              | Yes                                    | No (session-scoped)            |
| Access to local files      | No (fresh clone)                 | Yes                                    | Yes                            |
| MCP servers                | Connectors configured per task   | [Config files](/en/mcp) and connectors | Inherits from session          |
| Permission prompts         | No (runs autonomously)           | Configurable per task                  | Inherits from session          |
| Customizable schedule      | Via `/schedule` in the CLI       | Yes                                    | Yes                            |
| Minimum interval           | 1 hour                           | 1 minute                               | 1 minute                       |

<Tip>
  Use **cloud tasks** for work that should run reliably without your machine. Use **Desktop tasks** when you need access to local files and tools. Use **`/loop`** for quick polling during a session.
</Tip>

## Planifier un prompt récurrent avec /loop

La [compétence groupée](/fr/skills#bundled-skills) `/loop` est le moyen le plus rapide de planifier un prompt récurrent. Passez un intervalle optionnel et un prompt, et Claude configure une tâche cron qui s'exécute en arrière-plan pendant que la session reste ouverte.

```text  theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

Claude analyse l'intervalle, le convertit en expression cron, planifie la tâche et confirme la cadence et l'ID de la tâche.

### Syntaxe d'intervalle

Les intervalles sont optionnels. Vous pouvez les placer au début, à la fin ou les omettre entièrement.

| Forme                 | Exemple                               | Intervalle analysé               |
| :-------------------- | :------------------------------------ | :------------------------------- |
| Jeton initial         | `/loop 30m check the build`           | toutes les 30 minutes            |
| Clause `every` finale | `/loop check the build every 2 hours` | toutes les 2 heures              |
| Pas d'intervalle      | `/loop check the build`               | par défaut toutes les 10 minutes |

Les unités prises en charge sont `s` pour les secondes, `m` pour les minutes, `h` pour les heures et `d` pour les jours. Les secondes sont arrondies à la minute la plus proche puisque cron a une granularité d'une minute. Les intervalles qui ne se divisent pas uniformément dans leur unité, comme `7m` ou `90m`, sont arrondis à l'intervalle le plus proche et Claude vous indique ce qu'il a choisi.

### Boucler sur une autre commande

Le prompt planifié peut lui-même être une invocation de commande ou de compétence. C'est utile pour réexécuter un flux de travail que vous avez déjà empaqueté.

```text  theme={null}
/loop 20m /review-pr 1234
```

Chaque fois que la tâche s'exécute, Claude exécute `/review-pr 1234` comme si vous l'aviez tapé.

## Définir un rappel ponctuel

Pour les rappels ponctuels, décrivez ce que vous voulez en langage naturel au lieu d'utiliser `/loop`. Claude planifie une tâche à usage unique qui se supprime après son exécution.

```text  theme={null}
remind me at 3pm to push the release branch
```

```text  theme={null}
in 45 minutes, check whether the integration tests passed
```

Claude épingle l'heure d'exécution à une minute et une heure spécifiques en utilisant une expression cron et confirme quand elle s'exécutera.

## Gérer les tâches planifiées

Demandez à Claude en langage naturel de lister ou d'annuler les tâches, ou référencez directement les outils sous-jacents.

```text  theme={null}
what scheduled tasks do I have?
```

```text  theme={null}
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

Les tâches récurrentes expirent automatiquement 7 jours après leur création. La tâche s'exécute une dernière fois, puis se supprime. Cela limite la durée pendant laquelle une boucle oubliée peut s'exécuter. Si vous avez besoin qu'une tâche récurrente dure plus longtemps, annulez et recréez-la avant son expiration, ou utilisez [Tâches planifiées sur le cloud](/fr/web-scheduled-tasks) ou [Tâches planifiées sur le bureau](/fr/desktop#schedule-recurring-tasks) pour une planification durable.

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

* [Tâches planifiées sur le cloud](/fr/web-scheduled-tasks) : s'exécutent sur l'infrastructure gérée par Anthropic
* [GitHub Actions](/fr/github-actions) : utilisez un déclencheur `schedule` dans CI
* [Tâches planifiées sur le bureau](/fr/desktop#schedule-recurring-tasks) : s'exécutent localement sur votre machine
