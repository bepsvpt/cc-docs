> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Zéro conservation des données

> Découvrez la conservation zéro des données (ZDR) pour Claude Code sur Claude for Enterprise, y compris la portée, les fonctionnalités désactivées et comment demander l'activation.

La conservation zéro des données (ZDR) est disponible pour Claude Code lorsqu'il est utilisé via Claude for Enterprise. Lorsque ZDR est activée, les invites et les réponses du modèle générées lors des sessions Claude Code sont traitées en temps réel et ne sont pas conservées par Anthropic après le retour de la réponse, sauf si nécessaire pour se conformer à la loi ou combattre les abus.

ZDR sur Claude for Enterprise donne aux clients d'entreprise la possibilité d'utiliser Claude Code avec zéro conservation des données et d'accéder aux capacités administratives :

* Contrôles des coûts par utilisateur
* Tableau de bord [Analytics](/fr/analytics)
* [Paramètres gérés par le serveur](/fr/server-managed-settings)
* Journaux d'audit

ZDR pour Claude Code sur Claude for Enterprise s'applique uniquement à la plateforme directe d'Anthropic. Pour les déploiements de Claude sur AWS Bedrock, Google Vertex AI ou Microsoft Foundry, consultez les politiques de conservation des données de ces plateformes.

## Portée de ZDR

ZDR couvre l'inférence Claude Code sur Claude for Enterprise.

<Warning>
  ZDR est activée sur la base de chaque organisation. Chaque nouvelle organisation nécessite que ZDR soit activée séparément par votre équipe de compte Anthropic. ZDR ne s'applique pas automatiquement aux nouvelles organisations créées sous le même compte. Contactez votre équipe de compte pour activer ZDR pour toute nouvelle organisation.
</Warning>

### Ce que ZDR couvre

ZDR couvre les appels d'inférence du modèle effectués via Claude Code sur Claude for Enterprise. Lorsque vous utilisez Claude Code dans votre terminal, les invites que vous envoyez et les réponses que Claude génère ne sont pas conservées par Anthropic. Cela s'applique quel que soit le modèle Claude utilisé.

### Ce que ZDR ne couvre pas

ZDR ne s'étend pas aux éléments suivants, même pour les organisations avec ZDR activée. Ces fonctionnalités suivent les [politiques standard de conservation des données](/fr/data-usage#data-retention) :

| Fonctionnalité                         | Détails                                                                                                                                                                                                                                                                                                                                                 |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Chat sur claude.ai                     | Les conversations de chat via l'interface web Claude for Enterprise ne sont pas couvertes par ZDR.                                                                                                                                                                                                                                                      |
| Cowork                                 | Les sessions Cowork ne sont pas couvertes par ZDR.                                                                                                                                                                                                                                                                                                      |
| Claude Code Analytics                  | Ne stocke pas les invites ou les réponses du modèle, mais collecte les métadonnées de productivité telles que les e-mails de compte et les statistiques d'utilisation. Les métriques de contribution ne sont pas disponibles pour les organisations ZDR ; le [tableau de bord analytics](/fr/analytics) affiche uniquement les métriques d'utilisation. |
| Gestion des utilisateurs et des sièges | Les données administratives telles que les e-mails de compte et les attributions de sièges sont conservées selon les politiques standard.                                                                                                                                                                                                               |
| Intégrations tierces                   | Les données traitées par des outils tiers, des serveurs MCP ou d'autres intégrations externes ne sont pas couvertes par ZDR. Examinez indépendamment les pratiques de traitement des données de ces services.                                                                                                                                           |

## Fonctionnalités désactivées sous ZDR

Lorsque ZDR est activée pour une organisation Claude Code sur Claude for Enterprise, certaines fonctionnalités qui nécessitent de stocker les invites ou les complétions sont automatiquement désactivées au niveau du backend :

| Fonctionnalité                                                             | Raison                                                                                     |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| [Claude Code sur le Web](/fr/claude-code-on-the-web)                       | Nécessite le stockage côté serveur de l'historique des conversations.                      |
| [Sessions distantes](/fr/desktop#remote-sessions) de l'application Desktop | Nécessite des données de session persistantes qui incluent les invites et les complétions. |
| Soumission de commentaires (`/feedback`)                                   | La soumission de commentaires envoie les données de conversation à Anthropic.              |

Ces fonctionnalités sont bloquées au niveau du backend quel que soit l'affichage côté client. Si vous voyez une fonctionnalité désactivée dans le terminal Claude Code au démarrage, toute tentative d'utilisation retourne une erreur indiquant que les politiques de l'organisation ne permettent pas cette action.

Les futures fonctionnalités peuvent également être désactivées si elles nécessitent de stocker les invites ou les complétions.

## Conservation des données pour les violations de politique

Même avec ZDR activée, Anthropic peut conserver les données si la loi l'exige ou pour résoudre les violations de la politique d'utilisation. Si une session est signalée pour une violation de politique, Anthropic peut conserver les entrées et sorties associées pendant jusqu'à 2 ans, conformément à la politique ZDR standard d'Anthropic.

## Demander ZDR

Pour demander ZDR pour Claude Code sur Claude for Enterprise, contactez votre équipe de compte Anthropic. Votre équipe de compte soumettra la demande en interne, et Anthropic examinera et activera ZDR sur votre organisation après avoir confirmé l'admissibilité. Toutes les actions d'activation sont enregistrées dans les journaux d'audit.

Si vous utilisez actuellement ZDR pour Claude Code via des clés API à l'usage, vous pouvez passer à Claude for Enterprise pour accéder aux fonctionnalités administratives tout en maintenant ZDR pour Claude Code. Contactez votre équipe de compte pour coordonner la migration.
