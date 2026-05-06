> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Справочник по плагинам

> Полный технический справочник по системе плагинов Claude Code, включая схемы, команды CLI и спецификации компонентов.

<Tip>
  Ищете способ установить плагины? Смотрите [Обнаружение и установка плагинов](/ru/discover-plugins). Для создания плагинов смотрите [Плагины](/ru/plugins). Для распространения плагинов смотрите [Маркетплейсы плагинов](/ru/plugin-marketplaces).
</Tip>

Этот справочник содержит полные технические спецификации для системы плагинов Claude Code, включая схемы компонентов, команды CLI и инструменты разработки.

**Плагин** — это самостоятельный каталог компонентов, который расширяет Claude Code пользовательской функциональностью. Компоненты плагина включают skills, agents, hooks, MCP servers, LSP servers и monitors.

## Справочник компонентов плагина

### Skills

Плагины добавляют skills в Claude Code, создавая сочетания клавиш `/name`, которые вы или Claude можете вызвать.

**Расположение**: каталог `skills/` или `commands/` в корне плагина

**Формат файла**: Skills — это каталоги с `SKILL.md`; команды — это простые файлы markdown

**Структура skill**:

```text theme={null}
skills/
├── pdf-processor/
│   ├── SKILL.md
│   ├── reference.md (опционально)
│   └── scripts/ (опционально)
└── code-reviewer/
    └── SKILL.md
```

**Поведение интеграции**:

* Skills и команды автоматически обнаруживаются при установке плагина
* Claude может вызывать их автоматически на основе контекста задачи
* Skills могут включать вспомогательные файлы рядом с SKILL.md

Для полной информации смотрите [Skills](/ru/skills).

### Agents

Плагины могут предоставлять специализированные subagents для конкретных задач, которые Claude может вызывать автоматически при необходимости.

**Расположение**: каталог `agents/` в корне плагина

**Формат файла**: Файлы markdown, описывающие возможности агента

**Структура агента**:

```markdown theme={null}
---
name: agent-name
description: Что специализирует этот агент и когда Claude должен его вызвать
model: sonnet
effort: medium
maxTurns: 20
disallowedTools: Write, Edit
---

Подробное системное приглашение для агента, описывающее его роль, опыт и поведение.
```

Плагины agents поддерживают поля frontmatter `name`, `description`, `model`, `effort`, `maxTurns`, `tools`, `disallowedTools`, `skills`, `memory`, `background` и `isolation`. Единственное допустимое значение `isolation` — это `"worktree"`. По соображениям безопасности `hooks`, `mcpServers` и `permissionMode` не поддерживаются для agents, поставляемых с плагинами.

**Точки интеграции**:

* Агенты появляются в интерфейсе `/agents`
* Claude может вызывать агентов автоматически на основе контекста задачи
* Агенты могут быть вызваны вручную пользователями
* Плагины agents работают наряду со встроенными agents Claude

Для полной информации смотрите [Subagents](/ru/sub-agents).

### Hooks

Плагины могут предоставлять обработчики событий, которые автоматически реагируют на события Claude Code.

**Расположение**: `hooks/hooks.json` в корне плагина или встроенный в plugin.json

**Формат**: Конфигурация JSON с сопоставителями событий и действиями

**Конфигурация hook**:

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

Плагины hooks реагируют на те же события жизненного цикла, что и [определённые пользователем hooks](/ru/hooks):

| Event                 | When it fires                                                                                                                                          |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| `SessionStart`        | When a session begins or resumes                                                                                                                       |
| `Setup`               | When you start Claude Code with `--init-only`, or with `--init` or `--maintenance` in `-p` mode. For one-time preparation in CI or scripts             |
| `UserPromptSubmit`    | When you submit a prompt, before Claude processes it                                                                                                   |
| `UserPromptExpansion` | When a user-typed command expands into a prompt, before it reaches Claude. Can block the expansion                                                     |
| `PreToolUse`          | Before a tool call executes. Can block it                                                                                                              |
| `PermissionRequest`   | When a permission dialog appears                                                                                                                       |
| `PermissionDenied`    | When a tool call is denied by the auto mode classifier. Return `{retry: true}` to tell the model it may retry the denied tool call                     |
| `PostToolUse`         | After a tool call succeeds                                                                                                                             |
| `PostToolUseFailure`  | After a tool call fails                                                                                                                                |
| `PostToolBatch`       | After a full batch of parallel tool calls resolves, before the next model call                                                                         |
| `Notification`        | When Claude Code sends a notification                                                                                                                  |
| `SubagentStart`       | When a subagent is spawned                                                                                                                             |
| `SubagentStop`        | When a subagent finishes                                                                                                                               |
| `TaskCreated`         | When a task is being created via `TaskCreate`                                                                                                          |
| `TaskCompleted`       | When a task is being marked as completed                                                                                                               |
| `Stop`                | When Claude finishes responding                                                                                                                        |
| `StopFailure`         | When the turn ends due to an API error. Output and exit code are ignored                                                                               |
| `TeammateIdle`        | When an [agent team](/en/agent-teams) teammate is about to go idle                                                                                     |
| `InstructionsLoaded`  | When a CLAUDE.md or `.claude/rules/*.md` file is loaded into context. Fires at session start and when files are lazily loaded during a session         |
| `ConfigChange`        | When a configuration file changes during a session                                                                                                     |
| `CwdChanged`          | When the working directory changes, for example when Claude executes a `cd` command. Useful for reactive environment management with tools like direnv |
| `FileChanged`         | When a watched file changes on disk. The `matcher` field specifies which filenames to watch                                                            |
| `WorktreeCreate`      | When a worktree is being created via `--worktree` or `isolation: "worktree"`. Replaces default git behavior                                            |
| `WorktreeRemove`      | When a worktree is being removed, either at session exit or when a subagent finishes                                                                   |
| `PreCompact`          | Before context compaction                                                                                                                              |
| `PostCompact`         | After context compaction completes                                                                                                                     |
| `Elicitation`         | When an MCP server requests user input during a tool call                                                                                              |
| `ElicitationResult`   | After a user responds to an MCP elicitation, before the response is sent back to the server                                                            |
| `SessionEnd`          | When a session terminates                                                                                                                              |

**Типы hook**:

* `command`: выполнение команд оболочки или скриптов
* `http`: отправка JSON события как POST запроса на URL
* `mcp_tool`: вызов инструмента на настроенном [MCP server](/ru/mcp)
* `prompt`: оценка приглашения с помощью LLM (использует заполнитель `$ARGUMENTS` для контекста)
* `agent`: запуск проверки агента с инструментами для сложных задач проверки

### MCP servers

Плагины могут включать серверы Model Context Protocol (MCP) для подключения Claude Code к внешним инструментам и сервисам.

**Расположение**: `.mcp.json` в корне плагина или встроенный в plugin.json

**Формат**: Стандартная конфигурация сервера MCP

**Конфигурация сервера MCP**:

```json theme={null}
{
  "mcpServers": {
    "plugin-database": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    },
    "plugin-api-client": {
      "command": "npx",
      "args": ["@company/mcp-server", "--plugin-mode"],
      "cwd": "${CLAUDE_PLUGIN_ROOT}"
    }
  }
}
```

**Поведение интеграции**:

* Серверы MCP плагина запускаются автоматически при включении плагина
* Серверы отображаются как стандартные инструменты MCP в наборе инструментов Claude
* Возможности сервера беспрепятственно интегрируются с существующими инструментами Claude
* Серверы плагина можно настраивать независимо от серверов MCP пользователя

### LSP servers

<Tip>
  Ищете способ использовать плагины LSP? Установите их из официального маркетплейса: найдите "lsp" на вкладке Discover в `/plugin`. Этот раздел документирует, как создавать плагины LSP для языков, не охватываемых официальным маркетплейсом.
</Tip>

Плагины могут предоставлять серверы [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) (LSP) для предоставления Claude интеллектуальной информации о коде в реальном времени при работе с вашей кодовой базой.

Интеграция LSP предоставляет:

* **Мгновенная диагностика**: Claude видит ошибки и предупреждения сразу после каждого редактирования
* **Навигация по коду**: переход к определению, поиск ссылок и информация при наведении
* **Осведомлённость о языке**: информация о типах и документация для символов кода

**Расположение**: `.lsp.json` в корне плагина или встроенный в `plugin.json`

**Формат**: Конфигурация JSON, сопоставляющая имена языковых серверов с их конфигурациями

**Формат файла `.lsp.json`**:

```json theme={null}
{
  "go": {
    "command": "gopls",
    "args": ["serve"],
    "extensionToLanguage": {
      ".go": "go"
    }
  }
}
```

**Встроенный в `plugin.json`**:

```json theme={null}
{
  "name": "my-plugin",
  "lspServers": {
    "go": {
      "command": "gopls",
      "args": ["serve"],
      "extensionToLanguage": {
        ".go": "go"
      }
    }
  }
}
```

**Обязательные поля:**

| Поле                  | Описание                                                 |
| :-------------------- | :------------------------------------------------------- |
| `command`             | Двоичный файл LSP для выполнения (должен быть в PATH)    |
| `extensionToLanguage` | Сопоставляет расширения файлов с идентификаторами языков |

**Опциональные поля:**

| Поле                    | Описание                                                          |
| :---------------------- | :---------------------------------------------------------------- |
| `args`                  | Аргументы командной строки для сервера LSP                        |
| `transport`             | Транспорт связи: `stdio` (по умолчанию) или `socket`              |
| `env`                   | Переменные окружения для установки при запуске сервера            |
| `initializationOptions` | Опции, передаваемые серверу при инициализации                     |
| `settings`              | Параметры, передаваемые через `workspace/didChangeConfiguration`  |
| `workspaceFolder`       | Путь папки рабочей области для сервера                            |
| `startupTimeout`        | Максимальное время ожидания запуска сервера (миллисекунды)        |
| `shutdownTimeout`       | Максимальное время ожидания корректного завершения (миллисекунды) |
| `restartOnCrash`        | Следует ли автоматически перезапустить сервер при сбое            |
| `maxRestarts`           | Максимальное количество попыток перезапуска перед отказом         |

<Warning>
  **Вы должны установить двоичный файл языкового сервера отдельно.** Плагины LSP настраивают способ подключения Claude Code к языковому серверу, но они не включают сам сервер. Если вы видите `Executable not found in $PATH` на вкладке Errors в `/plugin`, установите требуемый двоичный файл для вашего языка.
</Warning>

**Доступные плагины LSP:**

| Плагин              | Языковой сервер            | Команда установки                                                                            |
| :------------------ | :------------------------- | :------------------------------------------------------------------------------------------- |
| `pyright-lsp`       | Pyright (Python)           | `pip install pyright` или `npm install -g pyright`                                           |
| `typescript-lsp`    | TypeScript Language Server | `npm install -g typescript-language-server typescript`                                       |
| `rust-analyzer-lsp` | rust-analyzer              | [Смотрите установку rust-analyzer](https://rust-analyzer.github.io/manual.html#installation) |

Сначала установите языковой сервер, затем установите плагин из маркетплейса.

### Monitors

Плагины могут объявлять фоновые monitors, которые Claude Code автоматически запускает при активации плагина. Каждый monitor запускает команду оболочки на протяжении всего сеанса и доставляет каждую строку stdout Claude как уведомление, чтобы Claude мог реагировать на записи журнала, изменения статуса или опрашиваемые события без необходимости просить запустить наблюдение.

Плагины monitors используют тот же механизм, что и [инструмент Monitor](/ru/tools-reference#monitor-tool), и разделяют его ограничения доступности. Они работают только в интерактивных сеансах CLI, работают без песочницы на том же уровне доверия, что и [hooks](#hooks), и пропускаются на хостах, где инструмент Monitor недоступен.

<Note>
  Плагины monitors требуют Claude Code v2.1.105 или позже.
</Note>

**Расположение**: `monitors/monitors.json` в корне плагина или встроенный в `plugin.json`

**Формат**: Массив JSON записей monitor

Следующий `monitors/monitors.json` отслеживает конечную точку статуса развёртывания и локальный журнал ошибок:

```json theme={null}
[
  {
    "name": "deploy-status",
    "command": "${CLAUDE_PLUGIN_ROOT}/scripts/poll-deploy.sh ${user_config.api_endpoint}",
    "description": "Deployment status changes"
  },
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log",
    "when": "on-skill-invoke:debug"
  }
]
```

Для объявления monitors встроенным образом установите ключ `monitors` в `plugin.json` на тот же массив. Для загрузки из пути, отличного от пути по умолчанию, установите `monitors` на строку относительного пути, такую как `"./config/monitors.json"`.

**Обязательные поля:**

| Поле          | Описание                                                                                                                               |
| :------------ | :------------------------------------------------------------------------------------------------------------------------------------- |
| `name`        | Идентификатор, уникальный в пределах плагина. Предотвращает дублирование процессов при перезагрузке плагина или повторном вызове skill |
| `command`     | Команда оболочки, запускаемая как постоянный фоновый процесс в рабочем каталоге сеанса                                                 |
| `description` | Краткое резюме того, что отслеживается. Показывается в панели задач и в резюме уведомлений                                             |

**Опциональные поля:**

| Поле   | Описание                                                                                                                                                                                                                                                             |
| :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `when` | Управляет тем, когда запускается monitor. `"always"` запускает его при запуске сеанса и при перезагрузке плагина и является значением по умолчанию. `"on-skill-invoke:<skill-name>"` запускает его в первый раз, когда именованный skill в этом плагине отправляется |

Значение `command` поддерживает те же [подстановки переменных](#environment-variables), что и конфигурации серверов MCP и LSP: `${CLAUDE_PLUGIN_ROOT}`, `${CLAUDE_PLUGIN_DATA}`, `${user_config.*}` и любой `${ENV_VAR}` из окружения. Добавьте префикс команды с `cd "${CLAUDE_PLUGIN_ROOT}" && `, если скрипт должен работать из собственного каталога плагина.

Отключение плагина в середине сеанса не останавливает monitors, которые уже работают. Они останавливаются при завершении сеанса.

### Themes

Плагины могут поставлять цветовые темы, которые появляются в `/theme` наряду со встроенными предустановками и локальными темами пользователя. Тема — это JSON файл в `themes/` с предустановкой `base` и разреженной картой переопределений `overrides` цветовых токенов.

```json theme={null}
{
  "name": "Dracula",
  "base": "dark",
  "overrides": {
    "claude": "#bd93f9",
    "error": "#ff5555",
    "success": "#50fa7b"
  }
}
```

Выбор темы плагина сохраняет `custom:<plugin-name>:<slug>` в конфигурации пользователя. Темы плагина доступны только для чтения; нажатие `Ctrl+E` на одной из них в `/theme` копирует её в `~/.claude/themes/`, чтобы пользователь мог редактировать копию.

***

## Области установки плагина

При установке плагина вы выбираете **область**, которая определяет, где плагин доступен и кто ещё может его использовать:

| Область   | Файл параметров                                      | Вариант использования                                      |
| :-------- | :--------------------------------------------------- | :--------------------------------------------------------- |
| `user`    | `~/.claude/settings.json`                            | Личные плагины, доступные во всех проектах (по умолчанию)  |
| `project` | `.claude/settings.json`                              | Плагины команды, общие через контроль версий               |
| `local`   | `.claude/settings.local.json`                        | Плагины, специфичные для проекта, игнорируемые git         |
| `managed` | [Управляемые параметры](/ru/settings#settings-files) | Управляемые плагины (только для чтения, только обновление) |

Плагины используют ту же систему областей, что и другие конфигурации Claude Code. Для инструкций по установке и флагов области смотрите [Установка плагинов](/ru/discover-plugins#install-plugins). Для полного объяснения областей смотрите [Области конфигурации](/ru/settings#configuration-scopes).

***

## Схема манифеста плагина

Файл `.claude-plugin/plugin.json` определяет метаданные и конфигурацию вашего плагина. Этот раздел документирует все поддерживаемые поля и опции.

Манифест опционален. Если он опущен, Claude Code автоматически обнаруживает компоненты в [местоположениях по умолчанию](#file-locations-reference) и выводит имя плагина из имени каталога. Используйте манифест, когда вам нужно предоставить метаданные или пользовательские пути компонентов.

### Полная схема

```json theme={null}
{
  "name": "plugin-name",
  "version": "1.2.0",
  "description": "Brief plugin description",
  "author": {
    "name": "Author Name",
    "email": "author@example.com",
    "url": "https://github.com/author"
  },
  "homepage": "https://docs.example.com/plugin",
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "skills": "./custom/skills/",
  "commands": ["./custom/commands/special.md"],
  "agents": ["./custom/agents/reviewer.md"],
  "hooks": "./config/hooks.json",
  "mcpServers": "./mcp-config.json",
  "outputStyles": "./styles/",
  "themes": "./themes/",
  "lspServers": "./.lsp.json",
  "monitors": "./monitors.json",
  "dependencies": [
    "helper-lib",
    { "name": "secrets-vault", "version": "~2.1.0" }
  ]
}
```

### Обязательные поля

Если вы включаете манифест, `name` — единственное обязательное поле.

| Поле   | Тип    | Описание                                            | Пример               |
| :----- | :----- | :-------------------------------------------------- | :------------------- |
| `name` | string | Уникальный идентификатор (kebab-case, без пробелов) | `"deployment-tools"` |

Это имя используется для пространства имён компонентов. Например, в пользовательском интерфейсе агент `agent-creator` для плагина с именем `plugin-dev` будет отображаться как `plugin-dev:agent-creator`.

### Поля метаданных

| Поле          | Тип    | Описание                                                                                                                                                                                                                                                                                                                                                                                                                | Пример                                                            |
| :------------ | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------------------------------------------------------------- |
| `$schema`     | string | URL JSON Schema для автодополнения и валидации редактора. Claude Code игнорирует это поле при загрузке.                                                                                                                                                                                                                                                                                                                 | `"https://json.schemastore.org/claude-code-plugin-manifest.json"` |
| `version`     | string | Опционально. Семантическая версия. Установка этого параметра закрепляет плагин на этой строке версии, поэтому пользователи получают обновления только при её изменении. Если опущено, Claude Code использует SHA коммита git, поэтому каждый коммит рассматривается как новая версия. Если также установлено в записи маркетплейса, `plugin.json` имеет приоритет. Смотрите [Управление версиями](#version-management). | `"2.1.0"`                                                         |
| `description` | string | Краткое объяснение назначения плагина                                                                                                                                                                                                                                                                                                                                                                                   | `"Deployment automation tools"`                                   |
| `author`      | object | Информация об авторе                                                                                                                                                                                                                                                                                                                                                                                                    | `{"name": "Dev Team", "email": "dev@company.com"}`                |
| `homepage`    | string | URL документации                                                                                                                                                                                                                                                                                                                                                                                                        | `"https://docs.example.com"`                                      |
| `repository`  | string | URL исходного кода                                                                                                                                                                                                                                                                                                                                                                                                      | `"https://github.com/user/plugin"`                                |
| `license`     | string | Идентификатор лицензии                                                                                                                                                                                                                                                                                                                                                                                                  | `"MIT"`, `"Apache-2.0"`                                           |
| `keywords`    | array  | Теги обнаружения                                                                                                                                                                                                                                                                                                                                                                                                        | `["deployment", "ci-cd"]`                                         |

### Поля пути компонента

| Поле           | Тип                   | Описание                                                                                                                                                                            | Пример                                               |
| :------------- | :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------------------------------------------------- |
| `skills`       | string\|array         | Пользовательские каталоги skills, содержащие `<name>/SKILL.md` (заменяет по умолчанию `skills/`)                                                                                    | `"./custom/skills/"`                                 |
| `commands`     | string\|array         | Пользовательские плоские файлы `.md` skill или каталоги (заменяет по умолчанию `commands/`)                                                                                         | `"./custom/cmd.md"` или `["./cmd1.md"]`              |
| `agents`       | string\|array         | Пользовательские файлы агентов (заменяет по умолчанию `agents/`)                                                                                                                    | `"./custom/agents/reviewer.md"`                      |
| `hooks`        | string\|array\|object | Пути конфигурации hooks или встроенная конфигурация                                                                                                                                 | `"./my-extra-hooks.json"`                            |
| `mcpServers`   | string\|array\|object | Пути конфигурации MCP или встроенная конфигурация                                                                                                                                   | `"./my-extra-mcp-config.json"`                       |
| `outputStyles` | string\|array         | Пользовательские файлы/каталоги стилей вывода (заменяет по умолчанию `output-styles/`)                                                                                              | `"./styles/"`                                        |
| `themes`       | string\|array         | Файлы/каталоги цветовых тем (заменяет по умолчанию `themes/`). Смотрите [Themes](#themes)                                                                                           | `"./themes/"`                                        |
| `lspServers`   | string\|array\|object | Конфигурации [Language Server Protocol](https://microsoft.github.io/language-server-protocol/) для интеллектуальной информации о коде (переход к определению, поиск ссылок и т. д.) | `"./.lsp.json"`                                      |
| `monitors`     | string\|array         | Конфигурации фонового [Monitor](/ru/tools-reference#monitor-tool), которые запускаются автоматически при активации плагина. Смотрите [Monitors](#monitors)                          | `"./monitors.json"`                                  |
| `userConfig`   | object                | Значения, настраиваемые пользователем, запрашиваемые при включении. Смотрите [Конфигурация пользователя](#user-configuration)                                                       | Смотрите ниже                                        |
| `channels`     | array                 | Объявления каналов для внедрения сообщений (стиль Telegram, Slack, Discord). Смотрите [Каналы](#channels)                                                                           | Смотрите ниже                                        |
| `dependencies` | array                 | Другие плагины, которые требует этот плагин, опционально с ограничениями версии semver. Смотрите [Ограничение версий зависимостей плагина](/ru/plugin-dependencies)                 | `[{ "name": "secrets-vault", "version": "~2.1.0" }]` |

### Конфигурация пользователя

Поле `userConfig` объявляет значения, которые Claude Code запрашивает у пользователя при включении плагина. Используйте это вместо требования пользователям вручную редактировать `settings.json`.

```json theme={null}
{
  "userConfig": {
    "api_endpoint": {
      "type": "string",
      "title": "API endpoint",
      "description": "Your team's API endpoint"
    },
    "api_token": {
      "type": "string",
      "title": "API token",
      "description": "API authentication token",
      "sensitive": true
    }
  }
}
```

Ключи должны быть допустимыми идентификаторами. Каждое значение поддерживает эти поля:

| Поле          | Обязательно | Описание                                                                                      |
| :------------ | :---------- | :-------------------------------------------------------------------------------------------- |
| `type`        | Да          | Одно из `string`, `number`, `boolean`, `directory` или `file`                                 |
| `title`       | Да          | Метка, показываемая в диалоге конфигурации                                                    |
| `description` | Да          | Справочный текст, показываемый под полем                                                      |
| `sensitive`   | Нет         | Если `true`, скрывает ввод и сохраняет значение в защищённом хранилище вместо `settings.json` |
| `required`    | Нет         | Если `true`, проверка не пройдёт, когда поле пусто                                            |
| `default`     | Нет         | Значение, используемое, когда пользователь ничего не предоставляет                            |
| `multiple`    | Нет         | Для типа `string`, разрешить массив строк                                                     |
| `min` / `max` | Нет         | Границы для типа `number`                                                                     |

Каждое значение доступно для подстановки как `${user_config.KEY}` в конфигурациях серверов MCP и LSP, командах hooks и командах monitors. Нечувствительные значения также могут быть подставлены в содержимое skills и agents. Все значения экспортируются в подпроцессы плагина как переменные окружения `CLAUDE_PLUGIN_OPTION_<KEY>`.

Нечувствительные значения хранятся в `settings.json` под `pluginConfigs[<plugin-id>].options`. Чувствительные значения переходят в системный keychain (или `~/.claude/.credentials.json`, где keychain недоступен). Хранилище keychain общее с OAuth токенами и имеет приблизительный лимит 2 КБ, поэтому держите чувствительные значения небольшими.

### Каналы

Поле `channels` позволяет плагину объявить один или несколько каналов сообщений, которые внедряют содержимое в разговор. Каждый канал привязывается к серверу MCP, который предоставляет плагин.

```json theme={null}
{
  "channels": [
    {
      "server": "telegram",
      "userConfig": {
        "bot_token": {
          "type": "string",
          "title": "Bot token",
          "description": "Telegram bot token",
          "sensitive": true
        },
        "owner_id": {
          "type": "string",
          "title": "Owner ID",
          "description": "Your Telegram user ID"
        }
      }
    }
  ]
}
```

Поле `server` обязательно и должно соответствовать ключу в `mcpServers` плагина. Опциональный `userConfig` для каждого канала использует ту же схему, что и поле верхнего уровня, позволяя плагину запрашивать токены ботов или ID владельцев при включении плагина.

### Правила поведения пути

Для `skills`, `commands`, `agents`, `outputStyles`, `themes` и `monitors` пользовательский путь заменяет путь по умолчанию. Если манифест указывает `skills`, каталог по умолчанию `skills/` не сканируется; если он указывает `monitors`, по умолчанию `monitors/monitors.json` не загружается. [Hooks](#hooks), [MCP servers](#mcp-servers) и [LSP servers](#lsp-servers) имеют другую семантику для обработки нескольких источников.

* Все пути должны быть относительны к корню плагина и начинаться с `./`
* Компоненты из пользовательских путей используют те же правила именования и пространства имён
* Несколько путей можно указать как массивы
* Чтобы сохранить каталог по умолчанию и добавить дополнительные пути для skills, commands, agents или output styles, включите значение по умолчанию в ваш массив: `"skills": ["./skills/", "./extras/"]`
* Когда путь skill указывает на каталог, который содержит `SKILL.md` напрямую, например `"skills": ["./"]`, указывающий на корень плагина, поле frontmatter `name` в `SKILL.md` определяет имя вызова skill. Это обеспечивает стабильное имя независимо от каталога установки. Если `name` не установлен в frontmatter, в качестве резервного варианта используется имя каталога.

**Примеры путей**:

```json theme={null}
{
  "commands": [
    "./specialized/deploy.md",
    "./utilities/batch-process.md"
  ],
  "agents": [
    "./custom-agents/reviewer.md",
    "./custom-agents/tester.md"
  ]
}
```

### Переменные окружения

Claude Code предоставляет две переменные для ссылки на пути плагина. Обе подставляются встроенно везде, где они появляются в содержимом skills, содержимом agents, командах hooks, командах monitors и конфигурациях серверов MCP или LSP. Обе также экспортируются как переменные окружения в процессы hooks и подпроцессы серверов MCP или LSP.

**`${CLAUDE_PLUGIN_ROOT}`**: абсолютный путь к каталогу установки вашего плагина. Используйте это для ссылки на скрипты, двоичные файлы и файлы конфигурации, поставляемые с плагином. Этот путь изменяется при обновлении плагина. Каталог предыдущей версии остаётся на диске примерно семь дней после обновления перед очисткой, но рассматривайте его как временный и не записывайте состояние здесь.

Когда плагин обновляется во время сеанса, команды hooks, monitors, серверы MCP и серверы LSP продолжают использовать путь предыдущей версии. Запустите `/reload-plugins` для переключения hooks, серверов MCP и серверов LSP на новый путь; monitors требуют перезагрузки сеанса.

**`${CLAUDE_PLUGIN_DATA}`**: постоянный каталог для состояния плагина, который сохраняется при обновлениях. Используйте это для установленных зависимостей, таких как `node_modules` или виртуальные окружения Python, сгенерированный код, кэши и любые другие файлы, которые должны сохраняться между версиями плагина. Каталог создаётся автоматически при первом обращении к этой переменной.

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/process.sh"
          }
        ]
      }
    ]
  }
}
```

#### Каталог постоянных данных

Каталог `${CLAUDE_PLUGIN_DATA}` разрешается в `~/.claude/plugins/data/{id}/`, где `{id}` — это идентификатор плагина с символами вне `a-z`, `A-Z`, `0-9`, `_` и `-`, заменённые на `-`. Для плагина, установленного как `formatter@my-marketplace`, каталог — это `~/.claude/plugins/data/formatter-my-marketplace/`.

Распространённое использование — установка языковых зависимостей один раз и их повторное использование в сеансах и обновлениях плагина. Поскольку каталог данных пережидает любую отдельную версию плагина, проверка только существования каталога не может обнаружить, когда обновление изменяет манифест зависимостей плагина. Рекомендуемый паттерн сравнивает поставляемый манифест с копией в каталоге данных и переустанавливает при различиях.

Этот hook `SessionStart` устанавливает `node_modules` при первом запуске и снова всякий раз, когда обновление плагина включает изменённый `package.json`:

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/package.json\" \"${CLAUDE_PLUGIN_DATA}/package.json\" >/dev/null 2>&1 || (cd \"${CLAUDE_PLUGIN_DATA}\" && cp \"${CLAUDE_PLUGIN_ROOT}/package.json\" . && npm install) || rm -f \"${CLAUDE_PLUGIN_DATA}/package.json\""
          }
        ]
      }
    ]
  }
}
```

`diff` выходит с ненулевым кодом, когда сохранённая копия отсутствует или отличается от поставляемой, охватывая как первый запуск, так и обновления, изменяющие зависимости. Если `npm install` не удаётся, завершающий `rm` удаляет скопированный манифест, чтобы следующий сеанс повторил попытку.

Скрипты, поставляемые в `${CLAUDE_PLUGIN_ROOT}`, затем могут работать с сохранённым `node_modules`:

```json theme={null}
{
  "mcpServers": {
    "routines": {
      "command": "node",
      "args": ["${CLAUDE_PLUGIN_ROOT}/server.js"],
      "env": {
        "NODE_PATH": "${CLAUDE_PLUGIN_DATA}/node_modules"
      }
    }
  }
}
```

Каталог данных удаляется автоматически при удалении плагина из последней области, где он установлен. Интерфейс `/plugin` показывает размер каталога и запрашивает перед удалением. CLI удаляет по умолчанию; передайте [`--keep-data`](#plugin-uninstall) для сохранения.

***

## Кэширование плагина и разрешение файлов

Плагины указываются одним из двух способов:

* Через `claude --plugin-dir`, на время сеанса.
* Через маркетплейс, установленный для будущих сеансов.

В целях безопасности и проверки Claude Code копирует плагины *маркетплейса* в локальный **кэш плагина** пользователя (`~/.claude/plugins/cache`) вместо использования их на месте. Понимание этого поведения важно при разработке плагинов, которые ссылаются на внешние файлы.

Каждая установленная версия — это отдельный каталог в кэше. Когда вы обновляете или удаляете плагин, предыдущий каталог версии помечается как сиротский и удаляется автоматически через 7 дней. Период отсрочки позволяет одновременным сеансам Claude Code, которые уже загрузили старую версию, продолжать работу без ошибок.

Инструменты Glob и Grep Claude пропускают сиротские каталоги версий при поиске, поэтому результаты файлов не включают устаревший код плагина.

### Ограничения обхода пути

Установленные плагины не могут ссылаться на файлы вне их каталога. Пути, которые выходят за пределы корня плагина (такие как `../shared-utils`), не будут работать после установки, потому что эти внешние файлы не копируются в кэш.

### Работа с внешними зависимостями

Если вашему плагину нужно получить доступ к файлам вне его каталога, вы можете создать символические ссылки на внешние файлы в каталоге вашего плагина. Символические ссылки сохраняются в кэше, а не разыменовываются, и они разрешаются к своей цели во время выполнения. Следующая команда создаёт ссылку из каталога вашего плагина на местоположение общих утилит:

```bash theme={null}
ln -s /path/to/shared-utils ./shared-utils
```

Это обеспечивает гибкость при сохранении преимуществ безопасности системы кэширования.

***

## Структура каталога плагина

### Стандартная раскладка плагина

Полный плагин следует этой структуре:

```text theme={null}
enterprise-plugin/
├── .claude-plugin/           # Каталог метаданных (опционально)
│   └── plugin.json             # манифест плагина
├── skills/                   # Skills
│   ├── code-reviewer/
│   │   └── SKILL.md
│   └── pdf-processor/
│       ├── SKILL.md
│       └── scripts/
├── commands/                 # Skills как плоские файлы .md
│   ├── status.md
│   └── logs.md
├── agents/                   # Определения subagent
│   ├── security-reviewer.md
│   ├── performance-tester.md
│   └── compliance-checker.md
├── output-styles/            # Определения стиля вывода
│   └── terse.md
├── themes/                   # Определения цветовой темы
│   └── dracula.json
├── monitors/                 # Конфигурации фонового monitor
│   └── monitors.json
├── hooks/                    # Конфигурации hook
│   ├── hooks.json           # Основная конфигурация hook
│   └── security-hooks.json  # Дополнительные hooks
├── bin/                      # Исполняемые файлы плагина, добавленные в PATH
│   └── my-tool               # Вызываемый как голая команда в инструменте Bash
├── settings.json            # Параметры по умолчанию для плагина
├── .mcp.json                # Определения сервера MCP
├── .lsp.json                # Конфигурации сервера LSP
├── scripts/                 # Скрипты hook и утилиты
│   ├── security-scan.sh
│   ├── format-code.py
│   └── deploy.js
├── LICENSE                  # Файл лицензии
└── CHANGELOG.md             # История версий
```

<Warning>
  Каталог `.claude-plugin/` содержит файл `plugin.json`. Все остальные каталоги (commands/, agents/, skills/, output-styles/, themes/, monitors/, hooks/) должны быть в корне плагина, а не внутри `.claude-plugin/`.
</Warning>

Файл `CLAUDE.md` в корне плагина не загружается как контекст проекта. Плагины предоставляют контекст через skills, agents и hooks, а не через CLAUDE.md. Чтобы отправить инструкции, которые загружаются в контекст Claude, поместите их в [skill](#skills).

### Справочник местоположений файлов

| Компонент         | Местоположение по умолчанию  | Назначение                                                                                                                                                                                           |
| :---------------- | :--------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Манифест**      | `.claude-plugin/plugin.json` | Метаданные и конфигурация плагина (опционально)                                                                                                                                                      |
| **Skills**        | `skills/`                    | Skills со структурой `<name>/SKILL.md`                                                                                                                                                               |
| **Commands**      | `commands/`                  | Skills как плоские файлы Markdown. Используйте `skills/` для новых плагинов                                                                                                                          |
| **Agents**        | `agents/`                    | Файлы Subagent Markdown                                                                                                                                                                              |
| **Output styles** | `output-styles/`             | Определения стиля вывода                                                                                                                                                                             |
| **Themes**        | `themes/`                    | Определения цветовой темы                                                                                                                                                                            |
| **Hooks**         | `hooks/hooks.json`           | Конфигурация hook                                                                                                                                                                                    |
| **MCP servers**   | `.mcp.json`                  | Определения сервера MCP                                                                                                                                                                              |
| **LSP servers**   | `.lsp.json`                  | Конфигурации языкового сервера                                                                                                                                                                       |
| **Monitors**      | `monitors/monitors.json`     | Конфигурации фонового monitor                                                                                                                                                                        |
| **Executables**   | `bin/`                       | Исполняемые файлы, добавленные в PATH инструмента Bash. Файлы здесь вызываются как голые команды в любом вызове инструмента Bash, пока плагин включен                                                |
| **Settings**      | `settings.json`              | Конфигурация по умолчанию, применяемая при включении плагина. В настоящее время поддерживаются только ключи [`agent`](/ru/sub-agents) и [`subagentStatusLine`](/ru/statusline#subagent-status-lines) |

***

## Справочник команд CLI

Claude Code предоставляет команды CLI для неинтерактивного управления плагинами, полезные для написания скриптов и автоматизации.

### plugin install

Установите плагин из доступных маркетплейсов.

```bash theme={null}
claude plugin install <plugin> [options]
```

**Аргументы:**

* `<plugin>`: Имя плагина или `plugin-name@marketplace-name` для конкретного маркетплейса

**Опции:**

| Опция                 | Описание                                         | По умолчанию |
| :-------------------- | :----------------------------------------------- | :----------- |
| `-s, --scope <scope>` | Область установки: `user`, `project` или `local` | `user`       |
| `-h, --help`          | Отобразить справку для команды                   |              |

Область определяет, в какой файл параметров добавляется установленный плагин. Например, `--scope project` записывает в `enabledPlugins` в .claude/settings.json, делая плагин доступным для всех, кто клонирует репозиторий проекта.

**Примеры:**

```bash theme={null}
# Установить в область пользователя (по умолчанию)
claude plugin install formatter@my-marketplace

# Установить в область проекта (общее с командой)
claude plugin install formatter@my-marketplace --scope project

# Установить в локальную область (игнорируется git)
claude plugin install formatter@my-marketplace --scope local
```

### plugin uninstall

Удалите установленный плагин.

```bash theme={null}
claude plugin uninstall <plugin> [options]
```

**Аргументы:**

* `<plugin>`: Имя плагина или `plugin-name@marketplace-name`

**Опции:**

| Опция                 | Описание                                                                                                                       | По умолчанию |
| :-------------------- | :----------------------------------------------------------------------------------------------------------------------------- | :----------- |
| `-s, --scope <scope>` | Удалить из области: `user`, `project` или `local`                                                                              | `user`       |
| `--keep-data`         | Сохранить [каталог постоянных данных](#persistent-data-directory) плагина                                                      |              |
| `--prune`             | Также удалить автоматически установленные зависимости, которые не требуются другим плагинам. См. [plugin prune](#plugin-prune) |              |
| `-y, --yes`           | Пропустить подтверждение `--prune`. Требуется, когда stdin не является TTY                                                     |              |
| `-h, --help`          | Отобразить справку для команды                                                                                                 |              |

**Псевдонимы:** `remove`, `rm`

По умолчанию удаление из последней оставшейся области также удаляет каталог `${CLAUDE_PLUGIN_DATA}` плагина. Используйте `--keep-data` для сохранения, например при переустановке после тестирования новой версии.

### plugin prune

Удалите автоматически установленные зависимости плагинов, которые больше не требуются ни одному установленному плагину. Зависимости, которые Claude Code подтянул для удовлетворения поля [`dependencies`](/ru/plugin-dependencies) другого плагина, удаляются; плагины, которые вы установили напрямую, никогда не затрагиваются.

```bash theme={null}
claude plugin prune [options]
```

**Опции:**

| Опция                 | Описание                                                         | По умолчанию |
| :-------------------- | :--------------------------------------------------------------- | :----------- |
| `-s, --scope <scope>` | Очистить в области: `user`, `project` или `local`                | `user`       |
| `--dry-run`           | Список того, что будет удалено, без фактического удаления        |              |
| `-y, --yes`           | Пропустить подтверждение. Требуется, когда stdin не является TTY |              |
| `-h, --help`          | Отобразить справку для команды                                   |              |

**Псевдонимы:** `autoremove`

Команда выводит список потерянных зависимостей и запрашивает подтверждение перед их удалением. Чтобы удалить плагин и очистить его зависимости в один шаг, запустите `claude plugin uninstall <plugin> --prune`.

<Note>
  `claude plugin prune` требует Claude Code v2.1.121 или более поздней версии.
</Note>

### plugin enable

Включите отключённый плагин.

```bash theme={null}
claude plugin enable <plugin> [options]
```

**Аргументы:**

* `<plugin>`: Имя плагина или `plugin-name@marketplace-name`

**Опции:**

| Опция                 | Описание                                             | По умолчанию |
| :-------------------- | :--------------------------------------------------- | :----------- |
| `-s, --scope <scope>` | Область для включения: `user`, `project` или `local` | `user`       |
| `-h, --help`          | Отобразить справку для команды                       |              |

### plugin disable

Отключите плагин без его удаления.

```bash theme={null}
claude plugin disable <plugin> [options]
```

**Аргументы:**

* `<plugin>`: Имя плагина или `plugin-name@marketplace-name`

**Опции:**

| Опция                 | Описание                                              | По умолчанию |
| :-------------------- | :---------------------------------------------------- | :----------- |
| `-s, --scope <scope>` | Область для отключения: `user`, `project` или `local` | `user`       |
| `-h, --help`          | Отобразить справку для команды                        |              |

### plugin update

Обновите плагин до последней версии.

```bash theme={null}
claude plugin update <plugin> [options]
```

**Аргументы:**

* `<plugin>`: Имя плагина или `plugin-name@marketplace-name`

**Опции:**

| Опция                 | Описание                                                         | По умолчанию |
| :-------------------- | :--------------------------------------------------------------- | :----------- |
| `-s, --scope <scope>` | Область для обновления: `user`, `project`, `local` или `managed` | `user`       |
| `-h, --help`          | Отобразить справку для команды                                   |              |

***

### plugin list

Список установленных плагинов с их версией, источником маркетплейса и статусом включения.

```bash theme={null}
claude plugin list [options]
```

**Опции:**

| Опция         | Описание                                                      | По умолчанию |
| :------------ | :------------------------------------------------------------ | :----------- |
| `--json`      | Вывести как JSON                                              |              |
| `--available` | Включить доступные плагины из маркетплейсов. Требует `--json` |              |
| `-h, --help`  | Отобразить справку для команды                                |              |

### plugin tag

Создайте тег выпуска git для плагина в текущем каталоге. Запустите из папки плагина. См. [Теги выпусков плагинов](/ru/plugin-dependencies#tag-plugin-releases-for-version-resolution).

```bash theme={null}
claude plugin tag [options]
```

**Опции:**

| Опция         | Описание                                                            | По умолчанию |
| :------------ | :------------------------------------------------------------------ | :----------- |
| `--push`      | Отправить тег на удалённый репозиторий после его создания           |              |
| `--dry-run`   | Вывести, что будет помечено тегом, без создания самого тега         |              |
| `-f, --force` | Создать тег даже если рабочее дерево грязное или тег уже существует |              |
| `-h, --help`  | Отобразить справку для команды                                      |              |

***

## Инструменты отладки и разработки

### Команды отладки

Используйте `claude --debug` для просмотра деталей загрузки плагина:

Это показывает:

* Какие плагины загружаются
* Любые ошибки в манифестах плагинов
* Регистрацию skill, agent и hook
* Инициализацию сервера MCP

### Распространённые проблемы

| Проблема                            | Причина                             | Решение                                                                                                                                                                |
| :---------------------------------- | :---------------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Плагин не загружается               | Неверный `plugin.json`              | Запустите `claude plugin validate` или `/plugin validate` для проверки `plugin.json`, frontmatter skill/agent/command и `hooks/hooks.json` на синтаксис и ошибки схемы |
| Skills не отображаются              | Неправильная структура каталога     | Убедитесь, что `skills/` или `commands/` находится в корне плагина, а не в `.claude-plugin/`                                                                           |
| Hooks не срабатывают                | Скрипт не исполняемый               | Запустите `chmod +x script.sh`                                                                                                                                         |
| Сервер MCP не работает              | Отсутствует `${CLAUDE_PLUGIN_ROOT}` | Используйте переменную для всех путей плагина                                                                                                                          |
| Ошибки пути                         | Используются абсолютные пути        | Все пути должны быть относительными и начинаться с `./`                                                                                                                |
| LSP `Executable not found in $PATH` | Языковой сервер не установлен       | Установите двоичный файл (например, `npm install -g typescript-language-server typescript`)                                                                            |

### Примеры сообщений об ошибках

**Ошибки проверки манифеста**:

* `Invalid JSON syntax: Unexpected token } in JSON at position 142`: проверьте наличие пропущенных запятых, лишних запятых или неквотированных строк
* `Plugin has an invalid manifest file at .claude-plugin/plugin.json. Validation errors: name: Required`: отсутствует обязательное поле
* `Plugin has a corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`: ошибка синтаксиса JSON

**Ошибки загрузки плагина**:

* `Warning: No commands found in plugin my-plugin custom directory: ./cmds. Expected .md files or SKILL.md in subdirectories.`: путь команды существует, но не содержит действительных файлов команд
* `Plugin directory not found at path: ./plugins/my-plugin. Check that the marketplace entry has the correct path.`: путь `source` в marketplace.json указывает на несуществующий каталог
* `Plugin my-plugin has conflicting manifests: both plugin.json and marketplace entry specify components.`: удалите дублирующиеся определения компонентов или удалите `strict: false` в записи маркетплейса

### Устранение неполадок Hook

**Скрипт hook не выполняется**:

1. Проверьте, что скрипт исполняемый: `chmod +x ./scripts/your-script.sh`
2. Проверьте строку shebang: Первая строка должна быть `#!/bin/bash` или `#!/usr/bin/env bash`
3. Проверьте, что путь использует `${CLAUDE_PLUGIN_ROOT}`: `"command": "${CLAUDE_PLUGIN_ROOT}/scripts/your-script.sh"`
4. Протестируйте скрипт вручную: `./scripts/your-script.sh`

**Hook не срабатывает на ожидаемых событиях**:

1. Проверьте, что имя события правильное (чувствительно к регистру): `PostToolUse`, а не `postToolUse`
2. Проверьте, что шаблон сопоставления соответствует вашим инструментам: `"matcher": "Write|Edit"` для операций с файлами
3. Подтвердите, что тип hook действителен: `command`, `http`, `mcp_tool`, `prompt` или `agent`

### Устранение неполадок сервера MCP

**Сервер не запускается**:

1. Проверьте, что команда существует и исполняемая
2. Проверьте, что все пути используют переменную `${CLAUDE_PLUGIN_ROOT}`
3. Проверьте журналы сервера MCP: `claude --debug` показывает ошибки инициализации
4. Протестируйте сервер вручную вне Claude Code

**Инструменты сервера не отображаются**:

1. Убедитесь, что сервер правильно настроен в `.mcp.json` или `plugin.json`
2. Проверьте, что сервер правильно реализует протокол MCP
3. Проверьте наличие тайм-аутов соединения в выводе отладки

### Ошибки структуры каталога

**Симптомы**: Плагин загружается, но компоненты (skills, agents, hooks) отсутствуют.

**Правильная структура**: Компоненты должны быть в корне плагина, а не внутри `.claude-plugin/`. Только `plugin.json` должен быть в `.claude-plugin/`.

```text theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json      ← Только манифест здесь
├── commands/            ← На уровне корня
├── agents/              ← На уровне корня
└── hooks/               ← На уровне корня
```

Если ваши компоненты находятся внутри `.claude-plugin/`, переместите их в корень плагина.

**Контрольный список отладки**:

1. Запустите `claude --debug` и ищите сообщения "loading plugin"
2. Проверьте, что каждый каталог компонента указан в выводе отладки
3. Проверьте, что разрешения файлов позволяют читать файлы плагина

***

## Справочник по распространению и версионированию

### Управление версиями

Claude Code использует версию плагина в качестве ключа кэша, который определяет, доступно ли обновление. Когда вы запускаете `/plugin update` или срабатывает автоматическое обновление, Claude Code вычисляет текущую версию и пропускает обновление, если она совпадает с уже установленной.

Версия определяется из первого из следующих параметров, который установлен:

1. Поле `version` в `plugin.json` плагина
2. Поле `version` в записи плагина на маркетплейсе в `marketplace.json`
3. SHA коммита git источника плагина для источников `github`, `url`, `git-subdir` и relative-path в маркетплейсе, размещённом на git
4. `unknown` для источников `npm` или локальных каталогов, не находящихся в репозитории git

Это дает вам два способа версионирования плагина:

| Подход                 | Как                                                       | Поведение обновления                                                                                                                                                                        | Лучше всего для                                        |
| :--------------------- | :-------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :----------------------------------------------------- |
| **Явная версия**       | Установите `"version": "2.1.0"` в `plugin.json`           | Пользователи получают обновления только когда вы обновляете это поле. Отправка новых коммитов без обновления не имеет эффекта, и `/plugin update` сообщает "already at the latest version". | Опубликованные плагины со стабильными циклами выпуска  |
| **Версия коммита SHA** | Опустите `version` из `plugin.json` и записи маркетплейса | Пользователи получают обновления при каждом новом коммите в источник git плагина                                                                                                            | Внутренние или командные плагины в активной разработке |

<Warning>
  Если вы установите `version` в `plugin.json`, вы должны обновлять его каждый раз, когда хотите, чтобы пользователи получили изменения. Отправка новых коммитов недостаточна, потому что Claude Code видит ту же строку версии и сохраняет кэшированную копию. Если вы быстро итерируете, оставьте `version` неустановленным, чтобы вместо этого использовалась SHA коммита git.
</Warning>

Если вы используете явные версии, следуйте [семантическому версионированию](https://semver.org) (`MAJOR.MINOR.PATCH`): обновляйте MAJOR для критических изменений, MINOR для новых функций, PATCH для исправлений ошибок. Документируйте изменения в `CHANGELOG.md`.

***

## Смотрите также

* [Плагины](/ru/plugins) - Учебные материалы и практическое использование
* [Маркетплейсы плагинов](/ru/plugin-marketplaces) - Создание и управление маркетплейсами
* [Skills](/ru/skills) - Детали разработки skills
* [Subagents](/ru/sub-agents) - Конфигурация и возможности агентов
* [Hooks](/ru/hooks) - Обработка событий и автоматизация
* [MCP](/ru/mcp) - Интеграция внешних инструментов
* [Параметры](/ru/settings) - Опции конфигурации для плагинов
