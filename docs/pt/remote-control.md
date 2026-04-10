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

# Continue sessões locais de qualquer dispositivo com Remote Control

> Continue uma sessão local do Claude Code do seu telefone, tablet ou qualquer navegador usando Remote Control. Funciona com claude.ai/code e o aplicativo Claude para dispositivos móveis.

<Note>
  Remote Control está disponível em todos os planos. Em Team e Enterprise, ele fica desativado por padrão até que um administrador ative o toggle Remote Control nas [configurações de administrador do Claude Code](https://claude.ai/admin-settings/claude-code).
</Note>

Remote Control conecta [claude.ai/code](https://claude.ai/code) ou o aplicativo Claude para [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) e [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) a uma sessão do Claude Code em execução na sua máquina. Inicie uma tarefa na sua mesa, depois continue a partir do seu telefone no sofá ou de um navegador em outro computador.

Quando você inicia uma sessão de Remote Control na sua máquina, Claude continua executando localmente o tempo todo, portanto nada se move para a nuvem. Com Remote Control você pode:

* **Usar seu ambiente local completo remotamente**: seu sistema de arquivos, [MCP servers](/pt/mcp), ferramentas e configuração do projeto permanecem disponíveis
* **Trabalhar em ambas as superfícies ao mesmo tempo**: a conversa permanece sincronizada em todos os dispositivos conectados, para que você possa enviar mensagens do seu terminal, navegador e telefone de forma intercambiável
* **Sobreviver a interrupções**: se seu laptop dormir ou sua rede cair, a sessão se reconecta automaticamente quando sua máquina voltar a ficar online

Diferentemente do [Claude Code na web](/pt/claude-code-on-the-web), que é executado em infraestrutura em nuvem, as sessões de Remote Control são executadas diretamente na sua máquina e interagem com seu sistema de arquivos local. As interfaces web e móvel são apenas uma janela para essa sessão local.

<Note>
  Remote Control requer Claude Code v2.1.51 ou posterior. Verifique sua versão com `claude --version`.
</Note>

Esta página aborda a configuração, como iniciar e conectar a sessões, e como Remote Control se compara ao Claude Code na web.

## Requisitos

Antes de usar Remote Control, confirme que seu ambiente atende a estas condições:

* **Assinatura**: disponível nos planos Pro, Max, Team e Enterprise. Chaves de API não são suportadas. Em Team e Enterprise, um administrador deve primeiro ativar o toggle Remote Control nas [configurações de administrador do Claude Code](https://claude.ai/admin-settings/claude-code).
* **Autenticação**: execute `claude` e use `/login` para fazer login através de claude.ai se você ainda não fez isso.
* **Confiança do workspace**: execute `claude` no diretório do seu projeto pelo menos uma vez para aceitar o diálogo de confiança do workspace.

## Inicie uma sessão de Remote Control

Você pode iniciar um servidor dedicado de Remote Control, iniciar uma sessão interativa com Remote Control ativado ou conectar a uma sessão que já está em execução.

<Tabs>
  <Tab title="Modo servidor">
    Navegue até o diretório do seu projeto e execute:

    ```bash  theme={null}
    claude remote-control
    ```

    O processo continua em execução no seu terminal em modo servidor, aguardando conexões remotas. Ele exibe uma URL de sessão que você pode usar para [conectar de outro dispositivo](#connect-from-another-device), e você pode pressionar a barra de espaço para mostrar um código QR para acesso rápido do seu telefone. Enquanto uma sessão remota está ativa, o terminal mostra o status da conexão e a atividade da ferramenta.

    Sinalizadores disponíveis:

    | Sinalizador                  | Descrição                                                                                                                                                                                                                                                                                                                                                                                                                                |
    | ---------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
    | `--name "My Project"`        | Define um título de sessão personalizado visível na lista de sessões em claude.ai/code.                                                                                                                                                                                                                                                                                                                                                  |
    | `--spawn <mode>`             | Como as sessões simultâneas são criadas. Pressione `w` em tempo de execução para alternar.<br />• `same-dir` (padrão): todas as sessões compartilham o diretório de trabalho atual, portanto podem entrar em conflito se editarem os mesmos arquivos.<br />• `worktree`: cada sessão sob demanda obtém seu próprio [git worktree](/pt/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees). Requer um repositório git. |
    | `--capacity <N>`             | Número máximo de sessões simultâneas. O padrão é 32.                                                                                                                                                                                                                                                                                                                                                                                     |
    | `--verbose`                  | Mostra logs detalhados de conexão e sessão.                                                                                                                                                                                                                                                                                                                                                                                              |
    | `--sandbox` / `--no-sandbox` | Ativa ou desativa [sandboxing](/pt/sandboxing) para isolamento de sistema de arquivos e rede. Desativado por padrão.                                                                                                                                                                                                                                                                                                                     |
  </Tab>

  <Tab title="Sessão interativa">
    Para iniciar uma sessão normal interativa do Claude Code com Remote Control ativado, use a flag `--remote-control` (ou `--rc`):

    ```bash  theme={null}
    claude --remote-control
    ```

    Opcionalmente, passe um nome para a sessão:

    ```bash  theme={null}
    claude --remote-control "My Project"
    ```

    Isso oferece uma sessão interativa completa no seu terminal que você também pode controlar a partir de claude.ai ou do aplicativo Claude. Diferentemente de `claude remote-control` (modo servidor), você pode digitar mensagens localmente enquanto a sessão também está disponível remotamente.
  </Tab>

  <Tab title="De uma sessão existente">
    Se você já está em uma sessão do Claude Code e deseja continuá-la remotamente, use o comando `/remote-control` (ou `/rc`):

    ```text  theme={null}
    /remote-control
    ```

    Passe um nome como argumento para definir um título de sessão personalizado:

    ```text  theme={null}
    /remote-control My Project
    ```

    Isso inicia uma sessão de Remote Control que carrega seu histórico de conversa atual e exibe uma URL de sessão e código QR que você pode usar para [conectar de outro dispositivo](#connect-from-another-device). As flags `--verbose`, `--sandbox` e `--no-sandbox` não estão disponíveis com este comando.
  </Tab>
</Tabs>

### Conectar de outro dispositivo

Depois que uma sessão de Remote Control está ativa, você tem algumas maneiras de conectar de outro dispositivo:

* **Abra a URL da sessão** em qualquer navegador para ir diretamente para a sessão em [claude.ai/code](https://claude.ai/code). Tanto `claude remote-control` quanto `/remote-control` exibem esta URL no terminal.
* **Escaneie o código QR** mostrado ao lado da URL da sessão para abri-lo diretamente no aplicativo Claude. Com `claude remote-control`, pressione a barra de espaço para alternar a exibição do código QR.
* **Abra [claude.ai/code](https://claude.ai/code) ou o aplicativo Claude** e encontre a sessão pelo nome na lista de sessões. As sessões de Remote Control mostram um ícone de computador com um ponto de status verde quando online.

O título da sessão remota é escolhido nesta ordem:

1. O nome que você passou para `--name`, `--remote-control` ou `/remote-control`
2. O título que você definiu com `/rename`
3. A última mensagem significativa no histórico de conversa existente
4. Seu primeiro prompt assim que você enviar um

Se o ambiente já tiver uma sessão ativa, você será perguntado se deseja continuá-la ou iniciar uma nova.

Se você ainda não tem o aplicativo Claude, use o comando `/mobile` dentro do Claude Code para exibir um código QR de download para [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) ou [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude).

### Ativar Remote Control para todas as sessões

Por padrão, Remote Control só é ativado quando você executa explicitamente `claude remote-control`, `claude --remote-control` ou `/remote-control`. Para ativá-lo automaticamente para cada sessão interativa, execute `/config` dentro do Claude Code e defina **Enable Remote Control for all sessions** como `true`. Defina-o de volta para `false` para desativar.

Com essa configuração ativada, cada processo interativo do Claude Code registra uma sessão remota. Se você executar várias instâncias, cada uma obtém seu próprio ambiente e sessão. Para executar várias sessões simultâneas a partir de um único processo, use o modo servidor com `--spawn` em vez disso.

## Conexão e segurança

Sua sessão local do Claude Code faz apenas solicitações HTTPS de saída e nunca abre portas de entrada na sua máquina. Quando você inicia Remote Control, ele se registra na API Anthropic e faz polling para trabalho. Quando você conecta de outro dispositivo, o servidor roteia mensagens entre o cliente web ou móvel e sua sessão local através de uma conexão de streaming.

Todo o tráfego viaja através da API Anthropic sobre TLS, o mesmo transporte de segurança que qualquer sessão do Claude Code. A conexão usa múltiplas credenciais de curta duração, cada uma com escopo para um único propósito e expirando independentemente.

## Remote Control vs Claude Code na web

Remote Control e [Claude Code na web](/pt/claude-code-on-the-web) usam a interface claude.ai/code. A diferença fundamental é onde a sessão é executada: Remote Control é executado na sua máquina, portanto seus MCP servers locais, ferramentas e configuração do projeto permanecem disponíveis. Claude Code na web é executado em infraestrutura em nuvem gerenciada pela Anthropic.

Use Remote Control quando você está no meio do trabalho local e deseja continuar de outro dispositivo. Use Claude Code na web quando você deseja iniciar uma tarefa sem nenhuma configuração local, trabalhar em um repositório que você não tem clonado ou executar várias tarefas em paralelo.

## Limitações

* **Uma sessão remota por processo interativo**: fora do modo servidor, cada instância do Claude Code suporta uma sessão remota por vez. Use o modo servidor com `--spawn` para executar várias sessões simultâneas a partir de um único processo.
* **Terminal deve permanecer aberto**: Remote Control é executado como um processo local. Se você fechar o terminal ou parar o processo `claude`, a sessão termina. Execute `claude remote-control` novamente para iniciar uma nova.
* **Interrupção de rede estendida**: se sua máquina estiver ligada mas não conseguir alcançar a rede por mais de aproximadamente 10 minutos, a sessão expira e o processo sai. Execute `claude remote-control` novamente para iniciar uma nova sessão.

## Solução de problemas

### "Remote Control is not yet enabled for your account"

A verificação de elegibilidade pode falhar com certas variáveis de ambiente presentes:

* `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` ou `DISABLE_TELEMETRY`: desative-as e tente novamente.
* `CLAUDE_CODE_USE_BEDROCK`, `CLAUDE_CODE_USE_VERTEX` ou `CLAUDE_CODE_USE_FOUNDRY`: Remote Control requer autenticação claude.ai e não funciona com provedores de terceiros.

Se nenhuma delas estiver definida, execute `/logout` e depois `/login` para atualizar.

### "Remote Control is disabled by your organization's policy"

Este erro tem três causas distintas. Execute `/status` primeiro para ver qual método de login e assinatura você está usando.

* **Você está autenticado com uma chave de API ou conta Console**: Remote Control requer OAuth claude.ai. Execute `/login` e escolha a opção claude.ai. Se `ANTHROPIC_API_KEY` estiver definida em seu ambiente, desative-a.
* **Seu administrador de Team ou Enterprise não ativou**: Remote Control fica desativado por padrão nesses planos. Um administrador pode ativá-lo em [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) ativando o toggle **Remote Control**. Esta é uma configuração de organização no lado do servidor, não uma chave de [configurações gerenciadas](/pt/permissions#managed-only-settings).
* **O toggle do administrador está acinzentado**: sua organização tem uma configuração de retenção de dados ou conformidade que é incompatível com Remote Control. Isso não pode ser alterado no painel de administração. Entre em contato com o suporte da Anthropic para discutir opções.

### "Remote credentials fetch failed"

Claude Code não conseguiu obter uma credencial de curta duração da API Anthropic para estabelecer a conexão. Execute novamente com `--verbose` para ver o erro completo:

```bash  theme={null}
claude remote-control --verbose
```

Causas comuns:

* Não conectado: execute `claude` e use `/login` para autenticar com sua conta claude.ai. A autenticação por chave de API não é suportada para Remote Control.
* Problema de rede ou proxy: um firewall ou proxy pode estar bloqueando a solicitação HTTPS de saída. Remote Control requer acesso à API Anthropic na porta 443.
* Falha na criação de sessão: se você também vir `Session creation failed — see debug log`, a falha aconteceu anteriormente na configuração. Verifique se sua assinatura está ativa.

## Escolha a abordagem correta

Claude Code offers several ways to work when you're not at your terminal. They differ in what triggers the work, where Claude runs, and how much you need to set up.

|                                                | Trigger                                                                                        | Claude runs on                                                                                          | Setup                                                                                                                                | Best for                                                      |
| :--------------------------------------------- | :--------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------ | :----------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------ |
| [Dispatch](/en/desktop#sessions-from-dispatch) | Message a task from the Claude mobile app                                                      | Your machine (Desktop)                                                                                  | [Pair the mobile app with Desktop](https://support.claude.com/en/articles/13947068)                                                  | Delegating work while you're away, minimal setup              |
| [Remote Control](/en/remote-control)           | Drive a running session from [claude.ai/code](https://claude.ai/code) or the Claude mobile app | Your machine (CLI or VS Code)                                                                           | Run `claude remote-control`                                                                                                          | Steering in-progress work from another device                 |
| [Channels](/en/channels)                       | Push events from a chat app like Telegram or Discord, or your own server                       | Your machine (CLI)                                                                                      | [Install a channel plugin](/en/channels#quickstart) or [build your own](/en/channels-reference)                                      | Reacting to external events like CI failures or chat messages |
| [Slack](/en/slack)                             | Mention `@Claude` in a team channel                                                            | Anthropic cloud                                                                                         | [Install the Slack app](/en/slack#setting-up-claude-code-in-slack) with [Claude Code on the web](/en/claude-code-on-the-web) enabled | PRs and reviews from team chat                                |
| [Scheduled tasks](/en/scheduled-tasks)         | Set a schedule                                                                                 | [CLI](/en/scheduled-tasks), [Desktop](/en/desktop-scheduled-tasks), or [cloud](/en/web-scheduled-tasks) | Pick a frequency                                                                                                                     | Recurring automation like daily reviews                       |

## Recursos relacionados

* [Claude Code na web](/pt/claude-code-on-the-web): execute sessões em ambientes em nuvem gerenciados pela Anthropic em vez de na sua máquina
* [Channels](/pt/channels): encaminhe Telegram ou Discord para uma sessão para que Claude reaja a mensagens enquanto você está ausente
* [Dispatch](/pt/desktop#sessions-from-dispatch): envie uma mensagem com uma tarefa do seu telefone e ela pode gerar uma sessão Desktop para lidar com isso
* [Autenticação](/pt/authentication): configure `/login` e gerencie credenciais para claude.ai
* [Referência de CLI](/pt/cli-reference): lista completa de flags e comandos incluindo `claude remote-control`
* [Segurança](/pt/security): como as sessões de Remote Control se encaixam no modelo de segurança do Claude Code
* [Uso de dados](/pt/data-usage): quais dados fluem através da API Anthropic durante sessões locais e remotas
