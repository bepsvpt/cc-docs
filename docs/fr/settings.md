> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Paramètres Claude Code

> Configurez Claude Code avec des paramètres globaux et au niveau du projet, ainsi que des variables d'environnement.

Claude Code offre une variété de paramètres pour configurer son comportement selon vos besoins. Vous pouvez configurer Claude Code en exécutant la commande `/config` lors de l'utilisation du REPL interactif, ce qui ouvre une interface Paramètres avec onglets où vous pouvez afficher les informations d'état et modifier les options de configuration.

## Portées de configuration

Claude Code utilise un **système de portées** pour déterminer où les configurations s'appliquent et qui les partage. Comprendre les portées vous aide à décider comment configurer Claude Code pour un usage personnel, une collaboration d'équipe ou un déploiement en entreprise.

### Portées disponibles

| Portée      | Emplacement                                                                                     | Qui est affecté                           | Partagé avec l'équipe ?    |
| :---------- | :---------------------------------------------------------------------------------------------- | :---------------------------------------- | :------------------------- |
| **Managed** | Paramètres gérés par le serveur, plist / registre, ou `managed-settings.json` au niveau système | Tous les utilisateurs de la machine       | Oui (déployé par l'IT)     |
| **User**    | Répertoire `~/.claude/`                                                                         | Vous, sur tous les projets                | Non                        |
| **Project** | `.claude/` dans le référentiel                                                                  | Tous les collaborateurs de ce référentiel | Oui (commité dans git)     |
| **Local**   | `.claude/settings.local.json`                                                                   | Vous, dans ce référentiel uniquement      | Non (ignoré par gitignore) |

### Quand utiliser chaque portée

La portée **Managed** est destinée à :

* Les politiques de sécurité qui doivent être appliquées à l'échelle de l'organisation
* Les exigences de conformité qui ne peuvent pas être contournées
* Les configurations standardisées déployées par l'IT/DevOps

La portée **User** est idéale pour :

* Les préférences personnelles que vous voulez partout (thèmes, paramètres d'éditeur)
* Les outils et plugins que vous utilisez sur tous les projets
* Les clés API et l'authentification (stockées de manière sécurisée)

La portée **Project** est idéale pour :

* Les paramètres partagés par l'équipe (permissions, hooks, serveurs MCP)
* Les plugins que toute l'équipe devrait avoir
* La standardisation des outils entre collaborateurs

La portée **Local** est idéale pour :

* Les remplacements personnels pour un projet spécifique
* Les configurations de test avant de les partager avec l'équipe
* Les paramètres spécifiques à la machine qui ne fonctionneront pas pour les autres

### Comment les portées interagissent

Lorsque le même paramètre est configuré dans plusieurs portées, les portées plus spécifiques ont la priorité :

1. **Managed** (la plus élevée) - ne peut pas être remplacée par quoi que ce soit
2. **Arguments de ligne de commande** - remplacements de session temporaires
3. **Local** - remplace les paramètres du projet et de l'utilisateur
4. **Project** - remplace les paramètres de l'utilisateur
5. **User** (la plus basse) - s'applique quand rien d'autre ne spécifie le paramètre

Par exemple, si une permission est autorisée dans les paramètres utilisateur mais refusée dans les paramètres du projet, le paramètre du projet a la priorité et la permission est bloquée.

### Ce qui utilise les portées

Les portées s'appliquent à de nombreuses fonctionnalités de Claude Code :

| Fonctionnalité   | Emplacement utilisateur   | Emplacement du projet              | Emplacement local             |
| :--------------- | :------------------------ | :--------------------------------- | :---------------------------- |
| **Paramètres**   | `~/.claude/settings.json` | `.claude/settings.json`            | `.claude/settings.local.json` |
| **Subagents**    | `~/.claude/agents/`       | `.claude/agents/`                  | —                             |
| **Serveurs MCP** | `~/.claude.json`          | `.mcp.json`                        | `~/.claude.json` (par projet) |
| **Plugins**      | `~/.claude/settings.json` | `.claude/settings.json`            | `.claude/settings.local.json` |
| **CLAUDE.md**    | `~/.claude/CLAUDE.md`     | `CLAUDE.md` ou `.claude/CLAUDE.md` | —                             |

***

## Fichiers de paramètres

Le fichier `settings.json` est notre mécanisme officiel pour configurer Claude Code via des paramètres hiérarchiques :

* Les **paramètres utilisateur** sont définis dans `~/.claude/settings.json` et s'appliquent à tous les projets.
* Les **paramètres du projet** sont enregistrés dans votre répertoire de projet :
  * `.claude/settings.json` pour les paramètres qui sont vérifiés dans le contrôle de source et partagés avec votre équipe
  * `.claude/settings.local.json` pour les paramètres qui ne sont pas vérifiés, utiles pour les préférences personnelles et l'expérimentation. Claude Code configurera git pour ignorer `.claude/settings.local.json` lors de sa création.
* **Paramètres gérés** : Pour les organisations qui ont besoin d'un contrôle centralisé, Claude Code prend en charge plusieurs mécanismes de livraison pour les paramètres gérés. Tous utilisent le même format JSON et ne peuvent pas être remplacés par les paramètres utilisateur ou du projet :

  * **Paramètres gérés par le serveur** : livrés depuis les serveurs d'Anthropic via la console d'administration Claude.ai. Voir [paramètres gérés par le serveur](/fr/server-managed-settings).
  * **Politiques MDM/au niveau du système d'exploitation** : livrées via la gestion native des appareils sur macOS et Windows :
    * macOS : domaine de préférences gérées `com.anthropic.claudecode` (déployé via des profils de configuration dans Jamf, Kandji ou d'autres outils MDM)
    * Windows : clé de registre `HKLM\SOFTWARE\Policies\ClaudeCode` avec une valeur `Settings` (REG\_SZ ou REG\_EXPAND\_SZ) contenant du JSON (déployé via la stratégie de groupe ou Intune)
    * Windows (au niveau utilisateur) : `HKCU\SOFTWARE\Policies\ClaudeCode` (priorité de politique la plus basse, utilisée uniquement quand aucune source au niveau administrateur n'existe)
  * **Basé sur fichier** : `managed-settings.json` et `managed-mcp.json` déployés dans les répertoires système :
    * macOS : `/Library/Application Support/ClaudeCode/`
    * Linux et WSL : `/etc/claude-code/`
    * Windows : `C:\Program Files\ClaudeCode\`

  Voir [paramètres gérés](/fr/permissions#managed-only-settings) et [Configuration MCP gérée](/fr/mcp#managed-mcp-configuration) pour plus de détails.

  <Note>
    Les déploiements gérés peuvent également restreindre les **ajouts de marketplace de plugins** en utilisant `strictKnownMarketplaces`. Pour plus d'informations, voir [Restrictions de marketplace gérées](/fr/plugin-marketplaces#managed-marketplace-restrictions).
  </Note>
* **Autre configuration** est stockée dans `~/.claude.json`. Ce fichier contient vos préférences (thème, paramètres de notification, mode d'éditeur), session OAuth, configurations de [serveur MCP](/fr/mcp) pour les portées utilisateur et locale, état par projet (outils autorisés, paramètres de confiance), et divers caches. Les serveurs MCP à portée de projet sont stockés séparément dans `.mcp.json`.

<Note>
  Claude Code crée automatiquement des sauvegardes horodatées des fichiers de configuration et conserve les cinq sauvegardes les plus récentes pour éviter la perte de données.
</Note>

```JSON Exemple settings.json theme={null}
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs",
    "New security policy in effect"
  ]
}
```

La ligne `$schema` dans l'exemple ci-dessus pointe vers le [schéma JSON officiel](https://json.schemastore.org/claude-code-settings.json) pour les paramètres Claude Code. L'ajouter à votre `settings.json` active l'autocomplétion et la validation en ligne dans VS Code, Cursor et tout autre éditeur qui prend en charge la validation de schéma JSON.

### Paramètres disponibles

`settings.json` prend en charge un certain nombre d'options :

| Clé                               | Description                                                                                                                                                                                                                                                                                                                                                                                   | Exemple                                                                 |
| :-------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `apiKeyHelper`                    | Script personnalisé, à exécuter dans `/bin/sh`, pour générer une valeur d'authentification. Cette valeur sera envoyée comme en-têtes `X-Api-Key` et `Authorization: Bearer` pour les demandes de modèle                                                                                                                                                                                       | `/bin/generate_temp_api_key.sh`                                         |
| `cleanupPeriodDays`               | Les sessions inactives plus longtemps que cette période sont supprimées au démarrage. La définition à `0` supprime immédiatement toutes les sessions. (par défaut : 30 jours)                                                                                                                                                                                                                 | `20`                                                                    |
| `companyAnnouncements`            | Annonce à afficher aux utilisateurs au démarrage. Si plusieurs annonces sont fournies, elles seront parcourues aléatoirement.                                                                                                                                                                                                                                                                 | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]` |
| `env`                             | Variables d'environnement qui seront appliquées à chaque session                                                                                                                                                                                                                                                                                                                              | `{"FOO": "bar"}`                                                        |
| `attribution`                     | Personnalisez l'attribution pour les commits git et les demandes de tirage. Voir [Paramètres d'attribution](#attribution-settings)                                                                                                                                                                                                                                                            | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                 |
| `includeCoAuthoredBy`             | **Obsolète** : Utilisez `attribution` à la place. S'il faut inclure la ligne `co-authored-by Claude` dans les commits git et les demandes de tirage (par défaut : `true`)                                                                                                                                                                                                                     | `false`                                                                 |
| `includeGitInstructions`          | Inclure les instructions de workflow de commit et de PR intégrées dans l'invite système de Claude (par défaut : `true`). Définissez à `false` pour supprimer ces instructions, par exemple lors de l'utilisation de vos propres skills de workflow git. La variable d'environnement `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` a la priorité sur ce paramètre lorsqu'elle est définie             | `false`                                                                 |
| `permissions`                     | Voir le tableau ci-dessous pour la structure des permissions.                                                                                                                                                                                                                                                                                                                                 |                                                                         |
| `hooks`                           | Configurez des commandes personnalisées à exécuter lors d'événements du cycle de vie. Voir [documentation des hooks](/fr/hooks) pour le format                                                                                                                                                                                                                                                | Voir [hooks](/fr/hooks)                                                 |
| `disableAllHooks`                 | Désactiver tous les [hooks](/fr/hooks) et toute [ligne d'état](/fr/statusline) personnalisée                                                                                                                                                                                                                                                                                                  | `true`                                                                  |
| `allowManagedHooksOnly`           | (Paramètres gérés uniquement) Empêcher le chargement des hooks utilisateur, projet et plugin. Autorise uniquement les hooks gérés et les hooks SDK. Voir [Configuration des hooks](#hook-configuration)                                                                                                                                                                                       | `true`                                                                  |
| `allowedHttpHookUrls`             | Liste blanche des modèles d'URL que les hooks HTTP peuvent cibler. Prend en charge `*` comme caractère générique. Lorsqu'elle est définie, les hooks avec des URL non correspondantes sont bloqués. Non défini = pas de restriction, tableau vide = bloquer tous les hooks HTTP. Les tableaux fusionnent entre les sources de paramètres. Voir [Configuration des hooks](#hook-configuration) | `["https://hooks.example.com/*"]`                                       |
| `httpHookAllowedEnvVars`          | Liste blanche des noms de variables d'environnement que les hooks HTTP peuvent interpoler dans les en-têtes. Lorsqu'elle est définie, le `allowedEnvVars` effectif de chaque hook est l'intersection avec cette liste. Non défini = pas de restriction. Les tableaux fusionnent entre les sources de paramètres. Voir [Configuration des hooks](#hook-configuration)                          | `["MY_TOKEN", "HOOK_SECRET"]`                                           |
| `allowManagedPermissionRulesOnly` | (Paramètres gérés uniquement) Empêcher les paramètres utilisateur et projet de définir les règles de permission `allow`, `ask` ou `deny`. Seules les règles des paramètres gérés s'appliquent. Voir [Paramètres réservés aux gérés](/fr/permissions#managed-only-settings)                                                                                                                    | `true`                                                                  |
| `allowManagedMcpServersOnly`      | (Paramètres gérés uniquement) Seul `allowedMcpServers` des paramètres gérés est respecté. `deniedMcpServers` fusionne toujours à partir de toutes les sources. Les utilisateurs peuvent toujours ajouter des serveurs MCP, mais seule la liste blanche définie par l'administrateur s'applique. Voir [Configuration MCP gérée](/fr/mcp#managed-mcp-configuration)                             | `true`                                                                  |
| `model`                           | Remplacer le modèle par défaut à utiliser pour Claude Code                                                                                                                                                                                                                                                                                                                                    | `"claude-sonnet-4-6"`                                                   |
| `availableModels`                 | Restreindre les modèles que les utilisateurs peuvent sélectionner via `/model`, `--model`, l'outil Config ou `ANTHROPIC_MODEL`. N'affecte pas l'option Par défaut. Voir [Restreindre la sélection de modèle](/fr/model-config#restrict-model-selection)                                                                                                                                       | `["sonnet", "haiku"]`                                                   |
| `modelOverrides`                  | Mapper les ID de modèle Anthropic aux ID de modèle spécifiques au fournisseur tels que les ARN de profil d'inférence Bedrock. Chaque entrée du sélecteur de modèle utilise sa valeur mappée lors de l'appel de l'API du fournisseur. Voir [Remplacer les ID de modèle par version](/fr/model-config#override-model-ids-per-version)                                                           | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                            |
| `otelHeadersHelper`               | Script pour générer des en-têtes OpenTelemetry dynamiques. S'exécute au démarrage et périodiquement (voir [En-têtes dynamiques](/fr/monitoring-usage#dynamic-headers))                                                                                                                                                                                                                        | `/bin/generate_otel_headers.sh`                                         |
| `statusLine`                      | Configurez une ligne d'état personnalisée pour afficher le contexte. Voir [documentation `statusLine`](/fr/statusline)                                                                                                                                                                                                                                                                        | `{"type": "command", "command": "~/.claude/statusline.sh"}`             |
| `fileSuggestion`                  | Configurez un script personnalisé pour l'autocomplétion de fichier `@`. Voir [Paramètres de suggestion de fichier](#file-suggestion-settings)                                                                                                                                                                                                                                                 | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`        |
| `respectGitignore`                | Contrôlez si le sélecteur de fichier `@` respecte les modèles `.gitignore`. Lorsque `true` (par défaut), les fichiers correspondant aux modèles `.gitignore` sont exclus des suggestions                                                                                                                                                                                                      | `false`                                                                 |
| `outputStyle`                     | Configurez un style de sortie pour ajuster l'invite système. Voir [documentation des styles de sortie](/fr/output-styles)                                                                                                                                                                                                                                                                     | `"Explanatory"`                                                         |
| `forceLoginMethod`                | Utilisez `claudeai` pour restreindre la connexion aux comptes Claude.ai, `console` pour restreindre la connexion aux comptes Claude Console (facturation d'utilisation d'API)                                                                                                                                                                                                                 | `claudeai`                                                              |
| `forceLoginOrgUUID`               | Spécifiez l'UUID d'une organisation pour la sélectionner automatiquement lors de la connexion, en contournant l'étape de sélection d'organisation. Nécessite que `forceLoginMethod` soit défini                                                                                                                                                                                               | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"`                                |
| `enableAllProjectMcpServers`      | Approuver automatiquement tous les serveurs MCP définis dans les fichiers `.mcp.json` du projet                                                                                                                                                                                                                                                                                               | `true`                                                                  |
| `enabledMcpjsonServers`           | Liste des serveurs MCP spécifiques des fichiers `.mcp.json` à approuver                                                                                                                                                                                                                                                                                                                       | `["memory", "github"]`                                                  |
| `disabledMcpjsonServers`          | Liste des serveurs MCP spécifiques des fichiers `.mcp.json` à rejeter                                                                                                                                                                                                                                                                                                                         | `["filesystem"]`                                                        |
| `allowedMcpServers`               | Lorsqu'elle est définie dans managed-settings.json, liste blanche des serveurs MCP que les utilisateurs peuvent configurer. Non défini = pas de restrictions, tableau vide = verrouillage. S'applique à toutes les portées. La liste noire a la priorité. Voir [Configuration MCP gérée](/fr/mcp#managed-mcp-configuration)                                                                   | `[{ "serverName": "github" }]`                                          |
| `deniedMcpServers`                | Lorsqu'elle est définie dans managed-settings.json, liste noire des serveurs MCP qui sont explicitement bloqués. S'applique à toutes les portées, y compris les serveurs gérés. La liste noire a la priorité sur la liste blanche. Voir [Configuration MCP gérée](/fr/mcp#managed-mcp-configuration)                                                                                          | `[{ "serverName": "filesystem" }]`                                      |
| `strictKnownMarketplaces`         | Lorsqu'elle est définie dans managed-settings.json, liste blanche des marketplaces de plugins que les utilisateurs peuvent ajouter. Non défini = pas de restrictions, tableau vide = verrouillage. S'applique uniquement aux ajouts de marketplace. Voir [Restrictions de marketplace gérées](/fr/plugin-marketplaces#managed-marketplace-restrictions)                                       | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                 |
| `blockedMarketplaces`             | (Paramètres gérés uniquement) Liste noire des sources de marketplace. Les sources bloquées sont vérifiées avant le téléchargement, elles ne touchent donc jamais le système de fichiers. Voir [Restrictions de marketplace gérées](/fr/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                  | `[{ "source": "github", "repo": "untrusted/plugins" }]`                 |
| `pluginTrustMessage`              | (Paramètres gérés uniquement) Message personnalisé ajouté à l'avertissement de confiance du plugin affiché avant l'installation. Utilisez ceci pour ajouter un contexte spécifique à l'organisation, par exemple pour confirmer que les plugins de votre marketplace interne sont vérifiés.                                                                                                   | `"All plugins from our marketplace are approved by IT"`                 |
| `awsAuthRefresh`                  | Script personnalisé qui modifie le répertoire `.aws` (voir [configuration avancée des identifiants](/fr/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                    | `aws sso login --profile myprofile`                                     |
| `awsCredentialExport`             | Script personnalisé qui génère du JSON avec les identifiants AWS (voir [configuration avancée des identifiants](/fr/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                        | `/bin/generate_aws_grant.sh`                                            |
| `alwaysThinkingEnabled`           | Activer la [réflexion étendue](/fr/common-workflows#use-extended-thinking-thinking-mode) par défaut pour toutes les sessions. Généralement configuré via la commande `/config` plutôt que d'éditer directement                                                                                                                                                                                | `true`                                                                  |
| `plansDirectory`                  | Personnalisez où les fichiers de plan sont stockés. Le chemin est relatif à la racine du projet. Par défaut : `~/.claude/plans`                                                                                                                                                                                                                                                               | `"./plans"`                                                             |
| `showTurnDuration`                | Afficher les messages de durée de tour après les réponses (par exemple, « Cooked for 1m 6s »). Définissez à `false` pour masquer ces messages                                                                                                                                                                                                                                                 | `true`                                                                  |
| `spinnerVerbs`                    | Personnalisez les verbes d'action affichés dans le spinner et les messages de durée de tour. Définissez `mode` à `"replace"` pour utiliser uniquement vos verbes, ou `"append"` pour les ajouter aux valeurs par défaut                                                                                                                                                                       | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                |
| `language`                        | Configurez la langue de réponse préférée de Claude (par exemple, `"japanese"`, `"spanish"`, `"french"`). Claude répondra dans cette langue par défaut                                                                                                                                                                                                                                         | `"japanese"`                                                            |
| `autoUpdatesChannel`              | Canal de version à suivre pour les mises à jour. Utilisez `"stable"` pour une version généralement une semaine plus ancienne et qui ignore les versions avec des régressions majeures, ou `"latest"` (par défaut) pour la version la plus récente                                                                                                                                             | `"stable"`                                                              |
| `spinnerTipsEnabled`              | Afficher les conseils dans le spinner pendant que Claude travaille. Définissez à `false` pour désactiver les conseils (par défaut : `true`)                                                                                                                                                                                                                                                   | `false`                                                                 |
| `spinnerTipsOverride`             | Remplacer les conseils du spinner par des chaînes personnalisées. `tips` : tableau de chaînes de conseil. `excludeDefault` : si `true`, afficher uniquement les conseils personnalisés ; si `false` ou absent, les conseils personnalisés sont fusionnés avec les conseils intégrés                                                                                                           | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`       |
| `terminalProgressBarEnabled`      | Activer la barre de progression du terminal qui affiche la progression dans les terminaux pris en charge comme Windows Terminal et iTerm2 (par défaut : `true`)                                                                                                                                                                                                                               | `false`                                                                 |
| `prefersReducedMotion`            | Réduire ou désactiver les animations de l'interface utilisateur (spinners, shimmer, effets flash) pour l'accessibilité                                                                                                                                                                                                                                                                        | `true`                                                                  |
| `fastModePerSessionOptIn`         | Lorsque `true`, le mode rapide ne persiste pas entre les sessions. Chaque session commence avec le mode rapide désactivé, ce qui nécessite que les utilisateurs l'activent avec `/fast`. La préférence de mode rapide de l'utilisateur est toujours enregistrée. Voir [Exiger l'opt-in par session](/fr/fast-mode#require-per-session-opt-in)                                                 | `true`                                                                  |
| `teammateMode`                    | Comment les coéquipiers de l'[équipe d'agents](/fr/agent-teams) s'affichent : `auto` (choisit les volets divisés dans tmux ou iTerm2, en processus sinon), `in-process` ou `tmux`. Voir [configurer les équipes d'agents](/fr/agent-teams#set-up-agent-teams)                                                                                                                                 | `"in-process"`                                                          |

### Paramètres de permission

| Clés                           | Description                                                                                                                                                                                                                                                                                             | Exemple                                                                |
| :----------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------- |
| `allow`                        | Tableau des règles de permission pour autoriser l'utilisation d'outils. Voir [Syntaxe des règles de permission](#permission-rule-syntax) ci-dessous pour les détails de correspondance de modèles                                                                                                       | `[ "Bash(git diff *)" ]`                                               |
| `ask`                          | Tableau des règles de permission pour demander une confirmation lors de l'utilisation d'outils. Voir [Syntaxe des règles de permission](#permission-rule-syntax) ci-dessous                                                                                                                             | `[ "Bash(git push *)" ]`                                               |
| `deny`                         | Tableau des règles de permission pour refuser l'utilisation d'outils. Utilisez ceci pour exclure les fichiers sensibles de l'accès de Claude Code. Voir [Syntaxe des règles de permission](#permission-rule-syntax) et [Limitations de permission Bash](/fr/permissions#tool-specific-permission-rules) | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`        | [Répertoires de travail](/fr/permissions#working-directories) supplémentaires auxquels Claude a accès                                                                                                                                                                                                   | `[ "../docs/" ]`                                                       |
| `defaultMode`                  | [Mode de permission](/fr/permissions#permission-modes) par défaut lors de l'ouverture de Claude Code                                                                                                                                                                                                    | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode` | Définissez à `"disable"` pour empêcher l'activation du mode `bypassPermissions`. Cela désactive l'indicateur de ligne de commande `--dangerously-skip-permissions`. Voir [paramètres gérés](/fr/permissions#managed-only-settings)                                                                      | `"disable"`                                                            |

### Syntaxe des règles de permission

Les règles de permission suivent le format `Tool` ou `Tool(specifier)`. Les règles sont évaluées dans l'ordre : d'abord les règles de refus, puis de demande, puis d'autorisation. La première règle correspondante gagne.

Exemples rapides :

| Règle                          | Effet                                                    |
| :----------------------------- | :------------------------------------------------------- |
| `Bash`                         | Correspond à toutes les commandes Bash                   |
| `Bash(npm run *)`              | Correspond aux commandes commençant par `npm run`        |
| `Read(./.env)`                 | Correspond à la lecture du fichier `.env`                |
| `WebFetch(domain:example.com)` | Correspond aux demandes de récupération vers example.com |

Pour la référence complète de la syntaxe des règles, y compris le comportement des caractères génériques, les modèles spécifiques aux outils pour Read, Edit, WebFetch, MCP et Agent, et les limitations de sécurité des modèles Bash, voir [Syntaxe des règles de permission](/fr/permissions#permission-rule-syntax).

### Paramètres de sandbox

Configurez le comportement avancé du sandboxing. Le sandboxing isole les commandes bash de votre système de fichiers et de votre réseau. Voir [Sandboxing](/fr/sandboxing) pour plus de détails.

| Clés                              | Description                                                                                                                                                                                                                                                                                                                                                                                                                | Exemple                         |
| :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `enabled`                         | Activer le sandboxing bash (macOS, Linux et WSL2). Par défaut : false                                                                                                                                                                                                                                                                                                                                                      | `true`                          |
| `autoAllowBashIfSandboxed`        | Approuver automatiquement les commandes bash lorsqu'elles sont sandboxées. Par défaut : true                                                                                                                                                                                                                                                                                                                               | `true`                          |
| `excludedCommands`                | Commandes qui doivent s'exécuter en dehors du sandbox                                                                                                                                                                                                                                                                                                                                                                      | `["git", "docker"]`             |
| `allowUnsandboxedCommands`        | Autoriser les commandes à s'exécuter en dehors du sandbox via le paramètre `dangerouslyDisableSandbox`. Lorsqu'elle est définie à `false`, l'échappatoire `dangerouslyDisableSandbox` est complètement désactivée et toutes les commandes doivent s'exécuter en sandbox (ou être dans `excludedCommands`). Utile pour les politiques d'entreprise qui nécessitent un sandboxing strict. Par défaut : true                  | `false`                         |
| `filesystem.allowWrite`           | Chemins supplémentaires où les commandes sandboxées peuvent écrire. Les tableaux sont fusionnés sur toutes les portées de paramètres : les chemins utilisateur, projet et gérés sont combinés, non remplacés. Également fusionnés avec les chemins des règles de permission `Edit(...)` allow. Voir [préfixes de chemin](#sandbox-path-prefixes) ci-dessous.                                                               | `["//tmp/build", "~/.kube"]`    |
| `filesystem.denyWrite`            | Chemins où les commandes sandboxées ne peuvent pas écrire. Les tableaux sont fusionnés sur toutes les portées de paramètres. Également fusionnés avec les chemins des règles de permission `Edit(...)` deny.                                                                                                                                                                                                               | `["//etc", "//usr/local/bin"]`  |
| `filesystem.denyRead`             | Chemins où les commandes sandboxées ne peuvent pas lire. Les tableaux sont fusionnés sur toutes les portées de paramètres. Également fusionnés avec les chemins des règles de permission `Read(...)` deny.                                                                                                                                                                                                                 | `["~/.aws/credentials"]`        |
| `network.allowUnixSockets`        | Chemins de socket Unix accessibles dans le sandbox (pour les agents SSH, etc.)                                                                                                                                                                                                                                                                                                                                             | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`     | Autoriser toutes les connexions de socket Unix dans le sandbox. Par défaut : false                                                                                                                                                                                                                                                                                                                                         | `true`                          |
| `network.allowLocalBinding`       | Autoriser la liaison aux ports localhost (macOS uniquement). Par défaut : false                                                                                                                                                                                                                                                                                                                                            | `true`                          |
| `network.allowedDomains`          | Tableau des domaines à autoriser pour le trafic réseau sortant. Prend en charge les caractères génériques (par exemple, `*.example.com`).                                                                                                                                                                                                                                                                                  | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly` | (Paramètres gérés uniquement) Seul `allowedDomains` et les règles allow `WebFetch(domain:...)` des paramètres gérés sont respectés. Les domaines des paramètres utilisateur, projet et local sont ignorés. Les domaines non autorisés sont bloqués automatiquement sans inviter l'utilisateur. Les domaines refusés sont toujours respectés à partir de toutes les sources. Par défaut : false                             | `true`                          |
| `network.httpProxyPort`           | Port du proxy HTTP utilisé si vous souhaitez apporter votre propre proxy. S'il n'est pas spécifié, Claude exécutera son propre proxy.                                                                                                                                                                                                                                                                                      | `8080`                          |
| `network.socksProxyPort`          | Port du proxy SOCKS5 utilisé si vous souhaitez apporter votre propre proxy. S'il n'est pas spécifié, Claude exécutera son propre proxy.                                                                                                                                                                                                                                                                                    | `8081`                          |
| `enableWeakerNestedSandbox`       | Activer un sandbox plus faible pour les environnements Docker non privilégiés (Linux et WSL2 uniquement). **Réduit la sécurité.** Par défaut : false                                                                                                                                                                                                                                                                       | `true`                          |
| `enableWeakerNetworkIsolation`    | (macOS uniquement) Autoriser l'accès au service de confiance TLS du système (`com.apple.trustd.agent`) dans le sandbox. Requis pour que les outils basés sur Go comme `gh`, `gcloud` et `terraform` vérifient les certificats TLS lors de l'utilisation de `httpProxyPort` avec un proxy MITM et une CA personnalisée. **Réduit la sécurité** en ouvrant un chemin potentiel d'exfiltration de données. Par défaut : false | `true`                          |

#### Préfixes de chemin du sandbox

Les chemins dans `filesystem.allowWrite`, `filesystem.denyWrite` et `filesystem.denyRead` prennent en charge ces préfixes :

| Préfixe                | Signification                                              | Exemple                                |
| :--------------------- | :--------------------------------------------------------- | :------------------------------------- |
| `//`                   | Chemin absolu à partir de la racine du système de fichiers | `//tmp/build` devient `/tmp/build`     |
| `~/`                   | Relatif au répertoire personnel                            | `~/.kube` devient `$HOME/.kube`        |
| `/`                    | Relatif au répertoire du fichier de paramètres             | `/build` devient `$SETTINGS_DIR/build` |
| `./` ou pas de préfixe | Chemin relatif (résolu par le runtime du sandbox)          | `./output`                             |

**Exemple de configuration :**

```json  theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["//tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "allowUnixSockets": [
        "/var/run/docker.sock"
      ],
      "allowLocalBinding": true
    }
  }
}
```

Les **restrictions de système de fichiers et de réseau** peuvent être configurées de deux façons qui sont fusionnées ensemble :

* **Paramètres `sandbox.filesystem`** (affichés ci-dessus) : Contrôlez les chemins à la limite du sandbox au niveau du système d'exploitation. Ces restrictions s'appliquent à toutes les commandes de sous-processus (par exemple, `kubectl`, `terraform`, `npm`), pas seulement aux outils de fichier de Claude.
* **Règles de permission** : Utilisez les règles allow/deny `Edit` pour contrôler l'accès à l'outil de fichier de Claude, les règles deny `Read` pour bloquer les lectures, et les règles allow/deny `WebFetch` pour contrôler les domaines réseau. Les chemins de ces règles sont également fusionnés dans la configuration du sandbox.

### Paramètres d'attribution

Claude Code ajoute l'attribution aux commits git et aux demandes de tirage. Ceux-ci sont configurés séparément :

* Les commits utilisent les [trailers git](https://git-scm.com/docs/git-interpret-trailers) (comme `Co-Authored-By`) par défaut, qui peuvent être personnalisés ou désactivés
* Les descriptions des demandes de tirage sont du texte brut

| Clés     | Description                                                                                                           |
| :------- | :-------------------------------------------------------------------------------------------------------------------- |
| `commit` | Attribution pour les commits git, y compris tous les trailers. La chaîne vide masque l'attribution du commit          |
| `pr`     | Attribution pour les descriptions des demandes de tirage. La chaîne vide masque l'attribution de la demande de tirage |

**Attribution de commit par défaut :**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Attribution de demande de tirage par défaut :**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Exemple :**

```json  theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

<Note>
  Le paramètre `attribution` a la priorité sur le paramètre obsolète `includeCoAuthoredBy`. Pour masquer toute attribution, définissez `commit` et `pr` à des chaînes vides.
</Note>

### Paramètres de suggestion de fichier

Configurez une commande personnalisée pour l'autocomplétion du chemin de fichier `@`. La suggestion de fichier intégrée utilise la traversée rapide du système de fichiers, mais les grands monorepos peuvent bénéficier d'une indexation spécifique au projet telle qu'un index de fichier pré-construit ou un outillage personnalisé.

```json  theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

La commande s'exécute avec les mêmes variables d'environnement que les [hooks](/fr/hooks), y compris `CLAUDE_PROJECT_DIR`. Elle reçoit du JSON via stdin avec un champ `query` :

```json  theme={null}
{"query": "src/comp"}
```

Générez les chemins de fichier séparés par des sauts de ligne vers stdout (actuellement limité à 15) :

```text  theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**Exemple :**

```bash  theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Configuration des hooks

Ces paramètres contrôlent les hooks autorisés à s'exécuter et ce que les hooks HTTP peuvent accéder. Le paramètre `allowManagedHooksOnly` ne peut être configuré que dans les [paramètres gérés](#settings-files). Les listes blanches d'URL et de variables d'environnement peuvent être définies à n'importe quel niveau de paramètres et fusionnent entre les sources.

**Comportement lorsque `allowManagedHooksOnly` est `true` :**

* Les hooks gérés et les hooks SDK sont chargés
* Les hooks utilisateur, projet et plugin sont bloqués

**Restreindre les URL des hooks HTTP :**

Limitez les URL que les hooks HTTP peuvent cibler. Prend en charge `*` comme caractère générique pour la correspondance. Lorsque le tableau est défini, les hooks HTTP ciblant des URL non correspondantes sont silencieusement bloqués.

```json  theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**Restreindre les variables d'environnement des hooks HTTP :**

Limitez les noms de variables d'environnement que les hooks HTTP peuvent interpoler dans les valeurs d'en-tête. Le `allowedEnvVars` effectif de chaque hook est l'intersection de sa propre liste et de ce paramètre.

```json  theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### Précédence des paramètres

Les paramètres s'appliquent dans l'ordre de précédence. Du plus élevé au plus bas :

1. **Paramètres gérés** ([gérés par le serveur](/fr/server-managed-settings), [politiques MDM/au niveau du système d'exploitation](#configuration-scopes), ou [paramètres gérés](/fr/settings#settings-files))
   * Politiques déployées par l'IT via la livraison par serveur, les profils de configuration MDM, les politiques de registre ou les fichiers de paramètres gérés
   * Ne peuvent pas être remplacés par aucun autre niveau, y compris les arguments de ligne de commande
   * Au sein du niveau géré, la précédence est : gérés par le serveur > politiques MDM/au niveau du système d'exploitation > `managed-settings.json` > registre HKCU (Windows uniquement). Une seule source gérée est utilisée ; les sources ne fusionnent pas.

2. **Arguments de ligne de commande**
   * Remplacements temporaires pour une session spécifique

3. **Paramètres du projet local** (`.claude/settings.local.json`)
   * Paramètres personnels spécifiques au projet

4. **Paramètres du projet partagé** (`.claude/settings.json`)
   * Paramètres du projet partagés par l'équipe dans le contrôle de source

5. **Paramètres utilisateur** (`~/.claude/settings.json`)
   * Paramètres globaux personnels

Cette hiérarchie garantit que les politiques organisationnelles sont toujours appliquées tout en permettant aux équipes et aux individus de personnaliser leur expérience.

Par exemple, si vos paramètres utilisateur autorisent `Bash(npm run *)` mais que les paramètres partagés d'un projet le refusent, le paramètre du projet a la priorité et la commande est bloquée.

<Note>
  **Les paramètres de tableau fusionnent entre les portées.** Lorsque le même paramètre à valeur de tableau (tel que `sandbox.filesystem.allowWrite` ou `permissions.allow`) apparaît dans plusieurs portées, les tableaux sont **concaténés et dédupliqués**, non remplacés. Cela signifie que les portées de priorité inférieure peuvent ajouter des entrées sans remplacer celles définies par les portées de priorité supérieure, et vice versa. Par exemple, si les paramètres gérés définissent `allowWrite` à `["//opt/company-tools"]` et qu'un utilisateur ajoute `["~/.kube"]`, les deux chemins sont inclus dans la configuration finale.
</Note>

### Vérifier les paramètres actifs

Exécutez `/status` dans Claude Code pour voir quelles sources de paramètres sont actives et d'où elles proviennent. La sortie affiche chaque couche de configuration (gérée, utilisateur, projet) ainsi que son origine, telle que `Enterprise managed settings (remote)`, `Enterprise managed settings (plist)`, `Enterprise managed settings (HKLM)` ou `Enterprise managed settings (file)`. Si un fichier de paramètres contient des erreurs, `/status` signale le problème afin que vous puissiez le corriger.

### Points clés du système de configuration

* **Fichiers de mémoire (`CLAUDE.md`)** : Contiennent les instructions et le contexte que Claude charge au démarrage
* **Fichiers de paramètres (JSON)** : Configurez les permissions, les variables d'environnement et le comportement des outils
* **Skills** : Invites personnalisées qui peuvent être invoquées avec `/skill-name` ou chargées automatiquement par Claude
* **Serveurs MCP** : Étendez Claude Code avec des outils et des intégrations supplémentaires
* **Précédence** : Les configurations de niveau supérieur (Managed) remplacent celles de niveau inférieur (User/Project)
* **Héritage** : Les paramètres sont fusionnés, les paramètres plus spécifiques s'ajoutant à ou remplaçant les paramètres plus larges

### Invite système

L'invite système interne de Claude Code n'est pas publiée. Pour ajouter des instructions personnalisées, utilisez les fichiers `CLAUDE.md` ou l'indicateur `--append-system-prompt`.

### Exclure les fichiers sensibles

Pour empêcher Claude Code d'accéder aux fichiers contenant des informations sensibles comme les clés API, les secrets et les fichiers d'environnement, utilisez le paramètre `permissions.deny` dans votre fichier `.claude/settings.json` :

```json  theme={null}
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

Cela remplace la configuration obsolète `ignorePatterns`. Les fichiers correspondant à ces modèles sont exclus de la découverte de fichiers et des résultats de recherche, et les opérations de lecture sur ces fichiers sont refusées.

## Configuration des subagents

Claude Code prend en charge les subagents IA personnalisés qui peuvent être configurés aux niveaux utilisateur et projet. Ces subagents sont stockés sous forme de fichiers Markdown avec du frontmatter YAML :

* **Subagents utilisateur** : `~/.claude/agents/` - Disponibles sur tous vos projets
* **Subagents du projet** : `.claude/agents/` - Spécifiques à votre projet et peuvent être partagés avec votre équipe

Les fichiers de subagent définissent des assistants IA spécialisés avec des invites personnalisées et des permissions d'outils. En savoir plus sur la création et l'utilisation de subagents dans la [documentation des subagents](/fr/sub-agents).

## Configuration des plugins

Claude Code prend en charge un système de plugins qui vous permet d'étendre les fonctionnalités avec des skills, des agents, des hooks et des serveurs MCP. Les plugins sont distribués via des marketplaces et peuvent être configurés aux niveaux utilisateur et référentiel.

### Paramètres des plugins

Paramètres liés aux plugins dans `settings.json` :

```json  theme={null}
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": "github",
      "repo": "acme-corp/claude-plugins"
    }
  }
}
```

#### `enabledPlugins`

Contrôle les plugins activés. Format : `"plugin-name@marketplace-name": true/false`

**Portées** :

* **Paramètres utilisateur** (`~/.claude/settings.json`) : Préférences personnelles des plugins
* **Paramètres du projet** (`.claude/settings.json`) : Plugins spécifiques au projet partagés avec l'équipe
* **Paramètres locaux** (`.claude/settings.local.json`) : Remplacements par machine (non commités)

**Exemple** :

```json  theme={null}
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}
```

#### `extraKnownMarketplaces`

Définit les marketplaces supplémentaires qui doivent être mises à disposition pour le référentiel. Généralement utilisé dans les paramètres au niveau du référentiel pour s'assurer que les membres de l'équipe ont accès aux sources de plugins requises.

**Lorsqu'un référentiel inclut `extraKnownMarketplaces`** :

1. Les membres de l'équipe sont invités à installer la marketplace lorsqu'ils font confiance au dossier
2. Les membres de l'équipe sont ensuite invités à installer les plugins de cette marketplace
3. Les utilisateurs peuvent ignorer les marketplaces ou les plugins indésirables (stockés dans les paramètres utilisateur)
4. L'installation respecte les limites de confiance et nécessite un consentement explicite

**Exemple** :

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}
```

**Types de sources de marketplace** :

* `github` : Référentiel GitHub (utilise `repo`)
* `git` : N'importe quelle URL git (utilise `url`)
* `directory` : Chemin du système de fichiers local (utilise `path`, pour le développement uniquement)
* `hostPattern` : Modèle regex pour correspondre aux hôtes de marketplace (utilise `hostPattern`)

#### `strictKnownMarketplaces`

**Paramètres gérés uniquement** : Contrôle les marketplaces de plugins que les utilisateurs sont autorisés à ajouter. Ce paramètre ne peut être configuré que dans les [paramètres gérés](/fr/settings#settings-files) et fournit aux administrateurs un contrôle strict sur les sources de marketplace.

**Emplacements des fichiers de paramètres gérés** :

* **macOS** : `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux et WSL** : `/etc/claude-code/managed-settings.json`
* **Windows** : `C:\Program Files\ClaudeCode\managed-settings.json`

**Caractéristiques clés** :

* Disponible uniquement dans les paramètres gérés (`managed-settings.json`)
* Ne peut pas être remplacé par les paramètres utilisateur ou projet (priorité la plus élevée)
* Appliqué AVANT les opérations de réseau/système de fichiers (les sources bloquées ne s'exécutent jamais)
* Utilise la correspondance exacte pour les spécifications de source (y compris `ref`, `path` pour les sources git), sauf `hostPattern`, qui utilise la correspondance regex

**Comportement de la liste blanche** :

* `undefined` (par défaut) : Pas de restrictions - les utilisateurs peuvent ajouter n'importe quelle marketplace
* Tableau vide `[]` : Verrouillage complet - les utilisateurs ne peuvent pas ajouter de nouvelles marketplaces
* Liste de sources : Les utilisateurs ne peuvent ajouter que les marketplaces qui correspondent exactement

**Tous les types de sources pris en charge** :

La liste blanche prend en charge sept types de sources de marketplace. La plupart des sources utilisent la correspondance exacte, tandis que `hostPattern` utilise la correspondance regex par rapport à l'hôte de la marketplace.

1. **Référentiels GitHub** :

```json  theme={null}
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

Champs : `repo` (requis), `ref` (optionnel : branche/tag/SHA), `path` (optionnel : sous-répertoire)

2. **Référentiels Git** :

```json  theme={null}
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

Champs : `url` (requis), `ref` (optionnel : branche/tag/SHA), `path` (optionnel : sous-répertoire)

3. **Marketplaces basées sur URL** :

```json  theme={null}
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

Champs : `url` (requis), `headers` (optionnel : en-têtes HTTP pour l'accès authentifié)

<Note>
  Les marketplaces basées sur URL téléchargent uniquement le fichier `marketplace.json`. Elles ne téléchargent pas les fichiers de plugin à partir du serveur. Les plugins dans les marketplaces basées sur URL doivent utiliser des sources externes (URLs GitHub, npm ou git) plutôt que des chemins relatifs. Pour les plugins avec des chemins relatifs, utilisez une marketplace basée sur Git à la place. Voir [Dépannage](/fr/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) pour plus de détails.
</Note>

4. **Packages NPM** :

```json  theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

Champs : `package` (requis, prend en charge les packages à portée)

5. **Chemins de fichier** :

```json  theme={null}
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

Champs : `path` (requis : chemin absolu vers le fichier marketplace.json)

6. **Chemins de répertoire** :

```json  theme={null}
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

Champs : `path` (requis : chemin absolu vers le répertoire contenant `.claude-plugin/marketplace.json`)

7. **Correspondance de modèle d'hôte** :

```json  theme={null}
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
```

Champs : `hostPattern` (requis : modèle regex pour correspondre à l'hôte de la marketplace)

Utilisez la correspondance de modèle d'hôte lorsque vous souhaitez autoriser toutes les marketplaces d'un hôte spécifique sans énumérer chaque référentiel individuellement. Ceci est utile pour les organisations avec des serveurs GitHub Enterprise ou GitLab internes où les développeurs créent leurs propres marketplaces.

Extraction d'hôte par type de source :

* `github` : correspond toujours à `github.com`
* `git` : extrait le nom d'hôte de l'URL (prend en charge les formats HTTPS et SSH)
* `url` : extrait le nom d'hôte de l'URL
* `npm`, `file`, `directory` : non pris en charge pour la correspondance de modèle d'hôte

**Exemples de configuration** :

Exemple : autoriser uniquement les marketplaces spécifiques :

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    },
    {
      "source": "npm",
      "package": "@acme-corp/compliance-plugins"
    }
  ]
}
```

Exemple - Désactiver tous les ajouts de marketplace :

```json  theme={null}
{
  "strictKnownMarketplaces": []
}
```

Exemple : autoriser toutes les marketplaces d'un serveur git interne :

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

**Exigences de correspondance exacte** :

Les sources de marketplace doivent correspondre **exactement** pour que l'ajout d'un utilisateur soit autorisé. Pour les sources basées sur git (`github` et `git`), cela inclut tous les champs optionnels :

* Le `repo` ou `url` doit correspondre exactement
* Le champ `ref` doit correspondre exactement (ou les deux être non définis)
* Le champ `path` doit correspondre exactement (ou les deux être non définis)

Exemples de sources qui **ne correspondent PAS** :

```json  theme={null}
// Ce sont des sources DIFFÉRENTES :
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// Ce sont aussi DIFFÉRENTES :
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
```

**Comparaison avec `extraKnownMarketplaces`** :

| Aspect                    | `strictKnownMarketplaces`                          | `extraKnownMarketplaces`                        |
| ------------------------- | -------------------------------------------------- | ----------------------------------------------- |
| **Objectif**              | Application de la politique organisationnelle      | Commodité de l'équipe                           |
| **Fichier de paramètres** | `managed-settings.json` uniquement                 | N'importe quel fichier de paramètres            |
| **Comportement**          | Bloque les ajouts non autorisés                    | Auto-installe les marketplaces manquantes       |
| **Quand appliqué**        | Avant les opérations de réseau/système de fichiers | Après l'invite de confiance de l'utilisateur    |
| **Peut être remplacé**    | Non (priorité la plus élevée)                      | Oui (par les paramètres de priorité supérieure) |
| **Format de source**      | Objet source direct                                | Marketplace nommée avec source imbriquée        |
| **Cas d'utilisation**     | Conformité, restrictions de sécurité               | Intégration, standardisation                    |

**Différence de format** :

`strictKnownMarketplaces` utilise des objets source directs :

```json  theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` nécessite des marketplaces nommées :

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**Notes importantes** :

* Les restrictions sont vérifiées AVANT toute demande réseau ou opération du système de fichiers
* Lorsqu'elles sont bloquées, les utilisateurs voient des messages d'erreur clairs indiquant que la source est bloquée par la politique gérée
* La restriction s'applique uniquement à l'ajout de NOUVELLES marketplaces ; les marketplaces précédemment installées restent accessibles
* Les paramètres gérés ont la priorité la plus élevée et ne peuvent pas être remplacés

Voir [Restrictions de marketplace gérées](/fr/plugin-marketplaces#managed-marketplace-restrictions) pour la documentation destinée aux utilisateurs.

### Gestion des plugins

Utilisez la commande `/plugin` pour gérer les plugins de manière interactive :

* Parcourir les plugins disponibles à partir des marketplaces
* Installer/désinstaller les plugins
* Activer/désactiver les plugins
* Afficher les détails du plugin (commandes, agents, hooks fournis)
* Ajouter/supprimer les marketplaces

En savoir plus sur le système de plugins dans la [documentation des plugins](/fr/plugins).

## Variables d'environnement

Claude Code prend en charge les variables d'environnement suivantes pour contrôler son comportement :

<Note>
  Toutes les variables d'environnement peuvent également être configurées dans [`settings.json`](#available-settings). Ceci est utile comme moyen de définir automatiquement les variables d'environnement pour chaque session, ou de déployer un ensemble de variables d'environnement pour toute votre équipe ou organisation.
</Note>

| Variable                                       | Objectif                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| :--------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| `ANTHROPIC_API_KEY`                            | Clé API envoyée comme en-tête `X-Api-Key`, généralement pour le SDK Claude (pour l'utilisation interactive, exécutez `/login`)                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `ANTHROPIC_AUTH_TOKEN`                         | Valeur personnalisée pour l'en-tête `Authorization` (la valeur que vous définissez ici sera préfixée avec `Bearer `)                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `ANTHROPIC_CUSTOM_HEADERS`                     | En-têtes personnalisés à ajouter aux demandes (format `Name: Value`, séparés par des sauts de ligne pour plusieurs en-têtes)                                                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`                | Voir [Configuration du modèle](/fr/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`                 | Voir [Configuration du modèle](/fr/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `ANTHROPIC_DEFAULT_SONNET_MODEL`               | Voir [Configuration du modèle](/fr/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `ANTHROPIC_FOUNDRY_API_KEY`                    | Clé API pour l'authentification Microsoft Foundry (voir [Microsoft Foundry](/fr/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `ANTHROPIC_FOUNDRY_BASE_URL`                   | URL de base complète pour la ressource Foundry (par exemple, `https://my-resource.services.ai.azure.com/anthropic`). Alternative à `ANTHROPIC_FOUNDRY_RESOURCE` (voir [Microsoft Foundry](/fr/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                            |     |
| `ANTHROPIC_FOUNDRY_RESOURCE`                   | Nom de la ressource Foundry (par exemple, `my-resource`). Requis si `ANTHROPIC_FOUNDRY_BASE_URL` n'est pas défini (voir [Microsoft Foundry](/fr/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `ANTHROPIC_MODEL`                              | Nom du paramètre de modèle à utiliser (voir [Configuration du modèle](/fr/model-config#environment-variables))                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `ANTHROPIC_SMALL_FAST_MODEL`                   | \[OBSOLÈTE] Nom du [modèle de classe Haiku pour les tâches de fond](/fr/costs)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION`        | Remplacer la région AWS pour le modèle de classe Haiku lors de l'utilisation de Bedrock                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `AWS_BEARER_TOKEN_BEDROCK`                     | Clé API Bedrock pour l'authentification (voir [Clés API Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/))                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `BASH_DEFAULT_TIMEOUT_MS`                      | Délai d'expiration par défaut pour les commandes bash longues                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `BASH_MAX_OUTPUT_LENGTH`                       | Nombre maximum de caractères dans les sorties bash avant qu'elles ne soient tronquées au milieu                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `BASH_MAX_TIMEOUT_MS`                          | Délai d'expiration maximal que le modèle peut définir pour les commandes bash longues                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`              | Définissez le pourcentage de capacité de contexte (1-100) auquel la compaction automatique se déclenche. Par défaut, la compaction automatique se déclenche à environ 95 % de capacité. Utilisez des valeurs inférieures comme `50` pour compacter plus tôt. Les valeurs au-dessus du seuil par défaut n'ont aucun effet. S'applique aux conversations principales et aux subagents. Ce pourcentage s'aligne avec le champ `context_window.used_percentage` disponible dans la [ligne d'état](/fr/statusline)                                                                |     |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR`     | Retourner au répertoire de travail d'origine après chaque commande Bash                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_ACCOUNT_UUID`                     | UUID du compte pour l'utilisateur authentifié. Utilisé par les appelants du SDK pour fournir les informations du compte de manière synchrone, évitant une condition de course où les événements de télémétrie précoces manquent de métadonnées de compte. Nécessite que `CLAUDE_CODE_USER_EMAIL` et `CLAUDE_CODE_ORGANIZATION_UUID` soient également définis                                                                                                                                                                                                                 |     |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | Définissez à `1` pour charger les fichiers CLAUDE.md à partir des répertoires spécifiés avec `--add-dir`. Par défaut, les répertoires supplémentaires ne chargent pas les fichiers de mémoire                                                                                                                                                                                                                                                                                                                                                                                | `1` |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`            | Intervalle en millisecondes auquel les identifiants doivent être actualisés (lors de l'utilisation de `apiKeyHelper`)                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_CLIENT_CERT`                      | Chemin vers le fichier de certificat client pour l'authentification mTLS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_CLIENT_KEY`                       | Chemin vers le fichier de clé privée client pour l'authentification mTLS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`            | Phrase de passe pour `CLAUDE_CODE_CLIENT_KEY` chiffré (optionnel)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT`               | Définissez à `1` pour désactiver le support de la [fenêtre de contexte 1M](/fr/model-config#extended-context). Lorsqu'elle est définie, les variantes de modèle 1M ne sont pas disponibles dans le sélecteur de modèle. Utile pour les environnements d'entreprise avec des exigences de conformité                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`        | Définissez à `1` pour désactiver le [raisonnement adaptatif](/fr/model-config#adjust-effort-level) pour Opus 4.6 et Sonnet 4.6. Lorsqu'elle est désactivée, ces modèles reviennent au budget de réflexion fixe contrôlé par `MAX_THINKING_TOKENS`                                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY`              | Définissez à `1` pour désactiver la [mémoire automatique](/fr/memory#auto-memory). Définissez à `0` pour forcer la mémoire automatique pendant le déploiement progressif. Lorsqu'elle est désactivée, Claude ne crée ni ne charge les fichiers de mémoire automatique                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS`         | Définissez à `1` pour supprimer les instructions de workflow de commit et de PR intégrées de l'invite système de Claude. Utile lors de l'utilisation de vos propres skills de workflow git. A la priorité sur le paramètre [`includeGitInstructions`](#available-settings) lorsqu'elle est définie                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`         | Définissez à `1` pour désactiver toute la fonctionnalité de tâche de fond, y compris le paramètre `run_in_background` sur les outils Bash et subagent, l'auto-backgrounding et le raccourci Ctrl+B                                                                                                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_DISABLE_CRON`                     | Définissez à `1` pour désactiver les [tâches planifiées](/fr/scheduled-tasks). Le skill `/loop` et les outils cron deviennent indisponibles et toutes les tâches planifiées existantes cessent de se déclencher, y compris les tâches qui s'exécutent déjà en milieu de session                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`       | Définissez à `1` pour désactiver les en-têtes `anthropic-beta` spécifiques à l'API Anthropic. Utilisez ceci si vous rencontrez des problèmes comme « Unexpected value(s) for the `anthropic-beta` header » lors de l'utilisation d'une passerelle LLM avec des fournisseurs tiers                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_DISABLE_FAST_MODE`                | Définissez à `1` pour désactiver le [mode rapide](/fr/fast-mode)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`          | Définissez à `1` pour désactiver les sondages de qualité de session « How is Claude doing? ». Également désactivé lors de l'utilisation de fournisseurs tiers ou lorsque la télémétrie est désactivée. Voir [Sondages de qualité de session](/fr/data-usage#session-quality-surveys)                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`     | Équivalent de la définition de `DISABLE_AUTOUPDATER`, `DISABLE_BUG_COMMAND`, `DISABLE_ERROR_REPORTING` et `DISABLE_TELEMETRY`                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`           | Définissez à `1` pour désactiver les mises à jour automatiques du titre du terminal en fonction du contexte de la conversation                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_EFFORT_LEVEL`                     | Définissez le niveau d'effort pour les modèles pris en charge. Valeurs : `low`, `medium`, `high`. L'effort inférieur est plus rapide et moins cher, l'effort supérieur fournit un raisonnement plus profond. Pris en charge sur Opus 4.6 et Sonnet 4.6. Voir [Ajuster le niveau d'effort](/fr/model-config#adjust-effort-level)                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION`         | Définissez à `false` pour désactiver les suggestions de prompt (le bouton bascule « Prompt suggestions » dans `/config`). Ce sont les prédictions grisées qui apparaissent dans votre entrée de prompt après que Claude réponde. Voir [Suggestions de prompt](/fr/interactive-mode#prompt-suggestions)                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_ENABLE_TASKS`                     | Définissez à `false` pour revenir temporairement à la liste TODO précédente au lieu du système de suivi des tâches. Par défaut : `true`. Voir [Liste des tâches](/fr/interactive-mode#task-list)                                                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                 | Définissez à `1` pour activer la collecte de données OpenTelemetry pour les métriques et la journalisation. Requis avant de configurer les exportateurs OTel. Voir [Surveillance](/fr/monitoring-usage)                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY`            | Temps en millisecondes à attendre après que la boucle de requête devienne inactive avant de quitter automatiquement. Utile pour les flux de travail automatisés et les scripts utilisant le mode SDK                                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`         | Définissez à `1` pour activer les [équipes d'agents](/fr/agent-teams). Les équipes d'agents sont expérimentales et désactivées par défaut                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS`      | Remplacer la limite de jetons par défaut pour les lectures de fichier. Utile lorsque vous devez lire des fichiers plus volumineux en intégralité                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_HIDE_ACCOUNT_INFO`                | Définissez à `1` pour masquer votre adresse e-mail et le nom de votre organisation de l'interface utilisateur de Claude Code. Utile lors de la diffusion en continu ou de l'enregistrement                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`            | Ignorer l'installation automatique des extensions IDE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS`                | Définissez le nombre maximal de jetons de sortie pour la plupart des demandes. Par défaut : 32 000. Maximum : 64 000. L'augmentation de cette valeur réduit la fenêtre de contexte effective disponible avant que la [compaction automatique](/fr/costs#reduce-token-usage) ne se déclenche.                                                                                                                                                                                                                                                                                 |     |
| `CLAUDE_CODE_ORGANIZATION_UUID`                | UUID de l'organisation pour l'utilisateur authentifié. Utilisé par les appelants du SDK pour fournir les informations du compte de manière synchrone. Nécessite que `CLAUDE_CODE_ACCOUNT_UUID` et `CLAUDE_CODE_USER_EMAIL` soient également définis                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`  | Intervalle pour actualiser les en-têtes OpenTelemetry dynamiques en millisecondes (par défaut : 1740000 / 29 minutes). Voir [En-têtes dynamiques](/fr/monitoring-usage#dynamic-headers)                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_PLAN_MODE_REQUIRED`               | Auto-défini à `true` sur les coéquipiers de l'[équipe d'agents](/fr/agent-teams) qui nécessitent l'approbation du plan. Lecture seule : défini par Claude Code lors du lancement des coéquipiers. Voir [exiger l'approbation du plan](/fr/agent-teams#require-plan-approval-for-teammates)                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`            | Délai d'expiration en millisecondes pour les opérations git lors de l'installation ou de la mise à jour des plugins (par défaut : 120000). Augmentez cette valeur pour les grands référentiels ou les connexions réseau lentes. Voir [Les opérations Git expirent](/fr/plugin-marketplaces#git-operations-time-out)                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_PROXY_RESOLVES_HOSTS`             | Définissez à `true` pour permettre au proxy d'effectuer la résolution DNS au lieu de l'appelant. Opt-in pour les environnements où le proxy doit gérer la résolution du nom d'hôte                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_SHELL`                            | Remplacer la détection automatique du shell. Utile lorsque votre shell de connexion diffère de votre shell de travail préféré (par exemple, `bash` vs `zsh`)                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `CLAUDE_CODE_SHELL_PREFIX`                     | Préfixe de commande pour envelopper toutes les commandes bash (par exemple, pour la journalisation ou l'audit). Exemple : `/path/to/logger.sh` exécutera `/path/to/logger.sh <command>`                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_SIMPLE`                           | Définissez à `1` pour exécuter avec une invite système minimale et uniquement les outils Bash, lecture de fichier et édition de fichier. Désactive les outils MCP, les pièces jointes, les hooks et les fichiers CLAUDE.md                                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH`                | Ignorer l'authentification AWS pour Bedrock (par exemple, lors de l'utilisation d'une passerelle LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH`                | Ignorer l'authentification Azure pour Microsoft Foundry (par exemple, lors de l'utilisation d'une passerelle LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH`                 | Ignorer l'authentification Google pour Vertex (par exemple, lors de l'utilisation d'une passerelle LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_SUBAGENT_MODEL`                   | Voir [Configuration du modèle](/fr/model-config)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_TASK_LIST_ID`                     | Partager une liste de tâches entre les sessions. Définissez le même ID dans plusieurs instances de Claude Code pour coordonner une liste de tâches partagée. Voir [Liste des tâches](/fr/interactive-mode#task-list)                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_TEAM_NAME`                        | Nom de l'équipe d'agents à laquelle appartient ce coéquipier. Défini automatiquement sur les membres de l'[équipe d'agents](/fr/agent-teams)                                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `CLAUDE_CODE_TMPDIR`                           | Remplacer le répertoire temporaire utilisé pour les fichiers temporaires internes. Claude Code ajoute `/claude/` à ce chemin. Par défaut : `/tmp` sur Unix/macOS, `os.tmpdir()` sur Windows                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_USER_EMAIL`                       | Adresse e-mail pour l'utilisateur authentifié. Utilisé par les appelants du SDK pour fournir les informations du compte de manière synchrone. Nécessite que `CLAUDE_CODE_ACCOUNT_UUID` et `CLAUDE_CODE_ORGANIZATION_UUID` soient également définis                                                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_USE_BEDROCK`                      | Utiliser [Bedrock](/fr/amazon-bedrock)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_USE_FOUNDRY`                      | Utiliser [Microsoft Foundry](/fr/microsoft-foundry)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_USE_VERTEX`                       | Utiliser [Vertex](/fr/google-vertex-ai)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CONFIG_DIR`                            | Personnalisez où Claude Code stocke ses fichiers de configuration et de données                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `DISABLE_AUTOUPDATER`                          | Définissez à `1` pour désactiver les mises à jour automatiques.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `DISABLE_BUG_COMMAND`                          | Définissez à `1` pour désactiver la commande `/bug`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `DISABLE_COST_WARNINGS`                        | Définissez à `1` pour désactiver les messages d'avertissement de coût                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `DISABLE_ERROR_REPORTING`                      | Définissez à `1` pour refuser la création de rapports d'erreur Sentry                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `DISABLE_INSTALLATION_CHECKS`                  | Définissez à `1` pour désactiver les avertissements d'installation. À utiliser uniquement lors de la gestion manuelle de l'emplacement d'installation, car cela peut masquer les problèmes avec les installations standard                                                                                                                                                                                                                                                                                                                                                   |     |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS`            | Définissez à `1` pour désactiver les appels de modèle pour les chemins non critiques comme le texte de saveur                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `DISABLE_PROMPT_CACHING`                       | Définissez à `1` pour désactiver la mise en cache des prompts pour tous les modèles (a la priorité sur les paramètres par modèle)                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `DISABLE_PROMPT_CACHING_HAIKU`                 | Définissez à `1` pour désactiver la mise en cache des prompts pour les modèles Haiku                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `DISABLE_PROMPT_CACHING_OPUS`                  | Définissez à `1` pour désactiver la mise en cache des prompts pour les modèles Opus                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `DISABLE_PROMPT_CACHING_SONNET`                | Définissez à `1` pour désactiver la mise en cache des prompts pour les modèles Sonnet                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `DISABLE_TELEMETRY`                            | Définissez à `1` pour refuser la télémétrie Statsig (notez que les événements Statsig n'incluent pas les données utilisateur comme le code, les chemins de fichier ou les commandes bash)                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `ENABLE_CLAUDEAI_MCP_SERVERS`                  | Définissez à `false` pour désactiver les [serveurs MCP claude.ai](/fr/mcp#use-mcp-servers-from-claudeai) dans Claude Code. Activé par défaut pour les utilisateurs connectés                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `ENABLE_TOOL_SEARCH`                           | Contrôle la [recherche d'outils MCP](/fr/mcp#scale-with-mcp-tool-search). Valeurs : `auto` (par défaut, active à 10 % du contexte), `auto:N` (seuil personnalisé, par exemple, `auto:5` pour 5 %), `true` (toujours activé), `false` (désactivé)                                                                                                                                                                                                                                                                                                                             |     |
| `FORCE_AUTOUPDATE_PLUGINS`                     | Définissez à `true` pour forcer les mises à jour automatiques des plugins même lorsque le mise à jour automatique principale est désactivée via `DISABLE_AUTOUPDATER`                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `HTTP_PROXY`                                   | Spécifiez le serveur proxy HTTP pour les connexions réseau                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `HTTPS_PROXY`                                  | Spécifiez le serveur proxy HTTPS pour les connexions réseau                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `IS_DEMO`                                      | Définissez à `true` pour activer le mode démo : masque l'e-mail et l'organisation de l'interface utilisateur, ignore l'intégration et masque les commandes internes. Utile pour la diffusion en continu ou l'enregistrement de sessions                                                                                                                                                                                                                                                                                                                                      |     |
| `MAX_MCP_OUTPUT_TOKENS`                        | Nombre maximal de jetons autorisés dans les réponses des outils MCP. Claude Code affiche un avertissement lorsque la sortie dépasse 10 000 jetons (par défaut : 25000)                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `MAX_THINKING_TOKENS`                          | Remplacer le budget de [réflexion étendue](https://platform.claude.com/docs/en/build-with-claude/extended-thinking). La réflexion est activée au budget maximal (31 999 jetons) par défaut. Utilisez ceci pour limiter le budget (par exemple, `MAX_THINKING_TOKENS=10000`) ou désactiver complètement la réflexion (`MAX_THINKING_TOKENS=0`). Pour Opus 4.6, la profondeur de réflexion est contrôlée par le [niveau d'effort](/fr/model-config#adjust-effort-level) à la place, et cette variable est ignorée sauf si elle est définie à `0` pour désactiver la réflexion. |     |
| `MCP_CLIENT_SECRET`                            | Secret client OAuth pour les serveurs MCP qui nécessitent des [identifiants pré-configurés](/fr/mcp#use-pre-configured-oauth-credentials). Évite l'invite interactive lors de l'ajout d'un serveur avec `--client-secret`                                                                                                                                                                                                                                                                                                                                                    |     |
| `MCP_OAUTH_CALLBACK_PORT`                      | Port fixe pour le rappel de redirection OAuth, comme alternative à `--callback-port` lors de l'ajout d'un serveur MCP avec des [identifiants pré-configurés](/fr/mcp#use-pre-configured-oauth-credentials)                                                                                                                                                                                                                                                                                                                                                                   |     |
| `MCP_TIMEOUT`                                  | Délai d'expiration en millisecondes pour le démarrage du serveur MCP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `MCP_TOOL_TIMEOUT`                             | Délai d'expiration en millisecondes pour l'exécution de l'outil MCP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `NO_PROXY`                                     | Liste des domaines et adresses IP vers lesquels les demandes seront émises directement, en contournant le proxy                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET`               | Remplacer le budget de caractères pour les métadonnées de skill affichées à l'[outil Skill](/fr/skills#control-who-invokes-a-skill). Le budget s'adapte dynamiquement à 2 % de la fenêtre de contexte, avec un repli de 16 000 caractères. Nom hérité conservé pour la compatibilité rétroactive                                                                                                                                                                                                                                                                             |     |
| `USE_BUILTIN_RIPGREP`                          | Définissez à `0` pour utiliser `rg` installé sur le système au lieu de `rg` inclus avec Claude Code                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU`               | Remplacer la région pour Claude 3.5 Haiku lors de l'utilisation de Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `VERTEX_REGION_CLAUDE_3_7_SONNET`              | Remplacer la région pour Claude 3.7 Sonnet lors de l'utilisation de Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `VERTEX_REGION_CLAUDE_4_0_OPUS`                | Remplacer la région pour Claude 4.0 Opus lors de l'utilisation de Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `VERTEX_REGION_CLAUDE_4_0_SONNET`              | Remplacer la région pour Claude 4.0 Sonnet lors de l'utilisation de Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `VERTEX_REGION_CLAUDE_4_1_OPUS`                | Remplacer la région pour Claude 4.1 Opus lors de l'utilisation de Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |

## Outils disponibles pour Claude

Claude Code a accès à un ensemble d'outils puissants qui l'aident à comprendre et à modifier votre base de code :

| Outil                    | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Permission requise |
| :----------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------- |
| **Agent**                | Génère un [subagent](/fr/sub-agents) avec sa propre fenêtre de contexte pour gérer une tâche                                                                                                                                                                                                                                                                                                                                                                                                                   | Non                |
| **AskUserQuestion**      | Pose des questions à choix multiples pour recueillir les exigences ou clarifier l'ambiguïté                                                                                                                                                                                                                                                                                                                                                                                                                    | Non                |
| **Bash**                 | Exécute les commandes shell dans votre environnement. Voir [Comportement de l'outil Bash](#bash-tool-behavior)                                                                                                                                                                                                                                                                                                                                                                                                 | Oui                |
| **CronCreate**           | Planifie une invite récurrente ou unique dans la session actuelle (disparaît lorsque Claude quitte). Voir [tâches planifiées](/fr/scheduled-tasks)                                                                                                                                                                                                                                                                                                                                                             | Non                |
| **CronDelete**           | Annule une tâche planifiée par ID                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Non                |
| **CronList**             | Liste toutes les tâches planifiées dans la session                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Non                |
| **Edit**                 | Effectue des modifications ciblées sur des fichiers spécifiques                                                                                                                                                                                                                                                                                                                                                                                                                                                | Oui                |
| **EnterPlanMode**        | Bascule en mode plan pour concevoir une approche avant de coder                                                                                                                                                                                                                                                                                                                                                                                                                                                | Non                |
| **EnterWorktree**        | Crée un [git worktree](/fr/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) isolé et y bascule                                                                                                                                                                                                                                                                                                                                                                                           | Non                |
| **ExitPlanMode**         | Présente un plan pour approbation et quitte le mode plan                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Oui                |
| **ExitWorktree**         | Quitte une session worktree et retourne au répertoire d'origine                                                                                                                                                                                                                                                                                                                                                                                                                                                | Non                |
| **Glob**                 | Trouve les fichiers en fonction de la correspondance de modèles                                                                                                                                                                                                                                                                                                                                                                                                                                                | Non                |
| **Grep**                 | Recherche les modèles dans le contenu des fichiers                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Non                |
| **ListMcpResourcesTool** | Liste les ressources exposées par les [serveurs MCP](/fr/mcp) connectés                                                                                                                                                                                                                                                                                                                                                                                                                                        | Non                |
| **LSP**                  | Intelligence du code via les serveurs de langage. Signale automatiquement les erreurs de type et les avertissements après les modifications de fichier. Prend également en charge les opérations de navigation : aller aux définitions, trouver les références, obtenir les informations de type, lister les symboles, trouver les implémentations, tracer les hiérarchies d'appels. Nécessite un [plugin d'intelligence du code](/fr/discover-plugins#code-intelligence) et son binaire de serveur de langage | Non                |
| **NotebookEdit**         | Modifie les cellules du notebook Jupyter                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Oui                |
| **Read**                 | Lit le contenu des fichiers                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | Non                |
| **ReadMcpResourceTool**  | Lit une ressource MCP spécifique par URI                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | Non                |
| **Skill**                | Exécute un [skill](/fr/skills#control-who-invokes-a-skill) dans la conversation principale                                                                                                                                                                                                                                                                                                                                                                                                                     | Oui                |
| **TaskCreate**           | Crée une nouvelle tâche dans la liste des tâches                                                                                                                                                                                                                                                                                                                                                                                                                                                               | Non                |
| **TaskGet**              | Récupère les détails complets d'une tâche spécifique                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Non                |
| **TaskList**             | Liste toutes les tâches avec leur statut actuel                                                                                                                                                                                                                                                                                                                                                                                                                                                                | Non                |
| **TaskOutput**           | Récupère la sortie d'une tâche de fond                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | Non                |
| **TaskStop**             | Tue une tâche de fond en cours d'exécution par ID                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Non                |
| **TaskUpdate**           | Met à jour le statut, les dépendances, les détails de la tâche ou supprime les tâches                                                                                                                                                                                                                                                                                                                                                                                                                          | Non                |
| **TodoWrite**            | Gère la liste de contrôle des tâches de session. Disponible en mode non interactif et dans le [SDK Agent](/fr/headless) ; les sessions interactives utilisent TaskCreate, TaskGet, TaskList et TaskUpdate à la place                                                                                                                                                                                                                                                                                           | Non                |
| **ToolSearch**           | Recherche et charge les outils différés lorsque la [recherche d'outils](/fr/mcp#scale-with-mcp-tool-search) est activée                                                                                                                                                                                                                                                                                                                                                                                        | Non                |
| **WebFetch**             | Récupère le contenu d'une URL spécifiée                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Oui                |
| **WebSearch**            | Effectue des recherches sur le web                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | Oui                |
| **Write**                | Crée ou remplace les fichiers                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | Oui                |

Les règles de permission peuvent être configurées en utilisant `/allowed-tools` ou dans les [paramètres de permission](/fr/settings#available-settings). Voir aussi [Règles de permission spécifiques aux outils](/fr/permissions#tool-specific-permission-rules).

### Comportement de l'outil Bash

L'outil Bash exécute les commandes shell avec le comportement de persistance suivant :

* **Le répertoire de travail persiste** : Lorsque Claude change le répertoire de travail (par exemple, `cd /path/to/dir`), les commandes Bash suivantes s'exécutent dans ce répertoire. Vous pouvez utiliser `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` pour réinitialiser le répertoire du projet après chaque commande.
* **Les variables d'environnement ne persistent PAS** : Les variables d'environnement définies dans une commande Bash (par exemple, `export MY_VAR=value`) ne sont **pas** disponibles dans les commandes Bash suivantes. Chaque commande Bash s'exécute dans un environnement shell frais.

Pour rendre les variables d'environnement disponibles dans les commandes Bash, vous avez **trois options** :

**Option 1 : Activer l'environnement avant de démarrer Claude Code** (approche la plus simple)

Activez votre environnement virtuel dans votre terminal avant de lancer Claude Code :

```bash  theme={null}
conda activate myenv
# ou : source /path/to/venv/bin/activate
claude
```

Cela fonctionne pour les environnements shell, mais les variables d'environnement définies dans les commandes Bash de Claude ne persisteront pas entre les commandes.

**Option 2 : Définir CLAUDE\_ENV\_FILE avant de démarrer Claude Code** (configuration d'environnement persistante)

Exportez le chemin vers un script shell contenant votre configuration d'environnement :

```bash  theme={null}
export CLAUDE_ENV_FILE=/path/to/env-setup.sh
claude
```

Où `/path/to/env-setup.sh` contient :

```bash  theme={null}
conda activate myenv
# ou : source /path/to/venv/bin/activate
# ou : export MY_VAR=value
```

Claude Code sourcera ce fichier avant chaque commande Bash, rendant l'environnement persistant sur toutes les commandes.

**Option 3 : Utiliser un hook SessionStart** (configuration spécifique au projet)

Configurez dans `.claude/settings.json` :

```json  theme={null}
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "echo 'conda activate myenv' >> \"$CLAUDE_ENV_FILE\""
      }]
    }]
  }
}
```

Le hook écrit dans `$CLAUDE_ENV_FILE`, qui est ensuite sourcé avant chaque commande Bash. Ceci est idéal pour les configurations de projet partagées par l'équipe.

Voir [Hooks SessionStart](/fr/hooks#persist-environment-variables) pour plus de détails sur l'option 3.

### Extension des outils avec des hooks

Vous pouvez exécuter des commandes personnalisées avant ou après l'exécution de n'importe quel outil en utilisant les [hooks Claude Code](/fr/hooks-guide).

Par exemple, vous pourriez exécuter automatiquement un formateur Python après que Claude modifie les fichiers Python, ou empêcher les modifications des fichiers de configuration de production en bloquant les opérations Write vers certains chemins.

## Voir aussi

* [Permissions](/fr/permissions) : système de permissions, syntaxe des règles, modèles spécifiques aux outils et politiques gérées
* [Authentification](/fr/authentication) : configurer l'accès utilisateur à Claude Code
* [Dépannage](/fr/troubleshooting) : solutions pour les problèmes de configuration courants
