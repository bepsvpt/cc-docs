> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configurações do Claude Code

> Configure o Claude Code com configurações globais e em nível de projeto, e variáveis de ambiente.

O Claude Code oferece uma variedade de configurações para personalizar seu comportamento de acordo com suas necessidades. Você pode configurar o Claude Code executando o comando `/config` ao usar o REPL interativo, que abre uma interface de Configurações com abas onde você pode visualizar informações de status e modificar opções de configuração.

## Escopos de configuração

O Claude Code usa um **sistema de escopo** para determinar onde as configurações se aplicam e com quem são compartilhadas. Compreender os escopos ajuda você a decidir como configurar o Claude Code para uso pessoal, colaboração em equipe ou implantação empresarial.

### Escopos disponíveis

| Escopo      | Localização                                                                                               | Quem afeta                               | Compartilhado com a equipe? |
| :---------- | :-------------------------------------------------------------------------------------------------------- | :--------------------------------------- | :-------------------------- |
| **Managed** | Configurações gerenciadas pelo servidor, plist / registro, ou `managed-settings.json` em nível de sistema | Todos os usuários na máquina             | Sim (implantado por TI)     |
| **User**    | Diretório `~/.claude/`                                                                                    | Você, em todos os projetos               | Não                         |
| **Project** | `.claude/` no repositório                                                                                 | Todos os colaboradores neste repositório | Sim (confirmado no git)     |
| **Local**   | `.claude/settings.local.json`                                                                             | Você, apenas neste repositório           | Não (ignorado pelo git)     |

### Quando usar cada escopo

**Escopo Managed** é para:

* Políticas de segurança que devem ser aplicadas em toda a organização
* Requisitos de conformidade que não podem ser substituídos
* Configurações padronizadas implantadas por TI/DevOps

**Escopo User** é melhor para:

* Preferências pessoais que você deseja em todos os lugares (temas, configurações do editor)
* Ferramentas e plugins que você usa em todos os projetos
* Chaves de API e autenticação (armazenadas com segurança)

**Escopo Project** é melhor para:

* Configurações compartilhadas pela equipe (permissões, hooks, MCP servers)
* Plugins que toda a equipe deve ter
* Padronização de ferramentas entre colaboradores

**Escopo Local** é melhor para:

* Substituições pessoais para um projeto específico
* Testar configurações antes de compartilhar com a equipe
* Configurações específicas da máquina que não funcionarão para outros

### Como os escopos interagem

Quando a mesma configuração é definida em vários escopos, escopos mais específicos têm precedência:

1. **Managed** (mais alta) - não pode ser substituída por nada
2. **Argumentos de linha de comando** - substituições de sessão temporária
3. **Local** - substitui configurações de projeto e usuário
4. **Project** - substitui configurações de usuário
5. **User** (mais baixa) - se aplica quando nada mais especifica a configuração

Por exemplo, se uma permissão é permitida nas configurações do usuário, mas negada nas configurações do projeto, a configuração do projeto tem precedência e a permissão é bloqueada.

### O que usa escopos

Os escopos se aplicam a muitos recursos do Claude Code:

| Recurso         | Localização do usuário    | Localização do projeto             | Localização local              |
| :-------------- | :------------------------ | :--------------------------------- | :----------------------------- |
| **Settings**    | `~/.claude/settings.json` | `.claude/settings.json`            | `.claude/settings.local.json`  |
| **Subagents**   | `~/.claude/agents/`       | `.claude/agents/`                  | —                              |
| **MCP servers** | `~/.claude.json`          | `.mcp.json`                        | `~/.claude.json` (por projeto) |
| **Plugins**     | `~/.claude/settings.json` | `.claude/settings.json`            | `.claude/settings.local.json`  |
| **CLAUDE.md**   | `~/.claude/CLAUDE.md`     | `CLAUDE.md` ou `.claude/CLAUDE.md` | —                              |

***

## Arquivos de configuração

O arquivo `settings.json` é nosso mecanismo oficial para configurar o Claude Code através de configurações hierárquicas:

* **Configurações do usuário** são definidas em `~/.claude/settings.json` e se aplicam a todos os projetos.
* **Configurações do projeto** são salvas no diretório do seu projeto:
  * `.claude/settings.json` para configurações que são verificadas no controle de origem e compartilhadas com sua equipe
  * `.claude/settings.local.json` para configurações que não são verificadas, úteis para preferências pessoais e experimentação. O Claude Code configurará o git para ignorar `.claude/settings.local.json` quando for criado.
* **Configurações gerenciadas**: Para organizações que precisam de controle centralizado, o Claude Code suporta múltiplos mecanismos de entrega para configurações gerenciadas. Todos usam o mesmo formato JSON e não podem ser substituídos por configurações de usuário ou projeto:

  * **Configurações gerenciadas pelo servidor**: entregues dos servidores da Anthropic através do console de administração do Claude.ai. Veja [configurações gerenciadas pelo servidor](/pt/server-managed-settings).
  * **Políticas de nível MDM/SO**: entregues através de gerenciamento nativo de dispositivos no macOS e Windows:
    * macOS: domínio de preferências gerenciadas `com.anthropic.claudecode` (implantado através de perfis de configuração no Jamf, Kandji ou outras ferramentas MDM)
    * Windows: chave de registro `HKLM\SOFTWARE\Policies\ClaudeCode` com um valor `Settings` (REG\_SZ ou REG\_EXPAND\_SZ) contendo JSON (implantado através de Política de Grupo ou Intune)
    * Windows (nível de usuário): `HKCU\SOFTWARE\Policies\ClaudeCode` (prioridade de política mais baixa, usada apenas quando nenhuma fonte de nível de administrador existe)
  * **Baseado em arquivo**: `managed-settings.json` e `managed-mcp.json` implantados em diretórios do sistema:
    * macOS: `/Library/Application Support/ClaudeCode/`
    * Linux e WSL: `/etc/claude-code/`
    * Windows: `C:\Program Files\ClaudeCode\`

  Veja [configurações gerenciadas](/pt/permissions#managed-only-settings) e [Configuração MCP gerenciada](/pt/mcp#managed-mcp-configuration) para detalhes.

  <Note>
    Implantações gerenciadas também podem restringir **adições do marketplace de plugins** usando `strictKnownMarketplaces`. Para mais informações, veja [Restrições de marketplace gerenciado](/pt/plugin-marketplaces#managed-marketplace-restrictions).
  </Note>
* **Outra configuração** é armazenada em `~/.claude.json`. Este arquivo contém suas preferências (tema, configurações de notificação, modo de editor), sessão OAuth, configurações de [MCP server](/pt/mcp) para escopos de usuário e local, estado por projeto (ferramentas permitidas, configurações de confiança) e vários caches. Os MCP servers com escopo de projeto são armazenados separadamente em `.mcp.json`.

<Note>
  O Claude Code cria automaticamente backups com timestamp dos arquivos de configuração e retém os cinco backups mais recentes para evitar perda de dados.
</Note>

```JSON Exemplo settings.json theme={null}
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "allow": [
      "Bash(npm run lint)",
      "Bash(npm run test *)",
      "Read(~/.zshrc)"
    ],
    "deny": [
      "Bash(curl *)",
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)"
    ]
  },
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp"
  },
  "companyAnnouncements": [
    "Welcome to Acme Corp! Review our code guidelines at docs.acme.com",
    "Reminder: Code reviews required for all PRs",
    "New security policy in effect"
  ]
}
```

A linha `$schema` no exemplo acima aponta para o [esquema JSON oficial](https://json.schemastore.org/claude-code-settings.json) para configurações do Claude Code. Adicioná-la ao seu `settings.json` ativa o preenchimento automático e validação inline no VS Code, Cursor e qualquer outro editor que suporte validação de esquema JSON.

### Configurações disponíveis

`settings.json` suporta várias opções:

| Chave                             | Descrição                                                                                                                                                                                                                                                                                                                                                        | Exemplo                                                                 |
| :-------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------- |
| `apiKeyHelper`                    | Script personalizado, a ser executado em `/bin/sh`, para gerar um valor de autenticação. Este valor será enviado como cabeçalhos `X-Api-Key` e `Authorization: Bearer` para solicitações de modelo                                                                                                                                                               | `/bin/generate_temp_api_key.sh`                                         |
| `cleanupPeriodDays`               | Sessões inativas por mais tempo que este período são deletadas na inicialização. Definir como `0` deleta imediatamente todas as sessões. (padrão: 30 dias)                                                                                                                                                                                                       | `20`                                                                    |
| `companyAnnouncements`            | Anúncio a ser exibido aos usuários na inicialização. Se vários anúncios forem fornecidos, eles serão alternados aleatoriamente.                                                                                                                                                                                                                                  | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]` |
| `env`                             | Variáveis de ambiente que serão aplicadas a cada sessão                                                                                                                                                                                                                                                                                                          | `{"FOO": "bar"}`                                                        |
| `attribution`                     | Personalize a atribuição para commits git e pull requests. Veja [Configurações de atribuição](#attribution-settings)                                                                                                                                                                                                                                             | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                 |
| `includeCoAuthoredBy`             | **Descontinuado**: Use `attribution` em vez disso. Se deve incluir a linha `co-authored-by Claude` em commits git e pull requests (padrão: `true`)                                                                                                                                                                                                               | `false`                                                                 |
| `includeGitInstructions`          | Incluir instruções de workflow de commit e PR integradas no prompt do sistema do Claude (padrão: `true`). Defina como `false` para remover essas instruções, por exemplo, ao usar seus próprios skills de workflow git. A variável de ambiente `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` tem precedência sobre esta configuração quando definida                    | `false`                                                                 |
| `permissions`                     | Veja a tabela abaixo para a estrutura de permissões.                                                                                                                                                                                                                                                                                                             |                                                                         |
| `hooks`                           | Configure comandos personalizados para executar em eventos do ciclo de vida. Veja [documentação de hooks](/pt/hooks) para o formato                                                                                                                                                                                                                              | Veja [hooks](/pt/hooks)                                                 |
| `disableAllHooks`                 | Desabilitar todos os [hooks](/pt/hooks) e qualquer [linha de status](/pt/statusline) personalizada                                                                                                                                                                                                                                                               | `true`                                                                  |
| `allowManagedHooksOnly`           | (Apenas configurações gerenciadas) Impedir o carregamento de hooks de usuário, projeto e plugin. Apenas permite hooks gerenciados e hooks SDK. Veja [Configuração de hooks](#hook-configuration)                                                                                                                                                                 | `true`                                                                  |
| `allowedHttpHookUrls`             | Lista de permissões de padrões de URL que hooks HTTP podem almejar. Suporta `*` como curinga. Quando definido, hooks com URLs não correspondentes são bloqueados. Indefinido = sem restrição, array vazio = bloquear todos os hooks HTTP. Arrays são mesclados entre fontes de configuração. Veja [Configuração de hooks](#hook-configuration)                   | `["https://hooks.example.com/*"]`                                       |
| `httpHookAllowedEnvVars`          | Lista de permissões de nomes de variáveis de ambiente que hooks HTTP podem interpolar em cabeçalhos. Quando definido, o `allowedEnvVars` efetivo de cada hook é a interseção com esta lista. Indefinido = sem restrição. Arrays são mesclados entre fontes de configuração. Veja [Configuração de hooks](#hook-configuration)                                    | `["MY_TOKEN", "HOOK_SECRET"]`                                           |
| `allowManagedPermissionRulesOnly` | (Apenas configurações gerenciadas) Impedir que configurações de usuário e projeto definam regras de permissão `allow`, `ask` ou `deny`. Apenas regras em configurações gerenciadas se aplicam. Veja [Configurações apenas gerenciadas](/pt/permissions#managed-only-settings)                                                                                    | `true`                                                                  |
| `allowManagedMcpServersOnly`      | (Apenas configurações gerenciadas) Apenas `allowedMcpServers` de configurações gerenciadas são respeitados. `deniedMcpServers` ainda é mesclado de todas as fontes. Os usuários ainda podem adicionar MCP servers, mas apenas a lista de permissões definida pelo administrador se aplica. Veja [Configuração MCP gerenciada](/pt/mcp#managed-mcp-configuration) | `true`                                                                  |
| `model`                           | Substituir o modelo padrão a ser usado para Claude Code                                                                                                                                                                                                                                                                                                          | `"claude-sonnet-4-6"`                                                   |
| `availableModels`                 | Restringir quais modelos os usuários podem selecionar via `/model`, `--model`, ferramenta Config ou `ANTHROPIC_MODEL`. Não afeta a opção Padrão. Veja [Restringir seleção de modelo](/pt/model-config#restrict-model-selection)                                                                                                                                  | `["sonnet", "haiku"]`                                                   |
| `modelOverrides`                  | Mapear IDs de modelo Anthropic para IDs de modelo específicos do provedor, como ARNs de perfil de inferência Bedrock. Cada entrada do seletor de modelo usa seu valor mapeado ao chamar a API do provedor. Veja [Substituir IDs de modelo por versão](/pt/model-config#override-model-ids-per-version)                                                           | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                            |
| `otelHeadersHelper`               | Script para gerar cabeçalhos OpenTelemetry dinâmicos. Executa na inicialização e periodicamente (veja [Cabeçalhos dinâmicos](/pt/monitoring-usage#dynamic-headers))                                                                                                                                                                                              | `/bin/generate_otel_headers.sh`                                         |
| `statusLine`                      | Configure uma linha de status personalizada para exibir contexto. Veja [documentação de `statusLine`](/pt/statusline)                                                                                                                                                                                                                                            | `{"type": "command", "command": "~/.claude/statusline.sh"}`             |
| `fileSuggestion`                  | Configure um script personalizado para preenchimento automático de arquivo `@`. Veja [Configurações de sugestão de arquivo](#file-suggestion-settings)                                                                                                                                                                                                           | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`        |
| `respectGitignore`                | Controlar se o seletor de arquivo `@` respeita padrões `.gitignore`. Quando `true` (padrão), arquivos que correspondem aos padrões `.gitignore` são excluídos das sugestões                                                                                                                                                                                      | `false`                                                                 |
| `outputStyle`                     | Configure um estilo de saída para ajustar o prompt do sistema. Veja [documentação de estilos de saída](/pt/output-styles)                                                                                                                                                                                                                                        | `"Explanatory"`                                                         |
| `forceLoginMethod`                | Use `claudeai` para restringir o login a contas Claude.ai, `console` para restringir o login a contas Claude Console (faturamento de uso de API)                                                                                                                                                                                                                 | `claudeai`                                                              |
| `forceLoginOrgUUID`               | Especifique o UUID de uma organização para selecioná-la automaticamente durante o login, contornando a etapa de seleção de organização. Requer que `forceLoginMethod` seja definido                                                                                                                                                                              | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"`                                |
| `enableAllProjectMcpServers`      | Aprovar automaticamente todos os MCP servers definidos em arquivos `.mcp.json` do projeto                                                                                                                                                                                                                                                                        | `true`                                                                  |
| `enabledMcpjsonServers`           | Lista de MCP servers específicos de arquivos `.mcp.json` para aprovar                                                                                                                                                                                                                                                                                            | `["memory", "github"]`                                                  |
| `disabledMcpjsonServers`          | Lista de MCP servers específicos de arquivos `.mcp.json` para rejeitar                                                                                                                                                                                                                                                                                           | `["filesystem"]`                                                        |
| `allowedMcpServers`               | Quando definido em managed-settings.json, lista de permissões de MCP servers que os usuários podem configurar. Indefinido = sem restrições, array vazio = bloqueio. Se aplica a todos os escopos. A lista de negação tem precedência. Veja [Configuração MCP gerenciada](/pt/mcp#managed-mcp-configuration)                                                      | `[{ "serverName": "github" }]`                                          |
| `deniedMcpServers`                | Quando definido em managed-settings.json, lista de negação de MCP servers que são explicitamente bloqueados. Se aplica a todos os escopos, incluindo servers gerenciados. A lista de negação tem precedência sobre a lista de permissões. Veja [Configuração MCP gerenciada](/pt/mcp#managed-mcp-configuration)                                                  | `[{ "serverName": "filesystem" }]`                                      |
| `strictKnownMarketplaces`         | Quando definido em managed-settings.json, lista de permissões de marketplaces de plugin que os usuários podem adicionar. Indefinido = sem restrições, array vazio = bloqueio. Se aplica apenas a adições de marketplace. Veja [Restrições de marketplace gerenciado](/pt/plugin-marketplaces#managed-marketplace-restrictions)                                   | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                 |
| `blockedMarketplaces`             | (Apenas configurações gerenciadas) Lista de negação de fontes de marketplace. Fontes bloqueadas são verificadas antes do download, portanto nunca tocam o sistema de arquivos. Veja [Restrições de marketplace gerenciado](/pt/plugin-marketplaces#managed-marketplace-restrictions)                                                                             | `[{ "source": "github", "repo": "untrusted/plugins" }]`                 |
| `pluginTrustMessage`              | (Apenas configurações gerenciadas) Mensagem personalizada anexada ao aviso de confiança de plugin mostrado antes da instalação. Use isso para adicionar contexto específico da organização, por exemplo, para confirmar que plugins do seu marketplace interno são verificados.                                                                                  | `"All plugins from our marketplace are approved by IT"`                 |
| `awsAuthRefresh`                  | Script personalizado que modifica o diretório `.aws` (veja [configuração avançada de credenciais](/pt/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                         | `aws sso login --profile myprofile`                                     |
| `awsCredentialExport`             | Script personalizado que gera JSON com credenciais AWS (veja [configuração avançada de credenciais](/pt/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                       | `/bin/generate_aws_grant.sh`                                            |
| `alwaysThinkingEnabled`           | Ativar [pensamento estendido](/pt/common-workflows#use-extended-thinking-thinking-mode) por padrão para todas as sessões. Normalmente configurado através do comando `/config` em vez de editar diretamente                                                                                                                                                      | `true`                                                                  |
| `plansDirectory`                  | Personalize onde os arquivos de plano são armazenados. O caminho é relativo à raiz do projeto. Padrão: `~/.claude/plans`                                                                                                                                                                                                                                         | `"./plans"`                                                             |
| `showTurnDuration`                | Mostrar mensagens de duração de turno após respostas (por exemplo, "Cooked for 1m 6s"). Defina como `false` para ocultar essas mensagens                                                                                                                                                                                                                         | `true`                                                                  |
| `spinnerVerbs`                    | Personalize os verbos de ação mostrados no spinner e mensagens de duração de turno. Defina `mode` como `"replace"` para usar apenas seus verbos, ou `"append"` para adicioná-los aos padrões                                                                                                                                                                     | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                |
| `language`                        | Configure o idioma de resposta preferido do Claude (por exemplo, `"japanese"`, `"spanish"`, `"french"`). Claude responderá neste idioma por padrão                                                                                                                                                                                                               | `"japanese"`                                                            |
| `autoUpdatesChannel`              | Canal de lançamento a seguir para atualizações. Use `"stable"` para uma versão que é tipicamente cerca de uma semana antiga e pula versões com regressões principais, ou `"latest"` (padrão) para o lançamento mais recente                                                                                                                                      | `"stable"`                                                              |
| `spinnerTipsEnabled`              | Mostrar dicas no spinner enquanto Claude está trabalhando. Defina como `false` para desabilitar dicas (padrão: `true`)                                                                                                                                                                                                                                           | `false`                                                                 |
| `spinnerTipsOverride`             | Substituir dicas do spinner com strings personalizadas. `tips`: array de strings de dica. `excludeDefault`: se `true`, mostrar apenas dicas personalizadas; se `false` ou ausente, dicas personalizadas são mescladas com dicas integradas                                                                                                                       | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`       |
| `terminalProgressBarEnabled`      | Ativar a barra de progresso do terminal que mostra progresso em terminais suportados como Windows Terminal e iTerm2 (padrão: `true`)                                                                                                                                                                                                                             | `false`                                                                 |
| `prefersReducedMotion`            | Reduzir ou desabilitar animações da UI (spinners, shimmer, efeitos de flash) para acessibilidade                                                                                                                                                                                                                                                                 | `true`                                                                  |
| `fastModePerSessionOptIn`         | Quando `true`, o modo rápido não persiste entre sessões. Cada sessão começa com o modo rápido desativado, exigindo que os usuários o ativem com `/fast`. A preferência de modo rápido do usuário ainda é salva. Veja [Exigir opt-in por sessão](/pt/fast-mode#require-per-session-opt-in)                                                                        | `true`                                                                  |
| `teammateMode`                    | Como [equipe de agentes](/pt/agent-teams) companheiros são exibidos: `auto` (escolhe painéis divididos em tmux ou iTerm2, em processo caso contrário), `in-process` ou `tmux`. Veja [configurar equipes de agentes](/pt/agent-teams#set-up-agent-teams)                                                                                                          | `"in-process"`                                                          |

### Configurações de permissão

| Chaves                         | Descrição                                                                                                                                                                                                                                                                    | Exemplo                                                                |
| :----------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                        | Array de regras de permissão para permitir uso de ferramenta. Veja [Sintaxe de regra de permissão](#permission-rule-syntax) abaixo para detalhes de correspondência de padrão                                                                                                | `[ "Bash(git diff *)" ]`                                               |
| `ask`                          | Array de regras de permissão para pedir confirmação ao usar ferramenta. Veja [Sintaxe de regra de permissão](#permission-rule-syntax) abaixo                                                                                                                                 | `[ "Bash(git push *)" ]`                                               |
| `deny`                         | Array de regras de permissão para negar uso de ferramenta. Use isso para excluir arquivos sensíveis do acesso do Claude Code. Veja [Sintaxe de regra de permissão](#permission-rule-syntax) e [Limitações de permissão Bash](/pt/permissions#tool-specific-permission-rules) | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`        | [Diretórios de trabalho](/pt/permissions#working-directories) adicionais que Claude tem acesso                                                                                                                                                                               | `[ "../docs/" ]`                                                       |
| `defaultMode`                  | [Modo de permissão](/pt/permissions#permission-modes) padrão ao abrir Claude Code                                                                                                                                                                                            | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode` | Defina como `"disable"` para impedir que o modo `bypassPermissions` seja ativado. Isso desabilita o sinalizador de linha de comando `--dangerously-skip-permissions`. Veja [configurações gerenciadas](/pt/permissions#managed-only-settings)                                | `"disable"`                                                            |

### Sintaxe de regra de permissão

Regras de permissão seguem o formato `Tool` ou `Tool(specifier)`. As regras são avaliadas em ordem: regras de negação primeiro, depois ask, depois allow. A primeira regra correspondente vence.

Exemplos rápidos:

| Regra                          | Efeito                                               |
| :----------------------------- | :--------------------------------------------------- |
| `Bash`                         | Corresponde a todos os comandos Bash                 |
| `Bash(npm run *)`              | Corresponde a comandos começando com `npm run`       |
| `Read(./.env)`                 | Corresponde à leitura do arquivo `.env`              |
| `WebFetch(domain:example.com)` | Corresponde a solicitações de fetch para example.com |

Para a referência completa de sintaxe de regra, incluindo comportamento de curinga, padrões específicos de ferramenta para Read, Edit, WebFetch, MCP e Agent, e limitações de segurança de padrões Bash, veja [Sintaxe de regra de permissão](/pt/permissions#permission-rule-syntax).

### Configurações de sandbox

Configure comportamento avançado de sandboxing. O sandboxing isola comandos bash do seu sistema de arquivos e rede. Veja [Sandboxing](/pt/sandboxing) para detalhes.

| Chaves                            | Descrição                                                                                                                                                                                                                                                                                                                                                                     | Exemplo                         |
| :-------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `enabled`                         | Ativar sandboxing bash (macOS, Linux e WSL2). Padrão: false                                                                                                                                                                                                                                                                                                                   | `true`                          |
| `autoAllowBashIfSandboxed`        | Aprovar automaticamente comandos bash quando sandboxed. Padrão: true                                                                                                                                                                                                                                                                                                          | `true`                          |
| `excludedCommands`                | Comandos que devem ser executados fora do sandbox                                                                                                                                                                                                                                                                                                                             | `["git", "docker"]`             |
| `allowUnsandboxedCommands`        | Permitir que comandos sejam executados fora do sandbox através do parâmetro `dangerouslyDisableSandbox`. Quando definido como `false`, a válvula de escape `dangerouslyDisableSandbox` é completamente desabilitada e todos os comandos devem ser sandboxed (ou estar em `excludedCommands`). Útil para políticas empresariais que exigem sandboxing rigoroso. Padrão: true   | `false`                         |
| `filesystem.allowWrite`           | Caminhos adicionais onde comandos sandboxed podem escrever. Arrays são mesclados em todos os escopos de configuração: caminhos de usuário, projeto e gerenciados são combinados, não substituídos. Também mesclado com caminhos de regras de permissão `Edit(...)` allow. Veja [prefixos de caminho de sandbox](#sandbox-path-prefixes) abaixo.                               | `["//tmp/build", "~/.kube"]`    |
| `filesystem.denyWrite`            | Caminhos onde comandos sandboxed não podem escrever. Arrays são mesclados em todos os escopos de configuração. Também mesclado com caminhos de regras de permissão `Edit(...)` deny.                                                                                                                                                                                          | `["//etc", "//usr/local/bin"]`  |
| `filesystem.denyRead`             | Caminhos onde comandos sandboxed não podem ler. Arrays são mesclados em todos os escopos de configuração. Também mesclado com caminhos de regras de permissão `Read(...)` deny.                                                                                                                                                                                               | `["~/.aws/credentials"]`        |
| `network.allowUnixSockets`        | Caminhos de socket Unix acessíveis no sandbox (para agentes SSH, etc.)                                                                                                                                                                                                                                                                                                        | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`     | Permitir todas as conexões de socket Unix no sandbox. Padrão: false                                                                                                                                                                                                                                                                                                           | `true`                          |
| `network.allowLocalBinding`       | Permitir vinculação a portas localhost (apenas macOS). Padrão: false                                                                                                                                                                                                                                                                                                          | `true`                          |
| `network.allowedDomains`          | Array de domínios para permitir para tráfego de rede de saída. Suporta wildcards (por exemplo, `*.example.com`).                                                                                                                                                                                                                                                              | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly` | (Apenas configurações gerenciadas) Apenas `allowedDomains` e regras allow `WebFetch(domain:...)` de configurações gerenciadas são respeitadas. Domínios de configurações de usuário, projeto e local são ignorados. Domínios não permitidos são bloqueados automaticamente sem solicitar ao usuário. Domínios negados ainda são respeitados de todas as fontes. Padrão: false | `true`                          |
| `network.httpProxyPort`           | Porta de proxy HTTP usada se você deseja trazer seu próprio proxy. Se não especificado, Claude executará seu próprio proxy.                                                                                                                                                                                                                                                   | `8080`                          |
| `network.socksProxyPort`          | Porta de proxy SOCKS5 usada se você deseja trazer seu próprio proxy. Se não especificado, Claude executará seu próprio proxy.                                                                                                                                                                                                                                                 | `8081`                          |
| `enableWeakerNestedSandbox`       | Ativar sandbox mais fraco para ambientes Docker sem privilégios (apenas Linux e WSL2). **Reduz segurança.** Padrão: false                                                                                                                                                                                                                                                     | `true`                          |
| `enableWeakerNetworkIsolation`    | (Apenas macOS) Permitir acesso ao serviço de confiança TLS do sistema (`com.apple.trustd.agent`) no sandbox. Necessário para ferramentas baseadas em Go como `gh`, `gcloud` e `terraform` verificarem certificados TLS ao usar `httpProxyPort` com um proxy MITM e CA personalizada. **Reduz segurança** abrindo um possível caminho de exfiltração de dados. Padrão: false   | `true`                          |

#### Prefixos de caminho de sandbox

Caminhos em `filesystem.allowWrite`, `filesystem.denyWrite` e `filesystem.denyRead` suportam estes prefixos:

| Prefixo             | Significado                                          | Exemplo                                 |
| :------------------ | :--------------------------------------------------- | :-------------------------------------- |
| `//`                | Caminho absoluto da raiz do sistema de arquivos      | `//tmp/build` se torna `/tmp/build`     |
| `~/`                | Relativo ao diretório home                           | `~/.kube` se torna `$HOME/.kube`        |
| `/`                 | Relativo ao diretório do arquivo de configuração     | `/build` se torna `$SETTINGS_DIR/build` |
| `./` ou sem prefixo | Caminho relativo (resolvido pelo runtime do sandbox) | `./output`                              |

**Exemplo de configuração:**

```json  theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker"],
    "filesystem": {
      "allowWrite": ["//tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "registry.yarnpkg.com"],
      "allowUnixSockets": [
        "/var/run/docker.sock"
      ],
      "allowLocalBinding": true
    }
  }
}
```

**Restrições de sistema de arquivos e rede** podem ser configuradas de duas maneiras que são mescladas:

* **Configurações `sandbox.filesystem`** (mostradas acima): Controlam caminhos no limite do sandbox de nível de SO. Essas restrições se aplicam a todos os comandos de subprocesso (por exemplo, `kubectl`, `terraform`, `npm`), não apenas às ferramentas de arquivo do Claude.
* **Regras de permissão**: Use regras allow/deny `Edit` para controlar o acesso à ferramenta de arquivo do Claude, regras deny `Read` para bloquear leituras e regras allow/deny `WebFetch` para controlar domínios de rede. Caminhos dessas regras também são mesclados na configuração do sandbox.

### Configurações de atribuição

O Claude Code adiciona atribuição a commits git e pull requests. Estes são configurados separadamente:

* Commits usam [git trailers](https://git-scm.com/docs/git-interpret-trailers) (como `Co-Authored-By`) por padrão, que podem ser personalizados ou desabilitados
* Descrições de pull request são texto simples

| Chaves   | Descrição                                                                                         |
| :------- | :------------------------------------------------------------------------------------------------ |
| `commit` | Atribuição para commits git, incluindo qualquer trailer. String vazia oculta atribuição de commit |
| `pr`     | Atribuição para descrições de pull request. String vazia oculta atribuição de pull request        |

**Atribuição de commit padrão:**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Atribuição de pull request padrão:**

```text  theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Exemplo:**

```json  theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": ""
  }
}
```

<Note>
  A configuração `attribution` tem precedência sobre a configuração descontinuada `includeCoAuthoredBy`. Para ocultar toda atribuição, defina `commit` e `pr` como strings vazias.
</Note>

### Configurações de sugestão de arquivo

Configure um comando personalizado para preenchimento automático de caminho de arquivo `@`. A sugestão de arquivo integrada usa travessia rápida do sistema de arquivos, mas grandes monorepos podem se beneficiar de indexação específica do projeto, como um índice de arquivo pré-construído ou ferramentas personalizadas.

```json  theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

O comando é executado com as mesmas variáveis de ambiente que [hooks](/pt/hooks), incluindo `CLAUDE_PROJECT_DIR`. Ele recebe JSON via stdin com um campo `query`:

```json  theme={null}
{"query": "src/comp"}
```

Saída de caminhos de arquivo separados por nova linha para stdout (atualmente limitado a 15):

```text  theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**Exemplo:**

```bash  theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Configuração de hooks

Essas configurações controlam quais hooks são permitidos executar e o que hooks HTTP podem acessar. A configuração `allowManagedHooksOnly` pode ser configurada apenas em [configurações gerenciadas](#settings-files). As listas de permissões de URL e variável de ambiente podem ser definidas em qualquer nível de configuração e são mescladas entre fontes.

**Comportamento quando `allowManagedHooksOnly` é `true`:**

* Hooks gerenciados e hooks SDK são carregados
* Hooks de usuário, hooks de projeto e hooks de plugin são bloqueados

**Restringir URLs de hook HTTP:**

Limitar quais URLs hooks HTTP podem almejar. Suporta `*` como curinga para correspondência. Quando o array é definido, hooks HTTP que almejam URLs não correspondentes são silenciosamente bloqueados.

```json  theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**Restringir variáveis de ambiente de hook HTTP:**

Limitar quais nomes de variáveis de ambiente hooks HTTP podem interpolar em valores de cabeçalho. O `allowedEnvVars` efetivo de cada hook é a interseção de sua própria lista e esta configuração.

```json  theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### Precedência de configurações

As configurações se aplicam em ordem de precedência. De mais alta para mais baixa:

1. **Configurações gerenciadas** ([gerenciadas pelo servidor](/pt/server-managed-settings), [políticas de nível MDM/SO](#configuration-scopes) ou [configurações gerenciadas](/pt/settings#settings-files))
   * Políticas implantadas por TI através de entrega de servidor, perfis de configuração MDM, políticas de registro ou arquivos de configurações gerenciadas
   * Não podem ser substituídas por nenhum outro nível, incluindo argumentos de linha de comando
   * Dentro do nível gerenciado, a precedência é: gerenciadas pelo servidor > políticas de nível MDM/SO > `managed-settings.json` > registro HKCU (apenas Windows). Apenas uma fonte gerenciada é usada; as fontes não são mescladas.

2. **Argumentos de linha de comando**
   * Substituições temporárias para uma sessão específica

3. **Configurações de projeto local** (`.claude/settings.local.json`)
   * Configurações pessoais específicas do projeto

4. **Configurações de projeto compartilhadas** (`.claude/settings.json`)
   * Configurações de projeto compartilhadas pela equipe no controle de origem

5. **Configurações do usuário** (`~/.claude/settings.json`)
   * Configurações globais pessoais

Esta hierarquia garante que as políticas organizacionais sejam sempre aplicadas, enquanto ainda permite que equipes e indivíduos personalizem sua experiência.

Por exemplo, se suas configurações de usuário permitem `Bash(npm run *)` mas as configurações compartilhadas do projeto negam, a configuração do projeto tem precedência e o comando é bloqueado.

<Note>
  **Configurações de array são mescladas entre escopos.** Quando a mesma configuração com valor de array (como `sandbox.filesystem.allowWrite` ou `permissions.allow`) aparece em vários escopos, os arrays são **concatenados e desduplicados**, não substituídos. Isso significa que escopos de prioridade mais baixa podem adicionar entradas sem substituir aquelas definidas por escopos de prioridade mais alta, e vice-versa. Por exemplo, se configurações gerenciadas definem `allowWrite` como `["//opt/company-tools"]` e um usuário adiciona `["~/.kube"]`, ambos os caminhos são incluídos na configuração final.
</Note>

### Verificar configurações ativas

Execute `/status` dentro do Claude Code para ver quais fontes de configuração estão ativas e de onde vêm. A saída mostra cada camada de configuração (gerenciada, usuário, projeto) junto com sua origem, como `Enterprise managed settings (remote)`, `Enterprise managed settings (plist)`, `Enterprise managed settings (HKLM)` ou `Enterprise managed settings (file)`. Se um arquivo de configuração contiver erros, `/status` relata o problema para que você possa corrigi-lo.

### Pontos-chave sobre o sistema de configuração

* **Arquivos de memória (`CLAUDE.md`)**: Contêm instruções e contexto que Claude carrega na inicialização
* **Arquivos de configuração (JSON)**: Configurar permissões, variáveis de ambiente e comportamento de ferramenta
* **Skills**: Prompts personalizados que podem ser invocados com `/skill-name` ou carregados automaticamente pelo Claude
* **MCP servers**: Estender Claude Code com ferramentas e integrações adicionais
* **Precedência**: Configurações de nível superior (Managed) substituem as de nível inferior (User/Project)
* **Herança**: As configurações são mescladas, com configurações mais específicas adicionando ou substituindo as mais amplas

### Prompt do sistema

O prompt do sistema interno do Claude Code não é publicado. Para adicionar instruções personalizadas, use arquivos `CLAUDE.md` ou o sinalizador `--append-system-prompt`.

### Excluindo arquivos sensíveis

Para impedir que Claude Code acesse arquivos contendo informações sensíveis como chaves de API, segredos e arquivos de ambiente, use a configuração `permissions.deny` em seu arquivo `.claude/settings.json`:

```json  theme={null}
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Read(./build)"
    ]
  }
}
```

Isso substitui a configuração descontinuada `ignorePatterns`. Arquivos que correspondem a esses padrões são excluídos da descoberta de arquivo e resultados de pesquisa, e operações de leitura nesses arquivos são negadas.

## Configuração de subagent

O Claude Code suporta subagents de IA personalizados que podem ser configurados em níveis de usuário e projeto. Esses subagents são armazenados como arquivos Markdown com frontmatter YAML:

* **Subagents de usuário**: `~/.claude/agents/` - Disponíveis em todos os seus projetos
* **Subagents de projeto**: `.claude/agents/` - Específicos do seu projeto e podem ser compartilhados com sua equipe

Arquivos de subagent definem assistentes de IA especializados com prompts personalizados e permissões de ferramenta. Saiba mais sobre como criar e usar subagents na [documentação de subagents](/pt/sub-agents).

## Configuração de plugin

O Claude Code suporta um sistema de plugin que permite estender a funcionalidade com skills, agentes, hooks e MCP servers. Os plugins são distribuídos através de marketplaces e podem ser configurados em níveis de usuário e repositório.

### Configurações de plugin

Configurações relacionadas a plugin em `settings.json`:

```json  theme={null}
{
  "enabledPlugins": {
    "formatter@acme-tools": true,
    "deployer@acme-tools": true,
    "analyzer@security-plugins": false
  },
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": "github",
      "repo": "acme-corp/claude-plugins"
    }
  }
}
```

#### `enabledPlugins`

Controla quais plugins estão habilitados. Formato: `"plugin-name@marketplace-name": true/false`

**Escopos**:

* **Configurações de usuário** (`~/.claude/settings.json`): Preferências de plugin pessoais
* **Configurações de projeto** (`.claude/settings.json`): Plugins específicos do projeto compartilhados com a equipe
* **Configurações locais** (`.claude/settings.local.json`): Substituições por máquina (não confirmadas)

**Exemplo**:

```json  theme={null}
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}
```

#### `extraKnownMarketplaces`

Define marketplaces adicionais que devem estar disponíveis para o repositório. Normalmente usado em configurações em nível de repositório para garantir que os membros da equipe tenham acesso às fontes de plugin necessárias.

**Quando um repositório inclui `extraKnownMarketplaces`**:

1. Os membros da equipe são solicitados a instalar o marketplace quando confiam na pasta
2. Os membros da equipe são então solicitados a instalar plugins desse marketplace
3. Os usuários podem pular marketplaces ou plugins indesejados (armazenados em configurações de usuário)
4. A instalação respeita limites de confiança e requer consentimento explícito

**Exemplo**:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}
```

**Tipos de fonte de marketplace**:

* `github`: Repositório GitHub (usa `repo`)
* `git`: Qualquer URL git (usa `url`)
* `directory`: Caminho do sistema de arquivos local (usa `path`, apenas para desenvolvimento)
* `hostPattern`: Padrão regex para corresponder hosts de marketplace (usa `hostPattern`)

#### `strictKnownMarketplaces`

**Apenas configurações gerenciadas**: Controla quais marketplaces de plugin os usuários podem adicionar. Esta configuração pode ser configurada apenas em [configurações gerenciadas](/pt/settings#settings-files) e fornece aos administradores controle rigoroso sobre fontes de marketplace.

**Localizações de arquivo de configurações gerenciadas**:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux e WSL**: `/etc/claude-code/managed-settings.json`
* **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

**Características principais**:

* Disponível apenas em configurações gerenciadas (`managed-settings.json`)
* Não pode ser substituída por configurações de usuário ou projeto (precedência mais alta)
* Aplicada ANTES de operações de rede/sistema de arquivos (fontes bloqueadas nunca são executadas)
* Usa correspondência exata para especificações de fonte (incluindo `ref`, `path` para fontes git), exceto `hostPattern`, que usa correspondência regex

**Comportamento de lista de permissões**:

* `undefined` (padrão): Sem restrições - os usuários podem adicionar qualquer marketplace
* Array vazio `[]`: Bloqueio completo - os usuários não podem adicionar novos marketplaces
* Lista de fontes: Os usuários podem adicionar apenas marketplaces que correspondem exatamente

**Todos os tipos de fonte suportados**:

A lista de permissões suporta sete tipos de fonte de marketplace. A maioria das fontes usa correspondência exata, enquanto `hostPattern` usa correspondência regex contra o host do marketplace.

1. **Repositórios GitHub**:

```json  theme={null}
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

Campos: `repo` (obrigatório), `ref` (opcional: branch/tag/SHA), `path` (opcional: subdiretório)

2. **Repositórios Git**:

```json  theme={null}
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

Campos: `url` (obrigatório), `ref` (opcional: branch/tag/SHA), `path` (opcional: subdiretório)

3. **Marketplaces baseados em URL**:

```json  theme={null}
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

Campos: `url` (obrigatório), `headers` (opcional: cabeçalhos HTTP para acesso autenticado)

<Note>
  Marketplaces baseados em URL apenas baixam o arquivo `marketplace.json`. Eles não baixam arquivos de plugin do servidor. Plugins em marketplaces baseados em URL devem usar fontes externas (URLs GitHub, npm ou git) em vez de caminhos relativos. Para plugins com caminhos relativos, use um marketplace baseado em Git. Veja [Troubleshooting](/pt/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) para detalhes.
</Note>

4. **Pacotes NPM**:

```json  theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

Campos: `package` (obrigatório, suporta pacotes com escopo)

5. **Caminhos de arquivo**:

```json  theme={null}
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

Campos: `path` (obrigatório: caminho absoluto para arquivo marketplace.json)

6. **Caminhos de diretório**:

```json  theme={null}
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

Campos: `path` (obrigatório: caminho absoluto para diretório contendo `.claude-plugin/marketplace.json`)

7. **Correspondência de padrão de host**:

```json  theme={null}
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
```

Campos: `hostPattern` (obrigatório: padrão regex para corresponder contra o host do marketplace)

Use correspondência de padrão de host quando você deseja permitir todos os marketplaces de um host específico sem enumerar cada repositório individualmente. Isso é útil para organizações com servidores GitHub Enterprise ou GitLab internos onde desenvolvedores criam seus próprios marketplaces.

Extração de host por tipo de fonte:

* `github`: sempre corresponde contra `github.com`
* `git`: extrai nome de host da URL (suporta formatos HTTPS e SSH)
* `url`: extrai nome de host da URL
* `npm`, `file`, `directory`: não suportado para correspondência de padrão de host

**Exemplos de configuração**:

Exemplo: permitir apenas marketplaces específicos:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "github",
      "repo": "acme-corp/approved-plugins"
    },
    {
      "source": "github",
      "repo": "acme-corp/security-tools",
      "ref": "v2.0"
    },
    {
      "source": "url",
      "url": "https://plugins.example.com/marketplace.json"
    },
    {
      "source": "npm",
      "package": "@acme-corp/compliance-plugins"
    }
  ]
}
```

Exemplo - Desabilitar todas as adições de marketplace:

```json  theme={null}
{
  "strictKnownMarketplaces": []
}
```

Exemplo: permitir todos os marketplaces de um servidor git interno:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

**Requisitos de correspondência exata**:

Fontes de marketplace devem corresponder **exatamente** para que a adição de um usuário seja permitida. Para fontes baseadas em git (`github` e `git`), isso inclui todos os campos opcionais:

* O `repo` ou `url` deve corresponder exatamente
* O campo `ref` deve corresponder exatamente (ou ambos serem indefinidos)
* O campo `path` deve corresponder exatamente (ou ambos serem indefinidos)

Exemplos de fontes que **NÃO correspondem**:

```json  theme={null}
// Estas são DIFERENTES fontes:
{ "source": "github", "repo": "acme-corp/plugins" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }

// Estas também são DIFERENTES:
{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }
{ "source": "github", "repo": "acme-corp/plugins" }
```

**Comparação com `extraKnownMarketplaces`**:

| Aspecto                     | `strictKnownMarketplaces`                      | `extraKnownMarketplaces`                         |
| --------------------------- | ---------------------------------------------- | ------------------------------------------------ |
| **Propósito**               | Aplicação de política organizacional           | Conveniência da equipe                           |
| **Arquivo de configuração** | Apenas `managed-settings.json`                 | Qualquer arquivo de configuração                 |
| **Comportamento**           | Bloqueia adições não permitidas                | Auto-instala marketplaces ausentes               |
| **Quando aplicado**         | Antes de operações de rede/sistema de arquivos | Após prompt de confiança do usuário              |
| **Pode ser substituído**    | Não (precedência mais alta)                    | Sim (por configurações de precedência mais alta) |
| **Formato de fonte**        | Objeto de fonte direto                         | Marketplace nomeado com fonte aninhada           |
| **Caso de uso**             | Conformidade, restrições de segurança          | Onboarding, padronização                         |

**Diferença de formato**:

`strictKnownMarketplaces` usa objetos de fonte diretos:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` requer marketplaces nomeados:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**Notas importantes**:

* Restrições são verificadas ANTES de qualquer solicitação de rede ou operação de sistema de arquivos
* Quando bloqueado, os usuários veem mensagens de erro claras indicando que a fonte é bloqueada por política gerenciada
* A restrição se aplica apenas à adição de NOVOS marketplaces; marketplaces instalados anteriormente permanecem acessíveis
* Configurações gerenciadas têm a precedência mais alta e não podem ser substituídas

Veja [Restrições de marketplace gerenciado](/pt/plugin-marketplaces#managed-marketplace-restrictions) para documentação voltada para o usuário.

### Gerenciando plugins

Use o comando `/plugin` para gerenciar plugins interativamente:

* Procurar plugins disponíveis de marketplaces
* Instalar/desinstalar plugins
* Ativar/desativar plugins
* Ver detalhes do plugin (comandos, agentes, hooks fornecidos)
* Adicionar/remover marketplaces

Saiba mais sobre o sistema de plugin na [documentação de plugins](/pt/plugins).

## Variáveis de ambiente

O Claude Code suporta as seguintes variáveis de ambiente para controlar seu comportamento:

<Note>
  Todas as variáveis de ambiente também podem ser configuradas em [`settings.json`](#available-settings). Isso é útil como uma forma de definir automaticamente variáveis de ambiente para cada sessão, ou para distribuir um conjunto de variáveis de ambiente para toda sua equipe ou organização.
</Note>

| Variável                                       | Propósito                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| :--------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --- |
| `ANTHROPIC_API_KEY`                            | Chave de API enviada como cabeçalho `X-Api-Key`, normalmente para o SDK Claude (para uso interativo, execute `/login`)                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `ANTHROPIC_AUTH_TOKEN`                         | Valor personalizado para o cabeçalho `Authorization` (o valor que você definir aqui será prefixado com `Bearer `)                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `ANTHROPIC_CUSTOM_HEADERS`                     | Cabeçalhos personalizados para adicionar a solicitações (formato `Name: Value`, separados por nova linha para múltiplos cabeçalhos)                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL`                | Veja [Configuração de modelo](/pt/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `ANTHROPIC_DEFAULT_OPUS_MODEL`                 | Veja [Configuração de modelo](/pt/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `ANTHROPIC_DEFAULT_SONNET_MODEL`               | Veja [Configuração de modelo](/pt/model-config#environment-variables)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `ANTHROPIC_FOUNDRY_API_KEY`                    | Chave de API para autenticação Microsoft Foundry (veja [Microsoft Foundry](/pt/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `ANTHROPIC_FOUNDRY_BASE_URL`                   | URL base completa para o recurso Foundry (por exemplo, `https://my-resource.services.ai.azure.com/anthropic`). Alternativa a `ANTHROPIC_FOUNDRY_RESOURCE` (veja [Microsoft Foundry](/pt/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                          |     |
| `ANTHROPIC_FOUNDRY_RESOURCE`                   | Nome do recurso Foundry (por exemplo, `my-resource`). Obrigatório se `ANTHROPIC_FOUNDRY_BASE_URL` não for definido (veja [Microsoft Foundry](/pt/microsoft-foundry))                                                                                                                                                                                                                                                                                                                                                                                                                 |     |
| `ANTHROPIC_MODEL`                              | Nome da configuração de modelo a usar (veja [Configuração de modelo](/pt/model-config#environment-variables))                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `ANTHROPIC_SMALL_FAST_MODEL`                   | \[DESCONTINUADO] Nome de [modelo classe Haiku para tarefas em segundo plano](/pt/costs)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `ANTHROPIC_SMALL_FAST_MODEL_AWS_REGION`        | Substituir região AWS para o modelo classe Haiku ao usar Bedrock                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `AWS_BEARER_TOKEN_BEDROCK`                     | Chave de API Bedrock para autenticação (veja [Chaves de API Bedrock](https://aws.amazon.com/blogs/machine-learning/accelerate-ai-development-with-amazon-bedrock-api-keys/))                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `BASH_DEFAULT_TIMEOUT_MS`                      | Timeout padrão para comandos bash de longa duração                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `BASH_MAX_OUTPUT_LENGTH`                       | Número máximo de caracteres em saídas bash antes de serem truncadas no meio                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `BASH_MAX_TIMEOUT_MS`                          | Timeout máximo que o modelo pode definir para comandos bash de longa duração                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`              | Defina a porcentagem de capacidade de contexto (1-100) em que a compactação automática é acionada. Por padrão, a compactação automática é acionada em aproximadamente 95% de capacidade. Use valores mais baixos como `50` para compactar mais cedo. Valores acima do limite padrão não têm efeito. Se aplica a conversas principais e subagents. Esta porcentagem se alinha com o campo `context_window.used_percentage` disponível em [linha de status](/pt/statusline)                                                                                                            |     |
| `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR`     | Retornar ao diretório de trabalho original após cada comando Bash                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `CLAUDE_CODE_ACCOUNT_UUID`                     | UUID da conta para o usuário autenticado. Usado por chamadores SDK para fornecer informações de conta de forma síncrona, evitando uma condição de corrida onde eventos de telemetria antigos carecem de metadados de conta. Requer que `CLAUDE_CODE_USER_EMAIL` e `CLAUDE_CODE_ORGANIZATION_UUID` também sejam definidos                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD` | Defina como `1` para carregar arquivos CLAUDE.md de diretórios especificados com `--add-dir`. Por padrão, diretórios adicionais não carregam arquivos de memória                                                                                                                                                                                                                                                                                                                                                                                                                     | `1` |
| `CLAUDE_CODE_API_KEY_HELPER_TTL_MS`            | Intervalo em milissegundos em que as credenciais devem ser atualizadas (ao usar `apiKeyHelper`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_CLIENT_CERT`                      | Caminho para arquivo de certificado de cliente para autenticação mTLS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_CLIENT_KEY`                       | Caminho para arquivo de chave privada de cliente para autenticação mTLS                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`            | Frase de senha para `CLAUDE_CODE_CLIENT_KEY` criptografado (opcional)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT`               | Defina como `1` para desabilitar suporte de [janela de contexto de 1M](/pt/model-config#extended-context). Quando definido, variantes de modelo 1M não estão disponíveis no seletor de modelo. Útil para ambientes empresariais com requisitos de conformidade                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING`        | Defina como `1` para desabilitar [raciocínio adaptativo](/pt/model-config#adjust-effort-level) para Opus 4.6 e Sonnet 4.6. Quando desabilitado, esses modelos voltam ao orçamento de pensamento fixo controlado por `MAX_THINKING_TOKENS`                                                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_DISABLE_AUTO_MEMORY`              | Defina como `1` para desabilitar [memória automática](/pt/memory#auto-memory). Defina como `0` para forçar memória automática durante o rollout gradual. Quando desabilitado, Claude não cria ou carrega arquivos de memória automática                                                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS`         | Defina como `1` para remover instruções de workflow de commit e PR integradas do prompt do sistema do Claude. Útil ao usar seus próprios skills de workflow git. Tem precedência sobre a configuração [`includeGitInstructions`](#available-settings) quando definido                                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`         | Defina como `1` para desabilitar toda funcionalidade de tarefa em segundo plano, incluindo o parâmetro `run_in_background` em ferramentas Bash e subagent, auto-backgrounding e o atalho Ctrl+B                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_DISABLE_CRON`                     | Defina como `1` para desabilitar [tarefas agendadas](/pt/scheduled-tasks). O skill `/loop` e ferramentas cron ficam indisponíveis e qualquer tarefa já agendada para de disparar, incluindo tarefas que já estão em execução no meio da sessão                                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS`       | Defina como `1` para desabilitar cabeçalhos `anthropic-beta` específicos da API Anthropic. Use isso se estiver enfrentando problemas como "Unexpected value(s) for the `anthropic-beta` header" ao usar um gateway LLM com provedores de terceiros                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_DISABLE_FAST_MODE`                | Defina como `1` para desabilitar [modo rápido](/pt/fast-mode)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`          | Defina como `1` para desabilitar as pesquisas de qualidade de sessão "How is Claude doing?". Também desabilitado ao usar provedores de terceiros ou quando a telemetria está desabilitada. Veja [Pesquisas de qualidade de sessão](/pt/data-usage#session-quality-surveys)                                                                                                                                                                                                                                                                                                           |     |
| `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`     | Equivalente a definir `DISABLE_AUTOUPDATER`, `DISABLE_BUG_COMMAND`, `DISABLE_ERROR_REPORTING` e `DISABLE_TELEMETRY`                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `CLAUDE_CODE_DISABLE_TERMINAL_TITLE`           | Defina como `1` para desabilitar atualizações automáticas de título do terminal com base no contexto da conversa                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_EFFORT_LEVEL`                     | Defina o nível de esforço para modelos suportados. Valores: `low`, `medium`, `high`. Esforço mais baixo é mais rápido e barato, esforço mais alto fornece raciocínio mais profundo. Suportado em Opus 4.6 e Sonnet 4.6. Veja [Ajustar nível de esforço](/pt/model-config#adjust-effort-level)                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION`         | Defina como `false` para desabilitar sugestões de prompt (o toggle "Prompt suggestions" em `/config`). Estas são as previsões acinzentadas que aparecem em sua entrada de prompt após Claude responder. Veja [Sugestões de prompt](/pt/interactive-mode#prompt-suggestions)                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_ENABLE_TASKS`                     | Defina como `false` para reverter temporariamente para a lista TODO anterior em vez do sistema de rastreamento de tarefas. Padrão: `true`. Veja [Lista de tarefas](/pt/interactive-mode#task-list)                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_ENABLE_TELEMETRY`                 | Defina como `1` para ativar coleta de dados OpenTelemetry para métricas e logging. Obrigatório antes de configurar exportadores OTel. Veja [Monitoramento](/pt/monitoring-usage)                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_EXIT_AFTER_STOP_DELAY`            | Tempo em milissegundos para aguardar após o loop de consulta ficar ocioso antes de sair automaticamente. Útil para fluxos de trabalho automatizados e scripts usando modo SDK                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS`         | Defina como `1` para ativar [equipes de agentes](/pt/agent-teams). Equipes de agentes são experimentais e desabilitadas por padrão                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_FILE_READ_MAX_OUTPUT_TOKENS`      | Substituir o limite de token padrão para leituras de arquivo. Útil quando você precisa ler arquivos maiores na íntegra                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_HIDE_ACCOUNT_INFO`                | Defina como `1` para ocultar seu endereço de email e nome da organização da UI do Claude Code. Útil ao transmitir ou gravar                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`            | Pular auto-instalação de extensões IDE                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS`                | Defina o número máximo de tokens de saída para a maioria das solicitações. Padrão: 32.000. Máximo: 64.000. Aumentar este valor reduz a janela de contexto efetiva disponível antes que [compactação automática](/pt/costs#reduce-token-usage) seja acionada.                                                                                                                                                                                                                                                                                                                         |     |
| `CLAUDE_CODE_ORGANIZATION_UUID`                | UUID da organização para o usuário autenticado. Usado por chamadores SDK para fornecer informações de conta de forma síncrona. Requer que `CLAUDE_CODE_ACCOUNT_UUID` e `CLAUDE_CODE_USER_EMAIL` também sejam definidos                                                                                                                                                                                                                                                                                                                                                               |     |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`  | Intervalo para atualizar cabeçalhos OpenTelemetry dinâmicos em milissegundos (padrão: 1740000 / 29 minutos). Veja [Cabeçalhos dinâmicos](/pt/monitoring-usage#dynamic-headers)                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `CLAUDE_CODE_PLAN_MODE_REQUIRED`               | Auto-definido como `true` em [equipe de agentes](/pt/agent-teams) companheiros que exigem aprovação de plano. Somente leitura: definido pelo Claude Code ao gerar companheiros. Veja [exigir aprovação de plano](/pt/agent-teams#require-plan-approval-for-teammates)                                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`            | Timeout em milissegundos para operações git ao instalar ou atualizar plugins (padrão: 120000). Aumente este valor para repositórios grandes ou conexões de rede lentas. Veja [Operações Git expiram](/pt/plugin-marketplaces#git-operations-time-out)                                                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_PROXY_RESOLVES_HOSTS`             | Defina como `true` para permitir que o proxy execute resolução DNS em vez do chamador. Opt-in para ambientes onde o proxy deve lidar com resolução de nome de host                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_SHELL`                            | Substituir detecção automática de shell. Útil quando seu shell de login difere do seu shell de trabalho preferido (por exemplo, `bash` vs `zsh`)                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `CLAUDE_CODE_SHELL_PREFIX`                     | Prefixo de comando para envolver todos os comandos bash (por exemplo, para logging ou auditoria). Exemplo: `/path/to/logger.sh` executará `/path/to/logger.sh <command>`                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `CLAUDE_CODE_SIMPLE`                           | Defina como `1` para executar com um prompt do sistema mínimo e apenas as ferramentas Bash, leitura de arquivo e edição de arquivo. Desabilita ferramentas MCP, anexos, hooks e arquivos CLAUDE.md                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_SKIP_BEDROCK_AUTH`                | Pular autenticação AWS para Bedrock (por exemplo, ao usar um gateway LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `CLAUDE_CODE_SKIP_FOUNDRY_AUTH`                | Pular autenticação Azure para Microsoft Foundry (por exemplo, ao usar um gateway LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `CLAUDE_CODE_SKIP_VERTEX_AUTH`                 | Pular autenticação Google para Vertex (por exemplo, ao usar um gateway LLM)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_SUBAGENT_MODEL`                   | Veja [Configuração de modelo](/pt/model-config)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_TASK_LIST_ID`                     | Compartilhar uma lista de tarefas entre sessões. Defina o mesmo ID em múltiplas instâncias do Claude Code para coordenar em uma lista de tarefas compartilhada. Veja [Lista de tarefas](/pt/interactive-mode#task-list)                                                                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_TEAM_NAME`                        | Nome da equipe de agentes à qual este companheiro pertence. Definido automaticamente em membros de [equipe de agentes](/pt/agent-teams)                                                                                                                                                                                                                                                                                                                                                                                                                                              |     |
| `CLAUDE_CODE_TMPDIR`                           | Substituir o diretório temporário usado para arquivos temporários internos. Claude Code anexa `/claude/` a este caminho. Padrão: `/tmp` em Unix/macOS, `os.tmpdir()` no Windows                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_USER_EMAIL`                       | Endereço de email para o usuário autenticado. Usado por chamadores SDK para fornecer informações de conta de forma síncrona. Requer que `CLAUDE_CODE_ACCOUNT_UUID` e `CLAUDE_CODE_ORGANIZATION_UUID` também sejam definidos                                                                                                                                                                                                                                                                                                                                                          |     |
| `CLAUDE_CODE_USE_BEDROCK`                      | Usar [Bedrock](/pt/amazon-bedrock)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `CLAUDE_CODE_USE_FOUNDRY`                      | Usar [Microsoft Foundry](/pt/microsoft-foundry)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |     |
| `CLAUDE_CODE_USE_VERTEX`                       | Usar [Vertex](/pt/google-vertex-ai)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `CLAUDE_CONFIG_DIR`                            | Personalizar onde Claude Code armazena seus arquivos de configuração e dados                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `DISABLE_AUTOUPDATER`                          | Defina como `1` para desabilitar atualizações automáticas.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `DISABLE_BUG_COMMAND`                          | Defina como `1` para desabilitar o comando `/bug`                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `DISABLE_COST_WARNINGS`                        | Defina como `1` para desabilitar mensagens de aviso de custo                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |     |
| `DISABLE_ERROR_REPORTING`                      | Defina como `1` para optar por não participar de relatório de erro Sentry                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `DISABLE_INSTALLATION_CHECKS`                  | Defina como `1` para desabilitar avisos de instalação. Use apenas ao gerenciar manualmente o local de instalação, pois isso pode mascarar problemas com instalações padrão                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `DISABLE_NON_ESSENTIAL_MODEL_CALLS`            | Defina como `1` para desabilitar chamadas de modelo para caminhos não críticos como texto de sabor                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `DISABLE_PROMPT_CACHING`                       | Defina como `1` para desabilitar prompt caching para todos os modelos (tem precedência sobre configurações por modelo)                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `DISABLE_PROMPT_CACHING_HAIKU`                 | Defina como `1` para desabilitar prompt caching para modelos Haiku                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `DISABLE_PROMPT_CACHING_OPUS`                  | Defina como `1` para desabilitar prompt caching para modelos Opus                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `DISABLE_PROMPT_CACHING_SONNET`                | Defina como `1` para desabilitar prompt caching para modelos Sonnet                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `DISABLE_TELEMETRY`                            | Defina como `1` para optar por não participar de telemetria Statsig (note que eventos Statsig não incluem dados do usuário como código, caminhos de arquivo ou comandos bash)                                                                                                                                                                                                                                                                                                                                                                                                        |     |
| `ENABLE_CLAUDEAI_MCP_SERVERS`                  | Defina como `false` para desabilitar [MCP servers claude.ai](/pt/mcp#use-mcp-servers-from-claudeai) no Claude Code. Habilitado por padrão para usuários conectados                                                                                                                                                                                                                                                                                                                                                                                                                   |     |
| `ENABLE_TOOL_SEARCH`                           | Controla [busca de ferramenta MCP](/pt/mcp#scale-with-mcp-tool-search). Valores: `auto` (padrão, ativa em 10% de contexto), `auto:N` (limite personalizado, por exemplo, `auto:5` para 5%), `true` (sempre ativado), `false` (desabilitado)                                                                                                                                                                                                                                                                                                                                          |     |
| `FORCE_AUTOUPDATE_PLUGINS`                     | Defina como `true` para forçar auto-atualizações de plugin mesmo quando o auto-atualizador principal está desabilitado via `DISABLE_AUTOUPDATER`                                                                                                                                                                                                                                                                                                                                                                                                                                     |     |
| `HTTP_PROXY`                                   | Especifique servidor proxy HTTP para conexões de rede                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |     |
| `HTTPS_PROXY`                                  | Especifique servidor proxy HTTPS para conexões de rede                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |     |
| `IS_DEMO`                                      | Defina como `true` para ativar modo demo: oculta email e organização da UI, pula onboarding e oculta comandos internos. Útil para transmitir ou gravar sessões                                                                                                                                                                                                                                                                                                                                                                                                                       |     |
| `MAX_MCP_OUTPUT_TOKENS`                        | Número máximo de tokens permitidos em respostas de ferramenta MCP. Claude Code exibe um aviso quando a saída excede 10.000 tokens (padrão: 25000)                                                                                                                                                                                                                                                                                                                                                                                                                                    |     |
| `MAX_THINKING_TOKENS`                          | Substituir o orçamento de token de [pensamento estendido](https://platform.claude.com/docs/en/build-with-claude/extended-thinking). O pensamento é ativado no orçamento máximo (31.999 tokens) por padrão. Use isso para limitar o orçamento (por exemplo, `MAX_THINKING_TOKENS=10000`) ou desabilitar pensamento completamente (`MAX_THINKING_TOKENS=0`). Para Opus 4.6, a profundidade de pensamento é controlada por [nível de esforço](/pt/model-config#adjust-effort-level) em vez disso, e esta variável é ignorada a menos que definida como `0` para desabilitar pensamento. |     |
| `MCP_CLIENT_SECRET`                            | Segredo de cliente OAuth para MCP servers que exigem [credenciais pré-configuradas](/pt/mcp#use-pre-configured-oauth-credentials). Evita o prompt interativo ao adicionar um servidor com `--client-secret`                                                                                                                                                                                                                                                                                                                                                                          |     |
| `MCP_OAUTH_CALLBACK_PORT`                      | Porta fixa para o callback de redirecionamento OAuth, como alternativa a `--callback-port` ao adicionar um MCP server com [credenciais pré-configuradas](/pt/mcp#use-pre-configured-oauth-credentials)                                                                                                                                                                                                                                                                                                                                                                               |     |
| `MCP_TIMEOUT`                                  | Timeout em milissegundos para inicialização de MCP server                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `MCP_TOOL_TIMEOUT`                             | Timeout em milissegundos para execução de ferramenta MCP                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `NO_PROXY`                                     | Lista de domínios e IPs para os quais as solicitações serão emitidas diretamente, contornando proxy                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |     |
| `SLASH_COMMAND_TOOL_CHAR_BUDGET`               | Substituir o orçamento de caracteres para metadados de skill mostrados à [ferramenta Skill](/pt/skills#control-who-invokes-a-skill). O orçamento é dimensionado dinamicamente em 2% da janela de contexto, com fallback de 16.000 caracteres. Nome legado mantido para compatibilidade com versões anteriores                                                                                                                                                                                                                                                                        |     |
| `USE_BUILTIN_RIPGREP`                          | Defina como `0` para usar `rg` instalado no sistema em vez de `rg` incluído com Claude Code                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |     |
| `VERTEX_REGION_CLAUDE_3_5_HAIKU`               | Substituir região para Claude 3.5 Haiku ao usar Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |     |
| `VERTEX_REGION_CLAUDE_3_7_SONNET`              | Substituir região para Claude 3.7 Sonnet ao usar Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `VERTEX_REGION_CLAUDE_4_0_OPUS`                | Substituir região para Claude 4.0 Opus ao usar Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |
| `VERTEX_REGION_CLAUDE_4_0_SONNET`              | Substituir região para Claude 4.0 Sonnet ao usar Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |     |
| `VERTEX_REGION_CLAUDE_4_1_OPUS`                | Substituir região para Claude 4.1 Opus ao usar Vertex AI                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |     |

## Ferramentas disponíveis para Claude

O Claude Code tem acesso a um conjunto de ferramentas poderosas que ajudam a entender e modificar sua base de código:

| Ferramenta               | Descrição                                                                                                                                                                                                                                                                                                                                                                                                                                           | Permissão Obrigatória |
| :----------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :-------------------- |
| **Agent**                | Gera um [subagent](/pt/sub-agents) com sua própria janela de contexto para lidar com uma tarefa                                                                                                                                                                                                                                                                                                                                                     | Não                   |
| **AskUserQuestion**      | Faz perguntas de múltipla escolha para reunir requisitos ou esclarecer ambiguidade                                                                                                                                                                                                                                                                                                                                                                  | Não                   |
| **Bash**                 | Executa comandos shell em seu ambiente. Veja [Comportamento da ferramenta Bash](#bash-tool-behavior)                                                                                                                                                                                                                                                                                                                                                | Sim                   |
| **CronCreate**           | Agenda uma tarefa recorrente ou única dentro da sessão atual (desaparece quando Claude sai). Veja [tarefas agendadas](/pt/scheduled-tasks)                                                                                                                                                                                                                                                                                                          | Não                   |
| **CronDelete**           | Cancela uma tarefa agendada por ID                                                                                                                                                                                                                                                                                                                                                                                                                  | Não                   |
| **CronList**             | Lista todas as tarefas agendadas na sessão                                                                                                                                                                                                                                                                                                                                                                                                          | Não                   |
| **Edit**                 | Faz edições direcionadas em arquivos específicos                                                                                                                                                                                                                                                                                                                                                                                                    | Sim                   |
| **EnterPlanMode**        | Muda para modo de plano para projetar uma abordagem antes de codificar                                                                                                                                                                                                                                                                                                                                                                              | Não                   |
| **EnterWorktree**        | Cria um [git worktree](/pt/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) isolado e muda para ele                                                                                                                                                                                                                                                                                                                           | Não                   |
| **ExitPlanMode**         | Apresenta um plano para aprovação e sai do modo de plano                                                                                                                                                                                                                                                                                                                                                                                            | Sim                   |
| **ExitWorktree**         | Sai de uma sessão worktree e retorna ao diretório original                                                                                                                                                                                                                                                                                                                                                                                          | Não                   |
| **Glob**                 | Encontra arquivos com base em correspondência de padrão                                                                                                                                                                                                                                                                                                                                                                                             | Não                   |
| **Grep**                 | Pesquisa padrões em conteúdo de arquivo                                                                                                                                                                                                                                                                                                                                                                                                             | Não                   |
| **ListMcpResourcesTool** | Lista recursos expostos por [MCP servers](/pt/mcp) conectados                                                                                                                                                                                                                                                                                                                                                                                       | Não                   |
| **LSP**                  | Inteligência de código via servidores de linguagem. Relata erros de tipo e avisos automaticamente após edições de arquivo. Também suporta operações de navegação: pular para definições, encontrar referências, obter informações de tipo, listar símbolos, encontrar implementações, rastrear hierarquias de chamadas. Requer um [plugin de inteligência de código](/pt/discover-plugins#code-intelligence) e seu binário de servidor de linguagem | Não                   |
| **NotebookEdit**         | Modifica células de notebook Jupyter                                                                                                                                                                                                                                                                                                                                                                                                                | Sim                   |
| **Read**                 | Lê o conteúdo de arquivos                                                                                                                                                                                                                                                                                                                                                                                                                           | Não                   |
| **ReadMcpResourceTool**  | Lê um recurso MCP específico por URI                                                                                                                                                                                                                                                                                                                                                                                                                | Não                   |
| **Skill**                | Executa um [skill](/pt/skills#control-who-invokes-a-skill) dentro da conversa principal                                                                                                                                                                                                                                                                                                                                                             | Sim                   |
| **TaskCreate**           | Cria uma nova tarefa na lista de tarefas                                                                                                                                                                                                                                                                                                                                                                                                            | Não                   |
| **TaskGet**              | Recupera detalhes completos para uma tarefa específica                                                                                                                                                                                                                                                                                                                                                                                              | Não                   |
| **TaskList**             | Lista todas as tarefas com seu status atual                                                                                                                                                                                                                                                                                                                                                                                                         | Não                   |
| **TaskOutput**           | Recupera saída de uma tarefa em segundo plano                                                                                                                                                                                                                                                                                                                                                                                                       | Não                   |
| **TaskStop**             | Mata uma tarefa em execução por ID                                                                                                                                                                                                                                                                                                                                                                                                                  | Não                   |
| **TaskUpdate**           | Atualiza status da tarefa, dependências, detalhes ou deleta tarefas                                                                                                                                                                                                                                                                                                                                                                                 | Não                   |
| **TodoWrite**            | Gerencia a lista de verificação de tarefas da sessão. Disponível em modo não interativo e [Agent SDK](/pt/headless); sessões interativas usam TaskCreate, TaskGet, TaskList e TaskUpdate em vez disso                                                                                                                                                                                                                                               | Não                   |
| **ToolSearch**           | Pesquisa e carrega ferramentas adiadas quando [busca de ferramenta](/pt/mcp#scale-with-mcp-tool-search) está habilitada                                                                                                                                                                                                                                                                                                                             | Não                   |
| **WebFetch**             | Busca conteúdo de uma URL especificada                                                                                                                                                                                                                                                                                                                                                                                                              | Sim                   |
| **WebSearch**            | Realiza buscas na web                                                                                                                                                                                                                                                                                                                                                                                                                               | Sim                   |
| **Write**                | Cria ou sobrescreve arquivos                                                                                                                                                                                                                                                                                                                                                                                                                        | Sim                   |

Regras de permissão podem ser configuradas usando `/allowed-tools` ou em [configurações de permissão](/pt/settings#available-settings). Veja também [Regras de permissão específicas de ferramenta](/pt/permissions#tool-specific-permission-rules).

### Comportamento da ferramenta Bash

A ferramenta Bash executa comandos shell com o seguinte comportamento de persistência:

* **Diretório de trabalho persiste**: Quando Claude muda o diretório de trabalho (por exemplo, `cd /path/to/dir`), comandos Bash subsequentes serão executados naquele diretório. Você pode usar `CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR=1` para retornar ao diretório do projeto após cada comando.
* **Variáveis de ambiente NÃO persistem**: Variáveis de ambiente definidas em um comando Bash (por exemplo, `export MY_VAR=value`) **não** estão disponíveis em comandos Bash subsequentes. Cada comando Bash é executado em um ambiente shell fresco.

Para disponibilizar variáveis de ambiente em comandos Bash, você tem **três opções**:

**Opção 1: Ativar ambiente antes de iniciar Claude Code** (abordagem mais simples)

Ative seu ambiente virtual em seu terminal antes de iniciar Claude Code:

```bash  theme={null}
conda activate myenv
# ou: source /path/to/venv/bin/activate
claude
```

Isso funciona para ambientes shell, mas variáveis de ambiente definidas dentro dos comandos Bash do Claude não persistirão entre comandos.

**Opção 2: Definir CLAUDE\_ENV\_FILE antes de iniciar Claude Code** (configuração de ambiente persistente)

Exporte o caminho para um script shell contendo sua configuração de ambiente:

```bash  theme={null}
export CLAUDE_ENV_FILE=/path/to/env-setup.sh
claude
```

Onde `/path/to/env-setup.sh` contém:

```bash  theme={null}
conda activate myenv
# ou: source /path/to/venv/bin/activate
# ou: export MY_VAR=value
```

Claude Code fornecerá este arquivo antes de cada comando Bash, tornando o ambiente persistente em todos os comandos.

**Opção 3: Usar um hook SessionStart** (configuração específica do projeto)

Configure em `.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [{
      "matcher": "startup",
      "hooks": [{
        "type": "command",
        "command": "echo 'conda activate myenv' >> \"$CLAUDE_ENV_FILE\""
      }]
    }]
  }
}
```

O hook escreve em `$CLAUDE_ENV_FILE`, que é então fornecido antes de cada comando Bash. Isso é ideal para configurações de projeto compartilhadas com a equipe.

Veja [hooks SessionStart](/pt/hooks#persist-environment-variables) para mais detalhes sobre a Opção 3.

### Estendendo ferramentas com hooks

Você pode executar comandos personalizados antes ou depois de qualquer ferramenta ser executada usando [hooks do Claude Code](/pt/hooks-guide).

Por exemplo, você pode executar automaticamente um formatador Python após Claude modificar arquivos Python, ou impedir modificações em arquivos de configuração de produção bloqueando operações Write em certos caminhos.

## Veja também

* [Permissões](/pt/permissions): sistema de permissões, sintaxe de regra, padrões específicos de ferramenta e políticas gerenciadas
* [Autenticação](/pt/authentication): configurar acesso do usuário ao Claude Code
* [Troubleshooting](/pt/troubleshooting): soluções para problemas comuns de configuração
