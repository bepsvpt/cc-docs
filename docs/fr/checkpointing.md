> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Checkpointing

> Suivez automatiquement et annulez les modifications de Claude pour récupérer rapidement des changements indésirables.

Claude Code suit automatiquement les modifications de fichiers effectuées par Claude au fur et à mesure que vous travaillez, ce qui vous permet d'annuler rapidement les modifications et de revenir à des états antérieurs si quelque chose s'écarte de la trajectoire.

## Fonctionnement des checkpoints

Au fur et à mesure que vous travaillez avec Claude, le checkpointing capture automatiquement l'état de votre code avant chaque modification. Ce filet de sécurité vous permet de poursuivre des tâches ambitieuses et à grande échelle en sachant que vous pouvez toujours revenir à un état de code antérieur.

### Suivi automatique

Claude Code suit tous les changements effectués par ses outils d'édition de fichiers :

* Chaque message utilisateur crée un nouveau checkpoint
* Les checkpoints persistent entre les sessions, vous pouvez donc y accéder dans les conversations reprises
* Nettoyés automatiquement avec les sessions après 30 jours (configurable)

### Annulation des modifications

Appuyez sur `Esc` deux fois (`Esc` + `Esc`) ou utilisez la commande `/rewind` pour ouvrir le menu d'annulation. Vous pouvez choisir de restaurer :

* **Conversation uniquement** : Annulez jusqu'à un message utilisateur tout en conservant les modifications de code
* **Code uniquement** : Annulez les modifications de fichiers tout en conservant la conversation
* **Code et conversation** : Restaurez les deux à un point antérieur de la session

## Cas d'usage courants

Les checkpoints sont particulièrement utiles lorsque :

* **Explorer des alternatives** : Essayez différentes approches d'implémentation sans perdre votre point de départ
* **Récupérer après des erreurs** : Annulez rapidement les modifications qui ont introduit des bugs ou cassé des fonctionnalités
* **Itérer sur les fonctionnalités** : Expérimentez des variations en sachant que vous pouvez revenir à des états fonctionnels

## Limitations

### Les modifications de commandes Bash ne sont pas suivies

Le checkpointing ne suit pas les fichiers modifiés par les commandes bash. Par exemple, si Claude Code exécute :

```bash  theme={null}
rm file.txt
mv old.txt new.txt
cp source.txt dest.txt
```

Ces modifications de fichiers ne peuvent pas être annulées via l'annulation. Seules les modifications de fichiers directes effectuées via les outils d'édition de fichiers de Claude sont suivies.

### Les modifications externes ne sont pas suivies

Le checkpointing suit uniquement les fichiers qui ont été modifiés au cours de la session actuelle. Les modifications manuelles que vous apportez aux fichiers en dehors de Claude Code et les modifications d'autres sessions concurrentes ne sont normalement pas capturées, sauf si elles modifient les mêmes fichiers que la session actuelle.

### Pas un remplacement du contrôle de version

Les checkpoints sont conçus pour une récupération rapide au niveau de la session. Pour un historique de version permanent et la collaboration :

* Continuez à utiliser le contrôle de version (ex. Git) pour les commits, les branches et l'historique à long terme
* Les checkpoints complètent mais ne remplacent pas le contrôle de version approprié
* Pensez aux checkpoints comme « annulation locale » et à Git comme « historique permanent »

## Voir aussi

* [Mode interactif](/fr/interactive-mode) - Raccourcis clavier et contrôles de session
* [Commandes intégrées](/fr/interactive-mode#built-in-commands) - Accès aux checkpoints via `/rewind`
* [Référence CLI](/fr/cli-reference) - Options de ligne de commande
