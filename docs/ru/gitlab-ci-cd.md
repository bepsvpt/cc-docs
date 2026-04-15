> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code GitLab CI/CD

> Узнайте об интеграции Claude Code в ваш рабочий процесс разработки с GitLab CI/CD

<Info>
  Claude Code для GitLab CI/CD в настоящее время находится в бета-версии. Функции и возможности могут развиваться по мере совершенствования опыта.

  Эта интеграция поддерживается GitLab. Для получения поддержки см. следующий [вопрос GitLab](https://gitlab.com/gitlab-org/gitlab/-/issues/573776).
</Info>

<Note>
  Эта интеграция построена на основе [Claude Code CLI и Agent SDK](https://platform.claude.com/docs/ru/agent-sdk/overview), обеспечивая программное использование Claude в ваших заданиях CI/CD и пользовательских рабочих процессах автоматизации.
</Note>

## Почему использовать Claude Code с GitLab?

* **Мгновенное создание MR**: Опишите, что вам нужно, и Claude предложит полный MR с изменениями и объяснением
* **Автоматизированная реализация**: Превратите проблемы в рабочий код с помощью одной команды или упоминания
* **Осведомленность о проекте**: Claude следует вашим рекомендациям `CLAUDE.md` и существующим шаблонам кода
* **Простая настройка**: Добавьте одно задание в `.gitlab-ci.yml` и замаскированную переменную CI/CD
* **Готово для предприятия**: Выберите Claude API, AWS Bedrock или Google Vertex AI для соответствия требованиям к месторасположению данных и закупкам
* **Безопасно по умолчанию**: Работает на ваших GitLab runners с вашей защитой ветвей и утверждениями

## Как это работает

Claude Code использует GitLab CI/CD для запуска задач AI в изолированных заданиях и фиксации результатов обратно через MR:

1. **Оркестровка, управляемая событиями**: GitLab прослушивает выбранные вами триггеры (например, комментарий, упоминающий `@claude` в проблеме, MR или потоке рецензирования). Задание собирает контекст из потока и репозитория, создает подсказки из этого ввода и запускает Claude Code.

2. **Абстракция поставщика**: Используйте поставщика, который подходит для вашей среды:
   * Claude API (SaaS)
   * AWS Bedrock (доступ на основе IAM, опции между регионами)
   * Google Vertex AI (собственный GCP, Workload Identity Federation)

3. **Изолированное выполнение**: Каждое взаимодействие выполняется в контейнере со строгими правилами сети и файловой системы. Claude Code обеспечивает разрешения с областью действия рабочего пространства для ограничения записей. Каждое изменение проходит через MR, чтобы рецензенты видели diff и применялись утверждения.

Выберите региональные конечные точки, чтобы снизить задержку и соответствовать требованиям суверенитета данных при использовании существующих облачных соглашений.

## Что может делать Claude?

Claude Code обеспечивает мощные рабочие процессы CI/CD, которые преобразуют способ работы с кодом:

* Создание и обновление MR из описаний проблем или комментариев
* Анализ регрессий производительности и предложение оптимизаций
* Прямая реализация функций в ветви, затем открытие MR
* Исправление ошибок и регрессий, выявленных тестами или комментариями
* Ответ на последующие комментарии для итерации по запрошенным изменениям

## Настройка

### Быстрая настройка

Самый быстрый способ начать работу — добавить минимальное задание в ваш `.gitlab-ci.yml` и установить ваш ключ API как замаскированную переменную.

1. **Добавьте замаскированную переменную CI/CD**
   * Перейдите в **Settings** → **CI/CD** → **Variables**
   * Добавьте `ANTHROPIC_API_KEY` (замаскирована, защищена по мере необходимости)

2. **Добавьте задание Claude в `.gitlab-ci.yml`**

```yaml theme={null}
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  # Отрегулируйте правила в соответствии с тем, как вы хотите запустить задание:
  # - ручные запуски
  # - события merge request
  # - веб/API триггеры, когда комментарий содержит '@claude'
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk update
    - apk add --no-cache git curl bash
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    # Опционально: запустите сервер GitLab MCP, если ваша настройка его предоставляет
    - /bin/gitlab-mcp-server || true
    # Используйте переменные AI_FLOW_* при вызове через веб/API триггеры с полезными нагрузками контекста
    - echo "$AI_FLOW_INPUT for $AI_FLOW_CONTEXT on $AI_FLOW_EVENT"
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Review this MR and implement the requested changes'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
```

После добавления задания и переменной `ANTHROPIC_API_KEY` протестируйте, запустив задание вручную из **CI/CD** → **Pipelines**, или запустите его из MR, чтобы позволить Claude предложить обновления в ветви и открыть MR при необходимости.

<Note>
  Для запуска на AWS Bedrock или Google Vertex AI вместо Claude API см. раздел [Использование с AWS Bedrock и Google Vertex AI](#using-with-aws-bedrock--google-vertex-ai) ниже для настройки аутентификации и окружения.
</Note>

### Ручная настройка (рекомендуется для производства)

Если вы предпочитаете более контролируемую настройку или вам нужны поставщики для предприятия:

1. **Настройте доступ поставщика**:
   * **Claude API**: Создайте и сохраните `ANTHROPIC_API_KEY` как замаскированную переменную CI/CD
   * **AWS Bedrock**: **Настройте GitLab** → **AWS OIDC** и создайте роль IAM для Bedrock
   * **Google Vertex AI**: **Настройте Workload Identity Federation для GitLab** → **GCP**

2. **Добавьте учетные данные проекта для операций GitLab API**:
   * Используйте `CI_JOB_TOKEN` по умолчанию или создайте Project Access Token с областью `api`
   * Сохраните как `GITLAB_ACCESS_TOKEN` (замаскирована), если используете PAT

3. **Добавьте задание Claude в `.gitlab-ci.yml`** (см. примеры ниже)

4. **(Опционально) Включите триггеры, управляемые упоминаниями**:
   * Добавьте webhook проекта для "Comments (notes)" к вашему прослушивателю событий (если вы его используете)
   * Попросите прослушиватель вызвать API триггера конвейера с переменными, такими как `AI_FLOW_INPUT` и `AI_FLOW_CONTEXT`, когда комментарий содержит `@claude`

## Примеры использования

### Превратите проблемы в MR

В комментарии проблемы:

```text theme={null}
@claude implement this feature based on the issue description
```

Claude анализирует проблему и кодовую базу, записывает изменения в ветви и открывает MR для рецензирования.

### Получите помощь в реализации

В обсуждении MR:

```text theme={null}
@claude suggest a concrete approach to cache the results of this API call
```

Claude предлагает изменения, добавляет код с соответствующим кешированием и обновляет MR.

### Быстро исправляйте ошибки

В комментарии проблемы или MR:

```text theme={null}
@claude fix the TypeError in the user dashboard component
```

Claude находит ошибку, реализует исправление и обновляет ветвь или открывает новый MR.

## Использование с AWS Bedrock и Google Vertex AI

Для корпоративных сред вы можете запустить Claude Code полностью на вашей облачной инфраструктуре с тем же опытом разработчика.

<Tabs>
  <Tab title="AWS Bedrock">
    ### Предварительные требования

    Перед настройкой Claude Code с AWS Bedrock вам потребуется:

    1. Учетная запись AWS с доступом Amazon Bedrock к желаемым моделям Claude
    2. GitLab, настроенный как поставщик идентификации OIDC в AWS IAM
    3. Роль IAM с разрешениями Bedrock и политикой доверия, ограниченной вашим проектом/ссылками GitLab
    4. Переменные GitLab CI/CD для предположения роли:
       * `AWS_ROLE_TO_ASSUME` (ARN роли)
       * `AWS_REGION` (регион Bedrock)

    ### Инструкции по настройке

    Настройте AWS, чтобы позволить заданиям GitLab CI предположить роль IAM через OIDC (без статических ключей).

    **Требуемая настройка:**

    1. Включите Amazon Bedrock и запросите доступ к целевым моделям Claude
    2. Создайте поставщика IAM OIDC для GitLab, если он еще не присутствует
    3. Создайте роль IAM, доверяющую поставщику GitLab OIDC, ограниченную вашим проектом и защищенными ссылками
    4. Прикрепите разрешения с наименьшими привилегиями для API вызова Bedrock

    **Требуемые значения для сохранения в переменных CI/CD:**

    * `AWS_ROLE_TO_ASSUME`
    * `AWS_REGION`

    Добавьте переменные в Settings → CI/CD → Variables:

    ```yaml theme={null}
    # Для AWS Bedrock:
    - AWS_ROLE_TO_ASSUME
    - AWS_REGION
    ```

    Используйте пример задания AWS Bedrock выше для обмена токена задания GitLab на временные учетные данные AWS во время выполнения.
  </Tab>

  <Tab title="Google Vertex AI">
    ### Предварительные требования

    Перед настройкой Claude Code с Google Vertex AI вам потребуется:

    1. Проект Google Cloud с:
       * Включенным API Vertex AI
       * Настроенной Workload Identity Federation для доверия GitLab OIDC
    2. Выделенная учетная запись сервиса только с требуемыми ролями Vertex AI
    3. Переменные GitLab CI/CD для WIF:
       * `GCP_WORKLOAD_IDENTITY_PROVIDER` (полное имя ресурса)
       * `GCP_SERVICE_ACCOUNT` (адрес электронной почты учетной записи сервиса)

    ### Инструкции по настройке

    Настройте Google Cloud, чтобы позволить заданиям GitLab CI олицетворять учетную запись сервиса через Workload Identity Federation.

    **Требуемая настройка:**

    1. Включите IAM Credentials API, STS API и Vertex AI API
    2. Создайте пул Workload Identity и поставщика для GitLab OIDC
    3. Создайте выделенную учетную запись сервиса с ролями Vertex AI
    4. Предоставьте основному принципу WIF разрешение на олицетворение учетной записи сервиса

    **Требуемые значения для сохранения в переменных CI/CD:**

    * `GCP_WORKLOAD_IDENTITY_PROVIDER`
    * `GCP_SERVICE_ACCOUNT`

    Добавьте переменные в Settings → CI/CD → Variables:

    ```yaml theme={null}
    # Для Google Vertex AI:
    - GCP_WORKLOAD_IDENTITY_PROVIDER
    - GCP_SERVICE_ACCOUNT
    - CLOUD_ML_REGION (например, us-east5)
    ```

    Используйте пример задания Google Vertex AI выше для аутентификации без сохранения ключей.
  </Tab>
</Tabs>

## Примеры конфигурации

Ниже приведены готовые к использованию фрагменты, которые вы можете адаптировать к вашему конвейеру.

### Базовый .gitlab-ci.yml (Claude API)

```yaml theme={null}
stages:
  - ai

claude:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
    - if: '$CI_PIPELINE_SOURCE == "merge_request_event"'
  variables:
    GIT_STRATEGY: fetch
  before_script:
    - apk update
    - apk add --no-cache git curl bash
    - curl -fsSL https://claude.ai/install.sh | bash
  script:
    - /bin/gitlab-mcp-server || true
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Summarize recent changes and suggest improvements'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  # Claude Code будет использовать ANTHROPIC_API_KEY из переменных CI/CD
```

### Пример задания AWS Bedrock (OIDC)

**Предварительные требования:**

* Amazon Bedrock включен с доступом к выбранной модели Claude
* GitLab OIDC настроен в AWS с ролью, которая доверяет вашему проекту GitLab и ссылкам
* Роль IAM с разрешениями Bedrock (рекомендуется наименьшие привилегии)

**Требуемые переменные CI/CD:**

* `AWS_ROLE_TO_ASSUME`: ARN роли IAM для доступа к Bedrock
* `AWS_REGION`: Регион Bedrock (например, `us-west-2`)

```yaml theme={null}
claude-bedrock:
  stage: ai
  image: node:24-alpine3.21
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
  before_script:
    - apk add --no-cache bash curl jq git python3 py3-pip
    - pip install --no-cache-dir awscli
    - curl -fsSL https://claude.ai/install.sh | bash
    # Обменяйте токен GitLab OIDC на учетные данные AWS
    - export AWS_WEB_IDENTITY_TOKEN_FILE="${CI_JOB_JWT_FILE:-/tmp/oidc_token}"
    - if [ -n "${CI_JOB_JWT_V2}" ]; then printf "%s" "$CI_JOB_JWT_V2" > "$AWS_WEB_IDENTITY_TOKEN_FILE"; fi
    - >
      aws sts assume-role-with-web-identity
      --role-arn "$AWS_ROLE_TO_ASSUME"
      --role-session-name "gitlab-claude-$(date +%s)"
      --web-identity-token "file://$AWS_WEB_IDENTITY_TOKEN_FILE"
      --duration-seconds 3600 > /tmp/aws_creds.json
    - export AWS_ACCESS_KEY_ID="$(jq -r .Credentials.AccessKeyId /tmp/aws_creds.json)"
    - export AWS_SECRET_ACCESS_KEY="$(jq -r .Credentials.SecretAccessKey /tmp/aws_creds.json)"
    - export AWS_SESSION_TOKEN="$(jq -r .Credentials.SessionToken /tmp/aws_creds.json)"
  script:
    - /bin/gitlab-mcp-server || true
    - >
      claude
      -p "${AI_FLOW_INPUT:-'Implement the requested changes and open an MR'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  variables:
    AWS_REGION: "us-west-2"
```

<Note>
  Идентификаторы моделей для Bedrock включают префиксы, специфичные для региона (например, `us.anthropic.claude-sonnet-4-6`). Передайте желаемую модель через конфигурацию задания или подсказку, если ваш рабочий процесс это поддерживает.
</Note>

### Пример задания Google Vertex AI (Workload Identity Federation)

**Предварительные требования:**

* API Vertex AI включен в вашем проекте GCP
* Workload Identity Federation настроена для доверия GitLab OIDC
* Учетная запись сервиса с разрешениями Vertex AI

**Требуемые переменные CI/CD:**

* `GCP_WORKLOAD_IDENTITY_PROVIDER`: Полное имя ресурса поставщика
* `GCP_SERVICE_ACCOUNT`: Адрес электронной почты учетной записи сервиса
* `CLOUD_ML_REGION`: Регион Vertex (например, `us-east5`)

```yaml theme={null}
claude-vertex:
  stage: ai
  image: gcr.io/google.com/cloudsdktool/google-cloud-cli:slim
  rules:
    - if: '$CI_PIPELINE_SOURCE == "web"'
  before_script:
    - apt-get update && apt-get install -y git && apt-get clean
    - curl -fsSL https://claude.ai/install.sh | bash
    # Аутентифицируйтесь в Google Cloud через WIF (без загруженных ключей)
    - >
      gcloud auth login --cred-file=<(cat <<EOF
      {
        "type": "external_account",
        "audience": "${GCP_WORKLOAD_IDENTITY_PROVIDER}",
        "subject_token_type": "urn:ietf:params:oauth:token-type:jwt",
        "service_account_impersonation_url": "https://iamcredentials.googleapis.com/v1/projects/-/serviceAccounts/${GCP_SERVICE_ACCOUNT}:generateAccessToken",
        "token_url": "https://sts.googleapis.com/v1/token"
      }
      EOF
      )
    - gcloud config set project "$(gcloud projects list --format='value(projectId)' --filter="name:${CI_PROJECT_NAMESPACE}" | head -n1)" || true
  script:
    - /bin/gitlab-mcp-server || true
    - >
      CLOUD_ML_REGION="${CLOUD_ML_REGION:-us-east5}"
      claude
      -p "${AI_FLOW_INPUT:-'Review and update code as requested'}"
      --permission-mode acceptEdits
      --allowedTools "Bash Read Edit Write mcp__gitlab"
      --debug
  variables:
    CLOUD_ML_REGION: "us-east5"
```

<Note>
  С Workload Identity Federation вам не нужно сохранять ключи учетной записи сервиса. Используйте условия доверия, специфичные для репозитория, и учетные записи сервиса с наименьшими привилегиями.
</Note>

## Лучшие практики

### Конфигурация CLAUDE.md

Создайте файл `CLAUDE.md` в корне репозитория, чтобы определить стандарты кодирования, критерии рецензирования и правила, специфичные для проекта. Claude читает этот файл во время запусков и следует вашим соглашениям при предложении изменений.

### Соображения безопасности

**Никогда не фиксируйте ключи API или учетные данные облака в вашем репозитории**. Всегда используйте переменные GitLab CI/CD:

* Добавьте `ANTHROPIC_API_KEY` как замаскированную переменную (и защитите ее при необходимости)
* Используйте OIDC, специфичный для поставщика, где возможно (без долгоживущих ключей)
* Ограничьте разрешения задания и исходящий трафик сети
* Рецензируйте MR Claude, как любого другого участника

### Оптимизация производительности

* Держите `CLAUDE.md` сосредоточенным и кратким
* Предоставляйте четкие описания проблем/MR, чтобы снизить количество итераций
* Настройте разумные тайм-ауты заданий, чтобы избежать неконтролируемых запусков
* Кешируйте npm и установки пакетов на runners, где возможно

### Затраты CI

При использовании Claude Code с GitLab CI/CD помните о связанных затратах:

* **Время GitLab Runner**:
  * Claude работает на ваших GitLab runners и потребляет минуты вычислений
  * Подробности о выставлении счетов за runner см. в плане GitLab

* **Затраты на API**:
  * Каждое взаимодействие Claude потребляет токены на основе размера подсказки и ответа
  * Использование токенов варьируется в зависимости от сложности задачи и размера кодовой базы
  * Подробности см. в [ценообразовании Anthropic](https://platform.claude.com/docs/ru/about-claude/pricing)

* **Советы по оптимизации затрат**:
  * Используйте конкретные команды `@claude` для снижения ненужных ходов
  * Установите соответствующие значения `max_turns` и тайм-аут задания
  * Ограничьте параллелизм для управления параллельными запусками

## Безопасность и управление

* Каждое задание выполняется в изолированном контейнере с ограниченным доступом в сеть
* Изменения Claude проходят через MR, чтобы рецензенты видели каждый diff
* Правила защиты ветвей и утверждения применяются к коду, созданному AI
* Claude Code использует разрешения с областью действия рабочего пространства для ограничения записей
* Затраты остаются под вашим контролем, потому что вы приносите свои собственные учетные данные поставщика

## Устранение неполадок

### Claude не отвечает на команды @claude

* Убедитесь, что ваш конвейер запускается (вручную, событие MR или через прослушиватель событий/webhook примечания)
* Убедитесь, что переменные CI/CD (`ANTHROPIC_API_KEY` или параметры облачного поставщика) присутствуют и не замаскированы
* Проверьте, что комментарий содержит `@claude` (не `/claude`) и что ваш триггер упоминания настроен

### Задание не может писать комментарии или открывать MR

* Убедитесь, что `CI_JOB_TOKEN` имеет достаточные разрешения для проекта, или используйте Project Access Token с областью `api`
* Проверьте, что инструмент `mcp__gitlab` включен в `--allowedTools`
* Подтвердите, что задание выполняется в контексте MR или имеет достаточный контекст через переменные `AI_FLOW_*`

### Ошибки аутентификации

* **Для Claude API**: Подтвердите, что `ANTHROPIC_API_KEY` действителен и не истек
* **Для Bedrock/Vertex**: Проверьте конфигурацию OIDC/WIF, олицетворение роли и имена секретов; подтвердите доступность региона и модели

## Расширенная конфигурация

### Общие параметры и переменные

Claude Code поддерживает эти часто используемые входные данные:

* `prompt` / `prompt_file`: Предоставьте инструкции встроенно (`-p`) или через файл
* `max_turns`: Ограничьте количество взаимных итераций
* `timeout_minutes`: Ограничьте общее время выполнения
* `ANTHROPIC_API_KEY`: Требуется для Claude API (не используется для Bedrock/Vertex)
* Окружение, специфичное для поставщика: `AWS_REGION`, переменные проекта/региона для Vertex

<Note>
  Точные флаги и параметры могут варьироваться в зависимости от версии `@anthropic-ai/claude-code`. Запустите `claude --help` в вашем задании, чтобы увидеть поддерживаемые опции.
</Note>

### Настройка поведения Claude

Вы можете направлять Claude двумя основными способами:

1. **CLAUDE.md**: Определите стандарты кодирования, требования безопасности и соглашения проекта. Claude читает это во время запусков и следует вашим правилам.
2. **Пользовательские подсказки**: Передайте инструкции, специфичные для задачи, через `prompt`/`prompt_file` в задании. Используйте разные подсказки для разных заданий (например, рецензирование, реализация, рефакторинг).
