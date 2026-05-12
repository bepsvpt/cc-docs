> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Guia de Início Rápido

> Bem-vindo ao Claude Code!

Este guia de início rápido o colocará usando assistência de codificação alimentada por IA em poucos minutos. Ao final, você entenderá como usar Claude Code para tarefas comuns de desenvolvimento.

## Antes de começar

Certifique-se de que você tem:

* Um terminal ou prompt de comando aberto
  * Se você nunca usou o terminal antes, confira o [guia de terminal](/pt/terminal-guide)
* Um projeto de código para trabalhar
* Uma [assinatura Claude](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=quickstart_prereq) (Pro, Max, Team ou Enterprise), conta do [Claude Console](https://console.anthropic.com/), ou acesso através de um [provedor de nuvem suportado](/pt/third-party-integrations)

<Note>
  Este guia cobre o CLI do terminal. Claude Code também está disponível na [web](https://claude.ai/code), como um [aplicativo de desktop](/pt/desktop), em [VS Code](/pt/vs-code) e [IDEs JetBrains](/pt/jetbrains), no [Slack](/pt/slack), e em CI/CD com [GitHub Actions](/pt/github-actions) e [GitLab](/pt/gitlab-ci-cd). Veja [todas as interfaces](/pt/overview#use-claude-code-everywhere).
</Note>

## Passo 1: Instale Claude Code

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. If you see `'irm' is not recognized as an internal or external command`, you're in CMD, not PowerShell. Your prompt shows `PS C:\` when you're in PowerShell and `C:\` without the `PS` when you're in CMD.

    [Git for Windows](https://git-scm.com/downloads/win) is recommended on native Windows so Claude Code can use the Bash tool. If Git for Windows is not installed, Claude Code uses PowerShell as the shell tool instead. WSL setups do not need Git for Windows.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash theme={null}
    brew install --cask claude-code
    ```

    Homebrew offers two casks. `claude-code` tracks the stable release channel, which is typically about a week behind and skips releases with major regressions. `claude-code@latest` tracks the latest channel and receives new versions as soon as they ship.

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` or `brew upgrade claude-code@latest`, depending on which cask you installed, to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

You can also install with [apt, dnf, or apk](/en/setup#install-with-linux-package-managers) on Debian, Fedora, RHEL, and Alpine.

## Passo 2: Faça login em sua conta

Claude Code requer uma conta para usar. Quando você inicia uma sessão interativa com o comando `claude`, você precisará fazer login:

```bash theme={null}
claude
# Você será solicitado a fazer login no primeiro uso
```

```bash theme={null}
/login
# Siga os prompts para fazer login com sua conta
```

Você pode fazer login usando qualquer um destes tipos de conta:

* [Claude Pro, Max, Team ou Enterprise](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=quickstart_login) (recomendado)
* [Claude Console](https://console.anthropic.com/) (acesso à API com créditos pré-pagos). No primeiro login, um workspace "Claude Code" é criado automaticamente no Console para rastreamento centralizado de custos.
* [Amazon Bedrock, Google Vertex AI ou Microsoft Foundry](/pt/third-party-integrations) (provedores de nuvem empresariais)

Depois de fazer login, suas credenciais são armazenadas e você não precisará fazer login novamente. Para trocar de conta mais tarde, use o comando `/login`.

## Passo 3: Inicie sua primeira sessão

Abra seu terminal em qualquer diretório de projeto e inicie Claude Code:

```bash theme={null}
cd /path/to/your/project
claude
```

Você verá a tela de boas-vindas do Claude Code com as informações da sua sessão, conversas recentes e atualizações mais recentes. Digite `/help` para comandos disponíveis ou `/resume` para continuar uma conversa anterior.

<Tip>
  Depois de fazer login (Passo 2), suas credenciais são armazenadas em seu sistema. Saiba mais em [Gerenciamento de Credenciais](/pt/authentication#credential-management).
</Tip>

## Passo 4: Faça sua primeira pergunta

Vamos começar entendendo sua base de código. Tente um destes comandos:

```text theme={null}
what does this project do?
```

Claude analisará seus arquivos e fornecerá um resumo. Você também pode fazer perguntas mais específicas:

```text theme={null}
what technologies does this project use?
```

```text theme={null}
where is the main entry point?
```

```text theme={null}
explain the folder structure
```

Você também pode perguntar ao Claude sobre suas próprias capacidades:

```text theme={null}
what can Claude Code do?
```

```text theme={null}
how do I create custom skills in Claude Code?
```

```text theme={null}
can Claude Code work with Docker?
```

<Note>
  Claude Code lê seus arquivos de projeto conforme necessário. Você não precisa adicionar contexto manualmente.
</Note>

## Passo 5: Faça sua primeira alteração de código

Agora vamos fazer Claude Code fazer alguma codificação real. Tente uma tarefa simples:

```text theme={null}
add a hello world function to the main file
```

Claude Code irá:

1. Encontrar o arquivo apropriado
2. Mostrar as alterações propostas
3. Pedir sua aprovação
4. Fazer a edição

<Note>
  Claude Code sempre pede permissão antes de modificar arquivos. Você pode aprovar alterações individuais ou ativar o modo "Aceitar tudo" para uma sessão.
</Note>

## Passo 6: Use Git com Claude Code

Claude Code torna as operações Git conversacionais:

```text theme={null}
what files have I changed?
```

```text theme={null}
commit my changes with a descriptive message
```

Você também pode solicitar operações Git mais complexas:

```text theme={null}
create a new branch called feature/quickstart
```

```text theme={null}
show me the last 5 commits
```

```text theme={null}
help me resolve merge conflicts
```

## Passo 7: Corrija um bug ou adicione um recurso

Claude é proficiente em depuração e implementação de recursos.

Descreva o que você quer em linguagem natural:

```text theme={null}
add input validation to the user registration form
```

Ou corrija problemas existentes:

```text theme={null}
there's a bug where users can submit empty forms - fix it
```

Claude Code irá:

* Localizar o código relevante
* Entender o contexto
* Implementar uma solução
* Executar testes se disponíveis

## Passo 8: Teste outros fluxos de trabalho comuns

Existem várias maneiras de trabalhar com Claude:

**Refatore código**

```text theme={null}
refactor the authentication module to use async/await instead of callbacks
```

**Escreva testes**

```text theme={null}
write unit tests for the calculator functions
```

**Atualize documentação**

```text theme={null}
update the README with installation instructions
```

**Revisão de código**

```text theme={null}
review my changes and suggest improvements
```

<Tip>
  Fale com Claude como você falaria com um colega prestativo. Descreva o que você quer alcançar, e ele o ajudará a chegar lá.
</Tip>

## Comandos essenciais

Aqui estão os comandos mais importantes para uso diário:

| Comando             | O que faz                                          | Exemplo                             |
| ------------------- | -------------------------------------------------- | ----------------------------------- |
| `claude`            | Iniciar modo interativo                            | `claude`                            |
| `claude "task"`     | Executar uma tarefa única                          | `claude "fix the build error"`      |
| `claude -p "query"` | Executar consulta única, depois sair               | `claude -p "explain this function"` |
| `claude -c`         | Continuar conversa mais recente no diretório atual | `claude -c`                         |
| `claude -r`         | Retomar uma conversa anterior                      | `claude -r`                         |
| `/clear`            | Limpar histórico de conversa                       | `/clear`                            |
| `/help`             | Mostrar comandos disponíveis                       | `/help`                             |
| `exit` ou Ctrl+D    | Sair do Claude Code                                | `exit`                              |

Veja a [referência CLI](/pt/cli-reference) para uma lista completa de comandos.

## Dicas profissionais para iniciantes

Para mais, veja [melhores práticas](/pt/best-practices) e [fluxos de trabalho comuns](/pt/common-workflows).

<AccordionGroup>
  <Accordion title="Seja específico com seus pedidos">
    Em vez de: "corrigir o bug"

    Tente: "corrigir o bug de login onde os usuários veem uma tela em branco após inserir credenciais incorretas"
  </Accordion>

  <Accordion title="Use instruções passo a passo">
    Divida tarefas complexas em etapas:

    ```text theme={null}
    1. criar uma nova tabela de banco de dados para perfis de usuário
    2. criar um endpoint de API para obter e atualizar perfis de usuário
    3. construir uma página da web que permite aos usuários ver e editar suas informações
    ```
  </Accordion>

  <Accordion title="Deixe Claude explorar primeiro">
    Antes de fazer alterações, deixe Claude entender seu código:

    ```text theme={null}
    analisar o esquema do banco de dados
    ```

    ```text theme={null}
    construir um painel mostrando produtos que são devolvidos com mais frequência por nossos clientes do Reino Unido
    ```
  </Accordion>

  <Accordion title="Economize tempo com atalhos">
    * Digite `/` para ver todos os comandos e skills
    * Use Tab para conclusão de comando
    * Pressione ↑ para histórico de comando
    * Pressione `Shift+Tab` para alternar modos de permissão
  </Accordion>
</AccordionGroup>

## Próximos passos

Agora que você aprendeu o básico, explore recursos mais avançados:

<CardGroup cols={2}>
  <Card title="Como Claude Code funciona" icon="microchip" href="/pt/how-claude-code-works">
    Entenda o loop agêntico, ferramentas integradas e como Claude Code interage com seu projeto
  </Card>

  <Card title="Melhores práticas" icon="star" href="/pt/best-practices">
    Obtenha melhores resultados com prompting eficaz e configuração de projeto
  </Card>

  <Card title="Fluxos de trabalho comuns" icon="graduation-cap" href="/pt/common-workflows">
    Guias passo a passo para tarefas comuns
  </Card>

  <Card title="Estenda Claude Code" icon="puzzle-piece" href="/pt/features-overview">
    Personalize com CLAUDE.md, skills, hooks, MCP e muito mais
  </Card>
</CardGroup>

## Obtendo ajuda

* **Em Claude Code**: Digite `/help` ou pergunte "how do I..."
* **Documentação**: Você está aqui! Navegue por outros guias
* **Comunidade**: Junte-se ao nosso [Discord](https://www.anthropic.com/discord) para dicas e suporte
