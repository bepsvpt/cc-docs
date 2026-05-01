> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# JetBrains IDEs

> Utilisez Claude Code avec les IDEs JetBrains, notamment IntelliJ, PyCharm, WebStorm et bien d'autres

Claude Code s'intègre aux IDEs JetBrains via un plugin dédié, offrant des fonctionnalités telles que l'affichage interactif des différences, le partage du contexte de sélection, et bien d'autres.

## IDEs supportés

Le plugin Claude Code fonctionne avec la plupart des IDEs JetBrains, notamment :

* IntelliJ IDEA
* PyCharm
* Android Studio
* WebStorm
* PhpStorm
* GoLand

## Fonctionnalités

* **Lancement rapide** : Utilisez `Cmd+Esc` (Mac) ou `Ctrl+Esc` (Windows/Linux) pour ouvrir Claude Code directement depuis votre éditeur, ou cliquez sur le bouton Claude Code dans l'interface utilisateur
* **Affichage des différences** : Les modifications de code peuvent être affichées directement dans la visionneuse de différences de l'IDE au lieu du terminal
* **Contexte de sélection** : La sélection actuelle ou l'onglet dans l'IDE est automatiquement partagé avec Claude Code
* **Raccourcis de référence de fichier** : Utilisez `Cmd+Option+K` (Mac) ou `Alt+Ctrl+K` (Linux/Windows) pour insérer des références de fichier telles que `@src/auth.ts#L1-99`
* **Partage des diagnostics** : Les erreurs de diagnostic de l'IDE, telles que les erreurs de lint et de syntaxe, sont automatiquement partagées avec Claude au fur et à mesure que vous travaillez

## Installation

### Installation via la Marketplace

Trouvez et installez le [plugin Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) depuis la marketplace JetBrains et redémarrez votre IDE.

Si vous n'avez pas encore installé Claude Code, consultez le [guide de démarrage rapide](/fr/quickstart) pour les instructions d'installation.

<Note>
  Après l'installation du plugin, vous devrez peut-être redémarrer complètement votre IDE pour que les modifications prennent effet.
</Note>

## Utilisation

### Depuis votre IDE

Exécutez `claude` depuis le terminal intégré de votre IDE, et toutes les fonctionnalités d'intégration seront actives.

### Depuis des terminaux externes

Utilisez la commande `/ide` dans n'importe quel terminal externe pour connecter Claude Code à votre IDE JetBrains et activer toutes les fonctionnalités :

```bash theme={null}
claude
```

```text theme={null}
/ide
```

Si vous souhaitez que Claude ait accès aux mêmes fichiers que votre IDE, démarrez Claude Code à partir du même répertoire que la racine du projet de votre IDE.

## Configuration

### Paramètres de Claude Code

Configurez l'intégration de l'IDE via les paramètres de Claude Code :

1. Exécutez `claude`
2. Entrez la commande `/config`
3. Définissez l'outil de différence sur `auto` pour afficher les différences dans l'IDE, ou `terminal` pour les conserver dans le terminal

### Paramètres du plugin

Configurez le plugin Claude Code en accédant à **Paramètres → Outils → Claude Code \[Beta]** :

#### Paramètres généraux

* **Commande Claude** : Spécifiez une commande personnalisée pour exécuter Claude, par exemple `claude`, `/usr/local/bin/claude`, ou `npx @anthropic-ai/claude-code`
* **Supprimer la notification pour la commande Claude non trouvée** : Ignorez les notifications concernant la non-détection de la commande Claude
* **Activer l'utilisation d'Option+Entrée pour les invites multi-lignes** : Sur macOS uniquement. Lorsqu'elle est activée, Option+Entrée insère de nouvelles lignes dans les invites Claude Code. Désactivez si la touche Option est capturée de manière inattendue. Nécessite un redémarrage du terminal.
* **Activer les mises à jour automatiques** : Vérifiez automatiquement et installez les mises à jour du plugin, appliquées au redémarrage

<Tip>
  Pour les utilisateurs WSL : Définissez `wsl -d Ubuntu -- bash -lic "claude"` comme votre commande Claude (remplacez `Ubuntu` par le nom de votre distribution WSL)
</Tip>

#### Configuration de la touche ESC

Si la touche ESC n'interrompt pas les opérations Claude Code dans les terminaux JetBrains :

1. Accédez à **Paramètres → Outils → Terminal**
2. Soit :
   * Décochez « Déplacer le focus vers l'éditeur avec Échap », soit
   * Cliquez sur « Configurer les raccourcis clavier du terminal » et supprimez le raccourci « Basculer le focus vers l'éditeur »
3. Appliquez les modifications

Cela permet à la touche ESC d'interrompre correctement les opérations Claude Code.

## Configurations spéciales

### Développement à distance

<Warning>
  Lors de l'utilisation du développement à distance JetBrains, vous devez installer le plugin sur l'hôte distant via **Paramètres → Plugin (Hôte)**.
</Warning>

Le plugin doit être installé sur l'hôte distant, et non sur votre machine cliente locale.

### Configuration WSL

Si vous utilisez Claude Code sur WSL2 avec un IDE JetBrains et que vous voyez « Aucun IDE disponible détecté », la cause est généralement le réseau NAT de WSL2 ou le Pare-feu Windows bloquant la connexion entre WSL2 et l'IDE s'exécutant sur l'hôte Windows. WSL1 utilise directement le réseau de l'hôte et n'est pas affecté.

#### Autoriser le trafic WSL2 via le Pare-feu Windows

Ceci est la correction recommandée car elle conserve votre mode de mise en réseau WSL2 existant.

<Steps>
  <Step title="Trouvez votre adresse IP WSL2">
    Depuis votre shell WSL, exécutez :

    ```bash theme={null}
    hostname -I
    ```

    Notez le sous-réseau, par exemple `172.21.123.45` se trouve dans `172.21.0.0/16`.
  </Step>

  <Step title="Créez une règle de pare-feu">
    Ouvrez PowerShell en tant qu'administrateur et exécutez ce qui suit, en ajustant la plage d'adresses IP pour correspondre à votre sous-réseau :

    ```powershell theme={null}
    New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
    ```
  </Step>

  <Step title="Redémarrez votre IDE et Claude Code">
    Fermez et rouvrez les deux pour que la nouvelle règle prenne effet.
  </Step>
</Steps>

#### Basculer WSL2 vers la mise en réseau en miroir

La mise en réseau en miroir nécessite Windows 11 22H2 ou version ultérieure. Si vous êtes sur Windows 10, utilisez la règle de pare-feu ci-dessus à la place.

Ajoutez ceci à `.wslconfig` dans votre répertoire utilisateur Windows :

```ini theme={null}
[wsl2]
networkingMode=mirrored
```

Ensuite, redémarrez WSL avec `wsl --shutdown` depuis PowerShell.

## Dépannage

### Le plugin ne fonctionne pas

Si le plugin est installé mais que les fonctionnalités Claude Code n'apparaissent pas dans votre IDE :

* Assurez-vous que vous exécutez Claude Code à partir du répertoire racine du projet
* Vérifiez que le plugin JetBrains est activé dans les paramètres de l'IDE
* Redémarrez complètement l'IDE (vous devrez peut-être le faire plusieurs fois)
* Pour le développement à distance, assurez-vous que le plugin est installé sur l'hôte distant

### IDE non détecté

Si l'exécution de `claude` affiche « Aucun IDE disponible détecté » :

* Vérifiez que le plugin est installé et activé
* Redémarrez complètement l'IDE
* Vérifiez que vous exécutez Claude Code à partir du terminal intégré
* Pour les utilisateurs WSL, consultez la [configuration WSL](#wsl-configuration) ci-dessus

### Commande non trouvée

Si cliquer sur l'icône Claude affiche « commande non trouvée » :

1. Vérifiez que Claude Code est installé en exécutant `claude --version` dans un terminal
2. Configurez le chemin de la commande Claude dans les paramètres du plugin
3. Pour les utilisateurs WSL, utilisez le format de commande WSL mentionné dans la section configuration

## Considérations de sécurité

Lorsque Claude Code s'exécute dans un IDE JetBrains avec les permissions d'édition automatique activées, il peut être en mesure de modifier les fichiers de configuration de l'IDE qui peuvent être exécutés automatiquement par votre IDE. Cela peut augmenter le risque d'exécution de Claude Code en mode édition automatique et permettre de contourner les invites de permission de Claude Code pour l'exécution bash.

Lors de l'exécution dans les IDEs JetBrains, considérez :

* L'utilisation du mode d'approbation manuelle pour les modifications
* La prise de précautions supplémentaires pour vous assurer que Claude n'est utilisé qu'avec des invites de confiance
* La sensibilisation aux fichiers auxquels Claude Code a accès pour les modifier

Pour les problèmes d'installation ou de connexion de Claude Code en dehors de l'IDE, consultez [Dépannage de l'installation et de la connexion](/fr/troubleshoot-install).
