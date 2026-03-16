> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Utilisation des données

> Découvrez les politiques d'utilisation des données d'Anthropic pour Claude

## Politiques de données

### Politique de formation aux données

**Utilisateurs grand public (plans Free, Pro et Max)** :
Nous vous donnons le choix de permettre à vos données d'être utilisées pour améliorer les futurs modèles Claude. Nous formerons de nouveaux modèles en utilisant les données des comptes Free, Pro et Max lorsque ce paramètre est activé (y compris lorsque vous utilisez Claude Code à partir de ces comptes).

**Utilisateurs commerciaux** : (plans Team et Enterprise, API, plateformes tierces et Claude Gov) maintiennent les politiques existantes : Anthropic ne forme pas de modèles génératifs en utilisant le code ou les invites envoyés à Claude Code selon les conditions commerciales, sauf si le client a choisi de nous fournir ses données pour l'amélioration du modèle (par exemple, le [Programme de partenariat pour développeurs](https://support.claude.com/en/articles/11174108-about-the-development-partner-program)).

### Programme de partenariat pour développeurs

Si vous acceptez explicitement les méthodes pour nous fournir des matériaux à utiliser pour la formation, comme via le [Programme de partenariat pour développeurs](https://support.claude.com/en/articles/11174108-about-the-development-partner-program), nous pouvons utiliser ces matériaux fournis pour former nos modèles. Un administrateur d'organisation peut accepter explicitement le Programme de partenariat pour développeurs pour son organisation. Notez que ce programme est disponible uniquement pour l'API Anthropic propriétaire, et non pour les utilisateurs de Bedrock ou Vertex.

### Retours d'information à l'aide de la commande `/bug`

Si vous choisissez de nous envoyer des retours d'information sur Claude Code à l'aide de la commande `/bug`, nous pouvons utiliser vos retours d'information pour améliorer nos produits et services. Les transcriptions partagées via `/bug` sont conservées pendant 5 ans.

### Sondages de qualité de session

Lorsque vous voyez l'invite « Comment Claude s'en sort-il cette session ? » dans Claude Code, répondre à ce sondage (y compris en sélectionnant « Ignorer »), seule votre note numérique (1, 2, 3 ou ignorer) est enregistrée. Nous ne collectons ni ne stockons de transcriptions de conversation, d'entrées, de sorties ou d'autres données de session dans le cadre de ce sondage. Contrairement aux retours d'information avec pouces vers le haut/bas ou aux rapports `/bug`, ce sondage de qualité de session est une simple métrique de satisfaction du produit. Vos réponses à ce sondage n'affectent pas vos préférences de formation aux données et ne peuvent pas être utilisées pour former nos modèles d'IA.

Pour désactiver ces sondages, définissez `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`. Le sondage est également automatiquement désactivé lors de l'utilisation de fournisseurs tiers (Bedrock, Vertex, Foundry) ou lorsque la télémétrie est désactivée.

### Conservation des données

Anthropic conserve les données de Claude Code en fonction de votre type de compte et de vos préférences.

**Utilisateurs grand public (plans Free, Pro et Max)** :

* Utilisateurs qui autorisent l'utilisation des données pour l'amélioration du modèle : période de conservation de 5 ans pour soutenir le développement et les améliorations de sécurité du modèle
* Utilisateurs qui n'autorisent pas l'utilisation des données pour l'amélioration du modèle : période de conservation de 30 jours
* Les paramètres de confidentialité peuvent être modifiés à tout moment sur [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls).

**Utilisateurs commerciaux (Team, Enterprise et API)** :

* Standard : période de conservation de 30 jours
* [Conservation zéro des données](/fr/zero-data-retention) : disponible pour Claude Code sur Claude for Enterprise. La conservation zéro des données est activée par organisation ; chaque nouvelle organisation doit avoir la conservation zéro des données activée séparément par votre équipe de compte
* Mise en cache locale : les clients Claude Code peuvent stocker les sessions localement pendant jusqu'à 30 jours pour permettre la reprise de session (configurable)

Vous pouvez supprimer les sessions individuelles de Claude Code sur le web à tout moment. La suppression d'une session supprime définitivement les données d'événement de la session. Pour obtenir des instructions sur la suppression des sessions, consultez [Gestion des sessions](/fr/claude-code-on-the-web#managing-sessions).

Découvrez-en plus sur les pratiques de conservation des données dans notre [Centre de confidentialité](https://privacy.anthropic.com/).

Pour plus de détails, veuillez consulter nos [Conditions commerciales](https://www.anthropic.com/legal/commercial-terms) (pour les utilisateurs Team, Enterprise et API) ou [Conditions grand public](https://www.anthropic.com/legal/consumer-terms) (pour les utilisateurs Free, Pro et Max) et [Politique de confidentialité](https://www.anthropic.com/legal/privacy).

## Accès aux données

Pour tous les utilisateurs propriétaires, vous pouvez en savoir plus sur les données enregistrées pour [Claude Code local](#local-claude-code-data-flow-and-dependencies) et [Claude Code distant](#cloud-execution-data-flow-and-dependencies). Les sessions [Contrôle distant](/fr/remote-control) suivent le flux de données local puisque toute l'exécution se fait sur votre machine. Notez que pour Claude Code distant, Claude accède au référentiel où vous lancez votre session Claude Code. Claude n'accède pas aux référentiels que vous avez connectés mais dans lesquels vous n'avez pas lancé de session.

## Claude Code local : flux de données et dépendances

Le diagramme ci-dessous montre comment Claude Code se connecte aux services externes lors de l'installation et du fonctionnement normal. Les lignes pleines indiquent les connexions requises, tandis que les lignes pointillées représentent les flux de données optionnels ou initiés par l'utilisateur.

<img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/claude-code-data-flow.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=b3f71c69d743bff63343207dfb7ad6ce" alt="Diagramme montrant les connexions externes de Claude Code : l'installation/mise à jour se connecte à NPM, et les demandes des utilisateurs se connectent aux services Anthropic, y compris l'authentification Console, l'API publique, et optionnellement Statsig, Sentry et les rapports de bogues" width="720" height="520" data-path="images/claude-code-data-flow.svg" />

Claude Code est installé à partir de [NPM](https://www.npmjs.com/package/@anthropic-ai/claude-code). Claude Code s'exécute localement. Pour interagir avec le LLM, Claude Code envoie des données sur le réseau. Ces données incluent tous les invites utilisateur et les sorties du modèle. Les données sont chiffrées en transit via TLS et ne sont pas chiffrées au repos. Claude Code est compatible avec la plupart des VPN et proxies LLM populaires.

Claude Code est construit sur les API d'Anthropic. Pour plus de détails concernant les contrôles de sécurité de notre API, y compris nos procédures de journalisation des API, veuillez consulter les artefacts de conformité offerts dans le [Centre de confiance Anthropic](https://trust.anthropic.com).

### Exécution cloud : flux de données et dépendances

Lors de l'utilisation de [Claude Code sur le web](/fr/claude-code-on-the-web), les sessions s'exécutent dans des machines virtuelles gérées par Anthropic au lieu de s'exécuter localement. Dans les environnements cloud :

* **Stockage du code et des données :** Votre référentiel est cloné sur une VM isolée. Le code et les données de session sont soumis aux politiques de conservation et d'utilisation pour votre type de compte (voir la section Conservation des données ci-dessus)
* **Identifiants :** L'authentification GitHub est gérée via un proxy sécurisé ; vos identifiants GitHub n'entrent jamais dans le bac à sable
* **Trafic réseau :** Tout le trafic sortant passe par un proxy de sécurité pour la journalisation d'audit et la prévention des abus
* **Données de session :** Les invites, les modifications de code et les sorties suivent les mêmes politiques de données que l'utilisation locale de Claude Code

Pour plus de détails sur la sécurité de l'exécution cloud, consultez [Sécurité](/fr/security#cloud-execution-security).

## Services de télémétrie

Claude Code se connecte à partir des machines des utilisateurs au service Statsig pour enregistrer les métriques opérationnelles telles que la latence, la fiabilité et les modèles d'utilisation. Cet enregistrement n'inclut aucun code ni chemin de fichier. Les données sont chiffrées en transit à l'aide de TLS et au repos à l'aide du chiffrement AES 256 bits. Lisez-en plus dans la [documentation de sécurité Statsig](https://www.statsig.com/trust/security). Pour refuser la télémétrie Statsig, définissez la variable d'environnement `DISABLE_TELEMETRY`.

Claude Code se connecte à partir des machines des utilisateurs à Sentry pour la journalisation des erreurs opérationnelles. Les données sont chiffrées en transit à l'aide de TLS et au repos à l'aide du chiffrement AES 256 bits. Lisez-en plus dans la [documentation de sécurité Sentry](https://sentry.io/security/). Pour refuser la journalisation des erreurs, définissez la variable d'environnement `DISABLE_ERROR_REPORTING`.

Lorsque les utilisateurs exécutent la commande `/bug`, une copie de leur historique de conversation complet, y compris le code, est envoyée à Anthropic. Les données sont chiffrées en transit et au repos. Optionnellement, un problème Github est créé dans notre référentiel public. Pour refuser les rapports de bogues, définissez la variable d'environnement `DISABLE_BUG_COMMAND`.

## Comportements par défaut par fournisseur d'API

Par défaut, nous désactivons tout le trafic non essentiel (y compris les rapports d'erreurs, la télémétrie, la fonctionnalité de rapport de bogues et les sondages de qualité de session) lors de l'utilisation de Bedrock, Vertex ou Foundry. Vous pouvez également refuser tous ces éléments à la fois en définissant la variable d'environnement `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`. Voici les comportements par défaut complets :

| Service                            | Claude API                                                                       | Vertex API                                                       | Bedrock API                                                       | Foundry API                                                       |
| ---------------------------------- | -------------------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------- | ----------------------------------------------------------------- |
| **Statsig (Métriques)**            | Activé par défaut.<br />`DISABLE_TELEMETRY=1` pour désactiver.                   | Désactivé par défaut.<br />`CLAUDE_CODE_USE_VERTEX` doit être 1. | Désactivé par défaut.<br />`CLAUDE_CODE_USE_BEDROCK` doit être 1. | Désactivé par défaut.<br />`CLAUDE_CODE_USE_FOUNDRY` doit être 1. |
| **Sentry (Erreurs)**               | Activé par défaut.<br />`DISABLE_ERROR_REPORTING=1` pour désactiver.             | Désactivé par défaut.<br />`CLAUDE_CODE_USE_VERTEX` doit être 1. | Désactivé par défaut.<br />`CLAUDE_CODE_USE_BEDROCK` doit être 1. | Désactivé par défaut.<br />`CLAUDE_CODE_USE_FOUNDRY` doit être 1. |
| **Claude API (rapports `/bug`)**   | Activé par défaut.<br />`DISABLE_BUG_COMMAND=1` pour désactiver.                 | Désactivé par défaut.<br />`CLAUDE_CODE_USE_VERTEX` doit être 1. | Désactivé par défaut.<br />`CLAUDE_CODE_USE_BEDROCK` doit être 1. | Désactivé par défaut.<br />`CLAUDE_CODE_USE_FOUNDRY` doit être 1. |
| **Sondages de qualité de session** | Activé par défaut.<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` pour désactiver. | Désactivé par défaut.<br />`CLAUDE_CODE_USE_VERTEX` doit être 1. | Désactivé par défaut.<br />`CLAUDE_CODE_USE_BEDROCK` doit être 1. | Désactivé par défaut.<br />`CLAUDE_CODE_USE_FOUNDRY` doit être 1. |

Toutes les variables d'environnement peuvent être vérifiées dans `settings.json` ([en savoir plus](/fr/settings)).
