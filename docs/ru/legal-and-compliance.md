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

# Правовые и нормативные требования

> Правовые соглашения, сертификаты соответствия и информация о безопасности для Claude Code.

## Правовые соглашения

### Лицензия

Ваше использование Claude Code подчиняется:

* [Коммерческие условия](https://www.anthropic.com/legal/commercial-terms) - для пользователей Team, Enterprise и Claude API
* [Условия обслуживания для потребителей](https://www.anthropic.com/legal/consumer-terms) - для пользователей Free, Pro и Max

### Коммерческие соглашения

Независимо от того, используете ли вы Claude API напрямую (1P) или получаете доступ через AWS Bedrock или Google Vertex (3P), ваше существующее коммерческое соглашение будет применяться к использованию Claude Code, если мы не договорились об ином.

## Соответствие нормативным требованиям

### Соответствие требованиям здравоохранения (BAA)

Если у клиента есть соглашение о деловом партнере (BAA) с нами и он хочет использовать Claude Code, BAA автоматически распространится на Claude Code, если клиент заключил BAA и активировал [Zero Data Retention (ZDR)](/ru/zero-data-retention). BAA будет применяться к трафику API этого клиента, проходящему через Claude Code. ZDR включается на основе организации, поэтому каждая организация должна иметь отдельно включенный ZDR, чтобы быть охваченной BAA.

## Политика использования

### Допустимое использование

Использование Claude Code подчиняется [Политике использования Anthropic](https://www.anthropic.com/legal/aup). Объявленные ограничения использования для планов Pro и Max предполагают обычное индивидуальное использование Claude Code и Agent SDK.

### Аутентификация и использование учетных данных

Claude Code аутентифицируется на серверах Anthropic с использованием токенов OAuth или ключей API. Эти методы аутентификации служат разным целям:

* **Аутентификация OAuth** (используется с планами Free, Pro и Max) предназначена исключительно для Claude Code и Claude.ai. Использование токенов OAuth, полученных через учетные записи Claude Free, Pro или Max, в любом другом продукте, инструменте или сервисе — включая [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) — не разрешено и представляет собой нарушение [Условий обслуживания для потребителей](https://www.anthropic.com/legal/consumer-terms).
* **Разработчики**, создающие продукты или сервисы, которые взаимодействуют с возможностями Claude, включая те, которые используют [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview), должны использовать аутентификацию по ключу API через [Claude Console](https://platform.claude.com/) или поддерживаемого облачного провайдера. Anthropic не разрешает сторонним разработчикам предлагать вход Claude.ai или маршрутизировать запросы через учетные данные планов Free, Pro или Max от имени своих пользователей.

Anthropic оставляет за собой право принимать меры для обеспечения соблюдения этих ограничений и может делать это без предварительного уведомления.

По вопросам о разрешенных методах аутентификации для вашего случая использования, пожалуйста, [свяжитесь с отделом продаж](https://www.anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=legal_compliance_contact_sales).

## Безопасность и доверие

### Доверие и безопасность

Вы можете найти дополнительную информацию в [Центре доверия Anthropic](https://trust.anthropic.com) и [Центре прозрачности](https://www.anthropic.com/transparency).

### Отчетность об уязвимостях безопасности

Anthropic управляет нашей программой безопасности через HackerOne. [Используйте эту форму для отчета об уязвимостях](https://hackerone.com/anthropic-vdp/reports/new?type=team\&report_type=vulnerability).

***

© Anthropic PBC. Все права защищены. Использование подчиняется применимым Условиям обслуживания Anthropic.
