> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 権限を設定する

> きめ細かい権限ルール、モード、管理ポリシーを使用して、Claude Code がアクセスして実行できる内容を制御します。

Claude Code は、エージェントが実行できることと実行できないことを正確に指定できるようにするため、きめ細かい権限をサポートしています。権限設定はバージョン管理にチェックインでき、組織内のすべての開発者に配布できるほか、個々の開発者がカスタマイズできます。

## 権限システム

Claude Code は、パワーと安全性のバランスを取るために、段階的な権限システムを使用しています。

| ツールタイプ    | 例               | 承認が必要 | 「はい、今後は聞かない」の動作         |
| :-------- | :-------------- | :---- | :---------------------- |
| 読み取り専用    | ファイル読み取り、Grep   | いいえ   | N/A                     |
| Bash コマンド | シェル実行           | はい    | プロジェクトディレクトリとコマンドごとに永続的 |
| ファイル変更    | Edit/Write ファイル | はい    | セッション終了まで               |

## 権限を管理する

`/permissions` を使用して、Claude Code のツール権限を表示および管理できます。この UI は、すべての権限ルールと、それらが取得される settings.json ファイルをリストします。

* **Allow** ルールは、Claude Code が手動承認なしで指定されたツールを使用できるようにします。
* **Ask** ルールは、Claude Code が指定されたツールを使用しようとするたびに確認を促します。
* **Deny** ルールは、Claude Code が指定されたツールを使用することを防止します。

ルールは順序で評価されます。**deny -> ask -> allow**。最初にマッチしたルールが優先されるため、deny ルールは常に優先されます。

## 権限モード

Claude Code は、ツールの承認方法を制御するいくつかの権限モードをサポートしています。[設定ファイル](/ja/settings#settings-files)で `defaultMode` を設定します。

| モード                 | 説明                                                                     |
| :------------------ | :--------------------------------------------------------------------- |
| `default`           | 標準動作。各ツールの最初の使用時に権限を促します                                               |
| `acceptEdits`       | セッション中のファイル編集権限を自動的に受け入れます                                             |
| `plan`              | Plan Mode。Claude はファイルを分析できますが、ファイルを変更したりコマンドを実行したりすることはできません          |
| `dontAsk`           | `/permissions` または `permissions.allow` ルールで事前に承認されていない限り、ツールを自動的に拒否します |
| `bypassPermissions` | すべての権限プロンプトをスキップします（安全な環境が必要です。以下の警告を参照してください）                         |

<Warning>
  `bypassPermissions` モードはすべての権限チェックを無効にします。このモードは、Claude Code が損害を引き起こせないコンテナや VM などの隔離された環境でのみ使用してください。管理者は、[管理設定](#managed-settings)で `disableBypassPermissionsMode` を `"disable"` に設定することで、このモードを防止できます。
</Warning>

## 権限ルール構文

権限ルールは、`Tool` または `Tool(specifier)` の形式に従います。

### ツールのすべての使用をマッチさせる

ツールのすべての使用をマッチさせるには、括弧なしでツール名を使用します。

| ルール        | 効果                       |
| :--------- | :----------------------- |
| `Bash`     | すべての Bash コマンドをマッチさせます   |
| `WebFetch` | すべてのウェブフェッチリクエストをマッチさせます |
| `Read`     | すべてのファイル読み取りをマッチさせます     |

`Bash(*)` は `Bash` と同等で、すべての Bash コマンドをマッチさせます。

### 細かい制御のためにスペシファイアを使用する

括弧内にスペシファイアを追加して、特定のツール使用をマッチさせます。

| ルール                            | 効果                                    |
| :----------------------------- | :------------------------------------ |
| `Bash(npm run build)`          | 正確なコマンド `npm run build` をマッチさせます      |
| `Read(./.env)`                 | 現在のディレクトリの `.env` ファイルを読み取ることをマッチさせます |
| `WebFetch(domain:example.com)` | example.com へのフェッチリクエストをマッチさせます       |

### ワイルドカードパターン

Bash ルールは `*` を使用したグロブパターンをサポートしています。ワイルドカードはコマンド内の任意の位置に表示できます。この設定により、npm および git commit コマンドが許可され、git push がブロックされます。

```json  theme={null}
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)",
      "Bash(* --version)",
      "Bash(* --help *)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

`*` の前のスペースは重要です。`Bash(ls *)` は `ls -la` にマッチしますが `lsof` にはマッチしません。一方、`Bash(ls*)` は両方にマッチします。レガシーな `:*` サフィックス構文は ` *` と同等ですが、非推奨です。

## ツール固有の権限ルール

### Bash

Bash 権限ルールは `*` を使用したワイルドカードマッチングをサポートしています。ワイルドカードは、開始、中央、終了を含むコマンド内の任意の位置に表示できます。

* `Bash(npm run build)` は正確な Bash コマンド `npm run build` をマッチさせます
* `Bash(npm run test *)` は `npm run test` で始まる Bash コマンドをマッチさせます
* `Bash(npm *)` は `npm ` で始まるコマンドをマッチさせます
* `Bash(* install)` は ` install` で終わるコマンドをマッチさせます
* `Bash(git * main)` は `git checkout main`、`git merge main` などのコマンドをマッチさせます

`*` が末尾にスペース付きで表示される場合（`Bash(ls *)` など）、単語境界を強制し、プレフィックスの後にスペースまたは文字列の終わりが続く必要があります。たとえば、`Bash(ls *)` は `ls -la` にマッチしますが `lsof` にはマッチしません。対照的に、スペースなしの `Bash(ls*)` は、単語境界制約がないため、`ls -la` と `lsof` の両方にマッチします。

<Tip>
  Claude Code はシェルオペレータ（`&&` など）を認識しているため、`Bash(safe-cmd *)` のようなプレフィックスマッチルールは、`safe-cmd && other-cmd` コマンドを実行する権限を与えません。
</Tip>

<Warning>
  コマンド引数を制約しようとする Bash 権限パターンは脆弱です。たとえば、`Bash(curl http://github.com/ *)` は curl を GitHub URL に制限することを意図していますが、次のようなバリエーションにはマッチしません。

  * URL の前のオプション。`curl -X GET http://github.com/...`
  * 異なるプロトコル。`curl https://github.com/...`
  * リダイレクト。`curl -L http://bit.ly/xyz`（github にリダイレクト）
  * 変数。`URL=http://github.com && curl $URL`
  * 余分なスペース。`curl  http://github.com`

  より信頼性の高い URL フィルタリングについては、以下を検討してください。

  * **Bash ネットワークツールを制限する**。deny ルールを使用して `curl`、`wget` などのコマンドをブロックし、許可されたドメインに対して `WebFetch(domain:github.com)` 権限で WebFetch ツールを使用します
  * **PreToolUse フックを使用する**。Bash コマンドの URL を検証し、許可されていないドメインをブロックするフックを実装します
  * CLAUDE.md を通じて Claude Code に許可された curl パターンについて指示します

  WebFetch のみを使用しても、ネットワークアクセスは防止されません。Bash が許可されている場合、Claude は `curl`、`wget` または他のツールを使用して任意の URL に到達できます。
</Warning>

### Read と Edit

`Edit` ルールは、ファイルを編集するすべての組み込みツールに適用されます。Claude は、Grep や Glob などのファイルを読み取るすべての組み込みツールに `Read` ルールを適用するためにベストエフォートを試みます。

Read と Edit ルールの両方は、[gitignore](https://git-scm.com/docs/gitignore) 仕様に従い、4 つの異なるパターンタイプがあります。

| パターン                | 意味                     | 例                                | マッチ                            |
| ------------------- | ---------------------- | -------------------------------- | ------------------------------ |
| `//path`            | ファイルシステムルートからの**絶対**パス | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`      |
| `~/path`            | **ホーム**ディレクトリからのパス     | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf` |
| `/path`             | **プロジェクトルートからの相対**パス   | `Edit(/src/**/*.ts)`             | `<project root>/src/**/*.ts`   |
| `path` または `./path` | **現在のディレクトリからの相対**パス   | `Read(*.env)`                    | `<cwd>/*.env`                  |

<Warning>
  `/Users/alice/file` のようなパターンは絶対パスではありません。プロジェクトルートからの相対パスです。絶対パスには `//Users/alice/file` を使用してください。
</Warning>

例。

* `Edit(/docs/**)`: `<project>/docs/` での編集（`/docs/` ではなく、`<project>/.claude/docs/` でもありません）
* `Read(~/.zshrc)`: ホームディレクトリの `.zshrc` を読み取ります
* `Edit(//tmp/scratch.txt)`: 絶対パス `/tmp/scratch.txt` を編集します
* `Read(src/**)`: `<current-directory>/src/` から読み取ります

<Note>
  gitignore パターンでは、`*` は単一のディレクトリ内のファイルをマッチさせ、`**` はディレクトリ全体で再帰的にマッチさせます。すべてのファイルアクセスを許可するには、括弧なしでツール名を使用します。`Read`、`Edit`、または `Write`。
</Note>

### WebFetch

* `WebFetch(domain:example.com)` は example.com へのフェッチリクエストをマッチさせます

### MCP

* `mcp__puppeteer` は `puppeteer` サーバーによって提供されるツール（Claude Code で設定された名前）をマッチさせます
* `mcp__puppeteer__*` ワイルドカード構文は、`puppeteer` サーバーからのすべてのツールもマッチさせます
* `mcp__puppeteer__puppeteer_navigate` は `puppeteer` サーバーによって提供される `puppeteer_navigate` ツールをマッチさせます

### Agent（subagents）

`Agent(AgentName)` ルールを使用して、Claude が使用できる [subagents](/ja/sub-agents) を制御します。

* `Agent(Explore)` は Explore subagent をマッチさせます
* `Agent(Plan)` は Plan subagent をマッチさせます
* `Agent(my-custom-agent)` は `my-custom-agent` という名前のカスタム subagent をマッチさせます

これらのルールを設定の `deny` 配列に追加するか、`--disallowedTools` CLI フラグを使用して特定のエージェントを無効にします。Explore エージェントを無効にするには。

```json  theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## フックで権限を拡張する

[Claude Code フック](/ja/hooks-guide)は、実行時に権限評価を実行するカスタムシェルコマンドを登録する方法を提供します。Claude Code がツール呼び出しを行うと、PreToolUse フックは権限システムの前に実行され、フック出力は権限システムの代わりにツール呼び出しを承認または拒否するかどうかを決定できます。

## 作業ディレクトリ

デフォルトでは、Claude は起動されたディレクトリ内のファイルにアクセスできます。このアクセスを拡張できます。

* **起動時**。`--add-dir <path>` CLI 引数を使用します
* **セッション中**。`/add-dir` コマンドを使用します
* **永続的な設定**。[設定ファイル](/ja/settings#settings-files)の `additionalDirectories` に追加します

追加ディレクトリ内のファイルは、元の作業ディレクトリと同じ権限ルールに従います。プロンプトなしで読み取り可能になり、ファイル編集権限は現在の権限モードに従います。

## 権限がサンドボックスとどのように相互作用するか

権限と[サンドボックス](/ja/sandboxing)は、補完的なセキュリティレイヤーです。

* **権限**は、Claude Code が使用できるツール、およびアクセスできるファイルまたはドメインを制御します。すべてのツール（Bash、Read、Edit、WebFetch、MCP など）に適用されます。
* **サンドボックス**は、Bash ツールのファイルシステムとネットワークアクセスを制限する OS レベルの強制を提供します。Bash コマンドとその子プロセスにのみ適用されます。

防御を深くするために両方を使用します。

* 権限 deny ルールは、Claude が制限されたリソースへのアクセスを試みることさえ防止します
* サンドボックス制限は、プロンプトインジェクションが Claude の意思決定をバイパスしても、Bash コマンドが定義された境界外のリソースに到達することを防止します
* サンドボックス内のファイルシステム制限は、Read と Edit deny ルールを使用し、別のサンドボックス設定は使用しません
* ネットワーク制限は、WebFetch 権限ルールとサンドボックスの `allowedDomains` リストを組み合わせます

## 管理設定

Claude Code 設定の一元的な制御が必要な組織の場合、管理者はユーザーまたはプロジェクト設定でオーバーライドできない管理設定をデプロイできます。これらのポリシー設定は通常の設定ファイルと同じ形式に従い、MDM/OS レベルのポリシー、管理設定ファイル、または[サーバー管理設定](/ja/server-managed-settings)を通じて配信できます。配信メカニズムとファイルの場所については、[設定ファイル](/ja/settings#settings-files)を参照してください。

### 管理のみの設定

一部の設定は管理設定でのみ有効です。

| 設定                                        | 説明                                                                                                                                                        |
| :---------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode`            | `bypassPermissions` モードと `--dangerously-skip-permissions` フラグを防止するために `"disable"` に設定します                                                                  |
| `allowManagedPermissionRulesOnly`         | `true` の場合、ユーザーおよびプロジェクト設定が `allow`、`ask`、または `deny` 権限ルールを定義することを防止します。管理設定のルールのみが適用されます                                                                 |
| `allowManagedHooksOnly`                   | `true` の場合、ユーザー、プロジェクト、およびプラグインフックの読み込みを防止します。管理フックと SDK フックのみが許可されます                                                                                     |
| `allowManagedMcpServersOnly`              | `true` の場合、管理設定からの `allowedMcpServers` のみが尊重されます。`deniedMcpServers` はすべてのソースからマージされます。[管理 MCP 設定](/ja/mcp#managed-mcp-configuration)を参照してください             |
| `blockedMarketplaces`                     | マーケットプレイスソースのブロックリスト。ブロックされたソースはダウンロード前にチェックされるため、ファイルシステムに触れることはありません。[管理マーケットプレイス制限](/ja/plugin-marketplaces#managed-marketplace-restrictions)を参照してください |
| `sandbox.network.allowManagedDomainsOnly` | `true` の場合、管理設定からの `allowedDomains` と `WebFetch(domain:...)` allow ルールのみが尊重されます。許可されていないドメインはユーザーに促すことなく自動的にブロックされます。拒否されたドメインはすべてのソースからマージされます           |
| `strictKnownMarketplaces`                 | ユーザーが追加できるプラグインマーケットプレイスを制御します。[管理マーケットプレイス制限](/ja/plugin-marketplaces#managed-marketplace-restrictions)を参照してください                                         |
| `allow_remote_sessions`                   | `true` の場合、ユーザーが[リモートコントロール](/ja/remote-control)と[ウェブセッション](/ja/claude-code-on-the-web)を開始できます。デフォルトは `true` です。リモートセッションアクセスを防止するには `false` に設定します       |

## 設定の優先順位

権限ルールは、他のすべての Claude Code 設定と同じ[設定優先順位](/ja/settings#settings-precedence)に従います。

1. **管理設定**。コマンドライン引数を含む他のレベルでオーバーライドできません
2. **コマンドライン引数**。一時的なセッションオーバーライド
3. **ローカルプロジェクト設定**（`.claude/settings.local.json`）
4. **共有プロジェクト設定**（`.claude/settings.json`）
5. **ユーザー設定**（`~/.claude/settings.json`）

ツールがいずれかのレベルで拒否されている場合、他のレベルはそれを許可できません。たとえば、管理設定 deny は `--allowedTools` でオーバーライドできず、`--disallowedTools` は管理設定が定義する内容を超えて制限を追加できます。

権限がユーザー設定で許可されているがプロジェクト設定で拒否されている場合、プロジェクト設定が優先され、権限はブロックされます。

## 設定例

この[リポジトリ](https://github.com/anthropics/claude-code/tree/main/examples/settings)には、一般的なデプロイメントシナリオのスターター設定が含まれています。これらを出発点として使用し、ニーズに合わせて調整してください。

## 関連項目

* [設定](/ja/settings)。権限設定テーブルを含む完全な設定リファレンス
* [サンドボックス](/ja/sandboxing)。Bash コマンドの OS レベルのファイルシステムとネットワーク分離
* [認証](/ja/authentication)。Claude Code へのユーザーアクセスを設定します
* [セキュリティ](/ja/security)。セキュリティ保護とベストプラクティス
* [フック](/ja/hooks-guide)。ワークフローを自動化し、権限評価を拡張します
