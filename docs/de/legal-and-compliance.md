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

# Rechtliche Bestimmungen und Compliance

> Rechtliche Vereinbarungen, Compliance-Zertifizierungen und Sicherheitsinformationen für Claude Code.

## Rechtliche Vereinbarungen

### Lizenz

Ihre Nutzung von Claude Code unterliegt:

* [Commercial Terms](https://www.anthropic.com/legal/commercial-terms) - für Team-, Enterprise- und Claude API-Nutzer
* [Consumer Terms of Service](https://www.anthropic.com/legal/consumer-terms) - für Free-, Pro- und Max-Nutzer

### Kommerzielle Vereinbarungen

Unabhängig davon, ob Sie die Claude API direkt (1P) nutzen oder über AWS Bedrock oder Google Vertex (3P) darauf zugreifen, gilt Ihre bestehende kommerzielle Vereinbarung für die Nutzung von Claude Code, sofern wir nicht etwas anderes gegenseitig vereinbart haben.

## Compliance

### Healthcare-Compliance (BAA)

Wenn ein Kunde eine Business Associate Agreement (BAA) mit uns hat und Claude Code nutzen möchte, wird die BAA automatisch auf Claude Code ausgeweitet, wenn der Kunde eine BAA abgeschlossen hat und [Zero Data Retention (ZDR)](/de/zero-data-retention) aktiviert hat. Die BAA gilt für den API-Datenverkehr dieses Kunden, der durch Claude Code fließt. ZDR wird auf Organisationsebene aktiviert, daher muss jede Organisation ZDR separat aktivieren, um unter die BAA abgedeckt zu sein.

## Nutzungsrichtlinie

### Akzeptable Nutzung

Die Nutzung von Claude Code unterliegt der [Anthropic Usage Policy](https://www.anthropic.com/legal/aup). Die beworbenen Nutzungslimits für Pro- und Max-Pläne gehen von einer gewöhnlichen, individuellen Nutzung von Claude Code und dem Agent SDK aus.

### Authentifizierung und Anmeldedatenverwaltung

Claude Code authentifiziert sich bei Anthropic-Servern mit OAuth-Token oder API-Schlüsseln. Diese Authentifizierungsmethoden dienen unterschiedlichen Zwecken:

* **OAuth-Authentifizierung** (verwendet mit Free-, Pro- und Max-Plänen) ist ausschließlich für Claude Code und Claude.ai vorgesehen. Die Verwendung von OAuth-Token, die über Claude Free-, Pro- oder Max-Konten erhalten wurden, in einem anderen Produkt, Tool oder Service – einschließlich des [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) – ist nicht zulässig und stellt einen Verstoß gegen die [Consumer Terms of Service](https://www.anthropic.com/legal/consumer-terms) dar.
* **Entwickler**, die Produkte oder Services entwickeln, die mit Claudes Funktionen interagieren, einschließlich derjenigen, die das [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) nutzen, sollten API-Schlüssel-Authentifizierung über die [Claude Console](https://platform.claude.com/) oder einen unterstützten Cloud-Anbieter verwenden. Anthropic gestattet Drittentwicklern nicht, Claude.ai-Anmeldungen anzubieten oder Anfragen über Free-, Pro- oder Max-Plan-Anmeldedaten im Namen ihrer Nutzer weiterzuleiten.

Anthropic behält sich das Recht vor, Maßnahmen zur Durchsetzung dieser Einschränkungen zu ergreifen, und kann dies ohne vorherige Ankündigung tun.

Bei Fragen zu zulässigen Authentifizierungsmethoden für Ihren Anwendungsfall wenden Sie sich bitte an den [Vertrieb](https://www.anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=legal_compliance_contact_sales).

## Sicherheit und Vertrauen

### Vertrauen und Sicherheit

Weitere Informationen finden Sie im [Anthropic Trust Center](https://trust.anthropic.com) und im [Transparency Hub](https://www.anthropic.com/transparency).

### Meldung von Sicherheitslücken

Anthropic verwaltet unser Sicherheitsprogramm über HackerOne. [Verwenden Sie dieses Formular, um Sicherheitslücken zu melden](https://hackerone.com/anthropic-vdp/reports/new?type=team\&report_type=vulnerability).

***

© Anthropic PBC. Alle Rechte vorbehalten. Die Nutzung unterliegt den geltenden Anthropic Terms of Service.
