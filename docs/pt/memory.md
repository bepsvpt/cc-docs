> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Como Claude se lembra do seu projeto

> Dê a Claude instruções persistentes com arquivos CLAUDE.md e deixe Claude acumular aprendizados automaticamente com memória automática.

Cada sessão do Claude Code começa com uma janela de contexto limpa. Dois mecanismos carregam conhecimento entre sessões:

* **Arquivos CLAUDE.md**: instruções que você escreve para dar a Claude contexto persistente
* **Memória automática**: notas que Claude escreve para si mesma com base em suas correções e preferências

Esta página cobre como:

* [Escrever e organizar arquivos CLAUDE.md](#claudemd-files)
* [Escopear regras para tipos de arquivo específicos](#organize-rules-with-clauderules) com `.claude/rules/`
* [Configurar memória automática](#auto-memory) para que Claude tome notas automaticamente
* [Solucionar problemas](#troubleshoot-memory-issues) quando as instruções não estão sendo seguidas

## CLAUDE.md vs memória automática

Claude Code tem dois sistemas de memória complementares. Ambos são carregados no início de cada conversa. Claude os trata como contexto, não como configuração imposta. Quanto mais específicas e concisas forem suas instruções, mais consistentemente Claude as seguirá.

|                  | Arquivos CLAUDE.md                                                 | Memória automática                                                              |
| :--------------- | :----------------------------------------------------------------- | :------------------------------------------------------------------------------ |
| **Quem escreve** | Você                                                               | Claude                                                                          |
| **O que contém** | Instruções e regras                                                | Aprendizados e padrões                                                          |
| **Escopo**       | Projeto, usuário ou organização                                    | Por worktree                                                                    |
| **Carregado em** | Cada sessão                                                        | Cada sessão (primeiras 200 linhas)                                              |
| **Usar para**    | Padrões de codificação, fluxos de trabalho, arquitetura do projeto | Comandos de compilação, insights de depuração, preferências que Claude descobre |

Use arquivos CLAUDE.md quando quiser guiar o comportamento de Claude. A memória automática permite que Claude aprenda com suas correções sem esforço manual.

Subagents também podem manter sua própria memória automática. Veja [configuração de subagent](/pt/sub-agents#enable-persistent-memory) para detalhes.

## Arquivos CLAUDE.md

Arquivos CLAUDE.md são arquivos markdown que dão a Claude instruções persistentes para um projeto, seu fluxo de trabalho pessoal ou toda a sua organização. Você escreve esses arquivos em texto simples; Claude os lê no início de cada sessão.

### Escolha onde colocar arquivos CLAUDE.md

Arquivos CLAUDE.md podem estar em vários locais, cada um com um escopo diferente. Locais mais específicos têm precedência sobre os mais amplos.

| Escopo                    | Localização                                                                                                                                                           | Propósito                                                  | Exemplos de caso de uso                                                               | Compartilhado com                        |
| ------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------- | ------------------------------------------------------------------------------------- | ---------------------------------------- |
| **Política gerenciada**   | • macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`<br />• Linux e WSL: `/etc/claude-code/CLAUDE.md`<br />• Windows: `C:\Program Files\ClaudeCode\CLAUDE.md` | Instruções em toda a organização gerenciadas por TI/DevOps | Padrões de codificação da empresa, políticas de segurança, requisitos de conformidade | Todos os usuários da organização         |
| **Instruções do projeto** | `./CLAUDE.md` ou `./.claude/CLAUDE.md`                                                                                                                                | Instruções compartilhadas pela equipe para o projeto       | Arquitetura do projeto, padrões de codificação, fluxos de trabalho comuns             | Membros da equipe via controle de versão |
| **Instruções do usuário** | `~/.claude/CLAUDE.md`                                                                                                                                                 | Preferências pessoais para todos os projetos               | Preferências de estilo de código, atalhos de ferramentas pessoais                     | Apenas você (todos os projetos)          |

Arquivos CLAUDE.md no diretório acima do diretório de trabalho são carregados completamente no lançamento. Arquivos CLAUDE.md em subdiretórios são carregados sob demanda quando Claude lê arquivos nesses diretórios. Veja [Como arquivos CLAUDE.md são carregados](#how-claudemd-files-load) para a ordem de resolução completa.

Para projetos grandes, você pode dividir instruções em arquivos específicos de tópicos usando [regras de projeto](#organize-rules-with-clauderules). As regras permitem que você escope instruções para tipos de arquivo específicos ou subdiretórios.

### Configure um CLAUDE.md de projeto

Um CLAUDE.md de projeto pode ser armazenado em `./CLAUDE.md` ou `./.claude/CLAUDE.md`. Crie este arquivo e adicione instruções que se apliquem a qualquer pessoa trabalhando no projeto: comandos de compilação e teste, padrões de codificação, decisões arquitetônicas, convenções de nomenclatura e fluxos de trabalho comuns. Essas instruções são compartilhadas com sua equipe através do controle de versão, então foque em padrões de nível de projeto em vez de preferências pessoais.

<Tip>
  Execute `/init` para gerar um CLAUDE.md inicial automaticamente. Claude analisa sua base de código e cria um arquivo com comandos de compilação, instruções de teste e convenções de projeto que descobre. Se um CLAUDE.md já existe, `/init` sugere melhorias em vez de sobrescrever. Refine a partir daí com instruções que Claude não descobriria por conta própria.
</Tip>

### Escreva instruções eficazes

Arquivos CLAUDE.md são carregados na janela de contexto no início de cada sessão, consumindo tokens junto com sua conversa. Como são contexto em vez de configuração imposta, como você escreve as instruções afeta o quão confiável Claude as segue. Instruções específicas, concisas e bem estruturadas funcionam melhor.

**Tamanho**: alvo de menos de 200 linhas por arquivo CLAUDE.md. Arquivos mais longos consomem mais contexto e reduzem a aderência. Se suas instruções estão crescendo muito, divida-as usando [importações](#import-additional-files) ou arquivos [`.claude/rules/`](#organize-rules-with-clauderules).

**Estrutura**: use cabeçalhos markdown e bullets para agrupar instruções relacionadas. Claude escaneia a estrutura da mesma forma que os leitores fazem: seções organizadas são mais fáceis de seguir do que parágrafos densos.

**Especificidade**: escreva instruções que sejam concretas o suficiente para verificar. Por exemplo:

* "Use indentação de 2 espaços" em vez de "Formate o código adequadamente"
* "Execute `npm test` antes de fazer commit" em vez de "Teste suas alterações"
* "Manipuladores de API vivem em `src/api/handlers/`" em vez de "Mantenha os arquivos organizados"

**Consistência**: se duas regras se contradizem, Claude pode escolher uma arbitrariamente. Revise seus arquivos CLAUDE.md, arquivos CLAUDE.md aninhados em subdiretórios e arquivos [`.claude/rules/`](#organize-rules-with-clauderules) periodicamente para remover instruções desatualizadas ou conflitantes. Em monorepos, use [`claudeMdExcludes`](#exclude-specific-claudemd-files) para pular arquivos CLAUDE.md de outras equipes que não são relevantes para seu trabalho.

### Importe arquivos adicionais

Arquivos CLAUDE.md podem importar arquivos adicionais usando a sintaxe `@path/to/import`. Arquivos importados são expandidos e carregados em contexto no lançamento junto com o CLAUDE.md que os referencia.

Caminhos relativos e absolutos são permitidos. Caminhos relativos são resolvidos em relação ao arquivo contendo a importação, não ao diretório de trabalho. Arquivos importados podem importar recursivamente outros arquivos, com uma profundidade máxima de cinco saltos.

Para trazer um README, package.json e um guia de fluxo de trabalho, referencie-os com a sintaxe `@` em qualquer lugar do seu CLAUDE.md:

```text  theme={null}
Veja @README para visão geral do projeto e @package.json para comandos npm disponíveis para este projeto.

# Instruções Adicionais
- fluxo de trabalho git @docs/git-instructions.md
```

Para preferências pessoais que você não quer fazer check-in, importe um arquivo do seu diretório home. A importação vai no CLAUDE.md compartilhado, mas o arquivo para o qual aponta fica na sua máquina:

```text  theme={null}
# Preferências Individuais
- @~/.claude/my-project-instructions.md
```

<Warning>
  A primeira vez que Claude Code encontra importações externas em um projeto, mostra um diálogo de aprovação listando os arquivos. Se você recusar, as importações permanecem desabilitadas e o diálogo não aparece novamente.
</Warning>

Para uma abordagem mais estruturada para organizar instruções, veja [`.claude/rules/`](#organize-rules-with-clauderules).

### Como arquivos CLAUDE.md são carregados

Claude Code lê arquivos CLAUDE.md caminhando para cima na árvore de diretórios a partir do seu diretório de trabalho atual, verificando cada diretório ao longo do caminho. Isso significa que se você executar Claude Code em `foo/bar/`, ele carrega instruções de `foo/bar/CLAUDE.md` e `foo/CLAUDE.md`.

Claude também descobre arquivos CLAUDE.md em subdiretórios sob seu diretório de trabalho atual. Em vez de carregá-los no lançamento, eles são incluídos quando Claude lê arquivos nesses subdiretórios.

Se você trabalha em um grande monorepo onde arquivos CLAUDE.md de outras equipes são capturados, use [`claudeMdExcludes`](#exclude-specific-claudemd-files) para pular.

#### Carregue de diretórios adicionais

A flag `--add-dir` dá a Claude acesso a diretórios adicionais fora do seu diretório de trabalho principal. Por padrão, arquivos CLAUDE.md desses diretórios não são carregados.

Para também carregar arquivos CLAUDE.md de diretórios adicionais, incluindo `CLAUDE.md`, `.claude/CLAUDE.md` e `.claude/rules/*.md`, defina a variável de ambiente `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD`:

```bash  theme={null}
CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1 claude --add-dir ../shared-config
```

### Organize regras com `.claude/rules/`

Para projetos maiores, você pode organizar instruções em múltiplos arquivos usando o diretório `.claude/rules/`. Isso mantém as instruções modulares e mais fáceis para as equipes manterem. As regras também podem ser [escopadas para caminhos de arquivo específicos](#path-specific-rules), então elas só são carregadas em contexto quando Claude trabalha com arquivos correspondentes, reduzindo ruído e economizando espaço de contexto.

<Note>
  As regras são carregadas em contexto a cada sessão ou quando arquivos correspondentes são abertos. Para instruções específicas de tarefa que não precisam estar em contexto o tempo todo, use [skills](/pt/skills) em vez disso, que só são carregadas quando você as invoca ou quando Claude determina que são relevantes para seu prompt.
</Note>

#### Configure regras

Coloque arquivos markdown no diretório `.claude/rules/` do seu projeto. Cada arquivo deve cobrir um tópico, com um nome de arquivo descritivo como `testing.md` ou `api-design.md`. Todos os arquivos `.md` são descobertos recursivamente, então você pode organizar regras em subdiretórios como `frontend/` ou `backend/`:

```text  theme={null}
seu-projeto/
├── .claude/
│   ├── CLAUDE.md           # Instruções principais do projeto
│   └── rules/
│       ├── code-style.md   # Diretrizes de estilo de código
│       ├── testing.md      # Convenções de teste
│       └── security.md     # Requisitos de segurança
```

Regras sem [frontmatter `paths`](#path-specific-rules) são carregadas no lançamento com a mesma prioridade que `.claude/CLAUDE.md`.

#### Regras específicas de caminho

As regras podem ser escopadas para arquivos específicos usando frontmatter YAML com o campo `paths`. Essas regras condicionais só se aplicam quando Claude está trabalhando com arquivos correspondentes aos padrões especificados.

```markdown  theme={null}
---
paths:
  - "src/api/**/*.ts"
---

# Regras de Desenvolvimento de API

- Todos os endpoints de API devem incluir validação de entrada
- Use o formato de resposta de erro padrão
- Inclua comentários de documentação OpenAPI
```

Regras sem um campo `paths` são carregadas incondicionalmente e se aplicam a todos os arquivos. Regras com escopo de caminho são acionadas quando Claude lê arquivos correspondentes ao padrão, não em cada uso de ferramenta.

Use padrões glob no campo `paths` para corresponder arquivos por extensão, diretório ou qualquer combinação:

| Padrão                 | Corresponde                                        |
| ---------------------- | -------------------------------------------------- |
| `**/*.ts`              | Todos os arquivos TypeScript em qualquer diretório |
| `src/**/*`             | Todos os arquivos sob o diretório `src/`           |
| `*.md`                 | Arquivos Markdown na raiz do projeto               |
| `src/components/*.tsx` | Componentes React em um diretório específico       |

Você pode especificar múltiplos padrões e usar expansão de chaves para corresponder múltiplas extensões em um padrão:

```markdown  theme={null}
---
paths:
  - "src/**/*.{ts,tsx}"
  - "lib/**/*.ts"
  - "tests/**/*.test.ts"
---
```

#### Compartilhe regras entre projetos com symlinks

O diretório `.claude/rules/` suporta symlinks, então você pode manter um conjunto compartilhado de regras e vinculá-las em múltiplos projetos. Symlinks são resolvidos e carregados normalmente, e symlinks circulares são detectados e tratados graciosamente.

Este exemplo vincula tanto um diretório compartilhado quanto um arquivo individual:

```bash  theme={null}
ln -s ~/shared-claude-rules .claude/rules/shared
ln -s ~/company-standards/security.md .claude/rules/security.md
```

#### Regras de nível de usuário

Regras pessoais em `~/.claude/rules/` se aplicam a cada projeto na sua máquina. Use-as para preferências que não são específicas do projeto:

```text  theme={null}
~/.claude/rules/
├── preferences.md    # Suas preferências pessoais de codificação
└── workflows.md      # Seus fluxos de trabalho preferidos
```

Regras de nível de usuário são carregadas antes das regras de projeto, dando às regras de projeto prioridade mais alta.

### Gerencie CLAUDE.md para grandes equipes

Para organizações implantando Claude Code em equipes, você pode centralizar instruções e controlar quais arquivos CLAUDE.md são carregados.

#### Implante CLAUDE.md em toda a organização

As organizações podem implantar um CLAUDE.md gerenciado centralmente que se aplica a todos os usuários em uma máquina. Este arquivo não pode ser excluído por configurações individuais.

<Steps>
  <Step title="Crie o arquivo no local da política gerenciada">
    * macOS: `/Library/Application Support/ClaudeCode/CLAUDE.md`
    * Linux e WSL: `/etc/claude-code/CLAUDE.md`
    * Windows: `C:\Program Files\ClaudeCode\CLAUDE.md`
  </Step>

  <Step title="Implante com seu sistema de gerenciamento de configuração">
    Use MDM, Group Policy, Ansible ou ferramentas similares para distribuir o arquivo entre máquinas de desenvolvedores. Veja [configurações gerenciadas](/pt/permissions#managed-settings) para outras opções de configuração em toda a organização.
  </Step>
</Steps>

#### Exclua arquivos CLAUDE.md específicos

Em grandes monorepos, arquivos CLAUDE.md ancestrais podem conter instruções que não são relevantes para seu trabalho. A configuração `claudeMdExcludes` permite que você pule arquivos específicos por caminho ou padrão glob.

Este exemplo exclui um CLAUDE.md de nível superior e um diretório de regras de uma pasta pai. Adicione-o a `.claude/settings.local.json` para que a exclusão permaneça local à sua máquina:

```json  theme={null}
{
  "claudeMdExcludes": [
    "**/monorepo/CLAUDE.md",
    "/home/user/monorepo/other-team/.claude/rules/**"
  ]
}
```

Padrões são correspondidos contra caminhos de arquivo absolutos usando sintaxe glob. Você pode configurar `claudeMdExcludes` em qualquer [camada de configurações](/pt/settings#settings-files): usuário, projeto, local ou política gerenciada. Arrays são mesclados entre camadas.

Arquivos CLAUDE.md de política gerenciada não podem ser excluídos. Isso garante que as instruções em toda a organização sempre se apliquem independentemente das configurações individuais.

## Memória automática

A memória automática permite que Claude acumule conhecimento entre sessões sem você escrever nada. Claude salva notas para si mesma enquanto trabalha: comandos de compilação, insights de depuração, notas de arquitetura, preferências de estilo de código e hábitos de fluxo de trabalho. Claude não salva algo a cada sessão. Ela decide o que vale a pena lembrar com base em se a informação seria útil em uma conversa futura.

<Note>
  A memória automática requer Claude Code v2.1.59 ou posterior. Verifique sua versão com `claude --version`.
</Note>

### Ative ou desative a memória automática

A memória automática está ativada por padrão. Para alterná-la, abra `/memory` em uma sessão e use o toggle de memória automática, ou defina `autoMemoryEnabled` nas configurações do seu projeto:

```json  theme={null}
{
  "autoMemoryEnabled": false
}
```

Para desabilitar a memória automática via variável de ambiente, defina `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`.

### Local de armazenamento

Cada projeto obtém seu próprio diretório de memória em `~/.claude/projects/<project>/memory/`. O caminho `<project>` é derivado do repositório git, então todos os worktrees e subdiretórios dentro do mesmo repositório compartilham um diretório de memória automática. Fora de um repositório git, a raiz do projeto é usada em vez disso.

Para armazenar memória automática em um local diferente, defina `autoMemoryDirectory` nas suas configurações de usuário ou local:

```json  theme={null}
{
  "autoMemoryDirectory": "~/my-custom-memory-dir"
}
```

Esta configuração é aceita de configurações de política, local e usuário. Não é aceita de configurações de projeto (`.claude/settings.json`) para evitar que um projeto compartilhado redirecione escritas de memória automática para locais sensíveis.

O diretório contém um ponto de entrada `MEMORY.md` e arquivos de tópico opcionais:

```text  theme={null}
~/.claude/projects/<project>/memory/
├── MEMORY.md          # Índice conciso, carregado em cada sessão
├── debugging.md       # Notas detalhadas sobre padrões de depuração
├── api-conventions.md # Decisões de design de API
└── ...                # Qualquer outro arquivo de tópico que Claude cria
```

`MEMORY.md` atua como um índice do diretório de memória. Claude lê e escreve arquivos neste diretório ao longo de sua sessão, usando `MEMORY.md` para acompanhar o que está armazenado onde.

A memória automática é local da máquina. Todos os worktrees e subdiretórios dentro do mesmo repositório git compartilham um diretório de memória automática. Os arquivos não são compartilhados entre máquinas ou ambientes em nuvem.

### Como funciona

As primeiras 200 linhas de `MEMORY.md` são carregadas no início de cada conversa. Conteúdo além da linha 200 não é carregado no início da sessão. Claude mantém `MEMORY.md` conciso movendo notas detalhadas para arquivos de tópico separados.

Este limite de 200 linhas se aplica apenas a `MEMORY.md`. Arquivos CLAUDE.md são carregados completamente independentemente do comprimento, embora arquivos mais curtos produzam melhor aderência.

Arquivos de tópico como `debugging.md` ou `patterns.md` não são carregados na inicialização. Claude os lê sob demanda usando suas ferramentas de arquivo padrão quando precisa da informação.

Claude lê e escreve arquivos de memória durante sua sessão. Quando você vê "Writing memory" ou "Recalled memory" na interface do Claude Code, Claude está ativamente atualizando ou lendo de `~/.claude/projects/<project>/memory/`.

### Audite e edite sua memória

Arquivos de memória automática são markdown simples que você pode editar ou deletar a qualquer momento. Execute [`/memory`](#view-and-edit-with-memory) para navegar e abrir arquivos de memória de dentro de uma sessão.

## Visualize e edite com `/memory`

O comando `/memory` lista todos os arquivos CLAUDE.md e rules carregados em sua sessão atual, permite que você alterne a memória automática ativada ou desativada, e fornece um link para abrir a pasta de memória automática. Selecione qualquer arquivo para abri-lo no seu editor.

Quando você pede a Claude para lembrar algo, como "sempre use pnpm, não npm" ou "lembre-se de que os testes de API requerem uma instância local de Redis," Claude salva em memória automática. Para adicionar instruções a CLAUDE.md em vez disso, peça a Claude diretamente, como "adicione isto a CLAUDE.md," ou edite o arquivo você mesmo via `/memory`.

## Solucione problemas de memória

Estes são os problemas mais comuns com CLAUDE.md e memória automática, junto com passos para depurá-los.

### Claude não está seguindo meu CLAUDE.md

O conteúdo de CLAUDE.md é entregue como uma mensagem de usuário após o prompt do sistema, não como parte do próprio prompt do sistema. Claude o lê e tenta segui-lo, mas não há garantia de conformidade estrita, especialmente para instruções vagas ou conflitantes.

Para depurar:

* Execute `/memory` para verificar se seus arquivos CLAUDE.md estão sendo carregados. Se um arquivo não estiver listado, Claude não pode vê-lo.
* Verifique se o CLAUDE.md relevante está em um local que é carregado para sua sessão (veja [Escolha onde colocar arquivos CLAUDE.md](#choose-where-to-put-claudemd-files)).
* Torne as instruções mais específicas. "Use indentação de 2 espaços" funciona melhor do que "formate o código adequadamente."
* Procure por instruções conflitantes entre arquivos CLAUDE.md. Se dois arquivos dão orientação diferente para o mesmo comportamento, Claude pode escolher um arbitrariamente.

Para instruções que você quer no nível do prompt do sistema, use [`--append-system-prompt`](/pt/cli-reference#system-prompt-flags). Isso deve ser passado a cada invocação, então é mais adequado para scripts e automação do que para uso interativo.

<Tip>
  Use o hook [`InstructionsLoaded`](/pt/hooks#instructionsloaded) para registrar exatamente quais arquivos de instrução são carregados, quando são carregados e por quê. Isso é útil para depurar regras específicas de caminho ou arquivos carregados preguiçosamente em subdiretórios.
</Tip>

### Não sei o que a memória automática salvou

Execute `/memory` e selecione a pasta de memória automática para navegar o que Claude salvou. Tudo é markdown simples que você pode ler, editar ou deletar.

### Meu CLAUDE.md é muito grande

Arquivos com mais de 200 linhas consomem mais contexto e podem reduzir a aderência. Mova conteúdo detalhado para arquivos separados referenciados com importações `@path` (veja [Importe arquivos adicionais](#import-additional-files)), ou divida suas instruções entre arquivos `.claude/rules/`.

### Instruções parecem perdidas após `/compact`

CLAUDE.md sobrevive completamente à compactação. Após `/compact`, Claude relê seu CLAUDE.md do disco e o reinjecta fresco na sessão. Se uma instrução desapareceu após compactação, ela foi dada apenas em conversa, não escrita em CLAUDE.md. Adicione-a a CLAUDE.md para torná-la persistir entre sessões.

Veja [Escreva instruções eficazes](#write-effective-instructions) para orientação sobre tamanho, estrutura e especificidade.

## Recursos relacionados

* [Skills](/pt/skills): empacote fluxos de trabalho repetíveis que carregam sob demanda
* [Settings](/pt/settings): configure o comportamento do Claude Code com arquivos de configurações
* [Manage sessions](/pt/sessions): gerencie contexto, retome conversas e execute sessões paralelas
* [Subagent memory](/pt/sub-agents#enable-persistent-memory): deixe subagents manter sua própria memória automática
