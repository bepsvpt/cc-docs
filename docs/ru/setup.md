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
* **Оборудование**: 4 ГБ+ ОЗУ
* **Сеть**: требуется подключение в Интернет. См. [конфигурация сети](/ru/network-config#network-access-requirements).
* **Shell**: Bash, Zsh, PowerShell или CMD. В Windows требуется [Git for Windows](https://git-scm.com/downloads/win).
* **Местоположение**: [поддерживаемые Anthropic страны](https://www.anthropic.com/supported-countries)

### Дополнительные зависимости

* **ripgrep**: обычно включен в Claude Code. Если поиск не работает, см. [устранение неполадок поиска](/ru/troubleshooting#search-and-discovery-issues).

## Установка Claude Code

<Tip>
  Предпочитаете графический интерфейс? [Приложение Desktop](/ru/desktop-quickstart) позволяет использовать Claude Code без терминала. Загрузите его для [macOS](https://claude.ai/api/desktop/darwin/universal/dmg/latest/redirect?utm_source=claude_code\&utm_medium=docs) или [Windows](https://claude.ai/api/desktop/win32/x64/exe/latest/redirect?utm_source=claude_code\&utm_medium=docs).

  Новичок в терминале? См. [руководство по терминалу](/ru/terminal-guide) для пошаговых инструкций.
</Tip>

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

    If you see `The token '&&' is not a valid statement separator`, you're in PowerShell, not CMD. Use the PowerShell command above instead. Your prompt shows `PS C:\` when you're in PowerShell.

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

После завершения установки откройте терминал в проекте, над которым вы хотите работать, и запустите Claude Code:

```bash  theme={null}
claude
```

Если вы столкнулись с какими-либо проблемами во время установки, см. [руководство по устранению неполадок](/ru/troubleshooting).

### Настройка в Windows

Claude Code в Windows требует [Git for Windows](https://git-scm.com/downloads/win) или WSL. Вы можете запустить `claude` из PowerShell, CMD или Git Bash. Claude Code использует Git Bash внутри для выполнения команд. Вам не нужно запускать PowerShell от имени администратора.

**Вариант 1: Native Windows с Git Bash**

Установите [Git for Windows](https://git-scm.com/downloads/win), затем выполните команду установки из PowerShell или CMD.

Если Claude Code не может найти вашу установку Git Bash, установите путь в [файле settings.json](/ru/settings):

```json  theme={null}
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

**Вариант 2: WSL**

Поддерживаются как WSL 1, так и WSL 2. WSL 2 поддерживает [sandboxing](/ru/sandboxing) для повышенной безопасности. WSL 1 не поддерживает sandboxing.

### Alpine Linux и дистрибутивы на основе musl

Встроенный установщик на Alpine и других дистрибутивах на основе musl/uClibc требует `libgcc`, `libstdc++` и `ripgrep`. Установите их с помощью менеджера пакетов вашего дистрибутива, затем установите `USE_BUILTIN_RIPGREP=0`.

Этот пример устанавливает необходимые пакеты на Alpine:

```bash  theme={null}
apk add libgcc libstdc++ ripgrep
```

Затем установите `USE_BUILTIN_RIPGREP` на `0` в файле [`settings.json`](/ru/settings#available-settings):

```json  theme={null}
{
  "env": {
    "USE_BUILTIN_RIPGREP": "0"
  }
}
```

## Проверка установки

После установки убедитесь, что Claude Code работает:

```bash  theme={null}
claude --version
```

Для более подробной проверки установки и конфигурации выполните [`claude doctor`](/ru/troubleshooting#get-more-help):

```bash  theme={null}
claude doctor
```

## Аутентификация

Claude Code требует учетную запись Pro, Max, Teams, Enterprise или Console. Бесплатный план Claude.ai не включает доступ к Claude Code. Вы также можете использовать Claude Code с поставщиком API третьей стороны, таким как [Amazon Bedrock](/ru/amazon-bedrock), [Google Vertex AI](/ru/google-vertex-ai) или [Microsoft Foundry](/ru/microsoft-foundry).

После установки войдите, выполнив `claude` и следуя подсказкам браузера. См. [Аутентификация](/ru/authentication) для всех типов учетных записей и параметров настройки команды.

## Обновление Claude Code

Встроенные установки автоматически обновляются в фоновом режиме. Вы можете [настроить канал выпуска](#configure-release-channel) для управления тем, получаете ли вы обновления немедленно или по отложенному стабильному расписанию, или [отключить автоматические обновления](#disable-auto-updates) полностью. Установки Homebrew и WinGet требуют ручного обновления.

### Автоматические обновления

Claude Code проверяет наличие обновлений при запуске и периодически во время работы. Обновления загружаются и устанавливаются в фоновом режиме, а затем вступают в силу при следующем запуске Claude Code.

<Note>
  Установки Homebrew и WinGet не обновляются автоматически. Используйте `brew upgrade claude-code` или `winget upgrade Anthropic.ClaudeCode` для ручного обновления.

  **Известная проблема:** Claude Code может уведомить вас об обновлениях до того, как новая версия будет доступна в этих менеджерах пакетов. Если обновление не удается, подождите и повторите попытку позже.

  Homebrew сохраняет старые версии на диске после обновлений. Периодически выполняйте `brew cleanup claude-code` для освобождения дискового пространства.
</Note>

### Настройка канала выпуска

Управляйте каналом выпуска, который Claude Code использует для автоматических обновлений и `claude update`, с помощью параметра `autoUpdatesChannel`:

* `"latest"`, по умолчанию: получайте новые функции сразу же после их выпуска
* `"stable"`: используйте версию, которая обычно имеет возраст около одной недели, пропуская выпуски с серьезными регрессиями

Настройте это через `/config` → **Auto-update channel**, или добавьте в [файл settings.json](/ru/settings):

```json  theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

Для развертываний в масштабах предприятия вы можете обеспечить согласованный канал выпуска во всей организации, используя [управляемые параметры](/ru/permissions#managed-settings).

### Отключение автоматических обновлений

Установите `DISABLE_AUTOUPDATER` на `"1"` в ключе `env` файла [`settings.json`](/ru/settings#available-settings):

```json  theme={null}
{
  "env": {
    "DISABLE_AUTOUPDATER": "1"
  }
}
```

### Ручное обновление

Чтобы применить обновление немедленно без ожидания следующей проверки в фоновом режиме, выполните:

```bash  theme={null}
claude update
```

## Расширенные параметры установки

Эти параметры предназначены для закрепления версии, миграции с npm и проверки целостности двоичного файла.

### Установка определенной версии

Встроенный установщик принимает либо конкретный номер версии, либо канал выпуска (`latest` или `stable`). Канал, который вы выбираете во время установки, становится вашим значением по умолчанию для автоматических обновлений. См. [настройка канала выпуска](#configure-release-channel) для получения дополнительной информации.

Для установки последней версии (по умолчанию):

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    irm https://claude.ai/install.ps1 | iex
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd && del install.cmd
    ```
  </Tab>
</Tabs>

Для установки стабильной версии:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s stable
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) stable
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd stable && del install.cmd
    ```
  </Tab>
</Tabs>

Для установки определенного номера версии:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    curl -fsSL https://claude.ai/install.sh | bash -s 1.0.58
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    & ([scriptblock]::Create((irm https://claude.ai/install.ps1))) 1.0.58
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch  theme={null}
    curl -fsSL https://claude.ai/install.cmd -o install.cmd && install.cmd 1.0.58 && del install.cmd
    ```
  </Tab>
</Tabs>

### Устаревшая установка npm

Установка npm устарела. Встроенный установщик быстрее, не требует зависимостей и автоматически обновляется в фоновом режиме. По возможности используйте метод [встроенной установки](#install-claude-code).

#### Миграция с npm на встроенный установщик

Если вы ранее установили Claude Code с помощью npm, переключитесь на встроенный установщик:

```bash  theme={null}
# Установка встроенного двоичного файла
curl -fsSL https://claude.ai/install.sh | bash

# Удаление старой установки npm
npm uninstall -g @anthropic-ai/claude-code
```

Вы также можете выполнить `claude install` из существующей установки npm для установки встроенного двоичного файла рядом с ней, а затем удалить версию npm.

#### Установка с npm

Если вам нужна установка npm по причинам совместимости, у вас должен быть установлен [Node.js 18+](https://nodejs.org/en/download). Установите пакет глобально:

```bash  theme={null}
npm install -g @anthropic-ai/claude-code
```

<Warning>
  НЕ используйте `sudo npm install -g`, так как это может привести к проблемам с разрешениями и рискам безопасности. Если вы столкнулись с ошибками разрешений, см. [устранение неполадок ошибок разрешений](/ru/troubleshooting#permission-errors-during-installation).
</Warning>

### Целостность двоичного файла и подпись кода

Вы можете проверить целостность двоичных файлов Claude Code, используя контрольные суммы SHA256 и подписи кода.

* Контрольные суммы SHA256 для всех платформ опубликованы в манифестах выпуска по адресу `https://storage.googleapis.com/claude-code-dist-86c565f3-f756-42ad-8dfa-d59b1c096819/claude-code-releases/{VERSION}/manifest.json`. Замените `{VERSION}` номером версии, например `2.0.30`.
* Подписанные двоичные файлы распространяются для следующих платформ:
  * **macOS**: подписано "Anthropic PBC" и заверено Apple
  * **Windows**: подписано "Anthropic, PBC"

## Удаление Claude Code

Чтобы удалить Claude Code, следуйте инструкциям для вашего метода установки.

### Встроенная установка

Удалите двоичный файл Claude Code и файлы версии:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    rm -f ~/.local/bin/claude
    rm -rf ~/.local/share/claude
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    Remove-Item -Path "$env:USERPROFILE\.local\bin\claude.exe" -Force
    Remove-Item -Path "$env:USERPROFILE\.local\share\claude" -Recurse -Force
    ```
  </Tab>
</Tabs>

### Установка Homebrew

Удалите cask Homebrew:

```bash  theme={null}
brew uninstall --cask claude-code
```

### Установка WinGet

Удалите пакет WinGet:

```powershell  theme={null}
winget uninstall Anthropic.ClaudeCode
```

### npm

Удалите глобальный пакет npm:

```bash  theme={null}
npm uninstall -g @anthropic-ai/claude-code
```

### Удаление файлов конфигурации

<Warning>
  Удаление файлов конфигурации удалит все ваши параметры, разрешенные инструменты, конфигурации MCP servers и историю сеансов.
</Warning>

Чтобы удалить параметры Claude Code и кэшированные данные:

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash  theme={null}
    # Удаление пользовательских параметров и состояния
    rm -rf ~/.claude
    rm ~/.claude.json

    # Удаление параметров для конкретного проекта (выполните из каталога вашего проекта)
    rm -rf .claude
    rm -f .mcp.json
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell  theme={null}
    # Удаление пользовательских параметров и состояния
    Remove-Item -Path "$env:USERPROFILE\.claude" -Recurse -Force
    Remove-Item -Path "$env:USERPROFILE\.claude.json" -Force

    # Удаление параметров для конкретного проекта (выполните из каталога вашего проекта)
    Remove-Item -Path ".claude" -Recurse -Force
    Remove-Item -Path ".mcp.json" -Force
    ```
  </Tab>
</Tabs>
