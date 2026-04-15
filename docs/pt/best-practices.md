> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Melhores práticas para Claude Code

> Dicas e padrões para aproveitar ao máximo o Claude Code, desde a configuração do seu ambiente até o dimensionamento em sessões paralelas.

Claude Code é um ambiente de codificação agentic. Diferentemente de um chatbot que responde perguntas e espera, Claude Code pode ler seus arquivos, executar comandos, fazer alterações e trabalhar autonomamente através de problemas enquanto você observa, redireciona ou se afasta completamente.

Isso muda a forma como você trabalha. Em vez de escrever código você mesmo e pedir ao Claude para revisá-lo, você descreve o que deseja e Claude descobre como construir. Claude explora, planeja e implementa.

Mas essa autonomia ainda vem com uma curva de aprendizado. Claude trabalha dentro de certas restrições que você precisa entender.

Este guia cobre padrões que se mostraram eficazes nas equipes internas da Anthropic e para engenheiros usando Claude Code em vários codebases, linguagens e ambientes. Para saber como o loop agentic funciona nos bastidores, consulte [How Claude Code works](/pt/how-claude-code-works).

***

A maioria das melhores práticas é baseada em uma restrição: a janela de contexto do Claude se enche rapidamente e o desempenho se degrada conforme ela se enche.

A janela de contexto do Claude contém toda a sua conversa, incluindo cada mensagem, cada arquivo que Claude lê e cada saída de comando. No entanto, isso pode se encher rapidamente. Uma única sessão de depuração ou exploração de codebase pode gerar e consumir dezenas de milhares de tokens.

Isso importa porque o desempenho do LLM se degrada conforme o contexto se enche. Quando a janela de contexto está ficando cheia, Claude pode começar a "esquecer" instruções anteriores ou cometer mais erros. A janela de contexto é o recurso mais importante a gerenciar. Rastreie o uso de contexto continuamente com uma [custom status line](/pt/statusline), e veja [Reduce token usage](/pt/costs#reduce-token-usage) para estratégias de redução do uso de tokens.

***

## Dê ao Claude uma forma de verificar seu trabalho

<Tip>
  Inclua testes, capturas de tela ou saídas esperadas para que Claude possa se verificar. Esta é a coisa de maior alavancagem que você pode fazer.
</Tip>

Claude funciona dramaticamente melhor quando pode verificar seu próprio trabalho, como executar testes, comparar capturas de tela e validar saídas.

Sem critérios de sucesso claros, ele pode produzir algo que parece certo mas na verdade não funciona. Você se torna o único loop de feedback, e cada erro requer sua atenção.

| Estratégia                                 | Antes                                                   | Depois                                                                                                                                                                                                                  |
| ------------------------------------------ | ------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Forneça critérios de verificação**       | *"implemente uma função que valida endereços de email"* | *"escreva uma função validateEmail. exemplos de casos de teste: [user@example.com](mailto:user@example.com) é verdadeiro, inválido é falso, [user@.com](mailto:user@.com) é falso. execute os testes após implementar"* |
| **Verifique mudanças de UI visualmente**   | *"faça o dashboard parecer melhor"*                     | *"\[cole captura de tela] implemente este design. tire uma captura de tela do resultado e compare com o original. liste as diferenças e corrija-as"*                                                                    |
| **Aborde as causas raiz, não os sintomas** | *"a compilação está falhando"*                          | *"a compilação falha com este erro: \[cole erro]. corrija-o e verifique se a compilação é bem-sucedida. aborde a causa raiz, não suprima o erro"*                                                                       |

Mudanças de UI podem ser verificadas usando a [Claude in Chrome extension](/pt/chrome). Ela abre novas abas no seu navegador, testa a UI e itera até que o código funcione.

Sua verificação também pode ser um conjunto de testes, um linter ou um comando Bash que verifica a saída. Invista em tornar sua verificação sólida.

***

## Explore primeiro, depois planeje, depois codifique

<Tip>
  Separe pesquisa e planejamento da implementação para evitar resolver o problema errado.
</Tip>

Deixar Claude pular direto para codificação pode produzir código que resolve o problema errado. Use [Plan Mode](/pt/common-workflows#use-plan-mode-for-safe-code-analysis) para separar exploração de execução.

O fluxo de trabalho recomendado tem quatro fases:

<Steps>
  <Step title="Explore">
    Entre em Plan Mode. Claude lê arquivos e responde perguntas sem fazer alterações.

    ```txt claude (Plan Mode) theme={null}
    read /src/auth and understand how we handle sessions and login.
    also look at how we manage environment variables for secrets.
    ```
  </Step>

  <Step title="Plan">
    Peça ao Claude para criar um plano de implementação detalhado.

    ```txt claude (Plan Mode) theme={null}
    I want to add Google OAuth. What files need to change?
    What's the session flow? Create a plan.
    ```

    Pressione `Ctrl+G` para abrir o plano no seu editor de texto para edição direta antes de Claude prosseguir.
  </Step>

  <Step title="Implement">
    Volte para Normal Mode e deixe Claude codificar, verificando contra seu plano.

    ```txt claude (Normal Mode) theme={null}
    implement the OAuth flow from your plan. write tests for the
    callback handler, run the test suite and fix any failures.
    ```
  </Step>

  <Step title="Commit">
    Peça ao Claude para fazer commit com uma mensagem descritiva e criar um PR.

    ```txt claude (Normal Mode) theme={null}
    commit with a descriptive message and open a PR
    ```
  </Step>
</Steps>

<Callout>
  Plan Mode é útil, mas também adiciona sobrecarga.

  Para tarefas onde o escopo é claro e a correção é pequena (como corrigir um erro de digitação, adicionar uma linha de log ou renomear uma variável) peça ao Claude para fazer isso diretamente.

  O planejamento é mais útil quando você está incerto sobre a abordagem, quando a mudança modifica vários arquivos ou quando você não está familiarizado com o código sendo modificado. Se você pudesse descrever o diff em uma frase, pule o plano.
</Callout>

***

## Forneça contexto específico em seus prompts

<Tip>
  Quanto mais precisas suas instruções, menos correções você precisará.
</Tip>

Claude pode inferir intenção, mas não pode ler sua mente. Referencie arquivos específicos, mencione restrições e aponte para padrões de exemplo.

| Estratégia                                                                                      | Antes                                                  | Depois                                                                                                                                                                                                                                                                                                                                                      |
| ----------------------------------------------------------------------------------------------- | ------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Escopo a tarefa.** Especifique qual arquivo, qual cenário e preferências de teste.            | *"adicione testes para foo.py"*                        | *"escreva um teste para foo.py cobrindo o caso extremo onde o usuário está desconectado. evite mocks."*                                                                                                                                                                                                                                                     |
| **Aponte para fontes.** Dirija Claude para a fonte que pode responder uma pergunta.             | *"por que ExecutionFactory tem uma API tão estranha?"* | *"procure no histórico git do ExecutionFactory e resuma como sua API chegou a ser assim"*                                                                                                                                                                                                                                                                   |
| **Referencie padrões existentes.** Aponte Claude para padrões em seu codebase.                  | *"adicione um widget de calendário"*                   | *"veja como os widgets existentes são implementados na página inicial para entender os padrões. HotDogWidget.php é um bom exemplo. siga o padrão para implementar um novo widget de calendário que permite ao usuário selecionar um mês e paginar para frente/trás para escolher um ano. construa do zero sem bibliotecas além das já usadas no codebase."* |
| **Descreva o sintoma.** Forneça o sintoma, a localização provável e como "corrigido" se parece. | *"corrija o bug de login"*                             | *"usuários relatam que o login falha após timeout de sessão. verifique o fluxo de autenticação em src/auth/, especialmente atualização de token. escreva um teste falhando que reproduz o problema, depois corrija-o"*                                                                                                                                      |

Prompts vagos podem ser úteis quando você está explorando e pode se dar ao luxo de corrigir o curso. Um prompt como `"o que você melhoraria neste arquivo?"` pode revelar coisas que você não teria pensado em perguntar.

### Forneça conteúdo rico

<Tip>
  Use `@` para referenciar arquivos, cole capturas de tela/imagens ou canalize dados diretamente.
</Tip>

Você pode fornecer dados ricos ao Claude de várias maneiras:

* **Referencie arquivos com `@`** em vez de descrever onde o código vive. Claude lê o arquivo antes de responder.
* **Cole imagens diretamente**. Copie/cole ou arraste e solte imagens no prompt.
* **Forneça URLs** para documentação e referências de API. Use `/permissions` para colocar na lista de permissões domínios frequentemente usados.
* **Canalize dados** executando `cat error.log | claude` para enviar conteúdos de arquivo diretamente.
* **Deixe Claude buscar o que precisa**. Diga ao Claude para puxar contexto ele mesmo usando comandos Bash, ferramentas MCP ou lendo arquivos.

***

## Configure seu ambiente

Alguns passos de configuração tornam Claude Code significativamente mais eficaz em todas as suas sessões. Para uma visão geral completa dos recursos de extensão e quando usar cada um, consulte [Extend Claude Code](/pt/features-overview).

### Escreva um CLAUDE.md eficaz

<Tip>
  Execute `/init` para gerar um arquivo CLAUDE.md inicial baseado na estrutura do seu projeto atual, depois refine ao longo do tempo.
</Tip>

CLAUDE.md é um arquivo especial que Claude lê no início de cada conversa. Inclua comandos Bash, estilo de código e regras de fluxo de trabalho. Isso dá ao Claude contexto persistente que ele não pode inferir apenas do código.

O comando `/init` analisa seu codebase para detectar sistemas de compilação, frameworks de teste e padrões de código, dando a você uma base sólida para refinar.

Não há formato obrigatório para arquivos CLAUDE.md, mas mantenha-o curto e legível para humanos. Por exemplo:

```markdown CLAUDE.md theme={null}
# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you're done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

CLAUDE.md é carregado a cada sessão, então inclua apenas coisas que se aplicam amplamente. Para conhecimento de domínio ou fluxos de trabalho que são apenas relevantes às vezes, use [skills](/pt/skills) em vez disso. Claude os carrega sob demanda sem inchar cada conversa.

Mantenha-o conciso. Para cada linha, pergunte: *"Remover isso causaria Claude cometer erros?"* Se não, corte. Arquivos CLAUDE.md inchados causam Claude ignorar suas instruções reais!

| ✅ Inclua                                                                 | ❌ Exclua                                                    |
| ------------------------------------------------------------------------ | ----------------------------------------------------------- |
| Comandos Bash que Claude não pode adivinhar                              | Qualquer coisa que Claude possa descobrir lendo código      |
| Regras de estilo de código que diferem dos padrões                       | Convenções de linguagem padrão que Claude já conhece        |
| Instruções de teste e executores de teste preferidos                     | Documentação detalhada de API (link para docs em vez disso) |
| Etiqueta de repositório (nomenclatura de branch, convenções de PR)       | Informações que mudam frequentemente                        |
| Decisões arquitetônicas específicas do seu projeto                       | Explicações longas ou tutoriais                             |
| Peculiaridades do ambiente de desenvolvedor (variáveis env obrigatórias) | Descrições arquivo por arquivo do codebase                  |
| Armadilhas comuns ou comportamentos não óbvios                           | Práticas auto-evidentes como "escreva código limpo"         |

Se Claude continua fazendo algo que você não quer apesar de ter uma regra contra isso, o arquivo provavelmente é muito longo e a regra está sendo perdida. Se Claude faz perguntas que são respondidas em CLAUDE.md, a redação pode ser ambígua. Trate CLAUDE.md como código: revise-o quando as coisas dão errado, poda-o regularmente e teste mudanças observando se o comportamento do Claude realmente muda.

Você pode ajustar instruções adicionando ênfase (por exemplo, "IMPORTANTE" ou "VOCÊ DEVE") para melhorar a adesão. Verifique CLAUDE.md no git para que sua equipe possa contribuir. O arquivo aumenta em valor ao longo do tempo.

Arquivos CLAUDE.md podem importar arquivos adicionais usando a sintaxe `@path/to/import`:

```markdown CLAUDE.md theme={null}
See @README.md for project overview and @package.json for available npm commands.

# Additional Instructions
- Git workflow: @docs/git-instructions.md
- Personal overrides: @~/.claude/my-project-instructions.md
```

Você pode colocar arquivos CLAUDE.md em vários locais:

* **Pasta home (`~/.claude/CLAUDE.md`)**: aplica-se a todas as sessões Claude
* **Raiz do projeto (`./CLAUDE.md`)**: verifique no git para compartilhar com sua equipe
* **Diretórios pai**: útil para monorepos onde tanto `root/CLAUDE.md` quanto `root/foo/CLAUDE.md` são puxados automaticamente
* **Diretórios filhos**: Claude puxa arquivos CLAUDE.md filhos sob demanda ao trabalhar com arquivos nesses diretórios

### Configure permissões

<Tip>
  Use [auto mode](/pt/permission-modes#eliminate-prompts-with-auto-mode) para deixar um classificador lidar com aprovações, `/permissions` para colocar na lista de permissões comandos específicos, ou `/sandbox` para isolamento em nível de SO. Cada um reduz interrupções enquanto mantém você no controle.
</Tip>

Por padrão, Claude Code solicita permissão para ações que podem modificar seu sistema: gravações de arquivo, comandos Bash, ferramentas MCP, etc. Isso é seguro mas tedioso. Após a décima aprovação você realmente não está revisando mais, você está apenas clicando. Existem três maneiras de reduzir essas interrupções:

* **Auto mode**: um modelo classificador separado revisa comandos e bloqueia apenas o que parece arriscado: escalação de escopo, infraestrutura desconhecida ou ações impulsionadas por conteúdo hostil. Melhor quando você confia na direção geral de uma tarefa mas não quer clicar em cada passo
* **Listas de permissões**: permita ferramentas específicas que você sabe que são seguras, como `npm run lint` ou `git commit`
* **Sandboxing**: ative isolamento em nível de SO que restringe acesso ao sistema de arquivos e rede, permitindo Claude trabalhar mais livremente dentro de limites definidos

Leia mais sobre [permission modes](/pt/permission-modes), [permission rules](/pt/permissions) e [sandboxing](/pt/sandboxing).

### Use ferramentas CLI

<Tip>
  Diga ao Claude Code para usar ferramentas CLI como `gh`, `aws`, `gcloud` e `sentry-cli` ao interagir com serviços externos.
</Tip>

Ferramentas CLI são a forma mais eficiente em contexto de interagir com serviços externos. Se você usa GitHub, instale o CLI `gh`. Claude sabe como usá-lo para criar issues, abrir pull requests e ler comentários. Sem `gh`, Claude ainda pode usar a API do GitHub, mas requisições não autenticadas frequentemente atingem limites de taxa.

Claude também é eficaz em aprender ferramentas CLI que não conhece. Tente prompts como `Use 'foo-cli-tool --help' to learn about foo tool, then use it to solve A, B, C.`

### Conecte MCP servers

<Tip>
  Execute `claude mcp add` para conectar ferramentas externas como Notion, Figma ou seu banco de dados.
</Tip>

Com [MCP servers](/pt/mcp), você pode pedir ao Claude para implementar recursos de rastreadores de issues, consultar bancos de dados, analisar dados de monitoramento, integrar designs do Figma e automatizar fluxos de trabalho.

### Configure hooks

<Tip>
  Use hooks para ações que devem acontecer toda vez com zero exceções.
</Tip>

[Hooks](/pt/hooks-guide) executam scripts automaticamente em pontos específicos do fluxo de trabalho do Claude. Diferentemente de instruções CLAUDE.md que são consultivas, hooks são determinísticos e garantem que a ação aconteça.

Claude pode escrever hooks para você. Tente prompts como *"Write a hook that runs eslint after every file edit"* ou *"Write a hook that blocks writes to the migrations folder."* Edite `.claude/settings.json` diretamente para configurar hooks manualmente, e execute `/hooks` para navegar o que está configurado.

### Crie skills

<Tip>
  Crie arquivos `SKILL.md` em `.claude/skills/` para dar ao Claude conhecimento de domínio e fluxos de trabalho reutilizáveis.
</Tip>

[Skills](/pt/skills) estendem o conhecimento do Claude com informações específicas do seu projeto, equipe ou domínio. Claude as aplica automaticamente quando relevante, ou você pode invocá-las diretamente com `/skill-name`.

Crie uma skill adicionando um diretório com um `SKILL.md` para `.claude/skills/`:

```markdown .claude/skills/api-conventions/SKILL.md theme={null}
---
name: api-conventions
description: REST API design conventions for our services
---
# API Conventions
- Use kebab-case for URL paths
- Use camelCase for JSON properties
- Always include pagination for list endpoints
- Version APIs in the URL path (/v1/, /v2/)
```

Skills também podem definir fluxos de trabalho reutilizáveis que você invoca diretamente:

```markdown .claude/skills/fix-issue/SKILL.md theme={null}
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---
Analyze and fix the GitHub issue: $ARGUMENTS.

1. Use `gh issue view` to get the issue details
2. Understand the problem described in the issue
3. Search the codebase for relevant files
4. Implement the necessary changes to fix the issue
5. Write and run tests to verify the fix
6. Ensure code passes linting and type checking
7. Create a descriptive commit message
8. Push and create a PR
```

Execute `/fix-issue 1234` para invocá-la. Use `disable-model-invocation: true` para fluxos de trabalho com efeitos colaterais que você quer disparar manualmente.

### Crie subagents personalizados

<Tip>
  Defina assistentes especializados em `.claude/agents/` que Claude pode delegar para tarefas isoladas.
</Tip>

[Subagents](/pt/sub-agents) executam em seu próprio contexto com seu próprio conjunto de ferramentas permitidas. Eles são úteis para tarefas que leem muitos arquivos ou precisam de foco especializado sem poluir sua conversa principal.

```markdown .claude/agents/security-reviewer.md theme={null}
---
name: security-reviewer
description: Reviews code for security vulnerabilities
tools: Read, Grep, Glob, Bash
model: opus
---
You are a senior security engineer. Review code for:
- Injection vulnerabilities (SQL, XSS, command injection)
- Authentication and authorization flaws
- Secrets or credentials in code
- Insecure data handling

Provide specific line references and suggested fixes.
```

Diga ao Claude para usar subagents explicitamente: *"Use a subagent to review this code for security issues."*

### Instale plugins

<Tip>
  Execute `/plugin` para navegar no marketplace. Plugins adicionam skills, ferramentas e integrações sem configuração.
</Tip>

[Plugins](/pt/plugins) agrupam skills, hooks, subagents e MCP servers em uma única unidade instalável da comunidade e Anthropic. Se você trabalha com uma linguagem tipada, instale um [code intelligence plugin](/pt/discover-plugins#code-intelligence) para dar ao Claude navegação de símbolo precisa e detecção automática de erros após edições.

Para orientação sobre escolher entre skills, subagents, hooks e MCP, consulte [Extend Claude Code](/pt/features-overview#match-features-to-your-goal).

***

## Comunique-se efetivamente

A forma como você se comunica com Claude Code impacta significativamente a qualidade dos resultados.

### Faça perguntas sobre o codebase

<Tip>
  Faça ao Claude perguntas que você faria a um engenheiro sênior.
</Tip>

Ao se integrar a um novo codebase, use Claude Code para aprendizado e exploração. Você pode fazer ao Claude o mesmo tipo de perguntas que faria a outro engenheiro:

* Como funciona o logging?
* Como faço um novo endpoint de API?
* O que `async move { ... }` faz na linha 134 de `foo.rs`?
* Quais casos extremos `CustomerOnboardingFlowImpl` trata?
* Por que este código chama `foo()` em vez de `bar()` na linha 333?

Usar Claude Code dessa forma é um fluxo de trabalho de integração eficaz, melhorando o tempo de ramp-up e reduzindo carga em outros engenheiros. Nenhum prompt especial necessário: faça perguntas diretamente.

### Deixe Claude entrevistá-lo

<Tip>
  Para recursos maiores, deixe Claude entrevistá-lo primeiro. Comece com um prompt mínimo e peça ao Claude para entrevistá-lo usando a ferramenta `AskUserQuestion`.
</Tip>

Claude pergunta sobre coisas que você pode não ter considerado ainda, incluindo implementação técnica, UI/UX, casos extremos e tradeoffs.

```text theme={null}
I want to build [brief description]. Interview me in detail using the AskUserQuestion tool.

Ask about technical implementation, UI/UX, edge cases, concerns, and tradeoffs. Don't ask obvious questions, dig into the hard parts I might not have considered.

Keep interviewing until we've covered everything, then write a complete spec to SPEC.md.
```

Uma vez que o spec está completo, comece uma nova sessão para executá-lo. A nova sessão tem contexto limpo focado inteiramente em implementação, e você tem um spec escrito para referenciar.

***

## Gerencie sua sessão

Conversas são persistentes e reversíveis. Use isso a seu favor!

### Corrija o curso cedo e frequentemente

<Tip>
  Corrija Claude assim que notar que está saindo do caminho.
</Tip>

Os melhores resultados vêm de loops de feedback apertados. Embora Claude ocasionalmente resolva problemas perfeitamente na primeira tentativa, corrigi-lo rapidamente geralmente produz melhores soluções mais rápido.

* **`Esc`**: pare Claude no meio da ação com a tecla `Esc`. O contexto é preservado, então você pode redirecionar.
* **`Esc + Esc` ou `/rewind`**: pressione `Esc` duas vezes ou execute `/rewind` para abrir o menu de rewind e restaurar conversa e estado de código anterior, ou resumir a partir de uma mensagem selecionada.
* **`"Undo that"`**: peça ao Claude para reverter suas alterações.
* **`/clear`**: redefina contexto entre tarefas não relacionadas. Sessões longas com contexto irrelevante podem reduzir desempenho.

Se você corrigiu Claude mais de duas vezes no mesmo problema em uma sessão, o contexto está poluído com abordagens falhadas. Execute `/clear` e comece de novo com um prompt mais específico que incorpore o que você aprendeu. Uma sessão limpa com um prompt melhor quase sempre supera uma sessão longa com correções acumuladas.

### Gerencie contexto agressivamente

<Tip>
  Execute `/clear` entre tarefas não relacionadas para redefinir contexto.
</Tip>

Claude Code compacta automaticamente o histórico de conversa quando você se aproxima dos limites de contexto, o que preserva código e decisões importantes enquanto libera espaço.

Durante sessões longas, a janela de contexto do Claude pode se encher com conversa irrelevante, conteúdos de arquivo e comandos. Isso pode reduzir desempenho e às vezes distrair Claude.

* Use `/clear` frequentemente entre tarefas para redefinir a janela de contexto inteiramente
* Quando auto compaction dispara, Claude resume o que importa mais, incluindo padrões de código, estados de arquivo e decisões-chave
* Para mais controle, execute `/compact <instructions>`, como `/compact Focus on the API changes`
* Para compactar apenas parte da conversa, use `Esc + Esc` ou `/rewind`, selecione um checkpoint de mensagem e escolha **Summarize from here**. Isso condensa mensagens daquele ponto em diante enquanto mantém contexto anterior intacto.
* Customize comportamento de compaction em CLAUDE.md com instruções como `"When compacting, always preserve the full list of modified files and any test commands"` para garantir que contexto crítico sobreviva à sumarização
* Para perguntas rápidas que não precisam ficar em contexto, use [`/btw`](/pt/interactive-mode#side-questions-with-btw). A resposta aparece em uma sobreposição dispensável e nunca entra no histórico de conversa, então você pode verificar um detalhe sem crescer contexto.

### Use subagents para investigação

<Tip>
  Delegue pesquisa com `"use subagents to investigate X"`. Eles exploram em um contexto separado, mantendo sua conversa principal limpa para implementação.
</Tip>

Como contexto é sua restrição fundamental, subagents são uma das ferramentas mais poderosas disponíveis. Quando Claude pesquisa um codebase ele lê muitos arquivos, todos os quais consomem seu contexto. Subagents executam em janelas de contexto separadas e relatam resumos:

```text theme={null}
Use subagents to investigate how our authentication system handles token
refresh, and whether we have any existing OAuth utilities I should reuse.
```

O subagent explora o codebase, lê arquivos relevantes e relata descobertas, tudo sem poluir sua conversa principal.

Você também pode usar subagents para verificação após Claude implementar algo:

```text theme={null}
use a subagent to review this code for edge cases
```

### Rewind com checkpoints

<Tip>
  Cada ação que Claude faz cria um checkpoint. Você pode restaurar conversa, código ou ambos para qualquer checkpoint anterior.
</Tip>

Claude automaticamente faz checkpoint antes de mudanças. Pressione Escape duas vezes ou execute `/rewind` para abrir o menu de rewind. Você pode restaurar apenas conversa, restaurar apenas código, restaurar ambos ou resumir a partir de uma mensagem selecionada. Veja [Checkpointing](/pt/checkpointing) para detalhes.

Em vez de planejar cuidadosamente cada movimento, você pode dizer ao Claude para tentar algo arriscado. Se não funcionar, rewind e tente uma abordagem diferente. Checkpoints persistem entre sessões, então você pode fechar seu terminal e ainda fazer rewind depois.

<Warning>
  Checkpoints apenas rastreiam mudanças feitas *por Claude*, não processos externos. Isso não é um substituto para git.
</Warning>

### Retome conversas

<Tip>
  Execute `claude --continue` para continuar de onde parou, ou `--resume` para escolher entre sessões recentes.
</Tip>

Claude Code salva conversas localmente. Quando uma tarefa abrange múltiplas sessões, você não tem que re-explicar o contexto:

```bash theme={null}
claude --continue    # Resume the most recent conversation
claude --resume      # Select from recent conversations
```

Use `/rename` para dar às sessões nomes descritivos como `"oauth-migration"` ou `"debugging-memory-leak"` para que você possa encontrá-las depois. Trate sessões como branches: diferentes fluxos de trabalho podem ter contextos separados e persistentes.

***

## Automatize e dimensione

Uma vez que você é eficaz com um Claude, multiplique sua saída com sessões paralelas, modo não-interativo e padrões de fan-out.

Tudo até agora assume um humano, um Claude e uma conversa. Mas Claude Code dimensiona horizontalmente. As técnicas nesta seção mostram como você pode fazer mais.

### Execute modo não-interativo

<Tip>
  Use `claude -p "prompt"` em CI, pre-commit hooks ou scripts. Adicione `--output-format stream-json` para saída JSON em streaming.
</Tip>

Com `claude -p "your prompt"`, você pode executar Claude não-interativamente, sem uma sessão. Modo não-interativo é como você integra Claude em pipelines CI, pre-commit hooks ou qualquer fluxo de trabalho automatizado. Os formatos de saída permitem você analisar resultados programaticamente: texto simples, JSON ou JSON em streaming.

```bash theme={null}
# One-off queries
claude -p "Explain what this project does"

# Structured output for scripts
claude -p "List all API endpoints" --output-format json

# Streaming for real-time processing
claude -p "Analyze this log file" --output-format stream-json
```

### Execute múltiplas sessões Claude

<Tip>
  Execute múltiplas sessões Claude em paralelo para acelerar desenvolvimento, executar experimentos isolados ou iniciar fluxos de trabalho complexos.
</Tip>

Existem três maneiras principais de executar sessões paralelas:

* [Claude Code desktop app](/pt/desktop#work-in-parallel-with-sessions): Gerencie múltiplas sessões locais visualmente. Cada sessão obtém seu próprio worktree isolado.
* [Claude Code on the web](/pt/claude-code-on-the-web): Execute na infraestrutura de nuvem segura da Anthropic em VMs isoladas.
* [Agent teams](/pt/agent-teams): Coordenação automatizada de múltiplas sessões com tarefas compartilhadas, mensagens e um team lead.

Além de paralelizar trabalho, múltiplas sessões habilitam fluxos de trabalho focados em qualidade. Um contexto fresco melhora revisão de código já que Claude não será enviesado para código que acabou de escrever.

Por exemplo, use um padrão Writer/Reviewer:

| Session A (Writer)                                                      | Session B (Reviewer)                                                                                                                                                     |
| ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `Implement a rate limiter for our API endpoints`                        |                                                                                                                                                                          |
|                                                                         | `Review the rate limiter implementation in @src/middleware/rateLimiter.ts. Look for edge cases, race conditions, and consistency with our existing middleware patterns.` |
| `Here's the review feedback: [Session B output]. Address these issues.` |                                                                                                                                                                          |

Você pode fazer algo similar com testes: ter um Claude escrever testes, depois outro escrever código para passá-los.

### Fan out entre arquivos

<Tip>
  Loop através de tarefas chamando `claude -p` para cada. Use `--allowedTools` para escopear permissões para operações em lote.
</Tip>

Para grandes migrações ou análises, você pode distribuir trabalho entre muitas invocações Claude paralelas:

<Steps>
  <Step title="Generate a task list">
    Tenha Claude listar todos os arquivos que precisam ser migrados (por exemplo, `list all 2,000 Python files that need migrating`)
  </Step>

  <Step title="Write a script to loop through the list">
    ```bash theme={null}
    for file in $(cat files.txt); do
      claude -p "Migrate $file from React to Vue. Return OK or FAIL." \
        --allowedTools "Edit,Bash(git commit *)"
    done
    ```
  </Step>

  <Step title="Test on a few files, then run at scale">
    Refine seu prompt baseado no que dá errado com os primeiros 2-3 arquivos, depois execute no conjunto completo. A flag `--allowedTools` restringe o que Claude pode fazer, o que importa quando você está executando sem supervisão.
  </Step>
</Steps>

Você também pode integrar Claude em pipelines de dados/processamento existentes:

```bash theme={null}
claude -p "<your prompt>" --output-format json | your_command
```

Use `--verbose` para depuração durante desenvolvimento e desligue em produção.

### Execute autonomamente com auto mode

Para execução ininterrupta com verificações de segurança em background, use [auto mode](/pt/permission-modes#eliminate-prompts-with-auto-mode). Um modelo classificador revisa comandos antes de serem executados, bloqueando escalação de escopo, infraestrutura desconhecida e ações impulsionadas por conteúdo hostil enquanto deixa trabalho rotineiro prosseguir sem prompts.

```bash theme={null}
claude --permission-mode auto -p "fix all lint errors"
```

Para execuções não-interativas com a flag `-p`, auto mode aborta se o classificador repetidamente bloqueia ações, já que não há usuário para recorrer. Veja [when auto mode falls back](/pt/permission-modes#when-auto-mode-falls-back) para limites.

***

## Evite padrões de falha comuns

Estes são erros comuns. Reconhecê-los cedo economiza tempo:

* **A sessão da pia da cozinha.** Você começa com uma tarefa, depois pergunta ao Claude algo não relacionado, depois volta para a primeira tarefa. Contexto está cheio de informação irrelevante.
  > **Correção**: `/clear` entre tarefas não relacionadas.
* **Corrigindo repetidamente.** Claude faz algo errado, você corrige, ainda está errado, você corrige novamente. Contexto está poluído com abordagens falhadas.
  > **Correção**: Após duas correções falhadas, `/clear` e escreva um prompt inicial melhor incorporando o que você aprendeu.
* **O CLAUDE.md sobre-especificado.** Se seu CLAUDE.md é muito longo, Claude ignora metade dele porque regras importantes se perdem no ruído.
  > **Correção**: Poda impiedosamente. Se Claude já faz algo corretamente sem a instrução, delete-a ou converta-a para um hook.
* **A lacuna confiança-depois-verificação.** Claude produz uma implementação que parece plausível mas não trata casos extremos.
  > **Correção**: Sempre forneça verificação (testes, scripts, capturas de tela). Se você não pode verificar, não envie.
* **A exploração infinita.** Você pede ao Claude para "investigar" algo sem escopá-lo. Claude lê centenas de arquivos, enchendo o contexto.
  > **Correção**: Escopo investigações estreitamente ou use subagents para que a exploração não consuma seu contexto principal.

***

## Desenvolva sua intuição

Os padrões neste guia não são gravados em pedra. Eles são pontos de partida que funcionam bem em geral, mas podem não ser ótimos para cada situação.

Às vezes você *deveria* deixar contexto acumular porque você está profundo em um problema complexo e o histórico é valioso. Às vezes você deveria pular planejamento e deixar Claude descobrir porque a tarefa é exploratória. Às vezes um prompt vago é exatamente certo porque você quer ver como Claude interpreta o problema antes de constrangê-lo.

Preste atenção ao que funciona. Quando Claude produz saída ótima, note o que você fez: a estrutura do prompt, o contexto que você forneceu, o modo que você estava. Quando Claude luta, pergunte por quê. O contexto era muito barulhento? O prompt muito vago? A tarefa muito grande para uma passagem?

Ao longo do tempo, você desenvolverá intuição que nenhum guia pode capturar. Você saberá quando ser específico e quando ser aberto, quando planejar e quando explorar, quando limpar contexto e quando deixá-lo acumular.

## Recursos relacionados

* [How Claude Code works](/pt/how-claude-code-works): o loop agentic, ferramentas e gerenciamento de contexto
* [Extend Claude Code](/pt/features-overview): skills, hooks, MCP, subagents e plugins
* [Common workflows](/pt/common-workflows): receitas passo a passo para depuração, teste, PRs e mais
* [CLAUDE.md](/pt/memory): armazene convenções de projeto e contexto persistente
