> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurar permissões

> Controle o que Claude Code pode acessar e fazer com regras de permissão refinadas, modos e políticas gerenciadas.

Claude Code suporta permissões refinadas para que você possa especificar exatamente o que o agente pode fazer e o que não pode. As configurações de permissão podem ser verificadas no controle de versão e distribuídas para todos os desenvolvedores da sua organização, bem como personalizadas por desenvolvedores individuais.

## Sistema de permissões

Claude Code usa um sistema de permissões em camadas para equilibrar poder e segurança:

| Tipo de ferramenta     | Exemplo                   | Aprovação necessária | Comportamento de "Sim, não pergunte novamente"     |
| :--------------------- | :------------------------ | :------------------- | :------------------------------------------------- |
| Somente leitura        | Leitura de arquivos, Grep | Não                  | N/A                                                |
| Comandos Bash          | Execução de shell         | Sim                  | Permanentemente por diretório de projeto e comando |
| Modificação de arquivo | Editar/escrever arquivos  | Sim                  | Até o final da sessão                              |

## Gerenciar permissões

Você pode visualizar e gerenciar as permissões de ferramentas do Claude Code com `/permissions`. Esta interface lista todas as regras de permissão e o arquivo settings.json do qual são originadas.

* As regras **Allow** permitem que Claude Code use a ferramenta especificada sem aprovação manual.
* As regras **Ask** solicitam confirmação sempre que Claude Code tenta usar a ferramenta especificada.
* As regras **Deny** impedem que Claude Code use a ferramenta especificada.

As regras são avaliadas em ordem: **deny -> ask -> allow**. A primeira regra correspondente vence, portanto as regras deny sempre têm precedência.

## Modos de permissão

Claude Code suporta vários modos de permissão que controlam como as ferramentas são aprovadas. Veja [Permission modes](/pt/permission-modes) para quando usar cada um. Defina o `defaultMode` em seus [arquivos de configuração](/pt/settings#settings-files):

| Modo                | Descrição                                                                                                                                                                                       |
| :------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Comportamento padrão: solicita permissão no primeiro uso de cada ferramenta                                                                                                                     |
| `acceptEdits`       | Aceita automaticamente permissões de edição de arquivo para a sessão, exceto escritas em diretórios protegidos                                                                                  |
| `plan`              | Plan Mode: Claude pode analisar mas não modificar arquivos ou executar comandos                                                                                                                 |
| `auto`              | Aprova automaticamente chamadas de ferramentas com verificações de segurança em segundo plano que verificam se as ações se alinham com sua solicitação. Atualmente uma visualização de pesquisa |
| `dontAsk`           | Nega automaticamente ferramentas a menos que pré-aprovadas via `/permissions` ou regras `permissions.allow`                                                                                     |
| `bypassPermissions` | Ignora prompts de permissão exceto para escritas em diretórios protegidos (veja aviso abaixo)                                                                                                   |

<Warning>
  O modo `bypassPermissions` ignora prompts de permissão. Escritas em diretórios `.git`, `.claude`, `.vscode`, `.idea` e `.husky` ainda solicitam confirmação para evitar corrupção acidental do estado do repositório, configuração do editor e git hooks. Escritas em `.claude/commands`, `.claude/agents` e `.claude/skills` são isentas e não solicitam, porque Claude rotineiramente escreve lá ao criar skills, subagents e comandos. Use este modo apenas em ambientes isolados como contêineres ou VMs onde Claude Code não pode causar danos. Administradores podem impedir este modo definindo `permissions.disableBypassPermissionsMode` como `"disable"` em [configurações gerenciadas](#managed-settings).
</Warning>

Para evitar que o modo `bypassPermissions` ou `auto` seja usado, defina `permissions.disableBypassPermissionsMode` ou `permissions.disableAutoMode` como `"disable"` em qualquer [arquivo de configuração](/pt/settings#settings-files). Estes são mais úteis em [configurações gerenciadas](#managed-settings) onde não podem ser substituídos.

## Sintaxe de regra de permissão

As regras de permissão seguem o formato `Tool` ou `Tool(specifier)`.

### Corresponder todos os usos de uma ferramenta

Para corresponder todos os usos de uma ferramenta, use apenas o nome da ferramenta sem parênteses:

| Regra      | Efeito                                              |
| :--------- | :-------------------------------------------------- |
| `Bash`     | Corresponde a todos os comandos Bash                |
| `WebFetch` | Corresponde a todas as solicitações de busca na web |
| `Read`     | Corresponde a todas as leituras de arquivo          |

`Bash(*)` é equivalente a `Bash` e corresponde a todos os comandos Bash.

### Use especificadores para controle refinado

Adicione um especificador entre parênteses para corresponder a usos específicos de ferramentas:

| Regra                          | Efeito                                                     |
| :----------------------------- | :--------------------------------------------------------- |
| `Bash(npm run build)`          | Corresponde ao comando exato `npm run build`               |
| `Read(./.env)`                 | Corresponde à leitura do arquivo `.env` no diretório atual |
| `WebFetch(domain:example.com)` | Corresponde a solicitações de busca para example.com       |

### Padrões com caracteres curinga

As regras Bash suportam padrões glob com `*`. Caracteres curinga podem aparecer em qualquer posição no comando. Esta configuração permite comandos npm e git commit enquanto bloqueia git push:

```json  theme={null}
{
  "permissions": {
    "allow": [
      "Bash(npm run *)",
      "Bash(git commit *)",
      "Bash(git * main)",
      "Bash(* --version)",
      "Bash(* --help *)"
    ],
    "deny": [
      "Bash(git push *)"
    ]
  }
}
```

O espaço antes de `*` importa: `Bash(ls *)` corresponde a `ls -la` mas não a `lsof`, enquanto `Bash(ls*)` corresponde a ambos. A sintaxe de sufixo legado `:*` é equivalente a ` *` mas está descontinuada.

## Regras de permissão específicas da ferramenta

### Bash

As regras de permissão Bash suportam correspondência com caracteres curinga `*`. Caracteres curinga podem aparecer em qualquer posição no comando, incluindo no início, meio ou fim:

* `Bash(npm run build)` corresponde ao comando Bash exato `npm run build`
* `Bash(npm run test *)` corresponde a comandos Bash começando com `npm run test`
* `Bash(npm *)` corresponde a qualquer comando começando com `npm `
* `Bash(* install)` corresponde a qualquer comando terminando com ` install`
* `Bash(git * main)` corresponde a comandos como `git checkout main`, `git merge main`

Quando `*` aparece no final com um espaço antes dele (como `Bash(ls *)`), ele impõe um limite de palavra, exigindo que o prefixo seja seguido por um espaço ou fim de string. Por exemplo, `Bash(ls *)` corresponde a `ls -la` mas não a `lsof`. Em contraste, `Bash(ls*)` sem espaço corresponde a ambos `ls -la` e `lsof` porque não há restrição de limite de palavra.

<Tip>
  Claude Code está ciente de operadores de shell (como `&&`) portanto uma regra de correspondência de prefixo como `Bash(safe-cmd *)` não lhe dará permissão para executar o comando `safe-cmd && other-cmd`.
</Tip>

Quando você aprova um comando composto com "Sim, não pergunte novamente", Claude Code salva uma regra separada para cada subcomando que requer aprovação, em vez de uma única regra para a string completa. Por exemplo, aprovar `git status && npm test` salva uma regra para `npm test`, portanto futuras invocações de `npm test` são reconhecidas independentemente do que precede o `&&`. Subcomandos como `cd` em um subdiretório geram sua própria regra Read para esse caminho. Até 5 regras podem ser salvas para um único comando composto.

<Warning>
  Padrões de permissão Bash que tentam restringir argumentos de comando são frágeis. Por exemplo, `Bash(curl http://github.com/ *)` pretende restringir curl a URLs do GitHub, mas não corresponderá a variações como:

  * Opções antes da URL: `curl -X GET http://github.com/...`
  * Protocolo diferente: `curl https://github.com/...`
  * Redirecionamentos: `curl -L http://bit.ly/xyz` (redireciona para github)
  * Variáveis: `URL=http://github.com && curl $URL`
  * Espaços extras: `curl  http://github.com`

  Para filtragem de URL mais confiável, considere:

  * **Restringir ferramentas de rede Bash**: use regras deny para bloquear `curl`, `wget` e comandos similares, depois use a ferramenta WebFetch com permissão `WebFetch(domain:github.com)` para domínios permitidos
  * **Use hooks PreToolUse**: implemente um hook que valida URLs em comandos Bash e bloqueia domínios não permitidos
  * Instruir Claude Code sobre seus padrões curl permitidos via CLAUDE.md

  Observe que usar WebFetch sozinho não impede acesso à rede. Se Bash for permitido, Claude ainda pode usar `curl`, `wget` ou outras ferramentas para alcançar qualquer URL.
</Warning>

### Read e Edit

As regras `Edit` se aplicam a todas as ferramentas integradas que editam arquivos. Claude faz uma tentativa de melhor esforço para aplicar regras `Read` a todas as ferramentas integradas que leem arquivos como Grep e Glob.

<Warning>
  As regras deny de Read e Edit se aplicam às ferramentas de arquivo integradas do Claude, não aos subprocessos Bash. Uma regra deny `Read(./.env)` bloqueia a ferramenta Read mas não impede `cat .env` em Bash. Para imposição em nível de SO que bloqueia todos os processos de acessar um caminho, [ative o sandbox](/pt/sandboxing).
</Warning>

As regras Read e Edit seguem a especificação [gitignore](https://git-scm.com/docs/gitignore) com quatro tipos de padrão distintos:

| Padrão             | Significado                                         | Exemplo                          | Corresponde                     |
| ------------------ | --------------------------------------------------- | -------------------------------- | ------------------------------- |
| `//path`           | Caminho **absoluto** da raiz do sistema de arquivos | `Read(//Users/alice/secrets/**)` | `/Users/alice/secrets/**`       |
| `~/path`           | Caminho do diretório **home**                       | `Read(~/Documents/*.pdf)`        | `/Users/alice/Documents/*.pdf`  |
| `/path`            | Caminho **relativo à raiz do projeto**              | `Edit(/src/**/*.ts)`             | `<raiz do projeto>/src/**/*.ts` |
| `path` ou `./path` | Caminho **relativo ao diretório atual**             | `Read(*.env)`                    | `<cwd>/*.env`                   |

<Warning>
  Um padrão como `/Users/alice/file` NÃO é um caminho absoluto. É relativo à raiz do projeto. Use `//Users/alice/file` para caminhos absolutos.
</Warning>

No Windows, os caminhos são normalizados para forma POSIX antes da correspondência. `C:\Users\alice` se torna `/c/Users/alice`, portanto use `//c/**/.env` para corresponder arquivos `.env` em qualquer lugar nessa unidade. Para corresponder em todas as unidades, use `//**/.env`.

Exemplos:

* `Edit(/docs/**)`: edita em `<projeto>/docs/` (NÃO `/docs/` e NÃO `<projeto>/.claude/docs/`)
* `Read(~/.zshrc)`: lê o `.zshrc` do seu diretório home
* `Edit(//tmp/scratch.txt)`: edita o caminho absoluto `/tmp/scratch.txt`
* `Read(src/**)`: lê de `<diretório-atual>/src/`

<Note>
  Em padrões gitignore, `*` corresponde a arquivos em um único diretório enquanto `**` corresponde recursivamente entre diretórios. Para permitir acesso a todos os arquivos, use apenas o nome da ferramenta sem parênteses: `Read`, `Edit` ou `Write`.
</Note>

### WebFetch

* `WebFetch(domain:example.com)` corresponde a solicitações de busca para example.com

### MCP

* `mcp__puppeteer` corresponde a qualquer ferramenta fornecida pelo servidor `puppeteer` (nome configurado em Claude Code)
* `mcp__puppeteer__*` sintaxe com caracteres curinga que também corresponde a todas as ferramentas do servidor `puppeteer`
* `mcp__puppeteer__puppeteer_navigate` corresponde à ferramenta `puppeteer_navigate` fornecida pelo servidor `puppeteer`

### Agent (subagents)

Use regras `Agent(AgentName)` para controlar quais [subagents](/pt/sub-agents) Claude pode usar:

* `Agent(Explore)` corresponde ao subagent Explore
* `Agent(Plan)` corresponde ao subagent Plan
* `Agent(my-custom-agent)` corresponde a um subagent personalizado chamado `my-custom-agent`

Adicione estas regras ao array `deny` em suas configurações ou use a flag CLI `--disallowedTools` para desabilitar agentes específicos. Para desabilitar o agente Explore:

```json  theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## Estender permissões com hooks

Os [hooks do Claude Code](/pt/hooks-guide) fornecem uma maneira de registrar comandos de shell personalizados para realizar avaliação de permissão em tempo de execução. Quando Claude Code faz uma chamada de ferramenta, os hooks PreToolUse são executados antes do prompt de permissão. A saída do hook pode negar a chamada de ferramenta, forçar um prompt ou pular o prompt para deixar a chamada prosseguir.

Pular o prompt não contorna as regras de permissão. As regras deny e ask ainda são avaliadas após um hook retornar `"allow"`, portanto uma regra deny correspondente ainda bloqueia a chamada. Isto preserva a precedência deny-first descrita em [Gerenciar permissões](#manage-permissions), incluindo regras deny definidas em configurações gerenciadas.

Um hook de bloqueio também tem precedência sobre regras allow. Um hook que sai com código 2 interrompe a chamada de ferramenta antes das regras de permissão serem avaliadas, portanto o bloqueio se aplica mesmo quando uma regra allow permitiria a chamada. Para executar todos os comandos Bash sem prompts exceto por alguns que você quer bloqueados, adicione `"Bash"` à sua lista allow e registre um hook PreToolUse que rejeita esses comandos específicos. Veja [Bloquear edições em arquivos protegidos](/pt/hooks-guide#block-edits-to-protected-files) para um script de hook que você pode adaptar.

## Diretórios de trabalho

Por padrão, Claude tem acesso a arquivos no diretório onde foi iniciado. Você pode estender este acesso:

* **Durante a inicialização**: use o argumento CLI `--add-dir <path>`
* **Durante a sessão**: use o comando `/add-dir`
* **Configuração persistente**: adicione a `additionalDirectories` em [arquivos de configuração](/pt/settings#settings-files)

Arquivos em diretórios adicionais seguem as mesmas regras de permissão do diretório de trabalho original: eles se tornam legíveis sem prompts, e as permissões de edição de arquivo seguem o modo de permissão atual.

### Diretórios adicionais concedem acesso a arquivos, não configuração

Adicionar um diretório estende onde Claude pode ler e editar arquivos. Não faz desse diretório uma raiz de configuração completa: a maioria da configuração `.claude/` não é descoberta de diretórios adicionais, embora alguns tipos sejam carregados como exceções.

Os seguintes tipos de configuração são carregados de diretórios `--add-dir`:

| Configuração                                        | Carregado de `--add-dir`                                                     |
| :-------------------------------------------------- | :--------------------------------------------------------------------------- |
| [Skills](/pt/skills) em `.claude/skills/`           | Sim, com recarga ao vivo                                                     |
| Configurações de plugin em `.claude/settings.json`  | Apenas `enabledPlugins` e `extraKnownMarketplaces`                           |
| Arquivos [CLAUDE.md](/pt/memory) e `.claude/rules/` | Apenas quando `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` está definido |

Tudo mais, incluindo subagents, comandos, estilos de saída, hooks e outras configurações, é descoberto apenas do diretório de trabalho atual e seus pais, seu diretório de usuário em `~/.claude/` e configurações gerenciadas. Para compartilhar essa configuração entre projetos, use uma destas abordagens:

* **Configuração em nível de usuário**: coloque arquivos em `~/.claude/agents/`, `~/.claude/output-styles/` ou `~/.claude/settings.json` para torná-los disponíveis em cada projeto
* **Plugins**: empacote e distribua configuração como um [plugin](/pt/plugins) que as equipes podem instalar
* **Inicie do diretório de configuração**: execute Claude Code do diretório contendo a configuração `.claude/` que você deseja

## Como as permissões interagem com sandboxing

Permissões e [sandboxing](/pt/sandboxing) são camadas de segurança complementares:

* **Permissões** controlam quais ferramentas Claude Code pode usar e quais arquivos ou domínios pode acessar. Elas se aplicam a todas as ferramentas (Bash, Read, Edit, WebFetch, MCP e outras).
* **Sandboxing** fornece imposição em nível de SO que restringe o acesso do Bash à rede e sistema de arquivos. Aplica-se apenas a comandos Bash e seus processos filhos.

Use ambos para defesa em profundidade:

* As regras deny de permissão bloqueiam Claude de até tentar acessar recursos restritos
* As restrições de sandbox impedem que comandos Bash alcancem recursos fora dos limites definidos, mesmo se uma injeção de prompt contornar a tomada de decisão de Claude
* As restrições de sistema de arquivos no sandbox usam regras deny de Read e Edit, não configuração de sandbox separada
* As restrições de rede combinam regras de permissão WebFetch com a lista `allowedDomains` do sandbox

## Configurações gerenciadas

Para organizações que precisam de controle centralizado sobre a configuração do Claude Code, administradores podem implantar configurações gerenciadas que não podem ser substituídas por configurações de usuário ou projeto. Estas configurações de política seguem o mesmo formato que arquivos de configuração regulares e podem ser entregues através de políticas MDM/nível de SO, arquivos de configuração gerenciados ou [configurações gerenciadas por servidor](/pt/server-managed-settings). Veja [arquivos de configuração](/pt/settings#settings-files) para mecanismos de entrega e locais de arquivo.

### Configurações apenas gerenciadas

As seguintes configurações são lidas apenas de configurações gerenciadas. Colocá-las em arquivos de configuração de usuário ou projeto não tem efeito.

| Configuração                                   | Descrição                                                                                                                                                                                                                                                                                 |
| :--------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowedChannelPlugins`                        | Lista de permissão de plugins de canal que podem enviar mensagens. Substitui a lista de permissão padrão da Anthropic quando definida. Requer `channelsEnabled: true`. Veja [Restringir quais plugins de canal podem ser executados](/pt/channels#restrict-which-channel-plugins-can-run) |
| `allowManagedHooksOnly`                        | Quando `true`, impede o carregamento de hooks de usuário, projeto e plugin. Apenas hooks gerenciados e hooks SDK são permitidos                                                                                                                                                           |
| `allowManagedMcpServersOnly`                   | Quando `true`, apenas `allowedMcpServers` de configurações gerenciadas são respeitados. `deniedMcpServers` ainda se mescla de todas as fontes. Veja [Configuração MCP gerenciada](/pt/mcp#managed-mcp-configuration)                                                                      |
| `allowManagedPermissionRulesOnly`              | Quando `true`, impede que configurações de usuário e projeto definam regras de permissão `allow`, `ask` ou `deny`. Apenas regras em configurações gerenciadas se aplicam                                                                                                                  |
| `blockedMarketplaces`                          | Lista de bloqueio de fontes de marketplace. Fontes bloqueadas são verificadas antes do download, portanto nunca tocam o sistema de arquivos. Veja [restrições de marketplace gerenciadas](/pt/plugin-marketplaces#managed-marketplace-restrictions)                                       |
| `channelsEnabled`                              | Permitir [channels](/pt/channels) para usuários Team e Enterprise. Não definido ou `false` bloqueia entrega de mensagem de canal independentemente do que os usuários passam para `--channels`                                                                                            |
| `pluginTrustMessage`                           | Mensagem personalizada anexada ao aviso de confiança de plugin mostrado antes da instalação                                                                                                                                                                                               |
| `sandbox.filesystem.allowManagedReadPathsOnly` | Quando `true`, apenas caminhos `filesystem.allowRead` de configurações gerenciadas são respeitados. `denyRead` ainda se mescla de todas as fontes                                                                                                                                         |
| `sandbox.network.allowManagedDomainsOnly`      | Quando `true`, apenas `allowedDomains` e regras allow `WebFetch(domain:...)` de configurações gerenciadas são respeitados. Domínios não permitidos são bloqueados automaticamente sem solicitar ao usuário. Domínios negados ainda se mesclam de todas as fontes                          |
| `strictKnownMarketplaces`                      | Controla quais marketplaces de plugin os usuários podem adicionar. Veja [restrições de marketplace gerenciadas](/pt/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                 |

`disableBypassPermissionsMode` é tipicamente colocado em configurações gerenciadas para impor política organizacional, mas funciona de qualquer escopo. Um usuário pode defini-lo em suas próprias configurações para se bloquear do modo bypass.

<Note>
  O acesso a [Remote Control](/pt/remote-control) e [sessões web](/pt/claude-code-on-the-web) não é controlado por uma chave de configurações gerenciadas. Em planos Team e Enterprise, um admin ativa ou desativa esses recursos em [configurações de admin do Claude Code](https://claude.ai/admin-settings/claude-code).
</Note>

## Revisar negações do modo auto

Quando o [modo auto](/pt/permission-modes#eliminate-prompts-with-auto-mode) nega uma chamada de ferramenta, uma notificação aparece e a ação negada é registrada em `/permissions` sob a aba Recently denied. Pressione `r` em uma ação negada para marcá-la para retry: quando você sair do diálogo, Claude Code envia uma mensagem dizendo ao modelo que pode tentar novamente essa chamada de ferramenta e retoma a conversa.

Para reagir a negações programaticamente, use o hook [`PermissionDenied`](/pt/hooks#permissiondenied).

## Configurar o classificador do modo auto

O [modo auto](/pt/permission-modes#eliminate-prompts-with-auto-mode) usa um modelo classificador para decidir se cada ação é segura para executar sem solicitar. Pronto para uso, ele confia apenas no diretório de trabalho e, se presente, nos remotes do repositório atual. Ações como fazer push para a organização de controle de fonte da sua empresa ou escrever em um bucket de nuvem de equipe serão bloqueadas como possível exfiltração de dados. O bloco de configurações `autoMode` permite que você diga ao classificador qual infraestrutura sua organização confia.

O classificador lê `autoMode` de configurações de usuário, `.claude/settings.local.json` e configurações gerenciadas. Ele não lê de configurações de projeto compartilhado em `.claude/settings.json`, porque um repositório verificado poderia injetar suas próprias regras allow.

| Escopo                       | Arquivo                       | Use para                                                       |
| :--------------------------- | :---------------------------- | :------------------------------------------------------------- |
| Um desenvolvedor             | `~/.claude/settings.json`     | Infraestrutura confiável pessoal                               |
| Um projeto, um desenvolvedor | `.claude/settings.local.json` | Buckets ou serviços confiáveis por projeto, gitignored         |
| Em toda a organização        | Configurações gerenciadas     | Infraestrutura confiável imposta para todos os desenvolvedores |

Entradas de cada escopo são combinadas. Um desenvolvedor pode estender `environment`, `allow` e `soft_deny` com entradas pessoais mas não pode remover entradas que as configurações gerenciadas fornecem. Porque as regras allow atuam como exceções às regras de bloqueio dentro do classificador, uma entrada `allow` adicionada por desenvolvedor pode substituir uma entrada `soft_deny` da organização: a combinação é aditiva, não um limite de política duro. Se você precisar de uma regra que desenvolvedores não possam contornar, use `permissions.deny` em configurações gerenciadas em vez disso, que bloqueia ações antes do classificador ser consultado.

### Definir infraestrutura confiável

Para a maioria das organizações, `autoMode.environment` é o único campo que você precisa definir. Ele diz ao classificador quais repos, buckets e domínios são confiáveis, sem tocar nas regras de bloqueio e allow integradas. O classificador usa `environment` para decidir o que "externo" significa: qualquer destino não listado é um alvo potencial de exfiltração.

```json  theme={null}
{
  "autoMode": {
    "environment": [
      "Source control: github.example.com/acme-corp and all repos under it",
      "Trusted cloud buckets: s3://acme-build-artifacts, gs://acme-ml-datasets",
      "Trusted internal domains: *.corp.example.com, api.internal.example.com",
      "Key internal services: Jenkins at ci.example.com, Artifactory at artifacts.example.com"
    ]
  }
}
```

Entradas são prosa, não regex ou padrões de ferramenta. O classificador as lê como regras em linguagem natural. Escreva-as da maneira que você descreveria sua infraestrutura para um novo engenheiro. Uma seção de ambiente completa cobre:

* **Organização**: o nome da sua empresa e para o que Claude Code é principalmente usado, como desenvolvimento de software, automação de infraestrutura ou engenharia de dados
* **Controle de fonte**: cada organização GitHub, GitLab ou Bitbucket para a qual seus desenvolvedores fazem push
* **Provedores de nuvem e buckets confiáveis**: nomes de bucket ou prefixos que Claude deve ser capaz de ler e escrever
* **Domínios internos confiáveis**: nomes de host para APIs, dashboards e serviços dentro de sua rede, como `*.internal.example.com`
* **Serviços internos chave**: CI, registros de artefatos, índices de pacotes internos, ferramentas de incidente
* **Contexto adicional**: restrições de indústria regulada, infraestrutura multi-tenant ou requisitos de conformidade que afetam o que o classificador deve tratar como arriscado

Um modelo inicial útil: preencha os campos entre colchetes e remova qualquer linha que não se aplique:

```json  theme={null}
{
  "autoMode": {
    "environment": [
      "Organization: {COMPANY_NAME}. Primary use: {PRIMARY_USE_CASE, e.g. software development, infrastructure automation}",
      "Source control: {SOURCE_CONTROL, e.g. GitHub org github.example.com/acme-corp}",
      "Cloud provider(s): {CLOUD_PROVIDERS, e.g. AWS, GCP, Azure}",
      "Trusted cloud buckets: {TRUSTED_BUCKETS, e.g. s3://acme-builds, gs://acme-datasets}",
      "Trusted internal domains: {TRUSTED_DOMAINS, e.g. *.internal.example.com, api.example.com}",
      "Key internal services: {SERVICES, e.g. Jenkins at ci.example.com, Artifactory at artifacts.example.com}",
      "Additional context: {EXTRA, e.g. regulated industry, multi-tenant infrastructure, compliance requirements}"
    ]
  }
}
```

Quanto mais contexto específico você fornecer, melhor o classificador pode distinguir operações internas rotineiras de tentativas de exfiltração.

Você não precisa preencher tudo de uma vez. Um rollout razoável: comece com os padrões e adicione sua organização de controle de fonte e serviços internos chave, que resolve os falsos positivos mais comuns como fazer push para seus próprios repos. Adicione domínios confiáveis e buckets de nuvem em seguida. Preencha o resto conforme bloqueios surgem.

### Substituir as regras de bloqueio e allow

Dois campos adicionais permitem que você substitua as listas de regras integradas do classificador: `autoMode.soft_deny` controla o que é bloqueado e `autoMode.allow` controla quais exceções se aplicam. Cada um é um array de descrições em prosa, lidas como regras em linguagem natural.

Dentro do classificador, a precedência é: regras `soft_deny` bloqueiam primeiro, depois regras `allow` substituem como exceções, depois intenção explícita do usuário substitui ambas. Se a mensagem do usuário descreve direta e especificamente a ação exata que Claude está prestes a tomar, o classificador a permite mesmo se uma regra `soft_deny` corresponder. Solicitações gerais não contam: pedir a Claude para "limpar o repo" não autoriza force-push, mas pedir a Claude para "force-push este branch" autoriza.

Para afrouxar: remova regras de `soft_deny` quando os padrões bloqueiam algo que seu pipeline já protege com revisão de PR, CI ou ambientes de staging, ou adicione a `allow` quando o classificador repetidamente sinaliza um padrão rotineiro que as exceções padrão não cobrem. Para apertar: adicione a `soft_deny` para riscos específicos do seu ambiente que os padrões perdem, ou remova de `allow` para manter uma exceção padrão às regras de bloqueio. Em todos os casos, execute `claude auto-mode defaults` para obter as listas padrão completas, depois copie e edite: nunca comece de uma lista vazia.

```json  theme={null}
{
  "autoMode": {
    "environment": [
      "Source control: github.example.com/acme-corp and all repos under it"
    ],
    "allow": [
      "Deploying to the staging namespace is allowed: staging is isolated from production and resets nightly",
      "Writing to s3://acme-scratch/ is allowed: ephemeral bucket with a 7-day lifecycle policy"
    ],
    "soft_deny": [
      "Never run database migrations outside the migrations CLI, even against dev databases",
      "Never modify files under infra/terraform/prod/: production infrastructure changes go through the review workflow",
      "...copy full default soft_deny list here first, then add your rules..."
    ]
  }
}
```

<Danger>
  Definir `allow` ou `soft_deny` substitui a lista padrão inteira para essa seção. Se você definir `soft_deny` com uma única entrada, cada regra de bloqueio integrada é descartada: force push, exfiltração de dados, `curl | bash`, deploys de produção e todas as outras regras de bloqueio padrão se tornam permitidas. Para personalizar com segurança, execute `claude auto-mode defaults` para imprimir as regras integradas, copie-as em seu arquivo de configurações, depois revise cada regra contra seu próprio pipeline e tolerância de risco. Apenas remova regras para riscos que sua infraestrutura já mitiga.
</Danger>

As três seções são avaliadas independentemente, portanto definir `environment` sozinho deixa as listas padrão `allow` e `soft_deny` intactas.

### Inspecionar os padrões e sua configuração efetiva

Porque definir `allow` ou `soft_deny` substitui os padrões, comece qualquer personalização copiando as listas padrão completas. Três subcomandos CLI ajudam você a inspecionar e validar:

```bash  theme={null}
claude auto-mode defaults  # the built-in environment, allow, and soft_deny rules
claude auto-mode config    # what the classifier actually uses: your settings where set, defaults otherwise
claude auto-mode critique  # get AI feedback on your custom allow and soft_deny rules
```

Salve a saída de `claude auto-mode defaults` em um arquivo, edite as listas para corresponder à sua política e cole o resultado em seu arquivo de configurações. Após salvar, execute `claude auto-mode config` para confirmar que as regras efetivas são o que você espera. Se você escreveu regras personalizadas, `claude auto-mode critique` as revisa e sinaliza entradas que são ambíguas, redundantes ou prováveis de causar falsos positivos.

## Precedência de configurações

As regras de permissão seguem a mesma [precedência de configurações](/pt/settings#settings-precedence) que todas as outras configurações do Claude Code:

1. **Configurações gerenciadas**: não podem ser substituídas por nenhum outro nível, incluindo argumentos de linha de comando
2. **Argumentos de linha de comando**: substituições de sessão temporária
3. **Configurações de projeto local** (`.claude/settings.local.json`)
4. **Configurações de projeto compartilhado** (`.claude/settings.json`)
5. **Configurações de usuário** (`~/.claude/settings.json`)

Se uma ferramenta for negada em qualquer nível, nenhum outro nível pode permitir. Por exemplo, uma negação de configurações gerenciadas não pode ser substituída por `--allowedTools`, e `--disallowedTools` pode adicionar restrições além do que as configurações gerenciadas definem.

Se uma permissão for permitida em configurações de usuário mas negada em configurações de projeto, a configuração de projeto tem precedência e a permissão é bloqueada.

## Configurações de exemplo

Este [repositório](https://github.com/anthropics/claude-code/tree/main/examples/settings) inclui configurações de configuração inicial para cenários de implantação comuns. Use-as como pontos de partida e ajuste-as para suas necessidades.

## Veja também

* [Settings](/pt/settings): referência de configuração completa incluindo a tabela de configurações de permissão
* [Sandboxing](/pt/sandboxing): isolamento de rede e sistema de arquivos em nível de SO para comandos Bash
* [Authentication](/pt/authentication): configure o acesso do usuário ao Claude Code
* [Security](/pt/security): salvaguardas de segurança e melhores práticas
* [Hooks](/pt/hooks-guide): automatize fluxos de trabalho e estenda avaliação de permissão
