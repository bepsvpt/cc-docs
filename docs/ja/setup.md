> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 高度なセットアップ

> Claude Code のシステム要件、プラットフォーム固有のインストール、バージョン管理、およびアンインストール。

このページでは、システム要件、プラットフォーム固有のインストール詳細、更新、およびアンインストールについて説明します。初回セッションのガイド付きウォークスルーについては、[クイックスタート](/ja/quickstart)を参照してください。ターミナルを使用したことがない場合は、[ターミナルガイド](/ja/terminal-guide)を参照してください。

## システム要件

Claude Code は以下のプラットフォームと構成で実行されます。

* **オペレーティングシステム**:
  * macOS 13.0 以上
  * Windows 10 1809 以上または Windows Server 2019 以上
  * Ubuntu 20.04 以上
  * Debian 10 以上
  * Alpine Linux 3.19 以上
* **ハードウェア**: 4 GB 以上の RAM
* **ネットワーク**: インターネット接続が必要です。[ネットワーク構成](/ja/network-config#network-access-requirements)を参照してください。
* **シェル**: Bash、Zsh、PowerShell、または CMD。Windows では、[Git for Windows](https://git-scm.com/downloads/win)が必要です。
* **場所**: [Anthropic サポート対象国](https://www.anthropic.com/supported-countries)

### 追加の依存関係

* **ripgrep**: 通常は Claude Code に含まれています。検索が失敗する場合は、[検索トラブルシューティング](/ja/troubleshooting#search-and-discovery-issues)を参照してください。

## Claude Code をインストール

<Tip>
  グラフィカルインターフェースをお好みですか？[Desktop app](/ja/desktop-quickstart)を使用すると、ターミナルなしで Claude Code を使用できます。[macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs)または[Windows](https://claude.com/download?utm_source=claude_code\&utm_medium=docs)でダウンロードしてください。

  ターミナルは初めてですか？[ターミナルガイド](/ja/terminal-guide)で段階的な手順を参照してください。
</Tip>

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. Use the PowerShell command above instead. Your prompt shows `PS C:\` when you're in PowerShell.

    **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash  theme={null}
    brew install --cask claude-code
    ```

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell  theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

インストールが完了したら、作業するプロジェクトでターミナルを開き、Claude Code を起動します。

```bash  theme={null}
claude
```

インストール中に問題が発生した場合は、[トラブルシューティングガイド](/ja/troubleshooting)を参照してください。

### Windows でのセットアップ

Windows 上の Claude Code には、[Git for Windows](https://git-scm.com/downloads/win)または WSL が必要です。PowerShell、CMD、または Git Bash から `claude` を起動できます。Claude Code は内部的に Git Bash を使用してコマンドを実行します。PowerShell を管理者として実行する必要はありません。

**オプション 1: Git Bash を使用したネイティブ Windows**

[Git for Windows](https://git-scm.com/downloads/win)をインストールしてから、PowerShell または CMD からインストールコマンドを実行します。

Claude Code が Git Bash インストールを見つけられない場合は、[settings.json ファイル](/ja/settings)でパスを設定します。

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

Claude Code は Windows でネイティブに PowerShell を実行することもできます（オプトインプレビュー）。セットアップと制限については、[PowerShell ツール](/ja/tools-reference#powershell-tool)を参照してください。

**オプション 2: WSL**

WSL 1 と WSL 2 の両方がサポートされています。WSL 2 は強化されたセキュリティのための[サンドボックス](/ja/sandboxing)をサポートしています。WSL 1 はサンドボックスをサポートしていません。

### Alpine Linux と musl ベースのディストリビューション

Alpine およびその他の musl/uClibc ベースのディストリビューション上のネイティブインストーラーには、`libgcc`、`libstdc++`、および `ripgrep` が必要です。ディストリビューションのパッケージマネージャーを使用してこれらをインストールしてから、`USE_BUILTIN_RIPGREP=0` を設定します。

この例は Alpine で必要なパッケージをインストールします。

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

次に、[`settings.json`](/ja/settings#available-settings)ファイルで `USE_BUILTIN_RIPGREP` を `0` に設定します。

```json  theme={null}
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

## インストールを確認

インストール後、Claude Code が機能していることを確認します。

```bash  theme={null}
claude --version
```

インストールと構成をより詳しく確認するには、[`claude doctor`](/ja/troubleshooting#get-more-help)を実行します。

```bash  theme={null}
claude doctor
```

## 認証

Claude Code には、Pro、Max、Team、Enterprise、または Console アカウントが必要です。無料の Claude.ai プランには Claude Code アクセスは含まれていません。[Amazon Bedrock](/ja/amazon-bedrock)、[Google Vertex AI](/ja/google-vertex-ai)、または[Microsoft Foundry](/ja/microsoft-foundry)などのサードパーティ API プロバイダーで Claude Code を使用することもできます。

インストール後、`claude` を実行してブラウザーのプロンプトに従ってログインします。すべてのアカウントタイプとチームセットアップオプションについては、[認証](/ja/authentication)を参照してください。

## Claude Code を更新

ネイティブインストールは自動的にバックグラウンドで更新されます。[リリースチャネルを構成](#configure-release-channel)して、更新をすぐに受け取るか遅延安定スケジュールで受け取るかを制御することも、[自動更新を完全に無効にする](#disable-auto-updates)こともできます。Homebrew および WinGet インストールは手動更新が必要です。

### 自動更新

Claude Code は起動時と実行中に定期的に更新をチェックします。更新はバックグラウンドでダウンロードおよびインストールされ、次に Claude Code を起動するときに有効になります。

<Note>
  Homebrew および WinGet インストールは自動更新されません。`brew upgrade claude-code` または `winget upgrade Anthropic.ClaudeCode` を使用して手動で更新します。

  **既知の問題**: Claude Code は、新しいバージョンがこれらのパッケージマネージャーで利用可能になる前に更新を通知する場合があります。アップグレードが失敗した場合は、しばらく待ってからもう一度試してください。

  Homebrew はアップグレード後、古いバージョンをディスク上に保持します。`brew cleanup claude-code` を定期的に実行してディスク容量を回収します。
</Note>

### リリースチャネルを構成

`autoUpdatesChannel` 設定を使用して、Claude Code が自動更新と `claude update` に従うリリースチャネルを制御します。

* `"latest"`、デフォルト: リリースされるとすぐに新機能を受け取ります
* `"stable"`: 通常約 1 週間前のバージョンを使用し、大きな回帰を伴うリリースをスキップします

これを `/config` → **自動更新チャネル**経由で構成するか、[settings.json ファイル](/ja/settings)に追加します。

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

エンタープライズデプロイメントの場合、[管理設定](/ja/permissions#managed-settings)を使用して、組織全体で一貫したリリースチャネルを適用できます。

### 自動更新を無効にする

[`settings.json`](/ja/settings#available-settings)ファイルの `env` キーで `DISABLE_AUTOUPDATER` を `"1"` に設定します。

```json  theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

### 手動で更新

次のバックグラウンドチェックを待たずに更新をすぐに適用するには、以下を実行します。

```bash  theme={null}
claude update
```

## 高度なインストールオプション

これらのオプションは、バージョンピニング、npm からの移行、およびバイナリ整合性の検証用です。

### 特定のバージョンをインストール

ネイティブインストーラーは、特定のバージョン番号またはリリースチャネル（`latest` または `stable`）を受け入れます。インストール時に選択したチャネルが自動更新のデフォルトになります。詳細については、[リリースチャネルを構成](#configure-release-channel)を参照してください。

最新バージョンをインストールするには（デフォルト）:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
  </Tab>
</Tabs>

安定版をインストールするには:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s stable
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
    ```
  </Tab>
</Tabs>

特定のバージョン番号をインストールするには:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 2.1.89
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 2.1.89 && del install.cmd
    ```
  </Tab>
</Tabs>

### 非推奨の npm インストール

npm インストールは非推奨です。ネイティブインストーラーはより高速で、依存関係が不要で、バックグラウンドで自動更新されます。可能な場合は[ネイティブインストール](#install-claude-code)方法を使用してください。

#### npm からネイティブへの移行

以前に npm で Claude Code をインストールした場合は、ネイティブインストーラーに切り替えます。

```bash  theme={null}
# ネイティブバイナリをインストール
curl -fsSL https://claude.ai/install.sh | bash

# 古い npm インストールを削除
npm uninstall -g @anthropic-ai/claude-code
```

既存の npm インストールから `claude install` を実行して、ネイティブバイナリを並行してインストールしてから、npm バージョンを削除することもできます。

#### npm でインストール

互換性上の理由で npm インストールが必要な場合は、[Node.js 18 以上](https://nodejs.org/en/download)がインストールされている必要があります。パッケージをグローバルにインストールします。

```bash  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  `sudo npm install -g` を使用しないでください。これはアクセス許可の問題とセキュリティリスクにつながる可能性があります。アクセス許可エラーが発生した場合は、[トラブルシューティングアクセス許可エラー](/ja/troubleshooting#permission-errors-during-installation)を参照してください。
</Warning>

### バイナリ整合性とコード署名

各リリースは、すべてのプラットフォームバイナリの SHA256 チェックサムを含む `manifest.json` を公開します。マニフェストは Anthropic GPG キーで署名されているため、マニフェスト上の署名を検証することで、それが列挙するすべてのバイナリを推移的に検証します。

#### マニフェスト署名を検証

ステップ 1～3 には、`gpg` と `curl` を備えた POSIX シェルが必要です。Windows では、Git Bash または WSL で実行します。ステップ 4 には PowerShell オプションが含まれています。

<Steps>
  <Step title="公開鍵をダウンロードしてインポート">
    リリース署名キーは固定 URL で公開されています。

    ```bash  theme={null}
    curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import
    ```

    インポートされたキーのフィンガープリントを表示します。

    ```bash  theme={null}
    gpg --fingerprint security@anthropic.com
    ```

    出力にこのフィンガープリントが含まれていることを確認します。

    ```text  theme={null}
    31DD DE24 DDFA B679 F42D  7BD2 BAA9 29FF 1A7E CACE
    ```
  </Step>

  <Step title="マニフェストと署名をダウンロード">
    `VERSION` を検証するリリースに設定します。

    ```bash  theme={null}
    REPO=https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases
    VERSION=2.1.89
    curl -fsSLO "$REPO/$VERSION/manifest.json"
    curl -fsSLO "$REPO/$VERSION/manifest.json.sig"
    ```
  </Step>

  <Step title="署名を検証">
    マニフェストに対して分離された署名を検証します。

    ```bash  theme={null}
    gpg --verify manifest.json.sig manifest.json
    ```

    有効な結果は `Good signature from "Anthropic Claude Code Release Signing <security@anthropic.com>"` を報告します。

    `gpg` は新しくインポートされたキーに対して `WARNING: This key is not certified with a trusted signature!` も出力します。これは予想されています。`Good signature` 行は暗号化チェックが成功したことを確認します。ステップ 1 のフィンガープリント比較はキー自体が本物であることを確認します。
  </Step>

  <Step title="バイナリをマニフェストに対して確認">
    ダウンロードしたバイナリの SHA256 チェックサムを `manifest.json` の `platforms.<platform>.checksum` の下にリストされている値と比較します。

    <Tabs>
      <Tab title="Linux">
        ```bash  theme={null}
        sha256sum claude
        ```
      </Tab>

      <Tab title="macOS">
        ```bash  theme={null}
        shasum -a 256 claude
        ```
      </Tab>

      <Tab title="Windows PowerShell">
        ```powershell  theme={null}
        (Get-FileHash claude.exe -Algorithm SHA256).Hash.ToLower()
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>

<Note>
  マニフェスト署名は `2.1.89` 以降のリリースで利用可能です。以前のリリースは分離された署名なしで `manifest.json` にチェックサムを公開します。
</Note>

#### プラットフォームコード署名

署名付きマニフェストに加えて、個別のバイナリはサポートされている場所でプラットフォーム固有のコード署名を実行します。

* **macOS**: "Anthropic PBC" によって署名され、Apple によって公証されています。`codesign --verify --verbose ./claude` で検証します。
* **Windows**: "Anthropic, PBC" によって署名されています。`Get-AuthenticodeSignature .\claude.exe` で検証します。
* **Linux**: 上記のマニフェスト署名を使用して整合性を検証します。Linux バイナリは個別にコード署名されていません。

## Claude Code をアンインストール

Claude Code を削除するには、インストール方法の指示に従います。

### ネイティブインストール

Claude Code バイナリとバージョンファイルを削除します。

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    rm -f ~/.local/bin/claude
    rm -rf ~/.local/share/claude
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
    Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
    ```
  </Tab>
</Tabs>

### Homebrew インストール

Homebrew cask を削除します。

```bash  theme={null}
brew uninstall --cask claude-code
```

### WinGet インストール

WinGet パッケージを削除します。

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### npm

グローバル npm パッケージを削除します。

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### 構成ファイルを削除

<Warning>
  構成ファイルを削除すると、すべての設定、許可されたツール、MCP サーバー構成、およびセッション履歴が削除されます。
</Warning>

Claude Code の設定とキャッシュされたデータを削除するには:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    # ユーザー設定と状態を削除
    rm -rf ~/.claude
    rm ~/.claude.json

    # プロジェクト固有の設定を削除（プロジェクトディレクトリから実行）
    rm -rf .claude
    rm -f .mcp.json
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    # ユーザー設定と状態を削除
    Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
    Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

    # プロジェクト固有の設定を削除（プロジェクトディレクトリから実行）
    Remove-Item -Path ".claude" -Recurse -Force
    Remove-Item -Path ".mcp.json" -Force
    ```
  </Tab>
</Tabs>
