> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> 設定自動化 PR 審查，使用多代理分析您的完整程式碼庫來捕捉邏輯錯誤、安全漏洞和迴歸

<Note>
  Code Review 處於研究預覽階段，適用於 [Teams 和 Enterprise](https://claude.ai/admin-settings/claude-code) 訂閱。對於啟用了 [Zero Data Retention](/zh-TW/zero-data-retention) 的組織，此功能不可用。
</Note>

Code Review 分析您的 GitHub pull request，並在發現問題的程式碼行上發佈內聯評論。一群專門的代理在您完整程式碼庫的背景下檢查程式碼變更，尋找邏輯錯誤、安全漏洞、破損的邊界情況和細微的迴歸。

發現結果按嚴重程度標記，不會批准或阻止您的 PR，因此現有的審查工作流程保持不變。您可以通過在存儲庫中添加 `CLAUDE.md` 或 `REVIEW.md` 文件來調整 Claude 標記的內容。

要在您自己的 CI 基礎設施中運行 Claude 而不是此託管服務，請參閱 [GitHub Actions](/zh-TW/github-actions) 或 [GitLab CI/CD](/zh-TW/gitlab-ci-cd)。

本頁涵蓋：

* [審查如何運作](#how-reviews-work)
* [設定](#set-up-code-review)
* [自訂審查](#customize-reviews)，使用 `CLAUDE.md` 和 `REVIEW.md`
* [定價](#pricing)

## 審查如何運作

一旦管理員為您的組織[啟用 Code Review](#set-up-code-review)，審查將在 PR 開啟時、每次推送時或手動請求時觸發，具體取決於存儲庫的配置行為。在任何模式下，評論 `@claude review` [在 PR 上啟動審查](#manually-trigger-reviews)。

當審查運行時，多個代理在 Anthropic 基礎設施上並行分析差異和周圍程式碼。每個代理尋找不同類別的問題，然後驗證步驟檢查候選項目是否符合實際程式碼行為，以過濾掉誤報。結果被去重、按嚴重程度排名，並作為內聯評論發佈在發現問題的特定行上。如果未發現問題，Claude 會在 PR 上發佈簡短的確認評論。

審查成本隨著 PR 大小和複雜性而擴展，平均在 20 分鐘內完成。管理員可以通過 [分析儀表板](#view-usage) 監控審查活動和支出。

### 嚴重程度級別

每個發現都標記有嚴重程度級別：

| 標記 | 嚴重程度 | 含義                   |
| :- | :--- | :------------------- |
| 🔴 | 正常   | 應在合併前修復的錯誤           |
| 🟡 | 細節   | 輕微問題，值得修復但不阻止        |
| 🟣 | 預先存在 | 程式碼庫中存在但未由此 PR 引入的錯誤 |

發現包括可折疊的擴展推理部分，您可以展開以了解 Claude 為什麼標記該問題以及它如何驗證問題。

### Code Review 檢查的內容

默認情況下，Code Review 專注於正確性：會破壞生產的錯誤，而不是格式設置偏好或缺失的測試覆蓋。您可以通過 [添加指導文件](#customize-reviews) 到您的存儲庫來擴展它檢查的內容。

## 設定 Code Review

管理員為組織啟用 Code Review 一次，並選擇要包含的存儲庫。

<Steps>
  <Step title="開啟 Claude Code 管理員設定">
    前往 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) 並找到 Code Review 部分。您需要對 Claude 組織的管理員存取權限以及在 GitHub 組織中安裝 GitHub Apps 的權限。
  </Step>

  <Step title="開始設定">
    點擊 **Setup**。這開始 GitHub App 安裝流程。
  </Step>

  <Step title="安裝 Claude GitHub App">
    按照提示將 Claude GitHub App 安裝到您的 GitHub 組織。該應用請求這些存儲庫權限：

    * **Contents**：讀取和寫入
    * **Issues**：讀取和寫入
    * **Pull requests**：讀取和寫入

    Code Review 使用對內容的讀取存取權限和對 pull request 的寫入存取權限。更廣泛的權限集也支持 [GitHub Actions](/zh-TW/github-actions)，如果您稍後啟用它。
  </Step>

  <Step title="選擇存儲庫">
    選擇要為 Code Review 啟用的存儲庫。如果您看不到存儲庫，請確保您在安裝期間給予 Claude GitHub App 存取權限。您可以稍後添加更多存儲庫。
  </Step>

  <Step title="設定每個存儲庫的審查觸發器">
    設定完成後，Code Review 部分在表格中顯示您的存儲庫。對於每個存儲庫，使用 **Review Behavior** 下拉菜單選擇何時運行審查：

    * **Once after PR creation**：當 PR 開啟或標記為準備審查時，審查運行一次
    * **After every push**：在每次推送到 PR 分支時運行審查，在 PR 演變時捕捉新問題，並在您修復標記的問題時自動解決線程
    * **Manual**：審查僅在有人 [在 PR 上評論 `@claude review`](#manually-trigger-reviews) 時開始；之後對該 PR 的後續推送會自動審查

    每次推送時審查運行最多的審查並花費最多。手動模式對於高流量存儲庫很有用，您想選擇特定 PR 進行審查，或者只在 PR 準備好時才開始審查您的 PR。
  </Step>
</Steps>

存儲庫表還顯示每個存儲庫基於最近活動的平均審查成本。使用行操作菜單按存儲庫打開或關閉 Code Review，或完全移除存儲庫。

要驗證設定，請開啟測試 PR。如果您選擇了自動觸發器，名為 **Claude Code Review** 的檢查運行會在幾分鐘內出現。如果您選擇了手動，在 PR 上評論 `@claude review` 以開始第一次審查。如果沒有檢查運行出現，請確認存儲庫列在您的管理員設定中，並且 Claude GitHub App 有權存取它。

## 手動觸發審查

在 pull request 上評論 `@claude review` 以開始審查，並選擇該 PR 進入推送觸發的審查。這適用於存儲庫的配置觸發器，無論如何：在手動模式下使用它來選擇特定 PR 進行審查，或在其他模式下獲得立即重新審查。無論哪種方式，對該 PR 的推送從那時起觸發審查。

要使評論觸發審查：

* 將其發佈為頂級 PR 評論，而不是差異行上的內聯評論
* 在評論開始時放置 `@claude review`
* 您必須對存儲庫具有所有者、成員或協作者存取權限
* PR 必須開啟且不是草稿

如果該 PR 上已有審查正在運行，請求將排隊直到進行中的審查完成。您可以通過 PR 上的檢查運行監控進度。

## 自訂審查

Code Review 從您的存儲庫讀取兩個文件來指導它標記的內容。兩者都是在默認正確性檢查之上的附加：

* **`CLAUDE.md`**：Claude Code 用於所有任務的共享項目指令，不僅僅是審查。當指導也適用於互動式 Claude Code 會話時使用它。
* **`REVIEW.md`**：僅審查指導，在程式碼審查期間專門讀取。對於嚴格關於在審查期間標記或跳過什麼的規則，以及會使您的一般 `CLAUDE.md` 混亂的規則，使用它。

### CLAUDE.md

Code Review 讀取您存儲庫的 `CLAUDE.md` 文件，並將新引入的違規視為細節級別的發現。這是雙向工作的：如果您的 PR 以使 `CLAUDE.md` 陳述過時的方式更改程式碼，Claude 會標記文件需要更新。

Claude 在目錄層次結構的每個級別讀取 `CLAUDE.md` 文件，因此子目錄的 `CLAUDE.md` 中的規則僅適用於該路徑下的文件。有關 `CLAUDE.md` 如何運作的更多信息，請參閱 [memory 文檔](/zh-TW/memory)。

對於您不想應用於一般 Claude Code 會話的審查特定指導，請改用 [`REVIEW.md`](#review-md)。

### REVIEW\.md

將 `REVIEW.md` 文件添加到您的存儲庫根目錄以獲取審查特定規則。使用它來編碼：

* 公司或團隊風格指南："優先使用早期返回而不是嵌套條件"
* 語言或框架特定的約定，不被 linter 覆蓋
* Claude 應始終標記的內容："任何新 API 路由必須有集成測試"
* Claude 應跳過的內容："不要評論 `/gen/` 下生成程式碼中的格式設置"

示例 `REVIEW.md`：

```markdown  theme={null}
# Code Review Guidelines

## Always check
- New API endpoints have corresponding integration tests
- Database migrations are backward-compatible
- Error messages don't leak internal details to users

## Style
- Prefer `match` statements over chained `isinstance` checks
- Use structured logging, not f-string interpolation in log calls

## Skip
- Generated files under `src/gen/`
- Formatting-only changes in `*.lock` files
```

Claude 在存儲庫根目錄自動發現 `REVIEW.md`。無需配置。

## 查看使用情況

前往 [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) 查看整個組織的 Code Review 活動。儀表板顯示：

| 部分                   | 它顯示什麼                          |
| :------------------- | :----------------------------- |
| PRs reviewed         | 在選定時間範圍內審查的 pull request 的每日計數 |
| Cost weekly          | Code Review 的每週支出              |
| Feedback             | 因開發人員解決問題而自動解決的審查評論計數          |
| Repository breakdown | 每個存儲庫審查的 PR 計數和解決的評論           |

管理員設定中的存儲庫表也顯示每個存儲庫的平均審查成本。

## 定價

Code Review 根據令牌使用情況計費。審查平均 \$15-25，隨著 PR 大小、程式碼庫複雜性和需要驗證的問題數量而擴展。Code Review 使用通過 [extra usage](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) 單獨計費，不計入您計劃的包含使用情況。

您選擇的審查觸發器影響總成本：

* **Once after PR creation**：每個 PR 運行一次
* **After every push**：在每次推送時運行，將成本乘以推送次數
* **Manual**：在有人在 PR 上評論 `@claude review` 之前沒有審查

在任何模式下，評論 `@claude review` [選擇 PR 進入推送觸發的審查](#manually-trigger-reviews)，因此在該評論之後每次推送都會產生額外成本。

成本出現在您的 Anthropic 帳單上，無論您的組織是否為其他 Claude Code 功能使用 AWS Bedrock 或 Google Vertex AI。要為 Code Review 設定月度支出上限，請前往 [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) 並為 Claude Code Review 服務配置限制。

通過 [analytics](#view-usage) 中的每週成本圖表或管理員設定中的每個存儲庫平均成本列監控支出。

## 相關資源

Code Review 設計用於與 Claude Code 的其餘部分一起工作。如果您想在開啟 PR 之前在本地運行審查、需要自託管設定，或想深入了解 `CLAUDE.md` 如何在工具中塑造 Claude 的行為，這些頁面是很好的下一步：

* [Plugins](/zh-TW/discover-plugins)：瀏覽插件市場，包括用於在推送前本地運行按需審查的 `code-review` 插件
* [GitHub Actions](/zh-TW/github-actions)：在您自己的 GitHub Actions 工作流中運行 Claude，以實現超越程式碼審查的自訂自動化
* [GitLab CI/CD](/zh-TW/gitlab-ci-cd)：GitLab 管道的自託管 Claude 集成
* [Memory](/zh-TW/memory)：`CLAUDE.md` 文件如何在 Claude Code 中工作
* [Analytics](/zh-TW/analytics)：追蹤超越程式碼審查的 Claude Code 使用情況
