> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Styles de sortie

> Adaptez Claude Code pour des usages au-delà de l'ingénierie logicielle

Les styles de sortie vous permettent d'utiliser Claude Code comme n'importe quel type d'agent tout en conservant ses capacités principales, telles que l'exécution de scripts locaux, la lecture/écriture de fichiers et le suivi des TODOs.

## Styles de sortie intégrés

Le style de sortie **Default** de Claude Code est l'invite système existante, conçue pour vous aider à accomplir efficacement les tâches d'ingénierie logicielle.

Il existe deux styles de sortie intégrés supplémentaires axés sur vous enseigner la base de code et le fonctionnement de Claude :

* **Explanatory** : Fournit des « Insights » éducatifs entre les tâches d'ingénierie logicielle pour vous aider à les accomplir. Vous aide à comprendre les choix d'implémentation et les modèles de base de code.

* **Learning** : Mode collaboratif d'apprentissage par la pratique où Claude ne partagera pas seulement des « Insights » lors du codage, mais vous demandera également de contribuer à de petits éléments de code stratégiques. Claude Code ajoutera des marqueurs `TODO(human)` dans votre code pour que vous les implémentiez.

## Fonctionnement des styles de sortie

Les styles de sortie modifient directement l'invite système de Claude Code.

* Les styles de sortie personnalisés excluent les instructions de codage (comme la vérification du code avec des tests), sauf si `keep-coding-instructions` est true.
* Tous les styles de sortie ont leurs propres instructions personnalisées ajoutées à la fin de l'invite système.
* Tous les styles de sortie déclenchent des rappels pour que Claude adhère aux instructions du style de sortie pendant la conversation.

L'utilisation des tokens dépend du style. L'ajout d'instructions à l'invite système augmente les tokens d'entrée, bien que la mise en cache des invites réduise ce coût après la première requête d'une session. Les styles Explanatory et Learning intégrés produisent des réponses plus longues que Default par conception, ce qui augmente les tokens de sortie. Pour les styles personnalisés, l'utilisation des tokens de sortie dépend de ce que vos instructions demandent à Claude de produire.

## Modifier votre style de sortie

Exécutez `/config` et sélectionnez **Output style** pour choisir un style dans un menu. Votre sélection est enregistrée dans `.claude/settings.local.json` au [niveau du projet local](/fr/settings).

Pour définir un style sans le menu, modifiez directement le champ `outputStyle` dans un fichier de paramètres :

```json theme={null}
{
  "outputStyle": "Explanatory"
}
```

Comme le style de sortie est défini dans l'invite système au démarrage de la session, les modifications prennent effet la prochaine fois que vous démarrez une nouvelle session. Cela maintient l'invite système stable tout au long d'une conversation afin que la mise en cache des invites puisse réduire la latence et les coûts.

## Créer un style de sortie personnalisé

Les styles de sortie personnalisés sont des fichiers Markdown avec frontmatter et le texte qui sera ajouté à l'invite système :

```markdown theme={null}
---
name: My Custom Style
description:
  A brief description of what this style does, to be displayed to the user
---

# Custom Style Instructions

You are an interactive CLI tool that helps users with software engineering
tasks. [Your custom instructions here...]

## Specific Behaviors

[Define how the assistant should behave in this style...]
```

Vous pouvez enregistrer ces fichiers au niveau utilisateur (`~/.claude/output-styles`) ou au niveau projet (`.claude/output-styles`).

### Frontmatter

Les fichiers de style de sortie prennent en charge frontmatter pour spécifier les métadonnées :

| Frontmatter                | Objectif                                                                                    | Par défaut               |
| :------------------------- | :------------------------------------------------------------------------------------------ | :----------------------- |
| `name`                     | Nom du style de sortie, s'il ne s'agit pas du nom du fichier                                | Hérité du nom du fichier |
| `description`              | Description du style de sortie, affichée dans le sélecteur `/config`                        | Aucun                    |
| `keep-coding-instructions` | Indique s'il faut conserver les parties de l'invite système de Claude Code liées au codage. | false                    |

## Comparaisons avec les fonctionnalités connexes

### Styles de sortie vs. CLAUDE.md vs. --append-system-prompt

Les styles de sortie « désactivent » complètement les parties de l'invite système par défaut de Claude Code spécifiques à l'ingénierie logicielle. Ni CLAUDE.md ni `--append-system-prompt` ne modifient l'invite système par défaut de Claude Code. CLAUDE.md ajoute le contenu en tant que message utilisateur *suivant* l'invite système par défaut de Claude Code. `--append-system-prompt` ajoute le contenu à l'invite système.

### Styles de sortie vs. [Agents](/fr/sub-agents)

Les styles de sortie affectent directement la boucle d'agent principal et n'affectent que l'invite système. Les agents sont invoqués pour gérer des tâches spécifiques et peuvent inclure des paramètres supplémentaires tels que le modèle à utiliser, les outils disponibles et un contexte sur le moment d'utiliser l'agent.

### Styles de sortie vs. [Skills](/fr/skills)

Les styles de sortie modifient la façon dont Claude répond (formatage, ton, structure) et sont toujours actifs une fois sélectionnés. Les skills sont des invites spécifiques à une tâche que vous invoquez avec `/skill-name` ou que Claude charge automatiquement si pertinent. Utilisez les styles de sortie pour les préférences de formatage cohérentes ; utilisez les skills pour les flux de travail et les tâches réutilisables.
