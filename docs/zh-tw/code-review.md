> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Code Review

> 設定自動化 PR 審查，使用多代理分析您的完整程式碼庫來捕捉邏輯錯誤、安全漏洞和迴歸

<Note>
  Code Review 處於研究預覽階段，適用於 [Teams 和 Enterprise](https://claude.ai/admin-settings/claude-code) 訂閱。不適用於啟用 [Zero Data Retention](/zh-TW/zero-data-retention) 的組織。
</Note>

Code Review 分析您的 GitHub pull request，並在發現問題的程式碼行上發佈內聯評論。一群專門的代理在您完整程式碼庫的背景下檢查程式碼變更，尋找邏輯錯誤、安全漏洞、破損的邊界情況和細微的迴歸。

發現結果按嚴重程度標記，不會批准或阻止您的 PR，因此現有的審查工作流程保持不變。您可以通過在您的儲存庫中新增 `CLAUDE.md` 或 `REVIEW.md` 檔案來調整 Claude 標記的內容。

若要在您自己的 CI 基礎設施中執行 Claude 而不是此託管服務，請參閱 [GitHub Actions](/zh-TW/github-actions) 或 [GitLab CI/CD](/zh-TW/gitlab-ci-cd)。

本頁涵蓋：

* [審查如何運作](#how-reviews-work)
* [設定](#set-up-code-review)
* [自訂審查](#customize-reviews)，使用 `CLAUDE.md` 和 `REVIEW.md`
* [定價](#pricing)

## 審查如何運作

一旦管理員為您的組織[啟用 Code Review](#set-up-code-review)，當 pull request 開啟或更新時，審查會自動執行。多個代理在 Anthropic 基礎設施上並行分析差異和周圍程式碼。每個代理尋找不同類別的問題，然後驗證步驟根據實際程式碼行為檢查候選項以過濾掉誤報。結果被去重複、按嚴重程度排名，並作為內聯評論發佈在發現問題的特定行上。如果未發現問題，Claude 會在 PR 上發佈簡短的確認評論。

審查成本隨著 PR 大小和複雜性而擴展，平均在 20 分鐘內完成。管理員可以通過[分析儀表板](#view-usage)監控審查活動和支出。

### 嚴重程度級別

每個發現都標記有嚴重程度級別：

| 標記 | 嚴重程度         | 含義                   |
| :- | :----------- | :------------------- |
| 🔴 | Normal       | 應在合併前修復的錯誤           |
| 🟡 | Nit          | 輕微問題，值得修復但不阻止        |
| 🟣 | Pre-existing | 程式碼庫中存在但未由此 PR 引入的錯誤 |

發現包括可摺疊的擴展推理部分，您可以展開以了解 Claude 為什麼標記該問題以及它如何驗證問題。

### Code Review 檢查的內容

預設情況下，Code Review 專注於正確性：會破壞生產的錯誤，而不是格式設定偏好或缺少的測試覆蓋。您可以通過[新增指導檔案](#customize-reviews)到您的儲存庫來擴展它檢查的內容。

## 設定 Code Review

管理員為組織啟用 Code Review 一次，並選擇要包含的儲存庫。

<Steps>
  <Step title="開啟 Claude Code 管理員設定">
    前往 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) 並找到 Code Review 部分。您需要對您的 Claude 組織具有管理員存取權限，以及在您的 GitHub 組織中安裝 GitHub Apps 的權限。
  </Step>

  <Step title="開始設定">
    點擊**設定**。這開始 GitHub App 安裝流程。
  </Step>

  <Step title="安裝 Claude GitHub App">
    按照提示將 Claude GitHub App 安裝到您的 GitHub 組織。該應用程式要求這些儲存庫權限：

    * **Contents**：讀取和寫入
    * **Issues**：讀取和寫入
    * **Pull requests**：讀取和寫入

    Code Review 使用對內容的讀取存取權限和對 pull request 的寫入存取權限。更廣泛的權限集也支援 [GitHub Actions](/zh-TW/github-actions)（如果您稍後啟用）。
  </Step>

  <Step title="選擇儲存庫">
    選擇要為 Code Review 啟用的儲存庫。如果您看不到儲存庫，請確保您在安裝期間給予 Claude GitHub App 存取權限。您可以稍後新增更多儲存庫。
  </Step>

  <Step title="設定每個儲存庫的審查觸發器">
    設定完成後，Code Review 部分在表格中顯示您的儲存庫。對於每個儲存庫，使用下拉式選單選擇審查執行的時間：

    * **僅在 PR 建立後**：當 PR 開啟或標記為準備審查時，審查執行一次
    * **在每次推送到 PR 分支後**：審查在每次推送時執行，在 PR 演變時捕捉新問題，並在您修復標記的問題時自動解決執行緒

    在每次推送時審查會執行更多審查並花費更多。從 PR 建立開始，然後對於您想要持續覆蓋和自動執行緒清理的儲存庫切換到推送時。
  </Step>
</Steps>

儲存庫表格還根據最近的活動顯示每個儲存庫的平均審查成本。使用行操作選單按儲存庫開啟或關閉 Code Review，或完全移除儲存庫。

若要驗證設定，請開啟測試 PR。名為 **Claude Code Review** 的檢查執行會在幾分鐘內出現。如果沒有，請確認儲存庫列在您的管理員設定中，並且 Claude GitHub App 有權存取它。

## 自訂審查

Code Review 從您的儲存庫讀取兩個檔案來指導它標記的內容。兩者都是在預設正確性檢查之上的附加項：

* **`CLAUDE.md`**：Claude Code 用於所有任務（不僅僅是審查）的共享專案指示。當指導也適用於互動式 Claude Code 工作階段時使用它。
* **`REVIEW.md`**：僅審查指導，在程式碼審查期間專門讀取。對於嚴格關於在審查期間標記或跳過什麼的規則，以及會使您的一般 `CLAUDE.md` 混亂的規則，使用它。

### CLAUDE.md

Code Review 讀取您儲存庫的 `CLAUDE.md` 檔案，並將新引入的違規視為 nit 級別的發現。這是雙向工作的：如果您的 PR 以使 `CLAUDE.md` 陳述過時的方式更改程式碼，Claude 會標記文件需要更新。

Claude 在您目錄層次結構的每個級別讀取 `CLAUDE.md` 檔案，因此子目錄的 `CLAUDE.md` 中的規則僅適用於該路徑下的檔案。有關 `CLAUDE.md` 如何運作的更多資訊，請參閱[記憶體文件](/zh-TW/memory)。

對於您不想應用於一般 Claude Code 工作階段的審查特定指導，請改用 [`REVIEW.md`](#review-md)。

### REVIEW\.md

將 `REVIEW.md` 檔案新增到您的儲存庫根目錄以獲取審查特定規則。使用它來編碼：

* 公司或團隊風格指南："優先使用早期返回而不是嵌套條件"
* 語言或框架特定的約定，不由 linter 涵蓋
* Claude 應始終標記的事項："任何新 API 路由必須有整合測試"
* Claude 應跳過的事項："不要評論 `/gen/` 下生成程式碼中的格式設定"

範例 `REVIEW.md`：

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

Claude 在儲存庫根目錄自動發現 `REVIEW.md`。無需配置。

## 檢視使用情況

前往 [claude.ai/analytics/code-review](https://claude.ai/analytics/code-review) 以查看整個組織的 Code Review 活動。儀表板顯示：

| 部分                   | 它顯示什麼                          |
| :------------------- | :----------------------------- |
| PRs reviewed         | 在選定時間範圍內審查的 pull request 的每日計數 |
| Cost weekly          | Code Review 的每週支出              |
| Feedback             | 因開發人員解決問題而自動解決的審查評論計數          |
| Repository breakdown | 每個儲存庫的審查 PR 計數和已解決評論           |

管理員設定中的儲存庫表格也顯示每個儲存庫的平均審查成本。

## 定價

Code Review 根據令牌使用情況計費。審查平均 \$15-25，隨著 PR 大小、程式碼庫複雜性和需要驗證的問題數量而擴展。Code Review 使用通過[額外使用](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)單獨計費，不計入您計劃的包含使用量。

您選擇的審查觸發器會影響總成本：

* **僅在 PR 建立後**：每個 PR 執行一次
* **在每次推送時**：在每次提交時執行，將成本乘以推送次數

無論您的組織是否為其他 Claude Code 功能使用 AWS Bedrock 或 Google Vertex AI，成本都會出現在您的 Anthropic 帳單上。若要為 Code Review 設定每月支出上限，請前往 [claude.ai/admin-settings/usage](https://claude.ai/admin-settings/usage) 並為 Claude Code Review 服務配置限制。

通過[分析](#view-usage)中的每週成本圖表或管理員設定中的每個儲存庫平均成本欄監控支出。

## 相關資源

Code Review 設計用於與 Claude Code 的其餘部分一起工作。如果您想在開啟 PR 之前在本地執行審查、需要自託管設定，或想深入了解 `CLAUDE.md` 如何在工具中塑造 Claude 的行為，這些頁面是很好的下一步：

* [Plugins](/zh-TW/discover-plugins)：瀏覽外掛程式市場，包括用於在推送前在本地執行按需審查的 `code-review` 外掛程式
* [GitHub Actions](/zh-TW/github-actions)：在您自己的 GitHub Actions 工作流程中執行 Claude，以實現超越程式碼審查的自訂自動化
* [GitLab CI/CD](/zh-TW/gitlab-ci-cd)：GitLab 管道的自託管 Claude 整合
* [Memory](/zh-TW/memory)：`CLAUDE.md` 檔案如何在 Claude Code 中工作
* [Analytics](/zh-TW/analytics)：追蹤超越程式碼審查的 Claude Code 使用情況
