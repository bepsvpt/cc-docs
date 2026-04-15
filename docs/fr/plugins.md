> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Créer des plugins

> Créez des plugins personnalisés pour étendre Claude Code avec des skills, des agents, des hooks et des serveurs MCP.

Les plugins vous permettent d'étendre Claude Code avec des fonctionnalités personnalisées qui peuvent être partagées entre les projets et les équipes. Ce guide couvre la création de vos propres plugins avec des skills, des agents, des hooks et des serveurs MCP.

Vous cherchez à installer des plugins existants ? Consultez [Découvrir et installer des plugins](/fr/discover-plugins). Pour les spécifications techniques complètes, consultez [Référence des plugins](/fr/plugins-reference).

## Quand utiliser les plugins par rapport à la configuration autonome

Claude Code prend en charge deux façons d'ajouter des skills, des agents et des hooks personnalisés :

| Approche                                                    | Noms des skills      | Idéal pour                                                                                                    |
| :---------------------------------------------------------- | :------------------- | :------------------------------------------------------------------------------------------------------------ |
| **Autonome** (répertoire `.claude/`)                        | `/hello`             | Flux de travail personnels, personnalisations spécifiques au projet, expériences rapides                      |
| **Plugins** (répertoires avec `.claude-plugin/plugin.json`) | `/plugin-name:hello` | Partage avec les coéquipiers, distribution à la communauté, versions publiées, réutilisable entre les projets |

**Utilisez la configuration autonome quand** :

* Vous personnalisez Claude Code pour un seul projet
* La configuration est personnelle et n'a pas besoin d'être partagée
* Vous expérimentez avec des skills ou des hooks avant de les empaqueter
* Vous voulez des noms de skills courts comme `/hello` ou `/deploy`

**Utilisez les plugins quand** :

* Vous voulez partager des fonctionnalités avec votre équipe ou la communauté
* Vous avez besoin des mêmes skills/agents sur plusieurs projets
* Vous voulez le contrôle de version et les mises à jour faciles pour vos extensions
* Vous distribuez via une marketplace
* Vous êtes d'accord avec les skills avec espace de noms comme `/my-plugin:hello` (l'espace de noms prévient les conflits entre les plugins)

<Tip>
  Commencez par la configuration autonome dans `.claude/` pour une itération rapide, puis [convertissez en plugin](#convert-existing-configurations-to-plugins) quand vous êtes prêt à partager.
</Tip>

## Démarrage rapide

Ce démarrage rapide vous guide dans la création d'un plugin avec un skill personnalisé. Vous allez créer un manifeste (le fichier de configuration qui définit votre plugin), ajouter un skill et le tester localement en utilisant le drapeau `--plugin-dir`.

### Prérequis

* Claude Code [installé et authentifié](/fr/quickstart#step-1-install-claude-code)

<Note>
  Si vous ne voyez pas la commande `/plugin`, mettez à jour Claude Code vers la dernière version. Consultez [Dépannage](/fr/troubleshooting) pour les instructions de mise à niveau.
</Note>

### Créez votre premier plugin

<Steps>
  <Step title="Créez le répertoire du plugin">
    Chaque plugin se trouve dans son propre répertoire contenant un manifeste et vos skills, agents ou hooks. Créez-en un maintenant :

    ```bash theme={null}
    mkdir my-first-plugin
    ```
  </Step>

  <Step title="Créez le manifeste du plugin">
    Le fichier manifeste à `.claude-plugin/plugin.json` définit l'identité de votre plugin : son nom, sa description et sa version. Claude Code utilise ces métadonnées pour afficher votre plugin dans le gestionnaire de plugins.

    Créez le répertoire `.claude-plugin` à l'intérieur de votre dossier de plugin :

    ```bash theme={null}
    mkdir my-first-plugin/.claude-plugin
    ```

    Ensuite, créez `my-first-plugin/.claude-plugin/plugin.json` avec ce contenu :

    ```json my-first-plugin/.claude-plugin/plugin.json theme={null}
    {
    "name": "my-first-plugin",
    "description": "A greeting plugin to learn the basics",
    "version": "1.0.0",
    "author": {
    "name": "Your Name"
    }
    }
    ```

    | Champ         | Objectif                                                                                                                   |
    | :------------ | :------------------------------------------------------------------------------------------------------------------------- |
    | `name`        | Identifiant unique et espace de noms du skill. Les skills sont préfixés avec ceci (par exemple, `/my-first-plugin:hello`). |
    | `description` | Affiché dans le gestionnaire de plugins lors de la navigation ou de l'installation de plugins.                             |
    | `version`     | Suivez les versions en utilisant le [versioning sémantique](/fr/plugins-reference#version-management).                     |
    | `author`      | Optionnel. Utile pour l'attribution.                                                                                       |

    Pour les champs supplémentaires comme `homepage`, `repository` et `license`, consultez le [schéma manifeste complet](/fr/plugins-reference#plugin-manifest-schema).
  </Step>

  <Step title="Ajoutez un skill">
    Les skills se trouvent dans le répertoire `skills/`. Chaque skill est un dossier contenant un fichier `SKILL.md`. Le nom du dossier devient le nom du skill, préfixé par l'espace de noms du plugin (`hello/` dans un plugin nommé `my-first-plugin` crée `/my-first-plugin:hello`).

    Créez un répertoire de skill dans votre dossier de plugin :

    ```bash theme={null}
    mkdir -p my-first-plugin/skills/hello
    ```

    Ensuite, créez `my-first-plugin/skills/hello/SKILL.md` avec ce contenu :

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    description: Greet the user with a friendly message
    disable-model-invocation: true
    ---

    Greet the user warmly and ask how you can help them today.
    ```
  </Step>

  <Step title="Testez votre plugin">
    Exécutez Claude Code avec le drapeau `--plugin-dir` pour charger votre plugin :

    ```bash theme={null}
    claude --plugin-dir ./my-first-plugin
    ```

    Une fois Claude Code démarré, essayez votre nouveau skill :

    ```shell theme={null}
    /my-first-plugin:hello
    ```

    Vous verrez Claude répondre avec un salut. Exécutez `/help` pour voir votre skill listé sous l'espace de noms du plugin.

    <Note>
      **Pourquoi l'espace de noms ?** Les skills des plugins sont toujours avec espace de noms (comme `/my-first-plugin:hello`) pour prévenir les conflits quand plusieurs plugins ont des skills avec le même nom.

      Pour changer le préfixe d'espace de noms, mettez à jour le champ `name` dans `plugin.json`.
    </Note>
  </Step>

  <Step title="Ajoutez des arguments au skill">
    Rendez votre skill dynamique en acceptant l'entrée de l'utilisateur. L'espace réservé `$ARGUMENTS` capture tout texte que l'utilisateur fournit après le nom du skill.

    Mettez à jour votre fichier `SKILL.md` :

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    description: Greet the user with a personalized message
    ---

    # Hello Skill

    Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.
    ```

    Exécutez `/reload-plugins` pour récupérer les modifications, puis essayez le skill avec votre nom :

    ```shell theme={null}
    /my-first-plugin:hello Alex
    ```

    Claude vous saluera par votre nom. Pour plus d'informations sur la transmission d'arguments aux skills, consultez [Skills](/fr/skills#pass-arguments-to-skills).
  </Step>
</Steps>

Vous avez créé et testé avec succès un plugin avec ces composants clés :

* **Manifeste du plugin** (`.claude-plugin/plugin.json`) : décrit les métadonnées de votre plugin
* **Répertoire des skills** (`skills/`) : contient vos skills personnalisés
* **Arguments du skill** (`$ARGUMENTS`) : capture l'entrée de l'utilisateur pour un comportement dynamique

<Tip>
  Le drapeau `--plugin-dir` est utile pour le développement et les tests. Quand vous êtes prêt à partager votre plugin avec d'autres, consultez [Créer et distribuer une marketplace de plugins](/fr/plugin-marketplaces).
</Tip>

## Aperçu de la structure du plugin

Vous avez créé un plugin avec un skill, mais les plugins peuvent inclure beaucoup plus : des agents personnalisés, des hooks, des serveurs MCP et des serveurs LSP.

<Warning>
  **Erreur courante** : Ne mettez pas `commands/`, `agents/`, `skills/` ou `hooks/` à l'intérieur du répertoire `.claude-plugin/`. Seul `plugin.json` va à l'intérieur de `.claude-plugin/`. Tous les autres répertoires doivent être au niveau racine du plugin.
</Warning>

| Répertoire        | Emplacement      | Objectif                                                                                                |
| :---------------- | :--------------- | :------------------------------------------------------------------------------------------------------ |
| `.claude-plugin/` | Racine du plugin | Contient le manifeste `plugin.json` (optionnel si les composants utilisent les emplacements par défaut) |
| `commands/`       | Racine du plugin | Skills en tant que fichiers Markdown                                                                    |
| `agents/`         | Racine du plugin | Définitions d'agents personnalisés                                                                      |
| `skills/`         | Racine du plugin | Agent Skills avec fichiers `SKILL.md`                                                                   |
| `hooks/`          | Racine du plugin | Gestionnaires d'événements dans `hooks.json`                                                            |
| `.mcp.json`       | Racine du plugin | Configurations du serveur MCP                                                                           |
| `.lsp.json`       | Racine du plugin | Configurations du serveur LSP pour l'intelligence du code                                               |
| `settings.json`   | Racine du plugin | [Paramètres](/fr/settings) par défaut appliqués quand le plugin est activé                              |

<Note>
  **Prochaines étapes** : Prêt à ajouter plus de fonctionnalités ? Allez à [Développer des plugins plus complexes](#develop-more-complex-plugins) pour ajouter des agents, des hooks, des serveurs MCP et des serveurs LSP. Pour les spécifications techniques complètes de tous les composants du plugin, consultez [Référence des plugins](/fr/plugins-reference).
</Note>

## Développer des plugins plus complexes

Une fois que vous êtes à l'aise avec les plugins de base, vous pouvez créer des extensions plus sophistiquées.

### Ajoutez des Skills à votre plugin

Les plugins peuvent inclure des [Agent Skills](/fr/skills) pour étendre les capacités de Claude. Les skills sont invoqués par le modèle : Claude les utilise automatiquement en fonction du contexte de la tâche.

Ajoutez un répertoire `skills/` à la racine de votre plugin avec des dossiers de Skill contenant des fichiers `SKILL.md` :

```text theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── code-review/
        └── SKILL.md
```

Chaque `SKILL.md` a besoin d'un frontmatter avec les champs `name` et `description`, suivi d'instructions :

```yaml theme={null}
---
name: code-review
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

Après l'installation du plugin, exécutez `/reload-plugins` pour charger les Skills. Pour des conseils complets sur la création de Skills incluant la divulgation progressive et les restrictions d'outils, consultez [Agent Skills](/fr/skills).

### Ajoutez des serveurs LSP à votre plugin

<Tip>
  Pour les langages courants comme TypeScript, Python et Rust, installez les plugins LSP pré-construits à partir de la marketplace officielle. Créez des plugins LSP personnalisés uniquement quand vous avez besoin de support pour des langages non encore couverts.
</Tip>

Les plugins LSP (Language Server Protocol) donnent à Claude l'intelligence du code en temps réel. Si vous avez besoin de supporter un langage qui n'a pas de plugin LSP officiel, vous pouvez en créer un en ajoutant un fichier `.lsp.json` à votre plugin :

```json .lsp.json theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

Les utilisateurs qui installent votre plugin doivent avoir le binaire du serveur de langage installé sur leur machine.

Pour les options de configuration LSP complètes, consultez [Serveurs LSP](/fr/plugins-reference#lsp-servers).

### Livrez les paramètres par défaut avec votre plugin

Les plugins peuvent inclure un fichier `settings.json` à la racine du plugin pour appliquer la configuration par défaut quand le plugin est activé. Actuellement, seule la clé `agent` est supportée.

Définir `agent` active l'un des [agents personnalisés](/fr/sub-agents) du plugin en tant que thread principal, en appliquant son invite système, ses restrictions d'outils et son modèle. Cela permet à un plugin de changer le comportement par défaut de Claude Code quand il est activé.

```json settings.json theme={null}
{
  "agent": "security-reviewer"
}
```

Cet exemple active l'agent `security-reviewer` défini dans le répertoire `agents/` du plugin. Les paramètres de `settings.json` ont priorité sur les `settings` déclarés dans `plugin.json`. Les clés inconnues sont silencieusement ignorées.

### Organisez les plugins complexes

Pour les plugins avec de nombreux composants, organisez votre structure de répertoires par fonctionnalité. Pour les dispositions de répertoires complètes et les modèles d'organisation, consultez [Structure du répertoire du plugin](/fr/plugins-reference#plugin-directory-structure).

### Testez vos plugins localement

Utilisez le drapeau `--plugin-dir` pour tester les plugins pendant le développement. Cela charge votre plugin directement sans nécessiter d'installation.

```bash theme={null}
claude --plugin-dir ./my-plugin
```

Quand un plugin `--plugin-dir` a le même nom qu'un plugin marketplace installé, la copie locale prend la priorité pour cette session. Cela vous permet de tester les modifications d'un plugin que vous avez déjà installé sans le désinstaller d'abord. Les plugins marketplace forcément activés par les paramètres gérés sont la seule exception et ne peuvent pas être remplacés.

À mesure que vous apportez des modifications à votre plugin, exécutez `/reload-plugins` pour récupérer les mises à jour sans redémarrer. Cela recharge les plugins, les skills, les agents, les hooks, les serveurs MCP du plugin et les serveurs LSP du plugin. Testez vos composants de plugin :

* Essayez vos skills avec `/plugin-name:skill-name`
* Vérifiez que les agents apparaissent dans `/agents`
* Vérifiez que les hooks fonctionnent comme prévu

<Tip>
  Vous pouvez charger plusieurs plugins à la fois en spécifiant le drapeau plusieurs fois :

  ```bash theme={null}
  claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
  ```
</Tip>

### Déboguez les problèmes de plugin

Si votre plugin ne fonctionne pas comme prévu :

1. **Vérifiez la structure** : Assurez-vous que vos répertoires sont à la racine du plugin, pas à l'intérieur de `.claude-plugin/`
2. **Testez les composants individuellement** : Vérifiez chaque commande, agent et hook séparément
3. **Utilisez les outils de validation et de débogage** : Consultez [Outils de débogage et de développement](/fr/plugins-reference#debugging-and-development-tools) pour les commandes CLI et les techniques de dépannage

### Partagez vos plugins

Quand votre plugin est prêt à être partagé :

1. **Ajoutez de la documentation** : Incluez un `README.md` avec les instructions d'installation et d'utilisation
2. **Versionnez votre plugin** : Utilisez le [versioning sémantique](/fr/plugins-reference#version-management) dans votre `plugin.json`
3. **Créez ou utilisez une marketplace** : Distribuez via des [marketplaces de plugins](/fr/plugin-marketplaces) pour l'installation
4. **Testez avec d'autres** : Faites tester le plugin par les membres de l'équipe avant une distribution plus large

Une fois que votre plugin est dans une marketplace, d'autres peuvent l'installer en utilisant les instructions dans [Découvrir et installer des plugins](/fr/discover-plugins).

### Soumettez votre plugin à la marketplace officielle

Pour soumettre un plugin à la marketplace officielle d'Anthropic, utilisez l'un des formulaires de soumission dans l'application :

* **Claude.ai** : [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
* **Console** : [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

<Note>
  Pour les spécifications techniques complètes, les techniques de débogage et les stratégies de distribution, consultez [Référence des plugins](/fr/plugins-reference).
</Note>

## Convertir les configurations existantes en plugins

Si vous avez déjà des skills ou des hooks dans votre répertoire `.claude/`, vous pouvez les convertir en plugin pour un partage et une distribution plus faciles.

### Étapes de migration

<Steps>
  <Step title="Créez la structure du plugin">
    Créez un nouveau répertoire de plugin :

    ```bash theme={null}
    mkdir -p my-plugin/.claude-plugin
    ```

    Créez le fichier manifeste à `my-plugin/.claude-plugin/plugin.json` :

    ```json my-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "my-plugin",
      "description": "Migrated from standalone configuration",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Copiez vos fichiers existants">
    Copiez vos configurations existantes dans le répertoire du plugin :

    ```bash theme={null}
    # Copy commands
    cp -r .claude/commands my-plugin/

    # Copy agents (if any)
    cp -r .claude/agents my-plugin/

    # Copy skills (if any)
    cp -r .claude/skills my-plugin/
    ```
  </Step>

  <Step title="Migrez les hooks">
    Si vous avez des hooks dans vos paramètres, créez un répertoire de hooks :

    ```bash theme={null}
    mkdir my-plugin/hooks
    ```

    Créez `my-plugin/hooks/hooks.json` avec votre configuration de hooks. Copiez l'objet `hooks` de votre `.claude/settings.json` ou `settings.local.json`, car le format est le même. La commande reçoit l'entrée du hook en tant que JSON sur stdin, donc utilisez `jq` pour extraire le chemin du fichier :

    ```json my-plugin/hooks/hooks.json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }]
          }
        ]
      }
    }
    ```
  </Step>

  <Step title="Testez votre plugin migré">
    Chargez votre plugin pour vérifier que tout fonctionne :

    ```bash theme={null}
    claude --plugin-dir ./my-plugin
    ```

    Testez chaque composant : exécutez vos commandes, vérifiez que les agents apparaissent dans `/agents` et vérifiez que les hooks se déclenchent correctement.
  </Step>
</Steps>

### Ce qui change lors de la migration

| Autonome (`.claude/`)                      | Plugin                                 |
| :----------------------------------------- | :------------------------------------- |
| Disponible uniquement dans un projet       | Peut être partagé via des marketplaces |
| Fichiers dans `.claude/commands/`          | Fichiers dans `plugin-name/commands/`  |
| Hooks dans `settings.json`                 | Hooks dans `hooks/hooks.json`          |
| Doit être copié manuellement pour partager | Installer avec `/plugin install`       |

<Note>
  Après la migration, vous pouvez supprimer les fichiers originaux de `.claude/` pour éviter les doublons. La version du plugin aura la priorité quand elle est chargée.
</Note>

## Prochaines étapes

Maintenant que vous comprenez le système de plugins de Claude Code, voici les chemins suggérés pour différents objectifs :

### Pour les utilisateurs de plugins

* [Découvrir et installer des plugins](/fr/discover-plugins) : parcourir les marketplaces et installer des plugins
* [Configurer les marketplaces d'équipe](/fr/discover-plugins#configure-team-marketplaces) : configurer les plugins au niveau du référentiel pour votre équipe

### Pour les développeurs de plugins

* [Créer et distribuer une marketplace](/fr/plugin-marketplaces) : empaqueter et partager vos plugins
* [Référence des plugins](/fr/plugins-reference) : spécifications techniques complètes
* Approfondissez les composants spécifiques du plugin :
  * [Skills](/fr/skills) : détails du développement des skills
  * [Subagents](/fr/sub-agents) : configuration et capacités des agents
  * [Hooks](/fr/hooks) : gestion des événements et automatisation
  * [MCP](/fr/mcp) : intégration d'outils externes
