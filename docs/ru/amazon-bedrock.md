> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code на Amazon Bedrock

> Узнайте о настройке Claude Code через Amazon Bedrock, включая установку, конфигурацию IAM и устранение неполадок.

## Предварительные требования

Перед настройкой Claude Code с Bedrock убедитесь, что у вас есть:

* Учетная запись AWS с включенным доступом к Bedrock
* Доступ к нужным моделям Claude (например, Claude Sonnet 4.6) в Bedrock
* AWS CLI установлен и настроен (опционально - требуется только если у вас нет другого механизма получения учетных данных)
* Соответствующие разрешения IAM

<Note>
  Если вы развертываете Claude Code для нескольких пользователей, [закрепите версии вашей модели](#4-pin-model-versions), чтобы предотвратить сбои при выпуске Anthropic новых моделей.
</Note>

## Установка

### 1. Отправьте детали варианта использования

Пользователи, впервые использующие модели Anthropic, должны отправить детали варианта использования перед вызовом модели. Это делается один раз на учетную запись.

1. Убедитесь, что у вас есть правильные разрешения IAM (см. подробнее ниже)
2. Перейдите на [консоль Amazon Bedrock](https://console.aws.amazon.com/bedrock/)
3. Выберите **Chat/Text playground**
4. Выберите любую модель Anthropic и вам будет предложено заполнить форму варианта использования

### 2. Настройте учетные данные AWS

Claude Code использует цепочку учетных данных AWS SDK по умолчанию. Установите ваши учетные данные, используя один из этих методов:

**Вариант A: конфигурация AWS CLI**

```bash  theme={null}
aws configure
```

**Вариант B: переменные окружения (ключ доступа)**

```bash  theme={null}
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key
export AWS_SESSION_TOKEN=your-session-token
```

**Вариант C: переменные окружения (профиль SSO)**

```bash  theme={null}
aws sso login --profile=<your-profile-name>

export AWS_PROFILE=your-profile-name
```

**Вариант D: учетные данные AWS Management Console**

```bash  theme={null}
aws login
```

[Узнайте больше](https://docs.aws.amazon.com/signin/latest/userguide/command-line-sign-in.html) о `aws login`.

**Вариант E: ключи API Bedrock**

```bash  theme={null}
export AWS_BEARER_TOKEN_BEDROCK=your-bedrock-api-key
```

Ключи API Bedrock предоставляют более простой метод аутентификации без необходимости полных учетных данных AWS. [Узнайте больше о ключах API Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/).

#### Расширенная конфигурация учетных данных

Claude Code поддерживает автоматическое обновление учетных данных для AWS SSO и корпоративных поставщиков идентификации. Добавьте эти параметры в файл параметров Claude Code (см. [Settings](/ru/settings) для расположения файлов).

Когда Claude Code обнаруживает, что ваши учетные данные AWS истекли (либо локально на основе их временной метки, либо когда Bedrock возвращает ошибку учетных данных), он автоматически запустит ваши настроенные команды `awsAuthRefresh` и/или `awsCredentialExport` для получения новых учетных данных перед повторной попыткой запроса.

##### Пример конфигурации

```json  theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile",
  "env": {
    "AWS_PROFILE": "myprofile"
  }
}
```

##### Объяснение параметров конфигурации

**`awsAuthRefresh`**: используйте это для команд, которые изменяют директорию `.aws`, такие как обновление учетных данных, кэша SSO или файлов конфигурации. Вывод команды отображается пользователю, но интерактивный ввод не поддерживается. Это хорошо работает для браузерных потоков SSO, где CLI отображает URL или код, и вы завершаете аутентификацию в браузере.

**`awsCredentialExport`**: используйте это только если вы не можете изменить `.aws` и должны напрямую вернуть учетные данные. Вывод захватывается молча и не показывается пользователю. Команда должна выводить JSON в этом формате:

```json  theme={null}
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

```bash  theme={null}
# Enable Bedrock integration
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1  # or your preferred region

# Optional: Override the region for the small/fast model (Haiku)
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
  Закрепите конкретные версии моделей для каждого развертывания. Если вы используете псевдонимы моделей (`sonnet`, `opus`, `haiku`) без закрепления, Claude Code может попытаться использовать более новую версию модели, которая недоступна в вашей учетной записи Bedrock, нарушив работу существующих пользователей при выпуске обновлений Anthropic.
</Warning>

Установите эти переменные окружения на конкретные ID моделей Bedrock:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'
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

```bash  theme={null}
# Using inference profile ID
export ANTHROPIC_MODEL='global.anthropic.claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='us.anthropic.claude-haiku-4-5-20251001-v1:0'

# Using application inference profile ARN
export ANTHROPIC_MODEL='arn:aws:bedrock:us-east-2:your-account-id:application-inference-profile/your-model-id'

# Optional: Disable prompt caching if needed
export DISABLE_PROMPT_CACHING=1
```

<Note>[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) может быть недоступен во всех регионах.</Note>

#### Сопоставьте каждую версию модели с профилем вывода

Переменные окружения `ANTHROPIC_DEFAULT_*_MODEL` настраивают один профиль вывода на семейство моделей. Если вашей организации необходимо предоставить несколько версий одного семейства в средстве выбора `/model`, каждая маршрутизируется на свой ARN профиля вывода приложения, используйте вместо этого параметр `modelOverrides` в вашем [файле параметров](/ru/settings#settings-files).

Этот пример сопоставляет три версии Opus с отдельными ARN, чтобы пользователи могли переключаться между ними без обхода профилей вывода вашей организации:

```json  theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-opus-4-1-20250805": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-41-prod"
  }
}
```

Когда пользователь выбирает одну из этих версий в `/model`, Claude Code вызывает Bedrock с сопоставленным ARN. Версии без переопределения возвращаются к встроенному ID модели Bedrock или любому соответствующему профилю вывода, обнаруженному при запуске. См. [Override model IDs per version](/ru/model-config#override-model-ids-per-version) для получения подробной информации о том, как переопределения взаимодействуют с `availableModels` и другими параметрами модели.

## Конфигурация IAM

Создайте политику IAM с необходимыми разрешениями для Claude Code:

```json  theme={null}
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "AllowModelAndInferenceProfileAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:ListInferenceProfiles"
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

Для получения подробной информации см. [документацию Bedrock IAM](https://docs.aws.amazon.com/bedrock/latest/userguide/security-iam.html).

<Note>
  Создайте выделенную учетную запись AWS для Claude Code, чтобы упростить отслеживание затрат и контроль доступа.
</Note>

## Окно контекста 1M токенов

Claude Opus 4.6 и Sonnet 4.6 поддерживают [окно контекста 1M токенов](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) на Amazon Bedrock. Claude Code автоматически включает расширенное окно контекста при выборе варианта модели 1M.

Чтобы включить окно контекста 1M для вашей закрепленной модели, добавьте `[1m]` к ID модели. См. [Pin models for third-party deployments](/ru/model-config#pin-models-for-third-party-deployments) для получения подробной информации.

## AWS Guardrails

[Amazon Bedrock Guardrails](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails.html) позволяют вам реализовать фильтрацию контента для Claude Code. Создайте Guardrail в [консоли Amazon Bedrock](https://console.aws.amazon.com/bedrock/), опубликуйте версию, затем добавьте заголовки Guardrail в ваш [файл параметров](/ru/settings). Включите Cross-Region inference на вашем Guardrail, если вы используете профили вывода между регионами.

Пример конфигурации:

```json  theme={null}
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "X-Amzn-Bedrock-GuardrailIdentifier: your-guardrail-id\nX-Amzn-Bedrock-GuardrailVersion: 1"
  }
}
```

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

## Дополнительные ресурсы

* [Документация Bedrock](https://docs.aws.amazon.com/bedrock/)
* [Цены Bedrock](https://aws.amazon.com/bedrock/pricing/)
* [Профили вывода Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/inference-profiles-support.html)
* [Claude Code на Amazon Bedrock: Quick Setup Guide](https://community.aws/content/2tXkZKrZzlrlu0KfH8gST5Dkppq/claude-code-on-amazon-bedrock-quick-setup-guide)
* [Claude Code Monitoring Implementation (Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)
