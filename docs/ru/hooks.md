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

Hooks срабатывают в определённых точках сеанса Claude Code. Когда событие срабатывает и совпадает с matcher, Claude Code передаёт JSON контекст события вашему обработчику hook. Для command hooks входные данные поступают на stdin. Для HTTP hooks они поступают как тело POST запроса. Ваш обработчик может затем проверить входные данные, выполнить действие и опционально вернуть решение. Некоторые события срабатывают один раз за сеанс, а другие срабатывают повторно внутри агентского цикла:

<div style={{maxWidth: "500px", margin: "0 auto"}}>
  <Frame>
    <img src="https://mintcdn.com/claude-code/lBsitdsGyD9caWJQ/images/hooks-lifecycle.svg?fit=max&auto=format&n=lBsitdsGyD9caWJQ&q=85&s=be3486ef2cf2563eb213b6cbbce93982" alt="Диаграмма жизненного цикла hook, показывающая последовательность hooks от SessionStart через агентский цикл к SessionEnd, с WorktreeCreate, WorktreeRemove и InstructionsLoaded как отдельные асинхронные события" width="520" height="1100" data-path="images/hooks-lifecycle.svg" />
  </Frame>
</div>

Таблица ниже суммирует, когда срабатывает каждое событие. Раздел [Hook events](#hook-events) документирует полную схему входа и параметры управления решением для каждого события.

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

### Как разрешается hook

Чтобы увидеть, как эти части работают вместе, рассмотрим этот hook `PreToolUse`, который блокирует деструктивные команды оболочки. Hook запускает `block-rm.sh` перед каждым вызовом инструмента Bash:

```json  theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": ".claude/hooks/block-rm.sh"
          }
        ]
      }
    ]
  }
}
```

Скрипт читает JSON входные данные из stdin, извлекает команду и возвращает `permissionDecision` со значением `"deny"`, если она содержит `rm -rf`:

```bash  theme={null}
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
  <img src="https://mintcdn.com/claude-code/c5r9_6tjPMzFdDDT/images/hook-resolution.svg?fit=max&auto=format&n=c5r9_6tjPMzFdDDT&q=85&s=ad667ee6d86ab2276aa48a4e73e220df" alt="Поток разрешения hook: событие PreToolUse срабатывает, matcher проверяет совпадение Bash, обработчик hook запускается, результат возвращается в Claude Code" width="780" height="290" data-path="images/hook-resolution.svg" />
</Frame>

<Steps>
  <Step title="Событие срабатывает">
    Событие `PreToolUse` срабатывает. Claude Code отправляет входные данные инструмента как JSON на stdin к hook:

    ```json  theme={null}
    { "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
    ```
  </Step>

  <Step title="Matcher проверяет">
    Matcher `"Bash"` совпадает с именем инструмента, поэтому запускается `block-rm.sh`. Если вы опустите matcher или используете `"*"`, hook запускается при каждом возникновении события. Hooks пропускаются только когда определён matcher и он не совпадает.
  </Step>

  <Step title="Обработчик hook запускается">
    Скрипт извлекает `"rm -rf /tmp/build"` из входных данных и находит `rm -rf`, поэтому он выводит решение на stdout:

    ```json  theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Destructive command blocked by hook"
      }
    }
    ```

    Если бы команда была безопасной (например, `npm test`), скрипт вместо этого выполнил бы `exit 0`, что говорит Claude Code разрешить вызов инструмента без дальнейших действий.
  </Step>

  <Step title="Claude Code действует на основе результата">
    Claude Code читает решение JSON, блокирует вызов инструмента и показывает Claude причину.
  </Step>
</Steps>

Раздел [Configuration](#configuration) ниже документирует полную схему, и каждый раздел [hook event](#hook-events) документирует, какие входные данные получает ваша команда и какие выходные данные она может вернуть.

## Конфигурация

Hooks определяются в файлах настроек JSON. Конфигурация имеет три уровня вложенности:

1. Выберите [hook event](#hook-events) для ответа, например `PreToolUse` или `Stop`
2. Добавьте [matcher group](#matcher-patterns) для фильтрации, когда он срабатывает, например "только для инструмента Bash"
3. Определите один или несколько [hook handlers](#hook-handler-fields) для запуска при совпадении

См. [Как разрешается hook](#how-a-hook-resolves) выше для полного пошагового руководства с аннотированным примером.

<Note>
  На этой странице используются специальные термины для каждого уровня: **hook event** для точки жизненного цикла, **matcher group** для фильтра и **hook handler** для команды оболочки, конечной точки HTTP, подсказки или агента, который запускается. "Hook" само по себе относится к общей функции.
</Note>

### Расположение hook

Место, где вы определяете hook, определяет его область действия:

| Расположение                                                | Область действия       | Общий доступ                          |
| :---------------------------------------------------------- | :--------------------- | :------------------------------------ |
| `~/.claude/settings.json`                                   | Все ваши проекты       | Нет, локально на вашей машине         |
| `.claude/settings.json`                                     | Один проект            | Да, можно зафиксировать в репозитории |
| `.claude/settings.local.json`                               | Один проект            | Нет, gitignored                       |
| Управляемые параметры политики                              | Организация            | Да, контролируется администратором    |
| [Plugin](/ru/plugins) `hooks/hooks.json`                    | Когда плагин включен   | Да, поставляется с плагином           |
| [Skill](/ru/skills) или [agent](/ru/sub-agents) frontmatter | Пока компонент активен | Да, определено в файле компонента     |

Для получения подробной информации о разрешении файлов настроек см. [settings](/ru/settings). Администраторы предприятия могут использовать `allowManagedHooksOnly` для блокировки пользовательских, проектных и плагинных hooks. См. [Hook configuration](/ru/settings#hook-configuration).

### Matcher patterns

Поле `matcher` — это строка regex, которая фильтрует, когда срабатывают hooks. Используйте `"*"`, `""` или опустите `matcher` полностью, чтобы совпадать со всеми вхождениями. Каждый тип события совпадает с другим полем:

| Событие                                                                                                               | На что фильтрует matcher      | Примеры значений matcher                                                           |
| :-------------------------------------------------------------------------------------------------------------------- | :---------------------------- | :--------------------------------------------------------------------------------- |
| `PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`                                                | имя инструмента               | `Bash`, `Edit\|Write`, `mcp__.*`                                                   |
| `SessionStart`                                                                                                        | как начался сеанс             | `startup`, `resume`, `clear`, `compact`                                            |
| `SessionEnd`                                                                                                          | почему закончился сеанс       | `clear`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`     |
| `Notification`                                                                                                        | тип уведомления               | `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`           |
| `SubagentStart`                                                                                                       | тип агента                    | `Bash`, `Explore`, `Plan` или пользовательские имена агентов                       |
| `PreCompact`                                                                                                          | что вызвало компактирование   | `manual`, `auto`                                                                   |
| `SubagentStop`                                                                                                        | тип агента                    | те же значения, что и `SubagentStart`                                              |
| `ConfigChange`                                                                                                        | источник конфигурации         | `user_settings`, `project_settings`, `local_settings`, `policy_settings`, `skills` |
| `UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove`, `InstructionsLoaded` | поддержка matcher отсутствует | всегда срабатывает при каждом вхождении                                            |

Matcher — это regex, поэтому `Edit|Write` совпадает с любым инструментом и `Notebook.*` совпадает с любым инструментом, начинающимся с Notebook. Matcher запускается против поля из [JSON входа](#hook-input-and-output), который Claude Code отправляет вашему hook на stdin. Для событий инструмента это поле — `tool_name`. Каждый раздел [hook event](#hook-events) перечисляет полный набор значений matcher и схему входа для этого события.

Этот пример запускает скрипт линтинга только когда Claude пишет или редактирует файл:

```json  theme={null}
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

`UserPromptSubmit`, `Stop`, `TeammateIdle`, `TaskCompleted`, `WorktreeCreate`, `WorktreeRemove` и `InstructionsLoaded` не поддерживают matchers и всегда срабатывают при каждом вхождении. Если вы добавите поле `matcher` к этим событиям, оно будет молча проигнорировано.

#### Совпадение MCP инструментов

Инструменты [MCP](/ru/mcp) сервера отображаются как обычные инструменты в событиях инструментов (`PreToolUse`, `PostToolUse`, `PostToolUseFailure`, `PermissionRequest`), поэтому вы можете совпадать с ними так же, как с любым другим именем инструмента.

MCP инструменты следуют шаблону именования `mcp__<server>__<tool>`, например:

* `mcp__memory__create_entities`: инструмент create entities сервера Memory
* `mcp__filesystem__read_file`: инструмент read file сервера Filesystem
* `mcp__github__search_repositories`: инструмент search сервера GitHub

Используйте regex шаблоны для нацеливания на конкретные MCP инструменты или группы инструментов:

* `mcp__memory__.*` совпадает со всеми инструментами сервера `memory`
* `mcp__.*__write.*` совпадает с любым инструментом, содержащим "write" из любого сервера

Этот пример логирует все операции сервера memory и проверяет операции write из любого MCP сервера:

```json  theme={null}
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

Каждый объект во внутреннем массиве `hooks` — это hook handler: команда оболочки, конечная точка HTTP, подсказка LLM или агент, который запускается при совпадении matcher. Есть четыре типа:

* **[Command hooks](#command-hook-fields)** (`type: "command"`): запускают команду оболочки. Ваш скрипт получает [JSON входные данные](#hook-input-and-output) события на stdin и передаёт результаты обратно через коды выхода и stdout.
* **[HTTP hooks](#http-hook-fields)** (`type: "http"`): отправляют JSON входные данные события как HTTP POST запрос на URL. Конечная точка передаёт результаты обратно через тело ответа, используя тот же [JSON формат выхода](#json-output), что и command hooks.
* **[Prompt hooks](#prompt-and-agent-hook-fields)** (`type: "prompt"`): отправляют подсказку модели Claude для однооборотной оценки. Модель возвращает решение да/нет как JSON. См. [Prompt-based hooks](#prompt-based-hooks).
* **[Agent hooks](#prompt-and-agent-hook-fields)** (`type: "agent"`): порождают subagent, который может использовать инструменты, такие как Read, Grep и Glob, для проверки условий перед возвратом решения. См. [Agent-based hooks](#agent-based-hooks).

#### Общие поля

Эти поля применяются ко всем типам hooks:

| Поле            | Обязательно | Описание                                                                                                                                                    |
| :-------------- | :---------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`          | да          | `"command"`, `"http"`, `"prompt"` или `"agent"`                                                                                                             |
| `timeout`       | нет         | Секунды перед отменой. Значения по умолчанию: 600 для command, 30 для prompt, 60 для agent                                                                  |
| `statusMessage` | нет         | Пользовательское сообщение спиннера, отображаемое во время выполнения hook                                                                                  |
| `once`          | нет         | Если `true`, запускается только один раз за сеанс, затем удаляется. Только skills, не agents. См. [Hooks in skills and agents](#hooks-in-skills-and-agents) |

#### Command hook fields

В дополнение к [общим полям](#common-fields), command hooks принимают эти поля:

| Поле      | Обязательно | Описание                                                                                                        |
| :-------- | :---------- | :-------------------------------------------------------------------------------------------------------------- |
| `command` | да          | Команда оболочки для выполнения                                                                                 |
| `async`   | нет         | Если `true`, запускается в фоне без блокировки. См. [Run hooks in the background](#run-hooks-in-the-background) |

#### HTTP hook fields

В дополнение к [общим полям](#common-fields), HTTP hooks принимают эти поля:

| Поле             | Обязательно | Описание                                                                                                                                                                                                                    |
| :--------------- | :---------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url`            | да          | URL для отправки POST запроса                                                                                                                                                                                               |
| `headers`        | нет         | Дополнительные HTTP заголовки как пары ключ-значение. Значения поддерживают интерполяцию переменных окружения, используя синтаксис `$VAR_NAME` или `${VAR_NAME}`. Разрешены только переменные, указанные в `allowedEnvVars` |
| `allowedEnvVars` | нет         | Список имён переменных окружения, которые могут быть интерполированы в значения заголовков. Ссылки на неуказанные переменные заменяются пустыми строками. Требуется для любой интерполяции переменных окружения             |

Claude Code отправляет [JSON входные данные](#hook-input-and-output) hook как тело POST запроса с `Content-Type: application/json`. Тело ответа использует тот же [JSON формат выхода](#json-output), что и command hooks.

Обработка ошибок отличается от command hooks: ответы не 2xx, сбои соединения и таймауты все производят неблокирующие ошибки, которые позволяют выполнению продолжаться. Чтобы заблокировать вызов инструмента или отклонить разрешение, верните ответ 2xx с телом JSON, содержащим `decision: "block"` или `hookSpecificOutput` с `permissionDecision: "deny"`.

Этот пример отправляет события `PreToolUse` на локальный сервис валидации, аутентифицируясь с помощью токена из переменной окружения `MY_TOKEN`:

```json  theme={null}
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

<Note>
  HTTP hooks должны быть настроены путём прямого редактирования JSON параметров. Интерактивное меню `/hooks` поддерживает только добавление command hooks.
</Note>

#### Prompt and agent hook fields

В дополнение к [общим полям](#common-fields), prompt и agent hooks принимают эти поля:

| Поле     | Обязательно | Описание                                                                                          |
| :------- | :---------- | :------------------------------------------------------------------------------------------------ |
| `prompt` | да          | Текст подсказки для отправки модели. Используйте `$ARGUMENTS` как заполнитель для JSON входа hook |
| `model`  | нет         | Модель для использования при оценке. По умолчанию быстрая модель                                  |

Все совпадающие hooks запускаются параллельно, и идентичные обработчики автоматически дедублируются. Command hooks дедублируются по строке команды, а HTTP hooks дедублируются по URL. Обработчики запускаются в текущем каталоге с окружением Claude Code. Переменная окружения `$CLAUDE_CODE_REMOTE` устанавливается на `"true"` в удалённых веб-окружениях и не устанавливается в локальном CLI.

### Ссылка на скрипты по пути

Используйте переменные окружения для ссылки на скрипты hook относительно корня проекта или плагина, независимо от рабочего каталога при запуске hook:

* `$CLAUDE_PROJECT_DIR`: корень проекта. Оберните в кавычки для обработки путей с пробелами.
* `${CLAUDE_PLUGIN_ROOT}`: корневой каталог плагина для скриптов, поставляемых с [плагином](/ru/plugins).

<Tabs>
  <Tab title="Project scripts">
    Этот пример использует `$CLAUDE_PROJECT_DIR` для запуска проверки стиля из каталога `.claude/hooks/` проекта после любого вызова инструмента `Write` или `Edit`:

    ```json  theme={null}
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
    Определите hooks плагина в `hooks/hooks.json` с опциональным полем `description` верхнего уровня. Когда плагин включен, его hooks объединяются с вашими пользовательскими и проектными hooks.

    Этот пример запускает скрипт форматирования, поставляемый с плагином:

    ```json  theme={null}
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

    См. [plugin components reference](/ru/plugins-reference#hooks) для получения подробной информации о создании hooks плагина.
  </Tab>
</Tabs>

### Hooks in skills and agents

В дополнение к файлам параметров и плагинам, hooks могут быть определены непосредственно в [skills](/ru/skills) и [subagents](/ru/sub-agents), используя frontmatter. Эти hooks ограничены жизненным циклом компонента и запускаются только, когда этот компонент активен.

Поддерживаются все события hook. Для subagents, hooks `Stop` автоматически преобразуются в `SubagentStop`, поскольку это событие, которое срабатывает при завершении subagent.

Hooks используют тот же формат конфигурации, что и hooks на основе параметров, но ограничены временем жизни компонента и очищаются при его завершении.

Этот skill определяет hook `PreToolUse`, который запускает скрипт проверки безопасности перед каждой командой `Bash`:

```yaml  theme={null}
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

Введите `/hooks` в Claude Code, чтобы открыть интерактивный менеджер hooks, где вы можете просматривать, добавлять и удалять hooks без прямого редактирования файлов параметров. Для пошагового руководства см. [Set up your first hook](/ru/hooks-guide#set-up-your-first-hook) в руководстве.

Каждый hook в меню помечен префиксом в скобках, указывающим его источник:

* `[User]`: из `~/.claude/settings.json`
* `[Project]`: из `.claude/settings.json`
* `[Local]`: из `.claude/settings.local.json`
* `[Plugin]`: из `hooks/hooks.json` плагина, только для чтения

### Отключение или удаление hooks

Чтобы удалить hook, удалите его запись из файла параметров JSON или используйте меню `/hooks` и выберите hook для его удаления.

Чтобы временно отключить все hooks без их удаления, установите `"disableAllHooks": true` в файле параметров или используйте переключатель в меню `/hooks`. Нет способа отключить отдельный hook, сохраняя его в конфигурации.

Параметр `disableAllHooks` соблюдает иерархию управляемых параметров. Если администратор настроил hooks через управляемые параметры политики, `disableAllHooks`, установленный в пользовательских, проектных или локальных параметрах, не может отключить эти управляемые hooks. Только `disableAllHooks`, установленный на уровне управляемых параметров, может отключить управляемые hooks.

Прямые редактирования hooks в файлах параметров не вступают в силу немедленно. Claude Code захватывает снимок hooks при запуске и использует его на протяжении всего сеанса. Это предотвращает вступление в силу вредоносных или случайных изменений hook в середине сеанса без вашего рассмотрения. Если hooks изменяются извне, Claude Code предупреждает вас и требует рассмотрения в меню `/hooks` перед применением изменений.

## Hook input and output

Command hooks получают JSON данные через stdin и передают результаты через коды выхода, stdout и stderr. HTTP hooks получают тот же JSON как тело POST запроса и передают результаты через тело ответа HTTP. Этот раздел охватывает поля и поведение, общие для всех событий. Каждый раздел события под [Hook events](#hook-events) включает его специфическую схему входа и параметры управления решением.

### Common input fields

Все события hook получают эти поля как JSON, в дополнение к полям, специфичным для события, документированным в каждом разделе [hook event](#hook-events). Для command hooks этот JSON поступает через stdin. Для HTTP hooks он поступает как тело POST запроса.

| Поле              | Описание                                                                                                                                    |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `session_id`      | Текущий идентификатор сеанса                                                                                                                |
| `transcript_path` | Путь к JSON разговора                                                                                                                       |
| `cwd`             | Текущий рабочий каталог при вызове hook                                                                                                     |
| `permission_mode` | Текущий [режим разрешения](/ru/permissions#permission-modes): `"default"`, `"plan"`, `"acceptEdits"`, `"dontAsk"` или `"bypassPermissions"` |
| `hook_event_name` | Имя события, которое сработало                                                                                                              |

При запуске с `--agent` или внутри subagent включаются два дополнительных поля:

| Поле         | Описание                                                                                                                                                                                                                     |
| :----------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `agent_id`   | Уникальный идентификатор для subagent. Присутствует только когда hook срабатывает внутри вызова subagent. Используйте это для различения вызовов hook subagent от вызовов основного потока.                                  |
| `agent_type` | Имя агента (например, `"Explore"` или `"security-reviewer"`). Присутствует когда сеанс использует `--agent` или hook срабатывает внутри subagent. Для subagents тип subagent имеет приоритет над значением `--agent` сеанса. |

Например, hook `PreToolUse` для команды Bash получает это на stdin:

```json  theme={null}
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

**Exit 0** означает успех. Claude Code анализирует stdout для [полей JSON выхода](#json-output). JSON выход обрабатывается только при выходе 0. Для большинства событий stdout показывается только в подробном режиме (`Ctrl+O`). Исключения — `UserPromptSubmit` и `SessionStart`, где stdout добавляется как контекст, который Claude может видеть и действовать.

**Exit 2** означает блокирующую ошибку. Claude Code игнорирует stdout и любой JSON в нём. Вместо этого текст stderr передаётся обратно Claude как сообщение об ошибке. Эффект зависит от события: `PreToolUse` блокирует вызов инструмента, `UserPromptSubmit` отклоняет подсказку и так далее. См. [exit code 2 behavior](#exit-code-2-behavior-per-event) для полного списка.

**Любой другой код выхода** — это неблокирующая ошибка. stderr показывается в подробном режиме (`Ctrl+O`) и выполнение продолжается.

Например, скрипт команды hook, который блокирует опасные команды Bash:

```bash  theme={null}
#!/bin/bash
# Читает JSON входные данные из stdin, проверяет команду
command=$(jq -r '.tool_input.command' < /dev/stdin)

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # Блокирующая ошибка: вызов инструмента предотвращен
fi

exit 0  # Успех: вызов инструмента продолжается
```

#### Exit code 2 behavior per event

Exit code 2 — это способ hook сигнализировать "стоп, не делай этого". Эффект зависит от события, потому что некоторые события представляют действия, которые могут быть заблокированы (например, вызов инструмента, который ещё не произошёл), а другие представляют вещи, которые уже произошли или не могут быть предотвращены.

| Hook event           | Может блокировать? | Что происходит при exit 2                                                     |
| :------------------- | :----------------- | :---------------------------------------------------------------------------- |
| `PreToolUse`         | Да                 | Блокирует вызов инструмента                                                   |
| `PermissionRequest`  | Да                 | Отклоняет разрешение                                                          |
| `UserPromptSubmit`   | Да                 | Блокирует обработку подсказки и стирает подсказку                             |
| `Stop`               | Да                 | Предотвращает остановку Claude, продолжает разговор                           |
| `SubagentStop`       | Да                 | Предотвращает остановку subagent                                              |
| `TeammateIdle`       | Да                 | Предотвращает переход товарища в режим ожидания (товарищ продолжает работать) |
| `TaskCompleted`      | Да                 | Предотвращает отметку задачи как завершённой                                  |
| `ConfigChange`       | Да                 | Блокирует применение изменения конфигурации (кроме `policy_settings`)         |
| `PostToolUse`        | Нет                | Показывает stderr Claude (инструмент уже запустился)                          |
| `PostToolUseFailure` | Нет                | Показывает stderr Claude (инструмент уже не прошёл)                           |
| `Notification`       | Нет                | Показывает stderr только пользователю                                         |
| `SubagentStart`      | Нет                | Показывает stderr только пользователю                                         |
| `SessionStart`       | Нет                | Показывает stderr только пользователю                                         |
| `SessionEnd`         | Нет                | Показывает stderr только пользователю                                         |
| `PreCompact`         | Нет                | Показывает stderr только пользователю                                         |
| `WorktreeCreate`     | Да                 | Любой ненулевой код выхода вызывает сбой создания worktree                    |
| `WorktreeRemove`     | Нет                | Сбои логируются только в режиме отладки                                       |
| `InstructionsLoaded` | Нет                | Код выхода игнорируется                                                       |

### HTTP response handling

HTTP hooks используют коды статуса HTTP и тела ответов вместо кодов выхода и stdout:

* **2xx с пустым телом**: успех, эквивалентно exit code 0 без выхода
* **2xx с телом простого текста**: успех, текст добавляется как контекст
* **2xx с телом JSON**: успех, анализируется с использованием той же схемы [JSON выхода](#json-output), что и command hooks
* **Статус не 2xx**: неблокирующая ошибка, выполнение продолжается
* **Сбой соединения или таймаут**: неблокирующая ошибка, выполнение продолжается

В отличие от command hooks, HTTP hooks не могут сигнализировать блокирующую ошибку только через коды статуса. Чтобы заблокировать вызов инструмента или отклонить разрешение, верните ответ 2xx с телом JSON, содержащим соответствующие поля решения.

### JSON output

Коды выхода позволяют вам разрешить или заблокировать, но JSON выход даёт вам более точное управление. Вместо выхода с кодом 2 для блокировки, выйдите с 0 и выведите объект JSON на stdout. Claude Code читает определённые поля из этого JSON для управления поведением, включая [decision control](#decision-control) для блокировки, разрешения или эскалации пользователю.

<Note>
  Вы должны выбрать один подход на hook, не оба: либо используйте коды выхода отдельно для сигнализации, либо выйдите с 0 и выведите JSON для структурированного управления. Claude Code обрабатывает JSON только при exit 0. Если вы выйдете с 2, любой JSON игнорируется.
</Note>

Stdout вашего hook должен содержать только объект JSON. Если ваш профиль оболочки выводит текст при запуске, это может помешать анализу JSON. См. [JSON validation failed](/ru/hooks-guide#json-validation-failed) в руководстве по устранению неполадок.

Объект JSON поддерживает три вида полей:

* **Универсальные поля** как `continue` работают во всех событиях. Они перечислены в таблице ниже.
* **Верхнеуровневые `decision` и `reason`** используются некоторыми событиями для блокировки или предоставления обратной связи.
* **`hookSpecificOutput`** — это вложенный объект для событий, которым требуется более богатое управление. Он требует поле `hookEventName`, установленное на имя события.

| Поле             | По умолчанию | Описание                                                                                                                                    |
| :--------------- | :----------- | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `continue`       | `true`       | Если `false`, Claude полностью прекращает обработку после запуска hook. Имеет приоритет над любыми полями решения, специфичными для события |
| `stopReason`     | нет          | Сообщение, показываемое пользователю при `continue` равном `false`. Не показывается Claude                                                  |
| `suppressOutput` | `false`      | Если `true`, скрывает stdout из выхода подробного режима                                                                                    |
| `systemMessage`  | нет          | Предупреждающее сообщение, показываемое пользователю                                                                                        |

Чтобы полностью остановить Claude независимо от типа события:

```json  theme={null}
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

#### Decision control

Не каждое событие поддерживает блокировку или управление поведением через JSON. События, которые это делают, каждое использует другой набор полей для выражения этого решения. Используйте эту таблицу как быструю ссылку перед написанием hook:

| События                                                                             | Шаблон решения                   | Ключевые поля                                                                                                                                                                      |
| :---------------------------------------------------------------------------------- | :------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| UserPromptSubmit, PostToolUse, PostToolUseFailure, Stop, SubagentStop, ConfigChange | Верхнеуровневое `decision`       | `decision: "block"`, `reason`                                                                                                                                                      |
| TeammateIdle, TaskCompleted                                                         | Код выхода или `continue: false` | Exit code 2 блокирует действие с обратной связью stderr. JSON `{"continue": false, "stopReason": "..."}` также останавливает товарища полностью, совпадая с поведением hook `Stop` |
| PreToolUse                                                                          | `hookSpecificOutput`             | `permissionDecision` (allow/deny/ask), `permissionDecisionReason`                                                                                                                  |
| PermissionRequest                                                                   | `hookSpecificOutput`             | `decision.behavior` (allow/deny)                                                                                                                                                   |
| WorktreeCreate                                                                      | путь stdout                      | Hook выводит абсолютный путь к созданному worktree. Ненулевой выход не удаётся создание                                                                                            |
| WorktreeRemove, Notification, SessionEnd, PreCompact, InstructionsLoaded            | Нет                              | Нет управления решением. Используется для побочных эффектов, таких как логирование или очистка                                                                                     |

Вот примеры каждого шаблона в действии:

<Tabs>
  <Tab title="Top-level decision">
    Используется `UserPromptSubmit`, `PostToolUse`, `PostToolUseFailure`, `Stop`, `SubagentStop` и `ConfigChange`. Единственное значение — `"block"`. Чтобы разрешить действию продолжаться, опустите `decision` из вашего JSON или выйдите с 0 без какого-либо JSON вообще:

    ```json  theme={null}
    {
      "decision": "block",
      "reason": "Test suite must pass before proceeding"
    }
    ```
  </Tab>

  <Tab title="PreToolUse">
    Использует `hookSpecificOutput` для более богатого управления: разрешить, отклонить или эскалировать пользователю. Вы также можете изменить входные данные инструмента перед его запуском или внедрить дополнительный контекст для Claude. См. [PreToolUse decision control](#pretooluse-decision-control) для полного набора параметров.

    ```json  theme={null}
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

    ```json  theme={null}
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

Каждое событие соответствует точке в жизненном цикле Claude Code, где могут запускаться hooks. Разделы ниже упорядочены в соответствии с жизненным циклом: от настройки сеанса через агентский цикл к концу сеанса. Каждый раздел описывает, когда срабатывает событие, какие matchers оно поддерживает, JSON входные данные, которые оно получает, и как управлять поведением через выход.

### SessionStart

Запускается при запуске Claude Code нового сеанса или возобновлении существующего сеанса. Полезно для загрузки контекста разработки, такого как существующие проблемы или недавние изменения в вашей кодовой базе, или установки переменных окружения. Для статического контекста, который не требует скрипта, используйте [CLAUDE.md](/ru/memory) вместо этого.

SessionStart запускается при каждом сеансе, поэтому держите эти hooks быстрыми. Поддерживаются только hooks `type: "command"`.

Значение matcher соответствует тому, как был инициирован сеанс:

| Matcher   | Когда он срабатывает                      |
| :-------- | :---------------------------------------- |
| `startup` | Новый сеанс                               |
| `resume`  | `--resume`, `--continue` или `/resume`    |
| `clear`   | `/clear`                                  |
| `compact` | Автоматическое или ручное компактирование |

#### SessionStart input

В дополнение к [общим полям входа](#common-input-fields), hooks SessionStart получают `source`, `model` и опционально `agent_type`. Поле `source` указывает, как начался сеанс: `"startup"` для новых сеансов, `"resume"` для возобновлённых сеансов, `"clear"` после `/clear` или `"compact"` после компактирования. Поле `model` содержит идентификатор модели. Если вы запустите Claude Code с `claude --agent <name>`, поле `agent_type` содержит имя агента.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SessionStart",
  "source": "startup",
  "model": "claude-sonnet-4-6"
}
```

#### SessionStart decision control

Любой текст, который ваш скрипт hook выводит на stdout, добавляется как контекст для Claude. В дополнение к [полям JSON выхода](#json-output), доступным для всех hooks, вы можете вернуть эти поля, специфичные для события:

| Поле                | Описание                                                                      |
| :------------------ | :---------------------------------------------------------------------------- |
| `additionalContext` | Строка, добавляемая в контекст Claude. Значения нескольких hooks объединяются |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "My additional context here"
  }
}
```

#### Persist environment variables

Hooks SessionStart имеют доступ к переменной окружения `CLAUDE_ENV_FILE`, которая предоставляет путь к файлу, где вы можете сохранять переменные окружения для последующих команд Bash.

Чтобы установить отдельные переменные окружения, напишите операторы `export` в `CLAUDE_ENV_FILE`. Используйте append (`>>`) для сохранения переменных, установленных другими hooks:

```bash  theme={null}
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

Чтобы захватить все изменения окружения из команд настройки, сравните экспортированные переменные до и после:

```bash  theme={null}
#!/bin/bash

ENV_BEFORE=$(export -p | sort)

# Запустите ваши команды настройки, которые изменяют окружение
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
  `CLAUDE_ENV_FILE` доступен для hooks SessionStart. Другие типы hooks не имеют доступа к этой переменной.
</Note>

### InstructionsLoaded

Срабатывает при загрузке файла `CLAUDE.md` или `.claude/rules/*.md` в контекст. Это событие срабатывает при запуске сеанса для нетерпеливо загруженных файлов и снова позже при ленивой загрузке, например, когда Claude получает доступ к подкаталогу, содержащему вложенный `CLAUDE.md`, или когда условные правила с frontmatter `paths:` совпадают. Hook не поддерживает блокировку или управление решением. Он запускается асинхронно в целях наблюдаемости.

InstructionsLoaded не поддерживает matchers и срабатывает при каждом вхождении загрузки.

#### InstructionsLoaded input

В дополнение к [общим полям входа](#common-input-fields), hooks InstructionsLoaded получают эти поля:

| Поле                | Описание                                                                                                       |
| :------------------ | :------------------------------------------------------------------------------------------------------------- |
| `file_path`         | Абсолютный путь к файлу инструкций, который был загружен                                                       |
| `memory_type`       | Область файла: `"User"`, `"Project"`, `"Local"` или `"Managed"`                                                |
| `load_reason`       | Почему файл был загружен: `"session_start"`, `"nested_traversal"`, `"path_glob_match"` или `"include"`         |
| `globs`             | Шаблоны glob пути из frontmatter `paths:` файла, если есть. Присутствует только для загрузок `path_glob_match` |
| `trigger_file_path` | Путь к файлу, доступ к которому вызвал эту загрузку, для ленивых загрузок                                      |
| `parent_file_path`  | Путь к родительскому файлу инструкций, который включил этот, для загрузок `include`                            |

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "permission_mode": "default",
  "hook_event_name": "InstructionsLoaded",
  "file_path": "/Users/my-project/CLAUDE.md",
  "memory_type": "Project",
  "load_reason": "session_start"
}
```

#### InstructionsLoaded decision control

Hooks InstructionsLoaded не имеют управления решением. Они не могут блокировать или изменять загрузку инструкций. Используйте это событие для аудита логирования, отслеживания соответствия или наблюдаемости.

### UserPromptSubmit

Запускается при отправке пользователем подсказки, перед обработкой Claude. Это позволяет вам добавлять дополнительный контекст на основе подсказки/разговора, проверять подсказки или блокировать определённые типы подсказок.

#### UserPromptSubmit input

В дополнение к [общим полям входа](#common-input-fields), hooks UserPromptSubmit получают поле `prompt`, содержащее текст, отправленный пользователем.

```json  theme={null}
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

Hooks `UserPromptSubmit` могут управлять тем, обрабатывается ли подсказка пользователя, и добавлять контекст. Доступны все [поля JSON выхода](#json-output).

Есть два способа добавить контекст к разговору при exit code 0:

* **Простой текст stdout**: любой текст, не являющийся JSON, написанный на stdout, добавляется как контекст
* **JSON с `additionalContext`**: используйте формат JSON ниже для большего управления. Поле `additionalContext` добавляется как контекст

Простой stdout показывается как выход hook в транскрипте. Поле `additionalContext` добавляется более дискретно.

Чтобы заблокировать подсказку, верните объект JSON с `decision`, установленным на `"block"`:

| Поле                | Описание                                                                                                                |
| :------------------ | :---------------------------------------------------------------------------------------------------------------------- |
| `decision`          | `"block"` предотвращает обработку подсказки и стирает её из контекста. Опустите, чтобы разрешить подсказке продолжаться |
| `reason`            | Показывается пользователю при `decision` равном `"block"`. Не добавляется в контекст                                    |
| `additionalContext` | Строка, добавляемая в контекст Claude                                                                                   |

```json  theme={null}
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

Запускается после того, как Claude создаёт параметры инструмента и перед обработкой вызова инструмента. Совпадает с именем инструмента: `Bash`, `Edit`, `Write`, `Read`, `Glob`, `Grep`, `Agent`, `WebFetch`, `WebSearch` и любые [имена MCP инструментов](#match-mcp-tools).

Используйте [PreToolUse decision control](#pretooluse-decision-control) для разрешения, отклонения или запроса разрешения на использование инструмента.

#### PreToolUse input

В дополнение к [общим полям входа](#common-input-fields), hooks PreToolUse получают `tool_name`, `tool_input` и `tool_use_id`. Поля `tool_input` зависят от инструмента:

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

Ищет содержимое файла с помощью регулярных выражений.

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

#### PreToolUse decision control

Hooks `PreToolUse` могут управлять тем, продолжается ли вызов инструмента. В отличие от других hooks, которые используют верхнеуровневое поле `decision`, PreToolUse возвращает своё решение внутри объекта `hookSpecificOutput`. Это даёт ему более богатое управление: три результата (разрешить, отклонить или спросить) плюс возможность изменить входные данные инструмента перед выполнением.

| Поле                       | Описание                                                                                                                                                           |
| :------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `permissionDecision`       | `"allow"` обходит систему разрешений, `"deny"` предотвращает вызов инструмента, `"ask"` предлагает пользователю подтвердить                                        |
| `permissionDecisionReason` | Для `"allow"` и `"ask"`, показывается пользователю, но не Claude. Для `"deny"`, показывается Claude                                                                |
| `updatedInput`             | Изменяет параметры входа инструмента перед выполнением. Объедините с `"allow"` для автоматического одобрения или `"ask"` для показа изменённого входа пользователю |
| `additionalContext`        | Строка, добавляемая в контекст Claude перед выполнением инструмента                                                                                                |

```json  theme={null}
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

<Note>
  PreToolUse ранее использовал верхнеуровневые поля `decision` и `reason`, но они устарели для этого события. Используйте `hookSpecificOutput.permissionDecision` и `hookSpecificOutput.permissionDecisionReason` вместо этого. Устаревшие значения `"approve"` и `"block"` отображаются на `"allow"` и `"deny"` соответственно. Другие события, такие как PostToolUse и Stop, продолжают использовать верхнеуровневые `decision` и `reason` как их текущий формат.
</Note>

### PermissionRequest

Запускается при показе пользователю диалога разрешения.
Используйте [PermissionRequest decision control](#permissionrequest-decision-control) для разрешения или отклонения от имени пользователя.

Совпадает с именем инструмента, те же значения, что и PreToolUse.

#### PermissionRequest input

Hooks PermissionRequest получают поля `tool_name` и `tool_input`, как hooks PreToolUse, но без `tool_use_id`. Опциональный массив `permission_suggestions` содержит параметры "всегда разрешить", которые пользователь обычно видит в диалоге разрешения. Разница в том, когда срабатывает hook: hooks PermissionRequest запускаются, когда диалог разрешения вот-вот будет показан пользователю, в то время как hooks PreToolUse запускаются перед выполнением инструмента независимо от статуса разрешения.

```json  theme={null}
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
    { "type": "toolAlwaysAllow", "tool": "Bash" }
  ]
}
```

#### PermissionRequest decision control

Hooks `PermissionRequest` могут разрешить или отклонить запросы разрешения. В дополнение к [полям JSON выхода](#json-output), доступным для всех hooks, ваш скрипт hook может вернуть объект `decision` с этими полями, специфичными для события:

| Поле                 | Описание                                                                                                                     |
| :------------------- | :--------------------------------------------------------------------------------------------------------------------------- |
| `behavior`           | `"allow"` предоставляет разрешение, `"deny"` отклоняет его                                                                   |
| `updatedInput`       | Только для `"allow"`: изменяет параметры входа инструмента перед выполнением                                                 |
| `updatedPermissions` | Только для `"allow"`: применяет обновления правил разрешения, эквивалентно выбору пользователем параметра "всегда разрешить" |
| `message`            | Только для `"deny"`: говорит Claude, почему разрешение было отклонено                                                        |
| `interrupt`          | Только для `"deny"`: если `true`, останавливает Claude                                                                       |

```json  theme={null}
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

### PostToolUse

Запускается сразу после успешного завершения инструмента.

Совпадает с именем инструмента, те же значения, что и PreToolUse.

#### PostToolUse input

Hooks `PostToolUse` срабатывают после того, как инструмент уже выполнился успешно. Входные данные включают как `tool_input`, аргументы, отправленные инструменту, так и `tool_response`, результат, который он вернул. Точная схема для обоих зависит от инструмента.

```json  theme={null}
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

Hooks `PostToolUse` могут предоставить обратную связь Claude после выполнения инструмента. В дополнение к [полям JSON выхода](#json-output), доступным для всех hooks, ваш скрипт hook может вернуть эти поля, специфичные для события:

| Поле                   | Описание                                                                                              |
| :--------------------- | :---------------------------------------------------------------------------------------------------- |
| `decision`             | `"block"` предлагает Claude с `reason`. Опустите, чтобы разрешить действию продолжаться               |
| `reason`               | Объяснение, показываемое Claude при `decision` равном `"block"`                                       |
| `additionalContext`    | Дополнительный контекст для Claude для рассмотрения                                                   |
| `updatedMCPToolOutput` | Только для [MCP инструментов](#match-mcp-tools): заменяет выход инструмента предоставленным значением |

```json  theme={null}
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

Hooks PostToolUseFailure получают те же поля `tool_name` и `tool_input`, что и PostToolUse, вместе с информацией об ошибке как верхнеуровневые поля:

```json  theme={null}
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

Hooks `PostToolUseFailure` могут предоставить контекст Claude после сбоя инструмента. В дополнение к [полям JSON выхода](#json-output), доступным для всех hooks, ваш скрипт hook может вернуть эти поля, специфичные для события:

| Поле                | Описание                                                             |
| :------------------ | :------------------------------------------------------------------- |
| `additionalContext` | Дополнительный контекст для Claude для рассмотрения наряду с ошибкой |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

### Notification

Запускается при отправке Claude Code уведомлений. Совпадает с типом уведомления: `permission_prompt`, `idle_prompt`, `auth_success`, `elicitation_dialog`. Опустите matcher для запуска hooks для всех типов уведомлений.

Используйте отдельные matchers для запуска разных обработчиков в зависимости от типа уведомления. Эта конфигурация запускает скрипт оповещения, специфичный для разрешения, когда Claude нуждается в одобрении разрешения, и другое уведомление, когда Claude был неактивен:

```json  theme={null}
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

В дополнение к [общим полям входа](#common-input-fields), hooks Notification получают `message` с текстом уведомления, опциональный `title` и `notification_type`, указывающий, какой тип сработал.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission to use Bash",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

Hooks Notification не могут блокировать или изменять уведомления. В дополнение к [полям JSON выхода](#json-output), доступным для всех hooks, вы можете вернуть `additionalContext` для добавления контекста к разговору:

| Поле                | Описание                              |
| :------------------ | :------------------------------------ |
| `additionalContext` | Строка, добавляемая в контекст Claude |

### SubagentStart

Запускается при порождении subagent Claude Code через инструмент Agent. Поддерживает matchers для фильтрации по имени типа агента (встроенные агенты, такие как `Bash`, `Explore`, `Plan`, или пользовательские имена агентов из `.claude/agents/`).

#### SubagentStart input

В дополнение к [общим полям входа](#common-input-fields), hooks SubagentStart получают `agent_id` с уникальным идентификатором для subagent и `agent_type` с именем агента (встроенные агенты, такие как `"Bash"`, `"Explore"`, `"Plan"`, или пользовательские имена агентов).

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

Hooks SubagentStart не могут блокировать создание subagent, но они могут внедрить контекст в subagent. В дополнение к [полям JSON выхода](#json-output), доступным для всех hooks, вы можете вернуть:

| Поле                | Описание                                |
| :------------------ | :-------------------------------------- |
| `additionalContext` | Строка, добавляемая в контекст subagent |

```json  theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

### SubagentStop

Запускается при завершении ответа subagent Claude Code. Совпадает с типом агента, те же значения, что и SubagentStart.

#### SubagentStop input

В дополнение к [общим полям входа](#common-input-fields), hooks SubagentStop получают `stop_hook_active`, `agent_id`, `agent_type`, `agent_transcript_path` и `last_assistant_message`. Поле `agent_type` — это значение, используемое для фильтрации matcher. `transcript_path` — это транскрипт основного сеанса, в то время как `agent_transcript_path` — это собственный транскрипт subagent, хранящийся в вложенной папке `subagents/`. Поле `last_assistant_message` содержит текстовое содержимое финального ответа subagent, поэтому hooks могут получить доступ к нему без анализа файла транскрипта.

```json  theme={null}
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

Hooks SubagentStop используют тот же формат управления решением, что и [hooks Stop](#stop-decision-control).

### Stop

Запускается при завершении ответа основного агента Claude Code. Не запускается, если остановка произошла из-за прерывания пользователя.

#### Stop input

В дополнение к [общим полям входа](#common-input-fields), hooks Stop получают `stop_hook_active` и `last_assistant_message`. Поле `stop_hook_active` равно `true`, когда Claude Code уже продолжает работу в результате hook stop. Проверьте это значение или обработайте транскрипт, чтобы предотвратить бесконечное выполнение Claude Code. Поле `last_assistant_message` содержит текстовое содержимое финального ответа Claude, поэтому hooks могут получить доступ к нему без анализа файла транскрипта.

```json  theme={null}
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

Hooks `Stop` и `SubagentStop` могут управлять тем, продолжает ли Claude работу. В дополнение к [полям JSON выхода](#json-output), доступным для всех hooks, ваш скрипт hook может вернуть эти поля, специфичные для события:

| Поле       | Описание                                                                                |
| :--------- | :-------------------------------------------------------------------------------------- |
| `decision` | `"block"` предотвращает остановку Claude. Опустите, чтобы разрешить Claude остановиться |
| `reason`   | Требуется при `decision` равном `"block"`. Говорит Claude, почему оно должно продолжить |

```json  theme={null}
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

### TeammateIdle

Запускается, когда товарищ [agent team](/ru/agent-teams) вот-вот перейдёт в режим ожидания после завершения своего хода. Используйте это для обеспечения качественных ворот перед остановкой работы товарища, такие как требование прохождения проверок lint или проверка существования выходных файлов.

Когда hook `TeammateIdle` выходит с кодом 2, товарищ получает сообщение stderr как обратную связь и продолжает работать вместо перехода в режим ожидания. Чтобы полностью остановить товарища вместо его повторного запуска, верните JSON с `{"continue": false, "stopReason": "..."}`. Hooks TeammateIdle не поддерживают matchers и срабатывают при каждом вхождении.

#### TeammateIdle input

В дополнение к [общим полям входа](#common-input-fields), hooks TeammateIdle получают `teammate_name` и `team_name`.

```json  theme={null}
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

| Поле            | Описание                                                |
| :-------------- | :------------------------------------------------------ |
| `teammate_name` | Имя товарища, который вот-вот перейдёт в режим ожидания |
| `team_name`     | Имя команды                                             |

#### TeammateIdle decision control

Hooks TeammateIdle поддерживают два способа управления поведением товарища:

* **Exit code 2**: товарищ получает сообщение stderr как обратную связь и продолжает работать вместо перехода в режим ожидания.
* **JSON `{"continue": false, "stopReason": "..."}`**: полностью останавливает товарища, совпадая с поведением hook `Stop`. `stopReason` показывается пользователю.

Этот пример проверяет, что артефакт сборки существует перед разрешением товарищу перейти в режим ожидания:

```bash  theme={null}
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2
fi

exit 0
```

### TaskCompleted

Запускается при отметке задачи как завершённой. Это срабатывает в двух ситуациях: когда любой агент явно отмечает задачу как завершённую через инструмент TaskUpdate, или когда товарищ [agent team](/ru/agent-teams) завершает свой ход с незавершёнными задачами. Используйте это для обеспечения критериев завершения, таких как прохождение тестов или проверок lint, перед закрытием задачи.

Когда hook `TaskCompleted` выходит с кодом 2, задача не отмечается как завершённая и сообщение stderr передаётся обратно модели как обратная связь. Чтобы полностью остановить товарища вместо его повторного запуска, верните JSON с `{"continue": false, "stopReason": "..."}`. Hooks TaskCompleted не поддерживают matchers и срабатывают при каждом вхождении.

#### TaskCompleted input

В дополнение к [общим полям входа](#common-input-fields), hooks TaskCompleted получают `task_id`, `task_subject` и опционально `task_description`, `teammate_name` и `team_name`.

```json  theme={null}
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

Hooks TaskCompleted поддерживают два способа управления завершением задачи:

* **Exit code 2**: задача не отмечается как завершённая и сообщение stderr передаётся обратно модели как обратная связь.
* **JSON `{"continue": false, "stopReason": "..."}`**: полностью останавливает товарища, совпадая с поведением hook `Stop`. `stopReason` показывается пользователю.

Этот пример запускает тесты и блокирует завершение задачи, если они не пройдены:

```bash  theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

# Запустите набор тестов
if ! npm test 2>&1; then
  echo "Tests not passing. Fix failing tests before completing: $TASK_SUBJECT" >&2
  exit 2
fi

exit 0
```

### ConfigChange

Запускается при изменении файла конфигурации во время сеанса. Используйте это для аудита изменений параметров, обеспечения политик безопасности или блокировки несанкционированных изменений файлов конфигурации.

Hooks ConfigChange срабатывают для изменений файлов параметров, управляемых параметров политики и файлов skills. Поле `source` во входных данных говорит вам, какой тип конфигурации изменился, и опциональное поле `file_path` предоставляет путь к изменённому файлу.

Matcher фильтрует по источнику конфигурации:

| Matcher            | Когда он срабатывает                      |
| :----------------- | :---------------------------------------- |
| `user_settings`    | `~/.claude/settings.json` изменяется      |
| `project_settings` | `.claude/settings.json` изменяется        |
| `local_settings`   | `.claude/settings.local.json` изменяется  |
| `policy_settings`  | Управляемые параметры политики изменяются |
| `skills`           | Файл skill в `.claude/skills/` изменяется |

Этот пример логирует все изменения конфигурации для аудита безопасности:

```json  theme={null}
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

В дополнение к [общим полям входа](#common-input-fields), hooks ConfigChange получают `source` и опционально `file_path`. Поле `source` указывает, какой тип конфигурации изменился, и `file_path` предоставляет путь к конкретному изменённому файлу.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "ConfigChange",
  "source": "project_settings",
  "file_path": "/Users/.../my-project/.claude/settings.json"
}
```

#### ConfigChange decision control

Hooks ConfigChange могут блокировать применение изменений конфигурации. Используйте exit code 2 или JSON `decision` для предотвращения изменения. При блокировке новые параметры не применяются к работающему сеансу.

| Поле       | Описание                                                                                       |
| :--------- | :--------------------------------------------------------------------------------------------- |
| `decision` | `"block"` предотвращает применение изменения конфигурации. Опустите, чтобы разрешить изменение |
| `reason`   | Объяснение, показываемое пользователю при `decision` равном `"block"`                          |

```json  theme={null}
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

Изменения `policy_settings` не могут быть заблокированы. Hooks всё ещё срабатывают для источников `policy_settings`, поэтому вы можете использовать их для аудита логирования, но любое решение блокировки игнорируется. Это гарантирует, что управляемые предприятием параметры всегда вступают в силу.

### WorktreeCreate

Когда вы запускаете `claude --worktree` или [subagent использует `isolation: "worktree"`](/ru/sub-agents#choose-the-subagent-scope), Claude Code создаёт изолированную рабочую копию, используя `git worktree`. Если вы настроите hook WorktreeCreate, он заменяет поведение git по умолчанию, позволяя вам использовать другую систему контроля версий, такую как SVN, Perforce или Mercurial.

Hook должен вывести абсолютный путь к созданному каталогу worktree на stdout. Claude Code использует этот путь как рабочий каталог для изолированного сеанса.

Этот пример создаёт рабочую копию SVN и выводит путь для использования Claude Code. Замените URL репозитория на свой:

```json  theme={null}
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

Hook читает `name` worktree из JSON входа на stdin, проверяет свежую копию в новый каталог и выводит путь каталога. `echo` на последней строке — это то, что Claude Code читает как путь worktree. Перенаправьте любой другой выход на stderr, чтобы он не мешал пути.

#### WorktreeCreate input

В дополнение к [общим полям входа](#common-input-fields), hooks WorktreeCreate получают поле `name`. Это идентификатор slug для нового worktree, либо указанный пользователем, либо автоматически сгенерированный (например, `bold-oak-a3f2`).

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

#### WorktreeCreate output

Hook должен вывести абсолютный путь к созданному каталогу worktree на stdout. Если hook не удаётся или не производит выход, создание worktree не удаётся с ошибкой.

Hooks WorktreeCreate не используют стандартную модель решения разрешить/заблокировать. Вместо этого успех или сбой hook определяет результат. Поддерживаются только hooks `type: "command"`.

### WorktreeRemove

Противоположность очистки [WorktreeCreate](#worktreecreate). Этот hook срабатывает при удалении worktree, либо когда вы выходите из сеанса `--worktree` и выбираете его удаление, либо когда subagent с `isolation: "worktree"` завершается. Для git-based worktrees Claude обрабатывает очистку автоматически с помощью `git worktree remove`. Если вы настроили hook WorktreeCreate для системы контроля версий, отличной от git, свяжите его с hook WorktreeRemove для обработки очистки. Без него каталог worktree остаётся на диске.

Claude Code передаёт путь, который WorktreeCreate вывел на stdout, как `worktree_path` во входных данных hook. Этот пример читает этот путь и удаляет каталог:

```json  theme={null}
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

В дополнение к [общим полям входа](#common-input-fields), hooks WorktreeRemove получают поле `worktree_path`, которое является абсолютным путём к удаляемому worktree.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

Hooks WorktreeRemove не имеют управления решением. Они не могут блокировать удаление worktree, но могут выполнять задачи очистки, такие как удаление состояния контроля версий или архивирование изменений. Сбои hook логируются только в режиме отладки. Поддерживаются только hooks `type: "command"`.

### PreCompact

Запускается перед тем, как Claude Code вот-вот запустит операцию compact.

Значение matcher указывает, было ли компактирование запущено вручную или автоматически:

| Matcher  | Когда он срабатывает                      |
| :------- | :---------------------------------------- |
| `manual` | `/compact`                                |
| `auto`   | Auto-compact когда контекстное окно полно |

#### PreCompact input

В дополнение к [общим полям входа](#common-input-fields), hooks PreCompact получают `trigger` и `custom_instructions`. Для `manual`, `custom_instructions` содержит то, что пользователь передаёт в `/compact`. Для `auto`, `custom_instructions` пусто.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": ""
}
```

### SessionEnd

Запускается при завершении сеанса Claude Code. Полезно для задач очистки, логирования статистики сеанса или сохранения состояния сеанса. Поддерживает matchers для фильтрации по причине выхода.

Поле `reason` во входных данных hook указывает, почему закончился сеанс:

| Причина                       | Описание                                          |
| :---------------------------- | :------------------------------------------------ |
| `clear`                       | Сеанс очищен с помощью команды `/clear`           |
| `logout`                      | Пользователь вышел                                |
| `prompt_input_exit`           | Пользователь вышел, пока был виден ввод подсказки |
| `bypass_permissions_disabled` | Режим обхода разрешений был отключен              |
| `other`                       | Другие причины выхода                             |

#### SessionEnd input

В дополнение к [общим полям входа](#common-input-fields), hooks SessionEnd получают поле `reason`, указывающее, почему закончился сеанс. См. таблицу [reason](#sessionend) выше для всех значений.

```json  theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

Hooks SessionEnd не имеют управления решением. Они не могут блокировать завершение сеанса, но могут выполнять задачи очистки.

## Prompt-based hooks

В дополнение к command и HTTP hooks, Claude Code поддерживает prompt-based hooks (`type: "prompt"`), которые используют LLM для оценки разрешения или блокировки действия, и agent hooks (`type: "agent"`), которые порождают агентского верификатора с доступом к инструментам. Не все события поддерживают каждый тип hook.

События, которые поддерживают все четыре типа hook (`command`, `http`, `prompt` и `agent`):

* `PermissionRequest`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `UserPromptSubmit`

События, которые поддерживают только hooks `type: "command"`:

* `ConfigChange`
* `InstructionsLoaded`
* `Notification`
* `PreCompact`
* `SessionEnd`
* `SessionStart`
* `SubagentStart`
* `TeammateIdle`
* `WorktreeCreate`
* `WorktreeRemove`

### How prompt-based hooks work

Вместо выполнения команды Bash, prompt-based hooks:

1. Отправляют входные данные hook и вашу подсказку модели Claude, Haiku по умолчанию
2. LLM отвечает структурированным JSON, содержащим решение
3. Claude Code автоматически обрабатывает решение

### Prompt hook configuration

Установите `type` на `"prompt"` и предоставьте строку `prompt` вместо `command`. Используйте заполнитель `$ARGUMENTS` для внедрения данных JSON входа hook в текст вашей подсказки. Claude Code отправляет объединённую подсказку и входные данные быстрой модели Claude, которая возвращает решение JSON.

Этот hook `Stop` просит LLM оценить, должен ли Claude остановиться перед разрешением Claude закончить:

```json  theme={null}
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

```json  theme={null}
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

```json  theme={null}
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

Agent-based hooks (`type: "agent"`) похожи на prompt-based hooks, но с многооборотным доступом к инструментам. Вместо одного вызова LLM, hook agent порождает subagent, который может читать файлы, искать код и проверять кодовую базу для проверки условий. Agent hooks поддерживают те же события, что и prompt-based hooks.

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

## Run hooks in the background

По умолчанию hooks блокируют выполнение Claude до их завершения. Для долгоживущих задач, таких как развёртывания, наборы тестов или вызовы внешних API, установите `"async": true` для запуска hook в фоне, пока Claude продолжает работать. Асинхронные hooks не могут блокировать или управлять поведением Claude: поля ответа, такие как `decision`, `permissionDecision` и `continue`, не имеют эффекта, потому что действие, которое они контролировали, уже завершено.

### Configure an async hook

Добавьте `"async": true` к конфигурации command hook для запуска его в фоне без блокировки Claude. Это поле доступно только на hooks `type: "command"`.

Этот hook запускает скрипт тестирования после каждого вызова инструмента `Write`. Claude продолжает работать немедленно, пока `run-tests.sh` выполняется до 120 секунд. Когда скрипт завершается, его выход доставляется на следующий ход разговора:

```json  theme={null}
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

Поле `timeout` устанавливает максимальное время в секундах для фонового процесса. Если не указано, асинхронные hooks используют то же значение по умолчанию 10 минут, что и синхронные hooks.

### How async hooks execute

Когда срабатывает асинхронный hook, Claude Code запускает процесс hook и немедленно продолжает без ожидания его завершения. Hook получает те же JSON входные данные через stdin, что и синхронный hook.

После выхода фонового процесса, если hook произвёл JSON ответ с полем `systemMessage` или `additionalContext`, это содержимое доставляется Claude как контекст на следующем ходу разговора.

### Example: run tests after file changes

Этот hook запускает набор тестов в фоне всякий раз, когда Claude пишет файл, затем сообщает результаты обратно Claude при завершении тестов. Сохраните этот скрипт в `.claude/hooks/run-tests-async.sh` в вашем проекте и сделайте его исполняемым с помощью `chmod +x`:

```bash  theme={null}
#!/bin/bash
# run-tests-async.sh

# Читает входные данные hook из stdin
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Запускайте тесты только для исходных файлов
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# Запустите тесты и сообщите результаты через systemMessage
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  echo "{\"systemMessage\": \"Tests passed after editing $FILE_PATH\"}"
else
  echo "{\"systemMessage\": \"Tests failed after editing $FILE_PATH: $RESULT\"}"
fi
```

Затем добавьте эту конфигурацию в `.claude/settings.json` в корне вашего проекта. Флаг `async: true` позволяет Claude продолжать работу, пока тесты запускаются:

```json  theme={null}
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
* Асинхронные hooks не могут блокировать вызовы инструментов или возвращать решения. К моменту завершения hook вызывающее действие уже произошло.
* Выход hook доставляется на следующем ходу разговора. Если сеанс неактивен, ответ ждёт до следующего взаимодействия пользователя.
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

Запустите `claude --debug` для просмотра деталей выполнения hook, включая какие hooks совпадали, их коды выхода и выход. Переключайте подробный режим с помощью `Ctrl+O` для просмотра прогресса hook в транскрипте.

```text  theme={null}
[DEBUG] Executing hooks for PostToolUse:Write
[DEBUG] Getting matching hook commands for PostToolUse with query: Write
[DEBUG] Found 1 hook matchers in settings
[DEBUG] Matched 1 hooks for query "Write"
[DEBUG] Found 1 hook commands to execute
[DEBUG] Executing hook command: <Your command> with timeout 600000ms
[DEBUG] Hook command completed with status 0: <Your stdout>
```

Для устранения неполадок распространённых проблем, таких как hooks, которые не срабатывают, бесконечные циклы Stop hook или ошибки конфигурации, см. [Limitations and troubleshooting](/ru/hooks-guide#limitations-and-troubleshooting) в руководстве.
