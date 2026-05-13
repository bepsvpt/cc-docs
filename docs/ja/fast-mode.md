> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 高速モードでレスポンスを高速化

> Claude Code で高速モードを切り替えて、Opus のレスポンスを高速化します。

<Note>
  高速モードは[リサーチプレビュー](#research-preview)段階です。機能、価格設定、および利用可能性はフィードバックに基づいて変更される可能性があります。
</Note>

高速モードは Claude Opus の高速構成で、モデルを 2.5 倍高速化しますが、トークンあたりのコストは高くなります。迅速な反復やライブデバッグなどのインタラクティブな作業で速度が必要な場合は `/fast` でオンにし、コストがレイテンシーより重要な場合はオフにします。

高速モードは異なるモデルではありません。Claude Opus を使用していますが、コスト効率よりも速度を優先する異なる API 構成です。同じ品質と機能が得られ、レスポンスが高速化されるだけです。高速モードは Opus 4.6 および Opus 4.7 でサポートされています。Sonnet、Haiku、または他のモデルでは利用できません。

<Note>
  高速モードには Claude Code v2.1.36 以降が必要です。`claude --version` でバージョンを確認してください。
</Note>

知っておくべきこと：

* Claude Code CLI で `/fast` を使用して高速モードをオンにします。Claude Code VS Code Extension でも `/fast` で利用可能です。
* デフォルトでは、`/fast` は Opus 4.6 で実行されます。代わりに Opus 4.7 で高速モードを実行するには、[`CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE`](#use-fast-mode-on-opus-4-7) 環境変数を設定します。
* 高速モード価格は Opus 4.6 と Opus 4.7 の両方で \$30/150 MTok です。
* サブスクリプションプラン（Pro/Max/Team/Enterprise）の Claude Code ユーザーと Claude Console のすべてのユーザーが利用可能です。
* サブスクリプションプラン（Pro/Max/Team/Enterprise）の Claude Code ユーザーの場合、高速モードは追加使用量のみで利用可能であり、サブスクリプションレート制限に含まれていません。

このページでは、[高速モードの切り替え](#toggle-fast-mode)、[Opus 4.7 で高速モードを使用](#use-fast-mode-on-opus-4-7)、[コストのトレードオフ](#understand-the-cost-tradeoff)、[使用時期の判断](#decide-when-to-use-fast-mode)、[要件](#requirements)、[セッションごとのオプトイン](#require-per-session-opt-in)、および[レート制限の処理](#handle-rate-limits)について説明します。

## 高速モードの切り替え

次のいずれかの方法で高速モードを切り替えます：

* `/fast` と入力して Tab キーを押してオンまたはオフに切り替える
* [ユーザー設定ファイル](/ja/settings)で `"fastMode": true` を設定する

デフォルトでは、高速モードはセッション全体で保持されます。管理者は高速モードを各セッションでリセットするように構成できます。詳細は[セッションごとのオプトインが必要](#require-per-session-opt-in)を参照してください。

最高のコスト効率を得るには、会話の途中で切り替えるのではなく、セッションの開始時に高速モードを有効にします。詳細は[コストのトレードオフを理解する](#understand-the-cost-tradeoff)を参照してください。

高速モードを有効にすると：

* 別のモデルを使用している場合、Claude Code は自動的に高速モードモデルに切り替わります：デフォルトでは Opus 4.6、または [`CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE`](#use-fast-mode-on-opus-4-7) が設定されている場合は Opus 4.7。
* 確認メッセージが表示されます：「Fast mode ON」
* 高速モードがアクティブな間、プロンプトの横に小さい `↯` アイコンが表示されます
* いつでも `/fast` を再度実行して、高速モードがオンかオフかを確認できます

`/fast` を再度実行して高速モードを無効にすると、高速モードが実行されていた同じ Opus バージョンに留まります。モデルは以前のモデルに戻りません。別のモデルに切り替えるには、`/model` を使用します。

## Opus 4.7 で高速モードを使用

<Note>
  Opus 4.7 での高速モードには Claude Code v2.1.139 以降が必要です。
</Note>

Claude Opus 4.7 の高速モードはリサーチプレビュー段階です。Opus 4.6 の高速モードと同じ 2.5 倍の速度と同じ価格で実行され、他の動作変更はありません。

<Note>
  2026 年 5 月 14 日に、Opus 4.7 が高速モードのデフォルトモデルになります。それまでは、`CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE=1` を設定してオプトインします。
</Note>

オプトインするには、Claude Code を起動する前に `CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE=1` を設定します。変数が設定されている場合、`/fast` は Opus 4.7 で実行されます。設定されていない場合、`/fast` は Opus 4.6 で実行され続けます。

変数をシェルエクスポートとして設定できます：

```bash theme={null}
export CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE=1
```

または、オプトインのスコープを設定するために、ユーザー、プロジェクト、管理設定を含む任意の Claude Code [設定ファイル](/ja/settings#settings-files)で設定します：

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE": "1"
  }
}
```

Opus 4.6 の高速モードは Opus 4.7 と並行して利用可能なままです。2 つは同じ高速モードレート制限プールを共有します：どちらかのモデルでの使用は同じ制限から引き出されます。

高速モードを Opus 4.6 に明示的にピンするには、`CLAUDE_CODE_OPUS_4_6_FAST_MODE_OVERRIDE=1` を設定します。この変数は優先されるため、`CLAUDE_CODE_ENABLE_OPUS_4_7_FAST_MODE` が設定されているかどうかに関わらず、高速モードは Opus 4.6 で実行されます。

## コストのトレードオフを理解する

高速モードは標準 Opus よりもトークンあたりの価格が高くなります：

| モード             | 入力（MTok） | 出力（MTok） |
| --------------- | -------- | -------- |
| Opus 4.6 の高速モード | \$30     | \$150    |
| Opus 4.7 の高速モード | \$30     | \$150    |

高速モード価格は完全な 1M トークンコンテキストウィンドウ全体で一定です。

会話の途中で高速モードに切り替えると、会話コンテキスト全体に対して完全な高速モードキャッシュなし入力トークン価格を支払います。これは最初から高速モードを有効にした場合よりもコストが高くなります。

## 高速モードの使用時期を判断する

高速モードはレスポンスレイテンシーがコストより重要なインタラクティブな作業に最適です：

* コード変更の迅速な反復
* ライブデバッグセッション
* 厳しい期限を持つ時間に敏感な作業

標準モードは以下に適しています：

* 速度がそれほど重要でない長い自動タスク
* バッチ処理または CI/CD パイプライン
* コストに敏感なワークロード

### 高速モードと努力レベル

高速モードと努力レベルはどちらもレスポンス速度に影響しますが、方法が異なります：

| 設定          | 効果                                  |
| ----------- | ----------------------------------- |
| **高速モード**   | 同じモデル品質、低レイテンシー、高コスト                |
| **低い努力レベル** | 思考時間が短い、レスポンスが高速、複雑なタスクでは品質が低下する可能性 |

両方を組み合わせることができます：単純なタスクで最大速度を得るために、低い[努力レベル](/ja/model-config#adjust-effort-level)で高速モードを使用します。

## 要件

高速モードには以下のすべてが必要です：

* **サードパーティクラウドプロバイダーでは利用不可**：高速モードは Amazon Bedrock、Google Vertex AI、または Microsoft Azure Foundry では利用できません。高速モードは Anthropic Console API および追加使用量を使用する Claude サブスクリプションプランで利用可能です。
* **追加使用量が有効**：アカウントで追加使用量が有効になっている必要があります。これにより、プランに含まれる使用量を超えて請求できます。個人アカウントの場合、[Console 請求設定](https://platform.claude.com/settings/organization/billing)で有効にします。Team および Enterprise の場合、管理者が組織の追加使用量を有効にする必要があります。

<Note>
  高速モード使用量は、プランに残りの使用量がある場合でも、追加使用量に直接請求されます。これは、高速モードトークンがプランに含まれる使用量にカウントされず、最初のトークンから高速モード料金で請求されることを意味します。
</Note>

* **Team および Enterprise の管理者による有効化**：高速モードは Team および Enterprise 組織ではデフォルトで無効になっています。ユーザーがアクセスできるようにするには、管理者が明示的に[高速モードを有効にする](#enable-fast-mode-for-your-organization)必要があります。

<Note>
  管理者が組織の高速モードを有効にしていない場合、`/fast` コマンドは「Fast mode has been disabled by your organization.」と表示されます。
</Note>

### 組織の高速モードを有効にする

管理者は以下で高速モードを有効にできます：

* **Console**（API カスタマー）：[Claude Code preferences](https://platform.claude.com/claude-code/preferences)
* **Claude AI**（Team および Enterprise）：[Admin Settings > Claude Code](https://claude.ai/admin-settings/claude-code)

高速モードを完全に無効にするもう 1 つのオプションは、`CLAUDE_CODE_DISABLE_FAST_MODE=1` を設定することです。[環境変数](/ja/env-vars)を参照してください。

### セッションごとのオプトインが必要

デフォルトでは、高速モードはセッション全体で保持されます：ユーザーが高速モードを有効にすると、将来のセッションでもオンのままです。[Team](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_teams#team-&-enterprise) または [Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=fast_mode_enterprise) プランの管理者は、[管理設定](/ja/settings#settings-files)または[サーバー管理設定](/ja/server-managed-settings)で `fastModePerSessionOptIn` を `true` に設定することでこれを防ぐことができます。これにより、各セッションは高速モードがオフで開始され、ユーザーが `/fast` で明示的に有効にする必要があります。

```json theme={null}
{
  "fastModePerSessionOptIn": true
}
```

これは、ユーザーが複数の同時セッションを実行する組織でコストを制御するのに役立ちます。ユーザーは速度が必要な場合でも `/fast` で高速モードを有効にできますが、新しいセッションの開始時にリセットされます。ユーザーの高速モード設定は保存されたままなので、この設定を削除するとデフォルトの永続的な動作が復元されます。

## レート制限の処理

高速モードは標準 Opus とは別のレート制限があります。Opus 4.6 および Opus 4.7 の高速モードは同じレート制限プールを共有します：どちらかのモデルでの使用は同じ制限から引き出されます。高速モードレート制限に達するか、追加使用量が不足した場合：

1. 高速モードは自動的に同じ Opus バージョンの標準速度にフォールバックします
2. `↯` アイコンがグレーに変わってクールダウンを示します
3. 標準速度と価格で作業を続けます
4. クールダウンが終了すると、高速モードは自動的に再度有効になります

クールダウンを待つ代わりに高速モードを手動で無効にするには、`/fast` を再度実行します。

## リサーチプレビュー

高速モードはリサーチプレビュー機能です。これは以下を意味します：

* 機能はフィードバックに基づいて変更される可能性があります
* 利用可能性と価格設定は変更される可能性があります
* 基盤となる API 構成は進化する可能性があります

通常の Anthropic サポートチャネルを通じて問題またはフィードバックを報告してください。

## 関連項目

* [モデル構成](/ja/model-config)：モデルを切り替えて努力レベルを調整する
* [コストを効果的に管理する](/ja/costs)：トークン使用量を追跡してコストを削減する
* [ステータスラインの構成](/ja/statusline)：モデルとコンテキスト情報を表示する
