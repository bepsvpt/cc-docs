> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Расширьте Claude с помощью skills

> Создавайте, управляйте и делитесь skills для расширения возможностей Claude в Claude Code. Включает пользовательские команды и встроенные skills.

Skills расширяют возможности Claude. Создайте файл `SKILL.md` с инструкциями, и Claude добавит его в свой набор инструментов. Claude использует skills при необходимости, или вы можете вызвать один напрямую с помощью `/skill-name`.

<Note>
  Для встроенных команд, таких как `/help` и `/compact`, см. [справочник встроенных команд](/ru/commands).

  **Пользовательские команды были объединены с skills.** Файл в `.claude/commands/deploy.md` и skill в `.claude/skills/deploy/SKILL.md` оба создают `/deploy` и работают одинаково. Ваши существующие файлы `.claude/commands/` продолжают работать. Skills добавляют дополнительные функции: каталог для вспомогательных файлов, frontmatter для [управления тем, кто вызывает skill](#control-who-invokes-a-skill), и возможность для Claude загружать их автоматически при необходимости.
</Note>

Skills в Claude Code следуют открытому стандарту [Agent Skills](https://agentskills.io), который работает с несколькими инструментами AI. Claude Code расширяет стандарт дополнительными функциями, такими как [управление вызовом](#control-who-invokes-a-skill), [выполнение subagent](#run-skills-in-a-subagent) и [динамическое внедрение контекста](#inject-dynamic-context).

## Встроенные skills

Встроенные skills поставляются с Claude Code и доступны в каждой сессии. В отличие от [встроенных команд](/ru/commands), которые выполняют фиксированную логику напрямую, встроенные skills основаны на подсказках: они дают Claude подробный план действий и позволяют ему организовать работу, используя свои инструменты. Это означает, что встроенные skills могут порождать параллельные агенты, читать файлы и адаптироваться к вашей кодовой базе.

Вы вызываете встроенные skills так же, как любой другой skill: введите `/` и затем имя skill. В таблице ниже `<arg>` указывает на обязательный аргумент, а `[arg]` указывает на необязательный.

| Skill                       | Назначение                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| :-------------------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `/batch <instruction>`      | Организуйте крупномасштабные изменения в кодовой базе параллельно. Исследует кодовую базу, разбивает работу на 5-30 независимых единиц и представляет план. После одобрения порождает один фоновый агент на единицу в изолированном [git worktree](/ru/common-workflows#run-parallel-claude-code-sessions-with-git-worktrees). Каждый агент реализует свою единицу, запускает тесты и открывает pull request. Требует git репозиторий. Пример: `/batch migrate src/ from Solid to React` |
| `/claude-api`               | Загрузите справочный материал Claude API для языка вашего проекта (Python, TypeScript, Java, Go, Ruby, C#, PHP или cURL) и справочник Agent SDK для Python и TypeScript. Охватывает использование инструментов, потоковую передачу, пакеты, структурированные выходные данные и распространённые ошибки. Также активируется автоматически, когда ваш код импортирует `anthropic`, `@anthropic-ai/sdk` или `claude_agent_sdk`                                                             |
| `/debug [description]`      | Устраните неполадки в вашей текущей сессии Claude Code, прочитав журнал отладки сессии. Опционально опишите проблему, чтобы сосредоточить анализ                                                                                                                                                                                                                                                                                                                                         |
| `/loop [interval] <prompt>` | Запустите подсказку повторно с интервалом, пока сессия остаётся открытой. Полезно для опроса развёртывания, присмотра за PR или периодического повторного запуска другого skill. Пример: `/loop 5m check if the deploy finished`. См. [Запуск подсказок по расписанию](/ru/scheduled-tasks)                                                                                                                                                                                              |
| `/simplify [focus]`         | Проверьте недавно изменённые файлы на переиспользование кода, качество и проблемы эффективности, затем исправьте их. Порождает трёх агентов проверки параллельно, агрегирует их выводы и применяет исправления. Передайте текст, чтобы сосредоточиться на конкретных проблемах: `/simplify focus on memory efficiency`                                                                                                                                                                   |

## Начало работы

### Создайте свой первый skill

Этот пример создаёт skill, который учит Claude объяснять код, используя визуальные диаграммы и аналогии. Поскольку он использует frontmatter по умолчанию, Claude может загружать его автоматически, когда вы спрашиваете, как что-то работает, или вы можете вызвать его напрямую с помощью `/explain-code`.

<Steps>
  <Step title="Создайте каталог skill">
    Создайте каталог для skill в папке личных skills. Личные skills доступны во всех ваших проектах.

    ```bash  theme={null}
    mkdir -p ~/.claude/skills/explain-code
    ```
  </Step>

  <Step title="Напишите SKILL.md">
    Каждому skill нужен файл `SKILL.md` с двумя частями: YAML frontmatter (между маркерами `---`), который говорит Claude, когда использовать skill, и содержимое markdown с инструкциями, которые Claude следует при вызове skill. Поле `name` становится `/slash-command`, а `description` помогает Claude решить, когда загружать его автоматически.

    Создайте `~/.claude/skills/explain-code/SKILL.md`:

    ```yaml  theme={null}
    ---
    name: explain-code
    description: Explains code with visual diagrams and analogies. Use when explaining how code works, teaching about a codebase, or when the user asks "how does this work?"
    ---

    When explaining code, always include:

    1. **Start with an analogy**: Compare the code to something from everyday life
    2. **Draw a diagram**: Use ASCII art to show the flow, structure, or relationships
    3. **Walk through the code**: Explain step-by-step what happens
    4. **Highlight a gotcha**: What's a common mistake or misconception?

    Keep explanations conversational. For complex concepts, use multiple analogies.
    ```
  </Step>

  <Step title="Протестируйте skill">
    Вы можете протестировать его двумя способами:

    **Позвольте Claude вызвать его автоматически**, задав вопрос, который соответствует описанию:

    ```text  theme={null}
    How does this code work?
    ```

    **Или вызовите его напрямую** с именем skill:

    ```text  theme={null}
    /explain-code src/auth/login.ts
    ```

    В любом случае Claude должен включить аналогию и ASCII диаграмму в своё объяснение.
  </Step>
</Steps>

### Где находятся skills

Место, где вы сохраняете skill, определяет, кто может его использовать:

| Местоположение | Путь                                                     | Применяется к                        |
| :------------- | :------------------------------------------------------- | :----------------------------------- |
| Enterprise     | См. [управляемые параметры](/ru/settings#settings-files) | Все пользователи в вашей организации |
| Personal       | `~/.claude/skills/<skill-name>/SKILL.md`                 | Все ваши проекты                     |
| Project        | `.claude/skills/<skill-name>/SKILL.md`                   | Только этот проект                   |
| Plugin         | `<plugin>/skills/<skill-name>/SKILL.md`                  | Где включен плагин                   |

Когда skills имеют одинаковые имена на разных уровнях, выигрывают места с более высоким приоритетом: enterprise > personal > project. Plugin skills используют пространство имён `plugin-name:skill-name`, поэтому они не могут конфликтовать с другими уровнями. Если у вас есть файлы в `.claude/commands/`, они работают так же, но если skill и команда имеют одинаковое имя, skill имеет приоритет.

#### Автоматическое обнаружение из вложенных каталогов

Когда вы работаете с файлами в подкаталогах, Claude Code автоматически обнаруживает skills из вложенных каталогов `.claude/skills/`. Например, если вы редактируете файл в `packages/frontend/`, Claude Code также ищет skills в `packages/frontend/.claude/skills/`. Это поддерживает настройки monorepo, где пакеты имеют свои собственные skills.

Каждый skill — это каталог с `SKILL.md` в качестве точки входа:

```text  theme={null}
my-skill/
├── SKILL.md           # Main instructions (required)
├── template.md        # Template for Claude to fill in
├── examples/
│   └── sample.md      # Example output showing expected format
└── scripts/
    └── validate.sh    # Script Claude can execute
```

`SKILL.md` содержит основные инструкции и является обязательным. Другие файлы необязательны и позволяют вам создавать более мощные skills: шаблоны для заполнения Claude, примеры выходных данных, показывающие ожидаемый формат, скрипты, которые Claude может выполнять, или подробную справочную документацию. Ссылайтесь на эти файлы из вашего `SKILL.md`, чтобы Claude знал, что они содержат и когда их загружать. См. [Добавьте вспомогательные файлы](#add-supporting-files) для получения дополнительной информации.

<Note>
  Файлы в `.claude/commands/` по-прежнему работают и поддерживают тот же [frontmatter](#frontmatter-reference). Skills рекомендуются, так как они поддерживают дополнительные функции, такие как вспомогательные файлы.
</Note>

#### Skills из дополнительных каталогов

Skills, определённые в `.claude/skills/` в каталогах, добавленных через `--add-dir`, загружаются автоматически и подхватываются обнаружением живых изменений, поэтому вы можете редактировать их во время сессии без перезагрузки.

<Note>
  Файлы CLAUDE.md из каталогов `--add-dir` не загружаются по умолчанию. Чтобы загружать их, установите `CLAUDE_CODE_ADDITIONAL_DIRECTORIES_CLAUDE_MD=1`. См. [Загрузка из дополнительных каталогов](/ru/memory#load-from-additional-directories).
</Note>

## Настройка skills

Skills настраиваются через YAML frontmatter в верхней части `SKILL.md` и содержимое markdown, которое следует.

### Типы содержимого skill

Файлы skill могут содержать любые инструкции, но размышление о том, как вы хотите их вызывать, помогает направить, что включить:

**Справочное содержимое** добавляет знания, которые Claude применяет к вашей текущей работе. Соглашения, паттерны, руководства по стилю, знания предметной области. Это содержимое выполняется встроенно, поэтому Claude может использовать его вместе с контекстом вашего разговора.

```yaml  theme={null}
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

**Содержимое задачи** даёт Claude пошаговые инструкции для конкретного действия, такого как развёртывания, коммиты или генерация кода. Это часто действия, которые вы хотите вызвать напрямую с помощью `/skill-name`, а не позволять Claude решать, когда их запускать. Добавьте `disable-model-invocation: true`, чтобы предотвратить автоматическое срабатывание Claude.

```yaml  theme={null}
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

Ваш `SKILL.md` может содержать что угодно, но размышление о том, как вы хотите вызывать skill (вы, Claude или оба) и где вы хотите его запускать (встроенно или в subagent), помогает направить, что включить. Для сложных skills вы также можете [добавить вспомогательные файлы](#add-supporting-files), чтобы сохранить основной skill сосредоточенным.

### Справочник frontmatter

Помимо содержимого markdown, вы можете настроить поведение skill, используя поля YAML frontmatter между маркерами `---` в верхней части вашего файла `SKILL.md`:

```yaml  theme={null}
---
name: my-skill
description: What this skill does
disable-model-invocation: true
allowed-tools: Read, Grep
---

Your skill instructions here...
```

Все поля необязательны. Только `description` рекомендуется, чтобы Claude знал, когда использовать skill.

| Поле                       | Обязательно   | Описание                                                                                                                                                                                               |
| :------------------------- | :------------ | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`                     | Нет           | Отображаемое имя для skill. Если опущено, использует имя каталога. Только строчные буквы, цифры и дефисы (максимум 64 символа).                                                                        |
| `description`              | Рекомендуется | Что делает skill и когда его использовать. Claude использует это, чтобы решить, когда применять skill. Если опущено, использует первый абзац содержимого markdown.                                     |
| `argument-hint`            | Нет           | Подсказка, показываемая при автодополнении, чтобы указать ожидаемые аргументы. Пример: `[issue-number]` или `[filename] [format]`.                                                                     |
| `disable-model-invocation` | Нет           | Установите на `true`, чтобы предотвратить автоматическую загрузку этого skill Claude. Используйте для рабочих процессов, которые вы хотите запустить вручную с помощью `/name`. По умолчанию: `false`. |
| `user-invocable`           | Нет           | Установите на `false`, чтобы скрыть из меню `/`. Используйте для фоновых знаний, которые пользователи не должны вызывать напрямую. По умолчанию: `true`.                                               |
| `allowed-tools`            | Нет           | Инструменты, которые Claude может использовать без запроса разрешения, когда этот skill активен.                                                                                                       |
| `model`                    | Нет           | Модель для использования, когда этот skill активен.                                                                                                                                                    |
| `context`                  | Нет           | Установите на `fork`, чтобы запустить в контексте forked subagent.                                                                                                                                     |
| `agent`                    | Нет           | Какой тип subagent использовать, когда установлен `context: fork`.                                                                                                                                     |
| `hooks`                    | Нет           | Hooks, ограниченные жизненным циклом этого skill. См. [Hooks в skills и agents](/ru/hooks#hooks-in-skills-and-agents) для формата конфигурации.                                                        |

#### Доступные подстановки строк

Skills поддерживают подстановку строк для динамических значений в содержимом skill:

| Переменная             | Описание                                                                                                                                                                                                                                                     |
| :--------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$ARGUMENTS`           | Все аргументы, переданные при вызове skill. Если `$ARGUMENTS` отсутствует в содержимом, аргументы добавляются как `ARGUMENTS: <value>`.                                                                                                                      |
| `$ARGUMENTS[N]`        | Доступ к конкретному аргументу по индексу на основе 0, например `$ARGUMENTS[0]` для первого аргумента.                                                                                                                                                       |
| `$N`                   | Сокращение для `$ARGUMENTS[N]`, например `$0` для первого аргумента или `$1` для второго.                                                                                                                                                                    |
| `${CLAUDE_SESSION_ID}` | Текущий ID сессии. Полезно для логирования, создания файлов, специфичных для сессии, или корреляции выходных данных skill с сессиями.                                                                                                                        |
| `${CLAUDE_SKILL_DIR}`  | Каталог, содержащий файл `SKILL.md` skill. Для plugin skills это подкаталог skill в плагине, а не корень плагина. Используйте это в командах bash injection для ссылки на скрипты или файлы, поставляемые с skill, независимо от текущего рабочего каталога. |

**Пример использования подстановок:**

```yaml  theme={null}
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

### Добавьте вспомогательные файлы

Skills могут включать несколько файлов в их каталоге. Это сохраняет `SKILL.md` сосредоточенным на основном, позволяя Claude получать доступ к подробному справочному материалу только при необходимости. Большие справочные документы, спецификации API или коллекции примеров не нужно загружать в контекст каждый раз, когда запускается skill.

```text  theme={null}
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

Ссылайтесь на вспомогательные файлы из `SKILL.md`, чтобы Claude знал, что содержит каждый файл и когда его загружать:

```markdown  theme={null}
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

<Tip>Сохраняйте `SKILL.md` под 500 строк. Переместите подробный справочный материал в отдельные файлы.</Tip>

### Управляйте тем, кто вызывает skill

По умолчанию как вы, так и Claude можете вызывать любой skill. Вы можете ввести `/skill-name`, чтобы вызвать его напрямую, и Claude может загружать его автоматически при необходимости для вашего разговора. Два поля frontmatter позволяют вам ограничить это:

* **`disable-model-invocation: true`**: Только вы можете вызвать skill. Используйте это для рабочих процессов с побочными эффектами или которые вы хотите контролировать по времени, такие как `/commit`, `/deploy` или `/send-slack-message`. Вы не хотите, чтобы Claude решил развернуть, потому что ваш код выглядит готовым.

* **`user-invocable: false`**: Только Claude может вызвать skill. Используйте это для фоновых знаний, которые не являются действенными как команда. Skill `legacy-system-context` объясняет, как работает старая система. Claude должен знать это при необходимости, но `/legacy-system-context` не является значимым действием для пользователей.

Этот пример создаёт skill развёртывания, который может запустить только вы. Поле `disable-model-invocation: true` предотвращает автоматическое запуск Claude:

```yaml  theme={null}
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

Вот как два поля влияют на вызов и загрузку контекста:

| Frontmatter                      | Вы можете вызвать | Claude может вызвать | Когда загружается в контекст                                       |
| :------------------------------- | :---------------- | :------------------- | :----------------------------------------------------------------- |
| (по умолчанию)                   | Да                | Да                   | Описание всегда в контексте, полный skill загружается при вызове   |
| `disable-model-invocation: true` | Да                | Нет                  | Описание не в контексте, полный skill загружается при вашем вызове |
| `user-invocable: false`          | Нет               | Да                   | Описание всегда в контексте, полный skill загружается при вызове   |

<Note>
  В обычной сессии описания skills загружаются в контекст, чтобы Claude знал, что доступно, но полное содержимое skill загружается только при вызове. [Subagents с предварительно загруженными skills](/ru/sub-agents#preload-skills-into-subagents) работают иначе: полное содержимое skill внедряется при запуске.
</Note>

### Ограничьте доступ к инструментам

Используйте поле `allowed-tools`, чтобы ограничить, какие инструменты Claude может использовать, когда skill активен. Этот skill создаёт режим только для чтения, где Claude может исследовать файлы, но не может их изменять:

```yaml  theme={null}
---
name: safe-reader
description: Read files without making changes
allowed-tools: Read, Grep, Glob
---
```

### Передайте аргументы в skills

Как вы, так и Claude можете передавать аргументы при вызове skill. Аргументы доступны через заполнитель `$ARGUMENTS`.

Этот skill исправляет проблему GitHub по номеру. Заполнитель `$ARGUMENTS` заменяется на всё, что следует за именем skill:

```yaml  theme={null}
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

Когда вы запускаете `/fix-issue 123`, Claude получает "Fix GitHub issue 123 following our coding standards..."

Если вы вызываете skill с аргументами, но skill не включает `$ARGUMENTS`, Claude Code добавляет `ARGUMENTS: <your input>` в конец содержимого skill, чтобы Claude всё ещё видел, что вы ввели.

Для доступа к отдельным аргументам по позиции используйте `$ARGUMENTS[N]` или более короткий `$N`:

```yaml  theme={null}
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $ARGUMENTS[0] component from $ARGUMENTS[1] to $ARGUMENTS[2].
Preserve all existing behavior and tests.
```

Запуск `/migrate-component SearchBar React Vue` заменяет `$ARGUMENTS[0]` на `SearchBar`, `$ARGUMENTS[1]` на `React` и `$ARGUMENTS[2]` на `Vue`. Тот же skill, используя сокращение `$N`:

```yaml  theme={null}
---
name: migrate-component
description: Migrate a component from one framework to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

## Продвинутые паттерны

### Внедрите динамический контекст

Синтаксис `!`command\`\` запускает команды оболочки перед отправкой содержимого skill Claude. Выходные данные команды заменяют заполнитель, поэтому Claude получает фактические данные, а не саму команду.

Этот skill суммирует pull request, получая живые данные PR с помощью GitHub CLI. Команды `!`gh pr diff\`\` и другие запускаются первыми, и их выходные данные вставляются в подсказку:

```yaml  theme={null}
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

Когда этот skill запускается:

1. Каждый `!`command\`\` выполняется немедленно (перед тем, как Claude что-либо увидит)
2. Выходные данные заменяют заполнитель в содержимом skill
3. Claude получает полностью отрендеренную подсказку с фактическими данными PR

Это предварительная обработка, а не то, что Claude выполняет. Claude видит только окончательный результат.

<Tip>
  Чтобы включить [расширенное мышление](/ru/common-workflows#use-extended-thinking-thinking-mode) в skill, включите слово "ultrathink" где-нибудь в содержимое skill.
</Tip>

### Запустите skills в subagent

Добавьте `context: fork` в ваш frontmatter, когда вы хотите, чтобы skill запускался в изоляции. Содержимое skill становится подсказкой, которая управляет subagent. Он не будет иметь доступ к истории вашего разговора.

<Warning>
  `context: fork` имеет смысл только для skills с явными инструкциями. Если ваш skill содержит рекомендации, такие как "используйте эти соглашения API" без задачи, subagent получает рекомендации, но не действенную подсказку, и возвращается без значимого выходного сигнала.
</Warning>

Skills и [subagents](/ru/sub-agents) работают вместе в двух направлениях:

| Подход                    | Системная подсказка                       | Задача                         | Также загружает                               |
| :------------------------ | :---------------------------------------- | :----------------------------- | :-------------------------------------------- |
| Skill с `context: fork`   | От типа агента (`Explore`, `Plan` и т.д.) | Содержимое SKILL.md            | CLAUDE.md                                     |
| Subagent с полем `skills` | Тело markdown subagent                    | Сообщение делегирования Claude | Предварительно загруженные skills + CLAUDE.md |

С `context: fork` вы пишете задачу в своём skill и выбираете тип агента для её выполнения. Для обратного (определение пользовательского subagent, который использует skills как справочный материал), см. [Subagents](/ru/sub-agents#preload-skills-into-subagents).

#### Пример: Research skill, используя Explore agent

Этот skill запускает исследование в forked Explore agent. Содержимое skill становится задачей, и агент предоставляет инструменты только для чтения, оптимизированные для исследования кодовой базы:

```yaml  theme={null}
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

Когда этот skill запускается:

1. Создаётся новый изолированный контекст
2. Subagent получает содержимое skill в качестве своей подсказки ("Research \$ARGUMENTS thoroughly...")
3. Поле `agent` определяет среду выполнения (модель, инструменты и разрешения)
4. Результаты суммируются и возвращаются в ваш основной разговор

Поле `agent` указывает, какую конфигурацию subagent использовать. Опции включают встроенные агенты (`Explore`, `Plan`, `general-purpose`) или любой пользовательский subagent из `.claude/agents/`. Если опущено, использует `general-purpose`.

### Ограничьте доступ Claude к skills

По умолчанию Claude может вызывать любой skill, у которого не установлен `disable-model-invocation: true`. Skills, которые определяют `allowed-tools`, предоставляют Claude доступ к этим инструментам без одобрения за использование, когда skill активен. Ваши [параметры разрешений](/ru/permissions) по-прежнему управляют поведением одобрения базовой линии для всех остальных инструментов. Встроенные команды, такие как `/compact` и `/init`, недоступны через инструмент Skill.

Три способа управления, какие skills может вызывать Claude:

**Отключите все skills**, отказав в инструменте Skill в `/permissions`:

```text  theme={null}
# Add to deny rules:
Skill
```

**Разрешите или запретите конкретные skills**, используя [правила разрешений](/ru/permissions):

```text  theme={null}
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

Синтаксис разрешений: `Skill(name)` для точного совпадения, `Skill(name *)` для совпадения префикса с любыми аргументами.

**Скройте отдельные skills**, добавив `disable-model-invocation: true` в их frontmatter. Это полностью удаляет skill из контекста Claude.

<Note>
  Поле `user-invocable` управляет только видимостью меню, а не доступом инструмента Skill. Используйте `disable-model-invocation: true`, чтобы заблокировать программный вызов.
</Note>

## Делитесь skills

Skills могут распространяться на разных уровнях в зависимости от вашей аудитории:

* **Project skills**: Зафиксируйте `.claude/skills/` в контроле версий
* **Plugins**: Создайте каталог `skills/` в вашем [плагине](/ru/plugins)
* **Managed**: Развёртывайте организацию-широко через [управляемые параметры](/ru/settings#settings-files)

### Генерируйте визуальный выходной сигнал

Skills могут объединять и запускать скрипты на любом языке, давая Claude возможности, выходящие за рамки того, что возможно в одной подсказке. Один мощный паттерн — генерирование визуального выходного сигнала: интерактивные HTML файлы, которые открываются в вашем браузере для исследования данных, отладки или создания отчётов.

Этот пример создаёт обозреватель кодовой базы: интерактивное древовидное представление, где вы можете развёртывать и свёртывать каталоги, видеть размеры файлов с первого взгляда и определять типы файлов по цвету.

Создайте каталог Skill:

```bash  theme={null}
mkdir -p ~/.claude/skills/codebase-visualizer/scripts
```

Создайте `~/.claude/skills/codebase-visualizer/SKILL.md`. Описание говорит Claude, когда активировать этот Skill, а инструкции говорят Claude запустить поставляемый скрипт:

````yaml  theme={null}
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase. Use when exploring a new repo, understanding project structure, or identifying large files.
allowed-tools: Bash(python *)
---

# Codebase Visualizer

Generate an interactive HTML tree view that shows your project's file structure with collapsible directories.

## Usage

Run the visualization script from your project root:

```bash
python ~/.claude/skills/codebase-visualizer/scripts/visualize.py .
```

This creates `codebase-map.html` in the current directory and opens it in your default browser.

## What the visualization shows

- **Collapsible directories**: Click folders to expand/collapse
- **File sizes**: Displayed next to each file
- **Colors**: Different colors for different file types
- **Directory totals**: Shows aggregate size of each folder
````

Создайте `~/.claude/skills/codebase-visualizer/scripts/visualize.py`. Этот скрипт сканирует дерево каталогов и генерирует самодостаточный HTML файл с:

* **Боковой панелью сводки**, показывающей количество файлов, количество каталогов, общий размер и количество типов файлов
* **Столбчатой диаграммой**, разбивающей кодовую базу по типу файла (топ 8 по размеру)
* **Свёртываемым деревом**, где вы можете развёртывать и свёртывать каталоги, с цветовыми индикаторами типов файлов

Скрипт требует Python, но использует только встроенные библиотеки, поэтому нет пакетов для установки:

```python expandable theme={null}
#!/usr/bin/env python3
"""Generate an interactive collapsible tree visualization of a codebase."""

import json
import sys
import webbrowser
from pathlib import Path
from collections import Counter

IGNORE = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}

def scan(path: Path, stats: dict) -> dict:
    result = {"name": path.name, "children": [], "size": 0}
    try:
        for item in sorted(path.iterdir()):
            if item.name in IGNORE or item.name.startswith('.'):
                continue
            if item.is_file():
                size = item.stat().st_size
                ext = item.suffix.lower() or '(no ext)'
                result["children"].append({"name": item.name, "size": size, "ext": ext})
                result["size"] += size
                stats["files"] += 1
                stats["extensions"][ext] += 1
                stats["ext_sizes"][ext] += size
            elif item.is_dir():
                stats["dirs"] += 1
                child = scan(item, stats)
                if child["children"]:
                    result["children"].append(child)
                    result["size"] += child["size"]
    except PermissionError:
        pass
    return result

def generate_html(data: dict, stats: dict, output: Path) -> None:
    ext_sizes = stats["ext_sizes"]
    total_size = sum(ext_sizes.values()) or 1
    sorted_exts = sorted(ext_sizes.items(), key=lambda x: -x[1])[:8]
    colors = {
        '.js': '#f7df1e', '.ts': '#3178c6', '.py': '#3776ab', '.go': '#00add8',
        '.rs': '#dea584', '.rb': '#cc342d', '.css': '#264de4', '.html': '#e34c26',
        '.json': '#6b7280', '.md': '#083fa1', '.yaml': '#cb171e', '.yml': '#cb171e',
        '.mdx': '#083fa1', '.tsx': '#3178c6', '.jsx': '#61dafb', '.sh': '#4eaa25',
    }
    lang_bars = "".join(
        f'<div class="bar-row"><span class="bar-label">{ext}</span>'
        f'<div class="bar" style="width:{(size/total_size)*100}%;background:{colors.get(ext,"#6b7280")}"></div>'
        f'<span class="bar-pct">{(size/total_size)*100:.1f}%</span></div>'
        for ext, size in sorted_exts
    )
    def fmt(b):
        if b < 1024: return f"{b} B"
        if b < 1048576: return f"{b/1024:.1f} KB"
        return f"{b/1048576:.1f} MB"

    html = f'''<!DOCTYPE html>
<html><head>
  <meta charset="utf-8"><title>Codebase Explorer</title>
  <style>
    body {{ font: 14px/1.5 system-ui, sans-serif; margin: 0; background: #1a1a2e; color: #eee; }}
    .container {{ display: flex; height: 100vh; }}
    .sidebar {{ width: 280px; background: #252542; padding: 20px; border-right: 1px solid #3d3d5c; overflow-y: auto; flex-shrink: 0; }}
    .main {{ flex: 1; padding: 20px; overflow-y: auto; }}
    h1 {{ margin: 0 0 10px 0; font-size: 18px; }}
    h2 {{ margin: 20px 0 10px 0; font-size: 14px; color: #888; text-transform: uppercase; }}
    .stat {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #3d3d5c; }}
    .stat-value {{ font-weight: bold; }}
    .bar-row {{ display: flex; align-items: center; margin: 6px 0; }}
    .bar-label {{ width: 55px; font-size: 12px; color: #aaa; }}
    .bar {{ height: 18px; border-radius: 3px; }}
    .bar-pct {{ margin-left: 8px; font-size: 12px; color: #666; }}
    .tree {{ list-style: none; padding-left: 20px; }}
    details {{ cursor: pointer; }}
    summary {{ padding: 4px 8px; border-radius: 4px; }}
    summary:hover {{ background: #2d2d44; }}
    .folder {{ color: #ffd700; }}
    .file {{ display: flex; align-items: center; padding: 4px 8px; border-radius: 4px; }}
    .file:hover {{ background: #2d2d44; }}
    .size {{ color: #888; margin-left: auto; font-size: 12px; }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }}
  </style>
</head><body>
  <div class="container">
    <div class="sidebar">
      <h1>📊 Summary</h1>
      <div class="stat"><span>Files</span><span class="stat-value">{stats["files"]:,}</span></div>
      <div class="stat"><span>Directories</span><span class="stat-value">{stats["dirs"]:,}</span></div>
      <div class="stat"><span>Total size</span><span class="stat-value">{fmt(data["size"])}</span></div>
      <div class="stat"><span>File types</span><span class="stat-value">{len(stats["extensions"])}</span></div>
      <h2>By file type</h2>
      {lang_bars}
    </div>
    <div class="main">
      <h1>📁 {data["name"]}</h1>
      <ul class="tree" id="root"></ul>
    </div>
  </div>
  <script>
    const data = {json.dumps(data)};
    const colors = {json.dumps(colors)};
    function fmt(b) {{ if (b < 1024) return b + ' B'; if (b < 1048576) return (b/1024).toFixed(1) + ' KB'; return (b/1048576).toFixed(1) + ' MB'; }}
    function render(node, parent) {{
      if (node.children) {{
        const det = document.createElement('details');
        det.open = parent === document.getElementById('root');
        det.innerHTML = `<summary><span class="folder">📁 ${{node.name}}</span><span class="size">${{fmt(node.size)}}</span></summary>`;
        const ul = document.createElement('ul'); ul.className = 'tree';
        node.children.sort((a,b) => (b.children?1:0)-(a.children?1:0) || a.name.localeCompare(b.name));
        node.children.forEach(c => render(c, ul));
        det.appendChild(ul);
        const li = document.createElement('li'); li.appendChild(det); parent.appendChild(li);
      }} else {{
        const li = document.createElement('li'); li.className = 'file';
        li.innerHTML = `<span class="dot" style="background:${{colors[node.ext]||'#6b7280'}}"></span>${{node.name}}<span class="size">${{fmt(node.size)}}</span>`;
        parent.appendChild(li);
      }}
    }}
    data.children.forEach(c => render(c, document.getElementById('root')));
  </script>
</body></html>'''
    output.write_text(html)

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    stats = {"files": 0, "dirs": 0, "extensions": Counter(), "ext_sizes": Counter()}
    data = scan(target, stats)
    out = Path('codebase-map.html')
    generate_html(data, stats, out)
    print(f'Generated {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')
```

Чтобы протестировать, откройте Claude Code в любом проекте и попросите "Visualize this codebase." Claude запускает скрипт, генерирует `codebase-map.html` и открывает его в вашем браузере.

Этот паттерн работает для любого визуального выходного сигнала: графики зависимостей, отчёты о покрытии тестами, документация API или визуализации схемы базы данных. Поставляемый скрипт выполняет тяжёлую работу, пока Claude обрабатывает оркестрацию.

## Устранение неполадок

### Skill не срабатывает

Если Claude не использует ваш skill при необходимости:

1. Проверьте, что описание включает ключевые слова, которые пользователи естественно скажут
2. Убедитесь, что skill появляется в `What skills are available?`
3. Попробуйте переформулировать ваш запрос, чтобы лучше соответствовать описанию
4. Вызовите его напрямую с помощью `/skill-name`, если skill может быть вызван пользователем

### Skill срабатывает слишком часто

Если Claude использует ваш skill, когда вы этого не хотите:

1. Сделайте описание более конкретным
2. Добавьте `disable-model-invocation: true`, если вы хотите только ручной вызов

### Claude не видит все мои skills

Описания skills загружаются в контекст, чтобы Claude знал, что доступно. Если у вас много skills, они могут превысить бюджет символов. Бюджет масштабируется динамически на 2% контекстного окна, с резервным значением 16 000 символов. Запустите `/context`, чтобы проверить предупреждение об исключённых skills.

Чтобы переопределить лимит, установите переменную окружения `SLASH_COMMAND_TOOL_CHAR_BUDGET`.

## Связанные ресурсы

* **[Subagents](/ru/sub-agents)**: делегируйте задачи специализированным агентам
* **[Plugins](/ru/plugins)**: упакуйте и распространяйте skills с другими расширениями
* **[Hooks](/ru/hooks)**: автоматизируйте рабочие процессы вокруг событий инструментов
* **[Memory](/ru/memory)**: управляйте файлами CLAUDE.md для постоянного контекста
* **[Built-in commands](/ru/commands)**: справочник для встроенных команд `/`
* **[Permissions](/ru/permissions)**: управляйте доступом к инструментам и skills
