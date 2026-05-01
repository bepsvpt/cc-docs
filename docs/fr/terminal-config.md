> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurez votre terminal pour Claude Code

> Corrigez Maj+Entrée pour les sauts de ligne, recevez une notification sonore du terminal lorsque Claude termine, configurez tmux, adaptez le thème de couleur et activez le mode Vim dans l'interface CLI de Claude Code.

Claude Code fonctionne dans n'importe quel terminal sans configuration. Cette page est destinée aux cas où quelque chose de spécifique ne se comporte pas comme prévu. Trouvez votre symptôme ci-dessous. Si tout vous semble déjà correct, vous n'avez pas besoin de cette page.

* [Maj+Entrée soumet au lieu d'insérer un saut de ligne](#enter-multiline-prompts)
* [Les raccourcis avec la touche Option ne font rien sur macOS](#enable-option-key-shortcuts-on-macos)
* [Aucun son ou alerte lorsque Claude termine](#get-a-terminal-bell-or-notification)
* [Vous exécutez Claude Code dans tmux](#configure-tmux)
* [L'affichage scintille ou le défilement saute](#switch-to-fullscreen-rendering)
* [Vous voulez les touches Vim dans l'invite](#edit-prompts-with-vim-keybindings)

Cette page concerne la configuration de votre terminal pour envoyer les bons signaux à Claude Code. Pour modifier les touches auxquelles Claude Code lui-même répond, consultez plutôt [keybindings](/fr/keybindings).

## Entrer des invites multilignes

Appuyer sur Entrée soumet votre message. Pour ajouter un saut de ligne sans soumettre, appuyez sur Ctrl+J, ou tapez `\` puis appuyez sur Entrée. Les deux fonctionnent dans tous les terminaux sans configuration.

Dans la plupart des terminaux, vous pouvez également appuyer sur Maj+Entrée, mais le support varie selon l'émulateur de terminal :

| Terminal                                                                            | Maj+Entrée pour saut de ligne                       |
| :---------------------------------------------------------------------------------- | :-------------------------------------------------- |
| Ghostty, Kitty, iTerm2, WezTerm, Warp, Apple Terminal                               | Fonctionne sans configuration                       |
| VS Code, Cursor, Windsurf, Alacritty, Zed                                           | Exécutez `/terminal-setup` une fois                 |
| Windows Terminal, gnome-terminal, JetBrains IDEs tels que PyCharm et Android Studio | Non disponible ; utilisez Ctrl+J ou `\` puis Entrée |

Pour VS Code, Cursor, Windsurf, Alacritty et Zed, `/terminal-setup` écrit Maj+Entrée et d'autres liaisons de clavier dans le fichier de configuration du terminal. Dans VS Code, Cursor et Windsurf, il définit également `terminal.integrated.mouseWheelScrollSensitivity` dans les paramètres de l'éditeur pour un défilement plus fluide en [mode plein écran](/fr/fullscreen). Les liaisons et paramètres existants sont conservés ; si vous voyez un message tel que `VSCode terminal Shift+Enter key binding already configured`, aucune modification n'a été apportée. Exécutez `/terminal-setup` directement dans le terminal hôte plutôt qu'à l'intérieur de tmux ou screen, car il doit écrire dans la configuration du terminal hôte.

Si vous exécutez à l'intérieur de tmux, Maj+Entrée nécessite également la [configuration tmux ci-dessous](#configure-tmux) même lorsque le terminal externe la supporte.

Pour lier le saut de ligne à une touche différente, ou pour inverser le comportement afin qu'Entrée insère un saut de ligne et Maj+Entrée soumet, mappez les actions `chat:newline` et `chat:submit` dans votre [fichier keybindings](/fr/keybindings).

## Activer les raccourcis de la touche Option sur macOS

Certains raccourcis de Claude Code utilisent la touche Option, comme Option+Entrée pour un saut de ligne ou Option+P pour changer de modèle. Sur macOS, la plupart des terminaux n'envoient pas Option comme modificateur par défaut, donc ces raccourcis ne font rien jusqu'à ce que vous l'activiez. Le paramètre du terminal pour cela est généralement étiqueté « Use Option as Meta Key » ; Meta est le nom Unix historique de la touche maintenant étiquetée Option ou Alt.

<Tabs>
  <Tab title="Apple Terminal">
    Ouvrez Paramètres → Profils → Clavier et cochez ' Utiliser Option comme touche Meta '.

    Si vous avez accepté l'invite de premier lancement de Claude Code qui proposait ' Option+Entrée pour les sauts de ligne et la cloche visuelle ', c'est déjà fait. Cette invite exécute `/terminal-setup` pour vous, ce qui active Option comme Meta et bascule la cloche audio vers un flash d'écran visuel dans votre profil Apple Terminal.
  </Tab>

  <Tab title="iTerm2">
    Ouvrez Paramètres → Profils → Touches → Général et définissez la touche Option gauche et la touche Option droite sur « Esc+ ».

    L'exécution de `/terminal-setup` dans iTerm2 active « Applications in terminal may access clipboard » sous Paramètres → Général → Sélection afin que la commande `/copy` puisse écrire dans votre presse-papiers système. La commande détecte iTerm2 même lorsqu'elle est exécutée depuis tmux. Redémarrez iTerm2 pour que la modification prenne effet.
  </Tab>

  <Tab title="VS Code">
    Ajoutez `"terminal.integrated.macOptionIsMeta": true` à vos paramètres VS Code.
  </Tab>
</Tabs>

Pour Ghostty, Kitty et d'autres terminaux, recherchez un paramètre Option-as-Alt ou Option-as-Meta dans le fichier de configuration du terminal.

## Obtenir une cloche de terminal ou une notification

Lorsque Claude termine une tâche ou s'arrête pour une invite de permission, il déclenche un événement de notification. Afficher cela comme une cloche de terminal ou une notification de bureau vous permet de passer à d'autres tâches pendant qu'une longue tâche s'exécute.

Claude Code envoie une notification de bureau uniquement dans Ghostty, Kitty et iTerm2 ; tous les autres terminaux ont besoin d'un [hook Notification](#play-a-sound-with-a-notification-hook) à la place. La notification atteint également votre machine locale via SSH, donc une session distante peut toujours vous alerter. Ghostty et Kitty la transmettent à votre centre de notifications du système d'exploitation sans configuration supplémentaire. iTerm2 nécessite que vous activiez la transmission :

<Steps>
  <Step title="Ouvrir les paramètres de notification iTerm2">
    Allez à Paramètres → Profils → Terminal.
  </Step>

  <Step title="Activer les alertes">
    Cochez « Notification Center Alerts », puis cliquez sur « Filter Alerts » et activez « Send escape sequence-generated alerts ».
  </Step>
</Steps>

Si les notifications n'apparaissent toujours pas, confirmez que votre application de terminal dispose de la permission de notification dans vos paramètres du système d'exploitation, et si vous exécutez à l'intérieur de tmux, [activez le passthrough](#configure-tmux).

### Jouer un son avec un hook Notification

Dans n'importe quel terminal, vous pouvez configurer un [hook Notification](/fr/hooks-guide#get-notified-when-claude-needs-input) pour jouer un son ou exécuter une commande personnalisée lorsque Claude a besoin de votre attention. Les hooks s'exécutent aux côtés de la notification de bureau plutôt que de la remplacer. Les terminaux tels que Warp ou Apple Terminal s'appuient sur un hook seul puisque Claude Code ne leur envoie pas de notification de bureau.

L'exemple ci-dessous joue un son système sur macOS. Le guide lié contient des commandes de notification de bureau pour macOS, Linux et Windows.

```json ~/.claude/settings.json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "hooks": [{ "type": "command", "command": "afplay /System/Library/Sounds/Glass.aiff" }]
      }
    ]
  }
}
```

## Configurer tmux

Lorsque Claude Code s'exécute à l'intérieur de tmux, deux choses se cassent par défaut : Maj+Entrée soumet au lieu d'insérer un saut de ligne, et les notifications de bureau et la [barre de progression](/fr/settings#available-settings) n'atteignent jamais le terminal externe. Ajoutez ces lignes à `~/.tmux.conf`, puis exécutez `tmux source-file ~/.tmux.conf` pour les appliquer au serveur en cours d'exécution :

```bash ~/.tmux.conf theme={null}
set -g allow-passthrough on
set -s extended-keys on
set -as terminal-features 'xterm*:extkeys'
```

La ligne `allow-passthrough` permet aux notifications et aux mises à jour de progression d'atteindre iTerm2, Ghostty ou Kitty au lieu d'être avalées par tmux. Les lignes `extended-keys` permettent à tmux de distinguer Maj+Entrée de la simple Entrée afin que le raccourci de saut de ligne fonctionne.

## Adapter le thème de couleur

Utilisez la commande `/theme`, ou le sélecteur de thème dans `/config`, pour choisir un thème Claude Code qui correspond à votre terminal. La sélection de l'option auto détecte le fond clair ou sombre de votre terminal, de sorte que le thème suit les changements d'apparence du système d'exploitation chaque fois que votre terminal le fait. Claude Code ne contrôle pas le schéma de couleurs du terminal lui-même, qui est défini par l'application de terminal.

Pour personnaliser ce qui apparaît en bas de l'interface, configurez une [ligne d'état personnalisée](/fr/statusline) qui affiche le modèle actuel, le répertoire de travail, la branche git ou d'autres contextes.

### Créer un thème personnalisé

<Note>
  Les thèmes personnalisés nécessitent Claude Code v2.1.118 ou version ultérieure.
</Note>

En plus des présets intégrés, `/theme` répertorie tous les thèmes personnalisés que vous avez définis et tous les thèmes contribués par les [plugins](/fr/plugins-reference#themes) installés. Sélectionnez **Nouveau thème personnalisé…** à la fin de la liste pour en créer un de manière interactive : vous nommez le thème, puis choisissez les jetons de couleur individuels à remplacer. Appuyez sur `Ctrl+E` tandis qu'un thème personnalisé est en surbrillance pour le modifier.

Chaque thème personnalisé est un fichier JSON dans `~/.claude/themes/`. Le nom de fichier sans l'extension `.json` est le slug du thème, et la sélection du thème stocke `custom:<slug>` comme préférence de thème. Le fichier a trois champs optionnels :

| Champ       | Type   | Description                                                                                                                                                |
| :---------- | :----- | :--------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`      | string | Étiquette d'affichage affichée dans `/theme`. Par défaut, le slug du nom de fichier                                                                        |
| `base`      | string | Preset intégré à partir duquel le thème commence : `dark`, `light`, `dark-daltonized`, `light-daltonized`, `dark-ansi`, ou `light-ansi`. Par défaut `dark` |
| `overrides` | object | Mappage des noms de jetons de couleur aux valeurs de couleur. Les jetons non listés ici passent au preset de base                                          |

Les valeurs de couleur acceptent `#rrggbb`, `#rgb`, `rgb(r,g,b)`, `ansi256(n)`, ou `ansi:<name>` où `<name>` est l'un des 16 noms de couleur ANSI standard tels que `red` ou `cyanBright`. Les jetons inconnus et les valeurs de couleur invalides sont ignorés, donc une faute de frappe ne peut pas casser le rendu.

L'exemple suivant définit un thème qui conserve le preset sombre mais recolore l'accent d'invite, le texte d'erreur et le texte de succès :

```json ~/.claude/themes/dracula.json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

Claude Code surveille `~/.claude/themes/` et recharge lorsqu'un fichier change, de sorte que les modifications apportées dans votre éditeur s'appliquent à une session en cours sans redémarrage.

Ci-dessous se trouve la liste complète des personnalisations que vous pouvez définir dans `overrides`. L'éditeur interactif dans `/theme` affiche les mêmes jetons avec un aperçu en direct, y compris un petit nombre de jetons internes non couverts ici.

<Accordion title="Référence des jetons de couleur">
  L'exemple suivant combine les jetons de plusieurs groupes ci-dessous : l'accent de marque, la bordure du mode plan, les arrière-plans de diff et l'arrière-plan du message en plein écran.

  ```json ~/.claude/themes/midnight.json theme={null}
  {
    "name": "Midnight",
    "base": "dark",
    "overrides": {
      "claude": "#a78bfa",
      "planMode": "#38bdf8",
      "diffAdded": "#14532d",
      "diffRemoved": "#7f1d1d",
      "userMessageBackground": "#1e1b4b"
    }
  }
  ```

  #### Couleurs de texte et d'accent

  Contrôlez l'accent de marque principal et les nuances de texte de premier plan utilisées dans toute l'interface.

  | Jeton         | Contrôle                                                                         |
  | :------------ | :------------------------------------------------------------------------------- |
  | `claude`      | Accent de marque principal, utilisé pour le spinner et l'étiquette d'assistant   |
  | `text`        | Texte de premier plan par défaut                                                 |
  | `inverseText` | Texte dessiné sur un arrière-plan coloré, comme les badges de statut             |
  | `inactive`    | Texte secondaire tel que les indices, les horodatages et les éléments désactivés |
  | `subtle`      | Bordures faibles et texte secondaire désaccentué                                 |
  | `permission`  | Bordures de dialogue, y compris les invites de permission et les sélecteurs      |
  | `remember`    | Indicateurs de mémoire et `CLAUDE.md`                                            |

  #### Couleurs de statut

  Signalez les états de succès, d'échec et d'avertissement dans les messages et les indicateurs.

  | Jeton     | Contrôle                                                     |
  | :-------- | :----------------------------------------------------------- |
  | `success` | Messages de succès et vérifications réussies                 |
  | `error`   | Messages d'erreur et échecs                                  |
  | `warning` | Avertissements, messages de prudence et bordure du mode auto |
  | `merged`  | Statut de demande de tirage fusionnée                        |

  #### Boîte d'entrée et indicateurs de mode

  Définissez la couleur de bordure de la boîte d'entrée et l'accent affiché tandis qu'un mode de permission ou un indicateur est actif.

  | Jeton          | Contrôle                                                               |
  | :------------- | :--------------------------------------------------------------------- |
  | `promptBorder` | Bordure de la boîte d'entrée en mode permission par défaut             |
  | `planMode`     | Accent et bordure du mode plan                                         |
  | `autoAccept`   | Accent et bordure du mode acceptation des modifications                |
  | `bashBorder`   | Bordure de la boîte d'entrée lors de l'entrée d'une commande shell `!` |
  | `ide`          | Indicateur de connexion IDE                                            |
  | `fastMode`     | Indicateur du mode rapide                                              |

  #### Rendu des diffs

  Colorez le code ajouté et supprimé dans les modifications et révisions de fichiers.

  | Jeton               | Contrôle                                                     |
  | :------------------ | :----------------------------------------------------------- |
  | `diffAdded`         | Arrière-plan des lignes ajoutées                             |
  | `diffRemoved`       | Arrière-plan des lignes supprimées                           |
  | `diffAddedDimmed`   | Arrière-plan du contexte inchangé près des lignes ajoutées   |
  | `diffRemovedDimmed` | Arrière-plan du contexte inchangé près des lignes supprimées |
  | `diffAddedWord`     | Surbrillance au niveau des mots dans une ligne ajoutée       |
  | `diffRemovedWord`   | Surbrillance au niveau des mots dans une ligne supprimée     |

  #### Mode plein écran

  S'applique uniquement en [mode de rendu plein écran](/fr/fullscreen), où les messages ont un remplissage d'arrière-plan.

  | Jeton                   | Contrôle                                                 |
  | :---------------------- | :------------------------------------------------------- |
  | `userMessageBackground` | Arrière-plan derrière vos messages dans la transcription |
  | `selectionBg`           | Arrière-plan du texte sélectionné à la souris            |

  #### Variantes de scintillement et couleurs des sous-agents

  Plusieurs jetons ont une variante `Shimmer` appariée, telle que `claudeShimmer` et `warningShimmer`, qui fournit la couleur plus claire utilisée dans le dégradé animé du spinner. Remplacez le scintillement aux côtés de son jeton de base si l'animation semble mal assortie.

  Chaque [sous-agent](/fr/sub-agents) et tâche parallèle est affiché dans l'une des huit couleurs nommées afin que vous puissiez les distinguer dans la transcription. Les noms de jetons suivent le modèle `<color>_FOR_SUBAGENTS_ONLY`, où `<color>` est `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink`, ou `cyan`. Remplacez-les pour modifier l'apparence de chaque couleur nommée. Par exemple, un sous-agent avec `color: blue` dans sa définition est dessiné en utilisant la valeur `blue_FOR_SUBAGENTS_ONLY`.
</Accordion>

## Basculer vers le rendu en plein écran

Si l'affichage scintille ou la position de défilement saute pendant que Claude travaille, basculez vers le [mode de rendu en plein écran](/fr/fullscreen). Il dessine sur un écran séparé que le terminal réserve aux applications en plein écran au lieu d'ajouter à votre défilement normal, ce qui maintient l'utilisation de la mémoire plate et ajoute le support de la souris pour le défilement et la sélection. Dans ce mode, vous faites défiler avec la souris ou PageUp à l'intérieur de Claude Code plutôt qu'avec le défilement natif de votre terminal ; consultez la [page plein écran](/fr/fullscreen#search-and-review-the-conversation) pour savoir comment rechercher et copier.

Exécutez `/tui fullscreen` pour basculer dans la session actuelle avec votre conversation intacte. Pour en faire la valeur par défaut, définissez la variable d'environnement `CLAUDE_CODE_NO_FLICKER` avant de démarrer Claude Code :

<CodeGroup>
  ```bash Bash and Zsh theme={null}
  CLAUDE_CODE_NO_FLICKER=1 claude
  ```

  ```powershell PowerShell theme={null}
  $env:CLAUDE_CODE_NO_FLICKER = "1"; claude
  ```

  ```json ~/.claude/settings.json theme={null}
  {
    "env": {
      "CLAUDE_CODE_NO_FLICKER": "1"
    }
  }
  ```
</CodeGroup>

## Coller du contenu volumineux

Lorsque vous collez plus de 10 000 caractères dans l'invite, Claude Code réduit l'entrée à un espace réservé `[Pasted text]` afin que la boîte d'entrée reste utilisable. Le contenu complet est toujours envoyé à Claude lorsque vous soumettez.

Le terminal intégré VS Code peut supprimer des caractères des très grands collages avant qu'ils n'atteignent Claude Code, donc préférez les flux basés sur des fichiers là-bas. Pour les très grandes entrées telles que des fichiers entiers ou de longs journaux, écrivez le contenu dans un fichier et demandez à Claude de le lire au lieu de coller. Cela maintient la transcription de la conversation lisible et permet à Claude de référencer le fichier par chemin dans les tours ultérieurs.

## Éditer les invites avec les liaisons de clavier Vim

Claude Code inclut un mode d'édition de style Vim pour l'entrée d'invite. Activez-le via `/config` → Editor mode, ou en définissant [`editorMode`](/fr/settings#available-settings) sur `"vim"` dans `~/.claude/settings.json`. Définissez Editor mode à nouveau sur `normal` pour le désactiver.

Le mode Vim supporte un sous-ensemble de motions et d'opérateurs en mode NORMAL et VISUAL, tels que la navigation `hjkl`, la sélection `v`/`V`, et `d`/`c`/`y` avec des objets texte. Consultez la [référence du mode éditeur Vim](/fr/interactive-mode#vim-editor-mode) pour la table de clés complète. Les motions Vim ne sont pas remappables via le fichier keybindings.

Appuyer sur Entrée soumet toujours votre invite en mode INSERT, contrairement à Vim standard. Utilisez `o` ou `O` en mode NORMAL, ou Ctrl+J, pour insérer un saut de ligne à la place.

## Ressources connexes

* [Mode interactif](/fr/interactive-mode) : référence complète des raccourcis clavier et table de clés Vim
* [Keybindings](/fr/keybindings) : remappez n'importe quel raccourci Claude Code, y compris Entrée et Maj+Entrée
* [Rendu en plein écran](/fr/fullscreen) : détails sur le défilement, la recherche et la copie en mode plein écran
* [Guide des hooks](/fr/hooks-guide) : plus d'exemples de hooks Notification pour Linux et Windows
* [Dépannage](/fr/troubleshooting) : corrections pour les problèmes en dehors de la configuration du terminal
