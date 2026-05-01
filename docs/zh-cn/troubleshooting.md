> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 故障排除

> 修复 Claude Code 中的高 CPU 或内存使用、挂起、自动压缩抖动和搜索问题，并找到其他问题的正确页面。

本页涵盖 Claude Code 运行后的性能、稳定性和搜索问题。对于其他问题，请从与您遇到的问题相匹配的页面开始：

| 症状                                                                              | 转到                                                                |
| :------------------------------------------------------------------------------ | :---------------------------------------------------------------- |
| `command not found`、安装失败、PATH 问题、`EACCES`、TLS 错误                                | [故障排除安装和登录](/zh-CN/troubleshoot-install)                          |
| 登录循环、OAuth 错误、`403 Forbidden`、"organization disabled"、Bedrock/Vertex/Foundry 凭据 | [故障排除安装和登录](/zh-CN/troubleshoot-install#login-and-authentication) |
| 设置未应用、hooks 未触发、MCP 服务器未加载                                                      | [调试您的配置](/zh-CN/debug-your-config)                                |
| `API Error: 5xx`、`529 Overloaded`、`429`、请求验证错误                                  | [错误参考](/zh-CN/errors)                                             |
| `model not found` 或 `you may not have access to it`                             | [错误参考](/zh-CN/errors#theres-an-issue-with-the-selected-model)     |
| VS Code 扩展未连接或未检测到 Claude                                                       | [VS Code 集成](/zh-CN/vs-code#fix-common-issues)                    |
| JetBrains 插件或 IDE 未检测到                                                          | [JetBrains 集成](/zh-CN/jetbrains#troubleshooting)                  |
| 高 CPU 或内存、响应缓慢、挂起、搜索找不到文件                                                       | [性能和稳定性](#performance-and-stability)下方                            |

如果您不确定哪个适用，请在 Claude Code 内运行 `/doctor` 以自动检查您的安装、设置、MCP 服务器和上下文使用情况。如果 `claude` 根本无法启动，请从您的 shell 运行 `claude doctor`。

## 性能和稳定性

这些部分涵盖与资源使用、响应性和搜索行为相关的问题。

### 高 CPU 或内存使用

Claude Code 设计用于大多数开发环境，但在处理大型代码库时可能消耗大量资源。如果您遇到性能问题：

1. 定期使用 `/compact` 以减少上下文大小
2. 在主要任务之间关闭并重启 Claude Code
3. 考虑将大型构建目录添加到您的 `.gitignore` 文件

如果内存使用在这些步骤后仍然很高，请运行 `/heapdump` 以将 JavaScript 堆快照和内存分解写入 `~/Desktop`。在 Linux 上没有 Desktop 文件夹的情况下，文件被写入您的主目录。

分解显示驻留集大小、JS 堆、数组缓冲区和未计算的本机内存，这有助于识别增长是在 JavaScript 对象还是本机代码中。要检查保留者，请在 Chrome DevTools 中的 Memory → Load 下打开 `.heapsnapshot` 文件。在 [GitHub](https://github.com/anthropics/claude-code/issues) 上报告内存问题时附加两个文件。

### 自动压缩停止并出现抖动错误

如果您看到 `Autocompact is thrashing: the context refilled to the limit...`，自动压缩成功，但文件或工具输出立即多次将上下文窗口重新填充到限制。Claude Code 停止重试以避免在没有取得进展的循环上浪费 API 调用。

要恢复：

1. 要求 Claude 以较小的块读取超大文件，例如特定行范围或函数，而不是整个文件
2. 运行 `/compact`，重点是删除大输出，例如 `/compact keep only the plan and the diff`
3. 将大文件工作移到 [subagent](/zh-CN/sub-agents)，以便它在单独的上下文窗口中运行
4. 如果早期对话不再需要，运行 `/clear`

### 命令挂起或冻结

如果 Claude Code 似乎无响应：

1. 按 Ctrl+C 尝试取消当前操作
2. 如果无响应，您可能需要关闭终端并重新启动

重新启动不会丢失您的对话。在同一目录中运行 `claude --resume` 以继续会话。

### 搜索和发现问题

如果搜索工具、`@file` 提及、自定义代理或自定义 skills 找不到文件，捆绑的 `ripgrep` 二进制文件可能无法在您的系统上运行。安装您平台的 `ripgrep` 包并告诉 Claude Code 改用它：

<Tabs>
  <Tab title="macOS">
    ```bash theme={null}
    brew install ripgrep
    ```
  </Tab>

  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt install ripgrep
    ```
  </Tab>

  <Tab title="Alpine">
    ```bash theme={null}
    apk add ripgrep
    ```
  </Tab>

  <Tab title="Arch">
    ```bash theme={null}
    pacman -S ripgrep
    ```
  </Tab>

  <Tab title="Windows">
    ```powershell theme={null}
    winget install BurntSushi.ripgrep.MSVC
    ```
  </Tab>
</Tabs>

然后在您的[环境](/zh-CN/env-vars)中设置 `USE_BUILTIN_RIPGREP=0`。

### WSL 上的搜索速度缓慢或结果不完整

在 WSL 上[跨文件系统工作](https://learn.microsoft.com/en-us/windows/wsl/filesystems)时的磁盘读取性能损失可能导致使用 Claude Code 在 WSL 上时搜索匹配数少于预期。搜索仍然有效，但返回的结果少于本机文件系统。

<Note>
  在这种情况下，`/doctor` 将显示搜索为正常。
</Note>

**解决方案：**

1. **提交更具体的搜索**：通过指定目录或文件类型来减少搜索的文件数："在 auth-service 包中搜索 JWT 验证逻辑"或"在 JS 文件中查找 md5 哈希的使用"。

2. **将项目移到 Linux 文件系统**：如果可能，确保您的项目位于 Linux 文件系统（`/home/`）而不是 Windows 文件系统（`/mnt/c/`）。

3. **改用本机 Windows**：考虑在 Windows 上本机运行 Claude Code 而不是通过 WSL，以获得更好的文件系统性能。

## 获取更多帮助

如果您遇到此处未涵盖的问题：

1. 运行 `/doctor` 以检查安装健康状况、设置有效性、MCP 配置和上下文使用情况
2. 在 Claude Code 中使用 `/feedback` 命令直接向 Anthropic 报告问题
3. 检查 [GitHub 存储库](https://github.com/anthropics/claude-code) 以了解已知问题
4. 直接向 Claude 询问其功能和特性。Claude 可以内置访问其文档。
