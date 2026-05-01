> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Troubleshooting

> Исправьте высокое использование CPU или памяти, зависания, auto-compact thrashing и проблемы поиска в Claude Code, и найдите нужную страницу для других проблем.

Эта страница охватывает проблемы производительности, стабильности и поиска после того, как Claude Code запущен. Для других проблем начните со страницы, которая соответствует тому, где вы застряли:

| Симптом                                                                                                    | Перейти к                                                                                |
| :--------------------------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------- |
| `command not found`, ошибка установки, проблемы PATH, `EACCES`, ошибки TLS                                 | [Troubleshoot installation and login](/ru/troubleshoot-install)                          |
| Циклы входа, ошибки OAuth, `403 Forbidden`, "organization disabled", учётные данные Bedrock/Vertex/Foundry | [Troubleshoot installation and login](/ru/troubleshoot-install#login-and-authentication) |
| Параметры не применяются, hooks не срабатывают, MCP servers не загружаются                                 | [Debug your configuration](/ru/debug-your-config)                                        |
| `API Error: 5xx`, `529 Overloaded`, `429`, ошибки валидации запроса                                        | [Error reference](/ru/errors)                                                            |
| `model not found` или `you may not have access to it`                                                      | [Error reference](/ru/errors#theres-an-issue-with-the-selected-model)                    |
| Расширение VS Code не подключается или не обнаруживает Claude                                              | [VS Code integration](/ru/vs-code#fix-common-issues)                                     |
| Плагин JetBrains или IDE не обнаружена                                                                     | [JetBrains integration](/ru/jetbrains#troubleshooting)                                   |
| Высокое использование CPU или памяти, медленные ответы, зависания, поиск не находит файлы                  | [Performance and stability](#performance-and-stability) ниже                             |

Если вы не уверены, какой применяется, запустите `/doctor` внутри Claude Code для автоматической проверки вашей установки, параметров, MCP servers и использования контекста. Если `claude` вообще не запускается, запустите `claude doctor` из вашей оболочки вместо этого.

## Performance and stability

Эти разделы охватывают проблемы, связанные с использованием ресурсов, отзывчивостью и поведением поиска.

### High CPU or memory usage

Claude Code разработан для работы с большинством сред разработки, но может потреблять значительные ресурсы при обработке больших кодовых баз. Если вы испытываете проблемы с производительностью:

1. Используйте `/compact` регулярно, чтобы уменьшить размер контекста
2. Закройте и перезагрузите Claude Code между основными задачами
3. Рассмотрите добавление больших директорий сборки в ваш файл `.gitignore`

Если использование памяти остаётся высоким после этих шагов, запустите `/heapdump`, чтобы записать снимок кучи JavaScript и разбор памяти на `~/Desktop`. На Linux без папки Desktop файлы записываются в вашу домашнюю директорию.

Разбор показывает размер набора резидентов, кучу JS, буферы массивов и неучтённую собственную память, что помогает определить, находится ли рост в объектах JavaScript или в собственном коде. Чтобы проверить удерживающие элементы, откройте файл `.heapsnapshot` в Chrome DevTools под Memory → Load. Прикрепите оба файла при сообщении о проблеме с памятью на [GitHub](https://github.com/anthropics/claude-code/issues).

### Auto-compaction stops with a thrashing error

Если вы видите `Autocompact is thrashing: the context refilled to the limit...`, автоматическое сжатие прошло успешно, но файл или вывод инструмента немедленно заполнили окно контекста несколько раз подряд. Claude Code останавливает повторные попытки, чтобы избежать траты вызовов API на цикл, который не делает прогресс.

Чтобы восстановиться:

1. Попросите Claude прочитать большой файл в меньших фрагментах, таких как конкретный диапазон строк или функция, вместо всего файла
2. Запустите `/compact` с фокусом, который удаляет большой вывод, например `/compact keep only the plan and the diff`
3. Переместите работу с большим файлом на [subagent](/ru/sub-agents), чтобы она работала в отдельном окне контекста
4. Запустите `/clear`, если более ранний разговор больше не нужен

### Command hangs or freezes

Если Claude Code кажется неотзывчивым:

1. Нажмите Ctrl+C, чтобы попытаться отменить текущую операцию
2. Если неотзывчив, вам может потребоваться закрыть терминал и перезагрузить

Перезагрузка не теряет вашу беседу. Запустите `claude --resume` в той же директории, чтобы продолжить сеанс.

### Search and discovery issues

Если инструмент Search, упоминания `@file`, пользовательские агенты или пользовательские skills не находят файлы, встроенный двоичный файл `ripgrep` может не работать на вашей системе. Установите пакет `ripgrep` вашей платформы и скажите Claude Code использовать его вместо этого:

<Tabs>
  <Tab title="macOS">
    ```bash theme={null}
    brew install ripgrep
    ```
  </Tab>

  <Tab title="Ubuntu/Debian">
    ```bash theme={null}
    sudo apt install ripgrep
    ```
  </Tab>

  <Tab title="Alpine">
    ```bash theme={null}
    apk add ripgrep
    ```
  </Tab>

  <Tab title="Arch">
    ```bash theme={null}
    pacman -S ripgrep
    ```
  </Tab>

  <Tab title="Windows">
    ```powershell theme={null}
    winget install BurntSushi.ripgrep.MSVC
    ```
  </Tab>
</Tabs>

Затем установите `USE_BUILTIN_RIPGREP=0` в вашем [окружении](/ru/env-vars).

### Slow or incomplete search results on WSL

Штрафы производительности чтения диска при [работе с файловыми системами на WSL](https://learn.microsoft.com/en-us/windows/wsl/filesystems) могут привести к меньшему количеству совпадений, чем ожидается, при использовании Claude Code на WSL. Поиск всё ещё функционирует, но возвращает меньше результатов, чем на собственной файловой системе.

<Note>
  `/doctor` будет показывать Search как OK в этом случае.
</Note>

**Решения:**

1. **Отправляйте более конкретные поиски**: уменьшите количество файлов, которые ищутся, указав директории или типы файлов: "Search for JWT validation logic in the auth-service package" или "Find use of md5 hash in JS files".

2. **Переместите проект на файловую систему Linux**: если возможно, убедитесь, что ваш проект находится на файловой системе Linux (`/home/`) вместо файловой системы Windows (`/mnt/c/`).

3. **Используйте нативный Windows вместо этого**: рассмотрите запуск Claude Code нативно на Windows вместо WSL для лучшей производительности файловой системы.

## Get more help

Если вы испытываете проблемы, не охватываемые здесь:

1. Запустите `/doctor`, чтобы проверить здоровье установки, валидность параметров, конфигурацию MCP и использование контекста в одном проходе
2. Используйте команду `/feedback` в Claude Code, чтобы сообщить о проблемах непосредственно в Anthropic
3. Проверьте [репозиторий GitHub](https://github.com/anthropics/claude-code) на известные проблемы
4. Спросите Claude напрямую о его возможностях и функциях. Claude имеет встроенный доступ к своей документации.
