> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Dépannage

> Découvrez les solutions aux problèmes courants liés à l'installation et l'utilisation de Claude Code.

## Dépanner les problèmes d'installation

<Tip>
  Si vous préférez éviter le terminal, l'[application Claude Code Desktop](/fr/desktop-quickstart) vous permet d'installer et d'utiliser Claude Code via une interface graphique. Téléchargez-la pour [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) ou [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) et commencez à coder sans aucune configuration en ligne de commande.
</Tip>

Trouvez le message d'erreur ou le symptôme que vous rencontrez :

| Ce que vous voyez                                                                | Solution                                                                                                                    |
| :------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------- |
| `command not found: claude` ou `'claude' is not recognized`                      | [Corriger votre PATH](#command-not-found-claude-after-installation)                                                         |
| `syntax error near unexpected token '<'`                                         | [Le script d'installation retourne du HTML](#install-script-returns-html-instead-of-a-shell-script)                         |
| `curl: (56) Failure writing output to destination`                               | [Télécharger le script d'abord, puis l'exécuter](#curl-56-failure-writing-output-to-destination)                            |
| `Killed` pendant l'installation sur Linux                                        | [Ajouter de l'espace d'échange pour les serveurs à faible mémoire](#install-killed-on-low-memory-linux-servers)             |
| `TLS connect error` ou `SSL/TLS secure channel`                                  | [Mettre à jour les certificats CA](#tls-or-ssl-connection-errors)                                                           |
| `Failed to fetch version` ou impossible d'atteindre le serveur de téléchargement | [Vérifier la connectivité réseau et les paramètres proxy](#check-network-connectivity)                                      |
| `irm is not recognized` ou `&& is not valid`                                     | [Utiliser la bonne commande pour votre shell](#windows-irm-or--not-recognized)                                              |
| `Claude Code on Windows requires git-bash`                                       | [Installer ou configurer Git Bash](#windows-claude-code-on-windows-requires-git-bash)                                       |
| `Error loading shared library`                                                   | [Mauvaise variante binaire pour votre système](#linux-wrong-binary-variant-installed-muslglibc-mismatch)                    |
| `Illegal instruction` sur Linux                                                  | [Incompatibilité d'architecture](#illegal-instruction-on-linux)                                                             |
| `dyld: cannot load` ou `Abort trap` sur macOS                                    | [Incompatibilité binaire](#dyld-cannot-load-on-macos)                                                                       |
| `Invoke-Expression: Missing argument in parameter list`                          | [Le script d'installation retourne du HTML](#install-script-returns-html-instead-of-a-shell-script)                         |
| `App unavailable in region`                                                      | Claude Code n'est pas disponible dans votre pays. Voir les [pays supportés](https://www.anthropic.com/supported-countries). |
| `unable to get local issuer certificate`                                         | [Configurer les certificats CA d'entreprise](#tls-or-ssl-connection-errors)                                                 |
| `OAuth error` ou `403 Forbidden`                                                 | [Corriger l'authentification](#authentication-issues)                                                                       |

Si votre problème n'est pas listé, suivez ces étapes de diagnostic.

## Déboguer les problèmes d'installation

### Vérifier la connectivité réseau

L'installateur télécharge depuis `storage.googleapis.com`. Vérifiez que vous pouvez l'atteindre :

```bash  theme={null}
curl -sI https://storage.googleapis.com
```

Si cela échoue, votre réseau bloque peut-être la connexion. Les causes courantes incluent :

* Les pare-feu d'entreprise ou les proxies bloquant Google Cloud Storage
* Les restrictions réseau régionales : essayez un VPN ou un réseau alternatif
* Les problèmes TLS/SSL : mettez à jour les certificats CA de votre système, ou vérifiez si `HTTPS_PROXY` est configuré

Si vous êtes derrière un proxy d'entreprise, définissez `HTTPS_PROXY` et `HTTP_PROXY` à l'adresse de votre proxy avant d'installer. Demandez à votre équipe informatique l'URL du proxy si vous ne la connaissez pas, ou vérifiez les paramètres proxy de votre navigateur.

Cet exemple définit les deux variables proxy, puis exécute l'installateur via votre proxy :

```bash  theme={null}
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
curl -fsSL https://claude.ai/install.sh | bash
```

### Vérifier votre PATH

Si l'installation a réussi mais que vous obtenez une erreur `command not found` ou `not recognized` lors de l'exécution de `claude`, le répertoire d'installation n'est pas dans votre PATH. Votre shell recherche les programmes dans les répertoires listés dans PATH, et l'installateur place `claude` à `~/.local/bin/claude` sur macOS/Linux ou `%USERPROFILE%\.local\bin\claude.exe` sur Windows.

Vérifiez si le répertoire d'installation est dans votre PATH en listant vos entrées PATH et en filtrant pour `local/bin` :

<Tabs>
  <Tab title="macOS/Linux">
    ```bash  theme={null}
    echo $PATH | tr ':' '\n' | grep local/bin
    ```

    S'il n'y a pas de sortie, le répertoire est manquant. Ajoutez-le à votre configuration shell :

    ```bash  theme={null}
    # Zsh (macOS par défaut)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc

    # Bash (Linux par défaut)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```

    Sinon, fermez et rouvrez votre terminal.

    Vérifiez que la correction a fonctionné :

    ```bash  theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    $env:PATH -split ';' | Select-String 'local\\bin'
    ```

    S'il n'y a pas de sortie, ajoutez le répertoire d'installation à votre PATH utilisateur :

    ```powershell  theme={null}
    $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
    [Environment]::SetEnvironmentVariable('PATH', "$currentPath;$env:USERPROFILE\.local\bin", 'User')
    ```

    Redémarrez votre terminal pour que la modification prenne effet.

    Vérifiez que la correction a fonctionné :

    ```powershell  theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    echo %PATH% | findstr /i "local\bin"
    ```

    S'il n'y a pas de sortie, ouvrez les Paramètres système, allez à Variables d'environnement, et ajoutez `%USERPROFILE%\.local\bin` à votre variable PATH utilisateur. Redémarrez votre terminal.

    Vérifiez que la correction a fonctionné :

    ```batch  theme={null}
    claude --version
    ```
  </Tab>
</Tabs>

### Vérifier les installations conflictuelles

Plusieurs installations de Claude Code peuvent causer des incompatibilités de version ou un comportement inattendu. Vérifiez ce qui est installé :

<Tabs>
  <Tab title="macOS/Linux">
    Listez tous les binaires `claude` trouvés dans votre PATH :

    ```bash  theme={null}
    which -a claude
    ```

    Vérifiez si les versions de l'installateur natif et npm sont présentes :

    ```bash  theme={null}
    ls -la ~/.local/bin/claude
    ```

    ```bash  theme={null}
    ls -la ~/.claude/local/
    ```

    ```bash  theme={null}
    npm -g ls @anthropic-ai/claude-code 2>/dev/null
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    where.exe claude
    Test-Path "$env:LOCALAPPDATA\Claude Code\claude.exe"
    ```
  </Tab>
</Tabs>

Si vous trouvez plusieurs installations, conservez-en une seule. L'installation native à `~/.local/bin/claude` est recommandée. Supprimez les installations supplémentaires :

Désinstallez une installation npm globale :

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

Supprimez une installation Homebrew sur macOS :

```bash  theme={null}
brew uninstall --cask claude-code
```

### Vérifier les permissions des répertoires

L'installateur a besoin d'accès en écriture à `~/.local/bin/` et `~/.claude/`. Si l'installation échoue avec des erreurs de permission, vérifiez si ces répertoires sont accessibles en écriture :

```bash  theme={null}
test -w ~/.local/bin && echo "writable" || echo "not writable"
test -w ~/.claude && echo "writable" || echo "not writable"
```

Si l'un des répertoires n'est pas accessible en écriture, créez le répertoire d'installation et définissez votre utilisateur comme propriétaire :

```bash  theme={null}
sudo mkdir -p ~/.local/bin
sudo chown -R $(whoami) ~/.local
```

### Vérifier que le binaire fonctionne

Si `claude` est installé mais plante ou se fige au démarrage, exécutez ces vérifications pour réduire la cause.

Confirmez que le binaire existe et est exécutable :

```bash  theme={null}
ls -la $(which claude)
```

Sur Linux, vérifiez les bibliothèques partagées manquantes. Si `ldd` affiche des bibliothèques manquantes, vous devrez peut-être installer des paquets système. Sur Alpine Linux et autres distributions basées sur musl, voir [Configuration Alpine Linux](/fr/setup#alpine-linux-and-musl-based-distributions).

```bash  theme={null}
ldd $(which claude) | grep "not found"
```

Exécutez une vérification rapide que le binaire peut s'exécuter :

```bash  theme={null}
claude --version
```

## Problèmes d'installation courants

Ce sont les problèmes d'installation les plus fréquemment rencontrés et leurs solutions.

### Le script d'installation retourne du HTML au lieu d'un script shell

Lors de l'exécution de la commande d'installation, vous pouvez voir l'une de ces erreurs :

```text  theme={null}
bash: line 1: syntax error near unexpected token `<'
bash: line 1: `<!DOCTYPE html>'
```

Sur PowerShell, le même problème apparaît comme :

```text  theme={null}
Invoke-Expression: Missing argument in parameter list.
```

Cela signifie que l'URL d'installation a retourné une page HTML au lieu du script d'installation. Si la page HTML dit « App unavailable in region », Claude Code n'est pas disponible dans votre pays. Voir les [pays supportés](https://www.anthropic.com/supported-countries).

Sinon, cela peut se produire en raison de problèmes réseau, de routage régional, ou d'une interruption de service temporaire.

**Solutions :**

1. **Utiliser une méthode d'installation alternative** :

   Sur macOS ou Linux, installez via Homebrew :

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   Sur Windows, installez via WinGet :

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

2. **Réessayez après quelques minutes** : le problème est souvent temporaire. Attendez et réessayez la commande originale.

### `command not found: claude` après l'installation

L'installation s'est terminée mais `claude` ne fonctionne pas. L'erreur exacte varie selon la plateforme :

| Plateforme  | Message d'erreur                                                       |
| :---------- | :--------------------------------------------------------------------- |
| macOS       | `zsh: command not found: claude`                                       |
| Linux       | `bash: claude: command not found`                                      |
| Windows CMD | `'claude' is not recognized as an internal or external command`        |
| PowerShell  | `claude : The term 'claude' is not recognized as the name of a cmdlet` |

Cela signifie que le répertoire d'installation n'est pas dans le chemin de recherche de votre shell. Voir [Vérifier votre PATH](#verify-your-path) pour la correction sur chaque plateforme.

### `curl: (56) Failure writing output to destination`

La commande `curl ... | bash` télécharge le script et le transmet directement à Bash pour exécution en utilisant un pipe (`|`). Cette erreur signifie que la connexion s'est interrompue avant que le script ne soit complètement téléchargé. Les causes courantes incluent les interruptions réseau, le téléchargement étant bloqué en cours de flux, ou les limites de ressources système.

**Solutions :**

1. **Vérifier la stabilité du réseau** : les binaires Claude Code sont hébergés sur Google Cloud Storage. Testez que vous pouvez l'atteindre :
   ```bash  theme={null}
   curl -fsSL https://storage.googleapis.com -o /dev/null
   ```
   Si la commande se termine silencieusement, votre connexion est correcte et le problème est probablement intermittent. Réessayez la commande d'installation. Si vous voyez une erreur, votre réseau bloque peut-être le téléchargement.

2. **Essayez une méthode d'installation alternative** :

   Sur macOS ou Linux :

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   Sur Windows :

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

### Erreurs de connexion TLS ou SSL

Les erreurs comme `curl: (35) TLS connect error`, `schannel: next InitializeSecurityContext failed`, ou le `Could not establish trust relationship for the SSL/TLS secure channel` de PowerShell indiquent des échecs de négociation TLS.

**Solutions :**

1. **Mettre à jour vos certificats CA système** :

   Sur Ubuntu/Debian :

   ```bash  theme={null}
   sudo apt-get update && sudo apt-get install ca-certificates
   ```

   Sur macOS via Homebrew :

   ```bash  theme={null}
   brew install ca-certificates
   ```

2. **Sur Windows, activez TLS 1.2** dans PowerShell avant d'exécuter l'installateur :
   ```powershell  theme={null}
   [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
   irm https://claude.ai/install.ps1 | iex
   ```

3. **Vérifiez l'interférence du proxy ou du pare-feu** : les proxies d'entreprise qui effectuent l'inspection TLS peuvent causer ces erreurs, y compris `unable to get local issuer certificate`. Définissez `NODE_EXTRA_CA_CERTS` sur votre bundle de certificat CA d'entreprise :
   ```bash  theme={null}
   export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca.pem
   ```
   Demandez à votre équipe informatique le fichier de certificat si vous ne l'avez pas. Vous pouvez également essayer sur une connexion directe pour confirmer que le proxy est la cause.

### `Failed to fetch version from storage.googleapis.com`

L'installateur n'a pas pu atteindre le serveur de téléchargement. Cela signifie généralement que `storage.googleapis.com` est bloqué sur votre réseau.

**Solutions :**

1. **Testez la connectivité directement** :
   ```bash  theme={null}
   curl -sI https://storage.googleapis.com
   ```

2. **Si derrière un proxy**, définissez `HTTPS_PROXY` pour que l'installateur puisse le router. Voir [configuration du proxy](/fr/network-config#proxy-configuration) pour les détails.
   ```bash  theme={null}
   export HTTPS_PROXY=http://proxy.example.com:8080
   curl -fsSL https://claude.ai/install.sh | bash
   ```

3. **Si sur un réseau restreint**, essayez un réseau différent ou un VPN, ou utilisez une méthode d'installation alternative :

   Sur macOS ou Linux :

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   Sur Windows :

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

### Windows : `irm` ou `&&` non reconnu

Si vous voyez `'irm' is not recognized` ou `The token '&&' is not valid`, vous exécutez la mauvaise commande pour votre shell.

* **`irm` non reconnu** : vous êtes dans CMD, pas PowerShell. Vous avez deux options :

  Ouvrez PowerShell en recherchant « PowerShell » dans le menu Démarrer, puis exécutez la commande d'installation originale :

  ```powershell  theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

  Ou restez dans CMD et utilisez l'installateur CMD à la place :

  ```batch  theme={null}
  curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
  ```

* **`&&` non valide** : vous êtes dans PowerShell mais avez exécuté la commande d'installateur CMD. Utilisez l'installateur PowerShell :
  ```powershell  theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

### Installation tuée sur les serveurs Linux à faible mémoire

Si vous voyez `Killed` pendant l'installation sur un VPS ou une instance cloud :

```text  theme={null}
Setting up Claude Code...
Installing Claude Code native build latest...
bash: line 142: 34803 Killed    "$binary_path" install ${TARGET:+"$TARGET"}
```

Le tueur OOM Linux a terminé le processus car le système a manqué de mémoire. Claude Code nécessite au moins 4 Go de RAM disponible.

**Solutions :**

1. **Ajouter de l'espace d'échange** si votre serveur a une RAM limitée. L'échange utilise l'espace disque comme mémoire de débordement, permettant à l'installation de se terminer même avec une RAM physique faible.

   Créez un fichier d'échange de 2 Go et activez-le :

   ```bash  theme={null}
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

   Puis réessayez l'installation :

   ```bash  theme={null}
   curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **Fermez les autres processus** pour libérer de la mémoire avant d'installer.

3. **Utilisez une instance plus grande** si possible. Claude Code nécessite au moins 4 Go de RAM.

### L'installation se fige dans Docker

Lors de l'installation de Claude Code dans un conteneur Docker, l'installation en tant que root dans `/` peut causer des blocages.

**Solutions :**

1. **Définir un répertoire de travail** avant d'exécuter l'installateur. Lorsqu'il est exécuté depuis `/`, l'installateur analyse l'ensemble du système de fichiers, ce qui provoque une utilisation excessive de la mémoire. La définition de `WORKDIR` limite l'analyse à un petit répertoire :
   ```dockerfile  theme={null}
   WORKDIR /tmp
   RUN curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **Augmentez les limites de mémoire Docker** si vous utilisez Docker Desktop :
   ```bash  theme={null}
   docker build --memory=4g .
   ```

### Windows : Claude Desktop remplace la commande CLI `claude`

Si vous avez installé une version antérieure de Claude Desktop, elle peut enregistrer un `Claude.exe` dans le répertoire `WindowsApps` qui prend la priorité PATH sur Claude Code CLI. L'exécution de `claude` ouvre l'application Desktop au lieu de la CLI.

Mettez à jour Claude Desktop vers la dernière version pour corriger ce problème.

### Windows : « Claude Code on Windows requires git-bash »

Claude Code sur Windows natif a besoin de [Git for Windows](https://git-scm.com/downloads/win), qui inclut Git Bash.

**Si Git n'est pas installé**, téléchargez et installez-le depuis [git-scm.com/downloads/win](https://git-scm.com/downloads/win). Pendant la configuration, sélectionnez « Add to PATH ». Redémarrez votre terminal après l'installation.

**Si Git est déjà installé** mais Claude Code ne peut toujours pas le trouver, définissez le chemin dans votre [fichier settings.json](/fr/settings) :

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

Si votre Git est installé ailleurs, trouvez le chemin en exécutant `where.exe git` dans PowerShell et utilisez le chemin `bin\bash.exe` de ce répertoire.

### Linux : mauvaise variante binaire installée (incompatibilité musl/glibc)

Si vous voyez des erreurs concernant des bibliothèques partagées manquantes comme `libstdc++.so.6` ou `libgcc_s.so.1` après l'installation, l'installateur a peut-être téléchargé la mauvaise variante binaire pour votre système.

```text  theme={null}
Error loading shared library libstdc++.so.6: No such file or directory
```

Cela peut se produire sur les systèmes basés sur glibc qui ont des paquets de compilation croisée musl installés, ce qui amène l'installateur à mal détecter le système comme musl.

**Solutions :**

1. **Vérifiez quelle libc votre système utilise** :
   ```bash  theme={null}
   ldd /bin/ls | head -1
   ```
   S'il affiche `linux-vdso.so` ou des références à `/lib/x86_64-linux-gnu/`, vous êtes sur glibc. S'il affiche `musl`, vous êtes sur musl.

2. **Si vous êtes sur glibc mais avez obtenu le binaire musl**, supprimez l'installation et réinstallez. Vous pouvez également télécharger manuellement le binaire correct depuis le bucket GCS à `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json`. Déposez un [problème GitHub](https://github.com/anthropics/claude-code/issues) avec la sortie de `ldd /bin/ls` et `ls /lib/libc.musl*`.

3. **Si vous êtes réellement sur musl** (Alpine Linux), installez les paquets requis :
   ```bash  theme={null}
   apk add libgcc libstdc++ ripgrep
   ```

### `Illegal instruction` sur Linux

Si l'installateur affiche `Illegal instruction` au lieu du message `Killed` OOM, le binaire téléchargé ne correspond pas à l'architecture de votre CPU. Cela se produit couramment sur les serveurs ARM qui reçoivent un binaire x86, ou sur les anciens CPU qui manquent d'ensembles d'instructions requis.

```text  theme={null}
bash: line 142: 2238232 Illegal instruction    "$binary_path" install ${TARGET:+"$TARGET"}
```

**Solutions :**

1. **Vérifiez votre architecture** :
   ```bash  theme={null}
   uname -m
   ```
   `x86_64` signifie 64 bits Intel/AMD, `aarch64` signifie ARM64. Si le binaire ne correspond pas, [déposez un problème GitHub](https://github.com/anthropics/claude-code/issues) avec la sortie.

2. **Essayez une méthode d'installation alternative** pendant que le problème d'architecture est résolu :
   ```bash  theme={null}
   brew install --cask claude-code
   ```

### `dyld: cannot load` sur macOS

Si vous voyez `dyld: cannot load` ou `Abort trap: 6` pendant l'installation, le binaire est incompatible avec votre version ou matériel macOS.

```text  theme={null}
dyld: cannot load 'claude-2.1.42-darwin-x64' (load command 0x80000034 is unknown)
Abort trap: 6
```

**Solutions :**

1. **Vérifiez votre version macOS** : Claude Code nécessite macOS 13.0 ou ultérieur. Ouvrez le menu Apple et sélectionnez À propos de ce Mac pour vérifier votre version.

2. **Mettez à jour macOS** si vous êtes sur une version antérieure. Le binaire utilise des commandes de chargement que les versions macOS antérieures ne supportent pas.

3. **Essayez Homebrew** comme méthode d'installation alternative :
   ```bash  theme={null}
   brew install --cask claude-code
   ```

### Problèmes d'installation Windows : erreurs dans WSL

Vous pourriez rencontrer les problèmes suivants dans WSL :

**Problèmes de détection d'OS/plateforme** : si vous recevez une erreur pendant l'installation, WSL peut utiliser npm Windows. Essayez :

* Exécutez `npm config set os linux` avant l'installation
* Installez avec `npm install -g @anthropic-ai/claude-code --force --no-os-check`. N'utilisez pas `sudo`.

**Erreurs Node non trouvé** : si vous voyez `exec: node: not found` lors de l'exécution de `claude`, votre environnement WSL peut utiliser une installation Windows de Node.js. Vous pouvez confirmer cela avec `which npm` et `which node`, qui devraient pointer vers des chemins Linux commençant par `/usr/` plutôt que `/mnt/c/`. Pour corriger cela, essayez d'installer Node via le gestionnaire de paquets de votre distribution Linux ou via [`nvm`](https://github.com/nvm-sh/nvm).

**Conflits de version nvm** : si vous avez nvm installé à la fois dans WSL et Windows, vous pouvez rencontrer des conflits de version lors du changement de versions Node dans WSL. Cela se produit car WSL importe le PATH Windows par défaut, ce qui amène Windows nvm/npm à prendre la priorité sur l'installation WSL.

Vous pouvez identifier ce problème par :

* L'exécution de `which npm` et `which node` - s'ils pointent vers des chemins Windows (commençant par `/mnt/c/`), les versions Windows sont utilisées
* L'expérience de fonctionnalités cassées après le changement de versions Node avec nvm dans WSL

Pour résoudre ce problème, corrigez votre PATH Linux pour assurer que les versions Linux node/npm prennent la priorité :

**Solution principale : Assurez-vous que nvm est correctement chargé dans votre shell**

La cause la plus courante est que nvm n'est pas chargé dans les shells non interactifs. Ajoutez ce qui suit à votre fichier de configuration shell (`~/.bashrc`, `~/.zshrc`, etc.) :

```bash  theme={null}
# Charger nvm s'il existe
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

Ou exécutez directement dans votre session actuelle :

```bash  theme={null}
source ~/.nvm/nvm.sh
```

**Alternative : Ajuster l'ordre du PATH**

Si nvm est correctement chargé mais que les chemins Windows prennent toujours la priorité, vous pouvez explicitement préfixer vos chemins Linux au PATH dans votre configuration shell :

```bash  theme={null}
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

<Warning>
  Évitez de désactiver l'importation du PATH Windows via `appendWindowsPath = false` car cela casse la capacité d'appeler les exécutables Windows depuis WSL. De même, évitez de désinstaller Node.js de Windows si vous l'utilisez pour le développement Windows.
</Warning>

### Configuration du sandbox WSL2

Le [sandboxing](/fr/sandboxing) est supporté sur WSL2 mais nécessite l'installation de paquets supplémentaires. Si vous voyez une erreur comme « Sandbox requires socat and bubblewrap » lors de l'exécution de `/sandbox`, installez les dépendances :

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash  theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash  theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

WSL1 ne supporte pas le sandboxing. Si vous voyez « Sandboxing requires WSL2 », vous devez mettre à niveau vers WSL2 ou exécuter Claude Code sans sandboxing.

### Erreurs de permission pendant l'installation

Si l'installateur natif échoue avec des erreurs de permission, le répertoire cible peut ne pas être accessible en écriture. Voir [Vérifier les permissions des répertoires](#check-directory-permissions).

Si vous avez précédemment installé avec npm et rencontrez des erreurs de permission spécifiques à npm, passez à l'installateur natif :

```bash  theme={null}
curl -fsSL https://claude.ai/install.sh | bash
```

## Permissions et authentification

Ces sections traitent des échecs de connexion, des problèmes de jetons et du comportement des invites de permission.

### Invites de permission répétées

Si vous vous trouvez à approuver à plusieurs reprises les mêmes commandes, vous pouvez autoriser des outils spécifiques à s'exécuter sans approbation en utilisant la commande `/permissions`. Voir la [documentation Permissions](/fr/permissions#manage-permissions).

### Problèmes d'authentification

Si vous rencontrez des problèmes d'authentification :

1. Exécutez `/logout` pour vous déconnecter complètement
2. Fermez Claude Code
3. Redémarrez avec `claude` et complétez le processus d'authentification à nouveau

Si le navigateur ne s'ouvre pas automatiquement pendant la connexion, appuyez sur `c` pour copier l'URL OAuth dans votre presse-papiers, puis collez-la dans votre navigateur manuellement.

### Erreur OAuth : Code invalide

Si vous voyez `OAuth error: Invalid code. Please make sure the full code was copied`, le code de connexion a expiré ou a été tronqué lors du copier-coller.

**Solutions :**

* Appuyez sur Entrée pour réessayer et complétez la connexion rapidement après l'ouverture du navigateur
* Tapez `c` pour copier l'URL complète si le navigateur ne s'ouvre pas automatiquement
* Si vous utilisez une session distante/SSH, le navigateur peut s'ouvrir sur la mauvaise machine. Copiez l'URL affichée dans le terminal et ouvrez-la dans votre navigateur local à la place.

### 403 Forbidden après la connexion

Si vous voyez `API Error: 403 {"error":{"type":"forbidden","message":"Request not allowed"}}` après la connexion :

* **Utilisateurs Claude Pro/Max** : vérifiez que votre abonnement est actif sur [claude.ai/settings](https://claude.ai/settings)
* **Utilisateurs Console** : confirmez que votre compte a le rôle « Claude Code » ou « Developer » assigné par votre administrateur
* **Derrière un proxy** : les proxies d'entreprise peuvent interférer avec les requêtes API. Voir [configuration réseau](/fr/network-config) pour la configuration du proxy.

### La connexion OAuth échoue dans WSL2

La connexion basée sur le navigateur dans WSL2 peut échouer si WSL ne peut pas ouvrir votre navigateur Windows. Définissez la variable d'environnement `BROWSER` :

```bash  theme={null}
export BROWSER="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
claude
```

Ou copiez l'URL manuellement : lorsque l'invite de connexion apparaît, appuyez sur `c` pour copier l'URL OAuth, puis collez-la dans votre navigateur Windows.

### « Not logged in » ou jeton expiré

Si Claude Code vous demande de vous connecter à nouveau après une session, votre jeton OAuth a peut-être expiré.

Exécutez `/login` pour vous réauthentifier. Si cela se produit fréquemment, vérifiez que votre horloge système est exacte, car la validation du jeton dépend des horodatages corrects.

## Emplacements des fichiers de configuration

Claude Code stocke la configuration dans plusieurs emplacements :

| Fichier                       | Objectif                                                                                                            |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------ |
| `~/.claude/settings.json`     | Paramètres utilisateur (permissions, hooks, remplacements de modèle)                                                |
| `.claude/settings.json`       | Paramètres de projet (vérifiés dans le contrôle de source)                                                          |
| `.claude/settings.local.json` | Paramètres de projet locaux (non validés)                                                                           |
| `~/.claude.json`              | État global (thème, OAuth, serveurs MCP)                                                                            |
| `.mcp.json`                   | Serveurs MCP de projet (vérifiés dans le contrôle de source)                                                        |
| `managed-mcp.json`            | [Serveurs MCP gérés](/fr/mcp#managed-mcp-configuration)                                                             |
| Paramètres gérés              | [Paramètres gérés](/fr/settings#settings-files) (gérés par serveur, politiques MDM/niveau OS, ou basés sur fichier) |

Sur Windows, `~` fait référence à votre répertoire personnel utilisateur, tel que `C:\Users\YourName`.

Pour plus de détails sur la configuration de ces fichiers, voir [Paramètres](/fr/settings) et [MCP](/fr/mcp).

### Réinitialiser la configuration

Pour réinitialiser Claude Code aux paramètres par défaut, vous pouvez supprimer les fichiers de configuration :

```bash  theme={null}
# Réinitialiser tous les paramètres utilisateur et l'état
rm ~/.claude.json
rm -rf ~/.claude/

# Réinitialiser les paramètres spécifiques au projet
rm -rf .claude/
rm .mcp.json
```

<Warning>
  Cela supprimera tous vos paramètres, configurations de serveur MCP et historique de session.
</Warning>

## Performance et stabilité

Ces sections couvrent les problèmes liés à l'utilisation des ressources, la réactivité et le comportement de recherche.

### Utilisation élevée du CPU ou de la mémoire

Claude Code est conçu pour fonctionner avec la plupart des environnements de développement, mais peut consommer des ressources importantes lors du traitement de grandes bases de code. Si vous rencontrez des problèmes de performance :

1. Utilisez `/compact` régulièrement pour réduire la taille du contexte
2. Fermez et redémarrez Claude Code entre les tâches majeures
3. Envisagez d'ajouter les grands répertoires de construction à votre fichier `.gitignore`

### Les commandes se figent ou se gèlent

Si Claude Code semble ne pas répondre :

1. Appuyez sur Ctrl+C pour tenter d'annuler l'opération actuelle
2. Si ne répond pas, vous devrez peut-être fermer le terminal et redémarrer

### Problèmes de recherche et de découverte

Si l'outil Search, les mentions `@file`, les agents personnalisés et les compétences personnalisées ne fonctionnent pas, installez le système `ripgrep` :

```bash  theme={null}
# macOS (Homebrew)  
brew install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC

# Ubuntu/Debian
sudo apt install ripgrep

# Alpine Linux
apk add ripgrep

# Arch Linux
pacman -S ripgrep
```

Puis définissez `USE_BUILTIN_RIPGREP=0` dans votre [environnement](/fr/env-vars).

### Résultats de recherche lents ou incomplets sur WSL

Les pénalités de performance de lecture de disque lors du [travail sur les systèmes de fichiers sur WSL](https://learn.microsoft.com/en-us/windows/wsl/filesystems) peuvent entraîner moins de correspondances que prévu lors de l'utilisation de Claude Code sur WSL. La recherche fonctionne toujours, mais retourne moins de résultats que sur un système de fichiers natif.

<Note>
  `/doctor` affichera Search comme OK dans ce cas.
</Note>

**Solutions :**

1. **Soumettre des recherches plus spécifiques** : réduisez le nombre de fichiers recherchés en spécifiant des répertoires ou des types de fichiers : « Search for JWT validation logic in the auth-service package » ou « Find use of md5 hash in JS files ».

2. **Déplacer le projet vers le système de fichiers Linux** : si possible, assurez-vous que votre projet est situé sur le système de fichiers Linux (`/home/`) plutôt que sur le système de fichiers Windows (`/mnt/c/`).

3. **Utiliser Windows natif à la place** : envisagez d'exécuter Claude Code nativement sur Windows au lieu de via WSL, pour une meilleure performance du système de fichiers.

## Problèmes d'intégration IDE

Si Claude Code ne se connecte pas à votre IDE ou se comporte de manière inattendue dans un terminal IDE, essayez les solutions ci-dessous.

### IDE JetBrains non détecté sur WSL2

Si vous utilisez Claude Code sur WSL2 avec les IDE JetBrains et obtenez des erreurs « No available IDEs detected », cela est probablement dû à la configuration réseau de WSL2 ou au pare-feu Windows bloquant la connexion.

#### Modes de mise en réseau WSL2

WSL2 utilise la mise en réseau NAT par défaut, ce qui peut empêcher la détection d'IDE. Vous avez deux options :

**Option 1 : Configurer le pare-feu Windows** (recommandé)

1. Trouvez votre adresse IP WSL2 :
   ```bash  theme={null}
   wsl hostname -I
   # Exemple de sortie : 172.21.123.45
   ```

2. Ouvrez PowerShell en tant qu'administrateur et créez une règle de pare-feu :
   ```powershell  theme={null}
   New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
   ```
   Ajustez la plage IP en fonction de votre sous-réseau WSL2 à partir de l'étape 1.

3. Redémarrez à la fois votre IDE et Claude Code

**Option 2 : Passer à la mise en réseau en miroir**

Ajoutez à `.wslconfig` dans votre répertoire utilisateur Windows :

```ini  theme={null}
[wsl2]
networkingMode=mirrored
```

Puis redémarrez WSL avec `wsl --shutdown` depuis PowerShell.

<Note>
  Ces problèmes de mise en réseau n'affectent que WSL2. WSL1 utilise directement le réseau de l'hôte et ne nécessite pas ces configurations.
</Note>

Pour des conseils de configuration JetBrains supplémentaires, voir le [guide IDE JetBrains](/fr/jetbrains#plugin-settings).

### Signaler les problèmes d'intégration IDE Windows

Si vous rencontrez des problèmes d'intégration IDE sur Windows, [créez un problème](https://github.com/anthropics/claude-code/issues) avec les informations suivantes :

* Type d'environnement : Windows natif (Git Bash) ou WSL1/WSL2
* Mode de mise en réseau WSL, le cas échéant : NAT ou miroir
* Nom et version de l'IDE
* Version de l'extension/plugin Claude Code
* Type de shell : Bash, Zsh, PowerShell, etc.

### La touche Échap ne fonctionne pas dans les terminaux IDE JetBrains

Si vous utilisez Claude Code dans les terminaux JetBrains et que la touche `Esc` n'interrompt pas l'agent comme prévu, cela est probablement dû à un conflit de liaison de touches avec les raccourcis par défaut de JetBrains.

Pour corriger ce problème :

1. Allez à Paramètres → Outils → Terminal
2. Soit :
   * Décochez « Move focus to the editor with Escape », soit
   * Cliquez sur « Configure terminal keybindings » et supprimez le raccourci « Switch focus to Editor »
3. Appliquez les modifications

Cela permet à la touche `Esc` d'interrompre correctement les opérations Claude Code.

## Problèmes de formatage Markdown

Claude Code génère parfois des fichiers markdown avec des balises de langage manquantes sur les clôtures de code, ce qui peut affecter la coloration syntaxique et la lisibilité dans GitHub, les éditeurs et les outils de documentation.

### Balises de langage manquantes dans les blocs de code

Si vous remarquez des blocs de code comme celui-ci dans le markdown généré :

````markdown  theme={null}
```
function example() {
  return "hello";
}
```text
````

Au lieu de blocs correctement balisés comme :

````markdown  theme={null}
```javascript
function example() {
  return "hello";
}
```text
````

**Solutions :**

1. **Demander à Claude d'ajouter des balises de langage** : demandez « Add appropriate language tags to all code blocks in this markdown file. »

2. **Utiliser des hooks de post-traitement** : configurez des hooks de formatage automatique pour détecter et ajouter les balises de langage manquantes. Voir [Auto-format code after edits](/fr/hooks-guide#auto-format-code-after-edits) pour un exemple de hook PostToolUse de formatage.

3. **Vérification manuelle** : après la génération de fichiers markdown, examinez-les pour un formatage correct des blocs de code et demandez des corrections si nécessaire.

### Espacement et formatage incohérents

Si le markdown généré a des lignes vides excessives ou un espacement incohérent :

**Solutions :**

1. **Demander des corrections de formatage** : demandez à Claude de « Fix spacing and formatting issues in this markdown file. »

2. **Utiliser des outils de formatage** : configurez des hooks pour exécuter des formateurs markdown comme `prettier` ou des scripts de formatage personnalisés sur les fichiers markdown générés.

3. **Spécifier les préférences de formatage** : incluez les exigences de formatage dans vos invites ou fichiers [memory](/fr/memory) de projet.

### Réduire les problèmes de formatage markdown

Pour minimiser les problèmes de formatage :

* **Être explicite dans les demandes** : demandez du « properly formatted markdown with language-tagged code blocks »
* **Utiliser les conventions de projet** : documentez votre style markdown préféré dans [`CLAUDE.md`](/fr/memory)
* **Configurer des hooks de validation** : utilisez des hooks de post-traitement pour vérifier et corriger automatiquement les problèmes de formatage courants

## Obtenir plus d'aide

Si vous rencontrez des problèmes non couverts ici :

1. Utilisez la commande `/bug` dans Claude Code pour signaler les problèmes directement à Anthropic
2. Vérifiez le [référentiel GitHub](https://github.com/anthropics/claude-code) pour les problèmes connus
3. Exécutez `/doctor` pour diagnostiquer les problèmes. Il vérifie :
   * Type d'installation, version et fonctionnalité de recherche
   * Statut de mise à jour automatique et versions disponibles
   * Fichiers de paramètres invalides (JSON malformé, types incorrects)
   * Erreurs de configuration du serveur MCP
   * Problèmes de configuration des liaisons de touches
   * Avertissements d'utilisation du contexte (fichiers CLAUDE.md volumineux, utilisation élevée de jetons MCP, règles de permission inaccessibles)
   * Erreurs de chargement des plugins et des agents
4. Demandez directement à Claude ses capacités et fonctionnalités - Claude a un accès intégré à sa documentation
