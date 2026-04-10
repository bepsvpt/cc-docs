> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Aspects juridiques et conformité

> Accords juridiques, certifications de conformité et informations de sécurité pour Claude Code.

## Accords juridiques

### Licence

Votre utilisation de Claude Code est soumise à :

* [Conditions commerciales](https://www.anthropic.com/legal/commercial-terms) - pour les utilisateurs Team, Enterprise et Claude API
* [Conditions d'utilisation pour les consommateurs](https://www.anthropic.com/legal/consumer-terms) - pour les utilisateurs Free, Pro et Max

### Accords commerciaux

Que vous utilisiez l'API Claude directement (1P) ou y accédiez via AWS Bedrock ou Google Vertex (3P), votre accord commercial existant s'appliquera à l'utilisation de Claude Code, sauf si nous avons convenu autrement.

## Conformité

### Conformité aux normes de santé (BAA)

Si un client a un accord d'associé commercial (BAA) avec nous et souhaite utiliser Claude Code, le BAA s'étendra automatiquement pour couvrir Claude Code si le client a exécuté un BAA et a activé la [rétention zéro des données (ZDR)](/fr/zero-data-retention). Le BAA s'appliquera au trafic API de ce client transitant par Claude Code. ZDR est activé par organisation, donc chaque organisation doit avoir ZDR activé séparément pour être couverte par le BAA.

## Politique d'utilisation

### Utilisation acceptable

L'utilisation de Claude Code est soumise à la [politique d'utilisation d'Anthropic](https://www.anthropic.com/legal/aup). Les limites d'utilisation annoncées pour les plans Pro et Max supposent une utilisation ordinaire et individuelle de Claude Code et du SDK Agent.

### Authentification et utilisation des identifiants

Claude Code s'authentifie auprès des serveurs d'Anthropic en utilisant des jetons OAuth ou des clés API. Ces méthodes d'authentification servent des objectifs différents :

* **L'authentification OAuth** (utilisée avec les plans Free, Pro et Max) est destinée exclusivement à Claude Code et Claude.ai. L'utilisation de jetons OAuth obtenus via des comptes Claude Free, Pro ou Max dans tout autre produit, outil ou service — y compris le [SDK Agent](https://platform.claude.com/docs/en/agent-sdk/overview) — n'est pas autorisée et constitue une violation des [Conditions d'utilisation pour les consommateurs](https://www.anthropic.com/legal/consumer-terms).
* **Les développeurs** créant des produits ou services qui interagissent avec les capacités de Claude, y compris ceux utilisant le [SDK Agent](https://platform.claude.com/docs/en/agent-sdk/overview), doivent utiliser l'authentification par clé API via la [Console Claude](https://platform.claude.com/) ou un fournisseur cloud pris en charge. Anthropic n'autorise pas les développeurs tiers à proposer la connexion Claude.ai ou à acheminer les demandes via les identifiants des plans Free, Pro ou Max au nom de leurs utilisateurs.

Anthropic se réserve le droit de prendre des mesures pour appliquer ces restrictions et peut le faire sans préavis.

Pour des questions sur les méthodes d'authentification autorisées pour votre cas d'utilisation, veuillez [contacter l'équipe commerciale](https://www.anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=legal_compliance_contact_sales).

## Sécurité et confiance

### Confiance et sécurité

Vous pouvez trouver plus d'informations dans le [Centre de confiance d'Anthropic](https://trust.anthropic.com) et le [Hub de transparence](https://www.anthropic.com/transparency).

### Signalement des vulnérabilités de sécurité

Anthropic gère notre programme de sécurité via HackerOne. [Utilisez ce formulaire pour signaler les vulnérabilités](https://hackerone.com/anthropic-vdp/reports/new?type=team\&report_type=vulnerability).

***

© Anthropic PBC. Tous droits réservés. L'utilisation est soumise aux conditions d'utilisation applicables d'Anthropic.
