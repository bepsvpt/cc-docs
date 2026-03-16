> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Hooks リファレンス

> Claude Code のフック イベント、設定スキーマ、JSON 入出力形式、終了コード、非同期フック、HTTP フック、プロンプト フック、MCP ツール フックのリファレンス。

<Tip>
  例を含むクイックスタート ガイドについては、[ワークフローをフックで自動化する](/ja/hooks-guide)を参照してください。
</Tip>

フックは、Claude Code のライフサイクル内の特定のポイントで自動的に実行されるユーザー定義のシェル コマンド、HTTP エンドポイント、または LLM プロンプトです。このリファレンスを使用して、イベント スキーマ、設定オプション、JSON 入出力形式、および非同期フック、HTTP フック、MCP ツール フックなどの高度な機能を検索してください。初めてフックを設定する場合は、代わりに[ガイド](/ja/hooks-guide)から始めてください。

## フック ライフサイクル

フックは Claude Code セッション中の特定のポイントで発火します。イベントが発火し、マッチャーがマッチすると、Claude Code はイベントに関する JSON コンテキストをフック ハンドラーに渡します。コマンド フックの場合、入力は stdin で到着します。HTTP フックの場合、POST リクエスト本体として到着します。ハンドラーは入力を検査し、アクションを実行し、オプションで決定を返すことができます。一部のイベントはセッションごとに 1 回発火しますが、他のイベントは agentic ループ内で繰り返し発火します。

<div style={{maxWidth: "500px", margin: "0 auto"}}>
  <Frame>
    <img src="https://mintcdn.com/claude-code/lBsitdsGyD9caWJQ/images/hooks-lifecycle.svg?fit=max&auto=format&n=lBsitdsGyD9caWJQ&q=85&s=be3486ef2cf2563eb213b6cbbce93982" alt="SessionStart から agentic ループを経由して SessionEnd までのフックのシーケンスを示すフック ライフサイクル図。WorktreeCreate、WorktreeRemove、InstructionsLoaded はスタンドアロン非同期イベント" width="520" height="1100" data-path="images/hooks-lifecycle.svg" />
  </Frame>
</div>

以下の表は、各イベントがいつ発火するかをまとめています。[フック イベント](#hook-events)セクションでは、各イベントの完全な入力スキーマと決定制御オプションについて説明しています。

| Event                | When it fires                                                                                                                                  |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                               |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                           |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                      |
| `PermissionRequest`  | When a permission dialog appears                                                                                                               |
| `PostToolUse`        | After a tool call succeeds                                                                                                                     |
| `PostToolUseFailure` | After a tool call fails                                                                                                                        |
| `Notification`       | When Claude Code sends a notification                                                                                                          |
| `SubagentStart`      | When a subagent is spawned                                                                                                                     |
| `SubagentStop`       | When a subagent finishes                                                                                                                       |
| `Stop`               | When Claude finishes responding                                                                                                                |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                             |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                       |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session |
| `ConfigChange`       | When a configuration file changes during a session                                                                                             |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                    |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                           |
| `PreCompact`         | Before context compaction                                                                                                                      |
| `PostCompact`        | After context compaction completes                                                                                                             |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                      |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                    |
| `SessionEnd`         | When a session terminates                                                                                                                      |

### フックがどのように解決されるか

これらの部分がどのように組み合わさるかを確認するために、破壊的なシェル コマンドをブロックする `PreToolUse` フックを考えてみましょう。フックは Bash ツール呼び出しの前に `block-rm.sh` を実行します。

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

スクリプトは stdin から JSON 入力を読み取り、コマンドを抽出し、`rm -rf` が含まれている場合は `permissionDecision` の `"deny"` を返します。

```bash  theme={null}
#!/bin/bash
# .claude/hooks/block-rm.sh
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0  # allow the command
fi
```

ここで Claude Code が `Bash "rm -rf /tmp/build"` を実行することを決定したとします。以下が起こります。

<Frame>
  <img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/hook-resolution.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=ad667ee6d86ab2276aa48a4e73e220df" alt="フック解決フロー: PreToolUse イベントが発火し、マッチャーが Bash マッチをチェックし、フック ハンドラーが実行され、結果が Claude Code に返される" width="780" height="290" data-path="images/hook-resolution.svg" />
</Frame>

<Steps>
  <Step title="イベントが発火">
    `PreToolUse` イベントが発火します。Claude Code はツール入力を JSON として stdin でフックに送信します。

    ```json  theme={null}
    { "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
    ```
  </Step>

  <Step title="マッチャーがチェック">
    マッチャー `"Bash"` がツール名にマッチするため、`block-rm.sh` が実行されます。マッチャーを省略するか `"*"` を使用すると、フックはイベントのすべての出現で実行されます。マッチャーが定義されていてマッチしない場合にのみ、フックはスキップされます。
  </Step>

  <Step title="フック ハンドラーが実行">
    スクリプトは入力から `"rm -rf /tmp/build"` を抽出し、`rm -rf` を見つけるため、決定を stdout に出力します。

    ```json  theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Destructive command blocked by hook"
      }
    }
    ```

    コマンドが安全だった場合（`npm test` など）、スクリプトは代わりに `exit 0` に到達し、これは Claude Code にツール呼び出しを許可するよう指示します。
  </Step>

  <Step title="Claude Code が結果に基づいて行動">
    Claude Code は JSON 決定を読み取り、ツール呼び出しをブロックし、Claude に理由を表示します。
  </Step>
</Steps>

以下の[設定](#configuration)セクションでは完全なスキーマについて説明し、各[フック イベント](#hook-events)セクションでは、コマンドが受け取る入力と返すことができる出力について説明しています。

## 設定

フックは JSON 設定ファイルで定義されます。設定には 3 つのネストレベルがあります。

1. 応答する[フック イベント](#hook-events)を選択します（`PreToolUse` や `Stop` など）
2. 発火するタイミングをフィルタリングする[マッチャー グループ](#matcher-patterns)を追加します（'Bash ツールのみ'など）
3. マッチしたときに実行する 1 つ以上の[フック ハンドラー](#hook-handler-fields)を定義します

完全なウォークスルーと注釈付きの例については、上記の[フックがどのように解決されるか](#how-a-hook-resolves)を参照してください。

<Note>
  このページでは各レベルに特定の用語を使用しています。ライフサイクル ポイントの場合は**フック イベント**、フィルターの場合は**マッチャー グループ**、実行されるシェル コマンド、HTTP エンドポイント、プロンプト、またはエージェントの場合は**フック ハンドラー**です。'フック'単独は一般的な機能を指します。
</Note>

### フック位置

フックを定義する場所によって、そのスコープが決まります。

| 位置                                                  | スコープ             | 共有可能               |
| :-------------------------------------------------- | :--------------- | :----------------- |
| `~/.claude/settings.json`                           | すべてのプロジェクト       | いいえ、マシンローカル        |
| `.claude/settings.json`                             | 単一プロジェクト         | はい、リポジトリにコミット可能    |
| `.claude/settings.local.json`                       | 単一プロジェクト         | いいえ、gitignored     |
| 管理ポリシー設定                                            | 組織全体             | はい、管理者制御           |
| [プラグイン](/ja/plugins) `hooks/hooks.json`             | プラグインが有効な場合      | はい、プラグインにバンドル      |
| [スキル](/ja/skills)または[エージェント](/ja/sub-agents)フロントマター | コンポーネントがアクティブな場合 | はい、コンポーネント ファイルで定義 |

設定ファイル解決の詳細については、[設定](/ja/settings)を参照してください。エンタープライズ管理者は `allowManagedHooksOnly` を使用して、ユーザー、プロジェクト、プラグイン フックをブロックできます。[フック設定](/ja/settings#hook-configuration)を参照してください。

### マッチャー パターン

`matcher` フィールドは、フックが発火するタイミングをフィルタリングする正規表現文字列です。すべての出現にマッチするには、`"*"`、`""`、または `matcher` を完全に省略します。各イベント タイプは異なるフィールドでマッチします。

| イベント                                                                                                            | マッチャーがフィルタリングするもの | マッチャー値の例                                                                       |
| :-------------------------------------------------------------------------------------------------------------- | :---------------- | :----------------------------------------------------------------------------- |
| `PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest`                                             | ツール名              | `Bash`、`Edit\|Write`、`mcp__.*`                                                 |
| `SessionStart`                                                                                                  | セッションの開始方法        | `startup`、`resume`、`clear`、`compact`                                           |
| `SessionEnd`                                                                                                    | セッションが終了した理由      | `clear`、`logout`、`prompt_input_exit`、`bypass_permissions_disabled`、`other`     |
| `Notification`                                                                                                  | 通知タイプ             | `permission_prompt`、`idle_prompt`、`auth_success`、`elicitation_dialog`          |
| `SubagentStart`                                                                                                 | エージェント タイプ        | `Bash`、`Explore`、`Plan`、またはカスタム エージェント名                                        |
| `PreCompact`                                                                                                    | コンパクション をトリガーしたもの | `manual`、`auto`                                                                |
| `SubagentStop`                                                                                                  | エージェント タイプ        | `SubagentStart` と同じ値                                                           |
| `ConfigChange`                                                                                                  | 設定ソース             | `user_settings`、`project_settings`、`local_settings`、`policy_settings`、`skills` |
| `UserPromptSubmit`、`Stop`、`TeammateIdle`、`TaskCompleted`、`WorktreeCreate`、`WorktreeRemove`、`InstructionsLoaded` | マッチャー サポートなし      | すべての出現で常に発火                                                                    |

マッチャーは正規表現であるため、`Edit|Write` は両方のツールにマッチし、`Notebook.*` は Notebook で始まるツールにマッチします。マッチャーは、Claude Code がフックに stdin で送信する[JSON 入力](#hook-input-and-output)のフィールドに対して実行されます。ツール イベントの場合、そのフィールドは `tool_name` です。各[フック イベント](#hook-events)セクションでは、マッチャー値の完全なセットとそのイベントの入力スキーマをリストしています。

この例は、Claude がファイルを書き込むまたは編集するときにのみリント スクリプトを実行します。

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```

`UserPromptSubmit`、`Stop`、`TeammateIdle`、`TaskCompleted`、`WorktreeCreate`、`WorktreeRemove`、`InstructionsLoaded` はマッチャーをサポートせず、すべての出現で常に発火します。これらのイベントに `matcher` フィールドを追加すると、サイレントに無視されます。

#### MCP ツールをマッチ

[MCP](/ja/mcp) サーバー ツールはツール イベント（`PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest`）で通常のツールとして表示されるため、他のツール名と同じ方法でマッチできます。

MCP ツールは `mcp__<server>__<tool>` という命名パターンに従います。例えば、

* `mcp__memory__create_entities`: Memory サーバーの create entities ツール
* `mcp__filesystem__read_file`: Filesystem サーバーの read file ツール
* `mcp__github__search_repositories`: GitHub サーバーの search ツール

正規表現パターンを使用して、特定の MCP ツールまたはツール グループをターゲットにします。

* `mcp__memory__.*` は `memory` サーバーのすべてのツールにマッチします
* `mcp__.*__write.*` はいずれかのサーバーから「write」を含むツールにマッチします

この例は、すべてのメモリ サーバー操作をログに記録し、任意の MCP サーバーからの書き込み操作を検証します。

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

### フック ハンドラー フィールド

内側の `hooks` 配列の各オブジェクトはフック ハンドラーです。マッチャーがマッチしたときに実行されるシェル コマンド、HTTP エンドポイント、LLM プロンプト、またはエージェントです。4 つのタイプがあります。

* **[コマンド フック](#command-hook-fields)**（`type: "command"`）: シェル コマンドを実行します。スクリプトはイベントの[JSON 入力](#hook-input-and-output)を stdin で受け取り、終了コードと stdout を通じて結果を通信します。
* **[HTTP フック](#http-hook-fields)**（`type: "http"`）: イベントの JSON 入力を HTTP POST リクエストとして URL に送信します。エンドポイントは、コマンド フックと同じ[JSON 出力形式](#json-output)を使用して、レスポンス本体を通じて結果を通信します。
* **[プロンプト フック](#prompt-and-agent-hook-fields)**（`type: "prompt"`）: Claude モデルにプロンプトを送信して、単一ターン評価を行います。モデルは yes/no 決定を JSON として返します。[プロンプト ベースのフック](#prompt-based-hooks)を参照してください。
* **[エージェント フック](#prompt-and-agent-hook-fields)**（`type: "agent"`）: Read、Grep、Glob などのツールを使用して条件を検証してから決定を返すことができるサブエージェントを生成します。[エージェント ベースのフック](#agent-based-hooks)を参照してください。

#### 共通フィールド

これらのフィールドはすべてのフック タイプに適用されます。

| フィールド           | 必須  | 説明                                                                                                               |
| :-------------- | :-- | :--------------------------------------------------------------------------------------------------------------- |
| `type`          | はい  | `"command"`、`"http"`、`"prompt"`、または `"agent"`                                                                    |
| `timeout`       | いいえ | キャンセルするまでの秒数。デフォルト: コマンドは 600、プロンプトは 30、エージェントは 60                                                               |
| `statusMessage` | いいえ | フックの実行中に表示されるカスタム スピナー メッセージ                                                                                     |
| `once`          | いいえ | `true` の場合、セッションごとに 1 回だけ実行してから削除されます。スキルのみ、エージェントではありません。[スキルとエージェントのフック](#hooks-in-skills-and-agents)を参照してください |

#### コマンド フック フィールド

[共通フィールド](#common-fields)に加えて、コマンド フックはこれらのフィールドを受け入れます。

| フィールド     | 必須  | 説明                                                                                         |
| :-------- | :-- | :----------------------------------------------------------------------------------------- |
| `command` | はい  | 実行するシェル コマンド                                                                               |
| `async`   | いいえ | `true` の場合、ブロックせずにバックグラウンドで実行されます。[バックグラウンドでフックを実行](#run-hooks-in-the-background)を参照してください |

#### HTTP フック フィールド

[共通フィールド](#common-fields)に加えて、HTTP フックはこれらのフィールドを受け入れます。

| フィールド            | 必須  | 説明                                                                                                                 |
| :--------------- | :-- | :----------------------------------------------------------------------------------------------------------------- |
| `url`            | はい  | POST リクエストを送信する URL                                                                                                |
| `headers`        | いいえ | キー値ペアとしての追加 HTTP ヘッダー。値は `$VAR_NAME` または `${VAR_NAME}` 構文を使用した環境変数補間をサポートします。`allowedEnvVars` にリストされている変数のみが解決されます |
| `allowedEnvVars` | いいえ | ヘッダー値に補間される可能性のある環境変数名のリスト。リストされていない変数への参照は空の文字列に置き換えられます。環境変数補間が機能するために必須です                                       |

Claude Code はフックの[JSON 入力](#hook-input-and-output)を `Content-Type: application/json` の POST リクエスト本体として送信します。レスポンス本体はコマンド フックと同じ[JSON 出力形式](#json-output)を使用します。

エラー処理はコマンド フックと異なります。2xx 以外のレスポンス、接続失敗、タイムアウトはすべて、実行を続行できる非ブロッキング エラーを生成します。ツール呼び出しをブロックまたは権限を拒否するには、`decision: "block"` または `permissionDecision: "deny"` を含む JSON 本体を持つ 2xx レスポンスを返します。

この例は、`PreToolUse` イベントをローカル検証サービスに送信し、`MY_TOKEN` 環境変数からのトークンで認証します。

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/pre-tool-use",
            "timeout": 30,
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

<Note>
  HTTP フックは設定 JSON を直接編集して設定する必要があります。`/hooks` インタラクティブ メニューはコマンド フックの追加のみをサポートしています。
</Note>

#### プロンプト フックとエージェント フック フィールド

[共通フィールド](#common-fields)に加えて、プロンプト フックとエージェント フックはこれらのフィールドを受け入れます。

| フィールド    | 必須  | 説明                                                             |
| :------- | :-- | :------------------------------------------------------------- |
| `prompt` | はい  | モデルに送信するプロンプト テキスト。フック入力 JSON のプレースホルダーとして `$ARGUMENTS` を使用します |
| `model`  | いいえ | 評価に使用するモデル。デフォルトは高速モデル                                         |

マッチするすべてのフックは並列で実行され、同一のハンドラーは自動的に重複排除されます。コマンド フックはコマンド文字列で重複排除され、HTTP フックは URL で重複排除されます。ハンドラーは Claude Code の環境で現在のディレクトリで実行されます。`$CLAUDE_CODE_REMOTE` 環境変数はリモート Web 環境で `"true"` に設定され、ローカル CLI では設定されません。

### パスでスクリプトを参照

環境変数を使用して、フック スクリプトをプロジェクトまたはプラグイン ルートを基準に参照し、フックが実行されるときの作業ディレクトリに関係なく参照します。

* `$CLAUDE_PROJECT_DIR`: プロジェクト ルート。スペースを含むパスを処理するために引用符で囲みます。
* `${CLAUDE_PLUGIN_ROOT}`: プラグインのルート ディレクトリ。[プラグイン](/ja/plugins)にバンドルされたスクリプト用です。

<Tabs>
  <Tab title="プロジェクト スクリプト">
    この例は `$CLAUDE_PROJECT_DIR` を使用して、`Write` または `Edit` ツール呼び出しの後、プロジェクトの `.claude/hooks/` ディレクトリからスタイル チェッカーを実行します。

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="プラグイン スクリプト">
    `hooks/hooks.json` でプラグイン フックを定義し、オプションのトップレベル `description` フィールドを含めます。プラグインが有効な場合、そのフックはユーザーおよびプロジェクト フックとマージされます。

    この例は、プラグインにバンドルされたフォーマット スクリプトを実行します。

    ```json  theme={null}
    {
      "description": "Automatic code formatting",
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
                "timeout": 30
              }
            ]
          }
        ]
      }
    }
    ```

    プラグイン フックの作成の詳細については、[プラグイン コンポーネント リファレンス](/ja/plugins-reference#hooks)を参照してください。
  </Tab>
</Tabs>

### スキルとエージェントのフック

設定ファイルとプラグインに加えて、フックはフロントマターを使用して[スキル](/ja/skills)と[サブエージェント](/ja/sub-agents)で直接定義できます。これらのフックはコンポーネントのライフサイクルにスコープされ、そのコンポーネントがアクティブな場合にのみ実行されます。

すべてのフック イベントがサポートされています。サブエージェントの場合、`Stop` フックは自動的に `SubagentStop` に変換されます。これはサブエージェントが完了したときに発火するイベントです。

フックは設定ベースのフックと同じ設定形式を使用しますが、コンポーネントの有効期間にスコープされ、完了時にクリーンアップされます。

このスキルは、各 `Bash` コマンドの前にセキュリティ検証スクリプトを実行する `PreToolUse` フックを定義します。

```yaml  theme={null}
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

エージェントは YAML フロントマターで同じ形式を使用します。

### `/hooks` メニュー

Claude Code で `/hooks` と入力して、インタラクティブ フック マネージャーを開きます。ここで、設定ファイルを直接編集せずにフックを表示、追加、削除できます。ステップバイステップのウォークスルーについては、ガイドの[最初のフックを設定](/ja/hooks-guide#set-up-your-first-hook)を参照してください。

メニュー内の各フックには、ソースを示すブラケット プレフィックスがラベル付けされています。

* `[User]`: `~/.claude/settings.json` から
* `[Project]`: `.claude/settings.json` から
* `[Local]`: `.claude/settings.local.json` から
* `[Plugin]`: プラグインの `hooks/hooks.json` から、読み取り専用

### フックを無効化または削除

フックを削除するには、設定 JSON ファイルからそのエントリを削除するか、`/hooks` メニューを使用してフックを選択して削除します。

すべてのフックを削除せずに一時的に無効化するには、設定ファイルで `"disableAllHooks": true` を設定するか、`/hooks` メニューのトグルを使用します。個別のフックを設定に保持したまま無効化する方法はありません。

`disableAllHooks` 設定は管理設定階層を尊重します。管理者が管理ポリシー設定を通じてフックを設定している場合、ユーザー、プロジェクト、またはローカル設定で設定された `disableAllHooks` はそれらの管理フックを無効化できません。管理設定レベルで設定された `disableAllHooks` のみが管理フックを無効化できます。

設定ファイルのフックへの直接編集は即座には有効になりません。Claude Code はスタートアップ時にフックのスナップショットをキャプチャし、セッション全体で使用します。これにより、悪意のある、または偶発的なフック変更がセッション中盤に有効になるのを防ぎます。フックが外部で変更された場合、Claude Code は警告を表示し、変更が適用される前に `/hooks` メニューでレビューが必要です。

## フック入出力

コマンド フックは stdin 経由で JSON データを受け取り、終了コード、stdout、stderr を通じて結果を通信します。HTTP フックは同じ JSON を POST リクエスト本体として受け取り、HTTP レスポンス本体を通じて結果を通信します。このセクションでは、すべてのイベントに共通するフィールドと動作について説明します。[フック イベント](#hook-events)の各セクションには、その特定の入力スキーマと決定制御オプションが含まれています。

### 共通入力フィールド

すべてのフック イベントは、各[フック イベント](#hook-events)セクションで説明されているイベント固有のフィールドに加えて、これらのフィールドを JSON として受け取ります。コマンド フックの場合、この JSON は stdin 経由で到着します。HTTP フックの場合、POST リクエスト本体として到着します。

| フィールド             | 説明                                                                                                                       |
| :---------------- | :----------------------------------------------------------------------------------------------------------------------- |
| `session_id`      | 現在のセッション識別子                                                                                                              |
| `transcript_path` | 会話 JSON へのパス                                                                                                             |
| `cwd`             | フックが呼び出されるときの現在の作業ディレクトリ                                                                                                 |
| `permission_mode` | 現在の[権限モード](/ja/permissions#permission-modes): `"default"`、`"plan"`、`"acceptEdits"`、`"dontAsk"`、または `"bypassPermissions"` |
| `hook_event_name` | 発火したイベントの名前                                                                                                              |

`--agent` で実行するか、サブエージェント内で実行する場合、2 つの追加フィールドが含まれます。

| フィールド        | 説明                                                                                                                                                          |
| :----------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id`   | サブエージェントの一意の識別子。フックがサブエージェント呼び出し内で発火する場合にのみ存在します。サブエージェント フック呼び出しをメイン スレッド呼び出しから区別するために使用します。                                                               |
| `agent_type` | エージェント名（例えば、`"Explore"` または `"security-reviewer"`）。セッションが `--agent` を使用するか、フックがサブエージェント内で発火する場合に存在します。サブエージェントの場合、サブエージェントのタイプがセッションの `--agent` 値よりも優先されます。 |

例えば、Bash コマンドの `PreToolUse` フックは stdin で以下を受け取ります。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

`tool_name` と `tool_input` フィールドはイベント固有です。各[フック イベント](#hook-events)セクションでは、そのイベントの追加フィールドについて説明しています。

### 終了コード出力

フック コマンドからの終了コードは、Claude Code にアクションを続行するか、ブロックするか、無視するかを指示します。

**終了 0** は成功を意味します。Claude Code は stdout を[JSON 出力フィールド](#json-output)で解析します。JSON 出力は終了 0 でのみ処理されます。ほとんどのイベントでは、stdout は詳細モード（`Ctrl+O`）でのみ表示されます。例外は `UserPromptSubmit` と `SessionStart` で、stdout は Claude が見て行動できるコンテキストとして追加されます。

**終了 2** はブロッキング エラーを意味します。Claude Code は stdout と JSON を無視します。代わりに、stderr テキストが Claude にエラー メッセージとしてフィードバックされます。効果はイベントに依存します。`PreToolUse` はツール呼び出しをブロックし、`UserPromptSubmit` はプロンプトを拒否します。詳細については、[終了コード 2 動作](#exit-code-2-behavior-per-event)を参照してください。

**その他の終了コード** は非ブロッキング エラーです。stderr は詳細モード（`Ctrl+O`）で表示され、実行は続行されます。

例えば、危険な Bash コマンドをブロックするフック コマンド スクリプト。

```bash  theme={null}
#!/bin/bash
# stdin から JSON 入力を読み取り、コマンドをチェック
command=$(jq -r '.tool_input.command' < /dev/stdin)

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # ブロッキング エラー: ツール呼び出しが防止される
fi

exit 0  # 成功: ツール呼び出しが続行される
```

#### イベントごとの終了コード 2 動作

終了コード 2 は、フックが「停止、これをしないでください」と通知する方法です。効果はイベントに依存します。一部のイベントはブロック可能なアクション（まだ発生していないツール呼び出しなど）を表し、他のイベントはすでに発生したか防止できないことを表します。

| フック イベント             | ブロック可能？ | 終了 2 で何が起こるか                            |
| :------------------- | :------ | :-------------------------------------- |
| `PreToolUse`         | はい      | ツール呼び出しをブロック                            |
| `PermissionRequest`  | はい      | 権限を拒否                                   |
| `UserPromptSubmit`   | はい      | プロンプト処理をブロックしてプロンプトを消去                  |
| `Stop`               | はい      | Claude が停止するのを防ぎ、会話を続行                  |
| `SubagentStop`       | はい      | サブエージェントが停止するのを防止                       |
| `TeammateIdle`       | はい      | チームメイトがアイドル状態になるのを防止（チームメイトが作業を続行）      |
| `TaskCompleted`      | はい      | タスクが完了としてマークされるのを防止                     |
| `ConfigChange`       | はい      | 設定変更が有効になるのをブロック（`policy_settings` を除く） |
| `PostToolUse`        | いいえ     | Claude に stderr を表示（ツールはすでに実行）          |
| `PostToolUseFailure` | いいえ     | Claude に stderr を表示（ツールはすでに失敗）          |
| `Notification`       | いいえ     | ユーザーのみに stderr を表示                      |
| `SubagentStart`      | いいえ     | ユーザーのみに stderr を表示                      |
| `SessionStart`       | いいえ     | ユーザーのみに stderr を表示                      |
| `SessionEnd`         | いいえ     | ユーザーのみに stderr を表示                      |
| `PreCompact`         | いいえ     | ユーザーのみに stderr を表示                      |
| `WorktreeCreate`     | はい      | 0 以外の終了コードはワークツリー作成を失敗させる               |
| `WorktreeRemove`     | いいえ     | 失敗はデバッグ モードでのみログに記録                     |
| `InstructionsLoaded` | いいえ     | 終了コードは無視される                             |

### HTTP レスポンス処理

HTTP フックは終了コードと stdout の代わりに HTTP ステータス コードとレスポンス本体を使用します。

* **2xx で空の本体**: 成功、終了コード 0 で出力なしと同等
* **2xx でプレーン テキスト本体**: 成功、テキストがコンテキストとして追加される
* **2xx で JSON 本体**: 成功、コマンド フックと同じ[JSON 出力](#json-output)スキーマを使用して解析
* **2xx 以外のステータス**: 非ブロッキング エラー、実行は続行
* **接続失敗またはタイムアウト**: 非ブロッキング エラー、実行は続行

コマンド フックとは異なり、HTTP フックはステータス コードのみでブロッキング エラーを通知できません。ツール呼び出しをブロックまたは権限を拒否するには、適切な決定フィールドを含む JSON 本体を持つ 2xx レスポンスを返します。

### JSON 出力

終了コードでは許可またはブロックできますが、JSON 出力はより細かい制御を提供します。終了コード 2 でブロックする代わりに、終了 0 して JSON オブジェクトを stdout に出力します。Claude Code はその JSON から特定のフィールドを読み取り、ブロック、許可、またはユーザーへのエスカレーションを含む動作を制御します。

<Note>
  フックごとに 1 つのアプローチを選択する必要があります。両方ではありません。終了コードのみでシグナリングするか、終了 0 して構造化制御のために JSON を出力するかです。Claude Code は終了 0 でのみ JSON を処理します。終了 2 の場合、JSON は無視されます。
</Note>

フックの stdout には JSON オブジェクトのみが含まれている必要があります。シェル プロファイルがスタートアップ時にテキストを出力する場合、JSON 解析に干渉する可能性があります。トラブルシューティング ガイドの[JSON 検証に失敗](/ja/hooks-guide#json-validation-failed)を参照してください。

JSON オブジェクトは 3 種類のフィールドをサポートしています。

* **`continue` などのユニバーサル フィールド** はすべてのイベントで機能します。これらは以下の表にリストされています。
* **トップレベルの `decision` と `reason`** は一部のイベントで使用され、ブロックまたはフィードバックを提供します。
* **`hookSpecificOutput`** はより豊かな制御が必要なイベント用のネストされたオブジェクトです。イベント名に設定された `hookEventName` フィールドが必要です。

| フィールド            | デフォルト   | 説明                                                             |
| :--------------- | :------ | :------------------------------------------------------------- |
| `continue`       | `true`  | `false` の場合、フック実行後 Claude は完全に処理を停止します。イベント固有の決定フィールドよりも優先されます |
| `stopReason`     | なし      | `continue` が `false` のときにユーザーに表示されるメッセージ。Claude には表示されません      |
| `suppressOutput` | `false` | `true` の場合、詳細モード出力から stdout を非表示にします                           |
| `systemMessage`  | なし      | ユーザーに表示される警告メッセージ                                              |

Claude を完全に停止するには、イベント タイプに関係なく。

```json  theme={null}
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

#### 決定制御

すべてのイベントが JSON を通じたブロッキングまたは動作制御をサポートしているわけではありません。サポートするイベントは、その決定を表現するために異なるフィールド セットを使用します。フックを書く前に、このテーブルをクイック リファレンスとして使用してください。

| イベント                                                                           | 決定パターン                     | キー フィールド                                                                                                                   |
| :----------------------------------------------------------------------------- | :------------------------- | :------------------------------------------------------------------------------------------------------------------------- |
| UserPromptSubmit、PostToolUse、PostToolUseFailure、Stop、SubagentStop、ConfigChange | トップレベル `decision`          | `decision: "block"`、`reason`                                                                                               |
| TeammateIdle、TaskCompleted                                                     | 終了コードまたは `continue: false` | 終了コード 2 はアクションをブロックし、stderr フィードバックを提供します。JSON `{"continue": false, "stopReason": "..."}` はチームメイト全体を停止し、`Stop` フック動作と一致します |
| PreToolUse                                                                     | `hookSpecificOutput`       | `permissionDecision`（allow/deny/ask）、`permissionDecisionReason`                                                            |
| PermissionRequest                                                              | `hookSpecificOutput`       | `decision.behavior`（allow/deny）                                                                                            |
| WorktreeCreate                                                                 | stdout パス                  | フックは作成されたワークツリーへの絶対パスを出力します。0 以外の終了は作成を失敗させます                                                                              |
| WorktreeRemove、Notification、SessionEnd、PreCompact、InstructionsLoaded           | なし                         | 決定制御なし。ログやクリーンアップなどの副作用に使用                                                                                                 |

各パターンの実行例を以下に示します。

<Tabs>
  <Tab title="トップレベル決定">
    `UserPromptSubmit`、`PostToolUse`、`PostToolUseFailure`、`Stop`、`SubagentStop`、`ConfigChange` で使用されます。唯一の値は `"block"` です。アクションを続行させるには、JSON から `decision` を省略するか、JSON なしで終了 0 で終了します。

    ```json  theme={null}
    {
      "decision": "block",
      "reason": "Test suite must pass before proceeding"
    }
    ```
  </Tab>

  <Tab title="PreToolUse">
    より豊かな制御のために `hookSpecificOutput` を使用します。許可、拒否、またはユーザーへのエスカレーション。ツール入力を実行前に変更したり、Claude 用に追加コンテキストを注入することもできます。オプションの完全なセットについては、[PreToolUse 決定制御](#pretooluse-decision-control)を参照してください。

    ```json  theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Database writes are not allowed"
      }
    }
    ```
  </Tab>

  <Tab title="PermissionRequest">
    `hookSpecificOutput` を使用して、ユーザーに代わって権限リクエストを許可または拒否します。許可する場合、ツールの入力を変更したり、権限ルールを適用して、ユーザーが再度プロンプトされないようにすることもできます。オプションの完全なセットについては、[PermissionRequest 決定制御](#permissionrequest-decision-control)を参照してください。

    ```json  theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PermissionRequest",
        "decision": {
          "behavior": "allow",
          "updatedInput": {
            "command": "npm run lint"
          }
        }
      }
    }
    ```
  </Tab>
</Tabs>

Bash コマンド検証、プロンプト フィルタリング、自動承認スクリプトを含む拡張例については、ガイドの[自動化できること](/ja/hooks-guide#what-you-can-automate)と[Bash コマンド バリデーター リファレンス実装](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)を参照してください。

## フック イベント

各イベントは Claude Code のライフサイクル内のポイントに対応し、フックが実行できます。以下のセクションはライフサイクルに一致するように順序付けられています。セッション セットアップから agentic ループを経由してセッション終了まで。各セクションでは、イベントがいつ発火するか、サポートするマッチャー、受け取る JSON 入力、出力を通じた動作制御方法について説明しています。

### SessionStart

新しいセッションを開始するか、既存のセッションを再開するときに実行されます。既存の問題や最近のコードベース変更など、開発コンテキストを読み込んだり、環境変数を設定したりするのに便利です。静的コンテキストでスクリプトが不要な場合は、代わりに[CLAUDE.md](/ja/memory)を使用してください。

SessionStart はすべてのセッションで実行されるため、これらのフックを高速に保ちます。`type: "command"` フックのみがサポートされています。

マッチャー値はセッションがどのように開始されたかに対応します。

| マッチャー     | いつ発火するか                               |
| :-------- | :------------------------------------ |
| `startup` | 新しいセッション                              |
| `resume`  | `--resume`、`--continue`、または `/resume` |
| `clear`   | `/clear`                              |
| `compact` | 自動またはマニュアル コンパクション                    |

#### SessionStart 入力

[共通入力フィールド](#common-input-fields)に加えて、SessionStart フックは `source`、`model`、およびオプションで `agent_type` を受け取ります。`source` フィールドはセッションがどのように開始されたかを示します。新しいセッションの場合は `"startup"`、再開されたセッションの場合は `"resume"`、`/clear` の後は `"clear"`、コンパクション後は `"compact"`。`model` フィールドはモデル識別子を含みます。`claude --agent <name>` で Claude Code を開始する場合、`agent_type` フィールドはエージェント名を含みます。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-6"
}
```

#### SessionStart 決定制御

フック スクリプトが stdout に出力するテキストは Claude のコンテキストとして追加されます。すべてのフックで利用可能な[JSON 出力フィールド](#json-output)に加えて、これらのイベント固有のフィールドを返すことができます。

| フィールド               | 説明                                      |
| :------------------ | :-------------------------------------- |
| `additionalContext` | Claude のコンテキストに追加される文字列。複数のフックの値は連結されます |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

#### 環境変数を永続化

SessionStart フックは `CLAUDE_ENV_FILE` 環境変数にアクセスでき、後続の Bash コマンド用に環境変数を永続化できるファイル パスを提供します。

個別の環境変数を設定するには、`CLAUDE_ENV_FILE` に `export` ステートメントを書き込みます。他のフックで設定された変数を保持するには、追加（`>>`）を使用します。

```bash  theme={null}
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

セットアップ コマンドからのすべての環境変更をキャプチャするには、前後でエクスポートされた変数を比較します。

```bash  theme={null}
#!/bin/bash

ENV_BEFORE=$(export -p | sort)

# 環境を変更するセットアップ コマンドを実行
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

このファイルに書き込まれた変数は、セッション中に Claude Code が実行するすべての後続の Bash コマンドで利用可能になります。

<Note>
  `CLAUDE_ENV_FILE` は SessionStart フックで利用可能です。他のフック タイプはこの変数にアクセスできません。
</Note>

### InstructionsLoaded

`CLAUDE.md` または `.claude/rules/*.md` ファイルがコンテキストに読み込まれるときに発火します。このイベントはセッション開始時に熱心に読み込まれたファイルに対して発火し、後で遅延読み込みされたときに再度発火します。例えば、Claude がネストされた `CLAUDE.md` を含むサブディレクトリにアクセスするか、`paths:` フロントマターを持つ条件付きルールがマッチするとき。フックはブロッキングまたは決定制御をサポートしていません。観測可能性の目的で非同期に実行されます。

InstructionsLoaded はマッチャーをサポートせず、すべての読み込み出現で発火します。

#### InstructionsLoaded 入力

[共通入力フィールド](#common-input-fields)に加えて、InstructionsLoaded フックはこれらのフィールドを受け取ります。

| フィールド               | 説明                                                                                        |
| :------------------ | :---------------------------------------------------------------------------------------- |
| `file_path`         | 読み込まれた命令ファイルへの絶対パス                                                                        |
| `memory_type`       | ファイルのスコープ: `"User"`、`"Project"`、`"Local"`、または `"Managed"`                                 |
| `load_reason`       | ファイルが読み込まれた理由: `"session_start"`、`"nested_traversal"`、`"path_glob_match"`、または `"include"` |
| `globs`             | ファイルの `paths:` フロントマターからのパス グロブ パターン（存在する場合）。`path_glob_match` 読み込みの場合のみ存在                |
| `trigger_file_path` | 遅延読み込みの場合、この読み込みをトリガーしたファイルへのパス                                                           |
| `parent_file_path`  | `include` 読み込みの場合、このファイルを含む親命令ファイルへのパス                                                    |

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "permission_mode": "default",
  "hook_event_name": "InstructionsLoaded",
  "file_path": "/Users/my-project/CLAUDE.md",
  "memory_type": "Project",
  "load_reason": "session_start"
}
```

#### InstructionsLoaded 決定制御

InstructionsLoaded フックは決定制御がありません。命令読み込みをブロックまたは変更できません。このイベントを監査ログ、コンプライアンス追跡、または観測可能性に使用します。

### UserPromptSubmit

ユーザーがプロンプトを送信するときに実行されます。Claude がそれを処理する前です。これにより、プロンプト/会話に基づいて追加コンテキストを追加したり、プロンプトを検証したり、特定のタイプのプロンプトをブロックしたりできます。

#### UserPromptSubmit 入力

[共通入力フィールド](#common-input-fields)に加えて、UserPromptSubmit フックはユーザーが送信したテキストを含む `prompt` フィールドを受け取ります。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

#### UserPromptSubmit 決定制御

`UserPromptSubmit` フックはユーザー プロンプトが処理されるかどうかを制御し、コンテキストを追加できます。すべての[JSON 出力フィールド](#json-output)が利用可能です。

終了コード 0 で会話にコンテキストを追加する 2 つの方法があります。

* **プレーン テキスト stdout**: stdout に書き込まれた非 JSON テキストはコンテキストとして追加されます
* **`additionalContext` を含む JSON**: より多くの制御のために以下の JSON 形式を使用します。`additionalContext` フィールドはコンテキストとして追加されます

プレーン stdout はトランスクリプトでフック出力として表示されます。`additionalContext` フィールドはより控えめに追加されます。

プロンプトをブロックするには、`decision` を `"block"` に設定した JSON オブジェクトを返します。

| フィールド               | 説明                                                    |
| :------------------ | :---------------------------------------------------- |
| `decision`          | `"block"` はプロンプトが処理されるのを防ぎ、コンテキストから消去します。許可するには省略します  |
| `reason`            | `decision` が `"block"` のときにユーザーに表示されます。コンテキストに追加されません |
| `additionalContext` | Claude のコンテキストに追加される文字列                               |

```json  theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

<Note>
  JSON 形式は単純なユースケースでは必須ではありません。コンテキストを追加するには、終了コード 0 で stdout にプレーン テキストを出力できます。プロンプトをブロックしたい場合、またはより構造化された制御が必要な場合は JSON を使用します。
</Note>

### PreToolUse

Claude がツール パラメーターを作成した後、ツール呼び出しを処理する前に実行されます。ツール名でマッチします。`Bash`、`Edit`、`Write`、`Read`、`Glob`、`Grep`、`Agent`、`WebFetch`、`WebSearch`、および任意の[MCP ツール名](#match-mcp-tools)。

[PreToolUse 決定制御](#pretooluse-decision-control)を使用して、ツールの使用を許可、拒否、または許可を求めます。

#### PreToolUse 入力

[共通入力フィールド](#common-input-fields)に加えて、PreToolUse フックは `tool_name`、`tool_input`、`tool_use_id` を受け取ります。`tool_input` フィールドはツールに依存します。

##### Bash

シェル コマンドを実行します。

| フィールド               | タイプ  | 例                  | 説明                     |
| :------------------ | :--- | :----------------- | :--------------------- |
| `command`           | 文字列  | `"npm test"`       | 実行するシェル コマンド           |
| `description`       | 文字列  | `"Run test suite"` | コマンドが何をするかのオプション説明     |
| `timeout`           | 数値   | `120000`           | ミリ秒単位のオプション タイムアウト     |
| `run_in_background` | ブール値 | `false`            | コマンドをバックグラウンドで実行するかどうか |

##### Write

ファイルを作成または上書きします。

| フィールド       | タイプ | 例                     | 説明             |
| :---------- | :-- | :-------------------- | :------------- |
| `file_path` | 文字列 | `"/path/to/file.txt"` | 書き込むファイルへの絶対パス |
| `content`   | 文字列 | `"file content"`      | ファイルに書き込むコンテンツ |

##### Edit

既存ファイル内の文字列を置換します。

| フィールド         | タイプ  | 例                     | 説明              |
| :------------ | :--- | :-------------------- | :-------------- |
| `file_path`   | 文字列  | `"/path/to/file.txt"` | 編集するファイルへの絶対パス  |
| `old_string`  | 文字列  | `"original text"`     | 検索して置換するテキスト    |
| `new_string`  | 文字列  | `"replacement text"`  | 置換テキスト          |
| `replace_all` | ブール値 | `false`               | すべての出現を置換するかどうか |

##### Read

ファイル コンテンツを読み取ります。

| フィールド       | タイプ | 例                     | 説明                 |
| :---------- | :-- | :-------------------- | :----------------- |
| `file_path` | 文字列 | `"/path/to/file.txt"` | 読み取るファイルへの絶対パス     |
| `offset`    | 数値  | `10`                  | 読み取りを開始する行番号のオプション |
| `limit`     | 数値  | `50`                  | 読み取る行数のオプション       |

##### Glob

グロブ パターンに一致するファイルを検索します。

| フィールド     | タイプ | 例                | 説明                                 |
| :-------- | :-- | :--------------- | :--------------------------------- |
| `pattern` | 文字列 | `"**/*.ts"`      | ファイルに対してマッチするグロブ パターン              |
| `path`    | 文字列 | `"/path/to/dir"` | 検索するオプション ディレクトリ。デフォルトは現在の作業ディレクトリ |

##### Grep

正規表現でファイル コンテンツを検索します。

| フィールド         | タイプ  | 例                | 説明                                                                             |
| :------------ | :--- | :--------------- | :----------------------------------------------------------------------------- |
| `pattern`     | 文字列  | `"TODO.*fix"`    | 検索する正規表現パターン                                                                   |
| `path`        | 文字列  | `"/path/to/dir"` | 検索するオプション ファイルまたはディレクトリ                                                        |
| `glob`        | 文字列  | `"*.ts"`         | ファイルをフィルタリングするオプション グロブ パターン                                                   |
| `output_mode` | 文字列  | `"content"`      | `"content"`、`"files_with_matches"`、または `"count"`。デフォルトは `"files_with_matches"` |
| `-i`          | ブール値 | `true`           | 大文字小文字を区別しない検索                                                                 |
| `multiline`   | ブール値 | `false`          | マルチライン マッチングを有効化                                                               |

##### WebFetch

Web コンテンツを取得して処理します。

| フィールド    | タイプ | 例                             | 説明                  |
| :------- | :-- | :---------------------------- | :------------------ |
| `url`    | 文字列 | `"https://example.com/api"`   | コンテンツを取得する URL      |
| `prompt` | 文字列 | `"Extract the API endpoints"` | 取得したコンテンツで実行するプロンプト |

##### WebSearch

Web を検索します。

| フィールド             | タイプ | 例                              | 説明                        |
| :---------------- | :-- | :----------------------------- | :------------------------ |
| `query`           | 文字列 | `"react hooks best practices"` | 検索クエリ                     |
| `allowed_domains` | 配列  | `["docs.example.com"]`         | オプション: これらのドメインからのみ結果を含める |
| `blocked_domains` | 配列  | `["spam.example.com"]`         | オプション: これらのドメインからの結果を除外   |

##### Agent

[サブエージェント](/ja/sub-agents)を生成します。

| フィールド           | タイプ | 例                          | 説明                             |
| :-------------- | :-- | :------------------------- | :----------------------------- |
| `prompt`        | 文字列 | `"Find all API endpoints"` | エージェントが実行するタスク                 |
| `description`   | 文字列 | `"Find API endpoints"`     | タスクの短い説明                       |
| `subagent_type` | 文字列 | `"Explore"`                | 使用する特殊エージェントのタイプ               |
| `model`         | 文字列 | `"sonnet"`                 | デフォルトをオーバーライドするオプション モデル エイリアス |

#### PreToolUse 決定制御

`PreToolUse` フックはツール呼び出しが続行されるかどうかを制御できます。トップレベル `decision` フィールドを使用する他のフックとは異なり、PreToolUse は `hookSpecificOutput` オブジェクト内に決定を返します。これにより、より豊かな制御が可能になります。3 つの結果（許可、拒否、または質問）と、実行前にツール入力を変更する機能。

| フィールド                      | 説明                                                                                |
| :------------------------- | :-------------------------------------------------------------------------------- |
| `permissionDecision`       | `"allow"` は権限システムをバイパスし、`"deny"` はツール呼び出しを防ぎ、`"ask"` はユーザーに確認を促します                |
| `permissionDecisionReason` | `"allow"` と `"ask"` の場合、ユーザーに表示されますが Claude には表示されません。`"deny"` の場合、Claude に表示されます |
| `updatedInput`             | 実行前にツールの入力パラメーターを変更します。`"allow"` と組み合わせて自動承認するか、`"ask"` と組み合わせて変更された入力をユーザーに表示します |
| `additionalContext`        | ツール実行前に Claude のコンテキストに追加される文字列                                                   |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

<Note>
  PreToolUse は以前、トップレベル `decision` と `reason` フィールドを使用していましたが、このイベントでは非推奨です。代わりに `hookSpecificOutput.permissionDecision` と `hookSpecificOutput.permissionDecisionReason` を使用してください。非推奨の値 `"approve"` と `"block"` は `"allow"` と `"deny"` にマップされます。PostToolUse と Stop などの他のイベントは、現在の形式としてトップレベル `decision` と `reason` を使用し続けます。
</Note>

### PermissionRequest

ユーザーに権限ダイアログが表示されるときに実行されます。
[PermissionRequest 決定制御](#permissionrequest-decision-control)を使用して、ユーザーに代わって許可または拒否します。

ツール名でマッチします。PreToolUse と同じ値。

#### PermissionRequest 入力

PermissionRequest フックは PreToolUse フックのような `tool_name` と `tool_input` フィールドを受け取りますが、`tool_use_id` はありません。オプションの `permission_suggestions` 配列には、ユーザーが通常権限ダイアログで見る「常に許可」オプションが含まれています。違いはフックが発火するタイミングです。PermissionRequest フックはユーザーに権限ダイアログが表示されようとしているときに実行され、PreToolUse フックは権限ステータスに関係なくツール実行前に実行されます。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules",
    "description": "Remove node_modules directory"
  },
  "permission_suggestions": [
    { "type": "toolAlwaysAllow", "tool": "Bash" }
  ]
}
```

#### PermissionRequest 決定制御

`PermissionRequest` フックは権限リクエストを許可または拒否できます。すべてのフックで利用可能な[JSON 出力フィールド](#json-output)に加えて、フック スクリプトはこれらのイベント固有のフィールドを持つ `decision` オブジェクトを返すことができます。

| フィールド                | 説明                                                      |
| :------------------- | :------------------------------------------------------ |
| `behavior`           | `"allow"` は権限を付与し、`"deny"` はそれを拒否します                    |
| `updatedInput`       | `"allow"` のみ: 実行前にツールの入力パラメーターを変更します                    |
| `updatedPermissions` | `"allow"` のみ: 権限ルール更新を適用します。ユーザーが「常に許可」オプションを選択するのと同等です |
| `message`            | `"deny"` のみ: 権限が拒否された理由を Claude に伝えます                   |
| `interrupt`          | `"deny"` のみ: `true` の場合、Claude を停止します                   |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

### PostToolUse

ツールが正常に完了した直後に実行されます。

ツール名でマッチします。PreToolUse と同じ値。

#### PostToolUse 入力

`PostToolUse` フックはツールがすでに正常に実行された後に発火します。入力には、ツールに送信された引数である `tool_input` と、それが返した結果である `tool_response` の両方が含まれます。両方の正確なスキーマはツールに依存します。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

#### PostToolUse 決定制御

`PostToolUse` フックはツール実行後に Claude にフィードバックを提供できます。すべてのフックで利用可能な[JSON 出力フィールド](#json-output)に加えて、フック スクリプトはこれらのイベント固有のフィールドを返すことができます。

| フィールド                  | 説明                                                     |
| :--------------------- | :----------------------------------------------------- |
| `decision`             | `"block"` は Claude に `reason` でプロンプトを表示します。許可するには省略します |
| `reason`               | `decision` が `"block"` のときに Claude に表示される説明            |
| `additionalContext`    | Claude が考慮する追加コンテキスト                                   |
| `updatedMCPToolOutput` | [MCP ツール](#match-mcp-tools)のみ: ツールの出力を提供された値に置き換えます    |

```json  theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}
```

### PostToolUseFailure

ツール実行が失敗するときに実行されます。このイベントはエラーをスローするか失敗結果を返すツール呼び出しに対して発火します。これを使用して失敗をログに記録したり、アラートを送信したり、Claude に是正フィードバックを提供したりします。

ツール名でマッチします。PreToolUse と同じ値。

#### PostToolUseFailure 入力

PostToolUseFailure フックは PostToolUse と同じ `tool_name` と `tool_input` フィールドを受け取り、エラー情報をトップレベル フィールドとして受け取ります。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite"
  },
  "tool_use_id": "toolu_01ABC123...",
  "error": "Command exited with non-zero status code 1",
  "is_interrupt": false
}
```

| フィールド          | 説明                                      |
| :------------- | :-------------------------------------- |
| `error`        | 何が悪かったかを説明する文字列                         |
| `is_interrupt` | 失敗がユーザー割り込みによって引き起こされたかどうかを示すオプション ブール値 |

#### PostToolUseFailure 決定制御

`PostToolUseFailure` フックはツール失敗後に Claude にコンテキストを提供できます。すべてのフックで利用可能な[JSON 出力フィールド](#json-output)に加えて、フック スクリプトはこれらのイベント固有のフィールドを返すことができます。

| フィールド               | 説明                      |
| :------------------ | :---------------------- |
| `additionalContext` | Claude がエラーと一緒に考慮する追加情報 |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### Notification

Claude Code が通知を送信するときに実行されます。通知タイプでマッチします。`permission_prompt`、`idle_prompt`、`auth_success`、`elicitation_dialog`。すべての通知タイプのフックを実行するには、マッチャーを省略します。

別のマッチャーを使用して、通知タイプに応じて異なるハンドラーを実行します。この設定は、Claude が権限承認を必要とするときに権限固有のアラート スクリプトをトリガーし、Claude がアイドル状態になったときに異なる通知をトリガーします。

```json  theme={null}
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/permission-alert.sh"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/idle-notification.sh"
          }
        ]
      }
    ]
  }
}
```

#### Notification 入力

[共通入力フィールド](#common-input-fields)に加えて、Notification フックは通知テキストを含む `message`、オプションの `title`、発火した種類を示す `notification_type` を受け取ります。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

Notification フックは通知をブロックまたは変更できません。すべてのフックで利用可能な[JSON 出力フィールド](#json-output)に加えて、`additionalContext` を返して会話にコンテキストを追加できます。

| フィールド               | 説明                      |
| :------------------ | :---------------------- |
| `additionalContext` | Claude のコンテキストに追加される文字列 |

### SubagentStart

Agent ツール経由で Claude Code サブエージェントが生成されるときに実行されます。エージェント タイプ名でフィルタリングするマッチャーをサポートします（`Bash`、`Explore`、`Plan` などの組み込みエージェント、または `.claude/agents/` からのカスタム エージェント名）。

#### SubagentStart 入力

[共通入力フィールド](#common-input-fields)に加えて、SubagentStart フックはサブエージェントの一意の識別子を含む `agent_id` とエージェント名を含む `agent_type`（`"Bash"`、`"Explore"`、`"Plan"` などの組み込みエージェント、またはカスタム エージェント名）を受け取ります。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

SubagentStart フックはサブエージェント作成をブロックできませんが、サブエージェントにコンテキストを注入できます。すべてのフックで利用可能な[JSON 出力フィールド](#json-output)に加えて、以下を返すことができます。

| フィールド               | 説明                       |
| :------------------ | :----------------------- |
| `additionalContext` | サブエージェントのコンテキストに追加される文字列 |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

### SubagentStop

Claude Code サブエージェントが応答を終了したときに実行されます。エージェント タイプでマッチします。SubagentStart と同じ値。

#### SubagentStop 入力

[共通入力フィールド](#common-input-fields)に加えて、SubagentStop フックは `stop_hook_active`、`agent_id`、`agent_type`、`agent_transcript_path`、`last_assistant_message` を受け取ります。`agent_type` フィールドはマッチャー フィルタリングに使用される値です。`transcript_path` はメイン セッションのトランスクリプトで、`agent_transcript_path` はネストされた `subagents/` フォルダに保存されるサブエージェント独自のトランスクリプトです。`last_assistant_message` フィールドはサブエージェントの最終応答のテキスト コンテンツを含むため、フックはトランスクリプト ファイルを解析せずにアクセスできます。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../abc123.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/projects/.../abc123/subagents/agent-def456.jsonl",
  "last_assistant_message": "Analysis complete. Found 3 potential issues..."
}
```

SubagentStop フックは[Stop フック](#stop-decision-control)と同じ決定制御形式を使用します。

### Stop

メイン Claude Code エージェントが応答を終了したときに実行されます。ユーザー割り込みが原因で停止が発生した場合は実行されません。

#### Stop 入力

[共通入力フィールド](#common-input-fields)に加えて、Stop フックは `stop_hook_active` と `last_assistant_message` を受け取ります。`stop_hook_active` フィールドは、Claude Code がすでに stop フックの結果として続行している場合は `true` です。この値をチェックするか、トランスクリプトを処理して Claude Code が無限に実行されるのを防ぎます。`last_assistant_message` フィールドは Claude の最終応答のテキスト コンテンツを含むため、フックはトランスクリプト ファイルを解析せずにアクセスできます。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true,
  "last_assistant_message": "I've completed the refactoring. Here's a summary..."
}
```

#### Stop 決定制御

`Stop` と `SubagentStop` フックは Claude が続行するかどうかを制御できます。すべてのフックで利用可能な[JSON 出力フィールド](#json-output)に加えて、フック スクリプトはこれらのイベント固有のフィールドを返すことができます。

| フィールド      | 説明                                                  |
| :--------- | :-------------------------------------------------- |
| `decision` | `"block"` は Claude が停止するのを防ぎます。Claude を停止させるには省略します |
| `reason`   | `decision` が `"block"` のときに必須。Claude が続行すべき理由を伝えます  |

```json  theme={null}
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

### TeammateIdle

[エージェント チーム](/ja/agent-teams)チームメイトがターンを終了した後、アイドル状態になろうとしているときに実行されます。これを使用して、チームメイトが作業を停止する前に品質ゲートを実施します。例えば、リント チェックの合格を要求したり、出力ファイルが存在することを確認したりします。

`TeammateIdle` フックが終了コード 2 で終了すると、チームメイトは stderr メッセージをフィードバックとして受け取り、アイドル状態になる代わりに作業を続行します。チームメイトを再実行する代わりに完全に停止するには、`{"continue": false, "stopReason": "..."}` を含む JSON を返します。TeammateIdle フックはマッチャーをサポートせず、すべての出現で発火します。

#### TeammateIdle 入力

[共通入力フィールド](#common-input-fields)に加えて、TeammateIdle フックは `teammate_name` と `team_name` を受け取ります。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "my-project"
}
```

| フィールド           | 説明                       |
| :-------------- | :----------------------- |
| `teammate_name` | アイドル状態になろうとしているチームメイトの名前 |
| `team_name`     | チームの名前                   |

#### TeammateIdle 決定制御

TeammateIdle フックはチームメイト動作を制御する 2 つの方法をサポートしています。

* **終了コード 2**: チームメイトは stderr メッセージをフィードバックとして受け取り、アイドル状態になる代わりに作業を続行します。
* **JSON `{"continue": false, "stopReason": "..."}`**: チームメイトを完全に停止します。`Stop` フック動作と一致します。`stopReason` はユーザーに表示されます。

この例は、チームメイトがアイドル状態になることを許可する前に、ビルド アーティファクトが存在することをチェックします。

```bash  theme={null}
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2
fi

exit 0
```

### TaskCompleted

タスクが完了としてマークされるときに実行されます。これは 2 つの状況で発火します。任意のエージェントが TaskUpdate ツール経由でタスクを明示的に完了としてマークするか、[エージェント チーム](/ja/agent-teams)チームメイトが進行中のタスクでターンを終了するとき。これを使用して、テストの合格やリント チェックなどの完了基準を実施します。

`TaskCompleted` フックが終了コード 2 で終了すると、タスクは完了としてマークされず、stderr メッセージはモデルにフィードバックとしてフィードバックされます。チームメイトを再実行する代わりに完全に停止するには、`{"continue": false, "stopReason": "..."}` を含む JSON を返します。TaskCompleted フックはマッチャーをサポートせず、すべての出現で発火します。

#### TaskCompleted 入力

[共通入力フィールド](#common-input-fields)に加えて、TaskCompleted フックは `task_id`、`task_subject`、およびオプションで `task_description`、`teammate_name`、`team_name` を受け取ります。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCompleted",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

| フィールド              | 説明                               |
| :----------------- | :------------------------------- |
| `task_id`          | 完了しているタスクの識別子                    |
| `task_subject`     | タスクのタイトル                         |
| `task_description` | タスクの詳細説明。存在しない場合があります            |
| `teammate_name`    | タスクを完了しているチームメイトの名前。存在しない場合があります |
| `team_name`        | チームの名前。存在しない場合があります              |

#### TaskCompleted 決定制御

TaskCompleted フックはタスク完了を制御する 2 つの方法をサポートしています。

* **終了コード 2**: タスクは完了としてマークされず、stderr メッセージはモデルにフィードバックとしてフィードバックされます。
* **JSON `{"continue": false, "stopReason": "..."}`**: チームメイトを完全に停止します。`Stop` フック動作と一致します。`stopReason` はユーザーに表示されます。

この例はテストを実行し、失敗した場合はタスク完了をブロックします。

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

# テスト スイートを実行
if ! npm test 2>&1; then
  echo "Tests not passing. Fix failing tests before completing: $TASK_SUBJECT" >&2
  exit 2
fi

exit 0
```

### ConfigChange

セッション中に設定ファイルが変更されるときに実行されます。設定変更を監査したり、セキュリティ ポリシーを実施したり、設定ファイルへの不正な変更をブロックしたりするために使用します。

ConfigChange フックは設定ファイル、管理ポリシー設定、スキル ファイルの変更に対して発火します。入力の `source` フィールドは、どのタイプの設定が変更されたかを示し、オプションの `file_path` フィールドは変更されたファイルへのパスを提供します。

マッチャーは設定ソースでフィルタリングします。

| マッチャー              | いつ発火するか                           |
| :----------------- | :-------------------------------- |
| `user_settings`    | `~/.claude/settings.json` が変更     |
| `project_settings` | `.claude/settings.json` が変更       |
| `local_settings`   | `.claude/settings.local.json` が変更 |
| `policy_settings`  | 管理ポリシー設定が変更                       |
| `skills`           | `.claude/skills/` のスキル ファイルが変更    |

この例はセキュリティ監査のためにすべての設定変更をログに記録します。

```json  theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/audit-config-change.sh"
          }
        ]
      }
    ]
  }
}
```

#### ConfigChange 入力

[共通入力フィールド](#common-input-fields)に加えて、ConfigChange フックは `source` とオプションで `file_path` を受け取ります。`source` フィールドは変更された設定タイプを示し、`file_path` は変更されたファイルへのパスを提供します。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "ConfigChange",
  "source": "project_settings",
  "file_path": "/Users/.../my-project/.claude/settings.json"
}
```

#### ConfigChange 決定制御

ConfigChange フックは設定変更が有効になるのをブロックできます。終了コード 2 または JSON `decision` を使用して変更を防ぎます。ブロックされた場合、新しい設定は実行中のセッションに適用されません。

| フィールド      | 説明                                         |
| :--------- | :----------------------------------------- |
| `decision` | `"block"` は設定変更が適用されるのを防ぎます。変更を許可するには省略します |
| `reason`   | `decision` が `"block"` のときにユーザーに表示される説明    |

```json  theme={null}
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

`policy_settings` の変更はブロックできません。フックは `policy_settings` ソースに対して発火するため、監査ログに使用できますが、ブロッキング決定は無視されます。これにより、エンタープライズ管理設定が常に有効になることが保証されます。

### WorktreeCreate

`claude --worktree` を実行するか、[サブエージェントが `isolation: "worktree"` を使用](/ja/sub-agents#choose-the-subagent-scope)するとき、Claude Code は `git worktree` を使用して分離されたワーキング コピーを作成します。WorktreeCreate フックを設定する場合、デフォルトの git 動作を置き換え、SVN、Perforce、Mercurial などの別のバージョン管理システムを使用できます。

フックは作成されたワークツリー ディレクトリへの絶対パスを stdout に出力する必要があります。Claude Code はこのパスを分離されたセッションの作業ディレクトリとして使用します。

この例は SVN ワーキング コピーを作成し、Claude Code が使用するパスを出力します。リポジトリ URL を自分のものに置き換えます。

```json  theme={null}
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

フックは stdin の JSON 入力からワークツリー `name` を読み取り、新しいディレクトリに新しいコピーをチェックアウトし、ディレクトリ パスを出力します。最後の行の `echo` は Claude Code が読み取るワークツリー パスです。他の出力を stderr にリダイレクトして、パスに干渉しないようにします。

#### WorktreeCreate 入力

[共通入力フィールド](#common-input-fields)に加えて、WorktreeCreate フックは `name` フィールドを受け取ります。これは新しいワークツリーのスラッグ識別子で、ユーザーが指定するか自動生成されます（例えば、`bold-oak-a3f2`）。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

#### WorktreeCreate 出力

フックは作成されたワークツリー ディレクトリへの絶対パスを stdout に出力する必要があります。フックが失敗するか出力を生成しない場合、ワークツリー作成はエラーで失敗します。

WorktreeCreate フックは標準的な許可/ブロック決定モデルを使用しません。代わりに、フックの成功または失敗が結果を決定します。`type: "command"` フックのみがサポートされています。

### WorktreeRemove

[WorktreeCreate](#worktreecreate) のクリーンアップ対応。このフックはワークツリーが削除されるときに発火します。`--worktree` セッションを終了して削除を選択するか、`isolation: "worktree"` を持つサブエージェントが完了するとき。git ベースのワークツリーの場合、Claude は `git worktree remove` で自動的にクリーンアップを処理します。非 git バージョン管理システムの WorktreeCreate フックを設定した場合、クリーンアップを処理するために WorktreeRemove フックとペアにします。なければ、ワークツリー ディレクトリはディスク上に残ります。

Claude Code は WorktreeCreate が stdout に出力したパスを `worktree_path` としてフック入力に渡します。この例はそのパスを読み取り、ディレクトリを削除します。

```json  theme={null}
{
  "hooks": {
    "WorktreeRemove": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'jq -r .worktree_path | xargs rm -rf'"
          }
        ]
      }
    ]
  }
}
```

#### WorktreeRemove 入力

[共通入力フィールド](#common-input-fields)に加えて、WorktreeRemove フックは削除されるワークツリーへの絶対パスである `worktree_path` フィールドを受け取ります。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

WorktreeRemove フックは決定制御がありません。ワークツリー削除をブロックできませんが、バージョン管理状態の削除やアーカイブ変更などのクリーンアップ タスクを実行できます。フック失敗はデバッグ モードでのみログに記録されます。`type: "command"` フックのみがサポートされています。

### PreCompact

Claude Code がコンパクト操作を実行しようとしている前に実行されます。

マッチャー値はコンパクションが手動でトリガーされたか自動でトリガーされたかを示します。

| マッチャー    | いつ発火するか                      |
| :------- | :--------------------------- |
| `manual` | `/compact`                   |
| `auto`   | コンテキスト ウィンドウが満杯のときの自動コンパクション |

#### PreCompact 入力

[共通入力フィールド](#common-input-fields)に加えて、PreCompact フックは `trigger` と `custom_instructions` を受け取ります。`manual` の場合、`custom_instructions` はユーザーが `/compact` に渡すものを含みます。`auto` の場合、`custom_instructions` は空です。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### SessionEnd

Claude Code セッションが終了するときに実行されます。クリーンアップ タスク、ログ セッション統計、またはセッション状態の保存に便利です。終了理由でフィルタリングするマッチャーをサポートします。

フック入力の `reason` フィールドはセッションが終了した理由を示します。

| 理由                            | 説明                       |
| :---------------------------- | :----------------------- |
| `clear`                       | `/clear` コマンドでセッションをクリア  |
| `logout`                      | ユーザーがログアウト               |
| `prompt_input_exit`           | プロンプト入力が表示されている間にユーザーが終了 |
| `bypass_permissions_disabled` | バイパス権限モードが無効化            |
| `other`                       | その他の終了理由                 |

#### SessionEnd 入力

[共通入力フィールド](#common-input-fields)に加えて、SessionEnd フックはセッションが終了した理由を示す `reason` フィールドを受け取ります。上記の[理由テーブル](#sessionend)をすべての値について参照してください。

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

SessionEnd フックは決定制御がありません。セッション終了をブロックできませんが、クリーンアップ タスクを実行できます。

## プロンプト ベースのフック

コマンド フックと HTTP フックに加えて、Claude Code はプロンプト ベースのフック（`type: "prompt"`）をサポートしており、LLM を使用してアクションを許可またはブロックするかを評価し、エージェント フック（`type: "agent"`）はツール アクセスを持つ agentic ベリファイアーを生成します。すべてのイベントがすべてのフック タイプをサポートしているわけではありません。

4 つのフック タイプ（`command`、`http`、`prompt`、`agent`）すべてをサポートするイベント。

* `PermissionRequest`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `UserPromptSubmit`

`type: "command"` フックのみをサポートするイベント。

* `ConfigChange`
* `InstructionsLoaded`
* `Notification`
* `PreCompact`
* `SessionEnd`
* `SessionStart`
* `SubagentStart`
* `TeammateIdle`
* `WorktreeCreate`
* `WorktreeRemove`

### プロンプト ベースのフックがどのように機能するか

Bash コマンドを実行する代わりに、プロンプト ベースのフック。

1. フック入力とプロンプトを Claude モデル（デフォルトは Haiku）に送信
2. LLM は決定を含む構造化 JSON で応答
3. Claude Code は決定を自動的に処理

### プロンプト フック設定

`type` を `"prompt"` に設定し、`command` の代わりに `prompt` 文字列を提供します。`$ARGUMENTS` プレースホルダーを使用して、フックの JSON 入力データをプロンプト テキストに注入します。Claude Code は結合されたプロンプトと入力を高速 Claude モデルに送信し、JSON 決定を返します。

この `Stop` フックは、Claude が終了する前にすべてのタスクが完了しているかどうかを評価するよう LLM に求めます。

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
          }
        ]
      }
    ]
  }
}
```

| フィールド     | 必須  | 説明                                                                                                          |
| :-------- | :-- | :---------------------------------------------------------------------------------------------------------- |
| `type`    | はい  | `"prompt"` である必要があります                                                                                       |
| `prompt`  | はい  | LLM に送信するプロンプト テキスト。フック入力 JSON のプレースホルダーとして `$ARGUMENTS` を使用します。`$ARGUMENTS` が存在しない場合、入力 JSON はプロンプトに追加されます |
| `model`   | いいえ | 評価に使用するモデル。デフォルトは高速モデル                                                                                      |
| `timeout` | いいえ | 秒単位のタイムアウト。デフォルト: 30                                                                                        |

### レスポンス スキーマ

LLM は以下を含む JSON で応答する必要があります。

```json  theme={null}
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

| フィールド    | 説明                                    |
| :------- | :------------------------------------ |
| `ok`     | `true` はアクションを許可し、`false` はそれを防ぎます    |
| `reason` | `ok` が `false` のときに必須。Claude に表示される説明 |

### 例: マルチ基準 Stop フック

この `Stop` フックは詳細なプロンプトを使用して、Claude が停止することを許可する前に 3 つの条件をチェックします。`"ok"` が `false` の場合、Claude は提供された理由を次の指示として受け取り、作業を続行します。`SubagentStop` フックは同じ形式を使用して、[サブエージェント](/ja/sub-agents)が停止すべきかどうかを評価します。

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## エージェント ベースのフック

エージェント ベースのフック（`type: "agent"`）はプロンプト ベースのフックのようですが、マルチターン ツール アクセスを備えています。単一の LLM 呼び出しの代わりに、エージェント フックはプロンプトとフックの JSON 入力を持つサブエージェントを生成します。サブエージェントはファイルを読み取り、コードを検索し、コードベースを検査して条件を検証できます。エージェント フックはプロンプト ベースのフックと同じイベントをサポートしています。

### エージェント フックがどのように機能するか

エージェント フックが発火するとき。

1. Claude Code はプロンプトとフックの JSON 入力を持つサブエージェントを生成
2. サブエージェントは Read、Grep、Glob などのツールを使用して調査できます
3. 最大 50 ターン後、サブエージェントは構造化 `{ "ok": true/false }` 決定を返します
4. Claude Code はプロンプト フックと同じ方法で決定を処理

エージェント フックは、フック入力データのみを評価するのではなく、実際のファイルを検査またはテスト出力を検査する必要がある検証に便利です。

### エージェント フック設定

`type` を `"agent"` に設定し、`prompt` 文字列を提供します。設定フィールドは[プロンプト フック](#prompt-hook-configuration)と同じで、より長いデフォルト タイムアウト。

| フィールド     | 必須  | 説明                                                           |
| :-------- | :-- | :----------------------------------------------------------- |
| `type`    | はい  | `"agent"` である必要があります                                         |
| `prompt`  | はい  | 検証する内容を説明するプロンプト。フック入力 JSON のプレースホルダーとして `$ARGUMENTS` を使用します |
| `model`   | いいえ | 使用するモデル。デフォルトは高速モデル                                          |
| `timeout` | いいえ | 秒単位のタイムアウト。デフォルト: 60                                         |

レスポンス スキーマはプロンプト フックと同じです。許可するには `{ "ok": true }` またはブロックするには `{ "ok": false, "reason": "..." }`。

この `Stop` フックは、Claude が終了することを許可する前にすべてのユニット テストが合格することを検証します。

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

## バックグラウンドでフックを実行

デフォルトでは、フックは完了するまで Claude の実行をブロックします。デプロイメント、テスト スイート、外部 API 呼び出しなどの長時間実行タスクの場合、`"async": true` を設定して、Claude が作業を続行している間、フックをバックグラウンドで実行します。非同期フックはブロックまたは Claude の動作を制御できません。`decision`、`permissionDecision`、`continue` などのレスポンス フィールドは、制御しようとしたアクションがすでに完了しているため、効果がありません。

### 非同期フックを設定

コマンド フックの設定に `"async": true` を追加して、Claude をブロックせずにバックグラウンドで実行します。このフィールドは `type: "command"` フックでのみ利用可能です。

このフックは `Write` ツール呼び出しの後、テスト スクリプトを実行します。Claude は `run-tests.sh` が最大 120 秒間実行されている間、すぐに作業を続行します。スクリプトが完了すると、その出力は次の会話ターンで配信されます。

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

`timeout` フィールドはバックグラウンド プロセスの最大時間を秒単位で設定します。指定されない場合、非同期フックは同期フックと同じ 10 分のデフォルトを使用します。

### 非同期フックがどのように実行されるか

非同期フックが発火すると、Claude Code はフック プロセスを開始し、完了を待たずにすぐに続行します。フックは同期フックと同じ JSON 入力を stdin 経由で受け取ります。

バックグラウンド プロセスが終了した後、フックが `systemMessage` または `additionalContext` フィールドを含む JSON レスポンスを生成した場合、そのコンテンツは次の会話ターンで Claude にコンテキストとして配信されます。

### 例: ファイル変更後にテストを実行

このフックは Claude がファイルを書き込むたびにバックグラウンドでテスト スイートを開始し、テストが完了したときに結果を Claude に報告します。このスクリプトをプロジェクトの `.claude/hooks/run-tests-async.sh` に保存し、`chmod +x` で実行可能にします。

```bash  theme={null}
#!/bin/bash
# run-tests-async.sh

# stdin からフック入力を読み取る
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# ソース ファイルのみテストを実行
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# テストを実行し、systemMessage 経由で結果を報告
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "{\"systemMessage\": \"Tests passed after editing $FILE_PATH\"}"
else
  echo "{\"systemMessage\": \"Tests failed after editing $FILE_PATH: $RESULT\"}"
fi
```

次に、プロジェクト ルートの `.claude/settings.json` にこの設定を追加します。`async: true` フラグにより、Claude はテストの実行中に作業を続行できます。

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run-tests-async.sh",
            "async": true,
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

### 制限事項

非同期フックは同期フックと比べていくつかの制約があります。

* `async` をサポートするのは `type: "command"` フックのみです。プロンプト ベースのフックは非同期で実行できません。
* 非同期フックはツール呼び出しをブロックまたは決定を返すことができません。フックが完了するまでに、トリガーするアクションはすでに進行しています。
* フック出力は次の会話ターンで配信されます。セッションがアイドル状態の場合、レスポンスは次のユーザー操作まで待機します。
* 各実行は個別のバックグラウンド プロセスを作成します。同じ非同期フックの複数の発火間での重複排除はありません。

## セキュリティに関する考慮事項

### 免責事項

コマンド フックはシステム ユーザーの完全な権限で実行されます。

<Warning>
  コマンド フックはユーザー アカウントの完全な権限でシェル コマンドを実行します。ユーザー アカウントがアクセスできるファイルを変更、削除、またはアクセスできます。フック コマンドを設定に追加する前に、すべてのフック コマンドを確認してテストしてください。
</Warning>

### セキュリティ ベスト プラクティス

フックを書くときは、これらのプラクティスに留意してください。

* **入力を検証およびサニタイズ**: 入力データを盲目的に信頼しないでください
* **常にシェル変数を引用**: `$VAR` ではなく `"$VAR"` を使用
* **パス トラバーサルをブロック**: ファイル パスで `..` をチェック
* **絶対パスを使用**: スクリプトの完全なパスを指定し、プロジェクト ルートに `"$CLAUDE_PROJECT_DIR"` を使用
* **機密ファイルをスキップ**: `.env`、`.git/`、キーなどを避ける

## フックをデバッグ

`claude --debug` を実行して、フック実行の詳細を確認します。マッチしたフック、終了コード、出力を含みます。`Ctrl+O` で詳細モードを切り替えて、トランスクリプトでフック進行状況を確認します。

```text  theme={null}
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

フックが発火しない、無限 Stop フック ループ、設定エラーなどの一般的な問題のトラブルシューティングについては、ガイドの[制限事項とトラブルシューティング](/ja/hooks-guide#limitations-and-troubleshooting)を参照してください。
