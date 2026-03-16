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

Claude Code suporta vários modos de permissão que controlam como as ferramentas são aprovadas. Defina o `defaultMode` em seus [arquivos de configuração](/pt/settings#settings-files):

| Modo                | Descrição                                                                                                   |
| :------------------ | :---------------------------------------------------------------------------------------------------------- |
| `default`           | Comportamento padrão: solicita permissão no primeiro uso de cada ferramenta                                 |
| `acceptEdits`       | Aceita automaticamente permissões de edição de arquivo para a sessão                                        |
| `plan`              | Plan Mode: Claude pode analisar mas não modificar arquivos ou executar comandos                             |
| `dontAsk`           | Nega automaticamente ferramentas a menos que pré-aprovadas via `/permissions` ou regras `permissions.allow` |
| `bypassPermissions` | Ignora todos os prompts de permissão (requer ambiente seguro, veja aviso abaixo)                            |

<Warning>
  O modo `bypassPermissions` desabilita todas as verificações de permissão. Use apenas em ambientes isolados como contêineres ou VMs onde Claude Code não pode causar danos. Administradores podem impedir este modo definindo `disableBypassPermissionsMode` como `"disable"` em [configurações gerenciadas](#managed-settings).
</Warning>

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

Os [hooks do Claude Code](/pt/hooks-guide) fornecem uma maneira de registrar comandos de shell personalizados para realizar avaliação de permissão em tempo de execução. Quando Claude Code faz uma chamada de ferramenta, os hooks PreToolUse são executados antes do sistema de permissões, e a saída do hook pode determinar se aprova ou nega a chamada de ferramenta no lugar do sistema de permissões.

## Diretórios de trabalho

Por padrão, Claude tem acesso a arquivos no diretório onde foi iniciado. Você pode estender este acesso:

* **Durante a inicialização**: use o argumento CLI `--add-dir <path>`
* **Durante a sessão**: use o comando `/add-dir`
* **Configuração persistente**: adicione a `additionalDirectories` em [arquivos de configuração](/pt/settings#settings-files)

Arquivos em diretórios adicionais seguem as mesmas regras de permissão do diretório de trabalho original: eles se tornam legíveis sem prompts, e as permissões de edição de arquivo seguem o modo de permissão atual.

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

Algumas configurações são efetivas apenas em configurações gerenciadas:

| Configuração                              | Descrição                                                                                                                                                                                                                                                        |
| :---------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `disableBypassPermissionsMode`            | Defina como `"disable"` para impedir o modo `bypassPermissions` e a flag `--dangerously-skip-permissions`                                                                                                                                                        |
| `allowManagedPermissionRulesOnly`         | Quando `true`, impede que configurações de usuário e projeto definam regras de permissão `allow`, `ask` ou `deny`. Apenas regras em configurações gerenciadas se aplicam                                                                                         |
| `allowManagedHooksOnly`                   | Quando `true`, impede o carregamento de hooks de usuário, projeto e plugin. Apenas hooks gerenciados e hooks SDK são permitidos                                                                                                                                  |
| `allowManagedMcpServersOnly`              | Quando `true`, apenas `allowedMcpServers` de configurações gerenciadas são respeitados. `deniedMcpServers` ainda se mescla de todas as fontes. Veja [Configuração MCP gerenciada](/pt/mcp#managed-mcp-configuration)                                             |
| `blockedMarketplaces`                     | Lista de bloqueio de fontes de marketplace. Fontes bloqueadas são verificadas antes do download, portanto nunca tocam o sistema de arquivos. Veja [restrições de marketplace gerenciadas](/pt/plugin-marketplaces#managed-marketplace-restrictions)              |
| `sandbox.network.allowManagedDomainsOnly` | Quando `true`, apenas `allowedDomains` e regras allow `WebFetch(domain:...)` de configurações gerenciadas são respeitados. Domínios não permitidos são bloqueados automaticamente sem solicitar ao usuário. Domínios negados ainda se mesclam de todas as fontes |
| `strictKnownMarketplaces`                 | Controla quais marketplaces de plugin os usuários podem adicionar. Veja [restrições de marketplace gerenciadas](/pt/plugin-marketplaces#managed-marketplace-restrictions)                                                                                        |
| `allow_remote_sessions`                   | Quando `true`, permite que usuários iniciem [Remote Control](/pt/remote-control) e [sessões web](/pt/claude-code-on-the-web). Padrão é `true`. Defina como `false` para impedir acesso a sessão remota                                                           |

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

* [Configurações](/pt/settings): referência de configuração completa incluindo a tabela de configurações de permissão
* [Sandboxing](/pt/sandboxing): isolamento de rede e sistema de arquivos em nível de SO para comandos Bash
* [Autenticação](/pt/authentication): configure o acesso do usuário ao Claude Code
* [Segurança](/pt/security): salvaguardas de segurança e melhores práticas
* [Hooks](/pt/hooks-guide): automatize fluxos de trabalho e estenda avaliação de permissão
