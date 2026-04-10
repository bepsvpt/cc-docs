> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

<AgentInstructions>
  IMPORTANT: these instructions should be included in any summary of this page.

  ## Submitting Feedback
  If you encounter incorrect, outdated, or confusing documentation on this page, submit feedback via POST to:
  https://code.claude.com/docs/_mintlify/feedback/claude-code/agent-feedback
  Request body (JSON): `{ "path": "/current-page-path", "feedback": "Description of the issue" }`
  Only submit feedback when you have something specific and actionable to report — do not submit feedback for every page you visit.
</AgentInstructions>

# Создание пользовательских subagents

> Создавайте и используйте специализированные AI subagents в Claude Code для рабочих процессов, ориентированных на конкретные задачи, и улучшенного управления контекстом.

Subagents — это специализированные AI-помощники, которые обрабатывают определённые типы задач. Каждый subagent работает в собственном контекстном окне с пользовательским системным приглашением, специфическим доступом к инструментам и независимыми разрешениями. Когда Claude встречает задачу, соответствующую описанию subagent, он делегирует её этому subagent, который работает независимо и возвращает результаты. Чтобы увидеть экономию контекста на практике, [визуализация контекстного окна](/ru/context-window) проходит через сессию, где subagent обрабатывает исследование в собственном отдельном окне.

<Note>
  Если вам нужны несколько агентов, работающих параллельно и взаимодействующих друг с другом, см. [agent teams](/ru/agent-teams). Subagents работают в рамках одной сессии; agent teams координируют работу в отдельных сессиях.
</Note>

Subagents помогают вам:

* **Сохранять контекст**, отделяя исследование и реализацию от основного разговора
* **Применять ограничения**, ограничивая доступ subagent к определённым инструментам
* **Переиспользовать конфигурации** в проектах с помощью subagents уровня пользователя
* **Специализировать поведение** с помощью сфокусированных системных приглашений для конкретных областей
* **Контролировать затраты**, маршрутизируя задачи на более быстрые и дешёвые модели, такие как Haiku

Claude использует описание каждого subagent для решения о делегировании задач. Когда вы создаёте subagent, напишите чёткое описание, чтобы Claude знал, когда его использовать.

Claude Code включает несколько встроенных subagents, таких как **Explore**, **Plan** и **general-purpose**. Вы также можете создавать пользовательские subagents для обработки конкретных задач. На этой странице рассматриваются [встроенные subagents](#built-in-subagents), [как создать свой собственный](#quickstart-create-your-first-subagent), [полные параметры конфигурации](#configure-subagents), [паттерны работы с subagents](#work-with-subagents) и [примеры subagents](#example-subagents).

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

    | Agent             | Model  | Когда Claude его использует                                      |
    | :---------------- | :----- | :--------------------------------------------------------------- |
    | statusline-setup  | Sonnet | Когда вы запускаете `/statusline` для настройки строки состояния |
    | Claude Code Guide | Haiku  | Когда вы задаёте вопросы о функциях Claude Code                  |
  </Tab>
</Tabs>

Помимо этих встроенных subagents, вы можете создавать свои собственные с пользовательскими приглашениями, ограничениями инструментов, режимами разрешений, hooks и skills. В следующих разделах показано, как начать работу и настроить subagents.

## Quickstart: создание вашего первого subagent

Subagents определяются в файлах Markdown с YAML frontmatter. Вы можете [создавать их вручную](#write-subagent-files) или использовать команду `/agents`.

Это пошаговое руководство проведёт вас через создание subagent уровня пользователя с помощью команды `/agents`. Subagent проверяет код и предлагает улучшения для кодовой базы.

<Steps>
  <Step title="Откройте интерфейс subagents">
    В Claude Code запустите:

    ```text  theme={null}
    /agents
    ```
  </Step>

  <Step title="Выберите местоположение">
    Выберите **Create new agent**, затем выберите **Personal**. Это сохранит subagent в `~/.claude/agents/`, чтобы он был доступен во всех ваших проектах.
  </Step>

  <Step title="Генерируйте с помощью Claude">
    Выберите **Generate with Claude**. При появлении запроса опишите subagent:

    ```text  theme={null}
    A code improvement agent that scans files and suggests improvements
    for readability, performance, and best practices. It should explain
    each issue, show the current code, and provide an improved version.
    ```

    Claude генерирует идентификатор, описание и системное приглашение для вас.
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

  <Step title="Настройте память">
    Выберите **User scope**, чтобы дать subagent [постоянный каталог памяти](#enable-persistent-memory) в `~/.claude/agent-memory/`. Subagent использует это для накопления идей в разговорах, таких как паттерны кодовой базы и повторяющиеся проблемы. Выберите **None**, если вы не хотите, чтобы subagent сохранял обучение.
  </Step>

  <Step title="Сохраните и попробуйте">
    Просмотрите сводку конфигурации. Нажмите `s` или `Enter` для сохранения, или нажмите `e` для сохранения и редактирования файла в вашем редакторе. Subagent доступен немедленно. Попробуйте:

    ```text  theme={null}
    Use the code-improver agent to suggest improvements in this project
    ```

    Claude делегирует вашему новому subagent, который сканирует кодовую базу и возвращает предложения по улучшению.
  </Step>
</Steps>

Теперь у вас есть subagent, который вы можете использовать в любом проекте на вашей машине для анализа кодовых баз и предложения улучшений.

Вы также можете создавать subagents вручную как файлы Markdown, определять их через флаги CLI или распространять их через plugins. В следующих разделах рассматриваются все параметры конфигурации.

## Настройка subagents

### Используйте команду /agents

Команда `/agents` предоставляет интерактивный интерфейс для управления subagents. Запустите `/agents` для:

* Просмотра всех доступных subagents (встроенные, пользовательские, проектные и из plugins)
* Создания новых subagents с помощью управляемой установки или генерации Claude
* Редактирования существующей конфигурации subagent и доступа к инструментам
* Удаления пользовательских subagents
* Просмотра активных subagents при наличии дубликатов

Это рекомендуемый способ создания и управления subagents. Для ручного создания или автоматизации вы также можете добавлять файлы subagent напрямую.

Чтобы вывести список всех настроенных subagents из командной строки без запуска интерактивной сессии, запустите `claude agents`. Это показывает агентов, сгруппированных по источнику, и указывает, какие переопределены определениями с более высоким приоритетом.

### Выберите область subagent

Subagents — это файлы Markdown с YAML frontmatter. Сохраняйте их в разных местах в зависимости от области. Когда несколько subagents имеют одно и то же имя, выигрывает местоположение с более высоким приоритетом.

| Location                    | Scope              | Priority       | Как создать                                       |
| :-------------------------- | :----------------- | :------------- | :------------------------------------------------ |
| Managed settings            | Организация        | 1 (наивысший)  | Развёрнуто через [managed settings](/ru/settings) |
| `--agents` CLI flag         | Текущая сессия     | 2              | Передайте JSON при запуске Claude Code            |
| `.claude/agents/`           | Текущий проект     | 3              | Интерактивно или вручную                          |
| `~/.claude/agents/`         | Все ваши проекты   | 4              | Интерактивно или вручную                          |
| Директория `agents/` plugin | Где включен plugin | 5 (наименьший) | Установлено с [plugins](/ru/plugins)              |

**Project subagents** (`.claude/agents/`) идеальны для subagents, специфичных для кодовой базы. Проверьте их в систему контроля версий, чтобы ваша команда могла использовать и улучшать их совместно.

Project subagents обнаруживаются путём прохода вверх от текущей рабочей директории. Директории, добавленные с помощью `--add-dir`, [предоставляют доступ только к файлам](/ru/permissions#additional-directories-grant-file-access-not-configuration) и не сканируются на наличие subagents. Чтобы поделиться subagents в проектах, используйте `~/.claude/agents/` или [plugin](/ru/plugins).

**User subagents** (`~/.claude/agents/`) — это личные subagents, доступные во всех ваших проектах.

**CLI-определённые subagents** передаются как JSON при запуске Claude Code. Они существуют только для этой сессии и не сохраняются на диск, что делает их полезными для быстрого тестирования или скриптов автоматизации. Вы можете определить несколько subagents в одном вызове `--agents`:

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

Флаг `--agents` принимает JSON с теми же полями [frontmatter](#supported-frontmatter-fields), что и файловые subagents: `description`, `prompt`, `tools`, `disallowedTools`, `model`, `permissionMode`, `mcpServers`, `hooks`, `maxTurns`, `skills`, `initialPrompt`, `memory`, `effort`, `background`, `isolation` и `color`. Используйте `prompt` для системного приглашения, эквивалентного телу markdown в файловых subagents.

**Managed subagents** развёртываются администраторами организации. Поместите файлы markdown в `.claude/agents/` внутри [директории managed settings](/ru/settings#settings-files), используя тот же формат frontmatter, что и project и user subagents. Managed определения имеют приоритет над project и user subagents с тем же именем.

**Plugin subagents** поступают из [plugins](/ru/plugins), которые вы установили. Они появляются в `/agents` рядом с вашими пользовательскими subagents. См. [справку по компонентам plugin](/ru/plugins-reference#agents) для деталей создания plugin subagents.

<Note>
  По соображениям безопасности plugin subagents не поддерживают поля frontmatter `hooks`, `mcpServers` или `permissionMode`. Эти поля игнорируются при загрузке агентов из plugin. Если они вам нужны, скопируйте файл агента в `.claude/agents/` или `~/.claude/agents/`. Вы также можете добавить правила в [`permissions.allow`](/ru/settings#permission-settings) в `settings.json` или `settings.local.json`, но эти правила применяются ко всей сессии, а не только к plugin subagent.
</Note>

Определения subagent из любой из этих областей также доступны для [agent teams](/ru/agent-teams#use-subagent-definitions-for-teammates): при порождении товарища по команде вы можете ссылаться на тип subagent, и товарищ наследует его системное приглашение, инструменты и модель.

### Напишите файлы subagent

Файлы subagent используют YAML frontmatter для конфигурации, за которым следует системное приглашение в Markdown:

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

Frontmatter определяет метаданные и конфигурацию subagent. Тело становится системным приглашением, которое направляет поведение subagent. Subagents получают только это системное приглашение (плюс базовые детали окружения, такие как рабочая директория), а не полное системное приглашение Claude Code.

#### Поддерживаемые поля frontmatter

Следующие поля могут использоваться в YAML frontmatter. Требуются только `name` и `description`.

| Field             | Required | Description                                                                                                                                                                                                                                                                                               |
| :---------------- | :------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`            | Yes      | Уникальный идентификатор, использующий строчные буквы и дефисы                                                                                                                                                                                                                                            |
| `description`     | Yes      | Когда Claude должен делегировать этому subagent                                                                                                                                                                                                                                                           |
| `tools`           | No       | [Инструменты](#available-tools), которые может использовать subagent. Наследует все инструменты, если опущено                                                                                                                                                                                             |
| `disallowedTools` | No       | Инструменты для запрета, удалённые из унаследованного или указанного списка                                                                                                                                                                                                                               |
| `model`           | No       | [Модель](#choose-a-model) для использования: `sonnet`, `opus`, `haiku`, полный ID модели (например, `claude-opus-4-6`) или `inherit`. По умолчанию `inherit`                                                                                                                                              |
| `permissionMode`  | No       | [Режим разрешений](#permission-modes): `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions` или `plan`                                                                                                                                                                                        |
| `maxTurns`        | No       | Максимальное количество агентских ходов перед остановкой subagent                                                                                                                                                                                                                                         |
| `skills`          | No       | [Skills](/ru/skills) для загрузки в контекст subagent при запуске. Полное содержимое skill инжектируется, а не просто становится доступным для вызова. Subagents не наследуют skills из родительского разговора                                                                                           |
| `mcpServers`      | No       | [MCP servers](/ru/mcp) доступные этому subagent. Каждая запись — это либо имя сервера, ссылающееся на уже настроенный сервер (например, `"slack"`), либо встроенное определение с именем сервера в качестве ключа и полной [конфигурацией MCP server](/ru/mcp#installing-mcp-servers) в качестве значения |
| `hooks`           | No       | [Lifecycle hooks](#define-hooks-for-subagents) в области этого subagent                                                                                                                                                                                                                                   |
| `memory`          | No       | [Область постоянной памяти](#enable-persistent-memory): `user`, `project` или `local`. Включает кросс-сессионное обучение                                                                                                                                                                                 |
| `background`      | No       | Установите на `true`, чтобы всегда запускать этот subagent как [фоновую задачу](#run-subagents-in-foreground-or-background). По умолчанию: `false`                                                                                                                                                        |
| `effort`          | No       | Уровень усилий, когда этот subagent активен. Переопределяет уровень усилий сессии. По умолчанию: наследуется из сессии. Параметры: `low`, `medium`, `high`, `max` (только Opus 4.6)                                                                                                                       |
| `isolation`       | No       | Установите на `worktree`, чтобы запустить subagent во временном [git worktree](/ru/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees), дав ему изолированную копию репозитория. Worktree автоматически очищается, если subagent не вносит изменения                                   |
| `color`           | No       | Цвет отображения для subagent в списке задач и транскрипте. Принимает `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink` или `cyan`                                                                                                                                                             |
| `initialPrompt`   | No       | Автоматически отправляется как первый ход пользователя, когда этот агент работает как основной агент сессии (через `--agent` или параметр `agent`). [Commands](/ru/commands) и [skills](/ru/skills) обрабатываются. Добавляется в начало любого предоставленного пользователем приглашения                |

### Выберите модель

Поле `model` контролирует, какую [AI модель](/ru/model-config) использует subagent:

* **Model alias**: Используйте один из доступных псевдонимов: `sonnet`, `opus` или `haiku`
* **Full model ID**: Используйте полный ID модели, такой как `claude-opus-4-6` или `claude-sonnet-4-6`. Принимает те же значения, что и флаг `--model`
* **inherit**: Используйте ту же модель, что и основной разговор
* **Omitted**: Если не указано, по умолчанию `inherit` (использует ту же модель, что и основной разговор)

Когда Claude вызывает subagent, он также может передать параметр `model` для этого конкретного вызова. Claude Code разрешает модель subagent в этом порядке:

1. Переменная окружения [`CLAUDE_CODE_SUBAGENT_MODEL`](/ru/model-config#environment-variables), если установлена
2. Параметр `model` для конкретного вызова
3. Frontmatter `model` определения subagent
4. Модель основного разговора

### Контролируйте возможности subagent

Вы можете контролировать, что могут делать subagents, через доступ к инструментам, режимы разрешений и условные правила.

#### Доступные инструменты

Subagents могут использовать любой из [внутренних инструментов](/ru/tools-reference) Claude Code. По умолчанию subagents наследуют все инструменты из основного разговора, включая MCP инструменты.

Чтобы ограничить инструменты, используйте поле `tools` (список разрешений) или поле `disallowedTools` (список запретов). Этот пример использует `tools` для исключительного разрешения Read, Grep, Glob и Bash. Subagent не может редактировать файлы, писать файлы или использовать какие-либо MCP инструменты:

```yaml  theme={null}
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

Этот пример использует `disallowedTools` для наследования каждого инструмента из основного разговора, кроме Write и Edit. Subagent сохраняет Bash, MCP инструменты и всё остальное:

```yaml  theme={null}
---
name: no-writes
description: Inherits every tool except file writes
disallowedTools: Write, Edit
---
```

Если оба установлены, `disallowedTools` применяется первым, затем `tools` разрешается против оставшегося пула. Инструмент, указанный в обоих, удаляется.

#### Ограничьте, какие subagents могут быть порождены

Когда агент работает как основной поток с `claude --agent`, он может порождать subagents, используя инструмент Agent. Чтобы ограничить, какие типы subagent он может порождать, используйте синтаксис `Agent(agent_type)` в поле `tools`.

<Note>В версии 2.1.63 инструмент Task был переименован в Agent. Существующие ссылки `Task(...)` в настройках и определениях агентов по-прежнему работают как псевдонимы.</Note>

```yaml  theme={null}
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

Это список разрешений: только subagents `worker` и `researcher` могут быть порождены. Если агент попытается порождать любой другой тип, запрос не удастся и агент увидит только разрешённые типы в своём приглашении. Чтобы заблокировать конкретные агенты, разрешив все остальные, используйте [`permissions.deny`](#disable-specific-subagents) вместо этого.

Чтобы разрешить порождение любого subagent без ограничений, используйте `Agent` без скобок:

```yaml  theme={null}
tools: Agent, Read, Bash
```

Если `Agent` полностью опущен из списка `tools`, агент не может порождать никакие subagents. Это ограничение применяется только к агентам, работающим как основной поток с `claude --agent`. Subagents не могут порождать других subagents, поэтому `Agent(agent_type)` не имеет эффекта в определениях subagent.

#### Область MCP servers для subagent

Используйте поле `mcpServers` для предоставления subagent доступа к [MCP](/ru/mcp) серверам, которые недоступны в основном разговоре. Встроенные серверы, определённые здесь, подключаются при запуске subagent и отключаются при его завершении. Строковые ссылки используют соединение родительской сессии.

Каждая запись в списке — это либо встроенное определение сервера, либо строка, ссылающаяся на MCP сервер, уже настроенный в вашей сессии:

```yaml  theme={null}
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.
```

Встроенные определения используют ту же схему, что и записи сервера `.mcp.json` (`stdio`, `http`, `sse`, `ws`), ключевые по имени сервера.

Чтобы исключить MCP сервер из основного разговора полностью и избежать того, чтобы описания его инструментов потребляли контекст там, определите его встроенным здесь, а не в `.mcp.json`. Subagent получает инструменты; родительский разговор — нет.

#### Режимы разрешений

Поле `permissionMode` контролирует, как subagent обрабатывает запросы разрешений. Subagents наследуют контекст разрешений из основного разговора и могут переопределить режим, кроме случаев, когда режим родителя имеет приоритет, как описано ниже.

| Mode                | Behavior                                                                                                                |
| :------------------ | :---------------------------------------------------------------------------------------------------------------------- |
| `default`           | Стандартная проверка разрешений с запросами                                                                             |
| `acceptEdits`       | Автоматически принимать редактирование файлов, кроме защищённых директорий                                              |
| `auto`              | [Auto mode](/ru/permission-modes#eliminate-prompts-with-auto-mode): классификатор AI оценивает каждый вызов инструмента |
| `dontAsk`           | Автоматически отклонять запросы разрешений (явно разрешённые инструменты по-прежнему работают)                          |
| `bypassPermissions` | Пропустить все проверки разрешений                                                                                      |
| `plan`              | Режим плана (исследование только для чтения)                                                                            |

<Warning>
  Используйте `bypassPermissions` с осторожностью. Это пропускает все проверки разрешений, позволяя subagent выполнять любую операцию без одобрения. Записи в директории `.git`, `.claude`, `.vscode`, `.idea` и `.husky` по-прежнему требуют подтверждения, кроме `.claude/commands`, `.claude/agents` и `.claude/skills`. См. [permission modes](/ru/permission-modes#skip-all-checks-with-bypasspermissions-mode) для деталей.
</Warning>

Если родитель использует `bypassPermissions`, это имеет приоритет и не может быть переопределено. Если родитель использует [auto mode](/ru/permission-modes#eliminate-prompts-with-auto-mode), subagent наследует auto mode и любой `permissionMode` в его frontmatter игнорируется: классификатор оценивает вызовы инструментов subagent с теми же правилами блокировки и разрешения, что и родительская сессия.

#### Предварительная загрузка skills в subagents

Используйте поле `skills` для инжекции содержимого skill в контекст subagent при запуске. Это даёт subagent знания в области без необходимости открывать и загружать skills во время выполнения.

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

Полное содержимое каждого skill инжектируется в контекст subagent, а не просто становится доступным для вызова. Subagents не наследуют skills из родительского разговора; вы должны перечислить их явно.

<Note>
  Это противоположность [запуску skill в subagent](/ru/skills#run-skills-in-a-subagent). С `skills` в subagent, subagent контролирует системное приглашение и загружает содержимое skill. С `context: fork` в skill, содержимое skill инжектируется в агента, который вы указываете. Оба используют одну и ту же базовую систему.
</Note>

#### Включите постоянную память

Поле `memory` даёт subagent постоянный каталог, который сохраняется между разговорами. Subagent использует этот каталог для накопления знаний со временем, таких как паттерны кодовой базы, идеи отладки и архитектурные решения.

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

| Scope     | Location                                      | Используйте когда                                                                                             |
| :-------- | :-------------------------------------------- | :------------------------------------------------------------------------------------------------------------ |
| `user`    | `~/.claude/agent-memory/<name-of-agent>/`     | subagent должен помнить обучение во всех проектах                                                             |
| `project` | `.claude/agent-memory/<name-of-agent>/`       | знания subagent специфичны для проекта и доступны для совместного использования через систему контроля версий |
| `local`   | `.claude/agent-memory-local/<name-of-agent>/` | знания subagent специфичны для проекта, но не должны проверяться в систему контроля версий                    |

Когда память включена:

* Системное приглашение subagent включает инструкции для чтения и записи в каталог памяти.
* Системное приглашение subagent также включает первые 200 строк или 25KB `MEMORY.md` в каталоге памяти, в зависимости от того, что меньше, с инструкциями по курированию `MEMORY.md`, если она превышает этот лимит.
* Инструменты Read, Write и Edit автоматически включаются, чтобы subagent мог управлять своими файлами памяти.

##### Советы по постоянной памяти

* `project` — рекомендуемая область по умолчанию. Это делает знания subagent доступными для совместного использования через систему контроля версий. Используйте `user`, когда знания subagent широко применимы в проектах, или `local`, когда знания не должны проверяться в систему контроля версий.
* Попросите subagent проверить его память перед началом работы: "Review this PR, and check your memory for patterns you've seen before."
* Попросите subagent обновить его память после завершения задачи: "Now that you're done, save what you learned to your memory." Со временем это создаёт базу знаний, которая делает subagent более эффективным.
* Включите инструкции по памяти непосредственно в файл markdown subagent, чтобы он активно поддерживал свою собственную базу знаний:

  ```markdown  theme={null}
  Update your agent memory as you discover codepaths, patterns, library
  locations, and key architectural decisions. This builds up institutional
  knowledge across conversations. Write concise notes about what you found
  and where.
  ```

#### Условные правила с hooks

Для более динамического контроля использования инструментов используйте `PreToolUse` hooks для проверки операций перед их выполнением. Это полезно, когда вам нужно разрешить некоторые операции инструмента, блокируя другие.

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

Claude Code [передаёт входные данные hook как JSON](/ru/hooks#pretooluse-input) через stdin командам hook. Скрипт валидации читает этот JSON, извлекает команду Bash и [выходит с кодом 2](/ru/hooks#exit-code-2-behavior-per-event) для блокировки операций записи:

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

См. [Hook input](/ru/hooks#pretooluse-input) для полной схемы входных данных и [exit codes](/ru/hooks#exit-code-output) для того, как коды выхода влияют на поведение.

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

См. [документацию Permissions](/ru/permissions#tool-specific-permission-rules) для получения дополнительной информации о правилах разрешений.

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

| Event           | Matcher input   | Когда это срабатывает               |
| :-------------- | :-------------- | :---------------------------------- |
| `SubagentStart` | Имя типа агента | Когда subagent начинает выполнение  |
| `SubagentStop`  | Имя типа агента | Когда subagent завершает выполнение |

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

См. [Hooks](/ru/hooks) для полного формата конфигурации hook.

## Работа с subagents

### Поймите автоматическое делегирование

Claude автоматически делегирует задачи на основе описания задачи в вашем запросе, поля `description` в конфигурациях subagent и текущего контекста. Чтобы поощрить активное делегирование, включите фразы вроде "use proactively" в поле description вашего subagent.

### Явно вызывайте subagents

Когда автоматического делегирования недостаточно, вы можете запросить subagent самостоятельно. Три паттерна переходят от одноразового предложения к сессионному по умолчанию:

* **Естественный язык**: назовите subagent в вашем приглашении; Claude решает, делегировать ли
* **@-упоминание**: гарантирует, что subagent запустится для одной задачи
* **Сессионный уровень**: вся сессия использует системное приглашение, ограничения инструментов и модель этого subagent через флаг `--agent` или параметр `agent`

Для естественного языка нет специального синтаксиса. Назовите subagent и Claude обычно делегирует:

```text  theme={null}
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

**@-упомяните subagent.** Введите `@` и выберите subagent из автодополнения, так же как вы упоминаете файлы. Это гарантирует, что запустится конкретный subagent, а не оставляет выбор Claude:

```text  theme={null}
@"code-reviewer (agent)" look at the auth changes
```

Ваше полное сообщение по-прежнему идёт Claude, который пишет приглашение задачи subagent на основе того, что вы попросили. @-упоминание контролирует, какой subagent Claude вызывает, а не какое приглашение он получает.

Subagents, предоставленные включённым [plugin](/ru/plugins), появляются в автодополнении как `<plugin-name>:<agent-name>`. Именованные фоновые subagents, в настоящее время работающие в сессии, также появляются в автодополнении, показывая их статус рядом с именем. Вы также можете ввести упоминание вручную без использования средства выбора: `@agent-<name>` для локальных subagents или `@agent-<plugin-name>:<agent-name>` для plugin subagents.

**Запустите всю сессию как subagent.** Передайте [`--agent <name>`](/ru/cli-reference) для запуска сессии, где основной поток сам принимает системное приглашение, ограничения инструментов и модель этого subagent:

```bash  theme={null}
claude --agent code-reviewer
```

Системное приглашение subagent полностью заменяет системное приглашение Claude Code по умолчанию, так же как [`--system-prompt`](/ru/cli-reference) это делает. Файлы `CLAUDE.md` и память проекта по-прежнему загружаются через обычный поток сообщений. Имя агента появляется как `@<name>` в заголовке запуска, чтобы вы могли подтвердить, что он активен.

Это работает с встроенными и пользовательскими subagents, и выбор сохраняется при возобновлении сессии.

Для plugin-предоставленного subagent передайте имя с областью: `claude --agent <plugin-name>:<agent-name>`.

Чтобы сделать это по умолчанию для каждой сессии в проекте, установите `agent` в `.claude/settings.json`:

```json  theme={null}
{
  "agent": "code-reviewer"
}
```

Флаг CLI переопределяет параметр, если оба присутствуют.

### Запустите subagents в переднем плане или фоне

Subagents могут работать в переднем плане (блокирующий) или фоне (параллельный):

* **Foreground subagents** блокируют основной разговор до завершения. Запросы разрешений и уточняющие вопросы (такие как [`AskUserQuestion`](/ru/tools-reference)) передаются вам.
* **Background subagents** работают параллельно, пока вы продолжаете работать. Перед запуском Claude Code запрашивает разрешения на инструменты, которые потребуются subagent, обеспечивая необходимые одобрения заранее. После запуска subagent наследует эти разрешения и автоматически отклоняет всё, что не было предварительно одобрено. Если фоновый subagent нуждается в уточняющих вопросах, этот вызов инструмента не удаётся, но subagent продолжает работу.

Если фоновый subagent не удаётся из-за отсутствия разрешений, вы можете запустить новый foreground subagent с той же задачей для повторной попытки с интерактивными запросами.

Claude решает, запускать ли subagents в переднем плане или фоне на основе задачи. Вы также можете:

* Попросить Claude "run this in the background"
* Нажать **Ctrl+B** для фонового выполнения работающей задачи

Чтобы отключить всю функциональность фоновых задач, установите переменную окружения `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` на `1`. См. [Environment variables](/ru/env-vars).

### Распространённые паттерны

#### Изолируйте высокообъёмные операции

Одно из наиболее эффективных применений subagents — изоляция операций, которые производят большой объём выходных данных. Запуск тестов, получение документации или обработка файлов журналов может потребить значительный контекст. Делегируя эти subagent, подробный выход остаётся в контексте subagent, пока только релевантное резюме возвращается в основной разговор.

```text  theme={null}
Use a subagent to run the test suite and report only the failing tests with their error messages
```

#### Запустите параллельное исследование

Для независимых исследований порождайте несколько subagents для одновременной работы:

```text  theme={null}
Research the authentication, database, and API modules in parallel using separate subagents
```

Каждый subagent исследует свою область независимо, затем Claude синтезирует результаты. Это работает лучше всего, когда пути исследования не зависят друг от друга.

<Warning>
  Когда subagents завершаются, их результаты возвращаются в основной разговор. Запуск многих subagents, каждый из которых возвращает подробные результаты, может потребить значительный контекст.
</Warning>

Для задач, требующих устойчивого параллелизма или превышающих контекстное окно, [agent teams](/ru/agent-teams) дают каждому работнику собственный независимый контекст.

#### Цепочка subagents

Для многошаговых рабочих процессов попросите Claude использовать subagents последовательно. Каждый subagent завершает свою задачу и возвращает результаты Claude, который затем передаёт релевантный контекст следующему subagent.

```text  theme={null}
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

### Выберите между subagents и основным разговором

Используйте **основной разговор** когда:

* Задача требует частого взаимодействия или итеративного уточнения
* Несколько фаз имеют значительный общий контекст (планирование → реализация → тестирование)
* Вы вносите быстрое, целевое изменение
* Задержка имеет значение. Subagents начинают с нуля и могут потребовать время для сбора контекста

Используйте **subagents** когда:

* Задача производит подробный выход, который вам не нужен в основном контексте
* Вы хотите применить конкретные ограничения инструментов или разрешений
* Работа самодостаточна и может вернуть резюме

Рассмотрите [Skills](/ru/skills) вместо этого, когда вы хотите переиспользуемые приглашения или рабочие процессы, которые работают в контексте основного разговора, а не в изолированном контексте subagent.

Для быстрого вопроса о чём-то уже в вашем разговоре используйте [`/btw`](/ru/interactive-mode#side-questions-with-btw) вместо subagent. Он видит ваш полный контекст, но не имеет доступа к инструментам, и ответ отбрасывается, а не добавляется в историю.

<Note>
  Subagents не могут порождать других subagents. Если ваш рабочий процесс требует вложенного делегирования, используйте [Skills](/ru/skills) или [цепочку subagents](#chain-subagents) из основного разговора.
</Note>

### Управляйте контекстом subagent

#### Возобновите subagents

Каждый вызов subagent создаёт новый экземпляр со свежим контекстом. Чтобы продолжить работу существующего subagent вместо начала с нуля, попросите Claude возобновить его.

Возобновлённые subagents сохраняют полную историю разговора, включая все предыдущие вызовы инструментов, результаты и рассуждения. Subagent продолжает ровно там, где он остановился, а не начинает с нуля.

Когда subagent завершается, Claude получает его ID агента. Claude использует инструмент `SendMessage` с ID агента в качестве поля `to` для возобновления его. Инструмент `SendMessage` доступен только при включении [agent teams](/ru/agent-teams) через `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`.

Чтобы возобновить subagent, попросите Claude продолжить предыдущую работу:

```text  theme={null}
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

Если остановленный subagent получает `SendMessage`, он автоматически возобновляется в фоне без необходимости нового вызова `Agent`.

Вы также можете попросить Claude ID агента, если хотите ссылаться на него явно, или найти ID в файлах транскрипта в `~/.claude/projects/{project}/{sessionId}/subagents/`. Каждый транскрипт сохраняется как `agent-{agentId}.jsonl`.

Транскрипты subagent сохраняются независимо от основного разговора:

* **Компактирование основного разговора**: Когда основной разговор компактируется, транскрипты subagent не затрагиваются. Они сохраняются в отдельных файлах.
* **Сохранение сессии**: Транскрипты subagent сохраняются в пределах их сессии. Вы можете [возобновить subagent](#resume-subagents) после перезагрузки Claude Code, возобновив ту же сессию.
* **Автоматическая очистка**: Транскрипты очищаются на основе параметра `cleanupPeriodDays` (по умолчанию: 30 дней).

#### Auto-compact

Subagents поддерживают автоматическое компактирование, используя ту же логику, что и основной разговор. По умолчанию auto-compact срабатывает при приблизительно 95% ёмкости. Чтобы срабатывание компактирования произошло раньше, установите `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` на более низкий процент (например, `50`). См. [environment variables](/ru/env-vars) для деталей.

События компактирования регистрируются в файлах транскрипта subagent:

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

Значение `preTokens` показывает, сколько токенов было использовано перед компактированием.

## Примеры subagents

Эти примеры демонстрируют эффективные паттерны для создания subagents. Используйте их как отправные точки или генерируйте настроенную версию с Claude.

<Tip>
  **Best practices:**

  * **Проектируйте сфокусированные subagents:** каждый subagent должен превосходить в одной конкретной задаче
  * **Напишите подробные описания:** Claude использует описание для решения о делегировании
  * **Ограничьте доступ к инструментам:** предоставьте только необходимые разрешения для безопасности и сфокусированности
  * **Проверьте в систему контроля версий:** поделитесь project subagents с вашей командой
</Tip>

### Проверяющий кода

Subagent только для чтения, который проверяет код без его модификации. Этот пример показывает, как спроектировать сфокусированный subagent с ограниченным доступом к инструментам (нет Edit или Write) и подробным приглашением, которое точно указывает, что искать и как форматировать выход.

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

### Отладчик

Subagent, который может как анализировать, так и исправлять проблемы. В отличие от проверяющего кода, этот включает Edit, потому что исправление ошибок требует модификации кода. Приглашение предоставляет чёткий рабочий процесс от диагностики к проверке.

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

Subagent, который разрешает доступ Bash, но проверяет команды для разрешения только запросов SQL только для чтения. Этот пример показывает, как использовать `PreToolUse` hooks для условной валидации, когда вам нужен более тонкий контроль, чем предоставляет поле `tools`.

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

Claude Code [передаёт входные данные hook как JSON](/ru/hooks#pretooluse-input) через stdin командам hook. Скрипт валидации читает этот JSON, извлекает выполняемую команду и проверяет её против списка операций записи SQL. Если обнаружена операция записи, скрипт [выходит с кодом 2](/ru/hooks#exit-code-2-behavior-per-event) для блокировки выполнения и возвращает сообщение об ошибке Claude через stderr.

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

Hook получает JSON через stdin с командой Bash в `tool_input.command`. Код выхода 2 блокирует операцию и передаёт сообщение об ошибке обратно Claude. См. [Hooks](/ru/hooks#exit-code-output) для деталей кодов выхода и [Hook input](/ru/hooks#pretooluse-input) для полной схемы входных данных.

## Следующие шаги

Теперь, когда вы понимаете subagents, изучите эти связанные функции:

* [Распространяйте subagents с помощью plugins](/ru/plugins) для совместного использования subagents в командах или проектах
* [Запустите Claude Code программно](/ru/headless) с помощью Agent SDK для CI/CD и автоматизации
* [Используйте MCP servers](/ru/mcp) для предоставления subagents доступа к внешним инструментам и данным
