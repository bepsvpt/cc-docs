> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# トラブルシューティング

> Claude Code のインストールと使用に関する一般的な問題の解決策を見つけます。

## インストール問題のトラブルシューティング

<Tip>
  ターミナルを完全にスキップしたい場合は、[Claude Code デスクトップアプリ](/ja/desktop-quickstart)を使用して、グラフィカルインターフェイスを通じて Claude Code をインストールして使用できます。[macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs)または[Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs)用にダウンロードして、コマンドラインセットアップなしでコーディングを開始できます。
</Tip>

表示されているエラーメッセージまたは症状を見つけてください：

| 表示内容                                                         | 解決策                                                                                               |
| :----------------------------------------------------------- | :------------------------------------------------------------------------------------------------ |
| `command not found: claude` または `'claude' is not recognized` | [PATH を修正する](#command-not-found-claude-after-installation)                                        |
| `syntax error near unexpected token '<'`                     | [インストールスクリプトが HTML を返す](#install-script-returns-html-instead-of-a-shell-script)                   |
| `curl: (56) Failure writing output to destination`           | [スクリプトをダウンロードしてから実行する](#curl-56-failure-writing-output-to-destination)                            |
| Linux でのインストール中に `Killed`                                    | [低メモリサーバーにスワップスペースを追加する](#install-killed-on-low-memory-linux-servers)                             |
| `TLS connect error` または `SSL/TLS secure channel`             | [CA 証明書を更新する](#tls-or-ssl-connection-errors)                                                      |
| `Failed to fetch version` またはダウンロードサーバーに到達できない               | [ネットワークとプロキシ設定を確認する](#check-network-connectivity)                                                 |
| `irm is not recognized` または `&& is not valid`                | [シェルに適切なコマンドを使用する](#windows-irm-or--not-recognized)                                               |
| `Claude Code on Windows requires git-bash`                   | [Git Bash をインストールまたは設定する](#windows-claude-code-on-windows-requires-git-bash)                      |
| `Error loading shared library`                               | [システムに適切なバイナリバリアントをインストールする](#linux-wrong-binary-variant-installed-muslglibc-mismatch)            |
| Linux での `Illegal instruction`                               | [アーキテクチャの不一致](#illegal-instruction-on-linux)                                                      |
| macOS での `dyld: cannot load` または `Abort trap`                | [バイナリの互換性](#dyld-cannot-load-on-macos)                                                            |
| `Invoke-Expression: Missing argument in parameter list`      | [インストールスクリプトが HTML を返す](#install-script-returns-html-instead-of-a-shell-script)                   |
| `App unavailable in region`                                  | Claude Code はお客様の国では利用できません。[サポートされている国](https://www.anthropic.com/supported-countries)を参照してください。 |
| `unable to get local issuer certificate`                     | [企業 CA 証明書を設定する](#tls-or-ssl-connection-errors)                                                   |
| `OAuth error` または `403 Forbidden`                            | [認証を修正する](#authentication-issues)                                                                 |

問題がリストに記載されていない場合は、これらの診断手順を実行してください。

## インストール問題のデバッグ

### ネットワーク接続を確認する

インストーラーは `storage.googleapis.com` からダウンロードします。到達可能であることを確認してください：

```bash  theme={null}
curl -sI https://storage.googleapis.com
```

これが失敗する場合、ネットワークが接続をブロックしている可能性があります。一般的な原因：

* Google Cloud Storage をブロックしている企業ファイアウォールまたはプロキシ
* 地域的なネットワーク制限：VPN または別のネットワークを試してください
* TLS/SSL の問題：システムの CA 証明書を更新するか、`HTTPS_PROXY` が設定されているかどうかを確認してください

企業プロキシの背後にいる場合は、インストール前に `HTTPS_PROXY` と `HTTP_PROXY` をプロキシのアドレスに設定してください。プロキシ URL がわからない場合は IT チームに問い合わせるか、ブラウザのプロキシ設定を確認してください。

この例は両方のプロキシ変数を設定してから、プロキシを通じてインストーラーを実行します：

```bash  theme={null}
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
curl -fsSL https://claude.ai/install.sh | bash
```

### PATH を確認する

インストールが成功したが、`claude` を実行するときに `command not found` または `not recognized` エラーが表示される場合、インストールディレクトリが PATH に含まれていません。シェルは PATH にリストされているディレクトリ内のプログラムを検索し、インストーラーは macOS/Linux では `~/.local/bin/claude` に、Windows では `%USERPROFILE%\.local\bin\claude.exe` に `claude` を配置します。

PATH にインストールディレクトリが含まれているかどうかを確認するには、PATH エントリをリストして `local/bin` でフィルタリングしてください：

<Tabs>
  <Tab title="macOS/Linux">
    ```bash  theme={null}
    echo $PATH | tr ':' '\n' | grep local/bin
    ```

    出力がない場合、ディレクトリが見つかりません。シェル設定に追加してください：

    ```bash  theme={null}
    # Zsh (macOS デフォルト)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc

    # Bash (Linux デフォルト)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```

    または、ターミナルを閉じて再度開いてください。

    修正が機能したことを確認してください：

    ```bash  theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    $env:PATH -split ';' | Select-String 'local\\bin'
    ```

    出力がない場合は、インストールディレクトリをユーザー PATH に追加してください：

    ```powershell  theme={null}
    $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
    [Environment]::SetEnvironmentVariable('PATH', "$currentPath;$env:USERPROFILE\.local\bin", 'User')
    ```

    変更を有効にするためにターミナルを再起動してください。

    修正が機能したことを確認してください：

    ```powershell  theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    echo %PATH% | findstr /i "local\bin"
    ```

    出力がない場合は、システム設定を開き、環境変数に移動して、`%USERPROFILE%\.local\bin` をユーザー PATH 変数に追加してください。ターミナルを再起動してください。

    修正が機能したことを確認してください：

    ```batch  theme={null}
    claude --version
    ```
  </Tab>
</Tabs>

### 競合するインストールを確認する

複数の Claude Code インストールはバージョンの不一致または予期しない動作を引き起こす可能性があります。インストールされているものを確認してください：

<Tabs>
  <Tab title="macOS/Linux">
    PATH に見つかったすべての `claude` バイナリをリストします：

    ```bash  theme={null}
    which -a claude
    ```

    ネイティブインストーラーと npm バージョンが存在するかどうかを確認してください：

    ```bash  theme={null}
    ls -la ~/.local/bin/claude
    ```

    ```bash  theme={null}
    ls -la ~/.claude/local/
    ```

    ```bash  theme={null}
    npm -g ls @anthropic-ai/claude-code 2>/dev/null
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    where.exe claude
    Test-Path "$env:LOCALAPPDATA\Claude Code\claude.exe"
    ```
  </Tab>
</Tabs>

複数のインストールが見つかった場合は、1 つだけを保持してください。`~/.local/bin/claude` でのネイティブインストールが推奨されます。余分なインストールを削除してください：

npm グローバルインストールをアンインストールします：

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

macOS で Homebrew インストールを削除します：

```bash  theme={null}
brew uninstall --cask claude-code
```

### ディレクトリのアクセス許可を確認する

インストーラーは `~/.local/bin/` と `~/.claude/` への書き込みアクセスが必要です。インストールがアクセス許可エラーで失敗する場合は、これらのディレクトリが書き込み可能かどうかを確認してください：

```bash  theme={null}
test -w ~/.local/bin && echo "writable" || echo "not writable"
test -w ~/.claude && echo "writable" || echo "not writable"
```

いずれかのディレクトリが書き込み可能でない場合は、インストールディレクトリを作成し、ユーザーを所有者として設定してください：

```bash  theme={null}
sudo mkdir -p ~/.local/bin
sudo chown -R $(whoami) ~/.local
```

### バイナリが機能することを確認する

`claude` がインストールされているがスタートアップでクラッシュまたはハングする場合は、これらのチェックを実行して原因を絞り込んでください。

バイナリが存在し、実行可能であることを確認してください：

```bash  theme={null}
ls -la $(which claude)
```

Linux では、不足している共有ライブラリを確認してください。`ldd` が不足しているライブラリを表示する場合は、システムパッケージをインストールする必要があるかもしれません。Alpine Linux および他の musl ベースのディストリビューションについては、[Alpine Linux セットアップ](/ja/setup#alpine-linux-and-musl-based-distributions)を参照してください。

```bash  theme={null}
ldd $(which claude) | grep "not found"
```

バイナリが実行できることを確認するための簡単なサニティチェックを実行してください：

```bash  theme={null}
claude --version
```

## 一般的なインストール問題

これらは最も頻繁に発生するインストール問題とその解決策です。

### インストールスクリプトがシェルスクリプトの代わりに HTML を返す

インストールコマンドを実行するときに、次のいずれかのエラーが表示される場合があります：

```text  theme={null}
bash: line 1: syntax error near unexpected token `<'
bash: line 1: `<!DOCTYPE html>'
```

PowerShell では、同じ問題は次のように表示されます：

```text  theme={null}
Invoke-Expression: Missing argument in parameter list.
```

これは、インストール URL がインストールスクリプトの代わりに HTML ページを返したことを意味します。HTML ページに「App unavailable in region」と表示されている場合、Claude Code はお客様の国では利用できません。[サポートされている国](https://www.anthropic.com/supported-countries)を参照してください。

それ以外の場合、これはネットワークの問題、地域的なルーティング、または一時的なサービス中断が原因で発生する可能性があります。

**解決策：**

1. **別のインストール方法を使用する**：

   macOS または Linux では、Homebrew 経由でインストールしてください：

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   Windows では、WinGet 経由でインストールしてください：

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

2. **数分後に再試行する**：この問題は一時的なことが多いです。待ってから元のコマンドを再度試してください。

### インストール後に `command not found: claude`

インストールが完了しましたが、`claude` が機能しません。正確なエラーはプラットフォームによって異なります：

| プラットフォーム    | エラーメッセージ                                                               |
| :---------- | :--------------------------------------------------------------------- |
| macOS       | `zsh: command not found: claude`                                       |
| Linux       | `bash: claude: command not found`                                      |
| Windows CMD | `'claude' is not recognized as an internal or external command`        |
| PowerShell  | `claude : The term 'claude' is not recognized as the name of a cmdlet` |

これは、インストールディレクトリがシェルの検索パスに含まれていないことを意味します。各プラットフォームでの修正については、[PATH を確認する](#verify-your-path)を参照してください。

### `curl: (56) Failure writing output to destination`

`curl ... | bash` コマンドはスクリプトをダウンロードし、パイプ（`|`）を使用して Bash に直接実行するために渡します。このエラーは、スクリプトのダウンロードが完了する前に接続が切断されたことを意味します。一般的な原因には、ネットワーク中断、ダウンロードがストリーム中にブロックされた、またはシステムリソースの制限が含まれます。

**解決策：**

1. **ネットワークの安定性を確認する**：Claude Code バイナリは Google Cloud Storage でホストされています。到達可能であることをテストしてください：
   ```bash  theme={null}
   curl -fsSL https://storage.googleapis.com -o /dev/null
   ```
   コマンドが静かに完了する場合、接続は問題なく、問題は一時的である可能性があります。インストールコマンドを再試行してください。エラーが表示される場合、ネットワークがダウンロードをブロックしている可能性があります。

2. **別のインストール方法を試す**：

   macOS または Linux：

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   Windows：

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

### TLS または SSL 接続エラー

`curl: (35) TLS connect error`、`schannel: next InitializeSecurityContext failed`、または PowerShell の `Could not establish trust relationship for the SSL/TLS secure channel` などのエラーは、TLS ハンドシェイク失敗を示します。

**解決策：**

1. **システム CA 証明書を更新する**：

   Ubuntu/Debian：

   ```bash  theme={null}
   sudo apt-get update && sudo apt-get install ca-certificates
   ```

   macOS（Homebrew 経由）：

   ```bash  theme={null}
   brew install ca-certificates
   ```

2. **Windows では、インストーラーを実行する前に PowerShell で TLS 1.2 を有効にする**：
   ```powershell  theme={null}
   [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
   irm https://claude.ai/install.ps1 | iex
   ```

3. **プロキシまたはファイアウォールの干渉を確認する**：TLS 検査を実行する企業プロキシは、`unable to get local issuer certificate` を含むこれらのエラーを引き起こす可能性があります。`NODE_EXTRA_CA_CERTS` を企業 CA 証明書バンドルに設定してください：
   ```bash  theme={null}
   export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca.pem
   ```
   証明書ファイルがない場合は IT チームに問い合わせてください。直接接続でも試して、プロキシが原因であることを確認できます。

### `Failed to fetch version from storage.googleapis.com`

インストーラーがダウンロードサーバーに到達できませんでした。これは通常、`storage.googleapis.com` がネットワークでブロックされていることを意味します。

**解決策：**

1. **接続を直接テストする**：
   ```bash  theme={null}
   curl -sI https://storage.googleapis.com
   ```

2. **プロキシの背後にいる場合**、`HTTPS_PROXY` を設定して、インストーラーがそれを通じてルーティングできるようにしてください。詳細については、[プロキシ設定](/ja/network-config#proxy-configuration)を参照してください。
   ```bash  theme={null}
   export HTTPS_PROXY=http://proxy.example.com:8080
   curl -fsSL https://claude.ai/install.sh | bash
   ```

3. **制限されたネットワーク上にいる場合**、別のネットワークまたは VPN を試すか、別のインストール方法を使用してください：

   macOS または Linux：

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   Windows：

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

### Windows：`irm` または `&&` が認識されない

`'irm' is not recognized` または `The token '&&' is not valid` が表示される場合、シェルに対して間違ったコマンドを実行しています。

* **`irm` が認識されない**：PowerShell ではなく CMD にいます。2 つのオプションがあります：

  スタートメニューで「PowerShell」を検索して PowerShell を開き、元のインストールコマンドを実行してください：

  ```powershell  theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

  または CMD にとどまり、代わりに CMD インストーラーを使用してください：

  ```batch  theme={null}
  curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
  ```

* **`&&` が有効でない**：PowerShell にいますが、CMD インストーラーコマンドを実行しました。PowerShell インストーラーを使用してください：
  ```powershell  theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

### 低メモリ Linux サーバーでインストールが強制終了される

VPS またはクラウドインスタンスでインストール中に `Killed` が表示される場合：

```text  theme={null}
Setting up Claude Code...
Installing Claude Code native build latest...
bash: line 142: 34803 Killed    "$binary_path" install ${TARGET:+"$TARGET"}
```

Linux OOM キラーがプロセスを終了しました。システムがメモリ不足になったためです。Claude Code には少なくとも 4 GB の利用可能な RAM が必要です。

**解決策：**

1. **サーバーの RAM が限定されている場合、スワップスペースを追加する**。スワップはディスク領域をオーバーフロー メモリとして使用し、物理 RAM が少ない場合でもインストールを完了できます。

   2 GB スワップファイルを作成して有効にしてください：

   ```bash  theme={null}
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

   その後、インストールを再試行してください：

   ```bash  theme={null}
   curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **インストール前に他のプロセスを閉じて**メモリを解放してください。

3. **可能であれば、より大きなインスタンスを使用する**。Claude Code には少なくとも 4 GB の RAM が必要です。

### Docker でインストールがハングする

Docker コンテナに Claude Code をインストールするときに、root として `/` にインストールするとハングが発生する可能性があります。

**解決策：**

1. **インストーラーを実行する前に作業ディレクトリを設定する**。`/` から実行すると、インストーラーはファイルシステム全体をスキャンし、過度なメモリ使用を引き起こします。`WORKDIR` を設定すると、スキャンが小さなディレクトリに制限されます：
   ```dockerfile  theme={null}
   WORKDIR /tmp
   RUN curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **Docker メモリ制限を増やす**（Docker Desktop を使用している場合）：
   ```bash  theme={null}
   docker build --memory=4g .
   ```

### Windows：Claude Desktop が `claude` CLI コマンドをオーバーライドする

古いバージョンの Claude Desktop をインストールした場合、`WindowsApps` ディレクトリに `Claude.exe` を登録して、Claude Code CLI よりも PATH の優先度を高くする可能性があります。`claude` を実行するとデスクトップアプリが開きます。

Claude Desktop を最新バージョンに更新して、この問題を修正してください。

### Windows：「Claude Code on Windows requires git-bash」

ネイティブ Windows の Claude Code には、Git Bash を含む[Git for Windows](https://git-scm.com/downloads/win)が必要です。

**Git がインストールされていない場合**、[git-scm.com/downloads/win](https://git-scm.com/downloads/win)からダウンロードしてインストールしてください。セットアップ中に「Add to PATH」を選択してください。インストール後、ターミナルを再起動してください。

**Git がすでにインストールされている**が、Claude Code がそれを見つけられない場合は、[settings.json ファイル](/ja/settings)でパスを設定してください：

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

Git がどこか別の場所にインストールされている場合は、PowerShell で `where.exe git` を実行してパスを見つけ、そのディレクトリから `bin\bash.exe` パスを使用してください。

### Linux：インストールされた間違ったバイナリバリアント（musl/glibc の不一致）

インストール後に `libstdc++.so.6` または `libgcc_s.so.1` などの不足している共有ライブラリに関するエラーが表示される場合、インストーラーがシステムに対して間違ったバイナリバリアントをダウンロードした可能性があります。

```text  theme={null}
Error loading shared library libstdc++.so.6: No such file or directory
```

これは、musl クロスコンパイルパッケージがインストールされている glibc ベースのシステムで発生する可能性があり、インストーラーがシステムを musl として誤検出します。

**解決策：**

1. **システムが使用している libc を確認する**：
   ```bash  theme={null}
   ldd /bin/ls | head -1
   ```
   `linux-vdso.so` または `/lib/x86_64-linux-gnu/` への参照が表示される場合、glibc を使用しています。`musl` が表示される場合、musl を使用しています。

2. **glibc を使用しているが musl バイナリを取得した場合**、インストールを削除して再インストールしてください。GCS バケット `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json` から正しいバイナリを手動でダウンロードすることもできます。`ldd /bin/ls` と `ls /lib/libc.musl*` の出力を含む[GitHub issue](https://github.com/anthropics/claude-code/issues)を提出してください。

3. **実際に musl を使用している場合**（Alpine Linux）、必要なパッケージをインストールしてください：
   ```bash  theme={null}
   apk add libgcc libstdc++ ripgrep
   ```

### Linux での `Illegal instruction`

インストーラーが OOM `Killed` メッセージの代わりに `Illegal instruction` を出力する場合、ダウンロードされたバイナリが CPU アーキテクチャと一致しません。これは、ARM サーバーが x86 バイナリを受け取った場合、または必要な命令セットがない古い CPU で一般的に発生します。

```text  theme={null}
bash: line 142: 2238232 Illegal instruction    "$binary_path" install ${TARGET:+"$TARGET"}
```

**解決策：**

1. **アーキテクチャを確認する**：
   ```bash  theme={null}
   uname -m
   ```
   `x86_64` は 64 ビット Intel/AMD を意味し、`aarch64` は ARM64 を意味します。バイナリが一致しない場合は、出力を含む[GitHub issue](https://github.com/anthropics/claude-code/issues)を提出してください。

2. **アーキテクチャの問題が解決されている間、別のインストール方法を試す**：
   ```bash  theme={null}
   brew install --cask claude-code
   ```

### macOS での `dyld: cannot load`

インストール中に `dyld: cannot load` または `Abort trap: 6` が表示される場合、バイナリは macOS バージョンまたはハードウェアと互換性がありません。

```text  theme={null}
dyld: cannot load 'claude-2.1.42-darwin-x64' (load command 0x80000034 is unknown)
Abort trap: 6
```

**解決策：**

1. **macOS バージョンを確認する**：Claude Code には macOS 13.0 以降が必要です。Apple メニューを開き、「このマックについて」を選択してバージョンを確認してください。

2. **古いバージョンを使用している場合は macOS を更新する**。バイナリは古い macOS バージョンがサポートしていないロードコマンドを使用しています。

3. **別のインストール方法として Homebrew を試す**：
   ```bash  theme={null}
   brew install --cask claude-code
   ```

### Windows インストール問題：WSL でのエラー

WSL で次の問題が発生する可能性があります：

**OS/プラットフォーム検出の問題**：インストール中にエラーが発生する場合、WSL が Windows `npm` を使用している可能性があります。試してください：

* インストール前に `npm config set os linux` を実行する
* `npm install -g @anthropic-ai/claude-code --force --no-os-check` でインストールする。`sudo` を使用しないでください。

**Node が見つからないエラー**：`claude` を実行するときに `exec: node: not found` が表示される場合、WSL 環境が Windows インストールの Node.js を使用している可能性があります。`which npm` と `which node` で確認できます。これらは `/usr/` で始まる Linux パスではなく `/mnt/c/` を指す必要があります。これを修正するには、Linux ディストリビューションのパッケージマネージャーまたは[`nvm`](https://github.com/nvm-sh/nvm)経由で Node をインストールしてみてください。

**nvm バージョンの競合**：WSL と Windows の両方に nvm がインストールされている場合、WSL で Node バージョンを切り替えるときにバージョンの競合が発生する可能性があります。これは WSL がデフォルトで Windows PATH をインポートするため、WSL インストールよりも Windows nvm/npm が優先されるためです。

この問題は以下で識別できます：

* `which npm` と `which node` を実行する - `/mnt/c/` で始まる Windows パスを指す場合、Windows バージョンが使用されています
* WSL で nvm を使用してノードバージョンを切り替えた後、機能が破損する

この問題を解決するには、Linux PATH を修正して、Linux ノード/npm バージョンが優先されるようにしてください：

**主要な解決策：nvm がシェルに適切にロードされていることを確認する**

最も一般的な原因は、nvm が非対話型シェルにロードされていないことです。シェル設定ファイル（`~/.bashrc`、`~/.zshrc` など）に以下を追加してください：

```bash  theme={null}
# nvm が存在する場合はロードする
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

または現在のセッションで直接実行してください：

```bash  theme={null}
source ~/.nvm/nvm.sh
```

**代替案：PATH の順序を調整する**

nvm が適切にロードされているが、Windows パスが依然として優先される場合、シェル設定で Linux パスを PATH の先頭に明示的に追加できます：

```bash  theme={null}
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

<Warning>
  `appendWindowsPath = false` で Windows PATH インポートを無効にすることは避けてください。これは WSL から Windows 実行可能ファイルを呼び出す機能を破損させます。同様に、Windows 開発に使用する場合は、Windows から Node.js をアンインストールすることは避けてください。
</Warning>

### WSL2 サンドボックスセットアップ

[サンドボックス](/ja/sandboxing)は WSL2 でサポートされていますが、追加のパッケージをインストールする必要があります。`/sandbox` を実行するときに「Sandbox requires socat and bubblewrap」というエラーが表示される場合は、依存関係をインストールしてください：

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash  theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash  theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

WSL1 はサンドボックスをサポートしていません。「Sandboxing requires WSL2」が表示される場合は、WSL2 にアップグレードするか、サンドボックスなしで Claude Code を実行する必要があります。

### インストール中のアクセス許可エラー

ネイティブインストーラーがアクセス許可エラーで失敗する場合、ターゲットディレクトリが書き込み可能でない可能性があります。[ディレクトリのアクセス許可を確認する](#check-directory-permissions)を参照してください。

以前に npm でインストールしており、npm 固有のアクセス許可エラーが発生している場合は、ネイティブインストーラーに切り替えてください：

```bash  theme={null}
curl -fsSL https://claude.ai/install.sh | bash
```

## アクセス許可と認証

これらのセクションでは、ログイン失敗、トークンの問題、およびアクセス許可プロンプトの動作に対処します。

### 繰り返されるアクセス許可プロンプト

同じコマンドを繰り返し承認する必要がある場合は、`/permissions` コマンドを使用して、特定のツールが承認なしで実行されるようにできます。[アクセス許可ドキュメント](/ja/permissions#manage-permissions)を参照してください。

### 認証の問題

認証の問題が発生している場合：

1. `/logout` を実行して完全にサインアウトしてください
2. Claude Code を閉じてください
3. `claude` で再起動して、認証プロセスを再度完了してください

ブラウザがログイン中に自動的に開かない場合は、`c` を押して OAuth URL をクリップボードにコピーしてから、手動でブラウザに貼り付けてください。

### OAuth エラー：無効なコード

`OAuth error: Invalid code. Please make sure the full code was copied` が表示される場合、ログインコードが期限切れになったか、コピー貼り付け中に切り詰められました。

**解決策：**

* ブラウザが開いた後、すぐにログインを完了するために Enter キーを押して再試行してください
* ブラウザが自動的に開かない場合は、`c` を入力して完全な URL をコピーしてください
* リモート/SSH セッションを使用している場合、ブラウザが間違ったマシンで開く可能性があります。ターミナルに表示されている URL をコピーして、ローカルブラウザで開いてください。

### ログイン後の 403 Forbidden

ログイン後に `API Error: 403 {"error":{"type":"forbidden","message":"Request not allowed"}}` が表示される場合：

* **Claude Pro/Max ユーザー**：[claude.ai/settings](https://claude.ai/settings)でサブスクリプションがアクティブであることを確認してください
* **Console ユーザー**：管理者によって「Claude Code」または「Developer」ロールが割り当てられていることを確認してください
* **プロキシの背後**：企業プロキシは API リクエストに干渉する可能性があります。[ネットワーク設定](/ja/network-config)でプロキシセットアップを参照してください。

### WSL2 での OAuth ログイン失敗

WSL2 でのブラウザベースのログインは、WSL が Windows ブラウザを開くことができない場合に失敗する可能性があります。`BROWSER` 環境変数を設定してください：

```bash  theme={null}
export BROWSER="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
claude
```

または、URL を手動でコピーしてください：ログインプロンプトが表示されたら、`c` を押して OAuth URL をコピーしてから、Windows ブラウザに貼り付けてください。

### 「ログインしていません」またはトークンの期限切れ

Claude Code がセッション後に再度ログインするよう求める場合、OAuth トークンが期限切れになった可能性があります。

`/login` を実行して再認証してください。これが頻繁に発生する場合は、システムクロックが正確であることを確認してください。トークン検証は正確なタイムスタンプに依存しています。

## 設定ファイルの場所

Claude Code は複数の場所に設定を保存します：

| ファイル                          | 目的                                                                       |
| :---------------------------- | :----------------------------------------------------------------------- |
| `~/.claude/settings.json`     | ユーザー設定（アクセス許可、hooks、モデルオーバーライド）                                          |
| `.claude/settings.json`       | プロジェクト設定（ソース管理にチェックイン）                                                   |
| `.claude/settings.local.json` | ローカルプロジェクト設定（コミットされない）                                                   |
| `~/.claude.json`              | グローバル状態（テーマ、OAuth、MCP サーバー）                                              |
| `.mcp.json`                   | プロジェクト MCP サーバー（ソース管理にチェックイン）                                            |
| `managed-mcp.json`            | [管理対象 MCP サーバー](/ja/mcp#managed-mcp-configuration)                       |
| 管理対象設定                        | [管理対象設定](/ja/settings#settings-files)（サーバー管理、MDM/OS レベルのポリシー、またはファイルベース） |

Windows では、`~` はユーザーホームディレクトリ（`C:\Users\YourName` など）を指します。

これらのファイルの設定の詳細については、[設定](/ja/settings)と[MCP](/ja/mcp)を参照してください。

### 設定をリセットする

Claude Code をデフォルト設定にリセットするには、設定ファイルを削除できます：

```bash  theme={null}
# すべてのユーザー設定と状態をリセットする
rm ~/.claude.json
rm -rf ~/.claude/

# プロジェクト固有の設定をリセットする
rm -rf .claude/
rm .mcp.json
```

<Warning>
  これにより、すべての設定、MCP サーバー設定、およびセッション履歴が削除されます。
</Warning>

## パフォーマンスと安定性

これらのセクションでは、リソース使用、応答性、および検索動作に関連する問題に対処します。

### CPU またはメモリ使用率が高い

Claude Code はほとんどの開発環境で動作するように設計されていますが、大規模なコードベースを処理するときに大量のリソースを消費する可能性があります。パフォーマンスの問題が発生している場合：

1. `/compact` を定期的に使用してコンテキストサイズを削減してください
2. 主要なタスク間で Claude Code を閉じて再起動してください
3. 大規模なビルドディレクトリを `.gitignore` ファイルに追加することを検討してください

### コマンドがハングまたはフリーズする

Claude Code が応答しないように見える場合：

1. Ctrl+C を押して現在の操作をキャンセルしてください
2. 応答しない場合は、ターミナルを閉じて再起動する必要があるかもしれません

### 検索と発見の問題

Search ツール、`@file` メンション、カスタムエージェント、およびカスタムスキルが機能していない場合は、システム `ripgrep` をインストールしてください：

```bash  theme={null}
# macOS (Homebrew)  
brew install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC

# Ubuntu/Debian
sudo apt install ripgrep

# Alpine Linux
apk add ripgrep

# Arch Linux
pacman -S ripgrep
```

その後、[環境](/ja/settings#environment-variables)で `USE_BUILTIN_RIPGREP=0` を設定してください。

### WSL での遅い、または不完全な検索結果

[WSL でのファイルシステム間での作業](https://learn.microsoft.com/en-us/windows/wsl/filesystems)時のディスク読み取りパフォーマンスペナルティにより、WSL で Claude Code を使用するときに Search ツールを使用して予想より少ないマッチが返される可能性があります。検索は依然として機能しますが、ネイティブファイルシステムよりも少ない結果を返します。

<Note>
  この場合、`/doctor` は Search を OK として表示します。
</Note>

**解決策：**

1. **より具体的な検索を送信する**：検索するファイル数を減らすために、ディレクトリまたはファイルタイプを指定してください：「auth-service パッケージで JWT 検証ロジックを検索する」または「JS ファイルで md5 ハッシュの使用を見つける」。

2. **プロジェクトを Linux ファイルシステムに移動する**：可能であれば、プロジェクトが Windows ファイルシステム（`/mnt/c/`）ではなく Linux ファイルシステム（`/home/`）に配置されていることを確認してください。

3. **ネイティブ Windows を使用する**：WSL ではなく Windows でネイティブに Claude Code を実行することを検討してください。ファイルシステムのパフォーマンスが向上します。

## IDE 統合の問題

Claude Code が IDE に接続しない場合、または IDE ターミナル内で予期しない動作をする場合は、以下の解決策を試してください。

### WSL2 で JetBrains IDE が検出されない

WSL2 で Claude Code を使用していて、JetBrains IDE を使用している場合に「No available IDEs detected」エラーが表示される場合、これは WSL2 のネットワーク設定または Windows ファイアウォールが接続をブロックしている可能性があります。

#### WSL2 ネットワークモード

WSL2 はデフォルトで NAT ネットワークを使用しており、IDE 検出を妨げる可能性があります。2 つのオプションがあります：

**オプション 1：Windows ファイアウォールを設定する**（推奨）

1. WSL2 IP アドレスを見つけてください：
   ```bash  theme={null}
   wsl hostname -I
   # 出力例：172.21.123.45
   ```

2. 管理者として PowerShell を開き、ファイアウォールルールを作成してください：
   ```powershell  theme={null}
   New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
   ```
   ステップ 1 の WSL2 サブネットに基づいて IP 範囲を調整してください。

3. IDE と Claude Code の両方を再起動してください

**オプション 2：ミラーリングネットワークに切り替える**

Windows ユーザーディレクトリの `.wslconfig` に追加してください：

```ini  theme={null}
[wsl2]
networkingMode=mirrored
```

その後、PowerShell から `wsl --shutdown` で WSL を再起動してください。

<Note>
  これらのネットワーク問題は WSL2 にのみ影響します。WSL1 はホストのネットワークを直接使用し、これらの設定は必要ありません。
</Note>

JetBrains の追加設定のヒントについては、[JetBrains IDE ガイド](/ja/jetbrains#plugin-settings)を参照してください。

### Windows IDE 統合の問題を報告する

Windows で IDE 統合の問題が発生している場合は、次の情報を含む[issue を作成](https://github.com/anthropics/claude-code/issues)してください：

* 環境タイプ：ネイティブ Windows（Git Bash）または WSL1/WSL2
* WSL ネットワークモード（該当する場合）：NAT またはミラーリング
* IDE 名とバージョン
* Claude Code 拡張機能/プラグインバージョン
* シェルタイプ：Bash、Zsh、PowerShell など

### JetBrains IDE ターミナルで Escape キーが機能しない

JetBrains ターミナルで Claude Code を使用していて、`Esc` キーがエージェントを中断しない場合、これは JetBrains のデフォルトショートカットとのキーバインディングの競合が原因である可能性があります。

この問題を修正するには：

1. 設定 → ツール → ターミナルに移動してください
2. 次のいずれかを実行してください：
   * 「Move focus to the editor with Escape」をオフにする、または
   * 「Configure terminal keybindings」をクリックして「Switch focus to Editor」ショートカットを削除する
3. 変更を適用してください

これにより、`Esc` キーが Claude Code 操作を適切に中断できるようになります。

## Markdown フォーマットの問題

Claude Code は、生成された Markdown ファイルにコードフェンスの言語タグが不足していることがあり、GitHub、エディター、およびドキュメントツールでの構文強調表示と読みやすさに影響を与える可能性があります。

### コードブロックの言語タグが不足している

生成された Markdown でこのようなコードブロックに気付いた場合：

````markdown  theme={null}
```
function example() {
  return "hello";
}
```text
````

適切にタグ付けされたブロックの代わりに：

````markdown  theme={null}
```javascript
function example() {
  return "hello";
}
```text
````

**解決策：**

1. **Claude に言語タグを追加するよう依頼する**：「Add appropriate language tags to all code blocks in this markdown file.」とリクエストしてください。

2. **後処理 hooks を使用する**：不足している言語タグを検出して追加するための自動フォーマット hooks を設定してください。例については、[編集後のコード自動フォーマット](/ja/hooks-guide#auto-format-code-after-edits)を参照してください。

3. **手動検証**：Markdown ファイルを生成した後、適切なコードブロックフォーマットを確認し、必要に応じて修正をリクエストしてください。

### 一貫性のないスペースとフォーマット

生成された Markdown に過度な空行または一貫性のないスペースがある場合：

**解決策：**

1. **フォーマット修正をリクエストする**：Claude に「Fix spacing and formatting issues in this markdown file.」とリクエストしてください。

2. **フォーマットツールを使用する**：`prettier` またはカスタムフォーマットスクリプトなどの Markdown フォーマッターを実行する hooks を設定してください。

3. **フォーマット設定を指定する**：プロンプトまたはプロジェクト[メモリ](/ja/memory)ファイルにフォーマット要件を含めてください。

### Markdown フォーマットの問題を減らす

フォーマットの問題を最小化するには：

* **リクエストで明示的にする**：「properly formatted markdown with language-tagged code blocks」を求めてください
* **プロジェクト規約を使用する**：[`CLAUDE.md`](/ja/memory)で推奨される Markdown スタイルを文書化してください
* **検証 hooks を設定する**：後処理 hooks を使用して、一般的なフォーマットの問題を自動的に検証および修正してください

## さらにヘルプを得る

ここに記載されていない問題が発生している場合：

1. Claude Code 内で `/bug` コマンドを使用して、Anthropic に直接問題を報告してください
2. [GitHub リポジトリ](https://github.com/anthropics/claude-code)で既知の問題を確認してください
3. `/doctor` を実行して問題を診断してください。以下をチェックします：
   * インストールタイプ、バージョン、および検索機能
   * 自動更新ステータスと利用可能なバージョン
   * 無効な設定ファイル（不正な形式の JSON、不正な型）
   * MCP サーバー設定エラー
   * キーバインディング設定の問題
   * コンテキスト使用警告（大規模な CLAUDE.md ファイル、高い MCP トークン使用、到達不可能なアクセス許可ルール）
   * プラグインとエージェントのロードエラー
4. Claude に直接その機能と特性について質問してください - Claude はドキュメントへの組み込みアクセスを持っています
