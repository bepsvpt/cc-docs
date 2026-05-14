> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Styles de sortie

> Adaptez Claude Code pour des usages au-delà de l'ingénierie logicielle

Les styles de sortie modifient la façon dont Claude répond, non ce que Claude sait. Ils modifient l'invite système pour définir le rôle, le ton et le format de sortie. Utilisez-en un lorsque vous continuez à relancer avec la même voix ou le même format à chaque tour, ou lorsque vous voulez que Claude agisse comme quelque chose d'autre qu'un ingénieur logiciel.

Un style de sortie personnalisé ajoute vos instructions à l'invite système et vous permet de choisir si vous souhaitez conserver les instructions d'ingénierie logicielle intégrées de Claude Code. Conservez-les lorsque vous modifiez la façon dont Claude communique mais que vous codez toujours, comme répondre toujours avec un diagramme. Omettez-les lorsque Claude ne fait pas d'ingénierie logicielle du tout, comme un assistant d'écriture ou un analyste de données.

Pour les instructions concernant votre projet, les conventions ou votre base de code, utilisez [CLAUDE.md](/fr/memory) à la place.

## Styles de sortie intégrés

Le style de sortie **Default** de Claude Code est l'invite système existante, conçue pour vous aider à accomplir efficacement les tâches d'ingénierie logicielle.

Il existe trois styles de sortie intégrés supplémentaires :

* **Proactive** : Claude s'exécute immédiatement, fait des hypothèses raisonnables au lieu de s'arrêter pour les décisions courantes, et préfère l'action à la planification. Cela applique les mêmes conseils que le [mode auto](/fr/permission-modes#eliminate-prompts-with-auto-mode) sans modifier votre mode de permission, vous voyez donc toujours les invites de permission avant l'exécution des outils.

* **Explanatory** : Fournit des « Insights » éducatifs entre les tâches d'ingénierie logicielle pour vous aider à les accomplir. Vous aide à comprendre les choix d'implémentation et les modèles de base de code.

* **Learning** : Mode collaboratif d'apprentissage par la pratique où Claude ne partagera pas seulement des « Insights » lors du codage, mais vous demandera également de contribuer à de petits éléments de code stratégiques. Claude Code ajoutera des marqueurs `TODO(human)` dans votre code pour que vous les implémentiez.

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

Un style de sortie personnalisé est un fichier Markdown : frontmatter pour les métadonnées, puis les instructions à ajouter à l'invite système.

<Steps>
  <Step title="Créer un fichier Markdown">
    Enregistrez-le à l'un des trois niveaux. Le nom du fichier devient le nom du style sauf si vous définissez `name` dans le frontmatter.

    * Utilisateur : `~/.claude/output-styles`
    * Projet : `.claude/output-styles`
    * Politique gérée : `.claude/output-styles` à l'intérieur du [répertoire des paramètres gérés](/fr/settings#settings-files)
  </Step>

  <Step title="Ajouter le frontmatter et les instructions">
    Décidez si vous souhaitez conserver les instructions d'ingénierie logicielle de Claude Code. Définissez `keep-coding-instructions: true` si vous modifiez la façon dont Claude communique mais que vous voulez qu'il code de la même manière. Omettez-le si Claude ne fera pas d'ingénierie logicielle.

    Cet exemple commence chaque explication par un diagramme tout en conservant le comportement de codage de Claude :

    ```markdown theme={null}
    ---
    name: Diagrams first
    description: Lead every explanation with a diagram
    keep-coding-instructions: true
    ---

    When explaining code, architecture, or data flow, start with a Mermaid diagram showing the structure, then explain in prose.

    ## Diagram conventions

    Use `flowchart TD` for control flow and `sequenceDiagram` for request paths. Keep diagrams under 15 nodes.
    ```
  </Step>

  <Step title="Basculer vers votre style">
    Exécutez `/config` et sélectionnez votre style sous **Output style**. Il prend effet la prochaine fois que vous démarrez une session.
  </Step>
</Steps>

Les [Plugins](/fr/plugins-reference) peuvent également fournir des styles de sortie dans un répertoire `output-styles/`.

### Frontmatter

Les fichiers de style de sortie prennent en charge ces champs frontmatter :

| Frontmatter                | Objectif                                                                                                                                                                                                                                                                                                     | Par défaut               |
| :------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------- |
| `name`                     | Nom du style de sortie, s'il ne s'agit pas du nom du fichier                                                                                                                                                                                                                                                 | Hérité du nom du fichier |
| `description`              | Description du style de sortie, affichée dans le sélecteur `/config`                                                                                                                                                                                                                                         | Aucun                    |
| `keep-coding-instructions` | Conserver les instructions d'ingénierie logicielle intégrées de Claude Code                                                                                                                                                                                                                                  | `false`                  |
| `force-for-plugin`         | Styles de sortie de plugin uniquement : appliquez ce style automatiquement chaque fois que le plugin est activé, sans nécessiter une sélection de l'utilisateur. Remplace le paramètre `outputStyle` de l'utilisateur. Si plusieurs plugins activés définissent ceci, Claude Code utilise le premier chargé. | `false`                  |

## Fonctionnement des styles de sortie

Les styles de sortie modifient directement l'invite système de Claude Code.

* Tous les styles de sortie ont leurs propres instructions personnalisées ajoutées à la fin de l'invite système.
* Tous les styles de sortie déclenchent des rappels pour que Claude adhère aux instructions du style de sortie pendant la conversation.
* Les styles de sortie personnalisés omettent les instructions d'ingénierie logicielle intégrées de Claude Code, comme la façon de délimiter les modifications, d'écrire des commentaires et de vérifier le travail, sauf si `keep-coding-instructions` est défini sur `true`.

L'utilisation des tokens dépend du style. L'ajout d'instructions à l'invite système augmente les tokens d'entrée, bien que la mise en cache des invites réduise ce coût après la première requête d'une session. Les styles Explanatory et Learning intégrés produisent des réponses plus longues que Default par conception, ce qui augmente les tokens de sortie. Pour les styles personnalisés, l'utilisation des tokens de sortie dépend de ce que vos instructions demandent à Claude de produire.

## Comparaisons avec les fonctionnalités connexes

Plusieurs fonctionnalités personnalisent le comportement de Claude Code. Les styles de sortie modifient directement l'invite système et s'appliquent à chaque réponse. Les autres ajoutent des instructions sans modifier l'invite système par défaut, ou les limitent à une tâche spécifique.

| Fonctionnalité           | Fonctionnement                                                                             | Utilisez-le quand                                                                                |
| :----------------------- | :----------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------- |
| Styles de sortie         | Modifie l'invite système                                                                   | Vous voulez un rôle, un ton ou un format de réponse par défaut différent à chaque tour           |
| [CLAUDE.md](/fr/memory)  | Ajoute un message utilisateur après l'invite système                                       | Claude devrait toujours connaître vos conventions de projet et le contexte de votre base de code |
| `--append-system-prompt` | Ajoute à l'invite système sans rien supprimer                                              | Vous voulez un ajout ponctuel pour une seule invocation                                          |
| [Agents](/fr/sub-agents) | Exécute un sous-agent avec sa propre invite système, son modèle et ses outils              | Vous voulez un assistant à portée séparée pour une tâche ciblée                                  |
| [Skills](/fr/skills)     | Charge les instructions spécifiques à une tâche lorsqu'elles sont invoquées ou pertinentes | Vous avez un flux de travail réutilisable                                                        |

## Ressources connexes

* [Settings](/fr/settings) : où se trouve le champ `outputStyle` et comment fonctionne la précédence des paramètres
* [Permission modes](/fr/permission-modes) : le style Proactive reflète le mode auto sans modifier votre mode de permission
* [Plugins](/fr/plugins) : empaquetez et distribuez les styles de sortie aux côtés des skills, des hooks et des agents
* [Debug your configuration](/fr/debug-your-config) : diagnostiquez pourquoi un style de sortie ne prend pas effet
