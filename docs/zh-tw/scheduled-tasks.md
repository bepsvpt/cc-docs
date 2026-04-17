> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 按排程執行提示

> 使用 /loop 和 cron 排程工具在 Claude Code 工作階段內重複執行提示、輪詢狀態或設定一次性提醒。

<Note>
  排程任務需要 Claude Code v2.1.72 或更新版本。使用 `claude --version` 檢查您的版本。
</Note>

排程任務讓 Claude 按間隔自動重新執行提示。使用它們來輪詢部署、監督 PR、檢查長時間執行的建置，或在工作階段稍後提醒自己執行某些操作。若要改為對事件發生時做出反應而不是輪詢，請參閱 [Channels](/zh-TW/channels)：您的 CI 可以直接將失敗推送到工作階段中。

任務的範圍限於工作階段：它們存在於目前的 Claude Code 程序中，當您退出時就會消失。如需在重新啟動後仍能持續的持久排程，請使用 [Routines](/zh-TW/routines)、[Desktop 排程任務](/zh-TW/desktop-scheduled-tasks) 或 [GitHub Actions](/zh-TW/github-actions)。

## 比較排程選項

Claude Code offers three ways to schedule recurring work:

|                            | [Cloud](/en/routines)          | [Desktop](/en/desktop-scheduled-tasks) | [`/loop`](/en/scheduled-tasks)      |
| :------------------------- | :----------------------------- | :------------------------------------- | :---------------------------------- |
| Runs on                    | Anthropic cloud                | Your machine                           | Your machine                        |
| Requires machine on        | No                             | Yes                                    | Yes                                 |
| Requires open session      | No                             | No                                     | Yes                                 |
| Persistent across restarts | Yes                            | Yes                                    | Restored on `--resume` if unexpired |
| Access to local files      | No (fresh clone)               | Yes                                    | Yes                                 |
| MCP servers                | Connectors configured per task | [Config files](/en/mcp) and connectors | Inherits from session               |
| Permission prompts         | No (runs autonomously)         | Configurable per task                  | Inherits from session               |
| Customizable schedule      | Via `/schedule` in the CLI     | Yes                                    | Yes                                 |
| Minimum interval           | 1 hour                         | 1 minute                               | 1 minute                            |

<Tip>
  Use **cloud tasks** for work that should run reliably without your machine. Use **Desktop tasks** when you need access to local files and tools. Use **`/loop`** for quick polling during a session.
</Tip>

## 使用 /loop 重複執行提示

`/loop` [bundled skill](/zh-TW/commands) 是排程重複執行提示的最快方式，同時工作階段保持開啟。間隔和提示都是選用的，您提供的內容決定了迴圈的行為方式。

| 您提供的內容 | 範例                          | 發生的情況                                                                |
| :----- | :-------------------------- | :------------------------------------------------------------------- |
| 間隔和提示  | `/loop 5m check the deploy` | 您的提示在[固定排程](#run-on-a-fixed-interval)上執行                             |
| 僅提示    | `/loop check the deploy`    | 您的提示在 [Claude 選擇的間隔](#let-claude-choose-the-interval)上執行，每次迭代        |
| 僅間隔或無  | `/loop`                     | [內建維護提示](#run-the-built-in-maintenance-prompt)執行，或您的 `loop.md`（如果存在） |

您也可以傳遞另一個命令作為提示，例如 `/loop 20m /review-pr 1234`，以在每次迭代時重新執行打包的工作流程。

### 在固定間隔上執行

當您提供間隔時，Claude 會將其轉換為 cron 表達式、排程工作，並確認頻率和工作 ID。

```text theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

間隔可以作為裸令牌（如 `30m`）在提示前面，或作為子句（如 `every 2 hours`）在後面。支援的單位為 `s`（秒）、`m`（分鐘）、`h`（小時）和 `d`（天）。

秒數會四捨五入到最近的分鐘，因為 cron 的粒度為一分鐘。不能均勻分割其單位的間隔（例如 `7m` 或 `90m`）會四捨五入到最近的整潔間隔，Claude 會告訴您它選擇了什麼。

### 讓 Claude 選擇間隔

當您省略間隔時，Claude 會動態選擇一個，而不是在固定的 cron 排程上執行。在每次迭代後，它會根據觀察到的情況選擇一個介於一分鐘到一小時之間的延遲：在建置完成或 PR 活躍時短暫等待，當沒有待處理項目時較長等待。選擇的延遲和原因會在每次迭代結束時列印。

下面的範例檢查 CI 和審查評論，Claude 在 PR 變得安靜後在迭代之間等待更長時間：

```text theme={null}
/loop check whether CI passed and address any review comments
```

當您要求動態 `/loop` 排程時，Claude 可能會直接使用 [Monitor tool](/zh-TW/tools-reference#monitor-tool)。Monitor 執行背景指令碼並串流回每個輸出行，這完全避免了輪詢，通常比在間隔上重新執行提示更具令牌效率和回應性。

動態排程的迴圈會像任何其他任務一樣出現在您的[排程任務清單](#manage-scheduled-tasks)中，因此您可以以相同的方式列出或取消它。[抖動規則](#jitter)不適用於它，但[七天過期](#seven-day-expiry)適用：迴圈在您啟動它七天後自動結束。

<Note>
  在 Bedrock、Vertex AI 和 Microsoft Foundry 上，沒有間隔的提示會改為在固定的 10 分鐘排程上執行。
</Note>

### 執行內建維護提示

當您省略提示時，Claude 會使用內建維護提示而不是您提供的提示。在每次迭代上，它會按順序進行以下操作：

* 繼續對話中任何未完成的工作
* 照顧目前分支的拉取請求：審查評論、失敗的 CI 執行、合併衝突
* 執行清理通過，例如當沒有其他待處理項目時的錯誤搜尋或簡化

Claude 不會在該範圍之外啟動新的計畫，不可逆的操作（例如推送或刪除）只在它們繼續文字記錄已授權的內容時進行。

```text theme={null}
/loop
```

裸 `/loop` 在[動態選擇的間隔](#let-claude-choose-the-interval)上執行此提示。新增間隔（例如 `/loop 15m`）以改為在固定排程上執行它。若要用您自己的預設值替換內建提示，請參閱[使用 loop.md 自訂預設提示](#customize-the-default-prompt-with-loop-md)。

<Note>
  在 Bedrock、Vertex AI 和 Microsoft Foundry 上，沒有提示的 `/loop` 會列印使用訊息，而不是啟動維護迴圈。
</Note>

### 使用 loop.md 自訂預設提示

`loop.md` 檔案用您自己的指示替換內建維護提示。它為裸 `/loop` 定義單一預設提示，而不是單獨排程任務的清單，並且每當您在命令行上提供提示時都會被忽略。若要在其旁邊排程其他提示，請使用 `/loop <prompt>` 或[直接要求 Claude](#manage-scheduled-tasks)。

Claude 在兩個位置尋找檔案，並使用它找到的第一個。

| 路徑                  | 範圍                   |
| :------------------ | :------------------- |
| `.claude/loop.md`   | 專案層級。當兩個檔案都存在時優先。    |
| `~/.claude/loop.md` | 使用者層級。適用於任何未定義自己的專案。 |

該檔案是純 Markdown，沒有必需的結構。將其寫成您直接輸入 `/loop` 提示的方式。以下範例保持發行分支健康：

```markdown title=".claude/loop.md" theme={null}
Check the `release/next` PR. If CI is red, pull the failing job log,
diagnose, and push a minimal fix. If new review comments have arrived,
address each one and resolve the thread. If everything is green and
quiet, say so in one line.
```

對 `loop.md` 的編輯在下次迭代時生效，因此您可以在迴圈執行時精煉指示。當任一位置都不存在 `loop.md` 時，迴圈會回退到內建維護提示。保持檔案簡潔：超過 25,000 位元組的內容會被截斷。

## 設定一次性提醒

對於一次性提醒，請用自然語言描述您想要的內容，而不是使用 `/loop`。Claude 會排程一個執行後自動刪除的單次執行任務。

```text theme={null}
remind me at 3pm to push the release branch
```

```text theme={null}
in 45 minutes, check whether the integration tests passed
```

Claude 會使用 cron 表達式將執行時間固定到特定的分鐘和小時，並確認何時執行。

## 管理排程任務

用自然語言要求 Claude 列出或取消任務，或直接參考基礎工具。

```text theme={null}
what scheduled tasks do I have?
```

```text theme={null}
cancel the deploy check job
```

在幕後，Claude 使用這些工具：

| 工具           | 用途                                         |
| :----------- | :----------------------------------------- |
| `CronCreate` | 排程新任務。接受 5 欄位 cron 表達式、要執行的提示，以及是否重複或執行一次。 |
| `CronList`   | 列出所有排程任務及其 ID、排程和提示。                       |
| `CronDelete` | 按 ID 取消任務。                                 |

每個排程任務都有一個 8 字元的 ID，您可以傳遞給 `CronDelete`。一個工作階段最多可以同時保存 50 個排程任務。

## 排程任務如何執行

排程器每秒檢查一次到期的任務，並以低優先級將其加入佇列。排程的提示在您的回合之間執行，而不是在 Claude 正在回應時執行。如果 Claude 在任務到期時忙碌，提示會等到目前回合結束。

所有時間都以您的本地時區解釋。cron 表達式（例如 `0 9 * * *`）表示您執行 Claude Code 的任何地方的上午 9 點，而不是 UTC。

### 抖動

為了避免每個工作階段在同一牆上時刻點擊 API，排程器會為執行時間添加一個小的確定性偏移：

* 重複執行的任務最多晚執行其週期的 10%，上限為 15 分鐘。每小時的工作可能在 `:00` 到 `:06` 之間的任何時間執行。
* 為整點或半點排程的一次性任務最多提前執行 90 秒。

偏移是從任務 ID 衍生的，所以相同的任務總是獲得相同的偏移。如果精確計時很重要，請選擇不是 `:00` 或 `:30` 的分鐘，例如 `3 9 * * *` 而不是 `0 9 * * *`，一次性抖動將不適用。

### 七天過期

重複執行的任務在建立後 7 天自動過期。任務最後執行一次，然後刪除自己。這限制了被遺忘的迴圈可以執行多長時間。如果您需要重複執行的任務持續更長時間，請在過期前取消並重新建立它，或使用 [Routines](/zh-TW/routines) 或 [Desktop 排程任務](/zh-TW/desktop-scheduled-tasks) 進行持久排程。

## Cron 表達式參考

`CronCreate` 接受標準 5 欄位 cron 表達式：`minute hour day-of-month month day-of-week`。所有欄位都支援萬用字元 (`*`)、單一值 (`5`)、步驟 (`*/15`)、範圍 (`1-5`) 和逗號分隔的清單 (`1,15,30`)。

| 範例             | 含義                    |
| :------------- | :-------------------- |
| `*/5 * * * *`  | 每 5 分鐘                |
| `0 * * * *`    | 每小時整點                 |
| `7 * * * *`    | 每小時的第 7 分鐘            |
| `0 9 * * *`    | 每天上午 9 點（本地時間）        |
| `0 9 * * 1-5`  | 工作日上午 9 點（本地時間）       |
| `30 14 15 3 *` | 3 月 15 日下午 2:30（本地時間） |

星期幾使用 `0` 或 `7` 表示星期日，`6` 表示星期六。不支援擴展語法，例如 `L`、`W`、`?` 和名稱別名，例如 `MON` 或 `JAN`。

當月份日期和星期幾都受到限制時，如果任一欄位匹配，日期就匹配。這遵循標準 vixie-cron 語義。

## 停用排程任務

在您的環境中設定 `CLAUDE_CODE_DISABLE_CRON=1` 以完全停用排程器。cron 工具和 `/loop` 變得不可用，任何已排程的任務都停止執行。請參閱 [環境變數](/zh-TW/env-vars) 以取得完整的停用標誌清單。

## 限制

工作階段範圍的排程有固有的限制：

* 任務只在 Claude Code 執行且閒置時執行。關閉終端或讓工作階段退出會取消所有內容。
* 沒有錯過執行的追趕。如果任務的排程時間在 Claude 忙於長時間執行的請求時經過，它會在 Claude 變為閒置時執行一次，而不是每個錯過的間隔執行一次。
* 沒有跨重新啟動的持久性。重新啟動 Claude Code 會清除所有工作階段範圍的任務。

對於需要無人值守執行的 cron 驅動自動化：

* [Routines](/zh-TW/routines)：在 Anthropic 管理的基礎設施上按排程執行、透過 API 呼叫或在 GitHub 事件上執行
* [GitHub Actions](/zh-TW/github-actions)：在 CI 中使用 `schedule` 觸發器
* [Desktop 排程任務](/zh-TW/desktop-scheduled-tasks)：在您的機器上本地執行
