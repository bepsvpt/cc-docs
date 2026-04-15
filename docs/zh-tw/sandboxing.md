> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Sandboxing

> 了解 Claude Code 的沙箱化 bash 工具如何提供檔案系統和網路隔離，以實現更安全、更自主的代理執行。

## 概述

Claude Code 具有原生沙箱化功能，為代理執行提供更安全的環境，同時減少對持續權限提示的需求。沙箱化不是要求每個 bash 命令的權限，而是預先建立定義的邊界，讓 Claude Code 能夠以降低風險的方式更自由地工作。

沙箱化 bash 工具使用作業系統級別的原語來強制執行檔案系統和網路隔離。

## 為什麼沙箱化很重要

傳統的基於權限的安全性需要對 bash 命令進行持續的使用者批准。雖然這提供了控制，但可能導致：

* **批准疲勞**：重複點擊「批准」可能導致使用者對他們批准的內容關注度降低
* **生產力降低**：持續的中斷會減慢開發工作流程
* **自主性受限**：當等待批准時，Claude Code 無法高效工作

沙箱化通過以下方式解決這些挑戰：

1. **定義清晰的邊界**：精確指定 Claude Code 可以存取的目錄和網路主機
2. **減少權限提示**：沙箱內的安全命令不需要批准
3. **維持安全性**：嘗試存取沙箱外的資源會觸發立即通知
4. **啟用自主性**：Claude Code 可以在定義的限制內更獨立地運行

<Warning>
  有效的沙箱化需要**同時**進行檔案系統和網路隔離。沒有網路隔離，受損的代理可能會洩露敏感檔案，如 SSH 金鑰。沒有檔案系統隔離，受損的代理可能會後門系統資源以獲得網路存取。配置沙箱化時，重要的是確保您配置的設定不會在這些系統中建立繞過。
</Warning>

## 它如何運作

### 檔案系統隔離

沙箱化 bash 工具將檔案系統存取限制在特定目錄：

* **預設寫入行為**：對目前工作目錄及其子目錄的讀取和寫入存取
* **預設讀取行為**：對整個電腦的讀取存取，除了某些被拒絕的目錄
* **被阻止的存取**：無法在沒有明確權限的情況下修改目前工作目錄外的檔案
* **可配置**：通過設定定義自訂允許和拒絕的路徑

您可以使用設定中的 `sandbox.filesystem.allowWrite` 授予對其他路徑的寫入存取。這些限制在作業系統級別強制執行（macOS 上的 Seatbelt，Linux 上的 bubblewrap），因此它們適用於所有子流程命令，包括 `kubectl`、`terraform` 和 `npm` 等工具，而不僅僅是 Claude 的檔案工具。

### 網路隔離

網路存取通過在沙箱外運行的代理伺服器進行控制：

* **域名限制**：只能存取已批准的域名
* **使用者確認**：新的域名請求會觸發權限提示（除非啟用了 [`allowManagedDomainsOnly`](/zh-TW/settings#sandbox-settings)，它會自動阻止非允許的域名）
* **自訂代理支援**：進階使用者可以在出站流量上實施自訂規則
* **全面覆蓋**：限制適用於所有指令碼、程式和由命令產生的子流程

### 作業系統級別的強制執行

沙箱化 bash 工具利用作業系統安全原語：

* **macOS**：使用 Seatbelt 進行沙箱強制執行
* **Linux**：使用 [bubblewrap](https://github.com/containers/bubblewrap) 進行隔離
* **WSL2**：使用 bubblewrap，與 Linux 相同

不支援 WSL1，因為 bubblewrap 需要僅在 WSL2 中可用的核心功能。

這些作業系統級別的限制確保由 Claude Code 命令產生的所有子流程都繼承相同的安全邊界。

## 入門

### 先決條件

在 **macOS** 上，沙箱化使用內建的 Seatbelt 框架開箱即用。

在 **Linux 和 WSL2** 上，首先安裝所需的套件：

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

### 啟用沙箱化

您可以通過執行 `/sandbox` 命令來啟用沙箱化：

```text theme={null}
/sandbox
```

這會開啟一個選單，您可以在其中選擇沙箱模式。如果缺少所需的依賴項（例如 Linux 上的 `bubblewrap` 或 `socat`），選單會顯示您平台的安裝說明。

預設情況下，如果沙箱無法啟動（缺少依賴項、不支援的平台或平台限制），Claude Code 會顯示警告並在沒有沙箱化的情況下運行命令。要改為將其設為硬失敗，請將 [`sandbox.failIfUnavailable`](/zh-TW/settings#sandbox-settings) 設定為 `true`。這適用於需要沙箱化作為安全閘道的受管部署。

### 沙箱模式

Claude Code 提供兩種沙箱模式：

**自動允許模式**：Bash 命令將嘗試在沙箱內運行，並自動允許而無需權限。無法沙箱化的命令（例如需要存取非允許主機的網路存取的命令）會回退到常規權限流程。您配置的明確詢問/拒絕規則始終被尊重。

**常規權限模式**：所有 bash 命令都通過標準權限流程進行，即使沙箱化也是如此。這提供了更多控制，但需要更多批准。

在兩種模式中，沙箱強制執行相同的檔案系統和網路限制。區別僅在於沙箱化命令是自動批准還是需要明確權限。

<Info>
  自動允許模式獨立於您的權限模式設定工作。即使您不在「接受編輯」模式中，當啟用自動允許時，沙箱化 bash 命令也會自動運行。這意味著在沙箱邊界內修改檔案的 bash 命令將執行而不提示，即使檔案編輯工具通常需要批准。
</Info>

### 配置沙箱化

通過您的 `settings.json` 檔案自訂沙箱行為。有關完整配置參考，請參閱 [Settings](/zh-TW/settings#sandbox-settings)。

#### 授予子流程對特定路徑的寫入存取

預設情況下，沙箱化命令只能寫入目前工作目錄。如果子流程命令（如 `kubectl`、`terraform` 或 `npm`）需要寫入專案目錄外，請使用 `sandbox.filesystem.allowWrite` 授予對特定路徑的存取：

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "allowWrite": ["~/.kube", "/tmp/build"]
    }
  }
}
```

這些路徑在作業系統級別強制執行，因此在沙箱內運行的所有命令（包括其子流程）都尊重它們。當工具需要對特定位置的寫入存取時，這是推薦的方法，而不是使用 `excludedCommands` 將工具排除在沙箱外。

當在多個 [settings scopes](/zh-TW/settings#settings-precedence) 中定義 `allowWrite`（或 `denyWrite`/`denyRead`/`allowRead`）時，陣列被**合併**，這意味著來自每個範圍的路徑被組合，而不是被替換。例如，如果受管設定允許寫入 `/opt/company-tools`，而使用者在其個人設定中新增 `~/.kube`，則兩個路徑都包含在最終沙箱配置中。這意味著使用者和專案可以擴展清單而無需複製或覆蓋由更高優先級範圍設定的路徑。

路徑前綴控制路徑的解析方式：

| 前綴        | 含義                                    | 範例                                                                |
| :-------- | :------------------------------------ | :---------------------------------------------------------------- |
| `/`       | 從檔案系統根目錄的絕對路徑                         | `/tmp/build` 保持 `/tmp/build`                                      |
| `~/`      | 相對於主目錄                                | `~/.kube` 變成 `$HOME/.kube`                                        |
| `./` 或無前綴 | 相對於專案設定的專案根目錄，或相對於 `~/.claude` 的使用者設定 | `.claude/settings.json` 中的 `./output` 解析為 `<project-root>/output` |

較舊的 `//path` 前綴用於絕對路徑仍然有效。如果您之前使用單斜線 `/path` 期望專案相對解析，請切換到 `./path`。此語法與 [Read and Edit](/zh-TW/permissions#read-and-edit) 權限規則不同，後者使用 `//path` 表示絕對路徑，`/path` 表示專案相對路徑。沙箱檔案系統路徑使用標準慣例：`/tmp/build` 是絕對路徑。

您也可以使用 `sandbox.filesystem.denyWrite` 和 `sandbox.filesystem.denyRead` 拒絕寫入或讀取存取。這些與來自 `Edit(...)` 和 `Read(...)` 權限規則的任何路徑合併。要重新允許讀取 `denyRead` 區域內的特定路徑，請使用 `sandbox.filesystem.allowRead`，它優先於 `denyRead`。當在受管設定中啟用 `allowManagedReadPathsOnly` 時，只有受管 `allowRead` 項目被尊重；使用者、專案和本地 `allowRead` 項目被忽略。`denyRead` 仍然從所有來源合併。

例如，要阻止從整個主目錄讀取，同時仍允許從目前專案讀取，請將此新增到您的專案的 `.claude/settings.json`：

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["."]
    }
  }
}
```

`allowRead` 中的 `.` 解析為專案根目錄，因為此配置位於專案設定中。如果您將相同的配置放在 `~/.claude/settings.json` 中，`.` 將解析為 `~/.claude`，專案檔案將保持被 `denyRead` 規則阻止。

<Tip>
  並非所有命令都與沙箱化開箱即用相容。一些可能幫助您充分利用沙箱的注意事項：

  * 許多 CLI 工具需要存取某些主機。當您使用這些工具時，它們將請求權限以存取某些主機。授予權限將允許它們現在和將來存取這些主機，使它們能夠在沙箱內安全執行。
  * `watchman` 與在沙箱中運行不相容。如果您正在執行 `jest`，請考慮使用 `jest --no-watchman`
  * `docker` 與在沙箱中運行不相容。考慮在 `excludedCommands` 中指定 `docker` 以強制其在沙箱外運行。
</Tip>

<Note>
  Claude Code 包含一個有意的逃生艙機制，允許命令在必要時在沙箱外運行。當命令因沙箱限制而失敗時（例如網路連接問題或不相容的工具），Claude 會被提示分析失敗，並可能使用 `dangerouslyDisableSandbox` 參數重試命令。使用此參數的命令通過需要使用者權限執行的常規 Claude Code 權限流程進行。這允許 Claude Code 處理某些工具或網路操作無法在沙箱約束內運作的邊界情況。

  您可以通過在 [sandbox settings](/zh-TW/settings#sandbox-settings) 中設定 `"allowUnsandboxedCommands": false` 來禁用此逃生艙。禁用時，`dangerouslyDisableSandbox` 參數被完全忽略，所有命令必須沙箱化運行或在 `excludedCommands` 中明確列出。
</Note>

## 安全優勢

### 防止提示注入

即使攻擊者通過提示注入成功操縱 Claude Code 的行為，沙箱也確保您的系統保持安全：

**檔案系統保護：**

* 無法修改關鍵配置檔案，如 `~/.bashrc`
* 無法修改 `/bin/` 中的系統級檔案
* 無法讀取在您的 [Claude 權限設定](/zh-TW/permissions#manage-permissions) 中被拒絕的檔案

**網路保護：**

* 無法將資料洩露到攻擊者控制的伺服器
* 無法從未授權的域名下載惡意指令碼
* 無法對未批准的服務進行意外的 API 呼叫
* 無法聯繫任何未明確允許的域名

**監控和控制：**

* 所有在沙箱外的存取嘗試都在作業系統級別被阻止
* 當邊界被測試時，您會收到立即通知
* 您可以選擇拒絕、允許一次或永久更新您的配置

### 減少攻擊面

沙箱化限制了以下可能造成的損害：

* **惡意依賴項**：具有有害程式碼的 NPM 套件或其他依賴項
* **受損指令碼**：具有安全漏洞的構建指令碼或工具
* **社交工程**：欺騙使用者執行危險命令的攻擊
* **提示注入**：欺騙 Claude 執行危險命令的攻擊

### 透明操作

當 Claude Code 嘗試存取沙箱外的網路資源時：

1. 操作在作業系統級別被阻止
2. 您會收到立即通知
3. 您可以選擇：
   * 拒絕請求
   * 允許一次
   * 更新您的沙箱配置以永久允許它

## 安全限制

* 網路沙箱化限制：網路過濾系統通過限制流程允許連接的域名來運作。它不會以其他方式檢查通過代理的流量，使用者負責確保他們在其策略中只允許受信任的域名。

<Warning>
  使用者應該意識到允許廣泛域名（如 `github.com`）可能帶來的潛在風險，這可能允許資料洩露。此外，在某些情況下，可能可以通過 [domain fronting](https://en.wikipedia.org/wiki/Domain_fronting) 繞過網路過濾。
</Warning>

* Unix 套接字特權提升：`allowUnixSockets` 配置可能會無意中授予對強大系統服務的存取，這可能導致沙箱繞過。例如，如果它用於允許存取 `/var/run/docker.sock`，這將有效地通過利用 docker 套接字授予對主機系統的存取。鼓勵使用者仔細考慮他們通過沙箱允許的任何 unix 套接字。
* 檔案系統權限提升：過於寬泛的檔案系統寫入權限可能導致特權提升攻擊。允許寫入包含 `$PATH` 中可執行檔案的目錄、系統配置目錄或使用者 shell 配置檔案（`.bashrc`、`.zshrc`）可能導致當其他使用者或系統流程存取這些檔案時在不同安全上下文中執行程式碼。
* Linux 沙箱強度：Linux 實現提供強大的檔案系統和網路隔離，但包含一個 `enableWeakerNestedSandbox` 模式，使其能夠在 Docker 環境中工作而無需特權命名空間。此選項大大削弱了安全性，應僅在其他隔離被強制執行的情況下使用。

## 沙箱化與權限的關係

沙箱化和 [permissions](/zh-TW/permissions) 是協同工作的互補安全層：

* **權限**控制 Claude Code 可以使用哪些工具，並在任何工具運行之前進行評估。它們適用於所有工具：Bash、Read、Edit、WebFetch、MCP 和其他工具。
* **沙箱化**提供作業系統級別的強制執行，限制 Bash 命令在檔案系統和網路級別可以存取的內容。它僅適用於 Bash 命令及其子流程。

檔案系統和網路限制通過沙箱設定和權限規則進行配置：

* 使用 `sandbox.filesystem.allowWrite` 授予子流程對工作目錄外路徑的寫入存取
* 使用 `sandbox.filesystem.denyWrite` 和 `sandbox.filesystem.denyRead` 阻止子流程對特定路徑的存取
* 使用 `sandbox.filesystem.allowRead` 重新允許讀取 `denyRead` 區域內的特定路徑
* 使用 `Read` 和 `Edit` 拒絕規則阻止對特定檔案或目錄的存取
* 使用 `WebFetch` 允許/拒絕規則控制域名存取
* 使用沙箱 `allowedDomains` 控制 Bash 命令可以到達的域名

來自 `sandbox.filesystem` 設定和權限規則的路徑被合併到最終沙箱配置中。

此 [repository](https://github.com/anthropics/claude-code/tree/main/examples/settings) 包含常見部署場景的入門設定配置，包括沙箱特定的範例。使用這些作為起點，並根據您的需求進行調整。

## 進階用法

### 自訂代理配置

對於需要進階網路安全的組織，您可以實施自訂代理以：

* 解密和檢查 HTTPS 流量
* 應用自訂過濾規則
* 記錄所有網路請求
* 與現有安全基礎設施整合

```json theme={null}
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080,
      "socksProxyPort": 8081
    }
  }
}
```

### 與現有安全工具的整合

沙箱化 bash 工具與以下工具配合使用：

* **權限規則**：與 [permission settings](/zh-TW/permissions) 結合以實現深度防禦
* **開發容器**：與 [devcontainers](/zh-TW/devcontainer) 一起使用以獲得額外隔離
* **企業策略**：通過 [managed settings](/zh-TW/settings#settings-precedence) 強制執行沙箱配置

## 最佳實踐

1. **從限制性開始**：從最小權限開始，根據需要擴展
2. **監控日誌**：檢查沙箱違規嘗試以了解 Claude Code 的需求
3. **使用環境特定配置**：開發與生產環境的不同沙箱規則
4. **與權限結合**：將沙箱化與 IAM 策略一起使用以實現全面安全
5. **測試配置**：驗證您的沙箱設定不會阻止合法工作流程

## 開源

沙箱執行時可作為開源 npm 套件供您在自己的代理專案中使用。這使更廣泛的 AI 代理社群能夠構建更安全、更安全的自主系統。這也可以用於沙箱化您可能希望運行的其他程式。例如，要沙箱化 MCP 伺服器，您可以執行：

```bash theme={null}
npx @anthropic-ai/sandbox-runtime <command-to-sandbox>
```

有關實現詳情和原始程式碼，請訪問 [GitHub repository](https://github.com/anthropic-experimental/sandbox-runtime)。

## 限制

* **效能開銷**：最小，但某些檔案系統操作可能稍慢
* **相容性**：某些需要特定系統存取模式的工具可能需要配置調整，或甚至可能需要在沙箱外運行
* **平台支援**：支援 macOS、Linux 和 WSL2。不支援 WSL1。計劃提供原生 Windows 支援。

## 沙箱化不涵蓋的內容

沙箱隔離 Bash 子流程。其他工具在不同的邊界下運作：

* **內建檔案工具**：Read、Edit 和 Write 直接使用權限系統，而不是通過沙箱運行。請參閱 [permissions](/zh-TW/permissions)。
* **電腦使用**：當 Claude 在 macOS 上打開應用程式並控制您的螢幕時，它在您的實際桌面上運行，而不是在隔離環境中。每個應用程式的權限提示控制每個應用程式。請參閱 [CLI 中的電腦使用](/zh-TW/computer-use) 或 [Desktop 中的電腦使用](/zh-TW/desktop#let-claude-use-your-computer)。

## 另請參閱

* [Security](/zh-TW/security) - 全面的安全功能和最佳實踐
* [Permissions](/zh-TW/permissions) - 權限配置和存取控制
* [Settings](/zh-TW/settings) - 完整配置參考
* [CLI reference](/zh-TW/cli-reference) - 命令列選項
