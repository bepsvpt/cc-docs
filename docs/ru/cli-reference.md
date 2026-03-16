> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Справочник CLI

> Полный справочник по интерфейсу командной строки Claude Code, включая команды и флаги.

## Команды CLI

Вы можете запускать сеансы, передавать содержимое, возобновлять беседы и управлять обновлениями с помощью этих команд:

| Команда                         | Описание                                                                                                                                                                                            | Пример                                             |
| :------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------- |
| `claude`                        | Запустить интерактивный сеанс                                                                                                                                                                       | `claude`                                           |
| `claude "query"`                | Запустить интерактивный сеанс с начальным запросом                                                                                                                                                  | `claude "explain this project"`                    |
| `claude -p "query"`             | Запрос через SDK, затем выход                                                                                                                                                                       | `claude -p "explain this function"`                |
| `cat file \| claude -p "query"` | Обработка переданного содержимого                                                                                                                                                                   | `cat logs.txt \| claude -p "explain"`              |
| `claude -c`                     | Продолжить последнюю беседу в текущем каталоге                                                                                                                                                      | `claude -c`                                        |
| `claude -c -p "query"`          | Продолжить через SDK                                                                                                                                                                                | `claude -c -p "Check for type errors"`             |
| `claude -r "<session>" "query"` | Возобновить сеанс по ID или имени                                                                                                                                                                   | `claude -r "auth-refactor" "Finish this PR"`       |
| `claude update`                 | Обновить до последней версии                                                                                                                                                                        | `claude update`                                    |
| `claude auth login`             | Войти в свою учетную запись Anthropic. Используйте `--email` для предварительного заполнения адреса электронной почты и `--sso` для принудительной аутентификации SSO                               | `claude auth login --email user@example.com --sso` |
| `claude auth logout`            | Выйти из своей учетной записи Anthropic                                                                                                                                                             | `claude auth logout`                               |
| `claude auth status`            | Показать статус аутентификации в формате JSON. Используйте `--text` для удобочитаемого вывода. Выходит с кодом 0, если вы вошли, 1, если нет                                                        | `claude auth status`                               |
| `claude agents`                 | Список всех настроенных [subagents](/ru/sub-agents), сгруппированных по источнику                                                                                                                   | `claude agents`                                    |
| `claude mcp`                    | Настроить серверы Model Context Protocol (MCP)                                                                                                                                                      | См. [документацию Claude Code MCP](/ru/mcp).       |
| `claude remote-control`         | Запустить сеанс [Remote Control](/ru/remote-control) для управления Claude Code из Claude.ai или приложения Claude во время локального запуска. См. [Remote Control](/ru/remote-control) для флагов | `claude remote-control`                            |

## Флаги CLI

Настройте поведение Claude Code с помощью этих флагов командной строки:

| Флаг                                   | Описание                                                                                                                                                                                                                                | Пример                                                                                             |
| :------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `--add-dir`                            | Добавить дополнительные рабочие каталоги для доступа Claude (проверяет, что каждый путь существует как каталог)                                                                                                                         | `claude --add-dir ../apps ../lib`                                                                  |
| `--agent`                              | Указать агента для текущего сеанса (переопределяет параметр `agent`)                                                                                                                                                                    | `claude --agent my-custom-agent`                                                                   |
| `--agents`                             | Определить пользовательские [subagents](/ru/sub-agents) динамически через JSON (см. ниже формат)                                                                                                                                        | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allow-dangerously-skip-permissions` | Включить обход разрешений как опцию без немедленной активации. Позволяет компоновать с `--permission-mode` (используйте с осторожностью)                                                                                                | `claude --permission-mode plan --allow-dangerously-skip-permissions`                               |
| `--allowedTools`                       | Инструменты, которые выполняются без запроса разрешения. См. [синтаксис правила разрешения](/ru/settings#permission-rule-syntax) для сопоставления шаблонов. Чтобы ограничить доступные инструменты, используйте `--tools` вместо этого | `"Bash(git log *)" "Bash(git diff *)" "Read"`                                                      |
| `--append-system-prompt`               | Добавить пользовательский текст в конец системного приглашения по умолчанию                                                                                                                                                             | `claude --append-system-prompt "Always use TypeScript"`                                            |
| `--append-system-prompt-file`          | Загрузить дополнительный текст системного приглашения из файла и добавить к приглашению по умолчанию                                                                                                                                    | `claude --append-system-prompt-file ./extra-rules.txt`                                             |
| `--betas`                              | Заголовки бета-версии для включения в запросы API (только пользователи API ключей)                                                                                                                                                      | `claude --betas interleaved-thinking`                                                              |
| `--chrome`                             | Включить [интеграцию браузера Chrome](/ru/chrome) для веб-автоматизации и тестирования                                                                                                                                                  | `claude --chrome`                                                                                  |
| `--continue`, `-c`                     | Загрузить последнюю беседу в текущем каталоге                                                                                                                                                                                           | `claude --continue`                                                                                |
| `--dangerously-skip-permissions`       | Пропустить все запросы разрешения (используйте с осторожностью)                                                                                                                                                                         | `claude --dangerously-skip-permissions`                                                            |
| `--debug`                              | Включить режим отладки с дополнительной фильтрацией категорий (например, `"api,hooks"` или `"!statsig,!file"`)                                                                                                                          | `claude --debug "api,mcp"`                                                                         |
| `--disable-slash-commands`             | Отключить все skills и команды для этого сеанса                                                                                                                                                                                         | `claude --disable-slash-commands`                                                                  |
| `--disallowedTools`                    | Инструменты, которые удаляются из контекста модели и не могут быть использованы                                                                                                                                                         | `"Bash(git log *)" "Bash(git diff *)" "Edit"`                                                      |
| `--fallback-model`                     | Включить автоматический переход на указанную модель, когда модель по умолчанию перегружена (только режим печати)                                                                                                                        | `claude -p --fallback-model sonnet "query"`                                                        |
| `--fork-session`                       | При возобновлении создать новый ID сеанса вместо повторного использования исходного (используйте с `--resume` или `--continue`)                                                                                                         | `claude --resume abc123 --fork-session`                                                            |
| `--from-pr`                            | Возобновить сеансы, связанные с конкретным PR GitHub. Принимает номер PR или URL. Сеансы автоматически связываются при создании через `gh pr create`                                                                                    | `claude --from-pr 123`                                                                             |
| `--ide`                                | Автоматически подключиться к IDE при запуске, если доступна ровно одна действительная IDE                                                                                                                                               | `claude --ide`                                                                                     |
| `--init`                               | Запустить hooks инициализации и запустить интерактивный режим                                                                                                                                                                           | `claude --init`                                                                                    |
| `--init-only`                          | Запустить hooks инициализации и выход (без интерактивного сеанса)                                                                                                                                                                       | `claude --init-only`                                                                               |
| `--include-partial-messages`           | Включить частичные события потока в вывод (требует `--print` и `--output-format=stream-json`)                                                                                                                                           | `claude -p --output-format stream-json --include-partial-messages "query"`                         |
| `--input-format`                       | Указать формат входных данных для режима печати (опции: `text`, `stream-json`)                                                                                                                                                          | `claude -p --output-format json --input-format stream-json`                                        |
| `--json-schema`                        | Получить проверенный вывод JSON, соответствующий JSON Schema после завершения рабочего процесса агента (только режим печати, см. [структурированные выходы](https://platform.claude.com/docs/en/agent-sdk/structured-outputs))          | `claude -p --json-schema '{"type":"object","properties":{...}}' "query"`                           |
| `--maintenance`                        | Запустить hooks обслуживания и выход                                                                                                                                                                                                    | `claude --maintenance`                                                                             |
| `--max-budget-usd`                     | Максимальная сумма в долларах для расходования на вызовы API перед остановкой (только режим печати)                                                                                                                                     | `claude -p --max-budget-usd 5.00 "query"`                                                          |
| `--max-turns`                          | Ограничить количество агентских ходов (только режим печати). Выходит с ошибкой при достижении лимита. По умолчанию нет лимита                                                                                                           | `claude -p --max-turns 3 "query"`                                                                  |
| `--mcp-config`                         | Загрузить MCP серверы из JSON файлов или строк (разделены пробелом)                                                                                                                                                                     | `claude --mcp-config ./mcp.json`                                                                   |
| `--model`                              | Установить модель для текущего сеанса с псевдонимом для последней модели (`sonnet` или `opus`) или полным именем модели                                                                                                                 | `claude --model claude-sonnet-4-6`                                                                 |
| `--no-chrome`                          | Отключить [интеграцию браузера Chrome](/ru/chrome) для этого сеанса                                                                                                                                                                     | `claude --no-chrome`                                                                               |
| `--no-session-persistence`             | Отключить сохранение сеанса, чтобы сеансы не сохранялись на диск и не могли быть возобновлены (только режим печати)                                                                                                                     | `claude -p --no-session-persistence "query"`                                                       |
| `--output-format`                      | Указать формат вывода для режима печати (опции: `text`, `json`, `stream-json`)                                                                                                                                                          | `claude -p "query" --output-format json`                                                           |
| `--permission-mode`                    | Начать в указанном [режиме разрешения](/ru/permissions#permission-modes)                                                                                                                                                                | `claude --permission-mode plan`                                                                    |
| `--permission-prompt-tool`             | Указать инструмент MCP для обработки запросов разрешения в неинтерактивном режиме                                                                                                                                                       | `claude -p --permission-prompt-tool mcp_auth_tool "query"`                                         |
| `--plugin-dir`                         | Загрузить plugins из каталогов только для этого сеанса (повторяемо)                                                                                                                                                                     | `claude --plugin-dir ./my-plugins`                                                                 |
| `--print`, `-p`                        | Вывести ответ без интерактивного режима (см. [документацию Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) для деталей программного использования)                                                                   | `claude -p "query"`                                                                                |
| `--remote`                             | Создать новый [веб-сеанс](/ru/claude-code-on-the-web) на claude.ai с описанием предоставленной задачи                                                                                                                                   | `claude --remote "Fix the login bug"`                                                              |
| `--resume`, `-r`                       | Возобновить конкретный сеанс по ID или имени, или показать интерактивный выбор для выбора сеанса                                                                                                                                        | `claude --resume auth-refactor`                                                                    |
| `--session-id`                         | Использовать конкретный ID сеанса для беседы (должен быть действительным UUID)                                                                                                                                                          | `claude --session-id "550e8400-e29b-41d4-a716-446655440000"`                                       |
| `--setting-sources`                    | Разделенный запятыми список источников параметров для загрузки (`user`, `project`, `local`)                                                                                                                                             | `claude --setting-sources user,project`                                                            |
| `--settings`                           | Путь к файлу JSON параметров или строка JSON для загрузки дополнительных параметров                                                                                                                                                     | `claude --settings ./settings.json`                                                                |
| `--strict-mcp-config`                  | Использовать только MCP серверы из `--mcp-config`, игнорируя все остальные конфигурации MCP                                                                                                                                             | `claude --strict-mcp-config --mcp-config ./mcp.json`                                               |
| `--system-prompt`                      | Заменить весь системный запрос пользовательским текстом                                                                                                                                                                                 | `claude --system-prompt "You are a Python expert"`                                                 |
| `--system-prompt-file`                 | Загрузить системный запрос из файла, заменяя приглашение по умолчанию                                                                                                                                                                   | `claude --system-prompt-file ./custom-prompt.txt`                                                  |
| `--teleport`                           | Возобновить [веб-сеанс](/ru/claude-code-on-the-web) в вашем локальном терминале                                                                                                                                                         | `claude --teleport`                                                                                |
| `--teammate-mode`                      | Установить способ отображения товарищей по команде [agent team](/ru/agent-teams): `auto` (по умолчанию), `in-process` или `tmux`. См. [настройка agent teams](/ru/agent-teams#set-up-agent-teams)                                       | `claude --teammate-mode in-process`                                                                |
| `--tools`                              | Ограничить, какие встроенные инструменты может использовать Claude. Используйте `""` для отключения всех, `"default"` для всех или имена инструментов как `"Bash,Edit,Read"`                                                            | `claude --tools "Bash,Edit,Read"`                                                                  |
| `--verbose`                            | Включить подробное логирование, показывает полный вывод по ходам                                                                                                                                                                        | `claude --verbose`                                                                                 |
| `--version`, `-v`                      | Вывести номер версии                                                                                                                                                                                                                    | `claude -v`                                                                                        |
| `--worktree`, `-w`                     | Запустить Claude в изолированном [git worktree](/ru/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees) в `<repo>/.claude/worktrees/<name>`. Если имя не указано, оно генерируется автоматически                     | `claude -w feature-auth`                                                                           |

<Tip>
  Флаг `--output-format json` особенно полезен для написания скриптов и
  автоматизации, позволяя вам программно анализировать ответы Claude.
</Tip>

### Формат флага agents

Флаг `--agents` принимает объект JSON, который определяет один или несколько пользовательских subagents. Каждый subagent требует уникального имени (в качестве ключа) и объекта определения со следующими полями:

| Поле              | Обязательно | Описание                                                                                                                                                                                                                                                |
| :---------------- | :---------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `description`     | Да          | Описание на естественном языке того, когда должен быть вызван subagent                                                                                                                                                                                  |
| `prompt`          | Да          | Системный запрос, который направляет поведение subagent                                                                                                                                                                                                 |
| `tools`           | Нет         | Массив конкретных инструментов, которые может использовать subagent, например `["Read", "Edit", "Bash"]`. Если опущено, наследует все инструменты. Поддерживает синтаксис [`Agent(agent_type)`](/ru/sub-agents#restrict-which-subagents-can-be-spawned) |
| `disallowedTools` | Нет         | Массив имен инструментов для явного отрицания для этого subagent                                                                                                                                                                                        |
| `model`           | Нет         | Псевдоним модели для использования: `sonnet`, `opus`, `haiku` или `inherit`. Если опущено, по умолчанию `inherit`                                                                                                                                       |
| `skills`          | Нет         | Массив имен [skill](/ru/skills) для предварительной загрузки в контекст subagent                                                                                                                                                                        |
| `mcpServers`      | Нет         | Массив [MCP servers](/ru/mcp) для этого subagent. Каждая запись — это строка имени сервера или объект `{name: config}`                                                                                                                                  |
| `maxTurns`        | Нет         | Максимальное количество агентских ходов перед остановкой subagent                                                                                                                                                                                       |

Пример:

```bash  theme={null}
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

Для получения дополнительной информации о создании и использовании subagents см. [документацию subagents](/ru/sub-agents).

### Флаги системного запроса

Claude Code предоставляет четыре флага для настройки системного запроса. Все четыре работают как в интерактивном, так и в неинтерактивном режимах.

| Флаг                          | Поведение                                             | Вариант использования                                                         |
| :---------------------------- | :---------------------------------------------------- | :---------------------------------------------------------------------------- |
| `--system-prompt`             | **Заменяет** весь запрос по умолчанию                 | Полный контроль над поведением и инструкциями Claude                          |
| `--system-prompt-file`        | **Заменяет** содержимым файла                         | Загрузить запросы из файлов для воспроизводимости и контроля версий           |
| `--append-system-prompt`      | **Добавляет** к запросу по умолчанию                  | Добавить конкретные инструкции, сохраняя поведение Claude Code по умолчанию   |
| `--append-system-prompt-file` | **Добавляет** содержимое файла к запросу по умолчанию | Загрузить дополнительные инструкции из файлов, сохраняя значения по умолчанию |

**Когда использовать каждый:**

* **`--system-prompt`**: используйте, когда вам нужен полный контроль над системным запросом Claude. Это удаляет все инструкции Claude Code по умолчанию, давая вам чистый лист.
  ```bash  theme={null}
  claude --system-prompt "You are a Python expert who only writes type-annotated code"
  ```

* **`--system-prompt-file`**: используйте, когда вы хотите загрузить пользовательский запрос из файла, полезно для согласованности команды или контролируемых версией шаблонов запросов.
  ```bash  theme={null}
  claude --system-prompt-file ./prompts/code-review.txt
  ```

* **`--append-system-prompt`**: используйте, когда вы хотите добавить конкретные инструкции, сохраняя возможности Claude Code по умолчанию. Это самый безопасный вариант для большинства случаев использования.
  ```bash  theme={null}
  claude --append-system-prompt "Always use TypeScript and include JSDoc comments"
  ```

* **`--append-system-prompt-file`**: используйте, когда вы хотите добавить инструкции из файла, сохраняя значения Claude Code по умолчанию. Полезно для контролируемых версией дополнений.
  ```bash  theme={null}
  claude --append-system-prompt-file ./prompts/style-rules.txt
  ```

`--system-prompt` и `--system-prompt-file` являются взаимоисключающими. Флаги добавления можно использовать вместе с любым флагом замены.

Для большинства случаев использования рекомендуется `--append-system-prompt` или `--append-system-prompt-file`, так как они сохраняют встроенные возможности Claude Code, добавляя ваши пользовательские требования. Используйте `--system-prompt` или `--system-prompt-file` только когда вам нужен полный контроль над системным запросом.

## См. также

* [Расширение Chrome](/ru/chrome) - Веб-автоматизация и веб-тестирование
* [Интерактивный режим](/ru/interactive-mode) - Сочетания клавиш, режимы ввода и интерактивные функции
* [Руководство быстрого старта](/ru/quickstart) - Начало работы с Claude Code
* [Общие рабочие процессы](/ru/common-workflows) - Продвинутые рабочие процессы и шаблоны
* [Параметры](/ru/settings) - Опции конфигурации
* [Документация Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) - Программное использование и интеграции
