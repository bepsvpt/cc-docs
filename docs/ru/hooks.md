> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Справочник по hooks

> Справочник по событиям hook Claude Code, схеме конфигурации, форматам JSON входа/выхода, кодам выхода, асинхронным hooks, HTTP hooks, prompt hooks и MCP tool hooks.

<Tip>
  Для краткого руководства с примерами см. [Автоматизация рабочих процессов с помощью hooks](/ru/hooks-guide).
</Tip>

Hooks — это определяемые пользователем команды оболочки, конечные точки HTTP или подсказки LLM, которые выполняются автоматически в определённых точках жизненного цикла Claude Code. Используйте этот справочник для поиска схем событий, параметров конфигурации, форматов JSON входа/выхода и расширенных функций, таких как асинхронные hooks, HTTP hooks и MCP tool hooks. Если вы настраиваете hooks впервые, начните с [руководства](/ru/hooks-guide).

## Жизненный цикл hook

Hooks срабатывают в определённых точках во время сеанса Claude Code. Когда событие срабатывает и совпадает с фильтром, Claude Code передаёт JSON-контекст события вашему обработчику hook. Для command hooks входные данные поступают на stdin. Для HTTP hooks они поступают как тело POST-запроса. Ваш обработчик может затем проверить входные данные, выполнить действие и опционально вернуть решение. Некоторые события срабатывают один раз за сеанс, а другие срабатывают повторно внутри агентного цикла:

<div style={{maxWidth: "500px", margin: "0 auto"}}>
  <Frame>
    <img src="https://mintcdn.com/claude-code/UMJp-WgTWngzO609/images/hooks-lifecycle.svg?fit=max&auto=format&n=UMJp-WgTWngzO609&q=85&s=3f4de67df216c87dc313943b32c15f62" alt="Диаграмма жизненного цикла hook, показывающая последовательность hooks от SessionStart через агентный цикл (PreToolUse, PermissionRequest, PostToolUse, SubagentStart/Stop, TaskCreated, TaskCompleted) к Stop или StopFailure, TeammateIdle, PreCompact, PostCompact и SessionEnd, с Elicitation и ElicitationResult вложенными внутри выполнения MCP tool, PermissionDenied как боковая ветвь от PermissionRequest для автоматических отказов, и WorktreeCreate, WorktreeRemove, Notification, ConfigChange, InstructionsLoaded, CwdChanged и FileChanged как отдельные асинхронные события" width="520" height="1155" data-path="images/hooks-lifecycle.svg" />
  </Frame>
</div>

Таблица ниже суммирует, когда срабатывает каждое событие. Раздел [Hook events](#hook-events) документирует полную схему входа и параметры управления решением для каждого события.

| Event                | When it fires                                                                                                                                          |
| :------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`       | When a session begins or resumes                                                                                                                       |
| `UserPromptSubmit`   | When you submit a prompt, before Claude processes it                                                                                                   |
| `PreToolUse`         | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`  | When a permission dialog appears                                                                                                                       |
| `PermissionDenied`   | When a tool call is denied by the auto mode classifier. Return `{retry: true}` to tell the model it may retry the denied tool call                     |
| `PostToolUse`        | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure` | After a tool call fails                                                                                                                                |
| `Notification`       | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`      | When a subagent is spawned                                                                                                                             |
| `SubagentStop`       | When a subagent finishes                                                                                                                               |
| `TaskCreated`        | When a task is being created via `TaskCreate`                                                                                                          |
| `TaskCompleted`      | When a task is being marked as completed                                                                                                               |
| `Stop`               | When Claude finishes responding                                                                                                                        |
| `StopFailure`        | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`       | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
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

### Как разрешается hook

Чтобы увидеть, как эти части работают вместе, рассмотрим этот hook `PreToolUse`, который блокирует деструктивные команды оболочки. Фильтр `matcher` сужает область до вызовов инструмента Bash, а условие `if` сужает её дальше до команд, начинающихся с `rm`, поэтому `block-rm.sh` запускается только когда оба фильтра совпадают:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "if": "Bash(rm *)",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

Скрипт читает JSON входные данные из stdin, извлекает команду и возвращает `permissionDecision` со значением `"deny"`, если она содержит `rm -rf`:

```bash theme={null}
#!/bin/bash
# .claude/hooks/block-rm.sh
COMMAND=$(jq -r '.tool_input.command')

if echo "$COMMAND" | grep -q 'rm -rf'; then
  jq -n '{
    hookSpecificOutput: {
      hookEventName: "PreToolUse",
      permissionDecision: "deny",
      permissionDecisionReason: "Destructive command blocked by hook"
    }
  }'
else
  exit 0  # allow the command
fi
```

Теперь предположим, что Claude Code решает запустить `Bash "rm -rf /tmp/build"`. Вот что происходит:

<Frame>
  <img src="https://mintcdn.com/claude-code/-tYw1BD_DEqfyyOZ/images/hook-resolution.svg?fit=max&auto=format&n=-tYw1BD_DEqfyyOZ&q=85&s=c73ebc1eeda2037570427d7af1e0a891" alt="Поток разрешения hook: срабатывает событие PreToolUse, фильтр проверяет совпадение Bash, условие if проверяет совпадение Bash(rm *), запускается обработчик hook, результат возвращается в Claude Code" width="930" height="290" data-path="images/hook-resolution.svg" />
</Frame>

<Steps>
  <Step title="Событие срабатывает">
    Событие `PreToolUse` срабатывает. Claude Code отправляет входные данные инструмента как JSON на stdin hook:

    ```json theme={null}
    { "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
    ```
  </Step>

  <Step title="Фильтр проверяет">
    Фильтр `"Bash"` совпадает с именем инструмента, поэтому эта группа hook активируется. Если вы опустите фильтр или используете `"*"`, группа активируется при каждом возникновении события.
  </Step>

  <Step title="Условие if проверяет">
    Условие `if` `"Bash(rm *)"` совпадает, потому что команда начинается с `rm`, поэтому этот обработчик запускается. Если бы команда была `npm test`, проверка `if` не удалась бы и `block-rm.sh` никогда не запустился бы, избегая затрат на порождение процесса. Поле `if` опционально; без него каждый обработчик в совпадающей группе запускается.
  </Step>

  <Step title="Обработчик hook запускается">
    Скрипт проверяет полную команду и находит `rm -rf`, поэтому выводит решение на stdout:

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Destructive command blocked by hook"
      }
    }
    ```

    Если бы команда была более безопасным вариантом `rm`, таким как `rm file.txt`, скрипт выполнил бы `exit 0` вместо этого, что говорит Claude Code разрешить вызов инструмента без дополнительных действий.
  </Step>

  <Step title="Claude Code действует на основе результата">
    Claude Code читает JSON решение, блокирует вызов инструмента и показывает Claude причину.
  </Step>
</Steps>

Раздел [Configuration](#configuration) ниже документирует полную схему, и каждый раздел [hook event](#hook-events) документирует, какой входной JSON получает ваша команда и какой выход она может вернуть.

## Конфигурация

Hooks определяются в JSON файлах настроек. Конфигурация имеет три уровня вложенности:

1. Выберите [hook event](#hook-events) для ответа, например `PreToolUse` или `Stop`
2. Добавьте [matcher group](#matcher-patterns) для фильтрации срабатывания, например "только для инструмента Bash"
3. Определите один или несколько [hook handlers](#hook-handler-fields) для запуска при совпадении

См. [Как разрешается hook](#how-a-hook-resolves) выше для полного пошагового руководства с аннотированным примером.

<Note>
  На этой странице используются специальные термины для каждого уровня: **hook event** для точки жизненного цикла, **matcher group** для фильтра и **hook handler** для команды оболочки, конечной точки HTTP, подсказки или агента, который запускается. "Hook" сам по себе относится к общей функции.
</Note>

### Расположение hook

Место, где вы определяете hook, определяет его область действия:

| Расположение                                                | Область действия       | Общий доступ                          |
| :---------------------------------------------------------- | :--------------------- | :------------------------------------ |
| `~/.claude/settings.json`                                   | Все ваши проекты       | Нет, локально на вашей машине         |
| `.claude/settings.json`                                     | Один проект            | Да, можно зафиксировать в репозитории |
| `.claude/settings.local.json`                               | Один проект            | Нет, игнорируется git                 |
| Управляемые параметры политики                              | Организация            | Да, контролируется администратором    |
| [Plugin](/ru/plugins) `hooks/hooks.json`                    | Когда плагин включен   | Да, поставляется с плагином           |
| [Skill](/ru/skills) или [agent](/ru/sub-agents) frontmatter | Пока компонент активен | Да, определено в файле компонента     |

Для получения подробной информации о разрешении файлов настроек см. [settings](/ru/settings). Администраторы предприятия могут использовать `allowManagedHooksOnly` для блокировки пользовательских, проектных и плагинных hooks. См. [Hook configuration](/ru/settings#hook-configuration).

### Matcher patterns

Поле `matcher` — это строка regex, которая фильтрует срабатывание hooks. Используйте `"*"`, `""` или опустите `matcher` полностью, чтобы совпадать со всеми вхождениями. Каждый тип события совпадает с другим полем:

| Событие                                                                                                        | На что фильтр влияет                      | Примеры значений фильтра                                                                                                  |
| :------------------------------------------------------------------------------------------------------------- | :---------------------------------------- | :------------------------------------------------------------------------------------------------------------------------ |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`                     | имя инструмента                           | `Bash`, `Edit\|Write`, `mcp__.*`                                                                                          |
| `SessionStart`                                                                                                 | как сеанс начался                         | `startup`, `resume`, `clear`, `compact`                                                                                   |
| `SessionEnd`                                                                                                   | почему сеанс закончился                   | `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`                                  |
| `Notification`                                                                                                 | тип уведомления                           | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`                                                  |
| `SubagentStart`                                                                                                | тип агента                                | `Bash`, `Explore`, `Plan` или пользовательские имена агентов                                                              |
| `PreCompact`, `PostCompact`                                                                                    | что вызвало компактирование               | `manual`, `auto`                                                                                                          |
| `SubagentStop`                                                                                                 | тип агента                                | те же значения, что и `SubagentStart`                                                                                     |
| `ConfigChange`                                                                                                 | источник конфигурации                     | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills`                                        |
| `CwdChanged`                                                                                                   | поддержка фильтра отсутствует             | всегда срабатывает при каждом изменении каталога                                                                          |
| `FileChanged`                                                                                                  | имя файла (базовое имя изменённого файла) | `.envrc`, `.env`, любое имя файла, которое вы хотите отслеживать                                                          |
| `StopFailure`                                                                                                  | тип ошибки                                | `rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens`, `unknown` |
| `InstructionsLoaded`                                                                                           | причина загрузки                          | `session_start`, `nested_traversal`, `path_glob_match`, `include`, `compact`                                              |
| `Elicitation`                                                                                                  | имя MCP сервера                           | ваши настроенные имена MCP серверов                                                                                       |
| `ElicitationResult`                                                                                            | имя MCP сервера                           | те же значения, что и `Elicitation`                                                                                       |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` | поддержка фильтра отсутствует             | всегда срабатывает при каждом вхождении                                                                                   |

Фильтр — это regex, поэтому `Edit|Write` совпадает с любым инструментом и `Notebook.*` совпадает с любым инструментом, начинающимся с Notebook. Фильтр запускается против поля из [JSON входа](#hook-input-and-output), который Claude Code отправляет вашему hook на stdin. Для событий инструмента это поле — `tool_name`. Каждый раздел [hook event](#hook-events) перечисляет полный набор значений фильтра и схему входа для этого события.

Этот пример запускает скрипт линтинга только когда Claude пишет или редактирует файл:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```

`UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCreated`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` и `CwdChanged` не поддерживают фильтры и всегда срабатывают при каждом вхождении. Если вы добавите поле `matcher` к этим событиям, оно будет молча проигнорировано.

Для событий инструмента вы можете фильтровать более узко, установив поле [`if`](#common-fields) на отдельных обработчиках hook. `if` использует [синтаксис правила разрешения](/ru/permissions) для совпадения с именем инструмента и аргументами вместе, поэтому `"Bash(git *)"` запускается только для команд `git` и `"Edit(*.ts)"` запускается только для файлов TypeScript.

#### Match MCP tools

[MCP](/ru/mcp) server инструменты отображаются как обычные инструменты в событиях инструментов (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`, `PermissionDenied`), поэтому вы можете совпадать с ними так же, как с любым другим именем инструмента.

MCP инструменты следуют шаблону именования `mcp__<server>__<tool>`, например:

* `mcp__memory__create_entities`: инструмент create entities сервера Memory
* `mcp__filesystem__read_file`: инструмент read file сервера Filesystem
* `mcp__github__search_repositories`: инструмент поиска сервера GitHub

Используйте regex шаблоны для нацеливания на конкретные MCP инструменты или группы инструментов:

* `mcp__memory__.*` совпадает со всеми инструментами сервера `memory`
* `mcp__.*__write.*` совпадает с любым инструментом, содержащим "write" из любого сервера

Этот пример логирует все операции сервера memory и проверяет операции записи из любого MCP сервера:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

### Hook handler fields

Каждый объект во внутреннем массиве `hooks` — это hook handler: команда оболочки, конечная точка HTTP, подсказка LLM или агент, который запускается при совпадении фильтра. Есть четыре типа:

* **[Command hooks](#command-hook-fields)** (`type: "command"`): запускают команду оболочки. Ваш скрипт получает [JSON входные данные](#hook-input-and-output) события на stdin и передаёт результаты обратно через коды выхода и stdout.
* **[HTTP hooks](#http-hook-fields)** (`type: "http"`): отправляют JSON входные данные события как HTTP POST запрос на URL. Конечная точка передаёт результаты обратно через тело ответа, используя тот же [JSON формат выхода](#json-output), что и command hooks.
* **[Prompt hooks](#prompt-and-agent-hook-fields)** (`type: "prompt"`): отправляют подсказку модели Claude для однооборотной оценки. Модель возвращает решение да/нет как JSON. См. [Prompt-based hooks](#prompt-based-hooks).
* **[Agent hooks](#prompt-and-agent-hook-fields)** (`type: "agent"`): порождают subagent, который может использовать инструменты, такие как Read, Grep и Glob, для проверки условий перед возвратом решения. См. [Agent-based hooks](#agent-based-hooks).

#### Common fields

Эти поля применяются ко всем типам hooks:

| Поле            | Обязательно | Описание                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| :-------------- | :---------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`          | да          | `"command"`, `"http"`, `"prompt"` или `"agent"`                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `if`            | нет         | Синтаксис правила разрешения для фильтрации срабатывания этого hook, такой как `"Bash(git *)"` или `"Edit(*.ts)"`. Hook запускается только если вызов инструмента совпадает с шаблоном. Оценивается только на событиях инструмента: `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest` и `PermissionDenied`. На других событиях hook с установленным `if` никогда не запускается. Использует тот же синтаксис, что и [правила разрешения](/ru/permissions) |
| `timeout`       | нет         | Секунды перед отменой. Значения по умолчанию: 600 для command, 30 для prompt, 60 для agent                                                                                                                                                                                                                                                                                                                                                                                     |
| `statusMessage` | нет         | Пользовательское сообщение спиннера, отображаемое во время выполнения hook                                                                                                                                                                                                                                                                                                                                                                                                     |
| `once`          | нет         | Если `true`, запускается только один раз за сеанс, затем удаляется. Только skills, не agents. См. [Hooks in skills and agents](#hooks-in-skills-and-agents)                                                                                                                                                                                                                                                                                                                    |

#### Command hook fields

В дополнение к [общим полям](#common-fields), command hooks принимают эти поля:

| Поле      | Обязательно | Описание                                                                                                                                                                                                                                                           |
| :-------- | :---------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `command` | да          | Команда оболочки для выполнения                                                                                                                                                                                                                                    |
| `async`   | нет         | Если `true`, запускается в фоне без блокировки. См. [Run hooks in the background](#run-hooks-in-the-background)                                                                                                                                                    |
| `shell`   | нет         | Оболочка для использования для этого hook. Принимает `"bash"` (по умолчанию) или `"powershell"`. Установка `"powershell"` запускает команду через PowerShell на Windows. Не требует `CLAUDE_CODE_USE_POWERSHELL_TOOL`, так как hooks порождают PowerShell напрямую |

#### HTTP hook fields

В дополнение к [общим полям](#common-fields), HTTP hooks принимают эти поля:

| Поле             | Обязательно | Описание                                                                                                                                                                                                                           |
| :--------------- | :---------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`            | да          | URL для отправки POST запроса                                                                                                                                                                                                      |
| `headers`        | нет         | Дополнительные HTTP заголовки как пары ключ-значение. Значения поддерживают интерполяцию переменных окружения с использованием синтаксиса `$VAR_NAME` или `${VAR_NAME}`. Разрешены только переменные, указанные в `allowedEnvVars` |
| `allowedEnvVars` | нет         | Список имён переменных окружения, которые могут быть интерполированы в значения заголовков. Ссылки на неуказанные переменные заменяются пустыми строками. Требуется для любой интерполяции переменных окружения                    |

Claude Code отправляет [JSON входные данные](#hook-input-and-output) hook как тело POST запроса с `Content-Type: application/json`. Тело ответа использует тот же [JSON формат выхода](#json-output), что и command hooks.

Обработка ошибок отличается от command hooks: ответы не 2xx, сбои соединения и таймауты все производят неблокирующие ошибки, которые позволяют выполнению продолжаться. Чтобы заблокировать вызов инструмента или отклонить разрешение, верните ответ 2xx с JSON телом, содержащим `decision: "block"` или `hookSpecificOutput` с `permissionDecision: "deny"`.

Этот пример отправляет события `PreToolUse` на локальный сервис валидации, аутентифицируясь с токеном из переменной окружения `MY_TOKEN`:

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/pre-tool-use",
            "timeout": 30,
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

#### Prompt and agent hook fields

В дополнение к [общим полям](#common-fields), prompt и agent hooks принимают эти поля:

| Поле     | Обязательно | Описание                                                                                          |
| :------- | :---------- | :------------------------------------------------------------------------------------------------ |
| `prompt` | да          | Текст подсказки для отправки модели. Используйте `$ARGUMENTS` как заполнитель для JSON входа hook |
| `model`  | нет         | Модель для использования при оценке. По умолчанию быстрая модель                                  |

Все совпадающие hooks запускаются параллельно, и идентичные обработчики автоматически дедублируются. Command hooks дедублируются по строке команды, а HTTP hooks дедублируются по URL. Обработчики запускаются в текущем каталоге с окружением Claude Code. Переменная окружения `$CLAUDE_CODE_REMOTE` устанавливается на `"true"` в удалённых веб-окружениях и не устанавливается в локальном CLI.

### Reference scripts by path

Используйте переменные окружения для ссылки на скрипты hook относительно корня проекта или плагина, независимо от рабочего каталога при запуске hook:

* `$CLAUDE_PROJECT_DIR`: корень проекта. Оберните в кавычки для обработки путей с пробелами.
* `${CLAUDE_PLUGIN_ROOT}`: корневой каталог плагина для скриптов, поставляемых с [плагином](/ru/plugins). Изменяется при каждом обновлении плагина.
* `${CLAUDE_PLUGIN_DATA}`: [каталог постоянных данных](/ru/plugins-reference#persistent-data-directory) плагина для зависимостей и состояния, которые должны пережить обновления плагина.

<Tabs>
  <Tab title="Project scripts">
    Этот пример использует `$CLAUDE_PROJECT_DIR` для запуска проверки стиля из каталога `.claude/hooks/` проекта после любого вызова инструмента `Write` или `Edit`:

    ```json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/check-style.sh"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Plugin scripts">
    Определите plugin hooks в `hooks/hooks.json` с опциональным полем `description` верхнего уровня. Когда плагин включен, его hooks объединяются с вашими пользовательскими и проектными hooks.

    Этот пример запускает скрипт форматирования, поставляемый с плагином:

    ```json theme={null}
    {
      "description": "Automatic code formatting",
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
                "timeout": 30
              }
            ]
          }
        ]
      }
    }
    ```

    См. [plugin components reference](/ru/plugins-reference#hooks) для получения подробной информации о создании plugin hooks.
  </Tab>
</Tabs>

### Hooks in skills and agents

В дополнение к файлам настроек и плагинам, hooks могут быть определены непосредственно в [skills](/ru/skills) и [subagents](/ru/sub-agents) с использованием frontmatter. Эти hooks ограничены жизненным циклом компонента и запускаются только когда этот компонент активен.

Поддерживаются все hook события. Для subagents, `Stop` hooks автоматически преобразуются в `SubagentStop`, так как это событие, которое срабатывает при завершении subagent.

Hooks используют тот же формат конфигурации, что и hooks на основе настроек, но ограничены жизненным циклом компонента и очищаются при его завершении.

Этот skill определяет hook `PreToolUse`, который запускает скрипт проверки безопасности перед каждой командой `Bash`:

```yaml theme={null}
---
name: secure-operations
description: Perform operations with security checks
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

Agents используют тот же формат в своём YAML frontmatter.

### Меню `/hooks`

Введите `/hooks` в Claude Code, чтобы открыть браузер только для чтения ваших настроенных hooks. Меню показывает каждое hook событие с количеством настроенных hooks, позволяет вам углубиться в фильтры и показывает полные детали каждого hook обработчика. Используйте его для проверки конфигурации, проверки того, из какого файла настроек пришёл hook, или проверки команды, подсказки или URL hook.

Меню отображает все четыре типа hook: `command`, `prompt`, `agent` и `http`. Каждый hook помечен префиксом `[type]` и источником, указывающим, где он был определён:

* `User`: из `~/.claude/settings.json`
* `Project`: из `.claude/settings.json`
* `Local`: из `.claude/settings.local.json`
* `Plugin`: из `hooks/hooks.json` плагина
* `Session`: зарегистрирован в памяти для текущего сеанса
* `Built-in`: зарегистрирован внутри Claude Code

Выбор hook открывает представление деталей, показывающее его событие, фильтр, тип, исходный файл и полную команду, подсказку или URL. Меню только для чтения: чтобы добавить, изменить или удалить hooks, отредактируйте JSON настроек напрямую или попросите Claude сделать изменение.

### Disable or remove hooks

Чтобы удалить hook, удалите его запись из JSON файла настроек.

Чтобы временно отключить все hooks без их удаления, установите `"disableAllHooks": true` в файле настроек. Нет способа отключить отдельный hook, сохраняя его в конфигурации.

Параметр `disableAllHooks` соблюдает иерархию управляемых настроек. Если администратор настроил hooks через управляемые параметры политики, `disableAllHooks`, установленный в пользовательских, проектных или локальных настройках, не может отключить эти управляемые hooks. Только `disableAllHooks`, установленный на уровне управляемых настроек, может отключить управляемые hooks.

Прямые редактирования hooks в файлах настроек обычно захватываются автоматически наблюдателем файлов.

## Hook input and output

Command hooks получают JSON данные через stdin и передают результаты через коды выхода, stdout и stderr. HTTP hooks получают тот же JSON как тело POST запроса и передают результаты через тело HTTP ответа. Этот раздел охватывает поля и поведение, общие для всех событий. Каждый раздел события под [Hook events](#hook-events) включает его специфическую схему входа и параметры управления решением.

### Common input fields

Все hook события получают эти поля как JSON, в дополнение к полям, специфичным для события, документированным в каждом разделе [hook event](#hook-events). Для command hooks этот JSON поступает через stdin. Для HTTP hooks он поступает как тело POST запроса.

| Поле              | Описание                                                                                                                                                                                                                                   |
| :---------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `session_id`      | Текущий идентификатор сеанса                                                                                                                                                                                                               |
| `transcript_path` | Путь к JSON разговора                                                                                                                                                                                                                      |
| `cwd`             | Текущий рабочий каталог при вызове hook                                                                                                                                                                                                    |
| `permission_mode` | Текущий [режим разрешения](/ru/permissions#permission-modes): `"default"`, `"plan"`, `"acceptEdits"`, `"auto"`, `"dontAsk"` или `"bypassPermissions"`. Не все события получают это поле: см. пример JSON каждого события ниже для проверки |
| `hook_event_name` | Имя события, которое сработало                                                                                                                                                                                                             |

При запуске с `--agent` или внутри subagent включаются два дополнительных поля:

| Поле         | Описание                                                                                                                                                                                                                     |
| :----------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id`   | Уникальный идентификатор для subagent. Присутствует только когда hook срабатывает внутри вызова subagent. Используйте это для различения вызовов hook subagent от вызовов основного потока.                                  |
| `agent_type` | Имя агента (например, `"Explore"` или `"security-reviewer"`). Присутствует когда сеанс использует `--agent` или hook срабатывает внутри subagent. Для subagents тип subagent имеет приоритет над значением `--agent` сеанса. |

Например, hook `PreToolUse` для команды Bash получает это на stdin:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test"
  }
}
```

Поля `tool_name` и `tool_input` специфичны для события. Каждый раздел [hook event](#hook-events) документирует дополнительные поля для этого события.

### Exit code output

Код выхода из вашей команды hook говорит Claude Code, должно ли действие продолжаться, быть заблокировано или быть проигнорировано.

**Exit 0** означает успех. Claude Code анализирует stdout для [JSON полей выхода](#json-output). JSON выход обрабатывается только при exit 0. Для большинства событий stdout показывается только в подробном режиме (`Ctrl+O`). Исключения — `UserPromptSubmit` и `SessionStart`, где stdout добавляется как контекст, который Claude может видеть и действовать.

**Exit 2** означает блокирующую ошибку. Claude Code игнорирует stdout и любой JSON в нём. Вместо этого текст stderr передаётся обратно Claude как сообщение об ошибке. Эффект зависит от события: `PreToolUse` блокирует вызов инструмента, `UserPromptSubmit` отклоняет подсказку и так далее. См. [exit code 2 behavior](#exit-code-2-behavior-per-event) для полного списка.

**Любой другой код выхода** — это неблокирующая ошибка. stderr показывается в подробном режиме (`Ctrl+O`) и выполнение продолжается.

Например, скрипт команды hook, который блокирует опасные команды Bash:

```bash theme={null}
#!/bin/bash
# Читает JSON входные данные из stdin, проверяет команду
command=$(jq -r '.tool_input.command' < /dev/stdin)

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # Blocking error: tool call is prevented
fi

exit 0  # Success: tool call proceeds
```

#### Exit code 2 behavior per event

Exit code 2 — это способ hook сигнализировать "стоп, не делай этого". Эффект зависит от события, потому что некоторые события представляют действия, которые могут быть заблокированы (например, вызов инструмента, который ещё не произошёл), а другие представляют вещи, которые уже произошли или не могут быть предотвращены.

| Hook событие         | Может блокировать? | Что происходит при exit 2                                                                                                                                       |
| :------------------- | :----------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `PreToolUse`         | Да                 | Блокирует вызов инструмента                                                                                                                                     |
| `PermissionRequest`  | Да                 | Отклоняет разрешение                                                                                                                                            |
| `UserPromptSubmit`   | Да                 | Блокирует обработку подсказки и стирает подсказку                                                                                                               |
| `Stop`               | Да                 | Предотвращает остановку Claude, продолжает разговор                                                                                                             |
| `SubagentStop`       | Да                 | Предотвращает остановку subagent                                                                                                                                |
| `TeammateIdle`       | Да                 | Предотвращает переход товарища в режим ожидания (товарищ продолжает работать)                                                                                   |
| `TaskCreated`        | Да                 | Откатывает создание задачи                                                                                                                                      |
| `TaskCompleted`      | Да                 | Предотвращает отметку задачи как завершённой                                                                                                                    |
| `ConfigChange`       | Да                 | Блокирует применение изменения конфигурации (кроме `policy_settings`)                                                                                           |
| `StopFailure`        | Нет                | Выход и код выхода игнорируются                                                                                                                                 |
| `PostToolUse`        | Нет                | Показывает stderr Claude (инструмент уже запустился)                                                                                                            |
| `PostToolUseFailure` | Нет                | Показывает stderr Claude (инструмент уже не удался)                                                                                                             |
| `PermissionDenied`   | Нет                | Код выхода и stderr игнорируются (отказ уже произошёл). Используйте JSON `hookSpecificOutput.retry: true` для сообщения модели, что она может повторить попытку |
| `Notification`       | Нет                | Показывает stderr только пользователю                                                                                                                           |
| `SubagentStart`      | Нет                | Показывает stderr только пользователю                                                                                                                           |
| `SessionStart`       | Нет                | Показывает stderr только пользователю                                                                                                                           |
| `SessionEnd`         | Нет                | Показывает stderr только пользователю                                                                                                                           |
| `CwdChanged`         | Нет                | Показывает stderr только пользователю                                                                                                                           |
| `FileChanged`        | Нет                | Показывает stderr только пользователю                                                                                                                           |
| `PreCompact`         | Нет                | Показывает stderr только пользователю                                                                                                                           |
| `PostCompact`        | Нет                | Показывает stderr только пользователю                                                                                                                           |
| `Elicitation`        | Да                 | Отклоняет elicitation                                                                                                                                           |
| `ElicitationResult`  | Да                 | Блокирует ответ (действие становится decline)                                                                                                                   |
| `WorktreeCreate`     | Да                 | Любой ненулевой код выхода вызывает сбой создания worktree                                                                                                      |
| `WorktreeRemove`     | Нет                | Сбои логируются только в режиме отладки                                                                                                                         |
| `InstructionsLoaded` | Нет                | Код выхода игнорируется                                                                                                                                         |

### HTTP response handling

HTTP hooks используют коды статуса HTTP и тела ответов вместо кодов выхода и stdout:

* **2xx с пустым телом**: успех, эквивалентно exit code 0 без выхода
* **2xx с телом простого текста**: успех, текст добавляется как контекст
* **2xx с JSON телом**: успех, анализируется с использованием той же [JSON выхода](#json-output) схемы, что и command hooks
* **Статус не 2xx**: неблокирующая ошибка, выполнение продолжается
* **Сбой соединения или таймаут**: неблокирующая ошибка, выполнение продолжается

В отличие от command hooks, HTTP hooks не могут сигнализировать блокирующую ошибку только через коды статуса. Чтобы заблокировать вызов инструмента или отклонить разрешение, верните ответ 2xx с JSON телом, содержащим соответствующие поля решения.

### JSON output

Коды выхода позволяют вам разрешить или заблокировать, но JSON выход даёт вам более точное управление. Вместо выхода с кодом 2 для блокировки, выйдите с 0 и выведите JSON объект на stdout. Claude Code читает специфические поля из этого JSON для управления поведением, включая [decision control](#decision-control) для блокировки, разрешения или эскалации пользователю.

<Note>
  Вы должны выбрать один подход на hook, не оба: либо используйте коды выхода отдельно для сигнализации, либо выйдите с 0 и выведите JSON для структурированного управления. Claude Code обрабатывает JSON только при exit 0. Если вы выйдете с 2, любой JSON игнорируется.
</Note>

Stdout вашего hook должен содержать только JSON объект. Если ваш профиль оболочки выводит текст при запуске, это может помешать анализу JSON. См. [JSON validation failed](/ru/hooks-guide#json-validation-failed) в руководстве по устранению неполадок.

JSON объект поддерживает три вида полей:

* **Универсальные поля** как `continue` работают во всех событиях. Они перечислены в таблице ниже.
* **Верхнеуровневые `decision` и `reason`** используются некоторыми событиями для блокировки или предоставления обратной связи.
* **`hookSpecificOutput`** — это вложенный объект для событий, которым нужно более богатое управление. Он требует поле `hookEventName`, установленное на имя события.

| Поле             | По умолчанию | Описание                                                                                                                                    |
| :--------------- | :----------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `continue`       | `true`       | Если `false`, Claude полностью прекращает обработку после запуска hook. Имеет приоритет над любыми полями решения, специфичными для события |
| `stopReason`     | нет          | Сообщение, показываемое пользователю при `continue` равном `false`. Не показывается Claude                                                  |
| `suppressOutput` | `false`      | Если `true`, скрывает stdout из выхода подробного режима                                                                                    |
| `systemMessage`  | нет          | Предупреждающее сообщение, показываемое пользователю                                                                                        |

Чтобы полностью остановить Claude независимо от типа события:

```json theme={null}
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

#### Decision control

Не каждое событие поддерживает блокировку или управление поведением через JSON. События, которые это делают, каждое использует другой набор полей для выражения этого решения. Используйте эту таблицу как быструю ссылку перед написанием hook:

| События                                                                                                                     | Шаблон решения                   | Ключевые поля                                                                                                                                                                       |
| :-------------------------------------------------------------------------------------------------------------------------- | :------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UserPromptSubmit, PostToolUse, PostToolUseFailure, Stop, SubagentStop, ConfigChange                                         | Верхнеуровневое `decision`       | `decision: "block"`, `reason`                                                                                                                                                       |
| TeammateIdle, TaskCreated, TaskCompleted                                                                                    | Код выхода или `continue: false` | Exit code 2 блокирует действие с обратной связью stderr. JSON `{"continue": false, "stopReason": "..."}` также полностью останавливает товарища, соответствуя поведению hook `Stop` |
| PreToolUse                                                                                                                  | `hookSpecificOutput`             | `permissionDecision` (allow/deny/ask/defer), `permissionDecisionReason`                                                                                                             |
| PermissionRequest                                                                                                           | `hookSpecificOutput`             | `decision.behavior` (allow/deny)                                                                                                                                                    |
| PermissionDenied                                                                                                            | `hookSpecificOutput`             | `retry: true` говорит модели, что она может повторить попытку отклонённого вызова инструмента                                                                                       |
| WorktreeCreate                                                                                                              | path return                      | Command hook выводит путь на stdout; HTTP hook возвращает `hookSpecificOutput.worktreePath`. Сбой hook или отсутствие пути вызывает сбой создания                                   |
| Elicitation                                                                                                                 | `hookSpecificOutput`             | `action` (accept/decline/cancel), `content` (значения полей формы для accept)                                                                                                       |
| ElicitationResult                                                                                                           | `hookSpecificOutput`             | `action` (accept/decline/cancel), `content` (переопределение значений полей формы)                                                                                                  |
| WorktreeRemove, Notification, SessionEnd, PreCompact, PostCompact, InstructionsLoaded, StopFailure, CwdChanged, FileChanged | Нет                              | Нет управления решением. Используется для побочных эффектов, таких как логирование или очистка                                                                                      |

Вот примеры каждого шаблона в действии:

<Tabs>
  <Tab title="Top-level decision">
    Используется `UserPromptSubmit`, `PostToolUse`, `PostToolUseFailure`, `Stop`, `SubagentStop` и `ConfigChange`. Единственное значение — `"block"`. Чтобы разрешить действию продолжаться, опустите `decision` из вашего JSON или выйдите с 0 без какого-либо JSON вообще:

    ```json theme={null}
    {
      "decision": "block",
      "reason": "Test suite must pass before proceeding"
    }
    ```
  </Tab>

  <Tab title="PreToolUse">
    Использует `hookSpecificOutput` для более богатого управления: разрешить, отклонить, спросить или отложить. Вы также можете изменить входные данные инструмента перед его запуском или внедрить дополнительный контекст для Claude. См. [PreToolUse decision control](#pretooluse-decision-control) для полного набора параметров.

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Database writes are not allowed"
      }
    }
    ```
  </Tab>

  <Tab title="PermissionRequest">
    Использует `hookSpecificOutput` для разрешения или отклонения запроса разрешения от имени пользователя. При разрешении вы также можете изменить входные данные инструмента или применить правила разрешения, чтобы пользователю не было предложено снова. См. [PermissionRequest decision control](#permissionrequest-decision-control) для полного набора параметров.

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PermissionRequest",
        "decision": {
          "behavior": "allow",
          "updatedInput": {
            "command": "npm run lint"
          }
        }
      }
    }
    ```
  </Tab>
</Tabs>

Для расширенных примеров, включая валидацию команд Bash, фильтрацию подсказок и скрипты автоматического одобрения, см. [What you can automate](/ru/hooks-guide#what-you-can-automate) в руководстве и [Bash command validator reference implementation](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py).

## Hook events

Каждое событие соответствует точке в жизненном цикле Claude Code, где могут запускаться hooks. Разделы ниже упорядочены в соответствии с жизненным циклом: от настройки сеанса через агентный цикл к концу сеанса. Каждый раздел описывает, когда срабатывает событие, какие фильтры оно поддерживает, JSON входные данные, которые оно получает, и как управлять поведением через выход.

### SessionStart

Запускается при запуске Claude Code нового сеанса или возобновлении существующего сеанса. Полезно для загрузки контекста разработки, такого как существующие проблемы или недавние изменения в вашей кодовой базе, или установки переменных окружения. Для статического контекста, который не требует скрипта, используйте [CLAUDE.md](/ru/memory) вместо этого.

SessionStart запускается при каждом сеансе, поэтому держите эти hooks быстрыми. Поддерживаются только hooks `type: "command"`.

Значение фильтра соответствует тому, как был инициирован сеанс:

| Фильтр    | Когда он срабатывает                      |
| :-------- | :---------------------------------------- |
| `startup` | Новый сеанс                               |
| `resume`  | `--resume`, `--continue` или `/resume`    |
| `clear`   | `/clear`                                  |
| `compact` | Автоматическое или ручное компактирование |

#### SessionStart input

В дополнение к [общим полям входа](#common-input-fields), SessionStart hooks получают `source`, `model` и опционально `agent_type`. Поле `source` указывает, как был запущен сеанс: `"startup"` для новых сеансов, `"resume"` для возобновлённых сеансов, `"clear"` после `/clear` или `"compact"` после компактирования. Поле `model` содержит идентификатор модели. Если вы запустите Claude Code с `claude --agent <name>`, поле `agent_type` содержит имя агента.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-6"
}
```

#### SessionStart decision control

Любой текст, который ваш скрипт hook выводит на stdout, добавляется как контекст для Claude. В дополнение к [JSON полям выхода](#json-output), доступным для всех hooks, вы можете вернуть эти поля, специфичные для события:

| Поле                | Описание                                                                      |
| :------------------ | :---------------------------------------------------------------------------- |
| `additionalContext` | Строка, добавленная в контекст Claude. Значения нескольких hooks объединяются |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

#### Persist environment variables

SessionStart hooks имеют доступ к переменной окружения `CLAUDE_ENV_FILE`, которая предоставляет путь к файлу, где вы можете сохранять переменные окружения для последующих команд Bash.

Чтобы установить отдельные переменные окружения, напишите операторы `export` в `CLAUDE_ENV_FILE`. Используйте добавление (`>>`) для сохранения переменных, установленных другими hooks:

```bash theme={null}
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Чтобы захватить все изменения окружения из команд настройки, сравните экспортированные переменные до и после:

```bash theme={null}
#!/bin/bash

ENV_BEFORE=$(export -p | sort)

# Run your setup commands that modify the environment
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Любые переменные, написанные в этот файл, будут доступны во всех последующих командах Bash, которые Claude Code выполняет во время сеанса.

<Note>
  `CLAUDE_ENV_FILE` доступен для SessionStart, [CwdChanged](#cwdchanged) и [FileChanged](#filechanged) hooks. Другие типы hooks не имеют доступа к этой переменной.
</Note>

### InstructionsLoaded

Срабатывает при загрузке файла `CLAUDE.md` или `.claude/rules/*.md` в контекст. Это событие срабатывает при запуске сеанса для нетерпеливо загруженных файлов и снова позже при ленивой загрузке, например когда Claude получает доступ к подкаталогу, содержащему вложенный `CLAUDE.md`, или когда условные правила с frontmatter `paths:` совпадают. Hook не поддерживает блокировку или управление решением. Он запускается асинхронно в целях наблюдаемости.

Фильтр запускается против `load_reason`. Например, используйте `"matcher": "session_start"` для срабатывания только для файлов, загруженных при запуске сеанса, или `"matcher": "path_glob_match|nested_traversal"` для срабатывания только для ленивых загрузок.

#### InstructionsLoaded input

В дополнение к [общим полям входа](#common-input-fields), InstructionsLoaded hooks получают эти поля:

| Поле                | Описание                                                                                                                                                                                                               |
| :------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `file_path`         | Абсолютный путь к файлу инструкций, который был загружен                                                                                                                                                               |
| `memory_type`       | Область действия файла: `"User"`, `"Project"`, `"Local"` или `"Managed"`                                                                                                                                               |
| `load_reason`       | Почему файл был загружен: `"session_start"`, `"nested_traversal"`, `"path_glob_match"`, `"include"` или `"compact"`. Значение `"compact"` срабатывает при перезагрузке файлов инструкций после события компактирования |
| `globs`             | Шаблоны glob пути из frontmatter `paths:` файла, если есть. Присутствует только для загрузок `path_glob_match`                                                                                                         |
| `trigger_file_path` | Путь к файлу, доступ к которому вызвал эту загрузку, для ленивых загрузок                                                                                                                                              |
| `parent_file_path`  | Путь к родительскому файлу инструкций, который включил этот, для загрузок `include`                                                                                                                                    |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "InstructionsLoaded",
  "file_path": "/Users/my-project/CLAUDE.md",
  "memory_type": "Project",
  "load_reason": "session_start"
}
```

#### InstructionsLoaded decision control

InstructionsLoaded hooks не имеют управления решением. Они не могут блокировать или изменять загрузку инструкций. Используйте это событие для аудита логирования, отслеживания соответствия или наблюдаемости.

### UserPromptSubmit

Запускается при отправке пользователем подсказки, перед обработкой Claude. Это позволяет вам добавить дополнительный контекст на основе подсказки/разговора, проверить подсказки или заблокировать определённые типы подсказок.

#### UserPromptSubmit input

В дополнение к [общим полям входа](#common-input-fields), UserPromptSubmit hooks получают поле `prompt`, содержащее текст, отправленный пользователем.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

#### UserPromptSubmit decision control

Hooks `UserPromptSubmit` могут управлять тем, обрабатывается ли подсказка пользователя, и добавлять контекст. Доступны все [JSON полей выхода](#json-output).

Есть два способа добавить контекст в разговор при exit code 0:

* **Простой текст stdout**: любой текст, не являющийся JSON, написанный на stdout, добавляется как контекст
* **JSON с `additionalContext`**: используйте формат JSON ниже для большего управления. Поле `additionalContext` добавляется как контекст

Простой stdout показывается как выход hook в транскрипте. Поле `additionalContext` добавляется более дискретно.

Чтобы заблокировать подсказку, верните JSON объект с `decision`, установленным на `"block"`:

| Поле                | Описание                                                                                                                |
| :------------------ | :---------------------------------------------------------------------------------------------------------------------- |
| `decision`          | `"block"` предотвращает обработку подсказки и стирает её из контекста. Опустите, чтобы разрешить подсказке продолжаться |
| `reason`            | Показывается пользователю при `decision` равном `"block"`. Не добавляется в контекст                                    |
| `additionalContext` | Строка, добавленная в контекст Claude                                                                                   |

```json theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here"
  }
}
```

<Note>
  Формат JSON не требуется для простых случаев использования. Чтобы добавить контекст, вы можете вывести простой текст на stdout с exit code 0. Используйте JSON, когда вам нужно блокировать подсказки или вам нужно более структурированное управление.
</Note>

### PreToolUse

Запускается после того, как Claude создаёт параметры инструмента и перед обработкой вызова инструмента. Совпадает с именем инструмента: `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `WebFetch`, `WebSearch`, `AskUserQuestion`, `ExitPlanMode` и любые [имена MCP инструментов](#match-mcp-tools).

Используйте [PreToolUse decision control](#pretooluse-decision-control) для разрешения, отклонения, запроса или отложения вызова инструмента.

#### PreToolUse input

В дополнение к [общим полям входа](#common-input-fields), PreToolUse hooks получают `tool_name`, `tool_input` и `tool_use_id`. Поля `tool_input` зависят от инструмента:

##### Bash

Выполняет команды оболочки.

| Поле                | Тип     | Пример             | Описание                                       |
| :------------------ | :------ | :----------------- | :--------------------------------------------- |
| `command`           | string  | `"npm test"`       | Команда оболочки для выполнения                |
| `description`       | string  | `"Run test suite"` | Опциональное описание того, что делает команда |
| `timeout`           | number  | `120000`           | Опциональный таймаут в миллисекундах           |
| `run_in_background` | boolean | `false`            | Запускать ли команду в фоне                    |

##### Write

Создаёт или перезаписывает файл.

| Поле        | Тип    | Пример                | Описание                           |
| :---------- | :----- | :-------------------- | :--------------------------------- |
| `file_path` | string | `"/path/to/file.txt"` | Абсолютный путь к файлу для записи |
| `content`   | string | `"file content"`      | Содержимое для записи в файл       |

##### Edit

Заменяет строку в существующем файле.

| Поле          | Тип     | Пример                | Описание                                   |
| :------------ | :------ | :-------------------- | :----------------------------------------- |
| `file_path`   | string  | `"/path/to/file.txt"` | Абсолютный путь к файлу для редактирования |
| `old_string`  | string  | `"original text"`     | Текст для поиска и замены                  |
| `new_string`  | string  | `"replacement text"`  | Текст замены                               |
| `replace_all` | boolean | `false`               | Заменять ли все вхождения                  |

##### Read

Читает содержимое файла.

| Поле        | Тип    | Пример                | Описание                                    |
| :---------- | :----- | :-------------------- | :------------------------------------------ |
| `file_path` | string | `"/path/to/file.txt"` | Абсолютный путь к файлу для чтения          |
| `offset`    | number | `10`                  | Опциональный номер строки для начала чтения |
| `limit`     | number | `50`                  | Опциональное количество строк для чтения    |

##### Glob

Находит файлы, соответствующие шаблону glob.

| Поле      | Тип    | Пример           | Описание                                                              |
| :-------- | :----- | :--------------- | :-------------------------------------------------------------------- |
| `pattern` | string | `"**/*.ts"`      | Шаблон glob для совпадения файлов                                     |
| `path`    | string | `"/path/to/dir"` | Опциональный каталог для поиска. По умолчанию текущий рабочий каталог |

##### Grep

Ищет содержимое файла с регулярными выражениями.

| Поле          | Тип     | Пример           | Описание                                                                               |
| :------------ | :------ | :--------------- | :------------------------------------------------------------------------------------- |
| `pattern`     | string  | `"TODO.*fix"`    | Шаблон регулярного выражения для поиска                                                |
| `path`        | string  | `"/path/to/dir"` | Опциональный файл или каталог для поиска                                               |
| `glob`        | string  | `"*.ts"`         | Опциональный шаблон glob для фильтрации файлов                                         |
| `output_mode` | string  | `"content"`      | `"content"`, `"files_with_matches"` или `"count"`. По умолчанию `"files_with_matches"` |
| `-i`          | boolean | `true`           | Поиск без учёта регистра                                                               |
| `multiline`   | boolean | `false`          | Включить многострочное совпадение                                                      |

##### WebFetch

Получает и обрабатывает веб-содержимое.

| Поле     | Тип    | Пример                        | Описание                                       |
| :------- | :----- | :---------------------------- | :--------------------------------------------- |
| `url`    | string | `"https://example.com/api"`   | URL для получения содержимого                  |
| `prompt` | string | `"Extract the API endpoints"` | Подсказка для запуска на полученном содержимом |

##### WebSearch

Ищет в веб.

| Поле              | Тип    | Пример                         | Описание                                                |
| :---------------- | :----- | :----------------------------- | :------------------------------------------------------ |
| `query`           | string | `"react hooks best practices"` | Поисковый запрос                                        |
| `allowed_domains` | array  | `["docs.example.com"]`         | Опциональный: включать результаты только с этих доменов |
| `blocked_domains` | array  | `["spam.example.com"]`         | Опциональный: исключить результаты с этих доменов       |

##### Agent

Порождает [subagent](/ru/sub-agents).

| Поле            | Тип    | Пример                     | Описание                                                       |
| :-------------- | :----- | :------------------------- | :------------------------------------------------------------- |
| `prompt`        | string | `"Find all API endpoints"` | Задача для выполнения агентом                                  |
| `description`   | string | `"Find API endpoints"`     | Краткое описание задачи                                        |
| `subagent_type` | string | `"Explore"`                | Тип специализированного агента для использования               |
| `model`         | string | `"sonnet"`                 | Опциональный псевдоним модели для переопределения по умолчанию |

##### AskUserQuestion

Задаёт пользователю один-четыре вопроса с множественным выбором.

| Поле        | Тип    | Пример                                                                                                             | Описание                                                                                                                                                                                                                      |
| :---------- | :----- | :----------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `questions` | array  | `[{"question": "Which framework?", "header": "Framework", "options": [{"label": "React"}], "multiSelect": false}]` | Вопросы для представления, каждый с текстом `question`, коротким `header`, массивом `options` и опциональным флагом `multiSelect`                                                                                             |
| `answers`   | object | `{"Which framework?": "React"}`                                                                                    | Опциональный. Соответствует текст вопроса выбранному ярлыку опции. Ответы с множественным выбором объединяют ярлыки запятыми. Claude не устанавливает это поле; предоставьте его через `updatedInput` для программного ответа |

#### PreToolUse decision control

Hooks `PreToolUse` могут управлять тем, продолжается ли вызов инструмента. В отличие от других hooks, которые используют верхнеуровневое поле `decision`, PreToolUse возвращает своё решение внутри объекта `hookSpecificOutput`. Это даёт ему более богатое управление: четыре результата (разрешить, отклонить, спросить или отложить) плюс возможность изменить входные данные инструмента перед выполнением.

| Поле                       | Описание                                                                                                                                                                                                                                                                                                                      |
| :------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `permissionDecision`       | `"allow"` обходит систему разрешений. `"deny"` предотвращает вызов инструмента. `"ask"` предлагает пользователю подтвердить. `"defer"` выходит корректно, чтобы инструмент мог быть возобновлён позже. [Правила отклонения и запроса](/ru/permissions#manage-permissions) всё ещё применяются когда hook возвращает `"allow"` |
| `permissionDecisionReason` | Для `"allow"` и `"ask"`, показывается пользователю, но не Claude. Для `"deny"`, показывается Claude. Для `"defer"`, игнорируется                                                                                                                                                                                              |
| `updatedInput`             | Изменяет параметры входа инструмента перед выполнением. Заменяет весь объект входа, поэтому включите неизменённые поля наряду с изменёнными. Объедините с `"allow"` для автоматического одобрения или `"ask"` для показа изменённого входа пользователю. Для `"defer"`, игнорируется                                          |
| `additionalContext`        | Строка, добавленная в контекст Claude перед выполнением инструмента. Для `"defer"`, игнорируется                                                                                                                                                                                                                              |

Когда несколько PreToolUse hooks возвращают разные решения, приоритет — `deny` > `defer` > `ask` > `allow`.

Когда hook возвращает `"ask"`, диалог разрешения, отображаемый пользователю, включает метку, идентифицирующую источник hook: например, `[User]`, `[Project]`, `[Plugin]` или `[Local]`. Это помогает пользователям понять, какой источник конфигурации запрашивает подтверждение.

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

`AskUserQuestion` и `ExitPlanMode` требуют взаимодействия пользователя и обычно блокируют в [неинтерактивном режиме](/ru/headless) с флагом `-p`. Возврат `permissionDecision: "allow"` вместе с `updatedInput` удовлетворяет этому требованию: hook читает входные данные инструмента из stdin, собирает ответ через ваш собственный UI и возвращает его в `updatedInput`, чтобы инструмент запустился без запроса. Возврат только `"allow"` недостаточен для этих инструментов. Для `AskUserQuestion` повторите исходный массив `questions` и добавьте объект [`answers`](#askuserquestion), соответствующий тексту каждого вопроса выбранному ответу.

<Note>
  PreToolUse ранее использовал верхнеуровневые поля `decision` и `reason`, но они устарели для этого события. Используйте `hookSpecificOutput.permissionDecision` и `hookSpecificOutput.permissionDecisionReason` вместо этого. Устаревшие значения `"approve"` и `"block"` соответствуют `"allow"` и `"deny"` соответственно. Другие события, такие как PostToolUse и Stop, продолжают использовать верхнеуровневые `decision` и `reason` как их текущий формат.
</Note>

#### Defer a tool call for later

`"defer"` предназначен для интеграций, которые запускают `claude -p` как подпроцесс и читают его JSON выход, таких как приложение Agent SDK или пользовательский UI, построенный на основе Claude Code. Это позволяет этому вызывающему процессу приостановить Claude при вызове инструмента, собрать входные данные через его собственный интерфейс и возобновить с того же места. Claude Code соблюдает это значение только в [неинтерактивном режиме](/ru/headless) с флагом `-p`. В интерактивных сеансах он логирует предупреждение и игнорирует результат hook.

<Note>
  Значение `defer` требует Claude Code v2.1.89 или позже. Более ранние версии не распознают его и инструмент проходит через обычный поток разрешений.
</Note>

Инструмент `AskUserQuestion` — это типичный случай: Claude хочет что-то спросить у пользователя, но нет терминала для ответа. Круговой путь работает так:

1. Claude вызывает `AskUserQuestion`. Срабатывает hook `PreToolUse`.
2. Hook возвращает `permissionDecision: "defer"`. Инструмент не выполняется. Процесс выходит с `stop_reason: "tool_deferred"` и отложенный вызов инструмента сохраняется в транскрипте.
3. Вызывающий процесс читает `deferred_tool_use` из результата SDK, выводит вопрос в своём UI и ждёт ответа.
4. Вызывающий процесс запускает `claude -p --resume <session-id>`. Тот же вызов инструмента срабатывает `PreToolUse` снова.
5. Hook возвращает `permissionDecision: "allow"` с ответом в `updatedInput`. Инструмент выполняется и Claude продолжает.

Поле `deferred_tool_use` содержит `id`, `name` и `input` инструмента. `input` — это параметры, которые Claude сгенерировал для вызова инструмента, захваченные перед выполнением:

```json theme={null}
{
  "type": "result",
  "subtype": "success",
  "stop_reason": "tool_deferred",
  "session_id": "abc123",
  "deferred_tool_use": {
    "id": "toolu_01abc",
    "name": "AskUserQuestion",
    "input": { "questions": [{ "question": "Which framework?", "header": "Framework", "options": [{"label": "React"}, {"label": "Vue"}], "multiSelect": false }] }
  }
}
```

Нет таймаута или лимита повторных попыток. Сеанс остаётся на диске до возобновления. Если ответ не готов при возобновлении, hook может вернуть `"defer"` снова и процесс выходит так же. Вызывающий процесс управляет тем, когда разорвать цикл, в конечном итоге возвращая `"allow"` или `"deny"` из hook.

`"defer"` работает только когда Claude делает один вызов инструмента в ходе. Если Claude делает несколько вызовов инструментов одновременно, `"defer"` игнорируется с предупреждением и инструмент проходит через обычный поток разрешений. Ограничение существует потому что возобновление может только повторно запустить один инструмент: нет способа отложить один вызов из пакета без оставления других неразрешённых.

Если отложенный инструмент больше не доступен при возобновлении, процесс выходит с `stop_reason: "tool_deferred_unavailable"` и `is_error: true` перед срабатыванием hook. Это происходит когда MCP сервер, который предоставил инструмент, не подключен для возобновлённого сеанса. Полезная нагрузка `deferred_tool_use` всё ещё включена, чтобы вы могли идентифицировать, какой инструмент исчез.

<Warning>
  `--resume` не восстанавливает режим разрешения из предыдущего сеанса. Передайте тот же флаг `--permission-mode` при возобновлении, который был активен при отложении инструмента. Claude Code логирует предупреждение, если режимы отличаются.
</Warning>

### PermissionRequest

Запускается при показе пользователю диалога разрешения.
Используйте [PermissionRequest decision control](#permissionrequest-decision-control) для разрешения или отклонения от имени пользователя.

Совпадает с именем инструмента, те же значения, что и PreToolUse.

#### PermissionRequest input

PermissionRequest hooks получают поля `tool_name` и `tool_input` как PreToolUse hooks, но без `tool_use_id`. Опциональный массив `permission_suggestions` содержит параметры "всегда разрешить", которые пользователь обычно видит в диалоге разрешения. Разница в том, когда срабатывает hook: PermissionRequest hooks запускаются при показе диалога разрешения пользователю, в то время как PreToolUse hooks запускаются перед выполнением инструмента независимо от статуса разрешения.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules",
    "description": "Remove node_modules directory"
  },
  "permission_suggestions": [
    {
      "type": "addRules",
      "rules": [{ "toolName": "Bash", "ruleContent": "rm -rf node_modules" }],
      "behavior": "allow",
      "destination": "localSettings"
    }
  ]
}
```

#### PermissionRequest decision control

Hooks `PermissionRequest` могут разрешить или отклонить запросы разрешения. В дополнение к [JSON полям выхода](#json-output), доступным для всех hooks, ваш скрипт hook может вернуть объект `decision` с этими полями, специфичными для события:

| Поле                 | Описание                                                                                                                                                                                |
| :------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `behavior`           | `"allow"` предоставляет разрешение, `"deny"` отклоняет его                                                                                                                              |
| `updatedInput`       | Только для `"allow"`: изменяет параметры входа инструмента перед выполнением. Заменяет весь объект входа, поэтому включите неизменённые поля наряду с изменёнными                       |
| `updatedPermissions` | Только для `"allow"`: массив [записей обновления разрешения](#permission-update-entries) для применения, таких как добавление правила разрешения или изменение режима разрешения сеанса |
| `message`            | Только для `"deny"`: говорит Claude, почему разрешение было отклонено                                                                                                                   |
| `interrupt`          | Только для `"deny"`: если `true`, останавливает Claude                                                                                                                                  |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

#### Permission update entries

Поле выхода `updatedPermissions` и поле входа [`permission_suggestions`](#permissionrequest-input) оба используют один и тот же массив объектов записей. Каждая запись имеет `type`, который определяет её другие поля, и `destination`, который управляет тем, где применяется изменение.

| `type`              | Поля                               | Эффект                                                                                                                                                                                               |
| :------------------ | :--------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `addRules`          | `rules`, `behavior`, `destination` | Добавляет правила разрешения. `rules` — это массив объектов `{toolName, ruleContent?}`. Опустите `ruleContent` для совпадения со всем инструментом. `behavior` — это `"allow"`, `"deny"` или `"ask"` |
| `replaceRules`      | `rules`, `behavior`, `destination` | Заменяет все правила данного `behavior` в `destination` предоставленными `rules`                                                                                                                     |
| `removeRules`       | `rules`, `behavior`, `destination` | Удаляет совпадающие правила данного `behavior`                                                                                                                                                       |
| `setMode`           | `mode`, `destination`              | Изменяет режим разрешения. Допустимые режимы — `default`, `acceptEdits`, `dontAsk`, `bypassPermissions` и `plan`                                                                                     |
| `addDirectories`    | `directories`, `destination`       | Добавляет рабочие каталоги. `directories` — это массив строк пути                                                                                                                                    |
| `removeDirectories` | `directories`, `destination`       | Удаляет рабочие каталоги                                                                                                                                                                             |

Поле `destination` на каждой записи определяет, остаётся ли изменение в памяти или сохраняется в файл настроек.

| `destination`     | Записывает в                                         |
| :---------------- | :--------------------------------------------------- |
| `session`         | только в памяти, отбрасывается при завершении сеанса |
| `localSettings`   | `.claude/settings.local.json`                        |
| `projectSettings` | `.claude/settings.json`                              |
| `userSettings`    | `~/.claude/settings.json`                            |

Hook может вывести одно из `permission_suggestions`, которые он получил, как свой собственный выход `updatedPermissions`, что эквивалентно выбору пользователем этого параметра "всегда разрешить" в диалоге.

### PostToolUse

Запускается сразу после успешного завершения инструмента.

Совпадает с именем инструмента, те же значения, что и PreToolUse.

#### PostToolUse input

Hooks `PostToolUse` срабатывают после того, как инструмент уже выполнился успешно. Входные данные включают как `tool_input`, аргументы, отправленные инструменту, так и `tool_response`, результат, который он вернул. Точная схема для обоих зависит от инструмента.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "success": true
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

#### PostToolUse decision control

Hooks `PostToolUse` могут предоставить обратную связь Claude после выполнения инструмента. В дополнение к [JSON полям выхода](#json-output), доступным для всех hooks, ваш скрипт hook может вернуть эти поля, специфичные для события:

| Поле                   | Описание                                                                                              |
| :--------------------- | :---------------------------------------------------------------------------------------------------- |
| `decision`             | `"block"` предлагает Claude с `reason`. Опустите, чтобы разрешить действию продолжаться               |
| `reason`               | Объяснение, показываемое Claude при `decision` равном `"block"`                                       |
| `additionalContext`    | Дополнительный контекст для Claude для рассмотрения                                                   |
| `updatedMCPToolOutput` | Только для [MCP инструментов](#match-mcp-tools): заменяет выход инструмента предоставленным значением |

```json theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude"
  }
}
```

### PostToolUseFailure

Запускается при сбое выполнения инструмента. Это событие срабатывает для вызовов инструментов, которые выбрасывают ошибки или возвращают результаты сбоя. Используйте это для логирования сбоев, отправки оповещений или предоставления исправляющей обратной связи Claude.

Совпадает с именем инструмента, те же значения, что и PreToolUse.

#### PostToolUseFailure input

PostToolUseFailure hooks получают те же поля `tool_name` и `tool_input`, что и PostToolUse, вместе с информацией об ошибке как верхнеуровневые поля:

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite"
  },
  "tool_use_id": "toolu_01ABC123...",
  "error": "Command exited with non-zero status code 1",
  "is_interrupt": false
}
```

| Поле           | Описание                                                                                   |
| :------------- | :----------------------------------------------------------------------------------------- |
| `error`        | Строка, описывающая, что пошло не так                                                      |
| `is_interrupt` | Опциональное логическое значение, указывающее, был ли сбой вызван прерыванием пользователя |

#### PostToolUseFailure decision control

Hooks `PostToolUseFailure` могут предоставить контекст Claude после сбоя инструмента. В дополнение к [JSON полям выхода](#json-output), доступным для всех hooks, ваш скрипт hook может вернуть эти поля, специфичные для события:

| Поле                | Описание                                                             |
| :------------------ | :------------------------------------------------------------------- |
| `additionalContext` | Дополнительный контекст для Claude для рассмотрения наряду с ошибкой |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### PermissionDenied

Запускается когда классификатор [auto mode](/ru/permission-modes#eliminate-prompts-with-auto-mode) отклоняет вызов инструмента. Этот hook срабатывает только в auto mode: он не запускается когда вы вручную отклоняете диалог разрешения, когда hook `PreToolUse` блокирует вызов или когда совпадает правило `deny`. Используйте это для логирования отказов классификатора, корректировки конфигурации или сообщения модели, что она может повторить попытку вызова инструмента.

Совпадает с именем инструмента, те же значения, что и PreToolUse.

#### PermissionDenied input

В дополнение к [общим полям входа](#common-input-fields), PermissionDenied hooks получают `tool_name`, `tool_input`, `tool_use_id` и `reason`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "auto",
  "hook_event_name": "PermissionDenied",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/build",
    "description": "Clean build directory"
  },
  "tool_use_id": "toolu_01ABC123...",
  "reason": "Auto mode denied: command targets a path outside the project"
}
```

| Поле     | Описание                                                              |
| :------- | :-------------------------------------------------------------------- |
| `reason` | Объяснение классификатора того, почему вызов инструмента был отклонён |

#### PermissionDenied decision control

PermissionDenied hooks могут сообщить модели, что она может повторить попытку отклонённого вызова инструмента. Верните JSON объект с `hookSpecificOutput.retry`, установленным на `true`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

Когда `retry` равно `true`, Claude Code добавляет сообщение в разговор, говорящее модели, что она может повторить попытку вызова инструмента. Отказ сам по себе не отменяется. Если ваш hook не возвращает JSON или возвращает `retry: false`, отказ остаётся и модель получает исходное сообщение об отклонении.

### Notification

Запускается при отправке Claude Code уведомлений. Совпадает с типом уведомления: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`. Опустите фильтр для запуска hooks для всех типов уведомлений.

Используйте отдельные фильтры для запуска разных обработчиков в зависимости от типа уведомления. Эта конфигурация запускает скрипт оповещения, специфичный для разрешения, когда Claude нуждается в одобрении разрешения, и другое уведомление, когда Claude был неактивен:

```json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/permission-alert.sh"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/idle-notification.sh"
          }
        ]
      }
    ]
  }
}
```

#### Notification input

В дополнение к [общим полям входа](#common-input-fields), Notification hooks получают `message` с текстом уведомления, опциональный `title` и `notification_type`, указывающий, какой тип сработал.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

Notification hooks не могут блокировать или изменять уведомления. В дополнение к [JSON полям выхода](#json-output), доступным для всех hooks, вы можете вернуть `additionalContext` для добавления контекста в разговор:

| Поле                | Описание                              |
| :------------------ | :------------------------------------ |
| `additionalContext` | Строка, добавленная в контекст Claude |

### SubagentStart

Запускается при порождении Claude Code subagent через инструмент Agent. Поддерживает фильтры для фильтрации по имени типа агента (встроенные агенты, такие как `Bash`, `Explore`, `Plan`, или пользовательские имена агентов из `.claude/agents/`).

#### SubagentStart input

В дополнение к [общим полям входа](#common-input-fields), SubagentStart hooks получают `agent_id` с уникальным идентификатором для subagent и `agent_type` с именем агента (встроенные агенты, такие как `"Bash"`, `"Explore"`, `"Plan"` или пользовательские имена агентов).

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

SubagentStart hooks не могут блокировать создание subagent, но они могут внедрить контекст в subagent. В дополнение к [JSON полям выхода](#json-output), доступным для всех hooks, вы можете вернуть:

| Поле                | Описание                                |
| :------------------ | :-------------------------------------- |
| `additionalContext` | Строка, добавленная в контекст subagent |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

### SubagentStop

Запускается при завершении ответа Claude Code subagent. Совпадает с типом агента, те же значения, что и SubagentStart.

#### SubagentStop input

В дополнение к [общим полям входа](#common-input-fields), SubagentStop hooks получают `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path` и `last_assistant_message`. Поле `agent_type` — это значение, используемое для фильтрации фильтра. `transcript_path` — это транскрипт основного сеанса, в то время как `agent_transcript_path` — это собственный транскрипт subagent, хранящийся в вложенной папке `subagents/`. Поле `last_assistant_message` содержит текстовое содержимое финального ответа subagent, поэтому hooks могут получить к нему доступ без анализа файла транскрипта.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../abc123.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/projects/.../abc123/subagents/agent-def456.jsonl",
  "last_assistant_message": "Analysis complete. Found 3 potential issues..."
}
```

SubagentStop hooks используют тот же формат управления решением, что и [Stop hooks](#stop-decision-control).

### TaskCreated

Запускается при создании задачи через инструмент `TaskCreate`. Используйте это для обеспечения соглашений об именовании, требования описаний задач или предотвращения создания определённых задач.

Когда hook `TaskCreated` выходит с кодом 2, задача не создаётся и сообщение stderr передаётся обратно модели как обратная связь. Чтобы полностью остановить товарища вместо его повторного запуска, верните JSON с `{"continue": false, "stopReason": "..."}`. TaskCreated hooks не поддерживают фильтры и срабатывают при каждом вхождении.

#### TaskCreated input

В дополнение к [общим полям входа](#common-input-fields), TaskCreated hooks получают `task_id`, `task_subject` и опционально `task_description`, `teammate_name` и `team_name`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCreated",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

| Поле               | Описание                                             |
| :----------------- | :--------------------------------------------------- |
| `task_id`          | Идентификатор создаваемой задачи                     |
| `task_subject`     | Название задачи                                      |
| `task_description` | Подробное описание задачи. Может отсутствовать       |
| `teammate_name`    | Имя товарища, создающего задачу. Может отсутствовать |
| `team_name`        | Имя команды. Может отсутствовать                     |

#### TaskCreated decision control

TaskCreated hooks поддерживают два способа управления созданием задачи:

* **Exit code 2**: задача не создаётся и сообщение stderr передаётся обратно модели как обратная связь.
* **JSON `{"continue": false, "stopReason": "..."}`**: полностью останавливает товарища, соответствуя поведению hook `Stop`. `stopReason` показывается пользователю.

Этот пример блокирует задачи, чьи названия не следуют требуемому формату:

```bash theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

if [[ ! "$TASK_SUBJECT" =~ ^\[TICKET-[0-9]+\] ]]; then
  echo "Task subject must start with a ticket number, e.g. '[TICKET-123] Add feature'" >&2
  exit 2
fi

exit 0
```

### TaskCompleted

Запускается при отметке задачи как завершённой. Это срабатывает в двух ситуациях: когда любой агент явно отмечает задачу как завершённую через инструмент TaskUpdate, или когда товарищ [agent team](/ru/agent-teams) завершает свой ход с незавершёнными задачами. Используйте это для обеспечения критериев завершения, таких как прохождение тестов или проверок линтинга перед закрытием задачи.

Когда hook `TaskCompleted` выходит с кодом 2, задача не отмечается как завершённая и сообщение stderr передаётся обратно модели как обратная связь. Чтобы полностью остановить товарища вместо его повторного запуска, верните JSON с `{"continue": false, "stopReason": "..."}`. TaskCompleted hooks не поддерживают фильтры и срабатывают при каждом вхождении.

#### TaskCompleted input

В дополнение к [общим полям входа](#common-input-fields), TaskCompleted hooks получают `task_id`, `task_subject` и опционально `task_description`, `teammate_name` и `team_name`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCompleted",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "my-project"
}
```

| Поле               | Описание                                               |
| :----------------- | :----------------------------------------------------- |
| `task_id`          | Идентификатор завершаемой задачи                       |
| `task_subject`     | Название задачи                                        |
| `task_description` | Подробное описание задачи. Может отсутствовать         |
| `teammate_name`    | Имя товарища, завершающего задачу. Может отсутствовать |
| `team_name`        | Имя команды. Может отсутствовать                       |

#### TaskCompleted decision control

TaskCompleted hooks поддерживают два способа управления завершением задачи:

* **Exit code 2**: задача не отмечается как завершённая и сообщение stderr передаётся обратно модели как обратная связь.
* **JSON `{"continue": false, "stopReason": "..."}`**: полностью останавливает товарища, соответствуя поведению hook `Stop`. `stopReason` показывается пользователю.

Этот пример запускает тесты и блокирует завершение задачи, если они не пройдены:

```bash theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

# Run the test suite
if ! npm test 2>&1; then
  echo "Tests not passing. Fix failing tests before completing: $TASK_SUBJECT" >&2
  exit 2
fi

exit 0
```

### Stop

Запускается при завершении ответа основного агента Claude Code. Не запускается, если остановка произошла из-за прерывания пользователя. Ошибки API срабатывают [StopFailure](#stopfailure) вместо этого.

#### Stop input

В дополнение к [общим полям входа](#common-input-fields), Stop hooks получают `stop_hook_active` и `last_assistant_message`. Поле `stop_hook_active` равно `true`, когда Claude Code уже продолжает в результате stop hook. Проверьте это значение или обработайте транскрипт, чтобы предотвратить бесконечное выполнение Claude Code. Поле `last_assistant_message` содержит текстовое содержимое финального ответа Claude, поэтому hooks могут получить к нему доступ без анализа файла транскрипта.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true,
  "last_assistant_message": "I've completed the refactoring. Here's a summary..."
}
```

#### Stop decision control

Hooks `Stop` и `SubagentStop` могут управлять тем, продолжает ли Claude. В дополнение к [JSON полям выхода](#json-output), доступным для всех hooks, ваш скрипт hook может вернуть эти поля, специфичные для события:

| Поле       | Описание                                                                                |
| :--------- | :-------------------------------------------------------------------------------------- |
| `decision` | `"block"` предотвращает остановку Claude. Опустите, чтобы разрешить Claude остановиться |
| `reason`   | Требуется при `decision` равном `"block"`. Говорит Claude, почему оно должно продолжить |

```json theme={null}
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

### StopFailure

Запускается вместо [Stop](#stop) когда ход заканчивается из-за ошибки API. Выход и код выхода игнорируются. Используйте это для логирования сбоев, отправки оповещений или принятия действий восстановления, когда Claude не может завершить ответ из-за ограничений скорости, проблем аутентификации или других ошибок API.

#### StopFailure input

В дополнение к [общим полям входа](#common-input-fields), StopFailure hooks получают `error`, опциональные `error_details` и `last_assistant_message`. Поле `error` определяет тип ошибки и используется для фильтрации фильтра.

| Поле                     | Описание                                                                                                                                                                                                                                |
| :----------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `error`                  | Тип ошибки: `rate_limit`, `authentication_failed`, `billing_error`, `invalid_request`, `server_error`, `max_output_tokens` или `unknown`                                                                                                |
| `error_details`          | Дополнительные детали об ошибке, когда доступны                                                                                                                                                                                         |
| `last_assistant_message` | Отрендеренный текст ошибки, показанный в разговоре. В отличие от `Stop` и `SubagentStop`, где это поле содержит разговорный выход Claude, для `StopFailure` оно содержит строку ошибки API, такую как `"API Error: Rate limit reached"` |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "StopFailure",
  "error": "rate_limit",
  "error_details": "429 Too Many Requests",
  "last_assistant_message": "API Error: Rate limit reached"
}
```

StopFailure hooks не имеют управления решением. Они запускаются только в целях уведомления и логирования.

### TeammateIdle

Запускается когда товарищ [agent team](/ru/agent-teams) собирается перейти в режим ожидания после завершения своего хода. Используйте это для обеспечения качественных ворот перед остановкой работы товарища, такие как требование прохождения проверок линтинга или проверка существования выходных файлов.

Когда hook `TeammateIdle` выходит с кодом 2, товарищ получает сообщение stderr как обратную связь и продолжает работать вместо перехода в режим ожидания. Чтобы полностью остановить товарища вместо его повторного запуска, верните JSON с `{"continue": false, "stopReason": "..."}`. TeammateIdle hooks не поддерживают фильтры и срабатывают при каждом вхождении.

#### TeammateIdle input

В дополнение к [общим полям входа](#common-input-fields), TeammateIdle hooks получают `teammate_name` и `team_name`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "my-project"
}
```

| Поле            | Описание                                                  |
| :-------------- | :-------------------------------------------------------- |
| `teammate_name` | Имя товарища, который собирается перейти в режим ожидания |
| `team_name`     | Имя команды                                               |

#### TeammateIdle decision control

TeammateIdle hooks поддерживают два способа управления поведением товарища:

* **Exit code 2**: товарищ получает сообщение stderr как обратную связь и продолжает работать вместо перехода в режим ожидания.
* **JSON `{"continue": false, "stopReason": "..."}`**: полностью останавливает товарища, соответствуя поведению hook `Stop`. `stopReason` показывается пользователю.

Этот пример проверяет, что артефакт сборки существует перед разрешением товарищу перейти в режим ожидания:

```bash theme={null}
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2
fi

exit 0
```

### ConfigChange

Запускается при изменении файла конфигурации во время сеанса. Используйте это для аудита изменений настроек, обеспечения политик безопасности или блокировки несанкционированных изменений файлов конфигурации.

ConfigChange hooks срабатывают для изменений файлов настроек, управляемых параметров политики и файлов skills. Поле `source` во входных данных говорит вам, какой тип конфигурации изменился, и опциональное поле `file_path` предоставляет путь к изменённому файлу.

Фильтр фильтрует по источнику конфигурации:

| Фильтр             | Когда он срабатывает                      |
| :----------------- | :---------------------------------------- |
| `user_settings`    | `~/.claude/settings.json` изменяется      |
| `project_settings` | `.claude/settings.json` изменяется        |
| `local_settings`   | `.claude/settings.local.json` изменяется  |
| `policy_settings`  | Управляемые параметры политики изменяются |
| `skills`           | Файл skill в `.claude/skills/` изменяется |

Этот пример логирует все изменения конфигурации для аудита безопасности:

```json theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/audit-config-change.sh"
          }
        ]
      }
    ]
  }
}
```

#### ConfigChange input

В дополнение к [общим полям входа](#common-input-fields), ConfigChange hooks получают `source` и опционально `file_path`. Поле `source` указывает, какой тип конфигурации изменился, и `file_path` предоставляет путь к конкретному изменённому файлу.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "ConfigChange",
  "source": "project_settings",
  "file_path": "/Users/.../my-project/.claude/settings.json"
}
```

#### ConfigChange decision control

ConfigChange hooks могут блокировать применение изменений конфигурации. Используйте exit code 2 или JSON `decision` для предотвращения изменения. При блокировке новые параметры не применяются к запущенному сеансу.

| Поле       | Описание                                                                                       |
| :--------- | :--------------------------------------------------------------------------------------------- |
| `decision` | `"block"` предотвращает применение изменения конфигурации. Опустите, чтобы разрешить изменение |
| `reason`   | Объяснение, показываемое пользователю при `decision` равном `"block"`                          |

```json theme={null}
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

Изменения `policy_settings` не могут быть заблокированы. Hooks всё ещё срабатывают для источников `policy_settings`, поэтому вы можете использовать их для аудита логирования, но любое решение блокировки игнорируется. Это гарантирует, что управляемые предприятием параметры всегда вступают в силу.

### CwdChanged

Запускается при изменении рабочего каталога во время сеанса, например когда Claude выполняет команду `cd`. Используйте это для реакции на изменения каталога: перезагрузка переменных окружения, активация специфичных для проекта цепочек инструментов или автоматический запуск скриптов настройки. Объединяется с [FileChanged](#filechanged) для инструментов, таких как [direnv](https://direnv.net/), которые управляют окружением для каждого каталога.

CwdChanged hooks имеют доступ к `CLAUDE_ENV_FILE`. Переменные, написанные в этот файл, сохраняются в последующих командах Bash для сеанса, как и в [SessionStart hooks](#persist-environment-variables). Поддерживаются только hooks `type: "command"`.

CwdChanged не поддерживает фильтры и срабатывает при каждом изменении каталога.

#### CwdChanged input

В дополнение к [общим полям входа](#common-input-fields), CwdChanged hooks получают `old_cwd` и `new_cwd`.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project/src",
  "hook_event_name": "CwdChanged",
  "old_cwd": "/Users/my-project",
  "new_cwd": "/Users/my-project/src"
}
```

#### CwdChanged output

В дополнение к [JSON полям выхода](#json-output), доступным для всех hooks, CwdChanged hooks могут вернуть `watchPaths` для динамической установки, какие пути файлов [FileChanged](#filechanged) отслеживает:

| Поле         | Описание                                                                                                                                                                                                                   |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `watchPaths` | Массив абсолютных путей. Заменяет текущий динамический список наблюдения (пути из конфигурации `matcher` всегда отслеживаются). Возврат пустого массива очищает динамический список, что типично при входе в новый каталог |

CwdChanged hooks не имеют управления решением. Они не могут блокировать изменение каталога.

### FileChanged

Запускается при изменении отслеживаемого файла на диске. Поле `matcher` в конфигурации hook управляет тем, какие имена файлов отслеживать: это список базовых имён, разделённых трубой (имена файлов без путей к каталогам, например `".envrc|.env"`). То же значение `matcher` также используется для фильтрации, какие hooks запускаются при изменении файла, совпадая с базовым именем изменённого файла. Полезно для перезагрузки переменных окружения при изменении файлов конфигурации проекта.

FileChanged hooks имеют доступ к `CLAUDE_ENV_FILE`. Переменные, написанные в этот файл, сохраняются в последующих командах Bash для сеанса, как и в [SessionStart hooks](#persist-environment-variables). Поддерживаются только hooks `type: "command"`.

#### FileChanged input

В дополнение к [общим полям входа](#common-input-fields), FileChanged hooks получают `file_path` и `event`.

| Поле        | Описание                                                                                     |
| :---------- | :------------------------------------------------------------------------------------------- |
| `file_path` | Абсолютный путь к файлу, который изменился                                                   |
| `event`     | Что произошло: `"change"` (файл изменён), `"add"` (файл создан) или `"unlink"` (файл удалён) |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "FileChanged",
  "file_path": "/Users/my-project/.envrc",
  "event": "change"
}
```

#### FileChanged output

В дополнение к [JSON полям выхода](#json-output), доступным для всех hooks, FileChanged hooks могут вернуть `watchPaths` для динамического обновления, какие пути файлов отслеживаются:

| Поле         | Описание                                                                                                                                                                                                                                              |
| :----------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `watchPaths` | Массив абсолютных путей. Заменяет текущий динамический список наблюдения (пути из конфигурации `matcher` всегда отслеживаются). Используйте это, когда ваш скрипт hook обнаруживает дополнительные файлы для отслеживания на основе изменённого файла |

FileChanged hooks не имеют управления решением. Они не могут блокировать изменение файла от возникновения.

### WorktreeCreate

Когда вы запускаете `claude --worktree` или [subagent использует `isolation: "worktree"`](/ru/sub-agents#choose-the-subagent-scope), Claude Code создаёт изолированную рабочую копию, используя `git worktree`. Если вы настроите hook WorktreeCreate, он заменяет поведение git по умолчанию, позволяя вам использовать другую систему контроля версий, такую как SVN, Perforce или Mercurial.

Потому что hook заменяет поведение по умолчанию полностью, [`.worktreeinclude`](/ru/common-workflows#copy-gitignored-files-to-worktrees) не обрабатывается. Если вам нужно скопировать локальные файлы конфигурации, такие как `.env`, в новый worktree, сделайте это внутри вашего скрипта hook.

Hook должен вернуть абсолютный путь к созданному каталогу worktree. Claude Code использует этот путь как рабочий каталог для изолированного сеанса. Command hooks выводят его на stdout; HTTP hooks возвращают его через `hookSpecificOutput.worktreePath`.

Этот пример создаёт рабочую копию SVN и выводит путь для использования Claude Code. Замените URL репозитория на свой:

```json theme={null}
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

Hook читает имя worktree `name` из JSON входа на stdin, проверяет свежую копию в новый каталог и выводит путь каталога. `echo` на последней строке — это то, что Claude Code читает как путь worktree. Перенаправьте любой другой выход на stderr, чтобы он не мешал пути.

#### WorktreeCreate input

В дополнение к [общим полям входа](#common-input-fields), WorktreeCreate hooks получают поле `name`. Это идентификатор slug для нового worktree, либо указанный пользователем, либо автоматически сгенерированный (например, `bold-oak-a3f2`).

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

#### WorktreeCreate output

WorktreeCreate hooks не используют стандартную модель решения разрешить/заблокировать. Вместо этого успех или сбой hook определяет результат. Hook должен вернуть абсолютный путь к созданному каталогу worktree:

* **Command hooks** (`type: "command"`): выводят путь на stdout.
* **HTTP hooks** (`type: "http"`): возвращают `{ "hookSpecificOutput": { "hookEventName": "WorktreeCreate", "worktreePath": "/absolute/path" } }` в теле ответа.

Если hook не удаётся или не производит путь, создание worktree не удаётся с ошибкой.

### WorktreeRemove

Аналог очистки для [WorktreeCreate](#worktreecreate). Этот hook срабатывает при удалении worktree, либо при выходе из сеанса `--worktree` и выборе его удаления, либо при завершении subagent с `isolation: "worktree"`. Для git-based worktrees Claude обрабатывает очистку автоматически с `git worktree remove`. Если вы настроили hook WorktreeCreate для системы контроля версий, не основанной на git, объедините его с hook WorktreeRemove для обработки очистки. Без него каталог worktree остаётся на диске.

Claude Code передаёт путь, который WorktreeCreate вывел на stdout, как `worktree_path` во входных данных hook. Этот пример читает этот путь и удаляет каталог:

```json theme={null}
{
  "hooks": {
    "WorktreeRemove": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'jq -r .worktree_path | xargs rm -rf'"
          }
        ]
      }
    ]
  }
}
```

#### WorktreeRemove input

В дополнение к [общим полям входа](#common-input-fields), WorktreeRemove hooks получают поле `worktree_path`, которое является абсолютным путём к удаляемому worktree.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

WorktreeRemove hooks не имеют управления решением. Они не могут блокировать удаление worktree, но могут выполнять задачи очистки, такие как удаление состояния контроля версий или архивирование изменений. Сбои hook логируются только в режиме отладки.

### PreCompact

Запускается перед тем, как Claude Code собирается запустить операцию компактирования.

Значение фильтра указывает, было ли компактирование запущено вручную или автоматически:

| Фильтр   | Когда он срабатывает                                            |
| :------- | :-------------------------------------------------------------- |
| `manual` | `/compact`                                                      |
| `auto`   | Автоматическое компактирование при заполнении контекстного окна |

#### PreCompact input

В дополнение к [общим полям входа](#common-input-fields), PreCompact hooks получают `trigger` и `custom_instructions`. Для `manual`, `custom_instructions` содержит то, что пользователь передаёт в `/compact`. Для `auto`, `custom_instructions` пусто.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### PostCompact

Запускается после завершения Claude Code операции компактирования. Используйте это событие для реакции на новое компактированное состояние, например для логирования сгенерированного резюме или обновления внешнего состояния.

Те же значения фильтра применяются как для `PreCompact`:

| Фильтр   | Когда он срабатывает                                                   |
| :------- | :--------------------------------------------------------------------- |
| `manual` | После `/compact`                                                       |
| `auto`   | После автоматического компактирования при заполнении контекстного окна |

#### PostCompact input

В дополнение к [общим полям входа](#common-input-fields), PostCompact hooks получают `trigger` и `compact_summary`. Поле `compact_summary` содержит резюме разговора, сгенерированное операцией компактирования.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostCompact",
  "trigger": "manual",
  "compact_summary": "Summary of the compacted conversation..."
}
```

PostCompact hooks не имеют управления решением. Они не могут влиять на результат компактирования, но могут выполнять последующие задачи.

### SessionEnd

Запускается при завершении сеанса Claude Code. Полезно для задач очистки, логирования статистики сеанса или сохранения состояния сеанса. Поддерживает фильтры для фильтрации по причине выхода.

Поле `reason` во входных данных hook указывает, почему сеанс закончился:

| Причина                       | Описание                                          |
| :---------------------------- | :------------------------------------------------ |
| `clear`                       | Сеанс очищен с помощью команды `/clear`           |
| `resume`                      | Сеанс переключен через интерактивный `/resume`    |
| `logout`                      | Пользователь вышел                                |
| `prompt_input_exit`           | Пользователь вышел, пока был виден ввод подсказки |
| `bypass_permissions_disabled` | Режим обхода разрешений был отключен              |
| `other`                       | Другие причины выхода                             |

#### SessionEnd input

В дополнение к [общим полям входа](#common-input-fields), SessionEnd hooks получают поле `reason`, указывающее, почему сеанс закончился. См. таблицу [reason](#sessionend) выше для всех значений.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

SessionEnd hooks не имеют управления решением. Они не могут блокировать завершение сеанса, но могут выполнять задачи очистки.

SessionEnd hooks имеют таймаут по умолчанию 1,5 секунды. Это применяется как к выходу из сеанса, так и к `/clear` и переключению сеансов через интерактивный `/resume`. Если вашим hooks нужно больше времени, установите переменную окружения `CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` на более высокое значение в миллисекундах. Любой параметр `timeout` для отдельного hook также ограничен этим значением.

```bash theme={null}
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000 claude
```

### Elicitation

Запускается, когда MCP сервер запрашивает ввод пользователя во время выполнения задачи. По умолчанию Claude Code показывает интерактивный диалог для ответа пользователя. Hooks могут перехватить этот запрос и ответить программно, полностью пропустив диалог.

Поле фильтра совпадает с именем MCP сервера.

#### Elicitation input

В дополнение к [общим полям входа](#common-input-fields), Elicitation hooks получают `mcp_server_name`, `message` и опциональные `mode`, `url`, `elicitation_id` и `requested_schema` поля.

Для form-mode elicitation (наиболее распространённый случай):

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please provide your credentials",
  "mode": "form",
  "requested_schema": {
    "type": "object",
    "properties": {
      "username": { "type": "string", "title": "Username" }
    }
  }
}
```

Для URL-mode elicitation (аутентификация на основе браузера):

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please authenticate",
  "mode": "url",
  "url": "https://auth.example.com/login"
}
```

#### Elicitation output

Чтобы ответить программно без показа диалога, верните JSON объект с `hookSpecificOutput`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept",
    "content": {
      "username": "alice"
    }
  }
}
```

| Поле      | Значения                      | Описание                                                                             |
| :-------- | :---------------------------- | :----------------------------------------------------------------------------------- |
| `action`  | `accept`, `decline`, `cancel` | Принять, отклонить или отменить запрос                                               |
| `content` | object                        | Значения полей формы для отправки. Используется только когда `action` равен `accept` |

Exit code 2 отклоняет elicitation и показывает stderr пользователю.

### ElicitationResult

Запускается после ответа пользователя на MCP elicitation. Hooks могут наблюдать, изменять или блокировать ответ перед его отправкой обратно на MCP сервер.

Поле фильтра совпадает с именем MCP сервера.

#### ElicitationResult input

В дополнение к [общим полям входа](#common-input-fields), ElicitationResult hooks получают `mcp_server_name`, `action` и опциональные `mode`, `elicitation_id` и `content` поля.

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "ElicitationResult",
  "mcp_server_name": "my-mcp-server",
  "action": "accept",
  "content": { "username": "alice" },
  "mode": "form",
  "elicitation_id": "elicit-123"
}
```

#### ElicitationResult output

Чтобы переопределить ответ пользователя, верните JSON объект с `hookSpecificOutput`:

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "ElicitationResult",
    "action": "decline",
    "content": {}
  }
}
```

| Поле      | Значения                      | Описание                                                                              |
| :-------- | :---------------------------- | :------------------------------------------------------------------------------------ |
| `action`  | `accept`, `decline`, `cancel` | Переопределяет действие пользователя                                                  |
| `content` | object                        | Переопределяет значения полей формы. Имеет смысл только когда `action` равен `accept` |

Exit code 2 блокирует ответ, изменяя эффективное действие на `decline`.

## Prompt-based hooks

В дополнение к command и HTTP hooks, Claude Code поддерживает prompt-based hooks (`type: "prompt"`), которые используют LLM для оценки разрешения или блокировки действия, и agent hooks (`type: "agent"`), которые порождают агентного верификатора с доступом к инструментам. Не все события поддерживают каждый тип hook.

События, которые поддерживают все четыре типа hook (`command`, `http`, `prompt` и `agent`):

* `PermissionRequest`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `TaskCreated`
* `UserPromptSubmit`

События, которые поддерживают `command` и `http` hooks, но не `prompt` или `agent`:

* `ConfigChange`
* `CwdChanged`
* `Elicitation`
* `ElicitationResult`
* `FileChanged`
* `InstructionsLoaded`
* `Notification`
* `PermissionDenied`
* `PostCompact`
* `PreCompact`
* `SessionEnd`
* `StopFailure`
* `SubagentStart`
* `TeammateIdle`
* `WorktreeCreate`
* `WorktreeRemove`

`SessionStart` поддерживает только hooks `type: "command"`.

### How prompt-based hooks work

Вместо выполнения команды Bash, prompt-based hooks:

1. Отправляют входные данные hook и вашу подсказку модели Claude, Haiku по умолчанию
2. LLM отвечает структурированным JSON, содержащим решение
3. Claude Code автоматически обрабатывает решение

### Prompt hook configuration

Установите `type` на `"prompt"` и предоставьте строку `prompt` вместо `command`. Используйте заполнитель `$ARGUMENTS` для внедрения данных JSON входа hook в текст вашей подсказки. Claude Code отправляет объединённую подсказку и входные данные быстрой модели Claude, которая возвращает JSON решение.

Этот hook `Stop` просит LLM оценить, должен ли Claude остановиться перед разрешением Claude закончить:

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
          }
        ]
      }
    ]
  }
}
```

| Поле      | Обязательно | Описание                                                                                                                                                          |
| :-------- | :---------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`    | да          | Должно быть `"prompt"`                                                                                                                                            |
| `prompt`  | да          | Текст подсказки для отправки LLM. Используйте `$ARGUMENTS` как заполнитель для JSON входа hook. Если `$ARGUMENTS` отсутствует, JSON входа добавляется к подсказке |
| `model`   | нет         | Модель для использования при оценке. По умолчанию быстрая модель                                                                                                  |
| `timeout` | нет         | Таймаут в секундах. По умолчанию: 30                                                                                                                              |

### Response schema

LLM должен ответить JSON, содержащим:

```json theme={null}
{
  "ok": true | false,
  "reason": "Explanation for the decision"
}
```

| Поле     | Описание                                                           |
| :------- | :----------------------------------------------------------------- |
| `ok`     | `true` разрешает действие, `false` предотвращает его               |
| `reason` | Требуется при `ok` равном `false`. Объяснение, показываемое Claude |

### Example: Multi-criteria Stop hook

Этот hook `Stop` использует подробную подсказку для проверки трёх условий перед разрешением Claude остановиться. Если `"ok"` равно `false`, Claude продолжает работать с предоставленной причиной как своей следующей инструкцией. Hooks `SubagentStop` используют тот же формат для оценки, должен ли [subagent](/ru/sub-agents) остановиться:

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

## Agent-based hooks

Agent-based hooks (`type: "agent"`) похожи на prompt-based hooks, но с многооборотным доступом к инструментам. Вместо одного вызова LLM, agent hook порождает subagent, который может читать файлы, искать код и проверять кодовую базу для проверки условий. Agent hooks поддерживают те же события, что и prompt-based hooks.

### How agent hooks work

Когда срабатывает agent hook:

1. Claude Code порождает subagent с вашей подсказкой и JSON входом hook
2. Subagent может использовать инструменты, такие как Read, Grep и Glob, для исследования
3. После до 50 оборотов subagent возвращает структурированное решение `{ "ok": true/false }`
4. Claude Code обрабатывает решение так же, как prompt hook

Agent hooks полезны, когда проверка требует проверки фактических файлов или выхода тестов, а не только оценки данных входа hook.

### Agent hook configuration

Установите `type` на `"agent"` и предоставьте строку `prompt`. Поля конфигурации те же, что и [prompt hooks](#prompt-hook-configuration), с более длинным таймаутом по умолчанию:

| Поле      | Обязательно | Описание                                                                                            |
| :-------- | :---------- | :-------------------------------------------------------------------------------------------------- |
| `type`    | да          | Должно быть `"agent"`                                                                               |
| `prompt`  | да          | Подсказка, описывающая, что проверять. Используйте `$ARGUMENTS` как заполнитель для JSON входа hook |
| `model`   | нет         | Модель для использования. По умолчанию быстрая модель                                               |
| `timeout` | нет         | Таймаут в секундах. По умолчанию: 60                                                                |

Схема ответа та же, что и prompt hooks: `{ "ok": true }` для разрешения или `{ "ok": false, "reason": "..." }` для блокировки.

Этот hook `Stop` проверяет, что все модульные тесты проходят перед разрешением Claude закончить:

```json theme={null}
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

## Run hooks in the background

По умолчанию hooks блокируют выполнение Claude до их завершения. Для долгоживущих задач, таких как развёртывания, наборы тестов или вызовы внешних API, установите `"async": true` для запуска hook в фоне, пока Claude продолжает работать. Асинхронные hooks не могут блокировать или управлять поведением Claude: поля ответа, такие как `decision`, `permissionDecision` и `continue`, не имеют эффекта, потому что действие, которое они контролировали, уже завершено.

### Configure an async hook

Добавьте `"async": true` к конфигурации command hook для запуска его в фоне без блокировки Claude. Это поле доступно только на hooks `type: "command"`.

Этот hook запускает скрипт тестирования после каждого вызова инструмента `Write`. Claude продолжает работать немедленно, пока `run-tests.sh` выполняется до 120 секунд. Когда скрипт завершается, его выход доставляется на следующий ход разговора:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true,
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

Поле `timeout` устанавливает максимальное время в секундах для фонового процесса. Если не указано, асинхронные hooks используют тот же 10-минутный таймаут по умолчанию, что и синхронные hooks.

### How async hooks execute

Когда срабатывает асинхронный hook, Claude Code запускает процесс hook и немедленно продолжает без ожидания его завершения. Hook получает те же JSON входные данные через stdin, что и синхронный hook.

После выхода фонового процесса, если hook произвёл JSON ответ с полем `systemMessage` или `additionalContext`, это содержимое доставляется Claude как контекст на следующем ходу разговора.

Уведомления о завершении асинхронного hook подавляются по умолчанию. Чтобы их увидеть, включите подробный режим с помощью `Ctrl+O` или запустите Claude Code с `--verbose`.

### Example: run tests after file changes

Этот hook запускает набор тестов в фоне всякий раз, когда Claude пишет файл, затем сообщает результаты обратно Claude при завершении тестов. Сохраните этот скрипт в `.claude/hooks/run-tests-async.sh` в вашем проекте и сделайте его исполняемым с помощью `chmod +x`:

```bash theme={null}
#!/bin/bash
# run-tests-async.sh

# Read hook input from stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Only run tests for source files
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# Run tests and report results via systemMessage
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "{\"systemMessage\": \"Tests passed after editing $FILE_PATH\"}"
else
  echo "{\"systemMessage\": \"Tests failed after editing $FILE_PATH: $RESULT\"}"
fi
```

Затем добавьте эту конфигурацию в `.claude/settings.json` в корне вашего проекта. Флаг `async: true` позволяет Claude продолжать работу, пока тесты запускаются:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/run-tests-async.sh",
            "async": true,
            "timeout": 300
          }
        ]
      }
    ]
  }
}
```

### Limitations

Асинхронные hooks имеют несколько ограничений по сравнению с синхронными hooks:

* Только hooks `type: "command"` поддерживают `async`. Prompt-based hooks не могут запускаться асинхронно.
* Асинхронные hooks не могут блокировать вызовы инструментов или возвращать решения. К моменту завершения hook действие, вызвавшее его, уже произошло.
* Выход hook доставляется на следующий ход разговора. Если сеанс неактивен, ответ ждёт до следующего взаимодействия пользователя.
* Каждое выполнение создаёт отдельный фоновый процесс. Нет дедупликации между несколькими срабатываниями одного и того же асинхронного hook.

## Security considerations

### Disclaimer

Command hooks запускаются с полными разрешениями системного пользователя.

<Warning>
  Command hooks выполняют команды оболочки с вашими полными разрешениями пользователя. Они могут изменять, удалять или получать доступ к любым файлам, к которым может получить доступ ваша учётная запись пользователя. Проверьте и протестируйте все команды hook перед добавлением их в вашу конфигурацию.
</Warning>

### Security best practices

Помните об этих практиках при написании hooks:

* **Проверяйте и санитизируйте входные данные**: никогда не доверяйте входным данным вслепую
* **Всегда заключайте переменные оболочки в кавычки**: используйте `"$VAR"` не `$VAR`
* **Блокируйте обход пути**: проверяйте наличие `..` в путях файлов
* **Используйте абсолютные пути**: указывайте полные пути для скриптов, используя `"$CLAUDE_PROJECT_DIR"` для корня проекта
* **Пропускайте чувствительные файлы**: избегайте `.env`, `.git/`, ключей и т. д.

## Debug hooks

Запустите `claude --debug` для просмотра деталей выполнения hook, включая какие hooks совпали, их коды выхода и выход.

```text theme={null}
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

Для более детальной информации о совпадении hooks установите `CLAUDE_CODE_DEBUG_LOG_LEVEL=verbose` для просмотра дополнительных строк логирования, таких как количество совпадений фильтра hook и совпадение запроса.

Для устранения неполадок распространённых проблем, таких как hooks, которые не срабатывают, бесконечные циклы Stop hook или ошибки конфигурации, см. [Limitations and troubleshooting](/ru/hooks-guide#limitations-and-troubleshooting) в руководстве.

## Windows PowerShell tool

На Windows вы можете запустить отдельные hooks в PowerShell, установив `"shell": "powershell"` на command hook. Hooks порождают PowerShell напрямую, поэтому это работает независимо от того, установлен ли `CLAUDE_CODE_USE_POWERSHELL_TOOL`. Claude Code автоматически обнаруживает `pwsh.exe` (PowerShell 7+) с резервным вариантом на `powershell.exe` (5.1).

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "command": "Write-Host 'File written'"
          }
        ]
      }
    ]
  }
}
```
