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

# Оптимизируйте настройку вашего терминала

> Claude Code работает лучше всего, когда ваш терминал правильно настроен. Следуйте этим рекомендациям, чтобы оптимизировать ваш опыт.

### Темы и внешний вид

Claude не может управлять темой вашего терминала. Это обрабатывается вашим приложением терминала. Вы можете в любое время сопоставить тему Claude Code с вашим терминалом через команду `/config`.

Для дополнительной настройки самого интерфейса Claude Code вы можете настроить [пользовательскую строку состояния](/ru/statusline) для отображения контекстной информации, такой как текущая модель, рабочий каталог или ветка git в нижней части вашего терминала.

### Разрывы строк

У вас есть несколько вариантов для ввода разрывов строк в Claude Code:

* **Быстрый выход**: Введите `\` с последующим Enter для создания новой строки
* **Shift+Enter**: Работает из коробки в iTerm2, WezTerm, Ghostty и Kitty
* **Сочетание клавиш**: Установите сочетание клавиш для вставки новой строки в других терминалах

**Установка Shift+Enter для других терминалов**

Запустите `/terminal-setup` в Claude Code, чтобы автоматически настроить Shift+Enter для VS Code, Alacritty, Zed и Warp.

<Note>
  Команда `/terminal-setup` видна только в терминалах, требующих ручной настройки. Если вы используете iTerm2, WezTerm, Ghostty или Kitty, вы не увидите эту команду, потому что Shift+Enter уже работает изначально.
</Note>

**Установка Option+Enter (VS Code, iTerm2 или macOS Terminal.app)**

**Для Mac Terminal.app:**

1. Откройте Settings → Profiles → Keyboard
2. Установите флажок "Use Option as Meta Key"

**Для iTerm2:**

1. Откройте Settings → Profiles → Keys
2. В разделе General установите Left/Right Option key на "Esc+"

**Для терминала VS Code:**

Установите `"terminal.integrated.macOptionIsMeta": true` в настройках VS Code.

### Настройка уведомлений

Когда Claude завершает работу и ожидает вашего ввода, он отправляет событие уведомления. Вы можете отобразить это событие как уведомление рабочего стола через ваш терминал или запустить пользовательскую логику с помощью [хуков уведомлений](/ru/hooks#notification).

#### Уведомления терминала

Kitty и Ghostty поддерживают уведомления рабочего стола без дополнительной настройки. iTerm 2 требует настройки:

1. Откройте iTerm 2 Settings → Profiles → Terminal
2. Включите "Notification Center Alerts"
3. Нажмите "Filter Alerts" и установите флажок "Send escape sequence-generated alerts"

Если уведомления не появляются, убедитесь, что ваше приложение терминала имеет разрешения на уведомления в настройках вашей ОС.

Когда Claude Code работает внутри tmux, уведомления и [полоса прогресса терминала](/ru/settings#global-config-settings) достигают внешнего терминала, такого как iTerm2, Kitty или Ghostty, только если вы включите passthrough в конфигурации tmux:

```
set -g allow-passthrough on
```

Без этого параметра tmux перехватывает escape-последовательности и они не достигают приложения терминала.

Другие терминалы, включая стандартный macOS Terminal, не поддерживают встроенные уведомления. Вместо этого используйте [хуки уведомлений](/ru/hooks#notification).

#### Хуки уведомлений

Чтобы добавить пользовательское поведение при срабатывании уведомлений, например воспроизведение звука или отправку сообщения, настройте [хук уведомления](/ru/hooks#notification). Хуки работают вместе с уведомлениями терминала, а не как замена.

### Уменьшение мерцания и использования памяти

Если вы видите мерцание во время длительных сеансов или позиция прокрутки вашего терминала прыгает в верхнюю часть, пока Claude работает, попробуйте [полноэкранный рендеринг](/ru/fullscreen). Он использует альтернативный путь рендеринга, который сохраняет память на плоском уровне и добавляет поддержку мыши. Включите его с помощью `CLAUDE_CODE_NO_FLICKER=1`.

### Обработка больших входных данных

При работе с обширным кодом или длинными инструкциями:

* **Избегайте прямой вставки**: Claude Code может испытывать трудности с очень длинным вставленным содержимым
* **Используйте рабочие процессы на основе файлов**: Запишите содержимое в файл и попросите Claude прочитать его
* **Будьте осведомлены об ограничениях VS Code**: Терминал VS Code особенно подвержен усечению длинных вставок

### Режим Vim

Claude Code поддерживает подмножество сочетаний клавиш Vim, которые можно включить с помощью `/vim` или настроить через `/config`. Чтобы установить режим непосредственно в файл конфигурации, установите глобальный ключ конфигурации [`editorMode`](/ru/settings#global-config-settings) на `"vim"` в `~/.claude.json`.

Поддерживаемое подмножество включает:

* Переключение режимов: `Esc` (в NORMAL), `i`/`I`, `a`/`A`, `o`/`O` (в INSERT)
* Навигация: `h`/`j`/`k`/`l`, `w`/`e`/`b`, `0`/`$`/`^`, `gg`/`G`, `f`/`F`/`t`/`T` с повтором `;`/`,`
* Редактирование: `x`, `dw`/`de`/`db`/`dd`/`D`, `cw`/`ce`/`cb`/`cc`/`C`, `.` (повтор)
* Копирование/вставка: `yy`/`Y`, `yw`/`ye`/`yb`, `p`/`P`
* Текстовые объекты: `iw`/`aw`, `iW`/`aW`, `i"`/`a"`, `i'`/`a'`, `i(`/`a(`, `i[`/`a[`, `i{`/`a{`
* Отступы: `>>`/`<<`
* Операции со строками: `J` (объединение строк)

Смотрите [Интерактивный режим](/ru/interactive-mode#vim-editor-mode) для полного справочника.
