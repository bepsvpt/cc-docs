> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Создание и распространение marketplace плагинов

> Создавайте и размещайте marketplace плагинов для распространения расширений Claude Code по командам и сообществам.

**plugin marketplace** — это каталог, который позволяет вам распространять плагины другим пользователям. Marketplace обеспечивают централизованное обнаружение, отслеживание версий, автоматические обновления и поддержку нескольких типов источников (репозитории Git, локальные пути и многое другое). Это руководство показывает, как создать собственный marketplace для совместного использования плагинов с вашей командой или сообществом.

Ищете способ установить плагины из существующего marketplace? См. [Обнаружение и установка готовых плагинов](/ru/discover-plugins).

## Обзор

Создание и распространение marketplace включает:

1. **Создание плагинов**: создайте один или несколько плагинов с командами, агентами, hooks, MCP servers или LSP servers. Это руководство предполагает, что у вас уже есть плагины для распространения; см. [Создание плагинов](/ru/plugins) для получения подробной информации о том, как их создавать.
2. **Создание файла marketplace**: определите `marketplace.json`, который перечисляет ваши плагины и где их найти (см. [Создание файла marketplace](#create-the-marketplace-file)).
3. **Размещение marketplace**: отправьте на GitHub, GitLab или другой хост Git (см. [Размещение и распространение marketplace](#host-and-distribute-marketplaces)).
4. **Совместное использование с пользователями**: пользователи добавляют ваш marketplace с помощью `/plugin marketplace add` и устанавливают отдельные плагины (см. [Обнаружение и установка плагинов](/ru/discover-plugins)).

После того как ваш marketplace будет запущен, вы можете обновить его, отправив изменения в ваш репозиторий. Пользователи обновляют свою локальную копию с помощью `/plugin marketplace update`.

## Пошаговое руководство: создание локального marketplace

Этот пример создает marketplace с одним плагином: skill `/quality-review` для проверки кода. Вы создадите структуру каталогов, добавите skill, создадите манифест плагина и каталог marketplace, затем установите и протестируете его.

<Steps>
  <Step title="Создание структуры каталогов">
    ```bash  theme={null}
    mkdir -p my-marketplace/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/.claude-plugin
    mkdir -p my-marketplace/plugins/quality-review-plugin/skills/quality-review
    ```
  </Step>

  <Step title="Создание skill">
    Создайте файл `SKILL.md`, который определяет, что делает skill `/quality-review`.

    ```markdown my-marketplace/plugins/quality-review-plugin/skills/quality-review/SKILL.md theme={null}
    ---
    description: Проверка кода на ошибки, безопасность и производительность
    disable-model-invocation: true
    ---

    Проверьте выбранный мной код или недавние изменения на предмет:
    - Потенциальных ошибок или граничных случаев
    - Проблем безопасности
    - Проблем производительности
    - Улучшений читаемости

    Будьте лаконичны и конкретны.
    ```
  </Step>

  <Step title="Создание манифеста плагина">
    Создайте файл `plugin.json`, который описывает плагин. Манифест находится в каталоге `.claude-plugin/`.

    ```json my-marketplace/plugins/quality-review-plugin/.claude-plugin/plugin.json theme={null}
    {
      "name": "quality-review-plugin",
      "description": "Добавляет skill /quality-review для быстрой проверки кода",
      "version": "1.0.0"
    }
    ```
  </Step>

  <Step title="Создание файла marketplace">
    Создайте каталог marketplace, который перечисляет ваш плагин.

    ```json my-marketplace/.claude-plugin/marketplace.json theme={null}
    {
      "name": "my-plugins",
      "owner": {
        "name": "Ваше имя"
      },
      "plugins": [
        {
          "name": "quality-review-plugin",
          "source": "./plugins/quality-review-plugin",
          "description": "Добавляет skill /quality-review для быстрой проверки кода"
        }
      ]
    }
    ```
  </Step>

  <Step title="Добавление и установка">
    Добавьте marketplace и установите плагин.

    ```shell  theme={null}
    /plugin marketplace add ./my-marketplace
    /plugin install quality-review-plugin@my-plugins
    ```
  </Step>

  <Step title="Попробуйте">
    Выберите некоторый код в вашем редакторе и запустите вашу новую команду.

    ```shell  theme={null}
    /quality-review
    ```
  </Step>
</Steps>

Чтобы узнать больше о том, что могут делать плагины, включая hooks, агентов, MCP servers и LSP servers, см. [Плагины](/ru/plugins).

<Note>
  **Как устанавливаются плагины**: Когда пользователи устанавливают плагин, Claude Code копирует каталог плагина в место кэша. Это означает, что плагины не могут ссылаться на файлы вне их каталога, используя пути вроде `../shared-utils`, потому что эти файлы не будут скопированы.

  Если вам нужно совместно использовать файлы между плагинами, используйте символические ссылки (которые следуют при копировании). См. [Кэширование плагинов и разрешение файлов](/ru/plugins-reference#plugin-caching-and-file-resolution) для получения подробной информации.
</Note>

## Создание файла marketplace

Создайте `.claude-plugin/marketplace.json` в корне вашего репозитория. Этот файл определяет имя вашего marketplace, информацию о владельце и список плагинов с их источниками.

Каждая запись плагина требует как минимум `name` и `source` (откуда его получить). См. [полную схему](#marketplace-schema) ниже для всех доступных полей.

```json  theme={null}
{
  "name": "company-tools",
  "owner": {
    "name": "DevTools Team",
    "email": "devtools@example.com"
  },
  "plugins": [
    {
      "name": "code-formatter",
      "source": "./plugins/formatter",
      "description": "Автоматическое форматирование кода при сохранении",
      "version": "2.1.0",
      "author": {
        "name": "DevTools Team"
      }
    },
    {
      "name": "deployment-tools",
      "source": {
        "source": "github",
        "repo": "company/deploy-plugin"
      },
      "description": "Инструменты автоматизации развертывания"
    }
  ]
}
```

## Схема marketplace

### Обязательные поля

| Поле      | Тип    | Описание                                                                                                                                                                            | Пример         |
| :-------- | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------- |
| `name`    | string | Идентификатор marketplace (kebab-case, без пробелов). Это общедоступное поле: пользователи видят его при установке плагинов (например, `/plugin install my-tool@your-marketplace`). | `"acme-tools"` |
| `owner`   | object | Информация о сопровождающем marketplace ([см. поля ниже](#owner-fields))                                                                                                            |                |
| `plugins` | array  | Список доступных плагинов                                                                                                                                                           | См. ниже       |

<Note>
  **Зарезервированные имена**: Следующие имена marketplace зарезервированы для официального использования Anthropic и не могут использоваться сторонними marketplace: `claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `knowledge-work-plugins`, `life-sciences`. Имена, которые выдают себя за официальные marketplace (например, `official-claude-plugins` или `anthropic-tools-v2`), также заблокированы.
</Note>

### Поля владельца

| Поле    | Тип    | Обязательно | Описание                                           |
| :------ | :----- | :---------- | :------------------------------------------------- |
| `name`  | string | Да          | Имя сопровождающего или команды                    |
| `email` | string | Нет         | Контактный адрес электронной почты сопровождающего |

### Дополнительные метаданные

| Поле                   | Тип    | Описание                                                                                                                                                                               |
| :--------------------- | :----- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `metadata.description` | string | Краткое описание marketplace                                                                                                                                                           |
| `metadata.version`     | string | Версия marketplace                                                                                                                                                                     |
| `metadata.pluginRoot`  | string | Базовый каталог, добавляемый к относительным путям источников плагинов (например, `"./plugins"` позволяет вам писать `"source": "formatter"` вместо `"source": "./plugins/formatter"`) |

## Записи плагинов

Каждая запись плагина в массиве `plugins` описывает плагин и где его найти. Вы можете включить любое поле из [схемы манифеста плагина](/ru/plugins-reference#plugin-manifest-schema) (например, `description`, `version`, `author`, `commands`, `hooks` и т. д.), плюс эти поля, специфичные для marketplace: `source`, `category`, `tags` и `strict`.

### Обязательные поля

| Поле     | Тип            | Описание                                                                                                                                                            |
| :------- | :------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `name`   | string         | Идентификатор плагина (kebab-case, без пробелов). Это общедоступное поле: пользователи видят его при установке (например, `/plugin install my-plugin@marketplace`). |
| `source` | string\|object | Откуда получить плагин (см. [Источники плагинов](#plugin-sources) ниже)                                                                                             |

### Дополнительные поля плагина

**Поля стандартных метаданных:**

| Поле          | Тип     | Описание                                                                                                                                    |
| :------------ | :------ | :------------------------------------------------------------------------------------------------------------------------------------------ |
| `description` | string  | Краткое описание плагина                                                                                                                    |
| `version`     | string  | Версия плагина                                                                                                                              |
| `author`      | object  | Информация об авторе плагина (`name` обязательно, `email` опционально)                                                                      |
| `homepage`    | string  | URL домашней страницы или документации плагина                                                                                              |
| `repository`  | string  | URL репозитория исходного кода                                                                                                              |
| `license`     | string  | Идентификатор лицензии SPDX (например, MIT, Apache-2.0)                                                                                     |
| `keywords`    | array   | Теги для обнаружения и категоризации плагинов                                                                                               |
| `category`    | string  | Категория плагина для организации                                                                                                           |
| `tags`        | array   | Теги для поиска                                                                                                                             |
| `strict`      | boolean | Контролирует, является ли `plugin.json` авторитетом для определений компонентов (по умолчанию: true). См. [Strict mode](#strict-mode) ниже. |

**Поля конфигурации компонентов:**

| Поле         | Тип            | Описание                                                   |
| :----------- | :------------- | :--------------------------------------------------------- |
| `commands`   | string\|array  | Пользовательские пути к файлам или каталогам команд        |
| `agents`     | string\|array  | Пользовательские пути к файлам агентов                     |
| `hooks`      | string\|object | Конфигурация пользовательских hooks или путь к файлу hooks |
| `mcpServers` | string\|object | Конфигурации MCP server или путь к конфигурации MCP        |
| `lspServers` | string\|object | Конфигурации LSP server или путь к конфигурации LSP        |

## Источники плагинов

Источники плагинов указывают Claude Code, откуда получить каждый отдельный плагин, указанный в вашем marketplace. Они устанавливаются в поле `source` каждой записи плагина в `marketplace.json`.

После того как плагин клонирован или скопирован на локальную машину, он копируется в локальный кэш плагинов с версией в `~/.claude/plugins/cache`.

| Источник           | Тип                                  | Поля                               | Примечания                                                                                                           |
| ------------------ | ------------------------------------ | ---------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Относительный путь | `string` (например, `"./my-plugin"`) | —                                  | Локальный каталог в репозитории marketplace. Должен начинаться с `./`                                                |
| `github`           | object                               | `repo`, `ref?`, `sha?`             |                                                                                                                      |
| `url`              | object                               | `url`, `ref?`, `sha?`              | Источник URL Git                                                                                                     |
| `git-subdir`       | object                               | `url`, `path`, `ref?`, `sha?`      | Подкаталог в репозитории Git. Клонирует разреженно, чтобы минимизировать пропускную способность для монорепозиториев |
| `npm`              | object                               | `package`, `version?`, `registry?` | Установлено через `npm install`                                                                                      |

<Note>
  **Источники marketplace и источники плагинов**: Это разные концепции, которые контролируют разные вещи.

  * **Источник marketplace** — откуда получить сам каталог `marketplace.json`. Устанавливается, когда пользователи запускают `/plugin marketplace add` или в параметрах `extraKnownMarketplaces`. Поддерживает `ref` (ветка/тег), но не `sha`.
  * **Источник плагина** — откуда получить отдельный плагин, указанный в marketplace. Устанавливается в поле `source` каждой записи плагина внутри `marketplace.json`. Поддерживает как `ref` (ветка/тег), так и `sha` (точный коммит).

  Например, marketplace, размещенный в `acme-corp/plugin-catalog` (источник marketplace), может перечислять плагин, полученный из `acme-corp/code-formatter` (источник плагина). Источник marketplace и источник плагина указывают на разные репозитории и закреплены независимо.
</Note>

### Относительные пути

Для плагинов в одном репозитории используйте путь, начинающийся с `./`:

```json  theme={null}
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin"
}
```

Пути разрешаются относительно корня marketplace, который является каталогом, содержащим `.claude-plugin/`. В приведенном выше примере `./plugins/my-plugin` указывает на `<repo>/plugins/my-plugin`, даже если `marketplace.json` находится в `<repo>/.claude-plugin/marketplace.json`. Не используйте `../` для выхода из `.claude-plugin/`.

<Note>
  Относительные пути работают только, когда пользователи добавляют ваш marketplace через Git (GitHub, GitLab или URL Git). Если пользователи добавляют ваш marketplace через прямой URL к файлу `marketplace.json`, относительные пути не будут разрешены правильно. Для распространения на основе URL используйте вместо этого источники GitHub, npm или URL Git. См. [Устранение неполадок](#plugins-with-relative-paths-fail-in-url-based-marketplaces) для получения подробной информации.
</Note>

### Репозитории GitHub

```json  theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo"
  }
}
```

Вы можете закрепить определенную ветку, тег или коммит:

```json  theme={null}
{
  "name": "github-plugin",
  "source": {
    "source": "github",
    "repo": "owner/plugin-repo",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Поле   | Тип    | Описание                                                                           |
| :----- | :----- | :--------------------------------------------------------------------------------- |
| `repo` | string | Обязательно. Репозиторий GitHub в формате `owner/repo`                             |
| `ref`  | string | Опционально. Ветка или тег Git (по умолчанию ветка по умолчанию репозитория)       |
| `sha`  | string | Опционально. Полный 40-символьный SHA коммита Git для закрепления на точной версии |

### Репозитории Git

```json  theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git"
  }
}
```

Вы можете закрепить определенную ветку, тег или коммит:

```json  theme={null}
{
  "name": "git-plugin",
  "source": {
    "source": "url",
    "url": "https://gitlab.com/team/plugin.git",
    "ref": "main",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

| Поле  | Тип    | Описание                                                                                                                                                    |
| :---- | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `url` | string | Обязательно. Полный URL репозитория Git (`https://` или `git@`). Суффикс `.git` опционален, поэтому URL Azure DevOps и AWS CodeCommit без суффикса работают |
| `ref` | string | Опционально. Ветка или тег Git (по умолчанию ветка по умолчанию репозитория)                                                                                |
| `sha` | string | Опционально. Полный 40-символьный SHA коммита Git для закрепления на точной версии                                                                          |

### Подкаталоги Git

Используйте `git-subdir` для указания плагина, который находится в подкаталоге репозитория Git. Claude Code использует разреженный, частичный клон для получения только подкаталога, минимизируя пропускную способность для больших монорепозиториев.

```json  theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin"
  }
}
```

Вы можете закрепить определенную ветку, тег или коммит:

```json  theme={null}
{
  "name": "my-plugin",
  "source": {
    "source": "git-subdir",
    "url": "https://github.com/acme-corp/monorepo.git",
    "path": "tools/claude-plugin",
    "ref": "v2.0.0",
    "sha": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0"
  }
}
```

Поле `url` также принимает сокращение GitHub (`owner/repo`) или SSH URL (`git@github.com:owner/repo.git`).

| Поле   | Тип    | Описание                                                                                           |
| :----- | :----- | :------------------------------------------------------------------------------------------------- |
| `url`  | string | Обязательно. URL репозитория Git, сокращение GitHub `owner/repo` или SSH URL                       |
| `path` | string | Обязательно. Путь подкаталога в репозитории, содержащий плагин (например, `"tools/claude-plugin"`) |
| `ref`  | string | Опционально. Ветка или тег Git (по умолчанию ветка по умолчанию репозитория)                       |
| `sha`  | string | Опционально. Полный 40-символьный SHA коммита Git для закрепления на точной версии                 |

### Пакеты npm

Плагины, распространяемые как пакеты npm, устанавливаются с помощью `npm install`. Это работает с любым пакетом в общедоступном реестре npm или в частном реестре, который размещает ваша команда.

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin"
  }
}
```

Чтобы закрепить определенную версию, добавьте поле `version`:

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "2.1.0"
  }
}
```

Для установки из частного или внутреннего реестра добавьте поле `registry`:

```json  theme={null}
{
  "name": "my-npm-plugin",
  "source": {
    "source": "npm",
    "package": "@acme/claude-plugin",
    "version": "^2.0.0",
    "registry": "https://npm.example.com"
  }
}
```

| Поле       | Тип    | Описание                                                                                            |
| :--------- | :----- | :-------------------------------------------------------------------------------------------------- |
| `package`  | string | Обязательно. Имя пакета или область пакета (например, `@org/plugin`)                                |
| `version`  | string | Опционально. Версия или диапазон версий (например, `2.1.0`, `^2.0.0`, `~1.5.0`)                     |
| `registry` | string | Опционально. Пользовательский URL реестра npm. По умолчанию системный реестр npm (обычно npmjs.org) |

### Расширенные записи плагинов

Этот пример показывает запись плагина, использующую множество дополнительных полей, включая пользовательские пути для команд, агентов, hooks и MCP servers:

```json  theme={null}
{
  "name": "enterprise-tools",
  "source": {
    "source": "github",
    "repo": "company/enterprise-plugin"
  },
  "description": "Инструменты автоматизации корпоративного рабочего процесса",
  "version": "2.1.0",
  "author": {
    "name": "Enterprise Team",
    "email": "enterprise@example.com"
  },
  "homepage": "https://docs.example.com/plugins/enterprise-tools",
  "repository": "https://github.com/company/enterprise-plugin",
  "license": "MIT",
  "keywords": ["enterprise", "workflow", "automation"],
  "category": "productivity",
  "commands": [
    "./commands/core/",
    "./commands/enterprise/",
    "./commands/experimental/preview.md"
  ],
  "agents": ["./agents/security-reviewer.md", "./agents/compliance-checker.md"],
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate.sh"
          }
        ]
      }
    ]
  },
  "mcpServers": {
    "enterprise-db": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
    }
  },
  "strict": false
}
```

Ключевые моменты, на которые следует обратить внимание:

* **`commands` и `agents`**: Вы можете указать несколько каталогов или отдельные файлы. Пути относительны к корню плагина.
* **`${CLAUDE_PLUGIN_ROOT}`**: Используйте эту переменную в hooks и конфигурациях MCP server для ссылки на файлы в каталоге установки плагина. Это необходимо, потому что плагины копируются в место кэша при установке. Для зависимостей или состояния, которое должно сохраняться при обновлениях плагина, используйте [`${CLAUDE_PLUGIN_DATA}`](/ru/plugins-reference#persistent-data-directory) вместо этого.
* **`strict: false`**: Поскольку это установлено на false, плагину не нужен собственный `plugin.json`. Запись marketplace определяет все. См. [Strict mode](#strict-mode) ниже.

### Strict mode

Поле `strict` контролирует, является ли `plugin.json` авторитетом для определений компонентов (команды, агенты, hooks, skills, MCP servers, стили вывода).

| Значение              | Поведение                                                                                                                                                   |
| :-------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `true` (по умолчанию) | `plugin.json` является авторитетом. Запись marketplace может дополнить его дополнительными компонентами, и оба источника объединяются.                      |
| `false`               | Запись marketplace является полным определением. Если плагин также имеет `plugin.json`, который объявляет компоненты, это конфликт и плагин не загружается. |

**Когда использовать каждый режим:**

* **`strict: true`**: плагин имеет собственный `plugin.json` и управляет своими компонентами. Запись marketplace может добавить дополнительные команды или hooks сверху. Это значение по умолчанию и работает для большинства плагинов.
* **`strict: false`**: оператор marketplace хочет полный контроль. Репозиторий плагина предоставляет необработанные файлы, и запись marketplace определяет, какие из этих файлов открыты как команды, агенты, hooks и т. д. Полезно, когда оператор marketplace переструктурирует или курирует компоненты плагина иначе, чем предполагал автор плагина.

## Размещение и распространение marketplace

### Размещение на GitHub (рекомендуется)

GitHub обеспечивает самый простой метод распространения:

1. **Создание репозитория**: Установите новый репозиторий для вашего marketplace
2. **Добавление файла marketplace**: Создайте `.claude-plugin/marketplace.json` с определениями ваших плагинов
3. **Совместное использование с командами**: Пользователи добавляют ваш marketplace с помощью `/plugin marketplace add owner/repo`

**Преимущества**: Встроенное управление версиями, отслеживание проблем и функции совместной работы команды.

### Размещение на других сервисах Git

Любой сервис хостинга Git работает, например GitLab, Bitbucket и самостоятельно размещаемые серверы. Пользователи добавляют с полным URL репозитория:

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

### Частные репозитории

Claude Code поддерживает установку плагинов из частных репозиториев. Для ручной установки и обновлений Claude Code использует ваши существующие помощники учетных данных Git. Если `git clone` работает для частного репозитория в вашем терминале, это работает и в Claude Code. Общие помощники учетных данных включают `gh auth login` для GitHub, macOS Keychain и `git-credential-store`.

Фоновые автоматические обновления запускаются при запуске без помощников учетных данных, так как интерактивные подсказки блокировали бы запуск Claude Code. Чтобы включить автоматические обновления для частных marketplace, установите соответствующий токен аутентификации в вашей среде:

| Поставщик | Переменные окружения          | Примечания                                        |
| :-------- | :---------------------------- | :------------------------------------------------ |
| GitHub    | `GITHUB_TOKEN` или `GH_TOKEN` | Личный токен доступа или токен GitHub App         |
| GitLab    | `GITLAB_TOKEN` или `GL_TOKEN` | Личный токен доступа или токен проекта            |
| Bitbucket | `BITBUCKET_TOKEN`             | Пароль приложения или токен доступа к репозиторию |

Установите токен в конфигурацию вашей оболочки (например, `.bashrc`, `.zshrc`) или передайте его при запуске Claude Code:

```bash  theme={null}
export GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxx
```

<Note>
  Для сред CI/CD настройте токен как переменную окружения секрета. GitHub Actions автоматически предоставляет `GITHUB_TOKEN` для репозиториев в одной организации.
</Note>

### Тестирование локально перед распространением

Протестируйте ваш marketplace локально перед совместным использованием:

```shell  theme={null}
/plugin marketplace add ./my-local-marketplace
/plugin install test-plugin@my-local-marketplace
```

Для полного диапазона команд добавления (GitHub, URL Git, локальные пути, удаленные URL), см. [Добавление marketplace](/ru/discover-plugins#add-marketplaces).

### Требование marketplace для вашей команды

Вы можете настроить ваш репозиторий так, чтобы члены команды автоматически получали предложение установить ваш marketplace, когда они доверяют папке проекта. Добавьте ваш marketplace в `.claude/settings.json`:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "company-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

Вы также можете указать, какие плагины должны быть включены по умолчанию:

```json  theme={null}
{
  "enabledPlugins": {
    "code-formatter@company-tools": true,
    "deployment-tools@company-tools": true
  }
}
```

Для полных параметров конфигурации см. [Параметры плагинов](/ru/settings#plugin-settings).

<Note>
  Если вы используете локальный источник `directory` или `file` с относительным путем, путь разрешается относительно основного checkout вашего репозитория. Когда вы запускаете Claude Code из git worktree, путь все еще указывает на основной checkout, поэтому все worktrees совместно используют одно и то же расположение marketplace. Состояние marketplace хранится один раз для каждого пользователя в `~/.claude/plugins/known_marketplaces.json`, а не для каждого проекта.
</Note>

### Предварительное заполнение плагинов для контейнеров

Для образов контейнеров и сред CI, вы можете предварительно заполнить каталог плагинов во время сборки, чтобы Claude Code запускался с уже доступными marketplace и плагинами, без клонирования во время выполнения. Установите переменную окружения `CLAUDE_CODE_PLUGIN_SEED_DIR` на этот каталог.

Чтобы наслоить несколько каталогов seed, разделите пути с `:` на Unix или `;` на Windows. Claude Code ищет каждый каталог по порядку, и первый seed, содержащий данный marketplace или кэш плагина, побеждает.

Каталог seed отражает структуру `~/.claude/plugins`:

```
$CLAUDE_CODE_PLUGIN_SEED_DIR/
  known_marketplaces.json
  marketplaces/<name>/...
  cache/<marketplace>/<plugin>/<version>/...
```

Самый простой способ построить каталог seed — запустить Claude Code один раз во время сборки образа, установить нужные вам плагины, затем скопировать полученный каталог `~/.claude/plugins` в ваш образ и указать `CLAUDE_CODE_PLUGIN_SEED_DIR` на него.

При запуске Claude Code регистрирует marketplace, найденные в `known_marketplaces.json` seed, в основную конфигурацию и использует кэши плагинов, найденные под `cache/`, на месте без повторного клонирования. Это работает как в интерактивном режиме, так и в неинтерактивном режиме с флагом `-p`.

Детали поведения:

* **Только для чтения**: каталог seed никогда не записывается. Автоматические обновления отключены для seed marketplace, так как git pull не удастся на файловой системе только для чтения.
* **Записи seed имеют приоритет**: marketplace, объявленные в seed, перезаписывают любые совпадающие записи в конфигурации пользователя при каждом запуске. Чтобы отказаться от seed плагина, используйте `/plugin disable` вместо удаления marketplace.
* **Разрешение пути**: Claude Code находит содержимое marketplace, проверяя `$CLAUDE_CODE_PLUGIN_SEED_DIR/marketplaces/<name>/` во время выполнения, а не доверяя путям, хранящимся внутри JSON seed. Это означает, что seed работает правильно, даже если он смонтирован по другому пути, чем где он был построен.
* **Компонуется с параметрами**: если `extraKnownMarketplaces` или `enabledPlugins` объявляют marketplace, который уже существует в seed, Claude Code использует копию seed вместо клонирования.

### Ограничения управляемого marketplace

Для организаций, требующих строгого контроля над источниками плагинов, администраторы могут ограничить, какие marketplace плагинов пользователи могут добавлять, используя параметр [`strictKnownMarketplaces`](/ru/settings#strictknownmarketplaces) в управляемых параметрах.

Когда `strictKnownMarketplaces` настроен в управляемых параметрах, поведение ограничения зависит от значения:

| Значение                     | Поведение                                                                                      |
| ---------------------------- | ---------------------------------------------------------------------------------------------- |
| Не определено (по умолчанию) | Нет ограничений. Пользователи могут добавлять любой marketplace                                |
| Пустой массив `[]`           | Полная блокировка. Пользователи не могут добавлять новые marketplace                           |
| Список источников            | Пользователи могут добавлять только marketplace, которые точно совпадают со списком разрешений |

#### Общие конфигурации

Отключение всех добавлений marketplace:

```json  theme={null}
{
  "strictKnownMarketplaces": []
}
```

Разрешение только определенных marketplace:

```json  theme={null}
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
    }
  ]
}
```

Разрешение всех marketplace с внутреннего сервера Git с использованием сопоставления шаблонов регулярных выражений на хосте. Это рекомендуемый подход для [GitHub Enterprise Server](/ru/github-enterprise-server#plugin-marketplaces-on-ghes) или самостоятельно размещаемых экземпляров GitLab:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "hostPattern",
      "hostPattern": "^github\\.example\\.com$"
    }
  ]
}
```

Разрешение marketplace на основе файловой системы из определенного каталога с использованием сопоставления шаблонов регулярных выражений на пути:

```json  theme={null}
{
  "strictKnownMarketplaces": [
    {
      "source": "pathPattern",
      "pathPattern": "^/opt/approved/"
    }
  ]
}
```

Используйте `".*"` как `pathPattern` для разрешения любого пути файловой системы при одновременном контроле сетевых источников с помощью `hostPattern`.

<Note>
  `strictKnownMarketplaces` ограничивает то, что пользователи могут добавлять, но не регистрирует marketplace самостоятельно. Чтобы сделать разрешенные marketplace доступными автоматически без запуска пользователями `/plugin marketplace add`, объедините его с [`extraKnownMarketplaces`](/ru/settings#extraknownmarketplaces) в одном файле `managed-settings.json`. См. [Использование обоих вместе](/ru/settings#strictknownmarketplaces).
</Note>

#### Как работают ограничения

Ограничения проверяются на ранней стадии процесса установки плагина, до любых сетевых запросов или операций файловой системы. Это предотвращает попытки несанкционированного доступа к marketplace.

Список разрешений использует точное сопоставление для большинства типов источников. Чтобы marketplace был разрешен, все указанные поля должны совпадать точно:

* Для источников GitHub: `repo` обязателен, и `ref` или `path` также должны совпадать, если указаны в списке разрешений
* Для источников URL: полный URL должен совпадать точно
* Для источников `hostPattern`: хост marketplace сопоставляется с шаблоном регулярного выражения
* Для источников `pathPattern`: путь файловой системы marketplace сопоставляется с шаблоном регулярного выражения

Поскольку `strictKnownMarketplaces` установлен в [управляемых параметрах](/ru/settings#settings-files), отдельные пользователи и конфигурации проекта не могут переопределить эти ограничения.

Для полных деталей конфигурации, включая все поддерживаемые типы источников и сравнение с `extraKnownMarketplaces`, см. [справку strictKnownMarketplaces](/ru/settings#strictknownmarketplaces).

### Разрешение версий и каналы выпуска

Версии плагинов определяют пути кэша и обнаружение обновлений. Вы можете указать версию в манифесте плагина (`plugin.json`) или в записи marketplace (`marketplace.json`).

<Warning>
  По возможности избегайте установки версии в обоих местах. Манифест плагина всегда побеждает молча, что может привести к игнорированию версии marketplace. Для плагинов с относительными путями установите версию в записи marketplace. Для всех остальных источников плагинов установите ее в манифесте плагина.
</Warning>

#### Установка каналов выпуска

Для поддержки каналов выпуска "stable" и "latest" для ваших плагинов вы можете установить два marketplace, которые указывают на разные refs или SHAs одного репозитория. Затем вы можете назначить два marketplace разным группам пользователей через [управляемые параметры](/ru/settings#settings-files).

<Warning>
  `plugin.json` плагина должен объявлять другую `version` в каждом закрепленном ref или коммите. Если два refs или коммита имеют одну и ту же версию манифеста, Claude Code рассматривает их как идентичные и пропускает обновление.
</Warning>

##### Пример

```json  theme={null}
{
  "name": "stable-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "stable"
      }
    }
  ]
}
```

```json  theme={null}
{
  "name": "latest-tools",
  "plugins": [
    {
      "name": "code-formatter",
      "source": {
        "source": "github",
        "repo": "acme-corp/code-formatter",
        "ref": "latest"
      }
    }
  ]
}
```

##### Назначение каналов группам пользователей

Назначьте каждый marketplace соответствующей группе пользователей через управляемые параметры. Например, стабильная группа получает:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "stable-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/stable-tools"
      }
    }
  }
}
```

Группа ранних доступов получает вместо этого `latest-tools`:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "latest-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/latest-tools"
      }
    }
  }
}
```

## Валидация и тестирование

Протестируйте ваш marketplace перед совместным использованием.

Проверьте синтаксис JSON вашего marketplace:

```bash  theme={null}
claude plugin validate .
```

Или из Claude Code:

```shell  theme={null}
/plugin validate .
```

Добавьте marketplace для тестирования:

```shell  theme={null}
/plugin marketplace add ./path/to/marketplace
```

Установите тестовый плагин, чтобы проверить, что все работает:

```shell  theme={null}
/plugin install test-plugin@marketplace-name
```

Для полного диапазона рабочих процессов тестирования плагинов см. [Тестирование ваших плагинов локально](/ru/plugins#test-your-plugins-locally). Для технического устранения неполадок см. [Справка плагинов](/ru/plugins-reference).

## Устранение неполадок

### Marketplace не загружается

**Симптомы**: Не удается добавить marketplace или увидеть плагины из него

**Решения**:

* Проверьте, что URL marketplace доступен
* Убедитесь, что `.claude-plugin/marketplace.json` существует по указанному пути
* Убедитесь, что синтаксис JSON действителен и frontmatter хорошо сформирован, используя `claude plugin validate` или `/plugin validate`
* Для частных репозиториев подтвердите, что у вас есть разрешения доступа

### Ошибки валидации marketplace

Запустите `claude plugin validate .` или `/plugin validate .` из каталога вашего marketplace, чтобы проверить наличие проблем. Валидатор проверяет `plugin.json`, frontmatter skill/agent/command и `hooks/hooks.json` на синтаксис и ошибки схемы. Общие ошибки:

| Ошибка                                            | Причина                                        | Решение                                                                                                 |
| :------------------------------------------------ | :--------------------------------------------- | :------------------------------------------------------------------------------------------------------ |
| `File not found: .claude-plugin/marketplace.json` | Отсутствует манифест                           | Создайте `.claude-plugin/marketplace.json` с обязательными полями                                       |
| `Invalid JSON syntax: Unexpected token...`        | Ошибка синтаксиса JSON в marketplace.json      | Проверьте отсутствующие запятые, лишние запятые или неквотированные строки                              |
| `Duplicate plugin name "x" found in marketplace`  | Два плагина имеют одно имя                     | Дайте каждому плагину уникальное значение `name`                                                        |
| `plugins[0].source: Path contains ".."`           | Путь источника содержит `..`                   | Используйте пути относительно корня marketplace без `..`. См. [Относительные пути](#relative-paths)     |
| `YAML frontmatter failed to parse: ...`           | Неверный YAML в файле skill, agent или command | Исправьте синтаксис YAML в блоке frontmatter. Во время выполнения этот файл загружается без метаданных. |
| `Invalid JSON syntax: ...` (hooks.json)           | Неправильный формат `hooks/hooks.json`         | Исправьте синтаксис JSON. Неправильный `hooks/hooks.json` предотвращает загрузку всего плагина.         |

**Предупреждения** (не блокирующие):

* `Marketplace has no plugins defined`: добавьте хотя бы один плагин в массив `plugins`
* `No marketplace description provided`: добавьте `metadata.description`, чтобы помочь пользователям понять ваш marketplace
* `Plugin name "x" is not kebab-case`: имя плагина содержит прописные буквы, пробелы или специальные символы. Переименуйте в строчные буквы, цифры и дефисы только (например, `my-plugin`). Claude Code принимает другие формы, но синхронизация marketplace Claude.ai их отклоняет.

### Ошибки установки плагина

**Симптомы**: Marketplace появляется, но установка плагина не удается

**Решения**:

* Проверьте, что URL источников плагинов доступны
* Убедитесь, что каталоги плагинов содержат необходимые файлы
* Для источников GitHub убедитесь, что репозитории являются общедоступными или у вас есть доступ
* Протестируйте источники плагинов вручную, клонируя/загружая их

### Ошибка аутентификации частного репозитория

**Симптомы**: Ошибки аутентификации при установке плагинов из частных репозиториев

**Решения**:

Для ручной установки и обновлений:

* Проверьте, что вы аутентифицированы у вашего поставщика Git (например, запустите `gh auth status` для GitHub)
* Проверьте, что ваш помощник учетных данных настроен правильно: `git config --global credential.helper`
* Попробуйте клонировать репозиторий вручную, чтобы проверить, что ваши учетные данные работают

Для фоновых автоматических обновлений:

* Установите соответствующий токен в вашей среде: `echo $GITHUB_TOKEN`
* Проверьте, что токен имеет необходимые разрешения (доступ на чтение к репозиторию)
* Для GitHub убедитесь, что токен имеет область `repo` для частных репозиториев
* Для GitLab убедитесь, что токен имеет как минимум область `read_repository`
* Проверьте, что токен не истек

### Операции Git истекают по времени

**Симптомы**: Установка плагина или обновление marketplace не удается с ошибкой истечения времени, например "Git clone timed out after 120s" или "Git pull timed out after 120s".

**Причина**: Claude Code использует 120-секундный таймаут для всех операций Git, включая клонирование репозиториев плагинов и извлечение обновлений marketplace. Большие репозитории или медленные сетевые соединения могут превысить этот лимит.

**Решение**: Увеличьте таймаут, используя переменную окружения `CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS`. Значение указывается в миллисекундах:

```bash  theme={null}
export CLAUDE_CODE_PLUGIN_GIT_TIMEOUT_MS=300000  # 5 минут
```

### Плагины с относительными путями не работают в marketplace на основе URL

**Симптомы**: Добавлен marketplace через URL (например, `https://example.com/marketplace.json`), но плагины с источниками относительных путей, такие как `"./plugins/my-plugin"`, не устанавливаются с ошибками "path not found".

**Причина**: Marketplace на основе URL загружают только сам файл `marketplace.json`. Они не загружают файлы плагинов с сервера. Относительные пути в записи marketplace ссылаются на файлы на удаленном сервере, которые не были загружены.

**Решения**:

* **Используйте внешние источники**: Измените записи плагинов, чтобы использовать источники GitHub, npm или URL Git вместо относительных путей:
  ```json  theme={null}
  { "name": "my-plugin", "source": { "source": "github", "repo": "owner/repo" } }
  ```
* **Используйте marketplace на основе Git**: Разместите ваш marketplace в репозитории Git и добавьте его с URL Git. Marketplace на основе Git клонируют весь репозиторий, что делает относительные пути рабочими.

### Файлы не найдены после установки

**Симптомы**: Плагин устанавливается, но ссылки на файлы не работают, особенно файлы вне каталога плагина

**Причина**: Плагины копируются в каталог кэша, а не используются на месте. Пути, которые ссылаются на файлы вне каталога плагина (например, `../shared-utils`), не будут работать, потому что эти файлы не копируются.

**Решения**: См. [Кэширование плагинов и разрешение файлов](/ru/plugins-reference#plugin-caching-and-file-resolution) для обходных путей, включая символические ссылки и переструктурирование каталогов.

Для дополнительных инструментов отладки и распространенных проблем см. [Инструменты отладки и разработки](/ru/plugins-reference#debugging-and-development-tools).

### Обновления marketplace не работают в автономных средах

**Симптомы**: Marketplace `git pull` не удается и Claude Code удаляет существующий кэш, что делает плагины недоступными.

**Причина**: По умолчанию, когда `git pull` не удается, Claude Code удаляет устаревший клон и пытается повторно клонировать. В автономных или изолированных средах повторное клонирование не удается так же, оставляя каталог marketplace пустым.

**Решение**: Установите `CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1`, чтобы сохранить существующий кэш при сбое pull вместо его удаления:

```bash  theme={null}
export CLAUDE_CODE_PLUGIN_KEEP_MARKETPLACE_ON_FAILURE=1
```

С этой переменной установленной, Claude Code сохраняет устаревший клон marketplace при сбое `git pull` и продолжает использовать последнее известное хорошее состояние. Для полностью автономных развертываний, где репозиторий никогда не будет доступен, используйте [`CLAUDE_CODE_PLUGIN_SEED_DIR`](#pre-populate-plugins-for-containers) для предварительного заполнения каталога плагинов во время сборки вместо этого.

## См. также

* [Обнаружение и установка готовых плагинов](/ru/discover-plugins) - Установка плагинов из существующих marketplace
* [Плагины](/ru/plugins) - Создание собственных плагинов
* [Справка плагинов](/ru/plugins-reference) - Полные технические спецификации и схемы
* [Параметры плагинов](/ru/settings#plugin-settings) - Параметры конфигурации плагинов
* [Справка strictKnownMarketplaces](/ru/settings#strictknownmarketplaces) - Ограничения управляемого marketplace
