> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

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
| **`sonnet`**     | Usa o modelo Sonnet mais recente para tarefas de codificação diária                                                                                                              |
| **`opus`**       | Usa o modelo Opus mais recente para tarefas de raciocínio complexo                                                                                                               |
| **`haiku`**      | Usa o modelo Haiku rápido e eficiente para tarefas simples                                                                                                                       |
| **`sonnet[1m]`** | Usa Sonnet com uma [janela de contexto de 1 milhão de tokens](https://platform.claude.com/docs/pt/build-with-claude/context-windows#1m-token-context-window) para sessões longas |
| **`opus[1m]`**   | Usa Opus com uma [janela de contexto de 1 milhão de tokens](https://platform.claude.com/docs/pt/build-with-claude/context-windows#1m-token-context-window) para sessões longas   |
| **`opusplan`**   | Modo especial que usa `opus` durante o modo de plano, depois muda para `sonnet` para execução                                                                                    |

Na API Anthropic, `opus` se resolve para Opus 4.7 e `sonnet` se resolve para Sonnet 4.6. No Bedrock, Vertex e Foundry, `opus` se resolve para Opus 4.6 e `sonnet` se resolve para Sonnet 4.5; modelos mais recentes estão disponíveis nesses provedores selecionando o nome completo do modelo explicitamente ou definindo `ANTHROPIC_DEFAULT_OPUS_MODEL` ou `ANTHROPIC_DEFAULT_SONNET_MODEL`.

Os aliases apontam para a versão recomendada para seu provedor e são atualizados ao longo do tempo. Para fixar uma versão específica, use o nome completo do modelo (por exemplo, `claude-opus-4-7`) ou defina a variável de ambiente correspondente como `ANTHROPIC_DEFAULT_OPUS_MODEL`.

<Note>
  Opus 4.7 requer Claude Code v2.1.111 ou posterior. Execute `claude update` para atualizar.
</Note>

### Configurando seu modelo

Você pode configurar seu modelo de várias maneiras, listadas em ordem de prioridade:

1. **Durante a sessão** - Use `/model <alias|name>` para alternar imediatamente, ou execute `/model` sem argumentos para abrir o seletor. O seletor pede confirmação quando a conversa tem saída anterior, pois a próxima resposta relê o histórico completo sem contexto em cache
2. **Na inicialização** - Inicie com `claude --model <alias|name>`
3. **Variável de ambiente** - Defina `ANTHROPIC_MODEL=<alias|name>`
4. **Configurações** - Configure permanentemente em seu arquivo de configurações usando o campo `model`.

Sua seleção de `/model` é salva nas configurações do usuário e persiste entre reinicializações. A partir da v2.1.117, se o `.claude/settings.json` do projeto fixar um modelo diferente, Claude Code também escreve sua escolha em `.claude/settings.local.json` para que continue a se aplicar nesse projeto após uma reinicialização. As configurações gerenciadas têm precedência e são reaplicadas no próximo lançamento.

Quando o modelo ativo na inicialização vem das configurações do projeto ou gerenciadas em vez de sua própria seleção, o cabeçalho de inicialização mostra qual arquivo de configurações o definiu. Execute `/model` para substituir pela sessão atual.

Exemplo de uso:

```bash theme={null}
# Iniciar com Opus
claude --model opus

# Alternar para Sonnet durante a sessão
/model sonnet
```

Exemplo de arquivo de configurações:

```json theme={null}
{
    "permissions": {
        ...
    },
    "model": "opus"
}
```

## Restringir seleção de modelo

Os administradores corporativos podem usar `availableModels` em [configurações gerenciadas ou de política](/pt/settings#settings-files) para restringir quais modelos os usuários podem selecionar.

Quando `availableModels` é definido, os usuários não podem alternar para modelos que não estão na lista via `/model`, sinalizador `--model` ou variável de ambiente `ANTHROPIC_MODEL`.

```json theme={null}
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

```json theme={null}
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

### IDs de modelo Mantle

Quando o [endpoint Bedrock Mantle](/pt/amazon-bedrock#use-the-mantle-endpoint) está habilitado, entradas em `availableModels` que começam com `anthropic.` são adicionadas ao seletor `/model` como opções personalizadas e roteadas para o endpoint Mantle. Esta é uma exceção à correspondência somente de alias descrita em [Fixar modelos para implantações de terceiros](#pin-models-for-third-party-deployments). A configuração ainda restringe o seletor às entradas listadas, portanto inclua os aliases padrão junto com qualquer ID Mantle.

## Comportamento especial do modelo

### Configuração do modelo `default`

O comportamento de `default` depende do tipo de sua conta:

* **Max e Team Premium**: padrão para Opus 4.7
* **Pro, Team Standard, Enterprise e API Anthropic**: padrão para Sonnet 4.6
* **Bedrock, Vertex e Foundry**: padrão para Sonnet 4.5

Claude Code pode fazer fallback automaticamente para Sonnet se você atingir um limite de uso com Opus.

<Note>
  Em 23 de abril de 2026, o modelo padrão para usuários Enterprise pagos conforme o uso e API Anthropic mudará para Opus 4.7. Para manter um padrão diferente, defina `ANTHROPIC_MODEL` ou o campo `model` em [configurações gerenciadas pelo servidor](/pt/server-managed-settings).
</Note>

### Configuração do modelo `opusplan`

O alias de modelo `opusplan` fornece uma abordagem híbrida automatizada:

* **No Plan Mode** - Usa `opus` para raciocínio complexo e decisões de arquitetura
* **No modo de execução** - Muda automaticamente para `sonnet` para geração de código e implementação

Isso oferece o melhor dos dois mundos: o raciocínio superior do Opus para planejamento e a eficiência do Sonnet para execução.

A fase Opus do Plan Mode é executada com a janela de contexto padrão de 200K. A atualização automática de 1M descrita em [Contexto estendido](#extended-context) se aplica à configuração do modelo `opus` e não se estende a `opusplan`.

### Ajustar nível de esforço

[Níveis de esforço](https://platform.claude.com/docs/pt/build-with-claude/effort) controlam raciocínio adaptativo, que permite que o modelo decida se e quanto pensar em cada etapa com base na complexidade da tarefa. Esforço menor é mais rápido e mais barato para tarefas diretas, enquanto esforço maior fornece raciocínio mais profundo para problemas complexos.

O esforço é suportado em Opus 4.7, Opus 4.6 e Sonnet 4.6. Os níveis disponíveis dependem do modelo:

| Modelo                | Níveis                                  |
| :-------------------- | :-------------------------------------- |
| Opus 4.7              | `low`, `medium`, `high`, `xhigh`, `max` |
| Opus 4.6 e Sonnet 4.6 | `low`, `medium`, `high`, `max`          |

Se você definir um nível que o modelo ativo não suporta, Claude Code volta para o nível mais alto suportado no ou abaixo do que você definiu. Por exemplo, `xhigh` é executado como `high` em Opus 4.6.

A partir da v2.1.117, o esforço padrão é `xhigh` em Opus 4.7 e `high` em Opus 4.6 e Sonnet 4.6.

Quando você executa Opus 4.7 pela primeira vez, Claude Code aplica `xhigh` mesmo que você tenha definido anteriormente um nível de esforço diferente para Opus 4.6 ou Sonnet 4.6. Execute `/effort` novamente para escolher um nível diferente após alternar.

`low`, `medium`, `high` e `xhigh` persistem entre sessões. `max` fornece o raciocínio mais profundo sem restrição no gasto de tokens e se aplica apenas à sessão atual, exceto quando definido através da variável de ambiente `CLAUDE_CODE_EFFORT_LEVEL`.

#### Escolher um nível de esforço

Cada nível negocia gasto de tokens contra capacidade. O padrão é adequado para a maioria das tarefas de codificação; ajuste quando você quiser um equilíbrio diferente.

| Nível    | Quando usá-lo                                                                                                                                           |
| :------- | :------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `low`    | Reserve para tarefas curtas, delimitadas, sensíveis à latência que não são sensíveis à inteligência                                                     |
| `medium` | Reduz o uso de tokens para trabalho sensível a custos que pode fazer concessões em inteligência                                                         |
| `high`   | Equilibra o uso de tokens e inteligência. Use como mínimo para trabalho sensível à inteligência, ou para reduzir o gasto de tokens em relação a `xhigh` |
| `xhigh`  | Melhores resultados para a maioria das tarefas de codificação e agentes. Padrão recomendado em Opus 4.7                                                 |
| `max`    | Pode melhorar o desempenho em tarefas exigentes, mas pode mostrar retornos decrescentes e é propenso a pensar demais. Teste antes de adotar amplamente  |

A escala de esforço é calibrada por modelo, portanto o mesmo nome de nível não representa o mesmo valor subjacente entre modelos.

#### Usar ultrathink para raciocínio profundo único

Inclua `ultrathink` em qualquer lugar em seu prompt para solicitar raciocínio mais profundo nessa volta sem alterar sua configuração de esforço de sessão. Claude Code reconhece a palavra-chave e adiciona uma instrução no contexto. O nível de esforço enviado para a API permanece inalterado. Outras frases como "think", "think hard" e "think more" são passadas como texto de prompt ordinário e não são reconhecidas como palavras-chave.

#### Definir o nível de esforço

Você pode alterar o esforço através de qualquer um dos seguintes:

* **`/effort`**: execute `/effort` sem argumentos para abrir um controle deslizante interativo, `/effort` seguido por um nome de nível para defini-lo diretamente, ou `/effort auto` para redefinir para o padrão do modelo
* **Em `/model`**: use as teclas de seta esquerda/direita para ajustar o controle deslizante de esforço ao selecionar um modelo
* **Sinalizador `--effort`**: passe um nome de nível para defini-lo para uma única sessão ao iniciar Claude Code
* **Variável de ambiente**: defina `CLAUDE_CODE_EFFORT_LEVEL` para um nome de nível ou `auto`
* **Configurações**: defina `effortLevel` em seu arquivo de configurações
* **Frontmatter de skill e subagent**: defina `effort` em um arquivo markdown de [skill](/pt/skills#frontmatter-reference) ou [subagent](/pt/sub-agents#supported-frontmatter-fields) para substituir o nível de esforço quando esse skill ou subagent é executado

A variável de ambiente tem precedência sobre todos os outros métodos, depois seu nível configurado, depois o padrão do modelo. O esforço de frontmatter se aplica quando esse skill ou subagent está ativo, substituindo o nível de sessão, mas não a variável de ambiente.

O controle deslizante de esforço aparece em `/model` quando um modelo suportado é selecionado. O nível de esforço atual também é exibido ao lado do logo e spinner, por exemplo "with low effort", para que você possa confirmar qual configuração está ativa sem abrir `/model`.

#### Raciocínio adaptativo e orçamentos de pensamento fixos

O raciocínio adaptativo torna o pensamento opcional em cada etapa, portanto Claude pode responder mais rápido a prompts rotineiros e reservar pensamento mais profundo para etapas que se beneficiam dele. Se você quiser que Claude pense mais ou menos frequentemente do que o nível atual produz, você pode dizer isso diretamente em seu prompt ou em `CLAUDE.md`; o modelo responde a essa orientação dentro de sua configuração de esforço.

Opus 4.7 sempre usa raciocínio adaptativo. O modo de orçamento de pensamento fixo e `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING` não se aplicam a ele.

Em Opus 4.6 e Sonnet 4.6, você pode definir `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING=1` para reverter para o orçamento de pensamento fixo anterior controlado por `MAX_THINKING_TOKENS`. Veja [variáveis de ambiente](/pt/env-vars).

### Pensamento estendido

Pensamento estendido é o raciocínio que Claude emite antes de responder. Em modelos que suportam [raciocínio adaptativo](#adjust-effort-level), o nível de esforço é o controle principal para quanto pensamento acontece; as configurações abaixo ativam ou desativam o pensamento e controlam como ele é exibido.

| Controle                                 | Como defini-lo                                                                                                                                                         |
| :--------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Alternar para a sessão atual             | Pressione `Option+T` no macOS ou `Alt+T` no Windows e Linux                                                                                                            |
| Definir o padrão global                  | Execute `/config` e alterne o modo de pensamento. Salvo como `alwaysThinkingEnabled` em `~/.claude/settings.json`                                                      |
| Desabilitar independentemente do esforço | Defina [`MAX_THINKING_TOKENS=0`](/pt/env-vars). Outros valores se aplicam apenas com um [orçamento de pensamento fixo](#adaptive-reasoning-and-fixed-thinking-budgets) |

A saída de pensamento é recolhida por padrão. Pressione `Ctrl+O` para alternar o modo verboso e ver o raciocínio como texto em itálico cinzento. Sessões interativas na API Anthropic recebem blocos de pensamento redigidos por padrão, portanto defina `showThinkingSummaries: true` em [configurações](/pt/settings) se você quiser os resumos completos disponíveis quando expandir. Você é cobrado por todos os tokens de pensamento gerados, mesmo quando recolhidos ou redigidos.

### Contexto estendido

Opus 4.7, Opus 4.6 e Sonnet 4.6 suportam uma [janela de contexto de 1 milhão de tokens](https://platform.claude.com/docs/pt/build-with-claude/context-windows#1m-token-context-window) para sessões longas com grandes bases de código.

A disponibilidade varia por modelo e plano. Nos planos Max, Team e Enterprise, Opus é automaticamente atualizado para contexto 1M sem configuração adicional. Isso se aplica aos assentos Team Standard e Team Premium.

| Plano                          | Opus com contexto 1M                                                                                  | Sonnet com contexto 1M                                                                                |
| ------------------------------ | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| Max, Team e Enterprise         | Incluído na assinatura                                                                                | Requer [uso extra](https://support.claude.com/pt/articles/12429409-extra-usage-for-paid-claude-plans) |
| Pro                            | Requer [uso extra](https://support.claude.com/pt/articles/12429409-extra-usage-for-paid-claude-plans) | Requer [uso extra](https://support.claude.com/pt/articles/12429409-extra-usage-for-paid-claude-plans) |
| API e pagamento conforme o uso | Acesso completo                                                                                       | Acesso completo                                                                                       |

Para desabilitar completamente o contexto 1M, defina `CLAUDE_CODE_DISABLE_1M_CONTEXT=1`. Isso remove variantes de modelo 1M do seletor de modelo. Veja [variáveis de ambiente](/pt/env-vars).

A janela de contexto 1M usa preços de modelo padrão sem prêmio para tokens além de 200K. Para planos onde o contexto estendido está incluído em sua assinatura, o uso permanece coberto por sua assinatura. Para planos que acessam contexto estendido através de uso extra, os tokens são cobrados para uso extra.

Se sua conta suporta contexto 1M, a opção aparece no seletor de modelo (`/model`) nas versões mais recentes do Claude Code. Se você não a vir, tente reiniciar sua sessão.

Você também pode usar o sufixo `[1m]` com aliases de modelo ou nomes de modelo completos:

```bash theme={null}
# Use o alias opus[1m] ou sonnet[1m]
/model opus[1m]
/model sonnet[1m]

# Ou anexe [1m] a um nome de modelo completo
/model claude-opus-4-7[1m]
```

## Verificando seu modelo atual

Você pode ver qual modelo está usando atualmente de várias maneiras:

1. Na [linha de status](/pt/statusline) (se configurada)
2. Em `/status`, que também exibe as informações de sua conta.

## Adicionar uma opção de modelo personalizado

Use `ANTHROPIC_CUSTOM_MODEL_OPTION` para adicionar uma única entrada personalizada ao seletor `/model` sem substituir os aliases integrados. Isso é útil para testar IDs de modelo que Claude Code não lista por padrão. Para implantações de gateway LLM, Claude Code pode preencher o seletor a partir do endpoint `/v1/models` do gateway quando `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` está definido, portanto essa variável é necessária apenas quando a descoberta está desabilitada ou não retorna o modelo que você deseja. Consulte [Seleção de modelo de gateway LLM](/pt/llm-gateway#model-selection).

Este exemplo define todas as três variáveis para tornar uma implantação Opus roteada por gateway selecionável:

```bash theme={null}
export ANTHROPIC_CUSTOM_MODEL_OPTION="my-gateway/claude-opus-4-7"
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

Sem fixação, Claude Code usa aliases de modelo (`sonnet`, `opus`, `haiku`) que resolvem para a versão mais recente. Quando Anthropic lança um novo modelo que ainda não está habilitado na conta de um usuário, os usuários de Bedrock e Vertex AI veem um aviso e voltam para a versão anterior para essa sessão, enquanto os usuários de Foundry veem erros porque Foundry não tem verificação de inicialização equivalente.

<Warning>
  Defina todas as três variáveis de ambiente de modelo para IDs de versão específicos como parte de sua configuração inicial. Fixar permite que você controle quando seus usuários se movem para um novo modelo.
</Warning>

Use as seguintes variáveis de ambiente com IDs de modelo específicos de versão para seu provedor:

| Provedor  | Exemplo                                                              |
| :-------- | :------------------------------------------------------------------- |
| Bedrock   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='us.anthropic.claude-opus-4-7'` |
| Vertex AI | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'`              |
| Foundry   | `export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7'`              |

Aplique o mesmo padrão para `ANTHROPIC_DEFAULT_SONNET_MODEL` e `ANTHROPIC_DEFAULT_HAIKU_MODEL`. Para IDs de modelo atuais e legados em todos os provedores, veja [Visão geral de modelos](https://platform.claude.com/docs/pt/about-claude/models/overview). Para atualizar usuários para uma nova versão de modelo, atualize essas variáveis de ambiente e reimplante.

Para habilitar [contexto estendido](#extended-context) para um modelo fixado, anexe `[1m]` ao ID do modelo em `ANTHROPIC_DEFAULT_OPUS_MODEL` ou `ANTHROPIC_DEFAULT_SONNET_MODEL`:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='claude-opus-4-7[1m]'
```

O sufixo `[1m]` aplica a janela de contexto 1M a todo o uso desse alias, incluindo `opusplan`. Claude Code remove o sufixo antes de enviar o ID do modelo para seu provedor. Apenas anexe `[1m]` quando o modelo subjacente suportar contexto 1M, como Opus 4.7 ou Sonnet 4.6.

<Note>
  A lista de permissões `settings.availableModels` ainda se aplica ao usar provedores de terceiros. A filtragem corresponde ao alias de modelo (`opus`, `sonnet`, `haiku`), não ao ID de modelo específico do provedor.
</Note>

### Personalizar exibição e capacidades do modelo fixado

Quando você fixa um modelo em um provedor de terceiros, o ID específico do provedor aparece como está no seletor `/model` e Claude Code pode não reconhecer quais recursos o modelo suporta. Você pode substituir o nome de exibição e declarar capacidades com variáveis de ambiente complementares para cada modelo fixado.

Essas variáveis têm efeito em provedores de terceiros, como Bedrock, Vertex AI e Foundry. As variáveis `_NAME` e `_DESCRIPTION` também têm efeito quando `ANTHROPIC_BASE_URL` aponta para um [gateway LLM](/pt/llm-gateway). Elas não têm efeito ao conectar diretamente a `api.anthropic.com`.

| Variável de ambiente                                  | Descrição                                                                                                                |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_NAME`                   | Nome de exibição para o modelo Opus fixado no seletor `/model`. Padrão para o ID do modelo quando não definido           |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION`            | Descrição de exibição para o modelo Opus fixado no seletor `/model`. Padrão para `Custom Opus model` quando não definido |
| `ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES` | Lista separada por vírgulas de capacidades que o modelo Opus fixado suporta                                              |

Os mesmos sufixos `_NAME`, `_DESCRIPTION` e `_SUPPORTED_CAPABILITIES` estão disponíveis para `ANTHROPIC_DEFAULT_SONNET_MODEL`, `ANTHROPIC_DEFAULT_HAIKU_MODEL` e `ANTHROPIC_CUSTOM_MODEL_OPTION`.

Claude Code habilita recursos como [níveis de esforço](#adjust-effort-level) e [pensamento estendido](#extended-thinking) correspondendo o ID do modelo contra padrões conhecidos. IDs específicos do provedor, como ARNs Bedrock ou nomes de implantação personalizados, geralmente não correspondem a esses padrões, deixando recursos suportados desabilitados. Defina `_SUPPORTED_CAPABILITIES` para informar ao Claude Code quais recursos o modelo realmente suporta:

| Valor de capacidade    | Habilita                                                                                      |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| `effort`               | [Níveis de esforço](#adjust-effort-level) e o comando `/effort`                               |
| `xhigh_effort`         | {/* min-version: 2.1.111 */}O nível de esforço `xhigh`                                        |
| `max_effort`           | O nível de esforço `max`                                                                      |
| `thinking`             | [Pensamento estendido](#extended-thinking)                                                    |
| `adaptive_thinking`    | Raciocínio adaptativo que aloca dinamicamente o pensamento com base na complexidade da tarefa |
| `interleaved_thinking` | Pensamento entre chamadas de ferramenta                                                       |

Quando `_SUPPORTED_CAPABILITIES` é definido, as capacidades listadas são habilitadas e as capacidades não listadas são desabilitadas para o modelo fixado correspondente. Quando a variável não está definida, Claude Code volta para detecção integrada baseada no ID do modelo.

Este exemplo fixa Opus para um ARN de modelo personalizado Bedrock, define um nome amigável e declara suas capacidades:

```bash theme={null}
export ANTHROPIC_DEFAULT_OPUS_MODEL='arn:aws:bedrock:us-east-1:123456789012:custom-model/abc'
export ANTHROPIC_DEFAULT_OPUS_MODEL_NAME='Opus via Bedrock'
export ANTHROPIC_DEFAULT_OPUS_MODEL_DESCRIPTION='Opus 4.7 routed through a Bedrock custom endpoint'
export ANTHROPIC_DEFAULT_OPUS_MODEL_SUPPORTED_CAPABILITIES='effort,xhigh_effort,max_effort,thinking,adaptive_thinking,interleaved_thinking'
```

### Substituir IDs de modelo por versão

As variáveis de ambiente no nível de família acima configuram um ID de modelo por alias de família. Se você precisar mapear várias versões dentro da mesma família para IDs de provedor distintos, use a configuração `modelOverrides` em vez disso.

`modelOverrides` mapeia IDs de modelo Anthropic individuais para as strings específicas do provedor que Claude Code envia para a API do seu provedor. Quando um usuário seleciona um modelo mapeado no seletor `/model`, Claude Code usa seu valor configurado em vez do padrão integrado.

Isso permite que administradores corporativos roteiem cada versão de modelo para um ARN de perfil de inferência Bedrock específico, nome de versão Vertex AI ou nome de implantação Foundry para governança, alocação de custos ou roteamento regional.

Defina `modelOverrides` em seu [arquivo de configurações](/pt/settings#settings-files):

```json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-7": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-prod",
    "claude-opus-4-6": "arn:aws:bedrock:us-east-2:123456789012:application-inference-profile/opus-46-prod",
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
