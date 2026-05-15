> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code на Amazon Bedrock

> Узнайте о настройке Claude Code через Amazon Bedrock, включая установку, конфигурацию IAM и устранение неполадок.

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

<ContactSalesCard surface="bedrock" />

## Предварительные требования

Перед настройкой Claude Code с Bedrock убедитесь, что у вас есть:

* Учетная запись AWS с включенным доступом к Bedrock
* Доступ к нужным моделям Claude (например, Claude Sonnet 4.6) в Bedrock
* AWS CLI установлен и настроен (опционально - требуется только если у вас нет другого механизма получения учетных данных)
* Соответствующие разрешения IAM

Чтобы войти со своими собственными учетными данными Bedrock, следуйте инструкциям [Вход с Bedrock](#sign-in-with-bedrock) ниже. Чтобы развернуть Claude Code в команде, используйте шаги [ручной установки](#set-up-manually) и [закрепите версии вашей модели](#4-pin-model-versions) перед развертыванием.

## Вход с Bedrock

Если у вас есть учетные данные AWS и вы хотите начать использовать Claude Code через Bedrock, мастер входа проведет вас через процесс. Вы выполняете предварительные требования на стороне AWS один раз на учетную запись; мастер обрабатывает сторону Claude Code.

<Steps>
  <Step title="Включите модели Anthropic в вашей учетной записи AWS">
    В [консоли Amazon Bedrock](https://console.aws.amazon.com/bedrock/) откройте каталог моделей, выберите модель Anthropic и отправьте форму варианта использования. Доступ предоставляется сразу же после отправки. См. [Отправьте детали варианта использования](#1-submit-use-case-details) для AWS Organizations и [конфигурацию IAM](#iam-configuration) для разрешений, которые требуются вашей роли.
  </Step>

  <Step title="Запустите Claude Code и выберите Bedrock">
    Запустите `claude`. При запросе входа выберите **3rd-party platform**, затем **Amazon Bedrock**.
  </Step>

  <Step title="Следуйте подсказкам мастера">
    Выберите способ аутентификации в AWS: профиль AWS, обнаруженный из вашей директории `~/.aws`, ключ API Bedrock, ключ доступа и секрет, или учетные данные уже в вашей среде. Мастер выбирает ваш регион, проверяет, какие модели Claude может вызывать ваша учетная запись, и позволяет вам их закрепить. Он сохраняет результат в блок `env` вашего [файла параметров пользователя](/ru/settings), поэтому вам не нужно самостоятельно экспортировать переменные окружения.
  </Step>
</Steps>

После входа запустите `/setup-bedrock` в любое время, чтобы снова открыть мастер и изменить ваши учетные данные, регион или закрепления моделей.

## Ручная установка

Чтобы настроить Bedrock через переменные окружения вместо мастера, например в CI или при развертывании в масштабе предприятия, следуйте шагам ниже.

### 1. Отправьте детали варианта использования

Пользователи, впервые использующие модели Anthropic, должны отправить детали варианта использования перед вызовом модели. Это делается один раз на учетную запись AWS.

1. Убедитесь, что у вас есть правильные разрешения IAM, описанные ниже
2. Перейдите на [консоль Amazon Bedrock](https://console.aws.amazon.com/bedrock/)
3. Выберите модель Anthropic из **Model catalog**
4. Заполните форму варианта использования. Доступ предоставляется сразу же после отправки.

Если вы используете AWS Organizations, вы можете отправить форму один раз из учетной записи управления, используя [`PutUseCaseForModelAccess` API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_PutUseCaseForModelAccess.html). Этот вызов требует разрешение IAM `bedrock:PutUseCaseForModelAccess`. Одобрение автоматически распространяется на дочерние учетные записи.

### 2. Настройте учетные данные AWS

Claude Code использует цепочку учетных данных AWS SDK по умолчанию. Установите ваши учетные данные, используя один из этих методов:

**Вариант A: конфигурация AWS CLI**

```bash theme={null}
aws configure
```

**Вариант B: переменные окружения (ключ доступа)**

```bash theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**Вариант C: переменные окружения (профиль SSO)**

```bash theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**Вариант D: учетные данные AWS Management Console**

```bash theme={null}
aws login
```

[Узнайте больше](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) о `aws login`.

**Вариант E: ключи API Bedrock**

```bash theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Ключи API Bedrock предоставляют более простой метод аутентификации без необходимости полных учетных данных AWS. [Узнайте больше о ключах API Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### Расширенная конфигурация учетных данных

Claude Code поддерживает автоматическое обновление учетных данных для AWS SSO и корпоративных поставщиков идентификации. Добавьте эти параметры в файл параметров Claude Code (см. [Settings](/ru/settings) для расположения файлов).

Эти два параметра имеют разные условия срабатывания:

* **`awsAuthRefresh`**: запускается только когда Claude Code обнаруживает, что ваши учетные данные AWS истекли, либо локально на основе их временной метки, либо когда Bedrock возвращает ошибку учетных данных, затем повторяет попытку запроса с обновленными учетными данными.
* **`awsCredentialExport`**: запускается при запуске сеанса и при каждой перезагрузке учетных данных, даже когда учетные данные в цепочке поставщика учетных данных AWS по умолчанию все еще действительны. Используйте это, когда ваша учетная запись Bedrock требует учетные данные между учетными записями, которые отличаются от тех, которые разрешила бы цепочка поставщика по умолчанию.

##### Пример конфигурации

```json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### Объяснение параметров конфигурации

**`awsAuthRefresh`**: используйте это для команд, которые изменяют директорию `.aws`, такие как обновление учетных данных, кэша SSO или файлов конфигурации. Вывод команды отображается пользователю, но интерактивный ввод не поддерживается. Это хорошо работает для браузерных потоков SSO, где CLI отображает URL или код, и вы завершаете аутентификацию в браузере.

**`awsCredentialExport`**: используйте это только если вы не можете изменить `.aws` и должны напрямую вернуть учетные данные. Эта команда запускается всякий раз, когда необходимо обновить учетные данные, а не только когда учетные данные истекли. Вывод захватывается молча и не показывается пользователю. Команда должна выводить JSON в этом формате:

```json theme={null}
{
  "Credentials": {
    "AccessKeyId": "value",
    "SecretAccessKey": "value",
    "SessionToken": "value"
  }
}
```

### 3. Настройте Claude Code

Установите следующие переменные окружения для включения Bedrock:

```bash theme={null}
# Enable Bedrock integration
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # or your preferred region

# Optional: Override the region for the small/fast model (Haiku).
# Also applies to Bedrock Mantle.
export ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION=us-west-2

# Optional: Override the Bedrock endpoint URL for custom endpoints or gateways
# export ANTHROPIC_BEDROCK_BASE_URL=https://bedrock-runtime.us-east-1.amazonaws.com
```

При включении Bedrock для Claude Code имейте в виду следующее:

* `AWS_REGION` - это обязательная переменная окружения. Claude Code не читает этот параметр из файла конфигурации `.aws`.
* При использовании Bedrock команды `/login` и `/logout` отключены, так как аутентификация обрабатывается через учетные данные AWS.
* Вы можете использовать файлы параметров для переменных окружения, таких как `AWS_PROFILE`, которые вы не хотите утечь в другие процессы. См. [Settings](/ru/settings) для получения дополнительной информации.

### 4. Закрепите версии моделей

<Warning>
  Закрепите конкретные версии моделей при развертывании для нескольких пользователей. Без закрепления псевдонимы моделей, такие как `sonnet` и `opus`, разрешаются на последнюю версию, которая может быть еще недоступна в вашей учетной записи Bedrock при выпуске обновления Anthropic. Claude Code [возвращается](#startup-model-checks) к предыдущей версии при запуске, когда последняя недоступна, но закрепление позволяет вам контролировать, когда ваши пользователи переходят на новую модель.
</Warning>

Установите эти переменные окружения на конкретные ID моделей Bedrock.

Без `ANTHROPIC_DEFAULT_OPUS_MODEL` псевдоним `opus` на Bedrock разрешается на Opus 4.6. Установите его на ID Opus 4.7, чтобы использовать последнюю модель:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'
```

Эти переменные используют ID профилей вывода между регионами (с префиксом `us.`). Если вы используете другой префикс региона или профили вывода приложения, отрегулируйте соответственно. Для текущих и устаревших ID моделей см. [Models overview](https://platform.claude.com/docs/en/about-claude/models/overview). См. [Model configuration](/ru/model-config#pin-models-for-third-party-deployments) для полного списка переменных окружения.

Claude Code использует эти модели по умолчанию, когда переменные закрепления не установлены:

| Тип модели           | Значение по умолчанию                          |
| :------------------- | :--------------------------------------------- |
| Основная модель      | `us.anthropic.claude-sonnet-4-5-20250929-v1:0` |
| Малая/быстрая модель | `us.anthropic.claude-haiku-4-5-20251001-v1:0`  |

Для дальнейшей настройки моделей используйте один из этих методов:

```bash theme={null}
# Using inference profile ID
export ANTHROPIC_MODEL='us.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Using application inference profile ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1

# Optional: Request 1-hour prompt cache TTL instead of the 5-minute default
export ENABLE_PROMPT_CACHING_1H=1
```

<Note>[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) может быть недоступен во всех регионах. Записи кэша с TTL в 1 час выставляются по более высокому тарифу, чем записи в 5 минут.</Note>

#### Сопоставьте каждую версию модели с профилем вывода

Переменные окружения `ANTHROPIC_DEFAULT_*_MODEL` настраивают один профиль вывода на семейство моделей. Если вашей организации необходимо предоставить несколько версий одного семейства в средстве выбора `/model`, каждая маршрутизируется на свой ARN профиля вывода приложения, используйте вместо этого параметр `modelOverrides` в вашем [файле параметров](/ru/settings#settings-files).

Этот пример сопоставляет четыре версии Opus с отдельными ARN, чтобы пользователи могли переключаться между ними без обхода профилей вывода вашей организации:

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-47-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

Когда пользователь выбирает одну из этих версий в `/model`, Claude Code вызывает Bedrock с сопоставленным ARN. Версии без переопределения возвращаются к встроенному ID модели Bedrock или любому соответствующему профилю вывода, обнаруженному при запуске. См. [Override model IDs per version](/ru/model-config#override-model-ids-per-version) для получения подробной информации о том, как переопределения взаимодействуют с `availableModels` и другими параметрами модели.

## Проверки моделей при запуске

Когда Claude Code запускается с настроенным Bedrock, он проверяет, что модели, которые он намеревается использовать, доступны в вашей учетной записи. Эта проверка требует Claude Code v2.1.94 или более поздней версии.

Если вы закрепили версию модели, которая старше текущего значения по умолчанию Claude Code, и ваша учетная запись может вызывать более новую версию, Claude Code предлагает вам обновить закрепление. Принятие записывает новый ID модели в ваш [файл параметров пользователя](/ru/settings) и перезапускает Claude Code. Отклонение запоминается до следующего изменения версии по умолчанию. Закрепления, указывающие на [ARN профиля вывода приложения](#map-each-model-version-to-an-inference-profile), пропускаются, так как они управляются вашим администратором.

Если вы не закрепили модель и текущее значение по умолчанию недоступно в вашей учетной записи, Claude Code возвращается к предыдущей версии для текущего сеанса и показывает уведомление. Возврат не сохраняется. Включите более новую модель в вашей учетной записи Bedrock или [закрепите версию](#4-pin-model-versions), чтобы сделать выбор постоянным.

## Конфигурация IAM

Создайте политику IAM с необходимыми разрешениями для Claude Code:

```json theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelAndInferenceProfileAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles",
        "bedrock:GetInferenceProfile"
      ],
      "Resource": [
        "arn:aws:bedrock:*:*:inference-profile/*",
        "arn:aws:bedrock:*:*:application-inference-profile/*",
        "arn:aws:bedrock:*:*:foundation-model/*"
      ]
    },
    {
      "Sid": "AllowMarketplaceSubscription",
      "Effect": "Allow",
      "Action": [
        "aws-marketplace:ViewSubscriptions",
        "aws-marketplace:Subscribe"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:CalledViaLast": "bedrock.amazonaws.com"
        }
      }
    }
  ]
}
```

Для более ограничительных разрешений вы можете ограничить Resource конкретными ARN профилей вывода.

`bedrock:GetInferenceProfile` позволяет Claude Code разрешить [ARN профиля вывода приложения](#map-each-model-version-to-an-inference-profile) в его базовую модель фундамента, которая используется для выбора правильной формы запроса для этой модели.

Если токену не хватает этого разрешения, Claude Code автоматически восстанавливается, повторив попытку один раз с альтернативной формой, поэтому запросы все еще успешны, но каждая новая модель добавляет дополнительный обход туда и обратно. Предоставление разрешения избегает повтора. Это применяется чаще всего к развертываниям `AWS_BEARER_TOKEN_BEDROCK`, где политика токена обычно уже, чем полная роль IAM.

Для получения подробной информации см. [документацию Bedrock IAM](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

<Note>
  Создайте выделенную учетную запись AWS для Claude Code, чтобы упростить отслеживание затрат и контроль доступа.
</Note>

## Окно контекста 1M токенов

Claude Opus 4.7, Opus 4.6 и Sonnet 4.6 поддерживают [окно контекста 1M токенов](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) на Amazon Bedrock. Claude Code автоматически включает расширенное окно контекста при выборе варианта модели 1M.

[Мастер установки](#sign-in-with-bedrock) предлагает опцию контекста 1M при закреплении моделей. Чтобы включить его для вручную закрепленной модели вместо этого, добавьте `[1m]` к ID модели. См. [Pin models for third-party deployments](/ru/model-config#pin-models-for-third-party-deployments) для получения подробной информации.

## Уровни обслуживания

[Уровни обслуживания Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/service-tiers-inference.html) позволяют вам выбирать между стоимостью и задержкой. Установите `ANTHROPIC_BEDROCK_SERVICE_TIER` на `default`, `flex` или `priority`:

```bash theme={null}
export ANTHROPIC_BEDROCK_SERVICE_TIER=priority
```

Claude Code отправляет это как заголовок `X-Amzn-Bedrock-Service-Tier` в каждом запросе. Доступность уровня варьируется по модели и региону. Зарезервированная емкость использует [provisioned throughput](https://docs.aws.amazon.com/bedrock/latest/userguide/prov-throughput.html) ARN в качестве ID модели вместо этого параметра.

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) позволяют вам реализовать фильтрацию контента для Claude Code. Создайте Guardrail в [консоли Amazon Bedrock](https://console.aws.amazon.com/bedrock/), опубликуйте версию, затем добавьте заголовки Guardrail в ваш [файл параметров](/ru/settings). Включите Cross-Region inference на вашем Guardrail, если вы используете профили вывода между регионами.

Пример конфигурации:

```json theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

## Используйте конечную точку Mantle

Mantle - это конечная точка Amazon Bedrock, которая обслуживает модели Claude через форму собственного API Anthropic, а не через Bedrock Invoke API. Она использует те же учетные данные AWS, разрешения IAM и конфигурацию `awsAuthRefresh`, описанные ранее на этой странице.

<Note>
  Mantle требует Claude Code v2.1.94 или более поздней версии. Запустите `claude --version`, чтобы проверить.
</Note>

### Включите Mantle

С уже настроенными учетными данными AWS установите `CLAUDE_CODE_USE_MANTLE` для маршрутизации запросов на конечную точку Mantle:

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export AWS_REGION=us-east-1
```

Claude Code конструирует URL конечной точки из `AWS_REGION`. Чтобы переопределить его для пользовательской конечной точки или шлюза, установите `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`.

Запустите `/status` внутри Claude Code для подтверждения. Строка поставщика показывает `Amazon Bedrock (Mantle)`, когда Mantle активен.

### Выберите модель Mantle

Mantle использует ID моделей с префиксом `anthropic.` и без суффикса версии, например `anthropic.claude-haiku-4-5`. Модели, доступные вашей учетной записи, зависят от того, что вам было предоставлено вашей организацией; дополнительные ID моделей указаны в ваших материалах по подключению от AWS. Свяжитесь с вашей командой учетной записи AWS, чтобы запросить доступ к разрешенным моделям.

Установите модель с флагом `--model` или с `/model` внутри Claude Code:

```bash theme={null}
claude --model anthropic.claude-haiku-4-5
```

### Запустите Mantle рядом с Invoke API

Модели, доступные вам на Mantle, могут не включать каждую модель, которую вы используете сегодня. Установка как `CLAUDE_CODE_USE_BEDROCK`, так и `CLAUDE_CODE_USE_MANTLE` позволяет Claude Code вызывать обе конечные точки из одного сеанса. ID моделей, соответствующие формату Mantle, маршрутизируются на Mantle, а все остальные ID моделей идут на Bedrock Invoke API.

```bash theme={null}
export CLAUDE_CODE_USE_BEDROCK=1
export CLAUDE_CODE_USE_MANTLE=1
```

Чтобы отобразить модель Mantle в средстве выбора `/model`, перечислите ее ID в `availableModels` в вашем [файле параметров](/ru/settings). Этот параметр также ограничивает средство выбора перечисленными записями, поэтому включите каждый псевдоним, который вы хотите сохранить доступным:

```json theme={null}
{
  "availableModels": ["opus", "sonnet", "haiku", "anthropic.claude-haiku-4-5"]
}
```

Записи с префиксом `anthropic.` добавляются как пользовательские опции средства выбора и маршрутизируются на Mantle. Замените `anthropic.claude-haiku-4-5` на ID модели, который была предоставлена вашей учетной записи. См. [Restrict model selection](/ru/model-config#restrict-model-selection) для получения информации о том, как `availableModels` взаимодействует с другими параметрами модели.

Когда оба поставщика активны, `/status` показывает `Amazon Bedrock + Amazon Bedrock (Mantle)`.

### Маршрутизируйте Mantle через шлюз

Если ваша организация маршрутизирует трафик модели через централизованный [LLM gateway](/ru/llm-gateway), который внедряет учетные данные AWS на стороне сервера, отключите аутентификацию на стороне клиента, чтобы Claude Code отправлял запросы без подписей SigV4 или заголовков `x-api-key`:

```bash theme={null}
export CLAUDE_CODE_USE_MANTLE=1
export CLAUDE_CODE_SKIP_MANTLE_AUTH=1
export ANTHROPIC_BEDROCK_MANTLE_BASE_URL=https://your-gateway.example.com
```

### Переменные окружения Mantle

Эти переменные специфичны для конечной точки Mantle. См. [Environment variables](/ru/env-vars) для полного списка.

| Переменная                              | Назначение                                                          |
| :-------------------------------------- | :------------------------------------------------------------------ |
| `CLAUDE_CODE_USE_MANTLE`                | Включите конечную точку Mantle. Установите на `1` или `true`.       |
| `ANTHROPIC_BEDROCK_MANTLE_BASE_URL`     | Переопределите URL конечной точки Mantle по умолчанию               |
| `CLAUDE_CODE_SKIP_MANTLE_AUTH`          | Пропустите аутентификацию на стороне клиента для настроек прокси    |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION` | Переопределите регион AWS для модели класса Haiku (общее с Bedrock) |

## Устранение неполадок

### Цикл аутентификации с SSO и корпоративными прокси

Если вкладки браузера открываются повторно при использовании AWS SSO, удалите параметр `awsAuthRefresh` из вашего [файла параметров](/ru/settings). Это может произойти, когда корпоративные VPN или прокси-серверы с проверкой TLS прерывают браузерный поток SSO. Claude Code рассматривает прерванное соединение как ошибку аутентификации, повторно запускает `awsAuthRefresh` и зацикливается бесконечно.

Если ваша сетевая среда мешает автоматическим браузерным потокам SSO, используйте `aws sso login` вручную перед запуском Claude Code вместо того, чтобы полагаться на `awsAuthRefresh`.

### Проблемы с регионом

Если вы столкнулись с проблемами региона:

* Проверьте доступность модели: `aws bedrock list-inference-profiles --region your-region`
* Переключитесь на поддерживаемый регион: `export AWS_REGION=us-east-1`
* Рассмотрите использование профилей вывода для доступа между регионами

Если вы получили ошибку "on-demand throughput isn't supported":

* Укажите модель как ID [профиля вывода](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)

Claude Code использует Bedrock [Invoke API](https://docs.aws.amazon.com/bedrock/latest/APIReference/API_runtime_InvokeModelWithResponseStream.html) и не поддерживает Converse API.

### Ошибки конечной точки Mantle

Если `/status` не показывает `Amazon Bedrock (Mantle)` после установки `CLAUDE_CODE_USE_MANTLE`, переменная не достигает процесса. Подтвердите, что она экспортирована в оболочке, где вы запустили `claude`, или установите ее в блоке `env` вашего [файла параметров](/ru/settings).

`403` от конечной точки Mantle с действительными учетными данными означает, что вашей учетной записи AWS не был предоставлен доступ к запрошенной модели. Свяжитесь с вашей командой учетной записи AWS, чтобы запросить доступ.

`400`, который называет ID модели, означает, что эта модель не обслуживается на Mantle. Mantle имеет свой собственный набор моделей, отдельный от стандартного каталога Bedrock, поэтому ID профилей вывода, такие как `us.anthropic.claude-sonnet-4-6`, не будут работать. Используйте ID формата Mantle или включите [обе конечные точки](#run-mantle-alongside-the-invoke-api), чтобы Claude Code маршрутизировал каждый запрос на конечную точку, где модель доступна.

## Дополнительные ресурсы

* [Документация Bedrock](https://docs.aws.amazon.com/bedrock/)
* [Цены Bedrock](https://aws.amazon.com/bedrock/pricing/)
* [Профили вывода Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Burndown токенов Bedrock и квоты](https://docs.aws.amazon.com/bedrock/latest/userguide/quotas-token-burndown.html)
* [Claude Code на Amazon Bedrock: Quick Setup Guide](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Claude Code Monitoring Implementation (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
