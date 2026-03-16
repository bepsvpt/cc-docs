> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code no Google Vertex AI

> Saiba como configurar Claude Code através do Google Vertex AI, incluindo configuração, configuração de IAM e resolução de problemas.

## Pré-requisitos

Antes de configurar Claude Code com Vertex AI, certifique-se de que você tem:

* Uma conta do Google Cloud Platform (GCP) com faturamento ativado
* Um projeto GCP com a API Vertex AI ativada
* Acesso aos modelos Claude desejados (por exemplo, Claude Sonnet 4.5)
* Google Cloud SDK (`gcloud`) instalado e configurado
* Cota alocada na região GCP desejada

## Configuração de região

Claude Code pode ser usado com endpoints globais e regionais do Vertex AI [global](https://cloud.google.com/blog/products/ai-machine-learning/global-endpoint-for-claude-models-generally-available-on-vertex-ai).

<Note>
  O Vertex AI pode não suportar os modelos padrão do Claude Code em todas as regiões. Você pode precisar mudar para uma [região ou modelo suportado](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations#genai-partner-models).
</Note>

<Note>
  O Vertex AI pode não suportar os modelos padrão do Claude Code em endpoints globais. Você pode precisar mudar para um endpoint regional ou [modelo suportado](https://cloud.google.com/vertex-ai/generative-ai/docs/partner-models/use-partner-models#supported_models).
</Note>

## Configuração

### 1. Ativar a API Vertex AI

Ative a API Vertex AI no seu projeto GCP:

```bash  theme={null}
# Defina seu ID de projeto
gcloud config set project YOUR-PROJECT-ID

# Ativar a API Vertex AI
gcloud services enable aiplatform.googleapis.com
```

### 2. Solicitar acesso ao modelo

Solicite acesso aos modelos Claude no Vertex AI:

1. Navegue até o [Vertex AI Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
2. Procure por modelos "Claude"
3. Solicite acesso aos modelos Claude desejados (por exemplo, Claude Sonnet 4.5)
4. Aguarde a aprovação (pode levar 24-48 horas)

### 3. Configurar credenciais GCP

Claude Code usa autenticação padrão do Google Cloud.

Para mais informações, consulte a [documentação de autenticação do Google Cloud](https://cloud.google.com/docs/authentication).

<Note>
  Ao autenticar, Claude Code usará automaticamente o ID do projeto da variável de ambiente `ANTHROPIC_VERTEX_PROJECT_ID`. Para substituir isso, defina uma destas variáveis de ambiente: `GCLOUD_PROJECT`, `GOOGLE_CLOUD_PROJECT` ou `GOOGLE_APPLICATION_CREDENTIALS`.
</Note>

### 4. Configurar Claude Code

Defina as seguintes variáveis de ambiente:

```bash  theme={null}
# Ativar integração Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=global
export ANTHROPIC_VERTEX_PROJECT_ID=YOUR-PROJECT-ID

# Opcional: Desativar prompt caching se necessário
export DISABLE_PROMPT_CACHING=1

# Quando CLOUD_ML_REGION=global, substituir região para modelos não suportados
export VERTEX_REGION_CLAUDE_3_5_HAIKU=us-east5

# Opcional: Substituir regiões para outros modelos específicos
export VERTEX_REGION_CLAUDE_3_5_SONNET=us-east5
export VERTEX_REGION_CLAUDE_3_7_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_0_OPUS=europe-west1
export VERTEX_REGION_CLAUDE_4_0_SONNET=us-east5
export VERTEX_REGION_CLAUDE_4_1_OPUS=europe-west1
```

<Note>
  [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching) é automaticamente suportado quando você especifica o sinalizador efêmero `cache_control`. Para desativá-lo, defina `DISABLE_PROMPT_CACHING=1`. Para limites de taxa aumentados, entre em contato com o suporte do Google Cloud.
</Note>

<Note>
  Ao usar Vertex AI, os comandos `/login` e `/logout` são desativados, pois a autenticação é tratada através de credenciais do Google Cloud.
</Note>

### 5. Configuração de modelo

Claude Code usa estes modelos padrão para Vertex AI:

| Tipo de modelo        | Valor padrão                 |
| :-------------------- | :--------------------------- |
| Modelo primário       | `claude-sonnet-4-5@20250929` |
| Modelo pequeno/rápido | `claude-haiku-4-5@20251001`  |

<Note>
  Para usuários do Vertex AI, Claude Code não será atualizado automaticamente de Haiku 3.5 para Haiku 4.5. Para mudar manualmente para um modelo Haiku mais recente, defina a variável de ambiente `ANTHROPIC_DEFAULT_HAIKU_MODEL` para o nome completo do modelo (por exemplo, `claude-haiku-4-5@20251001`).
</Note>

Para personalizar modelos:

```bash  theme={null}
export ANTHROPIC_MODEL='claude-opus-4-1@20250805'
export ANTHROPIC_SMALL_FAST_MODEL='claude-haiku-4-5@20251001'
```

## Configuração de IAM

Atribua as permissões de IAM necessárias:

A função `roles/aiplatform.user` inclui as permissões necessárias:

* `aiplatform.endpoints.predict` - Necessário para invocação de modelo e contagem de tokens

Para permissões mais restritivas, crie uma função personalizada com apenas as permissões acima.

Para detalhes, consulte a [documentação de IAM do Vertex](https://cloud.google.com/vertex-ai/docs/general/access-control).

<Note>
  Recomendamos criar um projeto GCP dedicado para Claude Code para simplificar o rastreamento de custos e controle de acesso.
</Note>

## Janela de contexto de 1M de tokens

Claude Sonnet 4 e Sonnet 4.5 suportam a [janela de contexto de 1M de tokens](https://platform.claude.com/docs/en/build-with-claude/context-windows#1m-token-context-window) no Vertex AI.

<Note>
  A janela de contexto de 1M de tokens está atualmente em beta. Para usar a janela de contexto estendida, inclua o cabeçalho beta `context-1m-2025-08-07` em suas solicitações do Vertex AI.
</Note>

## Resolução de problemas

Se você encontrar problemas de cota:

* Verifique as cotas atuais ou solicite um aumento de cota através do [Cloud Console](https://cloud.google.com/docs/quotas/view-manage)

Se você encontrar erros "model not found" 404:

* Confirme que o modelo está Ativado no [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden)
* Verifique se você tem acesso à região especificada
* Se estiver usando `CLOUD_ML_REGION=global`, verifique se seus modelos suportam endpoints globais no [Model Garden](https://console.cloud.google.com/vertex-ai/model-garden) em "Supported features". Para modelos que não suportam endpoints globais, faça um dos seguintes:
  * Especifique um modelo suportado via `ANTHROPIC_MODEL` ou `ANTHROPIC_SMALL_FAST_MODEL`, ou
  * Defina um endpoint regional usando variáveis de ambiente `VERTEX_REGION_<MODEL_NAME>`

Se você encontrar erros 429:

* Para endpoints regionais, certifique-se de que o modelo primário e o modelo pequeno/rápido são suportados em sua região selecionada
* Considere mudar para `CLOUD_ML_REGION=global` para melhor disponibilidade

## Recursos adicionais

* [Documentação do Vertex AI](https://cloud.google.com/vertex-ai/docs)
* [Preços do Vertex AI](https://cloud.google.com/vertex-ai/pricing)
* [Cotas e limites do Vertex AI](https://cloud.google.com/vertex-ai/docs/quotas)
