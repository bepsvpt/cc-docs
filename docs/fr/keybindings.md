> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Personnaliser les raccourcis clavier

> Personnalisez les raccourcis clavier dans Claude Code avec un fichier de configuration des liaisons de touches.

<Note>
  Les raccourcis clavier personnalisables nécessitent Claude Code v2.1.18 ou version ultérieure. Vérifiez votre version avec `claude --version`.
</Note>

Claude Code prend en charge les raccourcis clavier personnalisables. Exécutez `/keybindings` pour créer ou ouvrir votre fichier de configuration à `~/.claude/keybindings.json`.

## Fichier de configuration

Le fichier de configuration des liaisons de touches est un objet avec un tableau `bindings`. Chaque bloc spécifie un contexte et une carte des séquences de touches aux actions.

<Note>Les modifications du fichier keybindings sont automatiquement détectées et appliquées sans redémarrer Claude Code.</Note>

| Champ      | Description                                                     |
| :--------- | :-------------------------------------------------------------- |
| `$schema`  | URL du schéma JSON optionnel pour l'autocomplétion de l'éditeur |
| `$docs`    | URL de documentation optionnelle                                |
| `bindings` | Tableau de blocs de liaison par contexte                        |

Cet exemple lie `Ctrl+E` pour ouvrir un éditeur externe dans le contexte de chat, et délié `Ctrl+U` :

```json  theme={null}
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/fr/keybindings",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null
      }
    }
  ]
}
```

## Contextes

Chaque bloc de liaison spécifie un **contexte** où les liaisons s'appliquent :

| Contexte          | Description                                                           |
| :---------------- | :-------------------------------------------------------------------- |
| `Global`          | S'applique partout dans l'application                                 |
| `Chat`            | Zone de saisie de chat principale                                     |
| `Autocomplete`    | Le menu d'autocomplétion est ouvert                                   |
| `Settings`        | Menu des paramètres                                                   |
| `Confirmation`    | Dialogues de permission et de confirmation                            |
| `Tabs`            | Composants de navigation par onglets                                  |
| `Help`            | Le menu d'aide est visible                                            |
| `Transcript`      | Visionneuse de transcription                                          |
| `HistorySearch`   | Mode de recherche d'historique (Ctrl+R)                               |
| `Task`            | Une tâche de fond est en cours d'exécution                            |
| `ThemePicker`     | Dialogue du sélecteur de thème                                        |
| `Attachments`     | Navigation de la pièce jointe d'image dans les dialogues de sélection |
| `Footer`          | Navigation de l'indicateur de pied de page (tâches, équipes, diff)    |
| `MessageSelector` | Sélection de message du dialogue de rembobinage et de résumé          |
| `DiffDialog`      | Navigation de la visionneuse de diff                                  |
| `ModelPicker`     | Niveau d'effort du sélecteur de modèle                                |
| `Select`          | Composants génériques de sélection/liste                              |
| `Plugin`          | Dialogue du plugin (parcourir, découvrir, gérer)                      |

## Actions disponibles

Les actions suivent un format `namespace:action`, tel que `chat:submit` pour envoyer un message ou `app:toggleTodos` pour afficher la liste des tâches. Chaque contexte a des actions spécifiques disponibles.

### Actions d'application

Actions disponibles dans le contexte `Global` :

| Action                 | Par défaut | Description                                   |
| :--------------------- | :--------- | :-------------------------------------------- |
| `app:interrupt`        | Ctrl+C     | Annuler l'opération en cours                  |
| `app:exit`             | Ctrl+D     | Quitter Claude Code                           |
| `app:redraw`           | Ctrl+L     | Redessiner l'écran                            |
| `app:toggleTodos`      | Ctrl+T     | Basculer la visibilité de la liste des tâches |
| `app:toggleTranscript` | Ctrl+O     | Basculer la transcription détaillée           |

### Actions d'historique

Actions pour naviguer dans l'historique des commandes :

| Action             | Par défaut | Description                      |
| :----------------- | :--------- | :------------------------------- |
| `history:search`   | Ctrl+R     | Ouvrir la recherche d'historique |
| `history:previous` | Haut       | Élément d'historique précédent   |
| `history:next`     | Bas        | Élément d'historique suivant     |

### Actions de chat

Actions disponibles dans le contexte `Chat` :

| Action                | Par défaut                  | Description                               |
| :-------------------- | :-------------------------- | :---------------------------------------- |
| `chat:cancel`         | Échappement                 | Annuler l'entrée actuelle                 |
| `chat:killAgents`     | Ctrl+X Ctrl+K               | Arrêter tous les agents de fond           |
| `chat:cycleMode`      | Maj+Tab\*                   | Cycler les modes de permission            |
| `chat:modelPicker`    | Cmd+P / Meta+P              | Ouvrir le sélecteur de modèle             |
| `chat:fastMode`       | Meta+O                      | Basculer le mode rapide                   |
| `chat:thinkingToggle` | Cmd+T / Meta+T              | Basculer la réflexion étendue             |
| `chat:submit`         | Entrée                      | Soumettre le message                      |
| `chat:newline`        | (non lié)                   | Insérer une nouvelle ligne sans soumettre |
| `chat:undo`           | Ctrl+\_, Ctrl+Maj+-         | Annuler la dernière action                |
| `chat:externalEditor` | Ctrl+G, Ctrl+X Ctrl+E       | Ouvrir dans un éditeur externe            |
| `chat:stash`          | Ctrl+S                      | Mettre en cache l'invite actuelle         |
| `chat:imagePaste`     | Ctrl+V (Alt+V sous Windows) | Coller une image                          |

\*Sous Windows sans mode VT (Node \<24.2.0/\<22.17.0, Bun \<1.2.23), la valeur par défaut est Meta+M.

### Actions d'autocomplétion

Actions disponibles dans le contexte `Autocomplete` :

| Action                  | Par défaut  | Description            |
| :---------------------- | :---------- | :--------------------- |
| `autocomplete:accept`   | Tab         | Accepter la suggestion |
| `autocomplete:dismiss`  | Échappement | Fermer le menu         |
| `autocomplete:previous` | Haut        | Suggestion précédente  |
| `autocomplete:next`     | Bas         | Suggestion suivante    |

### Actions de confirmation

Actions disponibles dans le contexte `Confirmation` :

| Action                      | Par défaut     | Description                          |
| :-------------------------- | :------------- | :----------------------------------- |
| `confirm:yes`               | Y, Entrée      | Confirmer l'action                   |
| `confirm:no`                | N, Échappement | Refuser l'action                     |
| `confirm:previous`          | Haut           | Option précédente                    |
| `confirm:next`              | Bas            | Option suivante                      |
| `confirm:nextField`         | Tab            | Champ suivant                        |
| `confirm:previousField`     | (non lié)      | Champ précédent                      |
| `confirm:toggle`            | Espace         | Basculer la sélection                |
| `confirm:cycleMode`         | Maj+Tab        | Cycler les modes de permission       |
| `confirm:toggleExplanation` | Ctrl+E         | Basculer l'explication de permission |

### Actions de permission

Actions disponibles dans le contexte `Confirmation` pour les dialogues de permission :

| Action                   | Par défaut | Description                                         |
| :----------------------- | :--------- | :-------------------------------------------------- |
| `permission:toggleDebug` | Ctrl+D     | Basculer les informations de débogage de permission |

### Actions de transcription

Actions disponibles dans le contexte `Transcript` :

| Action                     | Par défaut             | Description                             |
| :------------------------- | :--------------------- | :-------------------------------------- |
| `transcript:toggleShowAll` | Ctrl+E                 | Basculer l'affichage de tout le contenu |
| `transcript:exit`          | q, Ctrl+C, Échappement | Quitter la vue de transcription         |

### Actions de recherche d'historique

Actions disponibles dans le contexte `HistorySearch` :

| Action                  | Par défaut       | Description                       |
| :---------------------- | :--------------- | :-------------------------------- |
| `historySearch:next`    | Ctrl+R           | Correspondance suivante           |
| `historySearch:accept`  | Échappement, Tab | Accepter la sélection             |
| `historySearch:cancel`  | Ctrl+C           | Annuler la recherche              |
| `historySearch:execute` | Entrée           | Exécuter la commande sélectionnée |

### Actions de tâche

Actions disponibles dans le contexte `Task` :

| Action            | Par défaut | Description                              |
| :---------------- | :--------- | :--------------------------------------- |
| `task:background` | Ctrl+B     | Mettre la tâche actuelle en arrière-plan |

### Actions de thème

Actions disponibles dans le contexte `ThemePicker` :

| Action                           | Par défaut | Description                       |
| :------------------------------- | :--------- | :-------------------------------- |
| `theme:toggleSyntaxHighlighting` | Ctrl+T     | Basculer la coloration syntaxique |

### Actions d'aide

Actions disponibles dans le contexte `Help` :

| Action         | Par défaut  | Description           |
| :------------- | :---------- | :-------------------- |
| `help:dismiss` | Échappement | Fermer le menu d'aide |

### Actions d'onglets

Actions disponibles dans le contexte `Tabs` :

| Action          | Par défaut      | Description      |
| :-------------- | :-------------- | :--------------- |
| `tabs:next`     | Tab, Droite     | Onglet suivant   |
| `tabs:previous` | Maj+Tab, Gauche | Onglet précédent |

### Actions de pièces jointes

Actions disponibles dans le contexte `Attachments` :

| Action                 | Par défaut                | Description                              |
| :--------------------- | :------------------------ | :--------------------------------------- |
| `attachments:next`     | Droite                    | Pièce jointe suivante                    |
| `attachments:previous` | Gauche                    | Pièce jointe précédente                  |
| `attachments:remove`   | Retour arrière, Supprimer | Supprimer la pièce jointe sélectionnée   |
| `attachments:exit`     | Bas, Échappement          | Quitter la navigation des pièces jointes |

### Actions de pied de page

Actions disponibles dans le contexte `Footer` :

| Action                  | Par défaut  | Description                                                        |
| :---------------------- | :---------- | :----------------------------------------------------------------- |
| `footer:next`           | Droite      | Élément de pied de page suivant                                    |
| `footer:previous`       | Gauche      | Élément de pied de page précédent                                  |
| `footer:up`             | Haut        | Naviguer vers le haut dans le pied de page (désélectionne en haut) |
| `footer:down`           | Bas         | Naviguer vers le bas dans le pied de page                          |
| `footer:openSelected`   | Entrée      | Ouvrir l'élément de pied de page sélectionné                       |
| `footer:clearSelection` | Échappement | Effacer la sélection du pied de page                               |

### Actions du sélecteur de message

Actions disponibles dans le contexte `MessageSelector` :

| Action                   | Par défaut                            | Description                         |
| :----------------------- | :------------------------------------ | :---------------------------------- |
| `messageSelector:up`     | Haut, K, Ctrl+P                       | Déplacer vers le haut dans la liste |
| `messageSelector:down`   | Bas, J, Ctrl+N                        | Déplacer vers le bas dans la liste  |
| `messageSelector:top`    | Ctrl+Haut, Maj+Haut, Meta+Haut, Maj+K | Sauter au début                     |
| `messageSelector:bottom` | Ctrl+Bas, Maj+Bas, Meta+Bas, Maj+J    | Sauter à la fin                     |
| `messageSelector:select` | Entrée                                | Sélectionner le message             |

### Actions de diff

Actions disponibles dans le contexte `DiffDialog` :

| Action                | Par défaut               | Description                                    |
| :-------------------- | :----------------------- | :--------------------------------------------- |
| `diff:dismiss`        | Échappement              | Fermer la visionneuse de diff                  |
| `diff:previousSource` | Gauche                   | Source de diff précédente                      |
| `diff:nextSource`     | Droite                   | Source de diff suivante                        |
| `diff:previousFile`   | Haut                     | Fichier précédent dans le diff                 |
| `diff:nextFile`       | Bas                      | Fichier suivant dans le diff                   |
| `diff:viewDetails`    | Entrée                   | Afficher les détails du diff                   |
| `diff:back`           | (spécifique au contexte) | Revenir en arrière dans la visionneuse de diff |

### Actions du sélecteur de modèle

Actions disponibles dans le contexte `ModelPicker` :

| Action                       | Par défaut | Description                  |
| :--------------------------- | :--------- | :--------------------------- |
| `modelPicker:decreaseEffort` | Gauche     | Diminuer le niveau d'effort  |
| `modelPicker:increaseEffort` | Droite     | Augmenter le niveau d'effort |

### Actions de sélection

Actions disponibles dans le contexte `Select` :

| Action            | Par défaut      | Description           |
| :---------------- | :-------------- | :-------------------- |
| `select:next`     | Bas, J, Ctrl+N  | Option suivante       |
| `select:previous` | Haut, K, Ctrl+P | Option précédente     |
| `select:accept`   | Entrée          | Accepter la sélection |
| `select:cancel`   | Échappement     | Annuler la sélection  |

### Actions de plugin

Actions disponibles dans le contexte `Plugin` :

| Action           | Par défaut | Description                        |
| :--------------- | :--------- | :--------------------------------- |
| `plugin:toggle`  | Espace     | Basculer la sélection du plugin    |
| `plugin:install` | I          | Installer les plugins sélectionnés |

### Actions des paramètres

Actions disponibles dans le contexte `Settings` :

| Action            | Par défaut | Description                                                                                                        |
| :---------------- | :--------- | :----------------------------------------------------------------------------------------------------------------- |
| `settings:search` | /          | Entrer en mode de recherche                                                                                        |
| `settings:retry`  | R          | Réessayer de charger les données d'utilisation (en cas d'erreur)                                                   |
| `settings:close`  | Entrée     | Enregistrer les modifications et fermer le panneau de configuration. Échappement annule les modifications et ferme |

### Actions vocales

Actions disponibles dans le contexte `Chat` lorsque la [dictée vocale](/fr/voice-dictation) est activée :

| Action             | Par défaut | Description                      |
| :----------------- | :--------- | :------------------------------- |
| `voice:pushToTalk` | Espace     | Maintenez pour dicter une invite |

## Syntaxe des séquences de touches

### Modificateurs

Utilisez les touches de modification avec le séparateur `+` :

* `ctrl` ou `control` - Touche Contrôle
* `alt`, `opt`, ou `option` - Touche Alt/Option
* `shift` - Touche Maj
* `meta`, `cmd`, ou `command` - Touche Meta/Commande

Par exemple :

```text  theme={null}
ctrl+k          Touche unique avec modificateur
shift+tab       Maj + Tab
meta+p          Commande/Meta + P
ctrl+shift+c    Plusieurs modificateurs
```

### Lettres majuscules

Une lettre majuscule autonome implique Maj. Par exemple, `K` est équivalent à `shift+k`. Ceci est utile pour les liaisons de style vim où les touches majuscules et minuscules ont des significations différentes.

Les lettres majuscules avec des modificateurs (par exemple, `ctrl+K`) sont traitées comme stylistiques et n'impliquent **pas** Maj — `ctrl+K` est identique à `ctrl+k`.

### Accords

Les accords sont des séquences de touches séparées par des espaces :

```text  theme={null}
ctrl+k ctrl+s   Appuyez sur Ctrl+K, relâchez, puis Ctrl+S
```

### Touches spéciales

* `escape` ou `esc` - Touche Échappement
* `enter` ou `return` - Touche Entrée
* `tab` - Touche Tab
* `space` - Barre d'espace
* `up`, `down`, `left`, `right` - Touches fléchées
* `backspace`, `delete` - Touches de suppression

## Délier les raccourcis par défaut

Définissez une action sur `null` pour délier un raccourci par défaut :

```json  theme={null}
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+s": null
      }
    }
  ]
}
```

Cela fonctionne également pour les liaisons d'accords. Délier tous les accords qui partagent un préfixe libère ce préfixe pour une utilisation comme liaison à touche unique :

```json  theme={null}
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+x ctrl+k": null,
        "ctrl+x ctrl+e": null,
        "ctrl+x": "chat:newline"
      }
    }
  ]
}
```

Si vous déliez certains accords mais pas tous sur un préfixe, appuyer sur le préfixe entre toujours en mode d'attente d'accord pour les liaisons restantes.

## Raccourcis réservés

Ces raccourcis ne peuvent pas être reliés :

| Raccourci | Raison                                                       |
| :-------- | :----------------------------------------------------------- |
| Ctrl+C    | Interruption/annulation codée en dur                         |
| Ctrl+D    | Sortie codée en dur                                          |
| Ctrl+M    | Identique à Entrée dans les terminaux (les deux envoient CR) |

## Conflits de terminal

Certains raccourcis peuvent entrer en conflit avec les multiplexeurs de terminal :

| Raccourci | Conflit                                       |
| :-------- | :-------------------------------------------- |
| Ctrl+B    | Préfixe tmux (appuyez deux fois pour envoyer) |
| Ctrl+A    | Préfixe GNU screen                            |
| Ctrl+Z    | Suspension de processus Unix (SIGTSTP)        |

## Interaction du mode Vim

Lorsque le mode vim est activé (`/vim`), les liaisons de touches et le mode vim fonctionnent indépendamment :

* **Mode Vim** gère l'entrée au niveau de la saisie de texte (mouvement du curseur, modes, motions)
* **Liaisons de touches** gèrent les actions au niveau du composant (basculer les tâches, soumettre, etc.)
* La touche Échappement en mode vim bascule INSERT en mode NORMAL ; elle ne déclenche pas `chat:cancel`
* La plupart des raccourcis Ctrl+touche passent par le mode vim au système de liaison de touches
* En mode NORMAL vim, `?` affiche le menu d'aide (comportement vim)

## Validation

Claude Code valide vos liaisons de touches et affiche des avertissements pour :

* Erreurs d'analyse (JSON invalide ou structure)
* Noms de contexte invalides
* Conflits de raccourcis réservés
* Conflits de multiplexeur de terminal
* Liaisons en double dans le même contexte

Exécutez `/doctor` pour voir les avertissements de liaison de touches.
