> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code на Google Vertex AI

> Узнайте о настройке Claude Code через Google Vertex AI, включая установку, конфигурацию IAM и устранение неполадок.

export const ContactSalesCard = ({surface}) => {
  const utm = content => `utm_source=claude_code&utm_medium=docs&utm_content=${surface}_${content}`;
  const iconArrowRight = (size = 13) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>;
  const STYLES = `
.cc-cs {
  --cs-slate: #141413;
  --cs-clay: #d97757;
  --cs-clay-deep: #c6613f;
  --cs-gray-000: #ffffff;
  --cs-gray-700: #3d3d3a;
  --cs-border-default: rgba(31, 30, 29, 0.15);
  font-family: inherit;
}
.dark .cc-cs {
  --cs-slate: #f0eee6;
  --cs-gray-000: #262624;
  --cs-gray-700: #bfbdb4;
  --cs-border-default: rgba(240, 238, 230, 0.14);
}
.cc-cs-card {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; padding: 14px 16px; margin: 0;
  background: var(--cs-gray-000); border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; flex-wrap: wrap;
}
.cc-cs-text { font-size: 13px; color: var(--cs-gray-700); line-height: 1.5; flex: 1; min-width: 240px; }
.cc-cs-text strong { font-weight: 550; color: var(--cs-slate); }
.cc-cs-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.cc-cs-btn-clay {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--cs-clay-deep); color: #fff; border: none;
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
  transition: background-color 0.15s; white-space: nowrap;
}
.cc-cs-btn-clay:hover { background: var(--cs-clay); }
.cc-cs-btn-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; color: var(--cs-gray-700);
  border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
}
.cc-cs-btn-ghost:hover { background: rgba(0, 0, 0, 0.04); }
.dark .cc-cs-btn-ghost:hover { background: rgba(255, 255, 255, 0.04); }
@media (max-width: 720px) {
  .cc-cs-actions { width: 100%; }
}
`;
  return <div className="cc-cs not-prose">
      <style>{STYLES}</style>
      <div className="cc-cs-card">
        <div className="cc-cs-text">
          <strong>Deploying Claude Code across your organization?</strong> Talk to sales about enterprise plans, SSO, and centralized billing.
        </div>
        <div className="cc-cs-actions">
          <a href={`https://claude.com/pricing?${utm('view_plans')}#plans-business`} className="cc-cs-btn-ghost">
            View plans
          </a>
          <a href={`https://claude.com/contact-sales?${utm('contact_sales')}`} className="cc-cs-btn-clay">
            Contact sales {iconArrowRight()}
          </a>
        </div>
      </div>
    </div>;
};

<ContactSalesCard surface="vertex" />

## Предварительные требования

Перед настройкой Claude Code с Vertex AI убедитесь, что у вас есть:

* Учетная запись Google Cloud Platform (GCP) с включенной биллингом
* Проект GCP с включенным API Vertex AI
* Доступ к нужным моделям Claude (например, Claude Sonnet 4.6)
* Установленный и настроенный Google Cloud SDK (`gcloud`)
* Квота, выделенная в нужном регионе GCP

Чтобы войти со своими учетными данными Vertex AI, следуйте инструкциям [Вход с Vertex AI](#sign-in-with-vertex-ai) ниже. Чтобы развернуть Claude Code для команды, используйте шаги [ручной установки](#set-up-manually) и [закрепите версии ваших моделей](#5-pin-model-versions) перед развертыванием.

## Вход с Vertex AI

Если у вас есть учетные данные Google Cloud и вы хотите начать использовать Claude Code через Vertex AI, мастер входа проведет вас через этот процесс. Вы выполняете предварительные требования на стороне GCP один раз для каждого проекта; мастер обрабатывает сторону Claude Code.

<Note>
  Мастер установки Vertex AI требует Claude Code v2.1.98 или более поздней версии. Запустите `claude --version` для проверки.
</Note>

<Steps>
  <Step title="Включите модели Claude в вашем проекте GCP">
    [Включите API Vertex AI](#1-enable-vertex-ai-api) для вашего проекта, затем запросите доступ к моделям Claude, которые вам нужны, в [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden). См. [Конфигурация IAM](#iam-configuration) для разрешений, которые требуются вашей учетной записи.
  </Step>

  <Step title="Запустите Claude Code и выберите Vertex AI">
    Запустите `claude`. В приглашении входа выберите **3rd-party platform**, затем **Google Vertex AI**.
  </Step>

  <Step title="Следуйте подсказкам мастера">
    Выберите способ аутентификации в Google Cloud: Application Default Credentials из `gcloud`, файл ключа сервисного аккаунта или учетные данные, уже находящиеся в вашей среде. Мастер обнаруживает ваш проект и регион, проверяет, какие модели Claude может вызывать ваш проект, и позволяет вам их закрепить. Результат сохраняется в блок `env` вашего [файла пользовательских настроек](/ru/settings), поэтому вам не нужно самостоятельно экспортировать переменные окружения.
  </Step>
</Steps>

После входа запустите `/setup-vertex` в любое время, чтобы снова открыть мастер и изменить учетные данные, проект, регион или закрепления моделей.

## Конфигурация региона

Claude Code поддерживает [глобальные](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai), многорегиональные и региональные конечные точки Vertex AI. Установите `CLOUD_ML_REGION` на `global`, многорегиональное местоположение, такое как `eu` или `us`, или конкретный регион, такой как `us-east5`. Claude Code выбирает правильное имя хоста Vertex AI для каждой формы, включая хосты `aiplatform.eu.rep.googleapis.com` и `aiplatform.us.rep.googleapis.com` для многорегиональных местоположений.

<Note>
  Vertex AI может не поддерживать модели Claude Code по умолчанию на каждом типе конечной точки. Доступность моделей варьируется в зависимости от [конкретных регионов](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models), многорегиональных местоположений и [глобальных конечных точек](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models). Вам может потребоваться переключиться на поддерживаемое местоположение или указать поддерживаемую модель.
</Note>

## Ручная установка

Чтобы настроить Vertex AI через переменные окружения вместо мастера, например в CI или при развертывании в масштабах предприятия, следуйте приведенным ниже шагам.

### 1. Включите API Vertex AI

Включите API Vertex AI в вашем проекте GCP:

```bash theme={null}
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

Claude Code версии 2.1.121 или позже поддерживает [Федерацию рабочих нагрузок на основе сертификатов X.509](https://cloud.google.com/iam/docs/workload-identity-federation-with-x509-certificates) через ту же цепочку Application Default Credentials. Установите `GOOGLE_APPLICATION_CREDENTIALS` на путь к файлу конфигурации учетных данных.

<Note>
  Claude Code использует `ANTHROPIC_VERTEX_PROJECT_ID` как ID проекта для запросов Vertex AI. Переменные окружения `GCLOUD_PROJECT` и `GOOGLE_CLOUD_PROJECT` и файл учетных данных, на который ссылается `GOOGLE_APPLICATION_CREDENTIALS`, имеют приоритет над ним. Если ничего из этого не установлено, ID проекта разрешается из вашей конфигурации `gcloud` или присоединенной учетной записи сервиса.
</Note>

#### Расширенная конфигурация учетных данных

Claude Code поддерживает автоматическое обновление учетных данных GCP через параметр `gcpAuthRefresh`. Когда Claude Code обнаруживает, что ваши учетные данные GCP истекли или не могут быть загружены, он запускает настроенную команду для получения новых учетных данных перед повторной попыткой запроса.

```json theme={null}
{
  "gcpAuthRefresh": "gcloud auth application-default login",
  "env": {
    "ANTHROPIC_VERTEX_PROJECT_ID": "your-project-id"
  }
}
```

Вывод команды отображается пользователю, но интерактивный ввод не поддерживается. Это хорошо работает для потоков аутентификации на основе браузера, где CLI показывает URL, и вы завершаете аутентификацию в браузере. Команда обновления истекает через три минуты, если аутентификация не завершена. Если вы установите `gcpAuthRefresh` в параметрах проекта, таких как `.claude/settings.json`, команда запускается только после того, как вы примете приглашение доверия рабочей области.

### 4. Настройте Claude Code

Установите следующие переменные окружения:

```bash theme={null}
# Включите интеграцию Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Опционально: переопределите URL конечной точки Vertex для пользовательских конечных точек или шлюзов
# export ANTHROPIC_VERTEX_BASE_URL=https://aiplatform.googleapis.com

# Опционально: отключите кэширование запросов, если необходимо
export DISABLE_PROMPT_CACHING=1

# Опционально: запросите TTL кэша запросов на 1 час вместо стандартного 5-минутного
export ENABLE_PROMPT_CACHING_1H=1

# Когда CLOUD_ML_REGION=global, переопределите регион для моделей, которые не поддерживают глобальные конечные точки
export VERTEX_REGION_CLAUDE_HAIKU_4_5=us-east5
export VERTEX_REGION_CLAUDE_4_6_SONNET=europe-west1
```

Большинство версий моделей имеют соответствующую переменную `VERTEX_REGION_CLAUDE_*`. Полный список см. в [справочнике переменных окружения](/ru/env-vars). Проверьте [Vertex Model Garden](https://console.cloud.google.com/vertex-ai/model-garden), чтобы определить, какие модели поддерживают глобальные конечные точки в сравнении с региональными только.

[Кэширование запросов](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) включается автоматически. Чтобы отключить его, установите `DISABLE_PROMPT_CACHING=1`. Чтобы запросить TTL кэша на 1 час вместо стандартного 5-минутного, установите `ENABLE_PROMPT_CACHING_1H=1`; записи кэша с TTL на 1 час тарифицируются по более высокому тарифу. Для повышенных лимитов скорости обратитесь в поддержку Google Cloud. При использовании Vertex AI команды `/login` и `/logout` отключены, так как аутентификация обрабатывается через учетные данные Google Cloud.

Claude Code отключает [поиск инструментов MCP](/ru/mcp#scale-with-mcp-tool-search) по умолчанию на Vertex AI, поэтому определения инструментов MCP загружаются заранее. Vertex AI поддерживает поиск инструментов для Claude Sonnet 4.5 и позже, а также Claude Opus 4.5 и позже. Установите `ENABLE_TOOL_SEARCH=true`, чтобы включить его на этих моделях. Более ранние модели на Vertex AI не принимают требуемый бета-заголовок, и запросы не выполняются, если вы включите поиск инструментов с ними.

### 5. Закрепите версии моделей

<Warning>
  Закрепите конкретные версии моделей при развертывании для нескольких пользователей. Без закрепления псевдонимы моделей, такие как `sonnet` и `opus`, разрешаются в последнюю версию, которая может быть еще не включена в вашем проекте Vertex AI при выпуске Anthropic обновления. Claude Code [откатывается](#startup-model-checks) на предыдущую версию при запуске, когда последняя недоступна, но закрепление позволяет вам контролировать, когда ваши пользователи переходят на новую модель.
</Warning>

Установите эти переменные окружения на конкретные ID моделей Vertex AI.

Без `ANTHROPIC_DEFAULT_OPUS_MODEL` псевдоним `opus` на Vertex разрешается в Opus 4.6. Установите его на ID Opus 4.7, чтобы использовать последнюю модель:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

Для текущих и устаревших ID моделей см. [Обзор моделей](https://platform.claude.com/docs/en/about-claude/models/overview). Полный список переменных окружения см. в разделе [Конфигурация моделей](/ru/model-config#pin-models-for-third-party-deployments).

Claude Code использует эти модели по умолчанию, когда переменные закрепления не установлены:

| Тип модели           | Значение по умолчанию        |
| :------------------- | :--------------------------- |
| Основная модель      | `claude-sonnet-4-5@20250929` |
| Малая/быстрая модель | То же, что и основная модель |

Фоновые задачи, такие как генерация названия сеанса, используют малую/быструю модель, обычно модель класса Haiku. На Vertex AI Claude Code по умолчанию использует основную модель, потому что Haiku может быть не включен в каждом проекте или регионе. Чтобы использовать Haiku для фоновых задач, установите `ANTHROPIC_DEFAULT_HAIKU_MODEL` на ID модели, который доступен в вашем проекте.

Для дальнейшей настройки моделей:

```bash theme={null}
export ANTHROPIC_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5@20251001'
```

## Проверки моделей при запуске

Когда Claude Code запускается с настроенным Vertex AI, он проверяет, что модели, которые он намеревается использовать, доступны в вашем проекте. Эта проверка требует Claude Code v2.1.98 или более поздней версии.

Если вы закрепили версию модели, которая старше текущего значения по умолчанию Claude Code, и ваш проект может вызывать более новую версию, Claude Code предлагает вам обновить закрепление. Принятие записывает новый ID модели в ваш [файл пользовательских настроек](/ru/settings) и перезапускает Claude Code. Отклонение запоминается до следующего изменения версии по умолчанию.

Если вы не закрепили модель и текущее значение по умолчанию недоступно в вашем проекте, Claude Code откатывается на предыдущую версию для текущего сеанса и показывает уведомление. Откат не сохраняется. Включите более новую модель в [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) или [закрепите версию](#5-pin-model-versions), чтобы сделать выбор постоянным.

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

Claude Opus 4.7, Opus 4.6 и Sonnet 4.6 поддерживают [контекстное окно с 1M токенов](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) на Vertex AI. Claude Code автоматически включает расширенное контекстное окно при выборе варианта модели с 1M.

[Мастер установки](#sign-in-with-vertex-ai) предлагает опцию контекстного окна с 1M при закреплении моделей. Чтобы включить его для вручную закрепленной модели, добавьте `[1m]` к ID модели. Подробности см. в разделе [Закрепите модели для развертываний третьих сторон](/ru/model-config#pin-models-for-third-party-deployments).

## Устранение неполадок

Если вы столкнулись с ошибками "Could not load the default credentials":

* Запустите `gcloud auth application-default login` для установки Application Default Credentials
* Установите `GOOGLE_APPLICATION_CREDENTIALS` на путь файла ключа сервисного аккаунта
* См. [Configure GCP credentials](#3-configure-gcp-credentials) для всех вариантов

Если вы столкнулись с проблемами квоты:

* Проверьте текущие квоты или запросите увеличение квоты через [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

Если вы столкнулись с ошибками "model not found" 404:

* Подтвердите, что модель включена в [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Проверьте, что модель доступна в указанном вами местоположении. Некоторые модели предлагаются только на `global` или многорегиональных местоположениях, таких как `eu` и `us`, а не в конкретных регионах
* Если вы используете `CLOUD_ML_REGION=global`, проверьте, что ваши модели поддерживают глобальные конечные точки в [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) в разделе "Supported features". Для моделей, которые не поддерживают глобальные конечные точки, либо:
  * Укажите поддерживаемую модель через `ANTHROPIC_MODEL` или `ANTHROPIC_DEFAULT_HAIKU_MODEL`, либо
  * Установите регион или многорегиональное местоположение, используя переменные окружения `VERTEX_REGION_<MODEL_NAME>`

Если вы столкнулись с ошибками 429:

* Для региональных конечных точек убедитесь, что основная модель и малая/быстрая модель поддерживаются в выбранном регионе
* Рассмотрите возможность переключения на `CLOUD_ML_REGION=global` для лучшей доступности

## Дополнительные ресурсы

* [Документация Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Цены Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Квоты и лимиты Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
