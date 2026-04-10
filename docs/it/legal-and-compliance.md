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

# Aspetti legali e conformità

> Accordi legali, certificazioni di conformità e informazioni sulla sicurezza per Claude Code.

## Accordi legali

### Licenza

L'utilizzo di Claude Code è soggetto a:

* [Termini commerciali](https://www.anthropic.com/legal/commercial-terms) - per gli utenti di Team, Enterprise e Claude API
* [Termini di servizio per i consumatori](https://www.anthropic.com/legal/consumer-terms) - per gli utenti di Free, Pro e Max

### Accordi commerciali

Che stiate utilizzando l'API Claude direttamente (1P) o accedendovi tramite AWS Bedrock o Google Vertex (3P), il vostro accordo commerciale esistente si applicherà all'utilizzo di Claude Code, a meno che non abbiate concordato diversamente.

## Conformità

### Conformità sanitaria (BAA)

Se un cliente ha un Business Associate Agreement (BAA) con noi e desidera utilizzare Claude Code, il BAA si estenderà automaticamente per coprire Claude Code se il cliente ha eseguito un BAA e ha [Zero Data Retention (ZDR)](/it/zero-data-retention) attivato. Il BAA sarà applicabile al traffico API di quel cliente che scorre attraverso Claude Code. ZDR è abilitato su base per organizzazione, quindi ogni organizzazione deve avere ZDR abilitato separatamente per essere coperta dal BAA.

## Politica di utilizzo

### Utilizzo accettabile

L'utilizzo di Claude Code è soggetto alla [Politica di utilizzo di Anthropic](https://www.anthropic.com/legal/aup). I limiti di utilizzo pubblicizzati per i piani Pro e Max presuppongono un utilizzo ordinario e individuale di Claude Code e dell'Agent SDK.

### Autenticazione e utilizzo delle credenziali

Claude Code si autentica con i server di Anthropic utilizzando token OAuth o chiavi API. Questi metodi di autenticazione servono a scopi diversi:

* **L'autenticazione OAuth** (utilizzata con i piani Free, Pro e Max) è destinata esclusivamente a Claude Code e Claude.ai. L'utilizzo di token OAuth ottenuti tramite account Claude Free, Pro o Max in qualsiasi altro prodotto, strumento o servizio — incluso l'[Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) — non è consentito e costituisce una violazione dei [Termini di servizio per i consumatori](https://www.anthropic.com/legal/consumer-terms).
* **Gli sviluppatori** che creano prodotti o servizi che interagiscono con le capacità di Claude, inclusi quelli che utilizzano l'[Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview), devono utilizzare l'autenticazione tramite chiave API tramite [Claude Console](https://platform.claude.com/) o un provider cloud supportato. Anthropic non consente ai sviluppatori di terze parti di offrire l'accesso a Claude.ai o di instradare le richieste tramite credenziali dei piani Free, Pro o Max per conto dei loro utenti.

Anthropic si riserva il diritto di adottare misure per far rispettare queste restrizioni e può farlo senza preavviso.

Per domande sui metodi di autenticazione consentiti per il vostro caso d'uso, vi preghiamo di [contattare il team di vendita](https://www.anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=legal_compliance_contact_sales).

## Sicurezza e fiducia

### Fiducia e sicurezza

Potete trovare ulteriori informazioni nel [Centro fiducia di Anthropic](https://trust.anthropic.com) e nell'[Hub di trasparenza](https://www.anthropic.com/transparency).

### Segnalazione di vulnerabilità di sicurezza

Anthropic gestisce il nostro programma di sicurezza tramite HackerOne. [Utilizzate questo modulo per segnalare vulnerabilità](https://hackerone.com/anthropic-vdp/reports/new?type=team\&report_type=vulnerability).

***

© Anthropic PBC. Tutti i diritti riservati. L'utilizzo è soggetto ai Termini di servizio di Anthropic applicabili.
