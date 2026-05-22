> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Conectar Claude Code a ferramentas via MCP

> Aprenda como conectar Claude Code às suas ferramentas com o Model Context Protocol.

Claude Code pode se conectar a centenas de ferramentas e fontes de dados externas através do [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), um padrão de código aberto para integrações de IA com ferramentas. Os servidores MCP dão ao Claude Code acesso às suas ferramentas, bancos de dados e APIs.

Conecte um servidor quando você se encontrar copiando dados para o chat de outra ferramenta, como um rastreador de problemas ou um painel de monitoramento. Uma vez conectado, Claude pode ler e agir nesse sistema diretamente em vez de trabalhar com o que você cola.

## O que você pode fazer com MCP

Com servidores MCP conectados, você pode pedir ao Claude Code para:

* **Implementar recursos de rastreadores de problemas**: "Adicione o recurso descrito no problema JIRA ENG-4521 e crie um PR no GitHub."
* **Analisar dados de monitoramento**: "Verifique Sentry e Statsig para verificar o uso do recurso descrito em ENG-4521."
* **Consultar bancos de dados**: "Encontre emails de 10 usuários aleatórios que usaram o recurso ENG-4521, com base no nosso banco de dados PostgreSQL."
* **Integrar designs**: "Atualize nosso modelo de email padrão com base nos novos designs do Figma que foram postados no Slack"
* **Automatizar fluxos de trabalho**: "Crie rascunhos do Gmail convidando esses 10 usuários para uma sessão de feedback sobre o novo recurso."
* **Reagir a eventos externos**: Um servidor MCP também pode atuar como um [canal](/pt/channels) que envia mensagens para sua sessão, para que Claude reaja a mensagens do Telegram, chats do Discord ou eventos de webhook enquanto você está ausente.

## Encontre e crie servidores MCP

Navegue por conectores revisados no [Diretório Anthropic](https://claude.ai/directory). Os conectores do Diretório usam a mesma infraestrutura MCP que Claude Code, então você pode adicionar qualquer servidor remoto listado lá com `claude mcp add`.

<Warning>
  Verifique se você confia em cada servidor antes de conectá-lo. Servidores que buscam conteúdo externo podem expô-lo ao [risco de injeção de prompt](/pt/security#protect-against-prompt-injection).
</Warning>

Para criar seu próprio servidor, consulte o [guia do servidor MCP](https://modelcontextprotocol.io/docs/develop/build-server) para os fundamentos do protocolo e a [documentação de construção de conectores Claude](https://claude.com/docs/connectors/building) para autenticação, testes e envio ao Diretório.

Você também pode fazer com que Claude crie um servidor para você com o plugin oficial [`mcp-server-dev`](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/mcp-server-dev).

<Steps>
  <Step title="Instale o plugin">
    Em uma sessão Claude Code, execute:

    ```
    /plugin install mcp-server-dev@claude-plugins-official
    ```

    Em seguida, execute `/reload-plugins` para ativá-lo na sessão atual.
  </Step>

  <Step title="Execute a skill de construção">
    ```
    /mcp-server-dev:build-mcp-server
    ```

    Claude pergunta sobre seu caso de uso e cria um servidor HTTP remoto ou servidor stdio local.
  </Step>
</Steps>

## Instalando servidores MCP

Os servidores MCP podem ser configurados de três maneiras diferentes dependendo de suas necessidades:

### Opção 1: Adicionar um servidor HTTP remoto

Servidores HTTP são a opção recomendada para conectar a servidores MCP remotos. Este é o transporte mais amplamente suportado para serviços baseados em nuvem.

```bash theme={null}
# Sintaxe básica
claude mcp add --transport http <name> <url>

# Exemplo real: Conectar ao Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Exemplo com token Bearer
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

Ao configurar servidores MCP via JSON em `.mcp.json`, `~/.claude.json`, ou `claude mcp add-json`, o campo `type` aceita `streamable-http` como um alias para `http`. A especificação MCP usa o nome `streamable-http` para este transporte, portanto as configurações copiadas da documentação do servidor funcionam sem modificação.

### Opção 2: Adicionar um servidor SSE remoto

<Warning>
  O transporte SSE (Server-Sent Events) está descontinuado. Use servidores HTTP em vez disso, quando disponível.
</Warning>

```bash theme={null}
# Sintaxe básica
claude mcp add --transport sse <name> <url>

# Exemplo real: Conectar ao Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Exemplo com cabeçalho de autenticação
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

### Opção 3: Adicionar um servidor stdio local

Servidores Stdio são executados como processos locais em sua máquina. Eles são ideais para ferramentas que precisam de acesso direto ao sistema ou scripts personalizados.

Claude Code define `CLAUDE_PROJECT_DIR` no ambiente do servidor gerado para a raiz do projeto, para que seu servidor possa resolver caminhos relativos ao projeto sem depender do diretório de trabalho. Este é o mesmo diretório que hooks recebem em sua variável `CLAUDE_PROJECT_DIR`. Leia-o de dentro do seu processo de servidor, por exemplo `process.env.CLAUDE_PROJECT_DIR` em Node ou `os.environ["CLAUDE_PROJECT_DIR"]` em Python. Seu servidor também pode chamar a solicitação MCP `roots/list`, que retorna o diretório do qual Claude Code foi iniciado.

Esta variável é definida no ambiente do servidor, não no ambiente do próprio Claude Code, portanto referenciá-la via expansão `${VAR}` em um `.mcp.json` com escopo de projeto ou usuário `command` ou `args` requer um padrão como `${CLAUDE_PROJECT_DIR:-.}`. As configurações MCP fornecidas por plugins substituem `${CLAUDE_PROJECT_DIR}` diretamente e não precisam do padrão.

```bash theme={null}
# Sintaxe básica
claude mcp add [options] <name> -- <command> [args...]

# Exemplo real: Adicionar servidor Airtable
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server
```

<Note>
  **Importante: Ordenação de opções**

  Todas as opções (`--transport`, `--env`, `--scope`, `--header`) devem vir **antes** do nome do servidor. O `--` (travessão duplo) então separa o nome do servidor do comando e argumentos que são passados para o servidor MCP.

  Por exemplo:

  * `claude mcp add --transport stdio myserver -- npx server` → executa `npx server`
  * `claude mcp add --transport stdio --env KEY=value myserver -- python server.py --port 8080` → executa `python server.py --port 8080` com `KEY=value` no ambiente

  Isso evita conflitos entre as flags do Claude e as flags do servidor.
</Note>

### Gerenciando seus servidores

Uma vez configurados, você pode gerenciar seus servidores MCP com estes comandos:

```bash theme={null}
# Listar todos os servidores configurados
claude mcp list

# Obter detalhes para um servidor específico
claude mcp get github

# Remover um servidor
claude mcp remove github

# (dentro do Claude Code) Verificar status do servidor
/mcp
```

O painel `/mcp` mostra a contagem de ferramentas ao lado de cada servidor conectado e sinaliza servidores que anunciam a capacidade de ferramentas, mas não expõem nenhuma ferramenta.

Se sua solicitação precisar de ferramentas de um servidor que ainda está se conectando em segundo plano, Claude aguarda esse servidor antes de continuar. Com [pesquisa de ferramentas](#scale-with-mcp-tool-search) habilitada, que é o padrão, a espera acontece dentro da chamada `ToolSearch`. Em configurações sem pesquisa de ferramentas, como Vertex AI, um `ANTHROPIC_BASE_URL` personalizado, ou `ENABLE_TOOL_SEARCH=false`, Claude usa a ferramenta `WaitForMcpServers` em vez disso.

O nome do servidor `workspace` é reservado para uso interno. Se sua configuração define um servidor com esse nome, Claude Code o ignora no tempo de carregamento e mostra um aviso pedindo que você o renomeie.

### Atualizações dinâmicas de ferramentas

Claude Code suporta notificações MCP `list_changed`, permitindo que servidores MCP atualizem dinamicamente suas ferramentas, prompts e recursos disponíveis sem exigir que você se desconecte e reconecte. Quando um servidor MCP envia uma notificação `list_changed`, Claude Code atualiza automaticamente as capacidades disponíveis desse servidor.

### Reconexão automática

Se um servidor HTTP ou SSE se desconectar durante a sessão, Claude Code se reconecta automaticamente com backoff exponencial: até cinco tentativas, começando com um atraso de um segundo e dobrando a cada vez. O servidor aparece como pendente em `/mcp` enquanto a reconexão está em andamento. Após cinco tentativas falhadas, o servidor é marcado como falho e você pode tentar novamente manualmente de `/mcp`. Servidores Stdio são processos locais e não são reconectados automaticamente.

O mesmo backoff se aplica quando um servidor HTTP ou SSE falha sua conexão inicial na inicialização. A partir da v2.1.121, Claude Code tenta novamente a conexão inicial até três vezes em erros transitórios, como uma resposta 5xx, uma conexão recusada ou um tempo limite, e então marca o servidor como falho se ainda não conseguir se conectar. Erros de autenticação e não encontrado não são retentados porque exigem uma mudança de configuração para serem resolvidos.

### Enviar mensagens com canais

Um servidor MCP também pode enviar mensagens diretamente para sua sessão para que Claude possa reagir a eventos externos como resultados de CI, alertas de monitoramento ou mensagens de chat. Para habilitar isso, seu servidor declara a capacidade `claude/channel` e você a ativa com a flag `--channels` na inicialização. Veja [Canais](/pt/channels) para usar um canal oficialmente suportado, ou [Referência de canais](/pt/channels-reference) para construir o seu próprio.

<Tip>
  Dicas:

  * Use a flag `--scope` para especificar onde a configuração é armazenada:
    * `local` (padrão): Disponível apenas para você no projeto atual (era chamado de `project` em versões mais antigas)
    * `project`: Compartilhado com todos no projeto via arquivo `.mcp.json`
    * `user`: Disponível para você em todos os projetos (era chamado de `global` em versões mais antigas)
  * Defina variáveis de ambiente com flags `--env` (por exemplo, `--env KEY=value`)
  * Configure o tempo limite de inicialização do servidor MCP usando a variável de ambiente MCP\_TIMEOUT (por exemplo, `MCP_TIMEOUT=10000 claude` define um tempo limite de 10 segundos)
  * Servidores Stdio são processos locais e não são reconectados automaticamente.
  * Claude Code exibirá um aviso quando a saída da ferramenta MCP exceder 10.000 tokens. Para aumentar este limite, defina a variável de ambiente `MAX_MCP_OUTPUT_TOKENS` (por exemplo, `MAX_MCP_OUTPUT_TOKENS=50000`)
  * Use `/mcp` para autenticar com servidores remotos que exigem autenticação OAuth 2.0
</Tip>

O `timeout` por servidor é um limite de tempo de parede rígido por chamada de ferramenta, e notificações de progresso do servidor não o estendem. Valores abaixo de 1000 são arredondados para um segundo. Para servidores HTTP e SSE, o orçamento de primeiro byte por solicitação de busca tem um mínimo de 60 segundos independentemente deste valor, portanto apenas o watchdog de chamada de ferramenta honra valores menores.

### Servidores MCP fornecidos por plugins

[Plugins](/pt/plugins) podem agrupar servidores MCP, fornecendo automaticamente ferramentas e integrações quando o plugin está habilitado. Os servidores MCP de plugins funcionam de forma idêntica aos servidores configurados pelo usuário.

**Como funcionam os servidores MCP de plugins**:

* Plugins definem servidores MCP em `.mcp.json` na raiz do plugin ou inline em `plugin.json`
* Quando um plugin está habilitado, seus servidores MCP iniciam automaticamente
* As ferramentas MCP do plugin aparecem junto com as ferramentas MCP configuradas manualmente
* Os servidores de plugins são gerenciados através da instalação de plugins (não comandos `/mcp`)

**Exemplo de configuração MCP de plugin**:

Em `.mcp.json` na raiz do plugin:

```json theme={null}
{
  "mcpServers": {
    "database-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_URL": "${DB_URL}"
      }
    }
  }
}
```

Ou inline em `plugin.json`:

```json theme={null}
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

**Recursos de MCP de plugin**:

* **Ciclo de vida automático**: Na inicialização da sessão, os servidores para plugins habilitados se conectam automaticamente. Se você habilitar ou desabilitar um plugin durante uma sessão, execute `/reload-plugins` para conectar ou desconectar seus servidores MCP
* **Variáveis de ambiente**: Use `${CLAUDE_PLUGIN_ROOT}` para arquivos agrupados do plugin, `${CLAUDE_PLUGIN_DATA}` para [estado persistente](/pt/plugins-reference#persistent-data-directory) que sobrevive a atualizações de plugins, e `${CLAUDE_PROJECT_DIR}` para a raiz do projeto estável
* **Acesso a variáveis de ambiente do usuário**: Acesso às mesmas variáveis de ambiente que servidores configurados manualmente
* **Múltiplos tipos de transporte**: Suporte para transportes stdio, SSE e HTTP (o suporte de transporte pode variar por servidor)

**Visualizando servidores MCP de plugins**:

```bash theme={null}
# Dentro do Claude Code, veja todos os servidores MCP incluindo os de plugins
/mcp
```

Os servidores de plugins aparecem na lista com indicadores mostrando que vêm de plugins.

**Benefícios dos servidores MCP de plugins**:

* **Distribuição agrupada**: Ferramentas e servidores empacotados juntos
* **Configuração automática**: Nenhuma configuração MCP manual necessária
* **Consistência da equipe**: Todos obtêm as mesmas ferramentas quando o plugin está instalado

Veja a [referência de componentes de plugins](/pt/plugins-reference#mcp-servers) para detalhes sobre como agrupar servidores MCP com plugins.

## Escopos de instalação de MCP

Os servidores MCP podem ser configurados em três escopos. O escopo que você escolhe controla em quais projetos o servidor é carregado e se a configuração é compartilhada com sua equipe. Os administradores também podem implantar servidores no nível empresarial via [configuração gerenciada](#managed-mcp-configuration).

| Escopo                    | Carrega em             | Compartilhado com equipe    | Armazenado em                  |
| ------------------------- | ---------------------- | --------------------------- | ------------------------------ |
| [Local](#local-scope)     | Apenas projeto atual   | Não                         | `~/.claude.json`               |
| [Projeto](#project-scope) | Apenas projeto atual   | Sim, via controle de versão | `.mcp.json` na raiz do projeto |
| [Usuário](#user-scope)    | Todos os seus projetos | Não                         | `~/.claude.json`               |

### Escopo local

O escopo local é o padrão. Um servidor com escopo local carrega apenas no projeto onde você o adicionou e permanece privado para você. Claude Code o armazena em `~/.claude.json` sob o caminho desse projeto, então o mesmo servidor não aparecerá em seus outros projetos. Use o escopo local para servidores de desenvolvimento pessoal, configurações experimentais ou servidores com credenciais que você não deseja no controle de versão.

<Note>
  O termo "escopo local" para servidores MCP difere das configurações locais gerais. Os servidores MCP com escopo local são armazenados em `~/.claude.json` (seu diretório inicial), enquanto as configurações locais gerais usam `.claude/settings.local.json` (no diretório do projeto). Veja [Configurações](/pt/settings#settings-files) para detalhes sobre localizações de arquivos de configuração.
</Note>

```bash theme={null}
# Adicionar um servidor com escopo local (padrão)
claude mcp add --transport http stripe https://mcp.stripe.com

# Especificar explicitamente escopo local
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

O comando escreve o servidor na entrada do seu projeto atual dentro de `~/.claude.json`. O exemplo abaixo mostra o resultado quando você o executa de `/path/to/your/project`:

```json theme={null}
{
  "projects": {
    "/path/to/your/project": {
      "mcpServers": {
        "stripe": {
          "type": "http",
          "url": "https://mcp.stripe.com"
        }
      }
    }
  }
}
```

### Escopo de projeto

Servidores com escopo de projeto permitem colaboração em equipe armazenando configurações em um arquivo `.mcp.json` no diretório raiz do seu projeto. Este arquivo é projetado para ser verificado no controle de versão, garantindo que todos os membros da equipe tenham acesso às mesmas ferramentas e serviços MCP. Quando você adiciona um servidor com escopo de projeto, Claude Code cria ou atualiza automaticamente este arquivo com a estrutura de configuração apropriada.

```bash theme={null}
# Adicionar um servidor com escopo de projeto
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

O arquivo `.mcp.json` resultante segue um formato padronizado:

```json theme={null}
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

Por razões de segurança, Claude Code solicita aprovação antes de usar servidores com escopo de projeto de arquivos `.mcp.json`. Se você precisar redefinir essas escolhas de aprovação, use o comando `claude mcp reset-project-choices`.

### Escopo de usuário

Servidores com escopo de usuário são armazenados em `~/.claude.json` e fornecem acessibilidade entre projetos, tornando-os disponíveis em todos os projetos em sua máquina enquanto permanecem privados para sua conta de usuário. Este escopo funciona bem para servidores de utilitários pessoais, ferramentas de desenvolvimento ou serviços que você usa frequentemente em diferentes projetos.

```bash theme={null}
# Adicionar um servidor de usuário
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### Hierarquia de escopo e precedência

Quando o mesmo servidor é definido em mais de um lugar, Claude Code se conecta a ele uma vez, usando a definição da fonte com maior precedência:

1. Escopo local
2. Escopo de projeto
3. Escopo de usuário
4. [Servidores fornecidos por plugins](/pt/plugins)
5. [Conectores claude.ai](#use-mcp-servers-from-claude-ai)

Os três escopos correspondem duplicatas por nome. Plugins e conectores correspondem por endpoint, então um que aponta para a mesma URL ou comando que um servidor acima é tratado como uma duplicata.

### Expansão de variáveis de ambiente em `.mcp.json`

Claude Code suporta expansão de variáveis de ambiente em arquivos `.mcp.json`, permitindo que equipes compartilhem configurações mantendo flexibilidade para caminhos específicos da máquina e valores sensíveis como chaves de API.

**Sintaxe suportada:**

* `${VAR}` - Expande para o valor da variável de ambiente `VAR`
* `${VAR:-default}` - Expande para `VAR` se definida, caso contrário usa `default`

**Locais de expansão:**
As variáveis de ambiente podem ser expandidas em:

* `command` - O caminho do executável do servidor
* `args` - Argumentos de linha de comando
* `env` - Variáveis de ambiente passadas para o servidor
* `url` - Para tipos de servidor HTTP
* `headers` - Para autenticação de servidor HTTP

**Exemplo com expansão de variável:**

```json theme={null}
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

Se uma variável de ambiente necessária não estiver definida e não tiver um valor padrão, Claude Code falhará ao analisar a configuração.

## Exemplos práticos

{/* ### Exemplo: Automatizar testes de navegador com Playwright

```bash
claude mcp add --transport stdio playwright -- npx -y @playwright/mcp@latest
```

Então escreva e execute testes de navegador:

```text
Teste se o fluxo de login funciona com test@example.com
```
```text
Tire uma captura de tela da página de checkout em mobile
```
```text
Verifique se o recurso de pesquisa retorna resultados
``` */}

### Exemplo: Monitorar erros com Sentry

```bash theme={null}
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

Autentique com sua conta Sentry:

```text theme={null}
/mcp
```

Então depure problemas de produção:

```text theme={null}
Quais são os erros mais comuns nas últimas 24 horas?
```

```text theme={null}
Mostre-me o rastreamento de pilha para o erro ID abc123
```

```text theme={null}
Qual implantação introduziu esses novos erros?
```

### Exemplo: Conectar ao GitHub para revisões de código

O servidor MCP remoto do GitHub autentica com um token de acesso pessoal do GitHub passado como cabeçalho. Para obter um, abra suas [configurações de token do GitHub](https://github.com/settings/personal-access-tokens), gere um novo token refinado com acesso aos repositórios com os quais você deseja que Claude trabalhe, então adicione o servidor:

```bash theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
  --header "Authorization: Bearer YOUR_GITHUB_PAT"
```

Então trabalhe com GitHub:

```text theme={null}
Revise o PR #456 e sugira melhorias
```

```text theme={null}
Crie um novo problema para o bug que acabamos de encontrar
```

```text theme={null}
Mostre-me todos os PRs abertos atribuídos a mim
```

### Exemplo: Consultar seu banco de dados PostgreSQL

```bash theme={null}
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"
```

Então consulte seu banco de dados naturalmente:

```text theme={null}
Qual é nossa receita total este mês?
```

```text theme={null}
Mostre-me o esquema para a tabela de pedidos
```

```text theme={null}
Encontre clientes que não fizeram uma compra em 90 dias
```

## Autenticar com servidores MCP remotos

Muitos servidores MCP baseados em nuvem exigem autenticação. Claude Code suporta OAuth 2.0 para conexões seguras.

Claude Code marca um servidor remoto como necessitando autenticação quando o servidor responde com `401 Unauthorized` ou `403 Forbidden`. Qualquer código de status sinaliza o servidor em `/mcp` para que você possa completar o fluxo OAuth. Um servidor personalizado que retorna um cabeçalho `WWW-Authenticate` apontando para seu servidor de autorização obtém a mesma descoberta automática que qualquer outro servidor remoto.

<Steps>
  <Step title="Adicione o servidor que requer autenticação">
    Por exemplo:

    ```bash theme={null}
    claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
    ```
  </Step>

  <Step title="Use o comando /mcp dentro do Claude Code">
    No Claude Code, use o comando:

    ```text theme={null}
    /mcp
    ```

    Então siga os passos no seu navegador para fazer login.
  </Step>
</Steps>

<Tip>
  Dicas:

  * Os tokens de autenticação são armazenados com segurança e atualizados automaticamente
  * Use "Clear authentication" no menu `/mcp` para revogar acesso
  * Se seu navegador não abrir automaticamente, copie a URL fornecida e abra-a manualmente
  * Se o redirecionamento do navegador falhar com um erro de conexão após autenticar, cole a URL de callback completa da barra de endereços do seu navegador no prompt de URL que aparece no Claude Code
  * A autenticação OAuth funciona com servidores HTTP
</Tip>

### Usar uma porta de callback OAuth fixa

Alguns servidores MCP exigem um URI de redirecionamento específico registrado antecipadamente. Por padrão, Claude Code escolhe uma porta aleatória disponível para o callback OAuth. Use `--callback-port` para fixar a porta para que corresponda a um URI de redirecionamento pré-registrado do formulário `http://localhost:PORT/callback`.

Você pode usar `--callback-port` sozinho (com registro dinâmico de cliente) ou junto com `--client-id` (com credenciais pré-configuradas).

```bash theme={null}
# Porta de callback fixa com registro dinâmico de cliente
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

### Usar credenciais OAuth pré-configuradas

Alguns servidores MCP não suportam configuração automática de OAuth via Registro Dinâmico de Cliente. Se você vir um erro como "Incompatible auth server: does not support dynamic client registration," o servidor requer credenciais pré-configuradas. Claude Code também suporta servidores que usam um Documento de Metadados de ID do Cliente (CIMD) em vez de Registro Dinâmico de Cliente, e descobre esses automaticamente. Se a descoberta automática falhar, registre um aplicativo OAuth através do portal do desenvolvedor do servidor primeiro, depois forneça as credenciais ao adicionar o servidor.

<Steps>
  <Step title="Registre um aplicativo OAuth com o servidor">
    Crie um aplicativo através do portal do desenvolvedor do servidor e anote seu ID do cliente e segredo do cliente.

    Muitos servidores também exigem um URI de redirecionamento. Se assim for, escolha uma porta e registre um URI de redirecionamento no formato `http://localhost:PORT/callback`. Use essa mesma porta com `--callback-port` na próxima etapa.
  </Step>

  <Step title="Adicione o servidor com suas credenciais">
    Escolha um dos seguintes métodos. A porta usada para `--callback-port` pode ser qualquer porta disponível. Ela apenas precisa corresponder ao URI de redirecionamento que você registrou na etapa anterior.

    <Tabs>
      <Tab title="claude mcp add">
        Use `--client-id` para passar o ID do cliente do seu aplicativo. A flag `--client-secret` solicita o segredo com entrada mascarada:

        ```bash theme={null}
        claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>

      <Tab title="claude mcp add-json">
        Inclua o objeto `oauth` na configuração JSON e passe `--client-secret` como uma flag separada:

        ```bash theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' \
          --client-secret
        ```
      </Tab>

      <Tab title="claude mcp add-json (apenas porta de callback)">
        Use `--callback-port` sem um ID de cliente para fixar a porta enquanto usa registro dinâmico de cliente:

        ```bash theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"callbackPort":8080}}'
        ```
      </Tab>

      <Tab title="CI / variável de ambiente">
        Defina o segredo via variável de ambiente para pular o prompt interativo:

        ```bash theme={null}
        MCP_CLIENT_SECRET=your-secret claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Autentique no Claude Code">
    Execute `/mcp` no Claude Code e siga o fluxo de login do navegador.
  </Step>
</Steps>

<Tip>
  Dicas:

  * O segredo do cliente é armazenado com segurança no seu chaveiro do sistema (macOS) ou em um arquivo de credenciais, não na sua configuração
  * Se o servidor usar um cliente OAuth público sem segredo, use apenas `--client-id` sem `--client-secret`
  * `--callback-port` pode ser usado com ou sem `--client-id`
  * Essas flags se aplicam apenas aos transportes HTTP e SSE. Elas não têm efeito em servidores stdio
  * Use `claude mcp get <name>` para verificar se as credenciais OAuth estão configuradas para um servidor
</Tip>

### Substituir descoberta de metadados OAuth

Aponte Claude Code para uma URL de metadados específica de servidor de autorização OAuth para contornar a cadeia de descoberta padrão. Defina `authServerMetadataUrl` quando os endpoints padrão do servidor MCP falharem, ou quando você deseja rotear a descoberta através de um proxy interno. Por padrão, Claude Code primeiro verifica os Metadados de Recurso Protegido RFC 9728 em `/.well-known/oauth-protected-resource`, depois volta para os metadados do servidor de autorização RFC 8414 em `/.well-known/oauth-authorization-server`.

Defina `authServerMetadataUrl` no objeto `oauth` da configuração do seu servidor em `.mcp.json`:

```json theme={null}
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

A URL deve usar `https://`. `authServerMetadataUrl` requer Claude Code v2.1.64 ou posterior. Os `scopes_supported` da URL de metadados substituem os escopos que o servidor upstream anuncia.

### Restringir escopos OAuth

Defina `oauth.scopes` para fixar os escopos que Claude Code solicita durante o fluxo de autorização. Esta é a forma suportada de restringir um servidor MCP a um subconjunto aprovado pela equipe de segurança quando o servidor de autorização upstream anuncia mais escopos do que você deseja conceder. O valor é uma única string separada por espaço, correspondendo ao formato do parâmetro `scope` em RFC 6749 §3.3.

```json theme={null}
{
  "mcpServers": {
    "slack": {
      "type": "http",
      "url": "https://mcp.slack.com/mcp",
      "oauth": {
        "scopes": "channels:read chat:write search:read"
      }
    }
  }
}
```

`oauth.scopes` tem precedência sobre `authServerMetadataUrl` e os escopos que o servidor descobre em `/.well-known`. Deixe-o indefinido para permitir que o servidor MCP determine o conjunto de escopos solicitado.

Se o servidor de autorização anuncia `offline_access` em `scopes_supported`, Claude Code o acrescenta aos escopos fixados para que o token de acesso possa ser atualizado sem um novo login no navegador.

Se o servidor depois retorna um 403 `insufficient_scope` para uma chamada de ferramenta, Claude Code se autentica novamente com os mesmos escopos fixados. Amplie `oauth.scopes` quando uma ferramenta que você precisa requer um escopo fora do pino.

### Usar cabeçalhos dinâmicos para autenticação personalizada

Se seu servidor MCP usar um esquema de autenticação diferente de OAuth (como Kerberos, tokens de curta duração ou um SSO interno), use `headersHelper` para gerar cabeçalhos de solicitação no momento da conexão. Claude Code executa o comando e mescla sua saída nos cabeçalhos de conexão.

```json theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "/opt/bin/get-mcp-auth-headers.sh"
    }
  }
}
```

O comando também pode ser inline:

```json theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "echo '{\"Authorization\": \"Bearer '\"$(get-token)\"'\"}'"
    }
  }
}
```

**Requisitos:**

* O comando deve escrever um objeto JSON de pares chave-valor de string para stdout
* O comando é executado em um shell com um tempo limite de 10 segundos
* Cabeçalhos dinâmicos substituem qualquer `headers` estático com o mesmo nome

O auxiliar é executado novamente em cada conexão (no início da sessão e ao reconectar). Não há cache, então seu script é responsável por qualquer reutilização de token.

Claude Code define essas variáveis de ambiente ao executar o auxiliar:

| Variável                      | Valor                  |
| :---------------------------- | :--------------------- |
| `CLAUDE_CODE_MCP_SERVER_NAME` | o nome do servidor MCP |
| `CLAUDE_CODE_MCP_SERVER_URL`  | a URL do servidor MCP  |

Use essas para escrever um único script auxiliar que serve múltiplos servidores MCP.

<Note>
  `headersHelper` executa comandos shell arbitrários. Quando definido no escopo de projeto ou local, ele só é executado após você aceitar o diálogo de confiança do espaço de trabalho.
</Note>

## Adicionar servidores MCP de configuração JSON

Se você tiver uma configuração JSON para um servidor MCP, você pode adicioná-la diretamente:

<Steps>
  <Step title="Adicione um servidor MCP de JSON">
    ```bash theme={null}
    # Sintaxe básica
    claude mcp add-json <name> '<json>'

    # Exemplo: Adicionar um servidor HTTP com configuração JSON
    claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'

    # Exemplo: Adicionar um servidor stdio com configuração JSON
    claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'

    # Exemplo: Adicionar um servidor HTTP com credenciais OAuth pré-configuradas
    claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' --client-secret
    ```
  </Step>

  <Step title="Verifique se o servidor foi adicionado">
    ```bash theme={null}
    claude mcp get weather-api
    ```
  </Step>
</Steps>

<Tip>
  Dicas:

  * Certifique-se de que o JSON está adequadamente escapado no seu shell
  * O JSON deve estar em conformidade com o esquema de configuração do servidor MCP
  * Você pode usar `--scope user` para adicionar o servidor à sua configuração de usuário em vez da específica do projeto
</Tip>

## Importar servidores MCP do Claude Desktop

Se você já configurou servidores MCP no Claude Desktop, você pode importá-los:

<Steps>
  <Step title="Importe servidores do Claude Desktop">
    ```bash theme={null}
    # Sintaxe básica 
    claude mcp add-from-claude-desktop 
    ```
  </Step>

  <Step title="Selecione quais servidores importar">
    Após executar o comando, você verá um diálogo interativo que permite selecionar quais servidores você deseja importar.
  </Step>

  <Step title="Verifique se os servidores foram importados">
    ```bash theme={null}
    claude mcp list 
    ```
  </Step>
</Steps>

<Tip>
  Dicas:

  * Este recurso funciona apenas em macOS e Windows Subsystem for Linux (WSL)
  * Ele lê o arquivo de configuração do Claude Desktop de sua localização padrão nessas plataformas
  * Use a flag `--scope user` para adicionar servidores à sua configuração de usuário
  * Os servidores importados terão os mesmos nomes que no Claude Desktop
  * Se servidores com os mesmos nomes já existirem, eles receberão um sufixo numérico (por exemplo, `server_1`)
</Tip>

## Usar servidores MCP do Claude.ai

Se você fez login no Claude Code com uma conta [Claude.ai](https://claude.ai), os servidores MCP que você adicionou no Claude.ai estão automaticamente disponíveis no Claude Code:

<Steps>
  <Step title="Configure servidores MCP no Claude.ai">
    Adicione servidores em [claude.ai/customize/connectors](https://claude.ai/customize/connectors). Em planos Team e Enterprise, apenas administradores podem adicionar servidores.
  </Step>

  <Step title="Autentique o servidor MCP">
    Complete quaisquer etapas de autenticação necessárias no Claude.ai.
  </Step>

  <Step title="Visualize e gerencie servidores no Claude Code">
    No Claude Code, use o comando:

    ```text theme={null}
    /mcp
    ```

    Os servidores do Claude.ai aparecem na lista com indicadores mostrando que vêm do Claude.ai.
  </Step>
</Steps>

Os conectores do Claude.ai são buscados apenas quando seu [método de autenticação](/pt/authentication#authentication-precedence) ativo é sua assinatura do Claude.ai. Eles não são carregados quando `ANTHROPIC_API_KEY`, `ANTHROPIC_AUTH_TOKEN`, `apiKeyHelper`, ou um provedor de terceiros como Bedrock ou Vertex está ativo, mesmo que você tenha executado `/login` anteriormente. Se `/mcp` não listar um conector que você adicionou, execute `/status` para confirmar qual método de autenticação está ativo, desdefina essa variável de ambiente ou remova a configuração `apiKeyHelper`, depois execute `/login` para selecionar sua conta do Claude.ai.

Um servidor que você adicionou no Claude Code tem [precedência](#scope-hierarchy-and-precedence) sobre um conector do claude.ai que aponta para a mesma URL. Quando isso acontece, `/mcp` lista o conector como oculto e mostra como remover a duplicata se você preferir usar o conector.

Para desabilitar servidores MCP do claude.ai no Claude Code, defina a variável de ambiente `ENABLE_CLAUDEAI_MCP_SERVERS` como `false`:

```bash theme={null}
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

## Usar Claude Code como um servidor MCP

Você pode usar Claude Code em si como um servidor MCP que outros aplicativos podem se conectar:

```bash theme={null}
# Inicie Claude como um servidor MCP stdio
claude mcp serve
```

Você pode usar isso no Claude Desktop adicionando esta configuração ao claude\_desktop\_config.json:

```json theme={null}
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

<Warning>
  **Configurando o caminho do executável**: O campo `command` deve referenciar o executável do Claude Code. Se o comando `claude` não estiver no PATH do seu sistema, você precisará especificar o caminho completo para o executável.

  Para encontrar o caminho completo:

  ```bash theme={null}
  which claude
  ```

  Então use o caminho completo na sua configuração:

  ```json theme={null}
  {
    "mcpServers": {
      "claude-code": {
        "type": "stdio",
        "command": "/full/path/to/claude",
        "args": ["mcp", "serve"],
        "env": {}
      }
    }
  }
  ```

  Sem o caminho correto do executável, você encontrará erros como `spawn claude ENOENT`.
</Warning>

<Tip>
  Dicas:

  * O servidor fornece acesso às ferramentas do Claude como View, Edit, LS, etc.
  * No Claude Desktop, tente pedir ao Claude para ler arquivos em um diretório, fazer edições e muito mais.
  * Observe que este servidor MCP está apenas expondo as ferramentas do Claude Code ao seu cliente MCP, então seu próprio cliente é responsável por implementar confirmação do usuário para chamadas de ferramentas individuais.
</Tip>

## Limites de saída MCP e avisos

Quando as ferramentas MCP produzem grandes saídas, Claude Code ajuda a gerenciar o uso de tokens para evitar sobrecarregar seu contexto de conversa:

* **Limite de aviso de saída**: Claude Code exibe um aviso quando qualquer saída de ferramenta MCP excede 10.000 tokens
* **Limite configurável**: você pode ajustar o máximo de tokens de saída MCP permitidos usando a variável de ambiente `MAX_MCP_OUTPUT_TOKENS`
* **Limite padrão**: o máximo padrão é 25.000 tokens
* **Escopo**: a variável de ambiente se aplica a ferramentas que não declaram seu próprio limite. Ferramentas que definem [`anthropic/maxResultSizeChars`](#raise-the-limit-for-a-specific-tool) usam esse valor em vez disso para conteúdo de texto, independentemente do que `MAX_MCP_OUTPUT_TOKENS` está definido. Ferramentas que retornam dados de imagem ainda estão sujeitas a `MAX_MCP_OUTPUT_TOKENS`

Para aumentar o limite para ferramentas que produzem grandes saídas:

```bash theme={null}
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

Isso é particularmente útil ao trabalhar com servidores MCP que:

* Consultam grandes conjuntos de dados ou bancos de dados
* Geram relatórios ou documentação detalhados
* Processam arquivos de log extensos ou informações de depuração

### Aumentar o limite para uma ferramenta específica

Se você está construindo um servidor MCP, você pode permitir que ferramentas individuais retornem resultados maiores do que o limite padrão de persistência em disco definindo `_meta["anthropic/maxResultSizeChars"]` na entrada da ferramenta em resposta `tools/list`. Claude Code aumenta o limite dessa ferramenta para o valor anotado, até um teto rígido de 500.000 caracteres.

Isso é útil para ferramentas que retornam saídas inerentemente grandes mas necessárias, como esquemas de banco de dados ou árvores de arquivos completas. Sem a anotação, resultados que excedem o limite padrão são persistidos em disco e substituídos por uma referência de arquivo na conversa.

```json theme={null}
{
  "name": "get_schema",
  "description": "Returns the full database schema",
  "_meta": {
    "anthropic/maxResultSizeChars": 200000
  }
}
```

A anotação se aplica independentemente de `MAX_MCP_OUTPUT_TOKENS` para conteúdo de texto, então os usuários não precisam aumentar a variável de ambiente para ferramentas que a declaram. Ferramentas que retornam dados de imagem ainda estão sujeitas ao limite de token.

<Warning>
  Se você encontrar frequentemente avisos de saída com servidores MCP específicos que você não controla, considere aumentar o limite `MAX_MCP_OUTPUT_TOKENS`. Você também pode pedir ao autor do servidor para adicionar a anotação `anthropic/maxResultSizeChars` ou para paginar suas respostas. A anotação não tem efeito em ferramentas que retornam conteúdo de imagem; para essas, aumentar `MAX_MCP_OUTPUT_TOKENS` é a única opção.
</Warning>

## Responder a solicitações de elicitação MCP

Os servidores MCP podem solicitar entrada estruturada de você durante uma tarefa usando elicitação. Quando um servidor precisa de informações que não consegue obter por conta própria, Claude Code exibe um diálogo interativo e passa sua resposta de volta para o servidor. Nenhuma configuração é necessária do seu lado: diálogos de elicitação aparecem automaticamente quando um servidor os solicita.

Os servidores podem solicitar entrada de duas maneiras:

* **Modo de formulário**: Claude Code mostra um diálogo com campos de formulário definidos pelo servidor (por exemplo, um prompt de nome de usuário e senha). Preencha os campos e envie.
* **Modo de URL**: Claude Code abre uma URL do navegador para autenticação ou aprovação. Complete o fluxo no navegador, depois confirme no CLI.

Para responder automaticamente a solicitações de elicitação sem mostrar um diálogo, use o [hook `Elicitation`](/pt/hooks#Elicitation).

Se você está construindo um servidor MCP que usa elicitação, veja a [especificação de elicitação MCP](https://modelcontextprotocol.io/docs/learn/client-concepts#elicitation) para detalhes de protocolo e exemplos de esquema.

## Usar recursos MCP

Os servidores MCP podem expor recursos que você pode referenciar usando menções @, semelhante a como você referencia arquivos.

### Referenciar recursos MCP

<Steps>
  <Step title="Liste recursos disponíveis">
    Digite `@` no seu prompt para ver recursos disponíveis de todos os servidores MCP conectados. Os recursos aparecem junto com arquivos no menu de preenchimento automático.
  </Step>

  <Step title="Referencie um recurso específico">
    Use o formato `@server:protocol://resource/path` para referenciar um recurso:

    ```text theme={null}
    Você pode analisar @github:issue://123 e sugerir uma correção?
    ```

    ```text theme={null}
    Por favor, revise a documentação da API em @docs:file://api/authentication
    ```
  </Step>

  <Step title="Múltiplas referências de recursos">
    Você pode referenciar múltiplos recursos em um único prompt:

    ```text theme={null}
    Compare @postgres:schema://users com @docs:file://database/user-model
    ```
  </Step>
</Steps>

<Tip>
  Dicas:

  * Os recursos são automaticamente buscados e incluídos como anexos quando referenciados
  * Os caminhos dos recursos são pesquisáveis por correspondência aproximada no preenchimento automático de menção @
  * Claude Code fornece automaticamente ferramentas para listar e ler recursos MCP quando os servidores os suportam
  * Os recursos podem conter qualquer tipo de conteúdo que o servidor MCP fornece (texto, JSON, dados estruturados, etc.)
</Tip>

## Escalar com MCP Tool Search

Tool Search mantém o uso de contexto MCP baixo adiando definições de ferramentas até que Claude precise delas. Apenas nomes de ferramentas são carregados no início da sessão, então adicionar mais servidores MCP tem impacto mínimo na sua janela de contexto.

### Como funciona

Tool Search é ativado por padrão. As ferramentas MCP são adiadas em vez de carregadas no contexto antecipadamente, e Claude usa uma ferramenta de pesquisa para descobrir as relevantes quando uma tarefa precisa delas. Apenas as ferramentas que Claude realmente usa entram no contexto. Da sua perspectiva, as ferramentas MCP funcionam exatamente como antes.

Se você preferir carregamento baseado em limite, defina `ENABLE_TOOL_SEARCH=auto` para carregar esquemas antecipadamente quando se encaixarem em 10% da janela de contexto e adiar apenas o excesso. Veja [Configurar pesquisa de ferramentas](#configure-tool-search) para todas as opções.

### Para autores de servidores MCP

Se você está construindo um servidor MCP, o campo de instruções do servidor se torna mais útil com Tool Search habilitado. As instruções do servidor ajudam Claude a entender quando pesquisar suas ferramentas, semelhante a como [skills](/pt/skills) funcionam.

Adicione instruções de servidor claras e descritivas que expliquem:

* Que categoria de tarefas suas ferramentas lidam
* Quando Claude deve pesquisar suas ferramentas
* Capacidades principais do seu servidor

Claude Code trunca descrições de ferramentas e instruções de servidor em 2KB cada. Mantenha-as concisas para evitar truncamento, e coloque detalhes críticos perto do início.

### Configurar pesquisa de ferramentas

Tool Search é ativado por padrão: as ferramentas MCP são adiadas e descobertas sob demanda. Claude Code desabilita-o por padrão no Vertex AI. Também é desabilitado quando `ANTHROPIC_BASE_URL` aponta para um host que não é de primeira parte, já que a maioria dos proxies não encaminha blocos `tool_reference`. Defina `ENABLE_TOOL_SEARCH` explicitamente para substituir qualquer fallback.

Tool Search requer um modelo que suporte blocos `tool_reference`: Sonnet 4 e posterior, ou Opus 4 e posterior. Os modelos Haiku não suportam. No Vertex AI, tool search é suportado para Claude Sonnet 4.5 e posterior e Claude Opus 4.5 e posterior.

Controle o comportamento da pesquisa de ferramentas com a variável de ambiente `ENABLE_TOOL_SEARCH`:

| Valor          | Comportamento                                                                                                                                                                                                                                         |
| :------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| (não definido) | Todas as ferramentas MCP adiadas e carregadas sob demanda. Volta a carregar antecipadamente no Vertex AI ou quando `ANTHROPIC_BASE_URL` é um host que não é de primeira parte                                                                         |
| `true`         | Todas as ferramentas MCP adiadas. Claude Code envia o cabeçalho beta mesmo no Vertex AI e através de proxies. As solicitações falham em modelos Vertex AI anteriores a Sonnet 4.5 ou Opus 4.5, ou em proxies que não suportam blocos `tool_reference` |
| `auto`         | Modo de limite: ferramentas carregam antecipadamente se se encaixarem em 10% da janela de contexto, adiadas caso contrário                                                                                                                            |
| `auto:N`       | Modo de limite com uma porcentagem personalizada, onde `N` é 0-100. Por exemplo, `auto:5` para 5%                                                                                                                                                     |
| `false`        | Todas as ferramentas MCP carregadas antecipadamente, sem adiamento                                                                                                                                                                                    |

```bash theme={null}
# Use um limite personalizado de 5%
ENABLE_TOOL_SEARCH=auto:5 claude

# Desabilite a pesquisa de ferramentas completamente
ENABLE_TOOL_SEARCH=false claude
```

Ou defina o valor no seu [campo `env` de settings.json](/pt/settings#available-settings).

Você também pode desabilitar a ferramenta `ToolSearch` especificamente:

```json theme={null}
{
  "permissions": {
    "deny": ["ToolSearch"]
  }
}
```

### Isentar um servidor de adiamento

Se as ferramentas de um servidor devem estar sempre visíveis para Claude sem uma etapa de pesquisa, defina `alwaysLoad` como `true` na configuração desse servidor. Cada ferramenta desse servidor então carrega no contexto no início da sessão independentemente da configuração `ENABLE_TOOL_SEARCH`. Use isso para um pequeno número de ferramentas que Claude precisa a cada turno, já que cada ferramenta antecipada consome contexto que estaria disponível para sua conversa.

A seguinte entrada `.mcp.json` isenta um servidor HTTP enquanto deixa outros servidores adiados:

```json theme={null}
{
  "mcpServers": {
    "core-tools": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "alwaysLoad": true
    }
  }
}
```

O campo `alwaysLoad` está disponível em todos os tipos de servidor e requer Claude Code v2.1.121 ou posterior. Um servidor MCP também pode marcar ferramentas individuais como sempre carregadas incluindo `"anthropic/alwaysLoad": true` no objeto `_meta` da ferramenta, que tem o mesmo efeito apenas para essa ferramenta.

Definir `alwaysLoad: true` também bloqueia a inicialização até que o servidor se conecte, limitado ao tempo limite de conexão padrão de 5 segundos. Isso se aplica mesmo que a inicialização MCP seja [não bloqueante por padrão](/pt/env-vars), já que as ferramentas devem estar presentes quando o primeiro prompt é construído. Outros servidores continuam a se conectar em segundo plano.

## Usar prompts MCP como comandos

Os servidores MCP podem expor prompts que se tornam disponíveis como comandos no Claude Code.

### Executar prompts MCP

<Steps>
  <Step title="Descubra prompts disponíveis">
    Digite `/` para ver todos os comandos disponíveis, incluindo aqueles de servidores MCP. Os prompts MCP aparecem com o formato `/mcp__servername__promptname`.
  </Step>

  <Step title="Execute um prompt sem argumentos">
    ```text theme={null}
    /mcp__github__list_prs
    ```
  </Step>

  <Step title="Execute um prompt com argumentos">
    Muitos prompts aceitam argumentos. Passe-os separados por espaço após o comando:

    ```text theme={null}
    /mcp__github__pr_review 456
    ```

    ```text theme={null}
    /mcp__jira__create_issue "Bug no fluxo de login" high
    ```
  </Step>
</Steps>

<Tip>
  Dicas:

  * Os prompts MCP são descobertos dinamicamente de servidores conectados
  * Os argumentos são analisados com base nos parâmetros definidos do prompt
  * Os resultados do prompt são injetados diretamente na conversa
  * Os nomes do servidor e do prompt são normalizados (espaços se tornam sublinhados)
</Tip>

## Configuração MCP gerenciada

Para organizações que precisam de controle centralizado sobre quais servidores MCP os usuários podem se conectar, consulte [Configuração MCP gerenciada](/pt/managed-mcp). Ela aborda a implantação de um conjunto fixo de servidores com `managed-mcp.json`, restrição de servidores com `allowedMcpServers` e `deniedMcpServers`, e o que os usuários veem quando um servidor é bloqueado.
