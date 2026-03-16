> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Создание пользовательских subagents

> Создавайте и используйте специализированные AI subagents в Claude Code для рабочих процессов, ориентированных на конкретные задачи, и улучшенного управления контекстом.

Subagents — это специализированные AI-помощники, которые обрабатывают определённые типы задач. Каждый subagent работает в собственном context window с пользовательским системным промптом, специфическим доступом к инструментам и независимыми разрешениями. Когда Claude встречает задачу, соответствующую описанию subagent, он делегирует её этому subagent, который работает независимо и возвращает результаты.

<Note>
  Если вам нужны несколько агентов, работающих параллельно и взаимодействующих друг с другом, см. [agent teams](/ru/agent-teams). Subagents работают в рамках одной сессии; agent teams координируют работу в отдельных сессиях.
</Note>

Subagents помогают вам:

* **Сохранять контекст**, отделяя исследование и реализацию от основного разговора
* **Применять ограничения**, ограничивая доступ subagent к определённым инструментам
* **Переиспользовать конфигурации** в разных проектах с помощью subagents уровня пользователя
* **Специализировать поведение** с помощью сфокусированных системных промптов для конкретных областей
* **Контролировать затраты**, маршрутизируя задачи на более быстрые и дешёвые модели, такие как Haiku

Claude использует описание каждого subagent для решения о делегировании задач. Когда вы создаёте subagent, напишите чёткое описание, чтобы Claude знал, когда его использовать.

Claude Code включает несколько встроенных subagents, таких как **Explore**, **Plan** и **general-purpose**. Вы также можете создавать пользовательские subagents для обработки конкретных задач. На этой странице рассматриваются [встроенные subagents](#built-in-subagents), [как создать свои собственные](#quickstart-create-your-first-subagent), [полные параметры конфигурации](#configure-subagents), [паттерны работы с subagents](#work-with-subagents) и [примеры subagents](#example-subagents).

## Встроенные subagents

Claude Code включает встроенные subagents, которые Claude автоматически использует при необходимости. Каждый наследует разрешения родительского разговора с дополнительными ограничениями на инструменты.

<Tabs>
  <Tab title="Explore">
    Быстрый агент, доступный только для чтения, оптимизированный для поиска и анализа кодовых баз.

    * **Model**: Haiku (быстрый, низкая задержка)
    * **Tools**: Инструменты только для чтения (запрещён доступ к инструментам Write и Edit)
    * **Purpose**: Обнаружение файлов, поиск кода, исследование кодовой базы

    Claude делегирует Explore, когда ему нужно искать или понимать кодовую базу без внесения изменений. Это сохраняет результаты исследования вне контекста основного разговора.

    При вызове Explore Claude указывает уровень тщательности: **quick** для целевых поисков, **medium** для сбалансированного исследования или **very thorough** для комплексного анализа.
  </Tab>

  <Tab title="Plan">
    Исследовательский агент, используемый во время [plan mode](/ru/common-workflows#use-plan-mode-for-safe-code-analysis) для сбора контекста перед представлением плана.

    * **Model**: Наследуется из основного разговора
    * **Tools**: Инструменты только для чтения (запрещён доступ к инструментам Write и Edit)
    * **Purpose**: Исследование кодовой базы для планирования

    Когда вы находитесь в режиме плана и Claude нужно понять вашу кодовую базу, он делегирует исследование subagent Plan. Это предотвращает бесконечное вложение (subagents не могут порождать других subagents), при этом собирая необходимый контекст.
  </Tab>

  <Tab title="General-purpose">
    Способный агент для сложных многошаговых задач, требующих как исследования, так и действия.

    * **Model**: Наследуется из основного разговора
    * **Tools**: Все инструменты
    * **Purpose**: Сложное исследование, многошаговые операции, модификация кода

    Claude делегирует general-purpose, когда задача требует как исследования, так и модификации, сложного рассуждения для интерпретации результатов или нескольких зависимых шагов.
  </Tab>

  <Tab title="Other">
    Claude Code включает дополнительные вспомогательные агенты для конкретных задач. Обычно они вызываются автоматически, поэтому вам не нужно использовать их напрямую.

    | Agent             | Model       | Когда Claude его использует                                      |
    | :---------------- | :---------- | :--------------------------------------------------------------- |
    | Bash              | Наследуется | Запуск команд терминала в отдельном контексте                    |
    | statusline-setup  | Sonnet      | Когда вы запускаете `/statusline` для настройки строки состояния |
    | Claude Code Guide | Haiku       | Когда вы задаёте вопросы о функциях Claude Code                  |
  </Tab>
</Tabs>

Помимо этих встроенных subagents, вы можете создавать свои собственные с пользовательскими промптами, ограничениями на инструменты, режимами разрешений, hooks и skills. В следующих разделах показано, как начать работу и настроить subagents.

## Quickstart: создание вашего первого subagent

Subagents определяются в файлах Markdown с YAML frontmatter. Вы можете [создавать их вручную](#write-subagent-files) или использовать команду `/agents`.

Это пошаговое руководство проведёт вас через создание subagent уровня пользователя с помощью команды `/agent`. Subagent проверяет код и предлагает улучшения для кодовой базы.

<Steps>
  <Step title="Откройте интерфейс subagents">
    В Claude Code запустите:

    ```text  theme={null}
    /agents
    ```
  </Step>

  <Step title="Создайте нового агента уровня пользователя">
    Выберите **Create new agent**, затем выберите **User-level**. Это сохранит subagent в `~/.claude/agents/`, чтобы он был доступен во всех ваших проектах.
  </Step>

  <Step title="Генерируйте с помощью Claude">
    Выберите **Generate with Claude**. При появлении запроса опишите subagent:

    ```text  theme={null}
    A code improvement agent that scans files and suggests improvements
    for readability, performance, and best practices. It should explain
    each issue, show the current code, and provide an improved version.
    ```

    Claude генерирует системный промпт и конфигурацию. Нажмите `e`, чтобы открыть его в редакторе, если вы хотите его настроить.
  </Step>

  <Step title="Выберите инструменты">
    Для проверяющего, доступного только для чтения, отмените выбор всего, кроме **Read-only tools**. Если вы оставите все инструменты выбранными, subagent наследует все инструменты, доступные основному разговору.
  </Step>

  <Step title="Выберите модель">
    Выберите, какую модель использует subagent. Для этого примера агента выберите **Sonnet**, который обеспечивает баланс между возможностями и скоростью анализа паттернов кода.
  </Step>

  <Step title="Выберите цвет">
    Выберите цвет фона для subagent. Это помогает вам определить, какой subagent работает в пользовательском интерфейсе.
  </Step>

  <Step title="Сохраните и попробуйте">
    Сохраните subagent. Он доступен немедленно (перезагрузка не требуется). Попробуйте:

    ```text  theme={null}
    Use the code-improver agent to suggest improvements in this project
    ```

    Claude делегирует вашему новому subagent, который сканирует кодовую базу и возвращает предложения по улучшению.
  </Step>
</Steps>

Теперь у вас есть subagent, который вы можете использовать в любом проекте на вашей машине для анализа кодовых баз и предложения улучшений.

Вы также можете создавать subagents вручную как файлы Markdown, определять их через флаги CLI или распространять их через плагины. В следующих разделах рассматриваются все параметры конфигурации.

## Настройка subagents

### Используйте команду /agents

Команда `/agents` предоставляет интерактивный интерфейс для управления subagents. Запустите `/agents` для:

* Просмотра всех доступных subagents (встроенные, пользовательские, проектные и из плагинов)
* Создания новых subagents с помощью управляемой установки или генерации Claude
* Редактирования существующей конфигурации subagent и доступа к инструментам
* Удаления пользовательских subagents
* Просмотра активных subagents при наличии дубликатов

Это рекомендуемый способ создания и управления subagents. Для ручного создания или автоматизации вы также можете добавлять файлы subagent напрямую.

Чтобы вывести список всех настроенных subagents из командной строки без запуска интерактивной сессии, запустите `claude agents`. Это показывает агентов, сгруппированных по источнику, и указывает, какие переопределены определениями с более высоким приоритетом.

### Выберите область subagent

Subagents — это файлы Markdown с YAML frontmatter. Сохраняйте их в разных местах в зависимости от области. Когда несколько subagents имеют одно и то же имя, выигрывает местоположение с более высоким приоритетом.

| Location                     | Scope              | Priority       | Как создать                            |
| :--------------------------- | :----------------- | :------------- | :------------------------------------- |
| `--agents` CLI flag          | Текущая сессия     | 1 (наивысший)  | Передайте JSON при запуске Claude Code |
| `.claude/agents/`            | Текущий проект     | 2              | Интерактивно или вручную               |
| `~/.claude/agents/`          | Все ваши проекты   | 3              | Интерактивно или вручную               |
| Директория `agents/` плагина | Где плагин включён | 4 (наименьший) | Установлено с [plugins](/ru/plugins)   |

**Project subagents** (`.claude/agents/`) идеальны для subagents, специфичных для кодовой базы. Проверьте их в систему контроля версий, чтобы ваша команда могла использовать и улучшать их совместно.

**User subagents** (`~/.claude/agents/`) — это личные subagents, доступные во всех ваших проектах.

**CLI-defined subagents** передаются как JSON при запуске Claude Code. Они существуют только для этой сессии и не сохраняются на диск, что делает их полезными для быстрого тестирования или скриптов автоматизации:

```bash  theme={null}
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  }
}'
```

Флаг `--agents` принимает JSON с теми же полями [frontmatter](#supported-frontmatter-fields), что и файловые subagents: `description`, `prompt`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills` и `memory`. Используйте `prompt` для системного промпта, эквивалентного телу markdown в файловых subagents. Полный формат JSON см. в [справочнике CLI](/ru/cli-reference#agents-flag-format).

**Plugin subagents** поступают из [плагинов](/ru/plugins), которые вы установили. Они появляются в `/agents` рядом с вашими пользовательскими subagents. Подробности о создании subagents плагинов см. в [справочнике компонентов плагинов](/ru/plugins-reference#agents).

### Напишите файлы subagent

Файлы subagent используют YAML frontmatter для конфигурации, за которым следует системный промпт в Markdown:

<Note>
  Subagents загружаются при запуске сессии. Если вы создаёте subagent путём ручного добавления файла, перезагрузите сессию или используйте `/agents` для немедленной загрузки.
</Note>

```markdown  theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

Frontmatter определяет метаданные и конфигурацию subagent. Тело становится системным промптом, который направляет поведение subagent. Subagents получают только этот системный промпт (плюс базовые детали окружения, такие как рабочая директория), а не полный системный промпт Claude Code.

#### Поддерживаемые поля frontmatter

Следующие поля можно использовать в YAML frontmatter. Требуются только `name` и `description`.

| Field             | Required | Description                                                                                                                                                                                                                                                                                               |
| :---------------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | Yes      | Уникальный идентификатор, использующий строчные буквы и дефисы                                                                                                                                                                                                                                            |
| `description`     | Yes      | Когда Claude должен делегировать этому subagent                                                                                                                                                                                                                                                           |
| `tools`           | No       | [Tools](#available-tools), которые может использовать subagent. Наследует все инструменты, если опущено                                                                                                                                                                                                   |
| `disallowedTools` | No       | Инструменты для запрета, удалённые из унаследованного или указанного списка                                                                                                                                                                                                                               |
| `model`           | No       | [Model](#choose-a-model) для использования: `sonnet`, `opus`, `haiku` или `inherit`. По умолчанию `inherit`                                                                                                                                                                                               |
| `permissionMode`  | No       | [Permission mode](#permission-modes): `default`, `acceptEdits`, `dontAsk`, `bypassPermissions` или `plan`                                                                                                                                                                                                 |
| `maxTurns`        | No       | Максимальное количество агентских ходов перед остановкой subagent                                                                                                                                                                                                                                         |
| `skills`          | No       | [Skills](/ru/skills) для загрузки в контекст subagent при запуске. Полное содержимое навыка внедряется, а не просто становится доступным для вызова. Subagents не наследуют skills из родительского разговора                                                                                             |
| `mcpServers`      | No       | [MCP servers](/ru/mcp), доступные этому subagent. Каждая запись — это либо имя сервера, ссылающееся на уже настроенный сервер (например, `"slack"`), либо встроенное определение с именем сервера в качестве ключа и полной [конфигурацией MCP server](/ru/mcp#configure-mcp-servers) в качестве значения |
| `hooks`           | No       | [Lifecycle hooks](#define-hooks-for-subagents), ограниченные этим subagent                                                                                                                                                                                                                                |
| `memory`          | No       | [Persistent memory scope](#enable-persistent-memory): `user`, `project` или `local`. Включает кросс-сессионное обучение                                                                                                                                                                                   |
| `background`      | No       | Установите на `true`, чтобы всегда запускать этот subagent как [background task](#run-subagents-in-foreground-or-background). По умолчанию: `false`                                                                                                                                                       |
| `isolation`       | No       | Установите на `worktree`, чтобы запустить subagent во временном [git worktree](/ru/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), предоставляя ему изолированную копию репозитория. Worktree автоматически очищается, если subagent не вносит изменения                          |

### Выберите модель

Поле `model` контролирует, какую [AI model](/ru/model-config) использует subagent:

* **Model alias**: Используйте один из доступных псевдонимов: `sonnet`, `opus` или `haiku`
* **inherit**: Используйте ту же модель, что и основной разговор
* **Omitted**: Если не указано, по умолчанию используется `inherit` (использует ту же модель, что и основной разговор)

### Контролируйте возможности subagent

Вы можете контролировать, что могут делать subagents, через доступ к инструментам, режимы разрешений и условные правила.

#### Доступные инструменты

Subagents могут использовать любой из [внутренних инструментов](/ru/settings#tools-available-to-claude) Claude Code. По умолчанию subagents наследуют все инструменты из основного разговора, включая MCP инструменты.

Чтобы ограничить инструменты, используйте поле `tools` (список разрешений) или поле `disallowedTools` (список запретов):

```yaml  theme={null}
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
disallowedTools: Write, Edit
---
```

#### Ограничьте, какие subagents могут быть порождены

Когда агент работает как основной поток с `claude --agent`, он может порождать subagents, используя инструмент Agent. Чтобы ограничить, какие типы subagents он может порождать, используйте синтаксис `Agent(agent_type)` в поле `tools`.

<Note>В версии 2.1.63 инструмент Task был переименован в Agent. Существующие ссылки `Task(...)` в настройках и определениях агентов по-прежнему работают как псевдонимы.</Note>

```yaml  theme={null}
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

Это список разрешений: только subagents `worker` и `researcher` могут быть порождены. Если агент попытается породить любой другой тип, запрос не удастся, и агент увидит только разрешённые типы в своём промпте. Чтобы заблокировать конкретные агенты, разрешив все остальные, используйте [`permissions.deny`](#disable-specific-subagents).

Чтобы разрешить порождение любого subagent без ограничений, используйте `Agent` без скобок:

```yaml  theme={null}
tools: Agent, Read, Bash
```

Если `Agent` полностью опущен из списка `tools`, агент не может порождать никакие subagents. Это ограничение применяется только к агентам, работающим как основной поток с `claude --agent`. Subagents не могут порождать других subagents, поэтому `Agent(agent_type)` не имеет эффекта в определениях subagent.

#### Режимы разрешений

Поле `permissionMode` контролирует, как subagent обрабатывает запросы разрешений. Subagents наследуют контекст разрешений из основного разговора, но могут переопределить режим.

| Mode                | Behavior                                                                                       |
| :------------------ | :--------------------------------------------------------------------------------------------- |
| `default`           | Стандартная проверка разрешений с запросами                                                    |
| `acceptEdits`       | Автоматически принимать редактирование файлов                                                  |
| `dontAsk`           | Автоматически отклонять запросы разрешений (явно разрешённые инструменты по-прежнему работают) |
| `bypassPermissions` | Пропустить все проверки разрешений                                                             |
| `plan`              | Режим плана (исследование только для чтения)                                                   |

<Warning>
  Используйте `bypassPermissions` с осторожностью. Это пропускает все проверки разрешений, позволяя subagent выполнять любую операцию без одобрения.
</Warning>

Если родитель использует `bypassPermissions`, это имеет приоритет и не может быть переопределено.

#### Предварительно загружайте skills в subagents

Используйте поле `skills` для внедрения содержимого skill в контекст subagent при запуске. Это даёт subagent знания в области без необходимости обнаруживать и загружать skills во время выполнения.

```yaml  theme={null}
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

Полное содержимое каждого skill внедряется в контекст subagent, а не просто становится доступным для вызова. Subagents не наследуют skills из родительского разговора; вы должны перечислить их явно.

<Note>
  Это противоположно [запуску skill в subagent](/ru/skills#run-skills-in-a-subagent). С `skills` в subagent, subagent контролирует системный промпт и загружает содержимое skill. С `context: fork` в skill, содержимое skill внедряется в агента, который вы указываете. Оба используют одну и ту же базовую систему.
</Note>

#### Включите постоянную память

Поле `memory` даёт subagent постоянную директорию, которая сохраняется между разговорами. Subagent использует эту директорию для накопления знаний с течением времени, таких как паттерны кодовой базы, инсайты отладки и архитектурные решения.

```yaml  theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

Выберите область в зависимости от того, насколько широко должна применяться память:

| Scope     | Location                                      | Используйте, когда                                                                                            |
| :-------- | :-------------------------------------------- | :------------------------------------------------------------------------------------------------------------ |
| `user`    | `~/.claude/agent-memory/<name-of-agent>/`     | subagent должен помнить обучение во всех проектах                                                             |
| `project` | `.claude/agent-memory/<name-of-agent>/`       | знания subagent специфичны для проекта и доступны для совместного использования через систему контроля версий |
| `local`   | `.claude/agent-memory-local/<name-of-agent>/` | знания subagent специфичны для проекта, но не должны проверяться в систему контроля версий                    |

Когда память включена:

* Системный промпт subagent включает инструкции по чтению и записи в директорию памяти.
* Системный промпт subagent также включает первые 200 строк `MEMORY.md` в директории памяти с инструкциями по курированию `MEMORY.md`, если она превышает 200 строк.
* Инструменты Read, Write и Edit автоматически включаются, чтобы subagent мог управлять своими файлами памяти.

##### Советы по постоянной памяти

* `user` — рекомендуемая область по умолчанию. Используйте `project` или `local`, когда знания subagent применимы только к конкретной кодовой базе.
* Попросите subagent проверить его память перед началом работы: "Review this PR, and check your memory for patterns you've seen before."
* Попросите subagent обновить его память после завершения задачи: "Now that you're done, save what you learned to your memory." С течением времени это создаёт базу знаний, которая делает subagent более эффективным.
* Включите инструкции по памяти непосредственно в файл markdown subagent, чтобы он активно поддерживал свою собственную базу знаний:

  ```markdown  theme={null}
  Update your agent memory as you discover codepaths, patterns, library
  locations, and key architectural decisions. This builds up institutional
  knowledge across conversations. Write concise notes about what you found
  and where.
  ```

#### Условные правила с hooks

Для более динамического контроля использования инструментов используйте hooks `PreToolUse` для проверки операций перед их выполнением. Это полезно, когда вам нужно разрешить некоторые операции инструмента, блокируя другие.

Этот пример создаёт subagent, который разрешает только запросы к базе данных только для чтения. Hook `PreToolUse` запускает скрипт, указанный в `command`, перед каждым выполнением команды Bash:

```yaml  theme={null}
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

Claude Code [передаёт входные данные hook как JSON](/ru/hooks#pretooluse-input) через stdin командам hook. Скрипт валидации читает этот JSON, извлекает команду Bash и [выходит с кодом 2](/ru/hooks#exit-code-2-behavior-per-event) для блокирования операций записи:

```bash  theme={null}
#!/bin/bash
# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

Полную схему входных данных см. в [Hook input](/ru/hooks#pretooluse-input) и коды выхода см. в [exit codes](/ru/hooks#exit-code-output).

#### Отключите конкретные subagents

Вы можете предотвратить использование Claude конкретных subagents, добавив их в массив `deny` в ваших [settings](/ru/settings#permission-settings). Используйте формат `Agent(subagent-name)`, где `subagent-name` соответствует полю name subagent.

```json  theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

Это работает как для встроенных, так и для пользовательских subagents. Вы также можете использовать флаг CLI `--disallowedTools`:

```bash  theme={null}
claude --disallowedTools "Agent(Explore)"
```

Подробнее см. в [документации Permissions](/ru/permissions#tool-specific-permission-rules).

### Определите hooks для subagents

Subagents могут определять [hooks](/ru/hooks), которые запускаются во время жизненного цикла subagent. Есть два способа настройки hooks:

1. **В frontmatter subagent**: Определите hooks, которые запускаются только во время активности этого subagent
2. **В `settings.json`**: Определите hooks, которые запускаются в основной сессии при запуске или остановке subagents

#### Hooks в frontmatter subagent

Определите hooks непосредственно в файле markdown subagent. Эти hooks запускаются только во время активности этого конкретного subagent и очищаются при его завершении.

Поддерживаются все [hook events](/ru/hooks#hook-events). Наиболее распространённые события для subagents:

| Event         | Matcher input   | Когда это срабатывает                                                           |
| :------------ | :-------------- | :------------------------------------------------------------------------------ |
| `PreToolUse`  | Имя инструмента | Перед использованием инструмента subagent                                       |
| `PostToolUse` | Имя инструмента | После использования инструмента subagent                                        |
| `Stop`        | (none)          | Когда subagent завершается (преобразуется в `SubagentStop` во время выполнения) |

Этот пример проверяет команды Bash с помощью hook `PreToolUse` и запускает linter после редактирования файлов с помощью `PostToolUse`:

```yaml  theme={null}
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh $TOOL_INPUT"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

Hooks `Stop` в frontmatter автоматически преобразуются в события `SubagentStop`.

#### Hooks уровня проекта для событий subagent

Настройте hooks в `settings.json`, которые реагируют на события жизненного цикла subagent в основной сессии.

| Event           | Matcher input   | Когда это срабатывает              |
| :-------------- | :-------------- | :--------------------------------- |
| `SubagentStart` | Имя типа агента | Когда subagent начинает выполнение |
| `SubagentStop`  | Имя типа агента | Когда subagent завершается         |

Оба события поддерживают matchers для нацеливания на конкретные типы агентов по имени. Этот пример запускает скрипт установки только при запуске subagent `db-agent` и скрипт очистки при остановке любого subagent:

```json  theme={null}
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

Полный формат конфигурации hook см. в [Hooks](/ru/hooks).

## Работа с subagents

### Поймите автоматическое делегирование

Claude автоматически делегирует задачи на основе описания задачи в вашем запросе, поля `description` в конфигурациях subagent и текущего контекста. Чтобы поощрить активное делегирование, включите фразы вроде "use proactively" в поле description вашего subagent.

Вы также можете явно запросить конкретный subagent:

```text  theme={null}
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

### Запускайте subagents в foreground или background

Subagents могут работать в foreground (блокирующий) или background (параллельный):

* **Foreground subagents** блокируют основной разговор до завершения. Запросы разрешений и уточняющие вопросы (такие как [`AskUserQuestion`](/ru/settings#tools-available-to-claude)) передаются вам.
* **Background subagents** работают параллельно, пока вы продолжаете работать. Перед запуском Claude Code запрашивает разрешения на инструменты, которые потребуются subagent, обеспечивая необходимые одобрения заранее. После запуска subagent наследует эти разрешения и автоматически отклоняет всё, что не было предварительно одобрено. Если background subagent нужно задать уточняющие вопросы, этот вызов инструмента не удастся, но subagent продолжает работу.

Если background subagent не удаётся из-за отсутствия разрешений, вы можете [возобновить его](#resume-subagents) в foreground для повторной попытки с интерактивными запросами.

Claude решает, запускать ли subagents в foreground или background на основе задачи. Вы также можете:

* Попросить Claude "run this in the background"
* Нажать **Ctrl+B** для фонового выполнения работающей задачи

Чтобы отключить всю функциональность фоновых задач, установите переменную окружения `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` на `1`. См. [Environment variables](/ru/settings#environment-variables).

### Распространённые паттерны

#### Изолируйте высокообъёмные операции

Одно из наиболее эффективных применений subagents — изоляция операций, которые производят большой объём выходных данных. Запуск тестов, получение документации или обработка файлов журналов может потребить значительный контекст. Делегируя эти операции subagent, подробный выход остаётся в контексте subagent, в то время как только релевантное резюме возвращается в основной разговор.

```text  theme={null}
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### Запускайте параллельное исследование

Для независимых исследований порождайте несколько subagents для одновременной работы:

```text  theme={null}
Research the authentication, database, and API modules in parallel using separate subagents
```

Каждый subagent исследует свою область независимо, затем Claude синтезирует результаты. Это работает лучше всего, когда пути исследования не зависят друг от друга.

<Warning>
  Когда subagents завершаются, их результаты возвращаются в основной разговор. Запуск многих subagents, каждый из которых возвращает подробные результаты, может потребить значительный контекст.
</Warning>

Для задач, требующих устойчивого параллелизма или превышающих ваш context window, [agent teams](/ru/agent-teams) дают каждому работнику свой независимый контекст.

#### Цепочка subagents

Для многошаговых рабочих процессов попросите Claude использовать subagents последовательно. Каждый subagent завершает свою задачу и возвращает результаты Claude, который затем передаёт релевантный контекст следующему subagent.

```text  theme={null}
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Выберите между subagents и основным разговором

Используйте **основной разговор**, когда:

* Задача требует частого взаимодействия или итеративного уточнения
* Несколько фаз имеют значительный общий контекст (планирование → реализация → тестирование)
* Вы вносите быстрое, целевое изменение
* Задержка имеет значение. Subagents начинают с нуля и могут потребовать время для сбора контекста

Используйте **subagents**, когда:

* Задача производит подробный выход, который вам не нужен в основном контексте
* Вы хотите применить конкретные ограничения на инструменты или разрешения
* Работа самодостаточна и может вернуть резюме

Рассмотрите [Skills](/ru/skills) вместо этого, когда вы хотите переиспользуемые промпты или рабочие процессы, которые работают в контексте основного разговора, а не в изолированном контексте subagent.

Для быстрого вопроса о чём-то уже в вашем разговоре используйте [`/btw`](/ru/interactive-mode#side-questions-with-btw) вместо subagent. Он видит ваш полный контекст, но не имеет доступа к инструментам, и ответ отбрасывается, а не добавляется в историю.

<Note>
  Subagents не могут порождать других subagents. Если ваш рабочий процесс требует вложенного делегирования, используйте [Skills](/ru/skills) или [цепочку subagents](#chain-subagents) из основного разговора.
</Note>

### Управляйте контекстом subagent

#### Возобновите subagents

Каждый вызов subagent создаёт новый экземпляр со свежим контекстом. Чтобы продолжить работу существующего subagent вместо начала с нуля, попросите Claude возобновить его.

Возобновлённые subagents сохраняют полную историю разговора, включая все предыдущие вызовы инструментов, результаты и рассуждения. Subagent продолжает ровно там, где остановился, а не начинает с нуля.

Когда subagent завершается, Claude получает его ID агента. Чтобы возобновить subagent, попросите Claude продолжить предыдущую работу:

```text  theme={null}
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

Вы также можете попросить Claude ID агента, если хотите ссылаться на него явно, или найти ID в файлах транскриптов в `~/.claude/projects/{project}/{sessionId}/subagents/`. Каждый транскрипт сохраняется как `agent-{agentId}.jsonl`.

Транскрипты subagent сохраняются независимо от основного разговора:

* **Compaction основного разговора**: Когда основной разговор сжимается, транскрипты subagent не затрагиваются. Они сохраняются в отдельных файлах.
* **Persistence сессии**: Транскрипты subagent сохраняются в пределах их сессии. Вы можете [возобновить subagent](#resume-subagents) после перезагрузки Claude Code, возобновив ту же сессию.
* **Автоматическая очистка**: Транскрипты очищаются на основе параметра `cleanupPeriodDays` (по умолчанию: 30 дней).

#### Auto-compaction

Subagents поддерживают автоматическое сжатие, используя ту же логику, что и основной разговор. По умолчанию auto-compaction срабатывает при примерно 95% ёмкости. Чтобы срабатывание произошло раньше, установите `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` на более низкий процент (например, `50`). Подробности см. в [environment variables](/ru/settings#environment-variables).

События сжатия регистрируются в файлах транскриптов subagent:

```json  theme={null}
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}
```

Значение `preTokens` показывает, сколько токенов было использовано перед сжатием.

## Примеры subagents

Эти примеры демонстрируют эффективные паттерны для создания subagents. Используйте их как отправные точки или генерируйте настроенную версию с Claude.

<Tip>
  **Best practices:**

  * **Проектируйте сфокусированные subagents:** каждый subagent должен превосходить в одной конкретной задаче
  * **Напишите подробные описания:** Claude использует описание для решения о делегировании
  * **Ограничьте доступ к инструментам:** предоставьте только необходимые разрешения для безопасности и сфокусированности
  * **Проверьте в систему контроля версий:** поделитесь project subagents с вашей командой
</Tip>

### Проверяющий код

Subagent, доступный только для чтения, который проверяет код без его модификации. Этот пример показывает, как спроектировать сфокусированный subagent с ограниченным доступом к инструментам (без Edit или Write) и подробный промпт, который точно указывает, что искать и как форматировать выход.

```markdown  theme={null}
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

### Debugger

Subagent, который может как анализировать, так и исправлять проблемы. В отличие от проверяющего кода, этот включает Edit, потому что исправление ошибок требует модификации кода. Промпт предоставляет чёткий рабочий процесс от диагностики к проверке.

```markdown  theme={null}
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

### Специалист по данным

Специализированный subagent для работы анализа данных. Этот пример показывает, как создавать subagents для специализированных рабочих процессов вне типичных задач кодирования. Он явно устанавливает `model: sonnet` для более способного анализа.

```markdown  theme={null}
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

### Валидатор запросов к базе данных

Subagent, который разрешает доступ Bash, но проверяет команды, чтобы разрешить только запросы SQL только для чтения. Этот пример показывает, как использовать hooks `PreToolUse` для условной валидации, когда вам нужен более тонкий контроль, чем предоставляет поле `tools`.

```markdown  theme={null}
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.
```

Claude Code [передаёт входные данные hook как JSON](/ru/hooks#pretooluse-input) через stdin командам hook. Скрипт валидации читает этот JSON, извлекает выполняемую команду и проверяет её против списка операций записи SQL. Если обнаружена операция записи, скрипт [выходит с кодом 2](/ru/hooks#exit-code-2-behavior-per-event) для блокирования выполнения и возвращает сообщение об ошибке Claude через stderr.

Создайте скрипт валидации где-нибудь в вашем проекте. Путь должен соответствовать полю `command` в конфигурации hook:

```bash  theme={null}
#!/bin/bash
# Blocks SQL write operations, allows SELECT queries

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0
```

Сделайте скрипт исполняемым:

```bash  theme={null}
chmod +x ./scripts/validate-readonly-query.sh
```

Hook получает JSON через stdin с командой Bash в `tool_input.command`. Код выхода 2 блокирует операцию и передаёт сообщение об ошибке обратно Claude. Подробности см. в [Hooks](/ru/hooks#exit-code-output) и [Hook input](/ru/hooks#pretooluse-input) для полной схемы входных данных.

## Следующие шаги

Теперь, когда вы понимаете subagents, изучите эти связанные функции:

* [Распространяйте subagents с помощью плагинов](/ru/plugins) для совместного использования subagents в командах или проектах
* [Запускайте Claude Code программно](/ru/headless) с помощью Agent SDK для CI/CD и автоматизации
* [Используйте MCP servers](/ru/mcp) для предоставления subagents доступа к внешним инструментам и данным
