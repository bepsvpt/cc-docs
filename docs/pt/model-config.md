> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Configuração de modelo

> Saiba mais sobre a configuração do modelo Claude Code, incluindo aliases de modelo como `opusplan`

## Modelos disponíveis

Para a configuração `model` no Claude Code, você pode configurar:

* Um **alias de modelo**
* Um **nome de modelo**
  * API Anthropic: Um **[nome de modelo](https://platform.claude.com/docs/pt/about-claude/models/overview)** completo
  * Bedrock: um ARN de perfil de inferência
  * Foundry: um nome de implantação
  * Vertex: um nome de versão

### Aliases de modelo

Os aliases de modelo fornecem uma maneira conveniente de selecionar configurações de modelo sem precisar lembrar dos números exatos da versão:

| Alias de modelo  | Comportamento                                                                                                                                                                    |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **`default`**    | Valor especial que limpa qualquer substituição de modelo e reverte para o modelo recomendado para seu tipo de conta. Não é em si um alias de modelo                              |
| **`best`**       | Usa o modelo mais capaz disponível, atualmente equivalente a `opus`                                                                                                              |
| **`sonnet`**     | Usa o modelo Sonnet mais recente (atualmente Sonnet 4.6) para tarefas de codificação diária                                                                                      |
| **`opus`**       | Usa o modelo Opus mais recente (atualmente Opus 4.6) para tarefas de raciocínio complexo                                                                                         |
| **`haiku`**      | Usa o modelo Haiku rápido e eficiente para tarefas simples                                                                                                                       |
| **`sonnet[1m]`** | Usa Sonnet com uma [janela de contexto de 1 milhão de tokens](https://platform.claude.com/docs/pt/build-with-claude/context-windows#1m-token-context-window) para sessões longas |
| **`opus[1m]`**   | Usa Opus com uma [janela de contexto de 1 milhão de tokens](https://platform.claude.com/docs/pt/build-with-claude/context-windows#1m-token-context-window) para sessões longas   |
| **`opusplan`**   | Modo especial que usa `opus` durante o modo de plano, depois muda para `sonnet` para execução                                                                                    |

Os aliases sempre apontam para a versão mais recente. Para fixar uma versão específica, use o nome completo do modelo (por exemplo, `claude-opus-4-6`) ou defina a variável de ambiente correspondente como `ANTHROPIC_DEFAULT_OPUS_MODEL`.

### Configurando seu modelo

Você pode configurar seu modelo de várias maneiras, listadas em ordem de prioridade:

1. **Durante a sessão** - Use `/model <alias|name>` para alternar modelos durante a sessão
2. **Na inicialização** - Inicie com `claude --model <alias|name>`
3. **Variável de ambiente** - Defina `ANTHROPIC_MODEL=<alias|name>`
4. **Configurações** - Configure permanentemente em seu arquivo de configurações usando o campo `model`.

Exemplo de uso:

```bash  theme={null}
# Iniciar com Opus
claude --model opus

# Alternar para Sonnet durante a sessão
/model sonnet
```

Exemplo de arquivo de configurações:

```json  theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## Restringir seleção de modelo

Os administradores corporativos podem usar `availableModels` em [configurações gerenciadas ou de política](/pt/settings#settings-files) para restringir quais modelos os usuários podem selecionar.

Quando `availableModels` é definido, os usuários não podem alternar para modelos que não estão na lista via `/model`, sinalizador `--model`, ferramenta Config ou variável de ambiente `ANTHROPIC_MODEL`.

```json  theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

### Comportamento do modelo padrão

A opção Padrão no seletor de modelo não é afetada por `availableModels`. Ela sempre permanece disponível e representa o padrão de tempo de execução do sistema [baseado no nível de assinatura do usuário](#default-model-setting).

Mesmo com `availableModels: []`, os usuários ainda podem usar Claude Code com o modelo Padrão para seu nível.

### Controlar o modelo em que os usuários executam

A configuração `model` é uma seleção inicial, não uma imposição. Ela define qual modelo está ativo quando uma sessão é iniciada, mas os usuários ainda podem abrir `/model` e escolher Padrão, que se resolve para o padrão do sistema para seu nível, independentemente do que `model` está definido.

Para controlar totalmente a experiência do modelo, combine três configurações:

* **`availableModels`**: restringe para quais modelos nomeados os usuários podem alternar
* **`model`**: define a seleção de modelo inicial quando uma sessão é iniciada
* **`ANTHROPIC_DEFAULT_SONNET_MODEL`** / **`ANTHROPIC_DEFAULT_OPUS_MODEL`** / **`ANTHROPIC_DEFAULT_HAIKU_MODEL`**: controlam para o que a opção Padrão e os aliases `sonnet`, `opus` e `haiku` se resolvem

Este exemplo inicia os usuários em Sonnet 4.5, limita o seletor a Sonnet e Haiku, e fixa Padrão para se resolver em Sonnet 4.5 em vez da versão mais recente:

```json  theme={null}
{
  "model": "claude-sonnet-4-5",
  "availableModels": ["claude-sonnet-4-5", "haiku"],
  "env": {
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "claude-sonnet-4-5"
  }
}
```

Sem o bloco `env`, um usuário que seleciona Padrão no seletor obteria a versão mais recente do Sonnet, contornando a fixação de versão em `model` e `availableModels`.

### Comportamento de mesclagem

Quando `availableModels` é definido em vários níveis, como configurações de usuário e configurações de projeto, os arrays são mesclados e desduplicados. Para impor uma lista de permissões rigorosa, defina `availableModels` em configurações gerenciadas ou de política que têm a prioridade mais alta.

## Comportamento especial do modelo

### Configuração do modelo `default`

O comportamento de `default` depende do tipo de sua conta:

* **Max e Team Premium**: padrão para Opus 4.6
* **Pro e Team Standard**: padrão para Sonnet 4.6
* **Enterprise**: Opus 4.6 está disponível, mas não é o padrão

Claude Code pode fazer fallback automaticamente para Sonnet se você atingir um limite de uso com Opus.

### Configuração do modelo `opusplan`

O alias de modelo `opusplan` fornece uma abordagem híbrida automatizada:

* **No modo de plano** - Usa `opus` para raciocínio complexo e decisões de arquitetura
* **No modo de execução** - Muda automaticamente para `sonnet` para geração de código e implementação

Isso oferece o melhor dos dois mundos: o raciocínio superior do Opus para planejamento e a eficiência do Sonnet para execução.

### Ajustar nível de esforço

[Níveis de esforço](https://platform.claude.com/docs/pt/build-with-claude/effort) controlam raciocínio adaptativo, que aloca dinamicamente o pensamento com base na complexidade da tarefa. Esforço menor é mais rápido e mais barato para tarefas diretas, enquanto esforço maior fornece raciocínio mais profundo para problemas complexos.

Três níveis persistem entre sessões: **low**, **medium** e **high**. Um quarto nível, **max**, fornece o raciocínio mais profundo sem restrição no gasto de tokens, portanto as respostas são mais lentas e custam mais do que em `high`. `max` está disponível apenas em Opus 4.6 e não persiste entre sessões, exceto através da variável de ambiente `CLAUDE_CODE_EFFORT_LEVEL`.

Opus 4.6 e Sonnet 4.6 usam como padrão esforço médio. Isso se aplica a todos os provedores, incluindo Bedrock, Vertex AI e acesso direto à API.

Médio é o nível recomendado para a maioria das tarefas de codificação: equilibra velocidade e profundidade de raciocínio, e níveis mais altos podem fazer o modelo pensar demais em trabalho rotineiro. Reserve `high` ou `max` para tarefas que genuinamente se beneficiam de raciocínio mais profundo, como problemas de depuração difíceis ou decisões arquitetônicas complexas.

Para raciocínio profundo único sem alterar sua configuração de sessão, inclua "ultrathink" em seu prompt para disparar esforço alto para essa vez.

**Configurando esforço:**

* **`/effort`**: execute `/effort low`, `/effort medium`, `/effort high` ou `/effort max` para alterar o nível, ou `/effort auto` para redefinir para o padrão do modelo
* **Em `/model`**: use as teclas de seta esquerda/direita para ajustar o controle deslizante de esforço ao selecionar um modelo
* **Sinalizador `--effort`**: passe `low`, `medium`, `high` ou `max` para definir o nível para uma única sessão ao iniciar Claude Code
* **Variável de ambiente**: defina `CLAUDE_CODE_EFFORT_LEVEL` para `low`, `medium`, `high`, `max` ou `auto`
* **Configurações**: defina `effortLevel` em seu arquivo de configurações para `"low"`, `"medium"` ou `"high"`
* **Frontmatter de skill e subagent**: defina `effort` em um arquivo markdown de [skill](/pt/skills#frontmatter-reference) ou [subagent](/pt/sub-agents#supported-frontmatter-fields) para substituir o nível de esforço quando esse skill ou subagent é executado

A variável de ambiente tem precedência sobre todos os outros métodos, depois seu nível configurado, depois o padrão do modelo. O esforço de frontmatter se aplica quando esse skill ou subagent está ativo, substituindo o nível de sessão, mas não a variável de ambiente.

O esforço é suportado em Opus 4.6 e Sonnet 4.6. O controle deslizante de esforço aparece em `/model` quando um modelo suportado é selecionado. O nível de esforço atual também é exibido ao lado do logo e spinner, por exemplo "with low effort", para que você possa confirmar qual configuração está ativa sem abrir `/model`.

Para desabilitar raciocínio adaptativo em Opus 4.6 e Sonnet 4.6 e reverter para o orçamento de pensamento fixo anterior, defina `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1`. Quando desabilitado, esses modelos usam o orçamento fixo controlado por `MAX_THINKING_TOKENS`. Veja [variáveis de ambiente](/pt/env-vars).

### Contexto estendido

Opus 4.6 e Sonnet 4.6 suportam uma [janela de contexto de 1 milhão de tokens](https://platform.claude.com/docs/pt/build-with-claude/context-windows#1m-token-context-window) para sessões longas com grandes bases de código.

A disponibilidade varia por modelo e plano. Nos planos Max, Team e Enterprise, Opus é automaticamente atualizado para contexto 1M sem configuração adicional. Isso se aplica aos assentos Team Standard e Team Premium.

| Plano                          | Opus 4.6 com contexto 1M                                                                              | Sonnet 4.6 com contexto 1M                                                                            |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Max, Team e Enterprise         | Incluído na assinatura                                                                                | Requer [uso extra](https://support.claude.com/pt/articles/12429409-extra-usage-for-paid-claude-plans) |
| Pro                            | Requer [uso extra](https://support.claude.com/pt/articles/12429409-extra-usage-for-paid-claude-plans) | Requer [uso extra](https://support.claude.com/pt/articles/12429409-extra-usage-for-paid-claude-plans) |
| API e pagamento conforme o uso | Acesso completo                                                                                       | Acesso completo                                                                                       |

Para desabilitar completamente o contexto 1M, defina `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. Isso remove variantes de modelo 1M do seletor de modelo. Veja [variáveis de ambiente](/pt/env-vars).

A janela de contexto 1M usa preços de modelo padrão sem prêmio para tokens além de 200K. Para planos onde o contexto estendido está incluído em sua assinatura, o uso permanece coberto por sua assinatura. Para planos que acessam contexto estendido através de uso extra, os tokens são cobrados para uso extra.

Se sua conta suporta contexto 1M, a opção aparece no seletor de modelo (`/model`) nas versões mais recentes do Claude Code. Se você não a vir, tente reiniciar sua sessão.

Você também pode usar o sufixo `[1m]` com aliases de modelo ou nomes de modelo completos:

```bash  theme={null}
# Use o alias opus[1m] ou sonnet[1m]
/model opus[1m]
/model sonnet[1m]

# Ou anexe [1m] a um nome de modelo completo
/model claude-opus-4-6[1m]
```

## Verificando seu modelo atual

Você pode ver qual modelo está usando atualmente de várias maneiras:

1. Na [linha de status](/pt/statusline) (se configurada)
2. Em `/status`, que também exibe as informações de sua conta.

## Adicionar uma opção de modelo personalizado

Use `ANTHROPIC_CUSTOM_MODEL_OPTION` para adicionar uma única entrada personalizada ao seletor `/model` sem substituir os aliases integrados. Isso é útil para implantações de gateway LLM ou teste de IDs de modelo que Claude Code não lista por padrão.

Este exemplo define todas as três variáveis para tornar uma implantação Opus roteada por gateway selecionável:

```bash  theme={null}
export ANTHROPIC_CUSTOM_MODEL_OPTION="my-gateway/claude-opus-4-6"
export ANTHROPIC_CUSTOM_MODEL_OPTION_NAME="Opus via Gateway"
export ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION="Custom deployment routed through the internal LLM gateway"
```

A entrada personalizada aparece na parte inferior do seletor `/model`. `ANTHROPIC_CUSTOM_MODEL_OPTION_NAME` e `ANTHROPIC_CUSTOM_MODEL_OPTION_DESCRIPTION` são opcionais. Se omitidos, o ID do modelo é usado como o nome e a descrição padrão é `Custom model (<model-id>)`.

Claude Code ignora a validação para o ID do modelo definido em `ANTHROPIC_CUSTOM_MODEL_OPTION`, portanto você pode usar qualquer string que seu endpoint de API aceite.

## Variáveis de ambiente

Você pode usar as seguintes variáveis de ambiente, que devem ser **nomes de modelo** completos (ou equivalente para seu provedor de API), para controlar os nomes de modelo para os quais os aliases mapeiam.

| Variável de ambiente             | Descrição                                                                                    |
| -------------------------------- | -------------------------------------------------------------------------------------------- |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`   | O modelo a usar para `opus`, ou para `opusplan` quando Plan Mode está ativo.                 |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | O modelo a usar para `sonnet`, ou para `opusplan` quando Plan Mode não está ativo.           |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`  | O modelo a usar para `haiku`, ou [funcionalidade de fundo](/pt/costs#background-token-usage) |
| `CLAUDE_CODE_SUBAGENT_MODEL`     | O modelo a usar para [subagents](/pt/sub-agents)                                             |

Nota: `ANTHROPIC_SMALL_FAST_MODEL` está descontinuado em favor de `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

### Fixar modelos para implantações de terceiros

Ao implantar Claude Code através de [Bedrock](/pt/amazon-bedrock), [Vertex AI](/pt/google-vertex-ai) ou [Foundry](/pt/microsoft-foundry), fixe versões de modelo antes de lançar para usuários.

Sem fixação, Claude Code usa aliases de modelo (`sonnet`, `opus`, `haiku`) que resolvem para a versão mais recente. Quando Anthropic lança um novo modelo, os usuários cujas contas não têm a nova versão habilitada quebrarão silenciosamente.

<Warning>
  Defina todas as três variáveis de ambiente de modelo para IDs de versão específicos como parte de sua configuração inicial. Pular esta etapa significa que uma atualização do Claude Code pode quebrar seus usuários sem nenhuma ação de sua parte.
</Warning>

Use as seguintes variáveis de ambiente com IDs de modelo específicos de versão para seu provedor:

| Provedor  | Exemplo                                                                 |
| :-------- | :---------------------------------------------------------------------- |
| Bedrock   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-6-v1'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |
| Foundry   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6'`                 |

Aplique o mesmo padrão para `ANTHROPIC_DEFAULT_SONNET_MODEL` e `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Para IDs de modelo atuais e legados em todos os provedores, veja [Visão geral de modelos](https://platform.claude.com/docs/pt/about-claude/models/overview). Para atualizar usuários para uma nova versão de modelo, atualize essas variáveis de ambiente e reimplante.

Para habilitar [contexto estendido](#extended-context) para um modelo fixado, anexe `[1m]` ao ID do modelo em `ANTHROPIC_DEFAULT_OPUS_MODEL` ou `ANTHROPIC_DEFAULT_SONNET_MODEL`:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-6[1m]'
```

O sufixo `[1m]` aplica a janela de contexto 1M a todo o uso desse alias, incluindo `opusplan`. Claude Code remove o sufixo antes de enviar o ID do modelo para seu provedor. Apenas anexe `[1m]` quando o modelo subjacente suportar contexto 1M, como Opus 4.6 ou Sonnet 4.6.

<Note>
  A lista de permissões `settings.availableModels` ainda se aplica ao usar provedores de terceiros. A filtragem corresponde ao alias de modelo (`opus`, `sonnet`, `haiku`), não ao ID de modelo específico do provedor.
</Note>

### Personalizar exibição e capacidades do modelo fixado

Quando você fixa um modelo em um provedor de terceiros, o ID específico do provedor aparece como está no seletor `/model` e Claude Code pode não reconhecer quais recursos o modelo suporta. Você pode substituir o nome de exibição e declarar capacidades com variáveis de ambiente complementares para cada modelo fixado.

Essas variáveis só têm efeito em provedores de terceiros, como Bedrock, Vertex AI e Foundry. Elas não têm efeito ao usar a API Anthropic diretamente.

| Variável de ambiente                                  | Descrição                                                                                                                |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME`                   | Nome de exibição para o modelo Opus fixado no seletor `/model`. Padrão para o ID do modelo quando não definido           |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION`            | Descrição de exibição para o modelo Opus fixado no seletor `/model`. Padrão para `Custom Opus model` quando não definido |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` | Lista separada por vírgulas de capacidades que o modelo Opus fixado suporta                                              |

Os mesmos sufixos `_NAME`, `_DESCRIPTION` e `_SUPPORTED_CAPABILITIES` estão disponíveis para `ANTHROPIC_DEFAULT_SONNET_MODEL` e `ANTHROPIC_DEFAULT_HAIKU_MODEL`.

Claude Code habilita recursos como [níveis de esforço](#adjust-effort-level) e [pensamento estendido](/pt/common-workflows#use-extended-thinking-thinking-mode) correspondendo o ID do modelo contra padrões conhecidos. IDs específicos do provedor, como ARNs Bedrock ou nomes de implantação personalizados, geralmente não correspondem a esses padrões, deixando recursos suportados desabilitados. Defina `_SUPPORTED_CAPABILITIES` para informar ao Claude Code quais recursos o modelo realmente suporta:

| Valor de capacidade    | Habilita                                                                                      |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| `effort`               | [Níveis de esforço](#adjust-effort-level) e o comando `/effort`                               |
| `max_effort`           | O nível de esforço `max`                                                                      |
| `thinking`             | [Pensamento estendido](/pt/common-workflows#use-extended-thinking-thinking-mode)              |
| `adaptive_thinking`    | Raciocínio adaptativo que aloca dinamicamente o pensamento com base na complexidade da tarefa |
| `interleaved_thinking` | Pensamento entre chamadas de ferramenta                                                       |

Quando `_SUPPORTED_CAPABILITIES` é definido, as capacidades listadas são habilitadas e as capacidades não listadas são desabilitadas para o modelo fixado correspondente. Quando a variável não está definida, Claude Code volta para detecção integrada baseada no ID do modelo.

Este exemplo fixa Opus para um ARN de modelo personalizado Bedrock, define um nome amigável e declara suas capacidades:

```bash  theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='arn:aws:bedrock:us-east-1:123456789012:custom-model/abc'
export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME='Opus via Bedrock'
export ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION='Opus 4.6 routed through a Bedrock custom endpoint'
export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES='effort,max_effort,thinking,adaptive_thinking,interleaved_thinking'
```

### Substituir IDs de modelo por versão

As variáveis de ambiente no nível de família acima configuram um ID de modelo por alias de família. Se você precisar mapear várias versões dentro da mesma família para IDs de provedor distintos, use a configuração `modelOverrides` em vez disso.

`modelOverrides` mapeia IDs de modelo Anthropic individuais para as strings específicas do provedor que Claude Code envia para a API do seu provedor. Quando um usuário seleciona um modelo mapeado no seletor `/model`, Claude Code usa seu valor configurado em vez do padrão integrado.

Isso permite que administradores corporativos roteiem cada versão de modelo para um ARN de perfil de inferência Bedrock específico, nome de versão Vertex AI ou nome de implantação Foundry para governança, alocação de custos ou roteamento regional.

Defina `modelOverrides` em seu [arquivo de configurações](/pt/settings#settings-files):

```json  theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-5-20251101": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-45-prod",
    "claude-sonnet-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/sonnet-prod"
  }
}
```

As chaves devem ser IDs de modelo Anthropic conforme listado na [Visão geral de modelos](https://platform.claude.com/docs/pt/about-claude/models/overview). Para IDs de modelo datados, inclua o sufixo de data exatamente como aparece lá. Chaves desconhecidas são ignoradas.

As substituições substituem os IDs de modelo integrados que suportam cada entrada no seletor `/model`. No Bedrock, as substituições têm precedência sobre qualquer perfil de inferência que Claude Code descobre automaticamente na inicialização. Os valores que você fornece diretamente através de `ANTHROPIC_MODEL`, `--model` ou as variáveis de ambiente `ANTHROPIC_DEFAULT_*_MODEL` são passados para o provedor como estão e não são transformados por `modelOverrides`.

`modelOverrides` funciona junto com `availableModels`. A lista de permissões é avaliada contra o ID de modelo Anthropic, não o valor de substituição, então uma entrada como `"opus"` em `availableModels` continua a corresponder mesmo quando versões do Opus são mapeadas para ARNs.

### Configuração de prompt caching

Claude Code usa automaticamente [prompt caching](https://platform.claude.com/docs/pt/build-with-claude/prompt-caching) para otimizar o desempenho e reduzir custos. Você pode desabilitar prompt caching globalmente ou para níveis de modelo específicos:

| Variável de ambiente            | Descrição                                                                                                              |
| ------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `DISABLE_PROMPT_CACHING`        | Defina como `1` para desabilitar prompt caching para todos os modelos (tem precedência sobre configurações por modelo) |
| `DISABLE_PROMPT_CACHING_HAIKU`  | Defina como `1` para desabilitar prompt caching apenas para modelos Haiku                                              |
| `DISABLE_PROMPT_CACHING_SONNET` | Defina como `1` para desabilitar prompt caching apenas para modelos Sonnet                                             |
| `DISABLE_PROMPT_CACHING_OPUS`   | Defina como `1` para desabilitar prompt caching apenas para modelos Opus                                               |

Essas variáveis de ambiente oferecem controle refinado sobre o comportamento de prompt caching. A configuração global `DISABLE_PROMPT_CACHING` tem precedência sobre as configurações específicas do modelo, permitindo que você desabilite rapidamente todo o caching quando necessário. As configurações por modelo são úteis para controle seletivo, como ao depurar modelos específicos ou trabalhar com provedores de nuvem que podem ter implementações de caching diferentes.
