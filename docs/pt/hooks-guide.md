> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Automatizar fluxos de trabalho com hooks

> Execute comandos shell automaticamente quando Claude Code edita arquivos, conclui tarefas ou precisa de entrada. Formate código, envie notificações, valide comandos e aplique regras do projeto.

Hooks são comandos shell definidos pelo usuário que executam em pontos específicos do ciclo de vida do Claude Code. Eles fornecem controle determinístico sobre o comportamento do Claude Code, garantindo que certas ações sempre aconteçam em vez de depender do LLM para escolher executá-las. Use hooks para aplicar regras do projeto, automatizar tarefas repetitivas e integrar Claude Code com suas ferramentas existentes.

Para decisões que exigem julgamento em vez de regras determinísticas, você também pode usar [hooks baseados em prompt](#prompt-based-hooks) ou [hooks baseados em agente](#agent-based-hooks) que usam um modelo Claude para avaliar condições.

Para outras formas de estender Claude Code, consulte [skills](/pt/skills) para dar ao Claude instruções adicionais e comandos executáveis, [subagents](/pt/sub-agents) para executar tarefas em contextos isolados e [plugins](/pt/plugins) para empacotar extensões para compartilhar entre projetos.

<Tip>
  Este guia cobre casos de uso comuns e como começar. Para esquemas de eventos completos, formatos de entrada/saída JSON e recursos avançados como hooks assíncronos e hooks de ferramentas MCP, consulte a [referência de Hooks](/pt/hooks).
</Tip>

## Configure seu primeiro hook

Para criar um hook, adicione um bloco `hooks` a um [arquivo de configuração](#configure-hook-location). Este passo a passo cria um hook de notificação de desktop, para que você seja alertado sempre que Claude estiver aguardando sua entrada em vez de observar o terminal.

<Steps>
  <Step title="Adicione o hook às suas configurações">
    Abra `~/.claude/settings.json` e adicione um hook `Notification`. O exemplo abaixo usa `osascript` para macOS; consulte [Receba notificações quando Claude precisa de entrada](#get-notified-when-claude-needs-input) para comandos Linux e Windows.

    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
              }
            ]
          }
        ]
      }
    }
    ```

    Se seu arquivo de configuração já tem uma chave `hooks`, mescle a entrada `Notification` nela em vez de substituir o objeto inteiro. Você também pode pedir ao Claude para escrever o hook para você descrevendo o que deseja na CLI.
  </Step>

  <Step title="Verifique a configuração">
    Digite `/hooks` para abrir o navegador de hooks. Você verá uma lista de todos os eventos de hook disponíveis, com uma contagem ao lado de cada evento que tem hooks configurados. Selecione `Notification` para confirmar que seu novo hook aparece na lista. Selecionar o hook mostra seus detalhes: o evento, matcher, tipo, arquivo de origem e comando.
  </Step>

  <Step title="Teste o hook">
    Pressione `Esc` para retornar à CLI. Peça ao Claude para fazer algo que exija permissão, depois saia do terminal. Você deve receber uma notificação de desktop.
  </Step>
</Steps>

<Tip>
  O menu `/hooks` é somente leitura. Para adicionar, modificar ou remover hooks, edite seu JSON de configuração diretamente ou peça ao Claude para fazer a alteração.
</Tip>

## O que você pode automatizar

Hooks permitem executar código em pontos-chave do ciclo de vida do Claude Code: formatar arquivos após edições, bloquear comandos antes de executarem, enviar notificações quando Claude precisa de entrada, injetar contexto no início da sessão e muito mais. Para a lista completa de eventos de hook, consulte a [referência de Hooks](/pt/hooks#hook-lifecycle).

Cada exemplo inclui um bloco de configuração pronto para usar que você adiciona a um [arquivo de configuração](#configure-hook-location). Os padrões mais comuns:

* [Receba notificações quando Claude precisa de entrada](#get-notified-when-claude-needs-input)
* [Formatar código automaticamente após edições](#auto-format-code-after-edits)
* [Bloquear edições em arquivos protegidos](#block-edits-to-protected-files)
* [Re-injetar contexto após compactação](#re-inject-context-after-compaction)
* [Auditar mudanças de configuração](#audit-configuration-changes)
* [Recarregar ambiente quando diretório ou arquivos mudam](#reload-environment-when-directory-or-files-change)
* [Aprovar automaticamente prompts de permissão específicos](#auto-approve-specific-permission-prompts)

### Receba notificações quando Claude precisa de entrada

Receba uma notificação de desktop sempre que Claude terminar de trabalhar e precisar de sua entrada, para que você possa mudar para outras tarefas sem verificar o terminal.

Este hook usa o evento `Notification`, que dispara quando Claude está aguardando entrada ou permissão. Cada aba abaixo usa o comando de notificação nativo da plataforma. Adicione isto a `~/.claude/settings.json`:

<Tabs>
  <Tab title="macOS">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "osascript -e 'display notification \"Claude Code needs your attention\" with title \"Claude Code\"'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Linux">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "notify-send 'Claude Code' 'Claude Code needs your attention'"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Windows (PowerShell)">
    ```json  theme={null}
    {
      "hooks": {
        "Notification": [
          {
            "matcher": "",
            "hooks": [
              {
                "type": "command",
                "command": "powershell.exe -Command \"[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')\""
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

### Formatar código automaticamente após edições

Execute automaticamente [Prettier](https://prettier.io/) em cada arquivo que Claude edita, para que a formatação permaneça consistente sem intervenção manual.

Este hook usa o evento `PostToolUse` com um matcher `Edit|Write`, para que execute apenas após ferramentas de edição de arquivo. O comando extrai o caminho do arquivo editado com [`jq`](https://jqlang.github.io/jq/) e o passa para Prettier. Adicione isto a `.claude/settings.json` na raiz do seu projeto:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "jq -r '.tool_input.file_path' | xargs npx prettier --write"
          }
        ]
      }
    ]
  }
}
```

<Note>
  Os exemplos Bash nesta página usam `jq` para análise JSON. Instale-o com `brew install jq` (macOS), `apt-get install jq` (Debian/Ubuntu), ou consulte [downloads do `jq`](https://jqlang.github.io/jq/download/).
</Note>

### Bloquear edições em arquivos protegidos

Impeça que Claude modifique arquivos sensíveis como `.env`, `package-lock.json` ou qualquer coisa em `.git/`. Claude recebe feedback explicando por que a edição foi bloqueada, para que possa ajustar sua abordagem.

Este exemplo usa um arquivo de script separado que o hook chama. O script verifica o caminho do arquivo de destino contra uma lista de padrões protegidos e sai com código 2 para bloquear a edição.

<Steps>
  <Step title="Crie o script do hook">
    Salve isto em `.claude/hooks/protect-files.sh`:

    ```bash  theme={null}
    #!/bin/bash
    # protect-files.sh

    INPUT=$(cat)
    FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

    PROTECTED_PATTERNS=(".env" "package-lock.json" ".git/")

    for pattern in "${PROTECTED_PATTERNS[@]}"; do
      if [[ "$FILE_PATH" == *"$pattern"* ]]; then
        echo "Blocked: $FILE_PATH matches protected pattern '$pattern'" >&2
        exit 2
      fi
    done

    exit 0
    ```
  </Step>

  <Step title="Torne o script executável (macOS/Linux)">
    Scripts de hook devem ser executáveis para que Claude Code os execute:

    ```bash  theme={null}
    chmod +x .claude/hooks/protect-files.sh
    ```
  </Step>

  <Step title="Registre o hook">
    Adicione um hook `PreToolUse` a `.claude/settings.json` que execute o script antes de qualquer chamada de ferramenta `Edit` ou `Write`:

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/protect-files.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Step>
</Steps>

### Re-injetar contexto após compactação

Quando a janela de contexto do Claude fica cheia, a compactação resume a conversa para liberar espaço. Isto pode perder detalhes importantes. Use um hook `SessionStart` com um matcher `compact` para re-injetar contexto crítico após cada compactação.

Qualquer texto que seu comando escreve para stdout é adicionado ao contexto do Claude. Este exemplo lembra ao Claude as convenções do projeto e trabalho recente. Adicione isto a `.claude/settings.json` na raiz do seu projeto:

```json  theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "compact",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Reminder: use Bun, not npm. Run bun test before committing. Current sprint: auth refactor.'"
          }
        ]
      }
    ]
  }
}
```

Você pode substituir o `echo` por qualquer comando que produza saída dinâmica, como `git log --oneline -5` para mostrar commits recentes. Para injetar contexto em cada início de sessão, considere usar [CLAUDE.md](/pt/memory) em vez disso. Para variáveis de ambiente, consulte [`CLAUDE_ENV_FILE`](/pt/hooks#persist-environment-variables) na referência.

### Auditar mudanças de configuração

Rastreie quando arquivos de configuração ou skills mudam durante uma sessão. O evento `ConfigChange` dispara quando um processo externo ou editor modifica um arquivo de configuração, para que você possa registrar mudanças para conformidade ou bloquear modificações não autorizadas.

Este exemplo anexa cada mudança a um log de auditoria. Adicione isto a `~/.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "jq -c '{timestamp: now | todate, source: .source, file: .file_path}' >> ~/claude-config-audit.log"
          }
        ]
      }
    ]
  }
}
```

O matcher filtra por tipo de configuração: `user_settings`, `project_settings`, `local_settings`, `policy_settings` ou `skills`. Para bloquear uma mudança de entrar em vigor, saia com código 2 ou retorne `{"decision": "block"}`. Consulte a [referência de ConfigChange](/pt/hooks#configchange) para o esquema de entrada completo.

### Recarregar ambiente quando diretório ou arquivos mudam

Alguns projetos definem variáveis de ambiente diferentes dependendo de qual diretório você está. Ferramentas como [direnv](https://direnv.net/) fazem isto automaticamente no seu shell, mas a ferramenta Bash do Claude não pega essas mudanças por conta própria.

Um hook `CwdChanged` corrige isto: ele executa cada vez que Claude muda de diretório, para que você possa recarregar as variáveis corretas para o novo local. O hook escreve os valores atualizados para `CLAUDE_ENV_FILE`, que Claude Code aplica antes de cada comando Bash. Adicione isto a `~/.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "CwdChanged": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "direnv export bash >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

Para reagir a arquivos específicos em vez de cada mudança de diretório, use `FileChanged` com um `matcher` listando os nomes de arquivo para observar (separados por pipe). O `matcher` tanto configura quais arquivos observar quanto filtra quais hooks executam. Este exemplo observa `.envrc` e `.env` para mudanças no diretório atual:

```json  theme={null}
{
  "hooks": {
    "FileChanged": [
      {
        "matcher": ".envrc|.env",
        "hooks": [
          {
            "type": "command",
            "command": "direnv export bash >> \"$CLAUDE_ENV_FILE\""
          }
        ]
      }
    ]
  }
}
```

Consulte as entradas de referência [CwdChanged](/pt/hooks#cwdchanged) e [FileChanged](/pt/hooks#filechanged) para esquemas de entrada, saída `watchPaths` e detalhes de `CLAUDE_ENV_FILE`.

### Aprovar automaticamente prompts de permissão específicos

Pule o diálogo de aprovação para chamadas de ferramenta que você sempre permite. Este exemplo aprova automaticamente `ExitPlanMode`, a ferramenta que Claude chama quando termina de apresentar um plano e pede para prosseguir, para que você não seja solicitado toda vez que um plano estiver pronto.

Diferentemente dos exemplos de código de saída acima, a aprovação automática exige que seu hook escreva uma decisão JSON para stdout. Um hook `PermissionRequest` dispara quando Claude Code está prestes a mostrar um diálogo de permissão, e retornar `"behavior": "allow"` responde em seu nome.

O matcher restringe o hook apenas a `ExitPlanMode`, para que nenhum outro prompt seja afetado. Adicione isto a `~/.claude/settings.json`:

```json  theme={null}
{
  "hooks": {
    "PermissionRequest": [
      {
        "matcher": "ExitPlanMode",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\": {\"hookEventName\": \"PermissionRequest\", \"decision\": {\"behavior\": \"allow\"}}}'"
          }
        ]
      }
    ]
  }
}
```

Quando o hook aprova, Claude Code sai do modo de plano e restaura qualquer modo de permissão que estava ativo antes de você entrar no modo de plano. A transcrição mostra "Allowed by PermissionRequest hook" onde o diálogo teria aparecido. O caminho do hook sempre mantém a conversa atual: ele não pode limpar contexto e iniciar uma sessão de implementação fresca da forma que o diálogo pode.

Para definir um modo de permissão específico em vez disso, a saída do seu hook pode incluir um array `updatedPermissions` com uma entrada `setMode`. O valor `mode` é qualquer modo de permissão como `default`, `acceptEdits` ou `bypassPermissions`, e `destination: "session"` o aplica apenas para a sessão atual.

Para mudar a sessão para `acceptEdits`, seu hook escreve este JSON para stdout:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedPermissions": [
        { "type": "setMode", "mode": "acceptEdits", "destination": "session" }
      ]
    }
  }
}
```

Mantenha o matcher o mais restrito possível. Corresponder a `.*` ou deixar o matcher vazio aprovaria automaticamente cada prompt de permissão, incluindo escritas de arquivo e comandos shell. Consulte a [referência de PermissionRequest](/pt/hooks#permissionrequest-decision-control) para o conjunto completo de campos de decisão.

## Como hooks funcionam

Eventos de hook disparam em pontos específicos do ciclo de vida do Claude Code. Quando um evento dispara, todos os hooks correspondentes executam em paralelo, e comandos de hook idênticos são automaticamente desduplicados. A tabela abaixo mostra cada evento e quando dispara:

| Event                | When it fires                                                                                                                                          |
| :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                                       |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                                   |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`  | When a permission dialog appears                                                                                                                       |
| `PostToolUse`        | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure` | After a tool call fails                                                                                                                                |
| `Notification`       | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`      | When a subagent is spawned                                                                                                                             |
| `SubagentStop`       | When a subagent finishes                                                                                                                               |
| `Stop`               | When Claude finishes responding                                                                                                                        |
| `StopFailure`        | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                               |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`       | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`         | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`        | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`         | Before context compaction                                                                                                                              |
| `PostCompact`        | After context compaction completes                                                                                                                     |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`         | When a session terminates                                                                                                                              |

Cada hook tem um `type` que determina como ele executa. A maioria dos hooks usa `"type": "command"`, que executa um comando shell. Três outros tipos estão disponíveis:

* `"type": "http"`: POST dados de evento para uma URL. Consulte [HTTP hooks](#http-hooks).
* `"type": "prompt"`: avaliação LLM de turno único. Consulte [Hooks baseados em prompt](#prompt-based-hooks).
* `"type": "agent"`: verificação multi-turno com acesso a ferramentas. Consulte [Hooks baseados em agente](#agent-based-hooks).

### Ler entrada e retornar saída

Hooks se comunicam com Claude Code através de stdin, stdout, stderr e códigos de saída. Quando um evento dispara, Claude Code passa dados específicos do evento como JSON para stdin do seu script. Seu script lê esses dados, faz seu trabalho e diz ao Claude Code o que fazer a seguir através do código de saída.

#### Entrada do hook

Cada evento inclui campos comuns como `session_id` e `cwd`, mas cada tipo de evento adiciona dados diferentes. Por exemplo, quando Claude executa um comando Bash, um hook `PreToolUse` recebe algo assim em stdin:

```json  theme={null}
{
  "session_id": "abc123",          // ID único para esta sessão
  "cwd": "/Users/sarah/myproject", // diretório de trabalho quando o evento disparou
  "hook_event_name": "PreToolUse", // qual evento acionou este hook
  "tool_name": "Bash",             // a ferramenta que Claude está prestes a usar
  "tool_input": {                  // os argumentos que Claude passou para a ferramenta
    "command": "npm test"          // para Bash, este é o comando shell
  }
}
```

Seu script pode analisar esse JSON e agir em qualquer um desses campos. Hooks `UserPromptSubmit` obtêm o texto `prompt` em vez disso, hooks `SessionStart` obtêm a `source` (startup, resume, clear, compact) e assim por diante. Consulte [Campos de entrada comuns](/pt/hooks#common-input-fields) na referência para campos compartilhados e a seção de cada evento para esquemas específicos do evento.

#### Saída do hook

Seu script diz ao Claude Code o que fazer a seguir escrevendo para stdout ou stderr e saindo com um código específico. Por exemplo, um hook `PreToolUse` que quer bloquear um comando:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q "drop table"; then
  echo "Blocked: dropping tables is not allowed" >&2  # stderr se torna feedback do Claude
  exit 2 # exit 2 = bloquear a ação
fi

exit 0  # exit 0 = deixar prosseguir
```

O código de saída determina o que acontece a seguir:

* **Exit 0**: a ação prossegue. Para hooks `UserPromptSubmit` e `SessionStart`, qualquer coisa que você escrever para stdout é adicionada ao contexto do Claude.
* **Exit 2**: a ação é bloqueada. Escreva um motivo para stderr, e Claude o recebe como feedback para que possa se ajustar.
* **Qualquer outro código de saída**: a ação prossegue. Stderr é registrado mas não mostrado ao Claude. Alterne o modo verboso com `Ctrl+O` para ver essas mensagens na transcrição.

#### Saída JSON estruturada

Códigos de saída lhe dão duas opções: permitir ou bloquear. Para mais controle, saia com 0 e imprima um objeto JSON para stdout em vez disso.

<Note>
  Use exit 2 para bloquear com uma mensagem stderr, ou exit 0 com JSON para controle estruturado. Não misture: Claude Code ignora JSON quando você sai com 2.
</Note>

Por exemplo, um hook `PreToolUse` pode negar uma chamada de ferramenta e dizer ao Claude por quê, ou escalar para o usuário para aprovação:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep for better performance"
  }
}
```

Claude Code lê `permissionDecision` e cancela a chamada de ferramenta, depois alimenta `permissionDecisionReason` de volta ao Claude como feedback. Essas três opções são específicas para `PreToolUse`:

* `"allow"`: prosseguir sem mostrar um prompt de permissão. Negar e pedir regras, incluindo listas de negação gerenciadas por empresa, ainda se aplicam
* `"deny"`: cancelar a chamada de ferramenta e enviar o motivo ao Claude
* `"ask"`: mostrar o prompt de permissão ao usuário normalmente

Retornar `"allow"` pula o prompt interativo mas não substitui [regras de permissão](/pt/permissions#manage-permissions). Se uma regra de negação corresponder à chamada de ferramenta, a chamada é bloqueada mesmo quando seu hook retorna `"allow"`. Se uma regra de pedido corresponder, o usuário ainda é solicitado. Isto significa que regras de negação de qualquer escopo de configuração, incluindo [configurações gerenciadas](/pt/settings#settings-files), sempre têm precedência sobre aprovações de hook.

Outros eventos usam padrões de decisão diferentes. Por exemplo, hooks `PostToolUse` e `Stop` usam um campo `decision: "block"` de nível superior, enquanto `PermissionRequest` usa `hookSpecificOutput.decision.behavior`. Consulte a [tabela de resumo](/pt/hooks#decision-control) na referência para uma análise completa por evento.

Para hooks `UserPromptSubmit`, use `additionalContext` em vez disso para injetar texto no contexto do Claude. Hooks baseados em prompt (`type: "prompt"`) lidam com saída de forma diferente: consulte [Hooks baseados em prompt](#prompt-based-hooks).

### Filtrar hooks com matchers

Sem um matcher, um hook dispara em cada ocorrência de seu evento. Matchers permitem restringir isso. Por exemplo, se você quer executar um formatador apenas após edições de arquivo (não após cada chamada de ferramenta), adicione um matcher ao seu hook `PostToolUse`:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          { "type": "command", "command": "prettier --write ..." }
        ]
      }
    ]
  }
}
```

O matcher `"Edit|Write"` é um padrão regex que corresponde ao nome da ferramenta. O hook dispara apenas quando Claude usa a ferramenta `Edit` ou `Write`, não quando usa `Bash`, `Read` ou qualquer outra ferramenta.

Cada tipo de evento corresponde a um campo específico. Matchers suportam strings exatas e padrões regex:

| Evento                                                                                                        | O que o matcher filtra                         | Valores de matcher de exemplo                                                                                             |
| :------------------------------------------------------------------------------------------------------------ | :--------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`                                        | nome da ferramenta                             | `Bash`, `Edit\|Write`, `mcp__.*`                                                                                          |
| `SessionStart`                                                                                                | como a sessão começou                          | `startup`, `resume`, `clear`, `compact`                                                                                   |
| `SessionEnd`                                                                                                  | por que a sessão terminou                      | `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`                                  |
| `Notification`                                                                                                | tipo de notificação                            | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`                                                  |
| `SubagentStart`                                                                                               | tipo de agente                                 | `Bash`, `Explore`, `Plan` ou nomes de agentes personalizados                                                              |
| `PreCompact`, `PostCompact`                                                                                   | o que acionou a compactação                    | `manual`, `auto`                                                                                                          |
| `SubagentStop`                                                                                                | tipo de agente                                 | mesmos valores que `SubagentStart`                                                                                        |
| `ConfigChange`                                                                                                | fonte de configuração                          | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`                                        |
| `StopFailure`                                                                                                 | tipo de erro                                   | `rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown` |
| `InstructionsLoaded`                                                                                          | motivo de carregamento                         | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`                                              |
| `Elicitation`                                                                                                 | nome do servidor MCP                           | seus nomes de servidor MCP configurados                                                                                   |
| `ElicitationResult`                                                                                           | nome do servidor MCP                           | mesmos valores que `Elicitation`                                                                                          |
| `FileChanged`                                                                                                 | nome do arquivo (basename do arquivo alterado) | `.envrc`, `.env`, qualquer nome de arquivo que você queira observar                                                       |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `CwdChanged` | sem suporte a matcher                          | sempre dispara em cada ocorrência                                                                                         |

Alguns exemplos adicionais mostrando matchers em diferentes tipos de evento:

<Tabs>
  <Tab title="Registrar cada comando Bash">
    Corresponda apenas chamadas de ferramenta `Bash` e registre cada comando em um arquivo. O evento `PostToolUse` dispara após o comando ser concluído, então `tool_input.command` contém o que foi executado. O hook recebe os dados do evento como JSON em stdin, e `jq -r '.tool_input.command'` extrai apenas a string de comando, que `>>` anexa ao arquivo de log:

    ```json  theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "command": "jq -r '.tool_input.command' >> ~/.claude/command-log.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Corresponder ferramentas MCP">
    Ferramentas MCP usam uma convenção de nomenclatura diferente das ferramentas integradas: `mcp__<server>__<tool>`, onde `<server>` é o nome do servidor MCP e `<tool>` é a ferramenta que fornece. Por exemplo, `mcp__github__search_repositories` ou `mcp__filesystem__read_file`. Use um matcher regex para direcionar todas as ferramentas de um servidor específico, ou corresponder entre servidores com um padrão como `mcp__.*__write.*`. Consulte [Corresponder ferramentas MCP](/pt/hooks#match-mcp-tools) na referência para a lista completa de exemplos.

    O comando abaixo extrai o nome da ferramenta da entrada JSON do hook com `jq` e o escreve para stderr, onde aparece em modo verboso (`Ctrl+O`):

    ```json  theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "mcp__github__.*",
            "hooks": [
              {
                "type": "command",
                "command": "echo \"GitHub tool called: $(jq -r '.tool_name')\" >&2"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Limpar ao final da sessão">
    O evento `SessionEnd` suporta matchers na razão pela qual a sessão terminou. Este hook dispara apenas em `clear` (quando você executa `/clear`), não em saídas normais:

    ```json  theme={null}
    {
      "hooks": {
        "SessionEnd": [
          {
            "matcher": "clear",
            "hooks": [
              {
                "type": "command",
                "command": "rm -f /tmp/claude-scratch-*.txt"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>
</Tabs>

Para sintaxe completa de matcher, consulte a [referência de Hooks](/pt/hooks#configuration).

### Configurar local do hook

Onde você adiciona um hook determina seu escopo:

| Local                                                       | Escopo                                | Compartilhável                         |
| :---------------------------------------------------------- | :------------------------------------ | :------------------------------------- |
| `~/.claude/settings.json`                                   | Todos os seus projetos                | Não, local para sua máquina            |
| `.claude/settings.json`                                     | Projeto único                         | Sim, pode ser commitado no repo        |
| `.claude/settings.local.json`                               | Projeto único                         | Não, gitignored                        |
| Configurações de política gerenciada                        | Organização inteira                   | Sim, controlado por admin              |
| [Plugin](/pt/plugins) `hooks/hooks.json`                    | Quando o plugin está habilitado       | Sim, empacotado com o plugin           |
| [Skill](/pt/skills) ou [agente](/pt/sub-agents) frontmatter | Enquanto a skill ou agente está ativo | Sim, definido no arquivo do componente |

Execute [`/hooks`](/pt/hooks#the-hooks-menu) no Claude Code para navegar por todos os hooks configurados agrupados por evento. Para desabilitar todos os hooks de uma vez, defina `"disableAllHooks": true` no seu arquivo de configuração.

Se você editar arquivos de configuração diretamente enquanto Claude Code está em execução, o observador de arquivo normalmente pega mudanças de hook automaticamente.

## Hooks baseados em prompt

Para decisões que exigem julgamento em vez de regras determinísticas, use hooks `type: "prompt"`. Em vez de executar um comando shell, Claude Code envia seu prompt e os dados de entrada do hook para um modelo Claude (Haiku por padrão) para tomar a decisão. Você pode especificar um modelo diferente com o campo `model` se precisar de mais capacidade.

O único trabalho do modelo é retornar uma decisão sim/não como JSON:

* `"ok": true`: a ação prossegue
* `"ok": false`: a ação é bloqueada. O `"reason"` do modelo é alimentado de volta ao Claude para que possa se ajustar.

Este exemplo usa um hook `Stop` para perguntar ao modelo se todas as tarefas solicitadas estão completas. Se o modelo retornar `"ok": false`, Claude continua trabalhando e usa o `reason` como sua próxima instrução:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Check if all tasks are complete. If not, respond with {\"ok\": false, \"reason\": \"what remains to be done\"}."
          }
        ]
      }
    ]
  }
}
```

Para opções de configuração completas, consulte [Hooks baseados em prompt](/pt/hooks#prompt-based-hooks) na referência.

## Hooks baseados em agente

Quando a verificação exige inspecionar arquivos ou executar comandos, use hooks `type: "agent"`. Diferentemente de hooks de prompt que fazem uma única chamada LLM, hooks de agente geram um subagente que pode ler arquivos, pesquisar código e usar outras ferramentas para verificar condições antes de retornar uma decisão.

Hooks de agente usam o mesmo formato de resposta `"ok"` / `"reason"` que hooks de prompt, mas com um timeout padrão mais longo de 60 segundos e até 50 turnos de uso de ferramenta.

Este exemplo verifica que os testes passam antes de permitir que Claude pare:

```json  theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

Use hooks de prompt quando os dados de entrada do hook sozinhos são suficientes para tomar uma decisão. Use hooks de agente quando você precisa verificar algo contra o estado real da base de código.

Para opções de configuração completas, consulte [Hooks baseados em agente](/pt/hooks#agent-based-hooks) na referência.

## HTTP hooks

Use hooks `type: "http"` para POST dados de evento para um endpoint HTTP em vez de executar um comando shell. O endpoint recebe o mesmo JSON que um hook de comando receberia em stdin, e retorna resultados através do corpo da resposta HTTP usando o mesmo formato JSON.

HTTP hooks são úteis quando você quer que um servidor web, função em nuvem ou serviço externo manipule a lógica do hook: por exemplo, um serviço de auditoria compartilhado que registra eventos de uso de ferramenta em toda uma equipe.

Este exemplo posta cada uso de ferramenta para um serviço de logging local:

```json  theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/tool-use",
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

O endpoint deve retornar um corpo de resposta JSON usando o mesmo [formato de saída](/pt/hooks#json-output) que hooks de comando. Para bloquear uma chamada de ferramenta, retorne uma resposta 2xx com os campos `hookSpecificOutput` apropriados. Códigos de status HTTP sozinhos não podem bloquear ações.

Valores de header suportam interpolação de variável de ambiente usando sintaxe `$VAR_NAME` ou `${VAR_NAME}`. Apenas variáveis listadas no array `allowedEnvVars` são resolvidas; todas as outras referências `$VAR` permanecem vazias.

Para opções de configuração completas e manipulação de resposta, consulte [HTTP hooks](/pt/hooks#http-hook-fields) na referência.

## Limitações e solução de problemas

### Limitações

* Hooks de comando se comunicam apenas através de stdout, stderr e códigos de saída. Eles não podem disparar comandos ou chamadas de ferramenta diretamente. HTTP hooks se comunicam através do corpo da resposta em vez disso.
* O timeout do hook é 10 minutos por padrão, configurável por hook com o campo `timeout` (em segundos).
* Hooks `PostToolUse` não podem desfazer ações já que a ferramenta já foi executada.
* Hooks `PermissionRequest` não disparam em [modo não-interativo](/pt/headless) (`-p`). Use hooks `PreToolUse` para decisões de permissão automatizadas.
* Hooks `Stop` disparam sempre que Claude termina de responder, não apenas na conclusão de tarefas. Eles não disparam em interrupções do usuário. Erros de API disparam [StopFailure](/pt/hooks#stopfailure) em vez disso.

### Hook não dispara

O hook está configurado mas nunca executa.

* Execute `/hooks` e confirme que o hook aparece sob o evento correto
* Verifique que o padrão do matcher corresponde ao nome da ferramenta exatamente (matchers são sensíveis a maiúsculas)
* Verifique que você está acionando o tipo de evento correto (por exemplo, `PreToolUse` dispara antes da execução da ferramenta, `PostToolUse` dispara depois)
* Se usar hooks `PermissionRequest` em modo não-interativo (`-p`), mude para `PreToolUse` em vez disso

### Erro de hook na saída

Você vê uma mensagem como "PreToolUse hook error: ..." na transcrição.

* Seu script saiu com um código não-zero inesperadamente. Teste-o manualmente canalizando JSON de amostra:
  ```bash  theme={null}
  echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
  echo $?  # Verifique o código de saída
  ```
* Se você vir "command not found", use caminhos absolutos ou `$CLAUDE_PROJECT_DIR` para referenciar scripts
* Se você vir "jq: command not found", instale `jq` ou use Python/Node.js para análise JSON
* Se o script não está executando em tudo, torne-o executável: `chmod +x ./my-hook.sh`

### `/hooks` mostra nenhum hook configurado

Você editou um arquivo de configuração mas os hooks não aparecem no menu.

* Edições de arquivo são normalmente capturadas automaticamente. Se não tiverem aparecido após alguns segundos, o observador de arquivo pode ter perdido a mudança: reinicie sua sessão para forçar um recarregamento.
* Verifique que seu JSON é válido (vírgulas finais e comentários não são permitidos)
* Confirme que o arquivo de configuração está no local correto: `.claude/settings.json` para hooks de projeto, `~/.claude/settings.json` para hooks globais

### Stop hook executa para sempre

Claude continua trabalhando em um loop infinito em vez de parar.

Seu script de Stop hook precisa verificar se já acionou uma continuação. Analise o campo `stop_hook_active` da entrada JSON e saia cedo se for `true`:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # Permitir que Claude pare
fi
# ... resto da lógica do seu hook
```

### Validação JSON falhou

Claude Code mostra um erro de análise JSON mesmo que seu script de hook produza JSON válido.

Quando Claude Code executa um hook, ele gera um shell que fornece seu perfil (`~/.zshrc` ou `~/.bashrc`). Se seu perfil contiver instruções `echo` incondicionais, essa saída é adicionada ao seu JSON do hook:

```text  theme={null}
Shell ready on arm64
{"decision": "block", "reason": "Not allowed"}
```

Claude Code tenta analisar isto como JSON e falha. Para corrigir isto, envolva instruções echo no seu perfil shell para que executem apenas em shells interativos:

```bash  theme={null}
# Em ~/.zshrc ou ~/.bashrc
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

A variável `$-` contém flags de shell, e `i` significa interativo. Hooks executam em shells não-interativos, então o echo é pulado.

### Técnicas de debug

Alterne o modo verboso com `Ctrl+O` para ver a saída do hook na transcrição, ou execute `claude --debug` para detalhes de execução completos incluindo quais hooks corresponderam e seus códigos de saída.

## Saiba mais

* [Referência de Hooks](/pt/hooks): esquemas de eventos completos, formato de saída JSON, hooks assíncronos e hooks de ferramentas MCP
* [Considerações de segurança](/pt/hooks#security-considerations): revise antes de implantar hooks em ambientes compartilhados ou de produção
* [Exemplo de validador de comando Bash](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py): implementação de referência completa
