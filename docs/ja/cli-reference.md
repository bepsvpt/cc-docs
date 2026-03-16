> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# CLI リファレンス

> Claude Code コマンドラインインターフェースの完全なリファレンス。コマンドとフラグを含みます。

## CLI コマンド

これらのコマンドを使用して、セッションを開始し、コンテンツをパイプし、会話を再開し、更新を管理できます。

| コマンド                            | 説明                                                                                                                                                               | 例                                                  |
| :------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `claude`                        | インタラクティブセッションを開始                                                                                                                                                 | `claude`                                           |
| `claude "query"`                | 初期プロンプト付きでインタラクティブセッションを開始                                                                                                                                       | `claude "explain this project"`                    |
| `claude -p "query"`             | SDK 経由でクエリを実行してから終了                                                                                                                                              | `claude -p "explain this function"`                |
| `cat file \| claude -p "query"` | パイプされたコンテンツを処理                                                                                                                                                   | `cat logs.txt \| claude -p "explain"`              |
| `claude -c`                     | 現在のディレクトリで最新の会話を続行                                                                                                                                               | `claude -c`                                        |
| `claude -c -p "query"`          | SDK 経由で続行                                                                                                                                                        | `claude -c -p "Check for type errors"`             |
| `claude -r "<session>" "query"` | ID または名前でセッションを再開                                                                                                                                                | `claude -r "auth-refactor" "Finish this PR"`       |
| `claude update`                 | 最新バージョンに更新                                                                                                                                                       | `claude update`                                    |
| `claude auth login`             | Anthropic アカウントにサインイン。`--email` を使用してメールアドレスを事前入力し、`--sso` を使用して SSO 認証を強制します                                                                                    | `claude auth login --email user@example.com --sso` |
| `claude auth logout`            | Anthropic アカウントからログアウト                                                                                                                                           | `claude auth logout`                               |
| `claude auth status`            | 認証ステータスを JSON として表示。`--text` を使用して人間が読める形式で表示。ログイン済みの場合はコード 0 で終了、ログインしていない場合は 1 で終了                                                                             | `claude auth status`                               |
| `claude agents`                 | すべての設定済み [subagents](/ja/sub-agents) をソース別にグループ化して一覧表示                                                                                                           | `claude agents`                                    |
| `claude mcp`                    | Model Context Protocol（MCP）サーバーを設定                                                                                                                               | [Claude Code MCP ドキュメント](/ja/mcp) を参照してください。       |
| `claude remote-control`         | [Remote Control セッション](/ja/remote-control) を開始して、ローカルで実行中の Claude Code を Claude.ai または Claude アプリから制御します。フラグについては [Remote Control](/ja/remote-control) を参照してください | `claude remote-control`                            |

## CLI フラグ

これらのコマンドラインフラグを使用して Claude Code の動作をカスタマイズします。

| フラグ                                    | 説明                                                                                                                                                                         | 例                                                                                                  |
| :------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `--add-dir`                            | Claude がアクセスできる追加の作業ディレクトリを追加します（各パスがディレクトリとして存在することを検証）                                                                                                                   | `claude --add-dir ../apps ../lib`                                                                  |
| `--agent`                              | 現在のセッションのエージェントを指定します（`agent` 設定をオーバーライド）                                                                                                                                  | `claude --agent my-custom-agent`                                                                   |
| `--agents`                             | カスタム [subagents](/ja/sub-agents) を JSON 経由で動的に定義します（形式については以下を参照）                                                                                                          | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allow-dangerously-skip-permissions` | 権限バイパスをオプションとして有効にします（すぐには有効化しません）。`--permission-mode` との組み合わせを許可します（注意して使用）                                                                                               | `claude --permission-mode plan --allow-dangerously-skip-permissions`                               |
| `--allowedTools`                       | 権限を求めずに実行するツール。パターンマッチングについては [権限ルール構文](/ja/settings#permission-rule-syntax) を参照してください。利用可能なツールを制限するには、代わりに `--tools` を使用してください                                            | `"Bash(git log *)" "Bash(git diff *)" "Read"`                                                      |
| `--append-system-prompt`               | カスタムテキストをデフォルトシステムプロンプトの末尾に追加                                                                                                                                              | `claude --append-system-prompt "Always use TypeScript"`                                            |
| `--append-system-prompt-file`          | ファイルから追加のシステムプロンプトテキストを読み込み、デフォルトプロンプトに追加                                                                                                                                  | `claude --append-system-prompt-file ./extra-rules.txt`                                             |
| `--betas`                              | API リクエストに含めるベータヘッダー（API キーユーザーのみ）                                                                                                                                         | `claude --betas interleaved-thinking`                                                              |
| `--chrome`                             | Web 自動化とテストのための [Chrome ブラウザ統合](/ja/chrome) を有効化                                                                                                                           | `claude --chrome`                                                                                  |
| `--continue`, `-c`                     | 現在のディレクトリで最新の会話を読み込む                                                                                                                                                       | `claude --continue`                                                                                |
| `--dangerously-skip-permissions`       | すべての権限プロンプトをスキップします（注意して使用）                                                                                                                                                | `claude --dangerously-skip-permissions`                                                            |
| `--debug`                              | デバッグモードを有効化し、オプションのカテゴリフィルタリング（例：`"api,hooks"` または `"!statsig,!file"`）                                                                                                     | `claude --debug "api,mcp"`                                                                         |
| `--disable-slash-commands`             | このセッションのすべてのスキルとコマンドを無効化                                                                                                                                                   | `claude --disable-slash-commands`                                                                  |
| `--disallowedTools`                    | モデルのコンテキストから削除され、使用できないツール                                                                                                                                                 | `"Bash(git log *)" "Bash(git diff *)" "Edit"`                                                      |
| `--fallback-model`                     | デフォルトモデルがオーバーロードされた場合、指定されたモデルへの自動フォールバックを有効化（プリントモードのみ）                                                                                                                   | `claude -p --fallback-model sonnet "query"`                                                        |
| `--fork-session`                       | 再開時に、元のセッション ID を再利用する代わりに新しいセッション ID を作成します（`--resume` または `--continue` で使用）                                                                                              | `claude --resume abc123 --fork-session`                                                            |
| `--from-pr`                            | 特定の GitHub PR にリンクされたセッションを再開します。PR 番号または URL を受け入れます。`gh pr create` 経由で作成されたセッションは自動的にリンクされます                                                                             | `claude --from-pr 123`                                                                             |
| `--ide`                                | 起動時に IDE に自動的に接続します（正確に 1 つの有効な IDE が利用可能な場合）                                                                                                                              | `claude --ide`                                                                                     |
| `--init`                               | 初期化フックを実行してインタラクティブモードを開始                                                                                                                                                  | `claude --init`                                                                                    |
| `--init-only`                          | 初期化フックを実行して終了（インタラクティブセッションなし）                                                                                                                                             | `claude --init-only`                                                                               |
| `--include-partial-messages`           | 出力に部分的なストリーミングイベントを含めます（`--print` と `--output-format=stream-json` が必要）                                                                                                     | `claude -p --output-format stream-json --include-partial-messages "query"`                         |
| `--input-format`                       | プリントモードの入力形式を指定します（オプション：`text`、`stream-json`）                                                                                                                             | `claude -p --output-format json --input-format stream-json`                                        |
| `--json-schema`                        | エージェントがワークフローを完了した後、JSON Schema に一致する検証済み JSON 出力を取得します（プリントモードのみ、[構造化出力](https://platform.claude.com/docs/en/agent-sdk/structured-outputs) を参照）                           | `claude -p --json-schema '{"type":"object","properties":{...}}' "query"`                           |
| `--maintenance`                        | メンテナンスフックを実行して終了                                                                                                                                                           | `claude --maintenance`                                                                             |
| `--max-budget-usd`                     | 停止する前に API 呼び出しに費やす最大ドル金額（プリントモードのみ）                                                                                                                                       | `claude -p --max-budget-usd 5.00 "query"`                                                          |
| `--max-turns`                          | agentic ターンの数を制限します（プリントモードのみ）。制限に達するとエラーで終了します。デフォルトでは制限なし                                                                                                                | `claude -p --max-turns 3 "query"`                                                                  |
| `--mcp-config`                         | JSON ファイルまたは文字列から MCP サーバーを読み込みます（スペース区切り）                                                                                                                                 | `claude --mcp-config ./mcp.json`                                                                   |
| `--model`                              | 現在のセッションのモデルを設定します。最新モデルのエイリアス（`sonnet` または `opus`）またはモデルの完全な名前を使用                                                                                                         | `claude --model claude-sonnet-4-6`                                                                 |
| `--no-chrome`                          | このセッションの [Chrome ブラウザ統合](/ja/chrome) を無効化                                                                                                                                  | `claude --no-chrome`                                                                               |
| `--no-session-persistence`             | セッション永続化を無効化し、セッションがディスクに保存されず、再開できないようにします（プリントモードのみ）                                                                                                                     | `claude -p --no-session-persistence "query"`                                                       |
| `--output-format`                      | プリントモードの出力形式を指定します（オプション：`text`、`json`、`stream-json`）                                                                                                                      | `claude -p "query" --output-format json`                                                           |
| `--permission-mode`                    | 指定された [権限モード](/ja/permissions#permission-modes) で開始                                                                                                                        | `claude --permission-mode plan`                                                                    |
| `--permission-prompt-tool`             | 非インタラクティブモードで権限プロンプトを処理する MCP ツールを指定                                                                                                                                       | `claude -p --permission-prompt-tool mcp_auth_tool "query"`                                         |
| `--plugin-dir`                         | このセッションのみのプラグインをディレクトリから読み込みます（繰り返し可能）                                                                                                                                     | `claude --plugin-dir ./my-plugins`                                                                 |
| `--print`, `-p`                        | インタラクティブモードなしで応答を出力します（プログラム的な使用の詳細については [Agent SDK ドキュメント](https://platform.claude.com/docs/en/agent-sdk/overview) を参照）                                                   | `claude -p "query"`                                                                                |
| `--remote`                             | claude.ai で提供されたタスク説明を使用して新しい [Web セッション](/ja/claude-code-on-the-web) を作成                                                                                                  | `claude --remote "Fix the login bug"`                                                              |
| `--resume`, `-r`                       | ID または名前で特定のセッションを再開するか、セッションを選択するためのインタラクティブピッカーを表示                                                                                                                       | `claude --resume auth-refactor`                                                                    |
| `--session-id`                         | 会話に特定のセッション ID を使用します（有効な UUID である必要があります）                                                                                                                                 | `claude --session-id "550e8400-e29b-41d4-a716-446655440000"`                                       |
| `--setting-sources`                    | 読み込む設定ソースのカンマ区切りリスト（`user`、`project`、`local`）                                                                                                                              | `claude --setting-sources user,project`                                                            |
| `--settings`                           | 追加の設定を読み込むための settings JSON ファイルまたは JSON 文字列へのパス                                                                                                                           | `claude --settings ./settings.json`                                                                |
| `--strict-mcp-config`                  | `--mcp-config` からのみ MCP サーバーを使用し、他のすべての MCP 設定を無視                                                                                                                          | `claude --strict-mcp-config --mcp-config ./mcp.json`                                               |
| `--system-prompt`                      | デフォルトのシステムプロンプト全体をカスタムテキストに置き換え                                                                                                                                            | `claude --system-prompt "You are a Python expert"`                                                 |
| `--system-prompt-file`                 | ファイルからシステムプロンプトを読み込み、デフォルトプロンプトを置き換え                                                                                                                                       | `claude --system-prompt-file ./custom-prompt.txt`                                                  |
| `--teleport`                           | [Web セッション](/ja/claude-code-on-the-web) をローカルターミナルで再開                                                                                                                      | `claude --teleport`                                                                                |
| `--teammate-mode`                      | [エージェントチーム](/ja/agent-teams) のチームメイトの表示方法を設定します：`auto`（デフォルト）、`in-process`、または `tmux`。[エージェントチームのセットアップ](/ja/agent-teams#set-up-agent-teams) を参照                           | `claude --teammate-mode in-process`                                                                |
| `--tools`                              | Claude が使用できる組み込みツールを制限します。`""` を使用してすべてを無効化、`"default"` をすべてに使用、または `"Bash,Edit,Read"` のようなツール名を使用                                                                        | `claude --tools "Bash,Edit,Read"`                                                                  |
| `--verbose`                            | 詳細ログを有効化し、ターンバイターンの完全な出力を表示                                                                                                                                                | `claude --verbose`                                                                                 |
| `--version`, `-v`                      | バージョン番号を出力                                                                                                                                                                 | `claude -v`                                                                                        |
| `--worktree`, `-w`                     | Claude を `<repo>/.claude/worktrees/<name>` の分離された [git worktree](/ja/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) で開始します。名前が指定されていない場合は、自動生成されます | `claude -w feature-auth`                                                                           |

<Tip>
  `--output-format json` フラグは、スクリプトと自動化に特に役立ち、Claude の応答をプログラム的に解析できます。
</Tip>

### Agents フラグ形式

`--agents` フラグは、1 つ以上のカスタム subagents を定義する JSON オブジェクトを受け入れます。各 subagent には、一意の名前（キーとして）と、以下のフィールドを持つ定義オブジェクトが必要です。

| フィールド             | 必須  | 説明                                                                                                                                                                 |
| :---------------- | :-- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `description`     | はい  | subagent を呼び出すべき時期の自然言語説明                                                                                                                                          |
| `prompt`          | はい  | subagent の動作をガイドするシステムプロンプト                                                                                                                                        |
| `tools`           | いいえ | subagent が使用できる特定のツールの配列。例：`["Read", "Edit", "Bash"]`。省略された場合は、すべてのツールを継承します。[`Agent(agent_type)`](/ja/sub-agents#restrict-which-subagents-can-be-spawned) 構文をサポート |
| `disallowedTools` | いいえ | この subagent に対して明示的に拒否するツール名の配列                                                                                                                                    |
| `model`           | いいえ | 使用するモデルエイリアス：`sonnet`、`opus`、`haiku`、または `inherit`。省略された場合は、デフォルトで `inherit`                                                                                       |
| `skills`          | いいえ | subagent のコンテキストにプリロードする [skill](/ja/skills) 名の配列                                                                                                                  |
| `mcpServers`      | いいえ | この subagent の [MCP servers](/ja/mcp) の配列。各エントリはサーバー名文字列または `{name: config}` オブジェクト                                                                                 |
| `maxTurns`        | いいえ | subagent が停止する前の agentic ターンの最大数                                                                                                                                   |

例：

```bash  theme={null}
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

subagents の作成と使用の詳細については、[subagents ドキュメント](/ja/sub-agents) を参照してください。

### システムプロンプトフラグ

Claude Code は、システムプロンプトをカスタマイズするための 4 つのフラグを提供します。4 つすべてが、インタラクティブモードと非インタラクティブモードの両方で機能します。

| フラグ                           | 動作                         | ユースケース                               |
| :---------------------------- | :------------------------- | :----------------------------------- |
| `--system-prompt`             | デフォルトプロンプト全体を **置き換え**     | Claude の動作と指示を完全に制御                  |
| `--system-prompt-file`        | ファイルの内容で **置き換え**          | 再現性とバージョン管理のためにファイルからプロンプトを読み込む      |
| `--append-system-prompt`      | デフォルトプロンプトに **追加**         | デフォルトの Claude Code 動作を保持しながら特定の指示を追加 |
| `--append-system-prompt-file` | ファイルの内容をデフォルトプロンプトに **追加** | デフォルトを保持しながらファイルから追加の指示を読み込む         |

**各フラグを使用する時期：**

* **`--system-prompt`**：Claude のシステムプロンプトを完全に制御する必要がある場合に使用します。これにより、すべてのデフォルト Claude Code 指示が削除され、白紙の状態が得られます。
  ```bash  theme={null}
  claude --system-prompt "You are a Python expert who only writes type-annotated code"
  ```

* **`--system-prompt-file`**：ファイルからカスタムプロンプトを読み込みたい場合に使用します。チームの一貫性またはバージョン管理されたプロンプトテンプレートに役立ちます。
  ```bash  theme={null}
  claude --system-prompt-file ./prompts/code-review.txt
  ```

* **`--append-system-prompt`**：Claude Code のデフォルト機能を保持しながら特定の指示を追加したい場合に使用します。これはほとんどのユースケースで最も安全なオプションです。
  ```bash  theme={null}
  claude --append-system-prompt "Always use TypeScript and include JSDoc comments"
  ```

* **`--append-system-prompt-file`**：Claude Code のデフォルトを保持しながらファイルから指示を追加したい場合に使用します。バージョン管理された追加に役立ちます。
  ```bash  theme={null}
  claude --append-system-prompt-file ./prompts/style-rules.txt
  ```

`--system-prompt` と `--system-prompt-file` は相互に排他的です。追加フラグは、置き換えフラグのいずれかと一緒に使用できます。

ほとんどのユースケースでは、`--append-system-prompt` または `--append-system-prompt-file` が推奨されます。これらは Claude Code の組み込み機能を保持しながらカスタム要件を追加します。システムプロンプトを完全に制御する必要がある場合にのみ `--system-prompt` または `--system-prompt-file` を使用してください。

## 関連項目

* [Chrome 拡張機能](/ja/chrome) - ブラウザ自動化と Web テスト
* [インタラクティブモード](/ja/interactive-mode) - ショートカット、入力モード、インタラクティブ機能
* [クイックスタートガイド](/ja/quickstart) - Claude Code の開始方法
* [一般的なワークフロー](/ja/common-workflows) - 高度なワークフローとパターン
* [設定](/ja/settings) - 設定オプション
* [Agent SDK ドキュメント](https://platform.claude.com/docs/en/agent-sdk/overview) - プログラム的な使用と統合
