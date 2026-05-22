> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Расширенная настройка

> Системные требования, установка для конкретной платформы, управление версиями и удаление Claude Code.

На этой странице рассматриваются системные требования, детали установки для конкретной платформы, обновления и удаление. Для пошагового руководства по вашему первому сеансу см. [краткое руководство](/ru/quickstart). Если вы никогда раньше не использовали терминал, см. [руководство по терминалу](/ru/terminal-guide).

## Системные требования

Claude Code работает на следующих платформах и конфигурациях:

* **Операционная система**:
  * macOS 13.0+
  * Windows 10 1809+ или Windows Server 2019+
  * Ubuntu 20.04+
  * Debian 10+
  * Alpine Linux 3.19+
* **Оборудование**: 4 ГБ+ ОЗУ, процессор x64 или ARM64
* **Сеть**: требуется подключение в Интернет. См. [конфигурация сети](/ru/network-config#network-access-requirements).
* **Shell**: Bash, Zsh, PowerShell или CMD.
* **Местоположение**: [поддерживаемые Anthropic страны](https://www.anthropic.com/supported-countries)

### Дополнительные зависимости

* **ripgrep**: обычно включен в Claude Code. Если поиск не работает, см. [устранение неполадок поиска](/ru/troubleshooting#search-and-discovery-issues).

## Установка Claude Code

<Tip>
  Предпочитаете графический интерфейс? [Приложение Desktop](/ru/desktop-quickstart) позволяет использовать Claude Code без терминала. Загрузите его для [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) или [Windows](https://claude.com/download?utm_source=claude_code\&utm_medium=docs).

  Новичок в терминале? См. [руководство по терминалу](/ru/terminal-guide) для пошаговых инструкций.
</Tip>

To install Claude Code, use one of the following methods:

<Tabs>
  <Tab title="Native Install (Recommended)">
    **macOS, Linux, WSL:**

    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```

    **Windows PowerShell:**

    ```powershell theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```

    **Windows CMD:**

    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```

    If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. If you see `'irm' is not recognized as an internal or external command`, you're in CMD, not PowerShell. Your prompt shows `PS C:\` when you're in PowerShell and `C:\` without the `PS` when you're in CMD.

    [Git for Windows](https://git-scm.com/downloads/win) is recommended on native Windows so Claude Code can use the Bash tool. If Git for Windows is not installed, Claude Code uses PowerShell as the shell tool instead. WSL setups do not need Git for Windows.

    <Info>
      Native installations automatically update in the background to keep you on the latest version.
    </Info>
  </Tab>

  <Tab title="Homebrew">
    ```bash theme={null}
    brew install --cask claude-code
    ```

    Homebrew offers two casks. `claude-code` tracks the stable release channel, which is typically about a week behind and skips releases with major regressions. `claude-code@latest` tracks the latest channel and receives new versions as soon as they ship.

    <Info>
      Homebrew installations do not auto-update. Run `brew upgrade claude-code` or `brew upgrade claude-code@latest`, depending on which cask you installed, to get the latest features and security fixes.
    </Info>
  </Tab>

  <Tab title="WinGet">
    ```powershell theme={null}
    winget install Anthropic.ClaudeCode
    ```

    <Info>
      WinGet installations do not auto-update. Run `winget upgrade Anthropic.ClaudeCode` periodically to get the latest features and security fixes.
    </Info>
  </Tab>
</Tabs>

You can also install with [apt, dnf, or apk](/en/setup#install-with-linux-package-managers) on Debian, Fedora, RHEL, and Alpine.

После завершения установки откройте терминал в проекте, над которым вы хотите работать, и запустите Claude Code:

```bash theme={null}
claude
```

Если вы столкнулись с какими-либо проблемами во время установки, см. [Устранение неполадок при установке и входе](/ru/troubleshoot-install).

### Настройка в Windows

Вы можете запустить Claude Code изначально в Windows или внутри WSL. Выберите в зависимости от того, где находятся ваши проекты и какие функции вам нужны:

| Опция          | Требует                                                               | [Sandboxing](/ru/sandboxing) | Когда использовать                                             |
| -------------- | --------------------------------------------------------------------- | ---------------------------- | -------------------------------------------------------------- |
| Native Windows | Нет; [Git for Windows](https://git-scm.com/downloads/win) опционально | Не поддерживается            | Встроенные проекты и инструменты Windows                       |
| WSL 2          | WSL 2 включен                                                         | Поддерживается               | Цепочки инструментов Linux или изолированное выполнение команд |
| WSL 1          | WSL 1 включен                                                         | Не поддерживается            | Если WSL 2 недоступен                                          |

**Вариант 1: Native Windows**

Выполните команду установки из PowerShell или CMD. Вам не нужно запускать от имени администратора. Установка [Git for Windows](https://git-scm.com/downloads/win) опциональна. Она включает [инструмент Bash](/ru/tools-reference#bash-tool-behavior), предоставляя Git Bash.

Независимо от того, устанавливаете ли вы из PowerShell или CMD, это влияет только на то, какую команду установки вы выполняете. Ваша подсказка показывает `PS C:\Users\YourName>` в PowerShell и `C:\Users\YourName>` без `PS` в CMD. Если вы новичок в терминале, [руководство по терминалу](/ru/terminal-guide#windows) проходит через каждый шаг.

После установки запустите `claude` из любого терминала.

* **Без Git for Windows**, Claude Code запускает команды оболочки через [инструмент PowerShell](/ru/tools-reference#powershell-tool).
* **С Git for Windows**, Claude Code использует Git Bash для [инструмента Bash](/ru/tools-reference#bash-tool-behavior). Если Claude Code не может найти Git Bash, установите путь в вашем [файле settings.json](/ru/settings):

  ```json theme={null}
  {
    "env": {
      "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
    }
  }
  ```

Когда установлен Git for Windows, инструмент PowerShell развертывается постепенно как дополнительный вариант наряду с Bash. Установите `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` для включения или `0` для отключения. См. [инструмент PowerShell](/ru/tools-reference#powershell-tool) для настройки и ограничений.

**Вариант 2: WSL**

Откройте ваше распределение WSL и выполните установщик Linux из [инструкций установки](#install-claude-code) выше. Вы устанавливаете и запускаете `claude` внутри терминала WSL, а не из PowerShell или CMD.

### Alpine Linux и дистрибутивы на основе musl

Встроенный установщик на Alpine и других дистрибутивах на основе musl/uClibc требует `libgcc`, `libstdc++` и `ripgrep`. Установите их с помощью менеджера пакетов вашего дистрибутива, затем установите `USE_BUILTIN_RIPGREP=0`.

Этот пример устанавливает необходимые пакеты на Alpine:

```bash theme={null}
apk add libgcc libstdc++ ripgrep
```

Затем установите `USE_BUILTIN_RIPGREP` на `0` в файле [`settings.json`](/ru/settings#available-settings):

```json theme={null}
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

## Проверка установки

После установки убедитесь, что Claude Code работает:

```bash theme={null}
claude --version
```

Если это не сработает с ошибкой `command not found` или другой ошибкой, см. [Troubleshoot installation and login](/ru/troubleshoot-install).

Для более подробной проверки установки и конфигурации выполните [`claude doctor`](/ru/troubleshooting#get-more-help):

```bash theme={null}
claude doctor
```

## Аутентификация

Claude Code требует учетную запись Pro, Max, Team, Enterprise или Console. Бесплатный план Claude.ai не включает доступ к Claude Code. Вы также можете использовать Claude Code с поставщиком API третьей стороны, таким как [Amazon Bedrock](/ru/amazon-bedrock), [Google Vertex AI](/ru/google-vertex-ai) или [Microsoft Foundry](/ru/microsoft-foundry).

После установки войдите, выполнив `claude` и следуя подсказкам браузера. См. [Аутентификация](/ru/authentication) для всех типов учетных записей и параметров настройки команды.

## Обновление Claude Code

Встроенные установки автоматически обновляются в фоновом режиме. Вы можете [настроить канал выпуска](#configure-release-channel) для управления тем, получаете ли вы обновления немедленно или по отложенному стабильному расписанию, или [отключить автоматические обновления](#disable-auto-updates) полностью. Установки Homebrew, WinGet и [менеджер пакетов Linux](#install-with-linux-package-managers) требуют ручного обновления по умолчанию.

### Автоматические обновления

Claude Code проверяет наличие обновлений при запуске и периодически во время работы. Обновления загружаются и устанавливаются в фоновом режиме, а затем вступают в силу при следующем запуске Claude Code.

<Note>
  Установки Homebrew, WinGet, apt, dnf и apk не обновляются автоматически по умолчанию; см. ниже, чтобы согласиться для Homebrew и WinGet. Чтобы обновить Homebrew вручную, выполните `brew upgrade claude-code` или `brew upgrade claude-code@latest`, в зависимости от того, какой cask вы установили. Для WinGet выполните `winget upgrade Anthropic.ClaudeCode`. Для менеджеров пакетов Linux см. команды обновления в разделе [Install with Linux package managers](#install-with-linux-package-managers).

  Чтобы Claude Code выполнил команду обновления для вас на Homebrew или WinGet, установите [`CLAUDE_CODE_PACKAGE_MANAGER_AUTO_UPDATE`](/ru/env-vars) на `1`. Claude Code затем выполняет обновление в фоновом режиме, когда доступна новая версия, и показывает приглашение перезагрузки при успехе. Обновление затрагивает только пакет Claude Code и не влияет на другое программное обеспечение, которое вы установили.

  На WinGet обновление может не удаться, пока Claude Code работает, потому что Windows блокирует исполняемый файл. В этом случае Claude Code показывает команду ручного обновления вместо этого. apt, dnf и apk продолжают требовать ручного обновления, потому что эти команды требуют повышенных привилегий.

  **Известная проблема:** Claude Code может уведомить вас об обновлениях до того, как новая версия будет доступна в этих менеджерах пакетов. Если обновление не удается, подождите и повторите попытку позже.

  Homebrew сохраняет старые версии на диске после обновлений. Периодически выполняйте `brew cleanup` для освобождения дискового пространства.
</Note>

### Настройка канала выпуска

Управляйте каналом выпуска, который Claude Code использует для автоматических обновлений и `claude update`, с помощью параметра `autoUpdatesChannel`:

* `"latest"`, по умолчанию: получайте новые функции сразу же после их выпуска
* `"stable"`: используйте версию, которая обычно имеет возраст около одной недели, пропуская выпуски с серьезными регрессиями

Настройте это через `/config` → **Auto-update channel**, или добавьте в [файл settings.json](/ru/settings):

```json theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Для развертываний в масштабах предприятия вы можете обеспечить согласованный канал выпуска во всей организации, используя [управляемые параметры](/ru/permissions#managed-settings).

Установки Homebrew выбирают канал по имени cask вместо этого параметра: `claude-code` отслеживает стабильный и `claude-code@latest` отслеживает последний.

### Закрепление минимальной версии

Параметр `minimumVersion` устанавливает нижний предел. Фоновые автоматические обновления и `claude update` отказываются устанавливать любую версию ниже этого значения, поэтому переход на канал `"stable"` не понижает вас, если вы уже находитесь на более новой сборке `"latest"`.

Переключение с `"latest"` на `"stable"` через `/config` предлагает вам либо остаться на текущей версии, либо разрешить понижение. Выбор остаться устанавливает `minimumVersion` на эту версию. Переключение обратно на `"latest"` очищает его.

Добавьте его в [файл settings.json](/ru/settings) для явного закрепления нижнего предела:

```json theme={null}
{
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.100"
}
```

В [управляемых параметрах](/ru/permissions#managed-settings) это обеспечивает минимум на уровне организации, который параметры пользователя и проекта не могут переопределить.

### Отключение автоматических обновлений

Установите `DISABLE_AUTOUPDATER` на `"1"` в ключе `env` файла [`settings.json`](/ru/settings#available-settings):

```json theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

`DISABLE_AUTOUPDATER` только останавливает фоновую проверку; `claude update` и `claude install` по-прежнему работают. Чтобы заблокировать все пути обновления, включая ручные обновления, установите [`DISABLE_UPDATES`](/ru/env-vars) вместо этого. Используйте это, когда вы распространяете Claude Code через свои собственные каналы и вам нужно, чтобы пользователи оставались на версии, которую вы предоставляете.

### Ручное обновление

Чтобы применить обновление немедленно без ожидания следующей проверки в фоновом режиме, выполните:

```bash theme={null}
claude update
```

## Расширенные параметры установки

Эти параметры предназначены для закрепления версии, менеджеров пакетов Linux, npm и проверки целостности двоичного файла.

### Установка определенной версии

Встроенный установщик принимает либо конкретный номер версии, либо канал выпуска (`latest` или `stable`). Канал, который вы выбираете во время установки, становится вашим значением по умолчанию для автоматических обновлений. См. [настройка канала выпуска](#configure-release-channel) для получения дополнительной информации.

Для установки последней версии (по умолчанию):

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
  </Tab>
</Tabs>

Для установки стабильной версии:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s stable
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
    ```
  </Tab>
</Tabs>

Для установки определенного номера версии:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s 2.1.89
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 2.1.89
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 2.1.89 && del install.cmd
    ```
  </Tab>
</Tabs>

### Установка с менеджерами пакетов Linux

Claude Code публикует подписанные репозитории apt, dnf и apk. Замените `stable` на `latest` для канала rolling. Установки менеджеров пакетов не обновляются автоматически через Claude Code; обновления поступают через ваш обычный рабочий процесс обновления системы.

Все репозитории подписаны с помощью [ключа подписи выпуска Claude Code](#binary-integrity-and-code-signing). Перед доверием к ключу проверьте его, как описано в каждой вкладке.

<Tabs>
  <Tab title="apt">
    Для Debian и Ubuntu. Чтобы использовать канал rolling, измените оба вхождения `stable` в строке `deb`: путь URL и имя suite.

    ```bash theme={null}
    sudo install -d -m 0755 /etc/apt/keyrings
    sudo curl -fsSL https://downloads.claude.ai/keys/claude-code.asc \
      -o /etc/apt/keyrings/claude-code.asc
    echo "deb [signed-by=/etc/apt/keyrings/claude-code.asc] https://downloads.claude.ai/claude-code/apt/stable stable main" \
      | sudo tee /etc/apt/sources.list.d/claude-code.list
    sudo apt update
    sudo apt install claude-code
    ```

    Проверьте отпечаток ключа GPG перед доверием к нему: `gpg --show-keys /etc/apt/keyrings/claude-code.asc` должен сообщить `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE`.

    Для обновления позже выполните `sudo apt update && sudo apt upgrade claude-code`.
  </Tab>

  <Tab title="dnf">
    Для Fedora и RHEL:

    ```bash theme={null}
    sudo tee /etc/yum.repos.d/claude-code.repo <<'EOF'
    [claude-code]
    name=Claude Code
    baseurl=https://downloads.claude.ai/claude-code/rpm/stable
    enabled=1
    gpgcheck=1
    gpgkey=https://downloads.claude.ai/keys/claude-code.asc
    EOF
    sudo dnf install claude-code
    ```

    dnf загружает ключ при первой установке и предлагает вам подтвердить отпечаток. Проверьте, что он совпадает с `31DD DE24 DDFA B679 F42D 7BD2 BAA9 29FF 1A7E CACE` перед принятием.

    Для обновления позже выполните `sudo dnf upgrade claude-code`.
  </Tab>

  <Tab title="apk">
    Для Alpine Linux:

    ```sh theme={null}
    wget -O /etc/apk/keys/claude-code.rsa.pub \
      https://downloads.claude.ai/keys/claude-code.rsa.pub
    echo "https://downloads.claude.ai/claude-code/apk/stable" >> /etc/apk/repositories
    apk add claude-code
    ```

    Проверьте загруженный ключ с помощью `sha256sum /etc/apk/keys/claude-code.rsa.pub`, который должен сообщить `395759c1f7449ef4cdef305a42e820f3c766d6090d142634ebdb049f113168b6`.

    Для обновления позже выполните `apk update && apk upgrade claude-code`.
  </Tab>
</Tabs>

### Установка с npm

Вы также можете установить Claude Code как глобальный пакет npm. Пакет требует [Node.js 18 или позже](https://nodejs.org/en/download).

```bash theme={null}
npm install -g @anthropic-ai/claude-code
```

Пакет npm устанавливает тот же встроенный двоичный файл, что и автономный установщик. npm получает двоичный файл через дополнительную зависимость для каждой платформы, такую как `@anthropic-ai/claude-code-darwin-arm64`, и шаг postinstall связывает его на место. Установленный двоичный файл `claude` сам по себе не вызывает Node.

Поддерживаемые платформы установки npm: `darwin-arm64`, `darwin-x64`, `linux-x64`, `linux-arm64`, `linux-x64-musl`, `linux-arm64-musl`, `win32-x64` и `win32-arm64`. Ваш менеджер пакетов должен разрешать дополнительные зависимости. См. [устранение неполадок](/ru/troubleshoot-install#native-binary-not-found-after-npm-install), если двоичный файл отсутствует после установки.

Для обновления установки npm выполните `npm install -g @anthropic-ai/claude-code@latest`. Избегайте `npm update -g`, который соблюдает диапазон semver из исходной установки и может не переместить вас на самый новый выпуск.

<Warning>
  НЕ используйте `sudo npm install -g`, так как это может привести к проблемам с разрешениями и рискам безопасности. Если вы столкнулись с ошибками разрешений, см. [устранение неполадок ошибок разрешений](/ru/troubleshoot-install#permission-errors-during-installation).
</Warning>

### Целостность двоичного файла и подпись кода

Каждый выпуск публикует `manifest.json`, содержащий контрольные суммы SHA256 для каждого двоичного файла платформы. Манифест подписан ключом GPG Anthropic, поэтому проверка подписи на манифесте транзитивно проверяет каждый двоичный файл, который он указывает.

#### Проверка подписи манифеста

Шаги 1-3 требуют оболочки POSIX с `gpg` и `curl`. В Windows выполните их в Git Bash или WSL. Шаг 4 включает опцию PowerShell.

<Steps>
  <Step title="Загрузка и импорт открытого ключа">
    Ключ подписи выпуска опубликован по фиксированному URL.

    ```bash theme={null}
    curl -fsSL https://downloads.claude.ai/keys/claude-code.asc | gpg --import
    ```

    Отобразите отпечаток импортированного ключа.

    ```bash theme={null}
    gpg --fingerprint security@anthropic.com
    ```

    Подтвердите, что вывод включает этот отпечаток:

    ```text theme={null}
    31DD DE24 DDFA B679 F42D  7BD2 BAA9 29FF 1A7E CACE
    ```
  </Step>

  <Step title="Загрузка манифеста и подписи">
    Установите `VERSION` на выпуск, который вы хотите проверить.

    ```bash theme={null}
    REPO=https://downloads.claude.ai/claude-code-releases
    VERSION=2.1.89
    curl -fsSLO "$REPO/$VERSION/manifest.json"
    curl -fsSLO "$REPO/$VERSION/manifest.json.sig"
    ```
  </Step>

  <Step title="Проверка подписи">
    Проверьте отделенную подпись против манифеста.

    ```bash theme={null}
    gpg --verify manifest.json.sig manifest.json
    ```

    Действительный результат сообщает `Good signature from "Anthropic Claude Code Release Signing <security@anthropic.com>"`.

    `gpg` также выводит `WARNING: This key is not certified with a trusted signature!` для любого вновь импортированного ключа. Это ожидается. Строка `Good signature` подтверждает, что криптографическая проверка прошла. Сравнение отпечатков на шаге 1 подтверждает, что сам ключ является подлинным.
  </Step>

  <Step title="Проверка двоичного файла против манифеста">
    Сравните контрольную сумму SHA256 вашего загруженного двоичного файла со значением, указанным в `platforms.<platform>.checksum` в `manifest.json`.

    <Tabs>
      <Tab title="Linux">
        ```bash theme={null}
        sha256sum claude
        ```
      </Tab>

      <Tab title="macOS">
        ```bash theme={null}
        shasum -a 256 claude
        ```
      </Tab>

      <Tab title="Windows PowerShell">
        ```powershell theme={null}
        (Get-FileHash claude.exe -Algorithm SHA256).Hash.ToLower()
        ```
      </Tab>
    </Tabs>
  </Step>
</Steps>

<Note>
  Подписи манифеста доступны для выпусков начиная с `2.1.89`. Более ранние выпуски публикуют контрольные суммы в `manifest.json` без отделенной подписи.
</Note>

#### Подписи кода платформы

В дополнение к подписанному манифесту отдельные двоичные файлы несут подписи кода, специфичные для платформы, где это поддерживается.

* **macOS**: подписано "Anthropic PBC" и заверено Apple. Проверьте с помощью `codesign --verify --verbose ./claude`.
* **Windows**: подписано "Anthropic, PBC". Проверьте с помощью `Get-AuthenticodeSignature .\claude.exe`.
* **Linux**: двоичные файлы не подписаны индивидуально кодом. Если вы загружаете непосредственно из корзины `claude-code-releases` или используете встроенный установщик, проверьте целостность с помощью подписи манифеста выше. Если вы устанавливаете с помощью [apt, dnf или apk](#install-with-linux-package-managers), ваш менеджер пакетов автоматически проверяет подписи, используя ключ подписи репозитория.

## Удаление Claude Code

Чтобы удалить Claude Code, следуйте инструкциям для вашего метода установки. Если `claude` все еще работает после этого, у вас, вероятно, есть вторая установка или оставшийся псевдоним оболочки из старого установщика. См. [Проверка конфликтующих установок](/ru/troubleshoot-install#check-for-conflicting-installations), чтобы найти и удалить его.

### Встроенная установка

Удалите двоичный файл Claude Code и файлы версии:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    rm -f ~/.local/bin/claude
    rm -rf ~/.local/share/claude
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
    Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
    ```
  </Tab>
</Tabs>

### Установка Homebrew

Удалите cask Homebrew, который вы установили. Если вы установили стабильный cask:

```bash theme={null}
brew uninstall --cask claude-code
```

Если вы установили последний cask:

```bash theme={null}
brew uninstall --cask claude-code@latest
```

### Установка WinGet

Удалите пакет WinGet:

```powershell theme={null}
winget uninstall Anthropic.ClaudeCode
```

### apt / dnf / apk

Удалите пакет и конфигурацию репозитория:

<Tabs>
  <Tab title="apt">
    ```bash theme={null}
    sudo apt remove claude-code
    sudo rm /etc/apt/sources.list.d/claude-code.list /etc/apt/keyrings/claude-code.asc
    ```
  </Tab>

  <Tab title="dnf">
    ```bash theme={null}
    sudo dnf remove claude-code
    sudo rm /etc/yum.repos.d/claude-code.repo
    ```
  </Tab>

  <Tab title="apk">
    ```sh theme={null}
    apk del claude-code
    sed -i '\|downloads.claude.ai/claude-code/apk|d' /etc/apk/repositories
    rm /etc/apk/keys/claude-code.rsa.pub
    ```
  </Tab>
</Tabs>

### npm

Удалите глобальный пакет npm:

```bash theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Удаление файлов конфигурации

<Warning>
  Удаление файлов конфигурации удалит все ваши параметры, разрешенные инструменты, конфигурации MCP server и историю сеансов.
</Warning>

Расширение VS Code, плагин JetBrains и приложение Desktop также записывают в `~/.claude/`. Если какое-либо из них все еще установлено, каталог будет пересоздан при следующем запуске. Чтобы полностью удалить Claude Code, удалите [расширение VS Code](/ru/vs-code#uninstall-the-extension), плагин JetBrains и приложение Desktop перед удалением этих файлов.

Чтобы удалить параметры Claude Code и кэшированные данные:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    # Удаление пользовательских параметров и состояния
    rm -rf ~/.claude
    rm ~/.claude.json

    # Удаление параметров для конкретного проекта (выполните из каталога вашего проекта)
    rm -rf .claude
    rm -f .mcp.json
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    # Удаление пользовательских параметров и состояния
    Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
    Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

    # Удаление параметров для конкретного проекта (выполните из каталога вашего проекта)
    Remove-Item -Path ".claude" -Recurse -Force
    Remove-Item -Path ".mcp.json" -Force
    ```
  </Tab>
</Tabs>
