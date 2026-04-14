> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Откройте и установите готовые плагины через маркетплейсы

> Найдите и установите плагины из маркетплейсов, чтобы расширить Claude Code новыми командами, агентами и возможностями.

Плагины расширяют Claude Code с помощью skills, agents, hooks и MCP servers. Маркетплейсы плагинов — это каталоги, которые помогают вам обнаруживать и устанавливать эти расширения без необходимости создавать их самостоятельно.

Ищете способ создать и распространять свой собственный маркетплейс? См. [Создание и распространение маркетплейса плагинов](/ru/plugin-marketplaces).

## Как работают маркетплейсы

Маркетплейс — это каталог плагинов, которые кто-то другой создал и поделился. Использование маркетплейса — это двухэтапный процесс:

<Steps>
  <Step title="Добавьте маркетплейс">
    Это регистрирует каталог в Claude Code, чтобы вы могли просмотреть доступные плагины. Никакие плагины еще не установлены.
  </Step>

  <Step title="Установите отдельные плагины">
    Просмотрите каталог и установите нужные вам плагины.
  </Step>
</Steps>

Думайте об этом как о добавлении магазина приложений: добавление магазина дает вам доступ к просмотру его коллекции, но вы все равно выбираете, какие приложения загружать отдельно.

## Официальный маркетплейс Anthropic

Официальный маркетплейс Anthropic (`claude-plugins-official`) автоматически доступен при запуске Claude Code. Запустите `/plugin` и перейдите на вкладку **Discover**, чтобы просмотреть доступные плагины, или просмотрите каталог на [claude.com/plugins](https://claude.com/plugins).

Чтобы установить плагин из официального маркетплейса, используйте `/plugin install <name>@claude-plugins-official`. Например, чтобы установить интеграцию GitHub:

```shell  theme={null}
/plugin install github@claude-plugins-official
```

<Note>
  Официальный маркетплейс поддерживается компанией Anthropic. Чтобы отправить плагин в официальный маркетплейс, используйте одну из встроенных форм отправки:

  * **Claude.ai**: [claude.ai/settings/plugins/submit](https://claude.ai/settings/plugins/submit)
  * **Console**: [platform.claude.com/plugins/submit](https://platform.claude.com/plugins/submit)

  Чтобы распространять плагины независимо, [создайте свой собственный маркетплейс](/ru/plugin-marketplaces) и поделитесь им с пользователями.
</Note>

Официальный маркетплейс включает несколько категорий плагинов:

### Code intelligence

Плагины code intelligence включают встроенный инструмент LSP в Claude Code, предоставляя Claude возможность переходить к определениям, находить ссылки и видеть ошибки типов сразу после редактирования. Эти плагины настраивают подключения [Language Server Protocol](https://microsoft.github.io/language-server-protocol/), той же технологии, которая обеспечивает code intelligence в VS Code.

Эти плагины требуют установки двоичного файла языкового сервера в вашей системе. Если у вас уже установлен языковой сервер, Claude может предложить вам установить соответствующий плагин при открытии проекта.

| Язык       | Plugin              | Требуемый двоичный файл      |
| :--------- | :------------------ | :--------------------------- |
| C/C++      | `clangd-lsp`        | `clangd`                     |
| C#         | `csharp-lsp`        | `csharp-ls`                  |
| Go         | `gopls-lsp`         | `gopls`                      |
| Java       | `jdtls-lsp`         | `jdtls`                      |
| Kotlin     | `kotlin-lsp`        | `kotlin-language-server`     |
| Lua        | `lua-lsp`           | `lua-language-server`        |
| PHP        | `php-lsp`           | `intelephense`               |
| Python     | `pyright-lsp`       | `pyright-langserver`         |
| Rust       | `rust-analyzer-lsp` | `rust-analyzer`              |
| Swift      | `swift-lsp`         | `sourcekit-lsp`              |
| TypeScript | `typescript-lsp`    | `typescript-language-server` |

Вы также можете [создать свой собственный LSP plugin](/ru/plugins-reference#lsp-servers) для других языков.

<Note>
  Если вы видите `Executable not found in $PATH` на вкладке `/plugin` Errors после установки плагина, установите требуемый двоичный файл из таблицы выше.
</Note>

#### Что Claude получает от плагинов code intelligence

После установки плагина code intelligence и доступности его двоичного файла языкового сервера Claude получает две возможности:

* **Автоматическая диагностика**: после каждого редактирования файла, которое делает Claude, языковой сервер анализирует изменения и автоматически сообщает об ошибках и предупреждениях. Claude видит ошибки типов, отсутствующие импорты и проблемы синтаксиса без необходимости запуска компилятора или линтера. Если Claude вводит ошибку, он замечает и исправляет проблему в том же ходу. Это не требует никакой конфигурации, кроме установки плагина. Вы можете видеть диагностику встроенной, нажав **Ctrl+O**, когда появляется индикатор "diagnostics found".
* **Code navigation**: Claude может использовать языковой сервер для перехода к определениям, поиска ссылок, получения информации о типе при наведении, списка символов, поиска реализаций и отслеживания иерархий вызовов. Эти операции дают Claude более точную навигацию, чем поиск на основе grep, хотя доступность может варьироваться в зависимости от языка и окружения.

Если у вас возникли проблемы, см. [Code intelligence troubleshooting](#code-intelligence-issues).

### External integrations

Эти плагины объединяют предварительно настроенные [MCP servers](/ru/mcp), чтобы вы могли подключить Claude к внешним сервисам без ручной настройки:

* **Source control**: `github`, `gitlab`
* **Project management**: `atlassian` (Jira/Confluence), `asana`, `linear`, `notion`
* **Design**: `figma`
* **Infrastructure**: `vercel`, `firebase`, `supabase`
* **Communication**: `slack`
* **Monitoring**: `sentry`

### Development workflows

Плагины, которые добавляют команды и агентов для общих задач разработки:

* **commit-commands**: рабочие процессы Git commit, включая commit, push и создание PR
* **pr-review-toolkit**: специализированные агенты для проверки pull requests
* **agent-sdk-dev**: инструменты для разработки с Claude Agent SDK
* **plugin-dev**: набор инструментов для создания собственных плагинов

### Output styles

Настройте способ ответа Claude:

* **explanatory-output-style**: образовательные сведения о выборе реализации
* **learning-output-style**: интерактивный режим обучения для развития навыков

## Попробуйте: добавьте демо-маркетплейс

Anthropic также поддерживает [демо-маркетплейс плагинов](https://github.com/anthropics/claude-code/tree/main/plugins) (`claude-code-plugins`) с примерами плагинов, которые показывают, что возможно с системой плагинов. В отличие от официального маркетплейса, вам нужно добавить этот вручную.

<Steps>
  <Step title="Добавьте маркетплейс">
    Из Claude Code запустите команду `plugin marketplace add` для маркетплейса `anthropics/claude-code`:

    ```shell  theme={null}
    /plugin marketplace add anthropics/claude-code
    ```

    Это загружает каталог маркетплейса и делает его плагины доступными для вас.
  </Step>

  <Step title="Просмотрите доступные плагины">
    Запустите `/plugin`, чтобы открыть менеджер плагинов. Это открывает интерфейс с вкладками с четырьмя вкладками, по которым вы можете переходить, используя **Tab** (или **Shift+Tab** для перемещения назад):

    * **Discover**: просмотрите доступные плагины из всех ваших маркетплейсов
    * **Installed**: просмотрите и управляйте установленными плагинами
    * **Marketplaces**: добавляйте, удаляйте или обновляйте добавленные маркетплейсы
    * **Errors**: просмотрите любые ошибки загрузки плагинов

    Перейдите на вкладку **Discover**, чтобы увидеть плагины из маркетплейса, который вы только что добавили.
  </Step>

  <Step title="Установите плагин">
    Выберите плагин для просмотра его деталей, затем выберите область установки:

    * **User scope**: установите для себя во всех проектах
    * **Project scope**: установите для всех сотрудников в этом репозитории
    * **Local scope**: установите для себя только в этом репозитории

    Например, выберите **commit-commands** (плагин, который добавляет команды рабочего процесса git) и установите его в область пользователя.

    Вы также можете установить непосредственно из командной строки:

    ```shell  theme={null}
    /plugin install commit-commands@anthropics-claude-code
    ```

    См. [Configuration scopes](/ru/settings#configuration-scopes), чтобы узнать больше об областях.
  </Step>

  <Step title="Используйте свой новый плагин">
    После установки запустите `/reload-plugins` для активации плагина. Команды плагина имеют пространство имен по имени плагина, поэтому **commit-commands** предоставляет команды вроде `/commit-commands:commit`.

    Попробуйте, внеся изменение в файл и запустив:

    ```shell  theme={null}
    /commit-commands:commit
    ```

    Это подготавливает ваши изменения, генерирует сообщение commit и создает commit.

    Каждый плагин работает по-разному. Проверьте описание плагина на вкладке **Discover** или на его домашней странице, чтобы узнать, какие команды и возможности он предоставляет.
  </Step>
</Steps>

Остальная часть этого руководства охватывает все способы добавления маркетплейсов, установки плагинов и управления вашей конфигурацией.

## Add marketplaces

Используйте команду `/plugin marketplace add` для добавления маркетплейсов из разных источников.

<Tip>
  **Shortcuts**: вы можете использовать `/plugin market` вместо `/plugin marketplace` и `rm` вместо `remove`.
</Tip>

* **GitHub repositories**: формат `owner/repo` (например, `anthropics/claude-code`)
* **Git URLs**: любой URL репозитория git (GitLab, Bitbucket, самостоятельно размещенные)
* **Local paths**: каталоги или прямые пути к файлам `marketplace.json`
* **Remote URLs**: прямые URL к размещенным файлам `marketplace.json`

### Add from GitHub

Добавьте репозиторий GitHub, который содержит файл `.claude-plugin/marketplace.json`, используя формат `owner/repo` — где `owner` — это имя пользователя GitHub или организация, а `repo` — это имя репозитория.

Например, `anthropics/claude-code` относится к репозиторию `claude-code`, принадлежащему `anthropics`:

```shell  theme={null}
/plugin marketplace add anthropics/claude-code
```

### Add from other Git hosts

Добавьте любой репозиторий git, предоставив полный URL. Это работает с любым хостом Git, включая GitLab, Bitbucket и самостоятельно размещенные серверы:

Используя HTTPS:

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git
```

Используя SSH:

```shell  theme={null}
/plugin marketplace add git@gitlab.com:company/plugins.git
```

Чтобы добавить конкретную ветку или тег, добавьте `#`, за которым следует ref:

```shell  theme={null}
/plugin marketplace add https://gitlab.com/company/plugins.git#v1.0.0
```

### Add from local paths

Добавьте локальный каталог, который содержит файл `.claude-plugin/marketplace.json`:

```shell  theme={null}
/plugin marketplace add ./my-marketplace
```

Вы также можете добавить прямой путь к файлу `marketplace.json`:

```shell  theme={null}
/plugin marketplace add ./path/to/marketplace.json
```

### Add from remote URLs

Добавьте удаленный файл `marketplace.json` через URL:

```shell  theme={null}
/plugin marketplace add https://example.com/marketplace.json
```

<Note>
  Маркетплейсы на основе URL имеют некоторые ограничения по сравнению с маркетплейсами на основе Git. Если вы столкнулись с ошибками "path not found" при установке плагинов, см. [Troubleshooting](/ru/plugin-marketplaces#plugins-with-relative-paths-fail-in-url-based-marketplaces).
</Note>

## Install plugins

После добавления маркетплейсов вы можете установить плагины напрямую (по умолчанию устанавливается в область пользователя):

```shell  theme={null}
/plugin install plugin-name@marketplace-name
```

Чтобы выбрать другую [installation scope](/ru/settings#configuration-scopes), используйте интерактивный интерфейс: запустите `/plugin`, перейдите на вкладку **Discover** и нажмите **Enter** на плагине. Вы увидите опции для:

* **User scope** (по умолчанию): установите для себя во всех проектах
* **Project scope**: установите для всех сотрудников в этом репозитории (добавляет в `.claude/settings.json`)
* **Local scope**: установите для себя только в этом репозитории (не делится с сотрудниками)

Вы также можете увидеть плагины с областью **managed** — они установлены администраторами через [managed settings](/ru/settings#settings-files) и не могут быть изменены.

Запустите `/plugin` и перейдите на вкладку **Installed**, чтобы увидеть ваши плагины, сгруппированные по области.

<Warning>
  Убедитесь, что вы доверяете плагину перед его установкой. Anthropic не контролирует, какие MCP servers, файлы или другое программное обеспечение включены в плагины, и не может проверить, что они работают как предполагается. Проверьте домашнюю страницу каждого плагина для получения дополнительной информации.
</Warning>

## Manage installed plugins

Запустите `/plugin` и перейдите на вкладку **Installed**, чтобы просмотреть, включить, отключить или удалить ваши плагины. Введите текст для фильтрации списка по имени плагина или описанию.

Вы также можете управлять плагинами с помощью прямых команд.

Отключите плагин без удаления:

```shell  theme={null}
/plugin disable plugin-name@marketplace-name
```

Повторно включите отключенный плагин:

```shell  theme={null}
/plugin enable plugin-name@marketplace-name
```

Полностью удалите плагин:

```shell  theme={null}
/plugin uninstall plugin-name@marketplace-name
```

Опция `--scope` позволяет вам нацелить определенную область с помощью команд CLI:

```shell  theme={null}
claude plugin install formatter@your-org --scope project
claude plugin uninstall formatter@your-org --scope project
```

### Apply plugin changes without restarting

Когда вы устанавливаете, включаете или отключаете плагины во время сеанса, запустите `/reload-plugins` для активации всех изменений без перезагрузки:

```shell  theme={null}
/reload-plugins
```

Claude Code перезагружает все активные плагины и показывает количество плагинов, skills, agents, hooks, plugin MCP servers и plugin LSP servers.

## Manage marketplaces

Вы можете управлять маркетплейсами через интерактивный интерфейс `/plugin` или с помощью команд CLI.

### Use the interactive interface

Запустите `/plugin` и перейдите на вкладку **Marketplaces** для:

* Просмотра всех добавленных маркетплейсов с их источниками и статусом
* Добавления новых маркетплейсов
* Обновления списков маркетплейсов для получения последних плагинов
* Удаления маркетплейсов, которые вам больше не нужны

### Use CLI commands

Вы также можете управлять маркетплейсами с помощью прямых команд.

Список всех настроенных маркетплейсов:

```shell  theme={null}
/plugin marketplace list
```

Обновите списки плагинов из маркетплейса:

```shell  theme={null}
/plugin marketplace update marketplace-name
```

Удалите маркетплейс:

```shell  theme={null}
/plugin marketplace remove marketplace-name
```

<Warning>
  Удаление маркетплейса приведет к удалению всех плагинов, которые вы установили из него.
</Warning>

### Configure auto-updates

Claude Code может автоматически обновлять маркетплейсы и установленные плагины при запуске. Когда автоматическое обновление включено для маркетплейса, Claude Code обновляет данные маркетплейса и обновляет установленные плагины до их последних версий. Если какие-либо плагины были обновлены, вы увидите уведомление с предложением запустить `/reload-plugins`.

Переключайте автоматическое обновление для отдельных маркетплейсов через интерфейс:

1. Запустите `/plugin`, чтобы открыть менеджер плагинов
2. Выберите **Marketplaces**
3. Выберите маркетплейс из списка
4. Выберите **Enable auto-update** или **Disable auto-update**

Официальные маркетплейсы Anthropic имеют автоматическое обновление, включенное по умолчанию. Маркетплейсы третьих сторон и локальной разработки имеют автоматическое обновление, отключенное по умолчанию.

Чтобы полностью отключить все автоматические обновления для Claude Code и всех плагинов, установите переменную окружения `DISABLE_AUTOUPDATER`. См. [Auto updates](/ru/setup#auto-updates) для получения подробной информации.

Чтобы сохранить автоматические обновления плагинов включенными при отключении автоматических обновлений Claude Code, установите `FORCE_AUTOUPDATE_PLUGINS=1` вместе с `DISABLE_AUTOUPDATER`:

```bash  theme={null}
export DISABLE_AUTOUPDATER=1
export FORCE_AUTOUPDATE_PLUGINS=1
```

Это полезно, когда вы хотите управлять обновлениями Claude Code вручную, но все еще получать автоматические обновления плагинов.

## Configure team marketplaces

Администраторы команды могут настроить автоматическую установку маркетплейса для проектов, добавив конфигурацию маркетплейса в `.claude/settings.json`. Когда члены команды доверяют папке репозитория, Claude Code предлагает им установить эти маркетплейсы и плагины.

Добавьте `extraKnownMarketplaces` в `.claude/settings.json` вашего проекта:

```json  theme={null}
{
  "extraKnownMarketplaces": {
    "my-team-tools": {
      "source": {
        "source": "github",
        "repo": "your-org/claude-plugins"
      }
    }
  }
}
```

Для полных опций конфигурации, включая `extraKnownMarketplaces` и `enabledPlugins`, см. [Plugin settings](/ru/settings#plugin-settings).

## Security

Плагины и маркетплейсы — это высоконадежные компоненты, которые могут выполнять произвольный код на вашей машине с вашими привилегиями пользователя. Устанавливайте плагины и добавляйте маркетплейсы только из источников, которым вы доверяете. Организации могут ограничить, какие маркетплейсы пользователям разрешено добавлять, используя [managed marketplace restrictions](/ru/plugin-marketplaces#managed-marketplace-restrictions).

## Troubleshooting

### /plugin command not recognized

Если вы видите "unknown command" или команда `/plugin` не появляется:

1. **Check your version**: запустите `claude --version`, чтобы увидеть, что установлено.
2. **Update Claude Code**:
   * **Homebrew**: `brew upgrade claude-code`
   * **npm**: `npm update -g @anthropic-ai/claude-code`
   * **Native installer**: повторно запустите команду установки из [Setup](/ru/setup)
3. **Restart Claude Code**: после обновления перезагрузите терминал и снова запустите `claude`.

### Common issues

* **Marketplace not loading**: проверьте, что URL доступен и что `.claude-plugin/marketplace.json` существует по пути
* **Plugin installation failures**: проверьте, что URL источника плагина доступны и репозитории являются общедоступными (или у вас есть доступ)
* **Files not found after installation**: плагины копируются в кэш, поэтому пути, ссылающиеся на файлы вне каталога плагина, не будут работать
* **Plugin skills not appearing**: очистите кэш с помощью `rm -rf ~/.claude/plugins/cache`, перезагрузите Claude Code и переустановите плагин.

Для подробного устранения неполадок с решениями см. [Troubleshooting](/ru/plugin-marketplaces#troubleshooting) в руководстве маркетплейса. Для инструментов отладки см. [Debugging and development tools](/ru/plugins-reference#debugging-and-development-tools).

### Code intelligence issues

* **Language server not starting**: проверьте, что двоичный файл установлен и доступен в вашем `$PATH`. Проверьте вкладку `/plugin` Errors для получения подробной информации.
* **High memory usage**: языковые серверы, такие как `rust-analyzer` и `pyright`, могут потреблять значительную память на больших проектах. Если вы испытываете проблемы с памятью, отключите плагин с помощью `/plugin disable <plugin-name>` и вместо этого полагайтесь на встроенные инструменты поиска Claude.
* **False positive diagnostics in monorepos**: языковые серверы могут сообщать об ошибках неразрешенного импорта для внутренних пакетов, если рабочее пространство не настроено правильно. Это не влияет на способность Claude редактировать код.

## Next steps

* **Build your own plugins**: см. [Plugins](/ru/plugins) для создания skills, agents и hooks
* **Create a marketplace**: см. [Create a plugin marketplace](/ru/plugin-marketplaces) для распространения плагинов вашей команде или сообществу
* **Technical reference**: см. [Plugins reference](/ru/plugins-reference) для полных спецификаций
