> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Microsoft Foundry 上的 Claude Code

> 了解如何透過 Microsoft Foundry 配置 Claude Code，包括設定、配置和故障排除。

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

## 先決條件

在使用 Microsoft Foundry 配置 Claude Code 之前，請確保您具有：

* 具有 Microsoft Foundry 存取權限的 Azure 訂閱
* 建立 Microsoft Foundry 資源和部署的 RBAC 權限
* 已安裝並配置 Azure CLI（選用 - 僅在您沒有其他取得認證機制時才需要）

<Note>
  如果您要將 Claude Code 部署給多個使用者，請[固定您的模型版本](#4-pin-model-versions)以防止在 Anthropic 發佈新模型時發生中斷。
</Note>

## 設定

### 1. 佈建 Microsoft Foundry 資源

首先，在 Azure 中建立 Claude 資源：

1. 瀏覽至 [Microsoft Foundry 入口網站](https://ai.azure.com/)
2. 建立新資源，並記下您的資源名稱
3. 為 Claude 模型建立部署：
   * Claude Opus
   * Claude Sonnet
   * Claude Haiku

### 2. 配置 Azure 認證

Claude Code 支援 Microsoft Foundry 的兩種驗證方法。選擇最適合您安全性要求的方法。

**選項 A：API 金鑰驗證**

1. 在 Microsoft Foundry 入口網站中瀏覽至您的資源
2. 前往 **端點和金鑰** 部分
3. 複製 **API 金鑰**
4. 設定環境變數：

```bash theme={null}
export ANTHROPIC_FOUNDRY_API_KEY=your-azure-api-key
```

**選項 B：Microsoft Entra ID 驗證**

當未設定 `ANTHROPIC_FOUNDRY_API_KEY` 時，Claude Code 會自動使用 Azure SDK [預設認證鏈](https://learn.microsoft.com/en-us/azure/developer/javascript/sdk/authentication/credential-chains#defaultazurecredential-overview)。
這支援多種方法來驗證本機和遠端工作負載。

在本機環境中，您通常可以使用 Azure CLI：

```bash theme={null}
az login
```

<Note>
  使用 Microsoft Foundry 時，`/login` 和 `/logout` 命令已停用，因為驗證是透過 Azure 認證處理的。
</Note>

### 3. 配置 Claude Code

設定下列環境變數以啟用 Microsoft Foundry：

```bash theme={null}
# 啟用 Microsoft Foundry 整合
export CLAUDE_CODE_USE_FOUNDRY=1

# Azure 資源名稱（將 {resource} 替換為您的資源名稱）
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# 或提供完整的基礎 URL：
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com/anthropic
```

### 4. 固定模型版本

<Warning>
  為每個部署固定特定的模型版本。如果您使用模型別名（`sonnet`、`opus`、`haiku`）而不固定版本，Claude Code 可能會嘗試使用您的 Foundry 帳戶中不可用的較新模型版本，在 Anthropic 發佈更新時破壞現有使用者。建立 Azure 部署時，請選擇特定的模型版本，而不是「自動更新至最新版本」。
</Warning>

設定模型變數以符合您在步驟 1 中建立的部署名稱。

如果沒有 `ANTHROPIC_DEFAULT_OPUS_MODEL`，Foundry 上的 `opus` 別名會解析為 Opus 4.6。將其設定為 Opus 4.7 ID 以使用最新模型：

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-6'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
```

背景工作（例如工作階段標題生成）使用小型/快速模型，通常是 Haiku 級別的模型。在 Foundry 上，Claude Code 預設使用主要模型，因為並非每個帳戶都有 Haiku 部署。若要為背景工作使用 Haiku，請將 `ANTHROPIC_DEFAULT_HAIKU_MODEL` 設定為您帳戶中可用的 Haiku 部署，如上所示。

如需目前和舊版模型 ID，請參閱[模型概覽](https://platform.claude.com/docs/en/about-claude/models/overview)。如需完整的環境變數清單，請參閱[模型配置](/zh-TW/model-config#pin-models-for-third-party-deployments)。

[Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 會自動啟用。若要要求 1 小時的快取 TTL 而不是 5 分鐘的預設值，請設定下列變數；具有 1 小時 TTL 的快取寫入會以更高的費率計費：

```bash theme={null}
export ENABLE_PROMPT_CACHING_1H=1
```

## Azure RBAC 配置

`Azure AI User` 和 `Cognitive Services User` 預設角色包含叫用 Claude 模型所需的所有權限。

如需更嚴格的權限，請建立具有以下內容的自訂角色：

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

如需詳細資訊，請參閱 [Microsoft Foundry RBAC 文件](https://learn.microsoft.com/en-us/azure/ai-foundry/concepts/rbac-azure-ai-foundry)。

## 故障排除

如果您收到錯誤「Failed to get token from azureADTokenProvider: ChainedTokenCredential authentication failed」：

* 在環境中配置 Entra ID，或設定 `ANTHROPIC_FOUNDRY_API_KEY`。

## 其他資源

* [Microsoft Foundry 文件](https://learn.microsoft.com/en-us/azure/ai-foundry/what-is-azure-ai-foundry)
* [Microsoft Foundry 模型](https://ai.azure.com/explore/models)
* [Microsoft Foundry 定價](https://azure.microsoft.com/en-us/pricing/details/ai-foundry/)
