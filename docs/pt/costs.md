> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Gerencie custos de forma eficaz

> Rastreie o uso de tokens, defina limites de gastos da equipe e reduza os custos do Claude Code com gerenciamento de contexto, seleção de modelo, configurações de pensamento estendido e hooks de pré-processamento.

Claude Code consome tokens para cada interação. Os custos variam com base no tamanho da base de código, complexidade da consulta e comprimento da conversa. O custo médio é de \$6 por desenvolvedor por dia, com custos diários permanecendo abaixo de \$12 para 90% dos usuários.

Para uso em equipe, Claude Code cobra pelo consumo de tokens da API. Em média, Claude Code custa \~\$100-200/desenvolvedor por mês com Sonnet 4.6, embora haja grande variação dependendo de quantas instâncias os usuários estão executando e se estão usando em automação.

Esta página aborda como [rastrear seus custos](#track-your-costs), [gerenciar custos para equipes](#managing-costs-for-teams) e [reduzir o uso de tokens](#reduce-token-usage).

## Rastreie seus custos

### Usando o comando `/cost`

<Note>
  O comando `/cost` mostra o uso de tokens da API e é destinado a usuários de API. Assinantes do Claude Max e Pro têm uso incluído em sua assinatura, portanto, dados de `/cost` não são relevantes para fins de faturamento. Os assinantes podem usar `/stats` para visualizar padrões de uso.
</Note>

O comando `/cost` fornece estatísticas detalhadas de uso de tokens para sua sessão atual:

```text  theme={null}
Total cost:            $0.55
Total duration (API):  6m 19.7s
Total duration (wall): 6h 33m 10.2s
Total code changes:    0 lines added, 0 lines removed
```

## Gerenciando custos para equipes

Ao usar a API Claude, você pode [definir limites de gastos do workspace](https://platform.claude.com/docs/pt/build-with-claude/workspaces#workspace-limits) no gasto total do workspace do Claude Code. Administradores podem [visualizar relatórios de custo e uso](https://platform.claude.com/docs/pt/build-with-claude/workspaces#usage-and-cost-tracking) no Console.

<Note>
  Quando você autentica pela primeira vez o Claude Code com sua conta do Claude Console, um workspace chamado "Claude Code" é criado automaticamente para você. Este workspace fornece rastreamento e gerenciamento centralizado de custos para todo o uso do Claude Code em sua organização. Você não pode criar chaves de API para este workspace; é exclusivamente para autenticação e uso do Claude Code.
</Note>

No Bedrock, Vertex e Foundry, Claude Code não envia métricas da sua nuvem. Para obter métricas de custo, várias grandes empresas relataram usar [LiteLLM](/pt/llm-gateway#litellm-configuration), que é uma ferramenta de código aberto que ajuda empresas a [rastrear gastos por chave](https://docs.litellm.ai/docs/proxy/virtual_keys#tracking-spend). Este projeto não é afiliado à Anthropic e não foi auditado quanto à segurança.

### Recomendações de limite de taxa

Ao configurar Claude Code para equipes, considere estas recomendações de Token Por Minuto (TPM) e Requisição Por Minuto (RPM) por usuário com base no tamanho da sua organização:

| Tamanho da equipe | TPM por usuário | RPM por usuário |
| ----------------- | --------------- | --------------- |
| 1-5 usuários      | 200k-300k       | 5-7             |
| 5-20 usuários     | 100k-150k       | 2.5-3.5         |
| 20-50 usuários    | 50k-75k         | 1.25-1.75       |
| 50-100 usuários   | 25k-35k         | 0.62-0.87       |
| 100-500 usuários  | 15k-20k         | 0.37-0.47       |
| 500+ usuários     | 10k-15k         | 0.25-0.35       |

Por exemplo, se você tiver 200 usuários, você pode solicitar 20k TPM para cada usuário, ou 4 milhões de TPM total (200\*20.000 = 4 milhões).

O TPM por usuário diminui conforme o tamanho da equipe cresce porque menos usuários tendem a usar Claude Code simultaneamente em organizações maiores. Esses limites de taxa se aplicam no nível da organização, não por usuário individual, o que significa que usuários individuais podem consumir temporariamente mais do que sua cota calculada quando outros não estão usando ativamente o serviço.

<Note>
  Se você antecipar cenários com uso concorrente incomumente alto (como sessões de treinamento ao vivo com grandes grupos), você pode precisar de alocações de TPM mais altas por usuário.
</Note>

### Custos de tokens de equipes de agentes

[Equipes de agentes](/pt/agent-teams) geram múltiplas instâncias do Claude Code, cada uma com sua própria janela de contexto. O uso de tokens escala com o número de colegas de equipe ativos e quanto tempo cada um executa.

Para manter os custos das equipes de agentes gerenciáveis:

* Use Sonnet para colegas de equipe. Ele equilibra capacidade e custo para tarefas de coordenação.
* Mantenha equipes pequenas. Cada colega de equipe executa sua própria janela de contexto, portanto, o uso de tokens é aproximadamente proporcional ao tamanho da equipe.
* Mantenha prompts de geração focados. Colegas de equipe carregam CLAUDE.md, servidores MCP e skills automaticamente, mas tudo no prompt de geração adiciona ao seu contexto desde o início.
* Limpe equipes quando o trabalho estiver concluído. Colegas de equipe ativos continuam consumindo tokens mesmo se ociosos.
* Equipes de agentes são desabilitadas por padrão. Defina `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` em seu [settings.json](/pt/settings) ou ambiente para habilitá-las. Veja [habilitar equipes de agentes](/pt/agent-teams#enable-agent-teams).

## Reduza o uso de tokens

Os custos de tokens escalam com o tamanho do contexto: quanto mais contexto Claude processa, mais tokens você usa. Claude Code otimiza automaticamente os custos através do prompt caching (que reduz custos para conteúdo repetido como prompts do sistema) e auto-compaction (que resume o histórico de conversa ao se aproximar dos limites de contexto).

As seguintes estratégias ajudam você a manter o contexto pequeno e reduzir custos por mensagem.

### Gerencie o contexto proativamente

Use `/cost` para verificar seu uso atual de tokens, ou [configure sua linha de status](/pt/statusline#context-window-usage) para exibi-la continuamente.

* **Limpe entre tarefas**: Use `/clear` para começar do zero ao mudar para trabalho não relacionado. Contexto obsoleto desperdiça tokens em cada mensagem subsequente. Use `/rename` antes de limpar para que você possa encontrar facilmente a sessão depois, então `/resume` para retornar a ela.
* **Adicione instruções de compactação personalizadas**: `/compact Focus on code samples and API usage` diz a Claude o que preservar durante a sumarização.

Você também pode personalizar o comportamento de compactação em seu CLAUDE.md:

```markdown  theme={null}
# Compact instructions

When you are using compact, please focus on test output and code changes
```

### Escolha o modelo certo

Sonnet lida bem com a maioria das tarefas de codificação e custa menos que Opus. Reserve Opus para decisões arquitetônicas complexas ou raciocínio em múltiplas etapas. Use `/model` para alternar modelos no meio da sessão, ou defina um padrão em `/config`. Para tarefas simples de subagente, especifique `model: haiku` em sua [configuração de subagente](/pt/sub-agents#choose-a-model).

### Reduza a sobrecarga do servidor MCP

Cada servidor MCP adiciona definições de ferramentas ao seu contexto, mesmo quando ocioso. Execute `/context` para ver o que está consumindo espaço.

* **Prefira ferramentas CLI quando disponíveis**: Ferramentas como `gh`, `aws`, `gcloud` e `sentry-cli` são mais eficientes em contexto do que servidores MCP porque não adicionam definições de ferramentas persistentes. Claude pode executar comandos CLI diretamente sem a sobrecarga.
* **Desabilite servidores não utilizados**: Execute `/mcp` para ver servidores configurados e desabilite qualquer um que você não esteja usando ativamente.
* **A busca de ferramentas é automática**: Quando as descrições de ferramentas MCP excedem 10% de sua janela de contexto, Claude Code automaticamente as adia e carrega ferramentas sob demanda via [busca de ferramentas](/pt/mcp#scale-with-mcp-tool-search). Como ferramentas adiadas apenas entram no contexto quando realmente usadas, um limite mais baixo significa menos definições de ferramentas ociosas consumindo espaço. Defina um limite mais baixo com `ENABLE_TOOL_SEARCH=auto:<N>` (por exemplo, `auto:5` dispara quando ferramentas excedem 5% de sua janela de contexto).

### Instale plugins de inteligência de código para linguagens tipadas

[Plugins de inteligência de código](/pt/discover-plugins#code-intelligence) dão a Claude navegação de símbolo precisa em vez de busca baseada em texto, reduzindo leituras de arquivo desnecessárias ao explorar código desconhecido. Uma única chamada "ir para definição" substitui o que poderia ser um grep seguido de leitura de múltiplos arquivos candidatos. Servidores de linguagem instalados também relatam erros de tipo automaticamente após edições, portanto Claude detecta erros sem executar um compilador.

### Descarregue o processamento para hooks e skills

[Hooks](/pt/hooks) personalizados podem pré-processar dados antes de Claude vê-los. Em vez de Claude ler um arquivo de log de 10.000 linhas para encontrar erros, um hook pode fazer grep para `ERROR` e retornar apenas linhas correspondentes, reduzindo contexto de dezenas de milhares de tokens para centenas.

Uma [skill](/pt/skills) pode dar a Claude conhecimento de domínio para que não tenha que explorar. Por exemplo, uma skill "codebase-overview" poderia descrever a arquitetura do seu projeto, diretórios-chave e convenções de nomenclatura. Quando Claude invoca a skill, obtém este contexto imediatamente em vez de gastar tokens lendo múltiplos arquivos para entender a estrutura.

Por exemplo, este hook PreToolUse filtra a saída de teste para mostrar apenas falhas:

<Tabs>
  <Tab title="settings.json">
    Adicione isto ao seu [settings.json](/pt/settings#settings-files) para executar o hook antes de cada comando Bash:

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "~/.claude/hooks/filter-test-output.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="filter-test-output.sh">
    O hook chama este script, que verifica se o comando é um executor de teste e o modifica para mostrar apenas falhas:

    ```bash  theme={null}
    #!/bin/bash
    input=$(cat)
    cmd=$(echo "$input" | jq -r '.tool_input.command')

    # If running tests, filter to show only failures
    if [[ "$cmd" =~ ^(npm test|pytest|go test) ]]; then
      filtered_cmd="$cmd 2>&1 | grep -A 5 -E '(FAIL|ERROR|error:)' | head -100"
      echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PreToolUse\",\"permissionDecision\":\"allow\",\"updatedInput\":{\"command\":\"$filtered_cmd\"}}}"
    else
      echo "{}"
    fi
    ```
  </Tab>
</Tabs>

### Mova instruções de CLAUDE.md para skills

Seu arquivo [CLAUDE.md](/pt/memory) é carregado no contexto no início da sessão. Se contiver instruções detalhadas para fluxos de trabalho específicos (como revisões de PR ou migrações de banco de dados), esses tokens estão presentes mesmo quando você está fazendo trabalho não relacionado. [Skills](/pt/skills) carregam sob demanda apenas quando invocadas, portanto mover instruções especializadas para skills mantém seu contexto base menor. Procure manter CLAUDE.md com menos de \~500 linhas incluindo apenas essenciais.

### Ajuste o pensamento estendido

O pensamento estendido é habilitado por padrão com um orçamento de 31.999 tokens porque melhora significativamente o desempenho em tarefas complexas de planejamento e raciocínio. No entanto, tokens de pensamento são faturados como tokens de saída, portanto para tarefas mais simples onde raciocínio profundo não é necessário, você pode reduzir custos baixando o [nível de esforço](/pt/model-config#adjust-effort-level) em `/model` para Opus 4.6, desabilitando pensamento em `/config`, ou baixando o orçamento (por exemplo, `MAX_THINKING_TOKENS=8000`).

### Delegue operações verbosas para subagentes

Executar testes, buscar documentação ou processar arquivos de log pode consumir contexto significativo. Delegue estes para [subagentes](/pt/sub-agents#isolate-high-volume-operations) para que a saída verbosa permaneça no contexto do subagente enquanto apenas um resumo retorna à sua conversa principal.

### Gerencie custos de equipes de agentes

Equipes de agentes usam aproximadamente 7x mais tokens do que sessões padrão quando colegas de equipe executam em modo de plano, porque cada colega de equipe mantém sua própria janela de contexto e executa como uma instância Claude separada. Mantenha tarefas de equipe pequenas e auto-contidas para limitar o uso de tokens por colega de equipe. Veja [equipes de agentes](/pt/agent-teams) para detalhes.

### Escreva prompts específicos

Solicitações vagas como "melhorar esta base de código" disparam varredura ampla. Solicitações específicas como "adicionar validação de entrada à função de login em auth.ts" deixam Claude trabalhar eficientemente com leituras de arquivo mínimas.

### Trabalhe eficientemente em tarefas complexas

Para trabalho mais longo ou complexo, esses hábitos ajudam a evitar tokens desperdiçados por seguir o caminho errado:

* **Use modo de plano para tarefas complexas**: Pressione Shift+Tab para entrar em [modo de plano](/pt/common-workflows#use-plan-mode-for-safe-code-analysis) antes da implementação. Claude explora a base de código e propõe uma abordagem para sua aprovação, prevenindo retrabalho caro quando a direção inicial está errada.
* **Corrija o curso cedo**: Se Claude começar a seguir a direção errada, pressione Escape para parar imediatamente. Use `/rewind` ou toque duplo em Escape para restaurar conversa e código para um checkpoint anterior.
* **Dê alvos de verificação**: Inclua casos de teste, cole capturas de tela ou defina saída esperada em seu prompt. Quando Claude pode verificar seu próprio trabalho, detecta problemas antes de você precisar solicitar correções.
* **Teste incrementalmente**: Escreva um arquivo, teste-o, depois continue. Isto detecta problemas cedo quando são baratos de corrigir.

## Uso de tokens em segundo plano

Claude Code usa tokens para algumas funcionalidades em segundo plano mesmo quando ocioso:

* **Sumarização de conversa**: Trabalhos em segundo plano que resumem conversas anteriores para o recurso `claude --resume`
* **Processamento de comando**: Alguns comandos como `/cost` podem gerar solicitações para verificar status

Esses processos em segundo plano consomem uma pequena quantidade de tokens (tipicamente menos de \$0.04 por sessão) mesmo sem interação ativa.

## Entendendo mudanças no comportamento do Claude Code

Claude Code recebe regularmente atualizações que podem mudar como os recursos funcionam, incluindo relatório de custos. Execute `claude --version` para verificar sua versão atual. Para perguntas específicas de faturamento, entre em contato com o suporte da Anthropic através de sua [conta Console](https://platform.claude.com/login). Para implantações em equipe, comece com um pequeno grupo piloto para estabelecer padrões de uso antes de um lançamento mais amplo.
