> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Создание plugins

> Создавайте пользовательские plugins для расширения Claude Code с помощью skills, agents, hooks и MCP servers.

Plugins позволяют расширить Claude Code пользовательской функциональностью, которая может быть общей для проектов и команд. Это руководство охватывает создание собственных plugins с skills, agents, hooks и MCP servers.

Ищете установку существующих plugins? См. [Обнаружение и установка plugins](/ru/discover-plugins). Для полных технических спецификаций см. [Справочник plugins](/ru/plugins-reference).

## Когда использовать plugins в сравнении с автономной конфигурацией

Claude Code поддерживает два способа добавления пользовательских skills, agents и hooks:

| Подход                                                  | Имена Skill          | Лучше всего для                                                                                                            |
| :------------------------------------------------------ | :------------------- | :------------------------------------------------------------------------------------------------------------------------- |
| **Автономная** (директория `.claude/`)                  | `/hello`             | Личные рабочие процессы, настройки для конкретного проекта, быстрые эксперименты                                           |
| **Plugins** (директории с `.claude-plugin/plugin.json`) | `/plugin-name:hello` | Совместное использование с коллегами, распространение в сообществе, версионные выпуски, повторное использование в проектах |

**Используйте автономную конфигурацию когда**:

* Вы настраиваете Claude Code для одного проекта
* Конфигурация личная и не требует совместного использования
* Вы экспериментируете с skills или hooks перед их упаковкой
* Вы хотите короткие имена skills, такие как `/hello` или `/deploy`

**Используйте plugins когда**:

* Вы хотите поделиться функциональностью с вашей командой или сообществом
* Вам нужны одинаковые skills/agents в нескольких проектах
* Вы хотите контроль версий и простые обновления для ваших расширений
* Вы распространяете через marketplace
* Вы согласны с пространством имён skills, такими как `/my-plugin:hello` (пространство имён предотвращает конфликты между plugins)

<Tip>
  Начните с автономной конфигурации в `.claude/` для быстрой итерации, затем [преобразуйте в plugin](#convert-existing-configurations-to-plugins) когда будете готовы поделиться.
</Tip>

## Быстрый старт

Этот быстрый старт проведёт вас через создание plugin с пользовательским skill. Вы создадите манифест (файл конфигурации, который определяет ваш plugin), добавите skill и протестируете его локально, используя флаг `--plugin-dir`.

### Предварительные требования

* Claude Code [установлен и аутентифицирован](/ru/quickstart#step-1-install-claude-code)

<Note>
  Если вы не видите команду `/plugin`, обновите Claude Code до последней версии. См. [Troubleshooting](/ru/troubleshooting) для инструкций по обновлению.
</Note>

### Создайте ваш первый plugin

<Steps>
  <Step title="Создайте директорию plugin">
    Каждый plugin находится в собственной директории, содержащей манифест и ваши skills, agents или hooks. Создайте её сейчас:

    ```bash theme={null}
    mkdir my-first-plugin
    ```
  </Step>

  <Step title="Создайте манифест plugin">
    Файл манифеста в `.claude-plugin/plugin.json` определяет идентичность вашего plugin: его имя, описание и версию. Claude Code использует эти метаданные для отображения вашего plugin в менеджере plugins.

    Создайте директорию `.claude-plugin` внутри папки вашего plugin:

    ```bash theme={null}
    mkdir my-first-plugin/.claude-plugin
    ```

    Затем создайте `my-first-plugin/.claude-plugin/plugin.json` с этим содержимым:

    ```json my-first-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "my-first-plugin",
      "description": "A greeting plugin to learn the basics",
      "version": "1.0.0",
      "author": {
        "name": "Your Name"
      }
    }
    ```

    | Поле          | Назначение                                                                                                           |
    | :------------ | :------------------------------------------------------------------------------------------------------------------- |
    | `name`        | Уникальный идентификатор и пространство имён skill. Skills имеют префикс этого (например, `/my-first-plugin:hello`). |
    | `description` | Показывается в менеджере plugins при просмотре или установке plugins.                                                |
    | `version`     | Отслеживайте выпуски, используя [семантическое версионирование](/ru/plugins-reference#version-management).           |
    | `author`      | Опционально. Полезно для атрибуции.                                                                                  |

    Для дополнительных полей, таких как `homepage`, `repository` и `license`, см. [полную схему манифеста](/ru/plugins-reference#plugin-manifest-schema).
  </Step>

  <Step title="Добавьте skill">
    Skills находятся в директории `skills/`. Каждый skill — это папка, содержащая файл `SKILL.md`. Имя папки становится именем skill, с префиксом пространства имён plugin (`hello/` в plugin с именем `my-first-plugin` создаёт `/my-first-plugin:hello`).

    Создайте директорию skill в папке вашего plugin:

    ```bash theme={null}
    mkdir -p my-first-plugin/skills/hello
    ```

    Затем создайте `my-first-plugin/skills/hello/SKILL.md` с этим содержимым:

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    description: Greet the user with a friendly message
    disable-model-invocation: true
    ---

    Greet the user warmly and ask how you can help them today.
    ```
  </Step>

  <Step title="Протестируйте ваш plugin">
    Запустите Claude Code с флагом `--plugin-dir` для загрузки вашего plugin:

    ```bash theme={null}
    claude --plugin-dir ./my-first-plugin
    ```

    После запуска Claude Code попробуйте ваш новый skill:

    ```shell theme={null}
    /my-first-plugin:hello
    ```

    Вы увидите, как Claude ответит приветствием. Запустите `/help` для просмотра вашего skill, указанного в пространстве имён plugin.

    <Note>
      **Почему пространство имён?** Skills plugin всегда имеют пространство имён (например, `/my-first-plugin:hello`) для предотвращения конфликтов, когда несколько plugins имеют skills с одинаковым именем.

      Чтобы изменить префикс пространства имён, обновите поле `name` в `plugin.json`.
    </Note>
  </Step>

  <Step title="Добавьте аргументы skill">
    Сделайте ваш skill динамичным, принимая пользовательский ввод. Заполнитель `$ARGUMENTS` захватывает любой текст, который пользователь предоставляет после имени skill.

    Обновите ваш файл `SKILL.md`:

    ```markdown my-first-plugin/skills/hello/SKILL.md theme={null}
    ---
    description: Greet the user with a personalized message
    ---

    # Hello Skill

    Greet the user named "$ARGUMENTS" warmly and ask how you can help them today. Make the greeting personal and encouraging.
    ```

    Запустите `/reload-plugins` для применения изменений, затем попробуйте skill с вашим именем:

    ```shell theme={null}
    /my-first-plugin:hello Alex
    ```

    Claude поприветствует вас по имени. Для получения дополнительной информации о передаче аргументов в skills см. [Skills](/ru/skills#pass-arguments-to-skills).
  </Step>
</Steps>

Вы успешно создали и протестировали plugin с этими ключевыми компонентами:

* **Манифест plugin** (`.claude-plugin/plugin.json`): описывает метаданные вашего plugin
* **Директория skills** (`skills/`): содержит ваши пользовательские skills
* **Аргументы skill** (`$ARGUMENTS`): захватывает пользовательский ввод для динамического поведения

<Tip>
  Флаг `--plugin-dir` полезен для разработки и тестирования. Когда вы будете готовы поделиться вашим plugin с другими, см. [Создание и распространение marketplace plugin](/ru/plugin-marketplaces).
</Tip>

## Обзор структуры plugin

Вы создали plugin с skill, но plugins могут включать намного больше: пользовательские agents, hooks, MCP servers и LSP servers.

<Warning>
  **Частая ошибка**: Не помещайте `commands/`, `agents/`, `skills/` или `hooks/` внутри директории `.claude-plugin/`. Только `plugin.json` находится внутри `.claude-plugin/`. Все остальные директории должны быть на уровне корня plugin.
</Warning>

| Директория        | Местоположение | Назначение                                                                                            |
| :---------------- | :------------- | :---------------------------------------------------------------------------------------------------- |
| `.claude-plugin/` | Корень plugin  | Содержит манифест `plugin.json` (опционально, если компоненты используют местоположения по умолчанию) |
| `skills/`         | Корень plugin  | Skills как директории `<name>/SKILL.md`                                                               |
| `commands/`       | Корень plugin  | Skills как плоские файлы Markdown. Используйте `skills/` для новых plugins                            |
| `agents/`         | Корень plugin  | Определения пользовательских agents                                                                   |
| `hooks/`          | Корень plugin  | Обработчики событий в `hooks.json`                                                                    |
| `.mcp.json`       | Корень plugin  | Конфигурации MCP server                                                                               |
| `.lsp.json`       | Корень plugin  | Конфигурации LSP server для интеллекта кода                                                           |
| `monitors/`       | Корень plugin  | Конфигурации фонового монитора в `monitors.json`                                                      |
| `bin/`            | Корень plugin  | Исполняемые файлы, добавленные в `PATH` инструмента Bash во время включения plugin                    |
| `settings.json`   | Корень plugin  | Параметры по умолчанию [settings](/ru/settings), применяемые при включении plugin                     |

<Note>
  **Следующие шаги**: Готовы добавить больше функций? Перейдите к [Разработка более сложных plugins](#develop-more-complex-plugins) для добавления agents, hooks, MCP servers и LSP servers. Для полных технических спецификаций всех компонентов plugin см. [Справочник plugins](/ru/plugins-reference).
</Note>

## Разработка более сложных plugins

Когда вы будете комфортно чувствовать себя с базовыми plugins, вы сможете создавать более сложные расширения.

### Добавьте Skills в ваш plugin

Plugins могут включать [Agent Skills](/ru/skills) для расширения возможностей Claude. Skills вызываются моделью: Claude автоматически использует их на основе контекста задачи.

Добавьте директорию `skills/` в корень вашего plugin с папками Skill, содержащими файлы `SKILL.md`:

```text theme={null}
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── code-review/
        └── SKILL.md
```

Каждый `SKILL.md` содержит YAML frontmatter и инструкции. Включите `description` чтобы Claude знал, когда использовать skill:

```yaml theme={null}
---
description: Reviews code for best practices and potential issues. Use when reviewing code, checking PRs, or analyzing code quality.
---

When reviewing code, check for:
1. Code organization and structure
2. Error handling
3. Security concerns
4. Test coverage
```

После установки plugin запустите `/reload-plugins` для загрузки Skills. Для полного руководства по созданию Skill, включая прогрессивное раскрытие и ограничения инструментов, см. [Agent Skills](/ru/skills).

### Добавьте LSP servers в ваш plugin

<Tip>
  Для распространённых языков, таких как TypeScript, Python и Rust, установите предварительно созданные LSP plugins из официального marketplace. Создавайте пользовательские LSP plugins только когда вам нужна поддержка языков, которые ещё не охвачены.
</Tip>

LSP (Language Server Protocol) plugins дают Claude интеллект кода в реальном времени. Если вам нужна поддержка языка, который не имеет официального LSP plugin, вы можете создать свой собственный, добавив файл `.lsp.json` в ваш plugin:

```json .lsp.json theme={null}
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

Пользователи, устанавливающие ваш plugin, должны иметь двоичный файл языкового сервера, установленный на их машине.

Для полных опций конфигурации LSP см. [LSP servers](/ru/plugins-reference#lsp-servers).

### Добавьте фоновые мониторы в ваш plugin

Фоновые мониторы позволяют вашему plugin отслеживать логи, файлы или внешний статус в фоне и уведомлять Claude по мере поступления событий. Claude Code автоматически запускает каждый монитор при активации plugin, поэтому вам не нужно инструктировать Claude запустить наблюдение.

Добавьте файл `monitors/monitors.json` в корень plugin с массивом записей монитора:

```json monitors/monitors.json theme={null}
[
  {
    "name": "error-log",
    "command": "tail -F ./logs/error.log",
    "description": "Application error log"
  }
]
```

Каждая строка stdout из `command` доставляется Claude как уведомление во время сеанса. Для полной схемы, включая триггер `when` и подстановку переменных, см. [Monitors](/ru/plugins-reference#monitors).

### Поставляйте параметры по умолчанию с вашим plugin

Plugins могут включать файл `settings.json` в корне plugin для применения конфигурации по умолчанию при включении plugin. В настоящее время поддерживаются только ключи `agent` и `subagentStatusLine`.

Установка `agent` активирует один из [пользовательских agents](/ru/sub-agents) plugin в качестве основного потока, применяя его системный prompt, ограничения инструментов и модель. Это позволяет plugin изменить поведение Claude Code по умолчанию при включении.

```json settings.json theme={null}
{
  "agent": "security-reviewer"
}
```

Этот пример активирует agent `security-reviewer`, определённый в директории `agents/` plugin. Параметры из `settings.json` имеют приоритет над `settings`, объявленными в `plugin.json`. Неизвестные ключи молча игнорируются.

### Организуйте сложные plugins

Для plugins с множеством компонентов организуйте структуру вашей директории по функциональности. Для полных макетов директорий и шаблонов организации см. [Структура директории Plugin](/ru/plugins-reference#plugin-directory-structure).

### Протестируйте ваши plugins локально

Используйте флаг `--plugin-dir` для тестирования plugins во время разработки. Это загружает ваш plugin напрямую без необходимости установки.

```bash theme={null}
claude --plugin-dir ./my-plugin
```

Когда `--plugin-dir` plugin имеет то же имя, что и установленный marketplace plugin, локальная копия имеет приоритет для этого сеанса. Это позволяет вам протестировать изменения plugin, который у вас уже установлен, без необходимости его предварительной деинсталляции. Marketplace plugins, принудительно включённые управляемыми параметрами, являются единственным исключением и не могут быть переопределены.

По мере внесения изменений в ваш plugin запустите `/reload-plugins` для применения обновлений без перезагрузки. Это перезагружает plugins, skills, agents, hooks, plugin MCP servers и plugin LSP servers. Протестируйте компоненты вашего plugin:

* Попробуйте ваши skills с `/plugin-name:skill-name`
* Проверьте, что agents появляются в `/agents`
* Убедитесь, что hooks работают как ожидается

<Tip>
  Вы можете загружать несколько plugins одновременно, указав флаг несколько раз:

  ```bash theme={null}
  claude --plugin-dir ./plugin-one --plugin-dir ./plugin-two
  ```
</Tip>

### Отладка проблем plugin

Если ваш plugin не работает как ожидается:

1. **Проверьте структуру**: Убедитесь, что ваши директории находятся в корне plugin, а не внутри `.claude-plugin/`
2. **Протестируйте компоненты отдельно**: Проверьте каждый skill, agent и hook отдельно
3. **Используйте инструменты валидации и отладки**: См. [Инструменты отладки и разработки](/ru/plugins-reference#debugging-and-development-tools) для команд CLI и методов troubleshooting

### Поделитесь вашими plugins

Когда ваш plugin готов к совместному использованию:

1. **Добавьте документацию**: Включите `README.md` с инструкциями по установке и использованию
2. **Версионируйте ваш plugin**: Используйте [семантическое версионирование](/ru/plugins-reference#version-management) в вашем `plugin.json`
3. **Создайте или используйте marketplace**: Распространяйте через [plugin marketplaces](/ru/plugin-marketplaces) для установки
4. **Протестируйте с другими**: Попросите членов команды протестировать plugin перед более широким распространением

Когда ваш plugin находится в marketplace, другие могут установить его, используя инструкции в [Обнаружение и установка plugins](/ru/discover-plugins).

### Отправьте ваш plugin на официальный marketplace

Чтобы отправить plugin на официальный marketplace Anthropic, используйте одну из встроенных форм отправки:

* **Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
* **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

Когда ваш plugin будет указан, вы сможете иметь собственный CLI, который подскажет пользователям Claude Code установить его. См. [Рекомендуйте ваш plugin из вашего CLI](/ru/plugin-hints).

<Note>
  Для полных технических спецификаций, методов отладки и стратегий распространения см. [Справочник plugins](/ru/plugins-reference).
</Note>

## Преобразование существующих конфигураций в plugins

Если у вас уже есть skills или hooks в вашей директории `.claude/`, вы можете преобразовать их в plugin для более лёгкого совместного использования и распространения.

### Шаги миграции

<Steps>
  <Step title="Создайте структуру plugin">
    Создайте новую директорию plugin:

    ```bash theme={null}
    mkdir -p my-plugin/.claude-plugin
    ```

    Создайте файл манифеста в `my-plugin/.claude-plugin/plugin.json`:

    ```json my-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "my-plugin",
      "description": "Migrated from standalone configuration",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Скопируйте ваши существующие файлы">
    Скопируйте ваши существующие конфигурации в директорию plugin:

    ```bash theme={null}
    # Copy commands
    cp -r .claude/commands my-plugin/

    # Copy agents (if any)
    cp -r .claude/agents my-plugin/

    # Copy skills (if any)
    cp -r .claude/skills my-plugin/
    ```
  </Step>

  <Step title="Мигрируйте hooks">
    Если у вас есть hooks в ваших параметрах, создайте директорию hooks:

    ```bash theme={null}
    mkdir my-plugin/hooks
    ```

    Создайте `my-plugin/hooks/hooks.json` с конфигурацией вашего hooks. Скопируйте объект `hooks` из вашего `.claude/settings.json` или `settings.local.json`, так как формат одинаков. Команда получает входные данные hook как JSON на stdin, поэтому используйте `jq` для извлечения пути файла:

    ```json my-plugin/hooks/hooks.json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [{ "type": "command", "command": "jq -r '.tool_input.file_path' | xargs npm run lint:fix" }]
          }
        ]
      }
    }
    ```
  </Step>

  <Step title="Протестируйте ваш мигрированный plugin">
    Загрузите ваш plugin для проверки того, что всё работает:

    ```bash theme={null}
    claude --plugin-dir ./my-plugin
    ```

    Протестируйте каждый компонент: запустите ваши команды, проверьте, что agents появляются в `/agents`, и убедитесь, что hooks срабатывают правильно.
  </Step>
</Steps>

### Что изменяется при миграции

| Автономная (`.claude/`)                                     | Plugin                              |
| :---------------------------------------------------------- | :---------------------------------- |
| Доступна только в одном проекте                             | Может быть общей через marketplaces |
| Файлы в `.claude/commands/`                                 | Файлы в `plugin-name/commands/`     |
| Hooks в `settings.json`                                     | Hooks в `hooks/hooks.json`          |
| Необходимо вручную копировать для совместного использования | Установить с `/plugin install`      |

<Note>
  После миграции вы можете удалить исходные файлы из `.claude/` для избежания дубликатов. Версия plugin будет иметь приоритет при загрузке.
</Note>

## Следующие шаги

Теперь, когда вы понимаете систему plugins Claude Code, вот предлагаемые пути для различных целей:

### Для пользователей plugin

* [Обнаружение и установка plugins](/ru/discover-plugins): просмотр marketplaces и установка plugins
* [Настройка team marketplaces](/ru/discover-plugins#configure-team-marketplaces): установка plugins на уровне репозитория для вашей команды

### Для разработчиков plugin

* [Создание и распространение marketplace](/ru/plugin-marketplaces): упаковка и совместное использование ваших plugins
* [Справочник plugins](/ru/plugins-reference): полные технические спецификации
* Углубитесь в конкретные компоненты plugin:
  * [Skills](/ru/skills): детали разработки skill
  * [Subagents](/ru/sub-agents): конфигурация и возможности agent
  * [Hooks](/ru/hooks): обработка событий и автоматизация
  * [MCP](/ru/mcp): интеграция внешних инструментов
