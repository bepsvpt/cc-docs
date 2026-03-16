> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code на Google Vertex AI

> Узнайте о настройке Claude Code через Google Vertex AI, включая установку, конфигурацию IAM и устранение неполадок.

## Предварительные требования

Перед настройкой Claude Code с Vertex AI убедитесь, что у вас есть:

* Учетная запись Google Cloud Platform (GCP) с включенной биллингом
* Проект GCP с включенным API Vertex AI
* Доступ к нужным моделям Claude (например, Claude Sonnet 4.5)
* Установленный и настроенный Google Cloud SDK (`gcloud`)
* Квота, выделенная в нужном регионе GCP

## Конфигурация региона

Claude Code можно использовать как с [глобальными](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai), так и с региональными конечными точками Vertex AI.

<Note>
  Vertex AI может не поддерживать модели Claude Code по умолчанию во всех регионах. Вам может потребоваться переключиться на [поддерживаемый регион или модель](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models).
</Note>

<Note>
  Vertex AI может не поддерживать модели Claude Code по умолчанию на глобальных конечных точках. Вам может потребоваться переключиться на региональную конечную точку или [поддерживаемую модель](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models).
</Note>

## Установка

### 1. Включение API Vertex AI

Включите API Vertex AI в вашем проекте GCP:

```bash  theme={null}
# Установите ID вашего проекта
gcloud config set project YOUR-PROJECT-ID

# Включите API Vertex AI
gcloud services enable aiplatform.googleapis.com
```

### 2. Запрос доступа к модели

Запросите доступ к моделям Claude в Vertex AI:

1. Перейдите в [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Найдите модели "Claude"
3. Запросите доступ к нужным моделям Claude (например, Claude Sonnet 4.5)
4. Дождитесь одобрения (может занять 24-48 часов)

### 3. Конфигурация учетных данных GCP

Claude Code использует стандартную аутентификацию Google Cloud.

Для получения дополнительной информации см. [документацию по аутентификации Google Cloud](https://cloud.google.com/docs/authentication).

<Note>
  При аутентификации Claude Code автоматически будет использовать ID проекта из переменной окружения `ANTHROPIC_VERTEX_PROJECT_ID`. Чтобы переопределить это, установите одну из этих переменных окружения: `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT` или `GOOGLE_APPLICATION_CREDENTIALS`.
</Note>

### 4. Конфигурация Claude Code

Установите следующие переменные окружения:

```bash  theme={null}
# Включите интеграцию Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Опционально: отключите кэширование промптов при необходимости
export DISABLE_PROMPT_CACHING=1

# Когда CLOUD_ML_REGION=global, переопределите регион для неподдерживаемых моделей
export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-east5

# Опционально: переопределите регионы для других конкретных моделей
export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5
export VERTEX_REGION_CLAUDE_3_7_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west1
export VERTEX_REGION_CLAUDE_4_0_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_1_OPUS=europe-west1
```

<Note>
  [Кэширование промптов](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) автоматически поддерживается при указании флага `cache_control` ephemeral. Чтобы отключить его, установите `DISABLE_PROMPT_CACHING=1`. Для повышенных лимитов скорости обратитесь в поддержку Google Cloud.
</Note>

<Note>
  При использовании Vertex AI команды `/login` и `/logout` отключены, так как аутентификация обрабатывается через учетные данные Google Cloud.
</Note>

### 5. Конфигурация модели

Claude Code использует эти модели по умолчанию для Vertex AI:

| Тип модели           | Значение по умолчанию        |
| :------------------- | :--------------------------- |
| Основная модель      | `claude-sonnet-4-5@20250929` |
| Малая/быстрая модель | `claude-haiku-4-5@20251001`  |

<Note>
  Для пользователей Vertex AI Claude Code не будет автоматически обновляться с Haiku 3.5 на Haiku 4.5. Чтобы вручную переключиться на более новую модель Haiku, установите переменную окружения `ANTHROPIC_DEFAULT_HAIKU_MODEL` на полное имя модели (например, `claude-haiku-4-5@20251001`).
</Note>

Для настройки моделей:

```bash  theme={null}
export ANTHROPIC_MODEL='claude-opus-4-1@20250805'
export ANTHROPIC_SMALL_FAST_MODEL='claude-haiku-4-5@20251001'
```

## Конфигурация IAM

Назначьте требуемые разрешения IAM:

Роль `roles/aiplatform.user` включает требуемые разрешения:

* `aiplatform.endpoints.predict` - требуется для вызова модели и подсчета токенов

Для более строгих разрешений создайте пользовательскую роль только с указанными выше разрешениями.

Для получения подробной информации см. [документацию Vertex IAM](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Мы рекомендуем создать выделенный проект GCP для Claude Code, чтобы упростить отслеживание затрат и управление доступом.
</Note>

## Контекстное окно на 1M токенов

Claude Sonnet 4 и Sonnet 4.5 поддерживают [контекстное окно на 1M токенов](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) на Vertex AI.

<Note>
  Контекстное окно на 1M токенов в настоящее время находится в бета-версии. Чтобы использовать расширенное контекстное окно, включите заголовок бета-версии `context-1m-2025-08-07` в ваши запросы Vertex AI.
</Note>

## Устранение неполадок

Если вы столкнулись с проблемами квоты:

* Проверьте текущие квоты или запросите увеличение квоты через [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

Если вы столкнулись с ошибками "model not found" 404:

* Подтвердите, что модель включена в [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Проверьте, что у вас есть доступ к указанному региону
* Если используется `CLOUD_ML_REGION=global`, проверьте, что ваши модели поддерживают глобальные конечные точки в [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) в разделе "Supported features". Для моделей, которые не поддерживают глобальные конечные точки, либо:
  * Укажите поддерживаемую модель через `ANTHROPIC_MODEL` или `ANTHROPIC_SMALL_FAST_MODEL`, либо
  * Установите региональную конечную точку, используя переменные окружения `VERTEX_REGION_<MODEL_NAME>`

Если вы столкнулись с ошибками 429:

* Для региональных конечных точек убедитесь, что основная модель и малая/быстрая модель поддерживаются в выбранном регионе
* Рассмотрите возможность переключения на `CLOUD_ML_REGION=global` для лучшей доступности

## Дополнительные ресурсы

* [Документация Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Цены Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Квоты и лимиты Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
