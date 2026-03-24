> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code на Google Vertex AI

> Узнайте о настройке Claude Code через Google Vertex AI, включая установку, конфигурацию IAM и устранение неполадок.

## Предварительные требования

Перед настройкой Claude Code с Vertex AI убедитесь, что у вас есть:

* Учетная запись Google Cloud Platform (GCP) с включенной биллингом
* Проект GCP с включенным API Vertex AI
* Доступ к нужным моделям Claude (например, Claude Sonnet 4.6)
* Установленный и настроенный Google Cloud SDK (`gcloud`)
* Квота, выделенная в нужном регионе GCP

<Note>
  Если вы развертываете Claude Code для нескольких пользователей, [закрепите версии ваших моделей](#5-pin-model-versions), чтобы предотвратить сбои при выпуске Anthropic новых моделей.
</Note>

## Конфигурация региона

Claude Code можно использовать как с [глобальными](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai), так и с региональными конечными точками Vertex AI.

<Note>
  Vertex AI может не поддерживать модели Claude Code по умолчанию во всех [регионах](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models) или на [глобальных конечных точках](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models). Вам может потребоваться переключиться на поддерживаемый регион, использовать региональную конечную точку или указать поддерживаемую модель.
</Note>

## Установка

### 1. Включите API Vertex AI

Включите API Vertex AI в вашем проекте GCP:

```bash  theme={null}
# Установите ID вашего проекта
gcloud config set project YOUR-PROJECT-ID

# Включите API Vertex AI
gcloud services enable aiplatform.googleapis.com
```

### 2. Запросите доступ к модели

Запросите доступ к моделям Claude в Vertex AI:

1. Перейдите в [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Найдите модели "Claude"
3. Запросите доступ к нужным моделям Claude (например, Claude Sonnet 4.6)
4. Дождитесь одобрения (может занять 24-48 часов)

### 3. Настройте учетные данные GCP

Claude Code использует стандартную аутентификацию Google Cloud.

Для получения дополнительной информации см. [документацию по аутентификации Google Cloud](https://cloud.google.com/docs/authentication).

<Note>
  При аутентификации Claude Code автоматически будет использовать ID проекта из переменной окружения `ANTHROPIC_VERTEX_PROJECT_ID`. Чтобы переопределить это, установите одну из этих переменных окружения: `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT` или `GOOGLE_APPLICATION_CREDENTIALS`.
</Note>

### 4. Настройте Claude Code

Установите следующие переменные окружения:

```bash  theme={null}
# Включите интеграцию Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Опционально: отключите кэширование запросов, если необходимо
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

[Кэширование запросов](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) автоматически поддерживается при указании флага `cache_control` ephemeral. Чтобы отключить его, установите `DISABLE_PROMPT_CACHING=1`. Для повышенных лимитов скорости обратитесь в поддержку Google Cloud. При использовании Vertex AI команды `/login` и `/logout` отключены, так как аутентификация обрабатывается через учетные данные Google Cloud.

### 5. Закрепите версии моделей

<Warning>
  Закрепите конкретные версии моделей для каждого развертывания. Если вы используете псевдонимы моделей (`sonnet`, `opus`, `haiku`) без закрепления, Claude Code может попытаться использовать более новую версию модели, которая не включена в вашем проекте Vertex AI, что приведет к сбою существующих пользователей при выпуске обновлений Anthropic.
</Warning>

Установите эти переменные окружения на конкретные ID моделей Vertex AI:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

Для текущих и устаревших ID моделей см. [Обзор моделей](https://platform.claude.com/docs/en/about-claude/models/overview). Полный список переменных окружения см. в разделе [Конфигурация моделей](/ru/model-config#pin-models-for-third-party-deployments).

Claude Code использует эти модели по умолчанию, когда переменные закрепления не установлены:

| Тип модели           | Значение по умолчанию       |
| :------------------- | :-------------------------- |
| Основная модель      | `claude-sonnet-4-6`         |
| Малая/быстрая модель | `claude-haiku-4-5@20251001` |

Для дальнейшей настройки моделей:

```bash  theme={null}
export ANTHROPIC_MODEL='claude-opus-4-6'
export ANTHROPIC_SMALL_FAST_MODEL='claude-haiku-4-5@20251001'
```

## Конфигурация IAM

Назначьте требуемые разрешения IAM:

Роль `roles/aiplatform.user` включает требуемые разрешения:

* `aiplatform.endpoints.predict` - требуется для вызова модели и подсчета токенов

Для более строгих разрешений создайте пользовательскую роль только с указанными выше разрешениями.

Для получения дополнительной информации см. [документацию Vertex IAM](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Создайте выделенный проект GCP для Claude Code, чтобы упростить отслеживание затрат и контроль доступа.
</Note>

## Контекстное окно с 1M токенов

Claude Opus 4.6, Sonnet 4.6, Sonnet 4.5 и Sonnet 4 поддерживают [контекстное окно с 1M токенов](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) на Vertex AI. Claude Code автоматически включает расширенное контекстное окно при выборе варианта модели с 1M.

Чтобы включить контекстное окно с 1M для вашей закрепленной модели, добавьте `[1m]` к ID модели. Подробности см. в разделе [Закрепите модели для развертываний третьих сторон](/ru/model-config#pin-models-for-third-party-deployments).

## Устранение неполадок

Если вы столкнулись с проблемами квоты:

* Проверьте текущие квоты или запросите увеличение квоты через [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

Если вы столкнулись с ошибками "model not found" 404:

* Подтвердите, что модель включена в [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Проверьте, что у вас есть доступ к указанному региону
* Если вы используете `CLOUD_ML_REGION=global`, проверьте, что ваши модели поддерживают глобальные конечные точки в [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) в разделе "Supported features". Для моделей, которые не поддерживают глобальные конечные точки, либо:
  * Укажите поддерживаемую модель через `ANTHROPIC_MODEL` или `ANTHROPIC_SMALL_FAST_MODEL`, либо
  * Установите региональную конечную точку, используя переменные окружения `VERTEX_REGION_<MODEL_NAME>`

Если вы столкнулись с ошибками 429:

* Для региональных конечных точек убедитесь, что основная модель и малая/быстрая модель поддерживаются в выбранном регионе
* Рассмотрите возможность переключения на `CLOUD_ML_REGION=global` для лучшей доступности

## Дополнительные ресурсы

* [Документация Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Цены Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Квоты и лимиты Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
