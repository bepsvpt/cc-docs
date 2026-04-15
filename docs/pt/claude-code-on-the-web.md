> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Claude Code na web

> Execute tarefas Claude Code de forma assíncrona em infraestrutura em nuvem segura

<Note>
  Claude Code na web está atualmente em visualização de pesquisa.
</Note>

## O que é Claude Code na web?

Claude Code na web permite que desenvolvedores iniciem Claude Code a partir do aplicativo Claude. Isso é perfeito para:

* **Responder perguntas**: Pergunte sobre arquitetura de código e como os recursos são implementados
* **Correções de bugs e tarefas rotineiras**: Tarefas bem definidas que não requerem direcionamento frequente
* **Trabalho paralelo**: Aborde múltiplas correções de bugs em paralelo
* **Repositórios não em sua máquina local**: Trabalhe em código que você não tem verificado localmente
* **Alterações de backend**: Onde Claude Code pode escrever testes e depois escrever código para passar nesses testes

Claude Code também está disponível no aplicativo Claude para [iOS](https://apps.apple.com/us/app/claude-by-anthropic/id6473753684) e [Android](https://play.google.com/store/apps/details?id=com.anthropic.claude) para iniciar tarefas em movimento e monitorar trabalho em andamento.

Você pode [iniciar novas tarefas na web a partir do seu terminal](#from-terminal-to-web) com `--remote`, ou [teleportar sessões da web de volta para seu terminal](#from-web-to-terminal) para continuar localmente. Para usar a interface web enquanto executa Claude Code em sua própria máquina em vez de infraestrutura em nuvem, consulte [Remote Control](/pt/remote-control).

## Quem pode usar Claude Code na web?

Claude Code na web está disponível em visualização de pesquisa para:

* **Usuários Pro**
* **Usuários Max**
* **Usuários Team**
* **Usuários Enterprise** com assentos premium ou assentos Chat + Claude Code

## Começando

Configure Claude Code na web a partir do navegador ou do seu terminal.

### A partir do navegador

1. Visite [claude.ai/code](https://claude.ai/code)
2. Conecte sua conta GitHub
3. Instale o aplicativo Claude GitHub em seus repositórios
4. Selecione seu ambiente padrão
5. Envie sua tarefa de codificação
6. Revise as alterações na visualização de diff, itere com comentários e crie um pull request

### A partir do terminal

Execute `/web-setup` dentro de Claude Code para conectar GitHub usando suas credenciais locais de CLI `gh`. O comando sincroniza seu `gh auth token` para Claude Code na web, cria um ambiente em nuvem padrão e abre claude.ai/code em seu navegador quando termina.

Este caminho requer que o CLI `gh` esteja instalado e autenticado com `gh auth login`. Se `gh` não estiver disponível, `/web-setup` abre claude.ai/code para que você possa conectar GitHub a partir do navegador.

Suas credenciais `gh` dão a Claude acesso para clonar e enviar, para que você possa pular o aplicativo GitHub para sessões básicas. Instale o aplicativo mais tarde se quiser [Auto-fix](#auto-fix-pull-requests), que usa o aplicativo para receber webhooks de PR.

<Note>
  Administradores de Team e Enterprise podem desabilitar a configuração de terminal com o toggle Quick web setup em [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code).
</Note>

## Como funciona

Quando você inicia uma tarefa em Claude Code na web:

1. **Clonagem de repositório**: Seu repositório é clonado para uma máquina virtual gerenciada pela Anthropic
2. **Configuração de ambiente**: Claude prepara um ambiente em nuvem seguro com seu código e executa seu [script de configuração](#setup-scripts) se configurado
3. **Configuração de rede**: O acesso à Internet é configurado com base em suas configurações
4. **Execução de tarefa**: Claude analisa código, faz alterações, executa testes e verifica seu trabalho
5. **Conclusão**: Você é notificado quando termina e pode criar um PR com as alterações
6. **Resultados**: As alterações são enviadas para uma branch, prontas para criação de pull request

## Revise as alterações com visualização de diff

A visualização de diff permite que você veja exatamente o que Claude alterou antes de criar um pull request. Em vez de clicar em "Create PR" para revisar as alterações no GitHub, visualize o diff diretamente no aplicativo e itere com Claude até que as alterações estejam prontas.

Quando Claude faz alterações em arquivos, um indicador de estatísticas de diff aparece mostrando o número de linhas adicionadas e removidas (por exemplo, `+12 -1`). Selecione este indicador para abrir o visualizador de diff, que exibe uma lista de arquivos à esquerda e as alterações para cada arquivo à direita.

Na visualização de diff, você pode:

* Revisar alterações arquivo por arquivo
* Comentar em alterações específicas para solicitar modificações
* Continuar iterando com Claude com base no que você vê

Isso permite que você refine as alterações através de múltiplas rodadas de feedback sem criar PRs de rascunho ou alternar para GitHub.

## Corrigir automaticamente pull requests

Claude pode observar um pull request e responder automaticamente a falhas de CI e comentários de revisão. Claude se inscreve na atividade do GitHub no PR e, quando uma verificação falha ou um revisor deixa um comentário, Claude investiga e envia uma correção se uma for clara.

<Note>
  Auto-fix requer que o aplicativo Claude GitHub esteja instalado em seu repositório. Se você ainda não fez isso, instale-o a partir da [página do aplicativo GitHub](https://github.com/apps/claude) ou quando solicitado durante a [configuração](#getting-started).
</Note>

Existem algumas maneiras de ativar auto-fix dependendo de onde o PR veio e qual dispositivo você está usando:

* **PRs criados em Claude Code na web**: abra a barra de status de CI e selecione **Auto-fix**
* **A partir do aplicativo móvel**: diga a Claude para corrigir automaticamente o PR, por exemplo "watch this PR and fix any CI failures or review comments"
* **Qualquer PR existente**: cole a URL do PR em uma sessão e diga a Claude para corrigir automaticamente

### Como Claude responde à atividade de PR

Quando auto-fix está ativo, Claude recebe eventos do GitHub para o PR incluindo novos comentários de revisão e falhas de verificação de CI. Para cada evento, Claude investiga e decide como proceder:

* **Correções claras**: se Claude está confiante em uma correção e ela não entra em conflito com instruções anteriores, Claude faz a alteração, envia e explica o que foi feito na sessão
* **Solicitações ambíguas**: se um comentário de revisor pode ser interpretado de múltiplas maneiras ou envolve algo arquitetonicamente significativo, Claude pergunta a você antes de agir
* **Eventos duplicados ou sem ação**: se um evento é duplicado ou não requer alteração, Claude o anota na sessão e continua

Claude pode responder a threads de comentários de revisão no GitHub como parte da resolução deles. Essas respostas são postadas usando sua conta GitHub, então aparecem sob seu nome de usuário, mas cada resposta é rotulada como vindo de Claude Code para que os revisores saibam que foi escrita pelo agente e não por você diretamente.

<Warning>
  Se seu repositório usa automação acionada por comentário, como Atlantis, Terraform Cloud ou GitHub Actions personalizadas que são executadas em eventos `issue_comment`, esteja ciente de que as respostas de Claude podem acionar esses fluxos de trabalho. Revise a automação de seu repositório antes de ativar auto-fix e considere desabilitar auto-fix para repositórios onde um comentário de PR pode implantar infraestrutura ou executar operações privilegiadas.
</Warning>

## Movendo tarefas entre web e terminal

Você pode iniciar novas tarefas na web a partir do seu terminal ou puxar sessões da web para seu terminal para continuar localmente. As sessões da web persistem mesmo se você fechar seu laptop, e você pode monitorá-las de qualquer lugar, incluindo o aplicativo móvel Claude.

<Note>
  A transferência de sessão é unidirecional: você pode puxar sessões da web para seu terminal, mas não pode enviar uma sessão de terminal existente para a web. O sinalizador `--remote` cria uma *nova* sessão da web para seu repositório atual.
</Note>

### Do terminal para a web

Inicie uma sessão da web a partir da linha de comando com o sinalizador `--remote`:

```bash theme={null}
claude --remote "Fix the authentication bug in src/auth/login.ts"
```

Isso cria uma nova sessão da web em claude.ai. A tarefa é executada na nuvem enquanto você continua trabalhando localmente. Use `/tasks` para verificar o progresso ou abra a sessão em claude.ai ou no aplicativo móvel Claude para interagir diretamente. De lá, você pode orientar Claude, fornecer feedback ou responder perguntas como em qualquer outra conversa.

#### Dicas para tarefas remotas

**Planeje localmente, execute remotamente**: Para tarefas complexas, inicie Claude em Plan Mode para colaborar na abordagem e depois envie o trabalho para a web:

```bash theme={null}
claude --permission-mode plan
```

Em Plan Mode, Claude pode apenas ler arquivos e explorar a base de código. Depois de estar satisfeito com o plano, inicie uma sessão remota para execução autônoma:

```bash theme={null}
claude --remote "Execute the migration plan in docs/migration-plan.md"
```

Este padrão oferece controle sobre a estratégia enquanto permite que Claude execute autonomamente na nuvem.

**Execute tarefas em paralelo**: Cada comando `--remote` cria sua própria sessão da web que é executada independentemente. Você pode iniciar múltiplas tarefas e todas serão executadas simultaneamente em sessões separadas:

```bash theme={null}
claude --remote "Fix the flaky test in auth.spec.ts"
claude --remote "Update the API documentation"
claude --remote "Refactor the logger to use structured output"
```

Monitore todas as sessões com `/tasks`. Quando uma sessão é concluída, você pode criar um PR a partir da interface web ou [teleportar](#from-web-to-terminal) a sessão para seu terminal para continuar trabalhando.

### Da web para o terminal

Existem várias maneiras de puxar uma sessão da web para seu terminal:

* **Usando `/teleport`**: De dentro de Claude Code, execute `/teleport` (ou `/tp`) para ver um seletor interativo de suas sessões da web. Se você tiver alterações não confirmadas, será solicitado que você as guarde primeiro.
* **Usando `--teleport`**: A partir da linha de comando, execute `claude --teleport` para um seletor de sessão interativo, ou `claude --teleport <session-id>` para retomar uma sessão específica diretamente.
* **De `/tasks`**: Execute `/tasks` para ver suas sessões em segundo plano e pressione `t` para teleportar para uma
* **Da interface web**: Clique em "Open in CLI" para copiar um comando que você pode colar em seu terminal

Quando você teleporta uma sessão, Claude verifica se você está no repositório correto, busca e faz checkout da branch da sessão remota e carrega o histórico completo da conversa em seu terminal.

#### Requisitos para teleportação

Teleport verifica esses requisitos antes de retomar uma sessão. Se algum requisito não for atendido, você verá um erro ou será solicitado a resolver o problema.

| Requisito           | Detalhes                                                                                                                          |
| ------------------- | --------------------------------------------------------------------------------------------------------------------------------- |
| Estado git limpo    | Seu diretório de trabalho não deve ter alterações não confirmadas. Teleport solicita que você guarde as alterações se necessário. |
| Repositório correto | Você deve executar `--teleport` a partir de um checkout do mesmo repositório, não de um fork.                                     |
| Branch disponível   | A branch da sessão da web deve ter sido enviada para o remoto. Teleport busca e faz checkout automaticamente.                     |
| Mesma conta         | Você deve estar autenticado na mesma conta Claude.ai usada na sessão da web.                                                      |

### Compartilhando sessões

Para compartilhar uma sessão, alterne sua visibilidade de acordo com os tipos de conta abaixo. Depois disso, compartilhe o link da sessão como está. Os destinatários que abrem sua sessão compartilhada verão o estado mais recente da sessão ao carregar, mas a página do destinatário não será atualizada em tempo real.

#### Compartilhando de uma conta Enterprise ou Teams

Para contas Enterprise e Teams, as duas opções de visibilidade são **Private** e **Team**. A visibilidade Team torna a sessão visível para outros membros de sua organização Claude.ai. A verificação de acesso ao repositório é ativada por padrão, com base na conta GitHub conectada à conta do destinatário. O nome de exibição de sua conta é visível para todos os destinatários com acesso. As sessões [Claude in Slack](/pt/slack) são automaticamente compartilhadas com visibilidade Team.

#### Compartilhando de uma conta Max ou Pro

Para contas Max e Pro, as duas opções de visibilidade são **Private** e **Public**. A visibilidade Public torna a sessão visível para qualquer usuário conectado a claude.ai.

Verifique sua sessão para conteúdo sensível antes de compartilhar. As sessões podem conter código e credenciais de repositórios GitHub privados. A verificação de acesso ao repositório não é ativada por padrão.

Ative a verificação de acesso ao repositório e/ou retenha seu nome de suas sessões compartilhadas acessando Settings > Claude Code > Sharing settings.

## Agendar tarefas recorrentes

Execute Claude em um cronograma recorrente para automatizar trabalho como revisões diárias de PR, auditorias de dependência e análise de falhas de CI. Consulte [Schedule tasks on the web](/pt/web-scheduled-tasks) para o guia completo.

## Gerenciando sessões

### Arquivando sessões

Você pode arquivar sessões para manter sua lista de sessões organizada. As sessões arquivadas ficam ocultas da lista de sessões padrão, mas podem ser visualizadas filtrando por sessões arquivadas.

Para arquivar uma sessão, passe o mouse sobre a sessão na barra lateral e clique no ícone de arquivo.

### Deletando sessões

Deletar uma sessão remove permanentemente a sessão e seus dados. Esta ação não pode ser desfeita. Você pode deletar uma sessão de duas maneiras:

* **Da barra lateral**: Filtre por sessões arquivadas, passe o mouse sobre a sessão que deseja deletar e clique no ícone de exclusão
* **Do menu de sessão**: Abra uma sessão, clique no menu suspenso ao lado do título da sessão e selecione **Delete**

Você será solicitado a confirmar antes de uma sessão ser deletada.

## Ambiente em nuvem

### Imagem padrão

Construímos e mantemos uma imagem universal com cadeias de ferramentas comuns e ecossistemas de linguagem pré-instalados. Esta imagem inclui:

* Linguagens de programação e tempos de execução populares
* Ferramentas de compilação comuns e gerenciadores de pacotes
* Estruturas de teste e linters

#### Verificando ferramentas disponíveis

Para ver o que está pré-instalado em seu ambiente, peça a Claude Code para executar:

```bash theme={null}
check-tools
```

Este comando exibe:

* Linguagens de programação e suas versões
* Gerenciadores de pacotes disponíveis
* Ferramentas de desenvolvimento instaladas

#### Configurações específicas de linguagem

A imagem universal inclui ambientes pré-configurados para:

* **Python**: Python 3.x com pip, poetry e bibliotecas científicas comuns
* **Node.js**: Versões LTS mais recentes com npm, yarn, pnpm e bun
* **Ruby**: Versões 3.1.6, 3.2.6, 3.3.6 (padrão: 3.3.6) com gem, bundler e rbenv para gerenciamento de versão
* **PHP**: Versão 8.4.14
* **Java**: OpenJDK com Maven e Gradle
* **Go**: Versão estável mais recente com suporte a módulos
* **Rust**: Cadeia de ferramentas Rust com cargo
* **C++**: Compiladores GCC e Clang

#### Bancos de dados

A imagem universal inclui os seguintes bancos de dados:

* **PostgreSQL**: Versão 16
* **Redis**: Versão 7.0

### Configuração de ambiente

Quando você inicia uma sessão em Claude Code na web, aqui está o que acontece nos bastidores:

1. **Preparação de ambiente**: Clonamos seu repositório e executamos qualquer [script de configuração](#setup-scripts) configurado. O repositório será clonado com a branch padrão em seu repositório GitHub. Se você gostaria de fazer checkout de uma branch específica, você pode especificar isso no prompt.

2. **Configuração de rede**: Configuramos o acesso à Internet para o agente. O acesso à Internet é limitado por padrão, mas você pode configurar o ambiente para não ter Internet ou ter acesso total à Internet com base em suas necessidades.

3. **Execução de Claude Code**: Claude Code é executado para completar sua tarefa, escrevendo código, executando testes e verificando seu trabalho. Você pode guiar e orientar Claude durante toda a sessão através da interface web. Claude respeita o contexto que você definiu em seu `CLAUDE.md`.

4. **Resultado**: Quando Claude completa seu trabalho, ele enviará a branch para remoto. Você poderá criar um PR para a branch.

<Note>
  Claude opera inteiramente através do terminal e ferramentas CLI disponíveis no ambiente. Ele usa as ferramentas pré-instaladas na imagem universal e quaisquer ferramentas adicionais que você instale através de hooks ou gerenciamento de dependências.
</Note>

**Para adicionar um novo ambiente:** Selecione o ambiente atual para abrir o seletor de ambiente e selecione "Add environment". Isso abrirá um diálogo onde você pode especificar o nome do ambiente, nível de acesso à rede, variáveis de ambiente e um [script de configuração](#setup-scripts).

**Para atualizar um ambiente existente:** Selecione o ambiente atual, à direita do nome do ambiente, e selecione o botão de configurações. Isso abrirá um diálogo onde você pode atualizar o nome do ambiente, acesso à rede, variáveis de ambiente e script de configuração.

**Para selecionar seu ambiente padrão a partir do terminal:** Se você tiver múltiplos ambientes configurados, execute `/remote-env` para escolher qual usar ao iniciar sessões da web a partir do seu terminal com `--remote`. Com um único ambiente, este comando mostra sua configuração atual.

<Note>
  As variáveis de ambiente devem ser especificadas como pares chave-valor, em [formato `.env`](https://www.dotenv.org/). Por exemplo:

  ```text theme={null}
  API_KEY=your_api_key
  DEBUG=true
  ```
</Note>

### Setup scripts

Um setup script é um script Bash que é executado quando uma nova sessão em nuvem inicia, antes de Claude Code ser lançado. Use setup scripts para instalar dependências, configurar ferramentas ou preparar qualquer coisa que o ambiente em nuvem precise que não esteja na [imagem padrão](#default-image).

Os scripts são executados como root no Ubuntu 24.04, então `apt install` e a maioria dos gerenciadores de pacotes de linguagem funcionam.

<Tip>
  Para verificar o que já está instalado antes de adicioná-lo ao seu script, peça a Claude para executar `check-tools` em uma sessão em nuvem.
</Tip>

Para adicionar um setup script, abra o diálogo de configurações de ambiente e insira seu script no campo **Setup script**.

Este exemplo instala o CLI `gh`, que não está na imagem padrão:

```bash theme={null}
#!/bin/bash
apt update && apt install -y gh
```

Os setup scripts são executados apenas ao criar uma nova sessão. Eles são ignorados ao retomar uma sessão existente.

Se o script sair com código diferente de zero, a sessão falha ao iniciar. Acrescente `|| true` a comandos não críticos para evitar bloquear a sessão em uma instalação instável.

<Note>
  Os setup scripts que instalam pacotes precisam de acesso à rede para alcançar registros. O acesso à rede padrão permite conexões com [registros de pacotes comuns](#default-allowed-domains) incluindo npm, PyPI, RubyGems e crates.io. Os scripts falharão ao instalar pacotes se seu ambiente tiver acesso à rede desativado.
</Note>

#### Setup scripts vs. SessionStart hooks

Use um setup script para instalar coisas que a nuvem precisa mas seu laptop já tem, como um tempo de execução de linguagem ou ferramenta CLI. Use um [hook SessionStart](/pt/hooks#sessionstart) para configuração de projeto que deve ser executada em todos os lugares, nuvem e local, como `npm install`.

Ambos são executados no início de uma sessão, mas pertencem a lugares diferentes:

|                | Setup scripts                                             | SessionStart hooks                                                         |
| -------------- | --------------------------------------------------------- | -------------------------------------------------------------------------- |
| Anexado a      | O ambiente em nuvem                                       | Seu repositório                                                            |
| Configurado em | Interface do usuário do ambiente em nuvem                 | `.claude/settings.json` em seu repositório                                 |
| Executa        | Antes de Claude Code ser lançado, apenas em novas sessões | Depois de Claude Code ser lançado, em todas as sessões incluindo retomadas |
| Escopo         | Apenas ambientes em nuvem                                 | Ambientes locais e em nuvem                                                |

Os hooks SessionStart também podem ser definidos em seu `~/.claude/settings.json` no nível do usuário localmente, mas as configurações no nível do usuário não são transferidas para sessões em nuvem. Na nuvem, apenas os hooks confirmados no repositório são executados.

### Gerenciamento de dependências

Imagens de ambiente personalizadas e snapshots ainda não são suportados. Use [setup scripts](#setup-scripts) para instalar pacotes quando uma sessão inicia, ou [SessionStart hooks](/pt/hooks#sessionstart) para instalação de dependências que também deve ser executada em ambientes locais. Os SessionStart hooks têm [limitações conhecidas](#dependency-management-limitations).

Para configurar a instalação automática de dependências com um setup script, abra as configurações de seu ambiente e adicione um script:

```bash theme={null}
#!/bin/bash
npm install
pip install -r requirements.txt
```

Alternativamente, você pode usar SessionStart hooks no arquivo `.claude/settings.json` de seu repositório para instalação de dependências que também deve ser executada em ambientes locais:

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

Crie o script correspondente em `scripts/install_pkgs.sh`:

```bash theme={null}
#!/bin/bash

# Only run in remote environments
if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

Torne-o executável: `chmod +x scripts/install_pkgs.sh`

#### Persistir variáveis de ambiente

Os SessionStart hooks podem persistir variáveis de ambiente para comandos Bash subsequentes escrevendo no arquivo especificado na variável de ambiente `CLAUDE_ENV_FILE`. Para detalhes, consulte [SessionStart hooks](/pt/hooks#sessionstart) na referência de hooks.

#### Limitações de gerenciamento de dependências

* **Hooks disparam para todas as sessões**: Os SessionStart hooks são executados em ambientes locais e remotos. Não há configuração de hook para escopo de um hook apenas para sessões remotas. Para pular execução local, verifique a variável de ambiente `CLAUDE_CODE_REMOTE` em seu script conforme mostrado acima.
* **Requer acesso à rede**: Os comandos de instalação precisam de acesso à rede para alcançar registros de pacotes. Se seu ambiente estiver configurado com acesso "No internet", esses hooks falharão. Use acesso à rede "Limited" (o padrão) ou "Full". A [lista de permissões padrão](#default-allowed-domains) inclui registros comuns como npm, PyPI, RubyGems e crates.io.
* **Compatibilidade com proxy**: Todo o tráfego de saída em ambientes remotos passa por um [proxy de segurança](#security-proxy). Alguns gerenciadores de pacotes não funcionam corretamente com este proxy. Bun é um exemplo conhecido.
* **Executa a cada início de sessão**: Os hooks são executados cada vez que uma sessão inicia ou é retomada, adicionando latência de inicialização. Mantenha os scripts de instalação rápidos verificando se as dependências já estão presentes antes de reinstalar.

## Acesso à rede e segurança

### Política de rede

#### Proxy GitHub

Para segurança, todas as operações GitHub passam por um serviço de proxy dedicado que trata transparentemente todas as interações git. Dentro da sandbox, o cliente git autentica usando uma credencial com escopo personalizado. Este proxy:

* Gerencia autenticação GitHub com segurança - o cliente git usa uma credencial com escopo dentro da sandbox, que o proxy verifica e traduz para seu token de autenticação GitHub real
* Restringe operações git push para a branch de trabalho atual por segurança
* Permite clonagem, busca e operações de PR contínuas mantendo limites de segurança

#### Proxy de segurança

Os ambientes são executados atrás de um proxy de rede HTTP/HTTPS para fins de segurança e prevenção de abuso. Todo o tráfego de Internet de saída passa por este proxy, que fornece:

* Proteção contra solicitações maliciosas
* Limitação de taxa e prevenção de abuso
* Filtragem de conteúdo para segurança aprimorada

### Níveis de acesso

Por padrão, o acesso à rede é limitado aos [domínios na lista de permissões](#default-allowed-domains).

Você pode configurar acesso à rede personalizado, incluindo desabilitar o acesso à rede.

### Domínios padrão permitidos

Ao usar acesso à rede "Limited", os seguintes domínios são permitidos por padrão:

#### Serviços Anthropic

* api.anthropic.com
* statsig.anthropic.com
* platform.claude.com
* code.claude.com
* claude.ai

#### Controle de versão

* github.com
* [www.github.com](http://www.github.com)
* api.github.com
* npm.pkg.github.com
* raw\.githubusercontent.com
* pkg-npm.githubusercontent.com
* objects.githubusercontent.com
* codeload.github.com
* avatars.githubusercontent.com
* camo.githubusercontent.com
* gist.github.com
* gitlab.com
* [www.gitlab.com](http://www.gitlab.com)
* registry.gitlab.com
* bitbucket.org
* [www.bitbucket.org](http://www.bitbucket.org)
* api.bitbucket.org

#### Registros de contêiner

* registry-1.docker.io
* auth.docker.io
* index.docker.io
* hub.docker.com
* [www.docker.com](http://www.docker.com)
* production.cloudflare.docker.com
* download.docker.com
* gcr.io
* \*.gcr.io
* ghcr.io
* mcr.microsoft.com
* \*.data.mcr.microsoft.com
* public.ecr.aws

#### Plataformas em nuvem

* cloud.google.com
* accounts.google.com
* gcloud.google.com
* \*.googleapis.com
* storage.googleapis.com
* compute.googleapis.com
* container.googleapis.com
* azure.com
* portal.azure.com
* microsoft.com
* [www.microsoft.com](http://www.microsoft.com)
* \*.microsoftonline.com
* packages.microsoft.com
* dotnet.microsoft.com
* dot.net
* visualstudio.com
* dev.azure.com
* \*.amazonaws.com
* \*.api.aws
* oracle.com
* [www.oracle.com](http://www.oracle.com)
* java.com
* [www.java.com](http://www.java.com)
* java.net
* [www.java.net](http://www.java.net)
* download.oracle.com
* yum.oracle.com

#### Gerenciadores de pacotes - JavaScript/Node

* registry.npmjs.org
* [www.npmjs.com](http://www.npmjs.com)
* [www.npmjs.org](http://www.npmjs.org)
* npmjs.com
* npmjs.org
* yarnpkg.com
* registry.yarnpkg.com

#### Gerenciadores de pacotes - Python

* pypi.org
* [www.pypi.org](http://www.pypi.org)
* files.pythonhosted.org
* pythonhosted.org
* test.pypi.org
* pypi.python.org
* pypa.io
* [www.pypa.io](http://www.pypa.io)

#### Gerenciadores de pacotes - Ruby

* rubygems.org
* [www.rubygems.org](http://www.rubygems.org)
* api.rubygems.org
* index.rubygems.org
* ruby-lang.org
* [www.ruby-lang.org](http://www.ruby-lang.org)
* rubyforge.org
* [www.rubyforge.org](http://www.rubyforge.org)
* rubyonrails.org
* [www.rubyonrails.org](http://www.rubyonrails.org)
* rvm.io
* get.rvm.io

#### Gerenciadores de pacotes - Rust

* crates.io
* [www.crates.io](http://www.crates.io)
* index.crates.io
* static.crates.io
* rustup.rs
* static.rust-lang.org
* [www.rust-lang.org](http://www.rust-lang.org)

#### Gerenciadores de pacotes - Go

* proxy.golang.org
* sum.golang.org
* index.golang.org
* golang.org
* [www.golang.org](http://www.golang.org)
* goproxy.io
* pkg.go.dev

#### Gerenciadores de pacotes - JVM

* maven.org
* repo.maven.org
* central.maven.org
* repo1.maven.org
* jcenter.bintray.com
* gradle.org
* [www.gradle.org](http://www.gradle.org)
* services.gradle.org
* plugins.gradle.org
* kotlin.org
* [www.kotlin.org](http://www.kotlin.org)
* spring.io
* repo.spring.io

#### Gerenciadores de pacotes - Outras linguagens

* packagist.org (PHP Composer)
* [www.packagist.org](http://www.packagist.org)
* repo.packagist.org
* nuget.org (.NET NuGet)
* [www.nuget.org](http://www.nuget.org)
* api.nuget.org
* pub.dev (Dart/Flutter)
* api.pub.dev
* hex.pm (Elixir/Erlang)
* [www.hex.pm](http://www.hex.pm)
* cpan.org (Perl CPAN)
* [www.cpan.org](http://www.cpan.org)
* metacpan.org
* [www.metacpan.org](http://www.metacpan.org)
* api.metacpan.org
* cocoapods.org (iOS/macOS)
* [www.cocoapods.org](http://www.cocoapods.org)
* cdn.cocoapods.org
* haskell.org
* [www.haskell.org](http://www.haskell.org)
* hackage.haskell.org
* swift.org
* [www.swift.org](http://www.swift.org)

#### Distribuições Linux

* archive.ubuntu.com
* security.ubuntu.com
* ubuntu.com
* [www.ubuntu.com](http://www.ubuntu.com)
* \*.ubuntu.com
* ppa.launchpad.net
* launchpad.net
* [www.launchpad.net](http://www.launchpad.net)

#### Ferramentas de desenvolvimento e plataformas

* dl.k8s.io (Kubernetes)
* pkgs.k8s.io
* k8s.io
* [www.k8s.io](http://www.k8s.io)
* releases.hashicorp.com (HashiCorp)
* apt.releases.hashicorp.com
* rpm.releases.hashicorp.com
* archive.releases.hashicorp.com
* hashicorp.com
* [www.hashicorp.com](http://www.hashicorp.com)
* repo.anaconda.com (Anaconda/Conda)
* conda.anaconda.org
* anaconda.org
* [www.anaconda.com](http://www.anaconda.com)
* anaconda.com
* continuum.io
* apache.org (Apache)
* [www.apache.org](http://www.apache.org)
* archive.apache.org
* downloads.apache.org
* eclipse.org (Eclipse)
* [www.eclipse.org](http://www.eclipse.org)
* download.eclipse.org
* nodejs.org (Node.js)
* [www.nodejs.org](http://www.nodejs.org)

#### Serviços em nuvem e monitoramento

* statsig.com
* [www.statsig.com](http://www.statsig.com)
* api.statsig.com
* sentry.io
* \*.sentry.io
* http-intake.logs.datadoghq.com
* \*.datadoghq.com
* \*.datadoghq.eu

#### Entrega de conteúdo e espelhos

* sourceforge.net
* \*.sourceforge.net
* packagecloud.io
* \*.packagecloud.io

#### Schema e configuração

* json-schema.org
* [www.json-schema.org](http://www.json-schema.org)
* json.schemastore.org
* [www.schemastore.org](http://www.schemastore.org)

#### Model Context Protocol

* \*.modelcontextprotocol.io

<Note>
  Domínios marcados com `*` indicam correspondência de subdomínio curinga. Por exemplo, `*.gcr.io` permite acesso a qualquer subdomínio de `gcr.io`.
</Note>

### Melhores práticas de segurança para acesso à rede personalizado

1. **Princípio do menor privilégio**: Ative apenas o acesso à rede mínimo necessário
2. **Audite regularmente**: Revise os domínios permitidos periodicamente
3. **Use HTTPS**: Sempre prefira endpoints HTTPS em vez de HTTP

## Segurança e isolamento

Claude Code na web fornece garantias de segurança fortes:

* **Máquinas virtuais isoladas**: Cada sessão é executada em uma VM isolada gerenciada pela Anthropic
* **Controles de acesso à rede**: O acesso à rede é limitado por padrão e pode ser desativado

<Note>
  Ao executar com acesso à rede desativado, Claude Code é permitido se comunicar com a API Anthropic, o que ainda pode permitir que dados saiam da VM isolada de Claude Code.
</Note>

* **Proteção de credenciais**: Credenciais sensíveis (como credenciais git ou chaves de assinatura) nunca estão dentro da sandbox com Claude Code. A autenticação é tratada através de um proxy seguro usando credenciais com escopo
* **Análise segura**: O código é analisado e modificado dentro de VMs isoladas antes de criar PRs

## Preços e limites de taxa

Claude Code na web compartilha limites de taxa com todo o outro uso de Claude e Claude Code dentro de sua conta. Executar múltiplas tarefas em paralelo consumirá mais limites de taxa proporcionalmente.

## Limitações

* **Autenticação de repositório**: Você pode apenas mover sessões de web para local quando está autenticado na mesma conta
* **Restrições de plataforma**: Claude Code na web funciona apenas com código hospedado no GitHub. Instâncias [GitHub Enterprise Server](/pt/github-enterprise-server) auto-hospedadas são suportadas para planos Teams e Enterprise. GitLab e outros repositórios não-GitHub não podem ser usados com sessões em nuvem

## Melhores práticas

1. **Automatize a configuração de ambiente**: Use [setup scripts](#setup-scripts) para instalar dependências e configurar ferramentas antes de Claude Code ser lançado. Para cenários mais avançados, configure [SessionStart hooks](/pt/hooks#sessionstart).
2. **Documente requisitos**: Especifique claramente dependências e comandos em seu arquivo `CLAUDE.md`. Se você tiver um arquivo `AGENTS.md`, você pode obtê-lo em seu `CLAUDE.md` usando `@AGENTS.md` para manter uma única fonte de verdade.

## Recursos relacionados

* [Configuração de hooks](/pt/hooks)
* [Referência de configurações](/pt/settings)
* [Segurança](/pt/security)
* [Uso de dados](/pt/data-usage)
