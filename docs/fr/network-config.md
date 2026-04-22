> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuration réseau d'entreprise

> Configurez Claude Code pour les environnements d'entreprise avec des serveurs proxy, des autorités de certification (CA) personnalisées et l'authentification mutuelle Transport Layer Security (mTLS).

Claude Code prend en charge diverses configurations réseau et de sécurité d'entreprise via des variables d'environnement. Cela inclut le routage du trafic via des serveurs proxy d'entreprise, la confiance envers des autorités de certification (CA) personnalisées et l'authentification avec des certificats mTLS (Transport Layer Security mutuel) pour une sécurité renforcée.

<Note>
  Toutes les variables d'environnement affichées sur cette page peuvent également être configurées dans [`settings.json`](/fr/settings).
</Note>

## Configuration du proxy

### Variables d'environnement

Claude Code respecte les variables d'environnement proxy standard :

```bash theme={null}
# Proxy HTTPS (recommandé)
export HTTPS_PROXY=https://proxy.example.com:8080

# Proxy HTTP (si HTTPS non disponible)
export HTTP_PROXY=http://proxy.example.com:8080

# Contourner le proxy pour des requêtes spécifiques - format séparé par des espaces
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# Contourner le proxy pour des requêtes spécifiques - format séparé par des virgules
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# Contourner le proxy pour toutes les requêtes
export NO_PROXY="*"
```

<Note>
  Claude Code ne prend pas en charge les proxies SOCKS.
</Note>

### Authentification basique

Si votre proxy nécessite une authentification basique, incluez les identifiants dans l'URL du proxy :

```bash theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  Évitez de coder en dur les mots de passe dans les scripts. Utilisez plutôt des variables d'environnement ou un stockage sécurisé des identifiants.
</Warning>

<Tip>
  Pour les proxies nécessitant une authentification avancée (NTLM, Kerberos, etc.), envisagez d'utiliser un service LLM Gateway qui prend en charge votre méthode d'authentification.
</Tip>

## Magasin de certificats CA

Par défaut, Claude Code fait confiance à la fois aux certificats CA Mozilla fournis avec le produit et au magasin de certificats de votre système d'exploitation. Les proxies d'inspection TLS d'entreprise tels que CrowdStrike Falcon et Zscaler fonctionnent sans configuration supplémentaire lorsque leur certificat racine est installé dans le magasin de confiance du système d'exploitation.

<Note>
  L'intégration du magasin CA système nécessite la distribution binaire native de Claude Code. Lors de l'exécution sur le runtime Node.js, le magasin CA système n'est pas fusionné automatiquement. Dans ce cas, définissez `NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem` pour approuver une CA racine d'entreprise.
</Note>

`CLAUDE_CODE_CERT_STORE` accepte une liste séparée par des virgules de sources. Les valeurs reconnues sont `bundled` pour l'ensemble de certificats CA Mozilla fourni avec Claude Code et `system` pour le magasin de confiance du système d'exploitation. La valeur par défaut est `bundled,system`.

Pour approuver uniquement l'ensemble de certificats CA Mozilla fourni :

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=bundled
```

Pour approuver uniquement le magasin de certificats du système d'exploitation :

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=system
```

<Note>
  `CLAUDE_CODE_CERT_STORE` n'a pas de clé de schéma dédiée dans `settings.json`. Définissez-la via le bloc `env` dans `~/.claude/settings.json` ou directement dans l'environnement du processus.
</Note>

## Certificats CA personnalisés

Si votre environnement d'entreprise utilise une CA personnalisée, configurez Claude Code pour la faire confiance directement :

```bash theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## Authentification mTLS

Pour les environnements d'entreprise nécessitant une authentification par certificat client :

```bash theme={null}
# Certificat client pour l'authentification
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Clé privée du client
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Optionnel : phrase de passe pour la clé privée chiffrée
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## Exigences d'accès réseau

Claude Code nécessite l'accès aux URL suivantes :

* `api.anthropic.com` : points de terminaison de l'API Claude
* `claude.ai` : authentification pour les comptes claude.ai
* `platform.claude.com` : authentification pour les comptes Anthropic Console

Assurez-vous que ces URL sont autorisées dans votre configuration proxy et vos règles de pare-feu. C'est particulièrement important lors de l'utilisation de Claude Code dans des environnements réseau conteneurisés ou restreints.

Lors de l'utilisation de [Bedrock](/fr/amazon-bedrock), [Vertex AI](/fr/google-vertex-ai), ou [Foundry](/fr/microsoft-foundry), le trafic du modèle va vers votre fournisseur au lieu de `api.anthropic.com`. L'outil WebFetch appelle toujours `api.anthropic.com` pour sa [vérification de sécurité du domaine](/fr/data-usage#webfetch-domain-safety-check) sauf si vous définissez `skipWebFetchPreflight: true` dans les [paramètres](/fr/settings).

L'installateur natif et les vérifications de mise à jour nécessitent également les URL suivantes. Autorisez les deux, car les clients exécutant des versions plus anciennes de Claude Code téléchargent depuis `storage.googleapis.com`. Si vous installez Claude Code via npm ou gérez votre propre distribution binaire, les utilisateurs finaux n'auront peut-être pas besoin d'accès :

* `downloads.claude.ai` : hôte de téléchargement pour le binaire Claude Code, la mise à jour automatique, les pointeurs de version, les manifestes, le script d'installation, les clés de signature et les exécutables de plugins
* `storage.googleapis.com` : hôte de téléchargement hérité utilisé par les clients plus anciens

L'[intégration Chrome](/fr/chrome) se connecte à l'extension de navigateur via un pont WebSocket. Si vous utilisez Claude dans Chrome, autorisez `bridge.claudeusercontent.com` pour les connexions WebSocket sortantes.

[Claude Code sur le web](/fr/claude-code-on-the-web) et [Code Review](/fr/code-review) se connectent à vos référentiels à partir de l'infrastructure gérée par Anthropic. Si votre organisation GitHub Enterprise Cloud restreint l'accès par adresse IP, activez [l'héritage de la liste d'autorisation IP pour les applications GitHub installées](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps). L'application GitHub Claude enregistre ses plages d'adresses IP, donc l'activation de ce paramètre permet l'accès sans configuration manuelle. Pour [ajouter les plages à votre liste d'autorisation manuellement](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address) à la place, ou pour configurer d'autres pare-feu, consultez les [adresses IP de l'API Anthropic](https://platform.claude.com/docs/en/api/ip-addresses).

Pour les instances [GitHub Enterprise Server](/fr/github-enterprise-server) auto-hébergées derrière un pare-feu, autorisez les mêmes [adresses IP de l'API Anthropic](https://platform.claude.com/docs/en/api/ip-addresses) afin que l'infrastructure Anthropic puisse accéder à votre hôte GHES pour cloner les référentiels et publier les commentaires d'examen.

## Ressources supplémentaires

* [Paramètres Claude Code](/fr/settings)
* [Référence des variables d'environnement](/fr/env-vars)
* [Guide de dépannage](/fr/troubleshooting)
