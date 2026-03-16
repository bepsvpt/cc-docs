> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Обзор Claude Code

> Claude Code — это агентский инструмент кодирования, который читает вашу кодовую базу, редактирует файлы, выполняет команды и интегрируется с вашими инструментами разработки. Доступен в вашем терминале, IDE, приложении для рабочего стола и браузере.

Claude Code — это AI-помощник по кодированию, который помогает вам создавать функции, исправлять ошибки и автоматизировать задачи разработки. Он понимает всю вашу кодовую базу и может работать с несколькими файлами и инструментами для выполнения задач.

## Начало работы

Выберите вашу среду для начала работы. Большинство поверхностей требуют [подписку Claude](https://claude.com/pricing) или учетную запись [Anthropic Console](https://console.anthropic.com/). Terminal CLI и VS Code также поддерживают [сторонних поставщиков](/ru/third-party-integrations).

<Tabs>
  <Tab title="Terminal">
    Полнофункциональный CLI для работы с Claude Code прямо в вашем терминале. Редактируйте файлы, выполняйте команды и управляйте всем проектом из командной строки.

    To install Claude Code, use one of the following methods:

    <Tabs>
      <Tab title="Native Install (Recommended)">
        **macOS, Linux, WSL:**

        ```bash  theme={null}
        curl -fsSL https://claude.ai/install.sh | bash
        ```

        **Windows PowerShell:**

        ```powershell  theme={null}
        irm https://claude.ai/install.ps1 | iex
        ```

        **Windows CMD:**

        ```batch  theme={null}
        curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
        ```

        **Windows requires [Git for Windows](https://git-scm.com/downloads/win).** Install it first if you don't have it.

        <Info>
          Native installations automatically update in the background to keep you on the latest version.
        </Info>
      </Tab>

      <Tab title="Homebrew">
        ```bash  theme={null}
        brew install --cask claude-code
        ```

        <Info>
          Homebrew installations do not auto-update. Run `brew upgrade claude-code` periodically to get the latest features and security fixes.
        </Info>
      </Tab>

      <Tab title="WinGet">
        ```powershell  theme={null}
        winget install Anthropic.ClaudeCode
        ```

        <Info>
          WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
        </Info>
      </Tab>
    </Tabs>

    Затем запустите Claude Code в любом проекте:

    ```bash  theme={null}
    cd your-project
    claude
    ```

    При первом использовании вам будет предложено войти. Вот и все! [Продолжите с Quickstart →](/ru/quickstart)

    <Tip>
      Смотрите [расширенную настройку](/ru/setup) для опций установки, ручных обновлений или инструкций по удалению. Посетите [troubleshooting](/ru/troubleshooting), если у вас возникли проблемы.
    </Tip>
  </Tab>

  <Tab title="VS Code">
    Расширение VS Code предоставляет встроенные различия, @-упоминания, проверку плана и историю разговоров прямо в вашем редакторе.

    * [Установить для VS Code](vscode:extension/anthropic.claude-code)
    * [Установить для Cursor](cursor:extension/anthropic.claude-code)

    Или найдите "Claude Code" в представлении расширений (`Cmd+Shift+X` на Mac, `Ctrl+Shift+X` на Windows/Linux). После установки откройте палитру команд (`Cmd+Shift+P` / `Ctrl+Shift+P`), введите "Claude Code" и выберите **Open in New Tab**.

    [Начните работу с VS Code →](/ru/vs-code#get-started)
  </Tab>

  <Tab title="Desktop app">
    Автономное приложение для запуска Claude Code вне вашей IDE или терминала. Просматривайте различия визуально, запускайте несколько сеансов рядом, планируйте повторяющиеся задачи и запускайте облачные сеансы.

    Загрузите и установите:

    * [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) (Intel и Apple Silicon)
    * [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) (x64)
    * [Windows ARM64](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) (только удаленные сеансы)

    После установки запустите Claude, войдите и нажмите вкладку **Code** для начала кодирования. Требуется [платная подписка](https://claude.com/pricing).

    [Узнайте больше о приложении для рабочего стола →](/ru/desktop-quickstart)
  </Tab>

  <Tab title="Web">
    Запустите Claude Code в вашем браузере без локальной настройки. Запускайте долгоживущие задачи и возвращайтесь, когда они будут готовы, работайте с репозиториями, которые у вас нет локально, или запускайте несколько задач параллельно. Доступно на настольных браузерах и приложении Claude iOS.

    Начните кодирование на [claude.ai/code](https://claude.ai/code).

    [Начните работу в веб-версии →](/ru/claude-code-on-the-web#getting-started)
  </Tab>

  <Tab title="JetBrains">
    Плагин для IntelliJ IDEA, PyCharm, WebStorm и других IDE JetBrains с интерактивным просмотром различий и совместным использованием контекста выделения.

    Установите [плагин Claude Code](https://plugins.jetbrains.com/plugin/27310-claude-code-beta-) из JetBrains Marketplace и перезагрузите вашу IDE.

    [Начните работу с JetBrains →](/ru/jetbrains)
  </Tab>
</Tabs>

## Что вы можете делать

Вот некоторые способы использования Claude Code:

<AccordionGroup>
  <Accordion title="Автоматизируйте работу, которую вы постоянно откладываете" icon="wand-magic-sparkles">
    Claude Code справляется с утомительными задачами, которые съедают ваш день: написание тестов для непроверенного кода, исправление ошибок lint по всему проекту, разрешение конфликтов слияния, обновление зависимостей и написание заметок о выпуске.

    ```bash  theme={null}
    claude "write tests for the auth module, run them, and fix any failures"
    ```
  </Accordion>

  <Accordion title="Создавайте функции и исправляйте ошибки" icon="hammer">
    Опишите то, что вы хотите, на простом языке. Claude Code планирует подход, пишет код в нескольких файлах и проверяет, что он работает.

    Для ошибок вставьте сообщение об ошибке или опишите симптом. Claude Code отслеживает проблему через вашу кодовую базу, определяет основную причину и реализует исправление. Смотрите [распространенные рабочие процессы](/ru/common-workflows) для получения дополнительных примеров.
  </Accordion>

  <Accordion title="Создавайте коммиты и pull requests" icon="code-branch">
    Claude Code работает непосредственно с git. Он подготавливает изменения, пишет сообщения коммитов, создает ветки и открывает pull requests.

    ```bash  theme={null}
    claude "commit my changes with a descriptive message"
    ```

    В CI вы можете автоматизировать проверку кода и сортировку проблем с помощью [GitHub Actions](/ru/github-actions) или [GitLab CI/CD](/ru/gitlab-ci-cd).
  </Accordion>

  <Accordion title="Подключите свои инструменты с помощью MCP" icon="plug">
    [Model Context Protocol (MCP)](/ru/mcp) — это открытый стандарт для подключения инструментов AI к внешним источникам данных. С помощью MCP Claude Code может читать ваши документы дизайна в Google Drive, обновлять задачи в Jira, извлекать данные из Slack или использовать ваши собственные пользовательские инструменты.
  </Accordion>

  <Accordion title="Настройте с помощью инструкций, skills и hooks" icon="sliders">
    [`CLAUDE.md`](/ru/memory) — это файл markdown, который вы добавляете в корень вашего проекта, и Claude Code читает его в начале каждого сеанса. Используйте его для установки стандартов кодирования, решений по архитектуре, предпочитаемых библиотек и контрольных списков проверки. Claude также создает [автоматическую память](/ru/memory#auto-memory) по мере работы, сохраняя знания, такие как команды сборки и идеи отладки, в разных сеансах без вашего участия.

    Создавайте [пользовательские команды](/ru/skills) для упаковки повторяемых рабочих процессов, которые ваша команда может использовать, например `/review-pr` или `/deploy-staging`.

    [Hooks](/ru/hooks) позволяют вам запускать команды shell до или после действий Claude Code, например автоматическое форматирование после каждого редактирования файла или запуск lint перед коммитом.
  </Accordion>

  <Accordion title="Запускайте команды агентов и создавайте пользовательских агентов" icon="users">
    Запускайте [несколько агентов Claude Code](/ru/sub-agents), которые работают над разными частями задачи одновременно. Главный агент координирует работу, назначает подзадачи и объединяет результаты.

    Для полностью пользовательских рабочих процессов [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview) позволяет вам создавать собственных агентов, работающих на инструментах и возможностях Claude Code, с полным контролем над оркестровкой, доступом к инструментам и разрешениями.
  </Accordion>

  <Accordion title="Передавайте, создавайте скрипты и автоматизируйте с помощью CLI" icon="terminal">
    Claude Code является составным и следует философии Unix. Передавайте в него логи, запускайте его в CI или объединяйте его с другими инструментами:

    ```bash  theme={null}
    # Monitor logs and get alerted
    tail -f app.log | claude -p "Slack me if you see any anomalies"

    # Automate translations in CI
    claude -p "translate new strings into French and raise a PR for review"

    # Bulk operations across files
    git diff main --name-only | claude -p "review these changed files for security issues"
    ```

    Смотрите [справочник CLI](/ru/cli-reference) для полного набора команд и флагов.
  </Accordion>

  <Accordion title="Работайте откуда угодно" icon="globe">
    Сеансы не привязаны к одной поверхности. Перемещайте работу между средами по мере изменения вашего контекста:

    * Отойдите от своего стола и продолжайте работать со своего телефона или любого браузера с помощью [Remote Control](/ru/remote-control)
    * Запустите долгоживущую задачу в [веб-версии](/ru/claude-code-on-the-web) или [приложении iOS](https://apps.apple.com/app/claude-by-anthropic/id6473753684), затем перенесите ее в свой терминал с помощью `/teleport`
    * Передайте сеанс терминала [приложению для рабочего стола](/ru/desktop) с помощью `/desktop` для визуальной проверки различий
    * Маршрутизируйте задачи из командного чата: упомяните `@Claude` в [Slack](/ru/slack) с отчетом об ошибке и получите pull request обратно
  </Accordion>
</AccordionGroup>

## Используйте Claude Code везде

Каждая поверхность подключается к одному и тому же базовому механизму Claude Code, поэтому ваши файлы CLAUDE.md, параметры и MCP servers работают на всех них.

Помимо сред [Terminal](/ru/quickstart), [VS Code](/ru/vs-code), [JetBrains](/ru/jetbrains), [Desktop](/ru/desktop) и [Web](/ru/claude-code-on-the-web) выше, Claude Code интегрируется с CI/CD, чатом и рабочими процессами браузера:

| Я хочу...                                                                  | Лучший вариант                                                                                                             |
| -------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| Продолжить локальный сеанс со своего телефона или другого устройства       | [Remote Control](/ru/remote-control)                                                                                       |
| Начать задачу локально, продолжить на мобильном                            | [Web](/ru/claude-code-on-the-web) или [приложение Claude iOS](https://apps.apple.com/app/claude-by-anthropic/id6473753684) |
| Автоматизировать проверки PR и сортировку проблем                          | [GitHub Actions](/ru/github-actions) или [GitLab CI/CD](/ru/gitlab-ci-cd)                                                  |
| Получить автоматическую проверку кода на каждый PR                         | [GitHub Code Review](/ru/code-review)                                                                                      |
| Маршрутизировать отчеты об ошибках из Slack в pull requests                | [Slack](/ru/slack)                                                                                                         |
| Отладить живые веб-приложения                                              | [Chrome](/ru/chrome)                                                                                                       |
| Создавать пользовательских агентов для ваших собственных рабочих процессов | [Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)                                                        |

## Следующие шаги

После установки Claude Code эти руководства помогут вам углубиться.

* [Quickstart](/ru/quickstart): пройдите через вашу первую реальную задачу, от изучения кодовой базы до коммита исправления
* [Сохраняйте инструкции и воспоминания](/ru/memory): дайте Claude постоянные инструкции с файлами CLAUDE.md и автоматической памятью
* [Распространенные рабочие процессы](/ru/common-workflows) и [лучшие практики](/ru/best-practices): шаблоны для получения максимума от Claude Code
* [Параметры](/ru/settings): настройте Claude Code для вашего рабочего процесса
* [Troubleshooting](/ru/troubleshooting): решения для распространенных проблем
* [code.claude.com](https://code.claude.com/): демонстрации, цены и детали продукта
