> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Démarrer avec l'application de bureau

> Installez Claude Code sur le bureau et commencez votre première session de codage

L'application de bureau vous donne accès à Claude Code avec une interface graphique : examen des différences visuelles, aperçu en direct de l'application, surveillance des PR GitHub avec fusion automatique, sessions parallèles avec isolation Git worktree, tâches planifiées et la possibilité d'exécuter des tâches à distance. Aucun terminal requis.

Cette page vous guide dans l'installation de l'application et le démarrage de votre première session. Si vous êtes déjà configuré, consultez [Utiliser Claude Code Desktop](/fr/desktop) pour la référence complète.

<Frame>
  <img src="https://mintcdn.com/claude-code/CNLUpFGiXoc9mhvD/images/desktop-code-tab-light.png?fit=max&auto=format&n=CNLUpFGiXoc9mhvD&q=85&s=9a36a7a27b9f4c6f2e1c83bdb34f69ce" className="block dark:hidden" alt="L'interface Claude Code Desktop montrant l'onglet Code sélectionné, avec une boîte de saisie, un sélecteur de mode de permission défini sur Demander les permissions, un sélecteur de modèle, un sélecteur de dossier et l'option Environnement local" width="2500" height="1376" data-path="images/desktop-code-tab-light.png" />

  <img src="https://mintcdn.com/claude-code/CNLUpFGiXoc9mhvD/images/desktop-code-tab-dark.png?fit=max&auto=format&n=CNLUpFGiXoc9mhvD&q=85&s=5463defe81c459fb9b1f91f6a958cfb8" className="hidden dark:block" alt="L'interface Claude Code Desktop en mode sombre montrant l'onglet Code sélectionné, avec une boîte de saisie, un sélecteur de mode de permission défini sur Demander les permissions, un sélecteur de modèle, un sélecteur de dossier et l'option Environnement local" width="2504" height="1374" data-path="images/desktop-code-tab-dark.png" />
</Frame>

L'application de bureau a trois onglets :

* **Chat** : Conversation générale sans accès aux fichiers, similaire à claude.ai.
* **Cowork** : Un agent autonome en arrière-plan qui travaille sur des tâches dans une VM cloud avec son propre environnement. Il peut fonctionner indépendamment pendant que vous faites autre chose.
* **Code** : Un assistant de codage interactif avec accès direct à vos fichiers locaux. Vous examinez et approuvez chaque modification en temps réel.

Chat et Cowork sont couverts dans les [articles d'assistance Claude Desktop](https://support.claude.com/en/collections/16163169-claude-desktop). Cette page se concentre sur l'onglet **Code**.

<Note>
  Claude Code nécessite un [abonnement Pro, Max, Teams ou Enterprise](https://claude.com/pricing).
</Note>

## Installer

<Steps>
  <Step title="Télécharger l'application">
    Téléchargez Claude pour votre plateforme.

    <CardGroup cols={2}>
      <Card title="macOS" icon="apple" href="https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs">
        Build universel pour Intel et Apple Silicon
      </Card>

      <Card title="Windows" icon="windows" href="https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs">
        Pour les processeurs x64
      </Card>
    </CardGroup>

    Pour Windows ARM64, [téléchargez ici](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs).

    Linux n'est actuellement pas supporté.
  </Step>

  <Step title="Se connecter">
    Lancez Claude à partir de votre dossier Applications (macOS) ou du menu Démarrer (Windows). Connectez-vous avec votre compte Anthropic.
  </Step>

  <Step title="Ouvrir l'onglet Code">
    Cliquez sur l'onglet **Code** en haut au centre. Si cliquer sur Code vous invite à mettre à niveau, vous devez d'abord [vous abonner à un plan payant](https://claude.com/pricing). S'il vous invite à vous connecter en ligne, complétez la connexion et redémarrez l'application. Si vous voyez une erreur 403, consultez [dépannage de l'authentification](/fr/desktop#403-or-authentication-errors-in-the-code-tab).
  </Step>
</Steps>

L'application de bureau inclut Claude Code. Vous n'avez pas besoin d'installer Node.js ou la CLI séparément. Pour utiliser `claude` depuis le terminal, installez la CLI séparément. Consultez [Démarrer avec la CLI](/fr/quickstart).

## Commencer votre première session

Avec l'onglet Code ouvert, choisissez un projet et donnez à Claude quelque chose à faire.

<Steps>
  <Step title="Choisir un environnement et un dossier">
    Sélectionnez **Local** pour exécuter Claude sur votre machine en utilisant vos fichiers directement. Cliquez sur **Sélectionner le dossier** et choisissez votre répertoire de projet.

    <Tip>
      Commencez par un petit projet que vous connaissez bien. C'est le moyen le plus rapide de voir ce que Claude Code peut faire. Sur Windows, [Git](https://git-scm.com/downloads/win) doit être installé pour que les sessions locales fonctionnent. La plupart des Mac incluent Git par défaut.
    </Tip>

    Vous pouvez également sélectionner :

    * **Remote** : Exécutez les sessions sur l'infrastructure cloud d'Anthropic qui continue même si vous fermez l'application. Les sessions distantes utilisent la même infrastructure que [Claude Code sur le web](/fr/claude-code-on-the-web).
    * **SSH** : Connectez-vous à une machine distante via SSH (vos propres serveurs, VM cloud ou conteneurs de développement). Claude Code doit être installé sur la machine distante.
  </Step>

  <Step title="Choisir un modèle">
    Sélectionnez un modèle dans la liste déroulante à côté du bouton d'envoi. Consultez [modèles](/fr/model-config#available-models) pour une comparaison d'Opus, Sonnet et Haiku. Vous ne pouvez pas changer le modèle après le démarrage de la session.
  </Step>

  <Step title="Dire à Claude ce qu'il faut faire">
    Tapez ce que vous voulez que Claude fasse :

    * `Trouver un commentaire TODO et le corriger`
    * `Ajouter des tests pour la fonction principale`
    * `Créer un CLAUDE.md avec des instructions pour cette base de code`

    Une [session](/fr/desktop#work-in-parallel-with-sessions) est une conversation avec Claude sur votre code. Chaque session suit son propre contexte et ses modifications, vous pouvez donc travailler sur plusieurs tâches sans qu'elles n'interfèrent les unes avec les autres.
  </Step>

  <Step title="Examiner et accepter les modifications">
    Par défaut, l'onglet Code démarre en [mode Demander les permissions](/fr/desktop#choose-a-permission-mode), où Claude propose des modifications et attend votre approbation avant de les appliquer. Vous verrez :

    1. Une [vue de différence](/fr/desktop#review-changes-with-diff-view) montrant exactement ce qui changera dans chaque fichier
    2. Des boutons Accepter/Rejeter pour approuver ou refuser chaque modification
    3. Des mises à jour en temps réel pendant que Claude travaille sur votre demande

    Si vous rejetez une modification, Claude vous demandera comment vous aimeriez procéder différemment. Vos fichiers ne sont pas modifiés tant que vous n'acceptez pas.
  </Step>
</Steps>

## Et maintenant ?

Vous avez fait votre première modification. Pour la référence complète sur tout ce que Desktop peut faire, consultez [Utiliser Claude Code Desktop](/fr/desktop). Voici quelques choses à essayer ensuite.

**Interrompre et diriger.** Vous pouvez interrompre Claude à tout moment. S'il prend la mauvaise direction, cliquez sur le bouton d'arrêt ou tapez votre correction et appuyez sur **Entrée**. Claude arrête ce qu'il fait et s'ajuste en fonction de votre entrée. Vous n'avez pas besoin d'attendre qu'il finisse ou de recommencer.

**Donner à Claude plus de contexte.** Tapez `@filename` dans la boîte de saisie pour extraire un fichier spécifique dans la conversation, joignez des images et des PDF en utilisant le bouton de pièce jointe, ou glissez-déposez des fichiers directement dans la saisie. Plus Claude a de contexte, meilleurs sont les résultats. Consultez [Ajouter des fichiers et du contexte](/fr/desktop#add-files-and-context-to-prompts).

**Utiliser les skills pour les tâches répétables.** Tapez `/` ou cliquez sur **+** → **Slash commands** pour parcourir les [commandes intégrées](/fr/interactive-mode#built-in-commands), les [skills personnalisés](/fr/skills) et les skills de plugin. Les skills sont des invites réutilisables que vous pouvez invoquer chaque fois que vous en avez besoin, comme des listes de contrôle d'examen de code ou des étapes de déploiement.

**Examiner les modifications avant de valider.** Après que Claude modifie les fichiers, un indicateur `+12 -1` apparaît. Cliquez dessus pour ouvrir la [vue de différence](/fr/desktop#review-changes-with-diff-view), examinez les modifications fichier par fichier et commentez des lignes spécifiques. Claude lit vos commentaires et révise. Cliquez sur **Examiner le code** pour que Claude évalue lui-même les différences et laisse des suggestions en ligne.

**Ajuster le contrôle que vous avez.** Votre [mode de permission](/fr/desktop#choose-a-permission-mode) contrôle l'équilibre. Demander les permissions (par défaut) nécessite une approbation avant chaque modification. Auto accept edits accepte automatiquement les modifications de fichiers pour une itération plus rapide. Plan mode permet à Claude de cartographier une approche sans toucher à aucun fichier, ce qui est utile avant une grande refonte.

**Ajouter des plugins pour plus de capacités.** Cliquez sur le bouton **+** à côté de la boîte de saisie et sélectionnez **Plugins** pour parcourir et installer des [plugins](/fr/desktop#install-plugins) qui ajoutent des skills, des agents, des MCP servers et plus.

**Prévisualiser votre application.** Cliquez sur la liste déroulante **Preview** pour exécuter votre serveur de développement directement dans le bureau. Claude peut voir l'application en cours d'exécution, tester les points de terminaison, inspecter les journaux et itérer sur ce qu'il voit. Consultez [Prévisualiser votre application](/fr/desktop#preview-your-app).

**Suivre votre demande de tirage.** Après avoir ouvert une PR, Claude Code surveille les résultats des vérifications CI et peut corriger automatiquement les défaillances ou fusionner la PR une fois que toutes les vérifications sont réussies. Consultez [Surveiller l'état de la demande de tirage](/fr/desktop#monitor-pull-request-status).

**Mettre Claude sur un calendrier.** Configurez des [tâches planifiées](/fr/desktop#schedule-recurring-tasks) pour exécuter Claude automatiquement de manière récurrente : un examen de code quotidien chaque matin, un audit de dépendances hebdomadaire ou un briefing qui extrait de vos outils connectés.

**Augmenter l'échelle quand vous êtes prêt.** Ouvrez des [sessions parallèles](/fr/desktop#work-in-parallel-with-sessions) à partir de la barre latérale pour travailler sur plusieurs tâches à la fois, chacune dans son propre Git worktree. Envoyez des [travaux de longue durée vers le cloud](/fr/desktop#run-long-running-tasks-remotely) pour qu'ils continuent même si vous fermez l'application, ou [continuez une session sur le web ou dans votre IDE](/fr/desktop#continue-in-another-surface) si une tâche prend plus de temps que prévu. [Connectez des outils externes](/fr/desktop#extend-claude-code) comme GitHub, Slack et Linear pour réunir votre flux de travail.

## Venant de la CLI ?

Desktop exécute le même moteur que la CLI avec une interface graphique. Vous pouvez exécuter les deux simultanément sur le même projet, et ils partagent la configuration (fichiers CLAUDE.md, MCP servers, hooks, skills et paramètres). Pour une comparaison complète des fonctionnalités, des équivalents de drapeaux et de ce qui n'est pas disponible dans Desktop, consultez [Comparaison CLI](/fr/desktop#coming-from-the-cli).

## Prochaines étapes

* [Utiliser Claude Code Desktop](/fr/desktop) : modes de permission, sessions parallèles, vue de différence, connecteurs et configuration d'entreprise
* [Dépannage](/fr/desktop#troubleshooting) : solutions aux erreurs courantes et problèmes de configuration
* [Meilleures pratiques](/fr/best-practices) : conseils pour rédiger des invites efficaces et tirer le meilleur parti de Claude Code
* [Flux de travail courants](/fr/common-workflows) : tutoriels pour le débogage, la refonte, les tests et plus
