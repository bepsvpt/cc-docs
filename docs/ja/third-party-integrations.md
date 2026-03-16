> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# エンタープライズデプロイメント概要

> Claude Codeがさまざまなサードパーティサービスとインフラストラクチャと統合して、エンタープライズデプロイメント要件を満たす方法について学びます。

このページでは、利用可能なデプロイメントオプションの概要を提供し、組織に適した構成を選択するのに役立ちます。

## プロバイダー比較

<table>
  <thead>
    <tr>
      <th>機能</th>
      <th>Anthropic</th>
      <th>Amazon Bedrock</th>
      <th>Google Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>リージョン</td>
      <td>サポート対象[国](https://www.anthropic.com/supported-countries)</td>
      <td>複数のAWS [リージョン](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)</td>
      <td>複数のGCP [リージョン](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)</td>
      <td>複数のAzure [リージョン](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)</td>
    </tr>

    <tr>
      <td>プロンプトキャッシング</td>
      <td>デフォルトで有効</td>
      <td>デフォルトで有効</td>
      <td>デフォルトで有効</td>
      <td>デフォルトで有効</td>
    </tr>

    <tr>
      <td>認証</td>
      <td>APIキー</td>
      <td>APIキーまたはAWS認証情報</td>
      <td>GCP認証情報</td>
      <td>APIキーまたはMicrosoft Entra ID</td>
    </tr>

    <tr>
      <td>コスト追跡</td>
      <td>ダッシュボード</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
      <td>Azure Cost Management</td>
    </tr>

    <tr>
      <td>エンタープライズ機能</td>
      <td>チーム、使用状況監視</td>
      <td>IAMポリシー、CloudTrail</td>
      <td>IAMロール、Cloud Audit Logs</td>
      <td>RBACポリシー、Azure Monitor</td>
    </tr>
  </tbody>
</table>

## クラウドプロバイダー

<CardGroup cols={3}>
  <Card title="Amazon Bedrock" icon="aws" href="/ja/amazon-bedrock">
    AWSインフラストラクチャを通じてClaudeモデルを使用し、APIキーまたはIAMベースの認証とAWSネイティブ監視を備えています
  </Card>

  <Card title="Google Vertex AI" icon="google" href="/ja/google-vertex-ai">
    Google Cloud Platformを介してClaudeモデルにアクセスし、エンタープライズグレードのセキュリティとコンプライアンスを備えています
  </Card>

  <Card title="Microsoft Foundry" icon="microsoft" href="/ja/microsoft-foundry">
    Azureを通じてClaudeにアクセスし、APIキーまたはMicrosoft Entra ID認証とAzure課金を備えています
  </Card>
</CardGroup>

## 企業インフラストラクチャ

<CardGroup cols={2}>
  <Card title="Enterprise Network" icon="shield" href="/ja/network-config">
    Claude Codeを組織のプロキシサーバーとSSL/TLS要件と連携するように構成します
  </Card>

  <Card title="LLM Gateway" icon="server" href="/ja/llm-gateway">
    使用状況追跡、予算設定、監査ログを備えた集中型モデルアクセスをデプロイします
  </Card>
</CardGroup>

## 構成概要

Claude Codeは、異なるプロバイダーとインフラストラクチャを組み合わせることができる柔軟な構成オプションをサポートしています。

<Note>
  以下の違いを理解してください：

  * **企業プロキシ**: トラフィックをルーティングするためのHTTP/HTTPSプロキシ（`HTTPS_PROXY`または`HTTP_PROXY`経由で設定）
  * **LLM Gateway**: 認証を処理し、プロバイダー互換のエンドポイントを提供するサービス（`ANTHROPIC_BASE_URL`、`ANTHROPIC_BEDROCK_BASE_URL`、または`ANTHROPIC_VERTEX_BASE_URL`経由で設定）

  両方の構成を同時に使用できます。
</Note>

### 企業プロキシでBedrockを使用する

Bedrockトラフィックを企業HTTP/HTTPSプロキシを通じてルーティングします：

```bash  theme={null}
# Bedrockを有効にする
export CLAUDE_CODE_USE_BEDROCK=1
export AWS_REGION=us-east-1

# 企業プロキシを構成する
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### LLM GatewayでBedrockを使用する

Bedrock互換のエンドポイントを提供するゲートウェイサービスを使用します：

```bash  theme={null}
# Bedrockを有効にする
export CLAUDE_CODE_USE_BEDROCK=1

# LLM Gatewayを構成する
export ANTHROPIC_BEDROCK_BASE_URL='https://your-llm-gateway.com/bedrock'
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1  # ゲートウェイがAWS認証を処理する場合
```

### 企業プロキシでFoundryを使用する

Azureトラフィックを企業HTTP/HTTPSプロキシを通じてルーティングします：

```bash  theme={null}
# Microsoft Foundryを有効にする
export CLAUDE_CODE_USE_FOUNDRY=1
export ANTHROPIC_FOUNDRY_RESOURCE=your-resource
export ANTHROPIC_FOUNDRY_API_KEY=your-api-key  # またはEntra ID認証の場合は省略

# 企業プロキシを構成する
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### LLM GatewayでFoundryを使用する

Azure互換のエンドポイントを提供するゲートウェイサービスを使用します：

```bash  theme={null}
# Microsoft Foundryを有効にする
export CLAUDE_CODE_USE_FOUNDRY=1

# LLM Gatewayを構成する
export ANTHROPIC_FOUNDRY_BASE_URL='https://your-llm-gateway.com'
export CLAUDE_CODE_SKIP_FOUNDRY_AUTH=1  # ゲートウェイがAzure認証を処理する場合
```

### 企業プロキシでVertex AIを使用する

Vertex AIトラフィックを企業HTTP/HTTPSプロキシを通じてルーティングします：

```bash  theme={null}
# Vertexを有効にする
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
export ANTHROPIC_VERTEX_PROJECT_ID=your-project-id

# 企業プロキシを構成する
export HTTPS_PROXY='https://proxy.example.com:8080'
```

### LLM GatewayでVertex AIを使用する

Google Vertex AIモデルをLLM Gatewayと組み合わせて、集中管理を実現します：

```bash  theme={null}
# Vertexを有効にする
export CLAUDE_CODE_USE_VERTEX=1

# LLM Gatewayを構成する
export ANTHROPIC_VERTEX_BASE_URL='https://your-llm-gateway.com/vertex'
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1  # ゲートウェイがGCP認証を処理する場合
```

### 認証構成

Claude Codeは、必要に応じて`Authorization`ヘッダーに`ANTHROPIC_AUTH_TOKEN`を使用します。`SKIP_AUTH`フラグ（`CLAUDE_CODE_SKIP_BEDROCK_AUTH`、`CLAUDE_CODE_SKIP_VERTEX_AUTH`）は、ゲートウェイがプロバイダー認証を処理するLLM Gatewayシナリオで使用されます。

## 適切なデプロイメント構成を選択する

デプロイメントアプローチを選択する際は、以下の要因を考慮してください：

### 直接プロバイダーアクセス

以下の組織に最適です：

* 最もシンプルなセットアップを望む
* 既存のAWSまたはGCPインフラストラクチャを持っている
* プロバイダーネイティブの監視とコンプライアンスが必要

### 企業プロキシ

以下の組織に最適です：

* 既存の企業プロキシ要件を持っている
* トラフィック監視とコンプライアンスが必要
* すべてのトラフィックを特定のネットワークパスを通じてルーティングする必要がある

### LLM Gateway

以下の組織に最適です：

* チーム全体での使用状況追跡が必要
* モデル間を動的に切り替えたい
* カスタムレート制限または予算が必要
* 集中認証管理が必要

## デバッグ

デプロイメントをデバッグする場合：

* `claude /status` [スラッシュコマンド](/ja/slash-commands)を使用してください。このコマンドは、適用されている認証、プロキシ、およびURL設定の可視性を提供します。
* 環境変数`export ANTHROPIC_LOG=debug`を設定してリクエストをログします。

## 組織のベストプラクティス

### 1. ドキュメントとメモリに投資する

Claude Codeがコードベースを理解するようにドキュメントに投資することを強くお勧めします。組織は複数のレベルでCLAUDE.mdファイルをデプロイできます：

* **組織全体**: `/Library/Application Support/ClaudeCode/CLAUDE.md`（macOS）などのシステムディレクトリにデプロイして、会社全体の標準を設定します
* **リポジトリレベル**: リポジトリルートに`CLAUDE.md`ファイルを作成し、プロジェクトアーキテクチャ、ビルドコマンド、貢献ガイドラインを含めます。これらをソース管理にチェックインして、すべてのユーザーが利益を得られるようにします

  [詳細を学ぶ](/ja/memory)。

### 2. デプロイメントを簡素化する

カスタム開発環境がある場合、Claude Codeをインストールする「ワンクリック」の方法を作成することが、組織全体での採用を促進するための鍵となります。

### 3. ガイド付き使用から始める

新しいユーザーにClaude CodeをコードベースのQ\&Aや小さなバグ修正または機能リクエストで試すことを勧めます。Claude Codeに計画を立てるよう依頼してください。Claudeの提案を確認し、外れている場合はフィードバックを提供してください。時間が経つにつれて、ユーザーがこの新しいパラダイムをより理解するようになると、Claude Codeをより自律的に実行させるのに効果的になります。

### 4. セキュリティポリシーを構成する

セキュリティチームは、Claude Codeが実行できることと実行できないことに関する管理権限を構成できます。これはローカル構成によって上書きされません。[詳細を学ぶ](/ja/security)。

### 5. 統合にMCPを活用する

MCPは、チケット管理システムやエラーログへの接続など、Claude Codeにより多くの情報を提供する優れた方法です。1つの中央チームがMCPサーバーを構成し、`.mcp.json`構成をコードベースにチェックインして、すべてのユーザーが利益を得られるようにすることをお勧めします。[詳細を学ぶ](/ja/mcp)。

Anthropicでは、Claude CodeがすべてのAnthropicコードベース全体の開発を支援することを信頼しています。Claude Codeを使用することを楽しんでいただければ幸いです。

## 次のステップ

* [Amazon Bedrockをセットアップする](/ja/amazon-bedrock) - AWS固有のデプロイメント用
* [Google Vertex AIを構成する](/ja/google-vertex-ai) - GCPデプロイメント用
* [Microsoft Foundryをセットアップする](/ja/microsoft-foundry) - Azureデプロイメント用
* [Enterprise Networkを構成する](/ja/network-config) - ネットワーク要件用
* [LLM Gatewayをデプロイする](/ja/llm-gateway) - エンタープライズ管理用
* [設定](/ja/settings) - 構成オプションと環境変数用
