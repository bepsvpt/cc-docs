> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Checkpointing

> Suivez, rembobinez et résumez les modifications et la conversation de Claude pour gérer l'état de la session.

Claude Code suit automatiquement les modifications de fichiers effectuées par Claude au fur et à mesure que vous travaillez, ce qui vous permet d'annuler rapidement les modifications et de revenir à des états antérieurs si quelque chose s'écarte de la trajectoire.

## Comment fonctionne le checkpointing

Au fur et à mesure que vous travaillez avec Claude, le checkpointing capture automatiquement l'état de votre code avant chaque modification. Ce filet de sécurité vous permet de poursuivre des tâches ambitieuses et à grande échelle en sachant que vous pouvez toujours revenir à un état de code antérieur.

### Suivi automatique

Claude Code suit toutes les modifications apportées par ses outils d'édition de fichiers :

* Chaque invite utilisateur crée un nouveau checkpoint
* Les checkpoints persistent entre les sessions, vous pouvez donc y accéder dans les conversations reprises
* Nettoyés automatiquement avec les sessions après 30 jours (configurable)

### Rembobiner et résumer

Appuyez sur `Esc` deux fois (`Esc` + `Esc`) ou utilisez la commande `/rewind` pour ouvrir le menu de rembobinage. Une liste déroulante affiche chacune de vos invites de la session. Sélectionnez le point sur lequel vous souhaitez agir, puis choisissez une action :

* **Restaurer le code et la conversation** : revenir au code et à la conversation à ce moment
* **Restaurer la conversation** : rembobiner jusqu'à ce message tout en conservant le code actuel
* **Restaurer le code** : annuler les modifications de fichiers tout en conservant la conversation
* **Résumer à partir d'ici** : compresser la conversation à partir de ce moment en avant dans un résumé, libérant de l'espace de context window
* **Annuler** : revenir à la liste des messages sans apporter de modifications

Après la restauration de la conversation ou la résumé, l'invite originale du message sélectionné est restaurée dans le champ de saisie afin que vous puissiez la renvoyer ou la modifier.

#### Restaurer vs. résumer

Les trois options de restauration annulent l'état : elles annulent les modifications de code, l'historique de conversation, ou les deux. « Résumer à partir d'ici » fonctionne différemment :

* Les messages avant le message sélectionné restent intacts
* Le message sélectionné et tous les messages suivants sont remplacés par un résumé compact généré par l'IA
* Aucun fichier sur le disque n'est modifié
* Les messages originaux sont conservés dans la transcription de session, afin que Claude puisse référencer les détails si nécessaire

C'est similaire à `/compact`, mais ciblé : au lieu de résumer l'ensemble de la conversation, vous conservez le contexte initial en détail complet et ne compressez que les parties qui utilisent de l'espace. Vous pouvez taper des instructions optionnelles pour guider sur quoi le résumé se concentre.

<Note>
  Résumer vous garde dans la même session et compresse le contexte. Si vous souhaitez vous brancher et essayer une approche différente tout en préservant la session originale intacte, utilisez plutôt [fork](/fr/how-claude-code-works#resume-or-fork-sessions) (`claude --continue --fork-session`).
</Note>

## Cas d'usage courants

Les checkpoints sont particulièrement utiles quand :

* **Explorer les alternatives** : essayez différentes approches d'implémentation sans perdre votre point de départ
* **Récupérer des erreurs** : annulez rapidement les modifications qui ont introduit des bugs ou cassé des fonctionnalités
* **Itérer sur les fonctionnalités** : expérimentez des variations en sachant que vous pouvez revenir à des états fonctionnels
* **Libérer de l'espace de contexte** : résumez une session de débogage verbeuse à partir du point médian en avant, en conservant vos instructions initiales intactes

## Limitations

### Les modifications de commandes Bash ne sont pas suivies

Le checkpointing ne suit pas les fichiers modifiés par les commandes bash. Par exemple, si Claude Code exécute :

```bash theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

Ces modifications de fichiers ne peuvent pas être annulées via le rembobinage. Seules les modifications de fichiers directs effectuées via les outils d'édition de fichiers de Claude sont suivies.

### Les modifications externes ne sont pas suivies

Le checkpointing suit uniquement les fichiers qui ont été modifiés au cours de la session actuelle. Les modifications manuelles que vous apportez aux fichiers en dehors de Claude Code et les modifications d'autres sessions concurrentes ne sont normalement pas capturées, sauf si elles modifient par hasard les mêmes fichiers que la session actuelle.

### Pas un remplacement du contrôle de version

Les checkpoints sont conçus pour une récupération rapide au niveau de la session. Pour un historique de version permanent et la collaboration :

* Continuez à utiliser le contrôle de version (ex. Git) pour les commits, les branches et l'historique à long terme
* Les checkpoints complètent mais ne remplacent pas le contrôle de version approprié
* Pensez aux checkpoints comme « annulation locale » et à Git comme « historique permanent »

## Voir aussi

* [Mode interactif](/fr/interactive-mode) - Raccourcis clavier et contrôles de session
* [Commandes intégrées](/fr/commands) - Accès aux checkpoints en utilisant `/rewind`
* [Référence CLI](/fr/cli-reference) - Options de ligne de commande
