> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Troubleshooting

> Найдите решения распространённых проблем при установке и использовании Claude Code.

## Устранение проблем с установкой

<Tip>
  Если вы предпочитаете избежать терминала, [приложение Claude Code Desktop](/ru/desktop-quickstart) позволяет установить и использовать Claude Code через графический интерфейс. Загрузите его для [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) или [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs) и начните кодировать без настройки командной строки.
</Tip>

Найдите сообщение об ошибке или симптом, который вы видите:

| Что вы видите                                                     | Решение                                                                                                            |
| :---------------------------------------------------------------- | :----------------------------------------------------------------------------------------------------------------- |
| `command not found: claude` или `'claude' is not recognized`      | [Исправьте вашу PATH](#command-not-found-claude-after-installation)                                                |
| `syntax error near unexpected token '<'`                          | [Скрипт установки возвращает HTML](#install-script-returns-html-instead-of-a-shell-script)                         |
| `curl: (56) Failure writing output to destination`                | [Сначала загрузите скрипт, затем запустите его](#curl-56-failure-writing-output-to-destination)                    |
| `Killed` во время установки на Linux                              | [Добавьте пространство подкачки для серверов с низкой памятью](#install-killed-on-low-memory-linux-servers)        |
| `TLS connect error` или `SSL/TLS secure channel`                  | [Обновите сертификаты CA](#tls-or-ssl-connection-errors)                                                           |
| `Failed to fetch version` или невозможно достичь сервера загрузки | [Проверьте параметры сети и прокси](#check-network-connectivity)                                                   |
| `irm is not recognized` или `&& is not valid`                     | [Используйте правильную команду для вашей оболочки](#windows-irm-or--not-recognized)                               |
| `Claude Code on Windows requires git-bash`                        | [Установите или настройте Git Bash](#windows-claude-code-on-windows-requires-git-bash)                             |
| `Error loading shared library`                                    | [Неправильный вариант двоичного файла для вашей системы](#linux-wrong-binary-variant-installed-muslglibc-mismatch) |
| `Illegal instruction` на Linux                                    | [Несоответствие архитектуры](#illegal-instruction-on-linux)                                                        |
| `dyld: cannot load` или `Abort trap` на macOS                     | [Несовместимость двоичного файла](#dyld-cannot-load-on-macos)                                                      |
| `Invoke-Expression: Missing argument in parameter list`           | [Скрипт установки возвращает HTML](#install-script-returns-html-instead-of-a-shell-script)                         |
| `App unavailable in region`                                       | Claude Code недоступен в вашей стране. См. [поддерживаемые страны](https://www.anthropic.com/supported-countries). |
| `unable to get local issuer certificate`                          | [Настройте корпоративные сертификаты CA](#tls-or-ssl-connection-errors)                                            |
| `OAuth error` или `403 Forbidden`                                 | [Исправьте аутентификацию](#authentication-issues)                                                                 |

Если вашей проблемы нет в списке, выполните эти диагностические шаги.

## Отладка проблем установки

### Проверьте подключение к сети

Установщик загружает файлы с `storage.googleapis.com`. Убедитесь, что вы можете его достичь:

```bash  theme={null}
curl -sI https://storage.googleapis.com
```

Если это не удаётся, ваша сеть может блокировать соединение. Распространённые причины:

* Корпоративные брандмауэры или прокси, блокирующие Google Cloud Storage
* Региональные ограничения сети: попробуйте VPN или альтернативную сеть
* Проблемы TLS/SSL: обновите сертификаты CA вашей системы или проверьте, настроена ли переменная `HTTPS_PROXY`

Если вы находитесь за корпоративным прокси, установите `HTTPS_PROXY` и `HTTP_PROXY` на адрес вашего прокси перед установкой. Попросите URL прокси у вашей IT-команды, если вы его не знаете, или проверьте параметры прокси в браузере.

Этот пример устанавливает обе переменные прокси, а затем запускает установщик через ваш прокси:

```bash  theme={null}
export HTTP_PROXY=http://proxy.example.com:8080
export HTTPS_PROXY=http://proxy.example.com:8080
curl -fsSL https://claude.ai/install.sh | bash
```

### Проверьте вашу PATH

Если установка прошла успешно, но вы получаете ошибку `command not found` или `not recognized` при запуске `claude`, директория установки не находится в вашей PATH. Ваша оболочка ищет программы в директориях, указанных в PATH, и установщик размещает `claude` в `~/.local/bin/claude` на macOS/Linux или `%USERPROFILE%\.local\bin\claude.exe` на Windows.

Проверьте, находится ли директория установки в вашей PATH, перечислив записи PATH и отфильтровав `local/bin`:

<Tabs>
  <Tab title="macOS/Linux">
    ```bash  theme={null}
    echo $PATH | tr ':' '\n' | grep local/bin
    ```

    Если нет вывода, директория отсутствует. Добавьте её в конфигурацию вашей оболочки:

    ```bash  theme={null}
    # Zsh (стандартная оболочка macOS)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc

    # Bash (стандартная оболочка Linux)
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    source ~/.bashrc
    ```

    Или закройте и снова откройте ваш терминал.

    Проверьте, что исправление сработало:

    ```bash  theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    $env:PATH -split ';' | Select-String 'local\\bin'
    ```

    Если нет вывода, добавьте директорию установки в вашу User PATH:

    ```powershell  theme={null}
    $currentPath = [Environment]::GetEnvironmentVariable('PATH', 'User')
    [Environment]::SetEnvironmentVariable('PATH', "$currentPath;$env:USERPROFILE\.local\bin", 'User')
    ```

    Перезагрузите ваш терминал, чтобы изменение вступило в силу.

    Проверьте, что исправление сработало:

    ```powershell  theme={null}
    claude --version
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    echo %PATH% | findstr /i "local\bin"
    ```

    Если нет вывода, откройте параметры системы, перейдите в переменные окружения и добавьте `%USERPROFILE%\.local\bin` в вашу переменную User PATH. Перезагрузите ваш терминал.

    Проверьте, что исправление сработало:

    ```batch  theme={null}
    claude --version
    ```
  </Tab>
</Tabs>

### Проверьте конфликтующие установки

Несколько установок Claude Code могут вызвать несоответствия версий или неожиданное поведение. Проверьте, что установлено:

<Tabs>
  <Tab title="macOS/Linux">
    Перечислите все двоичные файлы `claude`, найденные в вашей PATH:

    ```bash  theme={null}
    which -a claude
    ```

    Проверьте, присутствуют ли собственный установщик и версии npm:

    ```bash  theme={null}
    ls -la ~/.local/bin/claude
    ```

    ```bash  theme={null}
    ls -la ~/.claude/local/
    ```

    ```bash  theme={null}
    npm -g ls @anthropic-ai/claude-code 2>/dev/null
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    where.exe claude
    Test-Path "$env:LOCALAPPDATA\Claude Code\claude.exe"
    ```
  </Tab>
</Tabs>

Если вы найдёте несколько установок, оставьте только одну. Собственная установка в `~/.local/bin/claude` рекомендуется. Удалите все дополнительные установки:

Удалите глобальную установку npm:

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

Удалите установку Homebrew на macOS:

```bash  theme={null}
brew uninstall --cask claude-code
```

### Проверьте разрешения директории

Установщику требуется доступ на запись в `~/.local/bin/` и `~/.claude/`. Если установка не удаётся с ошибками разрешений, проверьте, доступны ли эти директории для записи:

```bash  theme={null}
test -w ~/.local/bin && echo "writable" || echo "not writable"
test -w ~/.claude && echo "writable" || echo "not writable"
```

Если какая-либо директория недоступна для записи, создайте директорию установки и установите вашего пользователя владельцем:

```bash  theme={null}
sudo mkdir -p ~/.local/bin
sudo chown -R $(whoami) ~/.local
```

### Проверьте, работает ли двоичный файл

Если `claude` установлен, но падает или зависает при запуске, выполните эти проверки, чтобы сузить причину.

Подтвердите, что двоичный файл существует и исполняемый:

```bash  theme={null}
ls -la $(which claude)
```

На Linux проверьте отсутствующие общие библиотеки. Если `ldd` показывает отсутствующие библиотеки, вам может потребоваться установить системные пакеты. На Alpine Linux и других дистрибутивах на основе musl см. [Настройка Alpine Linux](/ru/setup#alpine-linux-and-musl-based-distributions).

```bash  theme={null}
ldd $(which claude) | grep "not found"
```

Запустите быструю проверку работоспособности, что двоичный файл может выполняться:

```bash  theme={null}
claude --version
```

## Распространённые проблемы установки

Это наиболее часто встречающиеся проблемы установки и их решения.

### Скрипт установки возвращает HTML вместо скрипта оболочки

При запуске команды установки вы можете увидеть одну из этих ошибок:

```text  theme={null}
bash: line 1: syntax error near unexpected token `<'
bash: line 1: `<!DOCTYPE html>'
```

На PowerShell та же проблема выглядит как:

```text  theme={null}
Invoke-Expression: Missing argument in parameter list.
```

Это означает, что URL установки вернул HTML-страницу вместо скрипта установки. Если HTML-страница говорит "App unavailable in region", Claude Code недоступен в вашей стране. См. [поддерживаемые страны](https://www.anthropic.com/supported-countries).

В противном случае это может произойти из-за проблем с сетью, региональной маршрутизации или временного сбоя сервиса.

**Решения:**

1. **Используйте альтернативный метод установки**:

   На macOS или Linux установите через Homebrew:

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   На Windows установите через WinGet:

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

2. **Повторите попытку через несколько минут**: проблема часто временная. Подождите и попробуйте исходную команду снова.

### `command not found: claude` после установки

Установка завершилась, но `claude` не работает. Точная ошибка варьируется в зависимости от платформы:

| Платформа   | Сообщение об ошибке                                                    |
| :---------- | :--------------------------------------------------------------------- |
| macOS       | `zsh: command not found: claude`                                       |
| Linux       | `bash: claude: command not found`                                      |
| Windows CMD | `'claude' is not recognized as an internal or external command`        |
| PowerShell  | `claude : The term 'claude' is not recognized as the name of a cmdlet` |

Это означает, что директория установки не находится в пути поиска вашей оболочки. См. [Проверьте вашу PATH](#verify-your-path) для исправления на каждой платформе.

### `curl: (56) Failure writing output to destination`

Команда `curl ... | bash` загружает скрипт и передаёт его непосредственно Bash для выполнения через конвейер (`|`). Эта ошибка означает, что соединение разорвалось до завершения загрузки скрипта. Распространённые причины включают сетевые перебои, блокировку загрузки в процессе или ограничения системных ресурсов.

**Решения:**

1. **Проверьте стабильность сети**: двоичные файлы Claude Code размещены на Google Cloud Storage. Проверьте, что вы можете его достичь:
   ```bash  theme={null}
   curl -fsSL https://storage.googleapis.com -o /dev/null
   ```
   Если команда завершается молча, ваше соединение в порядке и проблема, вероятно, временная. Повторите команду установки. Если вы видите ошибку, ваша сеть может блокировать загрузку.

2. **Попробуйте альтернативный метод установки**:

   На macOS или Linux:

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   На Windows:

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

### Ошибки подключения TLS или SSL

Ошибки вроде `curl: (35) TLS connect error`, `schannel: next InitializeSecurityContext failed` или PowerShell's `Could not establish trust relationship for the SSL/TLS secure channel` указывают на сбои рукопожатия TLS.

**Решения:**

1. **Обновите сертификаты CA вашей системы**:

   На Ubuntu/Debian:

   ```bash  theme={null}
   sudo apt-get update && sudo apt-get install ca-certificates
   ```

   На macOS через Homebrew:

   ```bash  theme={null}
   brew install ca-certificates
   ```

2. **На Windows включите TLS 1.2** в PowerShell перед запуском установщика:
   ```powershell  theme={null}
   [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
   irm https://claude.ai/install.ps1 | iex
   ```

3. **Проверьте помехи прокси или брандмауэра**: корпоративные прокси, выполняющие проверку TLS, могут вызвать эти ошибки, включая `unable to get local issuer certificate`. Установите `NODE_EXTRA_CA_CERTS` на ваш пакет корпоративного сертификата CA:
   ```bash  theme={null}
   export NODE_EXTRA_CA_CERTS=/path/to/corporate-ca.pem
   ```
   Попросите файл сертификата у вашей IT-команды, если у вас его нет. Вы также можете попробовать прямое соединение, чтобы подтвердить, что прокси является причиной.

### `Failed to fetch version from storage.googleapis.com`

Установщик не смог достичь сервер загрузки. Это обычно означает, что `storage.googleapis.com` заблокирован в вашей сети.

**Решения:**

1. **Проверьте подключение напрямую**:
   ```bash  theme={null}
   curl -sI https://storage.googleapis.com
   ```

2. **Если находитесь за прокси**, установите `HTTPS_PROXY`, чтобы установщик мог маршрутизировать через него. См. [конфигурация прокси](/ru/network-config#proxy-configuration) для деталей.
   ```bash  theme={null}
   export HTTPS_PROXY=http://proxy.example.com:8080
   curl -fsSL https://claude.ai/install.sh | bash
   ```

3. **Если находитесь в ограниченной сети**, попробуйте другую сеть или VPN, или используйте альтернативный метод установки:

   На macOS или Linux:

   ```bash  theme={null}
   brew install --cask claude-code
   ```

   На Windows:

   ```powershell  theme={null}
   winget install Anthropic.ClaudeCode
   ```

### Windows: `irm` или `&&` не распознаны

Если вы видите `'irm' is not recognized` или `The token '&&' is not valid`, вы запускаете неправильную команду для вашей оболочки.

* **`irm` не распознана**: вы находитесь в CMD, а не PowerShell. У вас есть два варианта:

  Откройте PowerShell, выполнив поиск "PowerShell" в меню "Пуск", затем запустите исходную команду установки:

  ```powershell  theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

  Или оставайтесь в CMD и используйте вместо этого установщик CMD:

  ```batch  theme={null}
  curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
  ```

* **`&&` не действительна**: вы находитесь в PowerShell, но запустили команду установщика CMD. Используйте установщик PowerShell:
  ```powershell  theme={null}
  irm https://claude.ai/install.ps1 | iex
  ```

### Установка прервана на серверах Linux с низкой памятью

Если вы видите `Killed` во время установки на VPS или облачном экземпляре:

```text  theme={null}
Setting up Claude Code...
Installing Claude Code native build latest...
bash: line 142: 34803 Killed    "$binary_path" install ${TARGET:+"$TARGET"}
```

Убийца OOM Linux завершил процесс, потому что система исчерпала память. Claude Code требует как минимум 4 ГБ доступной оперативной памяти.

**Решения:**

1. **Добавьте пространство подкачки**, если ваш сервер имеет ограниченную оперативную память. Подкачка использует дисковое пространство как переполнение памяти, позволяя установке завершиться даже при низкой физической оперативной памяти.

   Создайте файл подкачки размером 2 ГБ и включите его:

   ```bash  theme={null}
   sudo fallocate -l 2G /swapfile
   sudo chmod 600 /swapfile
   sudo mkswap /swapfile
   sudo swapon /swapfile
   ```

   Затем повторите установку:

   ```bash  theme={null}
   curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **Закройте другие процессы**, чтобы освободить память перед установкой.

3. **Используйте больший экземпляр**, если возможно. Claude Code требует как минимум 4 ГБ оперативной памяти.

### Установка зависает в Docker

При установке Claude Code в контейнер Docker установка от имени root в `/` может вызвать зависания.

**Решения:**

1. **Установите рабочую директорию** перед запуском установщика. При запуске из `/` установщик сканирует всю файловую систему, что вызывает чрезмерное использование памяти. Установка `WORKDIR` ограничивает сканирование небольшой директорией:
   ```dockerfile  theme={null}
   WORKDIR /tmp
   RUN curl -fsSL https://claude.ai/install.sh | bash
   ```

2. **Увеличьте лимиты памяти Docker**, если используете Docker Desktop:
   ```bash  theme={null}
   docker build --memory=4g .
   ```

### Windows: Claude Desktop переопределяет команду CLI `claude`

Если вы установили старую версию Claude Desktop, она может зарегистрировать `Claude.exe` в директории `WindowsApps`, которая имеет приоритет PATH над Claude Code CLI. Запуск `claude` открывает приложение Desktop вместо CLI.

Обновите Claude Desktop до последней версии, чтобы исправить эту проблему.

### Windows: "Claude Code on Windows requires git-bash"

Claude Code на нативном Windows требует [Git for Windows](https://git-scm.com/downloads/win), который включает Git Bash.

**Если Git не установлен**, загрузите и установите его с [git-scm.com/downloads/win](https://git-scm.com/downloads/win). Во время установки выберите "Add to PATH." Перезагрузите ваш терминал после установки.

**Если Git уже установлен**, но Claude Code всё ещё не может его найти, установите путь в вашем [файле settings.json](/ru/settings):

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

Если ваш Git установлен в другом месте, найдите путь, запустив `where.exe git` в PowerShell и используйте путь `bin\bash.exe` из этой директории.

### Linux: неправильный вариант двоичного файла установлен (несоответствие musl/glibc)

Если вы видите ошибки об отсутствующих общих библиотеках вроде `libstdc++.so.6` или `libgcc_s.so.1` после установки, установщик мог загрузить неправильный вариант двоичного файла для вашей системы.

```text  theme={null}
Error loading shared library libstdc++.so.6: No such file or directory
```

Это может произойти на системах на основе glibc, которые имеют установленные пакеты кросс-компиляции musl, вызывая неправильное обнаружение системы как musl установщиком.

**Решения:**

1. **Проверьте, какой libc использует ваша система**:
   ```bash  theme={null}
   ldd /bin/ls | head -1
   ```
   Если это показывает `linux-vdso.so` или ссылки на `/lib/x86_64-linux-gnu/`, вы находитесь на glibc. Если это показывает `musl`, вы находитесь на musl.

2. **Если вы находитесь на glibc, но получили двоичный файл musl**, удалите установку и переустановите. Вы также можете вручную загрузить правильный двоичный файл из корзины GCS по адресу `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json`. Подайте [проблему GitHub](https://github.com/anthropics/claude-code/issues) с выводом `ldd /bin/ls` и `ls /lib/libc.musl*`.

3. **Если вы действительно находитесь на musl** (Alpine Linux), установите требуемые пакеты:
   ```bash  theme={null}
   apk add libgcc libstdc++ ripgrep
   ```

### `Illegal instruction` на Linux

Если установщик выводит `Illegal instruction` вместо сообщения OOM `Killed`, загруженный двоичный файл не соответствует архитектуре вашего процессора. Это обычно происходит на серверах ARM, которые получают двоичный файл x86, или на старых процессорах, которым не хватает требуемых наборов инструкций.

```text  theme={null}
bash: line 142: 2238232 Illegal instruction    "$binary_path" install ${TARGET:+"$TARGET"}
```

**Решения:**

1. **Проверьте вашу архитектуру**:
   ```bash  theme={null}
   uname -m
   ```
   `x86_64` означает 64-битный Intel/AMD, `aarch64` означает ARM64. Если двоичный файл не соответствует, [подайте проблему GitHub](https://github.com/anthropics/claude-code/issues) с выводом.

2. **Попробуйте альтернативный метод установки**, пока проблема архитектуры не будет решена:
   ```bash  theme={null}
   brew install --cask claude-code
   ```

### `dyld: cannot load` на macOS

Если вы видите `dyld: cannot load` или `Abort trap: 6` во время установки, двоичный файл несовместим с вашей версией macOS или оборудованием.

```text  theme={null}
dyld: cannot load 'claude-2.1.42-darwin-x64' (load command 0x80000034 is unknown)
Abort trap: 6
```

**Решения:**

1. **Проверьте вашу версию macOS**: Claude Code требует macOS 13.0 или позже. Откройте меню Apple и выберите "About This Mac", чтобы проверить вашу версию.

2. **Обновите macOS**, если вы находитесь на старой версии. Двоичный файл использует команды загрузки, которые старые версии macOS не поддерживают.

3. **Попробуйте Homebrew** как альтернативный метод установки:
   ```bash  theme={null}
   brew install --cask claude-code
   ```

### Проблемы установки Windows: ошибки в WSL

Вы можете столкнуться со следующими проблемами в WSL:

**Проблемы обнаружения ОС/платформы**: если вы получаете ошибку во время установки, WSL может использовать Windows `npm`. Попробуйте:

* Запустите `npm config set os linux` перед установкой
* Установите с `npm install -g @anthropic-ai/claude-code --force --no-os-check`. Не используйте `sudo`.

**Ошибки "Node not found"**: если вы видите `exec: node: not found` при запуске `claude`, ваша среда WSL может использовать установку Node.js для Windows. Вы можете подтвердить это с помощью `which npm` и `which node`, которые должны указывать на пути Linux, начинающиеся с `/usr/`, а не `/mnt/c/`. Чтобы исправить это, попробуйте установить Node через менеджер пакетов вашего дистрибутива Linux или через [`nvm`](https://github.com/nvm-sh/nvm).

**Конфликты версий nvm**: если у вас установлен nvm как в WSL, так и в Windows, вы можете испытать конфликты версий при переключении версий Node в WSL. Это происходит, потому что WSL импортирует Windows PATH по умолчанию, вызывая приоритет Windows nvm/npm над установкой WSL.

Вы можете определить эту проблему:

* Запустив `which npm` и `which node` - если они указывают на пути Windows (начинающиеся с `/mnt/c/`), используются версии Windows
* Испытав нарушенную функциональность после переключения версий Node с nvm в WSL

Чтобы решить эту проблему, исправьте вашу Linux PATH, чтобы убедиться, что версии Linux node/npm имеют приоритет:

**Основное решение: убедитесь, что nvm правильно загружен в вашей оболочке**

Наиболее распространённая причина заключается в том, что nvm не загружается в неинтерактивных оболочках. Добавьте следующее в ваш файл конфигурации оболочки (`~/.bashrc`, `~/.zshrc` и т. д.):

```bash  theme={null}
# Load nvm if it exists
export NVM_DIR="$HOME/.nvm"
[ -s "$NVM_DIR/nvm.sh" ] && \. "$NVM_DIR/nvm.sh"
[ -s "$NVM_DIR/bash_completion" ] && \. "$NVM_DIR/bash_completion"
```

Или запустите непосредственно в вашем текущем сеансе:

```bash  theme={null}
source ~/.nvm/nvm.sh
```

**Альтернатива: отрегулируйте порядок PATH**

Если nvm правильно загружен, но пути Windows всё ещё имеют приоритет, вы можете явно добавить ваши пути Linux в PATH в конфигурации вашей оболочки:

```bash  theme={null}
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

<Warning>
  Избегайте отключения импорта Windows PATH через `appendWindowsPath = false`, так как это нарушает возможность вызывать исполняемые файлы Windows из WSL. Аналогично, избегайте удаления Node.js из Windows, если вы используете его для разработки Windows.
</Warning>

### Настройка sandbox WSL2

[Sandboxing](/ru/sandboxing) поддерживается на WSL2, но требует установки дополнительных пакетов. Если вы видите ошибку вроде "Sandbox requires socat and bubblewrap" при запуске `/sandbox`, установите зависимости:

<Tabs>
  <Tab title="Ubuntu/Debian">
    ```bash  theme={null}
    sudo apt-get install bubblewrap socat
    ```
  </Tab>

  <Tab title="Fedora">
    ```bash  theme={null}
    sudo dnf install bubblewrap socat
    ```
  </Tab>
</Tabs>

WSL1 не поддерживает sandboxing. Если вы видите "Sandboxing requires WSL2", вам нужно обновиться на WSL2 или запустить Claude Code без sandboxing.

### Ошибки разрешений во время установки

Если собственный установщик не удаётся с ошибками разрешений, целевая директория может быть недоступна для записи. См. [Проверьте разрешения директории](#check-directory-permissions).

Если вы ранее установили с npm и получаете ошибки разрешений, специфичные для npm, переключитесь на собственный установщик:

```bash  theme={null}
curl -fsSL https://claude.ai/install.sh | bash
```

## Разрешения и аутентификация

Эти разделы рассматривают сбои входа, проблемы с токенами и поведение запросов разрешений.

### Повторяющиеся запросы разрешений

Если вы обнаружите, что постоянно одобряете одни и те же команды, вы можете разрешить определённым инструментам работать без одобрения, используя команду `/permissions`. См. [документацию разрешений](/ru/permissions#manage-permissions).

### Проблемы аутентификации

Если вы испытываете проблемы с аутентификацией:

1. Запустите `/logout`, чтобы полностью выйти
2. Закройте Claude Code
3. Перезагрузитесь с `claude` и завершите процесс аутентификации снова

Если браузер не открывается автоматически во время входа, нажмите `c`, чтобы скопировать URL OAuth в буфер обмена, затем вставьте его в браузер вручную.

### Ошибка OAuth: Invalid code

Если вы видите `OAuth error: Invalid code. Please make sure the full code was copied`, код входа истёк или был усечён при копировании-вставке.

**Решения:**

* Нажмите Enter, чтобы повторить попытку и завершить вход быстро после открытия браузера
* Введите `c`, чтобы скопировать полный URL, если браузер не открывается автоматически
* Если вы используете удалённый/SSH сеанс, браузер может открыться на неправильной машине. Скопируйте URL, отображаемый в терминале, и откройте его в вашем локальном браузере вместо этого.

### 403 Forbidden после входа

Если вы видите `API Error: 403 {"error":{"type":"forbidden","message":"Request not allowed"}}` после входа:

* **Пользователи Claude Pro/Max**: проверьте, что ваша подписка активна на [claude.ai/settings](https://claude.ai/settings)
* **Пользователи Console**: подтвердите, что ваша учётная запись имеет роль "Claude Code" или "Developer", назначенную вашим администратором
* **За прокси**: корпоративные прокси могут помешать запросам API. См. [конфигурация сети](/ru/network-config) для настройки прокси.

### Вход OAuth не удаётся в WSL2

Вход на основе браузера в WSL2 может не удаться, если WSL не может открыть ваш браузер Windows. Установите переменную окружения `BROWSER`:

```bash  theme={null}
export BROWSER="/mnt/c/Program Files/Google/Chrome/Application/chrome.exe"
claude
```

Или скопируйте URL вручную: когда появляется запрос входа, нажмите `c`, чтобы скопировать URL OAuth, затем вставьте его в ваш браузер Windows.

### "Not logged in" или токен истёк

Если Claude Code предлагает вам войти снова после сеанса, ваш токен OAuth может истечь.

Запустите `/login`, чтобы повторно аутентифицироваться. Если это происходит часто, проверьте, что ваши системные часы точны, так как проверка токена зависит от правильных временных меток.

## Расположение файлов конфигурации

Claude Code хранит конфигурацию в нескольких местах:

| Файл                          | Назначение                                                                                                               |
| :---------------------------- | :----------------------------------------------------------------------------------------------------------------------- |
| `~/.claude/settings.json`     | Параметры пользователя (разрешения, hooks, переопределения модели)                                                       |
| `.claude/settings.json`       | Параметры проекта (проверены в системе управления версиями)                                                              |
| `.claude/settings.local.json` | Локальные параметры проекта (не зафиксированы)                                                                           |
| `~/.claude.json`              | Глобальное состояние (тема, OAuth, MCP servers)                                                                          |
| `.mcp.json`                   | MCP servers проекта (проверены в системе управления версиями)                                                            |
| `managed-mcp.json`            | [Управляемые MCP servers](/ru/mcp#managed-mcp-configuration)                                                             |
| Управляемые параметры         | [Управляемые параметры](/ru/settings#settings-files) (управляемые сервером, политики MDM/уровня ОС или на основе файлов) |

На Windows `~` относится к вашей домашней директории пользователя, такой как `C:\Users\YourName`.

Для деталей по настройке этих файлов см. [Параметры](/ru/settings) и [MCP](/ru/mcp).

### Сброс конфигурации

Чтобы сбросить Claude Code на параметры по умолчанию, вы можете удалить файлы конфигурации:

```bash  theme={null}
# Reset all user settings and state
rm ~/.claude.json
rm -rf ~/.claude/

# Reset project-specific settings
rm -rf .claude/
rm .mcp.json
```

<Warning>
  Это удалит все ваши параметры, конфигурации MCP server и историю сеанса.
</Warning>

## Производительность и стабильность

Эти разделы охватывают проблемы, связанные с использованием ресурсов, отзывчивостью и поведением поиска.

### Высокое использование CPU или памяти

Claude Code разработан для работы с большинством сред разработки, но может потреблять значительные ресурсы при обработке больших кодовых баз. Если вы испытываете проблемы с производительностью:

1. Используйте `/compact` регулярно, чтобы уменьшить размер контекста
2. Закройте и перезагрузите Claude Code между основными задачами
3. Рассмотрите добавление больших директорий сборки в ваш файл `.gitignore`

### Команда зависает или замораживается

Если Claude Code кажется неотзывчивым:

1. Нажмите Ctrl+C, чтобы попытаться отменить текущую операцию
2. Если неотзывчив, вам может потребоваться закрыть терминал и перезагрузить

### Проблемы поиска и обнаружения

Если инструмент Search, упоминания `@file`, пользовательские агенты и пользовательские skills не работают, установите системный `ripgrep`:

```bash  theme={null}
# macOS (Homebrew)  
brew install ripgrep

# Windows (winget)
winget install BurntSushi.ripgrep.MSVC

# Ubuntu/Debian
sudo apt install ripgrep

# Alpine Linux
apk add ripgrep

# Arch Linux
pacman -S ripgrep
```

Затем установите `USE_BUILTIN_RIPGREP=0` в вашем [окружении](/ru/env-vars).

### Медленные или неполные результаты поиска на WSL

Штрафы производительности чтения диска при [работе с файловыми системами на WSL](https://learn.microsoft.com/en-us/windows/wsl/filesystems) могут привести к меньшему количеству совпадений, чем ожидается, при использовании Claude Code на WSL. Поиск всё ещё функционирует, но возвращает меньше результатов, чем на собственной файловой системе.

<Note>
  `/doctor` будет показывать Search как OK в этом случае.
</Note>

**Решения:**

1. **Отправляйте более конкретные поиски**: уменьшите количество файлов, которые ищутся, указав директории или типы файлов: "Search for JWT validation logic in the auth-service package" или "Find use of md5 hash in JS files".

2. **Переместите проект на файловую систему Linux**: если возможно, убедитесь, что ваш проект находится на файловой системе Linux (`/home/`) вместо файловой системы Windows (`/mnt/c/`).

3. **Используйте нативный Windows вместо этого**: рассмотрите запуск Claude Code нативно на Windows вместо WSL для лучшей производительности файловой системы.

## Проблемы интеграции IDE

Если Claude Code не подключается к вашей IDE или ведёт себя неожиданно в терминале IDE, попробуйте решения ниже.

### IDE JetBrains не обнаружена на WSL2

Если вы используете Claude Code на WSL2 с IDE JetBrains и получаете ошибки "No available IDEs detected", это, вероятно, связано с конфигурацией сети WSL2 или брандмауэром Windows, блокирующим соединение.

#### Режимы сети WSL2

WSL2 использует сетевой режим NAT по умолчанию, который может предотвратить обнаружение IDE. У вас есть два варианта:

**Вариант 1: Настройте брандмауэр Windows** (рекомендуется)

1. Найдите ваш IP-адрес WSL2:
   ```bash  theme={null}
   wsl hostname -I
   # Example output: 172.21.123.45
   ```

2. Откройте PowerShell от имени администратора и создайте правило брандмауэра:
   ```powershell  theme={null}
   New-NetFirewallRule -DisplayName "Allow WSL2 Internal Traffic" -Direction Inbound -Protocol TCP -Action Allow -RemoteAddress 172.21.0.0/16 -LocalAddress 172.21.0.0/16
   ```
   Отрегулируйте диапазон IP на основе вашей подсети WSL2 из шага 1.

3. Перезагрузите как вашу IDE, так и Claude Code

**Вариант 2: Переключитесь на зеркальную сеть**

Добавьте в `.wslconfig` в вашей директории пользователя Windows:

```ini  theme={null}
[wsl2]
networkingMode=mirrored
```

Затем перезагрузите WSL с `wsl --shutdown` из PowerShell.

<Note>
  Эти проблемы с сетью влияют только на WSL2. WSL1 использует сеть хоста напрямую и не требует этих конфигураций.
</Note>

Для дополнительных советов по конфигурации JetBrains см. [руководство IDE JetBrains](/ru/jetbrains#plugin-settings).

### Сообщите о проблемах интеграции IDE Windows

Если вы испытываете проблемы с интеграцией IDE на Windows, [создайте проблему](https://github.com/anthropics/claude-code/issues) со следующей информацией:

* Тип окружения: нативный Windows (Git Bash) или WSL1/WSL2
* Режим сети WSL, если применимо: NAT или зеркальный
* Имя и версия IDE
* Версия расширения/плагина Claude Code
* Тип оболочки: Bash, Zsh, PowerShell и т. д.

### Клавиша Escape не работает в терминалах IDE JetBrains

Если вы используете Claude Code в терминалах JetBrains и клавиша `Esc` не прерывает агента, как ожидается, это, вероятно, связано с конфликтом сочетаний клавиш с стандартными ярлыками JetBrains.

Чтобы исправить эту проблему:

1. Перейдите в Settings → Tools → Terminal
2. Либо:
   * Снимите флажок "Move focus to the editor with Escape", либо
   * Нажмите "Configure terminal keybindings" и удалите ярлык "Switch focus to Editor"
3. Примените изменения

Это позволяет клавише `Esc` правильно прерывать операции Claude Code.

## Проблемы форматирования Markdown

Claude Code иногда генерирует файлы markdown с отсутствующими тегами языка на ограждениях кода, что может повлиять на подсветку синтаксиса и читаемость в GitHub, редакторах и инструментах документации.

### Отсутствующие теги языка в блоках кода

Если вы заметите блоки кода вроде этого в сгенерированном markdown:

````markdown  theme={null}
```
function example() {
  return "hello";
}
```text
````

Вместо правильно помеченных блоков вроде:

````markdown  theme={null}
```javascript
function example() {
  return "hello";
}
```text
````

**Решения:**

1. **Попросите Claude добавить теги языка**: запросите "Add appropriate language tags to all code blocks in this markdown file."

2. **Используйте hooks постобработки**: установите автоматические hooks форматирования для обнаружения и добавления отсутствующих тегов языка. См. [Auto-format code after edits](/ru/hooks-guide#auto-format-code-after-edits) для примера hook PostToolUse форматирования.

3. **Ручная проверка**: после генерации файлов markdown проверьте их на правильное форматирование блоков кода и запросите исправления, если необходимо.

### Несогласованный интервал и форматирование

Если сгенерированный markdown имеет чрезмерные пустые строки или несогласованный интервал:

**Решения:**

1. **Запросите исправления форматирования**: попросите Claude "Fix spacing and formatting issues in this markdown file."

2. **Используйте инструменты форматирования**: установите hooks для запуска форматировщиков markdown вроде `prettier` или пользовательских скриптов форматирования на сгенерированных файлах markdown.

3. **Укажите предпочтения форматирования**: включите требования форматирования в ваши подсказки или файлы [памяти](/ru/memory) проекта.

### Уменьшите проблемы форматирования markdown

Чтобы минимизировать проблемы форматирования:

* **Будьте явны в запросах**: попросите "properly formatted markdown with language-tagged code blocks"
* **Используйте соглашения проекта**: документируйте ваш предпочитаемый стиль markdown в [`CLAUDE.md`](/ru/memory)
* **Установите hooks валидации**: используйте hooks постобработки для автоматической проверки и исправления распространённых проблем форматирования

## Получите дополнительную помощь

Если вы испытываете проблемы, не охватываемые здесь:

1. Используйте команду `/bug` в Claude Code, чтобы сообщить о проблемах непосредственно в Anthropic
2. Проверьте [репозиторий GitHub](https://github.com/anthropics/claude-code) на известные проблемы
3. Запустите `/doctor`, чтобы диагностировать проблемы. Он проверяет:
   * Тип установки, версию и функциональность поиска
   * Статус автообновления и доступные версии
   * Неправильные файлы параметров (неправильный JSON, неправильные типы)
   * Ошибки конфигурации MCP server
   * Проблемы конфигурации сочетаний клавиш
   * Предупреждения об использовании контекста (большие файлы CLAUDE.md, высокое использование токенов MCP, недостижимые правила разрешений)
   * Ошибки загрузки плагинов и агентов
4. Спросите Claude напрямую о его возможностях и функциях - Claude имеет встроенный доступ к своей документации
