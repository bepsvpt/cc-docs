> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Estenda Claude com skills

> Crie, gerencie e compartilhe skills para estender as capacidades do Claude no Claude Code. Inclui comandos personalizados e skills agrupadas.

Skills estendem o que Claude pode fazer. Crie um arquivo `SKILL.md` com instruções, e Claude o adiciona ao seu kit de ferramentas. Claude usa skills quando relevante, ou você pode invocar uma diretamente com `/skill-name`.

<Note>
  Para comandos integrados como `/help` e `/compact`, consulte a [referência de comandos integrados](/pt/commands).

  **Comandos personalizados foram mesclados em skills.** Um arquivo em `.claude/commands/deploy.md` e uma skill em `.claude/skills/deploy/SKILL.md` ambos criam `/deploy` e funcionam da mesma forma. Seus arquivos `.claude/commands/` existentes continuam funcionando. Skills adicionam recursos opcionais: um diretório para arquivos de suporte, frontmatter para [controlar se você ou Claude invoca eles](#control-who-invokes-a-skill), e a capacidade de Claude carregá-los automaticamente quando relevante.
</Note>

Skills do Claude Code seguem o padrão aberto [Agent Skills](https://agentskills.io), que funciona em múltiplas ferramentas de IA. Claude Code estende o padrão com recursos adicionais como [controle de invocação](#control-who-invokes-a-skill), [execução de subagent](#run-skills-in-a-subagent), e [injeção de contexto dinâmico](#inject-dynamic-context).

## Skills agrupadas

Skills agrupadas são fornecidas com Claude Code e estão disponíveis em cada sessão. Diferentemente dos [comandos integrados](/pt/commands), que executam lógica fixa diretamente, skills agrupadas são baseadas em prompt: elas dão ao Claude um manual detalhado e deixam que ele orquestre o trabalho usando suas ferramentas. Isso significa que skills agrupadas podem gerar agentes paralelos, ler arquivos e se adaptar ao seu codebase.

Você invoca skills agrupadas da mesma forma que qualquer outra skill: digite `/` seguido do nome da skill. Na tabela abaixo, `<arg>` indica um argumento obrigatório e `[arg]` indica um opcional.

| Skill                       | Propósito                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| :-------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/batch <instruction>`      | Orquestre mudanças em larga escala em um codebase em paralelo. Pesquisa o codebase, decompõe o trabalho em 5 a 30 unidades independentes e apresenta um plano. Uma vez aprovado, gera um agente de fundo por unidade em um [git worktree](/pt/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) isolado. Cada agente implementa sua unidade, executa testes e abre um pull request. Requer um repositório git. Exemplo: `/batch migrate src/ from Solid to React` |
| `/claude-api`               | Carregue material de referência da API Claude para a linguagem do seu projeto (Python, TypeScript, Java, Go, Ruby, C#, PHP, ou cURL) e referência do Agent SDK para Python e TypeScript. Cobre uso de ferramentas, streaming, batches, saídas estruturadas e armadilhas comuns. Também ativa automaticamente quando seu código importa `anthropic`, `@anthropic-ai/sdk`, ou `claude_agent_sdk`                                                                                         |
| `/debug [description]`      | Solucione problemas de sua sessão atual do Claude Code lendo o log de debug da sessão. Opcionalmente descreva o problema para focar a análise                                                                                                                                                                                                                                                                                                                                          |
| `/loop [interval] <prompt>` | Execute um prompt repetidamente em um intervalo enquanto a sessão permanece aberta. Útil para pesquisar uma implantação, cuidar de um PR, ou executar periodicamente outra skill. Exemplo: `/loop 5m check if the deploy finished`. Consulte [Executar prompts em um cronograma](/pt/scheduled-tasks)                                                                                                                                                                                  |
| `/simplify [focus]`         | Revise seus arquivos recentemente alterados para reutilização de código, qualidade e problemas de eficiência, depois corrija-os. Gera três agentes de revisão em paralelo, agrega suas descobertas e aplica correções. Passe texto para focar em preocupações específicas: `/simplify focus on memory efficiency`                                                                                                                                                                      |

## Começando

### Crie sua primeira skill

Este exemplo cria uma skill que ensina Claude a explicar código usando diagramas visuais e analogias. Como usa frontmatter padrão, Claude pode carregá-la automaticamente quando você pergunta como algo funciona, ou você pode invocá-la diretamente com `/explain-code`.

<Steps>
  <Step title="Crie o diretório da skill">
    Crie um diretório para a skill em sua pasta de skills pessoais. Skills pessoais estão disponíveis em todos os seus projetos.

    ```bash  theme={null}
    mkdir -p ~/.claude/skills/explain-code
    ```
  </Step>

  <Step title="Escreva SKILL.md">
    Cada skill precisa de um arquivo `SKILL.md` com duas partes: frontmatter YAML (entre marcadores `---`) que diz ao Claude quando usar a skill, e conteúdo markdown com instruções que Claude segue quando a skill é invocada. O campo `name` se torna o `/slash-command`, e a `description` ajuda Claude a decidir quando carregá-la automaticamente.

    Crie `~/.claude/skills/explain-code/SKILL.md`:

    ```yaml  theme={null}
    ---
    name: explain-code
    description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
    ---

    When explaining code, always include:

    1. **Start with an analogy**: Compare the code to something from everyday life
    2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
    3. **Walk through the code**: Explain step-by-step what happens
    4. **Highlight a gotcha**: What's a common mistake or misconception?

    Keep explanations conversational. For complex concepts, use multiple analogies.
    ```
  </Step>

  <Step title="Teste a skill">
    Você pode testá-la de duas formas:

    **Deixe Claude invocá-la automaticamente** perguntando algo que corresponda à descrição:

    ```text  theme={null}
    How does this code work?
    ```

    **Ou invoque-a diretamente** com o nome da skill:

    ```text  theme={null}
    /explain-code src/auth/login.ts
    ```

    De qualquer forma, Claude deve incluir uma analogia e diagrama ASCII em sua explicação.
  </Step>
</Steps>

### Onde as skills vivem

Onde você armazena uma skill determina quem pode usá-la:

| Localização | Caminho                                                           | Aplica-se a                          |
| :---------- | :---------------------------------------------------------------- | :----------------------------------- |
| Enterprise  | Consulte [configurações gerenciadas](/pt/settings#settings-files) | Todos os usuários em sua organização |
| Pessoal     | `~/.claude/skills/<skill-name>/SKILL.md`                          | Todos os seus projetos               |
| Projeto     | `.claude/skills/<skill-name>/SKILL.md`                            | Apenas este projeto                  |
| Plugin      | `<plugin>/skills/<skill-name>/SKILL.md`                           | Onde o plugin está habilitado        |

Quando skills compartilham o mesmo nome em diferentes níveis, localizações de maior prioridade vencem: enterprise > pessoal > projeto. Skills de plugin usam um namespace `plugin-name:skill-name`, então não podem conflitar com outros níveis. Se você tem arquivos em `.claude/commands/`, eles funcionam da mesma forma, mas se uma skill e um comando compartilham o mesmo nome, a skill tem precedência.

#### Descoberta automática de diretórios aninhados

Quando você trabalha com arquivos em subdiretórios, Claude Code descobre automaticamente skills de diretórios `.claude/skills/` aninhados. Por exemplo, se você está editando um arquivo em `packages/frontend/`, Claude Code também procura por skills em `packages/frontend/.claude/skills/`. Isso suporta configurações de monorepo onde pacotes têm suas próprias skills.

Cada skill é um diretório com `SKILL.md` como ponto de entrada:

```text  theme={null}
my-skill/
├── SKILL.md           # Instruções principais (obrigatório)
├── template.md        # Template para Claude preencher
├── examples/
│   └── sample.md      # Exemplo de saída mostrando formato esperado
└── scripts/
    └── validate.sh    # Script que Claude pode executar
```

O `SKILL.md` contém as instruções principais e é obrigatório. Outros arquivos são opcionais e permitem que você construa skills mais poderosas: templates para Claude preencher, exemplos de saída mostrando o formato esperado, scripts que Claude pode executar, ou documentação de referência detalhada. Referencie esses arquivos de seu `SKILL.md` para que Claude saiba o que cada arquivo contém e quando carregá-lo. Consulte [Adicione arquivos de suporte](#add-supporting-files) para mais detalhes.

<Note>
  Arquivos em `.claude/commands/` ainda funcionam e suportam o mesmo [frontmatter](#frontmatter-reference). Skills são recomendadas já que suportam recursos adicionais como arquivos de suporte.
</Note>

#### Skills de diretórios adicionais

Skills definidas em `.claude/skills/` dentro de diretórios adicionados via `--add-dir` são carregadas automaticamente e detectadas por detecção de mudança ao vivo, então você pode editá-las durante uma sessão sem reiniciar.

<Note>
  Arquivos CLAUDE.md de diretórios `--add-dir` não são carregados por padrão. Para carregá-los, defina `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`. Consulte [Carregar de diretórios adicionais](/pt/memory#load-from-additional-directories).
</Note>

## Configure skills

Skills são configuradas através de frontmatter YAML no topo de `SKILL.md` e o conteúdo markdown que segue.

### Tipos de conteúdo de skill

Arquivos de skill podem conter qualquer instrução, mas pensar em como você quer invocá-los ajuda a guiar o que incluir:

**Conteúdo de referência** adiciona conhecimento que Claude aplica ao seu trabalho atual. Convenções, padrões, guias de estilo, conhecimento de domínio. Este conteúdo é executado inline para que Claude possa usá-lo junto com seu contexto de conversa.

```yaml  theme={null}
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

**Conteúdo de tarefa** dá ao Claude instruções passo a passo para uma ação específica, como implantações, commits ou geração de código. Estas são frequentemente ações que você quer invocar diretamente com `/skill-name` em vez de deixar Claude decidir quando executá-las. Adicione `disable-model-invocation: true` para evitar que Claude a dispare automaticamente.

```yaml  theme={null}
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

Seu `SKILL.md` pode conter qualquer coisa, mas pensar em como você quer que a skill seja invocada (por você, por Claude, ou ambos) e onde você quer que seja executada (inline ou em um subagent) ajuda a guiar o que incluir. Para skills complexas, você também pode [adicionar arquivos de suporte](#add-supporting-files) para manter a skill principal focada.

### Referência de frontmatter

Além do conteúdo markdown, você pode configurar o comportamento da skill usando campos de frontmatter YAML entre marcadores `---` no topo de seu arquivo `SKILL.md`:

```yaml  theme={null}
---
name: my-skill
description: What this skill does
disable-model-invocation: true
allowed-tools: Read, Grep
---

Your skill instructions here...
```

Todos os campos são opcionais. Apenas `description` é recomendado para que Claude saiba quando usar a skill.

| Campo                      | Obrigatório | Descrição                                                                                                                                                                   |
| :------------------------- | :---------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                     | Não         | Nome de exibição para a skill. Se omitido, usa o nome do diretório. Apenas letras minúsculas, números e hífens (máximo 64 caracteres).                                      |
| `description`              | Recomendado | O que a skill faz e quando usá-la. Claude usa isso para decidir quando aplicar a skill. Se omitido, usa o primeiro parágrafo do conteúdo markdown.                          |
| `argument-hint`            | Não         | Dica mostrada durante autocomplete para indicar argumentos esperados. Exemplo: `[issue-number]` ou `[filename] [format]`.                                                   |
| `disable-model-invocation` | Não         | Defina como `true` para evitar que Claude carregue automaticamente esta skill. Use para fluxos de trabalho que você quer disparar manualmente com `/name`. Padrão: `false`. |
| `user-invocable`           | Não         | Defina como `false` para ocultar do menu `/`. Use para conhecimento de fundo que usuários não devem invocar diretamente. Padrão: `true`.                                    |
| `allowed-tools`            | Não         | Ferramentas que Claude pode usar sem pedir permissão quando esta skill está ativa.                                                                                          |
| `model`                    | Não         | Modelo a usar quando esta skill está ativa.                                                                                                                                 |
| `context`                  | Não         | Defina como `fork` para executar em um contexto de subagent bifurcado.                                                                                                      |
| `agent`                    | Não         | Qual tipo de subagent usar quando `context: fork` está definido.                                                                                                            |
| `hooks`                    | Não         | Hooks com escopo para o ciclo de vida desta skill. Consulte [Hooks em skills e agents](/pt/hooks#hooks-in-skills-and-agents) para formato de configuração.                  |

#### Substituições de string disponíveis

Skills suportam substituição de string para valores dinâmicos no conteúdo da skill:

| Variável               | Descrição                                                                                                                                                                                                                                                                                            |
| :--------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$ARGUMENTS`           | Todos os argumentos passados ao invocar a skill. Se `$ARGUMENTS` não estiver presente no conteúdo, argumentos são anexados como `ARGUMENTS: <value>`.                                                                                                                                                |
| `$ARGUMENTS[N]`        | Acesse um argumento específico por índice baseado em 0, como `$ARGUMENTS[0]` para o primeiro argumento.                                                                                                                                                                                              |
| `$N`                   | Abreviação para `$ARGUMENTS[N]`, como `$0` para o primeiro argumento ou `$1` para o segundo.                                                                                                                                                                                                         |
| `${CLAUDE_SESSION_ID}` | O ID da sessão atual. Útil para logging, criação de arquivos específicos da sessão, ou correlação de saída de skill com sessões.                                                                                                                                                                     |
| `${CLAUDE_SKILL_DIR}`  | O diretório contendo o arquivo `SKILL.md` da skill. Para skills de plugin, este é o subdiretório da skill dentro do plugin, não a raiz do plugin. Use isso em comandos de injeção bash para referenciar scripts ou arquivos agrupados com a skill, independentemente do diretório de trabalho atual. |

**Exemplo usando substituições:**

```yaml  theme={null}
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

### Adicione arquivos de suporte

Skills podem incluir múltiplos arquivos em seu diretório. Isso mantém `SKILL.md` focado no essencial enquanto deixa Claude acessar material de referência detalhado apenas quando necessário. Documentos de referência grandes, especificações de API, ou coleções de exemplos não precisam carregar em contexto toda vez que a skill é executada.

```text  theme={null}
my-skill/
├── SKILL.md (obrigatório - visão geral e navegação)
├── reference.md (documentação de API detalhada - carregada quando necessário)
├── examples.md (exemplos de uso - carregados quando necessário)
└── scripts/
    └── helper.py (script utilitário - executado, não carregado)
```

Referencie arquivos de suporte de `SKILL.md` para que Claude saiba o que cada arquivo contém e quando carregá-lo:

```markdown  theme={null}
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

<Tip>Mantenha `SKILL.md` com menos de 500 linhas. Mova material de referência detalhado para arquivos separados.</Tip>

### Controle quem invoca uma skill

Por padrão, tanto você quanto Claude podem invocar qualquer skill. Você pode digitar `/skill-name` para invocá-la diretamente, e Claude pode carregá-la automaticamente quando relevante para sua conversa. Dois campos de frontmatter permitem que você restrinja isso:

* **`disable-model-invocation: true`**: Apenas você pode invocar a skill. Use isso para fluxos de trabalho com efeitos colaterais ou que você quer controlar o tempo, como `/commit`, `/deploy`, ou `/send-slack-message`. Você não quer que Claude decida fazer deploy porque seu código parece pronto.

* **`user-invocable: false`**: Apenas Claude pode invocar a skill. Use isso para conhecimento de fundo que não é acionável como um comando. Uma skill `legacy-system-context` explica como um sistema antigo funciona. Claude deve saber disso quando relevante, mas `/legacy-system-context` não é uma ação significativa para usuários tomarem.

Este exemplo cria uma skill de deploy que apenas você pode disparar. O campo `disable-model-invocation: true` evita que Claude a execute automaticamente:

```yaml  theme={null}
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

Aqui está como os dois campos afetam invocação e carregamento de contexto:

| Frontmatter                      | Você pode invocar | Claude pode invocar | Quando carregado em contexto                                         |
| :------------------------------- | :---------------- | :------------------ | :------------------------------------------------------------------- |
| (padrão)                         | Sim               | Sim                 | Descrição sempre em contexto, skill completa carrega quando invocada |
| `disable-model-invocation: true` | Sim               | Não                 | Descrição não em contexto, skill completa carrega quando você invoca |
| `user-invocable: false`          | Não               | Sim                 | Descrição sempre em contexto, skill completa carrega quando invocada |

<Note>
  Em uma sessão regular, descrições de skills são carregadas em contexto para que Claude saiba o que está disponível, mas conteúdo completo de skill apenas carrega quando invocado. [Subagents com skills pré-carregadas](/pt/sub-agents#preload-skills-into-subagents) funcionam diferentemente: o conteúdo completo da skill é injetado na inicialização.
</Note>

### Restrinja acesso a ferramentas

Use o campo `allowed-tools` para limitar quais ferramentas Claude pode usar quando uma skill está ativa. Esta skill cria um modo somente leitura onde Claude pode explorar arquivos mas não modificá-los:

```yaml  theme={null}
---
name: safe-reader
description: Read files without making changes
allowed-tools: Read, Grep, Glob
---
```

### Passe argumentos para skills

Tanto você quanto Claude podem passar argumentos ao invocar uma skill. Argumentos estão disponíveis via placeholder `$ARGUMENTS`.

Esta skill corrige um problema do GitHub por número. O placeholder `$ARGUMENTS` é substituído por qualquer coisa que siga o nome da skill:

```yaml  theme={null}
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

Quando você executa `/fix-issue 123`, Claude recebe "Fix GitHub issue 123 following our coding standards..."

Se você invocar uma skill com argumentos mas a skill não incluir `$ARGUMENTS`, Claude Code anexa `ARGUMENTS: <your input>` ao final do conteúdo da skill para que Claude ainda veja o que você digitou.

Para acessar argumentos individuais por posição, use `$ARGUMENTS[N]` ou a forma mais curta `$N`:

```yaml  theme={null}
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $ARGUMENTS[0] component from $ARGUMENTS[1] to $ARGUMENTS[2].
Preserve all existing behavior and tests.
```

Executar `/migrate-component SearchBar React Vue` substitui `$ARGUMENTS[0]` com `SearchBar`, `$ARGUMENTS[1]` com `React`, e `$ARGUMENTS[2]` com `Vue`. A mesma skill usando a abreviação `$N`:

```yaml  theme={null}
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

## Padrões avançados

### Injete contexto dinâmico

A sintaxe `!`command\`\` executa comandos shell antes do conteúdo da skill ser enviado para Claude. A saída do comando substitui o placeholder, para que Claude receba dados reais, não o comando em si.

Esta skill resume um pull request buscando dados de PR ao vivo com o GitHub CLI. Os comandos `!`gh pr diff\`\` e outros são executados primeiro, e sua saída é inserida no prompt:

```yaml  theme={null}
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

Quando esta skill é executada:

1. Cada `!`command\`\` é executado imediatamente (antes de Claude ver qualquer coisa)
2. A saída substitui o placeholder no conteúdo da skill
3. Claude recebe o prompt totalmente renderizado com dados reais de PR

Isto é pré-processamento, não algo que Claude executa. Claude apenas vê o resultado final.

<Tip>
  Para habilitar [pensamento estendido](/pt/common-workflows#use-extended-thinking-thinking-mode) em uma skill, inclua a palavra "ultrathink" em qualquer lugar no conteúdo de sua skill.
</Tip>

### Execute skills em um subagent

Adicione `context: fork` ao seu frontmatter quando você quer que uma skill seja executada em isolamento. O conteúdo da skill se torna o prompt que dirige o subagent. Ele não terá acesso ao seu histórico de conversa.

<Warning>
  `context: fork` apenas faz sentido para skills com instruções explícitas. Se sua skill contém diretrizes como "use estas convenções de API" sem uma tarefa, o subagent recebe as diretrizes mas nenhum prompt acionável, e retorna sem saída significativa.
</Warning>

Skills e [subagents](/pt/sub-agents) trabalham juntos em duas direções:

| Abordagem                   | Prompt do sistema                          | Tarefa                          | Também carrega                    |
| :-------------------------- | :----------------------------------------- | :------------------------------ | :-------------------------------- |
| Skill com `context: fork`   | Do tipo de agent (`Explore`, `Plan`, etc.) | Conteúdo de SKILL.md            | CLAUDE.md                         |
| Subagent com campo `skills` | Corpo markdown do subagent                 | Mensagem de delegação do Claude | Skills pré-carregadas + CLAUDE.md |

Com `context: fork`, você escreve a tarefa em sua skill e escolhe um tipo de agent para executá-la. Para o inverso (definir um subagent personalizado que usa skills como material de referência), consulte [Subagents](/pt/sub-agents#preload-skills-into-subagents).

#### Exemplo: Skill de pesquisa usando agent Explore

Esta skill executa pesquisa em um agent Explore bifurcado. O conteúdo da skill se torna a tarefa, e o agent fornece ferramentas somente leitura otimizadas para exploração de codebase:

```yaml  theme={null}
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

Quando esta skill é executada:

1. Um novo contexto isolado é criado
2. O subagent recebe o conteúdo da skill como seu prompt ("Research \$ARGUMENTS thoroughly...")
3. O campo `agent` determina o ambiente de execução (modelo, ferramentas e permissões)
4. Resultados são resumidos e retornados para sua conversa principal

O campo `agent` especifica qual configuração de subagent usar. As opções incluem agents integrados (`Explore`, `Plan`, `general-purpose`) ou qualquer subagent personalizado de `.claude/agents/`. Se omitido, usa `general-purpose`.

### Restrinja acesso de skill do Claude

Por padrão, Claude pode invocar qualquer skill que não tenha `disable-model-invocation: true` definido. Skills que definem `allowed-tools` concedem a Claude acesso a essas ferramentas sem aprovação por uso quando a skill está ativa. Suas [configurações de permissão](/pt/permissions) ainda governam comportamento de aprovação de linha de base para todas as outras ferramentas. Comandos integrados como `/compact` e `/init` não estão disponíveis através da ferramenta Skill.

Três formas de controlar quais skills Claude pode invocar:

**Desabilite todas as skills** negando a ferramenta Skill em `/permissions`:

```text  theme={null}
# Add to deny rules:
Skill
```

**Permita ou negue skills específicas** usando [regras de permissão](/pt/permissions):

```text  theme={null}
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

Sintaxe de permissão: `Skill(name)` para correspondência exata, `Skill(name *)` para correspondência de prefixo com qualquer argumento.

**Oculte skills individuais** adicionando `disable-model-invocation: true` ao seu frontmatter. Isso remove a skill do contexto do Claude inteiramente.

<Note>
  O campo `user-invocable` apenas controla visibilidade de menu, não acesso à ferramenta Skill. Use `disable-model-invocation: true` para bloquear invocação programática.
</Note>

## Compartilhe skills

Skills podem ser distribuídas em diferentes escopos dependendo do seu público:

* **Skills de projeto**: Faça commit de `.claude/skills/` para controle de versão
* **Plugins**: Crie um diretório `skills/` em seu [plugin](/pt/plugins)
* **Gerenciado**: Implante em toda a organização através de [configurações gerenciadas](/pt/settings#settings-files)

### Gere saída visual

Skills podem agrupar e executar scripts em qualquer linguagem, dando ao Claude capacidades além do que é possível em um único prompt. Um padrão poderoso é gerar saída visual: arquivos HTML interativos que abrem em seu navegador para explorar dados, depurar ou criar relatórios.

Este exemplo cria um explorador de codebase: uma visualização de árvore interativa onde você pode expandir e recolher diretórios, ver tamanhos de arquivo em um relance, e identificar tipos de arquivo por cor.

Crie o diretório da Skill:

```bash  theme={null}
mkdir -p ~/.claude/skills/codebase-visualizer/scripts
```

Crie `~/.claude/skills/codebase-visualizer/SKILL.md`. A descrição diz ao Claude quando ativar esta Skill, e as instruções dizem ao Claude para executar o script agrupado:

````yaml  theme={null}
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase. Use when exploring a new repo, understanding project structure, or identifying large files.
allowed-tools: Bash(python *)
---

# Codebase Visualizer

Generate an interactive HTML tree view that shows your project's file structure with collapsible directories.

## Usage

Run the visualization script from your project root:

```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```

This creates `codebase-map.html` in the current directory and opens it in your default browser.

## What the visualization shows

- **Collapsible directories**: Click folders to expand/collapse
- **File sizes**: Displayed next to each file
- **Colors**: Different colors for different file types
- **Directory totals**: Shows aggregate size of each folder
````

Crie `~/.claude/skills/codebase-visualizer/scripts/visualize.py`. Este script varre uma árvore de diretório e gera um arquivo HTML auto-contido com:

* Uma **barra lateral de resumo** mostrando contagem de arquivos, contagem de diretórios, tamanho total e número de tipos de arquivo
* Um **gráfico de barras** dividindo o codebase por tipo de arquivo (top 8 por tamanho)
* Uma **árvore recolhível** onde você pode expandir e recolher diretórios, com indicadores de tipo de arquivo codificados por cor

O script requer Python mas usa apenas bibliotecas integradas, então não há pacotes para instalar:

```python expandable theme={null}
#!/usr/bin/env python3
"""Generate an interactive collapsible tree visualization of a codebase."""

import json
import sys
import webbrowser
from pathlib import Path
from collections import Counter

IGNORE = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}

def scan(path: Path, stats: dict) -> dict:
    result = {"name": path.name, "children": [], "size": 0}
    try:
        for item in sorted(path.iterdir()):
            if item.name in IGNORE or item.name.startswith('.'):
                continue
            if item.is_file():
                size = item.stat().st_size
                ext = item.suffix.lower() or '(no ext)'
                result["children"].append({"name": item.name, "size": size, "ext": ext})
                result["size"] += size
                stats["files"] += 1
                stats["extensions"][ext] += 1
                stats["ext_sizes"][ext] += size
            elif item.is_dir():
                stats["dirs"] += 1
                child = scan(item, stats)
                if child["children"]:
                    result["children"].append(child)
                    result["size"] += child["size"]
    except PermissionError:
        pass
    return result

def generate_html(data: dict, stats: dict, output: Path) -> None:
    ext_sizes = stats["ext_sizes"]
    total_size = sum(ext_sizes.values()) or 1
    sorted_exts = sorted(ext_sizes.items(), key=lambda x: -x[1])[:8]
    colors = {
        '.js': '#f7df1e', '.ts': '#3178c6', '.py': '#3776ab', '.go': '#00add8',
        '.rs': '#dea584', '.rb': '#cc342d', '.css': '#264de4', '.html': '#e34c26',
        '.json': '#6b7280', '.md': '#083fa1', '.yaml': '#cb171e', '.yml': '#cb171e',
        '.mdx': '#083fa1', '.tsx': '#3178c6', '.jsx': '#61dafb', '.sh': '#4eaa25',
    }
    lang_bars = "".join(
        f'<div class="bar-row"><span class="bar-label">{ext}</span>'
        f'<div class="bar" style="width:{(size/total_size)*100}%;background:{colors.get(ext,"#6b7280")}"></div>'
        f'<span class="bar-pct">{(size/total_size)*100:.1f}%</span></div>'
        for ext, size in sorted_exts
    )
    def fmt(b):
        if b < 1024: return f"{b} B"
        if b < 1048576: return f"{b/1024:.1f} KB"
        return f"{b/1048576:.1f} MB"

    html = f'''<!DOCTYPE html>
<html><head>
  <meta charset="utf-8"><title>Codebase Explorer</title>
  <style>
    body {{ font: 14px/1.5 system-ui, sans-serif; margin: 0; background: #1a1a2e; color: #eee; }}
    .container {{ display: flex; height: 100vh; }}
    .sidebar {{ width: 280px; background: #252542; padding: 20px; border-right: 1px solid #3d3d5c; overflow-y: auto; flex-shrink: 0; }}
    .main {{ flex: 1; padding: 20px; overflow-y: auto; }}
    h1 {{ margin: 0 0 10px 0; font-size: 18px; }}
    h2 {{ margin: 20px 0 10px 0; font-size: 14px; color: #888; text-transform: uppercase; }}
    .stat {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #3d3d5c; }}
    .stat-value {{ font-weight: bold; }}
    .bar-row {{ display: flex; align-items: center; margin: 6px 0; }}
    .bar-label {{ width: 55px; font-size: 12px; color: #aaa; }}
    .bar {{ height: 18px; border-radius: 3px; }}
    .bar-pct {{ margin-left: 8px; font-size: 12px; color: #666; }}
    .tree {{ list-style: none; padding-left: 20px; }}
    details {{ cursor: pointer; }}
    summary {{ padding: 4px 8px; border-radius: 4px; }}
    summary:hover {{ background: #2d2d44; }}
    .folder {{ color: #ffd700; }}
    .file {{ display: flex; align-items: center; padding: 4px 8px; border-radius: 4px; }}
    .file:hover {{ background: #2d2d44; }}
    .size {{ color: #888; margin-left: auto; font-size: 12px; }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }}
  </style>
</head><body>
  <div class="container">
    <div class="sidebar">
      <h1>📊 Summary</h1>
      <div class="stat"><span>Files</span><span class="stat-value">{stats["files"]:,}</span></div>
      <div class="stat"><span>Directories</span><span class="stat-value">{stats["dirs"]:,}</span></div>
      <div class="stat"><span>Total size</span><span class="stat-value">{fmt(data["size"])}</span></div>
      <div class="stat"><span>File types</span><span class="stat-value">{len(stats["extensions"])}</span></div>
      <h2>By file type</h2>
      {lang_bars}
    </div>
    <div class="main">
      <h1>📁 {data["name"]}</h1>
      <ul class="tree" id="root"></ul>
    </div>
  </div>
  <script>
    const data = {json.dumps(data)};
    const colors = {json.dumps(colors)};
    function fmt(b) {{ if (b < 1024) return b + ' B'; if (b < 1048576) return (b/1024).toFixed(1) + ' KB'; return (b/1048576).toFixed(1) + ' MB'; }}
    function render(node, parent) {{
      if (node.children) {{
        const det = document.createElement('details');
        det.open = parent === document.getElementById('root');
        det.innerHTML = `<summary><span class="folder">📁 ${{node.name}}</span><span class="size">${{fmt(node.size)}}</span></summary>`;
        const ul = document.createElement('ul'); ul.className = 'tree';
        node.children.sort((a,b) => (b.children?1:0)-(a.children?1:0) || a.name.localeCompare(b.name));
        node.children.forEach(c => render(c, ul));
        det.appendChild(ul);
        const li = document.createElement('li'); li.appendChild(det); parent.appendChild(li);
      }} else {{
        const li = document.createElement('li'); li.className = 'file';
        li.innerHTML = `<span class="dot" style="background:${{colors[node.ext]||'#6b7280'}}"></span>${{node.name}}<span class="size">${{fmt(node.size)}}</span>`;
        parent.appendChild(li);
      }}
    }}
    data.children.forEach(c => render(c, document.getElementById('root')));
  </script>
</body></html>'''
    output.write_text(html)

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    stats = {"files": 0, "dirs": 0, "extensions": Counter(), "ext_sizes": Counter()}
    data = scan(target, stats)
    out = Path('codebase-map.html')
    generate_html(data, stats, out)
    print(f'Generated {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')
```

Para testar, abra Claude Code em qualquer projeto e peça "Visualize this codebase." Claude executa o script, gera `codebase-map.html`, e abre em seu navegador.

Este padrão funciona para qualquer saída visual: gráficos de dependência, relatórios de cobertura de testes, documentação de API, ou visualizações de esquema de banco de dados. O script agrupado faz o trabalho pesado enquanto Claude lida com orquestração.

## Solução de problemas

### Skill não dispara

Se Claude não usa sua skill quando esperado:

1. Verifique se a descrição inclui palavras-chave que usuários naturalmente diriam
2. Verifique se a skill aparece em `What skills are available?`
3. Tente reformular sua solicitação para corresponder mais de perto à descrição
4. Invoque-a diretamente com `/skill-name` se a skill é invocável pelo usuário

### Skill dispara muito frequentemente

Se Claude usa sua skill quando você não quer:

1. Torne a descrição mais específica
2. Adicione `disable-model-invocation: true` se você quer apenas invocação manual

### Claude não vê todas as minhas skills

Descrições de skills são carregadas em contexto para que Claude saiba o que está disponível. Se você tem muitas skills, elas podem exceder o orçamento de caracteres. O orçamento escala dinamicamente em 2% da janela de contexto, com fallback de 16.000 caracteres. Execute `/context` para verificar um aviso sobre skills excluídas.

Para sobrescrever o limite, defina a variável de ambiente `SLASH_COMMAND_TOOL_CHAR_BUDGET`.

## Recursos relacionados

* **[Subagents](/pt/sub-agents)**: delegue tarefas para agents especializados
* **[Plugins](/pt/plugins)**: empacote e distribua skills com outras extensões
* **[Hooks](/pt/hooks)**: automatize fluxos de trabalho em torno de eventos de ferramentas
* **[Memory](/pt/memory)**: gerencie arquivos CLAUDE.md para contexto persistente
* **[Comandos integrados](/pt/commands)**: referência para comandos `/` integrados
* **[Permissões](/pt/permissions)**: controle acesso a ferramentas e skills
