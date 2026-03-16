> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Быстрый старт

> Добро пожаловать в Claude Code!

Это руководство по быстрому старту позволит вам использовать AI-powered кодирование всего за несколько минут. К концу вы поймёте, как использовать Claude Code для типичных задач разработки.

## Перед началом

Убедитесь, что у вас есть:

* Открытый терминал или командная строка
  * Если вы никогда раньше не использовали терминал, ознакомьтесь с [руководством по терминалу](/ru/terminal-guide)
* Проект кода для работы
* [Подписка Claude](https://claude.com/pricing) (Pro, Max, Teams или Enterprise), учётная запись [Claude Console](https://console.anthropic.com/) или доступ через [поддерживаемого облачного провайдера](/ru/third-party-integrations)

<Note>
  Это руководство охватывает CLI терминала. Claude Code также доступен в [веб-версии](https://claude.ai/code), как [настольное приложение](/ru/desktop), в [VS Code](/ru/vs-code) и [JetBrains IDEs](/ru/jetbrains), в [Slack](/ru/slack) и в CI/CD с [GitHub Actions](/ru/github-actions) и [GitLab](/ru/gitlab-ci-cd). Смотрите [все интерфейсы](/ru/overview#use-claude-code-everywhere).
</Note>

## Шаг 1: Установите Claude Code

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

## Шаг 2: Войдите в свою учётную запись

Claude Code требует учётную запись для использования. Когда вы начнёте интерактивный сеанс с командой `claude`, вам нужно будет войти:

```bash  theme={null}
claude
# При первом использовании вам будет предложено войти
```

```bash  theme={null}
/login
# Следуйте подсказкам для входа в свою учётную запись
```

Вы можете войти, используя любой из этих типов учётных записей:

* [Claude Pro, Max, Teams или Enterprise](https://claude.com/pricing) (рекомендуется)
* [Claude Console](https://console.anthropic.com/) (доступ к API с предоплаченными кредитами). При первом входе в Console автоматически создаётся рабочее пространство "Claude Code" для централизованного отслеживания затрат.
* [Amazon Bedrock, Google Vertex AI или Microsoft Foundry](/ru/third-party-integrations) (облачные провайдеры для предприятий)

После входа ваши учётные данные сохраняются, и вам не нужно будет входить снова. Чтобы позже переключиться на другую учётную запись, используйте команду `/login`.

## Шаг 3: Начните свой первый сеанс

Откройте терминал в любом каталоге проекта и запустите Claude Code:

```bash  theme={null}
cd /path/to/your/project
claude
```

Вы увидите экран приветствия Claude Code с информацией о вашем сеансе, недавними разговорами и последними обновлениями. Введите `/help` для доступных команд или `/resume` для продолжения предыдущего разговора.

<Tip>
  После входа (Шаг 2) ваши учётные данные сохраняются на вашей системе. Узнайте больше в [Управлении учётными данными](/ru/authentication#credential-management).
</Tip>

## Шаг 4: Задайте свой первый вопрос

Давайте начнём с понимания вашей кодовой базы. Попробуйте одну из этих команд:

```text  theme={null}
what does this project do?
```

Claude проанализирует ваши файлы и предоставит резюме. Вы также можете задать более конкретные вопросы:

```text  theme={null}
what technologies does this project use?
```

```text  theme={null}
where is the main entry point?
```

```text  theme={null}
explain the folder structure
```

Вы также можете спросить Claude о его собственных возможностях:

```text  theme={null}
what can Claude Code do?
```

```text  theme={null}
how do I create custom skills in Claude Code?
```

```text  theme={null}
can Claude Code work with Docker?
```

<Note>
  Claude Code читает файлы вашего проекта по мере необходимости. Вам не нужно вручную добавлять контекст.
</Note>

## Шаг 5: Сделайте своё первое изменение кода

Теперь давайте заставим Claude Code выполнить реальное кодирование. Попробуйте простую задачу:

```text  theme={null}
add a hello world function to the main file
```

Claude Code будет:

1. Найти подходящий файл
2. Показать вам предложенные изменения
3. Попросить ваше одобрение
4. Сделать редактирование

<Note>
  Claude Code всегда просит разрешение перед изменением файлов. Вы можете одобрить отдельные изменения или включить режим "Accept all" для сеанса.
</Note>

## Шаг 6: Используйте Git с Claude Code

Claude Code делает операции Git разговорными:

```text  theme={null}
what files have I changed?
```

```text  theme={null}
commit my changes with a descriptive message
```

Вы также можете запросить более сложные операции Git:

```text  theme={null}
create a new branch called feature/quickstart
```

```text  theme={null}
show me the last 5 commits
```

```text  theme={null}
help me resolve merge conflicts
```

## Шаг 7: Исправьте ошибку или добавьте функцию

Claude хорошо справляется с отладкой и реализацией функций.

Опишите то, что вы хотите, на естественном языке:

```text  theme={null}
add input validation to the user registration form
```

Или исправьте существующие проблемы:

```text  theme={null}
there's a bug where users can submit empty forms - fix it
```

Claude Code будет:

* Найти соответствующий код
* Понять контекст
* Реализовать решение
* Запустить тесты, если они доступны

## Шаг 8: Попробуйте другие типичные рабочие процессы

Есть несколько способов работать с Claude:

**Рефакторинг кода**

```text  theme={null}
refactor the authentication module to use async/await instead of callbacks
```

**Написание тестов**

```text  theme={null}
write unit tests for the calculator functions
```

**Обновление документации**

```text  theme={null}
update the README with installation instructions
```

**Проверка кода**

```text  theme={null}
review my changes and suggest improvements
```

<Tip>
  Разговаривайте с Claude как с полезным коллегой. Опишите, чего вы хотите достичь, и он поможет вам это сделать.
</Tip>

## Основные команды

Вот наиболее важные команды для ежедневного использования:

| Команда             | Что она делает                                         | Пример                              |
| ------------------- | ------------------------------------------------------ | ----------------------------------- |
| `claude`            | Запустить интерактивный режим                          | `claude`                            |
| `claude "task"`     | Запустить одноразовую задачу                           | `claude "fix the build error"`      |
| `claude -p "query"` | Запустить одноразовый запрос, затем выйти              | `claude -p "explain this function"` |
| `claude -c`         | Продолжить самый последний разговор в текущем каталоге | `claude -c`                         |
| `claude -r`         | Возобновить предыдущий разговор                        | `claude -r`                         |
| `claude commit`     | Создать коммит Git                                     | `claude commit`                     |
| `/clear`            | Очистить историю разговора                             | `/clear`                            |
| `/help`             | Показать доступные команды                             | `/help`                             |
| `exit` или Ctrl+C   | Выйти из Claude Code                                   | `exit`                              |

Смотрите [справочник CLI](/ru/cli-reference) для полного списка команд.

## Советы для начинающих

Для большего, смотрите [лучшие практики](/ru/best-practices) и [типичные рабочие процессы](/ru/common-workflows).

<AccordionGroup>
  <Accordion title="Будьте конкретны в своих запросах">
    Вместо: "fix the bug"

    Попробуйте: "fix the login bug where users see a blank screen after entering wrong credentials"
  </Accordion>

  <Accordion title="Используйте пошаговые инструкции">
    Разбейте сложные задачи на этапы:

    ```text  theme={null}
    1. create a new database table for user profiles
    2. create an API endpoint to get and update user profiles
    3. build a webpage that allows users to see and edit their information
    ```
  </Accordion>

  <Accordion title="Позвольте Claude сначала исследовать">
    Перед внесением изменений позвольте Claude понять ваш код:

    ```text  theme={null}
    analyze the database schema
    ```

    ```text  theme={null}
    build a dashboard showing products that are most frequently returned by our UK customers
    ```
  </Accordion>

  <Accordion title="Сэкономьте время с помощью ярлыков">
    * Нажмите `?` для просмотра всех доступных сочетаний клавиш
    * Используйте Tab для завершения команды
    * Нажмите ↑ для истории команд
    * Введите `/` для просмотра всех команд и skills
  </Accordion>
</AccordionGroup>

## Что дальше?

Теперь, когда вы изучили основы, исследуйте более продвинутые функции:

<CardGroup cols={2}>
  <Card title="Как работает Claude Code" icon="microchip" href="/ru/how-claude-code-works">
    Поймите цикл агента, встроенные инструменты и то, как Claude Code взаимодействует с вашим проектом
  </Card>

  <Card title="Лучшие практики" icon="star" href="/ru/best-practices">
    Получайте лучшие результаты с эффективным запросом и настройкой проекта
  </Card>

  <Card title="Типичные рабочие процессы" icon="graduation-cap" href="/ru/common-workflows">
    Пошаговые руководства для типичных задач
  </Card>

  <Card title="Расширьте Claude Code" icon="puzzle-piece" href="/ru/features-overview">
    Настройте с помощью CLAUDE.md, skills, hooks, MCP и многого другого
  </Card>
</CardGroup>

## Получение помощи

* **В Claude Code**: Введите `/help` или спросите "how do I..."
* **Документация**: Вы здесь! Просмотрите другие руководства
* **Сообщество**: Присоединитесь к нашему [Discord](https://www.anthropic.com/discord) для советов и поддержки
