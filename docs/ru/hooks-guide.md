> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Автоматизация рабочих процессов с помощью hooks

> Запускайте команды оболочки автоматически, когда Claude Code редактирует файлы, завершает задачи или требует ввода. Форматируйте код, отправляйте уведомления, проверяйте команды и применяйте правила проекта.

Hooks — это определяемые пользователем команды оболочки, которые выполняются в определённых точках жизненного цикла Claude Code. Они обеспечивают детерминированный контроль над поведением Claude Code, гарантируя, что определённые действия всегда происходят, а не полагаясь на то, что LLM выберет их запуск. Используйте hooks для применения правил проекта, автоматизации повторяющихся задач и интеграции Claude Code с вашими существующими инструментами.

Для решений, требующих суждения, а не детерминированных правил, вы также можете использовать [hooks на основе подсказок](#prompt-based-hooks) или [hooks на основе агентов](#agent-based-hooks), которые используют модель Claude для оценки условий.

Для других способов расширения Claude Code см. [skills](/ru/skills) для предоставления Claude дополнительных инструкций и исполняемых команд, [subagents](/ru/sub-agents) для запуска задач в изолированных контекстах и [plugins](/ru/plugins) для упаковки расширений для совместного использования в проектах.

<Tip>
  Это руководство охватывает распространённые варианты использования и как начать работу. Для полных схем событий, форматов JSON ввода/вывода и расширенных функций, таких как асинхронные hooks и MCP tool hooks, см. [справочник Hooks](/ru/hooks).
</Tip>

## Настройка вашего первого hook

Самый быстрый способ создать hook — это использовать интерактивное меню `/hooks` в Claude Code. В этом пошаговом руководстве создаётся hook для уведомлений на рабочем столе, чтобы вы получали оповещение всякий раз, когда Claude ждёт вашего ввода вместо того, чтобы смотреть на терминал.

<Steps>
  <Step title="Откройте меню hooks">
    Введите `/hooks` в CLI Claude Code. Вы увидите список всех доступных событий hook, а также опцию отключения всех hooks. Каждое событие соответствует точке в жизненном цикле Claude, где вы можете запустить пользовательский код. Выберите `Notification`, чтобы создать hook, который срабатывает, когда Claude требует вашего внимания.
  </Step>

  <Step title="Настройте matcher">
    Меню показывает список matchers, которые фильтруют, когда срабатывает hook. Установите matcher на `*`, чтобы срабатывать на все типы уведомлений. Вы можете сузить его позже, изменив matcher на конкретное значение, такое как `permission_prompt` или `idle_prompt`.
  </Step>

  <Step title="Добавьте вашу команду">
    Выберите `+ Add new hook…`. Меню запросит у вас команду оболочки для запуска при срабатывании события. Hooks запускают любую команду оболочки, которую вы предоставляете, поэтому вы можете использовать встроенный инструмент уведомлений вашей платформы. Скопируйте команду для вашей ОС:

    <Tabs>
      <Tab title="macOS">
        Использует [`osascript`](https://ss64.com/mac/osascript.html) для запуска собственного уведомления macOS через AppleScript:

        ```bash  theme={null}
        osascript -e 'display notification "Claude Code needs your attention" with title "Claude Code"'
        ```
      </Tab>

      <Tab title="Linux">
        Использует `notify-send`, который предустановлен на большинстве рабочих столов Linux с демоном уведомлений:

        ```bash  theme={null}
        notify-send 'Claude Code' 'Claude Code needs your attention'
        ```
      </Tab>

      <Tab title="Windows (PowerShell)">
        Использует PowerShell для отображения собственного окна сообщения через Windows Forms .NET:

        ```powershell  theme={null}
        powershell.exe -Command "[System.Reflection.Assembly]::LoadWithPartialName('System.Windows.Forms'); [System.Windows.Forms.MessageBox]::Show('Claude Code needs your attention', 'Claude Code')"
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Выберите место хранения">
    Меню спросит, где сохранить конфигурацию hook. Выберите `User settings`, чтобы сохранить её в `~/.claude/settings.json`, что применит hook ко всем вашим проектам. Вы также можете выбрать `Project settings`, чтобы ограничить его текущим проектом. См. [Настройка местоположения hook](#configure-hook-location) для всех доступных областей.
  </Step>

  <Step title="Протестируйте hook">
    Нажмите `Esc`, чтобы вернуться в CLI. Попросите Claude сделать что-то, что требует разрешения, затем переключитесь с терминала. Вы должны получить уведомление на рабочем столе.
  </Step>
</Steps>

## Что вы можете автоматизировать

Hooks позволяют запускать код в ключевых точках жизненного цикла Claude Code: форматировать файлы после редактирования, блокировать команды перед их выполнением, отправлять уведомления, когда Claude требует ввода, внедрять контекст при запуске сеанса и многое другое. Для полного списка событий hook см. [справочник Hooks](/ru/hooks#hook-lifecycle).

Каждый пример включает готовый к использованию блок конфигурации, который вы добавляете в [файл параметров](#configure-hook-location). Наиболее распространённые шаблоны:

* [Получайте уведомления, когда Claude требует ввода](#get-notified-when-claude-needs-input)
* [Автоматическое форматирование кода после редактирования](#auto-format-code-after-edits)
* [Блокировка редактирования защищённых файлов](#block-edits-to-protected-files)
* [Повторное внедрение контекста после компактирования](#re-inject-context-after-compaction)
* [Аудит изменений конфигурации](#audit-configuration-changes)

### Получайте уведомления, когда Claude требует ввода

Получайте уведомление на рабочем столе всякий раз, когда Claude завершает работу и требует вашего ввода, чтобы вы могли переключиться на другие задачи без проверки терминала.

Этот hook использует событие `Notification`, которое срабатывает, когда Claude ждёт ввода или разрешения. Каждая вкладка ниже использует собственную команду уведомлений платформы. Добавьте это в `~/.claude/settings.json` или используйте [интерактивное пошаговое руководство](#set-up-your-first-hook) выше, чтобы настроить его с помощью `/hooks`:

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

### Автоматическое форматирование кода после редактирования

Автоматически запускайте [Prettier](https://prettier.io/) на каждом файле, который редактирует Claude, чтобы форматирование оставалось согласованным без ручного вмешательства.

Этот hook использует событие `PostToolUse` с matcher `Edit|Write`, поэтому он запускается только после инструментов редактирования файлов. Команда извлекает путь отредактированного файла с помощью [`jq`](https://jqlang.github.io/jq/) и передаёт его в Prettier. Добавьте это в `.claude/settings.json` в корне вашего проекта:

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
  Примеры Bash на этой странице используют `jq` для анализа JSON. Установите его с помощью `brew install jq` (macOS), `apt-get install jq` (Debian/Ubuntu) или см. [загрузки `jq`](https://jqlang.github.io/jq/download/).
</Note>

### Блокировка редактирования защищённых файлов

Предотвратите изменение Claude чувствительных файлов, таких как `.env`, `package-lock.json` или что-либо в `.git/`. Claude получает обратную связь, объясняющую, почему редактирование было заблокировано, чтобы он мог скорректировать свой подход.

Этот пример использует отдельный файл скрипта, который вызывает hook. Скрипт проверяет путь целевого файла по списку защищённых шаблонов и выходит с кодом 2, чтобы заблокировать редактирование.

<Steps>
  <Step title="Создайте скрипт hook">
    Сохраните это в `.claude/hooks/protect-files.sh`:

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

  <Step title="Сделайте скрипт исполняемым (macOS/Linux)">
    Скрипты hook должны быть исполняемыми, чтобы Claude Code мог их запустить:

    ```bash  theme={null}
    chmod +x .claude/hooks/protect-files.sh
    ```
  </Step>

  <Step title="Зарегистрируйте hook">
    Добавьте hook `PreToolUse` в `.claude/settings.json`, который запускает скрипт перед любым вызовом инструмента `Edit` или `Write`:

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

### Повторное внедрение контекста после компактирования

Когда context window Claude заполняется, компактирование суммирует разговор, чтобы освободить место. Это может привести к потере важных деталей. Используйте hook `SessionStart` с matcher `compact`, чтобы повторно внедрить критический контекст после каждого компактирования.

Любой текст, который ваша команда выводит в stdout, добавляется в контекст Claude. Этот пример напоминает Claude о соглашениях проекта и недавней работе. Добавьте это в `.claude/settings.json` в корне вашего проекта:

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

Вы можете заменить `echo` любой командой, которая производит динамический вывод, например `git log --oneline -5` для отображения недавних коммитов. Для внедрения контекста при каждом запуске сеанса рассмотрите использование [CLAUDE.md](/ru/memory) вместо этого. Для переменных окружения см. [`CLAUDE_ENV_FILE`](/ru/hooks#persist-environment-variables) в справочнике.

### Аудит изменений конфигурации

Отслеживайте, когда файлы параметров или skills изменяются во время сеанса. Событие `ConfigChange` срабатывает, когда внешний процесс или редактор изменяет файл конфигурации, поэтому вы можете регистрировать изменения для соответствия или блокировать несанкционированные изменения.

Этот пример добавляет каждое изменение в журнал аудита. Добавьте это в `~/.claude/settings.json`:

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

Matcher фильтрует по типу конфигурации: `user_settings`, `project_settings`, `local_settings`, `policy_settings` или `skills`. Чтобы заблокировать вступление изменения в силу, выйдите с кодом 2 или верните `{"decision": "block"}`. См. [справочник ConfigChange](/ru/hooks#configchange) для полной схемы ввода.

## Как работают hooks

События hook срабатывают в определённых точках жизненного цикла Claude Code. Когда событие срабатывает, все соответствующие hooks запускаются параллельно, и идентичные команды hook автоматически дедублируются. Таблица ниже показывает каждое событие и когда оно срабатывает:

| Event                | When it fires                                                                                                                                  |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                               |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                           |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                      |
| `PermissionRequest`  | When a permission dialog appears                                                                                                               |
| `PostToolUse`        | After a tool call succeeds                                                                                                                     |
| `PostToolUseFailure` | After a tool call fails                                                                                                                        |
| `Notification`       | When Claude Code sends a notification                                                                                                          |
| `SubagentStart`      | When a subagent is spawned                                                                                                                     |
| `SubagentStop`       | When a subagent finishes                                                                                                                       |
| `Stop`               | When Claude finishes responding                                                                                                                |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                             |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                       |
| `InstructionsLoaded` | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session |
| `ConfigChange`       | When a configuration file changes during a session                                                                                             |
| `WorktreeCreate`     | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                    |
| `WorktreeRemove`     | When a worktree is being removed, either at session exit or when a subagent finishes                                                           |
| `PreCompact`         | Before context compaction                                                                                                                      |
| `PostCompact`        | After context compaction completes                                                                                                             |
| `Elicitation`        | When an MCP server requests user input during a tool call                                                                                      |
| `ElicitationResult`  | After a user responds to an MCP elicitation, before the response is sent back to the server                                                    |
| `SessionEnd`         | When a session terminates                                                                                                                      |

Каждый hook имеет `type`, который определяет, как он запускается. Большинство hooks используют `"type": "command"`, который запускает команду оболочки. Доступны три других типа:

* `"type": "http"`: POST данные события на URL. См. [HTTP hooks](#http-hooks).
* `"type": "prompt"`: однооборотная оценка LLM. См. [Hooks на основе подсказок](#prompt-based-hooks).
* `"type": "agent"`: многооборотная проверка с доступом к инструментам. См. [Hooks на основе агентов](#agent-based-hooks).

### Чтение ввода и возврат вывода

Hooks взаимодействуют с Claude Code через stdin, stdout, stderr и коды выхода. Когда событие срабатывает, Claude Code передаёт данные, специфичные для события, в виде JSON в stdin вашего скрипта. Ваш скрипт читает эти данные, выполняет свою работу и сообщает Claude Code, что делать дальше, через код выхода.

#### Ввод hook

Каждое событие включает общие поля, такие как `session_id` и `cwd`, но каждый тип события добавляет разные данные. Например, когда Claude запускает команду Bash, hook `PreToolUse` получает что-то вроде этого на stdin:

```json  theme={null}
{
  "session_id": "abc123",          // уникальный ID для этого сеанса
  "cwd": "/Users/sarah/myproject", // рабочий каталог при срабатывании события
  "hook_event_name": "PreToolUse", // какое событие запустило этот hook
  "tool_name": "Bash",             // инструмент, который Claude собирается использовать
  "tool_input": {                  // аргументы, которые Claude передал инструменту
    "command": "npm test"          // для Bash это команда оболочки
  }
}
```

Ваш скрипт может анализировать этот JSON и действовать на основе любого из этих полей. Hooks `UserPromptSubmit` получают текст `prompt` вместо этого, hooks `SessionStart` получают `source` (startup, resume, clear, compact) и так далее. См. [Общие поля ввода](/ru/hooks#common-input-fields) в справочнике для общих полей и раздел каждого события для схем, специфичных для события.

#### Вывод hook

Ваш скрипт сообщает Claude Code, что делать дальше, записывая в stdout или stderr и выходя с определённым кодом. Например, hook `PreToolUse`, который хочет заблокировать команду:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q "drop table"; then
  echo "Blocked: dropping tables is not allowed" >&2  # stderr становится обратной связью Claude
  exit 2 # exit 2 = заблокировать действие
fi

exit 0  # exit 0 = позволить ему продолжиться
```

Код выхода определяет, что происходит дальше:

* **Exit 0**: действие продолжается. Для hooks `UserPromptSubmit` и `SessionStart` всё, что вы пишете в stdout, добавляется в контекст Claude.
* **Exit 2**: действие заблокировано. Напишите причину в stderr, и Claude получит её как обратную связь, чтобы он мог скорректировать.
* **Любой другой код выхода**: действие продолжается. Stderr регистрируется, но не показывается Claude. Переключите режим подробности с помощью `Ctrl+O`, чтобы увидеть эти сообщения в стенограмме.

#### Структурированный вывод JSON

Коды выхода дают вам два варианта: разрешить или заблокировать. Для большего контроля выйдите с кодом 0 и выведите объект JSON в stdout вместо этого.

<Note>
  Используйте exit 2 для блокировки с сообщением stderr или exit 0 с JSON для структурированного контроля. Не смешивайте их: Claude Code игнорирует JSON, когда вы выходите с кодом 2.
</Note>

Например, hook `PreToolUse` может отклонить вызов инструмента и сказать Claude почему, или передать его пользователю на одобрение:

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "deny",
    "permissionDecisionReason": "Use rg instead of grep for better performance"
  }
}
```

Claude Code читает `permissionDecision` и отменяет вызов инструмента, затем передаёт `permissionDecisionReason` обратно Claude как обратную связь. Эти три варианта специфичны для `PreToolUse`:

* `"allow"`: продолжить без отображения подсказки разрешения
* `"deny"`: отменить вызов инструмента и отправить причину Claude
* `"ask"`: показать подсказку разрешения пользователю как обычно

Другие события используют разные шаблоны решений. Например, hooks `PostToolUse` и `Stop` используют поле `decision: "block"` верхнего уровня, а `PermissionRequest` использует `hookSpecificOutput.decision.behavior`. См. [таблицу сводки](/ru/hooks#decision-control) в справочнике для полного разбора по событиям.

Для hooks `UserPromptSubmit` используйте `additionalContext` вместо этого для внедрения текста в контекст Claude. Hooks на основе подсказок (`type: "prompt"`) обрабатывают вывод иначе: см. [Hooks на основе подсказок](#prompt-based-hooks).

### Фильтрация hooks с помощью matchers

Без matcher hook срабатывает при каждом возникновении его события. Matchers позволяют вам сузить это. Например, если вы хотите запустить форматер только после редактирования файлов (не после каждого вызова инструмента), добавьте matcher к вашему hook `PostToolUse`:

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

Matcher `"Edit|Write"` — это шаблон regex, который соответствует имени инструмента. Hook срабатывает только, когда Claude использует инструмент `Edit` или `Write`, а не когда он использует `Bash`, `Read` или любой другой инструмент.

Каждый тип события соответствует определённому полю. Matchers поддерживают точные строки и шаблоны regex:

| Событие                                                                                         | Что фильтрует matcher         | Примеры значений matcher                                                           |
| :---------------------------------------------------------------------------------------------- | :---------------------------- | :--------------------------------------------------------------------------------- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`                          | имя инструмента               | `Bash`, `Edit\|Write`, `mcp__.*`                                                   |
| `SessionStart`                                                                                  | как начался сеанс             | `startup`, `resume`, `clear`, `compact`                                            |
| `SessionEnd`                                                                                    | почему закончился сеанс       | `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`     |
| `Notification`                                                                                  | тип уведомления               | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`           |
| `SubagentStart`                                                                                 | тип агента                    | `Bash`, `Explore`, `Plan` или пользовательские имена агентов                       |
| `PreCompact`                                                                                    | что запустило компактирование | `manual`, `auto`                                                                   |
| `SubagentStop`                                                                                  | тип агента                    | те же значения, что и `SubagentStart`                                              |
| `ConfigChange`                                                                                  | источник конфигурации         | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | поддержка matcher отсутствует | всегда срабатывает при каждом возникновении                                        |

Несколько дополнительных примеров, показывающих matchers на разных типах событий:

<Tabs>
  <Tab title="Логирование каждой команды Bash">
    Соответствуйте только вызовам инструмента `Bash` и регистрируйте каждую команду в файл. Событие `PostToolUse` срабатывает после завершения команды, поэтому `tool_input.command` содержит то, что было запущено. Hook получает данные события в виде JSON на stdin, и `jq -r '.tool_input.command'` извлекает только строку команды, которую `>>` добавляет в файл журнала:

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

  <Tab title="Соответствие MCP инструментам">
    MCP инструменты используют другое соглашение об именовании, чем встроенные инструменты: `mcp__<server>__<tool>`, где `<server>` — это имя MCP сервера, а `<tool>` — это инструмент, который он предоставляет. Например, `mcp__github__search_repositories` или `mcp__filesystem__read_file`. Используйте matcher regex для нацеливания на все инструменты с определённого сервера или соответствуйте серверам с шаблоном, таким как `mcp__.*__write.*`. См. [Соответствие MCP инструментам](/ru/hooks#match-mcp-tools) в справочнике для полного списка примеров.

    Команда ниже извлекает имя инструмента из JSON ввода hook с помощью `jq` и записывает его в stderr, где оно появляется в режиме подробности (`Ctrl+O`):

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

  <Tab title="Очистка при завершении сеанса">
    Событие `SessionEnd` поддерживает matchers на причину завершения сеанса. Этот hook срабатывает только на `clear` (когда вы запускаете `/clear`), а не на нормальные выходы:

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

Для полного синтаксиса matcher см. [справочник Hooks](/ru/hooks#configuration).

### Настройка местоположения hook

Где вы добавляете hook, определяет его область:

| Местоположение                                              | Область                      | Общий доступ                       |
| :---------------------------------------------------------- | :--------------------------- | :--------------------------------- |
| `~/.claude/settings.json`                                   | Все ваши проекты             | Нет, локально на вашей машине      |
| `.claude/settings.json`                                     | Один проект                  | Да, можно зафиксировать в репо     |
| `.claude/settings.local.json`                               | Один проект                  | Нет, gitignored                    |
| Управляемые параметры политики                              | Организация                  | Да, контролируется администратором |
| [Plugin](/ru/plugins) `hooks/hooks.json`                    | Когда плагин включен         | Да, упакован с плагином            |
| [Skill](/ru/skills) или [agent](/ru/sub-agents) frontmatter | Пока skill или agent активен | Да, определено в файле компонента  |

Вы также можете использовать меню [`/hooks`](/ru/hooks#the-hooks-menu) в Claude Code для интерактивного добавления, удаления и просмотра hooks. Чтобы отключить все hooks сразу, используйте переключатель в нижней части меню `/hooks` или установите `"disableAllHooks": true` в файле параметров.

Hooks, добавленные через меню `/hooks`, вступают в силу немедленно. Если вы редактируете файлы параметров напрямую во время работы Claude Code, изменения не вступят в силу до тех пор, пока вы не просмотрите их в меню `/hooks` или не перезагрузите сеанс.

## Hooks на основе подсказок

Для решений, требующих суждения, а не детерминированных правил, используйте hooks `type: "prompt"`. Вместо запуска команды оболочки Claude Code отправляет вашу подсказку и данные ввода hook модели Claude (Haiku по умолчанию) для принятия решения. Вы можете указать другую модель с полем `model`, если вам нужна большая возможность.

Единственная работа модели — вернуть решение да/нет в виде JSON:

* `"ok": true`: действие продолжается
* `"ok": false`: действие заблокировано. `"reason"` модели передаётся обратно Claude, чтобы он мог скорректировать.

Этот пример использует hook `Stop` для запроса модели, завершены ли все запрошенные задачи. Если модель возвращает `"ok": false`, Claude продолжает работать и использует `reason` как свою следующую инструкцию:

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

Для полных параметров конфигурации см. [Hooks на основе подсказок](/ru/hooks#prompt-based-hooks) в справочнике.

## Hooks на основе агентов

Когда проверка требует проверки файлов или запуска команд, используйте hooks `type: "agent"`. В отличие от hooks подсказок, которые делают один вызов LLM, hooks агентов порождают subagent, который может читать файлы, искать код и использовать другие инструменты для проверки условий перед возвратом решения.

Hooks агентов используют тот же формат ответа `"ok"` / `"reason"`, что и hooks подсказок, но с более длительным временем ожидания по умолчанию 60 секунд и до 50 оборотов использования инструментов.

Этот пример проверяет, что тесты проходят перед тем, как позволить Claude остановиться:

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

Используйте hooks подсказок, когда данных ввода hook достаточно для принятия решения. Используйте hooks агентов, когда вам нужно проверить что-то против фактического состояния кодовой базы.

Для полных параметров конфигурации см. [Hooks на основе агентов](/ru/hooks#agent-based-hooks) в справочнике.

## HTTP hooks

Используйте hooks `type: "http"` для POST данных события на HTTP endpoint вместо запуска команды оболочки. Endpoint получает тот же JSON, который hook команды получил бы на stdin, и возвращает результаты через тело ответа HTTP, используя тот же формат JSON.

HTTP hooks полезны, когда вы хотите, чтобы веб-сервер, облачная функция или внешний сервис обрабатывали логику hook: например, общий сервис аудита, который регистрирует события использования инструментов в команде.

Этот пример отправляет каждое использование инструмента на локальный сервис логирования:

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

Endpoint должен вернуть тело ответа JSON, используя тот же [формат вывода](/ru/hooks#json-output), что и hooks команд. Чтобы заблокировать вызов инструмента, верните ответ 2xx с соответствующими полями `hookSpecificOutput`. Коды статуса HTTP сами по себе не могут блокировать действия.

Значения заголовков поддерживают интерполяцию переменных окружения, используя синтаксис `$VAR_NAME` или `${VAR_NAME}`. Разрешены только переменные, указанные в массиве `allowedEnvVars`; все остальные ссылки `$VAR` остаются пустыми.

<Note>
  HTTP hooks должны быть настроены путём прямого редактирования JSON параметров. Интерактивное меню `/hooks` поддерживает только добавление hooks команд.
</Note>

Для полных параметров конфигурации и обработки ответов см. [HTTP hooks](/ru/hooks#http-hook-fields) в справочнике.

## Ограничения и устранение неполадок

### Ограничения

* Hooks команд взаимодействуют только через stdout, stderr и коды выхода. Они не могут напрямую запускать команды или вызовы инструментов. HTTP hooks взаимодействуют через тело ответа вместо этого.
* Время ожидания hook по умолчанию составляет 10 минут, настраивается для каждого hook с помощью поля `timeout` (в секундах).
* Hooks `PostToolUse` не могут отменить действия, так как инструмент уже выполнен.
* Hooks `PermissionRequest` не срабатывают в [неинтерактивном режиме](/ru/headless) (`-p`). Используйте hooks `PreToolUse` для автоматизированных решений разрешений.
* Hooks `Stop` срабатывают всякий раз, когда Claude завершает ответ, а не только при завершении задачи. Они не срабатывают при прерывании пользователем.

### Hook не срабатывает

Hook настроен, но никогда не выполняется.

* Запустите `/hooks` и подтвердите, что hook появляется под правильным событием
* Проверьте, что шаблон matcher точно соответствует имени инструмента (matchers чувствительны к регистру)
* Убедитесь, что вы запускаете правильный тип события (например, `PreToolUse` срабатывает перед выполнением инструмента, `PostToolUse` срабатывает после)
* Если используете hooks `PermissionRequest` в неинтерактивном режиме (`-p`), переключитесь на `PreToolUse` вместо этого

### Ошибка hook в выводе

Вы видите сообщение вроде "PreToolUse hook error: ..." в стенограмме.

* Ваш скрипт неожиданно вышел с ненулевым кодом. Протестируйте его вручную, передав образец JSON:
  ```bash  theme={null}
  echo '{"tool_name":"Bash","tool_input":{"command":"ls"}}' | ./my-hook.sh
  echo $?  # Проверьте код выхода
  ```
* Если вы видите "command not found", используйте абсолютные пути или `$CLAUDE_PROJECT_DIR` для ссылки на скрипты
* Если вы видите "jq: command not found", установите `jq` или используйте Python/Node.js для анализа JSON
* Если скрипт вообще не запускается, сделайте его исполняемым: `chmod +x ./my-hook.sh`

### `/hooks` показывает, что hooks не настроены

Вы отредактировали файл параметров, но hooks не появляются в меню.

* Перезагрузите сеанс или откройте `/hooks` для перезагрузки. Hooks, добавленные через меню `/hooks`, вступают в силу немедленно, но ручные редактирования файлов требуют перезагрузки.
* Убедитесь, что ваш JSON действителен (запятые в конце и комментарии не допускаются)
* Подтвердите, что файл параметров находится в правильном месте: `.claude/settings.json` для hooks проекта, `~/.claude/settings.json` для глобальных hooks

### Hook Stop работает бесконечно

Claude продолжает работать в бесконечном цикле вместо остановки.

Ваш скрипт Stop hook должен проверить, не сработал ли он уже. Проанализируйте поле `stop_hook_active` из JSON ввода и выйдите рано, если оно `true`:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
if [ "$(echo "$INPUT" | jq -r '.stop_hook_active')" = "true" ]; then
  exit 0  # Позволить Claude остановиться
fi
# ... остальная логика hook
```

### Ошибка валидации JSON

Claude Code показывает ошибку анализа JSON, даже если ваш скрипт hook выводит действительный JSON.

Когда Claude Code запускает hook, он порождает оболочку, которая источает ваш профиль (`~/.zshrc` или `~/.bashrc`). Если ваш профиль содержит безусловные операторы `echo`, этот вывод добавляется к JSON вашего hook:

```text  theme={null}
Shell ready on arm64
{"decision": "block", "reason": "Not allowed"}
```

Claude Code пытается проанализировать это как JSON и не удаётся. Чтобы исправить это, оберните операторы echo в вашем профиле оболочки, чтобы они запускались только в интерактивных оболочках:

```bash  theme={null}
# В ~/.zshrc или ~/.bashrc
if [[ $- == *i* ]]; then
  echo "Shell ready"
fi
```

Переменная `$-` содержит флаги оболочки, и `i` означает интерактивный. Hooks запускаются в неинтерактивных оболочках, поэтому echo пропускается.

### Методы отладки

Переключите режим подробности с помощью `Ctrl+O`, чтобы увидеть вывод hook в стенограмме, или запустите `claude --debug` для полных деталей выполнения, включая какие hooks совпали и их коды выхода.

## Узнайте больше

* [Справочник Hooks](/ru/hooks): полные схемы событий, формат вывода JSON, асинхронные hooks и MCP tool hooks
* [Соображения безопасности](/ru/hooks#security-considerations): просмотрите перед развёртыванием hooks в общих или производственных средах
* [Пример валидатора команд Bash](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py): полная эталонная реализация
