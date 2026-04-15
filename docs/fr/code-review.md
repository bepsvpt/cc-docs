> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Révision de code

> Configurez des révisions de PR automatisées qui détectent les erreurs logiques, les vulnérabilités de sécurité et les régressions en utilisant l'analyse multi-agents de votre base de code complète

<Note>
  Code Review est en aperçu de recherche, disponible pour les abonnements [Teams et Enterprise](https://claude.ai/admin-settings/claude-code). Il n'est pas disponible pour les organisations avec [Zero Data Retention](/fr/zero-data-retention) activé.
</Note>

Code Review analyse vos pull requests GitHub et publie les résultats sous forme de commentaires en ligne sur les lignes de code où il a trouvé des problèmes. Une flotte d'agents spécialisés examine les modifications de code dans le contexte de votre base de code complète, en recherchant les erreurs logiques, les vulnérabilités de sécurité, les cas limites cassés et les régressions subtiles.

Les résultats sont étiquetés par gravité et n'approuvent ni ne bloquent votre PR, de sorte que les flux de travail d'examen existants restent intacts. Vous pouvez affiner ce que Claude signale en ajoutant un fichier `CLAUDE.md` ou `REVIEW.md` à votre référentiel.

Pour exécuter Claude dans votre propre infrastructure CI au lieu de ce service géré, consultez [GitHub Actions](/fr/github-actions) ou [GitLab CI/CD](/fr/gitlab-ci-cd). Pour les référentiels sur une instance GitHub auto-hébergée, consultez [GitHub Enterprise Server](/fr/github-enterprise-server).

Cette page couvre :

* [Comment fonctionnent les révisions](#how-reviews-work)
* [Configuration](#set-up-code-review)
* [Déclenchement manuel des révisions](#manually-trigger-reviews) avec `@claude review` et `@claude review once`
* [Personnalisation des révisions](#customize-reviews) avec `CLAUDE.md` et `REVIEW.md`
* [Tarification](#pricing)
* [Dépannage](#troubleshooting) des exécutions échouées et des commentaires manquants

## Comment fonctionnent les révisions

Une fois qu'un administrateur [active Code Review](#set-up-code-review) pour votre organisation, les révisions se déclenchent à l'ouverture d'une PR, à chaque push, ou sur demande manuelle, selon le comportement configuré du référentiel. Commenter `@claude review` [démarre les révisions sur une PR](#manually-trigger-reviews) dans n'importe quel mode.

Lorsqu'une révision s'exécute, plusieurs agents analysent le diff et le code environnant en parallèle sur l'infrastructure Anthropic. Chaque agent recherche une classe de problème différente, puis une étape de vérification vérifie les candidats par rapport au comportement réel du code pour filtrer les faux positifs. Les résultats sont dédupliqués, classés par gravité et publiés sous forme de commentaires en ligne sur les lignes spécifiques où les problèmes ont été trouvés. Si aucun problème n'est trouvé, Claude publie un court commentaire de confirmation sur la PR.

Les révisions s'adaptent en coût à la taille et à la complexité de la PR, se complétant en moyenne en 20 minutes. Les administrateurs peuvent surveiller l'activité de révision et les dépenses via le [tableau de bord analytique](#view-usage).

### Niveaux de gravité

Chaque résultat est étiqueté avec un niveau de gravité :

| Marqueur | Gravité     | Signification                                                                  |
| :------- | :---------- | :----------------------------------------------------------------------------- |
| 🔴       | Important   | Un bug qui devrait être corrigé avant la fusion                                |
| 🟡       | Nit         | Un problème mineur, utile à corriger mais non bloquant                         |
| 🟣       | Préexistant | Un bug qui existe dans la base de code mais n'a pas été introduit par cette PR |

Les résultats incluent une section de raisonnement étendu réductible que vous pouvez développer pour comprendre pourquoi Claude a signalé le problème et comment il a vérifié le problème.

### Sortie de l'exécution de vérification

Au-delà des commentaires de révision en ligne, chaque révision remplit l'exécution de vérification **Claude Code Review** qui apparaît aux côtés de vos vérifications CI. Développez son lien **Details** pour voir un résumé de chaque résultat en un seul endroit, trié par gravité :

| Gravité      | Fichier:Ligne             | Problème                                                                                                   |
| ------------ | ------------------------- | ---------------------------------------------------------------------------------------------------------- |
| 🔴 Important | `src/auth/session.ts:142` | L'actualisation du token entre en concurrence avec la déconnexion, laissant les sessions obsolètes actives |
| 🟡 Nit       | `src/auth/session.ts:88`  | `parseExpiry` retourne silencieusement 0 sur une entrée malformée                                          |

Chaque résultat apparaît également comme une annotation dans l'onglet **Files changed**, marqué directement sur les lignes de diff pertinentes. Les résultats importants s'affichent avec un marqueur rouge, les nits avec un avertissement jaune, et les bugs préexistants avec un avis gris. Les annotations et le tableau de gravité sont écrits dans l'exécution de vérification indépendamment des commentaires de révision en ligne, de sorte qu'ils restent disponibles même si GitHub rejette un commentaire en ligne sur une ligne qui a bougé.

L'exécution de vérification se termine toujours avec une conclusion neutre, de sorte qu'elle ne bloque jamais la fusion via les règles de protection de branche. Si vous souhaitez conditionner les fusions aux résultats de Code Review, lisez la répartition de gravité à partir de la sortie de l'exécution de vérification dans votre propre CI. La dernière ligne du texte Details est un commentaire lisible par machine que votre flux de travail peut analyser avec `gh` et jq :

```bash theme={null}
gh api repos/OWNER/REPO/check-runs/CHECK_RUN_ID \
  --jq '.output.text | split("bughunter-severity: ")[1] | split(" -->")[0] | fromjson'
```

Cela retourne un objet JSON avec des comptages par gravité, par exemple `{"normal": 2, "nit": 1, "pre_existing": 0}`. La clé `normal` contient le nombre de résultats importants ; une valeur non nulle signifie que Claude a trouvé au moins un bug à corriger avant la fusion.

### Ce que Code Review vérifie

Par défaut, Code Review se concentre sur la correction : les bugs qui cassent la production, pas les préférences de formatage ou la couverture de test manquante. Vous pouvez élargir ce qu'il vérifie en [ajoutant des fichiers de guidance](#customize-reviews) à votre référentiel.

## Configurer Code Review

Un administrateur active Code Review une fois pour l'organisation et sélectionne les référentiels à inclure.

<Steps>
  <Step title="Ouvrir les paramètres d'administration Claude Code">
    Allez à [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) et trouvez la section Code Review. Vous avez besoin d'un accès administrateur à votre organisation Claude et de la permission d'installer des GitHub Apps dans votre organisation GitHub.
  </Step>

  <Step title="Démarrer la configuration">
    Cliquez sur **Setup**. Cela commence le flux d'installation de GitHub App.
  </Step>

  <Step title="Installer la GitHub App Claude">
    Suivez les invites pour installer la GitHub App Claude à votre organisation GitHub. L'application demande ces permissions de référentiel :

    * **Contents** : lecture et écriture
    * **Issues** : lecture et écriture
    * **Pull requests** : lecture et écriture

    Code Review utilise l'accès en lecture aux contenus et l'accès en écriture aux pull requests. L'ensemble de permissions plus large supporte également [GitHub Actions](/fr/github-actions) si vous l'activez plus tard.
  </Step>

  <Step title="Sélectionner les référentiels">
    Choisissez les référentiels à activer pour Code Review. Si vous ne voyez pas un référentiel, assurez-vous d'avoir donné à la GitHub App Claude l'accès pendant l'installation. Vous pouvez ajouter plus de référentiels plus tard.
  </Step>

  <Step title="Définir les déclencheurs de révision par référentiel">
    Une fois la configuration terminée, la section Code Review affiche vos référentiels dans un tableau. Pour chaque référentiel, utilisez la liste déroulante **Review Behavior** pour choisir quand les révisions s'exécutent :

    * **Once after PR creation** : la révision s'exécute une fois à l'ouverture d'une PR ou marquée comme prête pour révision
    * **After every push** : la révision s'exécute à chaque push vers la branche PR, détectant les nouveaux problèmes à mesure que la PR évolue et résolvant automatiquement les threads lorsque vous corrigez les problèmes signalés
    * **Manual** : les révisions commencent uniquement quand quelqu'un [commente `@claude review` ou `@claude review once` sur une PR](#manually-trigger-reviews) ; `@claude review` abonne également la PR aux révisions lors des pushes ultérieurs

    Réviser à chaque push exécute le plus de révisions et coûte le plus cher. Le mode manuel est utile pour les référentiels à fort trafic où vous souhaitez opter pour des PR spécifiques dans la révision, ou pour commencer à réviser vos PR uniquement une fois qu'elles sont prêtes.
  </Step>
</Steps>

Le tableau des référentiels affiche également le coût moyen par révision pour chaque référentiel en fonction de l'activité récente. Utilisez le menu d'actions de ligne pour activer ou désactiver Code Review par référentiel, ou pour supprimer complètement un référentiel.

Pour vérifier la configuration, ouvrez une PR de test. Si vous avez choisi un déclencheur automatique, une exécution de vérification nommée **Claude Code Review** apparaît dans quelques minutes. Si vous avez choisi Manual, commentez `@claude review` sur la PR pour démarrer la première révision. Si aucune exécution de vérification n'apparaît, confirmez que le référentiel est listé dans vos paramètres d'administration et que la GitHub App Claude y a accès.

## Déclencher manuellement les révisions

Deux commandes de commentaire démarrent une révision à la demande. Les deux fonctionnent quel que soit le déclencheur configuré du référentiel, de sorte que vous pouvez les utiliser pour opter pour des PR spécifiques dans la révision en mode Manual ou pour obtenir une re-révision immédiate dans d'autres modes.

| Commande              | Ce qu'elle fait                                                                                |
| :-------------------- | :--------------------------------------------------------------------------------------------- |
| `@claude review`      | Démarre une révision et abonne la PR aux révisions déclenchées par push à partir de maintenant |
| `@claude review once` | Démarre une seule révision sans abonner la PR aux pushes futurs                                |

Utilisez `@claude review once` quand vous souhaitez des commentaires sur l'état actuel d'une PR mais ne souhaitez pas que chaque push ultérieur entraîne une révision. Cela est utile pour les PR longues avec des pushes fréquents, ou quand vous souhaitez un deuxième avis ponctuel sans modifier le comportement de révision de la PR.

Pour que l'une ou l'autre commande déclenche une révision :

* Publiez-la comme un commentaire PR de haut niveau, pas un commentaire en ligne sur une ligne de diff
* Mettez la commande au début du commentaire, avec `once` sur la même ligne si vous utilisez la forme ponctuelle
* Vous devez avoir un accès propriétaire, membre ou collaborateur au référentiel
* La PR doit être ouverte

Contrairement aux déclencheurs automatiques, les déclencheurs manuels s'exécutent sur les PR brouillon, car une demande explicite signale que vous souhaitez la révision maintenant quel que soit le statut de brouillon.

Si une révision s'exécute déjà sur cette PR, la demande est mise en file d'attente jusqu'à ce que la révision en cours se termine. Vous pouvez surveiller la progression via l'exécution de vérification sur la PR.

## Personnaliser les révisions

Code Review lit deux fichiers de votre référentiel pour guider ce qu'il signale. Les deux s'ajoutent aux vérifications de correction par défaut :

* **`CLAUDE.md`** : instructions de projet partagées que Claude Code utilise pour toutes les tâches, pas seulement les révisions. Utilisez-le quand la guidance s'applique également aux sessions Claude Code interactives.
* **`REVIEW.md`** : guidance de révision uniquement, lue exclusivement lors des révisions de code. Utilisez-le pour les règles qui concernent strictement ce qu'il faut signaler ou ignorer lors de la révision et qui encombreraient votre `CLAUDE.md` général.

### CLAUDE.md

Code Review lit vos fichiers `CLAUDE.md` du référentiel et traite les violations nouvellement introduites comme des résultats au niveau nit. Cela fonctionne bidirectionnellement : si votre PR modifie le code d'une manière qui rend une déclaration `CLAUDE.md` obsolète, Claude signale que les docs doivent être mises à jour aussi.

Claude lit les fichiers `CLAUDE.md` à chaque niveau de votre hiérarchie de répertoires, donc les règles dans le `CLAUDE.md` d'un sous-répertoire s'appliquent uniquement aux fichiers sous ce chemin. Consultez la [documentation de mémoire](/fr/memory) pour plus d'informations sur le fonctionnement de `CLAUDE.md`.

Pour la guidance spécifique à la révision que vous ne souhaitez pas appliquer aux sessions Claude Code générales, utilisez [`REVIEW.md`](#review-md) à la place.

### REVIEW\.md

Ajoutez un fichier `REVIEW.md` à la racine de votre référentiel pour les règles spécifiques à la révision. Utilisez-le pour encoder :

* Directives de style de l'entreprise ou de l'équipe : « préférer les retours précoces aux conditionnels imbriqués »
* Conventions spécifiques au langage ou au framework non couvertes par les linters
* Choses que Claude devrait toujours signaler : « tout nouvel itinéraire API doit avoir un test d'intégration »
* Choses que Claude devrait ignorer : « ne pas commenter le formatage dans le code généré sous `/gen/` »

Exemple `REVIEW.md` :

```markdown theme={null}
# Code Review Guidelines

## Always check
- New API endpoints have corresponding integration tests
- Database migrations are backward-compatible
- Error messages don't leak internal details to users

## Style
- Prefer `match` statements over chained `isinstance` checks
- Use structured logging, not f-string interpolation in log calls

## Skip
- Generated files under `src/gen/`
- Formatting-only changes in `*.lock` files
```

Claude découvre automatiquement `REVIEW.md` à la racine du référentiel. Aucune configuration nécessaire.

## Afficher l'utilisation

Allez à [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) pour voir l'activité Code Review dans votre organisation. Le tableau de bord affiche :

| Section              | Ce qu'il affiche                                                                                         |
| :------------------- | :------------------------------------------------------------------------------------------------------- |
| PRs reviewed         | Nombre quotidien de pull requests examinées sur la plage de temps sélectionnée                           |
| Cost weekly          | Dépenses hebdomadaires sur Code Review                                                                   |
| Feedback             | Nombre de commentaires de révision qui ont été auto-résolus parce qu'un développeur a résolu le problème |
| Repository breakdown | Comptages par référentiel des PR examinées et des commentaires résolus                                   |

Le tableau des référentiels dans les paramètres d'administration affiche également le coût moyen par révision pour chaque référentiel.

## Tarification

Code Review est facturé en fonction de l'utilisation des tokens. Chaque révision coûte en moyenne 15 à 25 dollars, s'adaptant à la taille de la PR, à la complexité de la base de code et au nombre de problèmes nécessitant une vérification. L'utilisation de Code Review est facturée séparément via [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) et ne compte pas par rapport à l'utilisation incluse de votre plan.

Le déclencheur de révision que vous choisissez affecte le coût total :

* **Once after PR creation** : s'exécute une fois par PR
* **After every push** : s'exécute à chaque push, multipliant le coût par le nombre de pushes
* **Manual** : aucune révision jusqu'à ce que quelqu'un commente `@claude review` sur une PR

Dans n'importe quel mode, commenter `@claude review` [opte la PR dans les révisions déclenchées par push](#manually-trigger-reviews), de sorte que des coûts supplémentaires s'accumulent par push après ce commentaire. Pour exécuter une seule révision sans abonner à des pushes futurs, commentez `@claude review once` à la place.

Les coûts apparaissent sur votre facture Anthropic quel que soit le fait que votre organisation utilise AWS Bedrock ou Google Vertex AI pour d'autres fonctionnalités Claude Code. Pour définir un plafond de dépenses mensuelles pour Code Review, allez à [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) et configurez la limite pour le service Claude Code Review.

Surveillez les dépenses via le graphique de coût hebdomadaire dans [analytics](#view-usage) ou la colonne de coût moyen par référentiel dans les paramètres d'administration.

## Dépannage

Les exécutions de révision sont au mieux. Une exécution échouée ne bloque jamais votre PR, mais elle ne se réessaye pas non plus d'elle-même. Cette section couvre comment récupérer d'une exécution échouée et où chercher quand l'exécution de vérification signale des problèmes que vous ne pouvez pas trouver.

### Redéclencher une révision échouée ou expirée

Quand l'infrastructure de révision rencontre une erreur interne ou dépasse sa limite de temps, l'exécution de vérification se termine avec un titre de **Code review encountered an error** ou **Code review timed out**. La conclusion est toujours neutre, de sorte que rien ne bloque votre fusion, mais aucun résultat n'est publié.

Pour exécuter la révision à nouveau, commentez `@claude review once` sur la PR. Cela démarre une révision fraîche sans abonner la PR aux pushes futurs. Si la PR est déjà abonnée aux révisions déclenchées par push, pousser un nouveau commit démarre également une nouvelle révision.

Le bouton **Re-run** dans l'onglet Checks de GitHub ne redéclenche pas Code Review. Utilisez la commande de commentaire ou un nouveau push à la place.

### Trouver les problèmes qui ne s'affichent pas comme des commentaires en ligne

Si le titre de l'exécution de vérification dit que des problèmes ont été trouvés mais que vous ne voyez pas de commentaires de révision en ligne sur le diff, cherchez dans ces autres emplacements où les résultats sont surfacés :

* **Check run Details** : cliquez sur **Details** à côté de la vérification Claude Code Review dans l'onglet Checks. Le tableau de gravité liste chaque résultat avec son fichier, sa ligne et son résumé quel que soit le fait que le commentaire en ligne ait été accepté.
* **Files changed annotations** : ouvrez l'onglet **Files changed** sur la PR. Les résultats s'affichent comme des annotations attachées directement aux lignes de diff, séparées des commentaires de révision.
* **Review body** : si vous avez poussé vers la PR pendant qu'une révision s'exécutait, certains résultats peuvent référencer des lignes qui n'existent plus dans le diff actuel. Ceux-ci apparaissent sous un titre **Additional findings** dans le texte du corps de révision plutôt que comme des commentaires en ligne.

## Ressources connexes

Code Review est conçu pour fonctionner aux côtés du reste de Claude Code. Si vous souhaitez exécuter des révisions localement avant d'ouvrir une PR, avez besoin d'une configuration auto-hébergée, ou souhaitez approfondir la façon dont `CLAUDE.md` façonne le comportement de Claude dans tous les outils, ces pages sont de bons prochains arrêts :

* [Plugins](/fr/discover-plugins) : parcourez la place de marché des plugins, y compris un plugin `code-review` pour exécuter des révisions à la demande localement avant de pousser
* [GitHub Actions](/fr/github-actions) : exécutez Claude dans vos propres flux de travail GitHub Actions pour une automatisation personnalisée au-delà de la révision de code
* [GitLab CI/CD](/fr/gitlab-ci-cd) : intégration Claude auto-hébergée pour les pipelines GitLab
* [Memory](/fr/memory) : comment les fichiers `CLAUDE.md` fonctionnent dans Claude Code
* [Analytics](/fr/analytics) : suivez l'utilisation de Claude Code au-delà de la révision de code
