> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# モデル設定

> Claude Code のモデル設定について学習します。opusplan などのモデルエイリアスを含みます。

## 利用可能なモデル

Claude Code の `model` 設定では、以下のいずれかを設定できます。

* **モデルエイリアス**
* **モデル名**
  * Anthropic API：完全な **[モデル名](https://platform.claude.com/docs/ja/about-claude/models/overview)**
  * Bedrock：推論プロファイル ARN
  * Foundry：デプロイメント名
  * Vertex：バージョン名

### モデルエイリアス

モデルエイリアスは、正確なバージョン番号を覚えることなくモデル設定を選択するための便利な方法を提供します。

| モデルエイリアス         | 動作                                                                                                                                                  |
| ---------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`default`**    | アカウントタイプに応じた推奨モデル設定                                                                                                                                 |
| **`sonnet`**     | 日常的なコーディングタスク用に最新の Sonnet モデル（現在は Sonnet 4.6）を使用します                                                                                                 |
| **`opus`**       | 複雑な推論タスク用に最新の Opus モデル（現在は Opus 4.6）を使用します                                                                                                          |
| **`haiku`**      | シンプルなタスク用に高速で効率的な Haiku モデルを使用します                                                                                                                   |
| **`sonnet[1m]`** | 長いセッション用に [100 万トークンのコンテキストウィンドウ](https://platform.claude.com/docs/ja/build-with-claude/context-windows#1m-token-context-window) を備えた Sonnet を使用します |
| **`opusplan`**   | Plan Mode 中は `opus` を使用し、実行中は `sonnet` に切り替わる特別なモード                                                                                                 |

エイリアスは常に最新バージョンを指します。特定のバージョンに固定するには、完全なモデル名（例：`claude-opus-4-6`）を使用するか、`ANTHROPIC_DEFAULT_OPUS_MODEL` のような対応する環境変数を設定します。

### モデルの設定

モデルは複数の方法で設定できます。優先順位順に以下の通りです。

1. **セッション中** - `/model <alias|name>` を使用してセッション中にモデルを切り替えます
2. **起動時** - `claude --model <alias|name>` で起動します
3. **環境変数** - `ANTHROPIC_MODEL=<alias|name>` を設定します
4. **設定** - `model` フィールドを使用して設定ファイルで永続的に設定します。

使用例：

```bash  theme={null}
# Opus で開始
claude --model opus

# セッション中に Sonnet に切り替え
/model sonnet
```

設定ファイルの例：

```json  theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## モデル選択の制限

エンタープライズ管理者は、[管理設定またはポリシー設定](/ja/settings#settings-files) で `availableModels` を使用して、ユーザーが選択できるモデルを制限できます。

`availableModels` が設定されている場合、ユーザーは `/model`、`--model` フラグ、Config ツール、または `ANTHROPIC_MODEL` 環境変数を使用してリスト内にないモデルに切り替えることはできません。

```json  theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### デフォルトモデルの動作

モデルピッカーの Default オプションは `availableModels` の影響を受けません。常に利用可能であり、[ユーザーのサブスクリプションティアに基づいた](#default-model-setting) システムのランタイムデフォルトを表します。

`availableModels: []` の場合でも、ユーザーはそのティア用の Default モデルで Claude Code を使用できます。

### ユーザーが実行するモデルを制御する

モデル体験を完全に制御するには、`availableModels` と `model` 設定を一緒に使用します。

* **availableModels**：ユーザーが切り替えられるものを制限します
* **model**：明示的なモデルオーバーライドを設定し、Default より優先されます

この例は、すべてのユーザーが Sonnet 4.6 を実行し、Sonnet と Haiku のみを選択できることを保証します。

```json  theme={null}
{
  "model": "sonnet",
  "availableModels": ["sonnet", "haiku"]
}
```

### マージ動作

`availableModels` がユーザー設定とプロジェクト設定など複数のレベルで設定されている場合、配列はマージされ、重複排除されます。厳密なアローリストを適用するには、最優先度を持つ管理設定またはポリシー設定で `availableModels` を設定します。

## 特別なモデルの動作

### `default` モデル設定

`default` の動作はアカウントタイプによって異なります。

* **Max と Team Premium**：Opus 4.6 がデフォルト
* **Pro と Team Standard**：Sonnet 4.6 がデフォルト
* **Enterprise**：Opus 4.6 は利用可能ですがデフォルトではありません

Claude Code は、Opus の使用量閾値に達した場合、自動的に Sonnet にフォールバックする可能性があります。

### `opusplan` モデル設定

`opusplan` モデルエイリアスは、自動化されたハイブリッドアプローチを提供します。

* **Plan Mode 中** - 複雑な推論とアーキテクチャの決定用に `opus` を使用します
* **実行モード中** - コード生成と実装用に自動的に `sonnet` に切り替わります

これにより、両方の長所が得られます。計画用の Opus の優れた推論と、実行用の Sonnet の効率性です。

### 努力レベルの調整

[努力レベル](https://platform.claude.com/docs/ja/build-with-claude/effort) は適応的推論を制御し、タスクの複雑さに基づいて思考を動的に割り当てます。低い努力はシンプルなタスクではより高速で安価ですが、高い努力は複雑な問題に対してより深い推論を提供します。

3 つのレベルが利用可能です。**low**、**medium**、**high**。Opus 4.6 は Max と Team サブスクライバーのデフォルトで medium 努力です。

**努力レベルの設定：**

* **`/model` 内**：モデルを選択する際に左右矢印キーを使用して努力スライダーを調整します
* **環境変数**：`CLAUDE_CODE_EFFORT_LEVEL=low|medium|high` を設定します
* **設定**：設定ファイルで `effortLevel` を設定します

努力は Opus 4.6 と Sonnet 4.6 でサポートされています。サポートされているモデルが選択されている場合、努力スライダーが `/model` に表示されます。現在の努力レベルはロゴとスピナーの横にも表示されます（例：「with low effort」）。`/model` を開かなくても、どの設定がアクティブであるかを確認できます。

Opus 4.6 と Sonnet 4.6 で適応的推論を無効にし、以前の固定思考予算に戻すには、`CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` を設定します。無効にされた場合、これらのモデルは `MAX_THINKING_TOKENS` で制御される固定予算を使用します。[環境変数](/ja/settings#environment-variables) を参照してください。

### 拡張コンテキスト

Opus 4.6 と Sonnet 4.6 は、大規模なコードベースを持つ長いセッション用に [100 万トークンのコンテキストウィンドウ](https://platform.claude.com/docs/ja/build-with-claude/context-windows#1m-token-context-window) をサポートしています。

<Note>
  1M コンテキストウィンドウは現在ベータ版です。機能、価格、および可用性は変更される可能性があります。
</Note>

拡張コンテキストは以下で利用可能です。

* **API と従量課金ユーザー**：1M コンテキストへのフルアクセス
* **Pro、Max、Teams、および Enterprise サブスクライバー**：[追加使用](https://support.claude.com/ja/articles/12429409-extra-usage-for-paid-claude-plans) が有効な場合に利用可能

1M コンテキストを完全に無効にするには、`CLAUDE_CODE_DISABLE_1M_CONTEXT=1` を設定します。これにより、1M モデルバリアントがモデルピッカーから削除されます。[環境変数](/ja/settings#environment-variables) を参照してください。

1M モデルを選択しても、請求はすぐには変わりません。セッションはコンテキストが 200K トークンを超えるまで標準レートを使用します。200K トークンを超えると、リクエストは [長コンテキスト価格](https://platform.claude.com/docs/ja/about-claude/pricing#long-context-pricing) で専用 [レート制限](https://platform.claude.com/docs/ja/api/rate-limits#long-context-rate-limits) で請求されます。サブスクライバーの場合、200K を超えるトークンはサブスクリプションではなく追加使用として請求されます。

アカウントが 1M コンテキストをサポートしている場合、オプションは Claude Code の最新バージョンのモデルピッカー（`/model`）に表示されます。表示されない場合は、セッションを再起動してみてください。

モデルエイリアスまたは完全なモデル名で `[1m]` サフィックスを使用することもできます。

```bash  theme={null}
# sonnet[1m] エイリアスを使用
/model sonnet[1m]

# または完全なモデル名に [1m] を追加
/model claude-sonnet-4-6[1m]
```

## 現在のモデルの確認

現在使用しているモデルは複数の方法で確認できます。

1. [ステータスライン](/ja/statusline) 内（設定されている場合）
2. `/status` 内。アカウント情報も表示されます。

## 環境変数

以下の環境変数を使用できます。これらはエイリアスがマップするモデル名を制御するために、完全な **モデル名**（または API プロバイダーの同等のもの）である必要があります。

| 環境変数                             | 説明                                                                           |
| -------------------------------- | ---------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | `opus` に使用するモデル、または Plan Mode がアクティブな場合の `opusplan` に使用するモデル。                |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | `sonnet` に使用するモデル、または Plan Mode がアクティブでない場合の `opusplan` に使用するモデル。            |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | `haiku` に使用するモデル、または [バックグラウンド機能](/ja/costs#background-token-usage) に使用するモデル |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | [subagents](/ja/sub-agents) に使用するモデル                                         |

注：`ANTHROPIC_SMALL_FAST_MODEL` は `ANTHROPIC_DEFAULT_HAIKU_MODEL` の代わりに非推奨です。

### サードパーティデプロイメント用のモデルのピン留め

[Bedrock](/ja/amazon-bedrock)、[Vertex AI](/ja/google-vertex-ai)、または [Foundry](/ja/microsoft-foundry) を通じて Claude Code をデプロイする場合、ユーザーへのロールアウト前にモデルバージョンをピン留めします。

ピン留めなしでは、Claude Code はモデルエイリアス（`sonnet`、`opus`、`haiku`）を使用し、最新バージョンに解決されます。Anthropic が新しいモデルをリリースすると、新しいバージョンが有効になっていないアカウントを持つユーザーは静かに破損します。

<Warning>
  初期セットアップの一部として、3 つのモデル環境変数すべてを特定のバージョン ID に設定します。このステップをスキップすると、Claude Code の更新があなたのアクションなしでユーザーを破損させる可能性があります。
</Warning>

プロバイダー用のバージョン固有のモデル ID で以下の環境変数を使用します。

| プロバイダー    | 例                                                                       |
| :-------- | :---------------------------------------------------------------------- |
| Bedrock   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |
| Foundry   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |

`ANTHROPIC_DEFAULT_SONNET_MODEL` と `ANTHROPIC_DEFAULT_HAIKU_MODEL` に同じパターンを適用します。すべてのプロバイダー全体の現在および従来のモデル ID については、[モデル概要](https://platform.claude.com/docs/ja/about-claude/models/overview) を参照してください。ユーザーを新しいモデルバージョンにアップグレードするには、これらの環境変数を更新して再デプロイします。

<Note>
  サードパーティプロバイダーを使用する場合、`settings.availableModels` アローリストは引き続き適用されます。フィルタリングはプロバイダー固有のモデル ID ではなく、モデルエイリアス（`opus`、`sonnet`、`haiku`）で一致します。
</Note>

### バージョンごとのモデル ID のオーバーライド

上記のファミリーレベルの環境変数は、ファミリーエイリアスごとに 1 つのモデル ID を設定します。同じファミリー内の複数のバージョンを異なるプロバイダー ID にマップする必要がある場合は、代わりに `modelOverrides` 設定を使用します。

`modelOverrides` は個別の Anthropic モデル ID をプロバイダー固有の文字列にマップします。Claude Code はこれらをプロバイダーの API に送信します。ユーザーが `/model` ピッカーでマップされたモデルを選択すると、Claude Code は組み込みのデフォルトの代わりに設定された値を使用します。

これにより、エンタープライズ管理者は、ガバナンス、コスト配分、または地域的ルーティング用に、各モデルバージョンを特定の Bedrock 推論プロファイル ARN、Vertex AI バージョン名、または Foundry デプロイメント名にルーティングできます。

[設定ファイル](/ja/settings#settings-files) で `modelOverrides` を設定します。

```json  theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

キーは [モデル概要](https://platform.claude.com/docs/ja/about-claude/models/overview) にリストされている Anthropic モデル ID である必要があります。日付付きモデル ID の場合、そこに表示されるとおりに日付サフィックスを含めます。不明なキーは無視されます。

オーバーライドは、`/model` ピッカーの各エントリをサポートする組み込みモデル ID を置き換えます。Bedrock では、オーバーライドは Claude Code が起動時に自動的に検出する推論プロファイルより優先されます。`ANTHROPIC_MODEL`、`--model`、または `ANTHROPIC_DEFAULT_*_MODEL` 環境変数を通じて直接提供する値は、プロバイダーにそのまま渡され、`modelOverrides` によって変換されません。

`modelOverrides` は `availableModels` と一緒に機能します。アローリストは Anthropic モデル ID に対して評価され、オーバーライド値に対してではないため、`availableModels` の `"opus"` のようなエントリは、Opus バージョンが ARN にマップされている場合でも一致し続けます。

### プロンプトキャッシング設定

Claude Code は [プロンプトキャッシング](https://platform.claude.com/docs/ja/build-with-claude/prompt-caching) を自動的に使用してパフォーマンスを最適化し、コストを削減します。プロンプトキャッシングをグローバルに、または特定のモデルティア用に無効にできます。

| 環境変数                            | 説明                                                       |
| ------------------------------- | -------------------------------------------------------- |
| `DISABLE_PROMPT_CACHING`        | すべてのモデルのプロンプトキャッシングを無効にするには `1` に設定します（モデル固有の設定より優先されます） |
| `DISABLE_PROMPT_CACHING_HAIKU`  | Haiku モデルのみのプロンプトキャッシングを無効にするには `1` に設定します               |
| `DISABLE_PROMPT_CACHING_SONNET` | Sonnet モデルのみのプロンプトキャッシングを無効にするには `1` に設定します              |
| `DISABLE_PROMPT_CACHING_OPUS`   | Opus モデルのみのプロンプトキャッシングを無効にするには `1` に設定します                |

これらの環境変数は、プロンプトキャッシング動作に対する細かい制御を提供します。グローバル `DISABLE_PROMPT_CACHING` 設定はモデル固有の設定より優先され、必要に応じてすべてのキャッシングをすばやく無効にできます。モデル固有の設定は、特定のモデルをデバッグする場合や、異なるキャッシング実装を持つ可能性があるクラウドプロバイダーと連携する場合など、選択的な制御に役立ちます。
