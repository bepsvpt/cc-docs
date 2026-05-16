> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code на Microsoft Foundry

> Узнайте о настройке Claude Code через Microsoft Foundry, включая установку, конфигурацию и устранение неполадок.

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

<ContactSalesCard surface="foundry" />

## Предварительные требования

Перед настройкой Claude Code с Microsoft Foundry убедитесь, что у вас есть:

* Подписка Azure с доступом к Microsoft Foundry
* Разрешения RBAC для создания ресурсов и развертываний Microsoft Foundry
* Azure CLI установлен и настроен (опционально - требуется только если у вас нет другого механизма для получения учетных данных)

<Note>
  Если вы развертываете Claude Code для нескольких пользователей, [закрепите версии вашей модели](#4-pin-model-versions), чтобы предотвратить сбои при выпуске Anthropic новых моделей.
</Note>

## Установка

### 1. Подготовка ресурса Microsoft Foundry

Сначала создайте ресурс Claude в Azure:

1. Перейдите на [портал Microsoft Foundry](https://ai.azure.com/)
2. Создайте новый ресурс, отметив имя вашего ресурса
3. Создайте развертывания для моделей Claude:
   * Claude Opus
   * Claude Sonnet
   * Claude Haiku

### 2. Настройка учетных данных Azure

Claude Code поддерживает два метода аутентификации для Microsoft Foundry. Выберите метод, который лучше всего соответствует вашим требованиям безопасности.

**Вариант A: Аутентификация по ключу API**

1. Перейдите к вашему ресурсу на портале Microsoft Foundry
2. Перейдите в раздел **Endpoints and keys**
3. Скопируйте **API Key**
4. Установите переменную окружения:

```bash theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**Вариант B: Аутентификация Microsoft Entra ID**

Когда `ANTHROPIC_FOUNDRY_API_KEY` не установлен, Claude Code автоматически использует Azure SDK [цепочку учетных данных по умолчанию](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview).
Это поддерживает различные методы аутентификации локальных и удаленных рабочих нагрузок.

В локальных средах вы обычно можете использовать Azure CLI:

```bash theme={null}
az login
```

<Note>
  При использовании Microsoft Foundry команды `/login` и `/logout` отключены, так как аутентификация обрабатывается через учетные данные Azure.
</Note>

### 3. Настройка Claude Code

Установите следующие переменные окружения для включения интеграции Microsoft Foundry:

```bash theme={null}
# Enable Microsoft Foundry integration
export CLAUDE_CODE_USE_FOUNDRY=1

# Azure resource name (replace {resource} with your resource name)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Or provide the full base URL:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic
```

### 4. Pin model versions

<Warning>
  Закрепите конкретные версии моделей для каждого развертывания. Если вы используете псевдонимы моделей (`sonnet`, `opus`, `haiku`) без закрепления, Claude Code может попытаться использовать более новую версию модели, которая недоступна в вашей учетной записи Foundry, что приведет к сбою существующих пользователей при выпуске обновлений Anthropic. При создании развертываний Azure выберите конкретную версию модели вместо "автоматического обновления до последней версии".
</Warning>

Установите переменные модели в соответствии с именами развертываний, которые вы создали на шаге 1.

Без `ANTHROPIC_DEFAULT_OPUS_MODEL` псевдоним `opus` на Foundry разрешается в Opus 4.6. Установите его на идентификатор Opus 4.7, чтобы использовать последнюю модель:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
```

Фоновые задачи, такие как генерация заголовков сеансов, используют небольшую/быструю модель, обычно модель класса Haiku. На Foundry Claude Code по умолчанию использует основную модель, потому что не каждая учетная запись имеет развертывание Haiku. Чтобы использовать Haiku для фоновых задач, установите `ANTHROPIC_DEFAULT_HAIKU_MODEL` на развертывание Haiku, доступное в вашей учетной записи, как показано выше.

Для получения текущих и устаревших идентификаторов моделей см. [Обзор моделей](https://platform.claude.com/docs/en/about-claude/models/overview). Полный список переменных окружения см. в разделе [Конфигурация модели](/ru/model-config#pin-models-for-third-party-deployments).

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) включен автоматически. Чтобы запросить TTL кэша в 1 час вместо стандартного 5-минутного, установите следующую переменную; записи кэша с TTL в 1 час выставляются по более высокому тарифу:

```bash theme={null}
export ENABLE_PROMPT_CACHING_1H=1
```

## Конфигурация Azure RBAC

Роли по умолчанию `Azure AI User` и `Cognitive Services User` включают все необходимые разрешения для вызова моделей Claude.

Для более ограничительных разрешений создайте пользовательскую роль со следующим содержимым:

```json theme={null}
{
  "permissions": [
    {
      "dataActions": [
        "Microsoft.CognitiveServices/accounts/providers/*"
      ]
    }
  ]
}
```

Для получения дополнительной информации см. [документацию Microsoft Foundry RBAC](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

## Устранение неполадок

Если вы получаете ошибку "Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed":

* Настройте Entra ID в среде или установите `ANTHROPIC_FOUNDRY_API_KEY`.

## Дополнительные ресурсы

* [Документация Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Модели Microsoft Foundry](https://ai.azure.com/explore/models)
* [Цены Microsoft Foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
