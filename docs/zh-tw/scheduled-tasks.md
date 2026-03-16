> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 按排程執行提示

> 使用 /loop 和 cron 排程工具在 Claude Code 工作階段內重複執行提示、輪詢狀態或設定一次性提醒。

<Note>
  排程任務需要 Claude Code v2.1.72 或更新版本。使用 `claude --version` 檢查您的版本。
</Note>

排程任務讓 Claude 按間隔自動重新執行提示。使用它們來輪詢部署、監督 PR、檢查長時間執行的建置，或在工作階段稍後提醒自己執行某些操作。

任務的範圍限於工作階段：它們存在於目前的 Claude Code 程序中，當您退出時就會消失。如需在重新啟動後仍能持續且無需活躍終端工作階段即可執行的持久排程，請參閱 [Desktop 排程任務](/zh-TW/desktop#schedule-recurring-tasks) 或 [GitHub Actions](/zh-TW/github-actions)。

## 使用 /loop 排程重複提示

`/loop` [bundled skill](/zh-TW/skills#bundled-skills) 是排程重複提示的最快方式。傳遞選用的間隔和提示，Claude 會設定在背景執行的 cron 工作，同時工作階段保持開啟。

```text  theme={null}
/loop 5m check if the deployment finished and tell me what happened
```

Claude 解析間隔、將其轉換為 cron 表達式、排程工作，並確認節奏和工作 ID。

### 間隔語法

間隔是選用的。您可以在開頭使用、在結尾使用，或完全省略。

| 形式            | 範例                                    | 解析的間隔      |
| :------------ | :------------------------------------ | :--------- |
| 前置令牌          | `/loop 30m check the build`           | 每 30 分鐘    |
| 尾部 `every` 子句 | `/loop check the build every 2 hours` | 每 2 小時     |
| 無間隔           | `/loop check the build`               | 預設為每 10 分鐘 |

支援的單位為 `s`（秒）、`m`（分鐘）、`h`（小時）和 `d`（天）。秒數會四捨五入到最近的分鐘，因為 cron 的粒度為一分鐘。不能均勻分割其單位的間隔（例如 `7m` 或 `90m`）會四捨五入到最近的整潔間隔，Claude 會告訴您它選擇了什麼。

### 迴圈執行另一個命令

排程提示本身可以是命令或 skill 呼叫。這對於重新執行您已經打包的工作流程很有用。

```text  theme={null}
/loop 20m /review-pr 1234
```

每次工作執行時，Claude 會執行 `/review-pr 1234`，就像您輸入了它一樣。

## 設定一次性提醒

對於一次性提醒，請用自然語言描述您想要的內容，而不是使用 `/loop`。Claude 排程一個執行後自動刪除的單次執行任務。

```text  theme={null}
remind me at 3pm to push the release branch
```

```text  theme={null}
in 45 minutes, check whether the integration tests passed
```

Claude 使用 cron 表達式將執行時間固定到特定的分鐘和小時，並確認何時執行。

## 管理排程任務

用自然語言要求 Claude 列出或取消任務，或直接參考基礎工具。

```text  theme={null}
what scheduled tasks do I have?
```

```text  theme={null}
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

排程器每秒檢查一次到期的任務，並以低優先級將其加入佇列。排程提示在您的回合之間執行，而不是在 Claude 正在回應時執行。如果 Claude 在任務到期時忙碌，提示會等到目前回合結束。

所有時間都以您的本地時區解釋。cron 表達式（例如 `0 9 * * *`）表示您執行 Claude Code 的任何地方的上午 9 點，而不是 UTC。

### 抖動

為了避免每個工作階段在同一牆上時刻點擊 API，排程器會為執行時間添加一個小的確定性偏移：

* 重複任務的執行時間最多晚於其週期的 10%，上限為 15 分鐘。每小時的工作可能在 `:00` 到 `:06` 之間的任何時間執行。
* 為小時頂部或底部排程的一次性任務最多提前 90 秒執行。

偏移是從任務 ID 衍生的，因此相同的任務始終獲得相同的偏移。如果精確時序很重要，請選擇不是 `:00` 或 `:30` 的分鐘，例如 `3 9 * * *` 而不是 `0 9 * * *`，一次性抖動將不適用。

### 三天過期

重複任務在建立後 3 天自動過期。任務最後執行一次，然後刪除自己。這限制了被遺忘的迴圈可以執行多長時間。如果您需要重複任務持續更長時間，請在過期前取消並重新建立它，或使用 [Desktop 排程任務](/zh-TW/desktop#schedule-recurring-tasks) 進行持久排程。

## Cron 表達式參考

`CronCreate` 接受標準 5 欄位 cron 表達式：`minute hour day-of-month month day-of-week`。所有欄位都支援萬用字元 (`*`)、單一值 (`5`)、步驟 (`*/15`)、範圍 (`1-5`) 和逗號分隔清單 (`1,15,30`)。

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

在您的環境中設定 `CLAUDE_CODE_DISABLE_CRON=1` 以完全停用排程器。cron 工具和 `/loop` 變得不可用，任何已排程的任務都停止執行。請參閱 [環境變數](/zh-TW/settings#environment-variables) 以取得完整的停用旗標清單。

## 限制

工作階段範圍的排程有固有的限制：

* 任務只在 Claude Code 執行且閒置時執行。關閉終端或讓工作階段退出會取消所有內容。
* 沒有錯過執行的追趕。如果任務的排程時間在 Claude 忙於長時間執行的請求時經過，它會在 Claude 變為閒置時執行一次，而不是每個錯過的間隔執行一次。
* 重新啟動時沒有持久性。重新啟動 Claude Code 會清除所有工作階段範圍的任務。

對於需要無人值守執行的 cron 驅動自動化，請使用具有 `schedule` 觸發器的 [GitHub Actions 工作流程](/zh-TW/github-actions)，或如果您想要圖形化設定流程，請使用 [Desktop 排程任務](/zh-TW/desktop#schedule-recurring-tasks)。
