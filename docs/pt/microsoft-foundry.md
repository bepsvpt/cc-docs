> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code no Microsoft Foundry

> Saiba como configurar Claude Code através do Microsoft Foundry, incluindo configuração, instalação e resolução de problemas.

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

## Pré-requisitos

Antes de configurar Claude Code com Microsoft Foundry, certifique-se de que você tem:

* Uma assinatura do Azure com acesso ao Microsoft Foundry
* Permissões RBAC para criar recursos e implantações do Microsoft Foundry
* Azure CLI instalado e configurado (opcional - necessário apenas se você não tiver outro mecanismo para obter credenciais)

<Note>
  Se você está implantando Claude Code para vários usuários, [fixe suas versões de modelo](#4-pin-model-versions) para evitar problemas quando Anthropic lançar novos modelos.
</Note>

## Configuração

### 1. Provisionar recurso do Microsoft Foundry

Primeiro, crie um recurso Claude no Azure:

1. Navegue até o [portal do Microsoft Foundry](https://ai.azure.com/)
2. Crie um novo recurso, anotando o nome do seu recurso
3. Crie implantações para os modelos Claude:
   * Claude Opus
   * Claude Sonnet
   * Claude Haiku

### 2. Configurar credenciais do Azure

Claude Code suporta dois métodos de autenticação para Microsoft Foundry. Escolha o método que melhor se adequa aos seus requisitos de segurança.

**Opção A: Autenticação por chave de API**

1. Navegue até seu recurso no portal do Microsoft Foundry
2. Vá para a seção **Endpoints e chaves**
3. Copie a **Chave de API**
4. Defina a variável de ambiente:

```bash theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**Opção B: Autenticação do Microsoft Entra ID**

Quando `ANTHROPIC_FOUNDRY_API_KEY` não está definido, Claude Code usa automaticamente a [cadeia de credenciais padrão](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview) do Azure SDK.
Isso suporta uma variedade de métodos para autenticar cargas de trabalho locais e remotas.

Em ambientes locais, você pode usar comumente a Azure CLI:

```bash theme={null}
az login
```

<Note>
  Ao usar Microsoft Foundry, os comandos `/login` e `/logout` são desabilitados, pois a autenticação é tratada através de credenciais do Azure.
</Note>

### 3. Configurar Claude Code

Defina as seguintes variáveis de ambiente para ativar Microsoft Foundry:

```bash theme={null}
# Ativar integração do Microsoft Foundry
export CLAUDE_CODE_USE_FOUNDRY=1

# Nome do recurso do Azure (substitua {resource} pelo nome do seu recurso)
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# Ou forneça a URL base completa:
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic
```

### 4. Pin model versions

<Warning>
  Fixe versões de modelo específicas para cada implantação. Se você usar aliases de modelo (`sonnet`, `opus`, `haiku`) sem fixar, Claude Code pode tentar usar uma versão de modelo mais recente que não está disponível em sua conta Foundry, quebrando usuários existentes quando Anthropic lançar atualizações. Quando você criar implantações do Azure, selecione uma versão de modelo específica em vez de "atualizar automaticamente para a mais recente".
</Warning>

Defina as variáveis de modelo para corresponder aos nomes de implantação que você criou na etapa 1.

Sem `ANTHROPIC_DEFAULT_OPUS_MODEL`, o alias `opus` no Foundry resolve para Opus 4.6. Defina-o para o ID Opus 4.7 para usar o modelo mais recente:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
```

Para IDs de modelo atuais e legados, consulte [Visão geral de modelos](https://platform.claude.com/docs/en/about-claude/models/overview). Consulte [Configuração de modelo](/pt/model-config#pin-models-for-third-party-deployments) para a lista completa de variáveis de ambiente.

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) está ativado automaticamente. Para solicitar um TTL de cache de 1 hora em vez do padrão de 5 minutos, defina a seguinte variável; gravações de cache com TTL de 1 hora são cobradas a uma taxa mais alta:

```bash theme={null}
export ENABLE_PROMPT_CACHING_1H=1
```

## Configuração do Azure RBAC

As funções padrão `Azure AI User` e `Cognitive Services User` incluem todas as permissões necessárias para invocar modelos Claude.

Para permissões mais restritivas, crie uma função personalizada com o seguinte:

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

Para detalhes, consulte [documentação RBAC do Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry).

## Resolução de problemas

Se você receber um erro "Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed":

* Configure Entra ID no ambiente, ou defina `ANTHROPIC_FOUNDRY_API_KEY`.

## Recursos adicionais

* [Documentação do Microsoft Foundry](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Modelos do Microsoft Foundry](https://ai.azure.com/explore/models)
* [Preços do Microsoft Foundry](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
