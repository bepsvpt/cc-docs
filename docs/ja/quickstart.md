> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# クイックスタート

> Claude Code へようこそ！

このクイックスタートガイドを使用すれば、数分で AI を活用したコーディング支援を利用できます。このガイドを終了する頃には、一般的な開発タスクに Claude Code を使用する方法を理解できるようになります。

## 始める前に

以下を確認してください：

* ターミナルまたはコマンドプロンプトが開いている
  * ターミナルを使用したことがない場合は、[ターミナルガイド](/ja/terminal-guide)をご覧ください
* 作業するコードプロジェクトがある
* [Claude サブスクリプション](https://claude.com/pricing)（Pro、Max、Teams、または Enterprise）、[Claude Console](https://console.anthropic.com/) アカウント、または[サポートされているクラウドプロバイダー](/ja/third-party-integrations)経由のアクセスがある

<Note>
  このガイドは、ターミナル CLI について説明しています。Claude Code は、[ウェブ](https://claude.ai/code)、[デスクトップアプリ](/ja/desktop)、[VS Code](/ja/vs-code) および [JetBrains IDE](/ja/jetbrains)、[Slack](/ja/slack)、および [GitHub Actions](/ja/github-actions) と [GitLab](/ja/gitlab-ci-cd) を使用した CI/CD でも利用できます。[すべてのインターフェース](/ja/overview#use-claude-code-everywhere)を参照してください。
</Note>

## ステップ 1：Claude Code をインストールする

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

## ステップ 2：アカウントにログインする

Claude Code を使用するにはアカウントが必要です。`claude` コマンドでインタラクティブセッションを開始すると、ログインが必要になります：

```bash  theme={null}
claude
# 初回使用時にログインするよう求められます
```

```bash  theme={null}
/login
# プロンプトに従ってアカウントでログインします
```

以下のいずれかのアカウントタイプを使用してログインできます：

* [Claude Pro、Max、Teams、または Enterprise](https://claude.com/pricing)（推奨）
* [Claude Console](https://console.anthropic.com/)（プリペイドクレジット付き API アクセス）。初回ログイン時に、「Claude Code」ワークスペースが Console に自動的に作成され、コスト追跡が一元化されます。
* [Amazon Bedrock、Google Vertex AI、または Microsoft Foundry](/ja/third-party-integrations)（エンタープライズクラウドプロバイダー）

ログイン後、認証情報がシステムに保存され、再度ログインする必要はありません。後でアカウントを切り替えるには、`/login` コマンドを使用します。

## ステップ 3：最初のセッションを開始する

任意のプロジェクトディレクトリでターミナルを開き、Claude Code を開始します：

```bash  theme={null}
cd /path/to/your/project
claude
```

Claude Code のウェルカムスクリーンが表示され、セッション情報、最近の会話、および最新の更新が表示されます。利用可能なコマンドについては `/help` を入力するか、前のセッションを続行するには `/resume` を入力します。

<Tip>
  ログイン後（ステップ 2）、認証情報がシステムに保存されます。詳細については、[認証情報管理](/ja/authentication#credential-management)を参照してください。
</Tip>

## ステップ 4：最初の質問をする

コードベースを理解することから始めましょう。以下のコマンドのいずれかを試してください：

```text  theme={null}
what does this project do?
```

Claude がファイルを分析し、概要を提供します。より具体的な質問をすることもできます：

```text  theme={null}
what technologies does this project use?
```

```text  theme={null}
where is the main entry point?
```

```text  theme={null}
explain the folder structure
```

Claude 自体の機能について質問することもできます：

```text  theme={null}
what can Claude Code do?
```

```text  theme={null}
how do I create custom skills in Claude Code?
```

```text  theme={null}
can Claude Code work with Docker?
```

<Note>
  Claude Code は必要に応じてプロジェクトファイルを読み込みます。コンテキストを手動で追加する必要はありません。
</Note>

## ステップ 5：最初のコード変更を行う

次に、Claude Code に実際のコーディングを行わせましょう。簡単なタスクを試してください：

```text  theme={null}
add a hello world function to the main file
```

Claude Code は以下を実行します：

1. 適切なファイルを検索する
2. 提案された変更を表示する
3. 承認を求める
4. 編集を行う

<Note>
  Claude Code は、ファイルを変更する前に常に許可を求めます。個別の変更を承認するか、セッション中に「すべて承認」モードを有効にすることができます。
</Note>

## ステップ 6：Claude Code で Git を使用する

Claude Code は Git 操作を会話形式にします：

```text  theme={null}
what files have I changed?
```

```text  theme={null}
commit my changes with a descriptive message
```

より複雑な Git 操作を求めることもできます：

```text  theme={null}
create a new branch called feature/quickstart
```

```text  theme={null}
show me the last 5 commits
```

```text  theme={null}
help me resolve merge conflicts
```

## ステップ 7：バグを修正するか機能を追加する

Claude はデバッグと機能実装に長けています。

自然言語で実現したいことを説明します：

```text  theme={null}
add input validation to the user registration form
```

または既存の問題を修正します：

```text  theme={null}
there's a bug where users can submit empty forms - fix it
```

Claude Code は以下を実行します：

* 関連するコードを特定する
* コンテキストを理解する
* ソリューションを実装する
* 利用可能な場合はテストを実行する

## ステップ 8：その他の一般的なワークフローを試す

Claude と連携する方法は多数あります：

**コードをリファクタリングする**

```text  theme={null}
refactor the authentication module to use async/await instead of callbacks
```

**テストを作成する**

```text  theme={null}
write unit tests for the calculator functions
```

**ドキュメントを更新する**

```text  theme={null}
update the README with installation instructions
```

**コードレビュー**

```text  theme={null}
review my changes and suggest improvements
```

<Tip>
  Claude に、役立つ同僚に話しかけるように話しかけてください。実現したいことを説明すれば、Claude がそこに到達するのを支援します。
</Tip>

## 重要なコマンド

日常的に使用する最も重要なコマンドは以下の通りです：

| コマンド                | 機能                   | 例                                   |
| ------------------- | -------------------- | ----------------------------------- |
| `claude`            | インタラクティブモードを開始する     | `claude`                            |
| `claude "task"`     | 1 回限りのタスクを実行する       | `claude "fix the build error"`      |
| `claude -p "query"` | 1 回限りのクエリを実行してから終了する | `claude -p "explain this function"` |
| `claude -c`         | 現在のディレクトリで最新の会話を続行する | `claude -c`                         |
| `claude -r`         | 前のセッションを再開する         | `claude -r`                         |
| `claude commit`     | Git コミットを作成する        | `claude commit`                     |
| `/clear`            | 会話履歴をクリアする           | `/clear`                            |
| `/help`             | 利用可能なコマンドを表示する       | `/help`                             |
| `exit` または Ctrl+C   | Claude Code を終了する    | `exit`                              |

コマンドの完全なリストについては、[CLI リファレンス](/ja/cli-reference)を参照してください。

## 初心者向けのプロのヒント

詳細については、[ベストプラクティス](/ja/best-practices)および[一般的なワークフロー](/ja/common-workflows)を参照してください。

<AccordionGroup>
  <Accordion title="リクエストを具体的にする">
    代わりに：'バグを修正する'

    試してください：'ユーザーが間違った認証情報を入力した後に空白の画面が表示されるログインバグを修正する'
  </Accordion>

  <Accordion title="段階的な指示を使用する">
    複雑なタスクをステップに分割します：

    ```text  theme={null}
    1. create a new database table for user profiles
    2. create an API endpoint to get and update user profiles
    3. build a webpage that allows users to see and edit their information
    ```
  </Accordion>

  <Accordion title="Claude に最初に探索させる">
    変更を加える前に、Claude にコードを理解させます：

    ```text  theme={null}
    analyze the database schema
    ```

    ```text  theme={null}
    build a dashboard showing products that are most frequently returned by our UK customers
    ```
  </Accordion>

  <Accordion title="ショートカットで時間を節約する">
    * `?` を押してすべての利用可能なキーボードショートカットを表示する
    * Tab キーでコマンド補完を使用する
    * ↑ キーでコマンド履歴を表示する
    * `/` を入力してすべてのコマンドと skills を表示する
  </Accordion>
</AccordionGroup>

## 次のステップ

基本を学習したので、より高度な機能を探索してください：

<CardGroup cols={2}>
  <Card title="Claude Code の仕組み" icon="microchip" href="/ja/how-claude-code-works">
    agentic ループ、組み込みツール、および Claude Code がプロジェクトと相互作用する方法を理解する
  </Card>

  <Card title="ベストプラクティス" icon="star" href="/ja/best-practices">
    効果的なプロンプティングとプロジェクト設定でより良い結果を得る
  </Card>

  <Card title="一般的なワークフロー" icon="graduation-cap" href="/ja/common-workflows">
    一般的なタスクのステップバイステップガイド
  </Card>

  <Card title="Claude Code を拡張する" icon="puzzle-piece" href="/ja/features-overview">
    CLAUDE.md、skills、hooks、MCP などでカスタマイズする
  </Card>
</CardGroup>

## ヘルプを取得する

* **Claude Code 内**：`/help` を入力するか、「how do I...」と質問する
* **ドキュメント**：ここにいます！他のガイドを参照してください
* **コミュニティ**：[Discord](https://www.anthropic.com/discord) に参加して、ヒントとサポートを受けてください
