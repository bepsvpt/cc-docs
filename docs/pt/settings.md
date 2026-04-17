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

O escopo **Managed** é para:

* Políticas de segurança que devem ser aplicadas em toda a organização
* Requisitos de conformidade que não podem ser substituídos
* Configurações padronizadas implantadas por TI/DevOps

O escopo **User** é melhor para:

* Preferências pessoais que você deseja em todos os lugares (temas, configurações do editor)
* Ferramentas e plugins que você usa em todos os projetos
* Chaves de API e autenticação (armazenadas com segurança)

O escopo **Project** é melhor para:

* Configurações compartilhadas pela equipe (permissões, hooks, MCP servers)
* Plugins que toda a equipe deve ter
* Padronização de ferramentas entre colaboradores

O escopo **Local** é melhor para:

* Substituições pessoais para um projeto específico
* Testar configurações antes de compartilhar com a equipe
* Configurações específicas da máquina que não funcionarão para outros

### Como os escopos interagem

Quando a mesma configuração é definida em vários escopos, escopos mais específicos têm precedência:

1. **Managed** (mais alta) - não pode ser substituída por nada
2. **Argumentos de linha de comando** - substituições de sessão temporárias
3. **Local** - substitui configurações de projeto e usuário
4. **Project** - substitui configurações de usuário
5. **User** (mais baixa) - se aplica quando nada mais especifica a configuração

Por exemplo, se uma permissão é permitida nas configurações do usuário, mas negada nas configurações do projeto, a configuração do projeto tem precedência e a permissão é bloqueada.

### O que usa escopos

Os escopos se aplicam a muitos recursos do Claude Code:

| Recurso         | Localização do usuário    | Localização do projeto             | Localização local              |
| :-------------- | :------------------------ | :--------------------------------- | :----------------------------- |
| **Settings**    | `~/.claude/settings.json` | `.claude/settings.json`            | `.claude/settings.local.json`  |
| **Subagents**   | `~/.claude/agents/`       | `.claude/agents/`                  | Nenhum                         |
| **MCP servers** | `~/.claude.json`          | `.mcp.json`                        | `~/.claude.json` (por projeto) |
| **Plugins**     | `~/.claude/settings.json` | `.claude/settings.json`            | `.claude/settings.local.json`  |
| **CLAUDE.md**   | `~/.claude/CLAUDE.md`     | `CLAUDE.md` ou `.claude/CLAUDE.md` | `CLAUDE.local.md`              |

***

## Arquivos de configuração

O arquivo `settings.json` é o mecanismo oficial para configurar o Claude Code através de configurações hierárquicas:

* As **configurações do usuário** são definidas em `~/.claude/settings.json` e se aplicam a todos os projetos.
* As **configurações do projeto** são salvas no diretório do seu projeto:
  * `.claude/settings.json` para configurações que são verificadas no controle de origem e compartilhadas com sua equipe
  * `.claude/settings.local.json` para configurações que não são verificadas, úteis para preferências pessoais e experimentação. O Claude Code configurará o git para ignorar `.claude/settings.local.json` quando for criado.
* **Configurações gerenciadas**: Para organizações que precisam de controle centralizado, o Claude Code suporta múltiplos mecanismos de entrega para configurações gerenciadas. Todos usam o mesmo formato JSON e não podem ser substituídos por configurações de usuário ou projeto:

  * **Configurações gerenciadas pelo servidor**: entregues dos servidores da Anthropic através do console de administração do Claude.ai. Veja [configurações gerenciadas pelo servidor](/pt/server-managed-settings).
  * **Políticas de nível MDM/SO**: entregues através do gerenciamento nativo de dispositivos no macOS e Windows:
    * macOS: domínio de preferências gerenciadas `com.anthropic.claudecode` (implantado via perfis de configuração em Jamf, Iru (Kandji), ou outras ferramentas MDM)
    * Windows: chave de registro `HKLM\SOFTWARE\Policies\ClaudeCode` com um valor `Settings` (REG\_SZ ou REG\_EXPAND\_SZ) contendo JSON (implantado via Política de Grupo ou Intune)
    * Windows (nível de usuário): `HKCU\SOFTWARE\Policies\ClaudeCode` (prioridade de política mais baixa, usada apenas quando nenhuma fonte de nível de administrador existe)
  * **Baseado em arquivo**: `managed-settings.json` e `managed-mcp.json` implantados em diretórios do sistema:

    * macOS: `/Library/Application Support/ClaudeCode/`
    * Linux e WSL: `/etc/claude-code/`
    * Windows: `C:\Program Files\ClaudeCode\`

    <Warning>
      O caminho legado do Windows `C:\ProgramData\ClaudeCode\managed-settings.json` não é mais suportado a partir da v2.1.75. Administradores que implantaram configurações nesse local devem migrar arquivos para `C:\Program Files\ClaudeCode\managed-settings.json`.
    </Warning>

    Configurações gerenciadas baseadas em arquivo também suportam um diretório drop-in em `managed-settings.d/` no mesmo diretório do sistema ao lado de `managed-settings.json`. Isto permite que equipes separadas implantem fragmentos de política independentes sem coordenar edições em um único arquivo.

    Seguindo a convenção systemd, `managed-settings.json` é mesclado primeiro como base, então todos os arquivos `*.json` no diretório drop-in são classificados alfabeticamente e mesclados por cima. Arquivos posteriores substituem anteriores para valores escalares; arrays são concatenados e desduplicados; objetos são mesclados profundamente. Arquivos ocultos começando com `.` são ignorados.

    Use prefixos numéricos para controlar a ordem de mesclagem, por exemplo `10-telemetry.json` e `20-security.json`.

  Veja [configurações gerenciadas](/pt/permissions#managed-only-settings) e [Configuração MCP gerenciada](/pt/mcp#managed-mcp-configuration) para detalhes.

  Este [repositório](https://github.com/anthropics/claude-code/tree/main/examples/mdm) inclui modelos de implantação iniciais para Jamf, Iru (Kandji), Intune, e Política de Grupo. Use estes como pontos de partida e ajuste-os para suas necessidades.

  <Note>
    Implantações gerenciadas também podem restringir **adições ao marketplace de plugins** usando `strictKnownMarketplaces`. Para mais informações, veja [Restrições de marketplace gerenciado](/pt/plugin-marketplaces#managed-marketplace-restrictions).
  </Note>
* **Outra configuração** é armazenada em `~/.claude.json`. Este arquivo contém suas preferências (tema, configurações de notificação, modo do editor), sessão OAuth, configurações de [MCP server](/pt/mcp) para escopos de usuário e local, estado por projeto (ferramentas permitidas, configurações de confiança), e vários caches. Os MCP servers com escopo de projeto são armazenados separadamente em `.mcp.json`.

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

O esquema publicado é atualizado periodicamente e pode não incluir configurações adicionadas nos lançamentos CLI mais recentes, então um aviso de validação em um campo documentado recentemente não significa necessariamente que sua configuração é inválida.

### Configurações disponíveis

`settings.json` suporta várias opções:

| Chave                             | Descrição                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | Exemplo                                                                                                                        |
| :-------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------------------- |
| `agent`                           | Executar a thread principal como um subagent nomeado. Aplica o prompt do sistema, restrições de ferramenta e modelo do subagent. Veja [Invocar subagents explicitamente](/pt/sub-agents#invoke-subagents-explicitly)                                                                                                                                                                                                                                                                                                                                                                                   | `"code-reviewer"`                                                                                                              |
| `allowedChannelPlugins`           | (Apenas configurações gerenciadas) Lista de permissões de plugins de canal que podem enviar mensagens. Substitui a lista de permissões padrão da Anthropic quando definido. Indefinido = voltar para o padrão, array vazio = bloquear todos os plugins de canal. Requer `channelsEnabled: true`. Veja [Restringir quais plugins de canal podem executar](/pt/channels#restrict-which-channel-plugins-can-run)                                                                                                                                                                                          | `[{ "marketplace": "claude-plugins-official", "plugin": "telegram" }]`                                                         |
| `allowedHttpHookUrls`             | Lista de permissões de padrões de URL que hooks HTTP podem almejar. Suporta `*` como curinga. Quando definido, hooks com URLs não correspondentes são bloqueados. Indefinido = sem restrição, array vazio = bloquear todos os hooks HTTP. Arrays se mesclam entre fontes de configuração. Veja [Configuração de hooks](#hook-configuration)                                                                                                                                                                                                                                                            | `["https://hooks.example.com/*"]`                                                                                              |
| `allowedMcpServers`               | Quando definido em managed-settings.json, lista de permissões de MCP servers que os usuários podem configurar. Indefinido = sem restrições, array vazio = bloqueio. Se aplica a todos os escopos. A lista de negação tem precedência. Veja [Configuração MCP gerenciada](/pt/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                            | `[{ "serverName": "github" }]`                                                                                                 |
| `allowManagedHooksOnly`           | (Apenas configurações gerenciadas) Apenas hooks gerenciados, hooks SDK, e hooks de plugins força-habilitados em configurações gerenciadas `enabledPlugins` são carregados. Hooks de usuário, projeto e todos os outros plugins são bloqueados. Veja [Configuração de hooks](#hook-configuration)                                                                                                                                                                                                                                                                                                       | `true`                                                                                                                         |
| `allowManagedMcpServersOnly`      | (Apenas configurações gerenciadas) Apenas `allowedMcpServers` de configurações gerenciadas são respeitados. `deniedMcpServers` ainda se mescla de todas as fontes. Usuários ainda podem adicionar MCP servers, mas apenas a lista de permissões definida pelo administrador se aplica. Veja [Configuração MCP gerenciada](/pt/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                           | `true`                                                                                                                         |
| `allowManagedPermissionRulesOnly` | (Apenas configurações gerenciadas) Impedir que configurações de usuário e projeto definam regras de permissão `allow`, `ask` ou `deny`. Apenas regras em configurações gerenciadas se aplicam. Veja [Configurações apenas gerenciadas](/pt/permissions#managed-only-settings)                                                                                                                                                                                                                                                                                                                          | `true`                                                                                                                         |
| `alwaysThinkingEnabled`           | Ativar [pensamento estendido](/pt/common-workflows#use-extended-thinking-thinking-mode) por padrão para todas as sessões. Tipicamente configurado via comando `/config` em vez de editar diretamente                                                                                                                                                                                                                                                                                                                                                                                                   | `true`                                                                                                                         |
| `apiKeyHelper`                    | Script personalizado, a ser executado em `/bin/sh`, para gerar um valor de autenticação. Este valor será enviado como cabeçalhos `X-Api-Key` e `Authorization: Bearer` para solicitações de modelo                                                                                                                                                                                                                                                                                                                                                                                                     | `/bin/generate_temp_api_key.sh`                                                                                                |
| `attribution`                     | Personalizar atribuição para commits git e pull requests. Veja [Configurações de atribuição](#attribution-settings)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    | `{"commit": "🤖 Generated with Claude Code", "pr": ""}`                                                                        |
| `autoMemoryDirectory`             | Diretório personalizado para armazenamento de [memória automática](/pt/memory#storage-location). Aceita caminhos expandidos com `~/`. Não aceito em configurações de projeto (`.claude/settings.json`) para evitar que repositórios compartilhados redirecionem escritas de memória para locais sensíveis. Aceito de configurações de política, local e usuário                                                                                                                                                                                                                                        | `"~/my-memory-dir"`                                                                                                            |
| `autoMode`                        | Personalizar o que o classificador de [modo automático](/pt/permission-modes#eliminate-prompts-with-auto-mode) bloqueia e permite. Contém arrays `environment`, `allow`, e `soft_deny` de regras em prosa. Veja [Configurar o classificador de modo automático](/pt/permissions#configure-the-auto-mode-classifier). Não lido de configurações de projeto compartilhadas                                                                                                                                                                                                                               | `{"environment": ["Trusted repo: github.example.com/acme"]}`                                                                   |
| `autoUpdatesChannel`              | Canal de lançamento a seguir para atualizações. Use `"stable"` para uma versão que é tipicamente cerca de uma semana antiga e pula versões com regressões maiores, ou `"latest"` (padrão) para o lançamento mais recente                                                                                                                                                                                                                                                                                                                                                                               | `"stable"`                                                                                                                     |
| `availableModels`                 | Restringir quais modelos os usuários podem selecionar via `/model`, `--model`, ferramenta Config, ou `ANTHROPIC_MODEL`. Não afeta a opção Padrão. Veja [Restringir seleção de modelo](/pt/model-config#restrict-model-selection)                                                                                                                                                                                                                                                                                                                                                                       | `["sonnet", "haiku"]`                                                                                                          |
| `awsAuthRefresh`                  | Script personalizado que modifica o diretório `.aws` (veja [configuração avançada de credenciais](/pt/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                                                                                                                                                                                                                               | `aws sso login --profile myprofile`                                                                                            |
| `awsCredentialExport`             | Script personalizado que produz JSON com credenciais AWS (veja [configuração avançada de credenciais](/pt/amazon-bedrock#advanced-credential-configuration))                                                                                                                                                                                                                                                                                                                                                                                                                                           | `/bin/generate_aws_grant.sh`                                                                                                   |
| `blockedMarketplaces`             | (Apenas configurações gerenciadas) Lista de negação de fontes de marketplace. Fontes bloqueadas são verificadas antes do download, então nunca tocam o sistema de arquivos. Veja [Restrições de marketplace gerenciado](/pt/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                                                                                                                                                                                                                      | `[{ "source": "github", "repo": "untrusted/plugins" }]`                                                                        |
| `channelsEnabled`                 | (Apenas configurações gerenciadas) Permitir [channels](/pt/channels) para usuários de Team e Enterprise. Indefinido ou `false` bloqueia entrega de mensagens de canal independentemente do que os usuários passam para `--channels`                                                                                                                                                                                                                                                                                                                                                                    | `true`                                                                                                                         |
| `cleanupPeriodDays`               | Arquivos de sessão mais antigos que este período são deletados na inicialização (padrão: 30 dias, mínimo 1). Definir como `0` é rejeitado com um erro de validação. Também controla o corte de idade para remoção automática de [worktrees de subagent órfãos](/pt/common-workflows#worktree-cleanup) na inicialização. Para desabilitar escritas de transcrição completamente, defina a variável de ambiente [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/pt/env-vars), ou em modo não interativo (`-p`) use a flag `--no-session-persistence` ou a opção SDK `persistSession: false`.                        | `20`                                                                                                                           |
| `companyAnnouncements`            | Anúncio a ser exibido aos usuários na inicialização. Se múltiplos anúncios forem fornecidos, eles serão alternados aleatoriamente.                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `["Welcome to Acme Corp! Review our code guidelines at docs.acme.com"]`                                                        |
| `defaultShell`                    | Shell padrão para comandos `!` da caixa de entrada. Aceita `"bash"` (padrão) ou `"powershell"`. Definir `"powershell"` roteia comandos `!` interativos através do PowerShell no Windows. Requer `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`. Veja [Ferramenta PowerShell](/pt/tools-reference#powershell-tool)                                                                                                                                                                                                                                                                                                 | `"powershell"`                                                                                                                 |
| `deniedMcpServers`                | Quando definido em managed-settings.json, lista de negação de MCP servers que são explicitamente bloqueados. Se aplica a todos os escopos incluindo servers gerenciados. A lista de negação tem precedência sobre a lista de permissões. Veja [Configuração MCP gerenciada](/pt/mcp#managed-mcp-configuration)                                                                                                                                                                                                                                                                                         | `[{ "serverName": "filesystem" }]`                                                                                             |
| `disableAllHooks`                 | Desabilitar todos os [hooks](/pt/hooks) e qualquer [linha de status](/pt/statusline) personalizada                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `true`                                                                                                                         |
| `disableAutoMode`                 | Defina como `"disable"` para impedir que o [modo automático](/pt/permission-modes#eliminate-prompts-with-auto-mode) seja ativado. Remove `auto` do ciclo `Shift+Tab` e rejeita `--permission-mode auto` na inicialização. Mais útil em [configurações gerenciadas](/pt/permissions#managed-settings) onde os usuários não podem substituir                                                                                                                                                                                                                                                             | `"disable"`                                                                                                                    |
| `disableDeepLinkRegistration`     | Defina como `"disable"` para impedir que o Claude Code registre o manipulador de protocolo `claude-cli://` com o sistema operacional na inicialização. Deep links permitem que ferramentas externas abram uma sessão do Claude Code com um prompt pré-preenchido via `claude-cli://open?q=...`. O parâmetro `q` suporta prompts multi-linha usando newlines codificados em URL (`%0A`). Útil em ambientes onde o registro de manipulador de protocolo é restrito ou gerenciado separadamente                                                                                                           | `"disable"`                                                                                                                    |
| `disabledMcpjsonServers`          | Lista de MCP servers específicos de arquivos `.mcp.json` para rejeitar                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `["filesystem"]`                                                                                                               |
| `disableSkillShellExecution`      | Desabilitar execução de shell inline para blocos `` !`...` `` e ` ```! ` em [skills](/pt/skills) e comandos personalizados de fontes de usuário, projeto, plugin ou diretório adicional. Comandos são substituídos por `[shell command execution disabled by policy]` em vez de serem executados. Skills agrupadas e gerenciadas não são afetadas. Mais útil em [configurações gerenciadas](/pt/permissions#managed-settings) onde os usuários não podem substituir                                                                                                                                    | `true`                                                                                                                         |
| `effortLevel`                     | Persistir o [nível de esforço](/pt/model-config#adjust-effort-level) entre sessões. Aceita `"low"`, `"medium"`, `"high"`, ou `"xhigh"`. Escrito automaticamente quando você executa `/effort` com um desses valores. Veja [Ajustar nível de esforço](/pt/model-config#adjust-effort-level) para modelos suportados                                                                                                                                                                                                                                                                                     | `"xhigh"`                                                                                                                      |
| `enableAllProjectMcpServers`      | Aprovar automaticamente todos os MCP servers definidos em arquivos `.mcp.json` do projeto                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `true`                                                                                                                         |
| `enabledMcpjsonServers`           | Lista de MCP servers específicos de arquivos `.mcp.json` para aprovar                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `["memory", "github"]`                                                                                                         |
| `env`                             | Variáveis de ambiente que serão aplicadas a cada sessão                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                | `{"FOO": "bar"}`                                                                                                               |
| `fastModePerSessionOptIn`         | Quando `true`, o modo rápido não persiste entre sessões. Cada sessão começa com modo rápido desligado, exigindo que os usuários o habilitem com `/fast`. A preferência de modo rápido do usuário ainda é salva. Veja [Exigir opt-in por sessão](/pt/fast-mode#require-per-session-opt-in)                                                                                                                                                                                                                                                                                                              | `true`                                                                                                                         |
| `feedbackSurveyRate`              | Probabilidade (0–1) que a [pesquisa de qualidade de sessão](/pt/data-usage#session-quality-surveys) aparece quando elegível. Defina como `0` para suprimir completamente. Útil ao usar Bedrock, Vertex, ou Foundry onde a taxa de amostra padrão não se aplica                                                                                                                                                                                                                                                                                                                                         | `0.05`                                                                                                                         |
| `fileSuggestion`                  | Configure um script personalizado para preenchimento automático de arquivo `@`. Veja [Configurações de sugestão de arquivo](#file-suggestion-settings)                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `{"type": "command", "command": "~/.claude/file-suggestion.sh"}`                                                               |
| `forceLoginMethod`                | Use `claudeai` para restringir login a contas Claude.ai, `console` para restringir login a contas Claude Console (faturamento de uso de API)                                                                                                                                                                                                                                                                                                                                                                                                                                                           | `claudeai`                                                                                                                     |
| `forceLoginOrgUUID`               | Exigir que o login pertença a uma organização específica. Aceita uma string UUID única, que também pré-seleciona essa organização durante o login, ou um array de UUIDs onde qualquer organização listada é aceita sem pré-seleção. Quando definido em configurações gerenciadas, o login falha se a conta autenticada não pertencer a uma organização listada; um array vazio falha fechado e bloqueia o login com uma mensagem de configuração incorreta                                                                                                                                             | `"xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"` ou `["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"]` |
| `forceRemoteSettingsRefresh`      | (Apenas configurações gerenciadas) Bloquear inicialização da CLI até que configurações gerenciadas remotas sejam buscadas recentemente do servidor. Se a busca falhar, a CLI sai em vez de continuar com configurações em cache ou sem configurações. Quando não definido, a inicialização continua sem esperar por configurações remotas. Veja [aplicação fail-closed](/pt/server-managed-settings#enforce-fail-closed-startup)                                                                                                                                                                       | `true`                                                                                                                         |
| `hooks`                           | Configure comandos personalizados para executar em eventos do ciclo de vida. Veja [documentação de hooks](/pt/hooks) para formato                                                                                                                                                                                                                                                                                                                                                                                                                                                                      | Veja [hooks](/pt/hooks)                                                                                                        |
| `httpHookAllowedEnvVars`          | Lista de permissões de nomes de variáveis de ambiente que hooks HTTP podem interpolar em cabeçalhos. Quando definido, o `allowedEnvVars` efetivo de cada hook é a interseção com esta lista. Indefinido = sem restrição. Arrays se mesclam entre fontes de configuração. Veja [Configuração de hooks](#hook-configuration)                                                                                                                                                                                                                                                                             | `["MY_TOKEN", "HOOK_SECRET"]`                                                                                                  |
| `includeCoAuthoredBy`             | **Descontinuado**: Use `attribution` em vez disso. Se deve incluir a linha `co-authored-by Claude` em commits git e pull requests (padrão: `true`)                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `false`                                                                                                                        |
| `includeGitInstructions`          | Incluir instruções de workflow de commit e PR integradas e o snapshot de status git no prompt do sistema do Claude (padrão: `true`). Defina como `false` para remover ambos, por exemplo ao usar suas próprias skills de workflow git. A variável de ambiente `CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS` tem precedência sobre esta configuração quando definida                                                                                                                                                                                                                                           | `false`                                                                                                                        |
| `language`                        | Configure o idioma de resposta preferido do Claude (por exemplo, `"japanese"`, `"spanish"`, `"french"`). Claude responderá neste idioma por padrão. Também define o idioma de [ditado por voz](/pt/voice-dictation#change-the-dictation-language)                                                                                                                                                                                                                                                                                                                                                      | `"japanese"`                                                                                                                   |
| `minimumVersion`                  | Impedir que o auto-atualizador faça downgrade abaixo de uma versão específica. Automaticamente definido ao mudar para o canal estável e escolher ficar na versão atual até que o estável alcance. Usado com `autoUpdatesChannel`                                                                                                                                                                                                                                                                                                                                                                       | `"2.1.85"`                                                                                                                     |
| `model`                           | Substituir o modelo padrão a usar para Claude Code                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     | `"claude-sonnet-4-6"`                                                                                                          |
| `modelOverrides`                  | Mapear IDs de modelo Anthropic para IDs de modelo específicos do provedor, como ARNs de perfil de inferência Bedrock. Cada entrada do seletor de modelo usa seu valor mapeado ao chamar a API do provedor. Veja [Substituir IDs de modelo por versão](/pt/model-config#override-model-ids-per-version)                                                                                                                                                                                                                                                                                                 | `{"claude-opus-4-6": "arn:aws:bedrock:..."}`                                                                                   |
| `otelHeadersHelper`               | Script para gerar cabeçalhos OpenTelemetry dinâmicos. Executa na inicialização e periodicamente (veja [Cabeçalhos dinâmicos](/pt/monitoring-usage#dynamic-headers))                                                                                                                                                                                                                                                                                                                                                                                                                                    | `/bin/generate_otel_headers.sh`                                                                                                |
| `outputStyle`                     | Configure um estilo de saída para ajustar o prompt do sistema. Veja [documentação de estilos de saída](/pt/output-styles)                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `"Explanatory"`                                                                                                                |
| `permissions`                     | Veja a tabela abaixo para a estrutura de permissões.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |                                                                                                                                |
| `plansDirectory`                  | Personalizar onde os arquivos de plano são armazenados. O caminho é relativo à raiz do projeto. Padrão: `~/.claude/plans`                                                                                                                                                                                                                                                                                                                                                                                                                                                                              | `"./plans"`                                                                                                                    |
| `pluginTrustMessage`              | (Apenas configurações gerenciadas) Mensagem personalizada anexada ao aviso de confiança de plugin mostrado antes da instalação. Use isto para adicionar contexto específico da organização, por exemplo para confirmar que plugins do seu marketplace interno são verificados.                                                                                                                                                                                                                                                                                                                         | `"All plugins from our marketplace are approved by IT"`                                                                        |
| `prefersReducedMotion`            | Reduzir ou desabilitar animações de UI (spinners, shimmer, efeitos de flash) para acessibilidade                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       | `true`                                                                                                                         |
| `respectGitignore`                | Controlar se o seletor de arquivo `@` respeita padrões `.gitignore`. Quando `true` (padrão), arquivos correspondentes a padrões `.gitignore` são excluídos das sugestões                                                                                                                                                                                                                                                                                                                                                                                                                               | `false`                                                                                                                        |
| `showClearContextOnPlanAccept`    | Mostrar a opção "limpar contexto" na tela de aceitação do plano. Padrão: `false`. Defina como `true` para restaurar a opção                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `true`                                                                                                                         |
| `showThinkingSummaries`           | Mostrar resumos de [pensamento estendido](/pt/common-workflows#use-extended-thinking-thinking-mode) em sessões interativas. Quando indefinido ou `false` (padrão em modo interativo), blocos de pensamento são redatados pela API e mostrados como um stub recolhido. A redação apenas muda o que você vê, não o que o modelo gera: para reduzir gastos de pensamento, [reduza o orçamento ou desabilite o pensamento](/pt/common-workflows#use-extended-thinking-thinking-mode) em vez disso. Modo não interativo (`-p`) e chamadores SDK sempre recebem resumos independentemente desta configuração | `true`                                                                                                                         |
| `spinnerTipsEnabled`              | Mostrar dicas no spinner enquanto Claude está trabalhando. Defina como `false` para desabilitar dicas (padrão: `true`)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 | `false`                                                                                                                        |
| `spinnerTipsOverride`             | Substituir dicas do spinner com strings personalizadas. `tips`: array de strings de dica. `excludeDefault`: se `true`, mostrar apenas dicas personalizadas; se `false` ou ausente, dicas personalizadas são mescladas com dicas integradas                                                                                                                                                                                                                                                                                                                                                             | `{ "excludeDefault": true, "tips": ["Use our internal tool X"] }`                                                              |
| `spinnerVerbs`                    | Personalizar os verbos de ação mostrados no spinner e mensagens de duração de turno. Defina `mode` como `"replace"` para usar apenas seus verbos, ou `"append"` para adicioná-los aos padrões                                                                                                                                                                                                                                                                                                                                                                                                          | `{"mode": "append", "verbs": ["Pondering", "Crafting"]}`                                                                       |
| `statusLine`                      | Configure uma linha de status personalizada para exibir contexto. Veja [documentação de `statusLine`](/pt/statusline)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  | `{"type": "command", "command": "~/.claude/statusline.sh"}`                                                                    |
| `strictKnownMarketplaces`         | (Apenas configurações gerenciadas) Lista de permissões de marketplaces de plugin que os usuários podem adicionar. Indefinido = sem restrições, array vazio = bloqueio. Se aplica apenas a adições de marketplace. Veja [Restrições de marketplace gerenciado](/pt/plugin-marketplaces#managed-marketplace-restrictions)                                                                                                                                                                                                                                                                                | `[{ "source": "github", "repo": "acme-corp/plugins" }]`                                                                        |
| `useAutoModeDuringPlan`           | Se o Plan Mode usa semântica de modo automático quando o modo automático está disponível. Padrão: `true`. Não lido de configurações de projeto compartilhadas. Aparece em `/config` como "Use auto mode during plan"                                                                                                                                                                                                                                                                                                                                                                                   | `false`                                                                                                                        |
| `viewMode`                        | Modo de visualização de transcrição padrão na inicialização: `"default"`, `"verbose"`, ou `"focus"`. Substitui a seleção pegajosa Ctrl+O quando definido                                                                                                                                                                                                                                                                                                                                                                                                                                               | `"verbose"`                                                                                                                    |
| `voiceEnabled`                    | Ativar [ditado por voz](/pt/voice-dictation) push-to-talk. Escrito automaticamente quando você executa `/voice`. Requer uma conta Claude.ai                                                                                                                                                                                                                                                                                                                                                                                                                                                            | `true`                                                                                                                         |

### Configurações de config global

Estas configurações são armazenadas em `~/.claude.json` em vez de `settings.json`. Adicioná-las a `settings.json` acionará um erro de validação de esquema.

| Chave                        | Descrição                                                                                                                                                                                                                                                                                                                       | Exemplo        |
| :--------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :------------- |
| `autoConnectIde`             | Conectar automaticamente a um IDE em execução quando Claude Code inicia de um terminal externo. Padrão: `false`. Aparece em `/config` como **Auto-connect to IDE (external terminal)** ao executar fora de um terminal VS Code ou JetBrains                                                                                     | `true`         |
| `autoInstallIdeExtension`    | Instalar automaticamente a extensão IDE do Claude Code ao executar de um terminal VS Code. Padrão: `true`. Aparece em `/config` como **Auto-install IDE extension** ao executar dentro de um terminal VS Code ou JetBrains. Você também pode definir a variável de ambiente [`CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`](/pt/env-vars) | `false`        |
| `editorMode`                 | Modo de atalho de teclado para o prompt de entrada: `"normal"` ou `"vim"`. Padrão: `"normal"`. Aparece em `/config` como **Editor mode**                                                                                                                                                                                        | `"vim"`        |
| `showTurnDuration`           | Mostrar mensagens de duração de turno após respostas, por exemplo "Cooked for 1m 6s". Padrão: `true`. Aparece em `/config` como **Show turn duration**                                                                                                                                                                          | `false`        |
| `terminalProgressBarEnabled` | Mostrar a barra de progresso do terminal em terminais suportados: ConEmu, Ghostty 1.2.0+, e iTerm2 3.6.6+. Padrão: `true`. Aparece em `/config` como **Terminal progress bar**                                                                                                                                                  | `false`        |
| `teammateMode`               | Como [colegas de equipe de agente](/pt/agent-teams) são exibidos: `auto` (escolhe painéis divididos em tmux ou iTerm2, em processo caso contrário), `in-process`, ou `tmux`. Veja [escolher um modo de exibição](/pt/agent-teams#choose-a-display-mode)                                                                         | `"in-process"` |

### Configurações de worktrees

Configure como `--worktree` cria e gerencia git worktrees. Use estas configurações para reduzir uso de disco e tempo de inicialização em grandes monorepos.

| Chave                         | Descrição                                                                                                                                                                        | Exemplo                               |
| :---------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------ |
| `worktree.symlinkDirectories` | Diretórios para criar symlink do repositório principal em cada worktree para evitar duplicar grandes diretórios no disco. Nenhum diretório é criado symlink por padrão           | `["node_modules", ".cache"]`          |
| `worktree.sparsePaths`        | Diretórios para fazer checkout em cada worktree via git sparse-checkout (modo cone). Apenas os caminhos listados são escritos no disco, o que é mais rápido em grandes monorepos | `["packages/my-app", "shared/utils"]` |

Para copiar arquivos ignorados pelo git como `.env` em novos worktrees, use um arquivo [`.worktreeinclude`](/pt/common-workflows#copy-gitignored-files-to-worktrees) na raiz do seu projeto em vez de uma configuração.

### Configurações de permissão

| Chaves                              | Descrição                                                                                                                                                                                                                                                                                                                        | Exemplo                                                                |
| :---------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------- |
| `allow`                             | Array de regras de permissão para permitir uso de ferramenta. Veja [Sintaxe de regra de permissão](#permission-rule-syntax) abaixo para detalhes de correspondência de padrão                                                                                                                                                    | `[ "Bash(git diff *)" ]`                                               |
| `ask`                               | Array de regras de permissão para pedir confirmação ao usar ferramenta. Veja [Sintaxe de regra de permissão](#permission-rule-syntax) abaixo                                                                                                                                                                                     | `[ "Bash(git push *)" ]`                                               |
| `deny`                              | Array de regras de permissão para negar uso de ferramenta. Use isto para excluir arquivos sensíveis do acesso do Claude Code. Veja [Sintaxe de regra de permissão](#permission-rule-syntax) e [Limitações de permissão Bash](/pt/permissions#tool-specific-permission-rules)                                                     | `[ "WebFetch", "Bash(curl *)", "Read(./.env)", "Read(./secrets/**)" ]` |
| `additionalDirectories`             | [Diretórios de trabalho](/pt/permissions#working-directories) adicionais para acesso a arquivos. A maioria da configuração `.claude/` [não é descoberta](/pt/permissions#additional-directories-grant-file-access-not-configuration) destes diretórios                                                                           | `[ "../docs/" ]`                                                       |
| `defaultMode`                       | [Modo de permissão](/pt/permission-modes) padrão ao abrir Claude Code. Valores válidos: `default`, `acceptEdits`, `plan`, `auto`, `dontAsk`, `bypassPermissions`. A flag CLI `--permission-mode` substitui esta configuração para uma única sessão                                                                               | `"acceptEdits"`                                                        |
| `disableBypassPermissionsMode`      | Defina como `"disable"` para impedir que o modo `bypassPermissions` seja ativado. Isto desabilita a flag de linha de comando `--dangerously-skip-permissions`. Tipicamente colocado em [configurações gerenciadas](/pt/permissions#managed-settings) para aplicar política organizacional, mas funciona de qualquer escopo       | `"disable"`                                                            |
| `skipDangerousModePermissionPrompt` | Pular o prompt de confirmação mostrado antes de entrar no modo de permissões de bypass via `--dangerously-skip-permissions` ou `defaultMode: "bypassPermissions"`. Ignorado quando definido em configurações de projeto (`.claude/settings.json`) para evitar que repositórios não confiáveis contornem automaticamente o prompt | `true`                                                                 |

### Sintaxe de regra de permissão

Regras de permissão seguem o formato `Tool` ou `Tool(specifier)`. Regras são avaliadas em ordem: regras de negação primeiro, depois ask, depois allow. A primeira regra correspondente vence.

Exemplos rápidos:

| Regra                          | Efeito                                               |
| :----------------------------- | :--------------------------------------------------- |
| `Bash`                         | Corresponde a todos os comandos Bash                 |
| `Bash(npm run *)`              | Corresponde a comandos começando com `npm run`       |
| `Read(./.env)`                 | Corresponde a leitura do arquivo `.env`              |
| `WebFetch(domain:example.com)` | Corresponde a solicitações de fetch para example.com |

Para a referência completa de sintaxe de regra, incluindo comportamento de curinga, padrões específicos de ferramenta para Read, Edit, WebFetch, MCP, e regras de Agent, e limitações de segurança de padrões Bash, veja [Sintaxe de regra de permissão](/pt/permissions#permission-rule-syntax).

### Configurações de sandbox

Configure comportamento avançado de sandboxing. Sandboxing isola comandos bash do seu sistema de arquivos e rede. Veja [Sandboxing](/pt/sandboxing) para detalhes.

| Chaves                                 | Descrição                                                                                                                                                                                                                                                                                                                                                                    | Exemplo                         |
| :------------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------ |
| `enabled`                              | Ativar sandboxing bash (macOS, Linux, e WSL2). Padrão: false                                                                                                                                                                                                                                                                                                                 | `true`                          |
| `failIfUnavailable`                    | Sair com um erro na inicialização se `sandbox.enabled` é true mas o sandbox não pode iniciar (dependências faltantes, plataforma não suportada, ou restrições de plataforma). Quando false (padrão), um aviso é mostrado e comandos executam sem sandbox. Destinado para implantações de configurações gerenciadas que exigem sandboxing como um portão duro                 | `true`                          |
| `autoAllowBashIfSandboxed`             | Aprovar automaticamente comandos bash quando sandboxed. Padrão: true                                                                                                                                                                                                                                                                                                         | `true`                          |
| `excludedCommands`                     | Comandos que devem executar fora do sandbox                                                                                                                                                                                                                                                                                                                                  | `["docker *"]`                  |
| `allowUnsandboxedCommands`             | Permitir que comandos executem fora do sandbox via parâmetro `dangerouslyDisableSandbox`. Quando definido como `false`, a saída de escape `dangerouslyDisableSandbox` é completamente desabilitada e todos os comandos devem executar sandboxed (ou estar em `excludedCommands`). Útil para políticas empresariais que exigem sandboxing rigoroso. Padrão: true              | `false`                         |
| `filesystem.allowWrite`                | Caminhos adicionais onde comandos sandboxed podem escrever. Arrays são mesclados em todos os escopos de configuração: caminhos de usuário, projeto e gerenciados são combinados, não substituídos. Também mesclado com caminhos de regras de permissão `Edit(...)` allow. Veja [prefixos de caminho de sandbox](#sandbox-path-prefixes) abaixo.                              | `["/tmp/build", "~/.kube"]`     |
| `filesystem.denyWrite`                 | Caminhos onde comandos sandboxed não podem escrever. Arrays são mesclados em todos os escopos de configuração. Também mesclado com caminhos de regras de permissão `Edit(...)` deny.                                                                                                                                                                                         | `["/etc", "/usr/local/bin"]`    |
| `filesystem.denyRead`                  | Caminhos onde comandos sandboxed não podem ler. Arrays são mesclados em todos os escopos de configuração. Também mesclado com caminhos de regras de permissão `Read(...)` deny.                                                                                                                                                                                              | `["~/.aws/credentials"]`        |
| `filesystem.allowRead`                 | Caminhos para re-permitir leitura dentro de regiões `denyRead`. Tem precedência sobre `denyRead`. Arrays são mesclados em todos os escopos de configuração. Use isto para criar padrões de acesso de leitura apenas para workspace.                                                                                                                                          | `["."]`                         |
| `filesystem.allowManagedReadPathsOnly` | (Apenas configurações gerenciadas) Apenas caminhos `allowRead` de configurações gerenciadas são respeitados. `denyRead` ainda se mescla de todas as fontes. Padrão: false                                                                                                                                                                                                    | `true`                          |
| `network.allowUnixSockets`             | (Apenas macOS) Caminhos de socket Unix acessíveis no sandbox. Ignorado no Linux e WSL2, onde o filtro seccomp não pode inspecionar caminhos de socket; use `allowAllUnixSockets` em vez disso.                                                                                                                                                                               | `["~/.ssh/agent-socket"]`       |
| `network.allowAllUnixSockets`          | Permitir todas as conexões de socket Unix no sandbox. No Linux e WSL2 esta é a única maneira de permitir sockets Unix, já que pula o filtro seccomp que de outra forma bloqueia chamadas `socket(AF_UNIX, ...)`. Padrão: false                                                                                                                                               | `true`                          |
| `network.allowLocalBinding`            | Permitir vinculação a portas localhost (apenas macOS). Padrão: false                                                                                                                                                                                                                                                                                                         | `true`                          |
| `network.allowMachLookup`              | Nomes de serviço XPC/Mach adicionais que o sandbox pode procurar (apenas macOS). Suporta um único `*` à direita para correspondência de prefixo. Necessário para ferramentas que se comunicam via XPC, como o iOS Simulator ou Playwright.                                                                                                                                   | `["com.apple.coresimulator.*"]` |
| `network.allowedDomains`               | Array de domínios para permitir para tráfego de rede de saída. Suporta curingas (por exemplo, `*.example.com`).                                                                                                                                                                                                                                                              | `["github.com", "*.npmjs.org"]` |
| `network.allowManagedDomainsOnly`      | (Apenas configurações gerenciadas) Apenas `allowedDomains` e regras allow `WebFetch(domain:...)` de configurações gerenciadas são respeitadas. Domínios de configurações de usuário, projeto e local são ignorados. Domínios não permitidos são bloqueados automaticamente sem solicitar o usuário. Domínios negados ainda são respeitados de todas as fontes. Padrão: false | `true`                          |
| `network.httpProxyPort`                | Porta de proxy HTTP usada se você deseja trazer seu próprio proxy. Se não especificado, Claude executará seu próprio proxy.                                                                                                                                                                                                                                                  | `8080`                          |
| `network.socksProxyPort`               | Porta de proxy SOCKS5 usada se você deseja trazer seu próprio proxy. Se não especificado, Claude executará seu próprio proxy.                                                                                                                                                                                                                                                | `8081`                          |
| `enableWeakerNestedSandbox`            | Ativar sandbox mais fraco para ambientes Docker sem privilégios (apenas Linux e WSL2). **Reduz segurança.** Padrão: false                                                                                                                                                                                                                                                    | `true`                          |
| `enableWeakerNetworkIsolation`         | (Apenas macOS) Permitir acesso ao serviço de confiança TLS do sistema (`com.apple.trustd.agent`) no sandbox. Necessário para ferramentas baseadas em Go como `gh`, `gcloud`, e `terraform` verificarem certificados TLS ao usar `httpProxyPort` com um proxy MITM e CA personalizada. **Reduz segurança** abrindo um possível caminho de exfiltração de dados. Padrão: false | `true`                          |

#### Prefixos de caminho de sandbox

Caminhos em `filesystem.allowWrite`, `filesystem.denyWrite`, `filesystem.denyRead`, e `filesystem.allowRead` suportam estes prefixos:

| Prefixo             | Significado                                                                                              | Exemplo                                                                    |
| :------------------ | :------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| `/`                 | Caminho absoluto da raiz do sistema de arquivos                                                          | `/tmp/build` permanece `/tmp/build`                                        |
| `~/`                | Relativo ao diretório home                                                                               | `~/.kube` se torna `$HOME/.kube`                                           |
| `./` ou sem prefixo | Relativo à raiz do projeto para configurações de projeto, ou a `~/.claude` para configurações de usuário | `./output` em `.claude/settings.json` resolve para `<project-root>/output` |

O prefixo mais antigo `//path` para caminhos absolutos ainda funciona. Se você usou anteriormente `/path` esperando resolução relativa ao projeto, mude para `./path`. Esta sintaxe difere de [regras de permissão Read e Edit](/pt/permissions#read-and-edit), que usam `//path` para absoluto e `/path` para relativo ao projeto. Caminhos de sistema de arquivos de sandbox usam convenções padrão: `/tmp/build` é um caminho absoluto.

**Exemplo de configuração:**

```json theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker *"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
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

**Restrições de sistema de arquivos e rede** podem ser configuradas de duas formas que são mescladas juntas:

* **Configurações `sandbox.filesystem`** (mostradas acima): Controlam caminhos no limite do sandbox de nível de SO. Estas restrições se aplicam a todos os comandos de subprocesso (por exemplo, `kubectl`, `terraform`, `npm`), não apenas às ferramentas de arquivo do Claude.
* **Regras de permissão**: Use regras allow/deny `Edit` para controlar acesso à ferramenta de arquivo do Claude, regras deny `Read` para bloquear leituras, e regras allow/deny `WebFetch` para controlar domínios de rede. Caminhos destas regras também são mesclados na configuração do sandbox.

### Configurações de atribuição

O Claude Code adiciona atribuição a commits git e pull requests. Estes são configurados separadamente:

* Commits usam [git trailers](https://git-scm.com/docs/git-interpret-trailers) (como `Co-Authored-By`) por padrão, que podem ser personalizados ou desabilitados
* Descrições de pull request são texto simples

| Chaves   | Descrição                                                                                         |
| :------- | :------------------------------------------------------------------------------------------------ |
| `commit` | Atribuição para commits git, incluindo qualquer trailer. String vazia oculta atribuição de commit |
| `pr`     | Atribuição para descrições de pull request. String vazia oculta atribuição de pull request        |

**Atribuição de commit padrão:**

```text theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)

   Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
```

**Atribuição de pull request padrão:**

```text theme={null}
🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

**Exemplo:**

```json theme={null}
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

```json theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

O comando executa com as mesmas variáveis de ambiente que [hooks](/pt/hooks), incluindo `CLAUDE_PROJECT_DIR`. Recebe JSON via stdin com um campo `query`:

```json theme={null}
{"query": "src/comp"}
```

Produz caminhos de arquivo separados por nova linha para stdout (atualmente limitado a 15):

```text theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

**Exemplo:**

```bash theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
your-repo-file-index --query "$query" | head -20
```

### Configuração de hooks

Estas configurações controlam quais hooks são permitidos executar e o que hooks HTTP podem acessar. A configuração `allowManagedHooksOnly` pode ser configurada apenas em [configurações gerenciadas](#settings-files). As listas de permissões de URL e variável de ambiente podem ser definidas em qualquer nível de configuração e se mesclam entre fontes.

**Comportamento quando `allowManagedHooksOnly` é `true`:**

* Hooks gerenciados e hooks SDK são carregados
* Hooks de plugins força-habilitados em configurações gerenciadas `enabledPlugins` são carregados. Isto permite que administradores distribuam hooks verificados através de um marketplace de organização enquanto bloqueiam tudo mais. A confiança é concedida pelo ID completo `plugin@marketplace`, então um plugin com o mesmo nome de um marketplace diferente permanece bloqueado
* Hooks de usuário, hooks de projeto e todos os outros hooks de plugin são bloqueados

**Restringir URLs de hook HTTP:**

Limitar quais URLs hooks HTTP podem almejar. Suporta `*` como curinga para correspondência. Quando o array é definido, hooks HTTP almejando URLs não correspondentes são silenciosamente bloqueados.

```json theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

**Restringir variáveis de ambiente de hook HTTP:**

Limitar quais nomes de variáveis de ambiente hooks HTTP podem interpolar em valores de cabeçalho. O `allowedEnvVars` efetivo de cada hook é a interseção de sua própria lista e esta configuração.

```json theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

### Precedência de configurações

Configurações se aplicam em ordem de precedência. De mais alta para mais baixa:

1. **Configurações gerenciadas** ([gerenciadas pelo servidor](/pt/server-managed-settings), [políticas de nível MDM/SO](#configuration-scopes), ou [configurações gerenciadas](/pt/settings#settings-files))
   * Políticas implantadas por TI através de entrega de servidor, perfis de configuração MDM, políticas de registro, ou arquivos de configurações gerenciadas
   * Não podem ser substituídas por qualquer outro nível, incluindo argumentos de linha de comando
   * Dentro do nível gerenciado, a precedência é: gerenciadas pelo servidor > políticas de nível MDM/SO > baseadas em arquivo (`managed-settings.d/*.json` + `managed-settings.json`) > registro HKCU (apenas Windows). Apenas uma fonte gerenciada é usada; fontes não se mesclam entre camadas. Dentro da camada baseada em arquivo, arquivos drop-in e o arquivo base são mesclados juntos.

2. **Argumentos de linha de comando**
   * Substituições temporárias para uma sessão específica

3. **Configurações de projeto local** (`.claude/settings.local.json`)
   * Configurações pessoais específicas do projeto

4. **Configurações de projeto compartilhadas** (`.claude/settings.json`)
   * Configurações de projeto compartilhadas pela equipe no controle de origem

5. **Configurações de usuário** (`~/.claude/settings.json`)
   * Configurações globais pessoais

Esta hierarquia garante que políticas organizacionais sejam sempre aplicadas enquanto ainda permite que equipes e indivíduos personalizem sua experiência. A mesma precedência se aplica se você executar Claude Code a partir da CLI, da [extensão VS Code](/pt/vs-code), ou de um [IDE JetBrains](/pt/jetbrains).

Por exemplo, se suas configurações de usuário permitem `Bash(npm run *)` mas as configurações compartilhadas de um projeto negam, a configuração do projeto tem precedência e o comando é bloqueado.

<Note>
  **Configurações de array se mesclam entre escopos.** Quando a mesma configuração com valor de array (como `sandbox.filesystem.allowWrite` ou `permissions.allow`) aparece em múltiplos escopos, os arrays são **concatenados e desduplicados**, não substituídos. Isto significa que escopos de prioridade mais baixa podem adicionar entradas sem substituir aquelas definidas por escopos de prioridade mais alta, e vice-versa. Por exemplo, se configurações gerenciadas definem `allowWrite` como `["/opt/company-tools"]` e um usuário adiciona `["~/.kube"]`, ambos os caminhos são incluídos na configuração final.
</Note>

### Verificar configurações ativas

Execute `/status` dentro do Claude Code para ver quais fontes de configuração estão ativas e de onde vêm. A saída mostra cada camada de configuração (gerenciada, usuário, projeto) junto com sua origem, como `Enterprise managed settings (remote)`, `Enterprise managed settings (plist)`, `Enterprise managed settings (HKLM)`, ou `Enterprise managed settings (file)`. Se um arquivo de configuração contém erros, `/status` relata o problema para que você possa corrigi-lo.

### Pontos-chave sobre o sistema de configuração

* **Arquivos de memória (`CLAUDE.md`)**: Contêm instruções e contexto que Claude carrega na inicialização
* **Arquivos de configuração (JSON)**: Configurar permissões, variáveis de ambiente, e comportamento de ferramenta
* **Skills**: Prompts personalizados que podem ser invocados com `/skill-name` ou carregados pelo Claude automaticamente
* **MCP servers**: Estender Claude Code com ferramentas e integrações adicionais
* **Precedência**: Configurações de nível mais alto (Managed) substituem as de nível mais baixo (User/Project)
* **Herança**: Configurações são mescladas, com configurações mais específicas adicionando ou substituindo as mais amplas

### Prompt do sistema

O prompt do sistema interno do Claude Code não é publicado. Para adicionar instruções personalizadas, use arquivos `CLAUDE.md` ou a flag `--append-system-prompt`.

### Excluindo arquivos sensíveis

Para impedir que Claude Code acesse arquivos contendo informações sensíveis como chaves de API, segredos, e arquivos de ambiente, use a configuração `permissions.deny` no seu arquivo `.claude/settings.json`:

```json theme={null}
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

Isto substitui a configuração descontinuada `ignorePatterns`. Arquivos correspondentes a estes padrões são excluídos da descoberta de arquivo e resultados de busca, e operações de leitura nestes arquivos são negadas.

## Configuração de subagent

O Claude Code suporta subagents de IA personalizados que podem ser configurados em níveis de usuário e projeto. Estes subagents são armazenados como arquivos Markdown com frontmatter YAML:

* **Subagents de usuário**: `~/.claude/agents/` - Disponíveis em todos os seus projetos
* **Subagents de projeto**: `.claude/agents/` - Específicos ao seu projeto e podem ser compartilhados com sua equipe

Arquivos de subagent definem assistentes de IA especializados com prompts personalizados e permissões de ferramenta. Saiba mais sobre criação e uso de subagents na [documentação de subagents](/pt/sub-agents).

## Configuração de plugin

O Claude Code suporta um sistema de plugin que permite estender funcionalidade com skills, agents, hooks, e MCP servers. Plugins são distribuídos através de marketplaces e podem ser configurados em níveis de usuário e repositório.

### Configurações de plugin

Configurações relacionadas a plugin em `settings.json`:

```json theme={null}
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

* **Configurações de usuário** (`~/.claude/settings.json`): Preferências pessoais de plugin
* **Configurações de projeto** (`.claude/settings.json`): Plugins específicos do projeto compartilhados com equipe
* **Configurações locais** (`.claude/settings.local.json`): Substituições por máquina (não confirmadas)
* **Configurações gerenciadas** (`managed-settings.json`): Substituições de política em toda a organização que bloqueiam instalação em todos os escopos e ocultam o plugin do marketplace

**Exemplo**:

```json theme={null}
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}
```

#### `extraKnownMarketplaces`

Define marketplaces adicionais que devem ser disponibilizados para o repositório. Tipicamente usado em configurações em nível de repositório para garantir que membros da equipe tenham acesso a fontes de plugin necessárias.

**Quando um repositório inclui `extraKnownMarketplaces`**:

1. Membros da equipe são solicitados a instalar o marketplace quando confiam na pasta
2. Membros da equipe são então solicitados a instalar plugins daquele marketplace
3. Usuários podem pular marketplaces ou plugins indesejados (armazenados em configurações de usuário)
4. Instalação respeita limites de confiança e requer consentimento explícito

**Exemplo**:

```json theme={null}
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
* `settings`: marketplace inline declarado diretamente em settings.json sem um repositório hospedado separado (usa `name` e `plugins`)

Use `source: 'settings'` para declarar um pequeno conjunto de plugins inline sem configurar um repositório de marketplace hospedado. Plugins listados aqui devem referenciar fontes externas como GitHub ou npm. Você ainda precisa habilitar cada plugin separadamente em `enabledPlugins`.

```json theme={null}
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "settings",
        "name": "team-tools",
        "plugins": [
          {
            "name": "code-formatter",
            "source": {
              "source": "github",
              "repo": "acme-corp/code-formatter"
            }
          }
        ]
      }
    }
  }
}
```

#### `strictKnownMarketplaces`

**Apenas configurações gerenciadas**: Controla quais marketplaces de plugin os usuários podem adicionar. Esta configuração pode ser configurada apenas em [configurações gerenciadas](/pt/settings#settings-files) e fornece aos administradores controle rigoroso sobre fontes de marketplace.

**Localizações de arquivo de configurações gerenciadas**:

* **macOS**: `/Library/Application Support/ClaudeCode/managed-settings.json`
* **Linux e WSL**: `/etc/claude-code/managed-settings.json`
* **Windows**: `C:\Program Files\ClaudeCode\managed-settings.json`

**Características principais**:

* Apenas disponível em configurações gerenciadas (`managed-settings.json`)
* Não pode ser substituída por configurações de usuário ou projeto (precedência mais alta)
* Aplicada ANTES de operações de rede/sistema de arquivos (fontes bloqueadas nunca executam)
* Usa correspondência exata para especificações de fonte (incluindo `ref`, `path` para fontes git), exceto `hostPattern`, que usa correspondência regex

**Comportamento de lista de permissões**:

* `undefined` (padrão): Sem restrições - usuários podem adicionar qualquer marketplace
* Array vazio `[]`: Bloqueio completo - usuários não podem adicionar novos marketplaces
* Lista de fontes: Usuários podem apenas adicionar marketplaces que correspondem exatamente

**Todos os tipos de fonte suportados**:

A lista de permissões suporta múltiplos tipos de fonte de marketplace. A maioria das fontes usa correspondência exata, enquanto `hostPattern` usa correspondência regex contra o host do marketplace.

1. **Repositórios GitHub**:

```json theme={null}
{ "source": "github", "repo": "acme-corp/approved-plugins" }
{ "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" }
{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }
```

Campos: `repo` (obrigatório), `ref` (opcional: branch/tag/SHA), `path` (opcional: subdiretório)

2. **Repositórios Git**:

```json theme={null}
{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git" }
{ "source": "git", "url": "https://bitbucket.org/acme-corp/plugins.git", "ref": "production" }
{ "source": "git", "url": "ssh://git@git.example.com/plugins.git", "ref": "v3.1", "path": "approved" }
```

Campos: `url` (obrigatório), `ref` (opcional: branch/tag/SHA), `path` (opcional: subdiretório)

3. **Marketplaces baseados em URL**:

```json theme={null}
{ "source": "url", "url": "https://plugins.example.com/marketplace.json" }
{ "source": "url", "url": "https://cdn.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }
```

Campos: `url` (obrigatório), `headers` (opcional: cabeçalhos HTTP para acesso autenticado)

<Note>
  Marketplaces baseados em URL apenas baixam o arquivo `marketplace.json`. Eles não baixam arquivos de plugin do servidor. Plugins em marketplaces baseados em URL devem usar fontes externas (URLs GitHub, npm, ou git) em vez de caminhos relativos. Para plugins com caminhos relativos, use um marketplace baseado em Git em vez disso. Veja [Troubleshooting](/pt/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces) para detalhes.
</Note>

4. **Pacotes NPM**:

```json theme={null}
{ "source": "npm", "package": "@acme-corp/claude-plugins" }
{ "source": "npm", "package": "@acme-corp/approved-marketplace" }
```

Campos: `package` (obrigatório, suporta pacotes com escopo)

5. **Caminhos de arquivo**:

```json theme={null}
{ "source": "file", "path": "/usr/local/share/claude/acme-marketplace.json" }
{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }
```

Campos: `path` (obrigatório: caminho absoluto para arquivo marketplace.json)

6. **Caminhos de diretório**:

```json theme={null}
{ "source": "directory", "path": "/usr/local/share/claude/acme-plugins" }
{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }
```

Campos: `path` (obrigatório: caminho absoluto para diretório contendo `.claude-plugin/marketplace.json`)

7. **Correspondência de padrão de host**:

```json theme={null}
{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }
{ "source": "hostPattern", "hostPattern": "^gitlab\\.internal\\.example\\.com$" }
```

Campos: `hostPattern` (obrigatório: padrão regex para corresponder contra o host do marketplace)

Use correspondência de padrão de host quando você deseja permitir todos os marketplaces de um host específico sem enumerar cada repositório individualmente. Isto é útil para organizações com GitHub Enterprise interno ou servidores GitLab onde desenvolvedores criam seus próprios marketplaces.

Extração de host por tipo de fonte:

* `github`: sempre corresponde contra `github.com`
* `git`: extrai nome de host da URL (suporta formatos HTTPS e SSH)
* `url`: extrai nome de host da URL
* `npm`, `file`, `directory`: não suportado para correspondência de padrão de host

**Exemplos de configuração**:

Exemplo: permitir apenas marketplaces específicos:

```json theme={null}
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

```json theme={null}
{
  "strictKnownMarketplaces": []
}
```

Exemplo: permitir todos os marketplaces de um servidor git interno:

```json theme={null}
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

Fontes de marketplace devem corresponder **exatamente** para que a adição de um usuário seja permitida. Para fontes baseadas em git (`github` e `git`), isto inclui todos os campos opcionais:

* O `repo` ou `url` deve corresponder exatamente
* O campo `ref` deve corresponder exatamente (ou ambos serem indefinidos)
* O campo `path` deve corresponder exatamente (ou ambos serem indefinidos)

Exemplos de fontes que **NÃO correspondem**:

```json theme={null}
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
| **Comportamento**           | Bloqueia adições não permitidas                | Auto-instala marketplaces faltantes              |
| **Quando aplicado**         | Antes de operações de rede/sistema de arquivos | Após prompt de confiança do usuário              |
| **Pode ser substituído**    | Não (precedência mais alta)                    | Sim (por configurações de precedência mais alta) |
| **Formato de fonte**        | Objeto de fonte direto                         | Marketplace nomeado com fonte aninhada           |
| **Caso de uso**             | Conformidade, restrições de segurança          | Onboarding, padronização                         |

**Diferença de formato**:

`strictKnownMarketplaces` usa objetos de fonte diretos:

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ]
}
```

`extraKnownMarketplaces` requer marketplaces nomeados:

```json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

**Usando ambos juntos**:

`strictKnownMarketplaces` é um portão de política: controla o que os usuários podem adicionar mas não registra nenhum marketplace. Para restringir e pré-registrar um marketplace para todos os usuários, defina ambos em `managed-settings.json`:

```json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ],
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

Com apenas `strictKnownMarketplaces` definido, usuários ainda podem adicionar o marketplace permitido manualmente via `/plugin marketplace add`, mas não está disponível automaticamente.

**Notas importantes**:

* Restrições são verificadas ANTES de qualquer solicitação de rede ou operação de sistema de arquivos
* Quando bloqueado, usuários veem mensagens de erro claras indicando que a fonte é bloqueada por política gerenciada
* A restrição se aplica apenas a adição de NOVOS marketplaces; marketplaces previamente instalados permanecem acessíveis
* Configurações gerenciadas têm a precedência mais alta e não podem ser substituídas

Veja [Restrições de marketplace gerenciado](/pt/plugin-marketplaces#managed-marketplace-restrictions) para documentação voltada para o usuário.

### Gerenciando plugins

Use o comando `/plugin` para gerenciar plugins interativamente:

* Procurar plugins disponíveis de marketplaces
* Instalar/desinstalar plugins
* Habilitar/desabilitar plugins
* Ver detalhes de plugin (skills, agents, hooks fornecidos)
* Adicionar/remover marketplaces

Saiba mais sobre o sistema de plugin na [documentação de plugins](/pt/plugins).

## Variáveis de ambiente

Variáveis de ambiente permitem controlar o comportamento do Claude Code sem editar arquivos de configuração. Qualquer variável também pode ser configurada em [`settings.json`](#available-settings) sob a chave `env` para aplicá-la a cada sessão ou implantá-la para sua equipe.

Veja a [referência de variáveis de ambiente](/pt/env-vars) para a lista completa.

## Ferramentas disponíveis para Claude

O Claude Code tem acesso a um conjunto de ferramentas para leitura, edição, busca, execução de comandos, e orquestração de subagents. Nomes de ferramenta são as strings exatas que você usa em regras de permissão e correspondedores de hook.

Veja a [referência de ferramentas](/pt/tools-reference) para a lista completa e detalhes de comportamento da ferramenta Bash.

## Veja também

* [Permissões](/pt/permissions): sistema de permissões, sintaxe de regra, padrões específicos de ferramenta, e políticas gerenciadas
* [Autenticação](/pt/authentication): configurar acesso de usuário ao Claude Code
* [Troubleshooting](/pt/troubleshooting): soluções para problemas comuns de configuração
