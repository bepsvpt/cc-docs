> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Révision de code

> Configurez des révisions de PR automatisées qui détectent les erreurs logiques, les vulnérabilités de sécurité et les régressions en utilisant une analyse multi-agents de votre base de code complète

<Note>
  Code Review est en aperçu de recherche, disponible pour les abonnements [Teams et Enterprise](https://claude.ai/admin-settings/claude-code). Il n'est pas disponible pour les organisations avec [Zero Data Retention](/fr/zero-data-retention) activé.
</Note>

Code Review analyse vos pull requests GitHub et publie les résultats sous forme de commentaires en ligne sur les lignes de code où il a trouvé des problèmes. Une flotte d'agents spécialisés examine les modifications de code dans le contexte de votre base de code complète, en recherchant les erreurs logiques, les vulnérabilités de sécurité, les cas limites cassés et les régressions subtiles.

Les résultats sont étiquetés par gravité et n'approuvent ni ne bloquent votre PR, de sorte que les flux de travail d'examen existants restent intacts. Vous pouvez affiner ce que Claude signale en ajoutant un fichier `CLAUDE.md` ou `REVIEW.md` à votre référentiel.

Pour exécuter Claude dans votre propre infrastructure CI au lieu de ce service géré, consultez [GitHub Actions](/fr/github-actions) ou [GitLab CI/CD](/fr/gitlab-ci-cd).

Cette page couvre :

* [Comment fonctionnent les révisions](#how-reviews-work)
* [Configuration](#set-up-code-review)
* [Personnalisation des révisions](#customize-reviews) avec `CLAUDE.md` et `REVIEW.md`
* [Tarification](#pricing)

## Comment fonctionnent les révisions

Une fois qu'un administrateur [active Code Review](#set-up-code-review) pour votre organisation, les révisions s'exécutent automatiquement lorsqu'une pull request s'ouvre ou se met à jour. Plusieurs agents analysent le diff et le code environnant en parallèle sur l'infrastructure Anthropic. Chaque agent recherche une classe de problème différente, puis une étape de vérification vérifie les candidats par rapport au comportement réel du code pour filtrer les faux positifs. Les résultats sont dédupliqués, classés par gravité et publiés sous forme de commentaires en ligne sur les lignes spécifiques où les problèmes ont été trouvés. Si aucun problème n'est trouvé, Claude publie un court commentaire de confirmation sur la PR.

Les révisions s'adaptent en coût à la taille et à la complexité de la PR, se complétant en moyenne en 20 minutes. Les administrateurs peuvent surveiller l'activité de révision et les dépenses via le [tableau de bord analytique](#view-usage).

### Niveaux de gravité

Chaque résultat est étiqueté avec un niveau de gravité :

| Marqueur | Gravité     | Signification                                                                  |
| :------- | :---------- | :----------------------------------------------------------------------------- |
| 🔴       | Normal      | Un bug qui devrait être corrigé avant la fusion                                |
| 🟡       | Nit         | Un problème mineur, utile à corriger mais non bloquant                         |
| 🟣       | Préexistant | Un bug qui existe dans la base de code mais n'a pas été introduit par cette PR |

Les résultats incluent une section de raisonnement étendu réductible que vous pouvez développer pour comprendre pourquoi Claude a signalé le problème et comment il a vérifié le problème.

### Ce que Code Review vérifie

Par défaut, Code Review se concentre sur la correction : les bugs qui cassent la production, pas les préférences de formatage ou la couverture de test manquante. Vous pouvez développer ce qu'il vérifie en [ajoutant des fichiers de guidance](#customize-reviews) à votre référentiel.

## Configurer Code Review

Un administrateur active Code Review une fois pour l'organisation et sélectionne les référentiels à inclure.

<Steps>
  <Step title="Ouvrir les paramètres d'administration Claude Code">
    Allez à [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) et trouvez la section Code Review. Vous avez besoin d'un accès administrateur à votre organisation Claude et de la permission d'installer des GitHub Apps dans votre organisation GitHub.
  </Step>

  <Step title="Démarrer la configuration">
    Cliquez sur **Configuration**. Cela commence le flux d'installation de GitHub App.
  </Step>

  <Step title="Installer la GitHub App Claude">
    Suivez les invites pour installer la GitHub App Claude à votre organisation GitHub. L'application demande ces permissions de référentiel :

    * **Contents** : lecture et écriture
    * **Issues** : lecture et écriture
    * **Pull requests** : lecture et écriture

    Code Review utilise l'accès en lecture aux contenus et l'accès en écriture aux pull requests. L'ensemble de permissions plus large supporte également [GitHub Actions](/fr/github-actions) si vous l'activez plus tard.
  </Step>

  <Step title="Sélectionner les référentiels">
    Choisissez les référentiels à activer pour Code Review. Si vous ne voyez pas un référentiel, assurez-vous d'avoir donné à la GitHub App Claude l'accès à celui-ci lors de l'installation. Vous pouvez ajouter d'autres référentiels plus tard.
  </Step>

  <Step title="Définir les déclencheurs de révision par référentiel">
    Une fois la configuration terminée, la section Code Review affiche vos référentiels dans un tableau. Pour chaque référentiel, utilisez la liste déroulante pour choisir quand les révisions s'exécutent :

    * **Après la création de PR uniquement** : la révision s'exécute une fois lorsqu'une PR est ouverte ou marquée comme prête pour révision
    * **Après chaque push vers la branche PR** : la révision s'exécute à chaque push, détectant les nouveaux problèmes au fur et à mesure que la PR évolue et résolvant automatiquement les threads lorsque vous corrigez les problèmes signalés

    La révision à chaque push exécute plus de révisions et coûte plus cher. Commencez par la création de PR uniquement et passez à on-push pour les référentiels où vous voulez une couverture continue et un nettoyage automatique des threads.
  </Step>
</Steps>

Le tableau des référentiels affiche également le coût moyen par révision pour chaque référentiel en fonction de l'activité récente. Utilisez le menu des actions de ligne pour activer ou désactiver Code Review par référentiel, ou pour supprimer complètement un référentiel.

Pour vérifier la configuration, ouvrez une PR de test. Une exécution de vérification nommée **Claude Code Review** apparaît dans quelques minutes. Si ce n'est pas le cas, confirmez que le référentiel est listé dans vos paramètres d'administration et que la GitHub App Claude y a accès.

## Personnaliser les révisions

Code Review lit deux fichiers de votre référentiel pour guider ce qu'il signale. Les deux s'ajoutent aux vérifications de correction par défaut :

* **`CLAUDE.md`** : instructions de projet partagées que Claude Code utilise pour toutes les tâches, pas seulement les révisions. Utilisez-le lorsque la guidance s'applique également aux sessions Claude Code interactives.
* **`REVIEW.md`** : guidance réservée à la révision, lue exclusivement lors des révisions de code. Utilisez-le pour les règles qui concernent strictement ce qu'il faut signaler ou ignorer lors de la révision et qui encombreraient votre `CLAUDE.md` général.

### CLAUDE.md

Code Review lit vos fichiers `CLAUDE.md` du référentiel et traite les violations nouvellement introduites comme des résultats au niveau nit. Cela fonctionne bidirectionnellement : si votre PR modifie le code d'une manière qui rend une déclaration `CLAUDE.md` obsolète, Claude signale que la documentation doit être mise à jour aussi.

Claude lit les fichiers `CLAUDE.md` à chaque niveau de votre hiérarchie de répertoires, de sorte que les règles dans le `CLAUDE.md` d'un sous-répertoire s'appliquent uniquement aux fichiers sous ce chemin. Consultez la [documentation de mémoire](/fr/memory) pour plus d'informations sur le fonctionnement de `CLAUDE.md`.

Pour la guidance spécifique à la révision que vous ne voulez pas appliquer aux sessions Claude Code générales, utilisez [`REVIEW.md`](#review-md) à la place.

### REVIEW\.md

Ajoutez un fichier `REVIEW.md` à la racine de votre référentiel pour les règles spécifiques à la révision. Utilisez-le pour encoder :

* Directives de style de l'entreprise ou de l'équipe : « préférer les retours précoces aux conditionnels imbriqués »
* Conventions spécifiques au langage ou au framework non couvertes par les linters
* Choses que Claude devrait toujours signaler : « tout nouvel itinéraire API doit avoir un test d'intégration »
* Choses que Claude devrait ignorer : « ne pas commenter le formatage dans le code généré sous `/gen/` »

Exemple `REVIEW.md` :

```markdown  theme={null}
# Directives de révision de code

## Toujours vérifier
- Les nouveaux points de terminaison API ont des tests d'intégration correspondants
- Les migrations de base de données sont rétrocompatibles
- Les messages d'erreur ne divulguent pas les détails internes aux utilisateurs

## Style
- Préférer les déclarations `match` aux vérifications `isinstance` chaînées
- Utiliser la journalisation structurée, pas l'interpolation de chaîne f dans les appels de journal

## Ignorer
- Fichiers générés sous `src/gen/`
- Modifications de formatage uniquement dans les fichiers `*.lock`
```

Claude découvre automatiquement `REVIEW.md` à la racine du référentiel. Aucune configuration nécessaire.

## Afficher l'utilisation

Allez à [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) pour voir l'activité de Code Review dans votre organisation. Le tableau de bord affiche :

| Section                     | Ce qu'il affiche                                                                                                    |
| :-------------------------- | :------------------------------------------------------------------------------------------------------------------ |
| PRs révisées                | Nombre quotidien de pull requests révisées sur la plage de temps sélectionnée                                       |
| Coût hebdomadaire           | Dépenses hebdomadaires sur Code Review                                                                              |
| Feedback                    | Nombre de commentaires de révision qui ont été résolus automatiquement parce qu'un développeur a résolu le problème |
| Répartition par référentiel | Comptages par référentiel des PRs révisées et des commentaires résolus                                              |

Le tableau des référentiels dans les paramètres d'administration affiche également le coût moyen par révision pour chaque référentiel.

## Tarification

Code Review est facturé en fonction de l'utilisation des tokens. Les révisions coûtent en moyenne 15 à 25 dollars, s'adaptant à la taille de la PR, à la complexité de la base de code et au nombre de problèmes nécessitant une vérification. L'utilisation de Code Review est facturée séparément via [l'utilisation supplémentaire](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) et ne compte pas par rapport à l'utilisation incluse de votre plan.

Le déclencheur de révision que vous choisissez affecte le coût total :

* **Après la création de PR uniquement** : s'exécute une fois par PR
* **Après chaque push** : s'exécute à chaque commit, multipliant le coût par le nombre de pushes

Les coûts apparaissent sur votre facture Anthropic indépendamment du fait que votre organisation utilise AWS Bedrock ou Google Vertex AI pour d'autres fonctionnalités Claude Code. Pour définir un plafond de dépenses mensuelles pour Code Review, allez à [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) et configurez la limite pour le service Claude Code Review.

Surveillez les dépenses via le graphique des coûts hebdomadaires dans [analytics](#view-usage) ou la colonne de coût moyen par référentiel dans les paramètres d'administration.

## Ressources connexes

Code Review est conçu pour fonctionner aux côtés du reste de Claude Code. Si vous voulez exécuter des révisions localement avant d'ouvrir une PR, avez besoin d'une configuration auto-hébergée ou voulez approfondir la façon dont `CLAUDE.md` façonne le comportement de Claude dans tous les outils, ces pages sont de bonnes prochaines étapes :

* [Plugins](/fr/discover-plugins) : parcourez la place de marché des plugins, y compris un plugin `code-review` pour exécuter des révisions à la demande localement avant de pousser
* [GitHub Actions](/fr/github-actions) : exécutez Claude dans vos propres flux de travail GitHub Actions pour une automatisation personnalisée au-delà de la révision de code
* [GitLab CI/CD](/fr/gitlab-ci-cd) : intégration Claude auto-hébergée pour les pipelines GitLab
* [Memory](/fr/memory) : comment les fichiers `CLAUDE.md` fonctionnent dans Claude Code
* [Analytics](/fr/analytics) : suivez l'utilisation de Claude Code au-delà de la révision de code
