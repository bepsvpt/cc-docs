> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 設定伺服器管理的設定 (公開測試版)

> 透過伺服器傳遞的設定在 Claude.ai 上為您的組織集中設定 Claude Code，無需裝置管理基礎設施。

伺服器管理的設定允許管理員透過 Claude.ai 上的網頁介面集中設定 Claude Code。Claude Code 用戶端在使用者使用其組織認證進行身份驗證時會自動接收這些設定。

此方法適用於沒有裝置管理基礎設施的組織，或需要為非受管裝置上的使用者管理設定的組織。

<Note>
  伺服器管理的設定處於公開測試版，適用於 [Claude for Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_teams#team-&-enterprise) 和 [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_enterprise) 客戶。功能可能在正式推出前進行演變。
</Note>

## 需求

若要使用伺服器管理的設定，您需要：

* Claude for Teams 或 Claude for Enterprise 方案
* Claude for Teams 的 Claude Code 版本 2.1.38 或更新版本，或 Claude for Enterprise 的版本 2.1.30 或更新版本
* 對 `api.anthropic.com` 的網路存取

## 在伺服器管理和端點管理的設定之間選擇

Claude Code 支援兩種集中設定方法。伺服器管理的設定從 Anthropic 的伺服器傳遞設定。[端點管理的設定](/zh-TW/settings#settings-files) 透過原生作業系統原則 (macOS 受管偏好設定、Windows 登錄) 或受管設定檔直接部署到裝置。

| 方法                                            | 最適合                    | 安全模型                          |
| :-------------------------------------------- | :--------------------- | :---------------------------- |
| **伺服器管理的設定**                                  | 沒有 MDM 的組織，或非受管裝置上的使用者 | 在身份驗證時從 Anthropic 伺服器傳遞的設定    |
| **[端點管理的設定](/zh-TW/settings#settings-files)** | 具有 MDM 或端點管理的組織        | 透過 MDM 設定檔、登錄原則或受管設定檔部署到裝置的設定 |

如果您的裝置已在 MDM 或端點管理解決方案中註冊，端點管理的設定提供更強的安全保證，因為設定檔可以在作業系統層級受到保護，防止使用者修改。

## 設定伺服器管理的設定

<Steps>
  <Step title="開啟管理員主控台">
    在 [Claude.ai](https://claude.ai) 中，導覽至 **Admin Settings > Claude Code > Managed settings**。
  </Step>

  <Step title="定義您的設定">
    將您的設定新增為 JSON。支援 [`settings.json` 中提供的所有設定](/zh-TW/settings#available-settings)，包括 [hooks](/zh-TW/hooks)、[環境變數](/zh-TW/env-vars) 和[僅限受管的設定](/zh-TW/permissions#managed-only-settings)，例如 `allowManagedPermissionRulesOnly`。

    此範例強制執行權限拒絕清單，防止使用者繞過權限，並將權限規則限制為在受管設定中定義的規則：

    ```json  theme={null}
    {
      "permissions": {
        "deny": [
          "Bash(curl *)",
          "Read(./.env)",
          "Read(./.env.*)",
          "Read(./secrets/**)"
        ],
        "disableBypassPermissionsMode": "disable"
      },
      "allowManagedPermissionRulesOnly": true
    }
    ```

    Hooks 使用與 `settings.json` 中相同的格式。

    此範例在整個組織中的每次檔案編輯後執行稽核指令碼：

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              { "type": "command", "command": "/usr/local/bin/audit-edit.sh" }
            ]
          }
        ]
      }
    }
    ```

    若要設定 [auto mode](/zh-TW/permission-modes#eliminate-prompts-with-auto-mode) 分類器，使其知道您的組織信任哪些儲存庫、儲存桶和網域：

    ```json  theme={null}
    {
      "autoMode": {
        "environment": [
          "Source control: github.example.com/acme-corp and all repos under it",
          "Trusted cloud buckets: s3://acme-build-artifacts, gs://acme-ml-datasets",
          "Trusted internal domains: *.corp.example.com"
        ]
      }
    }
    ```

    因為 hooks 執行 shell 命令，使用者在套用前會看到[安全核准對話方塊](#security-approval-dialogs)。請參閱[設定 auto mode 分類器](/zh-TW/permissions#configure-the-auto-mode-classifier)，了解 `autoMode` 項目如何影響分類器阻止的內容，以及關於 `allow` 和 `soft_deny` 欄位的重要警告。
  </Step>

  <Step title="儲存並部署">
    儲存您的變更。Claude Code 用戶端在下次啟動或每小時輪詢週期時會接收更新的設定。
  </Step>
</Steps>

### 驗證設定傳遞

若要確認設定正在套用，請要求使用者重新啟動 Claude Code。如果設定包含觸發[安全核准對話方塊](#security-approval-dialogs)的設定，使用者會在啟動時看到描述受管設定的提示。您也可以透過讓使用者執行 `/permissions` 來檢視其有效的權限規則，以驗證受管權限規則是否處於作用中。

### 存取控制

以下角色可以管理伺服器管理的設定：

* **主要擁有者**
* **擁有者**

限制對受信任人員的存取，因為設定變更會套用到組織中的所有使用者。

### 僅限受管的設定

大多數[設定金鑰](/zh-TW/settings#available-settings)可在任何範圍中運作。少數金鑰只能從受管設定中讀取，在放置於使用者或專案設定檔中時無效。請參閱[僅限受管的設定](/zh-TW/permissions#managed-only-settings)以取得完整清單。任何不在該清單上的設定仍然可以放置在受管設定中，並具有最高優先順序。

### 目前的限制

伺服器管理的設定在測試版期間有以下限制：

* 設定統一套用到組織中的所有使用者。尚不支援每個群組的設定。
* [MCP 伺服器設定](/zh-TW/mcp#managed-mcp-configuration) 無法透過伺服器管理的設定分發。

## 設定傳遞

### 設定優先順序

伺服器管理的設定和[端點管理的設定](/zh-TW/settings#settings-files)都佔據 Claude Code [設定階層](/zh-TW/settings#settings-precedence)中的最高層級。沒有其他設定層級可以覆蓋它們，包括命令列引數。

在受管層級內，第一個傳遞非空設定的來源會獲勝。伺服器管理的設定會先檢查，然後是端點管理的設定。來源不會合併：如果伺服器管理的設定傳遞任何金鑰，端點管理的設定會被完全忽略。如果伺服器管理的設定不傳遞任何內容，端點管理的設定會套用。

如果您在管理員主控台中清除伺服器管理的設定，意圖回退到端點管理的 plist 或登錄原則，請注意[快取的設定](#fetch-and-caching-behavior)會在用戶端機器上持續存在，直到下次成功擷取。執行 `/status` 以查看哪個受管來源處於作用中。

### 擷取和快取行為

Claude Code 在啟動時從 Anthropic 的伺服器擷取設定，並在作用中的工作階段期間每小時輪詢一次更新。

**首次啟動而無快取設定：**

* Claude Code 非同步擷取設定
* 如果擷取失敗，Claude Code 會在沒有受管設定的情況下繼續
* 在設定載入之前有一個簡短的視窗，其中限制尚未強制執行

**後續啟動並有快取設定：**

* 快取設定在啟動時立即套用
* Claude Code 在背景擷取新鮮設定
* 快取設定透過網路故障持續存在

Claude Code 自動套用設定更新而無需重新啟動，除了進階設定（例如 OpenTelemetry 設定）需要完整重新啟動才能生效。

### 安全核准對話方塊

某些可能造成安全風險的設定需要明確的使用者核准才能套用：

* **Shell 命令設定**：執行 shell 命令的設定
* **自訂環境變數**：不在已知安全允許清單中的變數
* **Hook 設定**：任何 hook 定義

當這些設定存在時，使用者會看到安全對話方塊，說明正在設定的內容。使用者必須核准才能繼續。如果使用者拒絕設定，Claude Code 會結束。

<Note>
  在使用 `-p` 旗標的非互動模式中，Claude Code 會略過安全對話方塊並在沒有使用者核准的情況下套用設定。
</Note>

## 平台可用性

伺服器管理的設定需要直接連線到 `api.anthropic.com`，在使用第三方模型提供者時無法使用：

* Amazon Bedrock
* Google Vertex AI
* Microsoft Foundry
* 透過 `ANTHROPIC_BASE_URL` 或 [LLM 閘道](/zh-TW/llm-gateway) 的自訂 API 端點

## 稽核記錄

設定變更的稽核記錄事件可透過合規性 API 或稽核記錄匯出取得。請聯絡您的 Anthropic 帳戶團隊以取得存取權。

稽核事件包括執行的動作類型、執行動作的帳戶和裝置，以及對先前和新值的參考。

## 安全考量

伺服器管理的設定提供集中式原則強制執行，但它們作為用戶端控制運作。在非受管裝置上，具有管理員或 sudo 存取權的使用者可以修改 Claude Code 二進位檔、檔案系統或網路設定。

| 情況                             | 行為                                 |
| :----------------------------- | :--------------------------------- |
| 使用者編輯快取的設定檔                    | 篡改的檔案在啟動時套用，但正確的設定會在下次伺服器擷取時還原     |
| 使用者刪除快取的設定檔                    | 首次啟動行為發生：設定非同步擷取，有一個簡短的未強制執行視窗     |
| API 無法使用                       | 如果可用，快取設定會套用，否則受管設定在下次成功擷取之前不會強制執行 |
| 使用者使用不同的組織進行身份驗證               | 不會為受管組織外的帳戶傳遞設定                    |
| 使用者設定非預設的 `ANTHROPIC_BASE_URL` | 使用第三方 API 提供者時，伺服器管理的設定會被略過        |

若要偵測執行時期設定變更，請使用 [`ConfigChange` hooks](/zh-TW/hooks#configchange) 來記錄修改或在未授權的變更生效前阻止它們。

如需更強的強制執行保證，請在已在 MDM 解決方案中註冊的裝置上使用[端點管理的設定](/zh-TW/settings#settings-files)。

## 另請參閱

用於管理 Claude Code 設定的相關頁面：

* [Settings](/zh-TW/settings)：完整的設定參考，包括所有可用的設定
* [Endpoint-managed settings](/zh-TW/settings#settings-files)：由 IT 部門部署到裝置的受管設定
* [Authentication](/zh-TW/authentication)：設定使用者對 Claude Code 的存取
* [Security](/zh-TW/security)：安全保護措施和最佳實踐
