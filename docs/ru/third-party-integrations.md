> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Обзор корпоративного развертывания

> Узнайте, как Claude Code может интегрироваться с различными сторонними сервисами и инфраструктурой для удовлетворения требований корпоративного развертывания.

Организации могут развертывать Claude Code непосредственно через Anthropic или через поставщика облачных услуг. Эта страница поможет вам выбрать правильную конфигурацию.

## Сравнение вариантов развертывания

Для большинства организаций Claude for Teams или Claude for Enterprise обеспечивает лучший опыт. Члены команды получают доступ как к Claude Code, так и к Claude в веб-версии с одной подпиской, централизованным выставлением счетов и без необходимости настройки инфраструктуры.

**Claude for Teams** — это самообслуживаемое решение, которое включает функции сотрудничества, инструменты администратора и управление выставлением счетов. Лучше всего подходит для небольших команд, которым нужно быстро начать работу.

**Claude for Enterprise** добавляет SSO и захват домена, разрешения на основе ролей, доступ к API соответствия требованиям и управляемые параметры политики для развертывания конфигураций Claude Code на уровне организации. Лучше всего подходит для крупных организаций с требованиями безопасности и соответствия требованиям.

Узнайте больше о [планах Team](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) и [планах Enterprise](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan).

Если ваша организация имеет специфические требования к инфраструктуре, сравните варианты ниже:

<table>
  <thead>
    <tr>
      <th>Функция</th>
      <th>Claude for Teams/Enterprise</th>
      <th>Anthropic Console</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>Лучше всего подходит для</td>
      <td>Большинства организаций (рекомендуется)</td>
      <td>Отдельных разработчиков</td>
      <td>Развертываний, собственных для AWS</td>
      <td>Развертываний, собственных для GCP</td>
      <td>Развертываний, собственных для Azure</td>
    </tr>

    <tr>
      <td>Выставление счетов</td>
      <td><strong>Teams:</strong> \$150/место (Premium) с доступной оплатой по мере использования<br /><strong>Enterprise:</strong> <a href="https://claude.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=third_party_enterprise">Свяжитесь с отделом продаж</a></td>
      <td>Оплата по мере использования</td>
      <td>Оплата по мере использования через AWS</td>
      <td>Оплата по мере использования через GCP</td>
      <td>Оплата по мере использования через Azure</td>
    </tr>

    <tr>
      <td>Регионы</td>
      <td>Поддерживаемые [страны](https://www.anthropic.com/supported-countries)</td>
      <td>Поддерживаемые [страны](https://www.anthropic.com/supported-countries)</td>
      <td>Несколько AWS [регионов](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)</td>
      <td>Несколько GCP [регионов](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)</td>
      <td>Несколько Azure [регионов](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)</td>
    </tr>

    <tr>
      <td>prompt caching</td>
      <td>Включено по умолчанию</td>
      <td>Включено по умолчанию</td>
      <td>Включено по умолчанию</td>
      <td>Включено по умолчанию</td>
      <td>Включено по умолчанию</td>
    </tr>

    <tr>
      <td>Аутентификация</td>
      <td>Claude.ai SSO или электронная почта</td>
      <td>API ключ</td>
      <td>API ключ или учетные данные AWS</td>
      <td>Учетные данные GCP</td>
      <td>API ключ или Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>Отслеживание затрат</td>
      <td>Панель использования</td>
      <td>Панель использования</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
      <td>Azure Cost Management</td>
    </tr>

    <tr>
      <td>Включает Claude в веб-версии</td>
      <td>Да</td>
      <td>Нет</td>
      <td>Нет</td>
      <td>Нет</td>
      <td>Нет</td>
    </tr>

    <tr>
      <td>Функции Enterprise</td>
      <td>Управление командой, SSO, мониторинг использования</td>
      <td>Нет</td>
      <td>Политики IAM, CloudTrail</td>
      <td>Роли IAM, Cloud Audit Logs</td>
      <td>Политики RBAC, Azure Monitor</td>
    </tr>
  </tbody>
</table>

Выберите вариант развертывания для просмотра инструкций по настройке:

* [Claude for Teams или Enterprise](/ru/authentication#claude-for-teams-or-enterprise)
* [Anthropic Console](/ru/authentication#claude-console-authentication)
* [Amazon Bedrock](/ru/amazon-bedrock)
* [Google Vertex AI](/ru/google-vertex-ai)
* [Microsoft Foundry](/ru/microsoft-foundry)

## Настройка прокси и шлюзов

Большинство организаций могут использовать поставщика облачных услуг напрямую без дополнительной конфигурации. Однако вам может потребоваться настроить корпоративный прокси или шлюз LLM, если ваша организация имеет специфические требования к сети или управлению. Это разные конфигурации, которые можно использовать вместе:

* **Корпоративный прокси**: маршрутизирует трафик через прокси HTTP/HTTPS. Используйте это, если ваша организация требует, чтобы весь исходящий трафик проходил через прокси-сервер для мониторинга безопасности, соответствия требованиям или обеспечения политики сети. Настройте с помощью переменных окружения `HTTPS_PROXY` или `HTTP_PROXY`. Узнайте больше в разделе [Конфигурация корпоративной сети](/ru/network-config).
* **Шлюз LLM**: сервис, который находится между Claude Code и поставщиком облачных услуг для обработки аутентификации и маршрутизации. Используйте это, если вам нужно централизованное отслеживание использования между командами, пользовательское ограничение скорости или бюджеты, или централизованное управление аутентификацией. Настройте с помощью переменных окружения `ANTHROPIC_BASE_URL`, `ANTHROPIC_BEDROCK_BASE_URL` или `ANTHROPIC_VERTEX_BASE_URL`. Узнайте больше в разделе [Конфигурация шлюза LLM](/ru/llm-gateway).

Следующие примеры показывают переменные окружения для установки в вашей оболочке или профиле оболочки (`.bashrc`, `.zshrc`). См. раздел [Параметры](/ru/settings) для других методов конфигурации.

### Amazon Bedrock

<Tabs>
  <Tab title="Корпоративный прокси">
    Маршрутизируйте трафик Bedrock через ваш корпоративный прокси, установив следующие [переменные окружения](/ru/env-vars):

    ```bash theme={null}
    # Включить Bedrock
    export CLAUDE_CODE_USE_BEDROCK=1
    export AWS_REGION=us-east-1

    # Настроить корпоративный прокси
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="Шлюз LLM">
    Маршрутизируйте трафик Bedrock через ваш шлюз LLM, установив следующие [переменные окружения](/ru/env-vars):

    ```bash theme={null}
    # Включить Bedrock
    export CLAUDE_CODE_USE_BEDROCK=1

    # Настроить шлюз LLM
    export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
    export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # Если шлюз обрабатывает аутентификацию AWS
    ```
  </Tab>
</Tabs>

### Microsoft Foundry

<Tabs>
  <Tab title="Корпоративный прокси">
    Маршрутизируйте трафик Foundry через ваш корпоративный прокси, установив следующие [переменные окружения](/ru/env-vars):

    ```bash theme={null}
    # Включить Microsoft Foundry
    export CLAUDE_CODE_USE_FOUNDRY=1
    export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
    export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # Или опустите для аутентификации Entra ID

    # Настроить корпоративный прокси
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="Шлюз LLM">
    Маршрутизируйте трафик Foundry через ваш шлюз LLM, установив следующие [переменные окружения](/ru/env-vars):

    ```bash theme={null}
    # Включить Microsoft Foundry
    export CLAUDE_CODE_USE_FOUNDRY=1

    # Настроить шлюз LLM
    export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
    export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # Если шлюз обрабатывает аутентификацию Azure
    ```
  </Tab>
</Tabs>

### Google Vertex AI

<Tabs>
  <Tab title="Корпоративный прокси">
    Маршрутизируйте трафик Vertex AI через ваш корпоративный прокси, установив следующие [переменные окружения](/ru/env-vars):

    ```bash theme={null}
    # Включить Vertex
    export CLAUDE_CODE_USE_VERTEX=1
    export CLOUD_ML_REGION=us-east5
    export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

    # Настроить корпоративный прокси
    export HTTPS_PROXY='https://proxy.example.com:8080'
    ```
  </Tab>

  <Tab title="Шлюз LLM">
    Маршрутизируйте трафик Vertex AI через ваш шлюз LLM, установив следующие [переменные окружения](/ru/env-vars):

    ```bash theme={null}
    # Включить Vertex
    export CLAUDE_CODE_USE_VERTEX=1

    # Настроить шлюз LLM
    export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
    export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # Если шлюз обрабатывает аутентификацию GCP
    ```
  </Tab>
</Tabs>

<Tip>
  Используйте `/status` в Claude Code для проверки того, что конфигурация прокси и шлюза применена правильно.
</Tip>

## Лучшие практики для организаций

### Инвестируйте в документацию и память

Мы настоятельно рекомендуем инвестировать в документацию, чтобы Claude Code понимал вашу кодовую базу. Организации могут развертывать файлы CLAUDE.md на нескольких уровнях:

* **На уровне организации**: развертывайте в системные каталоги, такие как `/Library/Application Support/ClaudeCode/CLAUDE.md` (macOS) для стандартов компании
* **На уровне репозитория**: создавайте файлы `CLAUDE.md` в корнях репозиториев, содержащие архитектуру проекта, команды сборки и рекомендации по внесению вклада. Проверяйте их в систему контроля версий, чтобы все пользователи получали выгоду

Узнайте больше в разделе [Память и файлы CLAUDE.md](/ru/memory).

### Упростите развертывание

Если у вас есть пользовательская среда разработки, мы считаем, что создание "одноклик" способа установки Claude Code является ключом к расширению внедрения в организации.

### Начните с управляемого использования

Поощряйте новых пользователей попробовать Claude Code для вопросов и ответов по кодовой базе, или на небольших исправлениях ошибок или запросах функций. Попросите Claude Code составить план. Проверьте предложения Claude и дайте обратную связь, если что-то не так. Со временем, по мере того как пользователи лучше поймут эту новую парадигму, они будут более эффективны в том, чтобы позволить Claude Code работать более агентивно.

### Закрепите версии моделей для поставщиков облачных услуг

Если вы развертываете через [Bedrock](/ru/amazon-bedrock), [Vertex AI](/ru/google-vertex-ai) или [Foundry](/ru/microsoft-foundry), закрепите конкретные версии моделей, используя `ANTHROPIC_DEFAULT_OPUS_MODEL`, `ANTHROPIC_DEFAULT_SONNET_MODEL` и `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Без закрепления, псевдонимы Claude Code разрешаются на последнюю версию, что может нарушить работу пользователей, когда Anthropic выпускает новую модель, которая еще не включена в вашей учетной записи. См. раздел [Конфигурация модели](/ru/model-config#pin-models-for-third-party-deployments) для получения подробной информации.

### Настройте политики безопасности

Команды безопасности могут настроить управляемые разрешения для того, что Claude Code может и не может делать, которые не могут быть переопределены локальной конфигурацией. [Узнайте больше](/ru/security).

### Используйте MCP для интеграций

MCP — это отличный способ предоставить Claude Code больше информации, например подключение к системам управления билетами или журналам ошибок. Мы рекомендуем, чтобы одна центральная команда настроила MCP servers и проверила конфигурацию `.mcp.json` в кодовую базу, чтобы все пользователи получали выгоду. [Узнайте больше](/ru/mcp).

В Anthropic мы доверяем Claude Code для питания разработки во всех кодовых базах Anthropic. Мы надеемся, что вам понравится использовать Claude Code так же, как и нам.

## Следующие шаги

После того как вы выбрали вариант развертывания и настроили доступ для вашей команды:

1. **Развертывание в вашей команде**: поделитесь инструкциями по установке и попросите членов команды [установить Claude Code](/ru/setup) и аутентифицироваться с помощью своих учетных данных.
2. **Настройте общую конфигурацию**: создайте [файл CLAUDE.md](/ru/memory) в ваших репозиториях, чтобы помочь Claude Code понять вашу кодовую базу и стандарты кодирования.
3. **Настройте разрешения**: просмотрите [параметры безопасности](/ru/security) для определения того, что Claude Code может и не может делать в вашей среде.
