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
| **User**    | Répertoire `~/.claude/`                                                                         | Vous, dans tous les projets               | Non                        |
| **Project** | `.claude/` dans le référentiel                                                                  | Tous les collaborateurs de ce référentiel | Oui (commité dans git)     |
| **Local**   | `.claude/settings.local.json`                                                                   | Vous, dans ce référentiel uniquement      | Non (ignoré par gitignore) |

### Quand utiliser chaque portée

La portée **Managed** est pour :

* Les politiques de sécurité qui doivent être appliquées à l'échelle de l'organisation
* Les exigences de conformité qui ne peuvent pas être contournées
* Les configurations standardisées déployées par l'IT/DevOps

La portée **User** est idéale pour :

* Les préférences personnelles que vous voulez partout (thèmes, paramètres d'éditeur)
* Les outils et plugins que vous utilisez dans tous les projets
* Les clés API et l'authentification (stockées de manière sécurisée)

La portée **Project** est idéale pour :

* Les paramètres partagés par l'équipe (permissions, hooks, MCP servers)
* Les plugins que toute l'équipe devrait avoir
* La standardisation des outils entre collaborateurs

La portée **Local** est idéale pour :

* Les remplacements personnels pour un projet spécifique
* Tester les configurations avant de les partager avec l'équipe
* Les paramètres spécifiques à la machine qui ne fonctionneront pas pour les autres

### Comment les portées interagissent

Quand le même paramètre est configuré dans plusieurs portées, les portées plus spécifiques ont la priorité :

1. **Managed** (la plus élevée) - ne peut pas être contournée par quoi que ce soit
2. **Arguments de ligne de commande** - remplacements de session temporaires
3. **Local** - remplace les paramètres de projet et d'utilisateur
4. **Project** - remplace les paramètres d'utilisateur
5. **User** (la plus basse) - s'applique quand rien d'autre ne spécifie le paramètre

Par exemple, si une permission est autorisée dans les paramètres utilisateur mais refusée dans les paramètres de projet, le paramètre de projet a la priorité et la permission est bloquée.

### Ce qui utilise les portées

Les portées s'appliquent à de nombreuses fonctionnalités de Claude Code :

| Fonctionnalité  | Emplacement utilisateur   | Emplacement projet                 | Emplacement local             |
| :-------------- | :------------------------ | :--------------------------------- | :---------------------------- |
| **Settings**    | `~/.claude/settings.json` | `.claude/settings.json`            | `.claude/settings.local.json` |
| **Subagents**   | `~/.claude/agents/`       | `.claude/agents/`                  | Aucun                         |
| **MCP servers** | `~/.claude.json`          | `.mcp.json`                        | `~/.claude.json` (par projet) |
| **Plugins**     | `~/.claude/settings.json` | `.claude/settings.json`            | `.claude/settings.local.json` |
| **CLAUDE.md**   | `~/.claude/CLAUDE.md`     | `CLAUDE.md` ou `.claude/CLAUDE.md` | Aucun                         |

***

## Fichiers de paramètres

Le fichier `settings.json` est le mécanisme officiel pour configurer Claude Code via des paramètres hiérarchiques :

* Les **paramètres utilisateur** sont définis dans `~/.claude/settings.json` et s'appliquent à tous les projets.
* Les **paramètres de projet** sont enregistrés dans votre répertoire de projet :
  * `.claude/settings.json` pour les paramètres qui sont vérifiés dans le contrôle de source et partagés avec votre équipe
  * `.claude/settings.local.json` pour les paramètres qui ne sont pas vérifiés, utiles pour les préférences personnelles et l'expérimentation. Claude Code configurera git pour ignorer `.claude/settings.local.json` quand il est créé.
* **Paramètres gérés** : Pour les organisations qui ont besoin d'un contrôle centralisé, Claude Code supporte plusieurs mécanismes de livraison pour les paramètres gérés. Tous utilisent le même format JSON et ne peuvent pas être contournés par les paramètres utilisateur ou de projet :

  * **Paramètres gérés par le serveur** : livrés depuis les serveurs d'Anthropic via la console d'administration Claude.ai. Voir [paramètres gérés par le serveur](/fr/server-managed-settings).
  * **Politiques MDM/au niveau du système d'exploitation** : livrées via la gestion native des appareils sur macOS et Windows :
    * macOS : domaine de préférences gérées `com.anthropic.claudecode` (déployé via des profils de configuration dans Jamf, Kandji, ou d'autres outils MDM)
    * Windows : clé de registre `HKLM\SOFTWARE\Policies\ClaudeCode` avec une valeur `Settings` (REG\_SZ ou REG\_EXPAND\_SZ) contenant du JSON (déployé via Group Policy ou Intune)
    * Windows (au niveau utilisateur) : `HKCU\SOFTWARE\Policies\ClaudeCode` (priorité de politique la plus basse, utilisée uniquement quand aucune source au niveau administrateur n'existe)
  * **Basé sur fichier** : `managed-settings.json` et `managed-mcp.json` déployés dans les répertoires système :

    * macOS : `/Library/Application Support/ClaudeCode/`
    * Linux et WSL : `/etc/claude-code/`
    * Windows : `C:\Program Files\ClaudeCode\`

    <Warning>
      Le chemin Windows hérité `C:\ProgramData\ClaudeCode\managed-settings.json` n'est plus supporté à partir de v2.1.75. Les administrateurs qui ont déployé des paramètres à cet emplacement doivent migrer les fichiers vers `C:\Program Files\ClaudeCode\managed-settings.json`.
    </Warning>

    Les paramètres gérés basés sur fichier supportent également un répertoire drop-in à `managed-settings.d/` dans le même répertoire système à côté de `managed-settings.json`. Cela permet à des équipes séparées de déployer des fragments de politique indépendants sans coordonner les modifications d'un seul fichier.

    Suivant la convention systemd, `managed-settings.json` est fusionné en premier comme base, puis tous les fichiers `*.json` dans le répertoire drop-in sont triés alphabétiquement et fusionnés par-dessus. Les fichiers ultérieurs remplacent les fichiers antérieurs pour les valeurs scalaires ; les tableaux sont concaténés et dédupliqués ; les objets sont fusionnés en profondeur. Les fichiers cachés commençant par `.` sont ignorés.

    Utilisez des préfixes numériques pour contrôler l'ordre de fusion, par exemple `10-telemetry.json` et `20-security.json`.

  Voir [paramètres gérés](/fr/permissions#managed-only-settings) et [Configuration MCP gérée](/fr/mcp#managed-mcp-configuration) pour plus de détails.

  <Note>
    Les déploiements gérés peuvent également restreindre les **ajouts de marketplace de plugins** en utilisant `strictKnownMarketplaces`. Pour plus d'informations, voir [Restrictions de marketplace gérées](/fr/plugin-marketplaces#managed-marketplace-restrictions).
  </Note>
* **Autre configuration** est stockée dans `~/.claude.json`. Ce fichier contient vos préférences (thème, paramètres de notification, mode d'éditeur), session OAuth, configurations de [MCP server](/fr/mcp) pour les portées utilisateur et locale, état par projet (outils autorisés, paramètres de confiance), et divers caches. Les MCP servers au niveau du projet sont stockés séparément dans `.mcp.json`.

<Note>
  Claude Code crée automatiquement des sauvegardes horodatées des fichiers de configuration et conserve les cinq sauvegardes les plus récentes pour prévenir la perte de données.
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

La ligne `$schema` dans l'exemple ci-dessus pointe vers le [schéma JSON officiel](https://json.schemastore.org/claude-code-settings.json) pour les paramètres Claude Code. L'ajouter à votre `settings.json` active l'autocomplétion et la validation en ligne dans VS Code, Cursor, et tout autre éditeur qui supporte la validation de schéma JSON.

### Paramètres disponibles

`settings.json` supporte un certain nombre d'options :

| Clé                               | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | Exemple                                                                                                                        |
| :-------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| `agent`                           | Exécuter le thread principal en tant que subagent nommé. Applique l'invite système, les restrictions d'outils et le modèle de ce subagent. Voir [Invoquer les subagents explicitement](/fr/sub-agents#invoke-subagents-explicitly)                                                                                                                                                                                                                                                                                                                                                                                                                 | `"code-reviewer"`                                                                                                              |
| `allowedChannelPlugins`           | (Paramètres gérés uniquement) Liste blanche des plugins de channel qui peuvent envoyer des messages. Remplace la liste blanche Anthropic par défaut quand défini. Non défini = revenir à la valeur par défaut, tableau vide = bloquer tous les plugins de channel. Nécessite `channelsEnabled: true`. Voir [Restreindre quels plugins de channel peuvent s'exécuter](/fr/channels#restrict-which-channel-plugins-can-run)                                                                                                                                                                                                                          | `[{ "marketplace": "claude-plugins-official", "plugin": "telegram" }]`                                                         |
| `allowedHttpHookUrls`             | Liste blanche des modèles d'URL que les hooks HTTP peuvent cibler. Supporte `*` comme caractère générique. Quand défini, les hooks avec des URL non correspondantes sont bloqués. Non défini = pas de restriction, tableau vide = bloquer tous les hooks HTTP. Les tableaux fusionnent entre les sources de paramètres. Voir [Configuration des hooks](#hook-configuration)                                                                                                                                                                                                                                                                        | `["https://hooks.example.com/*"]`                                                                                              |
| `allowedMcpServers`               | Quand défini dans managed-settings.json, liste blanche des MCP servers que les utilisateurs peuvent configurer. Non défini = pas de restrictions, tableau vide = verrouillage. S'applique à toutes les portées. La liste noire a la priorité. Voir [Configuration MCP gérée](/fr/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                                                                    | `[{ "serverName": "github" }]`                                                                                                 |
| `allowManagedHooksOnly`           | (Paramètres gérés uniquement) Empêcher le chargement des hooks utilisateur, projet et plugin. Permet uniquement les hooks gérés et les hooks SDK. Voir [Configuration des hooks](#hook-configuration)                                                                                                                                                                                                                                                                                                                                                                                                                                              | `true`                                                                                                                         |
| `allowManagedMcpServersOnly`      | (Paramètres gérés uniquement) Seul `allowedMcpServers` à partir des paramètres gérés est respecté. `deniedMcpServers` fusionne toujours à partir de toutes les sources. Les utilisateurs peuvent toujours ajouter des MCP servers, mais seule la liste blanche définie par l'administrateur s'applique. Voir [Configuration MCP gérée](/fr/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                          | `true`                                                                                                                         |
| `allowManagedPermissionRulesOnly` | (Paramètres gérés uniquement) Empêcher les paramètres utilisateur et projet de définir les règles de permission `allow`, `ask`, ou `deny`. Seules les règles dans les paramètres gérés s'appliquent. Voir [Paramètres gérés uniquement](/fr/permissions#managed-only-settings)                                                                                                                                                                                                                                                                                                                                                                     | `true`                                                                                                                         |
| `alwaysThinkingEnabled`           | Activer la [réflexion étendue](/fr/common-workflows#use-extended-thinking-thinking-mode) par défaut pour toutes les sessions. Généralement configuré via la commande `/config` plutôt que d'éditer directement                                                                                                                                                                                                                                                                                                                                                                                                                                     | `true`                                                                                                                         |
| `apiKeyHelper`                    | Script personnalisé, à exécuter dans `/bin/sh`, pour générer une valeur d'authentification. Cette valeur sera envoyée comme en-têtes `X-Api-Key` et `Authorization: Bearer` pour les demandes de modèle                                                                                                                                                                                                                                                                                                                                                                                                                                            | `/bin/generate_temp_api_key.sh`                                                                                                |
| `attribution`                     | Personnalisez l'attribution pour les commits git et les pull requests. Voir [Paramètres d'attribution](#attribution-settings)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                                                                        |
| `autoMemoryDirectory`             | Répertoire personnalisé pour le stockage de la [mémoire automatique](/fr/memory#storage-location). Accepte les chemins développés avec `~/`. Non accepté dans les paramètres de projet (`.claude/settings.json`) pour empêcher les référentiels partagés de rediriger les écritures de mémoire vers des emplacements sensibles. Accepté à partir des paramètres de politique, locaux et utilisateur                                                                                                                                                                                                                                                | `"~/my-memory-dir"`                                                                                                            |
| `autoMode`                        | Personnalisez ce que le classificateur du [mode auto](/fr/permission-modes#eliminate-prompts-with-auto-mode) bloque et autorise. Contient les tableaux `environment`, `allow`, et `soft_deny` de règles en prose. Voir [Configurer le classificateur du mode auto](/fr/permissions#configure-the-auto-mode-classifier). Non lu à partir des paramètres de projet partagés                                                                                                                                                                                                                                                                          | `{"environment": ["Trusted repo: github.example.com/acme"]}`                                                                   |
| `autoUpdatesChannel`              | Canal de version à suivre pour les mises à jour. Utilisez `"stable"` pour une version généralement une semaine ancienne et qui ignore les versions avec des régressions majeures, ou `"latest"` (par défaut) pour la version la plus récente                                                                                                                                                                                                                                                                                                                                                                                                       | `"stable"`                                                                                                                     |
| `availableModels`                 | Restreindre les modèles que les utilisateurs peuvent sélectionner via `/model`, `--model`, l'outil Config, ou `ANTHROPIC_MODEL`. N'affecte pas l'option Par défaut. Voir [Restreindre la sélection de modèle](/fr/model-config#restrict-model-selection)                                                                                                                                                                                                                                                                                                                                                                                           | `["sonnet", "haiku"]`                                                                                                          |
| `awsAuthRefresh`                  | Script personnalisé qui modifie le répertoire `.aws` (voir [configuration avancée des identifiants](/fr/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `aws sso login --profile myprofile`                                                                                            |
| `awsCredentialExport`             | Script personnalisé qui génère du JSON avec les identifiants AWS (voir [configuration avancée des identifiants](/fr/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `/bin/generate_aws_grant.sh`                                                                                                   |
| `blockedMarketplaces`             | (Paramètres gérés uniquement) Liste noire des sources de marketplace. Les sources bloquées sont vérifiées avant le téléchargement, donc elles ne touchent jamais le système de fichiers. Voir [Restrictions de marketplace gérées](/fr/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                                                                                                                                                                                                                                                       | `[{ "source": "github", "repo": "untrusted/plugins" }]`                                                                        |
| `channelsEnabled`                 | (Paramètres gérés uniquement) Autoriser les [channels](/fr/channels) pour les utilisateurs Team et Enterprise. Non défini ou `false` bloque la livraison des messages de channel indépendamment de ce que les utilisateurs passent à `--channels`                                                                                                                                                                                                                                                                                                                                                                                                  | `true`                                                                                                                         |
| `cleanupPeriodDays`               | Les sessions inactives pendant plus longtemps que cette période sont supprimées au démarrage (par défaut : 30 jours, minimum 1). Définir à `0` est rejeté avec une erreur de validation. Pour désactiver complètement les écritures de transcript en mode non interactif (`-p`), utilisez l'indicateur `--no-session-persistence` ou l'option SDK `persistSession: false` ; il n'y a pas d'équivalent en mode interactif.                                                                                                                                                                                                                          | `20`                                                                                                                           |
| `companyAnnouncements`            | Annonce à afficher aux utilisateurs au démarrage. Si plusieurs annonces sont fournies, elles seront affichées aléatoirement.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]`                                                        |
| `defaultShell`                    | Shell par défaut pour les commandes `!` de la boîte d'entrée. Accepte `"bash"` (par défaut) ou `"powershell"`. Définir à `"powershell"` achemine les commandes `!` interactives via PowerShell sur Windows. Nécessite `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`. Voir [Outil PowerShell](/fr/tools-reference#powershell-tool)                                                                                                                                                                                                                                                                                                                            | `"powershell"`                                                                                                                 |
| `deniedMcpServers`                | Quand défini dans managed-settings.json, liste noire des MCP servers qui sont explicitement bloqués. S'applique à toutes les portées y compris les servers gérés. La liste noire a la priorité sur la liste blanche. Voir [Configuration MCP gérée](/fr/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                                                                                             | `[{ "serverName": "filesystem" }]`                                                                                             |
| `disableAllHooks`                 | Désactiver tous les [hooks](/fr/hooks) et toute [ligne d'état](/fr/statusline) personnalisée                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `true`                                                                                                                         |
| `disableAutoMode`                 | Définir à `"disable"` pour empêcher l'activation du [mode auto](/fr/permission-modes#eliminate-prompts-with-auto-mode). Supprime `auto` du cycle `Shift+Tab` et rejette `--permission-mode auto` au démarrage. Très utile dans les [paramètres gérés](/fr/permissions#managed-settings) où les utilisateurs ne peuvent pas le contourner                                                                                                                                                                                                                                                                                                           | `"disable"`                                                                                                                    |
| `disableDeepLinkRegistration`     | Définir à `"disable"` pour empêcher Claude Code d'enregistrer le gestionnaire de protocole `claude-cli://` auprès du système d'exploitation au démarrage. Les liens profonds permettent aux outils externes d'ouvrir une session Claude Code avec une invite pré-remplie via `claude-cli://open?q=...`. Utile dans les environnements où l'enregistrement du gestionnaire de protocole est restreint ou géré séparément                                                                                                                                                                                                                            | `"disable"`                                                                                                                    |
| `disabledMcpjsonServers`          | Liste des MCP servers spécifiques à partir des fichiers `.mcp.json` à rejeter                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `["filesystem"]`                                                                                                               |
| `effortLevel`                     | Persister le [niveau d'effort](/fr/model-config#adjust-effort-level) entre les sessions. Accepte `"low"`, `"medium"`, ou `"high"`. Écrit automatiquement quand vous exécutez `/effort low`, `/effort medium`, ou `/effort high`. Supporté sur Opus 4.6 et Sonnet 4.6                                                                                                                                                                                                                                                                                                                                                                               | `"medium"`                                                                                                                     |
| `enableAllProjectMcpServers`      | Approuver automatiquement tous les MCP servers définis dans les fichiers `.mcp.json` du projet                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `true`                                                                                                                         |
| `enabledMcpjsonServers`           | Liste des MCP servers spécifiques à partir des fichiers `.mcp.json` à approuver                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `["memory", "github"]`                                                                                                         |
| `env`                             | Variables d'environnement qui seront appliquées à chaque session                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   | `{"FOO": "bar"}`                                                                                                               |
| `fastModePerSessionOptIn`         | Quand `true`, le mode rapide ne persiste pas entre les sessions. Chaque session commence avec le mode rapide désactivé, nécessitant que les utilisateurs l'activent avec `/fast`. La préférence de mode rapide de l'utilisateur est toujours enregistrée. Voir [Exiger l'opt-in par session](/fr/fast-mode#require-per-session-opt-in)                                                                                                                                                                                                                                                                                                             | `true`                                                                                                                         |
| `feedbackSurveyRate`              | Probabilité (0–1) que l'[enquête de qualité de session](/fr/data-usage#session-quality-surveys) apparaisse quand elle est admissible. Définir à `0` pour supprimer complètement. Utile lors de l'utilisation de Bedrock, Vertex, ou Foundry où le taux d'échantillonnage par défaut ne s'applique pas                                                                                                                                                                                                                                                                                                                                              | `0.05`                                                                                                                         |
| `fileSuggestion`                  | Configurez un script personnalisé pour l'autocomplétion de fichier `@`. Voir [Paramètres de suggestion de fichier](#file-suggestion-settings)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`                                                               |
| `forceLoginMethod`                | Utilisez `claudeai` pour restreindre la connexion aux comptes Claude.ai, `console` pour restreindre la connexion aux comptes Claude Console (facturation d'utilisation d'API)                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | `claudeai`                                                                                                                     |
| `forceLoginOrgUUID`               | Exiger que la connexion appartienne à une organisation spécifique. Accepte une seule chaîne UUID, qui pré-sélectionne également cette organisation lors de la connexion, ou un tableau d'UUID où n'importe quelle organisation listée est acceptée sans pré-sélection. Quand défini dans les paramètres gérés, la connexion échoue si le compte authentifié n'appartient pas à une organisation listée ; un tableau vide échoue fermé et bloque la connexion avec un message de mauvaise configuration                                                                                                                                             | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"` ou `["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"]` |
| `hooks`                           | Configurez des commandes personnalisées à exécuter lors d'événements du cycle de vie. Voir [documentation des hooks](/fr/hooks) pour le format                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | Voir [hooks](/fr/hooks)                                                                                                        |
| `httpHookAllowedEnvVars`          | Liste blanche des noms de variables d'environnement que les hooks HTTP peuvent interpoler dans les en-têtes. Quand défini, le `allowedEnvVars` effectif de chaque hook est l'intersection avec cette liste. Non défini = pas de restriction. Les tableaux fusionnent entre les sources de paramètres. Voir [Configuration des hooks](#hook-configuration)                                                                                                                                                                                                                                                                                          | `["MY_TOKEN", "HOOK_SECRET"]`                                                                                                  |
| `includeCoAuthoredBy`             | **Déprécié** : Utilisez `attribution` à la place. S'il faut inclure la ligne `co-authored-by Claude` dans les commits git et les pull requests (par défaut : `true`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                               | `false`                                                                                                                        |
| `includeGitInstructions`          | Inclure les instructions de workflow de commit et PR intégrées et l'instantané du statut git dans l'invite système de Claude (par défaut : `true`). Définir à `false` pour supprimer les deux, par exemple lors de l'utilisation de vos propres skills de workflow git. La variable d'environnement `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` a la priorité sur ce paramètre quand elle est définie                                                                                                                                                                                                                                                   | `false`                                                                                                                        |
| `language`                        | Configurez la langue de réponse préférée de Claude (par exemple, `"japanese"`, `"spanish"`, `"french"`). Claude répondra dans cette langue par défaut. Définit également la langue de la [dictée vocale](/fr/voice-dictation#change-the-dictation-language)                                                                                                                                                                                                                                                                                                                                                                                        | `"japanese"`                                                                                                                   |
| `model`                           | Remplacer le modèle par défaut à utiliser pour Claude Code                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         | `"claude-sonnet-4-6"`                                                                                                          |
| `modelOverrides`                  | Mapper les ID de modèle Anthropic aux ID de modèle spécifiques au fournisseur tels que les ARN de profil d'inférence Bedrock. Chaque entrée du sélecteur de modèle utilise sa valeur mappée lors de l'appel de l'API du fournisseur. Voir [Remplacer les ID de modèle par version](/fr/model-config#override-model-ids-per-version)                                                                                                                                                                                                                                                                                                                | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                                                                                   |
| `otelHeadersHelper`               | Script pour générer des en-têtes OpenTelemetry dynamiques. S'exécute au démarrage et périodiquement (voir [En-têtes dynamiques](/fr/monitoring-usage#dynamic-headers))                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `/bin/generate_otel_headers.sh`                                                                                                |
| `outputStyle`                     | Configurez un style de sortie pour ajuster l'invite système. Voir [documentation des styles de sortie](/fr/output-styles)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          | `"Explanatory"`                                                                                                                |
| `permissions`                     | Voir le tableau ci-dessous pour la structure des permissions.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |                                                                                                                                |
| `plansDirectory`                  | Personnalisez où les fichiers de plan sont stockés. Le chemin est relatif à la racine du projet. Par défaut : `~/.claude/plans`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `"./plans"`                                                                                                                    |
| `pluginTrustMessage`              | (Paramètres gérés uniquement) Message personnalisé ajouté à l'avertissement de confiance du plugin affiché avant l'installation. Utilisez ceci pour ajouter du contexte spécifique à l'organisation, par exemple pour confirmer que les plugins de votre marketplace interne sont vérifiés.                                                                                                                                                                                                                                                                                                                                                        | `"All plugins from our marketplace are approved by IT"`                                                                        |
| `prefersReducedMotion`            | Réduire ou désactiver les animations de l'interface utilisateur (spinners, shimmer, effets flash) pour l'accessibilité                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `true`                                                                                                                         |
| `respectGitignore`                | Contrôler si le sélecteur de fichier `@` respecte les modèles `.gitignore`. Quand `true` (par défaut), les fichiers correspondant aux modèles `.gitignore` sont exclus des suggestions                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `false`                                                                                                                        |
| `showClearContextOnPlanAccept`    | Afficher l'option « effacer le contexte » sur l'écran d'acceptation du plan. Par défaut : `false`. Définir à `true` pour restaurer l'option                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        | `true`                                                                                                                         |
| `showThinkingSummaries`           | Afficher les résumés de [réflexion étendue](/fr/common-workflows#use-extended-thinking-thinking-mode) dans les sessions interactives. Quand non défini ou `false` (par défaut en mode interactif), les blocs de réflexion sont redactés par l'API et affichés comme un stub réduit. La redaction change uniquement ce que vous voyez, pas ce que le modèle génère : pour réduire les dépenses de réflexion, [réduisez le budget ou désactivez la réflexion](/fr/common-workflows#use-extended-thinking-thinking-mode) à la place. Le mode non interactif (`-p`) et les appelants SDK reçoivent toujours les résumés indépendamment de ce paramètre | `true`                                                                                                                         |
| `spinnerTipsEnabled`              | Afficher les conseils dans le spinner pendant que Claude travaille. Définir à `false` pour désactiver les conseils (par défaut : `true`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `false`                                                                                                                        |
| `spinnerTipsOverride`             | Remplacer les conseils du spinner par des chaînes personnalisées. `tips` : tableau de chaînes de conseil. `excludeDefault` : si `true`, afficher uniquement les conseils personnalisés ; si `false` ou absent, les conseils personnalisés sont fusionnés avec les conseils intégrés                                                                                                                                                                                                                                                                                                                                                                | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`                                                              |
| `spinnerVerbs`                    | Personnalisez les verbes d'action affichés dans le spinner et les messages de durée de tour. Définir `mode` à `"replace"` pour utiliser uniquement vos verbes, ou `"append"` pour les ajouter aux valeurs par défaut                                                                                                                                                                                                                                                                                                                                                                                                                               | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                                                                       |
| `statusLine`                      | Configurez une ligne d'état personnalisée pour afficher le contexte. Voir [documentation `statusLine`](/fr/statusline)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             | `{"type": "command", "command": "~/.claude/statusline.sh"}`                                                                    |
| `strictKnownMarketplaces`         | (Paramètres gérés uniquement) Liste blanche des marketplaces de plugins que les utilisateurs peuvent ajouter. Non défini = pas de restrictions, tableau vide = verrouillage. S'applique uniquement aux ajouts de marketplace. Voir [Restrictions de marketplace gérées](/fr/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                                                                                                                                                                                                                  | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                                                                        |
| `useAutoModeDuringPlan`           | Si le mode plan utilise la sémantique du mode auto quand le mode auto est disponible. Par défaut : `true`. Non lu à partir des paramètres de projet partagés. Apparaît dans `/config` comme « Utiliser le mode auto pendant le plan »                                                                                                                                                                                                                                                                                                                                                                                                              | `false`                                                                                                                        |
| `voiceEnabled`                    | Activer la [dictée vocale](/fr/voice-dictation) push-to-talk. Écrit automatiquement quand vous exécutez `/voice`. Nécessite un compte Claude.ai                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `true`                                                                                                                         |

### Paramètres de configuration globale

Ces paramètres sont stockés dans `~/.claude.json` plutôt que dans `settings.json`. Les ajouter à `settings.json` déclenchera une erreur de validation de schéma.

| Clé                          | Description                                                                                                                                                                                                                                                                                                                                                          | Exemple        |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------- |
| `autoConnectIde`             | Se connecter automatiquement à un IDE en cours d'exécution quand Claude Code démarre à partir d'un terminal externe. Par défaut : `false`. Apparaît dans `/config` comme **Auto-connect to IDE (external terminal)** lors de l'exécution en dehors d'un terminal VS Code ou JetBrains                                                                                | `true`         |
| `autoInstallIdeExtension`    | Installer automatiquement l'extension Claude Code IDE lors de l'exécution à partir d'un terminal VS Code. Par défaut : `true`. Apparaît dans `/config` comme **Auto-install IDE extension** lors de l'exécution dans un terminal VS Code ou JetBrains. Vous pouvez également définir la variable d'environnement [`CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`](/fr/env-vars) | `false`        |
| `editorMode`                 | Mode de liaison de touches pour l'invite d'entrée : `"normal"` ou `"vim"`. Par défaut : `"normal"`. Écrit automatiquement quand vous exécutez `/vim`. Apparaît dans `/config` comme **Key binding mode**                                                                                                                                                             | `"vim"`        |
| `showTurnDuration`           | Afficher les messages de durée de tour après les réponses, par exemple « Cooked for 1m 6s ». Par défaut : `true`. Apparaît dans `/config` comme **Show turn duration**                                                                                                                                                                                               | `false`        |
| `terminalProgressBarEnabled` | Afficher la barre de progression du terminal dans les terminaux supportés : ConEmu, Ghostty 1.2.0+, et iTerm2 3.6.6+. Par défaut : `true`. Apparaît dans `/config` comme **Terminal progress bar**                                                                                                                                                                   | `false`        |
| `teammateMode`               | Comment les coéquipiers de l'[équipe d'agents](/fr/agent-teams) s'affichent : `auto` (choisit les volets divisés dans tmux ou iTerm2, en processus sinon), `in-process`, ou `tmux`. Voir [configurer un mode d'affichage](/fr/agent-teams#choose-a-display-mode)                                                                                                     | `"in-process"` |

### Paramètres de worktree

Configurez comment `--worktree` crée et gère les git worktrees. Utilisez ces paramètres pour réduire l'utilisation du disque et le temps de démarrage dans les grands monorepos.

| Clé                           | Description                                                                                                                                                                                                            | Exemple                               |
| :---------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------ |
| `worktree.symlinkDirectories` | Répertoires à créer en lien symbolique à partir du référentiel principal dans chaque worktree pour éviter de dupliquer les grands répertoires sur le disque. Aucun répertoire n'est créé en lien symbolique par défaut | `["node_modules", ".cache"]`          |
| `worktree.sparsePaths`        | Répertoires à extraire dans chaque worktree via git sparse-checkout (mode cone). Seuls les chemins listés sont écrits sur le disque, ce qui est plus rapide dans les grands monorepos                                  | `["packages/my-app", "shared/utils"]` |

Pour copier les fichiers ignorés par git comme `.env` dans les nouveaux worktrees, utilisez un [fichier `.worktreeinclude`](/fr/common-workflows#copy-gitignored-files-to-worktrees) dans la racine de votre projet à la place d'un paramètre.

### Paramètres de permission

| Clés                                | Description                                                                                                                                                                                                                                                                                                       | Exemple                                                                |
| :---------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                             | Tableau de règles de permission pour autoriser l'utilisation d'outils. Voir [Syntaxe de règle de permission](#permission-rule-syntax) ci-dessous pour les détails de correspondance de modèle                                                                                                                     | `[ "Bash(git diff *)" ]`                                               |
| `ask`                               | Tableau de règles de permission pour demander une confirmation lors de l'utilisation d'outils. Voir [Syntaxe de règle de permission](#permission-rule-syntax) ci-dessous                                                                                                                                          | `[ "Bash(git push *)" ]`                                               |
| `deny`                              | Tableau de règles de permission pour refuser l'utilisation d'outils. Utilisez ceci pour exclure les fichiers sensibles de l'accès de Claude Code. Voir [Syntaxe de règle de permission](#permission-rule-syntax) et [Limitations de permission Bash](/fr/permissions#tool-specific-permission-rules)              | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`             | [Répertoires de travail](/fr/permissions#working-directories) supplémentaires pour l'accès aux fichiers. La plupart de la configuration `.claude/` n'est [pas découverte](/fr/permissions#additional-directories-grant-file-access-not-configuration) à partir de ces répertoires                                 | `[ "../docs/" ]`                                                       |
| `defaultMode`                       | [Mode de permission](/fr/permission-modes) par défaut lors de l'ouverture de Claude Code. Valeurs valides : `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. L'indicateur CLI `--permission-mode` remplace ce paramètre pour une seule session                                           | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode`      | Définir à `"disable"` pour empêcher l'activation du mode `bypassPermissions`. Ceci désactive l'indicateur de ligne de commande `--dangerously-skip-permissions`. Très utile dans les [paramètres gérés](/fr/permissions#managed-settings) où les utilisateurs ne peuvent pas le contourner                        | `"disable"`                                                            |
| `skipDangerousModePermissionPrompt` | Ignorer l'invite de confirmation affichée avant d'entrer en mode bypass permissions via `--dangerously-skip-permissions` ou `defaultMode: "bypassPermissions"`. Ignoré quand défini dans les paramètres de projet (`.claude/settings.json`) pour empêcher les référentiels non fiables d'auto-contourner l'invite | `true`                                                                 |

### Syntaxe de règle de permission

Les règles de permission suivent le format `Tool` ou `Tool(specifier)`. Les règles sont évaluées dans l'ordre : d'abord les règles de refus, puis de demande, puis d'autorisation. La première règle correspondante gagne.

Exemples rapides :

| Règle                          | Effet                                                    |
| :----------------------------- | :------------------------------------------------------- |
| `Bash`                         | Correspond à toutes les commandes Bash                   |
| `Bash(npm run *)`              | Correspond aux commandes commençant par `npm run`        |
| `Read(./.env)`                 | Correspond à la lecture du fichier `.env`                |
| `WebFetch(domain:example.com)` | Correspond aux demandes de récupération vers example.com |

Pour la référence complète de la syntaxe des règles, y compris le comportement des caractères génériques, les modèles spécifiques aux outils pour Read, Edit, WebFetch, MCP, et Agent, et les limitations de sécurité des modèles Bash, voir [Syntaxe de règle de permission](/fr/permissions#permission-rule-syntax).

### Paramètres de sandbox

Configurez le comportement avancé du sandboxing. Le sandboxing isole les commandes bash de votre système de fichiers et réseau. Voir [Sandboxing](/fr/sandboxing) pour plus de détails.

| Clés                                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                 | Exemple                         |
| :------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `enabled`                              | Activer le sandboxing bash (macOS, Linux, et WSL2). Par défaut : false                                                                                                                                                                                                                                                                                                                                                      | `true`                          |
| `failIfUnavailable`                    | Quitter avec une erreur au démarrage si `sandbox.enabled` est true mais que le sandbox ne peut pas démarrer (dépendances manquantes, plateforme non supportée, ou restrictions de plateforme). Quand false (par défaut), un avertissement est affiché et les commandes s'exécutent sans sandbox. Destiné aux déploiements de paramètres gérés qui nécessitent le sandboxing comme une porte dure                            | `true`                          |
| `autoAllowBashIfSandboxed`             | Approuver automatiquement les commandes bash quand sandboxées. Par défaut : true                                                                                                                                                                                                                                                                                                                                            | `true`                          |
| `excludedCommands`                     | Commandes qui doivent s'exécuter en dehors du sandbox                                                                                                                                                                                                                                                                                                                                                                       | `["git", "docker"]`             |
| `allowUnsandboxedCommands`             | Autoriser les commandes à s'exécuter en dehors du sandbox via le paramètre `dangerouslyDisableSandbox`. Quand défini à `false`, l'échappatoire `dangerouslyDisableSandbox` est complètement désactivée et toutes les commandes doivent s'exécuter en sandbox (ou être dans `excludedCommands`). Utile pour les politiques d'entreprise qui nécessitent un sandboxing strict. Par défaut : true                              | `false`                         |
| `filesystem.allowWrite`                | Chemins supplémentaires où les commandes sandboxées peuvent écrire. Les tableaux sont fusionnés dans toutes les portées de paramètres : les chemins utilisateur, projet et gérés sont combinés, non remplacés. Également fusionnés avec les chemins des règles de permission `Edit(...)` allow. Voir [préfixes de chemin sandbox](#sandbox-path-prefixes) ci-dessous.                                                       | `["/tmp/build", "~/.kube"]`     |
| `filesystem.denyWrite`                 | Chemins où les commandes sandboxées ne peuvent pas écrire. Les tableaux sont fusionnés dans toutes les portées de paramètres. Également fusionnés avec les chemins des règles de permission `Edit(...)` deny.                                                                                                                                                                                                               | `["/etc", "/usr/local/bin"]`    |
| `filesystem.denyRead`                  | Chemins où les commandes sandboxées ne peuvent pas lire. Les tableaux sont fusionnés dans toutes les portées de paramètres. Également fusionnés avec les chemins des règles de permission `Read(...)` deny.                                                                                                                                                                                                                 | `["~/.aws/credentials"]`        |
| `filesystem.allowRead`                 | Chemins à réautoriser pour la lecture dans les régions `denyRead`. A la priorité sur `denyRead`. Les tableaux sont fusionnés dans toutes les portées de paramètres. Utilisez ceci pour créer des modèles d'accès en lecture spécifiques à l'espace de travail.                                                                                                                                                              | `["."]`                         |
| `filesystem.allowManagedReadPathsOnly` | (Paramètres gérés uniquement) Seuls les chemins `allowRead` à partir des paramètres gérés sont respectés. `denyRead` fusionne toujours à partir de toutes les sources. Par défaut : false                                                                                                                                                                                                                                   | `true`                          |
| `network.allowUnixSockets`             | Chemins de socket Unix accessibles dans le sandbox (pour les agents SSH, etc.)                                                                                                                                                                                                                                                                                                                                              | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`          | Autoriser toutes les connexions de socket Unix dans le sandbox. Par défaut : false                                                                                                                                                                                                                                                                                                                                          | `true`                          |
| `network.allowLocalBinding`            | Autoriser la liaison aux ports localhost (macOS uniquement). Par défaut : false                                                                                                                                                                                                                                                                                                                                             | `true`                          |
| `network.allowedDomains`               | Tableau de domaines à autoriser pour le trafic réseau sortant. Supporte les caractères génériques (par exemple, `*.example.com`).                                                                                                                                                                                                                                                                                           | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly`      | (Paramètres gérés uniquement) Seul `allowedDomains` et les règles allow `WebFetch(domain:...)` à partir des paramètres gérés sont respectés. Les domaines à partir des paramètres utilisateur, projet et locaux sont ignorés. Les domaines non autorisés sont bloqués automatiquement sans inviter l'utilisateur. Les domaines refusés sont toujours respectés à partir de toutes les sources. Par défaut : false           | `true`                          |
| `network.httpProxyPort`                | Port du proxy HTTP utilisé si vous souhaitez apporter votre propre proxy. S'il n'est pas spécifié, Claude exécutera son propre proxy.                                                                                                                                                                                                                                                                                       | `8080`                          |
| `network.socksProxyPort`               | Port du proxy SOCKS5 utilisé si vous souhaitez apporter votre propre proxy. S'il n'est pas spécifié, Claude exécutera son propre proxy.                                                                                                                                                                                                                                                                                     | `8081`                          |
| `enableWeakerNestedSandbox`            | Activer un sandbox plus faible pour les environnements Docker non privilégiés (Linux et WSL2 uniquement). **Réduit la sécurité.** Par défaut : false                                                                                                                                                                                                                                                                        | `true`                          |
| `enableWeakerNetworkIsolation`         | (macOS uniquement) Autoriser l'accès au service de confiance TLS du système (`com.apple.trustd.agent`) dans le sandbox. Requis pour que les outils basés sur Go comme `gh`, `gcloud`, et `terraform` vérifient les certificats TLS lors de l'utilisation de `httpProxyPort` avec un proxy MITM et une CA personnalisée. **Réduit la sécurité** en ouvrant un chemin potentiel d'exfiltration de données. Par défaut : false | `true`                          |

#### Préfixes de chemin sandbox

Les chemins dans `filesystem.allowWrite`, `filesystem.denyWrite`, `filesystem.denyRead`, et `filesystem.allowRead` supportent ces préfixes :

| Préfixe                | Signification                                                                                                 | Exemple                                                                      |
| :--------------------- | :------------------------------------------------------------------------------------------------------------ | :--------------------------------------------------------------------------- |
| `/`                    | Chemin absolu à partir de la racine du système de fichiers                                                    | `/tmp/build` reste `/tmp/build`                                              |
| `~/`                   | Relatif au répertoire personnel                                                                               | `~/.kube` devient `$HOME/.kube`                                              |
| `./` ou pas de préfixe | Relatif à la racine du projet pour les paramètres de projet, ou à `~/.claude` pour les paramètres utilisateur | `./output` dans `.claude/settings.json` se résout en `<project-root>/output` |

Le préfixe plus ancien `//path` pour les chemins absolus fonctionne toujours. Si vous aviez précédemment utilisé `/path` en s'attendant à une résolution relative au projet, passez à `./path`. Cette syntaxe diffère des [règles de permission Read et Edit](/fr/permissions#read-and-edit), qui utilisent `//path` pour absolu et `/path` pour relatif au projet. Les chemins du système de fichiers sandbox utilisent les conventions standard : `/tmp/build` est un chemin absolu.

**Exemple de configuration :**

```json  theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
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

Les **restrictions de système de fichiers et réseau** peuvent être configurées de deux façons qui sont fusionnées ensemble :

* **Paramètres `sandbox.filesystem`** (affichés ci-dessus) : Contrôlez les chemins à la limite du sandbox au niveau du système d'exploitation. Ces restrictions s'appliquent à toutes les commandes de sous-processus (par exemple, `kubectl`, `terraform`, `npm`), pas seulement aux outils de fichier de Claude.
* **Règles de permission** : Utilisez les règles allow/deny `Edit` pour contrôler l'accès à l'outil de fichier de Claude, les règles deny `Read` pour bloquer les lectures, et les règles allow/deny `WebFetch` pour contrôler les domaines réseau. Les chemins de ces règles sont également fusionnés dans la configuration du sandbox.

### Paramètres d'attribution

Claude Code ajoute l'attribution aux commits git et aux pull requests. Ceux-ci sont configurés séparément :

* Les commits utilisent les [trailers git](https://git-scm.com/docs/git-interpret-trailers) (comme `Co-Authored-By`) par défaut, qui peuvent être personnalisés ou désactivés
* Les descriptions de pull request sont du texte brut

| Clés     | Description                                                                                                  |
| :------- | :----------------------------------------------------------------------------------------------------------- |
| `commit` | Attribution pour les commits git, y compris tous les trailers. La chaîne vide masque l'attribution de commit |
| `pr`     | Attribution pour les descriptions de pull request. La chaîne vide masque l'attribution de pull request       |

**Attribution de commit par défaut :**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Attribution de pull request par défaut :**

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
  Le paramètre `attribution` a la priorité sur le paramètre déprécié `includeCoAuthoredBy`. Pour masquer toute attribution, définissez `commit` et `pr` à des chaînes vides.
</Note>

### Paramètres de suggestion de fichier

Configurez une commande personnalisée pour l'autocomplétion de chemin de fichier `@`. La suggestion de fichier intégrée utilise la traversée rapide du système de fichiers, mais les grands monorepos peuvent bénéficier d'une indexation spécifique au projet telle qu'un index de fichier pré-construit ou un outillage personnalisé.

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

Ces paramètres contrôlent quels hooks sont autorisés à s'exécuter et ce que les hooks HTTP peuvent accéder. Le paramètre `allowManagedHooksOnly` ne peut être configuré que dans les [paramètres gérés](#settings-files). Les listes blanches d'URL et de variables d'environnement peuvent être définies à n'importe quel niveau de paramètres et fusionnent entre les sources.

**Comportement quand `allowManagedHooksOnly` est `true` :**

* Les hooks gérés et les hooks SDK sont chargés
* Les hooks utilisateur, projet et plugin sont bloqués

**Restreindre les URL des hooks HTTP :**

Limitez les URL que les hooks HTTP peuvent cibler. Supporte `*` comme caractère générique pour la correspondance. Quand le tableau est défini, les hooks HTTP ciblant des URL non correspondantes sont silencieusement bloqués.

```json  theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**Restreindre les variables d'environnement des hooks HTTP :**

Limitez les noms de variables d'environnement que les hooks HTTP peuvent interpoler dans les valeurs d'en-tête. Le `allowedEnvVars` effectif de chaque hook est l'intersection de sa propre liste et ce paramètre.

```json  theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### Précédence des paramètres

Les paramètres s'appliquent dans l'ordre de précédence. Du plus élevé au plus bas :

1. **Paramètres gérés** ([gérés par le serveur](/fr/server-managed-settings), [politiques MDM/au niveau du système d'exploitation](#configuration-scopes), ou [paramètres gérés](/fr/settings#settings-files))
   * Politiques déployées par l'IT via la livraison par serveur, les profils de configuration MDM, les politiques de registre, ou les fichiers de paramètres gérés
   * Ne peuvent pas être contournés par aucun autre niveau, y compris les arguments de ligne de commande
   * Au sein du niveau géré, la précédence est : gérés par le serveur > politiques MDM/au niveau du système d'exploitation > fichiers (`managed-settings.d/*.json` + `managed-settings.json`) > registre HKCU (Windows uniquement). Une seule source gérée est utilisée ; les sources ne fusionnent pas entre les niveaux. Au sein du niveau basé sur fichier, les fichiers drop-in et le fichier de base sont fusionnés ensemble.

2. **Arguments de ligne de commande**
   * Remplacements temporaires pour une session spécifique

3. **Paramètres de projet local** (`.claude/settings.local.json`)
   * Paramètres personnels spécifiques au projet

4. **Paramètres de projet partagés** (`.claude/settings.json`)
   * Paramètres de projet partagés par l'équipe dans le contrôle de source

5. **Paramètres utilisateur** (`~/.claude/settings.json`)
   * Paramètres globaux personnels

Cette hiérarchie garantit que les politiques organisationnelles sont toujours appliquées tout en permettant aux équipes et aux individus de personnaliser leur expérience. La même précédence s'applique que vous exécutiez Claude Code à partir de la CLI, de l'[extension VS Code](/fr/vs-code), ou d'un [IDE JetBrains](/fr/jetbrains).

Par exemple, si vos paramètres utilisateur autorisent `Bash(npm run *)` mais que les paramètres partagés d'un projet le refusent, le paramètre de projet a la priorité et la commande est bloquée.

<Note>
  **Les paramètres de tableau fusionnent entre les portées.** Quand le même paramètre avec valeur de tableau (tel que `sandbox.filesystem.allowWrite` ou `permissions.allow`) apparaît dans plusieurs portées, les tableaux sont **concaténés et dédupliqués**, non remplacés. Cela signifie que les portées de priorité inférieure peuvent ajouter des entrées sans remplacer celles définies par les portées de priorité supérieure, et vice versa. Par exemple, si les paramètres gérés définissent `allowWrite` à `["/opt/company-tools"]` et qu'un utilisateur ajoute `["~/.kube"]`, les deux chemins sont inclus dans la configuration finale.
</Note>

### Vérifier les paramètres actifs

Exécutez `/status` dans Claude Code pour voir quelles sources de paramètres sont actives et d'où elles proviennent. La sortie affiche chaque couche de configuration (gérée, utilisateur, projet) ainsi que son origine, telle que `Enterprise managed settings (remote)`, `Enterprise managed settings (plist)`, `Enterprise managed settings (HKLM)`, ou `Enterprise managed settings (file)`. Si un fichier de paramètres contient des erreurs, `/status` signale le problème pour que vous puissiez le corriger.

### Points clés du système de configuration

* **Fichiers de mémoire (`CLAUDE.md`)** : Contiennent les instructions et le contexte que Claude charge au démarrage
* **Fichiers de paramètres (JSON)** : Configurez les permissions, les variables d'environnement, et le comportement des outils
* **Skills** : Invites personnalisées qui peuvent être invoquées avec `/skill-name` ou chargées automatiquement par Claude
* **MCP servers** : Étendez Claude Code avec des outils et des intégrations supplémentaires
* **Précédence** : Les configurations de niveau supérieur (Managed) remplacent celles de niveau inférieur (User/Project)
* **Héritage** : Les paramètres sont fusionnés, avec les paramètres plus spécifiques s'ajoutant à ou remplaçant les paramètres plus larges

### Invite système

L'invite système interne de Claude Code n'est pas publiée. Pour ajouter des instructions personnalisées, utilisez les fichiers `CLAUDE.md` ou l'indicateur `--append-system-prompt`.

### Exclure les fichiers sensibles

Pour empêcher Claude Code d'accéder aux fichiers contenant des informations sensibles comme les clés API, les secrets, et les fichiers d'environnement, utilisez le paramètre `permissions.deny` dans votre fichier `.claude/settings.json` :

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

Ceci remplace la configuration dépréciée `ignorePatterns`. Les fichiers correspondant à ces modèles sont exclus de la découverte de fichiers et des résultats de recherche, et les opérations de lecture sur ces fichiers sont refusées.

## Configuration des subagents

Claude Code supporte les subagents IA personnalisés qui peuvent être configurés aux niveaux utilisateur et projet. Ces subagents sont stockés en tant que fichiers Markdown avec du frontmatter YAML :

* **Subagents utilisateur** : `~/.claude/agents/` - Disponibles dans tous vos projets
* **Subagents de projet** : `.claude/agents/` - Spécifiques à votre projet et peuvent être partagés avec votre équipe

Les fichiers de subagent définissent des assistants IA spécialisés avec des invites personnalisées et des permissions d'outils. En savoir plus sur la création et l'utilisation des subagents dans la [documentation des subagents](/fr/sub-agents).

## Configuration des plugins

Claude Code supporte un système de plugins qui vous permet d'étendre les fonctionnalités avec des skills, des agents, des hooks, et des MCP servers. Les plugins sont distribués via des marketplaces et peuvent être configurés aux niveaux utilisateur et référentiel.

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

Contrôle quels plugins sont activés. Format : `"plugin-name@marketplace-name": true/false`

**Portées** :

* **Paramètres utilisateur** (`~/.claude/settings.json`) : Préférences personnelles de plugin
* **Paramètres de projet** (`.claude/settings.json`) : Plugins spécifiques au projet partagés avec l'équipe
* **Paramètres locaux** (`.claude/settings.local.json`) : Remplacements par machine (non commités)
* **Paramètres gérés** (`managed-settings.json`) : Remplacements de politique au niveau de l'organisation qui bloquent l'installation à toutes les portées et masquent le plugin de la marketplace

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

**Quand un référentiel inclut `extraKnownMarketplaces`** :

1. Les membres de l'équipe sont invités à installer la marketplace quand ils font confiance au dossier
2. Les membres de l'équipe sont ensuite invités à installer les plugins de cette marketplace
3. Les utilisateurs peuvent ignorer les marketplaces ou plugins indésirables (stockés dans les paramètres utilisateur)
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

**Types de source de marketplace** :

* `github` : Référentiel GitHub (utilise `repo`)
* `git` : N'importe quelle URL git (utilise `url`)
* `directory` : Chemin du système de fichiers local (utilise `path`, pour le développement uniquement)
* `hostPattern` : Modèle regex pour correspondre aux hôtes de marketplace (utilise `hostPattern`)
* `settings` : marketplace en ligne déclarée directement dans settings.json sans référentiel hébergé séparé (utilise `name` et `plugins`)

Utilisez `source: 'settings'` pour déclarer un petit ensemble de plugins en ligne sans configurer un référentiel de marketplace hébergé. Les plugins listés ici doivent référencer des sources externes telles que GitHub ou npm. Vous devez toujours activer chaque plugin séparément dans `enabledPlugins`.

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "settings",
        "name": "team-tools",
        "plugins": [
          {
            "name": "code-formatter",
            "source": {
              "source": "github",
              "repo": "acme-corp/code-formatter"
            }
          }
        ]
      }
    }
  }
}
```

#### `strictKnownMarketplaces`

**Paramètres gérés uniquement** : Contrôle quelles marketplaces de plugins les utilisateurs sont autorisés à ajouter. Ce paramètre ne peut être configuré que dans les [paramètres gérés](/fr/settings#settings-files) et fournit aux administrateurs un contrôle strict sur les sources de marketplace.

**Emplacements des fichiers de paramètres gérés** :

* **macOS** : `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux et WSL** : `/etc/claude-code/managed-settings.json`
* **Windows** : `C:\Program Files\ClaudeCode\managed-settings.json`

**Caractéristiques clés** :

* Disponible uniquement dans les paramètres gérés (`managed-settings.json`)
* Ne peut pas être contourné par les paramètres utilisateur ou projet (précédence la plus élevée)
* Appliqué AVANT les opérations de réseau/système de fichiers (les sources bloquées ne s'exécutent jamais)
* Utilise la correspondance exacte pour les spécifications de source (y compris `ref`, `path` pour les sources git), sauf `hostPattern`, qui utilise la correspondance regex

**Comportement de la liste blanche** :

* `undefined` (par défaut) : Pas de restrictions - les utilisateurs peuvent ajouter n'importe quelle marketplace
* Tableau vide `[]` : Verrouillage complet - les utilisateurs ne peuvent pas ajouter de nouvelles marketplaces
* Liste de sources : Les utilisateurs ne peuvent ajouter que les marketplaces qui correspondent exactement

**Tous les types de source supportés** :

La liste blanche supporte plusieurs types de source de marketplace. La plupart des sources utilisent la correspondance exacte, tandis que `hostPattern` utilise la correspondance regex par rapport à l'hôte de la marketplace.

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
  Les marketplaces basées sur URL téléchargent uniquement le fichier `marketplace.json`. Elles ne téléchargent pas les fichiers de plugin à partir du serveur. Les plugins dans les marketplaces basées sur URL doivent utiliser des sources externes (URLs GitHub, npm, ou git) plutôt que des chemins relatifs. Pour les plugins avec des chemins relatifs, utilisez une marketplace basée sur Git à la place. Voir [Dépannage](/fr/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) pour plus de détails.
</Note>

4. **Packages NPM** :

```json  theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

Champs : `package` (requis, supporte les packages scoped)

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

Utilisez la correspondance de modèle d'hôte quand vous voulez autoriser toutes les marketplaces d'un hôte spécifique sans énumérer chaque référentiel individuellement. Ceci est utile pour les organisations avec des serveurs GitHub Enterprise ou GitLab internes où les développeurs créent leurs propres marketplaces.

Extraction d'hôte par type de source :

* `github` : correspond toujours à `github.com`
* `git` : extrait le nom d'hôte de l'URL (supporte les formats HTTPS et SSH)
* `url` : extrait le nom d'hôte de l'URL
* `npm`, `file`, `directory` : non supporté pour la correspondance de modèle d'hôte

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

Les sources de marketplace doivent correspondre **exactement** pour qu'un ajout d'utilisateur soit autorisé. Pour les sources basées sur git (`github` et `git`), cela inclut tous les champs optionnels :

* Le `repo` ou `url` doit correspondre exactement
* Le champ `ref` doit correspondre exactement (ou les deux être non définis)
* Le champ `path` doit correspondre exactement (ou les deux être non définis)

Exemples de sources qui **NE correspondent PAS** :

```json  theme={null}
// Ce sont des sources DIFFÉRENTES :
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// Ce sont aussi DIFFÉRENTES :
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
```

**Comparaison avec `extraKnownMarketplaces`** :

| Aspect                    | `strictKnownMarketplaces`                          | `extraKnownMarketplaces`                             |
| ------------------------- | -------------------------------------------------- | ---------------------------------------------------- |
| **Objectif**              | Application de la politique organisationnelle      | Commodité de l'équipe                                |
| **Fichier de paramètres** | `managed-settings.json` uniquement                 | N'importe quel fichier de paramètres                 |
| **Comportement**          | Bloque les ajouts non autorisés                    | Installe automatiquement les marketplaces manquantes |
| **Quand appliqué**        | Avant les opérations de réseau/système de fichiers | Après l'invite de confiance de l'utilisateur         |
| **Peut être contourné**   | Non (précédence la plus élevée)                    | Oui (par les paramètres de précédence supérieure)    |
| **Format de source**      | Objet de source direct                             | Marketplace nommée avec source imbriquée             |
| **Cas d'usage**           | Conformité, restrictions de sécurité               | Intégration, standardisation                         |

**Différence de format** :

`strictKnownMarketplaces` utilise des objets de source directs :

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

**Utiliser les deux ensemble** :

`strictKnownMarketplaces` est une porte de politique : elle contrôle ce que les utilisateurs peuvent ajouter mais n'enregistre aucune marketplace. Pour à la fois restreindre et pré-enregistrer une marketplace pour tous les utilisateurs, définissez les deux dans `managed-settings.json` :

```json  theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ],
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

Avec uniquement `strictKnownMarketplaces` défini, les utilisateurs peuvent toujours ajouter la marketplace autorisée manuellement via `/plugin marketplace add`, mais elle n'est pas disponible automatiquement.

**Notes importantes** :

* Les restrictions sont vérifiées AVANT toute demande réseau ou opération de système de fichiers
* Quand bloquée, les utilisateurs voient des messages d'erreur clairs indiquant que la source est bloquée par la politique gérée
* La restriction s'applique uniquement à l'ajout de NOUVELLES marketplaces ; les marketplaces précédemment installées restent accessibles
* Les paramètres gérés ont la précédence la plus élevée et ne peuvent pas être contournés

Voir [Restrictions de marketplace gérées](/fr/plugin-marketplaces#managed-marketplace-restrictions) pour la documentation destinée aux utilisateurs.

### Gérer les plugins

Utilisez la commande `/plugin` pour gérer les plugins de manière interactive :

* Parcourir les plugins disponibles à partir des marketplaces
* Installer/désinstaller les plugins
* Activer/désactiver les plugins
* Afficher les détails du plugin (commandes, agents, hooks fournis)
* Ajouter/supprimer les marketplaces

En savoir plus sur le système de plugins dans la [documentation des plugins](/fr/plugins).

## Variables d'environnement

Les variables d'environnement vous permettent de contrôler le comportement de Claude Code sans éditer les fichiers de paramètres. N'importe quelle variable peut également être configurée dans [`settings.json`](#available-settings) sous la clé `env` pour l'appliquer à chaque session ou la déployer à votre équipe.

Voir la [référence des variables d'environnement](/fr/env-vars) pour la liste complète.

## Outils disponibles pour Claude

Claude Code a accès à un ensemble d'outils pour lire, éditer, rechercher, exécuter des commandes, et orchestrer les subagents. Les noms d'outils sont les chaînes exactes que vous utilisez dans les règles de permission et les correspondances de hooks.

Voir la [référence des outils](/fr/tools-reference) pour la liste complète et les détails du comportement de l'outil Bash.

## Voir aussi

* [Permissions](/fr/permissions) : système de permissions, syntaxe des règles, modèles spécifiques aux outils, et politiques gérées
* [Authentification](/fr/authentication) : configurer l'accès utilisateur à Claude Code
* [Dépannage](/fr/troubleshooting) : solutions pour les problèmes de configuration courants
