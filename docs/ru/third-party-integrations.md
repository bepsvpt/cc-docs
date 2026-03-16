> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Обзор развертывания в масштабе предприятия

> Узнайте, как Claude Code может интегрироваться с различными сторонними сервисами и инфраструктурой для соответствия требованиям развертывания в масштабе предприятия.

На этой странице представлен обзор доступных вариантов развертывания и помощь в выборе правильной конфигурации для вашей организации.

## Сравнение поставщиков

<table>
  <thead>
    <tr>
      <th>Функция</th>
      <th>Anthropic</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Регионы</td>
      <td>Поддерживаемые [страны](https://www.anthropic.com/supported-countries)</td>
      <td>Несколько AWS [регионов](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)</td>
      <td>Несколько GCP [регионов](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)</td>
      <td>Несколько Azure [регионов](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)</td>
    </tr>

    <tr>
      <td>Кэширование подсказок</td>
      <td>Включено по умолчанию</td>
      <td>Включено по умолчанию</td>
      <td>Включено по умолчанию</td>
      <td>Включено по умолчанию</td>
    </tr>

    <tr>
      <td>Аутентификация</td>
      <td>Ключ API</td>
      <td>Ключ API или учетные данные AWS</td>
      <td>Учетные данные GCP</td>
      <td>Ключ API или Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>Отслеживание затрат</td>
      <td>Панель управления</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
      <td>Azure Cost Management</td>
    </tr>

    <tr>
      <td>Функции предприятия</td>
      <td>Команды, мониторинг использования</td>
      <td>Политики IAM, CloudTrail</td>
      <td>Роли IAM, Cloud Audit Logs</td>
      <td>Политики RBAC, Azure Monitor</td>
    </tr>
  </tbody>
</table>

## Облачные поставщики

<CardGroup cols={3}>
  <Card title="Amazon Bedrock" icon="aws" href="/ru/amazon-bedrock">
    Используйте модели Claude через инфраструктуру AWS с аутентификацией на основе ключа API или IAM и мониторингом, встроенным в AWS
  </Card>

  <Card title="Google Vertex AI" icon="google" href="/ru/google-vertex-ai">
    Получайте доступ к моделям Claude через Google Cloud Platform с безопасностью и соответствием требованиям корпоративного уровня
  </Card>

  <Card title="Microsoft Foundry" icon="microsoft" href="/ru/microsoft-foundry">
    Получайте доступ к Claude через Azure с аутентификацией на основе ключа API или Microsoft Entra ID и выставлением счетов Azure
  </Card>
</CardGroup>

## Корпоративная инфраструктура

<CardGroup cols={2}>
  <Card title="Enterprise Network" icon="shield" href="/ru/network-config">
    Настройте Claude Code для работы с прокси-серверами вашей организации и требованиями SSL/TLS
  </Card>

  <Card title="LLM Gateway" icon="server" href="/ru/llm-gateway">
    Разверните централизованный доступ к моделям с отслеживанием использования, бюджетированием и логированием аудита
  </Card>
</CardGroup>

## Обзор конфигурации

Claude Code поддерживает гибкие параметры конфигурации, которые позволяют вам комбинировать различные поставщиков и инфраструктуру:

<Note>
  Поймите разницу между:

  * **Корпоративный прокси**: HTTP/HTTPS прокси для маршрутизации трафика (установлен через `HTTPS_PROXY` или `HTTP_PROXY`)
  * **LLM Gateway**: Сервис, который обрабатывает аутентификацию и предоставляет совместимые с поставщиком конечные точки (установлен через `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL` или `ANTHROPIC_VERTEX_BASE_URL`)

  Обе конфигурации можно использовать одновременно.
</Note>

### Использование Bedrock с корпоративным прокси

Маршрутизируйте трафик Bedrock через корпоративный HTTP/HTTPS прокси:

```bash  theme={null}
# Включить Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

# Настроить корпоративный прокси
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Использование Bedrock с LLM Gateway

Используйте сервис шлюза, который предоставляет совместимые с Bedrock конечные точки:

```bash  theme={null}
# Включить Bedrock
export CLAUDE_CODE_USE_BEDROCK=1

# Настроить LLM gateway
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # Если шлюз обрабатывает аутентификацию AWS
```

### Использование Foundry с корпоративным прокси

Маршрутизируйте трафик Azure через корпоративный HTTP/HTTPS прокси:

```bash  theme={null}
# Включить Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1
export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # Или опустите для аутентификации Entra ID

# Настроить корпоративный прокси
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Использование Foundry с LLM Gateway

Используйте сервис шлюза, который предоставляет совместимые с Azure конечные точки:

```bash  theme={null}
# Включить Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# Настроить LLM gateway
export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # Если шлюз обрабатывает аутентификацию Azure
```

### Использование Vertex AI с корпоративным прокси

Маршрутизируйте трафик Vertex AI через корпоративный HTTP/HTTPS прокси:

```bash  theme={null}
# Включить Vertex
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

# Настроить корпоративный прокси
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### Использование Vertex AI с LLM Gateway

Комбинируйте модели Google Vertex AI с LLM gateway для централизованного управления:

```bash  theme={null}
# Включить Vertex
export CLAUDE_CODE_USE_VERTEX=1

# Настроить LLM gateway
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # Если шлюз обрабатывает аутентификацию GCP
```

### Конфигурация аутентификации

Claude Code использует `ANTHROPIC_AUTH_TOKEN` для заголовка `Authorization` при необходимости. Флаги `SKIP_AUTH` (`CLAUDE_CODE_SKIP_BEDROCK_AUTH`, `CLAUDE_CODE_SKIP_VERTEX_AUTH`) используются в сценариях LLM gateway, где шлюз обрабатывает аутентификацию поставщика.

## Выбор правильной конфигурации развертывания

Рассмотрите эти факторы при выборе подхода к развертыванию:

### Прямой доступ к поставщику

Лучше всего для организаций, которые:

* Хотят самую простую настройку
* Имеют существующую инфраструктуру AWS или GCP
* Нуждаются в мониторинге и соответствии требованиям, встроенных в поставщика

### Корпоративный прокси

Лучше всего для организаций, которые:

* Имеют существующие требования корпоративного прокси
* Нуждаются в мониторинге трафика и соответствии требованиям
* Должны маршрутизировать весь трафик через определенные сетевые пути

### LLM Gateway

Лучше всего для организаций, которые:

* Нуждаются в отслеживании использования по командам
* Хотят динамически переключаться между моделями
* Требуют пользовательское ограничение скорости или бюджеты
* Нуждаются в централизованном управлении аутентификацией

## Отладка

При отладке вашего развертывания:

* Используйте команду `claude /status` [slash command](/ru/slash-commands). Эта команда обеспечивает видимость в любые применяемые параметры аутентификации, прокси и URL.
* Установите переменную окружения `export ANTHROPIC_LOG=debug` для логирования запросов.

## Лучшие практики для организаций

### 1. Инвестируйте в документацию и память

Мы настоятельно рекомендуем инвестировать в документацию, чтобы Claude Code понимал вашу кодовую базу. Организации могут развертывать файлы CLAUDE.md на нескольких уровнях:

* **На уровне организации**: Разверните в системные директории, такие как `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) для стандартов компании
* **На уровне репозитория**: Создайте файлы `CLAUDE.md` в корнях репозиториев, содержащие архитектуру проекта, команды сборки и рекомендации по внесению вклада. Проверьте их в систему управления версиями, чтобы все пользователи получили выгоду

  [Узнайте больше](/ru/memory).

### 2. Упростите развертывание

Если у вас есть пользовательская среда разработки, мы считаем, что создание "одного клика" способа установки Claude Code является ключом к расширению внедрения по всей организации.

### 3. Начните с управляемого использования

Поощряйте новых пользователей попробовать Claude Code для вопросов и ответов по кодовой базе или на более мелких исправлениях ошибок или запросах функций. Попросите Claude Code составить план. Проверьте предложения Claude и дайте обратную связь, если это неправильно. Со временем, по мере того как пользователи лучше поймут эту новую парадигму, они будут более эффективны в том, чтобы позволить Claude Code работать более агентивно.

### 4. Настройте политики безопасности

Команды безопасности могут настроить управляемые разрешения для того, что Claude Code может и не может делать, которые не могут быть переопределены локальной конфигурацией. [Узнайте больше](/ru/security).

### 5. Используйте MCP для интеграций

MCP - это отличный способ дать Claude Code больше информации, например подключение к системам управления билетами или журналам ошибок. Мы рекомендуем, чтобы одна центральная команда настроила серверы MCP и проверила конфигурацию `.mcp.json` в кодовую базу, чтобы все пользователи получили выгоду. [Узнайте больше](/ru/mcp).

В Anthropic мы доверяем Claude Code для питания разработки во всей кодовой базе Anthropic. Мы надеемся, что вам понравится использовать Claude Code так же, как и нам.

## Следующие шаги

* [Настройте Amazon Bedrock](/ru/amazon-bedrock) для развертывания, встроенного в AWS
* [Настройте Google Vertex AI](/ru/google-vertex-ai) для развертывания GCP
* [Настройте Microsoft Foundry](/ru/microsoft-foundry) для развертывания Azure
* [Настройте Enterprise Network](/ru/network-config) для требований сети
* [Разверните LLM Gateway](/ru/llm-gateway) для управления предприятием
* [Параметры](/ru/settings) для параметров конфигурации и переменных окружения
