> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Use Claude Code with Chrome (beta)

> Conecte Claude Code ao seu navegador Chrome para testar aplicativos web, depurar com logs de console, automatizar preenchimento de formulários e extrair dados de páginas web.

Claude Code integra-se com a extensão Claude in Chrome do navegador para oferecer recursos de automação de navegador a partir da CLI ou da [extensão VS Code](/pt/vs-code#automate-browser-tasks-with-chrome). Construa seu código, depois teste e depure no navegador sem trocar de contexto.

Claude abre novas abas para tarefas do navegador e compartilha o estado de login do seu navegador, para que possa acessar qualquer site em que você já esteja conectado. As ações do navegador são executadas em uma janela Chrome visível em tempo real. Quando Claude encontra uma página de login ou CAPTCHA, ele pausa e pede que você a manipule manualmente.

<Note>
  A integração com Chrome está em beta e atualmente funciona apenas com Google Chrome. Ainda não é suportada em Brave, Arc ou outros navegadores baseados em Chromium. WSL (Windows Subsystem for Linux) também não é suportado.
</Note>

## Recursos

Com Chrome conectado, você pode encadear ações do navegador com tarefas de codificação em um único fluxo de trabalho:

* **Depuração ao vivo**: leia erros de console e estado do DOM diretamente, depois corrija o código que os causou
* **Verificação de design**: construa uma interface a partir de um mock do Figma, depois abra-a no navegador para verificar se corresponde
* **Teste de aplicativo web**: teste validação de formulário, verifique regressões visuais ou verifique fluxos de usuário
* **Aplicativos web autenticados**: interaja com Google Docs, Gmail, Notion ou qualquer aplicativo em que você esteja conectado sem conectores de API
* **Extração de dados**: extraia informações estruturadas de páginas web e salve-as localmente
* **Automação de tarefas**: automatize tarefas repetitivas do navegador como entrada de dados, preenchimento de formulários ou fluxos de trabalho em vários sites
* **Gravação de sessão**: grave interações do navegador como GIFs para documentar ou compartilhar o que aconteceu

## Pré-requisitos

Antes de usar Claude Code com Chrome, você precisa de:

* Navegador [Google Chrome](https://www.google.com/chrome/)
* Extensão [Claude in Chrome](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) versão 1.0.36 ou superior
* [Claude Code](/pt/quickstart#step-1-install-claude-code) versão 2.0.73 ou superior
* Um plano Anthropic direto (Pro, Max, Team ou Enterprise)

<Note>
  A integração com Chrome não está disponível através de provedores terceirizados como Amazon Bedrock, Google Cloud Vertex AI ou Microsoft Foundry. Se você acessa Claude exclusivamente através de um provedor terceirizado, você precisa de uma conta claude.ai separada para usar este recurso.
</Note>

## Comece na CLI

<Steps>
  <Step title="Inicie Claude Code com Chrome">
    Inicie Claude Code com a flag `--chrome`:

    ```bash  theme={null}
    claude --chrome
    ```

    Você também pode ativar Chrome dentro de uma sessão existente executando `/chrome`.
  </Step>

  <Step title="Peça a Claude para usar o navegador">
    Este exemplo navega para uma página, interage com ela e relata o que encontra, tudo a partir do seu terminal ou editor:

    ```text  theme={null}
    Go to code.claude.com/docs, click on the search box,
    type "hooks", and tell me what results appear
    ```
  </Step>
</Steps>

Execute `/chrome` a qualquer momento para verificar o status da conexão, gerenciar permissões ou reconectar a extensão.

Para VS Code, consulte [automação de navegador em VS Code](/pt/vs-code#automate-browser-tasks-with-chrome).

### Ativar Chrome por padrão

Para evitar passar `--chrome` em cada sessão, execute `/chrome` e selecione "Enabled by default".

Na [extensão VS Code](/pt/vs-code#automate-browser-tasks-with-chrome), Chrome está disponível sempre que a extensão Chrome está instalada. Nenhuma flag adicional é necessária.

<Note>
  Ativar Chrome por padrão na CLI aumenta o uso de contexto, pois as ferramentas do navegador estão sempre carregadas. Se você notar aumento no consumo de contexto, desative esta configuração e use `--chrome` apenas quando necessário.
</Note>

### Gerenciar permissões de site

As permissões no nível do site são herdadas da extensão Chrome. Gerencie permissões nas configurações da extensão Chrome para controlar quais sites Claude pode navegar, clicar e digitar.

## Fluxos de trabalho de exemplo

Estes exemplos mostram maneiras comuns de combinar ações do navegador com tarefas de codificação. Execute `/mcp` e selecione `claude-in-chrome` para ver a lista completa de ferramentas de navegador disponíveis.

### Teste um aplicativo web local

Ao desenvolver um aplicativo web, peça a Claude para verificar se suas alterações funcionam corretamente:

```text  theme={null}
I just updated the login form validation. Can you open localhost:3000,
try submitting the form with invalid data, and check if the error
messages appear correctly?
```

Claude navega para seu servidor local, interage com o formulário e relata o que observa.

### Depurar com logs de console

Claude pode ler a saída do console para ajudar a diagnosticar problemas. Diga a Claude quais padrões procurar em vez de pedir toda a saída do console, pois os logs podem ser verbosos:

```text  theme={null}
Open the dashboard page and check the console for any errors when
the page loads.
```

Claude lê as mensagens do console e pode filtrar padrões específicos ou tipos de erro.

### Automatizar preenchimento de formulários

Acelere tarefas repetitivas de entrada de dados:

```text  theme={null}
I have a spreadsheet of customer contacts in contacts.csv. For each row,
go to the CRM at crm.example.com, click "Add Contact", and fill in the
name, email, and phone fields.
```

Claude lê seu arquivo local, navega pela interface web e insere os dados para cada registro.

### Rascunhar conteúdo no Google Docs

Use Claude para escrever diretamente em seus documentos sem configuração de API:

```text  theme={null}
Draft a project update based on the recent commits and add it to my
Google Doc at docs.google.com/document/d/abc123
```

Claude abre o documento, clica no editor e digita o conteúdo. Isso funciona com qualquer aplicativo web em que você esteja conectado: Gmail, Notion, Sheets e muito mais.

### Extrair dados de páginas web

Extraia informações estruturadas de sites:

```text  theme={null}
Go to the product listings page and extract the name, price, and
availability for each item. Save the results as a CSV file.
```

Claude navega para a página, lê o conteúdo e compila os dados em um formato estruturado.

### Executar fluxos de trabalho em vários sites

Coordene tarefas em vários sites:

```text  theme={null}
Check my calendar for meetings tomorrow, then for each meeting with
an external attendee, look up their company website and add a note
about what they do.
```

Claude trabalha em abas para reunir informações e concluir o fluxo de trabalho.

### Gravar um GIF de demonstração

Crie gravações compartilháveis de interações do navegador:

```text  theme={null}
Record a GIF showing how to complete the checkout flow, from adding
an item to the cart through to the confirmation page.
```

Claude grava a sequência de interação e a salva como um arquivo GIF.

## Troubleshooting

### Extensão não detectada

Se Claude Code mostrar "Chrome extension not detected":

1. Verifique se a extensão Chrome está instalada e ativada em `chrome://extensions`
2. Verifique se Claude Code está atualizado executando `claude --version`
3. Verifique se Chrome está em execução
4. Execute `/chrome` e selecione "Reconnect extension" para restabelecer a conexão
5. Se o problema persistir, reinicie Claude Code e Chrome

Na primeira vez que você ativa a integração com Chrome, Claude Code instala um arquivo de configuração do host de mensagens nativas. Chrome lê este arquivo na inicialização, portanto, se a extensão não for detectada na sua primeira tentativa, reinicie Chrome para pegar a nova configuração.

Se a conexão ainda falhar, verifique se o arquivo de configuração do host existe em:

* **macOS**: `~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Linux**: `~/.config/google-chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Windows**: verifique `HKCU\Software\Google\Chrome\NativeMessagingHosts\` no Registro do Windows

### Navegador não respondendo

Se os comandos do navegador de Claude pararem de funcionar:

1. Verifique se uma caixa de diálogo modal (alerta, confirmação, prompt) está bloqueando a página. Caixas de diálogo JavaScript bloqueiam eventos do navegador e impedem que Claude receba comandos. Feche a caixa de diálogo manualmente e diga a Claude para continuar.
2. Peça a Claude para criar uma nova aba e tentar novamente
3. Reinicie a extensão Chrome desativando-a e reativando-a em `chrome://extensions`

### Conexão cai durante sessões longas

O service worker da extensão Chrome pode ficar inativo durante sessões estendidas, o que quebra a conexão. Se as ferramentas do navegador pararem de funcionar após um período de inatividade, execute `/chrome` e selecione "Reconnect extension".

### Problemas específicos do Windows

No Windows, você pode encontrar:

* **Conflitos de named pipe (EADDRINUSE)**: se outro processo estiver usando o mesmo named pipe, reinicie Claude Code. Feche qualquer outra sessão de Claude Code que possa estar usando Chrome.
* **Erros de host de mensagens nativas**: se o host de mensagens nativas falhar na inicialização, tente reinstalar Claude Code para regenerar a configuração do host.

### Mensagens de erro comuns

Estes são os erros mais frequentemente encontrados e como resolvê-los:

| Erro                                 | Causa                                                        | Solução                                                                 |
| ------------------------------------ | ------------------------------------------------------------ | ----------------------------------------------------------------------- |
| "Browser extension is not connected" | O host de mensagens nativas não consegue alcançar a extensão | Reinicie Chrome e Claude Code, depois execute `/chrome` para reconectar |
| "Extension not detected"             | A extensão Chrome não está instalada ou está desativada      | Instale ou ative a extensão em `chrome://extensions`                    |
| "No tab available"                   | Claude tentou agir antes de uma aba estar pronta             | Peça a Claude para criar uma nova aba e tentar novamente                |
| "Receiving end does not exist"       | O service worker da extensão ficou inativo                   | Execute `/chrome` e selecione "Reconnect extension"                     |

## Veja também

* [Use Claude Code in VS Code](/pt/vs-code#automate-browser-tasks-with-chrome): automação de navegador na extensão VS Code
* [Referência CLI](/pt/cli-reference): flags de linha de comando incluindo `--chrome`
* [Fluxos de trabalho comuns](/pt/common-workflows): mais maneiras de usar Claude Code
* [Dados e privacidade](/pt/data-usage): como Claude Code manipula seus dados
* [Getting started with Claude in Chrome](https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome): documentação completa para a extensão Chrome, incluindo atalhos, agendamento e permissões
