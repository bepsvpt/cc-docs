> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Настройте ваш терминал для Claude Code

> Исправьте Shift+Enter для разрывов строк, получайте звуковой сигнал терминала когда Claude завершает работу, настройте tmux, сопоставьте цветовую тему и включите режим Vim в CLI Claude Code.

Claude Code работает в любом терминале без конфигурации. Эта страница предназначена для случаев, когда что-то конкретное ведёт себя не так, как вы ожидаете. Найдите ваш симптом ниже. Если всё уже работает правильно, вам не нужна эта страница.

* [Shift+Enter отправляет вместо вставки разрыва строки](#enter-multiline-prompts)
* [Сочетания клавиш с клавишей Option ничего не делают на macOS](#enable-option-key-shortcuts-on-macos)
* [Нет звука или оповещения когда Claude завершает работу](#get-a-terminal-bell-or-notification)
* [Вы запускаете Claude Code внутри tmux](#configure-tmux)
* [Дисплей мерцает или позиция прокрутки прыгает](#switch-to-fullscreen-rendering)
* [Вы хотите клавиши Vim в приглашении](#edit-prompts-with-vim-keybindings)

Эта страница посвящена тому, чтобы ваш терминал отправлял правильные сигналы в Claude Code. Чтобы изменить, на какие клавиши сам Claude Code реагирует, см. вместо этого [сочетания клавиш](/ru/keybindings).

## Ввод многострочных приглашений

Нажатие Enter отправляет ваше сообщение. Чтобы добавить разрыв строки без отправки, нажмите Ctrl+J или введите `\` и затем нажмите Enter. Оба варианта работают в каждом терминале без настройки.

В большинстве терминалов вы также можете нажать Shift+Enter, но поддержка варьируется в зависимости от эмулятора терминала:

| Терминал                                                                            | Shift+Enter для разрыва строки                     |
| :---------------------------------------------------------------------------------- | :------------------------------------------------- |
| Ghostty, Kitty, iTerm2, WezTerm, Warp, Apple Terminal                               | Работает без настройки                             |
| VS Code, Cursor, Windsurf, Alacritty, Zed                                           | Запустите `/terminal-setup` один раз               |
| Windows Terminal, gnome-terminal, JetBrains IDEs такие как PyCharm и Android Studio | Недоступно; используйте Ctrl+J или `\` затем Enter |

Для VS Code, Cursor, Windsurf, Alacritty и Zed, `/terminal-setup` записывает Shift+Enter и другие сочетания клавиш в файл конфигурации терминала. В VS Code, Cursor и Windsurf он также устанавливает `terminal.integrated.mouseWheelScrollSensitivity` в параметрах редактора для более плавной прокрутки в [полноэкранном режиме](/ru/fullscreen). Существующие привязки и параметры остаются на месте; если вы видите сообщение, такое как `VSCode terminal Shift+Enter key binding already configured`, никаких изменений не было сделано. Запустите `/terminal-setup` непосредственно в хост-терминале, а не внутри tmux или screen, так как ему нужно записать в конфигурацию хост-терминала.

Если вы работаете внутри tmux, Shift+Enter также требует [конфигурацию tmux ниже](#configure-tmux) даже когда внешний терминал её поддерживает.

Чтобы привязать разрыв строки к другой клавише или поменять поведение так, чтобы Enter вставлял разрыв строки, а Shift+Enter отправлял, сопоставьте действия `chat:newline` и `chat:submit` в вашем [файле сочетаний клавиш](/ru/keybindings).

## Включите сочетания клавиш Option на macOS

Некоторые сочетания клавиш Claude Code используют клавишу Option, такие как Option+Enter для разрыва строки или Option+P для переключения моделей. На macOS большинство терминалов не отправляют Option как модификатор по умолчанию, поэтому эти сочетания клавиш ничего не делают, пока вы это не включите. Параметр терминала для этого обычно называется "Use Option as Meta Key"; Meta — это историческое имя Unix для клавиши, которая теперь называется Option или Alt.

<Tabs>
  <Tab title="Apple Terminal">
    Откройте Settings → Profiles → Keyboard и установите флажок "Use Option as Meta Key".

    Если вы приняли первое приглашение Claude Code, которое предлагало "Option+Enter для разрывов строк и визуального звонка", это уже сделано. Это приглашение запускает `/terminal-setup` для вас, что включает Option как Meta и переключает звуковой звонок на визуальную вспышку экрана в вашем профиле Apple Terminal.
  </Tab>

  <Tab title="iTerm2">
    Откройте Settings → Profiles → Keys → General и установите Left Option key и Right Option key на "Esc+".
  </Tab>

  <Tab title="VS Code">
    Добавьте `"terminal.integrated.macOptionIsMeta": true` в ваши настройки VS Code.
  </Tab>
</Tabs>

Для Ghostty, Kitty и других терминалов ищите параметр Option-as-Alt или Option-as-Meta в файле конфигурации терминала.

## Получите звуковой сигнал терминала или уведомление

Когда Claude завершает задачу или делает паузу для приглашения разрешения, он отправляет событие уведомления. Отображение этого как звукового сигнала терминала или уведомления рабочего стола позволяет вам переключиться на другую работу, пока выполняется длительная задача.

Claude Code отправляет уведомление рабочего стола только в Ghostty, Kitty и iTerm2; каждый другой терминал требует [хук Notification](#play-a-sound-with-a-notification-hook) вместо этого. Уведомление также достигает вашей локальной машины через SSH, поэтому удалённый сеанс всё ещё может вас оповестить. Ghostty и Kitty перенаправляют его в центр уведомлений вашей ОС без дополнительной настройки. iTerm2 требует, чтобы вы включили перенаправление:

<Steps>
  <Step title="Откройте параметры уведомлений iTerm2">
    Перейдите в Settings → Profiles → Terminal.
  </Step>

  <Step title="Включите оповещения">
    Установите флажок "Notification Center Alerts", затем нажмите "Filter Alerts" и включите "Send escape sequence-generated alerts".
  </Step>
</Steps>

Если уведомления всё ещё не появляются, убедитесь, что ваше приложение терминала имеет разрешение на уведомления в настройках вашей ОС, и если вы работаете внутри tmux, [включите passthrough](#configure-tmux).

### Воспроизведите звук с помощью хука Notification

В любом терминале вы можете настроить [хук Notification](/ru/hooks-guide#get-notified-when-claude-needs-input) для воспроизведения звука или запуска пользовательской команды, когда Claude нуждается в вашем внимании. Хуки работают вместе с уведомлением рабочего стола, а не заменяя его. Терминалы, такие как Warp или Apple Terminal, полагаются только на хук, так как Claude Code не отправляет им уведомление рабочего стола.

Пример ниже воспроизводит системный звук на macOS. Связанное руководство содержит команды уведомлений рабочего стола для macOS, Linux и Windows.

```json ~/.claude/settings.json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "hooks": [{ "type": "command", "command": "afplay /System/Library/Sounds/Glass.aiff" }]
      }
    ]
  }
}
```

## Настройте tmux

Когда Claude Code работает внутри tmux, две вещи ломаются по умолчанию: Shift+Enter отправляет вместо вставки разрыва строки, и уведомления рабочего стола и [полоса прогресса](/ru/settings#available-settings) никогда не достигают внешнего терминала. Добавьте эти строки в `~/.tmux.conf`, затем запустите `tmux source-file ~/.tmux.conf` чтобы применить их к работающему серверу:

```bash ~/.tmux.conf theme={null}
set -g allow-passthrough on
set -s extended-keys on
set -as terminal-features 'xterm*:extkeys'
```

Строка `allow-passthrough` позволяет уведомлениям и обновлениям прогресса достичь iTerm2, Ghostty или Kitty вместо того, чтобы быть поглощёнными tmux. Строки `extended-keys` позволяют tmux различать Shift+Enter от простого Enter, чтобы сочетание клавиш разрыва строки работало.

## Сопоставьте цветовую тему

Используйте команду `/theme` или средство выбора темы в `/config` для выбора темы Claude Code, которая соответствует вашему терминалу. Выбор опции auto обнаруживает светлый или тёмный фон вашего терминала, поэтому тема следует изменениям внешнего вида ОС всякий раз, когда это делает ваш терминал. Claude Code не управляет цветовой схемой самого терминала, которая устанавливается приложением терминала.

Чтобы настроить то, что отображается в нижней части интерфейса, настройте [пользовательскую строку состояния](/ru/statusline), которая показывает текущую модель, рабочий каталог, ветку git или другой контекст.

### Создайте пользовательскую тему

<Note>
  Custom themes require Claude Code v2.1.118 or later.
</Note>

В дополнение к встроенным предустановкам, `/theme` отображает любые пользовательские темы, которые вы определили, и любые темы, предоставленные установленными [plugins](/ru/plugins-reference#themes). Выберите **New custom theme…** в конце списка, чтобы создать её интерактивно: вы назовёте тему, а затем выберете отдельные цветовые токены для переопределения. Нажмите `Ctrl+E`, пока выделена пользовательская тема, чтобы отредактировать её.

Каждая пользовательская тема — это JSON-файл в `~/.claude/themes/`. Имя файла без расширения `.json` — это слаг темы, и выбор темы сохраняет `custom:<slug>` как ваше предпочтение темы. Файл имеет три необязательных поля:

| Field       | Type   | Description                                                                                                                                     |
| :---------- | :----- | :---------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`      | string | Display label shown in `/theme`. Defaults to the filename slug                                                                                  |
| `base`      | string | Built-in preset the theme starts from: `dark`, `light`, `dark-daltonized`, `light-daltonized`, `dark-ansi`, or `light-ansi`. Defaults to `dark` |
| `overrides` | object | Map of color token names to color values. Tokens not listed here fall through to the base preset                                                |

Цветовые значения принимают `#rrggbb`, `#rgb`, `rgb(r,g,b)`, `ansi256(n)` или `ansi:<name>`, где `<name>` — одно из 16 стандартных имён цветов ANSI, таких как `red` или `cyanBright`. Неизвестные токены и недопустимые цветовые значения игнорируются, поэтому опечатка не может нарушить отрисовку.

Следующий пример определяет тему, которая сохраняет тёмную предустановку, но перекрашивает акцент приглашения, текст ошибки и текст успеха:

```json ~/.claude/themes/dracula.json theme={null}
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

Claude Code отслеживает `~/.claude/themes/` и перезагружает при изменении файла, поэтому изменения, сделанные в вашем редакторе, применяются к работающему сеансу без перезагрузки.

Ниже приведён полный список настроек, которые вы можете установить в `overrides`. Интерактивный редактор в `/theme` показывает те же токены с живым предпросмотром, включая небольшое количество внутренних токенов, не описанных здесь.

<Accordion title="Color token reference">
  Следующий пример объединяет токены из нескольких групп ниже: фирменный акцент, граница режима Plan Mode, фоны diff и фон полноэкранного сообщения.

  ```json ~/.claude/themes/midnight.json theme={null}
  {
    "name": "Midnight",
    "base": "dark",
    "overrides": {
      "claude": "#a78bfa",
      "planMode": "#38bdf8",
      "diffAdded": "#14532d",
      "diffRemoved": "#7f1d1d",
      "userMessageBackground": "#1e1b4b"
    }
  }
  ```

  #### Text and accent colors

  Управляйте основным фирменным акцентом и оттенками переднего плана текста, используемыми во всём интерфейсе.

  | Token         | Controls                                                         |
  | :------------ | :--------------------------------------------------------------- |
  | `claude`      | Primary brand accent, used for the spinner and assistant label   |
  | `text`        | Default foreground text                                          |
  | `inverseText` | Text drawn on top of a colored background, such as status badges |
  | `inactive`    | Secondary text such as hints, timestamps, and disabled items     |
  | `subtle`      | Faint borders and de-emphasized secondary text                   |
  | `permission`  | Dialog borders, including permission prompts and pickers         |
  | `remember`    | Memory and `CLAUDE.md` indicators                                |

  #### Status colors

  Сигнализируйте об успехе, сбое и состояниях предупреждения в сообщениях и индикаторах.

  | Token     | Controls                                             |
  | :-------- | :--------------------------------------------------- |
  | `success` | Success messages and passing checks                  |
  | `error`   | Error messages and failures                          |
  | `warning` | Warnings, caution messages, and the auto mode border |
  | `merged`  | Merged pull request status                           |

  #### Input box and mode indicators

  Установите цвет границы поля ввода и акцент, отображаемый при активном режиме разрешения или индикаторе.

  | Token          | Controls                                           |
  | :------------- | :------------------------------------------------- |
  | `promptBorder` | Input box border in the default permission mode    |
  | `planMode`     | Plan mode accent and border                        |
  | `autoAccept`   | Accept-edits mode accent and border                |
  | `bashBorder`   | Input box border when entering a `!` shell command |
  | `ide`          | IDE connection indicator                           |
  | `fastMode`     | Fast mode indicator                                |

  #### Diff rendering

  Раскрасьте добавленный и удалённый код в редактировании файлов и рецензировании.

  | Token               | Controls                                           |
  | :------------------ | :------------------------------------------------- |
  | `diffAdded`         | Background of added lines                          |
  | `diffRemoved`       | Background of removed lines                        |
  | `diffAddedDimmed`   | Background of unchanged context near added lines   |
  | `diffRemovedDimmed` | Background of unchanged context near removed lines |
  | `diffAddedWord`     | Word-level highlight within an added line          |
  | `diffRemovedWord`   | Word-level highlight within a removed line         |

  #### Fullscreen mode

  Применяется только в [режиме полноэкранной отрисовки](/ru/fullscreen), где сообщения имеют заливку фона.

  | Token                   | Controls                                          |
  | :---------------------- | :------------------------------------------------ |
  | `userMessageBackground` | Background behind your messages in the transcript |
  | `selectionBg`           | Background of text selected with the mouse        |

  #### Shimmer variants and subagent colors

  Несколько токенов имеют парный вариант `Shimmer`, такой как `claudeShimmer` и `warningShimmer`, который предоставляет более светлый цвет, используемый в анимированном градиенте спиннера. Переопределите shimmer вместе с его базовым токеном, если анимация выглядит несоответствующей.

  Каждый [subagent](/ru/sub-agents) и параллельная задача отображаются в одном из восьми именованных цветов, чтобы вы могли различить их в транскрипте. Имена токенов следуют шаблону `<color>_FOR_SUBAGENTS_ONLY`, где `<color>` — это `red`, `blue`, `green`, `yellow`, `purple`, `orange`, `pink` или `cyan`. Переопределите их, чтобы изменить внешний вид каждого именованного цвета. Например, subagent с `color: blue` в его определении отображается с использованием значения `blue_FOR_SUBAGENTS_ONLY`.
</Accordion>

## Переключитесь на полноэкранный рендеринг

Если дисплей мерцает или позиция прокрутки прыгает, пока Claude работает, переключитесь на [режим полноэкранного рендеринга](/ru/fullscreen). Он рисует на отдельном экране, который терминал зарезервировал для полноэкранных приложений, вместо добавления в вашу обычную прокрутку, что сохраняет использование памяти на плоском уровне и добавляет поддержку мыши для прокрутки и выделения. В этом режиме вы прокручиваете с помощью мыши или PageUp внутри Claude Code, а не с помощью встроенной прокрутки вашего терминала; см. [страницу полноэкранного режима](/ru/fullscreen#search-and-review-the-conversation) для того, как искать и копировать.

Запустите `/tui fullscreen` для переключения в текущем сеансе с вашим разговором нетронутым. Чтобы сделать это по умолчанию, установите переменную окружения `CLAUDE_CODE_NO_FLICKER` перед запуском Claude Code:

<CodeGroup>
  ```bash Bash and Zsh theme={null}
  CLAUDE_CODE_NO_FLICKER=1 claude
  ```

  ```powershell PowerShell theme={null}
  $env:CLAUDE_CODE_NO_FLICKER = "1"; claude
  ```

  ```json ~/.claude/settings.json theme={null}
  {
    "env": {
      "CLAUDE_CODE_NO_FLICKER": "1"
    }
  }
  ```
</CodeGroup>

## Вставьте большое содержимое

Когда вы вставляете более 10 000 символов в приглашение, Claude Code сворачивает ввод в заполнитель `[Pasted text]`, чтобы поле ввода оставалось пригодным для использования. Полное содержимое всё ещё отправляется Claude при отправке.

Встроенный терминал VS Code может отбросить символы из очень больших вставок, прежде чем они достигнут Claude Code, поэтому предпочитайте рабочие процессы на основе файлов там. Для очень больших входных данных, таких как целые файлы или длинные журналы, запишите содержимое в файл и попросите Claude прочитать его вместо вставки. Это сохраняет стенограмму разговора читаемой и позволяет Claude ссылаться на файл по пути в более поздних ходах.

## Редактируйте приглашения с помощью сочетаний клавиш Vim

Claude Code включает режим редактирования в стиле Vim для ввода приглашения. Включите его через `/config` → Editor mode или установив [`editorMode`](/ru/settings#available-settings) на `"vim"` в `~/.claude/settings.json`. Установите Editor mode обратно на `normal`, чтобы отключить его.

Режим Vim поддерживает подмножество движений и операторов режима NORMAL и VISUAL, таких как навигация `hjkl`, выделение `v`/`V` и `d`/`c`/`y` с текстовыми объектами. См. [справочник режима редактора Vim](/ru/interactive-mode#vim-editor-mode) для полной таблицы клавиш. Движения Vim не переназначаются через файл сочетаний клавиш.

Нажатие Enter всё ещё отправляет ваше приглашение в режиме INSERT, в отличие от стандартного Vim. Используйте `o` или `O` в режиме NORMAL или Ctrl+J для вставки разрыва строки вместо этого.

## Связанные ресурсы

* [Интерактивный режим](/ru/interactive-mode): полный справочник сочетаний клавиш и таблица клавиш Vim
* [Сочетания клавиш](/ru/keybindings): переназначьте любое сочетание клавиш Claude Code, включая Enter и Shift+Enter
* [Полноэкранный рендеринг](/ru/fullscreen): детали прокрутки, поиска и копирования в полноэкранном режиме
* [Руководство по хукам](/ru/hooks-guide): больше примеров хуков Notification для Linux и Windows
* [Troubleshooting](/ru/troubleshooting): исправления для проблем вне конфигурации терминала
