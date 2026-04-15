> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code on Microsoft Foundry

> 了解如何透過 Microsoft Foundry 配置 Claude Code，包括設定、配置和故障排除。

## 先決條件

在使用 Microsoft Foundry 配置 Claude Code 之前，請確保您具有：

* 具有 Microsoft Foundry 存取權限的 Azure 訂閱
* 建立 Microsoft Foundry 資源和部署的 RBAC 權限
* 已安裝並配置 Azure CLI（選用 - 僅在您沒有其他取得認證機制時才需要）

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

設定下列環境變數以啟用 Microsoft Foundry。請注意，您的部署名稱會設定為 Claude Code 中的模型識別碼（如果使用建議的部署名稱，可能是選用的）。

```bash theme={null}
# 啟用 Microsoft Foundry 整合
export CLAUDE_CODE_USE_FOUNDRY=1

# Azure 資源名稱（將 {resource} 替換為您的資源名稱）
export ANTHROPIC_FOUNDRY_RESOURCE={resource}
# 或提供完整的基礎 URL：
# export ANTHROPIC_FOUNDRY_BASE_URL=https://{resource}.services.ai.azure.com

# 將模型設定為您資源的部署名稱
export ANTHROPIC_DEFAULT_SONNET_MODEL='claude-sonnet-4-5'
export ANTHROPIC_DEFAULT_HAIKU_MODEL='claude-haiku-4-5'
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-1'
```

如需模型配置選項的更多詳細資訊，請參閱[模型配置](/zh-TW/model-config)。

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
