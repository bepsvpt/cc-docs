> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 模型配置

> 了解 Claude Code 模型配置，包括模型別名如 `opusplan`

## 可用模型

對於 Claude Code 中的 `model` 設定，您可以配置以下任一項：

* 一個**模型別名**
* 一個**模型名稱**
  * Anthropic API：完整的\*\*[模型名稱](https://platform.claude.com/docs/zh-TW/about-claude/models/overview)\*\*
  * Bedrock：推論設定檔 ARN
  * Foundry：部署名稱
  * Vertex：版本名稱

### 模型別名

模型別名提供了一種便捷的方式來選擇模型設定，無需記住確切的版本號：

| 模型別名             | 行為                                                                                                                                                   |
| ---------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`default`**    | 特殊值，可清除任何模型覆蓋並還原為您帳戶類型的推薦模型。本身不是模型別名                                                                                                                 |
| **`best`**       | 使用最強大的可用模型，目前相當於 `opus`                                                                                                                              |
| **`sonnet`**     | 使用最新的 Sonnet 模型進行日常編碼任務                                                                                                                              |
| **`opus`**       | 使用最新的 Opus 模型進行複雜推理任務                                                                                                                                |
| **`haiku`**      | 使用快速高效的 Haiku 模型進行簡單任務                                                                                                                               |
| **`sonnet[1m]`** | 使用 Sonnet 搭配[100 萬個 token 的 context window](https://platform.claude.com/docs/zh-TW/build-with-claude/context-windows#1m-token-context-window)進行長時間會話 |
| **`opus[1m]`**   | 使用 Opus 搭配[100 萬個 token 的 context window](https://platform.claude.com/docs/zh-TW/build-with-claude/context-windows#1m-token-context-window)進行長時間會話   |
| **`opusplan`**   | 特殊模式，在 Plan Mode 期間使用 `opus`，然後在執行時切換到 `sonnet`                                                                                                      |

在 Anthropic API 上，`opus` 解析為 Opus 4.7，`sonnet` 解析為 Sonnet 4.6。在 Bedrock、Vertex 和 Foundry 上，`opus` 解析為 Opus 4.6，`sonnet` 解析為 Sonnet 4.5；透過明確選擇完整模型名稱或設定 `ANTHROPIC_DEFAULT_OPUS_MODEL` 或 `ANTHROPIC_DEFAULT_SONNET_MODEL`，這些提供者上可以使用更新的模型。

別名指向您提供者的推薦版本，並隨著時間推移而更新。若要固定到特定版本，請使用完整模型名稱（例如 `claude-opus-4-7`）或設定相應的環境變數，如 `ANTHROPIC_DEFAULT_OPUS_MODEL`。

<Note>
  Opus 4.7 需要 Claude Code v2.1.111 或更新版本。執行 `claude update` 以升級。
</Note>

### 設定您的模型

您可以透過多種方式配置模型，按優先順序列出：

1. **在會話期間** - 使用 `/model <alias|name>` 立即切換，或執行 `/model` 不帶任何引數以開啟選擇器。當會話有先前的輸出時，選擇器會要求確認，因為下一個回應會重新讀取完整歷史記錄而不使用快取的 context
2. **在啟動時** - 使用 `claude --model <alias|name>` 啟動
3. **環境變數** - 設定 `ANTHROPIC_MODEL=<alias|name>`
4. **設定** - 在設定檔中使用 `model` 欄位永久配置。

您的 `/model` 選擇會儲存到使用者設定並在重新啟動後保持。自 v2.1.117 起，如果專案的 `.claude/settings.json` 固定了不同的模型，Claude Code 也會將您的選擇寫入 `.claude/settings.local.json`，以便在重新啟動後在該專案中繼續應用。受管設定優先級最高，並在下次啟動時重新應用。

當啟動時的活動模型來自專案或受管設定而非您自己的選擇時，啟動標題會顯示哪個設定檔設定了它。執行 `/model` 以覆蓋目前會話。

使用範例：

```bash theme={null}
# 使用 Opus 啟動
claude --model opus

# 在會話期間切換到 Sonnet
/model sonnet
```

設定檔範例：

```json theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## 限制模型選擇

企業管理員可以在[受管理或政策設定](/zh-TW/settings#settings-files)中使用 `availableModels` 來限制使用者可以選擇的模型。

設定 `availableModels` 後，使用者無法透過 `/model`、`--model` 旗標或 `ANTHROPIC_MODEL` 環境變數切換到清單中沒有的模型。

```json theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### 預設模型行為

模型選擇器中的「預設」選項不受 `availableModels` 影響。它始終保持可用，並代表系統的執行時預設值[基於使用者的訂閱層級](#default-model-setting)。

即使使用 `availableModels: []`，使用者仍然可以使用其層級的預設模型來使用 Claude Code。

### 控制使用者執行的模型

`model` 設定是初始選擇，而非強制執行。它設定會話啟動時哪個模型處於活動狀態，但使用者仍然可以開啟 `/model` 並選擇「預設」，這會解析為其層級的系統預設值，無論 `model` 設定為何。

若要完全控制模型體驗，請結合三個設定：

* **`availableModels`**：限制使用者可以切換到的具名模型
* **`model`**：設定會話啟動時的初始模型選擇
* **`ANTHROPIC_DEFAULT_SONNET_MODEL`** / **`ANTHROPIC_DEFAULT_OPUS_MODEL`** / **`ANTHROPIC_DEFAULT_HAIKU_MODEL`**：控制「預設」選項以及 `sonnet`、`opus` 和 `haiku` 別名解析為什麼

此範例在 Sonnet 4.5 上啟動使用者，將選擇器限制為 Sonnet 和 Haiku，並將「預設」固定為解析為 Sonnet 4.5 而不是最新版本：

```json theme={null}
{
  "model": "claude-sonnet-4-5",
  "availableModels": ["claude-sonnet-4-5", "haiku"],
  "env": {
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5"
  }
}
```

沒有 `env` 區塊，在選擇器中選擇「預設」的使用者會獲得最新的 Sonnet 版本，繞過 `model` 和 `availableModels` 中的版本固定。

### 合併行為

當 `availableModels` 在多個層級設定時，例如使用者設定和專案設定，陣列會被合併並去重。若要強制執行嚴格的允許清單，請在受管理或政策設定中設定 `availableModels`，這具有最高優先順序。

### Mantle 模型 ID

當[Bedrock Mantle 端點](/zh-TW/amazon-bedrock#use-the-mantle-endpoint)啟用時，`availableModels` 中以 `anthropic.` 開頭的項目會作為自訂選項新增到 `/model` 選擇器，並路由到 Mantle 端點。這是對[為第三方部署固定模型](#pin-models-for-third-party-deployments)中描述的僅別名匹配的例外。該設定仍然將選擇器限制為列出的項目，因此請在任何 Mantle ID 旁邊包含標準別名。

## 特殊模型行為

### `default` 模型設定

`default` 的行為取決於您的帳戶類型：

* **Max 和 Team Premium**：預設為 Opus 4.7
* **Pro、Team Standard、Enterprise 和 Anthropic API**：預設為 Sonnet 4.6
* **Bedrock、Vertex 和 Foundry**：預設為 Sonnet 4.5

如果您達到 Opus 的使用閾值，Claude Code 可能會自動回退到 Sonnet。

<Note>
  2026 年 4 月 23 日，Enterprise 隨用隨付和 Anthropic API 使用者的預設模型將變更為 Opus 4.7。若要保持不同的預設值，請設定 `ANTHROPIC_MODEL` 或[伺服器管理設定](/zh-TW/server-managed-settings)中的 `model` 欄位。
</Note>

### `opusplan` 模型設定

`opusplan` 模型別名提供了一種自動化的混合方法：

* **在 Plan Mode 中** - 使用 `opus` 進行複雜推理和架構決策
* **在執行模式中** - 自動切換到 `sonnet` 進行程式碼生成和實現

這為您提供了兩全其美的方案：Opus 優越的推理能力用於計畫，Sonnet 的效率用於執行。

Plan Mode Opus 階段使用標準 200K context window 執行。[擴展 context](#extended-context) 中描述的自動 1M 升級適用於 `opus` 模型設定，不適用於 `opusplan`。

### 調整努力等級

[努力等級](https://platform.claude.com/docs/en/build-with-claude/effort)控制自適應推理，讓模型根據任務複雜性決定是否以及在每一步上思考多少。較低的努力對於直接的任務更快且更便宜，而較高的努力為複雜問題提供更深入的推理。

努力在 Opus 4.7、Opus 4.6 和 Sonnet 4.6 上受支援。可用的等級取決於模型：

| 模型                    | 等級                                  |
| :-------------------- | :---------------------------------- |
| Opus 4.7              | `low`、`medium`、`high`、`xhigh`、`max` |
| Opus 4.6 和 Sonnet 4.6 | `low`、`medium`、`high`、`max`         |

如果您設定活動模型不支援的等級，Claude Code 會回退到您設定的等級處或以下的最高支援等級。例如，`xhigh` 在 Opus 4.6 上執行為 `high`。

自 v2.1.117 起，Opus 4.7 上的預設努力為 `xhigh`，Opus 4.6 和 Sonnet 4.6 上的預設努力為 `high`。

當您首次執行 Opus 4.7 時，Claude Code 會應用 `xhigh`，即使您之前為 Opus 4.6 或 Sonnet 4.6 設定了不同的努力等級。執行 `/effort` 以在切換後選擇不同的等級。

`low`、`medium`、`high` 和 `xhigh` 在會話間持續存在。`max` 提供最深入的推理，對 token 支出沒有限制，並且僅適用於目前會話，除非透過 `CLAUDE_CODE_EFFORT_LEVEL` 環境變數設定。

#### 選擇努力等級

每個等級都在 token 支出和能力之間進行權衡。預設值適合大多數編碼任務；當您想要不同的平衡時進行調整。

| 等級       | 何時使用                                                  |
| :------- | :---------------------------------------------------- |
| `low`    | 保留用於短期、範圍有限、延遲敏感且不是智能敏感的任務                            |
| `medium` | 減少成本敏感工作的 token 使用，可以權衡一些智能                           |
| `high`   | 平衡 token 使用和智能。用作智能敏感工作的最低要求，或相對於 `xhigh` 減少 token 支出 |
| `xhigh`  | 大多數編碼和代理任務的最佳結果。Opus 4.7 上的推薦預設值                      |
| `max`    | 可以改善困難任務的效能，但可能顯示遞減回報，容易過度思考。在廣泛採用前進行測試               |

努力量表按模型進行校準，因此相同的等級名稱在模型之間不代表相同的基礎值。

#### 使用 ultrathink 進行一次性深入推理

在您的提示中的任何地方包含 `ultrathink` 以請求在該輪上進行更深入的推理，而不改變您的會話努力設定。Claude Code 識別該關鍵字並新增一個上下文指令。發送到 API 的努力等級保持不變。其他短語如「think」、「think hard」和「think more」會作為普通提示文本傳遞，不被識別為關鍵字。

#### 設定努力等級

您可以透過以下任何方式改變努力：

* **`/effort`**：執行 `/effort` 不帶引數以開啟互動式滑塊，執行 `/effort` 後跟等級名稱以直接設定，或執行 `/effort auto` 以重設為模型預設值
* **在 `/model` 中**：選擇模型時使用左/右箭頭鍵調整努力滑塊
* **`--effort` 旗標**：在啟動 Claude Code 時傳遞等級名稱以為單一會話設定
* **環境變數**：設定 `CLAUDE_CODE_EFFORT_LEVEL` 為等級名稱或 `auto`
* **設定**：在設定檔中設定 `effortLevel`
* **Skill 和 subagent frontmatter**：在 [skill](/zh-TW/skills#frontmatter-reference) 或 [subagent](/zh-TW/sub-agents#supported-frontmatter-fields) markdown 檔案中設定 `effort` 以在該 skill 或 subagent 執行時覆蓋努力等級

環境變數優先於所有其他方法，然後是您配置的等級，然後是模型預設值。Frontmatter 努力在該 skill 或 subagent 活動時適用，覆蓋會話等級但不覆蓋環境變數。

當選擇支援的模型時，努力滑塊會出現在 `/model` 中。目前的努力等級也會顯示在標誌和微調器旁邊，例如「with low effort」，因此您可以確認哪個設定處於活動狀態，而無需開啟 `/model`。

#### 自適應推理和固定思考預算

自適應推理使思考在每一步上都是可選的，因此 Claude 可以更快地回應常規提示，並為受益於思考的步驟保留更深入的思考。如果您想要 Claude 比目前等級產生的更頻繁或更少地思考，您可以直接在您的提示或 `CLAUDE.md` 中說明；模型在其努力設定範圍內回應該指導。

Opus 4.7 始終使用自適應推理。固定思考預算模式和 `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` 不適用於它。

在 Opus 4.6 和 Sonnet 4.6 上，您可以設定 `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` 以恢復到由 `MAX_THINKING_TOKENS` 控制的先前固定思考預算。請參閱[環境變數](/zh-TW/env-vars)。

### 擴展思考

擴展思考是 Claude 在回應前發出的推理。在支援[自適應推理](#adjust-effort-level)的模型上，努力等級是控制發生多少思考的主要控制項；下面的設定會開啟或關閉思考，並控制其顯示方式。

| 控制項      | 如何設定                                                                                                          |
| :------- | :------------------------------------------------------------------------------------------------------------ |
| 目前會話的切換  | 在 macOS 上按 `Option+T` 或在 Windows 和 Linux 上按 `Alt+T`                                                           |
| 設定全域預設值  | 執行 `/config` 並切換思考模式。儲存為 `~/.claude/settings.json` 中的 `alwaysThinkingEnabled`                                 |
| 無論努力如何禁用 | 設定 [`MAX_THINKING_TOKENS=0`](/zh-TW/env-vars)。其他值僅適用於[固定思考預算](#adaptive-reasoning-and-fixed-thinking-budgets) |

思考輸出預設為摺疊。按 `Ctrl+O` 以切換詳細模式並將推理視為灰色斜體文本。Anthropic API 上的互動式會話預設會收到編輯的思考區塊，因此如果您想要在展開時可用的完整摘要，請在[設定](/zh-TW/settings)中設定 `showThinkingSummaries: true`。您需要為所有生成的思考 token 付費，即使它們被摺疊或編輯。

### 擴展 context

Opus 4.7、Opus 4.6 和 Sonnet 4.6 支援[100 萬個 token 的 context window](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window)，用於具有大型程式碼庫的長時間會話。

可用性因模型和計畫而異。在 Max、Team 和 Enterprise 計畫上，Opus 會自動升級到 1M context，無需額外配置。這適用於 Team Standard 和 Team Premium 席位。

| 計畫                    | Opus 搭配 1M context                                                                          | Sonnet 搭配 1M context                                                                        |
| --------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| Max、Team 和 Enterprise | 包含在訂閱中                                                                                      | 需要[額外使用](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| Pro                   | 需要[額外使用](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) | 需要[額外使用](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| API 和隨用隨付             | 完全存取                                                                                        | 完全存取                                                                                        |

若要完全禁用 1M context，請設定 `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`。這會從模型選擇器中移除 1M 模型變體。請參閱[環境變數](/zh-TW/env-vars)。

1M context window 使用標準模型定價，超過 200K 的 token 無需額外費用。對於訂閱中包含擴展 context 的計畫，使用量仍由您的訂閱涵蓋。對於透過額外使用存取擴展 context 的計畫，token 會計入額外使用。

如果您的帳戶支援 1M context，該選項會出現在最新版本 Claude Code 的模型選擇器（`/model`）中。如果您看不到它，請嘗試重新啟動您的會話。

您也可以將 `[1m]` 後綴與模型別名或完整模型名稱一起使用：

```bash theme={null}
# 使用 opus[1m] 或 sonnet[1m] 別名
/model opus[1m]
/model sonnet[1m]

# 或將 [1m] 附加到完整模型名稱
/model claude-opus-4-7[1m]
```

## 檢查您目前的模型

您可以透過多種方式查看您目前使用的模型：

1. 在[狀態行](/zh-TW/statusline)中（如果已配置）
2. 在 `/status` 中，它也會顯示您的帳戶資訊。

## 新增自訂模型選項

使用 `ANTHROPIC_CUSTOM_MODEL_OPTION` 將單一自訂項目新增到 `/model` 選擇器，而無需取代內建別名。這對於測試 Claude Code 預設不列出的模型 ID 很有用。對於 LLM 閘道部署，當設定 `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` 時，Claude Code 可以從閘道的 `/v1/models` 端點填入選擇器，因此只有在探索被停用或未傳回您想要的模型時，才需要此變數。請參閱 [LLM 閘道模型選擇](/zh-TW/llm-gateway#model-selection)。

此範例設定所有三個變數以使閘道路由的 Opus 部署可選擇：

```bash theme={null}
export ANTHROPIC_CUSTOM_MODEL_OPTION="my-gateway/claude-opus-4-7"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Opus via Gateway"
export ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION="Custom deployment routed through the internal LLM gateway"
```

自訂項目出現在 `/model` 選擇器的底部。`ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` 和 `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` 是可選的。如果省略，模型 ID 會用作名稱，描述預設為 `Custom model (<model-id>)`。

Claude Code 會跳過在 `ANTHROPIC_CUSTOM_MODEL_OPTION` 中設定的模型 ID 的驗證，因此您可以使用您的 API 端點接受的任何字串。

## 環境變數

您可以使用以下環境變數，這些變數必須是完整的**模型名稱**（或您的 API 提供者的等效項），以控制別名對應到的模型名稱。

| 環境變數                             | 描述                                                          |
| -------------------------------- | ----------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | 用於 `opus` 的模型，或在 Plan Mode 活動時用於 `opusplan` 的模型。            |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | 用於 `sonnet` 的模型，或在 Plan Mode 未活動時用於 `opusplan` 的模型。         |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | 用於 `haiku` 的模型，或[背景功能](/zh-TW/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | 用於 [subagents](/zh-TW/sub-agents) 的模型                       |

注意：`ANTHROPIC_SMALL_FAST_MODEL` 已棄用，改用 `ANTHROPIC_DEFAULT_HAIKU_MODEL`。

### 為第三方部署固定模型

透過 [Bedrock](/zh-TW/amazon-bedrock)、[Vertex AI](/zh-TW/google-vertex-ai) 或 [Foundry](/zh-TW/microsoft-foundry) 部署 Claude Code 時，在向使用者推出前固定模型版本。

不固定模型時，Claude Code 使用模型別名（`sonnet`、`opus`、`haiku`），這些別名會解析為最新版本。當 Anthropic 發佈新模型時，帳戶未啟用新版本的使用者會看到通知並回退到該會話的先前版本，而 Foundry 使用者會看到錯誤，因為 Foundry 沒有等效的啟動檢查。

<Warning>
  在初始設定中將所有三個模型環境變數設定為特定版本 ID。固定讓您控制使用者何時移動到新模型。
</Warning>

使用以下環境變數搭配您提供者的版本特定模型 ID：

| 提供者       | 範例                                                                   |
| :-------- | :------------------------------------------------------------------- |
| Bedrock   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'`              |
| Foundry   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'`              |

對 `ANTHROPIC_DEFAULT_SONNET_MODEL` 和 `ANTHROPIC_DEFAULT_HAIKU_MODEL` 應用相同的模式。有關所有提供者的目前和舊版模型 ID，請參閱[模型概述](https://platform.claude.com/docs/en/about-claude/models/overview)。若要將使用者升級到新模型版本，請更新這些環境變數並重新部署。

若要為固定模型啟用[擴展 context](#extended-context)，請將 `[1m]` 附加到 `ANTHROPIC_DEFAULT_OPUS_MODEL` 或 `ANTHROPIC_DEFAULT_SONNET_MODEL` 中的模型 ID：

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7[1m]'
```

`[1m]` 後綴將 1M context window 應用於該別名的所有使用，包括 `opusplan`。Claude Code 在將模型 ID 發送到您的提供者之前會移除該後綴。只有當基礎模型支援 1M context（例如 Opus 4.7 或 Sonnet 4.6）時，才附加 `[1m]`。

<Note>
  使用第三方提供者時，`settings.availableModels` 允許清單仍然適用。篩選會根據模型別名（`opus`、`sonnet`、`haiku`）進行匹配，而不是提供者特定的模型 ID。
</Note>

### 為第三方部署自訂固定模型顯示和能力

當您在第三方提供者上固定模型時，提供者特定的 ID 會按原樣出現在 `/model` 選擇器中，Claude Code 可能無法識別模型支援的功能。您可以使用每個固定模型的伴隨環境變數覆蓋顯示名稱並宣告能力。

這些變數在 Bedrock、Vertex AI 和 Foundry 等第三方提供者上生效。`_NAME` 和 `_DESCRIPTION` 變數在 `ANTHROPIC_BASE_URL` 指向 [LLM gateway](/zh-TW/llm-gateway) 時也會生效。當直接連接到 `api.anthropic.com` 時無效。

| 環境變數                                                  | 描述                                                       |
| ----------------------------------------------------- | -------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME`                   | `/model` 選擇器中固定 Opus 模型的顯示名稱。未設定時預設為模型 ID                |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION`            | `/model` 選擇器中固定 Opus 模型的顯示描述。未設定時預設為 `Custom Opus model` |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` | 固定 Opus 模型支援的能力的逗號分隔清單                                   |

相同的 `_NAME`、`_DESCRIPTION` 和 `_SUPPORTED_CAPABILITIES` 後綴可用於 `ANTHROPIC_DEFAULT_SONNET_MODEL`、`ANTHROPIC_DEFAULT_HAIKU_MODEL` 和 `ANTHROPIC_CUSTOM_MODEL_OPTION`。

Claude Code 透過將模型 ID 與已知模式進行匹配來啟用[努力等級](#adjust-effort-level)和[擴展思考](#extended-thinking)等功能。提供者特定的 ID（例如 Bedrock ARN 或自訂部署名稱）通常不符合這些模式，導致支援的功能被禁用。設定 `_SUPPORTED_CAPABILITIES` 以告訴 Claude Code 模型實際支援的功能：

| 能力值                    | 啟用                                         |
| ---------------------- | ------------------------------------------ |
| `effort`               | [努力等級](#adjust-effort-level)和 `/effort` 命令 |
| `xhigh_effort`         | {/* min-version: 2.1.111 */}`xhigh` 努力等級   |
| `max_effort`           | `max` 努力等級                                 |
| `thinking`             | [擴展思考](#extended-thinking)                 |
| `adaptive_thinking`    | 根據任務複雜性動態分配思考的自適應推理                        |
| `interleaved_thinking` | 工具呼叫之間的思考                                  |

當設定 `_SUPPORTED_CAPABILITIES` 時，列出的能力會為匹配的固定模型啟用，未列出的能力會被禁用。當變數未設定時，Claude Code 會回退到基於模型 ID 的內建檢測。

此範例將 Opus 固定到 Bedrock 自訂模型 ARN，設定友善名稱，並宣告其能力：

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='arn:aws:bedrock:us-east-1:123456789012:custom-model/abc'
export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME='Opus via Bedrock'
export ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION='Opus 4.7 routed through a Bedrock custom endpoint'
export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES='effort,xhigh_effort,max_effort,thinking,adaptive_thinking,interleaved_thinking'
```

### 按版本覆蓋模型 ID

上述家族級環境變數為每個家族別名配置一個模型 ID。如果您需要將同一家族內的多個版本對應到不同的提供者 ID，請改用 `modelOverrides` 設定。

`modelOverrides` 將個別 Anthropic 模型 ID 對應到 Claude Code 發送到您提供者 API 的提供者特定字串。當使用者在 `/model` 選擇器中選擇對應的模型時，Claude Code 會使用您配置的值而不是內建預設值。

這讓企業管理員可以將每個模型版本路由到特定的 Bedrock 推論設定檔 ARN、Vertex AI 版本名稱或 Foundry 部署名稱，以進行治理、成本分配或區域路由。

在您的[設定檔](/zh-TW/settings#settings-files)中設定 `modelOverrides`：

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

鍵必須是[模型概述](https://platform.claude.com/docs/en/about-claude/models/overview)中列出的 Anthropic 模型 ID。對於日期模型 ID，請包含日期後綴，完全如其所示。未知的鍵會被忽略。

覆蓋會取代支援 `/model` 選擇器中每個項目的內建模型 ID。在 Bedrock 上，覆蓋優先於 Claude Code 在啟動時自動發現的任何推論設定檔。您直接透過 `ANTHROPIC_MODEL`、`--model` 或 `ANTHROPIC_DEFAULT_*_MODEL` 環境變數提供的值會按原樣傳遞給提供者，不會由 `modelOverrides` 轉換。

`modelOverrides` 與 `availableModels` 一起運作。允許清單會根據 Anthropic 模型 ID 進行評估，而不是覆蓋值，因此 `availableModels` 中的項目（如 `"opus"`）即使 Opus 版本對應到 ARN 時仍會繼續匹配。

### Prompt caching 配置

Claude Code 自動使用 [prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) 來優化效能並降低成本。您可以全域禁用 prompt caching 或針對特定模型層級禁用：

| 環境變數                            | 描述                                          |
| ------------------------------- | ------------------------------------------- |
| `DISABLE_PROMPT_CACHING`        | 設定為 `1` 以禁用所有模型的 prompt caching（優先於每個模型的設定） |
| `DISABLE_PROMPT_CACHING_HAIKU`  | 設定為 `1` 以僅禁用 Haiku 模型的 prompt caching       |
| `DISABLE_PROMPT_CACHING_SONNET` | 設定為 `1` 以僅禁用 Sonnet 模型的 prompt caching      |
| `DISABLE_PROMPT_CACHING_OPUS`   | 設定為 `1` 以僅禁用 Opus 模型的 prompt caching        |

這些環境變數為您提供對 prompt caching 行為的細粒度控制。全域 `DISABLE_PROMPT_CACHING` 設定優先於模型特定的設定，讓您可以在需要時快速禁用所有快取。每個模型的設定對於選擇性控制很有用，例如在偵錯特定模型或使用可能具有不同快取實現的雲端提供者時。
