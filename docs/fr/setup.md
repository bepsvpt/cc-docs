> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuration avancée

> Configuration requise, installation spécifique à la plateforme, gestion des versions et désinstallation pour Claude Code.

Cette page couvre la configuration requise, les détails d'installation spécifiques à la plateforme, les mises à jour et la désinstallation. Pour une présentation guidée de votre première session, consultez le [démarrage rapide](/fr/quickstart). Si vous n'avez jamais utilisé un terminal auparavant, consultez le [guide du terminal](/fr/terminal-guide).

## Configuration requise

Claude Code s'exécute sur les plateformes et configurations suivantes :

* **Système d'exploitation** :
  * macOS 13.0+
  * Windows 10 1809+ ou Windows Server 2019+
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+
* **Matériel** : 4 Go+ de RAM
* **Réseau** : connexion Internet requise. Consultez la [configuration réseau](/fr/network-config#network-access-requirements).
* **Shell** : Bash, Zsh, PowerShell ou CMD. Sur Windows, [Git for Windows](https://git-scm.com/downloads/win) est requis.
* **Localisation** : [pays supportés par Anthropic](https://www.anthropic.com/supported-countries)

### Dépendances supplémentaires

* **ripgrep** : généralement inclus avec Claude Code. Si la recherche échoue, consultez le [dépannage de la recherche](/fr/troubleshooting#search-and-discovery-issues).

## Installer Claude Code

<Tip>
  Préférez une interface graphique ? L'[application de bureau](/fr/desktop-quickstart) vous permet d'utiliser Claude Code sans le terminal. Téléchargez-la pour [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) ou [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs).

  Nouveau sur le terminal ? Consultez le [guide du terminal](/fr/terminal-guide) pour des instructions étape par étape.
</Tip>

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell  theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

Une fois l'installation terminée, ouvrez un terminal dans le projet sur lequel vous souhaitez travailler et démarrez Claude Code :

```bash  theme={null}
claude
```

Si vous rencontrez des problèmes lors de l'installation, consultez le [guide de dépannage](/fr/troubleshooting).

### Configuration sur Windows

Claude Code sur Windows nécessite [Git for Windows](https://git-scm.com/downloads/win) ou WSL. Vous pouvez lancer `claude` à partir de PowerShell, CMD ou Git Bash. Claude Code utilise Git Bash en interne pour exécuter les commandes. Vous n'avez pas besoin d'exécuter PowerShell en tant qu'administrateur.

**Option 1 : Windows natif avec Git Bash**

Installez [Git for Windows](https://git-scm.com/downloads/win), puis exécutez la commande d'installation à partir de PowerShell ou CMD.

Si Claude Code ne trouve pas votre installation de Git Bash, définissez le chemin dans votre [fichier settings.json](/fr/settings) :

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

**Option 2 : WSL**

WSL 1 et WSL 2 sont tous deux supportés. WSL 2 supporte le [sandboxing](/fr/sandboxing) pour une sécurité renforcée. WSL 1 ne supporte pas le sandboxing.

### Alpine Linux et distributions basées sur musl

L'installateur natif sur Alpine et autres distributions basées sur musl/uClibc nécessite `libgcc`, `libstdc++` et `ripgrep`. Installez-les à l'aide du gestionnaire de paquets de votre distribution, puis définissez `USE_BUILTIN_RIPGREP=0`.

Cet exemple installe les paquets requis sur Alpine :

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

Ensuite, définissez `USE_BUILTIN_RIPGREP` à `0` dans votre fichier [`settings.json`](/fr/settings#available-settings) :

```json  theme={null}
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

## Vérifier votre installation

Après l'installation, confirmez que Claude Code fonctionne :

```bash  theme={null}
claude --version
```

Pour une vérification plus détaillée de votre installation et configuration, exécutez [`claude doctor`](/fr/troubleshooting#get-more-help) :

```bash  theme={null}
claude doctor
```

## S'authentifier

Claude Code nécessite un compte Pro, Max, Teams, Enterprise ou Console. Le plan gratuit Claude.ai n'inclut pas l'accès à Claude Code. Vous pouvez également utiliser Claude Code avec un fournisseur d'API tiers comme [Amazon Bedrock](/fr/amazon-bedrock), [Google Vertex AI](/fr/google-vertex-ai) ou [Microsoft Foundry](/fr/microsoft-foundry).

Après l'installation, connectez-vous en exécutant `claude` et en suivant les invites du navigateur. Consultez [Authentification](/fr/authentication) pour tous les types de comptes et les options de configuration d'équipe.

## Mettre à jour Claude Code

Les installations natives se mettent à jour automatiquement en arrière-plan. Vous pouvez [configurer le canal de version](#configure-release-channel) pour contrôler si vous recevez les mises à jour immédiatement ou selon un calendrier stable retardé, ou [désactiver les mises à jour automatiques](#disable-auto-updates) entièrement. Les installations Homebrew et WinGet nécessitent des mises à jour manuelles.

### Mises à jour automatiques

Claude Code vérifie les mises à jour au démarrage et périodiquement pendant l'exécution. Les mises à jour se téléchargent et s'installent en arrière-plan, puis prennent effet la prochaine fois que vous démarrez Claude Code.

<Note>
  Les installations Homebrew et WinGet ne se mettent pas à jour automatiquement. Utilisez `brew upgrade claude-code` ou `winget upgrade Anthropic.ClaudeCode` pour mettre à jour manuellement.

  **Problème connu :** Claude Code peut vous notifier des mises à jour avant que la nouvelle version soit disponible dans ces gestionnaires de paquets. Si une mise à niveau échoue, attendez et réessayez plus tard.

  Homebrew conserve les anciennes versions sur le disque après les mises à niveau. Exécutez `brew cleanup claude-code` périodiquement pour récupérer de l'espace disque.
</Note>

### Configurer le canal de version

Contrôlez le canal de version que Claude Code suit pour les mises à jour automatiques et `claude update` avec le paramètre `autoUpdatesChannel` :

* `"latest"`, la valeur par défaut : recevez les nouvelles fonctionnalités dès qu'elles sont publiées
* `"stable"` : utilisez une version qui a généralement environ une semaine, en ignorant les versions avec des régressions majeures

Configurez ceci via `/config` → **Canal de mise à jour automatique**, ou ajoutez-le à votre [fichier settings.json](/fr/settings) :

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Pour les déploiements d'entreprise, vous pouvez appliquer un canal de version cohérent dans votre organisation à l'aide des [paramètres gérés](/fr/permissions#managed-settings).

### Désactiver les mises à jour automatiques

Définissez `DISABLE_AUTOUPDATER` à `"1"` dans la clé `env` de votre fichier [`settings.json`](/fr/settings#available-settings) :

```json  theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

### Mettre à jour manuellement

Pour appliquer une mise à jour immédiatement sans attendre la prochaine vérification en arrière-plan, exécutez :

```bash  theme={null}
claude update
```

## Options d'installation avancées

Ces options sont destinées à l'épinglage de version, à la migration depuis npm et à la vérification de l'intégrité des binaires.

### Installer une version spécifique

L'installateur natif accepte soit un numéro de version spécifique, soit un canal de version (`latest` ou `stable`). Le canal que vous choisissez au moment de l'installation devient votre valeur par défaut pour les mises à jour automatiques. Consultez [configurer le canal de version](#configure-release-channel) pour plus d'informations.

Pour installer la dernière version (par défaut) :

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
  </Tab>
</Tabs>

Pour installer la version stable :

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s stable
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
    ```
  </Tab>
</Tabs>

Pour installer un numéro de version spécifique :

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 1.0.58 && del install.cmd
    ```
  </Tab>
</Tabs>

### Installation npm dépréciée

L'installation npm est dépréciée. L'installateur natif est plus rapide, ne nécessite aucune dépendance et se met à jour automatiquement en arrière-plan. Utilisez la méthode [d'installation native](#install-claude-code) si possible.

#### Migrer de npm vers natif

Si vous avez précédemment installé Claude Code avec npm, passez à l'installateur natif :

```bash  theme={null}
# Installer le binaire natif
curl -fsSL https://claude.ai/install.sh | bash

# Supprimer l'ancienne installation npm
npm uninstall -g @anthropic-ai/claude-code
```

Vous pouvez également exécuter `claude install` à partir d'une installation npm existante pour installer le binaire natif à côté, puis supprimer la version npm.

#### Installer avec npm

Si vous avez besoin de l'installation npm pour des raisons de compatibilité, vous devez avoir [Node.js 18+](https://nodejs.org/en/download) installé. Installez le paquet globalement :

```bash  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  N'utilisez PAS `sudo npm install -g` car cela peut entraîner des problèmes de permissions et des risques de sécurité. Si vous rencontrez des erreurs de permissions, consultez le [dépannage des erreurs de permissions](/fr/troubleshooting#permission-errors-during-installation).
</Warning>

### Intégrité des binaires et signature du code

Vous pouvez vérifier l'intégrité des binaires Claude Code à l'aide des sommes de contrôle SHA256 et des signatures de code.

* Les sommes de contrôle SHA256 pour toutes les plateformes sont publiées dans les manifestes de version à `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json`. Remplacez `{VERSION}` par un numéro de version tel que `2.0.30`.
* Les binaires signés sont distribués pour les plateformes suivantes :
  * **macOS** : signé par ' Anthropic PBC ' et notarié par Apple
  * **Windows** : signé par ' Anthropic, PBC '

## Désinstaller Claude Code

Pour supprimer Claude Code, suivez les instructions correspondant à votre méthode d'installation.

### Installation native

Supprimez le binaire Claude Code et les fichiers de version :

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    rm -f ~/.local/bin/claude
    rm -rf ~/.local/share/claude
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
    Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
    ```
  </Tab>
</Tabs>

### Installation Homebrew

Supprimez le cask Homebrew :

```bash  theme={null}
brew uninstall --cask claude-code
```

### Installation WinGet

Supprimez le paquet WinGet :

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### npm

Supprimez le paquet npm global :

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Supprimer les fichiers de configuration

<Warning>
  La suppression des fichiers de configuration supprimera tous vos paramètres, outils autorisés, configurations de serveur MCP et historique de session.
</Warning>

Pour supprimer les paramètres et données en cache de Claude Code :

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    # Supprimer les paramètres utilisateur et l'état
    rm -rf ~/.claude
    rm ~/.claude.json

    # Supprimer les paramètres spécifiques au projet (exécutez depuis votre répertoire de projet)
    rm -rf .claude
    rm -f .mcp.json
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    # Supprimer les paramètres utilisateur et l'état
    Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
    Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

    # Supprimer les paramètres spécifiques au projet (exécutez depuis votre répertoire de projet)
    Remove-Item -Path ".claude" -Recurse -Force
    Remove-Item -Path ".mcp.json" -Force
    ```
  </Tab>
</Tabs>
