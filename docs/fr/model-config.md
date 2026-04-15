> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuration du modèle

> Découvrez la configuration du modèle Claude Code, y compris les alias de modèle comme `opusplan`

## Modèles disponibles

Pour le paramètre `model` dans Claude Code, vous pouvez configurer l'un des éléments suivants :

* Un **alias de modèle**
* Un **nom de modèle**
  * API Anthropic : un **[nom de modèle](https://platform.claude.com/docs/fr/about-claude/models/overview)** complet
  * Bedrock : un ARN de profil d'inférence
  * Foundry : un nom de déploiement
  * Vertex : un nom de version

### Alias de modèle

Les alias de modèle offrent un moyen pratique de sélectionner les paramètres du modèle sans avoir à mémoriser les numéros de version exacts :

| Alias de modèle  | Comportement                                                                                                                                                                                  |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`default`**    | Valeur spéciale qui efface tout remplacement de modèle et revient au modèle recommandé pour votre type de compte. N'est pas en soi un alias de modèle                                         |
| **`best`**       | Utilise le modèle disponible le plus capable, actuellement équivalent à `opus`                                                                                                                |
| **`sonnet`**     | Utilise le dernier modèle Sonnet (actuellement Sonnet 4.6) pour les tâches de codage quotidiennes                                                                                             |
| **`opus`**       | Utilise le dernier modèle Opus (actuellement Opus 4.6) pour les tâches de raisonnement complexe                                                                                               |
| **`haiku`**      | Utilise le modèle Haiku rapide et efficace pour les tâches simples                                                                                                                            |
| **`sonnet[1m]`** | Utilise Sonnet avec une [fenêtre de contexte de 1 million de tokens](https://platform.claude.com/docs/fr/build-with-claude/context-windows#1m-token-context-window) pour les sessions longues |
| **`opus[1m]`**   | Utilise Opus avec une [fenêtre de contexte de 1 million de tokens](https://platform.claude.com/docs/fr/build-with-claude/context-windows#1m-token-context-window) pour les sessions longues   |
| **`opusplan`**   | Mode spécial qui utilise `opus` pendant le mode plan, puis bascule vers `sonnet` pour l'exécution                                                                                             |

Les alias pointent toujours vers la dernière version. Pour épingler une version spécifique, utilisez le nom de modèle complet (par exemple, `claude-opus-4-6`) ou définissez la variable d'environnement correspondante comme `ANTHROPIC_DEFAULT_OPUS_MODEL`.

### Définir votre modèle

Vous pouvez configurer votre modèle de plusieurs façons, énumérées par ordre de priorité :

1. **Pendant la session** - Utilisez `/model <alias|name>` pour basculer les modèles en cours de session
2. **Au démarrage** - Lancez avec `claude --model <alias|name>`
3. **Variable d'environnement** - Définissez `ANTHROPIC_MODEL=<alias|name>`
4. **Paramètres** - Configurez de manière permanente dans votre fichier de paramètres en utilisant le champ `model`.

Exemple d'utilisation :

```bash theme={null}
# Démarrer avec Opus
claude --model opus

# Basculer vers Sonnet pendant la session
/model sonnet
```

Exemple de fichier de paramètres :

```json theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## Restreindre la sélection du modèle

Les administrateurs d'entreprise peuvent utiliser `availableModels` dans les [paramètres gérés ou de politique](/fr/settings#settings-files) pour restreindre les modèles que les utilisateurs peuvent sélectionner.

Lorsque `availableModels` est défini, les utilisateurs ne peuvent pas basculer vers des modèles ne figurant pas dans la liste via `/model`, le drapeau `--model`, l'outil Config ou la variable d'environnement `ANTHROPIC_MODEL`.

```json theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### Comportement du modèle par défaut

L'option Par défaut dans le sélecteur de modèle n'est pas affectée par `availableModels`. Elle reste toujours disponible et représente la valeur par défaut du système [basée sur le niveau d'abonnement de l'utilisateur](#default-model-setting).

Même avec `availableModels: []`, les utilisateurs peuvent toujours utiliser Claude Code avec le modèle Par défaut pour leur niveau.

### Contrôler le modèle sur lequel les utilisateurs s'exécutent

Le paramètre `model` est une sélection initiale, pas une application. Il définit quel modèle est actif au démarrage d'une session, mais les utilisateurs peuvent toujours ouvrir `/model` et choisir Par défaut, qui se résout au système par défaut pour leur niveau indépendamment de ce que `model` est défini.

Pour contrôler complètement l'expérience du modèle, combinez trois paramètres :

* **`availableModels`** : restreint les modèles nommés vers lesquels les utilisateurs peuvent basculer
* **`model`** : définit la sélection de modèle initiale au démarrage d'une session
* **`ANTHROPIC_DEFAULT_SONNET_MODEL`** / **`ANTHROPIC_DEFAULT_OPUS_MODEL`** / **`ANTHROPIC_DEFAULT_HAIKU_MODEL`** : contrôlent ce vers quoi l'option Par défaut et les alias `sonnet`, `opus` et `haiku` se résolvent

Cet exemple démarre les utilisateurs sur Sonnet 4.5, limite le sélecteur à Sonnet et Haiku, et épingle Par défaut pour se résoudre à Sonnet 4.5 plutôt qu'à la dernière version :

```json theme={null}
{
  "model": "claude-sonnet-4-5",
  "availableModels": ["claude-sonnet-4-5", "haiku"],
  "env": {
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5"
  }
}
```

Sans le bloc `env`, un utilisateur qui sélectionne Par défaut dans le sélecteur obtiendrait la dernière version de Sonnet, contournant l'épinglage de version dans `model` et `availableModels`.

### Comportement de fusion

Lorsque `availableModels` est défini à plusieurs niveaux, comme les paramètres utilisateur et les paramètres de projet, les tableaux sont fusionnés et dédupliqués. Pour appliquer une liste d'autorisation stricte, définissez `availableModels` dans les paramètres gérés ou de politique qui ont la priorité la plus élevée.

## Comportement spécial du modèle

### Paramètre de modèle `default`

Le comportement de `default` dépend de votre type de compte :

* **Max et Team Premium** : par défaut Opus 4.6
* **Pro et Team Standard** : par défaut Sonnet 4.6
* **Enterprise** : Opus 4.6 est disponible mais pas par défaut

Claude Code peut automatiquement revenir à Sonnet si vous atteignez un seuil d'utilisation avec Opus.

### Paramètre de modèle `opusplan`

L'alias de modèle `opusplan` fournit une approche hybride automatisée :

* **En mode plan** - Utilise `opus` pour le raisonnement complexe et les décisions architecturales
* **En mode exécution** - Bascule automatiquement vers `sonnet` pour la génération de code et l'implémentation

Cela vous donne le meilleur des deux mondes : le raisonnement supérieur d'Opus pour la planification et l'efficacité de Sonnet pour l'exécution.

### Ajuster le niveau d'effort

Les [niveaux d'effort](https://platform.claude.com/docs/fr/build-with-claude/effort) contrôlent le raisonnement adaptatif, qui alloue dynamiquement la réflexion en fonction de la complexité de la tâche. Un effort inférieur est plus rapide et moins cher pour les tâches simples, tandis qu'un effort supérieur fournit un raisonnement plus profond pour les problèmes complexes.

Trois niveaux persistent entre les sessions : **low**, **medium** et **high**. Un quatrième niveau, **max**, fournit le raisonnement le plus profond sans contrainte sur les dépenses en tokens, donc les réponses sont plus lentes et coûtent plus cher qu'à `high`. `max` est disponible uniquement sur Opus 4.6 et ne persiste pas entre les sessions sauf via la variable d'environnement `CLAUDE_CODE_EFFORT_LEVEL`.

Opus 4.6 et Sonnet 4.6 utilisent par défaut un effort moyen. Cela s'applique à tous les fournisseurs, y compris Bedrock, Vertex AI et l'accès direct à l'API.

Le niveau moyen est recommandé pour la plupart des tâches de codage : il équilibre la vitesse et la profondeur du raisonnement, et les niveaux supérieurs peuvent amener le modèle à trop réfléchir sur le travail de routine. Réservez `high` ou `max` pour les tâches qui bénéficient véritablement d'un raisonnement plus profond, comme les problèmes de débogage difficiles ou les décisions architecturales complexes.

Pour un raisonnement profond ponctuel sans modifier votre paramètre de session, incluez « ultrathink » dans votre invite pour déclencher un effort élevé pour ce tour.

**Définir l'effort :**

* **`/effort`** : exécutez `/effort low`, `/effort medium`, `/effort high` ou `/effort max` pour changer le niveau, ou `/effort auto` pour réinitialiser à la valeur par défaut du modèle
* **Dans `/model`** : utilisez les touches fléchées gauche/droite pour ajuster le curseur d'effort lors de la sélection d'un modèle
* **Drapeau `--effort`** : passez `low`, `medium`, `high` ou `max` pour définir le niveau pour une seule session lors du lancement de Claude Code
* **Variable d'environnement** : définissez `CLAUDE_CODE_EFFORT_LEVEL` sur `low`, `medium`, `high`, `max` ou `auto`
* **Paramètres** : définissez `effortLevel` dans votre fichier de paramètres sur `"low"`, `"medium"` ou `"high"`
* **Frontmatter de skill et de subagent** : définissez `effort` dans un fichier markdown de [skill](/fr/skills#frontmatter-reference) ou de [subagent](/fr/sub-agents#supported-frontmatter-fields) pour remplacer le niveau d'effort lorsque ce skill ou subagent s'exécute

La variable d'environnement prend la priorité sur toutes les autres méthodes, puis votre niveau configuré, puis la valeur par défaut du modèle. L'effort du frontmatter s'applique lorsque ce skill ou subagent est actif, remplaçant le niveau de session mais pas la variable d'environnement.

L'effort est pris en charge sur Opus 4.6 et Sonnet 4.6. Le curseur d'effort apparaît dans `/model` lorsqu'un modèle pris en charge est sélectionné. Le niveau d'effort actuel est également affiché à côté du logo et du spinner, par exemple « with low effort », vous pouvez donc confirmer quel paramètre est actif sans ouvrir `/model`.

Pour désactiver le raisonnement adaptatif sur Opus 4.6 et Sonnet 4.6 et revenir au budget de réflexion fixe précédent, définissez `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. Lorsqu'il est désactivé, ces modèles utilisent le budget fixe contrôlé par `MAX_THINKING_TOKENS`. Voir [variables d'environnement](/fr/env-vars).

### Contexte étendu

Opus 4.6 et Sonnet 4.6 prennent en charge une [fenêtre de contexte de 1 million de tokens](https://platform.claude.com/docs/fr/build-with-claude/context-windows#1m-token-context-window) pour les sessions longues avec de grandes bases de code.

La disponibilité varie selon le modèle et le plan. Sur les plans Max, Team et Enterprise, Opus est automatiquement mis à niveau vers un contexte 1M sans configuration supplémentaire. Cela s'applique aux sièges Team Standard et Team Premium.

| Plan                            | Opus 4.6 avec contexte 1M                                                                                                     | Sonnet 4.6 avec contexte 1M                                                                                                   |
| ------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| Max, Team et Enterprise         | Inclus dans l'abonnement                                                                                                      | Nécessite une [utilisation supplémentaire](https://support.claude.com/fr/articles/12429409-extra-usage-for-paid-claude-plans) |
| Pro                             | Nécessite une [utilisation supplémentaire](https://support.claude.com/fr/articles/12429409-extra-usage-for-paid-claude-plans) | Nécessite une [utilisation supplémentaire](https://support.claude.com/fr/articles/12429409-extra-usage-for-paid-claude-plans) |
| API et paiement à l'utilisation | Accès complet                                                                                                                 | Accès complet                                                                                                                 |

Pour désactiver complètement le contexte 1M, définissez `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. Cela supprime les variantes de modèle 1M du sélecteur de modèle. Voir [variables d'environnement](/fr/env-vars).

La fenêtre de contexte 1M utilise la tarification standard du modèle sans prime pour les tokens au-delà de 200 K. Pour les plans où le contexte étendu est inclus dans votre abonnement, l'utilisation reste couverte par votre abonnement. Pour les plans qui accèdent au contexte étendu via une utilisation supplémentaire, les tokens sont facturés à l'utilisation supplémentaire.

Si votre compte prend en charge le contexte 1M, l'option apparaît dans le sélecteur de modèle (`/model`) dans les dernières versions de Claude Code. Si vous ne la voyez pas, essayez de redémarrer votre session.

Vous pouvez également utiliser le suffixe `[1m]` avec les alias de modèle ou les noms de modèle complets :

```bash theme={null}
# Utiliser l'alias opus[1m] ou sonnet[1m]
/model opus[1m]
/model sonnet[1m]

# Ou ajouter [1m] à un nom de modèle complet
/model claude-opus-4-6[1m]
```

## Vérifier votre modèle actuel

Vous pouvez voir quel modèle vous utilisez actuellement de plusieurs façons :

1. Dans la [ligne d'état](/fr/statusline) (si configurée)
2. Dans `/status`, qui affiche également vos informations de compte.

## Ajouter une option de modèle personnalisé

Utilisez `ANTHROPIC_CUSTOM_MODEL_OPTION` pour ajouter une seule entrée personnalisée au sélecteur `/model` sans remplacer les alias intégrés. Ceci est utile pour les déploiements de passerelle LLM ou pour tester les ID de modèle que Claude Code ne répertorie pas par défaut.

Cet exemple définit les trois variables pour rendre un déploiement Opus acheminé par passerelle sélectionnable :

```bash theme={null}
export ANTHROPIC_CUSTOM_MODEL_OPTION="my-gateway/claude-opus-4-6"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Opus via Gateway"
export ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION="Custom deployment routed through the internal LLM gateway"
```

L'entrée personnalisée apparaît au bas du sélecteur `/model`. `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` et `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` sont optionnels. S'ils sont omis, l'ID du modèle est utilisé comme nom et la description par défaut est `Custom model (<model-id>)`.

Claude Code ignore la validation pour l'ID de modèle défini dans `ANTHROPIC_CUSTOM_MODEL_OPTION`, vous pouvez donc utiliser n'importe quelle chaîne que votre point de terminaison API accepte.

## Variables d'environnement

Vous pouvez utiliser les variables d'environnement suivantes, qui doivent être des **noms de modèle** complets (ou équivalents pour votre fournisseur d'API), pour contrôler les noms de modèle auxquels les alias sont mappés.

| Variable d'environnement         | Description                                                                                             |
| -------------------------------- | ------------------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | Le modèle à utiliser pour `opus`, ou pour `opusplan` lorsque le mode Plan est actif.                    |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | Le modèle à utiliser pour `sonnet`, ou pour `opusplan` lorsque le mode Plan n'est pas actif.            |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | Le modèle à utiliser pour `haiku`, ou [fonctionnalité d'arrière-plan](/fr/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | Le modèle à utiliser pour les [subagents](/fr/sub-agents)                                               |

Remarque : `ANTHROPIC_SMALL_FAST_MODEL` est déprécié au profit de `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

### Épingler les modèles pour les déploiements tiers

Lors du déploiement de Claude Code via [Bedrock](/fr/amazon-bedrock), [Vertex AI](/fr/google-vertex-ai) ou [Foundry](/fr/microsoft-foundry), épinglez les versions de modèle avant de les déployer auprès des utilisateurs.

Sans épinglage, Claude Code utilise les alias de modèle (`sonnet`, `opus`, `haiku`) qui se résolvent à la dernière version. Lorsqu'Anthropic publie un nouveau modèle, les utilisateurs dont les comptes n'ont pas la nouvelle version activée se cassent silencieusement.

<Warning>
  Définissez les trois variables d'environnement de modèle sur des ID de version spécifiques dans le cadre de votre configuration initiale. Ignorer cette étape signifie qu'une mise à jour de Claude Code peut casser vos utilisateurs sans aucune action de votre part.
</Warning>

Utilisez les variables d'environnement suivantes avec des ID de modèle spécifiques à la version pour votre fournisseur :

| Fournisseur | Exemple                                                                 |
| :---------- | :---------------------------------------------------------------------- |
| Bedrock     | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'` |
| Vertex AI   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |
| Foundry     | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |

Appliquez le même modèle pour `ANTHROPIC_DEFAULT_SONNET_MODEL` et `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Pour les ID de modèle actuels et hérités sur tous les fournisseurs, voir [Aperçu des modèles](https://platform.claude.com/docs/fr/about-claude/models/overview). Pour mettre à niveau les utilisateurs vers une nouvelle version de modèle, mettez à jour ces variables d'environnement et redéployez.

Pour activer le [contexte étendu](#extended-context) pour un modèle épinglé, ajoutez `[1m]` à l'ID du modèle dans `ANTHROPIC_DEFAULT_OPUS_MODEL` ou `ANTHROPIC_DEFAULT_SONNET_MODEL` :

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6[1m]'
```

Le suffixe `[1m]` applique la fenêtre de contexte 1M à toute utilisation de cet alias, y compris `opusplan`. Claude Code supprime le suffixe avant d'envoyer l'ID du modèle à votre fournisseur. N'ajoutez `[1m]` que lorsque le modèle sous-jacent prend en charge le contexte 1M, comme Opus 4.6 ou Sonnet 4.6.

<Note>
  La liste d'autorisation `settings.availableModels` s'applique toujours lors de l'utilisation de fournisseurs tiers. Le filtrage correspond à l'alias de modèle (`opus`, `sonnet`, `haiku`), et non à l'ID de modèle spécifique au fournisseur.
</Note>

### Personnaliser l'affichage et les capacités du modèle épinglé

Lorsque vous épinglez un modèle sur un fournisseur tiers, l'ID spécifique au fournisseur apparaît tel quel dans le sélecteur `/model` et Claude Code peut ne pas reconnaître les fonctionnalités que le modèle prend en charge. Vous pouvez remplacer le nom d'affichage et déclarer les capacités avec des variables d'environnement complémentaires pour chaque modèle épinglé.

Ces variables ne prennent effet que sur les fournisseurs tiers tels que Bedrock, Vertex AI et Foundry. Elles n'ont aucun effet lors de l'utilisation directe de l'API Anthropic.

| Variable d'environnement                              | Description                                                                                                                                |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME`                   | Nom d'affichage pour le modèle Opus épinglé dans le sélecteur `/model`. Par défaut, l'ID du modèle lorsqu'il n'est pas défini              |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION`            | Description d'affichage pour le modèle Opus épinglé dans le sélecteur `/model`. Par défaut, `Custom Opus model` lorsqu'il n'est pas défini |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` | Liste séparée par des virgules des capacités que le modèle Opus épinglé prend en charge                                                    |

Les mêmes suffixes `_NAME`, `_DESCRIPTION` et `_SUPPORTED_CAPABILITIES` sont disponibles pour `ANTHROPIC_DEFAULT_SONNET_MODEL` et `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

Claude Code active les fonctionnalités comme les [niveaux d'effort](#adjust-effort-level) et la [réflexion étendue](/fr/common-workflows#use-extended-thinking-thinking-mode) en faisant correspondre l'ID du modèle à des modèles connus. Les ID spécifiques au fournisseur tels que les ARN Bedrock ou les noms de déploiement personnalisés ne correspondent souvent pas à ces modèles, laissant les fonctionnalités prises en charge désactivées. Définissez `_SUPPORTED_CAPABILITIES` pour indiquer à Claude Code les fonctionnalités que le modèle prend réellement en charge :

| Valeur de capacité     | Active                                                                                                |
| ---------------------- | ----------------------------------------------------------------------------------------------------- |
| `effort`               | [Niveaux d'effort](#adjust-effort-level) et la commande `/effort`                                     |
| `max_effort`           | Le niveau d'effort `max`                                                                              |
| `thinking`             | [Réflexion étendue](/fr/common-workflows#use-extended-thinking-thinking-mode)                         |
| `adaptive_thinking`    | Raisonnement adaptatif qui alloue dynamiquement la réflexion en fonction de la complexité de la tâche |
| `interleaved_thinking` | Réflexion entre les appels d'outils                                                                   |

Lorsque `_SUPPORTED_CAPABILITIES` est défini, les capacités listées sont activées et les capacités non listées sont désactivées pour le modèle épinglé correspondant. Lorsque la variable n'est pas définie, Claude Code revient à la détection intégrée basée sur l'ID du modèle.

Cet exemple épingle Opus à un ARN de modèle personnalisé Bedrock, définit un nom convivial et déclare ses capacités :

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='arn:aws:bedrock:us-east-1:123456789012:custom-model/abc'
export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME='Opus via Bedrock'
export ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION='Opus 4.6 routed through a Bedrock custom endpoint'
export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES='effort,max_effort,thinking,adaptive_thinking,interleaved_thinking'
```

### Remplacer les ID de modèle par version

Les variables d'environnement au niveau de la famille ci-dessus configurent un ID de modèle par alias de famille. Si vous devez mapper plusieurs versions au sein de la même famille à des ID de fournisseur distincts, utilisez plutôt le paramètre `modelOverrides`.

`modelOverrides` mappe les ID de modèle Anthropic individuels aux chaînes spécifiques au fournisseur que Claude Code envoie à l'API de votre fournisseur. Lorsqu'un utilisateur sélectionne un modèle mappé dans le sélecteur `/model`, Claude Code utilise votre valeur configurée au lieu de la valeur par défaut intégrée.

Cela permet aux administrateurs d'entreprise d'acheminer chaque version de modèle vers un ARN de profil d'inférence Bedrock spécifique, un nom de version Vertex AI ou un nom de déploiement Foundry pour la gouvernance, l'allocation des coûts ou l'acheminement régional.

Définissez `modelOverrides` dans votre [fichier de paramètres](/fr/settings#settings-files) :

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

Les clés doivent être des ID de modèle Anthropic tels que listés dans l'[Aperçu des modèles](https://platform.claude.com/docs/fr/about-claude/models/overview). Pour les ID de modèle datés, incluez le suffixe de date exactement tel qu'il apparaît là. Les clés inconnues sont ignorées.

Les remplacements remplacent les ID de modèle intégrés qui soutiennent chaque entrée dans le sélecteur `/model`. Sur Bedrock, les remplacements prennent la priorité sur tous les profils d'inférence que Claude Code découvre automatiquement au démarrage. Les valeurs que vous fournissez directement via `ANTHROPIC_MODEL`, `--model` ou les variables d'environnement `ANTHROPIC_DEFAULT_*_MODEL` sont transmises au fournisseur telles quelles et ne sont pas transformées par `modelOverrides`.

`modelOverrides` fonctionne aux côtés de `availableModels`. La liste d'autorisation est évaluée par rapport à l'ID de modèle Anthropic, et non à la valeur de remplacement, donc une entrée comme `"opus"` dans `availableModels` continue de correspondre même lorsque les versions d'Opus sont mappées à des ARN.

### Configuration de la mise en cache des invites

Claude Code utilise automatiquement la [mise en cache des invites](https://platform.claude.com/docs/fr/build-with-claude/prompt-caching) pour optimiser les performances et réduire les coûts. Vous pouvez désactiver la mise en cache des invites globalement ou pour des niveaux de modèle spécifiques :

| Variable d'environnement        | Description                                                                                                                             |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| `DISABLE_PROMPT_CACHING`        | Définissez sur `1` pour désactiver la mise en cache des invites pour tous les modèles (prend la priorité sur les paramètres par modèle) |
| `DISABLE_PROMPT_CACHING_HAIKU`  | Définissez sur `1` pour désactiver la mise en cache des invites pour les modèles Haiku uniquement                                       |
| `DISABLE_PROMPT_CACHING_SONNET` | Définissez sur `1` pour désactiver la mise en cache des invites pour les modèles Sonnet uniquement                                      |
| `DISABLE_PROMPT_CACHING_OPUS`   | Définissez sur `1` pour désactiver la mise en cache des invites pour les modèles Opus uniquement                                        |

Ces variables d'environnement vous donnent un contrôle granulaire sur le comportement de la mise en cache des invites. Le paramètre global `DISABLE_PROMPT_CACHING` prend la priorité sur les paramètres spécifiques au modèle, vous permettant de désactiver rapidement toute la mise en cache si nécessaire. Les paramètres par modèle sont utiles pour un contrôle sélectif, par exemple lors du débogage de modèles spécifiques ou du travail avec des fournisseurs cloud qui peuvent avoir des implémentations de mise en cache différentes.
