> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Visão geral do Claude Code

> Claude Code é uma ferramenta de codificação agentic que lê sua base de código, edita arquivos, executa comandos e se integra com suas ferramentas de desenvolvimento. Disponível em seu terminal, IDE, aplicativo de desktop e navegador.

Claude Code é um assistente de codificação alimentado por IA que ajuda você a construir recursos, corrigir bugs e automatizar tarefas de desenvolvimento. Ele compreende toda a sua base de código e pode trabalhar em múltiplos arquivos e ferramentas para realizar tarefas.

## Comece agora

Escolha seu ambiente para começar. A maioria das superfícies requer uma [assinatura Claude](https://claude.com/pricing) ou uma conta do [Anthropic Console](https://console.anthropic.com/). O Terminal CLI e VS Code também suportam [provedores de terceiros](/pt/third-party-integrations).

<Tabs>
  <Tab title="Terminal">
    O CLI completo para trabalhar com Claude Code diretamente em seu terminal. Edite arquivos, execute comandos e gerencie todo o seu projeto a partir da linha de comando.

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

    Em seguida, inicie Claude Code em qualquer projeto:

    ```bash  theme={null}
    cd your-project
    claude
    ```

    Você será solicitado a fazer login no primeiro uso. É isso! [Continue com o Quickstart →](/pt/quickstart)

    <Tip>
      Veja [configuração avançada](/pt/setup) para opções de instalação, atualizações manuais ou instruções de desinstalação. Visite [troubleshooting](/pt/troubleshooting) se você encontrar problemas.
    </Tip>
  </Tab>

  <Tab title="VS Code">
    A extensão VS Code fornece diffs inline, @-mentions, revisão de plano e histórico de conversa diretamente em seu editor.

    * [Instalar para VS Code](vscode:extension/anthropic.claude-code)
    * [Instalar para Cursor](cursor:extension/anthropic.claude-code)

    Ou procure por "Claude Code" na visualização de Extensões (`Cmd+Shift+X` no Mac, `Ctrl+Shift+X` no Windows/Linux). Após instalar, abra a Paleta de Comandos (`Cmd+Shift+P` / `Ctrl+Shift+P`), digite "Claude Code" e selecione **Open in New Tab**.

    [Comece com VS Code →](/pt/vs-code#get-started)
  </Tab>

  <Tab title="Aplicativo de desktop">
    Um aplicativo independente para executar Claude Code fora de seu IDE ou terminal. Revise diffs visualmente, execute múltiplas sessões lado a lado, agende tarefas recorrentes e inicie sessões em nuvem.

    Baixe e instale:

    * [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) (Intel e Apple Silicon)
    * [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) (x64)
    * [Windows ARM64](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) (apenas sessões remotas)

    Após instalar, inicie Claude, faça login e clique na aba **Code** para começar a codificar. Uma [assinatura paga](https://claude.com/pricing) é necessária.

    [Saiba mais sobre o aplicativo de desktop →](/pt/desktop-quickstart)
  </Tab>

  <Tab title="Web">
    Execute Claude Code em seu navegador sem configuração local. Inicie tarefas de longa duração e verifique quando estiverem prontas, trabalhe em repositórios que você não tem localmente ou execute múltiplas tarefas em paralelo. Disponível em navegadores de desktop e no aplicativo Claude iOS.

    Comece a codificar em [claude.ai/code](https://claude.ai/code).

    [Comece na web →](/pt/claude-code-on-the-web#getting-started)
  </Tab>

  <Tab title="JetBrains">
    Um plugin para IntelliJ IDEA, PyCharm, WebStorm e outras IDEs JetBrains com visualização de diff interativa e compartilhamento de contexto de seleção.

    Instale o [plugin Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) do JetBrains Marketplace e reinicie sua IDE.

    [Comece com JetBrains →](/pt/jetbrains)
  </Tab>
</Tabs>

## O que você pode fazer

Aqui estão algumas das maneiras como você pode usar Claude Code:

<AccordionGroup>
  <Accordion title="Automatize o trabalho que você continua adiando" icon="wand-magic-sparkles">
    Claude Code lida com as tarefas tediosas que consomem seu dia: escrever testes para código não testado, corrigir erros de lint em um projeto, resolver conflitos de mesclagem, atualizar dependências e escrever notas de lançamento.

    ```bash  theme={null}
    claude "write tests for the auth module, run them, and fix any failures"
    ```
  </Accordion>

  <Accordion title="Construa recursos e corrija bugs" icon="hammer">
    Descreva o que você quer em linguagem simples. Claude Code planeja a abordagem, escreve o código em múltiplos arquivos e verifica se funciona.

    Para bugs, cole uma mensagem de erro ou descreva o sintoma. Claude Code rastreia o problema em sua base de código, identifica a causa raiz e implementa uma correção. Veja [fluxos de trabalho comuns](/pt/common-workflows) para mais exemplos.
  </Accordion>

  <Accordion title="Crie commits e pull requests" icon="code-branch">
    Claude Code funciona diretamente com git. Ele prepara alterações, escreve mensagens de commit, cria branches e abre pull requests.

    ```bash  theme={null}
    claude "commit my changes with a descriptive message"
    ```

    Em CI, você pode automatizar revisão de código e triagem de problemas com [GitHub Actions](/pt/github-actions) ou [GitLab CI/CD](/pt/gitlab-ci-cd).
  </Accordion>

  <Accordion title="Conecte suas ferramentas com MCP" icon="plug">
    O [Model Context Protocol (MCP)](/pt/mcp) é um padrão aberto para conectar ferramentas de IA a fontes de dados externas. Com MCP, Claude Code pode ler seus documentos de design no Google Drive, atualizar tickets no Jira, extrair dados do Slack ou usar suas próprias ferramentas personalizadas.
  </Accordion>

  <Accordion title="Personalize com instruções, skills e hooks" icon="sliders">
    [`CLAUDE.md`](/pt/memory) é um arquivo markdown que você adiciona à raiz do seu projeto que Claude Code lê no início de cada sessão. Use-o para definir padrões de codificação, decisões de arquitetura, bibliotecas preferidas e listas de verificação de revisão. Claude também constrói [memória automática](/pt/memory#auto-memory) conforme trabalha, salvando aprendizados como comandos de compilação e insights de depuração em sessões sem você escrever nada.

    Crie [comandos personalizados](/pt/skills) para empacotar fluxos de trabalho repetíveis que sua equipe pode compartilhar, como `/review-pr` ou `/deploy-staging`.

    [Hooks](/pt/hooks) permitem que você execute comandos shell antes ou depois de ações do Claude Code, como formatação automática após cada edição de arquivo ou execução de lint antes de um commit.
  </Accordion>

  <Accordion title="Execute equipes de agentes e construa agentes personalizados" icon="users">
    Inicie [múltiplos agentes Claude Code](/pt/sub-agents) que trabalham em diferentes partes de uma tarefa simultaneamente. Um agente líder coordena o trabalho, atribui subtarefas e mescla resultados.

    Para fluxos de trabalho totalmente personalizados, o [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) permite que você construa seus próprios agentes alimentados pelas ferramentas e capacidades do Claude Code, com controle total sobre orquestração, acesso a ferramentas e permissões.
  </Accordion>

  <Accordion title="Pipe, script e automatize com o CLI" icon="terminal">
    Claude Code é composável e segue a filosofia Unix. Pipe logs nele, execute-o em CI ou encadeie-o com outras ferramentas:

    ```bash  theme={null}
    # Monitor logs and get alerted
    tail -f app.log | claude -p "Slack me if you see any anomalies"

    # Automate translations in CI
    claude -p "translate new strings into French and raise a PR for review"

    # Bulk operations across files
    git diff main --name-only | claude -p "review these changed files for security issues"
    ```

    Veja a [referência CLI](/pt/cli-reference) para o conjunto completo de comandos e flags.
  </Accordion>

  <Accordion title="Trabalhe de qualquer lugar" icon="globe">
    As sessões não estão vinculadas a uma única superfície. Mova o trabalho entre ambientes conforme seu contexto muda:

    * Afaste-se de sua mesa e continue trabalhando do seu telefone ou qualquer navegador com [Remote Control](/pt/remote-control)
    * Inicie uma tarefa de longa duração na [web](/pt/claude-code-on-the-web) ou [aplicativo iOS](https://apps.apple.com/app/claude-by-anthropic/id6473753684), depois puxe-a para seu terminal com `/teleport`
    * Entregue uma sessão de terminal para o [aplicativo Desktop](/pt/desktop) com `/desktop` para revisão visual de diff
    * Rotear tarefas do chat da equipe: mencione `@Claude` no [Slack](/pt/slack) com um relatório de bug e obtenha um pull request de volta
  </Accordion>
</AccordionGroup>

## Use Claude Code em qualquer lugar

Cada superfície se conecta ao mesmo mecanismo Claude Code subjacente, portanto seus arquivos CLAUDE.md, configurações e servidores MCP funcionam em todos eles.

Além dos ambientes [Terminal](/pt/quickstart), [VS Code](/pt/vs-code), [JetBrains](/pt/jetbrains), [Desktop](/pt/desktop) e [Web](/pt/claude-code-on-the-web) acima, Claude Code se integra com CI/CD, chat e fluxos de trabalho de navegador:

| Eu quero...                                                            | Melhor opção                                                                                                              |
| ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------- |
| Continuar uma sessão local do meu telefone ou outro dispositivo        | [Remote Control](/pt/remote-control)                                                                                      |
| Iniciar uma tarefa localmente, continuar no celular                    | [Web](/pt/claude-code-on-the-web) ou [aplicativo Claude iOS](https://apps.apple.com/app/claude-by-anthropic/id6473753684) |
| Automatizar revisões de PR e triagem de problemas                      | [GitHub Actions](/pt/github-actions) ou [GitLab CI/CD](/pt/gitlab-ci-cd)                                                  |
| Obter revisão de código automática em cada PR                          | [GitHub Code Review](/pt/code-review)                                                                                     |
| Rotear relatórios de bug do Slack para pull requests                   | [Slack](/pt/slack)                                                                                                        |
| Depurar aplicações web ao vivo                                         | [Chrome](/pt/chrome)                                                                                                      |
| Construir agentes personalizados para seus próprios fluxos de trabalho | [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)                                                       |

## Próximos passos

Depois de instalar Claude Code, estes guias ajudam você a aprofundar.

* [Quickstart](/pt/quickstart): caminhe através de sua primeira tarefa real, desde explorar uma base de código até fazer commit de uma correção
* [Armazene instruções e memórias](/pt/memory): dê ao Claude instruções persistentes com arquivos CLAUDE.md e memória automática
* [Fluxos de trabalho comuns](/pt/common-workflows) e [melhores práticas](/pt/best-practices): padrões para aproveitar ao máximo Claude Code
* [Configurações](/pt/settings): personalize Claude Code para seu fluxo de trabalho
* [Troubleshooting](/pt/troubleshooting): soluções para problemas comuns
* [code.claude.com](https://code.claude.com/): demos, preços e detalhes do produto
