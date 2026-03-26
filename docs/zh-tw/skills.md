> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用 skills 擴展 Claude

> 在 Claude Code 中建立、管理和分享 skills，以擴展 Claude 的功能。包括自訂命令和捆綁的 skills。

Skills 擴展了 Claude 能做的事情。建立一個 `SKILL.md` 檔案，其中包含說明，Claude 就會將其新增到其工具組中。Claude 在相關時會使用 skills，或者您可以直接使用 `/skill-name` 叫用一個。

<Note>
  對於內建命令（如 `/help` 和 `/compact`），請參閱[內建命令參考](/zh-TW/commands)。

  **自訂命令已合併到 skills 中。** `.claude/commands/deploy.md` 中的檔案和 `.claude/skills/deploy/SKILL.md` 中的 skill 都會建立 `/deploy` 並以相同方式運作。您現有的 `.claude/commands/` 檔案會繼續運作。Skills 新增了可選功能：支援檔案的目錄、[控制您或 Claude 是否叫用它們](#control-who-invokes-a-skill)的 frontmatter，以及 Claude 在相關時自動載入它們的能力。
</Note>

Claude Code skills 遵循 [Agent Skills](https://agentskills.io) 開放標準，該標準適用於多個 AI 工具。Claude Code 使用額外功能擴展了該標準，例如[叫用控制](#control-who-invokes-a-skill)、[subagent 執行](#run-skills-in-a-subagent)和[動態上下文注入](#inject-dynamic-context)。

## 捆綁的 skills

捆綁的 skills 隨 Claude Code 一起提供，在每個工作階段中都可用。與[內建命令](/zh-TW/commands)不同，內建命令直接執行固定邏輯，捆綁的 skills 是基於提示的：它們為 Claude 提供詳細的劇本，並讓它使用其工具來協調工作。這意味著捆綁的 skills 可以生成平行代理、讀取檔案並適應您的程式碼庫。

您叫用捆綁的 skills 的方式與任何其他 skill 相同：輸入 `/` 後跟 skill 名稱。在下表中，`<arg>` 表示必需的引數，`[arg]` 表示可選的引數。

| Skill                       | 目的                                                                                                                                                                                                                                                     |
| :-------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/batch <instruction>`      | 在平行中跨程式碼庫協調大規模變更。研究程式碼庫，將工作分解為 5 到 30 個獨立單位，並呈現計畫。獲得批准後，在隔離的 [git worktree](/zh-TW/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) 中為每個單位生成一個背景代理。每個代理實現其單位、執行測試並開啟拉取請求。需要 git 存放庫。範例：`/batch migrate src/ from Solid to React` |
| `/claude-api`               | 為您的專案語言（Python、TypeScript、Java、Go、Ruby、C# 或 cURL）載入 Claude API 參考資料，以及 Python 和 TypeScript 的 Agent SDK 參考。涵蓋工具使用、串流、批次、結構化輸出和常見陷阱。當您的程式碼匯入 `anthropic`、`@anthropic-ai/sdk` 或 `claude_agent_sdk` 時也會自動啟動                                                |
| `/debug [description]`      | 啟用目前工作階段的偵錯記錄，並透過讀取工作階段偵錯日誌來排查問題。偵錯記錄預設為關閉，除非您使用 `claude --debug` 啟動，因此在工作階段中途執行 `/debug` 會從該點開始捕獲日誌。可選擇描述問題以聚焦分析                                                                                                                                      |
| `/loop [interval] <prompt>` | 在工作階段保持開啟時按間隔重複執行提示。適用於輪詢部署、監督拉取請求或定期重新執行另一個 skill。範例：`/loop 5m check if the deploy finished`。請參閱[按排程執行提示](/zh-TW/scheduled-tasks)                                                                                                                     |
| `/simplify [focus]`         | 檢查您最近變更的檔案以尋找程式碼重用、品質和效率問題，然後修復它們。在平行中生成三個審查代理，彙總其發現並應用修復。傳遞文字以聚焦於特定關注點：`/simplify focus on memory efficiency`                                                                                                                                         |

## 開始使用

### 建立您的第一個 skill

此範例建立一個 skill，教導 Claude 使用視覺圖表和類比來解釋程式碼。由於它使用預設 frontmatter，Claude 可以在您詢問某事如何運作時自動載入它，或者您可以直接使用 `/explain-code` 叫用它。

<Steps>
  <Step title="建立 skill 目錄">
    在您的個人 skills 資料夾中為 skill 建立一個目錄。個人 skills 在您的所有專案中都可用。

    ```bash  theme={null}
    mkdir -p ~/.claude/skills/explain-code
    ```
  </Step>

  <Step title="編寫 SKILL.md">
    每個 skill 都需要一個 `SKILL.md` 檔案，包含兩部分：YAML frontmatter（在 `---` 標記之間），告訴 Claude 何時使用該 skill，以及包含 Claude 在叫用該 skill 時遵循的說明的 markdown 內容。`name` 欄位變成 `/slash-command`，`description` 幫助 Claude 決定何時自動載入它。

    建立 `~/.claude/skills/explain-code/SKILL.md`：

    ```yaml  theme={null}
    ---
    name: explain-code
    description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
    ---

    When explaining code, always include:

    1. **Start with an analogy**: Compare the code to something from everyday life
    2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
    3. **Walk through the code**: Explain step-by-step what happens
    4. **Highlight a gotcha**: What's a common mistake or misconception?

    Keep explanations conversational. For complex concepts, use multiple analogies.
    ```
  </Step>

  <Step title="測試 skill">
    您可以透過兩種方式測試它：

    **讓 Claude 自動叫用它**，詢問與描述相符的內容：

    ```text  theme={null}
    How does this code work?
    ```

    **或直接使用 skill 名稱叫用它**：

    ```text  theme={null}
    /explain-code src/auth/login.ts
    ```

    無論哪種方式，Claude 都應該在其解釋中包含類比和 ASCII 圖表。
  </Step>
</Steps>

### Skills 的位置

您儲存 skill 的位置決定了誰可以使用它：

| 位置 | 路徑                                        | 適用於        |
| :- | :---------------------------------------- | :--------- |
| 企業 | 請參閱[受管設定](/zh-TW/settings#settings-files) | 您組織中的所有使用者 |
| 個人 | `~/.claude/skills/<skill-name>/SKILL.md`  | 您的所有專案     |
| 專案 | `.claude/skills/<skill-name>/SKILL.md`    | 僅此專案       |
| 外掛 | `<plugin>/skills/<skill-name>/SKILL.md`   | 啟用外掛的位置    |

當 skills 在各個層級共享相同名稱時，優先級較高的位置獲勝：企業 > 個人 > 專案。外掛 skills 使用 `plugin-name:skill-name` 命名空間，因此它們不能與其他層級衝突。如果您在 `.claude/commands/` 中有檔案，它們的運作方式相同，但如果 skill 和命令共享相同名稱，skill 優先。

#### 從巢狀目錄自動發現

當您在子目錄中使用檔案時，Claude Code 會自動從巢狀 `.claude/skills/` 目錄發現 skills。例如，如果您正在編輯 `packages/frontend/` 中的檔案，Claude Code 也會在 `packages/frontend/.claude/skills/` 中尋找 skills。這支援 monorepo 設定，其中套件有自己的 skills。

每個 skill 是一個以 `SKILL.md` 作為進入點的目錄：

```text  theme={null}
my-skill/
├── SKILL.md           # 主要說明（必需）
├── template.md        # Claude 要填入的範本
├── examples/
│   └── sample.md      # 顯示預期格式的範例輸出
└── scripts/
    └── validate.sh    # Claude 可以執行的指令碼
```

`SKILL.md` 包含主要說明，是必需的。其他檔案是可選的，讓您建立更強大的 skills：Claude 要填入的範本、顯示預期格式的範例輸出、Claude 可以執行的指令碼或詳細的參考文件。從您的 `SKILL.md` 參考這些檔案，以便 Claude 知道它們包含什麼以及何時載入它們。請參閱[新增支援檔案](#add-supporting-files)以取得更多詳細資訊。

<Note>
  `.claude/commands/` 中的檔案仍然有效，並支援相同的 [frontmatter](#frontmatter-reference)。建議使用 Skills，因為它們支援額外功能，例如支援檔案。
</Note>

#### 來自其他目錄的 skills

在透過 `--add-dir` 新增的目錄中的 `.claude/skills/` 中定義的 skills 會自動載入並由即時變更偵測拾取，因此您可以在工作階段期間編輯它們而無需重新啟動。

<Note>
  來自 `--add-dir` 目錄的 CLAUDE.md 檔案預設不會載入。若要載入它們，請設定 `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`。請參閱[從其他目錄載入](/zh-TW/memory#load-from-additional-directories)。
</Note>

## 設定 skills

Skills 透過 `SKILL.md` 頂部的 YAML frontmatter 和隨後的 markdown 內容進行設定。

### Skills 內容的類型

Skill 檔案可以包含任何說明，但思考您想如何叫用它們有助於指導要包含的內容：

**參考內容**新增 Claude 應用於您目前工作的知識。慣例、模式、風格指南、領域知識。此內容內聯執行，以便 Claude 可以將其與您的對話上下文一起使用。

```yaml  theme={null}
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

**任務內容**為 Claude 提供特定動作的逐步說明，例如部署、提交或程式碼生成。這些通常是您想使用 `/skill-name` 直接叫用的動作，而不是讓 Claude 決定何時執行它們。新增 `disable-model-invocation: true` 以防止 Claude 自動觸發它。

```yaml  theme={null}
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

您的 `SKILL.md` 可以包含任何內容，但思考您想如何叫用該 skill（由您、由 Claude 或兩者）以及您想在哪裡執行它（內聯或在 subagent 中）有助於指導要包含的內容。對於複雜的 skills，您也可以[新增支援檔案](#add-supporting-files)以保持主要 skill 的焦點。

### Frontmatter 參考

除了 markdown 內容外，您可以使用 `SKILL.md` 檔案頂部 `---` 標記之間的 YAML frontmatter 欄位來設定 skill 行為：

```yaml  theme={null}
---
name: my-skill
description: What this skill does
disable-model-invocation: true
allowed-tools: Read, Grep
---

Your skill instructions here...
```

所有欄位都是可選的。建議只使用 `description`，以便 Claude 知道何時使用該 skill。

| 欄位                         | 必需 | 描述                                                                                                                                  |
| :------------------------- | :- | :---------------------------------------------------------------------------------------------------------------------------------- |
| `name`                     | 否  | Skill 的顯示名稱。如果省略，使用目錄名稱。僅限小寫字母、數字和連字號（最多 64 個字元）。                                                                                   |
| `description`              | 建議 | Skill 的功能以及何時使用它。Claude 使用此來決定何時應用該 skill。如果省略，使用 markdown 內容的第一段。                                                                  |
| `argument-hint`            | 否  | 自動完成期間顯示的提示，指示預期的引數。範例：`[issue-number]` 或 `[filename] [format]`。                                                                    |
| `disable-model-invocation` | 否  | 設定為 `true` 以防止 Claude 自動載入此 skill。用於您想使用 `/name` 手動觸發的工作流程。預設值：`false`。                                                             |
| `user-invocable`           | 否  | 設定為 `false` 以從 `/` 功能表中隱藏。用於使用者不應直接叫用的背景知識。預設值：`true`。                                                                              |
| `allowed-tools`            | 否  | 當此 skill 處於作用中時，Claude 可以使用而無需詢問許可的工具。                                                                                              |
| `model`                    | 否  | 當此 skill 處於作用中時要使用的模型。                                                                                                              |
| `effort`                   | 否  | 當此 skill 處於作用中時的[努力級別](/zh-TW/model-config#adjust-effort-level)。覆蓋工作階段努力級別。預設值：繼承自工作階段。選項：`low`、`medium`、`high`、`max`（僅限 Opus 4.6）。 |
| `context`                  | 否  | 設定為 `fork` 以在分叉的 subagent 上下文中執行。                                                                                                   |
| `agent`                    | 否  | 當設定 `context: fork` 時要使用的 subagent 類型。                                                                                              |
| `hooks`                    | 否  | 限定於此 skill 生命週期的 hooks。請參閱 [Skills 和代理中的 Hooks](/zh-TW/hooks#hooks-in-skills-and-agents) 以取得設定格式。                                   |

#### 可用的字串替換

Skills 支援 skill 內容中動態值的字串替換：

| 變數                     | 描述                                                                                                                 |
| :--------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `$ARGUMENTS`           | 叫用 skill 時傳遞的所有引數。如果 `$ARGUMENTS` 不在內容中，引數會附加為 `ARGUMENTS: <value>`。                                               |
| `$ARGUMENTS[N]`        | 透過 0 為基礎的索引存取特定引數，例如 `$ARGUMENTS[0]` 表示第一個引數。                                                                      |
| `$N`                   | `$ARGUMENTS[N]` 的簡寫，例如 `$0` 表示第一個引數或 `$1` 表示第二個引數。                                                                 |
| `${CLAUDE_SESSION_ID}` | 目前的工作階段 ID。適用於記錄、建立工作階段特定檔案或將 skill 輸出與工作階段相關聯。                                                                    |
| `${CLAUDE_SKILL_DIR}`  | 包含 skill 的 `SKILL.md` 檔案的目錄。對於外掛 skills，這是外掛中 skill 的子目錄，而不是外掛根目錄。在 bash 注入命令中使用此來參考與 skill 捆綁的指令碼或檔案，無論目前的工作目錄如何。 |

**使用替換的範例：**

```yaml  theme={null}
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

### 新增支援檔案

Skills 可以在其目錄中包含多個檔案。這使 `SKILL.md` 專注於基本要素，同時讓 Claude 僅在需要時存取詳細的參考資料。大型參考文件、API 規格或範例集合不需要在每次 skill 執行時載入上下文。

```text  theme={null}
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

從 `SKILL.md` 參考支援檔案，以便 Claude 知道每個檔案包含什麼以及何時載入它：

```markdown  theme={null}
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

<Tip>將 `SKILL.md` 保持在 500 行以下。將詳細的參考資料移至單獨的檔案。</Tip>

### 控制誰叫用 skill

預設情況下，您和 Claude 都可以叫用任何 skill。您可以輸入 `/skill-name` 直接叫用它，Claude 可以在與您的對話相關時自動載入它。兩個 frontmatter 欄位讓您限制此：

* **`disable-model-invocation: true`**：只有您可以叫用該 skill。用於具有副作用或您想控制時機的工作流程，例如 `/commit`、`/deploy` 或 `/send-slack-message`。您不希望 Claude 因為您的程式碼看起來準備好就決定部署。

* **`user-invocable: false`**：只有 Claude 可以叫用該 skill。用於不可作為命令操作的背景知識。`legacy-system-context` skill 解釋舊系統如何運作。Claude 在相關時應該知道這一點，但 `/legacy-system-context` 對使用者來說不是有意義的動作。

此範例建立一個只有您可以觸發的部署 skill。`disable-model-invocation: true` 欄位防止 Claude 自動執行它：

```yaml  theme={null}
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

以下是兩個欄位如何影響叫用和上下文載入：

| Frontmatter                      | 您可以叫用 | Claude 可以叫用 | 何時載入上下文                 |
| :------------------------------- | :---- | :---------- | :---------------------- |
| （預設）                             | 是     | 是           | 描述始終在上下文中，叫用時載入完整 skill |
| `disable-model-invocation: true` | 是     | 否           | 描述不在上下文中，您叫用時載入完整 skill |
| `user-invocable: false`          | 否     | 是           | 描述始終在上下文中，叫用時載入完整 skill |

<Note>
  在常規工作階段中，skill 描述會載入上下文，以便 Claude 知道可用的內容，但完整 skill 內容僅在叫用時載入。[預載入 skills 的 Subagents](/zh-TW/sub-agents#preload-skills-into-subagents) 的運作方式不同：完整 skill 內容在啟動時注入。
</Note>

### 限制工具存取

使用 `allowed-tools` 欄位來限制當 skill 處於作用中時 Claude 可以使用的工具。此 skill 建立一個唯讀模式，其中 Claude 可以探索檔案但不能修改它們：

```yaml  theme={null}
---
name: safe-reader
description: Read files without making changes
allowed-tools: Read, Grep, Glob
---
```

### 將引數傳遞給 skills

您和 Claude 都可以在叫用 skill 時傳遞引數。引數可透過 `$ARGUMENTS` 預留位置取得。

此 skill 透過編號修復 GitHub 問題。`$ARGUMENTS` 預留位置會被 skill 名稱後面的任何內容取代：

```yaml  theme={null}
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

當您執行 `/fix-issue 123` 時，Claude 會收到'Fix GitHub issue 123 following our coding standards...'

如果您使用引數叫用 skill，但 skill 不包含 `$ARGUMENTS`，Claude Code 會將 `ARGUMENTS: <your input>` 附加到 skill 內容的末尾，以便 Claude 仍然看到您輸入的內容。

若要按位置存取個別引數，請使用 `$ARGUMENTS[N]` 或較短的 `$N`：

```yaml  theme={null}
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $ARGUMENTS[0] component from $ARGUMENTS[1] to $ARGUMENTS[2].
Preserve all existing behavior and tests.
```

執行 `/migrate-component SearchBar React Vue` 會將 `$ARGUMENTS[0]` 替換為 `SearchBar`、`$ARGUMENTS[1]` 替換為 `React`、`$ARGUMENTS[2]` 替換為 `Vue`。使用 `$N` 簡寫的相同 skill：

```yaml  theme={null}
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

## 進階模式

### 注入動態上下文

`` !`<command>` `` 語法在將 skill 內容傳送給 Claude 之前執行 shell 命令。命令輸出替換預留位置，因此 Claude 會收到實際資料，而不是命令本身。

此 skill 透過使用 GitHub CLI 擷取即時 PR 資料來總結拉取請求。`` !`gh pr diff` `` 和其他命令首先執行，其輸出會插入到提示中：

```yaml  theme={null}
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

當此 skill 執行時：

1. 每個 `` !`<command>` `` 立即執行（在 Claude 看到任何內容之前）
2. 輸出替換 skill 內容中的預留位置
3. Claude 收到具有實際 PR 資料的完全呈現的提示

這是預處理，不是 Claude 執行的內容。Claude 只看到最終結果。

<Tip>
  若要在 skill 中啟用[擴展思考](/zh-TW/common-workflows#use-extended-thinking-thinking-mode)，請在您的 skill 內容中的任何位置包含'ultrathink'一詞。
</Tip>

### 在 subagent 中執行 skills

當您想要 skill 在隔離中執行時，將 `context: fork` 新增到您的 frontmatter。Skill 內容變成驅動 subagent 的提示。它將無法存取您的對話歷史記錄。

<Warning>
  `context: fork` 僅對具有明確說明的 skills 有意義。如果您的 skill 包含'使用這些 API 慣例'之類的指南而沒有任務，subagent 會收到指南但沒有可操作的提示，並返回而沒有有意義的輸出。
</Warning>

Skills 和 [subagents](/zh-TW/sub-agents) 以兩個方向協同運作：

| 方法                         | 系統提示                       | 任務           | 也載入                     |
| :------------------------- | :------------------------- | :----------- | :---------------------- |
| 具有 `context: fork` 的 Skill | 來自代理類型（`Explore`、`Plan` 等） | SKILL.md 內容  | CLAUDE.md               |
| 具有 `skills` 欄位的 Subagent   | Subagent 的 markdown 主體     | Claude 的委派訊息 | 預載入的 skills + CLAUDE.md |

使用 `context: fork`，您在 skill 中編寫任務並選擇代理類型來執行它。對於反向（定義使用 skills 作為參考資料的自訂 subagent），請參閱 [Subagents](/zh-TW/sub-agents#preload-skills-into-subagents)。

#### 範例：使用 Explore 代理的研究 skill

此 skill 在分叉的 Explore 代理中執行研究。Skill 內容變成任務，代理提供針對程式碼庫探索最佳化的唯讀工具：

```yaml  theme={null}
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

當此 skill 執行時：

1. 建立新的隔離上下文
2. Subagent 收到 skill 內容作為其提示（'Research \$ARGUMENTS thoroughly...'）
3. `agent` 欄位決定執行環境（模型、工具和許可）
4. 結果會總結並返回到您的主要對話

`agent` 欄位指定要使用的 subagent 設定。選項包括內建代理（`Explore`、`Plan`、`general-purpose`）或來自 `.claude/agents/` 的任何自訂 subagent。如果省略，使用 `general-purpose`。

### 限制 Claude 的 skill 存取

預設情況下，Claude 可以叫用任何沒有設定 `disable-model-invocation: true` 的 skill。定義 `allowed-tools` 的 Skills 在 skill 處於作用中時授予 Claude 對這些工具的存取權，無需每次使用批准。您的[許可設定](/zh-TW/permissions)仍然管理所有其他工具的基準批准行為。內建命令（如 `/compact` 和 `/init`）無法透過 Skill 工具取得。

控制 Claude 可以叫用哪些 skills 的三種方式：

**透過在 `/permissions` 中拒絕 Skill 工具來停用所有 skills**：

```text  theme={null}
# Add to deny rules:
Skill
```

**使用[許可規則](/zh-TW/permissions)允許或拒絕特定 skills**：

```text  theme={null}
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

許可語法：`Skill(name)` 用於精確匹配，`Skill(name *)` 用於帶有任何引數的前綴匹配。

**透過將 `disable-model-invocation: true` 新增到其 frontmatter 來隱藏個別 skills**。這會從 Claude 的上下文中完全移除該 skill。

<Note>
  `user-invocable` 欄位僅控制功能表可見性，不控制 Skill 工具存取。使用 `disable-model-invocation: true` 來阻止程式化叫用。
</Note>

## 分享 skills

Skills 可以根據您的受眾在不同範圍內分發：

* **專案 skills**：將 `.claude/skills/` 提交到版本控制
* **外掛**：在您的[外掛](/zh-TW/plugins)中建立 `skills/` 目錄
* **受管**：透過[受管設定](/zh-TW/settings#settings-files)部署組織範圍

### 生成視覺輸出

Skills 可以捆綁並執行任何語言的指令碼，為 Claude 提供超越單個提示可能的功能。一個強大的模式是生成視覺輸出：在您的瀏覽器中開啟的互動式 HTML 檔案，用於探索資料、偵錯或建立報告。

此範例建立一個程式碼庫探索器：一個互動式樹狀檢視，您可以在其中展開和摺疊目錄、一目瞭然地查看檔案大小，並按顏色識別檔案類型。

建立 Skill 目錄：

```bash  theme={null}
mkdir -p ~/.claude/skills/codebase-visualizer/scripts
```

建立 `~/.claude/skills/codebase-visualizer/SKILL.md`。描述告訴 Claude 何時啟動此 Skill，說明告訴 Claude 執行捆綁的指令碼：

````yaml  theme={null}
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase. Use when exploring a new repo, understanding project structure, or identifying large files.
allowed-tools: Bash(python *)
---

# Codebase Visualizer

Generate an interactive HTML tree view that shows your project's file structure with collapsible directories.

## Usage

Run the visualization script from your project root:

```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```

This creates `codebase-map.html` in the current directory and opens it in your default browser.

## What the visualization shows

- **Collapsible directories**: Click folders to expand/collapse
- **File sizes**: Displayed next to each file
- **Colors**: Different colors for different file types
- **Directory totals**: Shows aggregate size of each folder
````

建立 `~/.claude/skills/codebase-visualizer/scripts/visualize.py`。此指令碼掃描目錄樹並生成一個自包含的 HTML 檔案，包含：

* 一個**摘要側邊欄**，顯示檔案計數、目錄計數、總大小和檔案類型數量
* 一個**長條圖**，按檔案類型（按大小排名前 8）分解程式碼庫
* 一個**可摺疊樹**，您可以在其中展開和摺疊目錄，具有顏色編碼的檔案類型指示器

該指令碼需要 Python，但僅使用內建程式庫，因此無需安裝套件：

```python expandable theme={null}
#!/usr/bin/env python3
"""Generate an interactive collapsible tree visualization of a codebase."""

import json
import sys
import webbrowser
from pathlib import Path
from collections import Counter

IGNORE = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}

def scan(path: Path, stats: dict) -> dict:
    result = {"name": path.name, "children": [], "size": 0}
    try:
        for item in sorted(path.iterdir()):
            if item.name in IGNORE or item.name.startswith('.'):
                continue
            if item.is_file():
                size = item.stat().st_size
                ext = item.suffix.lower() or '(no ext)'
                result["children"].append({"name": item.name, "size": size, "ext": ext})
                result["size"] += size
                stats["files"] += 1
                stats["extensions"][ext] += 1
                stats["ext_sizes"][ext] += size
            elif item.is_dir():
                stats["dirs"] += 1
                child = scan(item, stats)
                if child["children"]:
                    result["children"].append(child)
                    result["size"] += child["size"]
    except PermissionError:
        pass
    return result

def generate_html(data: dict, stats: dict, output: Path) -> None:
    ext_sizes = stats["ext_sizes"]
    total_size = sum(ext_sizes.values()) or 1
    sorted_exts = sorted(ext_sizes.items(), key=lambda x: -x[1])[:8]
    colors = {
        '.js': '#f7df1e', '.ts': '#3178c6', '.py': '#3776ab', '.go': '#00add8',
        '.rs': '#dea584', '.rb': '#cc342d', '.css': '#264de4', '.html': '#e34c26',
        '.json': '#6b7280', '.md': '#083fa1', '.yaml': '#cb171e', '.yml': '#cb171e',
        '.mdx': '#083fa1', '.tsx': '#3178c6', '.jsx': '#61dafb', '.sh': '#4eaa25',
    }
    lang_bars = "".join(
        f'<div class="bar-row"><span class="bar-label">{ext}</span>'
        f'<div class="bar" style="width:{(size/total_size)*100}%;background:{colors.get(ext,"#6b7280")}"></div>'
        f'<span class="bar-pct">{(size/total_size)*100:.1f}%</span></div>'
        for ext, size in sorted_exts
    )
    def fmt(b):
        if b < 1024: return f"{b} B"
        if b < 1048576: return f"{b/1024:.1f} KB"
        return f"{b/1048576:.1f} MB"

    html = f'''<!DOCTYPE html>
<html><head>
  <meta charset="utf-8"><title>Codebase Explorer</title>
  <style>
    body {{ font: 14px/1.5 system-ui, sans-serif; margin: 0; background: #1a1a2e; color: #eee; }}
    .container {{ display: flex; height: 100vh; }}
    .sidebar {{ width: 280px; background: #252542; padding: 20px; border-right: 1px solid #3d3d5c; overflow-y: auto; flex-shrink: 0; }}
    .main {{ flex: 1; padding: 20px; overflow-y: auto; }}
    h1 {{ margin: 0 0 10px 0; font-size: 18px; }}
    h2 {{ margin: 20px 0 10px 0; font-size: 14px; color: #888; text-transform: uppercase; }}
    .stat {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #3d3d5c; }}
    .stat-value {{ font-weight: bold; }}
    .bar-row {{ display: flex; align-items: center; margin: 6px 0; }}
    .bar-label {{ width: 55px; font-size: 12px; color: #aaa; }}
    .bar {{ height: 18px; border-radius: 3px; }}
    .bar-pct {{ margin-left: 8px; font-size: 12px; color: #666; }}
    .tree {{ list-style: none; padding-left: 20px; }}
    details {{ cursor: pointer; }}
    summary {{ padding: 4px 8px; border-radius: 4px; }}
    summary:hover {{ background: #2d2d44; }}
    .folder {{ color: #ffd700; }}
    .file {{ display: flex; align-items: center; padding: 4px 8px; border-radius: 4px; }}
    .file:hover {{ background: #2d2d44; }}
    .size {{ color: #888; margin-left: auto; font-size: 12px; }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }}
  </style>
</head><body>
  <div class="container">
    <div class="sidebar">
      <h1>📊 Summary</h1>
      <div class="stat"><span>Files</span><span class="stat-value">{stats["files"]:,}</span></div>
      <div class="stat"><span>Directories</span><span class="stat-value">{stats["dirs"]:,}</span></div>
      <div class="stat"><span>Total size</span><span class="stat-value">{fmt(data["size"])}</span></div>
      <div class="stat"><span>File types</span><span class="stat-value">{len(stats["extensions"])}</span></div>
      <h2>By file type</h2>
      {lang_bars}
    </div>
    <div class="main">
      <h1>📁 {data["name"]}</h1>
      <ul class="tree" id="root"></ul>
    </div>
  </div>
  <script>
    const data = {json.dumps(data)};
    const colors = {json.dumps(colors)};
    function fmt(b) {{ if (b < 1024) return b + ' B'; if (b < 1048576) return (b/1024).toFixed(1) + ' KB'; return (b/1048576).toFixed(1) + ' MB'; }}
    function render(node, parent) {{
      if (node.children) {{
        const det = document.createElement('details');
        det.open = parent === document.getElementById('root');
        det.innerHTML = `<summary><span class="folder">📁 ${{node.name}}</span><span class="size">${{fmt(node.size)}}</span></summary>`;
        const ul = document.createElement('ul'); ul.className = 'tree';
        node.children.sort((a,b) => (b.children?1:0)-(a.children?1:0) || a.name.localeCompare(b.name));
        node.children.forEach(c => render(c, ul));
        det.appendChild(ul);
        const li = document.createElement('li'); li.appendChild(det); parent.appendChild(li);
      }} else {{
        const li = document.createElement('li'); li.className = 'file';
        li.innerHTML = `<span class="dot" style="background:${{colors[node.ext]||'#6b7280'}}"></span>${{node.name}}<span class="size">${{fmt(node.size)}}</span>`;
        parent.appendChild(li);
      }}
    }}
    data.children.forEach(c => render(c, document.getElementById('root')));
  </script>
</body></html>'''
    output.write_text(html)

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    stats = {"files": 0, "dirs": 0, "extensions": Counter(), "ext_sizes": Counter()}
    data = scan(target, stats)
    out = Path('codebase-map.html')
    generate_html(data, stats, out)
    print(f'Generated {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')
```

若要測試，在任何專案中開啟 Claude Code 並詢問「Visualize this codebase.」Claude 執行指令碼、生成 `codebase-map.html` 並在您的瀏覽器中開啟它。

此模式適用於任何視覺輸出：相依性圖表、測試涵蓋範圍報告、API 文件或資料庫架構視覺化。捆綁的指令碼完成繁重工作，而 Claude 處理協調。

## 疑難排解

### Skill 未觸發

如果 Claude 在預期時不使用您的 skill：

1. 檢查描述是否包含使用者會自然說出的關鍵字
2. 驗證 skill 是否出現在「What skills are available?」中
3. 嘗試重新表述您的請求以更密切地匹配描述
4. 如果 skill 是使用者可叫用的，請使用 `/skill-name` 直接叫用它

### Skill 觸發過於頻繁

如果 Claude 在您不想要時使用您的 skill：

1. 使描述更具體
2. 如果您只想手動叫用，請新增 `disable-model-invocation: true`

### Claude 看不到我的所有 skills

Skill 描述會載入上下文，以便 Claude 知道可用的內容。如果您有許多 skills，它們可能會超過字元預算。預算在上下文視窗的 2% 處動態縮放，回退為 16,000 個字元。執行 `/context` 以檢查有關排除的 skills 的警告。

若要覆蓋限制，請設定 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 環境變數。

## 相關資源

* **[Subagents](/zh-TW/sub-agents)**：委派任務給專門的代理
* **[外掛](/zh-TW/plugins)**：使用其他擴展功能打包和分發 skills
* **[Hooks](/zh-TW/hooks)**：自動化工具事件周圍的工作流程
* **[記憶](/zh-TW/memory)**：管理 CLAUDE.md 檔案以取得持久上下文
* **[內建命令](/zh-TW/commands)**：內建 `/` 命令的參考
* **[許可](/zh-TW/permissions)**：控制工具和 skill 存取
