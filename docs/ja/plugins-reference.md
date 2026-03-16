> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# プラグインリファレンス

> Claude Code プラグインシステムの完全な技術リファレンス。スキーマ、CLI コマンド、コンポーネント仕様を含みます。

<Tip>
  プラグインをインストールしたいですか？[プラグインの検出とインストール](/ja/discover-plugins)を参照してください。プラグインの作成については、[プラグイン](/ja/plugins)を参照してください。プラグインの配布については、[プラグインマーケットプレイス](/ja/plugin-marketplaces)を参照してください。
</Tip>

このリファレンスは、Claude Code プラグインシステムの完全な技術仕様を提供します。コンポーネントスキーマ、CLI コマンド、開発ツールを含みます。

**プラグイン**は、Claude Code をカスタム機能で拡張する自己完結型のコンポーネントディレクトリです。プラグインコンポーネントには、skills、agents、hooks、MCP servers、LSP servers が含まれます。

## プラグインコンポーネントリファレンス

### Skills

プラグインは Claude Code に skills を追加し、`/name` ショートカットを作成します。これらは、あなたまたは Claude が呼び出すことができます。

**場所**: プラグインルートの `skills/` または `commands/` ディレクトリ

**ファイル形式**: Skills はディレクトリで `SKILL.md` を含みます。commands はシンプルなマークダウンファイルです。

**Skill 構造**:

```text  theme={null}
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (optional)
│   └── scripts/ (optional)
└── code-reviewer/
    └── SKILL.md
```

**統合動作**:

* Skills と commands はプラグインがインストールされると自動的に検出されます
* Claude はタスクコンテキストに基づいて自動的にそれらを呼び出すことができます
* Skills は SKILL.md の横にサポートファイルを含めることができます

詳細については、[Skills](/ja/skills)を参照してください。

### Agents

プラグインは、特定のタスク用の特化した subagents を提供できます。Claude は必要に応じて自動的にそれらを呼び出すことができます。

**場所**: プラグインルートの `agents/` ディレクトリ

**ファイル形式**: エージェント機能を説明するマークダウンファイル

**Agent 構造**:

```markdown  theme={null}
---
name: agent-name
description: このエージェントが専門とする内容と、Claude がそれを呼び出すべき時期
---

エージェントの役割、専門知識、動作を説明する詳細なシステムプロンプト。
```

**統合ポイント**:

* Agents は `/agents` インターフェイスに表示されます
* Claude はタスクコンテキストに基づいて自動的にエージェントを呼び出すことができます
* Agents はユーザーが手動で呼び出すことができます
* プラグインエージェントは組み込みの Claude エージェントと一緒に動作します

詳細については、[Subagents](/ja/sub-agents)を参照してください。

### Hooks

プラグインは Claude Code イベントに自動的に応答するイベントハンドラーを提供できます。

**場所**: プラグインルートの `hooks/hooks.json`、または plugin.json 内のインライン

**形式**: イベントマッチャーとアクションを含む JSON 設定

**Hook 設定**:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

**利用可能なイベント**:

* `PreToolUse`: Claude がツールを使用する前
* `PostToolUse`: Claude がツールを正常に使用した後
* `PostToolUseFailure`: Claude ツール実行が失敗した後
* `PermissionRequest`: パーミッションダイアログが表示されるとき
* `UserPromptSubmit`: ユーザーがプロンプトを送信するとき
* `Notification`: Claude Code が通知を送信するとき
* `Stop`: Claude が停止を試みるとき
* `SubagentStart`: subagent が開始されるとき
* `SubagentStop`: subagent が停止を試みるとき
* `SessionStart`: セッションの開始時
* `SessionEnd`: セッションの終了時
* `TeammateIdle`: エージェントチームのチームメイトがアイドル状態になろうとしているとき
* `TaskCompleted`: タスクが完了としてマークされているとき
* `PreCompact`: 会話履歴がコンパクト化される前

**Hook タイプ**:

* `command`: シェルコマンドまたはスクリプトを実行
* `prompt`: LLM でプロンプトを評価（コンテキストの `$ARGUMENTS` プレースホルダーを使用）
* `agent`: 複雑な検証タスク用のツール付き agentic verifier を実行

### MCP servers

プラグインは Model Context Protocol（MCP）servers をバンドルして、Claude Code を外部ツールおよびサービスに接続できます。

**場所**: プラグインルートの `.mcp.json`、または plugin.json 内のインライン

**形式**: 標準 MCP サーバー設定

**MCP サーバー設定**:

```json  theme={null}
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**統合動作**:

* プラグイン MCP servers はプラグインが有効になると自動的に開始されます
* Servers は Claude のツールキットに標準 MCP ツールとして表示されます
* サーバー機能は Claude の既存ツールとシームレスに統合されます
* プラグインサーバーはユーザー MCP servers とは独立して設定できます

### LSP servers

<Tip>
  LSP プラグインを使用したいですか？公式マーケットプレイスからインストールしてください。`/plugin` Discover タブで「lsp」を検索してください。このセクションでは、公式マーケットプレイスでカバーされていない言語用の LSP プラグインを作成する方法を説明しています。
</Tip>

プラグインは [Language Server Protocol](https://microsoft.github.io/language-server-protocol/)（LSP）servers を提供して、Claude がコードベースで作業する際にリアルタイムコード インテリジェンスを得ることができます。

LSP 統合は以下を提供します:

* **即座の診断**: Claude は各編集後すぐにエラーと警告を確認できます
* **コードナビゲーション**: 定義へのジャンプ、参照の検索、ホバー情報
* **言語認識**: コードシンボルの型情報とドキュメント

**場所**: プラグインルートの `.lsp.json`、または `plugin.json` 内のインライン

**形式**: 言語サーバー名をその設定にマップする JSON 設定

**`.lsp.json` ファイル形式**:

```json  theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**`plugin.json` 内のインライン**:

```json  theme={null}
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**必須フィールド:**

| フィールド                 | 説明                                 |
| :-------------------- | :--------------------------------- |
| `command`             | 実行する LSP バイナリ（PATH に含まれている必要があります） |
| `extensionToLanguage` | ファイル拡張子を言語識別子にマップ                  |

**オプションフィールド:**

| フィールド                   | 説明                                           |
| :---------------------- | :------------------------------------------- |
| `args`                  | LSP サーバーのコマンドライン引数                           |
| `transport`             | 通信トランスポート: `stdio`（デフォルト）または `socket`        |
| `env`                   | サーバー起動時に設定する環境変数                             |
| `initializationOptions` | 初期化中にサーバーに渡されるオプション                          |
| `settings`              | `workspace/didChangeConfiguration` 経由で渡される設定 |
| `workspaceFolder`       | サーバーのワークスペースフォルダーパス                          |
| `startupTimeout`        | サーバー起動を待つ最大時間（ミリ秒）                           |
| `shutdownTimeout`       | グレースフルシャットダウンを待つ最大時間（ミリ秒）                    |
| `restartOnCrash`        | サーバーがクラッシュした場合に自動的に再起動するかどうか                 |
| `maxRestarts`           | 諦める前の最大再起動試行回数                               |

<Warning>
  **言語サーバーバイナリを別途インストールする必要があります。** LSP プラグインは Claude Code が言語サーバーに接続する方法を設定しますが、サーバー自体は含まれていません。`/plugin` Errors タブに `Executable not found in $PATH` が表示される場合は、言語に必要なバイナリをインストールしてください。
</Warning>

**利用可能な LSP プラグイン:**

| プラグイン            | 言語サーバー                     | インストールコマンド                                                                          |
| :--------------- | :------------------------- | :---------------------------------------------------------------------------------- |
| `pyright-lsp`    | Pyright（Python）            | `pip install pyright` または `npm install -g pyright`                                  |
| `typescript-lsp` | TypeScript Language Server | `npm install -g typescript-language-server typescript`                              |
| `rust-lsp`       | rust-analyzer              | [rust-analyzer インストールを参照](https://rust-analyzer.github.io/manual.html#installation) |

言語サーバーをまずインストールしてから、マーケットプレイスからプラグインをインストールしてください。

***

## プラグインインストールスコープ

プラグインをインストールするときは、プラグインが利用可能な場所と他のユーザーが使用できるかどうかを決定する**スコープ**を選択します。

| スコープ      | 設定ファイル                              | ユースケース                           |
| :-------- | :---------------------------------- | :------------------------------- |
| `user`    | `~/.claude/settings.json`           | すべてのプロジェクト全体で利用可能な個人プラグイン（デフォルト） |
| `project` | `.claude/settings.json`             | バージョン管理経由で共有されるチームプラグイン          |
| `local`   | `.claude/settings.local.json`       | プロジェクト固有のプラグイン、gitignored        |
| `managed` | [管理設定](/ja/settings#settings-files) | 管理プラグイン（読み取り専用、更新のみ）             |

プラグインは他の Claude Code 設定と同じスコープシステムを使用します。インストール手順とスコープフラグについては、[プラグインのインストール](/ja/discover-plugins#install-plugins)を参照してください。スコープの完全な説明については、[設定スコープ](/ja/settings#configuration-scopes)を参照してください。

***

## プラグインマニフェストスキーマ

`.claude-plugin/plugin.json` ファイルはプラグインのメタデータと設定を定義します。このセクションでは、サポートされているすべてのフィールドとオプションを説明しています。

マニフェストはオプションです。省略された場合、Claude Code は[デフォルト場所](#file-locations-reference)のコンポーネントを自動検出し、ディレクトリ名からプラグイン名を導出します。メタデータを提供するか、カスタムコンポーネントパスが必要な場合はマニフェストを使用してください。

### 完全なスキーマ

```json  theme={null}
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./custom/commands/special.md"],
  "agents": "./custom/agents/",
  "skills": "./custom/skills/",
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "lspServers": "./.lsp.json"
}
```

### 必須フィールド

マニフェストを含める場合、`name` は唯一の必須フィールドです。

| フィールド  | 型      | 説明                        | 例                    |
| :----- | :----- | :------------------------ | :------------------- |
| `name` | string | 一意の識別子（kebab-case、スペースなし） | `"deployment-tools"` |

この名前はコンポーネントの名前空間に使用されます。たとえば、UI では、名前が `plugin-dev` のプラグインのエージェント `agent-creator` は `plugin-dev:agent-creator` として表示されます。

### メタデータフィールド

| フィールド         | 型      | 説明                                                                              | 例                                                  |
| :------------ | :----- | :------------------------------------------------------------------------------ | :------------------------------------------------- |
| `version`     | string | セマンティックバージョン。マーケットプレイスエントリにも設定されている場合、`plugin.json` が優先されます。1 つの場所に設定するだけで済みます。 | `"2.1.0"`                                          |
| `description` | string | プラグインの目的の簡潔な説明                                                                  | `"Deployment automation tools"`                    |
| `author`      | object | 著者情報                                                                            | `{"name": "Dev Team", "email": "dev@company.com"}` |
| `homepage`    | string | ドキュメント URL                                                                      | `"https://docs.example.com"`                       |
| `repository`  | string | ソースコード URL                                                                      | `"https://github.com/user/plugin"`                 |
| `license`     | string | ライセンス識別子                                                                        | `"MIT"`、`"Apache-2.0"`                             |
| `keywords`    | array  | 検出タグ                                                                            | `["deployment", "ci-cd"]`                          |

### コンポーネントパスフィールド

| フィールド          | 型                     | 説明                                                                                                                  | 例                                       |
| :------------- | :-------------------- | :------------------------------------------------------------------------------------------------------------------ | :-------------------------------------- |
| `commands`     | string\|array         | 追加のコマンドファイル/ディレクトリ                                                                                                  | `"./custom/cmd.md"` または `["./cmd1.md"]` |
| `agents`       | string\|array         | 追加のエージェントファイル                                                                                                       | `"./custom/agents/reviewer.md"`         |
| `skills`       | string\|array         | 追加のスキルディレクトリ                                                                                                        | `"./custom/skills/"`                    |
| `hooks`        | string\|array\|object | Hook 設定パスまたはインライン設定                                                                                                 | `"./my-extra-hooks.json"`               |
| `mcpServers`   | string\|array\|object | MCP 設定パスまたはインライン設定                                                                                                  | `"./my-extra-mcp-config.json"`          |
| `outputStyles` | string\|array         | 追加の出力スタイルファイル/ディレクトリ                                                                                                | `"./styles/"`                           |
| `lspServers`   | string\|array\|object | [Language Server Protocol](https://microsoft.github.io/language-server-protocol/)コード インテリジェンス用の設定（定義へのジャンプ、参照の検索など） | `"./.lsp.json"`                         |

### パス動作ルール

**重要**: カスタムパスはデフォルトディレクトリを置き換えるのではなく、補足します。

* `commands/` が存在する場合、カスタムコマンドパスに加えてロードされます
* すべてのパスはプラグインルートに相対的で、`./` で始まる必要があります
* カスタムパスからのコマンドは同じ命名と名前空間ルールを使用します
* 複数のパスを配列として指定して柔軟性を確保できます

**パスの例**:

```json  theme={null}
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### 環境変数

**`${CLAUDE_PLUGIN_ROOT}`**: プラグインディレクトリへの絶対パスを含みます。hooks、MCP servers、スクリプトでこれを使用して、インストール場所に関係なく正しいパスを確保してください。

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

***

## プラグインキャッシングとファイル解決

プラグインは 2 つの方法で指定されます:

* `claude --plugin-dir` を通じて、セッションの期間。
* マーケットプレイスを通じて、将来のセッション用にインストール。

セキュリティと検証の目的で、Claude Code は\_マーケットプレイス\_プラグインをユーザーのローカル**プラグインキャッシュ**（`~/.claude/plugins/cache`）にコピーします。これらを所定の場所で使用するのではなく。この動作を理解することは、外部ファイルを参照するプラグインを開発する際に重要です。

### パストラバーサル制限

インストールされたプラグインはディレクトリの外側のファイルを参照できません。プラグインルートの外側をトラバースするパス（`../shared-utils` など）は、これらの外部ファイルがキャッシュにコピーされないため、インストール後は機能しません。

### 外部依存関係の操作

プラグインがディレクトリの外側のファイルにアクセスする必要がある場合、プラグインディレクトリ内の外部ファイルへのシンボリックリンクを作成できます。シンボリックリンクはコピープロセス中に尊重されます:

```bash  theme={null}
# プラグインディレクトリ内
ln -s /path/to/shared-utils ./shared-utils
```

シンボリックリンクされたコンテンツはプラグインキャッシュにコピーされます。これはキャッシングシステムのセキュリティ上の利点を維持しながら柔軟性を提供します。

***

## プラグインディレクトリ構造

### 標準プラグインレイアウト

完全なプラグインは次の構造に従います:

```text  theme={null}
enterprise-plugin/
├── .claude-plugin/           # メタデータディレクトリ（オプション）
│   └── plugin.json             # プラグインマニフェスト
├── commands/                 # デフォルトコマンド場所
│   ├── status.md
│   └── logs.md
├── agents/                   # デフォルトエージェント場所
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── skills/                   # エージェント Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── hooks/                    # Hook 設定
│   ├── hooks.json           # メイン hook 設定
│   └── security-hooks.json  # 追加 hooks
├── settings.json            # プラグインのデフォルト設定
├── .mcp.json                # MCP サーバー定義
├── .lsp.json                # LSP サーバー設定
├── scripts/                 # Hook とユーティリティスクリプト
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # ライセンスファイル
└── CHANGELOG.md             # バージョン履歴
```

<Warning>
  `.claude-plugin/` ディレクトリは `plugin.json` ファイルを含みます。他のすべてのディレクトリ（commands/、agents/、skills/、hooks/）は `.claude-plugin/` 内ではなく、プラグインルートにある必要があります。
</Warning>

### ファイル場所リファレンス

| コンポーネント         | デフォルト場所                      | 目的                                                                      |
| :-------------- | :--------------------------- | :---------------------------------------------------------------------- |
| **マニフェスト**      | `.claude-plugin/plugin.json` | プラグインメタデータと設定（オプション）                                                    |
| **コマンド**        | `commands/`                  | Skill マークダウンファイル（レガシー。新しい skills には `skills/` を使用）                      |
| **エージェント**      | `agents/`                    | Subagent マークダウンファイル                                                     |
| **Skills**      | `skills/`                    | `<name>/SKILL.md` 構造の Skills                                            |
| **Hooks**       | `hooks/hooks.json`           | Hook 設定                                                                 |
| **MCP servers** | `.mcp.json`                  | MCP サーバー定義                                                              |
| **LSP servers** | `.lsp.json`                  | 言語サーバー設定                                                                |
| **設定**          | `settings.json`              | プラグインが有効になったときに適用されるデフォルト設定。現在、[`agent`](/ja/sub-agents)設定のみがサポートされています |

***

## CLI コマンドリファレンス

Claude Code は非対話的なプラグイン管理用の CLI コマンドを提供します。スクリプトと自動化に役立ちます。

### plugin install

利用可能なマーケットプレイスからプラグインをインストールします。

```bash  theme={null}
claude plugin install <plugin> [options]
```

**引数:**

* `<plugin>`: プラグイン名または特定のマーケットプレイス用の `plugin-name@marketplace-name`

**オプション:**

| オプション                 | 説明                                       | デフォルト  |
| :-------------------- | :--------------------------------------- | :----- |
| `-s, --scope <scope>` | インストールスコープ: `user`、`project`、または `local` | `user` |
| `-h, --help`          | コマンドのヘルプを表示                              |        |

スコープはインストールされたプラグインが追加される設定ファイルを決定します。たとえば、--scope project は `.claude/settings.json` の `enabledPlugins` に書き込み、プロジェクトリポジトリをクローンした全員がプラグインを利用できるようにします。

**例:**

```bash  theme={null}
# ユーザースコープにインストール（デフォルト）
claude plugin install formatter@my-marketplace

# プロジェクトスコープにインストール（チームと共有）
claude plugin install formatter@my-marketplace --scope project

# ローカルスコープにインストール（gitignored）
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

インストール済みプラグインを削除します。

```bash  theme={null}
claude plugin uninstall <plugin> [options]
```

**引数:**

* `<plugin>`: プラグイン名または `plugin-name@marketplace-name`

**オプション:**

| オプション                 | 説明                                           | デフォルト  |
| :-------------------- | :------------------------------------------- | :----- |
| `-s, --scope <scope>` | スコープからアンインストール: `user`、`project`、または `local` | `user` |
| `-h, --help`          | コマンドのヘルプを表示                                  |        |

**エイリアス:** `remove`、`rm`

### plugin enable

無効なプラグインを有効にします。

```bash  theme={null}
claude plugin enable <plugin> [options]
```

**引数:**

* `<plugin>`: プラグイン名または `plugin-name@marketplace-name`

**オプション:**

| オプション                 | 説明                                      | デフォルト  |
| :-------------------- | :-------------------------------------- | :----- |
| `-s, --scope <scope>` | 有効にするスコープ: `user`、`project`、または `local` | `user` |
| `-h, --help`          | コマンドのヘルプを表示                             |        |

### plugin disable

プラグインをアンインストールせずに無効にします。

```bash  theme={null}
claude plugin disable <plugin> [options]
```

**引数:**

* `<plugin>`: プラグイン名または `plugin-name@marketplace-name`

**オプション:**

| オプション                 | 説明                                      | デフォルト  |
| :-------------------- | :-------------------------------------- | :----- |
| `-s, --scope <scope>` | 無効にするスコープ: `user`、`project`、または `local` | `user` |
| `-h, --help`          | コマンドのヘルプを表示                             |        |

### plugin update

プラグインを最新バージョンに更新します。

```bash  theme={null}
claude plugin update <plugin> [options]
```

**引数:**

* `<plugin>`: プラグイン名または `plugin-name@marketplace-name`

**オプション:**

| オプション                 | 説明                                               | デフォルト  |
| :-------------------- | :----------------------------------------------- | :----- |
| `-s, --scope <scope>` | 更新するスコープ: `user`、`project`、`local`、または `managed` | `user` |
| `-h, --help`          | コマンドのヘルプを表示                                      |        |

***

## デバッグと開発ツール

### デバッグコマンド

`claude --debug`（または TUI 内の `/debug`）を使用してプラグイン読み込みの詳細を確認します:

これは以下を表示します:

* どのプラグインが読み込まれているか
* プラグインマニフェストのエラー
* コマンド、エージェント、hook 登録
* MCP サーバー初期化

### 一般的な問題

| 問題                                  | 原因                          | 解決策                                                                    |
| :---------------------------------- | :-------------------------- | :--------------------------------------------------------------------- |
| プラグインが読み込まれない                       | 無効な `plugin.json`           | `claude plugin validate` または `/plugin validate` で JSON 構文を検証           |
| コマンドが表示されない                         | ディレクトリ構造が間違っている             | `commands/` がルートにあることを確認。`.claude-plugin/` 内ではない                       |
| Hooks が発火しない                        | スクリプトが実行可能でない               | `chmod +x script.sh` を実行                                               |
| MCP サーバーが失敗                         | `${CLAUDE_PLUGIN_ROOT}` が不足 | すべてのプラグインパスに変数を使用                                                      |
| パスエラー                               | 絶対パスが使用されている                | すべてのパスは相対的で `./` で始まる必要があります                                           |
| LSP `Executable not found in $PATH` | 言語サーバーがインストールされていない         | バイナリをインストール（例: `npm install -g typescript-language-server typescript`） |

### エラーメッセージの例

**マニフェスト検証エラー**:

* `Invalid JSON syntax: Unexpected token } in JSON at position 142`: コンマの欠落、余分なコンマ、またはクォートされていない文字列を確認
* `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required`: 必須フィールドが不足
* `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`: JSON 構文エラー

**プラグイン読み込みエラー**:

* `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`: コマンドパスが存在するが有効なコマンドファイルが含まれていない
* `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`: marketplace.json の `source` パスが存在しないディレクトリを指している
* `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`: 重複するコンポーネント定義を削除するか、marketplace エントリから `strict: false` を削除

### Hook トラブルシューティング

**Hook スクリプトが実行されない**:

1. スクリプトが実行可能であることを確認: `chmod +x ./scripts/your-script.sh`
2. shebang 行を確認: 最初の行は `#!/bin/bash` または `#!/usr/bin/env bash` である必要があります
3. パスが `${CLAUDE_PLUGIN_ROOT}` を使用していることを確認: `"command": "${CLAUDE_PLUGIN_ROOT}/scripts/your-script.sh"`
4. スクリプトを手動でテスト: `./scripts/your-script.sh`

**Hook が予期されたイベントでトリガーされない**:

1. イベント名が正しいことを確認（大文字小文字を区別）: `PostToolUse`、`postToolUse` ではない
2. マッチャーパターンがツールと一致することを確認: ファイル操作の場合 `"matcher": "Write|Edit"`
3. hook タイプが有効であることを確認: `command`、`prompt`、または `agent`

### MCP サーバートラブルシューティング

**サーバーが起動しない**:

1. コマンドが存在し、実行可能であることを確認
2. すべてのパスが `${CLAUDE_PLUGIN_ROOT}` 変数を使用していることを確認
3. MCP サーバーログを確認: `claude --debug` は初期化エラーを表示
4. Claude Code の外部でサーバーを手動でテスト

**サーバーツールが表示されない**:

1. サーバーが `.mcp.json` または `plugin.json` で正しく設定されていることを確認
2. サーバーが MCP プロトコルを正しく実装していることを確認
3. デバッグ出力で接続タイムアウトを確認

### ディレクトリ構造の間違い

**症状**: プラグインは読み込まれるがコンポーネント（コマンド、エージェント、hooks）が不足している。

**正しい構造**: コンポーネントはプラグインルートにある必要があり、`.claude-plugin/` 内ではありません。`.claude-plugin/` には `plugin.json` のみが属します。

```text  theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← マニフェストのみここ
├── commands/            ← ルートレベル
├── agents/              ← ルートレベル
└── hooks/               ← ルートレベル
```

コンポーネントが `.claude-plugin/` 内にある場合は、プラグインルートに移動してください。

**デバッグチェックリスト**:

1. `claude --debug` を実行し、「loading plugin」メッセージを探す
2. 各コンポーネントディレクトリがデバッグ出力にリストされていることを確認
3. プラグインファイルを読み取ることができるファイルパーミッションを確認

***

## 配布とバージョン管理リファレンス

### バージョン管理

プラグインリリースにはセマンティックバージョニングに従ってください:

```json  theme={null}
{
  "name": "my-plugin",
  "version": "2.1.0"
}
```

**バージョン形式**: `MAJOR.MINOR.PATCH`

* **MAJOR**: 破壊的変更（互換性のない API 変更）
* **MINOR**: 新機能（後方互換性のある追加）
* **PATCH**: バグ修正（後方互換性のある修正）

**ベストプラクティス**:

* 最初の安定リリースは `1.0.0` から開始
* 変更を配布する前に `plugin.json` のバージョンを更新
* `CHANGELOG.md` ファイルで変更を文書化
* テスト用に `2.0.0-beta.1` のようなプレリリースバージョンを使用

<Warning>
  Claude Code はバージョンを使用してプラグインを更新するかどうかを判断します。プラグインのコードを変更しても `plugin.json` のバージョンをバンプしない場合、キャッシングのため既存ユーザーは変更を確認できません。

  プラグインが[マーケットプレイス](/ja/plugin-marketplaces)ディレクトリ内にある場合、代わりに `marketplace.json` を通じてバージョンを管理でき、`plugin.json` から `version` フィールドを省略できます。
</Warning>

***

## 関連項目

* [プラグイン](/ja/plugins) - チュートリアルと実践的な使用法
* [プラグインマーケットプレイス](/ja/plugin-marketplaces) - マーケットプレイスの作成と管理
* [Skills](/ja/skills) - Skill 開発の詳細
* [Subagents](/ja/sub-agents) - エージェント設定と機能
* [Hooks](/ja/hooks) - イベント処理と自動化
* [MCP](/ja/mcp) - 外部ツール統合
* [設定](/ja/settings) - プラグインの設定オプション
