> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Accélérez les réponses avec le mode rapide

> Obtenez des réponses Opus 4.6 plus rapides dans Claude Code en activant le mode rapide.

<Note>
  Le mode rapide est en [aperçu de recherche](#research-preview). La fonctionnalité, la tarification et la disponibilité peuvent changer en fonction des commentaires.
</Note>

Le mode rapide est une configuration haute vitesse pour Claude Opus 4.6, rendant le modèle 2,5 fois plus rapide à un coût par token plus élevé. Activez-le avec `/fast` quand vous avez besoin de vitesse pour un travail interactif comme l'itération rapide ou le débogage en direct, et désactivez-le quand le coût importe plus que la latence.

Le mode rapide n'est pas un modèle différent. Il utilise le même Opus 4.6 avec une configuration API différente qui privilégie la vitesse à l'efficacité des coûts. Vous obtenez une qualité et des capacités identiques, juste des réponses plus rapides.

<Note>
  Le mode rapide nécessite Claude Code v2.1.36 ou ultérieur. Vérifiez votre version avec `claude --version`.
</Note>

Ce qu'il faut savoir :

* Utilisez `/fast` pour activer/désactiver le mode rapide dans Claude Code CLI. Également disponible via `/fast` dans l'extension Claude Code VS Code.
* La tarification du mode rapide pour Opus 4.6 commence à 30 \$/150 MTok. Le mode rapide est disponible avec une réduction de 50 % pour tous les plans jusqu'à 23 h 59 PT le 16 février.
* Disponible pour tous les utilisateurs de Claude Code sur les plans d'abonnement (Pro/Max/Team/Enterprise) et Claude Console.
* Pour les utilisateurs de Claude Code sur les plans d'abonnement (Pro/Max/Team/Enterprise), le mode rapide est disponible via l'utilisation supplémentaire uniquement et n'est pas inclus dans les limites de taux d'utilisation de l'abonnement.

Cette page couvre comment [activer le mode rapide](#toggle-fast-mode), son [compromis de coût](#understand-the-cost-tradeoff), [quand l'utiliser](#decide-when-to-use-fast-mode), les [exigences](#requirements), l'[opt-in par session](#require-per-session-opt-in), et le [comportement des limites de taux](#handle-rate-limits).

## Activer le mode rapide

Activez le mode rapide de l'une de ces deux façons :

* Tapez `/fast` et appuyez sur Tab pour activer ou désactiver
* Définissez `"fastMode": true` dans votre [fichier de paramètres utilisateur](/fr/settings)

Par défaut, le mode rapide persiste entre les sessions. Les administrateurs peuvent configurer le mode rapide pour qu'il se réinitialise à chaque session. Consultez [opt-in par session](#require-per-session-opt-in) pour plus de détails.

Pour la meilleure efficacité des coûts, activez le mode rapide au début d'une session plutôt que de basculer en milieu de conversation. Consultez [comprendre le compromis de coût](#understand-the-cost-tradeoff) pour plus de détails.

Quand vous activez le mode rapide :

* Si vous êtes sur un modèle différent, Claude Code bascule automatiquement vers Opus 4.6
* Vous verrez un message de confirmation : « Mode rapide ACTIVÉ »
* Une petite icône `↯` apparaît à côté de l'invite pendant que le mode rapide est actif
* Exécutez `/fast` à nouveau à tout moment pour vérifier si le mode rapide est activé ou désactivé

Quand vous désactivez le mode rapide avec `/fast` à nouveau, vous restez sur Opus 4.6. Le modèle ne revient pas à votre modèle précédent. Pour basculer vers un modèle différent, utilisez `/model`.

## Comprendre le compromis de coût

Le mode rapide a une tarification par token plus élevée que l'Opus 4.6 standard :

| Mode                              | Entrée (MTok) | Sortie (MTok) |
| --------------------------------- | ------------- | ------------- |
| Mode rapide sur Opus 4.6 (\<200K) | 30 \$         | 150 \$        |
| Mode rapide sur Opus 4.6 (>200K)  | 60 \$         | 225 \$        |

Le mode rapide est compatible avec la fenêtre de contexte étendue de 1M token.

Quand vous basculez en mode rapide en milieu de conversation, vous payez le prix complet du token d'entrée non mis en cache du mode rapide pour tout le contexte de la conversation. Cela coûte plus cher que si vous aviez activé le mode rapide dès le départ.

## Décider quand utiliser le mode rapide

Le mode rapide est idéal pour le travail interactif où la latence de réponse importe plus que le coût :

* Itération rapide sur les modifications de code
* Sessions de débogage en direct
* Travail sensible au temps avec des délais serrés

Le mode standard est meilleur pour :

* Les tâches autonomes longues où la vitesse importe moins
* Le traitement par lots ou les pipelines CI/CD
* Les charges de travail sensibles aux coûts

### Mode rapide par rapport au niveau d'effort

Le mode rapide et le niveau d'effort affectent tous deux la vitesse de réponse, mais différemment :

| Paramètre                     | Effet                                                                                                           |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Mode rapide**               | Même qualité de modèle, latence inférieure, coût plus élevé                                                     |
| **Niveau d'effort inférieur** | Moins de temps de réflexion, réponses plus rapides, qualité potentiellement inférieure sur les tâches complexes |

Vous pouvez combiner les deux : utilisez le mode rapide avec un [niveau d'effort](/fr/model-config#adjust-effort-level) inférieur pour une vitesse maximale sur les tâches simples.

## Exigences

Le mode rapide nécessite tous les éléments suivants :

* **Non disponible sur les fournisseurs cloud tiers** : le mode rapide n'est pas disponible sur Amazon Bedrock, Google Vertex AI ou Microsoft Azure Foundry. Le mode rapide est disponible via l'API Anthropic Console et pour les plans d'abonnement Claude utilisant l'utilisation supplémentaire.
* **Utilisation supplémentaire activée** : votre compte doit avoir l'utilisation supplémentaire activée, ce qui permet la facturation au-delà de l'utilisation incluse dans votre plan. Pour les comptes individuels, activez ceci dans vos [paramètres de facturation Console](https://platform.claude.com/settings/organization/billing). Pour Teams et Enterprise, un administrateur doit activer l'utilisation supplémentaire pour l'organisation.

<Note>
  L'utilisation du mode rapide est facturée directement à l'utilisation supplémentaire, même si vous avez une utilisation restante sur votre plan. Cela signifie que les tokens du mode rapide ne comptent pas par rapport à l'utilisation incluse de votre plan et sont facturés au tarif du mode rapide à partir du premier token.
</Note>

* **Activation par l'administrateur pour Teams et Enterprise** : le mode rapide est désactivé par défaut pour les organisations Teams et Enterprise. Un administrateur doit explicitement [activer le mode rapide](#enable-fast-mode-for-your-organization) avant que les utilisateurs puissent y accéder.

<Note>
  Si votre administrateur n'a pas activé le mode rapide pour votre organisation, la commande `/fast` affichera « Le mode rapide a été désactivé par votre organisation. »
</Note>

### Activer le mode rapide pour votre organisation

Les administrateurs peuvent activer le mode rapide dans :

* **Console** (clients API) : [Préférences Claude Code](https://platform.claude.com/claude-code/preferences)
* **Claude AI** (Teams et Enterprise) : [Paramètres administrateur > Claude Code](https://claude.ai/admin-settings/claude-code)

Une autre option pour désactiver complètement le mode rapide est de définir `CLAUDE_CODE_DISABLE_FAST_MODE=1`. Consultez [Variables d'environnement](/fr/settings#environment-variables).

### Opt-in par session

Par défaut, le mode rapide persiste entre les sessions : si un utilisateur active le mode rapide, il reste activé dans les sessions futures. Les administrateurs sur les plans [Teams](https://claude.com/pricing#team-&-enterprise) ou [Enterprise](https://anthropic.com/contact-sales) peuvent empêcher cela en définissant `fastModePerSessionOptIn` à `true` dans les [paramètres gérés](/fr/settings#settings-files) ou les [paramètres gérés par le serveur](/fr/server-managed-settings). Cela fait que chaque session commence avec le mode rapide désactivé, obligeant les utilisateurs à l'activer explicitement avec `/fast`.

```json  theme={null}
{
  "fastModePerSessionOptIn": true
}
```

Ceci est utile pour contrôler les coûts dans les organisations où les utilisateurs exécutent plusieurs sessions simultanées. Les utilisateurs peuvent toujours activer le mode rapide avec `/fast` quand ils ont besoin de vitesse, mais il se réinitialise au début de chaque nouvelle session. La préférence du mode rapide de l'utilisateur est toujours enregistrée, donc supprimer ce paramètre restaure le comportement persistant par défaut.

## Gérer les limites de taux

Le mode rapide a des limites de taux séparées de l'Opus 4.6 standard. Quand vous atteignez la limite de taux du mode rapide ou que vous manquez de crédits d'utilisation supplémentaire :

1. Le mode rapide bascule automatiquement vers l'Opus 4.6 standard
2. L'icône `↯` devient grise pour indiquer le refroidissement
3. Vous continuez à travailler à la vitesse et à la tarification standard
4. Quand le refroidissement expire, le mode rapide se réactive automatiquement

Pour désactiver manuellement le mode rapide au lieu d'attendre le refroidissement, exécutez `/fast` à nouveau.

## Aperçu de recherche

Le mode rapide est une fonctionnalité d'aperçu de recherche. Cela signifie :

* La fonctionnalité peut changer en fonction des commentaires
* La disponibilité et la tarification sont sujettes à changement
* La configuration API sous-jacente peut évoluer

Signalez les problèmes ou les commentaires via vos canaux de support Anthropic habituels.

## Voir aussi

* [Configuration du modèle](/fr/model-config) : basculer les modèles et ajuster les niveaux d'effort
* [Gérer les coûts efficacement](/fr/costs) : suivre l'utilisation des tokens et réduire les coûts
* [Configuration de la ligne d'état](/fr/statusline) : afficher les informations du modèle et du contexte
