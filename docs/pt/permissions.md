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
| Modificação de arquivo | Edit/Write de arquivos    | Sim                  | Até o final da sessão                              |

## Gerenciar permissões

Você pode visualizar e gerenciar as permissões de ferramentas do Claude Code com `/permissions`. Esta interface lista todas as regras de permissão e o arquivo settings.json do qual são originadas.

* As regras **Allow** permitem que Claude Code use a ferramenta especificada sem aprovação manual.
* As regras **Ask** solicitam confirmação sempre que Claude Code tenta usar a ferramenta especificada.
* As regras **Deny** impedem que Claude Code use a ferramenta especificada.

As regras são avaliadas em ordem: **deny -> ask -> allow**. A primeira regra correspondente vence, portanto as regras deny sempre têm precedência.

As regras deny se comportam de forma diferente dependendo se nomeiam uma ferramenta ou definem o escopo de um padrão dentro de uma. Um nome de ferramenta simples como `Bash` remove a ferramenta do contexto do Claude completamente, então Claude nunca a vê. Uma regra com escopo como `Bash(rm *)` deixa a ferramenta disponível e bloqueia chamadas correspondentes quando Claude tenta usá-las.

<Note>
  As regras de permissão são aplicadas pelo Claude Code, não pelo modelo. As instruções em seu prompt ou `CLAUDE.md` moldam o que Claude tenta fazer, mas não alteram o que Claude Code permite. Para conceder ou revogar acesso, use `/permissions`, as regras descritas aqui, um [modo de permissão](/pt/permission-modes), ou um [hook PreToolUse](#extend-permissions-with-hooks).
</Note>

## Modos de permissão

Claude Code suporta vários modos de permissão que controlam como as ferramentas são aprovadas. Veja [Permission modes](/pt/permission-modes) para quando usar cada um. Defina o `defaultMode` em seus [arquivos de configuração](/pt/settings#settings-files):

| Modo                | Descrição                                                                                                                                                                                       |
| :------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `default`           | Comportamento padrão: solicita permissão no primeiro uso de cada ferramenta                                                                                                                     |
| `acceptEdits`       | Aceita automaticamente edições de arquivo e comandos comuns do sistema de arquivos (`mkdir`, `touch`, `mv`, `cp`, etc.) para caminhos no diretório de trabalho ou `additionalDirectories`       |
| `plan`              | Plan Mode: Claude lê arquivos e executa comandos shell somente leitura para explorar, mas não edita seus arquivos de origem                                                                     |
| `auto`              | Aprova automaticamente chamadas de ferramentas com verificações de segurança em segundo plano que verificam se as ações se alinham com sua solicitação. Atualmente uma visualização de pesquisa |
| `dontAsk`           | Nega automaticamente ferramentas a menos que pré-aprovadas via `/permissions` ou regras `permissions.allow`                                                                                     |
| `bypassPermissions` | Ignora todos os prompts de permissão. Remoções de diretório raiz e diretório inicial como `rm -rf /` ainda solicitam como um disjuntor                                                          |

<Warning>
  O modo `bypassPermissions` ignora todos os prompts de permissão, incluindo escritas em `.git`, `.claude`, `.vscode`, `.idea` e `.husky`. Remoções direcionadas ao diretório raiz do sistema de arquivos ou diretório inicial, como `rm -rf /` e `rm -rf ~`, ainda solicitam como um disjuntor contra erro do modelo. Use este modo apenas em ambientes isolados como contêineres ou VMs onde Claude Code não pode causar danos. Administradores podem impedir este modo definindo `permissions.disableBypassPermissionsMode` como `"disable"` em [configurações gerenciadas](#managed-settings).
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

`Bash(*)` é equivalente a `Bash` e corresponde a todos os comandos Bash. Como uma regra de negação, ambas as formas removem a ferramenta do contexto do Claude.

### Use especificadores para controle refinado

Adicione um especificador entre parênteses para corresponder a usos específicos de ferramentas:

| Regra                          | Efeito                                                     |
| :----------------------------- | :--------------------------------------------------------- |
| `Bash(npm run build)`          | Corresponde ao comando exato `npm run build`               |
| `Read(./.env)`                 | Corresponde à leitura do arquivo `.env` no diretório atual |
| `WebFetch(domain:example.com)` | Corresponde a solicitações de busca para example.com       |

### Padrões com caracteres curinga

As regras Bash suportam padrões glob com `*`. Caracteres curinga podem aparecer em qualquer posição no comando. Esta configuração permite comandos npm e git commit enquanto bloqueia git push:

```json theme={null}
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

O espaço antes de `*` importa: `Bash(ls *)` corresponde a `ls -la` mas não a `lsof`, enquanto `Bash(ls*)` corresponde a ambos. O sufixo `:*` é uma maneira equivalente de escrever um caractere curinga à direita, portanto `Bash(ls:*)` corresponde aos mesmos comandos que `Bash(ls *)`.

O diálogo de permissão escreve a forma separada por espaço quando você seleciona "Sim, não pergunte novamente" para um prefixo de comando. A forma `:*` é reconhecida apenas no final de um padrão. Em um padrão como `Bash(git:* push)`, o dois-pontos é tratado como um caractere literal e não corresponderá a comandos git.

## Regras de permissão específicas da ferramenta

### Bash

As regras de permissão Bash suportam correspondência com caracteres curinga `*`. Caracteres curinga podem aparecer em qualquer posição no comando, incluindo no início, meio ou fim:

* `Bash(npm run build)` corresponde ao comando Bash exato `npm run build`
* `Bash(npm run test *)` corresponde a comandos Bash começando com `npm run test`
* `Bash(npm *)` corresponde a qualquer comando começando com `npm `
* `Bash(* install)` corresponde a qualquer comando terminando com ` install`
* `Bash(git * main)` corresponde a comandos como `git checkout main` e `git log --oneline main`

Um único `*` corresponde a qualquer sequência de caracteres incluindo espaços, portanto um caractere curinga pode abranger múltiplos argumentos. `Bash(git *)` corresponde a `git log --oneline --all`, e `Bash(git * main)` corresponde a `git push origin main` bem como `git merge main`.

Quando `*` aparece no final com um espaço antes dele (como `Bash(ls *)`), ele impõe um limite de palavra, exigindo que o prefixo seja seguido por um espaço ou fim de string. Por exemplo, `Bash(ls *)` corresponde a `ls -la` mas não a `lsof`. Em contraste, `Bash(ls*)` sem espaço corresponde a ambos `ls -la` e `lsof` porque não há restrição de limite de palavra.

#### Comandos compostos

<Tip>
  Claude Code está ciente de operadores de shell, portanto uma regra como `Bash(safe-cmd *)` não lhe dará permissão para executar o comando `safe-cmd && other-cmd`. Os separadores de comando reconhecidos são `&&`, `||`, `;`, `|`, `|&`, `&` e quebras de linha. Uma regra deve corresponder a cada subcomando independentemente.
</Tip>

Quando você aprova um comando composto com "Sim, não pergunte novamente", Claude Code salva uma regra separada para cada subcomando que requer aprovação, em vez de uma única regra para a string completa. Por exemplo, aprovar `git status && npm test` salva uma regra para `npm test`, portanto futuras invocações de `npm test` são reconhecidas independentemente do que precede o `&&`. Subcomandos como `cd` em um subdiretório geram sua própria regra Read para esse caminho. Até 5 regras podem ser salvas para um único comando composto.

#### Wrappers de processo

Antes de corresponder regras Bash, Claude Code remove um conjunto fixo de wrappers de processo para que uma regra como `Bash(npm test *)` também corresponda a `timeout 30 npm test`. Os wrappers reconhecidos são `timeout`, `time`, `nice`, `nohup` e `stdbuf`.

`xargs` simples também é removido, portanto `Bash(grep *)` corresponde a `xargs grep pattern`. A remoção se aplica apenas quando `xargs` não tem flags: uma invocação como `xargs -n1 grep pattern` é correspondida como um comando `xargs`, portanto regras escritas para o comando interno não a cobrem.

Esta lista de wrapper é integrada e não é configurável. Executores de ambiente de desenvolvimento como `direnv exec`, `devbox run`, `mise exec`, `npx` e `docker exec` não estão na lista. Porque essas ferramentas executam seus argumentos como um comando, uma regra como `Bash(devbox run *)` corresponde a tudo que vem após `run`, incluindo `devbox run rm -rf .`. Para aprovar trabalho dentro de um executor de ambiente, escreva uma regra específica que inclua tanto o executor quanto o comando interno, como `Bash(devbox run npm test)`. Adicione uma regra por comando interno que você quer permitir.

Wrappers exec como `watch`, `setsid`, `ionice` e `flock` sempre solicitam e não podem ser auto-aprovados por uma regra de prefixo como `Bash(watch *)`. O mesmo se aplica a `find` com `-exec` ou `-delete`: uma regra `Bash(find *)` não cobre essas formas. Para aprovar uma invocação específica, escreva uma regra de correspondência exata para a string de comando completa.

#### Comandos somente leitura

Claude Code reconhece um conjunto integrado de comandos Bash como somente leitura e os executa sem um prompt de permissão em cada modo. Estes incluem `ls`, `cat`, `echo`, `pwd`, `head`, `tail`, `grep`, `find`, `wc`, `which`, `diff`, `stat`, `du`, `cd` e formas somente leitura de `git`. O conjunto não é configurável; para exigir um prompt para um desses comandos, adicione uma regra `ask` ou `deny` para ele.

Padrões glob sem aspas são permitidos para comandos cujas todas as flags são somente leitura, portanto `ls *.ts` e `wc -l src/*.py` são executados sem um prompt. Comandos com flags capazes de escrita ou execução, como `find`, `sort`, `sed` e `git`, ainda solicitam quando um glob sem aspas está presente porque o glob poderia expandir para uma flag como `-delete`.

Um `cd` em um caminho dentro do seu diretório de trabalho ou um [diretório adicional](#working-directories) também é somente leitura. Um comando composto como `cd packages/api && ls` é executado sem um prompt quando cada parte se qualifica por conta própria. Combinar `cd` com `git` em um comando composto sempre solicita, independentemente do diretório de destino.

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
  * **Adicione orientação CLAUDE.md**: descreva seus padrões curl permitidos em `CLAUDE.md`. Isso molda o que Claude tenta mas não impõe um limite, portanto combine com uma das opções acima

  Observe que usar WebFetch sozinho não impede acesso à rede. Se Bash for permitido, Claude ainda pode usar `curl`, `wget` ou outras ferramentas para alcançar qualquer URL.
</Warning>

### PowerShell

As regras de permissão PowerShell usam a mesma forma que as regras Bash. Caracteres curinga com `*` correspondem em qualquer posição, o sufixo `:*` é equivalente a um ` *` final, e um `PowerShell` simples ou `PowerShell(*)` corresponde a cada comando. Esta configuração permite comandos `Get-ChildItem` e `git commit` enquanto bloqueia `Remove-Item`:

```json theme={null}
{
  "permissions": {
    "allow": [
      "PowerShell(Get-ChildItem *)",
      "PowerShell(git commit *)"
    ],
    "deny": [
      "PowerShell(Remove-Item *)"
    ]
  }
}
```

Aliases comuns são canonicalizados antes da correspondência. Uma regra escrita para o nome do cmdlet também corresponde a seus aliases, portanto `PowerShell(Get-ChildItem *)` corresponde a `gci`, `ls` e `dir` também. A correspondência é insensível a maiúsculas e minúsculas.

Claude Code analisa o AST do PowerShell e verifica cada comando em um comando composto independentemente. Os operadores de pipeline `|`, separadores de instrução `;` e nos operadores de cadeia PowerShell 7+ `&&` e `||` dividem um comando composto em subcomandos. Uma regra deve corresponder a cada subcomando para que o comando composto seja permitido.

### Read e Edit

As regras `Edit` se aplicam a todas as ferramentas integradas que editam arquivos. Claude faz uma tentativa de melhor esforço para aplicar regras `Read` a todas as ferramentas integradas que leem arquivos como Grep e Glob, a menções `@file` em seus prompts, e à seleção e contexto de arquivo aberto que um [IDE](/pt/vs-code#the-built-in-ide-mcp-server) conectado compartilha com Claude.

<Warning>
  As regras deny de Read e Edit se aplicam às ferramentas de arquivo integradas do Claude e aos comandos de arquivo que Claude Code reconhece em Bash, como `cat`, `head`, `tail` e `sed`. Elas não se aplicam a subprocessos arbitrários que leem ou escrevem arquivos indiretamente, como um script Python ou Node que abre arquivos por conta própria. Para imposição em nível de SO que bloqueia todos os processos de acessar um caminho, [ative o sandbox](/pt/sandboxing).
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

Uma regra só corresponde a arquivos sob sua âncora, portanto a âncora determina o quão longe uma regra deny alcança. Nomes de arquivo simples seguem semântica gitignore e correspondem em qualquer profundidade, portanto `Read(.env)` e `Read(**/.env)` são equivalentes:

| Regra deny                      | Bloqueia                                                 | Não bloqueia                                            |
| ------------------------------- | -------------------------------------------------------- | ------------------------------------------------------- |
| `Read(.env)` ou `Read(**/.env)` | qualquer `.env` no ou sob o diretório atual              | `.env` em um diretório pai ou outro projeto             |
| `Read(//**/.env)`               | qualquer `.env` em qualquer lugar do sistema de arquivos | nada; a regra é ancorada na raiz do sistema de arquivos |

<Note>
  Em padrões gitignore, `*` corresponde a arquivos em um único diretório enquanto `**` corresponde recursivamente entre diretórios. Para permitir acesso a todos os arquivos, use apenas o nome da ferramenta sem parênteses: `Read`, `Edit` ou `Write`.
</Note>

Quando Claude acessa um symlink, as regras de permissão verificam dois caminhos: o próprio symlink e o arquivo para o qual ele se resolve. As regras allow e deny tratam esse par de forma diferente: as regras allow voltam a solicitar, enquanto as regras deny bloqueiam imediatamente.

* **Regras allow**: se aplicam apenas quando tanto o caminho do symlink quanto seu alvo correspondem. Um symlink dentro de um diretório permitido que aponta para fora dele ainda solicita.
* **Regras deny**: se aplicam quando o caminho do symlink ou seu alvo correspondem. Um symlink que aponta para um arquivo negado é ele próprio negado.

Por exemplo, com `Read(./project/**)` permitido e `Read(~/.ssh/**)` negado, um symlink em `./project/key` apontando para `~/.ssh/id_rsa` é bloqueado: o alvo falha na regra allow e corresponde à regra deny.

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

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)"]
  }
}
```

## Estender permissões com hooks

Os [hooks do Claude Code](/pt/hooks-guide) fornecem uma maneira de registrar comandos de shell personalizados para realizar avaliação de permissão em tempo de execução. Quando Claude Code faz uma chamada de ferramenta, os hooks PreToolUse são executados antes do prompt de permissão. A saída do hook pode negar a chamada de ferramenta, forçar um prompt ou pular o prompt para deixar a chamada prosseguir.

As decisões do hook não contornam as regras de permissão. As regras deny e ask são avaliadas independentemente do que um hook PreToolUse retorna, portanto uma regra deny correspondente bloqueia a chamada e uma regra ask correspondente ainda solicita mesmo quando o hook retornou `"allow"` ou `"ask"`. Isto preserva a precedência deny-first descrita em [Gerenciar permissões](#manage-permissions), incluindo regras deny definidas em configurações gerenciadas.

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

| Configuração                                                           | Carregado de `--add-dir`                                                                                                                                                        |
| :--------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [Skills](/pt/skills) em `.claude/skills/`                              | Sim, com recarga ao vivo                                                                                                                                                        |
| Configurações de plugin em `.claude/settings.json`                     | Apenas `enabledPlugins` e `extraKnownMarketplaces`                                                                                                                              |
| Arquivos [CLAUDE.md](/pt/memory), `.claude/rules/` e `CLAUDE.local.md` | Apenas quando `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1` está definido. `CLAUDE.local.md` adicionalmente requer a fonte de configuração `local`, que é ativada por padrão |

Subagentes, comandos e estilos de saída são descobertos do diretório de trabalho atual e seus pais, seu diretório de usuário em `~/.claude/` e configurações gerenciadas. Hooks e outras chaves `settings.json` são carregadas da pasta `.claude/` do diretório de trabalho atual sem fallback de diretório pai, juntamente com seu `~/.claude/settings.json` de usuário e configurações gerenciadas. Para compartilhar essa configuração entre projetos, use uma destas abordagens:

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
* As restrições de sistema de arquivos no sandbox combinam as configurações [`sandbox.filesystem`](/pt/sandboxing) com regras deny de Read e Edit; ambas são mescladas no limite final do sandbox
* As restrições de rede combinam regras de permissão WebFetch com as listas `allowedDomains` e `deniedDomains` do sandbox

Quando o sandboxing é ativado com `autoAllowBashIfSandboxed: true`, que é o padrão, comandos Bash em sandbox são executados sem solicitar mesmo se suas permissões incluem `ask: Bash(*)`. O limite do sandbox substitui o prompt por comando. Regras deny explícitas ainda se aplicam, e comandos `rm` ou `rmdir` que visam `/`, seu diretório inicial ou outros caminhos críticos do sistema ainda acionam um prompt. Veja [modos de sandbox](/pt/sandboxing#sandbox-modes) para alterar este comportamento.

## Configurações gerenciadas

Para organizações que precisam de controle centralizado sobre a configuração do Claude Code, administradores podem implantar configurações gerenciadas que não podem ser substituídas por configurações de usuário ou projeto. Estas configurações de política seguem o mesmo formato que arquivos de configuração regulares e podem ser entregues através de políticas MDM/nível de SO, arquivos de configuração gerenciados ou [configurações gerenciadas por servidor](/pt/server-managed-settings). Veja [arquivos de configuração](/pt/settings#settings-files) para mecanismos de entrega e locais de arquivo.

### Configurações apenas gerenciadas

As seguintes configurações são lidas apenas de configurações gerenciadas. Colocá-las em arquivos de configuração de usuário ou projeto não tem efeito.

| Configuração                                   | Descrição                                                                                                                                                                                                                                                                                                                                            |
| :--------------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `allowedChannelPlugins`                        | Lista de permissão de plugins de canal que podem enviar mensagens. Substitui a lista de permissão padrão da Anthropic quando definida. Requer `channelsEnabled: true`. Veja [Restringir quais plugins de canal podem ser executados](/pt/channels#restrict-which-channel-plugins-can-run)                                                            |
| `allowManagedHooksOnly`                        | Quando `true`, apenas hooks gerenciados, hooks SDK e hooks de plugins força-ativados em configurações gerenciadas `enabledPlugins` são carregados. Hooks de usuário, projeto e todos os outros plugins são bloqueados                                                                                                                                |
| `allowManagedMcpServersOnly`                   | Quando `true`, apenas `allowedMcpServers` de configurações gerenciadas são respeitados. `deniedMcpServers` ainda se mescla de todas as fontes. Veja [Configuração MCP gerenciada](/pt/managed-mcp)                                                                                                                                                   |
| `allowManagedPermissionRulesOnly`              | Quando `true`, impede que configurações de usuário e projeto definam regras de permissão `allow`, `ask` ou `deny`. Apenas regras em configurações gerenciadas se aplicam. Não afeta a lista de permissão do servidor MCP; para isso, defina `allowManagedMcpServersOnly`                                                                             |
| `blockedMarketplaces`                          | Lista de bloqueio de fontes de marketplace. Fontes bloqueadas são verificadas antes do download, portanto nunca tocam o sistema de arquivos. Veja [restrições de marketplace gerenciadas](/pt/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                  |
| `channelsEnabled`                              | Permitir [channels](/pt/channels) para a organização. Veja [controles empresariais](/pt/channels#enterprise-controls) para o padrão em cada plano                                                                                                                                                                                                    |
| `forceRemoteSettingsRefresh`                   | Quando `true`, bloqueia a inicialização da CLI até que as configurações gerenciadas remotas sejam buscadas recentemente e sai se a busca falhar. Veja [imposição fail-closed](/pt/server-managed-settings#enforce-fail-closed-startup)                                                                                                               |
| `pluginTrustMessage`                           | Mensagem personalizada anexada ao aviso de confiança de plugin mostrado antes da instalação                                                                                                                                                                                                                                                          |
| `sandbox.filesystem.allowManagedReadPathsOnly` | Quando `true`, apenas caminhos `filesystem.allowRead` de configurações gerenciadas são respeitados. `denyRead` ainda se mescla de todas as fontes                                                                                                                                                                                                    |
| `sandbox.network.allowManagedDomainsOnly`      | Quando `true`, apenas `allowedDomains` e regras allow `WebFetch(domain:...)` de configurações gerenciadas são respeitados. Domínios não permitidos são bloqueados automaticamente sem solicitar ao usuário. Domínios negados ainda se mesclam de todas as fontes                                                                                     |
| `strictKnownMarketplaces`                      | Controla quais marketplaces de plugin os usuários podem adicionar e instalar plugins. Veja [restrições de marketplace gerenciadas](/pt/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                                                         |
| `strictPluginOnlyCustomization`                | Bloqueia skills, agents, hooks e servidores MCP de fontes de usuário e projeto, para que possam vir apenas de plugins ou configurações gerenciadas. `true` bloqueia todas as quatro superfícies; um array como `["skills", "hooks"]` bloqueia apenas as nomeadas. Veja [`strictPluginOnlyCustomization`](/pt/settings#strictpluginonlycustomization) |
| `wslInheritsWindowsSettings`                   | Quando `true` na chave de registro HKLM do Windows ou `C:\Program Files\ClaudeCode\managed-settings.json`, WSL lê configurações gerenciadas da cadeia de política do Windows além de `/etc/claude-code`. Veja [Arquivos de configuração](/pt/settings#settings-files)                                                                                |

`disableBypassPermissionsMode` é tipicamente colocado em configurações gerenciadas para impor política organizacional, mas funciona de qualquer escopo. Um usuário pode defini-lo em suas próprias configurações para se bloquear do modo bypass.

<Note>
  Em planos Team e Enterprise, um admin ativa ou desativa [Remote Control](/pt/remote-control) e [sessões web](/pt/claude-code-on-the-web) em toda a organização em [configurações de admin do Claude Code](https://claude.ai/admin-settings/claude-code). Remote Control pode ser adicionalmente desativado por dispositivo com a configuração gerenciada [`disableRemoteControl`](/pt/settings#available-settings). Sessões web não têm chave de configurações gerenciadas por dispositivo.
</Note>

## Precedência de configurações

As regras de permissão seguem a mesma [precedência de configurações](/pt/settings#settings-precedence) que todas as outras configurações do Claude Code:

1. **Configurações gerenciadas**: não podem ser substituídas por nenhum outro nível, incluindo argumentos de linha de comando
2. **Argumentos de linha de comando**: substituições de sessão temporária
3. **Configurações de projeto local** (`.claude/settings.local.json`)
4. **Configurações de projeto compartilhado** (`.claude/settings.json`)
5. **Configurações de usuário** (`~/.claude/settings.json`)

Se uma ferramenta for negada em qualquer nível, nenhum outro nível pode permitir. Por exemplo, uma negação de configurações gerenciadas não pode ser substituída por `--allowedTools`, e `--disallowedTools` pode adicionar restrições além do que as configurações gerenciadas definem.

Os hosts de incorporação podem fornecer política gerenciada adicional por meio da opção `managedSettings` do SDK quando [`parentSettingsBehavior`](/pt/settings#settings-precedence) está definido como `"merge"`; os valores do incorporador podem apertar a política, mas não afrouxá-la.

Por exemplo, se as configurações de usuário permitirem uma permissão e as configurações de projeto a negarem, a regra de negação a bloqueia. O inverso também é verdadeiro: uma negação no nível de usuário bloqueia uma permissão no nível de projeto, porque as regras de negação de qualquer escopo são avaliadas antes das regras de permissão.

## Configurações de exemplo

Este [repositório](https://github.com/anthropics/claude-code/tree/main/examples/settings) inclui configurações de configuração inicial para cenários de implantação comuns. Use-as como pontos de partida e ajuste-as para suas necessidades.

## Veja também

* [Settings](/pt/settings): referência de configuração completa incluindo a tabela de configurações de permissão
* [Configure auto mode](/pt/auto-mode-config): diga ao classificador do modo auto qual infraestrutura sua organização confia
* [Sandboxing](/pt/sandboxing): isolamento de rede e sistema de arquivos em nível de SO para comandos Bash
* [Authentication](/pt/authentication): configure o acesso do usuário ao Claude Code
* [Security](/pt/security): salvaguardas de segurança e melhores práticas
* [Hooks](/pt/hooks-guide): automatize fluxos de trabalho e estenda avaliação de permissão
