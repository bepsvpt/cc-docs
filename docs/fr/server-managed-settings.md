> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurer les paramètres gérés par le serveur (bêta publique)

> Configurez centralement Claude Code pour votre organisation via des paramètres livrés par le serveur, sans nécessiter d'infrastructure de gestion des appareils.

Les paramètres gérés par le serveur permettent aux administrateurs de configurer centralement Claude Code via une interface web sur Claude.ai. Les clients Claude Code reçoivent automatiquement ces paramètres lorsque les utilisateurs s'authentifient avec leurs identifiants d'organisation.

Cette approche est conçue pour les organisations qui n'ont pas d'infrastructure de gestion des appareils en place, ou qui ont besoin de gérer les paramètres pour les utilisateurs sur des appareils non gérés.

<Note>
  Les paramètres gérés par le serveur sont en bêta publique et disponibles pour les clients [Claude for Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_teams#team-&-enterprise) et [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_enterprise). Les fonctionnalités peuvent évoluer avant la disponibilité générale.
</Note>

## Conditions requises

Pour utiliser les paramètres gérés par le serveur, vous avez besoin de :

* Un plan Claude for Teams ou Claude for Enterprise
* Claude Code version 2.1.38 ou ultérieure pour Claude for Teams, ou version 2.1.30 ou ultérieure pour Claude for Enterprise
* Un accès réseau à `api.anthropic.com`

## Choisir entre les paramètres gérés par le serveur et gérés par le point de terminaison

Claude Code prend en charge deux approches pour la configuration centralisée. Les paramètres gérés par le serveur livrent la configuration à partir des serveurs d'Anthropic. Les [paramètres gérés par le point de terminaison](/fr/settings#settings-files) sont déployés directement sur les appareils via des stratégies natives du système d'exploitation (préférences gérées macOS, registre Windows) ou des fichiers de paramètres gérés.

| Approche                                                                        | Idéal pour                                                          | Modèle de sécurité                                                                                                                         |
| :------------------------------------------------------------------------------ | :------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------------- |
| **Paramètres gérés par le serveur**                                             | Organisations sans MDM, ou utilisateurs sur des appareils non gérés | Paramètres livrés à partir des serveurs d'Anthropic au moment de l'authentification                                                        |
| **[Paramètres gérés par le point de terminaison](/fr/settings#settings-files)** | Organisations avec MDM ou gestion des points de terminaison         | Paramètres déployés sur les appareils via des profils de configuration MDM, des stratégies de registre ou des fichiers de paramètres gérés |

Si vos appareils sont inscrits dans une solution MDM ou de gestion des points de terminaison, les paramètres gérés par le point de terminaison offrent des garanties de sécurité plus fortes car le fichier de paramètres peut être protégé contre les modifications de l'utilisateur au niveau du système d'exploitation.

## Configurer les paramètres gérés par le serveur

<Steps>
  <Step title="Ouvrir la console d'administration">
    Dans [Claude.ai](https://claude.ai), accédez à **Admin Settings > Claude Code > Managed settings**.
  </Step>

  <Step title="Définir vos paramètres">
    Ajoutez votre configuration en JSON. Tous les [paramètres disponibles dans `settings.json`](/fr/settings#available-settings) sont pris en charge, y compris les [paramètres réservés à la gestion](/fr/permissions#managed-only-settings) comme `disableBypassPermissionsMode`.

    Cet exemple applique une liste de refus de permissions et empêche les utilisateurs de contourner les permissions :

    ```json  theme={null}
    {
      "permissions": {
        "deny": [
          "Bash(curl *)",
          "Read(./.env)",
          "Read(./.env.*)",
          "Read(./secrets/**)"
        ],
        "disableBypassPermissionsMode": "disable"
      }
    }
    ```
  </Step>

  <Step title="Enregistrer et déployer">
    Enregistrez vos modifications. Les clients Claude Code reçoivent les paramètres mis à jour au prochain démarrage ou lors du cycle d'interrogation horaire.
  </Step>
</Steps>

### Vérifier la livraison des paramètres

Pour confirmer que les paramètres sont appliqués, demandez à un utilisateur de redémarrer Claude Code. Si la configuration inclut des paramètres qui déclenchent la [boîte de dialogue d'approbation de sécurité](#security-approval-dialogs), l'utilisateur voit une invite décrivant les paramètres gérés au démarrage. Vous pouvez également vérifier que les règles de permission gérées sont actives en demandant à un utilisateur d'exécuter `/permissions` pour afficher ses règles de permission effectives.

### Contrôle d'accès

Les rôles suivants peuvent gérer les paramètres gérés par le serveur :

* **Propriétaire principal**
* **Propriétaire**

Limitez l'accès au personnel de confiance, car les modifications de paramètres s'appliquent à tous les utilisateurs de l'organisation.

### Limitations actuelles

Les paramètres gérés par le serveur ont les limitations suivantes pendant la période bêta :

* Les paramètres s'appliquent uniformément à tous les utilisateurs de l'organisation. Les configurations par groupe ne sont pas encore prises en charge.
* Les [configurations de serveur MCP](/fr/mcp#managed-mcp-configuration) ne peuvent pas être distribuées via les paramètres gérés par le serveur.

## Livraison des paramètres

### Précédence des paramètres

Les paramètres gérés par le serveur et les [paramètres gérés par le point de terminaison](/fr/settings#settings-files) occupent tous deux le niveau le plus élevé dans la [hiérarchie des paramètres](/fr/settings#settings-precedence) de Claude Code. Aucun autre niveau de paramètres ne peut les remplacer, y compris les arguments de ligne de commande. Lorsque les deux sont présents, les paramètres gérés par le serveur ont la priorité et les paramètres gérés par le point de terminaison ne sont pas utilisés.

### Comportement de récupération et de mise en cache

Claude Code récupère les paramètres à partir des serveurs d'Anthropic au démarrage et interroge les mises à jour toutes les heures pendant les sessions actives.

**Premier lancement sans paramètres en cache :**

* Claude Code récupère les paramètres de manière asynchrone
* Si la récupération échoue, Claude Code continue sans paramètres gérés
* Il y a une brève fenêtre avant le chargement des paramètres où les restrictions ne sont pas encore appliquées

**Lancements ultérieurs avec paramètres en cache :**

* Les paramètres en cache s'appliquent immédiatement au démarrage
* Claude Code récupère les paramètres actualisés en arrière-plan
* Les paramètres en cache persistent en cas de défaillance réseau

Claude Code applique les mises à jour des paramètres automatiquement sans redémarrage, sauf pour les paramètres avancés comme la configuration OpenTelemetry, qui nécessitent un redémarrage complet pour prendre effet.

### Boîtes de dialogue d'approbation de sécurité

Certains paramètres qui pourraient présenter des risques de sécurité nécessitent une approbation explicite de l'utilisateur avant d'être appliqués :

* **Paramètres de commande shell** : paramètres qui exécutent des commandes shell
* **Variables d'environnement personnalisées** : variables ne figurant pas dans la liste de sécurité connue
* **Configurations de hook** : toute définition de hook

Lorsque ces paramètres sont présents, les utilisateurs voient une boîte de dialogue de sécurité expliquant ce qui est configuré. Les utilisateurs doivent approuver pour continuer. Si un utilisateur rejette les paramètres, Claude Code se ferme.

<Note>
  En mode non interactif avec l'indicateur `-p`, Claude Code ignore les boîtes de dialogue de sécurité et applique les paramètres sans approbation de l'utilisateur.
</Note>

## Disponibilité de la plateforme

Les paramètres gérés par le serveur nécessitent une connexion directe à `api.anthropic.com` et ne sont pas disponibles lors de l'utilisation de fournisseurs de modèles tiers :

* Amazon Bedrock
* Google Vertex AI
* Microsoft Foundry
* Points de terminaison API personnalisés via `ANTHROPIC_BASE_URL` ou [passerelles LLM](/fr/llm-gateway)

## Journalisation d'audit

Les événements du journal d'audit pour les modifications de paramètres sont disponibles via l'API de conformité ou l'export du journal d'audit. Contactez votre équipe de compte Anthropic pour accéder.

Les événements d'audit incluent le type d'action effectuée, le compte et l'appareil qui ont effectué l'action, et les références aux valeurs précédentes et nouvelles.

## Considérations de sécurité

Les paramètres gérés par le serveur fournissent une application de stratégie centralisée, mais ils fonctionnent comme un contrôle côté client. Sur les appareils non gérés, les utilisateurs ayant un accès administrateur ou sudo peuvent modifier le binaire Claude Code, le système de fichiers ou la configuration réseau.

| Scénario                                                            | Comportement                                                                                                                                            |
| :------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| L'utilisateur modifie le fichier de paramètres en cache             | Le fichier falsifié s'applique au démarrage, mais les paramètres corrects se restaurent lors de la prochaine récupération du serveur                    |
| L'utilisateur supprime le fichier de paramètres en cache            | Le comportement du premier lancement se produit : les paramètres sont récupérés de manière asynchrone avec une brève fenêtre non appliquée              |
| L'API est indisponible                                              | Les paramètres en cache s'appliquent s'ils sont disponibles, sinon les paramètres gérés ne sont pas appliqués jusqu'à la prochaine récupération réussie |
| L'utilisateur s'authentifie avec une organisation différente        | Les paramètres ne sont pas livrés pour les comptes en dehors de l'organisation gérée                                                                    |
| L'utilisateur définit un `ANTHROPIC_BASE_URL` non défini par défaut | Les paramètres gérés par le serveur sont contournés lors de l'utilisation de fournisseurs d'API tiers                                                   |

Pour détecter les modifications de configuration au moment de l'exécution, utilisez les [hooks `ConfigChange`](/fr/hooks#configchange) pour enregistrer les modifications ou bloquer les modifications non autorisées avant qu'elles ne prennent effet.

Pour des garanties d'application plus fortes, utilisez les [paramètres gérés par le point de terminaison](/fr/settings#settings-files) sur les appareils inscrits dans une solution MDM.

## Voir aussi

Pages connexes pour gérer la configuration de Claude Code :

* [Paramètres](/fr/settings) : référence de configuration complète incluant tous les paramètres disponibles
* [Paramètres gérés par le point de terminaison](/fr/settings#settings-files) : paramètres gérés déployés sur les appareils par l'informatique
* [Authentification](/fr/authentication) : configurer l'accès des utilisateurs à Claude Code
* [Sécurité](/fr/security) : garanties de sécurité et meilleures pratiques
