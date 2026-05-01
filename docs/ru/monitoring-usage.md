> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Мониторинг

> Узнайте, как включить и настроить OpenTelemetry для Claude Code.

Отслеживайте использование Claude Code, затраты и активность инструментов в вашей организации, экспортируя данные телеметрии через OpenTelemetry (OTel). Claude Code экспортирует метрики как данные временных рядов через стандартный протокол метрик, события через протокол логов/событий и опционально распределенные трассировки через [протокол трассировки](#traces-beta). Настройте ваши бэкенды метрик, логов и трассировок в соответствии с требованиями мониторинга.

## Быстрый старт

Настройте OpenTelemetry с помощью переменных окружения:

```bash theme={null}
# 1. Включить телеметрию
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. Выбрать экспортеры (оба опциональны - настройте только необходимое)
export OTEL_METRICS_EXPORTER=otlp       # Опции: otlp, prometheus, console, none
export OTEL_LOGS_EXPORTER=otlp          # Опции: otlp, console, none

# 3. Настроить OTLP endpoint (для OTLP экспортера)
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. Установить аутентификацию (если требуется)
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. Для отладки: сократить интервалы экспорта
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 секунд (по умолчанию: 60000ms)
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 секунд (по умолчанию: 5000ms)

# 6. Запустить Claude Code
claude
```

<Note>
  Интервалы экспорта по умолчанию составляют 60 секунд для метрик и 5 секунд для логов. Во время настройки вы можете использовать более короткие интервалы для целей отладки. Не забудьте сбросить эти значения для использования в production.
</Note>

Для полного списка параметров конфигурации см. [спецификацию OpenTelemetry](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options).

## Конфигурация администратора

Администраторы могут настраивать параметры OpenTelemetry для всех пользователей через [файл управляемых параметров](/ru/settings#settings-files). Это позволяет централизованно управлять параметрами телеметрии в организации. Дополнительную информацию о том, как применяются параметры, см. в разделе [приоритет параметров](/ru/settings#settings-precedence).

Пример конфигурации управляемых параметров:

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer example-token"
  }
}
```

<Note>
  Управляемые параметры можно распространять через MDM (Mobile Device Management) или другие решения для управления устройствами. Переменные окружения, определенные в файле управляемых параметров, имеют высокий приоритет и не могут быть переопределены пользователями.
</Note>

## Детали конфигурации

### Общие переменные конфигурации

| Переменная окружения                                | Описание                                                                                                                                                                                                                                                                                                                                | Примеры значений                                                                                                            |
| --------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                      | Включает сбор телеметрии (обязательно)                                                                                                                                                                                                                                                                                                  | `1`                                                                                                                         |
| `OTEL_METRICS_EXPORTER`                             | Типы экспортера метрик, разделенные запятыми. Используйте `none` для отключения                                                                                                                                                                                                                                                         | `console`, `otlp`, `prometheus`, `none`                                                                                     |
| `OTEL_LOGS_EXPORTER`                                | Типы экспортера логов/событий, разделенные запятыми. Используйте `none` для отключения                                                                                                                                                                                                                                                  | `console`, `otlp`, `none`                                                                                                   |
| `OTEL_EXPORTER_OTLP_PROTOCOL`                       | Протокол для OTLP экспортера, применяется ко всем сигналам                                                                                                                                                                                                                                                                              | `grpc`, `http/json`, `http/protobuf`                                                                                        |
| `OTEL_EXPORTER_OTLP_ENDPOINT`                       | OTLP endpoint коллектора для всех сигналов                                                                                                                                                                                                                                                                                              | `http://localhost:4317`                                                                                                     |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL`               | Протокол для метрик, переопределяет общий параметр                                                                                                                                                                                                                                                                                      | `grpc`, `http/json`, `http/protobuf`                                                                                        |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`               | OTLP endpoint метрик, переопределяет общий параметр                                                                                                                                                                                                                                                                                     | `http://localhost:4318/v1/metrics`                                                                                          |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL`                  | Протокол для логов, переопределяет общий параметр                                                                                                                                                                                                                                                                                       | `grpc`, `http/json`, `http/protobuf`                                                                                        |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT`                  | OTLP endpoint логов, переопределяет общий параметр                                                                                                                                                                                                                                                                                      | `http://localhost:4318/v1/logs`                                                                                             |
| `OTEL_EXPORTER_OTLP_HEADERS`                        | Заголовки аутентификации для OTLP                                                                                                                                                                                                                                                                                                       | `Authorization=Bearer token`                                                                                                |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY`             | Ключ клиента для аутентификации mTLS                                                                                                                                                                                                                                                                                                    | Путь к файлу ключа клиента                                                                                                  |
| `OTEL_EXPORTER_OTLP_METRICS_CLIENT_CERTIFICATE`     | Сертификат клиента для аутентификации mTLS                                                                                                                                                                                                                                                                                              | Путь к файлу сертификата клиента                                                                                            |
| `OTEL_METRIC_EXPORT_INTERVAL`                       | Интервал экспорта в миллисекундах (по умолчанию: 60000)                                                                                                                                                                                                                                                                                 | `5000`, `60000`                                                                                                             |
| `OTEL_LOGS_EXPORT_INTERVAL`                         | Интервал экспорта логов в миллисекундах (по умолчанию: 5000)                                                                                                                                                                                                                                                                            | `1000`, `10000`                                                                                                             |
| `OTEL_LOG_USER_PROMPTS`                             | Включить логирование содержимого пользовательских подсказок (по умолчанию: отключено)                                                                                                                                                                                                                                                   | `1` для включения                                                                                                           |
| `OTEL_LOG_TOOL_DETAILS`                             | Включить логирование параметров инструмента и аргументов входных данных в событиях инструментов и атрибутах span трассировки: команды Bash, имена MCP сервера и инструмента, имена навыков и входные данные инструмента. Также включает пользовательские, плагин и MCP имена команд на событиях `user_prompt` (по умолчанию: отключено) | `1` для включения                                                                                                           |
| `OTEL_LOG_TOOL_CONTENT`                             | Включить логирование входных и выходных данных инструмента в событиях span (по умолчанию: отключено). Требует [трассировку](#traces-beta). Содержимое усекается на 60 КБ                                                                                                                                                                | `1` для включения                                                                                                           |
| `OTEL_LOG_RAW_API_BODIES`                           | Выдавать полный JSON запроса и ответа Anthropic Messages API как события логов `api_request_body` / `api_response_body` (по умолчанию: отключено). Тела включают всю историю разговора. Включение этого подразумевает согласие со всем, что раскрыли бы `OTEL_LOG_USER_PROMPTS`, `OTEL_LOG_TOOL_DETAILS` и `OTEL_LOG_TOOL_CONTENT`      | `1` для встроенных тел, усеченных на 60 КБ, или `file:<dir>` для неусеченных тел на диске с указателем `body_ref` в событии |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | Предпочтение временности метрик (по умолчанию: `delta`). Установите на `cumulative`, если ваш бэкенд ожидает кумулятивную временность                                                                                                                                                                                                   | `delta`, `cumulative`                                                                                                       |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`       | Интервал для обновления динамических заголовков (по умолчанию: 1740000ms / 29 минут)                                                                                                                                                                                                                                                    | `900000`                                                                                                                    |

### Управление кардинальностью метрик

Следующие переменные окружения управляют тем, какие атрибуты включены в метрики для управления кардинальностью:

| Переменная окружения                | Описание                                                          | Значение по умолчанию | Пример для отключения |
| ----------------------------------- | ----------------------------------------------------------------- | --------------------- | --------------------- |
| `OTEL_METRICS_INCLUDE_SESSION_ID`   | Включить атрибут session.id в метрики                             | `true`                | `false`               |
| `OTEL_METRICS_INCLUDE_VERSION`      | Включить атрибут app.version в метрики                            | `false`               | `true`                |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | Включить атрибуты user.account\_uuid и user.account\_id в метрики | `true`                | `false`               |

Эти переменные помогают управлять кардинальностью метрик, что влияет на требования к хранилищу и производительность запросов в вашем бэкенде метрик. Более низкая кардинальность обычно означает лучшую производительность и более низкие затраты на хранилище, но менее детальные данные для анализа.

### Traces (beta)

Распределенная трассировка экспортирует spans, которые связывают каждую пользовательскую подсказку с запросами API и выполнением инструментов, которые она вызывает, так что вы можете просмотреть полный запрос как одну трассировку в вашем бэкенде трассировки.

Трассировка отключена по умолчанию. Чтобы включить её, установите оба `CLAUDE_CODE_ENABLE_TELEMETRY=1` и `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`, затем установите `OTEL_TRACES_EXPORTER` для выбора места отправки spans. Трассировки повторно используют [общую конфигурацию OTLP](#common-configuration-variables) для endpoint, протокола и заголовков.

| Переменная окружения                  | Описание                                                                                    | Примеры значений                     |
| ------------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------ |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` | Включить трассировку span (обязательно). `ENABLE_ENHANCED_TELEMETRY_BETA` также принимается | `1`                                  |
| `OTEL_TRACES_EXPORTER`                | Типы экспортера трассировок, разделенные запятыми. Используйте `none` для отключения        | `console`, `otlp`, `none`            |
| `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL`  | Протокол для трассировок, переопределяет `OTEL_EXPORTER_OTLP_PROTOCOL`                      | `grpc`, `http/json`, `http/protobuf` |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`  | OTLP endpoint трассировок, переопределяет `OTEL_EXPORTER_OTLP_ENDPOINT`                     | `http://localhost:4318/v1/traces`    |
| `OTEL_TRACES_EXPORT_INTERVAL`         | Интервал экспорта пакета span в миллисекундах (по умолчанию: 5000)                          | `1000`, `10000`                      |

Spans скрывают текст пользовательской подсказки, детали входных данных инструмента и содержимое инструмента по умолчанию. Установите `OTEL_LOG_USER_PROMPTS=1`, `OTEL_LOG_TOOL_DETAILS=1` и `OTEL_LOG_TOOL_CONTENT=1` для их включения.

Когда трассировка активна, подпроцессы Bash и PowerShell автоматически наследуют переменную окружения `TRACEPARENT`, содержащую контекст трассировки W3C активного span выполнения инструмента. Это позволяет любому подпроцессу, который читает `TRACEPARENT`, родить свои собственные spans под той же трассировкой, обеспечивая сквозную распределенную трассировку через скрипты и команды, которые запускает Claude.

В Agent SDK и неинтерактивных сеансах, запущенных с `-p`, Claude Code также читает `TRACEPARENT` и `TRACESTATE` из своего собственного окружения при запуске каждого span взаимодействия. Это позволяет процессу встраивания передать свой активный контекст трассировки W3C в подпроцесс, так что spans Claude Code появляются как дочерние элементы трассировки вызывающей стороны. Интерактивные сеансы игнорируют входящий `TRACEPARENT`, чтобы избежать случайного наследования значений окружения из CI или контейнерных сред.

#### Иерархия span

Каждая пользовательская подсказка запускает корневой span `claude_code.interaction`. Вызовы API, вызовы инструментов и выполнения hooks записываются как его дочерние элементы. Spans инструментов имеют два собственных дочерних span: один для времени, потраченного на ожидание решения о разрешении, и один для самого выполнения. Когда инструмент Task порождает подагента, spans API и инструментов подагента вложены под span `claude_code.tool` родителя.

```text theme={null}
claude_code.interaction
├── claude_code.llm_request
├── claude_code.hook                    (требует детальную бета-трассировку)
└── claude_code.tool
    ├── claude_code.tool.blocked_on_user
    ├── claude_code.tool.execution
    └── (инструмент Task) spans claude_code.llm_request / claude_code.tool подагента
```

В сеансах Agent SDK и `claude -p`, `claude_code.interaction` сам становится дочерним элементом span вызывающей стороны, когда `TRACEPARENT` установлен в окружении.

#### Атрибуты span

Каждый span несет [стандартные атрибуты](#standard-attributes) плюс атрибут `span.type`, соответствующий его имени. Таблицы ниже перечисляют дополнительные атрибуты, установленные на каждом span. Spans `llm_request`, `tool.execution` и `hook` устанавливают статус OpenTelemetry `ERROR` при записи сбоя; другие spans всегда заканчиваются со статусом `UNSET`.

**`claude_code.interaction`**

| Атрибут                   | Описание                                                       | Управляется             |
| ------------------------- | -------------------------------------------------------------- | ----------------------- |
| `user_prompt`             | Текст подсказки. Значение `<REDACTED>` если gate не установлен | `OTEL_LOG_USER_PROMPTS` |
| `user_prompt_length`      | Длина подсказки в символах                                     |                         |
| `interaction.sequence`    | Счетчик на основе 1 взаимодействий в этом сеансе               |                         |
| `interaction.duration_ms` | Длительность хода в реальном времени                           |                         |

**`claude_code.llm_request`**

| Атрибут                          | Описание                                                                                                             | Управляется |
| -------------------------------- | -------------------------------------------------------------------------------------------------------------------- | ----------- |
| `model`                          | Идентификатор модели                                                                                                 |             |
| `gen_ai.system`                  | Всегда `anthropic`. Семантическое соглашение OpenTelemetry GenAI                                                     |             |
| `gen_ai.request.model`           | То же значение, что и `model`. Семантическое соглашение OpenTelemetry GenAI                                          |             |
| `query_source`                   | Подсистема, которая выдала запрос, такая как `repl_main_thread` или имя подагента                                    |             |
| `speed`                          | `fast` или `normal`                                                                                                  |             |
| `llm_request.context`            | `interaction`, `tool` или `standalone` в зависимости от родительского span                                           |             |
| `duration_ms`                    | Длительность в реальном времени, включая повторные попытки                                                           |             |
| `ttft_ms`                        | Время до первого токена в миллисекундах                                                                              |             |
| `input_tokens`                   | Количество входных токенов из блока использования API                                                                |             |
| `output_tokens`                  | Количество выходных токенов                                                                                          |             |
| `cache_read_tokens`              | Токены, прочитанные из кэша подсказок                                                                                |             |
| `cache_creation_tokens`          | Токены, записанные в кэш подсказок                                                                                   |             |
| `request_id`                     | ID запроса Anthropic API из заголовка ответа `request-id`                                                            |             |
| `gen_ai.response.id`             | То же значение, что и `request_id`. Семантическое соглашение OpenTelemetry GenAI                                     |             |
| `client_request_id`              | Сгенерированный клиентом `x-client-request-id` последней попытки                                                     |             |
| `attempt`                        | Всего попыток для этого запроса                                                                                      |             |
| `success`                        | `true` или `false`                                                                                                   |             |
| `status_code`                    | HTTP код состояния при сбое запроса                                                                                  |             |
| `error`                          | Сообщение об ошибке при сбое запроса                                                                                 |             |
| `response.has_tool_call`         | `true` когда ответ содержал блоки tool-use                                                                           |             |
| `stop_reason`                    | API ответ `stop_reason`, такой как `end_turn`, `tool_use`, `max_tokens`, `stop_sequence`, `pause_turn` или `refusal` |             |
| `gen_ai.response.finish_reasons` | То же значение, что и `stop_reason`, обернутое в массив строк. Семантическое соглашение OpenTelemetry GenAI          |             |

Каждая повторная попытка также записывается как событие span `gen_ai.request.attempt` с атрибутами `attempt` и `client_request_id`.

**`claude_code.tool`**

| Атрибут         | Описание                                                                  | Управляется             |
| --------------- | ------------------------------------------------------------------------- | ----------------------- |
| `tool_name`     | Имя инструмента                                                           |                         |
| `duration_ms`   | Длительность в реальном времени, включая ожидание разрешения и выполнение |                         |
| `result_tokens` | Приблизительный размер токена результата инструмента                      |                         |
| `file_path`     | Целевой путь файла для инструментов Read, Edit и Write                    | `OTEL_LOG_TOOL_DETAILS` |
| `full_command`  | Строка команды для инструмента Bash                                       | `OTEL_LOG_TOOL_DETAILS` |
| `skill_name`    | Имя навыка для инструмента Skill                                          | `OTEL_LOG_TOOL_DETAILS` |
| `subagent_type` | Тип подагента для инструмента Task                                        | `OTEL_LOG_TOOL_DETAILS` |

Когда `OTEL_LOG_TOOL_CONTENT=1`, этот span также записывает событие span `tool.output`, чьи атрибуты содержат входные и выходные тела инструмента, усеченные на 60 КБ на атрибут.

**`claude_code.tool.blocked_on_user`**

| Атрибут       | Описание                                                  | Управляется |
| ------------- | --------------------------------------------------------- | ----------- |
| `duration_ms` | Время, потраченное на ожидание решения о разрешении       |             |
| `decision`    | `accept` или `reject`                                     |             |
| `source`      | Источник решения, соответствующий событию `tool_decision` |             |

**`claude_code.tool.execution`**

| Атрибут       | Описание                                                                                                                                                        | Управляется             |
| ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------- |
| `duration_ms` | Время, потраченное на запуск тела инструмента                                                                                                                   |                         |
| `success`     | `true` или `false`                                                                                                                                              |                         |
| `error`       | Строка категории ошибки при сбое выполнения, такая как `Error:ENOENT` или `ShellError`. Содержит полное сообщение об ошибке вместо этого, когда gate установлен | `OTEL_LOG_TOOL_DETAILS` |

**`claude_code.hook`**

Этот span выдается только при активной детальной бета-трассировке, которая требует `ENABLE_BETA_TRACING_DETAILED=1` и `BETA_TRACING_ENDPOINT` в дополнение к конфигурации экспортера трассировки выше. В интерактивных сеансах CLI это также требует, чтобы ваша организация была в списке разрешений для функции. Сеансы Agent SDK и неинтерактивные сеансы `-p` не имеют ограничений. Он не выдается, когда установлен только `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA`.

| Атрибут                  | Описание                                                     | Управляется             |
| ------------------------ | ------------------------------------------------------------ | ----------------------- |
| `hook_event`             | Тип события hook, такой как `PreToolUse`                     |                         |
| `hook_name`              | Полное имя hook, такой как `PreToolUse:Write`                |                         |
| `num_hooks`              | Количество выполненных команд hook, соответствующих условиям |                         |
| `hook_definitions`       | JSON-сериализованная конфигурация hook                       | `OTEL_LOG_TOOL_DETAILS` |
| `duration_ms`            | Длительность в реальном времени всех соответствующих hooks   |                         |
| `num_success`            | Количество hooks, которые завершились успешно                |                         |
| `num_blocking`           | Количество hooks, которые вернули решение блокировки         |                         |
| `num_non_blocking_error` | Количество hooks, которые не удались без блокировки          |                         |
| `num_cancelled`          | Количество hooks, отмененных до завершения                   |                         |

<Note>
  Дополнительные атрибуты, содержащие содержимое, такие как `new_context`, `system_prompt_preview`, `user_system_prompt`, `tool_input` и `response.model_output`, выдаются только при активной детальной бета-трассировке. Они не являются частью стабильной схемы span. `user_system_prompt` дополнительно требует `OTEL_LOG_USER_PROMPTS=1`. Он содержит только текст системной подсказки, который вы предоставляете через опцию SDK `systemPrompt` или флаги `--system-prompt` и `--append-system-prompt`, усеченный на 60 КБ, и выдается один раз за сеанс, а не за запрос.
</Note>

### Динамические заголовки

Для корпоративных сред, требующих динамической аутентификации, вы можете настроить скрипт для динамического создания заголовков:

#### Конфигурация параметров

Добавьте в ваш `.claude/settings.json`:

```json theme={null}
{
  "otelHeadersHelper": "/bin/generate_opentelemetry_headers.sh"
}
```

#### Требования к скрипту

Скрипт должен выводить корректный JSON с парами строк ключ-значение, представляющими HTTP заголовки:

```bash theme={null}
#!/bin/bash
# Пример: несколько заголовков
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

#### Поведение обновления

Скрипт помощника заголовков запускается при запуске и периодически после этого для поддержки обновления токена. По умолчанию скрипт запускается каждые 29 минут. Настройте интервал с помощью переменной окружения `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`.

### Поддержка многокомандной организации

Организации с несколькими командами или отделами могут добавлять пользовательские атрибуты для различия между разными группами, используя переменную окружения `OTEL_RESOURCE_ATTRIBUTES`:

```bash theme={null}
# Добавить пользовательские атрибуты для идентификации команды
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

Эти пользовательские атрибуты будут включены во все метрики и события, позволяя вам:

* Фильтровать метрики по команде или отделу
* Отслеживать затраты по центру затрат
* Создавать панели мониторинга для конкретных команд
* Настраивать оповещения для конкретных команд

<Warning>
  **Важные требования к форматированию для OTEL\_RESOURCE\_ATTRIBUTES:**

  Переменная окружения `OTEL_RESOURCE_ATTRIBUTES` использует пары ключ=значение, разделенные запятыми, со строгими требованиями к форматированию:

  * **Пробелы не допускаются**: Значения не могут содержать пробелы. Например, `user.organizationName=My Company` недопустимо
  * **Формат**: Должны быть пары ключ=значение, разделенные запятыми: `key1=value1,key2=value2`
  * **Допустимые символы**: Только символы US-ASCII, исключая управляющие символы, пробелы, двойные кавычки, запятые, точки с запятой и обратные слэши
  * **Специальные символы**: Символы вне допустимого диапазона должны быть закодированы в процентах

  **Примеры:**

  ```bash theme={null}
  # ❌ Недопустимо - содержит пробелы
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John's Organization"

  # ✅ Допустимо - используйте подчеркивания или camelCase вместо этого
  export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"
  export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"

  # ✅ Допустимо - закодируйте специальные символы в процентах, если необходимо
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"
  ```

  Примечание: заключение значений в кавычки не экранирует пробелы. Например, `org.name="My Company"` приводит к буквальному значению `"My Company"` (с кавычками включены), а не `My Company`.
</Warning>

### Примеры конфигураций

Установите эти переменные окружения перед запуском `claude`. Каждый блок показывает полную конфигурацию для другого экспортера или сценария развертывания:

```bash theme={null}
# Отладка консоли (интервалы 1 секунда)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000

# OTLP/gRPC
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Prometheus
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus

# Несколько экспортеров
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json

# Разные endpoints/бэкенды для метрик и логов
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.example.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.example.com:4317

# Только метрики (без событий/логов)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# Только события/логи (без метрик)
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

## Доступные метрики и события

### Стандартные атрибуты

Все метрики и события имеют эти стандартные атрибуты:

| Атрибут             | Описание                                                                                                                               | Управляется                                              |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------- |
| `session.id`        | Уникальный идентификатор сеанса                                                                                                        | `OTEL_METRICS_INCLUDE_SESSION_ID` (по умолчанию: true)   |
| `app.version`       | Текущая версия Claude Code                                                                                                             | `OTEL_METRICS_INCLUDE_VERSION` (по умолчанию: false)     |
| `organization.id`   | UUID организации (при аутентификации)                                                                                                  | Всегда включается, когда доступно                        |
| `user.account_uuid` | UUID учетной записи (при аутентификации)                                                                                               | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (по умолчанию: true) |
| `user.account_id`   | ID учетной записи в формате с тегами, соответствующий API администратора Anthropic (при аутентификации), такой как `user_01BWBeN28...` | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` (по умолчанию: true) |
| `user.id`           | Анонимный идентификатор устройства/установки, генерируемый для каждой установки Claude Code                                            | Всегда включается                                        |
| `user.email`        | Адрес электронной почты пользователя (при аутентификации через OAuth)                                                                  | Всегда включается, когда доступно                        |
| `terminal.type`     | Тип терминала, такой как `iTerm.app`, `vscode`, `cursor` или `tmux`                                                                    | Всегда включается при обнаружении                        |

События дополнительно включают следующие атрибуты. Они никогда не прикрепляются к метрикам, потому что они вызовут неограниченную кардинальность:

* `prompt.id`: UUID, коррелирующий пользовательскую подсказку со всеми последующими событиями до следующей подсказки. См. [Атрибуты корреляции событий](#event-correlation-attributes).
* `workspace.host_paths`: каталоги рабочей области хоста, выбранные в приложении для рабочего стола, как массив строк

### Метрики

Claude Code экспортирует следующие метрики:

| Имя метрики                           | Описание                                                        | Единица |
| ------------------------------------- | --------------------------------------------------------------- | ------- |
| `claude_code.session.count`           | Количество запущенных сеансов CLI                               | count   |
| `claude_code.lines_of_code.count`     | Количество строк кода, которые были изменены                    | count   |
| `claude_code.pull_request.count`      | Количество созданных pull request                               | count   |
| `claude_code.commit.count`            | Количество созданных git коммитов                               | count   |
| `claude_code.cost.usage`              | Стоимость сеанса Claude Code                                    | USD     |
| `claude_code.token.usage`             | Количество использованных токенов                               | tokens  |
| `claude_code.code_edit_tool.decision` | Количество решений о разрешении инструмента редактирования кода | count   |
| `claude_code.active_time.total`       | Общее активное время в секундах                                 | s       |

### Детали метрик

Каждая метрика включает стандартные атрибуты, перечисленные выше. Метрики с дополнительными контекстно-специфичными атрибутами отмечены ниже.

#### Счетчик сеансов

Увеличивается в начале каждого сеанса.

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `start_type`: Как был запущен сеанс. Один из `"fresh"`, `"resume"` или `"continue"`

#### Счетчик строк кода

Увеличивается при добавлении или удалении кода.

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `type`: (`"added"`, `"removed"`)

#### Счетчик pull request

Увеличивается при создании pull request через Claude Code.

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)

#### Счетчик коммитов

Увеличивается при создании git коммитов через Claude Code.

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)

#### Счетчик затрат

Увеличивается после каждого запроса API.

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `model`: Идентификатор модели (например, "claude-sonnet-4-6")
* `query_source`: Категория подсистемы, которая выдала запрос. Один из `"main"`, `"subagent"` или `"auxiliary"`
* `speed`: `"fast"` когда запрос использовал быстрый режим. Отсутствует в противном случае
* `effort`: [Уровень усилий](/ru/model-config#adjust-effort-level), применяемый к запросу: `"low"`, `"medium"`, `"high"`, `"xhigh"` или `"max"`. Отсутствует, когда модель не поддерживает усилия.

#### Счетчик токенов

Увеличивается после каждого запроса API.

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `type`: (`"input"`, `"output"`, `"cacheRead"`, `"cacheCreation"`)
* `model`: Идентификатор модели (например, "claude-sonnet-4-6")
* `query_source`: Категория подсистемы, которая выдала запрос. Один из `"main"`, `"subagent"` или `"auxiliary"`
* `speed`: `"fast"` когда запрос использовал быстрый режим. Отсутствует в противном случае
* `effort`: [Уровень усилий](/ru/model-config#adjust-effort-level), применяемый к запросу. Подробности см. в разделе [Счетчик затрат](#cost-counter).

#### Счетчик решений инструмента редактирования кода

Увеличивается, когда пользователь принимает или отклоняет использование инструмента Edit, Write или NotebookEdit.

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `tool_name`: Имя инструмента (`"Edit"`, `"Write"`, `"NotebookEdit"`)
* `decision`: Решение пользователя (`"accept"`, `"reject"`)
* `source`: Источник решения - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"` или `"user_reject"`
* `language`: Язык программирования отредактированного файла, такой как `"TypeScript"`, `"Python"`, `"JavaScript"` или `"Markdown"`. Возвращает `"unknown"` для неузнанных расширений файлов.

#### Счетчик активного времени

Отслеживает фактическое время, потраченное на активное использование Claude Code, исключая время простоя. Эта метрика увеличивается во время взаимодействия пользователя (ввод текста, чтение ответов) и во время обработки CLI (выполнение инструментов, генерация ответов AI).

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `type`: `"user"` для взаимодействия с клавиатурой, `"cli"` для выполнения инструментов и ответов AI

### События

Claude Code экспортирует следующие события через логи/события OpenTelemetry (когда настроен `OTEL_LOGS_EXPORTER`):

#### Атрибуты корреляции событий

Когда пользователь отправляет подсказку, Claude Code может сделать несколько вызовов API и запустить несколько инструментов. Атрибут `prompt.id` позволяет связать все эти события с одной подсказкой, которая их вызвала.

| Атрибут     | Описание                                                                                                 |
| ----------- | -------------------------------------------------------------------------------------------------------- |
| `prompt.id` | Идентификатор UUID v4, связывающий все события, созданные при обработке одной пользовательской подсказки |

Чтобы отследить всю активность, вызванную одной подсказкой, отфильтруйте события по определенному значению `prompt.id`. Это возвращает событие user\_prompt, любые события api\_request и любые события tool\_result, которые произошли при обработке этой подсказки.

<Note>
  `prompt.id` намеренно исключен из метрик, потому что каждая подсказка генерирует уникальный ID, что создало бы постоянно растущее количество временных рядов. Используйте его только для анализа на уровне событий и аудита.
</Note>

#### Событие пользовательской подсказки

Логируется, когда пользователь отправляет подсказку.

**Имя события**: `claude_code.user_prompt`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"user_prompt"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `prompt_length`: Длина подсказки
* `prompt`: Содержимое подсказки (скрыто по умолчанию, включите с помощью `OTEL_LOG_USER_PROMPTS=1`)
* `command_name`: Имя команды, когда подсказка вызывает одну. Встроенные и поставляемые имена команд, такие как `compact` или `debug`, выдаются как есть; псевдонимы, такие как `reset`, выдаются как введено, а не как каноническое имя. Пользовательские, плагин и MCP имена команд сворачиваются в `custom` или `mcp`, если не установлен `OTEL_LOG_TOOL_DETAILS=1`
* `command_source`: Происхождение команды, когда присутствует: `builtin`, `custom` или `mcp`. Команды, предоставляемые плагинами, сообщают как `custom`

#### Событие результата инструмента

Логируется, когда инструмент завершает выполнение.

**Имя события**: `claude_code.tool_result`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"tool_result"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `tool_name`: Имя инструмента
* `tool_use_id`: Уникальный идентификатор для этого вызова инструмента. Совпадает с `tool_use_id`, переданным в hooks, позволяя корреляцию между событиями OTel и данными, захваченными hooks.
* `success`: `"true"` или `"false"`
* `duration_ms`: Время выполнения в миллисекундах
* `error_type`: Строка категории ошибки при сбое инструмента, такая как `"Error:ENOENT"` или `"ShellError"`
* `error` (когда `OTEL_LOG_TOOL_DETAILS=1`): Полное сообщение об ошибке при сбое инструмента
* `decision_type`: Либо `"accept"`, либо `"reject"`
* `decision_source`: Источник решения - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"` или `"user_reject"`
* `tool_input_size_bytes`: Размер JSON-сериализованного входа инструмента в байтах
* `tool_result_size_bytes`: Размер результата инструмента в байтах
* `mcp_server_scope`: Идентификатор области MCP сервера (для инструментов MCP)
* `tool_parameters` (когда `OTEL_LOG_TOOL_DETAILS=1`): JSON строка, содержащая параметры, специфичные для инструмента:
  * Для инструмента Bash: включает `bash_command`, `full_command`, `timeout`, `description`, `dangerouslyDisableSandbox` и `git_commit_id` (SHA коммита, когда команда `git commit` успешна)
  * Для инструментов MCP: включает `mcp_server_name`, `mcp_tool_name`
  * Для инструмента Skill: включает `skill_name`
  * Для инструмента Task: включает `subagent_type`
* `tool_input` (когда `OTEL_LOG_TOOL_DETAILS=1`): JSON-сериализованные аргументы инструмента. Отдельные значения более 512 символов усекаются, и полная нагрузка ограничена примерно 4 K символами. Применяется ко всем инструментам, включая инструменты MCP.

#### Событие запроса API

Логируется для каждого запроса API к Claude.

**Имя события**: `claude_code.api_request`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"api_request"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `model`: Используемая модель (например, "claude-sonnet-4-6")
* `cost_usd`: Приблизительная стоимость в USD
* `duration_ms`: Длительность запроса в миллисекундах
* `input_tokens`: Количество входных токенов
* `output_tokens`: Количество выходных токенов
* `cache_read_tokens`: Количество токенов, прочитанных из кэша
* `cache_creation_tokens`: Количество токенов, использованных для создания кэша
* `request_id`: ID запроса Anthropic API из заголовка ответа `request-id`, такой как `"req_011..."`. Присутствует только, когда API возвращает его.
* `speed`: `"fast"` или `"normal"`, указывающий, был ли активен быстрый режим
* `query_source`: Подсистема, которая выдала запрос, такая как `"repl_main_thread"`, `"compact"` или имя подагента
* `effort`: [Уровень усилий](/ru/model-config#adjust-effort-level), применяемый к запросу: `"low"`, `"medium"`, `"high"`, `"xhigh"` или `"max"`. Отсутствует, когда модель не поддерживает усилия.

#### Событие ошибки API

Логируется, когда запрос API к Claude не удается.

**Имя события**: `claude_code.api_error`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"api_error"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `model`: Используемая модель (например, "claude-sonnet-4-6")
* `error`: Сообщение об ошибке
* `status_code`: HTTP код состояния в виде числа. Отсутствует для ошибок, не связанных с HTTP, таких как сбои соединения.
* `duration_ms`: Длительность запроса в миллисекундах
* `attempt`: Общее количество попыток, включая исходный запрос (`1` означает, что повторных попыток не было)
* `request_id`: ID запроса Anthropic API из заголовка ответа `request-id`, такой как `"req_011..."`. Присутствует только, когда API возвращает его.
* `speed`: `"fast"` или `"normal"`, указывающий, был ли активен быстрый режим
* `query_source`: Подсистема, которая выдала запрос, такая как `"repl_main_thread"`, `"compact"` или имя подагента
* `effort`: [Уровень усилий](/ru/model-config#adjust-effort-level), применяемый к запросу. Отсутствует, когда модель не поддерживает усилия.

#### Событие тела запроса API

Логируется для каждой попытки запроса API, когда установлен `OTEL_LOG_RAW_API_BODIES`. Одно событие выдается за попытку, поэтому повторные попытки с скорректированными параметрами каждая производят свое собственное событие.

**Имя события**: `claude_code.api_request_body`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"api_request_body"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `body`: JSON-сериализованные параметры запроса Messages API (системная подсказка, сообщения, инструменты и т.д.), усеченные на 60 КБ. Содержимое расширенного мышления в предыдущих ходах помощника скрыто. Выдается только в встроенном режиме (`OTEL_LOG_RAW_API_BODIES=1`).
* `body_ref`: Абсолютный путь к файлу `<dir>/<uuid>.request.json`, содержащему неусеченное тело. Выдается только в режиме файла (`OTEL_LOG_RAW_API_BODIES=file:<dir>`).
* `body_length`: Длина неусеченного тела. UTF-8 байты, когда `OTEL_LOG_RAW_API_BODIES=file:<dir>`, или единицы кода UTF-16, когда `=1`
* `body_truncated`: `"true"` когда произошло встроенное усечение. Отсутствует в режиме файла и когда усечение не произошло.
* `model`: Идентификатор модели из параметров запроса
* `query_source`: Подсистема, которая выдала запрос (например, `"compact"`)

#### Событие тела ответа API

Логируется для каждого успешного ответа API, когда установлен `OTEL_LOG_RAW_API_BODIES`.

**Имя события**: `claude_code.api_response_body`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"api_response_body"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `body`: JSON-сериализованный ответ Messages API (id, блоки содержимого, использование, причина остановки), усеченный на 60 КБ. Содержимое расширенного мышления скрыто. Выдается только в встроенном режиме (`OTEL_LOG_RAW_API_BODIES=1`).
* `body_ref`: Абсолютный путь к файлу `<dir>/<request_id>.response.json`, содержащему неусеченное тело. Выдается только в режиме файла (`OTEL_LOG_RAW_API_BODIES=file:<dir>`).
* `body_length`: Длина неусеченного тела. UTF-8 байты, когда `OTEL_LOG_RAW_API_BODIES=file:<dir>`, или единицы кода UTF-16, когда `=1`
* `body_truncated`: `"true"` когда произошло встроенное усечение. Отсутствует в режиме файла и когда усечение не произошло.
* `model`: Идентификатор модели
* `query_source`: Подсистема, которая выдала запрос
* `request_id`: ID запроса Anthropic API из заголовка ответа `request-id`, такой как `"req_011..."`. Присутствует только, когда API возвращает его.

#### Событие решения инструмента

Логируется, когда принимается решение о разрешении инструмента (принять/отклонить).

**Имя события**: `claude_code.tool_decision`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"tool_decision"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `tool_name`: Имя инструмента (например, "Read", "Edit", "Write", "NotebookEdit")
* `tool_use_id`: Уникальный идентификатор для этого вызова инструмента. Совпадает с `tool_use_id`, переданным в hooks, позволяя корреляцию между событиями OTel и данными, захваченными hooks.
* `decision`: Либо `"accept"`, либо `"reject"`
* `source`: Источник решения - `"config"`, `"hook"`, `"user_permanent"`, `"user_temporary"`, `"user_abort"` или `"user_reject"`

#### Событие изменения режима разрешений

Логируется, когда режим разрешений изменяется, например при циклировании Shift+Tab, выходе из Plan Mode или проверке gate автоматического режима.

**Имя события**: `claude_code.permission_mode_changed`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"permission_mode_changed"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `from_mode`: Предыдущий режим разрешений, например `"default"`, `"plan"`, `"acceptEdits"`, `"auto"` или `"bypassPermissions"`
* `to_mode`: Новый режим разрешений
* `trigger`: Что вызвало изменение. Один из `"shift_tab"`, `"exit_plan_mode"`, `"auto_gate_denied"` или `"auto_opt_in"`. Отсутствует, когда переход исходит из SDK или моста

#### Событие аутентификации

Логируется, когда `/login` или `/logout` завершается.

**Имя события**: `claude_code.auth`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"auth"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `action`: `"login"` или `"logout"`
* `success`: `"true"` или `"false"`
* `auth_method`: Метод аутентификации, такой как `"oauth"`
* `error_category`: Категориальный вид ошибки при сбое действия. Исходное сообщение об ошибке никогда не включается
* `status_code`: HTTP код состояния в виде строки при сбое действия с ошибкой HTTP

#### Событие подключения MCP сервера

Логируется, когда MCP сервер подключается, отключается или не удается подключиться.

**Имя события**: `claude_code.mcp_server_connection`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"mcp_server_connection"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `status`: `"connected"`, `"failed"` или `"disconnected"`
* `transport_type`: Транспорт сервера, такой как `"stdio"`, `"sse"` или `"http"`
* `server_scope`: Область, в которой настроен сервер, такая как `"user"`, `"project"` или `"local"`
* `duration_ms`: Длительность попытки подключения в миллисекундах
* `error_code`: Код ошибки при сбое подключения
* `server_name` (когда `OTEL_LOG_TOOL_DETAILS=1`): Настроенное имя сервера
* `error` (когда `OTEL_LOG_TOOL_DETAILS=1`): Полное сообщение об ошибке при сбое подключения

#### Событие внутренней ошибки

Логируется, когда Claude Code перехватывает неожиданную внутреннюю ошибку. Записываются только имя класса ошибки и код в стиле errno. Сообщение об ошибке и трассировка стека никогда не включаются. Это событие не выдается при запуске против Bedrock, Vertex или Foundry, или когда установлен `DISABLE_ERROR_REPORTING`.

**Имя события**: `claude_code.internal_error`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"internal_error"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `error_name`: Имя класса ошибки, такой как `"TypeError"` или `"SyntaxError"`
* `error_code`: Код errno Node.js, такой как `"ENOENT"`, когда присутствует в ошибке

#### Событие установки плагина

Логируется, когда плагин завершает установку, как из команды CLI `claude plugin install`, так и из интерактивного UI `/plugin`.

**Имя события**: `claude_code.plugin_installed`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"plugin_installed"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `marketplace.is_official`: `"true"` если маркетплейс является официальным маркетплейсом Anthropic, `"false"` в противном случае
* `install.trigger`: `"cli"` или `"ui"`
* `plugin.name`: Имя установленного плагина. Для сторонних маркетплейсов это включается только, когда `OTEL_LOG_TOOL_DETAILS=1`
* `plugin.version`: Версия плагина, когда объявлена в записи маркетплейса. Для сторонних маркетплейсов это включается только, когда `OTEL_LOG_TOOL_DETAILS=1`
* `marketplace.name`: Маркетплейс, из которого был установлен плагин. Для сторонних маркетплейсов это включается только, когда `OTEL_LOG_TOOL_DETAILS=1`

#### Событие активации навыка

Логируется, когда навык вызывается, будь то Claude вызывает его через инструмент Skill или вы запускаете его как команду `/`.

**Имя события**: `claude_code.skill_activated`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"skill_activated"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `skill.name`: Имя навыка. Для определяемых пользователем и сторонних плагин навыков значение является заполнителем `"custom_skill"`, если не установлен `OTEL_LOG_TOOL_DETAILS=1`
* `invocation_trigger`: Как был вызван навык (`"user-slash"`, `"claude-proactive"` или `"nested-skill"`)
* `skill.source`: Откуда был загружен навык (например, `"bundled"`, `"userSettings"`, `"projectSettings"`, `"plugin"`)
* `plugin.name` (когда `OTEL_LOG_TOOL_DETAILS=1` или плагин из официального маркетплейса): Имя владельца плагина, когда навык предоставляется плагином
* `marketplace.name` (когда `OTEL_LOG_TOOL_DETAILS=1` или плагин из официального маркетплейса): Маркетплейс владельца плагина, когда навык предоставляется плагином

#### Событие упоминания @

Логируется, когда Claude Code разрешает упоминание `@` в подсказке. Не каждое упоминание выдает событие: пути раннего выхода, такие как отказ в разрешении, файлы большого размера, вложения ссылок PDF и сбои при перечислении каталогов, возвращаются без логирования.

**Имя события**: `claude_code.at_mention`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"at_mention"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `mention_type`: Тип упоминания (`"file"`, `"directory"`, `"agent"`, `"mcp_resource"`)
* `success`: Было ли упоминание успешно разрешено (`"true"` или `"false"`)

#### Событие исчерпания повторных попыток API

Логируется один раз, когда запрос API не удается после более чем одной попытки. Выдается вместе с финальным событием `api_error`.

**Имя события**: `claude_code.api_retries_exhausted`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"api_retries_exhausted"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `model`: Используемая модель
* `error`: Финальное сообщение об ошибке
* `status_code`: HTTP код состояния в виде числа. Отсутствует для ошибок, не связанных с HTTP.
* `total_attempts`: Общее количество попыток
* `total_retry_duration_ms`: Общее время в реальном времени по всем попыткам
* `speed`: `"fast"` или `"normal"`

#### Событие начала выполнения hook

Логируется, когда один или несколько hooks начинают выполняться для события hook.

**Имя события**: `claude_code.hook_execution_start`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"hook_execution_start"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `hook_event`: Тип события hook, такой как `"PreToolUse"` или `"PostToolUse"`
* `hook_name`: Полное имя hook, включая matcher, такой как `"PreToolUse:Write"`
* `num_hooks`: Количество соответствующих команд hook
* `managed_only`: `"true"` когда разрешены только управляемые политики hooks
* `hook_source`: `"policySettings"` или `"merged"`
* `hook_definitions`: JSON-сериализованная конфигурация hook. Включается только, когда включены как детальная бета-трассировка, так и `OTEL_LOG_TOOL_DETAILS=1`

#### Событие завершения выполнения hook

Логируется, когда все hooks для события hook завершены.

**Имя события**: `claude_code.hook_execution_complete`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"hook_execution_complete"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `hook_event`: Тип события hook
* `hook_name`: Полное имя hook, включая matcher
* `num_hooks`: Количество соответствующих команд hook
* `num_success`: Количество, которые завершились успешно
* `num_blocking`: Количество, которые вернули решение блокировки
* `num_non_blocking_error`: Количество, которые не удались без блокировки
* `num_cancelled`: Количество, отмененные до завершения
* `total_duration_ms`: Длительность в реальном времени всех соответствующих hooks
* `managed_only`: `"true"` когда разрешены только управляемые политики hooks
* `hook_source`: `"policySettings"` или `"merged"`
* `hook_definitions`: JSON-сериализованная конфигурация hook. Включается только, когда включены как детальная бета-трассировка, так и `OTEL_LOG_TOOL_DETAILS=1`

#### Событие компактирования

Логируется, когда компактирование разговора завершается.

**Имя события**: `claude_code.compaction`

**Атрибуты**:

* Все [стандартные атрибуты](#standard-attributes)
* `event.name`: `"compaction"`
* `event.timestamp`: Временная метка ISO 8601
* `event.sequence`: монотонно возрастающий счетчик для упорядочивания событий в сеансе
* `trigger`: `"auto"` или `"manual"`
* `success`: `"true"` или `"false"`
* `duration_ms`: Длительность компактирования
* `pre_tokens`: Приблизительное количество токенов до компактирования
* `post_tokens`: Приблизительное количество токенов после компактирования
* `error`: Сообщение об ошибке при сбое компактирования

## Интерпретация данных метрик и событий

Экспортируемые метрики и события поддерживают ряд анализов:

### Мониторинг использования

| Метрика                                                       | Возможность анализа                                                |
| ------------------------------------------------------------- | ------------------------------------------------------------------ |
| `claude_code.token.usage`                                     | Разбить по `type` (input/output), пользователю, команде или модели |
| `claude_code.session.count`                                   | Отслеживать принятие и вовлеченность с течением времени            |
| `claude_code.lines_of_code.count`                             | Измерить производительность, отслеживая добавления/удаления кода   |
| `claude_code.commit.count` & `claude_code.pull_request.count` | Понять влияние на рабочие процессы разработки                      |

### Мониторинг затрат

Метрика `claude_code.cost.usage` помогает с:

* Отслеживанием тенденций использования по командам или отдельным лицам
* Выявлением сеансов с высоким использованием для оптимизации

<Note>
  Метрики затрат являются приблизительными. Для официальных данных о выставлении счетов обратитесь к вашему поставщику API (Claude Console, AWS Bedrock или Google Cloud Vertex).
</Note>

### Оповещения и сегментация

Распространенные оповещения, которые следует рассмотреть:

* Скачки затрат
* Необычное потребление токенов
* Высокий объем сеансов от конкретных пользователей

Все метрики можно сегментировать по `user.account_uuid`, `user.account_id`, `organization.id`, `session.id`, `model` и `app.version`.

### Обнаружение исчерпания повторных попыток

Claude Code повторяет неудачные запросы API внутри и выдает одно событие `claude_code.api_error` только после того, как сдается, поэтому само событие является терминальным сигналом для этого запроса. Промежуточные повторные попытки не логируются как отдельные события.

Атрибут `attempt` на событии записывает, сколько попыток было сделано в общей сложности. Значение больше `CLAUDE_CODE_MAX_RETRIES` (по умолчанию `10`) указывает, что запрос исчерпал все повторные попытки при переходной ошибке. Более низкое значение указывает на неповторяемую ошибку, такую как ответ `400`.

Чтобы различить сеанс, который восстановился, от того, который застопорился, сгруппируйте события по `session.id` и проверьте, существует ли более позднее событие `api_request` после ошибки.

### Анализ событий

Данные событий предоставляют подробные сведения о взаимодействиях Claude Code:

**Паттерны использования инструментов**: анализируйте события результатов инструментов для выявления:

* Наиболее часто используемых инструментов
* Показателей успеха инструментов
* Среднего времени выполнения инструментов
* Паттернов ошибок по типам инструментов

**Мониторинг производительности**: отслеживайте длительность запросов API и время выполнения инструментов для выявления узких мест производительности.

## Рассмотрения бэкенда

Выбор вашего бэкенда метрик, логов и трассировок определяет типы анализов, которые вы можете выполнять:

### Для метрик

* **Базы данных временных рядов (например, Prometheus)**: Расчеты скорости, агрегированные метрики
* **Колончатые хранилища (например, ClickHouse)**: Сложные запросы, анализ уникальных пользователей
* **Полнофункциональные платформы наблюдаемости (например, Honeycomb, Datadog)**: Продвинутые запросы, визуализация, оповещения

### Для событий/логов

* **Системы агрегации логов (например, Elasticsearch, Loki)**: Полнотекстовый поиск, анализ логов
* **Колончатые хранилища (например, ClickHouse)**: Анализ структурированных событий
* **Полнофункциональные платформы наблюдаемости (например, Honeycomb, Datadog)**: Корреляция между метриками и событиями

### Для трассировок

Выберите бэкенд, поддерживающий хранилище распределенных трассировок и корреляцию span:

* **Системы распределенной трассировки (например, Jaeger, Zipkin, Grafana Tempo)**: Визуализация span, водопады запросов, анализ задержки
* **Полнофункциональные платформы наблюдаемости (например, Honeycomb, Datadog)**: Поиск трассировок и корреляция с метриками и логами

Для организаций, требующих метрик Daily/Weekly/Monthly Active User (DAU/WAU/MAU), рассмотрите бэкенды, поддерживающие эффективные запросы уникальных значений.

## Информация о сервисе

Все метрики и события экспортируются со следующими атрибутами ресурса:

* `service.name`: `claude-code`
* `service.version`: Текущая версия Claude Code
* `os.type`: Тип операционной системы (например, `linux`, `darwin`, `windows`)
* `os.version`: Строка версии операционной системы
* `host.arch`: Архитектура хоста (например, `amd64`, `arm64`)
* `wsl.version`: Номер версии WSL (присутствует только при запуске на Windows Subsystem for Linux)
* Имя счетчика: `com.anthropic.claude_code`

## Ресурсы для измерения ROI

Для полного руководства по измерению возврата инвестиций для Claude Code, включая настройку телеметрии, анализ затрат, метрики производительности и автоматизированные отчеты, см. [Руководство по измерению ROI Claude Code](https://github.com/anthropics/claude-code-monitoring-guide). Этот репозиторий предоставляет готовые конфигурации Docker Compose, настройки Prometheus и OpenTelemetry, а также шаблоны для создания отчетов о производительности, интегрированные с такими инструментами, как Linear.

## Безопасность и конфиденциальность

* Экспорт OpenTelemetry на ваш бэкенд является добровольным и требует явной конфигурации. Информацию об отдельной операционной телеметрии Anthropic и о том, как её отключить, см. в разделе [Data usage](/ru/data-usage#telemetry-services)
* Содержимое файлов в исходном виде и фрагменты кода не включаются в метрики или события. Span трассировок — это отдельный путь данных: см. пункт `OTEL_LOG_TOOL_CONTENT` ниже
* При аутентификации через OAuth `user.email` включается в атрибуты телеметрии. Если это вызывает беспокойство для вашей организации, работайте с вашим бэкендом телеметрии для фильтрации или редактирования этого поля
* Содержимое пользовательской подсказки не собирается по умолчанию. Записывается только длина подсказки. Чтобы включить содержимое подсказки, установите `OTEL_LOG_USER_PROMPTS=1`
* Аргументы входных данных инструмента и параметры не логируются по умолчанию. Чтобы включить их, установите `OTEL_LOG_TOOL_DETAILS=1`. Когда включено, события `tool_result` включают атрибут `tool_parameters` с командами Bash, именами MCP сервера и инструмента и именами навыков, плюс атрибут `tool_input` с путями к файлам, URL-адресами, шаблонами поиска и другими аргументами. События `user_prompt` включают буквальное `command_name` для пользовательских, plugin и MCP команд. Span трассировки включают тот же атрибут `tool_input` и атрибуты, полученные из входных данных, такие как `file_path`. Отдельные значения более 512 символов усекаются, и общее количество ограничено примерно 4 K символами, но аргументы могут по-прежнему содержать конфиденциальные значения. Настройте ваш бэкенд телеметрии для фильтрации или редактирования этих атрибутов по мере необходимости
* Входные и выходные данные инструмента не логируются в span событиях по умолчанию. Чтобы включить их, установите `OTEL_LOG_TOOL_CONTENT=1`. Когда включено, события span включают полное содержимое входных и выходных данных инструмента, усеченное на 60 КБ на span. Это может включать содержимое исходного файла из результатов инструмента Read и выходные данные команды Bash. Настройте ваш бэкенд телеметрии для фильтрации или редактирования этих атрибутов по мере необходимости
* Тела запроса и ответа Anthropic Messages API в исходном виде не логируются по умолчанию. Чтобы включить их, установите `OTEL_LOG_RAW_API_BODIES`. С `=1` каждый вызов API выдает события логов `api_request_body` и `api_response_body`, чей атрибут `body` является JSON-сериализованной нагрузкой, усеченной на 60 КБ. С `=file:<dir>`, неусеченные тела записываются в файлы `.request.json` и `.response.json` в этом каталоге, и события несут путь `body_ref` вместо встроенного тела. Отправьте каталог с коллектором логов или sidecar, а не через поток телеметрии. В обоих режимах тела содержат полную историю разговора (системная подсказка, каждый предыдущий ход пользователя и помощника, результаты инструментов), поэтому включение этого подразумевает согласие со всем, что раскрыли бы другие флаги содержимого `OTEL_LOG_*`. Содержимое расширенного мышления Claude всегда скрыто из этих тел независимо от других параметров

## Мониторинг Claude Code на Amazon Bedrock

Для подробного руководства по мониторингу использования Claude Code для Amazon Bedrock см. [Реализация мониторинга Claude Code (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md).
