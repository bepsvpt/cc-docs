> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 自訂鍵盤快捷鍵

> 使用快捷鍵配置檔案在 Claude Code 中自訂鍵盤快捷鍵。

<Note>
  可自訂的鍵盤快捷鍵需要 Claude Code v2.1.18 或更新版本。使用 `claude --version` 檢查您的版本。
</Note>

Claude Code 支援可自訂的鍵盤快捷鍵。執行 `/keybindings` 以在 `~/.claude/keybindings.json` 建立或開啟您的配置檔案。

## 配置檔案

快捷鍵配置檔案是一個包含 `bindings` 陣列的物件。每個區塊指定一個上下文和一個按鍵組合到動作的對應。

<Note>快捷鍵檔案的變更會自動偵測並套用，無需重新啟動 Claude Code。</Note>

| 欄位         | 說明                            |
| :--------- | :---------------------------- |
| `$schema`  | 選用的 JSON Schema URL，用於編輯器自動完成 |
| `$docs`    | 選用的文件 URL                     |
| `bindings` | 按上下文分組的繫結區塊陣列                 |

此範例在聊天上下文中將 `Ctrl+E` 繫結到開啟外部編輯器，並取消繫結 `Ctrl+U`：

```json  theme={null}
{
  "$schema": "https://www.schemastore.org/claude-code-keybindings.json",
  "$docs": "https://code.claude.com/docs/zh-TW/keybindings",
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+e": "chat:externalEditor",
        "ctrl+u": null
      }
    }
  ]
}
```

## 上下文

每個繫結區塊指定一個**上下文**，其中快捷鍵適用：

| 上下文               | 說明                   |
| :---------------- | :------------------- |
| `Global`          | 在應用程式的任何地方適用         |
| `Chat`            | 主聊天輸入區域              |
| `Autocomplete`    | 自動完成選單已開啟            |
| `Settings`        | 設定選單                 |
| `Confirmation`    | 權限和確認對話框             |
| `Tabs`            | 標籤導覽元件               |
| `Help`            | 說明選單可見               |
| `Transcript`      | 文字記錄檢視器              |
| `HistorySearch`   | 歷史記錄搜尋模式 (Ctrl+R)    |
| `Task`            | 背景工作正在執行             |
| `ThemePicker`     | 主題選擇器對話框             |
| `Attachments`     | 影像附件導覽在選擇對話框中        |
| `Footer`          | 頁尾指示器導覽（工作、團隊、差異）    |
| `MessageSelector` | 回溯和摘要對話框訊息選擇         |
| `DiffDialog`      | 差異檢視器導覽              |
| `ModelPicker`     | 模型選擇器努力程度            |
| `Select`          | 通用選擇/清單元件            |
| `Plugin`          | Plugin 對話框（瀏覽、探索、管理） |

## 可用動作

動作遵循 `namespace:action` 格式，例如 `chat:submit` 用於傳送訊息，或 `app:toggleTodos` 用於顯示工作清單。每個上下文都有特定的可用動作。

### 應用程式動作

在 `Global` 上下文中可用的動作：

| 動作                     | 預設值    | 說明             |
| :--------------------- | :----- | :------------- |
| `app:interrupt`        | Ctrl+C | 取消目前操作         |
| `app:exit`             | Ctrl+D | 結束 Claude Code |
| `app:redraw`           | Ctrl+L | 重新繪製螢幕         |
| `app:toggleTodos`      | Ctrl+T | 切換工作清單可見性      |
| `app:toggleTranscript` | Ctrl+O | 切換詳細文字記錄       |

### 歷史記錄動作

用於導覽命令歷史記錄的動作：

| 動作                 | 預設值    | 說明        |
| :----------------- | :----- | :-------- |
| `history:search`   | Ctrl+R | 開啟歷史記錄搜尋  |
| `history:previous` | Up     | 上一個歷史記錄項目 |
| `history:next`     | Down   | 下一個歷史記錄項目 |

### 聊天動作

在 `Chat` 上下文中可用的動作：

| 動作                    | 預設值                       | 說明        |
| :-------------------- | :------------------------ | :-------- |
| `chat:cancel`         | Escape                    | 取消目前輸入    |
| `chat:killAgents`     | Ctrl+X Ctrl+K             | 終止所有背景代理  |
| `chat:cycleMode`      | Shift+Tab\*               | 循環權限模式    |
| `chat:modelPicker`    | Cmd+P / Meta+P            | 開啟模型選擇器   |
| `chat:fastMode`       | Meta+O                    | 切換快速模式    |
| `chat:thinkingToggle` | Cmd+T / Meta+T            | 切換延伸思考    |
| `chat:submit`         | Enter                     | 提交訊息      |
| `chat:newline`        | (未繫結)                     | 插入換行符而不提交 |
| `chat:undo`           | Ctrl+\_, Ctrl+Shift+-     | 復原上一個動作   |
| `chat:externalEditor` | Ctrl+G, Ctrl+X Ctrl+E     | 在外部編輯器中開啟 |
| `chat:stash`          | Ctrl+S                    | 暫存目前提示    |
| `chat:imagePaste`     | Ctrl+V (Windows 上為 Alt+V) | 貼上影像      |

\*在沒有 VT 模式的 Windows 上（Node \<24.2.0/\<22.17.0、Bun \<1.2.23），預設為 Meta+M。

### 自動完成動作

在 `Autocomplete` 上下文中可用的動作：

| 動作                      | 預設值    | 說明    |
| :---------------------- | :----- | :---- |
| `autocomplete:accept`   | Tab    | 接受建議  |
| `autocomplete:dismiss`  | Escape | 關閉選單  |
| `autocomplete:previous` | Up     | 上一個建議 |
| `autocomplete:next`     | Down   | 下一個建議 |

### 確認動作

在 `Confirmation` 上下文中可用的動作：

| 動作                          | 預設值       | 說明     |
| :-------------------------- | :-------- | :----- |
| `confirm:yes`               | Y, Enter  | 確認動作   |
| `confirm:no`                | N, Escape | 拒絕動作   |
| `confirm:previous`          | Up        | 上一個選項  |
| `confirm:next`              | Down      | 下一個選項  |
| `confirm:nextField`         | Tab       | 下一個欄位  |
| `confirm:previousField`     | (未繫結)     | 上一個欄位  |
| `confirm:toggle`            | Space     | 切換選擇   |
| `confirm:cycleMode`         | Shift+Tab | 循環權限模式 |
| `confirm:toggleExplanation` | Ctrl+E    | 切換權限說明 |

### 權限動作

在 `Confirmation` 上下文中可用於權限對話框的動作：

| 動作                       | 預設值    | 說明       |
| :----------------------- | :----- | :------- |
| `permission:toggleDebug` | Ctrl+D | 切換權限偵錯資訊 |

### 文字記錄動作

在 `Transcript` 上下文中可用的動作：

| 動作                         | 預設值               | 說明       |
| :------------------------- | :---------------- | :------- |
| `transcript:toggleShowAll` | Ctrl+E            | 切換顯示所有內容 |
| `transcript:exit`          | q, Ctrl+C, Escape | 結束文字記錄檢視 |

### 歷史記錄搜尋動作

在 `HistorySearch` 上下文中可用的動作：

| 動作                      | 預設值         | 說明      |
| :---------------------- | :---------- | :------ |
| `historySearch:next`    | Ctrl+R      | 下一個符合項目 |
| `historySearch:accept`  | Escape, Tab | 接受選擇    |
| `historySearch:cancel`  | Ctrl+C      | 取消搜尋    |
| `historySearch:execute` | Enter       | 執行選定的命令 |

### 工作動作

在 `Task` 上下文中可用的動作：

| 動作                | 預設值    | 說明       |
| :---------------- | :----- | :------- |
| `task:background` | Ctrl+B | 背景執行目前工作 |

### 主題動作

在 `ThemePicker` 上下文中可用的動作：

| 動作                               | 預設值    | 說明       |
| :------------------------------- | :----- | :------- |
| `theme:toggleSyntaxHighlighting` | Ctrl+T | 切換語法醒目提示 |

### 說明動作

在 `Help` 上下文中可用的動作：

| 動作             | 預設值    | 說明     |
| :------------- | :----- | :----- |
| `help:dismiss` | Escape | 關閉說明選單 |

### 標籤動作

在 `Tabs` 上下文中可用的動作：

| 動作              | 預設值             | 說明    |
| :-------------- | :-------------- | :---- |
| `tabs:next`     | Tab, Right      | 下一個標籤 |
| `tabs:previous` | Shift+Tab, Left | 上一個標籤 |

### 附件動作

在 `Attachments` 上下文中可用的動作：

| 動作                     | 預設值               | 說明      |
| :--------------------- | :---------------- | :------ |
| `attachments:next`     | Right             | 下一個附件   |
| `attachments:previous` | Left              | 上一個附件   |
| `attachments:remove`   | Backspace, Delete | 移除選定的附件 |
| `attachments:exit`     | Down, Escape      | 結束附件導覽  |

### 頁尾動作

在 `Footer` 上下文中可用的動作：

| 動作                      | 預設值    | 說明                |
| :---------------------- | :----- | :---------------- |
| `footer:next`           | Right  | 下一個頁尾項目           |
| `footer:previous`       | Left   | 上一個頁尾項目           |
| `footer:up`             | Up     | 在頁尾中向上導覽（在頂部取消選擇） |
| `footer:down`           | Down   | 在頁尾中向下導覽          |
| `footer:openSelected`   | Enter  | 開啟選定的頁尾項目         |
| `footer:clearSelection` | Escape | 清除頁尾選擇            |

### 訊息選擇器動作

在 `MessageSelector` 上下文中可用的動作：

| 動作                       | 預設值                                       | 說明       |
| :----------------------- | :---------------------------------------- | :------- |
| `messageSelector:up`     | Up, K, Ctrl+P                             | 在清單中向上移動 |
| `messageSelector:down`   | Down, J, Ctrl+N                           | 在清單中向下移動 |
| `messageSelector:top`    | Ctrl+Up, Shift+Up, Meta+Up, Shift+K       | 跳至頂部     |
| `messageSelector:bottom` | Ctrl+Down, Shift+Down, Meta+Down, Shift+J | 跳至底部     |
| `messageSelector:select` | Enter                                     | 選擇訊息     |

### 差異動作

在 `DiffDialog` 上下文中可用的動作：

| 動作                    | 預設值      | 說明        |
| :-------------------- | :------- | :-------- |
| `diff:dismiss`        | Escape   | 關閉差異檢視器   |
| `diff:previousSource` | Left     | 上一個差異來源   |
| `diff:nextSource`     | Right    | 下一個差異來源   |
| `diff:previousFile`   | Up       | 差異中的上一個檔案 |
| `diff:nextFile`       | Down     | 差異中的下一個檔案 |
| `diff:viewDetails`    | Enter    | 檢視差異詳細資訊  |
| `diff:back`           | (特定於上下文) | 在差異檢視器中返回 |

### 模型選擇器動作

在 `ModelPicker` 上下文中可用的動作：

| 動作                           | 預設值   | 說明     |
| :--------------------------- | :---- | :----- |
| `modelPicker:decreaseEffort` | Left  | 降低努力程度 |
| `modelPicker:increaseEffort` | Right | 提高努力程度 |

### 選擇動作

在 `Select` 上下文中可用的動作：

| 動作                | 預設值             | 說明    |
| :---------------- | :-------------- | :---- |
| `select:next`     | Down, J, Ctrl+N | 下一個選項 |
| `select:previous` | Up, K, Ctrl+P   | 上一個選項 |
| `select:accept`   | Enter           | 接受選擇  |
| `select:cancel`   | Escape          | 取消選擇  |

### Plugin 動作

在 `Plugin` 上下文中可用的動作：

| 動作               | 預設值   | 說明            |
| :--------------- | :---- | :------------ |
| `plugin:toggle`  | Space | 切換 plugin 選擇  |
| `plugin:install` | I     | 安裝選定的 plugins |

### 設定動作

在 `Settings` 上下文中可用的動作：

| 動作                | 預設值   | 說明                          |
| :---------------- | :---- | :-------------------------- |
| `settings:search` | /     | 進入搜尋模式                      |
| `settings:retry`  | R     | 重試載入使用量資料（發生錯誤時）            |
| `settings:close`  | Enter | 儲存變更並關閉配置面板。Escape 會捨棄變更並關閉 |

### 語音動作

在啟用[語音聽寫](/zh-TW/voice-dictation)時，在 `Chat` 上下文中可用的動作：

| 動作                 | 預設值   | 說明      |
| :----------------- | :---- | :------ |
| `voice:pushToTalk` | Space | 按住以聽寫提示 |

## 按鍵組合語法

### 修飾鍵

使用 `+` 分隔符搭配修飾鍵：

* `ctrl` 或 `control` - Control 鍵
* `alt`、`opt` 或 `option` - Alt/Option 鍵
* `shift` - Shift 鍵
* `meta`、`cmd` 或 `command` - Meta/Command 鍵

例如：

```text  theme={null}
ctrl+k          單一鍵搭配修飾鍵
shift+tab       Shift + Tab
meta+p          Command/Meta + P
ctrl+shift+c    多個修飾鍵
```

### 大寫字母

獨立的大寫字母表示 Shift。例如，`K` 等同於 `shift+k`。這對於 vim 風格的繫結很有用，其中大寫和小寫鍵有不同的含義。

搭配修飾鍵的大寫字母（例如 `ctrl+K`）被視為風格上的，**不**表示 Shift — `ctrl+K` 與 `ctrl+k` 相同。

### 和弦

和弦是由空格分隔的按鍵組合序列：

```text  theme={null}
ctrl+k ctrl+s   按 Ctrl+K，放開，然後按 Ctrl+S
```

### 特殊鍵

* `escape` 或 `esc` - Escape 鍵
* `enter` 或 `return` - Enter 鍵
* `tab` - Tab 鍵
* `space` - 空格鍵
* `up`、`down`、`left`、`right` - 方向鍵
* `backspace`、`delete` - 刪除鍵

## 取消繫結預設快捷鍵

將動作設定為 `null` 以取消繫結預設快捷鍵：

```json  theme={null}
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+s": null
      }
    }
  ]
}
```

這也適用於和弦繫結。取消繫結共享前綴的每個和弦會釋放該前綴以用作單一鍵繫結：

```json  theme={null}
{
  "bindings": [
    {
      "context": "Chat",
      "bindings": {
        "ctrl+x ctrl+k": null,
        "ctrl+x ctrl+e": null,
        "ctrl+x": "chat:newline"
      }
    }
  ]
}
```

如果您取消繫結前綴上的某些但不是全部和弦，按下前綴仍會進入和弦等待模式以進行剩餘的繫結。

## 保留的快捷鍵

這些快捷鍵無法重新繫結：

| 快捷鍵    | 原因                        |
| :----- | :------------------------ |
| Ctrl+C | 硬編碼的中斷/取消                 |
| Ctrl+D | 硬編碼的結束                    |
| Ctrl+M | 與終端機中的 Enter 相同（兩者都傳送 CR） |

## 終端機衝突

某些快捷鍵可能與終端機多工器衝突：

| 快捷鍵    | 衝突                  |
| :----- | :------------------ |
| Ctrl+B | tmux 前綴（按兩次以傳送）     |
| Ctrl+A | GNU screen 前綴       |
| Ctrl+Z | Unix 程序暫停 (SIGTSTP) |

## Vim 模式互動

啟用 vim 模式時（`/vim`），快捷鍵和 vim 模式獨立運作：

* **Vim 模式**在文字輸入層級處理輸入（游標移動、模式、動作）
* **快捷鍵**在元件層級處理動作（切換待辦事項、提交等）
* vim 模式中的 Escape 鍵從 INSERT 切換到 NORMAL 模式；它不會觸發 `chat:cancel`
* 大多數 Ctrl+鍵快捷鍵通過 vim 模式傳遞到快捷鍵系統
* 在 vim NORMAL 模式中，`?` 顯示說明選單（vim 行為）

## 驗證

Claude Code 驗證您的快捷鍵並顯示以下警告：

* 解析錯誤（無效的 JSON 或結構）
* 無效的上下文名稱
* 保留快捷鍵衝突
* 終端機多工器衝突
* 同一上下文中的重複繫結

執行 `/doctor` 以查看任何快捷鍵警告。
