> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurer Claude Code

> Installez, authentifiez-vous et commencez à utiliser Claude Code sur votre machine de développement.

## Configuration requise

* **Système d'exploitation** :
  * macOS 13.0+
  * Windows 10 1809+ ou Windows Server 2019+ ([voir les notes de configuration](#platform-specific-setup))
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+ ([dépendances supplémentaires requises](#platform-specific-setup))
* **Matériel** : 4 Go+ de RAM
* **Réseau** : Connexion Internet requise (voir [configuration réseau](/fr/network-config#network-access-requirements))
* **Shell** : Fonctionne mieux avec Bash ou Zsh
* **Localisation** : [Pays supportés par Anthropic](https://www.anthropic.com/supported-countries)

### Dépendances supplémentaires

* **ripgrep** : Généralement inclus avec Claude Code. Si la recherche échoue, voir [dépannage de la recherche](/fr/troubleshooting#search-and-discovery-issues).
* **[Node.js 18+](https://nodejs.org/en/download)** : Requis uniquement pour [l'installation npm dépréciée](#npm-installation-deprecated)

## Installation

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

Une fois le processus d'installation terminé, accédez à votre projet et démarrez Claude Code :

```bash  theme={null}
cd your-awesome-project
claude
```

Si vous rencontrez des problèmes lors de l'installation, consultez le [guide de dépannage](/fr/troubleshooting).

<Tip>
  Exécutez `claude doctor` après l'installation pour vérifier votre type d'installation et votre version.
</Tip>

### Configuration spécifique à la plateforme

**Windows** : Exécutez Claude Code en mode natif (nécessite [Git Bash](https://git-scm.com/downloads/win)) ou dans WSL. WSL 1 et WSL 2 sont tous deux supportés, mais WSL 1 a un support limité et ne supporte pas les fonctionnalités comme le sandboxing de l'outil Bash.

**Alpine Linux et autres distributions basées sur musl/uClibc** :

Le programme d'installation natif sur Alpine et autres distributions basées sur musl/uClibc nécessite `libgcc`, `libstdc++` et `ripgrep`. Installez-les à l'aide du gestionnaire de paquets de votre distribution, puis définissez `USE_BUILTIN_RIPGREP=0`.

Sur Alpine :

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

### Authentification

#### Pour les particuliers

1. **Plan Claude Pro ou Max** (recommandé) : Abonnez-vous au [plan Pro ou Max](https://claude.ai/pricing) de Claude pour un abonnement unifié qui inclut à la fois Claude Code et Claude sur le web. Gérez votre compte en un seul endroit et connectez-vous avec votre compte Claude.ai.
2. **Claude Console** : Connectez-vous via la [Claude Console](https://console.anthropic.com) et complétez le processus OAuth. Nécessite une facturation active dans la Console Anthropic. Un espace de travail « Claude Code » est automatiquement créé pour le suivi de l'utilisation et la gestion des coûts. Vous ne pouvez pas créer de clés API pour l'espace de travail Claude Code ; il est dédié exclusivement à l'utilisation de Claude Code.

#### Pour les équipes et organisations

1. **Claude for Teams ou Enterprise** (recommandé) : Abonnez-vous à [Claude for Teams](https://claude.com/pricing#team-&-enterprise) ou [Claude for Enterprise](https://anthropic.com/contact-sales) pour une facturation centralisée, la gestion d'équipe et l'accès à la fois à Claude Code et Claude sur le web. Les membres de l'équipe se connectent avec leurs comptes Claude.ai.
2. **Claude Console avec facturation d'équipe** : Configurez une organisation [Claude Console](https://console.anthropic.com) partagée avec facturation d'équipe. Invitez les membres de l'équipe et attribuez des rôles pour le suivi de l'utilisation.
3. **Fournisseurs cloud** : Configurez Claude Code pour utiliser [Amazon Bedrock, Google Vertex AI ou Microsoft Foundry](/fr/third-party-integrations) pour les déploiements avec votre infrastructure cloud existante.

### Installer une version spécifique

Le programme d'installation natif accepte soit un numéro de version spécifique, soit un canal de version (`latest` ou `stable`). Le canal que vous choisissez au moment de l'installation devient votre canal par défaut pour les mises à jour automatiques. Voir [Configurer le canal de version](#configure-release-channel) pour plus d'informations.

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

### Intégrité binaire et signature de code

* Les sommes de contrôle SHA256 pour toutes les plateformes sont publiées dans les manifestes de version, actuellement situés à `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json` (exemple : remplacez `{VERSION}` par `2.0.30`)
* Les binaires signés sont distribués pour les plateformes suivantes :
  * macOS : Signé par ' Anthropic PBC ' et notarié par Apple
  * Windows : Signé par ' Anthropic, PBC '

## Installation NPM (dépréciée)

L'installation NPM est dépréciée. Utilisez la méthode [d'installation native](#installation) si possible. Pour migrer une installation npm existante vers la version native, exécutez `claude install`.

**Installation npm globale**

```sh  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  N'utilisez PAS `sudo npm install -g` car cela peut entraîner des problèmes de permissions et des risques de sécurité.
  Si vous rencontrez des erreurs de permission, voir [dépannage des erreurs de permission](/fr/troubleshooting#command-not-found-claude-or-permission-errors) pour les solutions recommandées.
</Warning>

## Configuration Windows

**Option 1 : Claude Code dans WSL**

* WSL 1 et WSL 2 sont tous deux supportés
* WSL 2 supporte le [sandboxing](/fr/sandboxing) pour une sécurité renforcée. WSL 1 ne supporte pas le sandboxing.

**Option 2 : Claude Code sur Windows natif avec Git Bash**

* Nécessite [Git for Windows](https://git-scm.com/downloads/win)
* Pour les installations Git portables, spécifiez le chemin vers votre `bash.exe` :
  ```powershell  theme={null}
  $env:CLAUDE_CODE_GIT_BASH_PATH="C:\Program Files\Git\bin\bash.exe"
  ```

## Mettre à jour Claude Code

### Mises à jour automatiques

Claude Code se met à jour automatiquement pour vous assurer que vous disposez des dernières fonctionnalités et correctifs de sécurité.

* **Vérifications de mise à jour** : Effectuées au démarrage et périodiquement pendant l'exécution
* **Processus de mise à jour** : Télécharge et installe automatiquement en arrière-plan
* **Notifications** : Vous verrez une notification lorsque les mises à jour sont installées
* **Application des mises à jour** : Les mises à jour prennent effet la prochaine fois que vous démarrez Claude Code

<Note>
  Les installations Homebrew et WinGet ne se mettent pas à jour automatiquement. Utilisez `brew upgrade claude-code` ou `winget upgrade Anthropic.ClaudeCode` pour mettre à jour manuellement.

  **Problème connu :** Claude Code peut vous notifier des mises à jour avant que la nouvelle version soit disponible dans ces gestionnaires de paquets. Si une mise à niveau échoue, attendez et réessayez plus tard.
</Note>

### Configurer le canal de version

Configurez le canal de version que Claude Code suit pour les mises à jour automatiques et `claude update` avec le paramètre `autoUpdatesChannel` :

* `"latest"` (par défaut) : Recevez les nouvelles fonctionnalités dès qu'elles sont publiées
* `"stable"` : Utilisez une version qui a généralement environ une semaine, en ignorant les versions avec des régressions majeures

Configurez ceci via `/config` → **Canal de mise à jour automatique**, ou ajoutez-le à votre [fichier settings.json](/fr/settings) :

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Pour les déploiements d'entreprise, vous pouvez appliquer un canal de version cohérent dans votre organisation en utilisant les [paramètres gérés](/fr/settings#settings-files).

### Désactiver les mises à jour automatiques

Définissez la variable d'environnement `DISABLE_AUTOUPDATER` dans votre shell ou [fichier settings.json](/fr/settings) :

```bash  theme={null}
export DISABLE_AUTOUPDATER=1
```

### Mettre à jour manuellement

```bash  theme={null}
claude update
```

## Désinstaller Claude Code

Si vous devez désinstaller Claude Code, suivez les instructions pour votre méthode d'installation.

### Installation native

Supprimez le binaire Claude Code et les fichiers de version :

**macOS, Linux, WSL :**

```bash  theme={null}
rm -f ~/.local/bin/claude
rm -rf ~/.local/share/claude
```

**Windows PowerShell :**

```powershell  theme={null}
Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
```

**Windows CMD :**

```batch  theme={null}
del "%USERPROFILE%\.local\bin\claude.exe"
rmdir /s /q "%USERPROFILE%\.local\share\claude"
```

### Installation Homebrew

```bash  theme={null}
brew uninstall --cask claude-code
```

### Installation WinGet

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### Installation NPM

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Nettoyer les fichiers de configuration (optionnel)

<Warning>
  La suppression des fichiers de configuration supprimera tous vos paramètres, outils autorisés, configurations de serveur MCP et l'historique de session.
</Warning>

Pour supprimer les paramètres et données en cache de Claude Code :

**macOS, Linux, WSL :**

```bash  theme={null}
# Supprimer les paramètres utilisateur et l'état
rm -rf ~/.claude
rm ~/.claude.json

# Supprimer les paramètres spécifiques au projet (exécutez depuis votre répertoire de projet)
rm -rf .claude
rm -f .mcp.json
```

**Windows PowerShell :**

```powershell  theme={null}
# Supprimer les paramètres utilisateur et l'état
Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

# Supprimer les paramètres spécifiques au projet (exécutez depuis votre répertoire de projet)
Remove-Item -Path ".claude" -Recurse -Force
Remove-Item -Path ".mcp.json" -Force
```

**Windows CMD :**

```batch  theme={null}
REM Supprimer les paramètres utilisateur et l'état
rmdir /s /q "%USERPROFILE%\.claude"
del "%USERPROFILE%\.claude.json"

REM Supprimer les paramètres spécifiques au projet (exécutez depuis votre répertoire de projet)
rmdir /s /q ".claude"
del ".mcp.json"
```
