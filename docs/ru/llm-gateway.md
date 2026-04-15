> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Конфигурация LLM gateway

> Узнайте, как настроить Claude Code для работы с решениями LLM gateway. Охватывает требования к шлюзу, конфигурацию аутентификации, выбор модели и настройку конечных точек для конкретных поставщиков.

LLM gateways предоставляют централизованный прокси-слой между Claude Code и поставщиками моделей, часто предоставляя:

* **Централизованная аутентификация** - Единая точка управления ключами API
* **Отслеживание использования** - Мониторинг использования в командах и проектах
* **Контроль затрат** - Реализация бюджетов и ограничений скорости
* **Логирование аудита** - Отслеживание всех взаимодействий с моделью для соответствия требованиям
* **Маршрутизация моделей** - Переключение между поставщиками без изменения кода

## Требования к шлюзу

Чтобы LLM gateway работал с Claude Code, он должен соответствовать следующим требованиям:

**Формат API**

Шлюз должен предоставлять клиентам по крайней мере один из следующих форматов API:

1. **Anthropic Messages**: `/v1/messages`, `/v1/messages/count_tokens`
   * Должен перенаправлять заголовки запроса: `anthropic-beta`, `anthropic-version`

2. **Bedrock InvokeModel**: `/invoke`, `/invoke-with-response-stream`
   * Должен сохранять поля тела запроса: `anthropic_beta`, `anthropic_version`

3. **Vertex rawPredict**: `:rawPredict`, `:streamRawPredict`, `/count-tokens:rawPredict`
   * Должен перенаправлять заголовки запроса: `anthropic-beta`, `anthropic-version`

Невозможность перенаправления заголовков или сохранения полей тела может привести к снижению функциональности или невозможности использования функций Claude Code.

<Note>
  Claude Code определяет, какие функции включить, на основе формата API. При использовании формата Anthropic Messages с Bedrock или Vertex может потребоваться установить переменную окружения `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`.
</Note>

## Конфигурация

### Выбор модели

По умолчанию Claude Code будет использовать стандартные имена моделей для выбранного формата API.

Если вы настроили пользовательские имена моделей в вашем шлюзе, используйте переменные окружения, описанные в [Конфигурация модели](/ru/model-config), чтобы соответствовать вашим пользовательским именам.

## Конфигурация LiteLLM

<Warning>
  LiteLLM версии PyPI 1.82.7 и 1.82.8 были скомпрометированы вредоносным ПО для кражи учетных данных. Не устанавливайте эти версии. Если вы уже установили их:

  * Удалите пакет
  * Измените все учетные данные на затронутых системах
  * Следуйте шагам восстановления в [BerriAI/litellm#24518](https://github.com/BerriAI/litellm/issues/24518)

  LiteLLM - это сторонний прокси-сервис. Anthropic не одобряет, не поддерживает и не проверяет безопасность или функциональность LiteLLM. Это руководство предоставляется в информационных целях и может устаревать. Используйте на свой риск.
</Warning>

### Предварительные требования

* Claude Code обновлен до последней версии
* LiteLLM Proxy Server развернут и доступен
* Доступ к моделям Claude через выбранного поставщика

### Базовая настройка LiteLLM

**Конфигурация Claude Code**:

#### Методы аутентификации

##### Статический ключ API

Самый простой метод с использованием фиксированного ключа API:

```bash theme={null}
# Установить в окружении
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# Или в настройках Claude Code
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

Это значение будет отправлено как заголовок `Authorization`.

##### Динамический ключ API с помощником

Для ротации ключей или аутентификации для каждого пользователя:

1. Создайте скрипт помощника ключа API:

```bash theme={null}
#!/bin/bash
# ~/bin/get-litellm-key.sh

# Пример: Получить ключ из хранилища
vault kv get -field=api_key secret/litellm/claude-code

# Пример: Сгенерировать JWT токен
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'
```

2. Настройте параметры Claude Code для использования помощника:

```json theme={null}
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. Установите интервал обновления токена:

```bash theme={null}
# Обновлять каждый час (3600000 мс)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

Это значение будет отправлено как заголовки `Authorization` и `X-Api-Key`. `apiKeyHelper` имеет более низкий приоритет, чем `ANTHROPIC_AUTH_TOKEN` или `ANTHROPIC_API_KEY`.

#### Унифицированная конечная точка (рекомендуется)

Использование [конечной точки формата Anthropic](https://docs.litellm.ai/docs/anthropic_unified) LiteLLM:

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**Преимущества унифицированной конечной точки над сквозными конечными точками:**

* Балансировка нагрузки
* Резервные варианты
* Последовательная поддержка отслеживания затрат и отслеживания конечного пользователя

#### Конечные точки сквозного прохода для конкретных поставщиков (альтернатива)

##### Claude API через LiteLLM

Использование [сквозной конечной точки](https://docs.litellm.ai/docs/pass_through/anthropic_completion):

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### Amazon Bedrock через LiteLLM

Использование [сквозной конечной точки](https://docs.litellm.ai/docs/pass_through/bedrock):

```bash theme={null}
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### Google Vertex AI через LiteLLM

Использование [сквозной конечной точки](https://docs.litellm.ai/docs/pass_through/vertex_ai):

```bash theme={null}
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

Для получения более подробной информации обратитесь к [документации LiteLLM](https://docs.litellm.ai/).

## Дополнительные ресурсы

* [Документация LiteLLM](https://docs.litellm.ai/)
* [Параметры Claude Code](/ru/settings)
* [Конфигурация корпоративной сети](/ru/network-config)
* [Обзор интеграций третьих сторон](/ru/third-party-integrations)
