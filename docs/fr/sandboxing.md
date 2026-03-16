> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Sandboxing

> Découvrez comment l'outil bash en sandbox de Claude Code fournit une isolation du système de fichiers et du réseau pour une exécution d'agent plus sûre et plus autonome.

## Aperçu

Claude Code dispose d'un sandboxing natif pour fournir un environnement plus sécurisé pour l'exécution des agents tout en réduisant le besoin de demandes de permission constantes. Au lieu de demander une permission pour chaque commande bash, le sandboxing crée des limites définies à l'avance où Claude Code peut travailler plus librement avec un risque réduit.

L'outil bash en sandbox utilise des primitives au niveau du système d'exploitation pour appliquer à la fois l'isolation du système de fichiers et du réseau.

## Pourquoi le sandboxing est important

La sécurité basée sur les permissions traditionnelles nécessite une approbation constante de l'utilisateur pour les commandes bash. Bien que cela offre un contrôle, cela peut entraîner :

* **Fatigue d'approbation** : Cliquer répétitivement sur « approuver » peut amener les utilisateurs à prêter moins attention à ce qu'ils approuvent
* **Productivité réduite** : Les interruptions constantes ralentissent les flux de travail de développement
* **Autonomie limitée** : Claude Code ne peut pas fonctionner aussi efficacement en attendant les approbations

Le sandboxing résout ces défis en :

1. **Définissant des limites claires** : Spécifiez exactement quels répertoires et hôtes réseau Claude Code peut accéder
2. **Réduisant les demandes de permission** : Les commandes sûres dans le sandbox ne nécessitent pas d'approbation
3. **Maintenant la sécurité** : Les tentatives d'accès aux ressources en dehors du sandbox déclenchent des notifications immédiates
4. **Permettant l'autonomie** : Claude Code peut fonctionner plus indépendamment dans les limites définies

<Warning>
  Un sandboxing efficace nécessite **à la fois** l'isolation du système de fichiers et du réseau. Sans isolation réseau, un agent compromis pourrait exfiltrer des fichiers sensibles comme les clés SSH. Sans isolation du système de fichiers, un agent compromis pourrait installer une porte dérobée sur les ressources système pour accéder au réseau. Lors de la configuration du sandboxing, il est important de s'assurer que vos paramètres configurés ne créent pas de contournements dans ces systèmes.
</Warning>

## Comment ça marche

### Isolation du système de fichiers

L'outil bash en sandbox restreint l'accès au système de fichiers à des répertoires spécifiques :

* **Comportement d'écriture par défaut** : Accès en lecture et écriture au répertoire de travail actuel et à ses sous-répertoires
* **Comportement de lecture par défaut** : Accès en lecture à l'ensemble de l'ordinateur, sauf certains répertoires refusés
* **Accès bloqué** : Impossible de modifier les fichiers en dehors du répertoire de travail actuel sans permission explicite
* **Configurable** : Définissez des chemins autorisés et refusés personnalisés via les paramètres

Vous pouvez accorder l'accès en écriture à des chemins supplémentaires en utilisant `sandbox.filesystem.allowWrite` dans vos paramètres. Ces restrictions sont appliquées au niveau du système d'exploitation (Seatbelt sur macOS, bubblewrap sur Linux), elles s'appliquent donc à toutes les commandes de sous-processus, y compris les outils comme `kubectl`, `terraform` et `npm`, pas seulement aux outils de fichiers de Claude.

### Isolation réseau

L'accès réseau est contrôlé via un serveur proxy s'exécutant en dehors du sandbox :

* **Restrictions de domaine** : Seuls les domaines approuvés peuvent être accédés
* **Confirmation de l'utilisateur** : Les nouvelles demandes de domaine déclenchent des demandes de permission (sauf si [`allowManagedDomainsOnly`](/fr/settings#sandbox-settings) est activé, ce qui bloque automatiquement les domaines non autorisés)
* **Support de proxy personnalisé** : Les utilisateurs avancés peuvent implémenter des règles personnalisées sur le trafic sortant
* **Couverture complète** : Les restrictions s'appliquent à tous les scripts, programmes et sous-processus générés par les commandes

### Application au niveau du système d'exploitation

L'outil bash en sandbox exploite les primitives de sécurité du système d'exploitation :

* **macOS** : Utilise Seatbelt pour l'application du sandbox
* **Linux** : Utilise [bubblewrap](https://github.com/containers/bubblewrap) pour l'isolation
* **WSL2** : Utilise bubblewrap, comme Linux

WSL1 n'est pas supporté car bubblewrap nécessite des fonctionnalités du noyau uniquement disponibles dans WSL2.

Ces restrictions au niveau du système d'exploitation garantissent que tous les processus enfants générés par les commandes de Claude Code héritent des mêmes limites de sécurité.

## Démarrage

### Prérequis

Sur **macOS**, le sandboxing fonctionne directement en utilisant le framework Seatbelt intégré.

Sur **Linux et WSL2**, installez d'abord les packages requis :

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

### Activer le sandboxing

Vous pouvez activer le sandboxing en exécutant la commande `/sandbox` :

```text  theme={null}
/sandbox
```

Cela ouvre un menu où vous pouvez choisir entre les modes de sandbox. Si les dépendances requises sont manquantes (comme `bubblewrap` ou `socat` sur Linux), le menu affiche les instructions d'installation pour votre plateforme.

### Modes de sandbox

Claude Code offre deux modes de sandbox :

**Mode auto-allow** : Les commandes Bash tenteront de s'exécuter dans le sandbox et sont automatiquement autorisées sans nécessiter de permission. Les commandes qui ne peuvent pas être sandboxées (comme celles nécessitant un accès réseau à des hôtes non autorisés) reviennent au flux de permission régulier. Les règles d'ask/deny explicites que vous avez configurées sont toujours respectées.

**Mode permissions régulières** : Toutes les commandes bash passent par le flux de permission standard, même lorsqu'elles sont sandboxées. Cela offre plus de contrôle mais nécessite plus d'approbations.

Dans les deux modes, le sandbox applique les mêmes restrictions de système de fichiers et de réseau. La différence réside uniquement dans le fait que les commandes sandboxées sont auto-approuvées ou nécessitent une permission explicite.

<Info>
  Le mode auto-allow fonctionne indépendamment de votre paramètre de mode de permission. Même si vous n'êtes pas en mode « accepter les modifications », les commandes bash sandboxées s'exécuteront automatiquement lorsque l'auto-allow est activé. Cela signifie que les commandes bash qui modifient les fichiers dans les limites du sandbox s'exécuteront sans invite, même lorsque les outils de modification de fichiers nécessiteraient normalement une approbation.
</Info>

### Configurer le sandboxing

Personnalisez le comportement du sandbox via votre fichier `settings.json`. Consultez [Paramètres](/fr/settings#sandbox-settings) pour la référence de configuration complète.

#### Accorder l'accès en écriture des sous-processus à des chemins spécifiques

Par défaut, les commandes sandboxées ne peuvent écrire que dans le répertoire de travail actuel. Si les commandes de sous-processus comme `kubectl`, `terraform` ou `npm` doivent écrire en dehors du répertoire du projet, utilisez `sandbox.filesystem.allowWrite` pour accorder l'accès à des chemins spécifiques :

```json  theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowWrite": ["~/.kube", "//tmp/build"]
    }
  }
}
```

Ces chemins sont appliqués au niveau du système d'exploitation, donc toutes les commandes s'exécutant dans le sandbox, y compris leurs processus enfants, les respectent. C'est l'approche recommandée lorsqu'un outil a besoin d'un accès en écriture à un emplacement spécifique, plutôt que d'exclure complètement l'outil du sandbox avec `excludedCommands`.

Lorsque `allowWrite` (ou `denyWrite`/`denyRead`) est défini dans plusieurs [portées de paramètres](/fr/settings#settings-precedence), les tableaux sont **fusionnés**, ce qui signifie que les chemins de chaque portée sont combinés, non remplacés. Par exemple, si les paramètres gérés autorisent les écritures à `//opt/company-tools` et qu'un utilisateur ajoute `~/.kube` dans ses paramètres personnels, les deux chemins sont inclus dans la configuration finale du sandbox. Cela signifie que les utilisateurs et les projets peuvent étendre la liste sans dupliquer ou remplacer les chemins définis par les portées de priorité plus élevée.

Les préfixes de chemin contrôlent la façon dont les chemins sont résolus :

| Préfixe                | Signification                                              | Exemple                                |
| :--------------------- | :--------------------------------------------------------- | :------------------------------------- |
| `//`                   | Chemin absolu à partir de la racine du système de fichiers | `//tmp/build` devient `/tmp/build`     |
| `~/`                   | Relatif au répertoire personnel                            | `~/.kube` devient `$HOME/.kube`        |
| `/`                    | Relatif au répertoire du fichier de paramètres             | `/build` devient `$SETTINGS_DIR/build` |
| `./` ou pas de préfixe | Chemin relatif (résolu par le runtime du sandbox)          | `./output`                             |

Vous pouvez également refuser l'accès en écriture ou en lecture en utilisant `sandbox.filesystem.denyWrite` et `sandbox.filesystem.denyRead`. Ceux-ci sont fusionnés avec tous les chemins des règles de permission `Edit(...)` et `Read(...)`.

<Tip>
  Toutes les commandes ne sont pas compatibles avec le sandboxing directement. Quelques notes qui peuvent vous aider à tirer le meilleur parti du sandbox :

  * De nombreux outils CLI nécessitent d'accéder à certains hôtes. Au fur et à mesure que vous utilisez ces outils, ils demanderont la permission d'accéder à certains hôtes. Accorder la permission leur permettra d'accéder à ces hôtes maintenant et à l'avenir, leur permettant de s'exécuter en toute sécurité dans le sandbox.
  * `watchman` est incompatible avec l'exécution dans le sandbox. Si vous exécutez `jest`, envisagez d'utiliser `jest --no-watchman`
  * `docker` est incompatible avec l'exécution dans le sandbox. Envisagez de spécifier `docker` dans `excludedCommands` pour le forcer à s'exécuter en dehors du sandbox.
</Tip>

<Note>
  Claude Code inclut un mécanisme d'échappatoire intentionnel qui permet aux commandes de s'exécuter en dehors du sandbox si nécessaire. Lorsqu'une commande échoue en raison des restrictions du sandbox (comme les problèmes de connectivité réseau ou les outils incompatibles), Claude est invité à analyser l'échec et peut réessayer la commande avec le paramètre `dangerouslyDisableSandbox`. Les commandes qui utilisent ce paramètre passent par le flux de permissions normal de Claude Code nécessitant une permission de l'utilisateur pour s'exécuter. Cela permet à Claude Code de gérer les cas limites où certains outils ou opérations réseau ne peuvent pas fonctionner dans les contraintes du sandbox.

  Vous pouvez désactiver cet échappatoire en définissant `"allowUnsandboxedCommands": false` dans vos [paramètres de sandbox](/fr/settings#sandbox-settings). Lorsqu'il est désactivé, le paramètre `dangerouslyDisableSandbox` est complètement ignoré et toutes les commandes doivent s'exécuter sandboxées ou être explicitement listées dans `excludedCommands`.
</Note>

## Avantages de sécurité

### Protection contre l'injection de prompt

Même si un attaquant manipule avec succès le comportement de Claude Code par injection de prompt, le sandbox garantit que votre système reste sécurisé :

**Protection du système de fichiers :**

* Impossible de modifier les fichiers de configuration critiques tels que `~/.bashrc`
* Impossible de modifier les fichiers au niveau du système dans `/bin/`
* Impossible de lire les fichiers qui sont refusés dans vos [paramètres de permission Claude](/fr/permissions#manage-permissions)

**Protection réseau :**

* Impossible d'exfiltrer les données vers des serveurs contrôlés par l'attaquant
* Impossible de télécharger des scripts malveillants à partir de domaines non autorisés
* Impossible de faire des appels API inattendus vers des services non approuvés
* Impossible de contacter des domaines non explicitement autorisés

**Surveillance et contrôle :**

* Toutes les tentatives d'accès en dehors du sandbox sont bloquées au niveau du système d'exploitation
* Vous recevez des notifications immédiates lorsque les limites sont testées
* Vous pouvez choisir de refuser, d'autoriser une fois ou de mettre à jour définitivement votre configuration

### Surface d'attaque réduite

Le sandboxing limite les dommages potentiels causés par :

* **Dépendances malveillantes** : Packages NPM ou autres dépendances avec du code nuisible
* **Scripts compromis** : Scripts de construction ou outils avec des vulnérabilités de sécurité
* **Ingénierie sociale** : Attaques qui trompent les utilisateurs pour qu'ils exécutent des commandes dangereuses
* **Injection de prompt** : Attaques qui trompent Claude pour qu'il exécute des commandes dangereuses

### Fonctionnement transparent

Lorsque Claude Code tente d'accéder à des ressources réseau en dehors du sandbox :

1. L'opération est bloquée au niveau du système d'exploitation
2. Vous recevez une notification immédiate
3. Vous pouvez choisir de :
   * Refuser la demande
   * L'autoriser une fois
   * Mettre à jour votre configuration de sandbox pour l'autoriser définitivement

## Limitations de sécurité

* Limitations du sandboxing réseau : Le système de filtrage réseau fonctionne en restreignant les domaines auxquels les processus sont autorisés à se connecter. Il n'inspecte pas autrement le trafic passant par le proxy et les utilisateurs sont responsables de s'assurer qu'ils n'autorisent que les domaines de confiance dans leur politique.

<Warning>
  Les utilisateurs doivent être conscients des risques potentiels liés à l'autorisation de domaines larges comme `github.com` qui peuvent permettre l'exfiltration de données. De plus, dans certains cas, il peut être possible de contourner le filtrage réseau via [domain fronting](https://en.wikipedia.org/wiki/Domain_fronting).
</Warning>

* Escalade de privilèges via les sockets Unix : La configuration `allowUnixSockets` peut accorder involontairement l'accès à des services système puissants qui pourraient entraîner des contournements du sandbox. Par exemple, si elle est utilisée pour autoriser l'accès à `/var/run/docker.sock`, cela accorderait effectivement l'accès au système hôte en exploitant le socket docker. Les utilisateurs sont encouragés à examiner attentivement tous les sockets Unix qu'ils autorisent via le sandbox.
* Escalade de permissions du système de fichiers : Les permissions d'écriture du système de fichiers trop larges peuvent permettre des attaques d'escalade de privilèges. Autoriser les écritures dans les répertoires contenant des exécutables dans `$PATH`, les répertoires de configuration système ou les fichiers de configuration du shell utilisateur (`.bashrc`, `.zshrc`) peut entraîner l'exécution de code dans différents contextes de sécurité lorsque d'autres utilisateurs ou processus système accèdent à ces fichiers.
* Force du sandbox Linux : L'implémentation Linux fournit une isolation forte du système de fichiers et du réseau mais inclut un mode `enableWeakerNestedSandbox` qui lui permet de fonctionner à l'intérieur des environnements Docker sans espaces de noms privilégiés. Cette option affaiblit considérablement la sécurité et ne doit être utilisée que dans les cas où une isolation supplémentaire est autrement appliquée.

## Comment le sandboxing se rapporte aux permissions

Le sandboxing et les [permissions](/fr/permissions) sont des couches de sécurité complémentaires qui fonctionnent ensemble :

* **Les permissions** contrôlent quels outils Claude Code peut utiliser et sont évaluées avant l'exécution de tout outil. Elles s'appliquent à tous les outils : Bash, Read, Edit, WebFetch, MCP et autres.
* **Le sandboxing** fournit une application au niveau du système d'exploitation qui restreint ce que les commandes Bash peuvent accéder au niveau du système de fichiers et du réseau. Il s'applique uniquement aux commandes Bash et à leurs processus enfants.

Les restrictions du système de fichiers et du réseau sont configurées via les paramètres de sandbox et les règles de permission :

* Utilisez `sandbox.filesystem.allowWrite` pour accorder l'accès en écriture des sous-processus à des chemins en dehors du répertoire de travail
* Utilisez `sandbox.filesystem.denyWrite` et `sandbox.filesystem.denyRead` pour bloquer l'accès des sous-processus à des chemins spécifiques
* Utilisez les règles de refus `Read` et `Edit` pour bloquer l'accès à des fichiers ou répertoires spécifiques
* Utilisez les règles d'autorisation/refus `WebFetch` pour contrôler l'accès au domaine
* Utilisez les `allowedDomains` du sandbox pour contrôler quels domaines les commandes Bash peuvent atteindre

Les chemins des paramètres `sandbox.filesystem` et des règles de permission sont fusionnés dans la configuration finale du sandbox.

Ce [référentiel](https://github.com/anthropics/claude-code/tree/main/examples/settings) inclut des configurations de paramètres de démarrage pour les scénarios de déploiement courants, y compris des exemples spécifiques au sandbox. Utilisez-les comme points de départ et ajustez-les selon vos besoins.

## Utilisation avancée

### Configuration de proxy personnalisée

Pour les organisations nécessitant une sécurité réseau avancée, vous pouvez implémenter un proxy personnalisé pour :

* Déchiffrer et inspecter le trafic HTTPS
* Appliquer des règles de filtrage personnalisées
* Enregistrer toutes les demandes réseau
* Intégrer avec l'infrastructure de sécurité existante

```json  theme={null}
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

### Intégration avec les outils de sécurité existants

L'outil bash en sandbox fonctionne aux côtés de :

* **Règles de permission** : Combinez avec les [paramètres de permission](/fr/permissions) pour une défense en profondeur
* **Conteneurs de développement** : Utilisez avec [devcontainers](/fr/devcontainer) pour une isolation supplémentaire
* **Politiques d'entreprise** : Appliquez les configurations de sandbox via les [paramètres gérés](/fr/settings#settings-precedence)

## Meilleures pratiques

1. **Commencez restrictif** : Commencez avec des permissions minimales et développez selon les besoins
2. **Surveillez les journaux** : Examinez les tentatives de violation du sandbox pour comprendre les besoins de Claude Code
3. **Utilisez des configurations spécifiques à l'environnement** : Différentes règles de sandbox pour les contextes de développement par rapport à la production
4. **Combinez avec les permissions** : Utilisez le sandboxing aux côtés des politiques IAM pour une sécurité complète
5. **Testez les configurations** : Vérifiez que vos paramètres de sandbox ne bloquent pas les flux de travail légitimes

## Open source

Le runtime du sandbox est disponible en tant que package npm open source pour une utilisation dans vos propres projets d'agent. Cela permet à la communauté plus large des agents IA de construire des systèmes autonomes plus sûrs et plus sécurisés. Cela peut également être utilisé pour sandboxer d'autres programmes que vous souhaitez exécuter. Par exemple, pour sandboxer un serveur MCP, vous pouvez exécuter :

```bash  theme={null}
npx @anthropic-ai/sandbox-runtime <command-to-sandbox>
```

Pour les détails d'implémentation et le code source, visitez le [référentiel GitHub](https://github.com/anthropic-experimental/sandbox-runtime).

## Limitations

* **Surcharge de performance** : Minimale, mais certaines opérations du système de fichiers peuvent être légèrement plus lentes
* **Compatibilité** : Certains outils qui nécessitent des modèles d'accès système spécifiques peuvent nécessiter des ajustements de configuration, ou même devront être exécutés en dehors du sandbox
* **Support de plateforme** : Supporte macOS, Linux et WSL2. WSL1 n'est pas supporté. Le support natif de Windows est prévu.

## Voir aussi

* [Sécurité](/fr/security) - Fonctionnalités de sécurité complètes et meilleures pratiques
* [Permissions](/fr/permissions) - Configuration des permissions et contrôle d'accès
* [Paramètres](/fr/settings) - Référence de configuration complète
* [Référence CLI](/fr/cli-reference) - Options de ligne de commande
