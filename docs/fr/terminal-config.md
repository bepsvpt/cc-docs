> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Optimisez votre configuration de terminal

> Claude Code fonctionne mieux lorsque votre terminal est correctement configuré. Suivez ces directives pour optimiser votre expérience.

### Thèmes et apparence

Claude ne peut pas contrôler le thème de votre terminal. C'est géré par votre application de terminal. Vous pouvez faire correspondre le thème de Claude Code à votre terminal à tout moment via la commande `/config`.

Pour une personnalisation supplémentaire de l'interface Claude Code elle-même, vous pouvez configurer une [ligne d'état personnalisée](/fr/statusline) pour afficher des informations contextuelles comme le modèle actuel, le répertoire de travail ou la branche git en bas de votre terminal.

### Sauts de ligne

Vous avez plusieurs options pour entrer des sauts de ligne dans Claude Code :

* **Échappement rapide** : Tapez `\` suivi d'Entrée pour créer une nouvelle ligne
* **Maj+Entrée** : Fonctionne directement dans iTerm2, WezTerm, Ghostty et Kitty
* **Raccourci clavier** : Configurez une liaison de clavier pour insérer une nouvelle ligne dans d'autres terminaux

**Configurez Maj+Entrée pour d'autres terminaux**

Exécutez `/terminal-setup` dans Claude Code pour configurer automatiquement Maj+Entrée pour VS Code, Alacritty, Zed et Warp.

<Note>
  La commande `/terminal-setup` n'est visible que dans les terminaux qui nécessitent une configuration manuelle. Si vous utilisez iTerm2, WezTerm, Ghostty ou Kitty, vous ne verrez pas cette commande car Maj+Entrée fonctionne déjà nativement.
</Note>

**Configurez Option+Entrée (VS Code, iTerm2 ou macOS Terminal.app)**

**Pour Mac Terminal.app :**

1. Ouvrez Paramètres → Profils → Clavier
2. Cochez « Utiliser Option comme touche Meta »

**Pour le terminal iTerm2 et VS Code :**

1. Ouvrez Paramètres → Profils → Touches
2. Sous Général, définissez la touche Option gauche/droite sur « Esc+ »

### Configuration des notifications

Lorsque Claude termine son travail et attend votre entrée, il déclenche un événement de notification. Vous pouvez afficher cet événement comme une notification de bureau via votre terminal ou exécuter une logique personnalisée avec des [hooks de notification](/fr/hooks#notification).

#### Notifications du terminal

Kitty et Ghostty prennent en charge les notifications de bureau sans configuration supplémentaire. iTerm 2 nécessite une configuration :

1. Ouvrez les Paramètres iTerm 2 → Profils → Terminal
2. Activez « Notification Center Alerts »
3. Cliquez sur « Filter Alerts » et cochez « Send escape sequence-generated alerts »

Si les notifications n'apparaissent pas, vérifiez que votre application de terminal dispose des autorisations de notification dans les paramètres de votre système d'exploitation.

Les autres terminaux, y compris le Terminal macOS par défaut, ne prennent pas en charge les notifications natives. Utilisez plutôt des [hooks de notification](/fr/hooks#notification).

#### Hooks de notification

Pour ajouter un comportement personnalisé lorsque les notifications se déclenchent, comme jouer un son ou envoyer un message, configurez un [hook de notification](/fr/hooks#notification). Les hooks s'exécutent aux côtés des notifications du terminal, pas en remplacement.

### Gestion des entrées volumineuses

Lorsque vous travaillez avec du code étendu ou des instructions longues :

* **Évitez le collage direct** : Claude Code peut avoir du mal avec du contenu très long collé
* **Utilisez des flux basés sur des fichiers** : Écrivez le contenu dans un fichier et demandez à Claude de le lire
* **Soyez conscient des limitations de VS Code** : Le terminal VS Code est particulièrement sujet à la troncature des longs collages

### Mode Vim

Claude Code supporte un sous-ensemble de liaisons de clavier Vim qui peut être activé avec `/vim` ou configuré via `/config`.

Le sous-ensemble supporté inclut :

* Changement de mode : `Esc` (vers NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (vers INSERT)
* Navigation : `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`, `f`/`F`/`t`/`T` avec répétition `;`/`,`
* Édition : `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (répétition)
* Copie/collage : `yy`/`Y`, `yw`/`ye`/`yb`, `p`/`P`
* Objets texte : `iw`/`aw`, `iW`/`aW`, `i"`/`a"`, `i'`/`a'`, `i(`/`a(`, `i[`/`a[`, `i{`/`a{`
* Indentation : `>>`/`<<`
* Opérations de ligne : `J` (fusionner les lignes)

Consultez [Mode interactif](/fr/interactive-mode#vim-editor-mode) pour la référence complète.
