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

# Начало работы с настольным приложением

> Установите Claude Code на рабочий стол и начните свой первый сеанс кодирования

Настольное приложение предоставляет вам Claude Code с графическим интерфейсом: визуальный просмотр различий, предпросмотр приложения в реальном времени, мониторинг GitHub PR с автоматическим слиянием, параллельные сеансы с изоляцией Git worktrees, запланированные задачи и возможность запуска задач удаленно. Терминал не требуется.

На этой странице описывается установка приложения и начало вашего первого сеанса. Если вы уже настроены, см. [Использование Claude Code Desktop](/ru/desktop) для полного справочника.

<Frame>
  <img src="https://mintcdn.com/claude-code/CNLUpFGiXoc9mhvD/images/desktop-code-tab-light.png?fit=max&auto=format&n=CNLUpFGiXoc9mhvD&q=85&s=9a36a7a27b9f4c6f2e1c83bdb34f69ce" className="block dark:hidden" alt="Интерфейс Claude Code Desktop, показывающий выбранную вкладку Code с полем подсказки, селектором режима разрешений, установленным на Ask permissions, средством выбора модели, селектором папки и опцией Local environment" width="2500" height="1376" data-path="images/desktop-code-tab-light.png" />

  <img src="https://mintcdn.com/claude-code/CNLUpFGiXoc9mhvD/images/desktop-code-tab-dark.png?fit=max&auto=format&n=CNLUpFGiXoc9mhvD&q=85&s=5463defe81c459fb9b1f91f6a958cfb8" className="hidden dark:block" alt="Интерфейс Claude Code Desktop в темном режиме, показывающий выбранную вкладку Code с полем подсказки, селектором режима разрешений, установленным на Ask permissions, средством выбора модели, селектором папки и опцией Local environment" width="2504" height="1374" data-path="images/desktop-code-tab-dark.png" />
</Frame>

Настольное приложение имеет три вкладки:

* **Chat**: Общее общение без доступа к файлам, аналогично claude.ai.
* **Cowork**: Автономный фоновый агент, который работает над задачами в облачной виртуальной машине с собственной средой. Он может работать независимо, пока вы занимаетесь другой работой.
* **Code**: Интерактивный помощник по кодированию с прямым доступом к вашим локальным файлам. Вы просматриваете и одобряете каждое изменение в реальном времени.

Chat и Cowork рассматриваются в [статьях поддержки Claude Desktop](https://support.claude.com/en/collections/16163169-claude-desktop). На этой странице основное внимание уделяется вкладке **Code**.

<Note>
  Claude Code требует [подписку Pro, Max, Teams или Enterprise](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=desktop_quickstart_pricing).
</Note>

## Установка

<Steps>
  <Step title="Загрузите приложение">
    Загрузите Claude для вашей платформы.

    <CardGroup cols={2}>
      <Card title="macOS" icon="apple" href="https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code&utm_medium=docs">
        Универсальная сборка для Intel и Apple Silicon
      </Card>

      <Card title="Windows" icon="windows" href="https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code&utm_medium=docs">
        Для процессоров x64
      </Card>
    </CardGroup>

    Для Windows ARM64 [загрузите здесь](https://claude.ai/api/desktop/win32/arm64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs).

    Linux в настоящее время не поддерживается.
  </Step>

  <Step title="Войдите в систему">
    Запустите Claude из папки Applications (macOS) или меню Start (Windows). Войдите со своей учетной записью Anthropic.
  </Step>

  <Step title="Откройте вкладку Code">
    Нажмите на вкладку **Code** в верхнем центре. Если нажатие на Code предлагает вам обновиться, вам необходимо сначала [подписаться на платный план](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=desktop_quickstart_upgrade). Если он предлагает вам войти в систему онлайн, завершите вход и перезагрузите приложение. Если вы видите ошибку 403, см. [устранение неполадок аутентификации](/ru/desktop#403-or-authentication-errors-in-the-code-tab).
  </Step>
</Steps>

Настольное приложение включает Claude Code. Вам не нужно устанавливать Node.js или CLI отдельно. Чтобы использовать `claude` из терминала, установите CLI отдельно. См. [Начало работы с CLI](/ru/quickstart).

## Начните свой первый сеанс

С открытой вкладкой Code выберите проект и дайте Claude что-нибудь сделать.

<Steps>
  <Step title="Выберите среду и папку">
    Выберите **Local**, чтобы запустить Claude на вашем компьютере, используя ваши файлы напрямую. Нажмите **Select folder** и выберите каталог вашего проекта.

    <Tip>
      Начните с небольшого проекта, который вы хорошо знаете. Это самый быстрый способ увидеть, что может делать Claude Code. На Windows [Git](https://git-scm.com/downloads/win) должен быть установлен для работы локальных сеансов. На большинстве Mac Git включен по умолчанию.
    </Tip>

    Вы также можете выбрать:

    * **Remote**: Запуск сеансов на облачной инфраструктуре Anthropic, которые продолжаются даже если вы закроете приложение. Удаленные сеансы используют ту же инфраструктуру, что и [Claude Code в веб-версии](/ru/claude-code-on-the-web).
    * **SSH**: Подключитесь к удаленной машине через SSH (ваши собственные серверы, облачные виртуальные машины или dev containers). Claude Code должен быть установлен на удаленной машине.
  </Step>

  <Step title="Выберите модель">
    Выберите модель из раскрывающегося списка рядом с кнопкой отправки. См. [модели](/ru/model-config#available-models) для сравнения Opus, Sonnet и Haiku. Вы не можете изменить модель после начала сеанса.
  </Step>

  <Step title="Скажите Claude, что делать">
    Введите, что вы хотите, чтобы Claude сделал:

    * `Find a TODO comment and fix it`
    * `Add tests for the main function`
    * `Create a CLAUDE.md with instructions for this codebase`

    [Сеанс](/ru/desktop#work-in-parallel-with-sessions) — это беседа с Claude о вашем коде. Каждый сеанс отслеживает свой собственный контекст и изменения, поэтому вы можете работать над несколькими задачами без их взаимного влияния.
  </Step>

  <Step title="Просмотрите и примите изменения">
    По умолчанию вкладка Code запускается в [режиме Ask permissions](/ru/desktop#choose-a-permission-mode), где Claude предлагает изменения и ждет вашего одобрения перед их применением. Вы увидите:

    1. [Представление различий](/ru/desktop#review-changes-with-diff-view), показывающее точно, что изменится в каждом файле
    2. Кнопки Accept/Reject для одобрения или отклонения каждого изменения
    3. Обновления в реальном времени по мере работы Claude над вашим запросом

    Если вы отклоните изменение, Claude спросит, как вы хотели бы действовать иначе. Ваши файлы не будут изменены, пока вы не примете их.
  </Step>
</Steps>

## Что дальше?

Вы сделали свое первое редактирование. Для полного справочника по всему, что может делать Desktop, см. [Использование Claude Code Desktop](/ru/desktop). Вот несколько вещей, которые стоит попробовать дальше.

**Прерывайте и направляйте.** Вы можете прервать Claude в любой момент. Если он идет по неправильному пути, нажмите кнопку остановки или введите свое исправление и нажмите **Enter**. Claude останавливает то, что он делает, и корректирует на основе вашего ввода. Вам не нужно ждать, пока он закончит, или начинать заново.

**Дайте Claude больше контекста.** Введите `@filename` в поле подсказки, чтобы вытащить конкретный файл в беседу, прикрепите изображения и PDF-файлы с помощью кнопки вложения или перетащите файлы прямо в подсказку. Чем больше контекста у Claude, тем лучше результаты. См. [Добавление файлов и контекста](/ru/desktop#add-files-and-context-to-prompts).

**Используйте skills для повторяющихся задач.** Введите `/` или нажмите **+** → **Slash commands**, чтобы просмотреть [встроенные команды](/ru/commands), [пользовательские skills](/ru/skills) и skills плагинов. Skills — это переиспользуемые подсказки, которые вы можете вызывать всякий раз, когда они вам нужны, например контрольные списки проверки кода или этапы развертывания.

**Просмотрите изменения перед фиксацией.** После того как Claude отредактирует файлы, появляется индикатор `+12 -1`. Нажмите на него, чтобы открыть [представление различий](/ru/desktop#review-changes-with-diff-view), просмотрите изменения файл за файлом и оставляйте комментарии к определенным строкам. Claude читает ваши комментарии и пересматривает. Нажмите **Review code**, чтобы Claude оценил различия сам и оставил встроенные предложения.

**Отрегулируйте, сколько контроля у вас есть.** Ваш [режим разрешений](/ru/desktop#choose-a-permission-mode) контролирует баланс. Ask permissions (по умолчанию) требует одобрения перед каждым редактированием. Auto accept edits автоматически принимает редактирование файлов для более быстрой итерации. Plan mode позволяет Claude наметить подход без касания каких-либо файлов, что полезно перед крупным рефакторингом.

**Добавьте плагины для большей функциональности.** Нажмите кнопку **+** рядом с полем подсказки и выберите **Plugins**, чтобы просмотреть и установить [плагины](/ru/desktop#install-plugins), которые добавляют skills, агентов, MCP servers и многое другое.

**Предпросмотрите ваше приложение.** Нажмите на раскрывающееся меню **Preview**, чтобы запустить ваш dev server прямо в настольном приложении. Claude может просмотреть работающее приложение, протестировать конечные точки, проверить журналы и повторить то, что он видит. См. [Предпросмотр вашего приложения](/ru/desktop#preview-your-app).

**Отслеживайте ваш pull request.** После открытия PR, Claude Code отслеживает результаты проверок CI и может автоматически исправить сбои или объединить PR после прохождения всех проверок. См. [Мониторинг статуса pull request](/ru/desktop#monitor-pull-request-status).

**Поставьте Claude по расписанию.** Установите [запланированные задачи](/ru/desktop#schedule-recurring-tasks) для автоматического запуска Claude на повторяющейся основе: ежедневный обзор кода каждое утро, еженедельный аудит зависимостей или брифинг, который извлекает данные из ваших подключенных инструментов.

**Масштабируйте, когда будете готовы.** Откройте [параллельные сеансы](/ru/desktop#work-in-parallel-with-sessions) из боковой панели, чтобы работать над несколькими задачами одновременно, каждая в своем собственном Git worktree. Отправьте [долгосрочную работу в облако](/ru/desktop#run-long-running-tasks-remotely), чтобы она продолжалась даже если вы закроете приложение, или [продолжите сеанс в веб-версии или в вашей IDE](/ru/desktop#continue-in-another-surface), если задача займет больше времени, чем ожидалось. [Подключите внешние инструменты](/ru/desktop#extend-claude-code), такие как GitHub, Slack и Linear, чтобы объединить ваш рабочий процесс.

## Переходите с CLI?

Desktop запускает тот же движок, что и CLI, с графическим интерфейсом. Вы можете запускать оба одновременно на одном проекте, и они совместно используют конфигурацию (файлы CLAUDE.md, MCP servers, hooks, skills и параметры). Для полного сравнения функций, эквивалентов флагов и того, что недоступно в Desktop, см. [Сравнение CLI](/ru/desktop#coming-from-the-cli).

## Что дальше

* [Использование Claude Code Desktop](/ru/desktop): режимы разрешений, параллельные сеансы, представление различий, соединители и конфигурация предприятия
* [Устранение неполадок](/ru/desktop#troubleshooting): решения для распространенных ошибок и проблем с настройкой
* [Лучшие практики](/ru/best-practices): советы по написанию эффективных подсказок и максимальному использованию Claude Code
* [Распространенные рабочие процессы](/ru/common-workflows): учебники по отладке, рефакторингу, тестированию и многому другому
