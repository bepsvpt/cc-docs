> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Подключите Claude Code к инструментам через MCP

> Узнайте, как подключить Claude Code к вашим инструментам с помощью Model Context Protocol.

export const MCPServersTable = ({platform = "all"}) => {
  const ifYouAreAnAiAgentReadingThisYouShouldInsteadFetch = 'https://api.anthropic.com/mcp-registry/docs';
  const [servers, setServers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  useEffect(() => {
    const fetchServers = async () => {
      try {
        setLoading(true);
        const allServers = [];
        let cursor = null;
        do {
          const url = new URL('https://api.anthropic.com/mcp-registry/v0/servers');
          url.searchParams.set('version', 'latest');
          url.searchParams.set('visibility', 'commercial');
          url.searchParams.set('limit', '100');
          if (cursor) {
            url.searchParams.set('cursor', cursor);
          }
          const response = await fetch(url);
          if (!response.ok) {
            throw new Error(`Failed to fetch MCP registry: ${response.status}`);
          }
          const data = await response.json();
          allServers.push(...data.servers);
          cursor = data.metadata?.nextCursor || null;
        } while (cursor);
        const transformedServers = allServers.map(item => {
          const server = item.server;
          const meta = item._meta?.['com.anthropic.api/mcp-registry'] || ({});
          const worksWith = meta.worksWith || [];
          const availability = {
            claudeCode: worksWith.includes('claude-code'),
            mcpConnector: worksWith.includes('claude-api'),
            claudeDesktop: worksWith.includes('claude-desktop')
          };
          const remotes = server.remotes || [];
          const httpRemote = remotes.find(r => r.type === 'streamable-http');
          const sseRemote = remotes.find(r => r.type === 'sse');
          const preferredRemote = httpRemote || sseRemote;
          const remoteUrl = preferredRemote?.url || meta.url;
          const remoteType = preferredRemote?.type;
          const isTemplatedUrl = remoteUrl?.includes('{');
          let setupUrl;
          if (isTemplatedUrl && meta.requiredFields) {
            const urlField = meta.requiredFields.find(f => f.field === 'url');
            setupUrl = urlField?.sourceUrl || meta.documentation;
          }
          const urls = {};
          if (!isTemplatedUrl) {
            if (remoteType === 'streamable-http') {
              urls.http = remoteUrl;
            } else if (remoteType === 'sse') {
              urls.sse = remoteUrl;
            }
          }
          let envVars = [];
          if (server.packages && server.packages.length > 0) {
            const npmPackage = server.packages.find(p => p.registryType === 'npm');
            if (npmPackage) {
              urls.stdio = `npx -y ${npmPackage.identifier}`;
              if (npmPackage.environmentVariables) {
                envVars = npmPackage.environmentVariables;
              }
            }
          }
          return {
            name: meta.displayName || server.title || server.name,
            description: meta.oneLiner || server.description,
            documentation: meta.documentation,
            urls: urls,
            envVars: envVars,
            availability: availability,
            customCommands: meta.claudeCodeCopyText ? {
              claudeCode: meta.claudeCodeCopyText
            } : undefined,
            setupUrl: setupUrl
          };
        });
        setServers(transformedServers);
        setError(null);
      } catch (err) {
        setError(err.message);
        console.error('Error fetching MCP registry:', err);
      } finally {
        setLoading(false);
      }
    };
    fetchServers();
  }, []);
  const generateClaudeCodeCommand = server => {
    if (server.customCommands && server.customCommands.claudeCode) {
      return server.customCommands.claudeCode.replace('--transport streamable-http', '--transport http');
    }
    const serverSlug = server.name.toLowerCase().replace(/[^a-z0-9]/g, '-');
    if (server.urls.http) {
      return `claude mcp add ${serverSlug} --transport http ${server.urls.http}`;
    }
    if (server.urls.sse) {
      return `claude mcp add ${serverSlug} --transport sse ${server.urls.sse}`;
    }
    if (server.urls.stdio) {
      const envFlags = server.envVars && server.envVars.length > 0 ? server.envVars.map(v => `--env ${v.name}=YOUR_${v.name}`).join(' ') : '';
      const baseCommand = `claude mcp add ${serverSlug} --transport stdio`;
      return envFlags ? `${baseCommand} ${envFlags} -- ${server.urls.stdio}` : `${baseCommand} -- ${server.urls.stdio}`;
    }
    return null;
  };
  if (loading) {
    return <div>Loading MCP servers...</div>;
  }
  if (error) {
    return <div>Error loading MCP servers: {error}</div>;
  }
  const filteredServers = servers.filter(server => {
    if (platform === "claudeCode") {
      return server.availability.claudeCode;
    } else if (platform === "mcpConnector") {
      return server.availability.mcpConnector;
    } else if (platform === "claudeDesktop") {
      return server.availability.claudeDesktop;
    } else if (platform === "all") {
      return true;
    } else {
      throw new Error(`Unknown platform: ${platform}`);
    }
  });
  return <>
      <style jsx>{`
        .cards-container {
          display: grid;
          gap: 1rem;
          margin-bottom: 2rem;
        }
        .server-card {
          border: 1px solid var(--border-color, #e5e7eb);
          border-radius: 6px;
          padding: 1rem;
        }
        .command-row {
          display: flex;
          align-items: center;
          gap: 0.25rem;
        }
        .command-row code {
          font-size: 0.75rem;
          overflow-x: auto;
        }
      `}</style>

      <div className="cards-container">
        {filteredServers.map(server => {
    const claudeCodeCommand = generateClaudeCodeCommand(server);
    const mcpUrl = server.urls.http || server.urls.sse;
    const commandToShow = platform === "claudeCode" ? claudeCodeCommand : mcpUrl;
    return <div key={server.name} className="server-card">
              <div>
                {server.documentation ? <a href={server.documentation}>
                    <strong>{server.name}</strong>
                  </a> : <strong>{server.name}</strong>}
              </div>

              <p style={{
      margin: '0.5rem 0',
      fontSize: '0.9rem'
    }}>
                {server.description}
              </p>

              {server.setupUrl && <p style={{
      margin: '0.25rem 0',
      fontSize: '0.8rem',
      fontStyle: 'italic',
      opacity: 0.7
    }}>
                  Requires user-specific URL.{' '}
                  <a href={server.setupUrl} style={{
      textDecoration: 'underline'
    }}>
                    Get your URL here
                  </a>.
                </p>}

              {commandToShow && !server.setupUrl && <>
                <p style={{
      display: 'block',
      fontSize: '0.75rem',
      fontWeight: 500,
      minWidth: 'fit-content',
      marginTop: '0.5rem',
      marginBottom: 0
    }}>
                  {platform === "claudeCode" ? "Command" : "URL"}
                </p>
                <div className="command-row">
                  <code>
                    {commandToShow}
                  </code>
                </div>
              </>}
            </div>;
  })}
      </div>
    </>;
};

Claude Code может подключаться к сотням внешних инструментов и источников данных через [Model Context Protocol (MCP)](https://modelcontextprotocol.io/introduction), открытый стандарт для интеграции AI с инструментами. MCP servers предоставляют Claude Code доступ к вашим инструментам, базам данных и API.

## Что вы можете делать с MCP

С подключенными MCP servers вы можете попросить Claude Code:

* **Реализовать функции из трекеров проблем**: "Добавьте функцию, описанную в задаче JIRA ENG-4521, и создайте PR на GitHub."
* **Анализировать данные мониторинга**: "Проверьте Sentry и Statsig, чтобы проверить использование функции, описанной в ENG-4521."
* **Запрашивать базы данных**: "Найдите адреса электронной почты 10 случайных пользователей, которые использовали функцию ENG-4521, на основе нашей базы данных PostgreSQL."
* **Интегрировать дизайны**: "Обновите наш стандартный шаблон электронного письма на основе новых дизайнов Figma, которые были опубликованы в Slack"
* **Автоматизировать рабочие процессы**: "Создайте черновики Gmail, приглашающие этих 10 пользователей на сеанс обратной связи о новой функции."
* **Реагировать на внешние события**: MCP server также может действовать как [канал](/ru/channels), который отправляет сообщения в вашу сессию, поэтому Claude реагирует на сообщения Telegram, чаты Discord или события webhook, пока вас нет.

## Популярные MCP servers

Вот некоторые часто используемые MCP servers, которые вы можете подключить к Claude Code:

<Warning>
  Используйте сторонние MCP servers на свой риск - Anthropic не проверил
  корректность или безопасность всех этих servers.
  Убедитесь, что вы доверяете MCP servers, которые устанавливаете.
  Будьте особенно осторожны при использовании MCP servers, которые могут получать ненадежный
  контент, так как это может подвергнуть вас риску prompt injection.
</Warning>

<MCPServersTable platform="claudeCode" />

<Note>
  **Нужна конкретная интеграция?** [Найдите сотни других MCP servers на GitHub](https://github.com/modelcontextprotocol/servers), или создайте свой собственный, используя [MCP SDK](https://modelcontextprotocol.io/quickstart/server).
</Note>

## Установка MCP servers

MCP servers можно настроить тремя различными способами в зависимости от ваших потребностей:

### Вариант 1: Добавьте удаленный HTTP server

HTTP servers — это рекомендуемый вариант для подключения к удаленным MCP servers. Это наиболее широко поддерживаемый транспорт для облачных сервисов.

```bash theme={null}
# Базовый синтаксис
claude mcp add --transport http <name> <url>

# Реальный пример: подключение к Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# Пример с токеном Bearer
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### Вариант 2: Добавьте удаленный SSE server

<Warning>
  Транспорт SSE (Server-Sent Events) устарел. Используйте вместо этого HTTP servers, где они доступны.
</Warning>

```bash theme={null}
# Базовый синтаксис
claude mcp add --transport sse <name> <url>

# Реальный пример: подключение к Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse

# Пример с заголовком аутентификации
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: your-key-here"
```

### Вариант 3: Добавьте локальный stdio server

Stdio servers работают как локальные процессы на вашей машине. Они идеальны для инструментов, которым требуется прямой доступ к системе или пользовательские скрипты.

```bash theme={null}
# Базовый синтаксис
claude mcp add [options] <name> -- <command> [args...]

# Реальный пример: добавление Airtable server
claude mcp add --transport stdio --env AIRTABLE_API_KEY=YOUR_KEY airtable \
  -- npx -y airtable-mcp-server
```

<Note>
  **Важно: порядок опций**

  Все опции (`--transport`, `--env`, `--scope`, `--header`) должны идти **перед** именем server. Затем `--` (двойной дефис) отделяет имя server от команды и аргументов, которые передаются MCP server.

  Например:

  * `claude mcp add --transport stdio myserver -- npx server` → запускает `npx server`
  * `claude mcp add --transport stdio --env KEY=value myserver -- python server.py --port 8080` → запускает `python server.py --port 8080` с `KEY=value` в окружении

  Это предотвращает конфликты между флагами Claude и флагами server.
</Note>

### Управление вашими servers

После настройки вы можете управлять своими MCP servers с помощью этих команд:

```bash theme={null}
# Список всех настроенных servers
claude mcp list

# Получить детали для конкретного server
claude mcp get github

# Удалить server
claude mcp remove github

# (в Claude Code) Проверить статус server
/mcp
```

### Динамические обновления инструментов

Claude Code поддерживает MCP `list_changed` уведомления, позволяя MCP servers динамически обновлять свои доступные инструменты, подсказки и ресурсы без необходимости отключения и переподключения. Когда MCP server отправляет уведомление `list_changed`, Claude Code автоматически обновляет доступные возможности от этого server.

### Отправка сообщений через каналы

MCP server также может отправлять сообщения непосредственно в вашу сессию, чтобы Claude мог реагировать на внешние события, такие как результаты CI, оповещения мониторинга или сообщения чата. Чтобы включить это, ваш server объявляет возможность `claude/channel` и вы включаете ее с флагом `--channels` при запуске. См. [Каналы](/ru/channels) для использования официально поддерживаемого канала или [Справочник каналов](/ru/channels-reference) для создания собственного.

<Tip>
  Советы:

  * Используйте флаг `--scope` для указания места хранения конфигурации:
    * `local` (по умолчанию): доступно только вам в текущем проекте (в старых версиях называлось `project`)
    * `project`: общий доступ для всех в проекте через файл `.mcp.json`
    * `user`: доступно вам во всех проектах (в старых версиях называлось `global`)
  * Установите переменные окружения с флагами `--env` (например, `--env KEY=value`)
  * Настройте timeout запуска MCP server, используя переменную окружения MCP\_TIMEOUT (например, `MCP_TIMEOUT=10000 claude` устанавливает timeout в 10 секунд)
  * Claude Code отобразит предупреждение, когда выход инструмента MCP превышает 10 000 токенов. Чтобы увеличить этот лимит, установите переменную окружения `MAX_MCP_OUTPUT_TOKENS` (например, `MAX_MCP_OUTPUT_TOKENS=50000`)
  * Используйте `/mcp` для аутентификации с удаленными servers, которые требуют аутентификацию OAuth 2.0
</Tip>

<Warning>
  **Пользователи Windows**: на нативной Windows (не WSL) локальные MCP servers, которые используют `npx`, требуют обертки `cmd /c` для обеспечения правильного выполнения.

  ```bash theme={null}
  # Это создает command="cmd", который Windows может выполнить
  claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
  ```

  Без обертки `cmd /c` вы столкнетесь с ошибками "Connection closed", потому что Windows не может напрямую выполнить `npx`. (См. примечание выше для объяснения параметра `--`.)
</Warning>

### MCP servers, предоставляемые плагинами

[Плагины](/ru/plugins) могут включать MCP servers, автоматически предоставляя инструменты и интеграции при включении плагина. Plugin MCP servers работают идентично пользовательским настроенным servers.

**Как работают plugin MCP servers**:

* Плагины определяют MCP servers в `.mcp.json` в корне плагина или встроенные в `plugin.json`
* Когда плагин включен, его MCP servers запускаются автоматически
* Plugin MCP tools отображаются рядом с вручную настроенными MCP tools
* Plugin servers управляются через установку плагина (не через команды `/mcp`)

**Пример конфигурации plugin MCP**:

В `.mcp.json` в корне плагина:

```json theme={null}
{
  "mcpServers": {
    "database-tools": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_URL": "${DB_URL}"
      }
    }
  }
}
```

Или встроенные в `plugin.json`:

```json theme={null}
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

**Функции plugin MCP**:

* **Автоматический жизненный цикл**: При запуске сеанса servers для включенных плагинов подключаются автоматически. Если вы включите или отключите плагин во время сеанса, запустите `/reload-plugins` для подключения или отключения его MCP servers
* **Переменные окружения**: используйте `${CLAUDE_PLUGIN_ROOT}` для файлов плагина и `${CLAUDE_PLUGIN_DATA}` для [постоянного состояния](/ru/plugins-reference#persistent-data-directory), которое сохраняется при обновлении плагина
* **Доступ к переменным окружения пользователя**: доступ к тем же переменным окружения, что и вручную настроенные servers
* **Несколько типов транспорта**: поддержка stdio, SSE и HTTP транспортов (поддержка транспорта может варьироваться в зависимости от server)

**Просмотр plugin MCP servers**:

```bash theme={null}
# В Claude Code, см. все MCP servers, включая plugin ones
/mcp
```

Plugin servers отображаются в списке с индикаторами, показывающими, что они поступают из плагинов.

**Преимущества plugin MCP servers**:

* **Упакованное распределение**: инструменты и servers упакованы вместе
* **Автоматическая настройка**: не требуется ручная конфигурация MCP
* **Согласованность команды**: все получают одинаковые инструменты при установке плагина

См. [справочник компонентов плагина](/ru/plugins-reference#mcp-servers) для получения подробной информации о включении MCP servers в плагины.

## Области установки MCP

MCP servers можно настроить на трех различных уровнях области, каждый из которых служит отдельным целям для управления доступностью server и совместным использованием. Понимание этих областей помогает вам определить лучший способ настройки servers для ваших конкретных потребностей.

### Локальная область

Servers с локальной областью представляют уровень конфигурации по умолчанию и хранятся в `~/.claude.json` в пути вашего проекта. Эти servers остаются приватными для вас и доступны только при работе в текущем каталоге проекта. Эта область идеальна для личных development servers, экспериментальных конфигураций или servers, содержащих чувствительные учетные данные, которые не должны быть общими.

<Note>
  Термин "локальная область" для MCP servers отличается от общих локальных параметров. MCP servers с локальной областью хранятся в `~/.claude.json` (ваш домашний каталог), в то время как общие локальные параметры используют `.claude/settings.local.json` (в каталоге проекта). См. [Параметры](/ru/settings#settings-files) для получения подробной информации о расположении файлов параметров.
</Note>

```bash theme={null}
# Добавить server с локальной областью (по умолчанию)
claude mcp add --transport http stripe https://mcp.stripe.com

# Явно указать локальную область
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

### Область проекта

Servers с областью проекта позволяют командной работе, сохраняя конфигурации в файле `.mcp.json` в корневом каталоге вашего проекта. Этот файл предназначен для проверки в систему контроля версий, обеспечивая всем членам команды доступ к одним и тем же MCP tools и сервисам. Когда вы добавляете server с областью проекта, Claude Code автоматически создает или обновляет этот файл с соответствующей структурой конфигурации.

```bash theme={null}
# Добавить server с областью проекта
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

Результирующий файл `.mcp.json` следует стандартизированному формату:

```json theme={null}
{
  "mcpServers": {
    "shared-server": {
      "command": "/path/to/server",
      "args": [],
      "env": {}
    }
  }
}
```

По соображениям безопасности Claude Code запрашивает одобрение перед использованием servers с областью проекта из файлов `.mcp.json`. Если вам нужно сбросить эти выборы одобрения, используйте команду `claude mcp reset-project-choices`.

### Область пользователя

Servers с областью пользователя хранятся в `~/.claude.json` и обеспечивают доступность между проектами, делая их доступными во всех проектах на вашей машине, оставаясь приватными для вашей учетной записи пользователя. Эта область хорошо работает для личных utility servers, инструментов разработки или сервисов, которые вы часто используете в разных проектах.

```bash theme={null}
# Добавить server пользователя
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### Выбор правильной области

Выберите вашу область на основе:

* **Локальная область**: личные servers, экспериментальные конфигурации или чувствительные учетные данные, специфичные для одного проекта
* **Область проекта**: servers, общие для команды, инструменты, специфичные для проекта, или сервисы, необходимые для сотрудничества
* **Область пользователя**: личные утилиты, необходимые в нескольких проектах, инструменты разработки или часто используемые сервисы

<Note>
  **Где хранятся MCP servers?**

  * **Область пользователя и локальная**: `~/.claude.json` (в поле `mcpServers` или в путях проекта)
  * **Область проекта**: `.mcp.json` в корне вашего проекта (проверено в систему контроля версий)
  * **Управляемые**: `managed-mcp.json` в системных каталогах (см. [Управляемая конфигурация MCP](#managed-mcp-configuration))
</Note>

### Иерархия области и приоритет

Конфигурации MCP server следуют четкой иерархии приоритета. Когда servers с одинаковым именем существуют в нескольких областях, система разрешает конфликты, отдавая приоритет servers с локальной областью в первую очередь, затем servers с областью проекта и, наконец, servers с областью пользователя. Этот дизайн гарантирует, что личные конфигурации могут переопределять общие, когда это необходимо.

Если server настроен как локально, так и через [соединитель claude.ai](#use-mcp-servers-from-claude-ai), локальная конфигурация имеет приоритет и запись соединителя пропускается.

### Расширение переменных окружения в `.mcp.json`

Claude Code поддерживает расширение переменных окружения в файлах `.mcp.json`, позволяя командам делиться конфигурациями, сохраняя гибкость для путей, специфичных для машины, и чувствительных значений, таких как ключи API.

**Поддерживаемый синтаксис:**

* `${VAR}` - расширяется до значения переменной окружения `VAR`
* `${VAR:-default}` - расширяется до `VAR`, если установлена, иначе использует `default`

**Места расширения:**
Переменные окружения могут быть расширены в:

* `command` - путь к исполняемому файлу server
* `args` - аргументы командной строки
* `env` - переменные окружения, передаваемые server
* `url` - для типов HTTP server
* `headers` - для аутентификации HTTP server

**Пример с расширением переменных:**

```json theme={null}
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

Если требуемая переменная окружения не установлена и не имеет значения по умолчанию, Claude Code не сможет разобрать конфигурацию.

## Практические примеры

{/* ### Пример: автоматизация тестирования браузера с помощью Playwright

```bash
claude mcp add --transport stdio playwright -- npx -y @playwright/mcp@latest
```

Затем напишите и запустите тесты браузера:

```text
Проверьте, работает ли поток входа с test@example.com
```
```text
Сделайте снимок экрана страницы оформления заказа на мобильном устройстве
```
```text
Убедитесь, что функция поиска возвращает результаты
``` */}

### Пример: мониторинг ошибок с помощью Sentry

```bash theme={null}
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

Аутентифицируйтесь с помощью вашей учетной записи Sentry:

```text theme={null}
/mcp
```

Затем отладьте проблемы в production:

```text theme={null}
Какие наиболее распространенные ошибки за последние 24 часа?
```

```text theme={null}
Покажите мне трассировку стека для ошибки ID abc123
```

```text theme={null}
Какое развертывание внесло эти новые ошибки?
```

### Пример: подключение к GitHub для проверки кода

```bash theme={null}
claude mcp add --transport http github https://api.githubcopilot.com/mcp/
```

Аутентифицируйтесь при необходимости, выбрав "Authenticate" для GitHub:

```text theme={null}
/mcp
```

Затем работайте с GitHub:

```text theme={null}
Проверьте PR #456 и предложите улучшения
```

```text theme={null}
Создайте новую проблему для найденной нами ошибки
```

```text theme={null}
Покажите мне все открытые PR, назначенные мне
```

### Пример: запрос к базе данных PostgreSQL

```bash theme={null}
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://readonly:pass@prod.db.com:5432/analytics"
```

Затем запрашивайте вашу базу данных естественным образом:

```text theme={null}
Какой у нас общий доход в этом месяце?
```

```text theme={null}
Покажите мне схему для таблицы orders
```

```text theme={null}
Найдите клиентов, которые не совершали покупку в течение 90 дней
```

## Аутентификация с удаленными MCP servers

Многие облачные MCP servers требуют аутентификации. Claude Code поддерживает OAuth 2.0 для безопасных соединений.

<Steps>
  <Step title="Добавьте server, который требует аутентификации">
    Например:

    ```bash theme={null}
    claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
    ```
  </Step>

  <Step title="Используйте команду /mcp в Claude Code">
    В Claude Code используйте команду:

    ```text theme={null}
    /mcp
    ```

    Затем следуйте инструкциям в вашем браузере для входа.
  </Step>
</Steps>

<Tip>
  Советы:

  * Токены аутентификации хранятся безопасно и автоматически обновляются
  * Используйте "Clear authentication" в меню `/mcp` для отзыва доступа
  * Если ваш браузер не открывается автоматически, скопируйте предоставленный URL и откройте его вручную
  * Если перенаправление браузера не удается с ошибкой соединения после аутентификации, вставьте полный URL обратного вызова из адресной строки браузера в приглашение URL, которое появляется в Claude Code
  * Аутентификация OAuth работает с HTTP servers
</Tip>

### Используйте фиксированный порт обратного вызова OAuth

Некоторые MCP servers требуют конкретный URI перенаправления, зарегистрированный заранее. По умолчанию Claude Code выбирает случайный доступный порт для обратного вызова OAuth. Используйте `--callback-port` для фиксации порта, чтобы он соответствовал предварительно зарегистрированному URI перенаправления формы `http://localhost:PORT/callback`.

Вы можете использовать `--callback-port` самостоятельно (с динамической регистрацией клиента) или вместе с `--client-id` (с предварительно настроенными учетными данными).

```bash theme={null}
# Фиксированный порт обратного вызова с динамической регистрацией клиента
claude mcp add --transport http \
  --callback-port 8080 \
  my-server https://mcp.example.com/mcp
```

### Используйте предварительно настроенные учетные данные OAuth

Некоторые MCP servers не поддерживают автоматическую настройку OAuth через Dynamic Client Registration. Если вы видите ошибку типа "Incompatible auth server: does not support dynamic client registration", server требует предварительно настроенные учетные данные. Claude Code также поддерживает servers, которые используют Client ID Metadata Document (CIMD) вместо Dynamic Client Registration, и обнаруживает их автоматически. Если автоматическое обнаружение не удается, сначала зарегистрируйте приложение OAuth через портал разработчика server, затем предоставьте учетные данные при добавлении server.

<Steps>
  <Step title="Зарегистрируйте приложение OAuth с помощью server">
    Создайте приложение через портал разработчика server и запишите ваш client ID и client secret.

    Многие servers также требуют URI перенаправления. Если это так, выберите порт и зарегистрируйте URI перенаправления в формате `http://localhost:PORT/callback`. Используйте тот же порт с `--callback-port` на следующем шаге.
  </Step>

  <Step title="Добавьте server с вашими учетными данными">
    Выберите один из следующих методов. Порт, используемый для `--callback-port`, может быть любым доступным портом. Он просто должен соответствовать URI перенаправления, который вы зарегистрировали на предыдущем шаге.

    <Tabs>
      <Tab title="claude mcp add">
        Используйте `--client-id` для передачи client ID вашего приложения. Флаг `--client-secret` запрашивает secret с замаскированным вводом:

        ```bash theme={null}
        claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>

      <Tab title="claude mcp add-json">
        Включите объект `oauth` в конфигурацию JSON и передайте `--client-secret` как отдельный флаг:

        ```bash theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' \
          --client-secret
        ```
      </Tab>

      <Tab title="claude mcp add-json (только порт обратного вызова)">
        Используйте `--callback-port` без client ID для фиксации порта при использовании динамической регистрации клиента:

        ```bash theme={null}
        claude mcp add-json my-server \
          '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"callbackPort":8080}}'
        ```
      </Tab>

      <Tab title="CI / переменная окружения">
        Установите secret через переменную окружения, чтобы пропустить интерактивное приглашение:

        ```bash theme={null}
        MCP_CLIENT_SECRET=your-secret claude mcp add --transport http \
          --client-id your-client-id --client-secret --callback-port 8080 \
          my-server https://mcp.example.com/mcp
        ```
      </Tab>
    </Tabs>
  </Step>

  <Step title="Аутентифицируйтесь в Claude Code">
    Запустите `/mcp` в Claude Code и следуйте потоку входа браузера.
  </Step>
</Steps>

<Tip>
  Советы:

  * Client secret хранится безопасно в вашей системной связке ключей (macOS) или файле учетных данных, а не в вашей конфигурации
  * Если server использует публичный OAuth клиент без secret, используйте только `--client-id` без `--client-secret`
  * `--callback-port` можно использовать с `--client-id` или без него
  * Эти флаги применяются только к HTTP и SSE транспортам. Они не влияют на stdio servers
  * Используйте `claude mcp get <name>` для проверки того, что учетные данные OAuth настроены для server
</Tip>

### Переопределите обнаружение метаданных OAuth

Если ваш MCP server возвращает ошибки на стандартной конечной точке метаданных OAuth, но предоставляет рабочую конечную точку OIDC, вы можете указать Claude Code на конкретный URL метаданных, чтобы обойти цепочку обнаружения по умолчанию. По умолчанию Claude Code сначала проверяет метаданные защищенного ресурса RFC 9728 на `/.well-known/oauth-protected-resource`, затем возвращается к метаданным сервера авторизации RFC 8414 на `/.well-known/oauth-authorization-server`.

Установите `authServerMetadataUrl` в объекте `oauth` конфигурации вашего server в `.mcp.json`:

```json theme={null}
{
  "mcpServers": {
    "my-server": {
      "type": "http",
      "url": "https://mcp.example.com/mcp",
      "oauth": {
        "authServerMetadataUrl": "https://auth.example.com/.well-known/openid-configuration"
      }
    }
  }
}
```

URL должен использовать `https://`. Эта опция требует Claude Code v2.1.64 или позже.

### Используйте динамические заголовки для пользовательской аутентификации

Если ваш MCP server использует схему аутентификации, отличную от OAuth (такую как Kerberos, краткосрочные токены или внутреннее SSO), используйте `headersHelper` для генерации заголовков запроса во время подключения. Claude Code запускает команду и объединяет ее выход в заголовки подключения.

```json theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "/opt/bin/get-mcp-auth-headers.sh"
    }
  }
}
```

Команда также может быть встроенной:

```json theme={null}
{
  "mcpServers": {
    "internal-api": {
      "type": "http",
      "url": "https://mcp.internal.example.com",
      "headersHelper": "echo '{\"Authorization\": \"Bearer '\"$(get-token)\"'\"}'"
    }
  }
}
```

**Требования:**

* Команда должна записать объект JSON пар строк ключ-значение в stdout
* Команда запускается в оболочке с timeout в 10 секунд
* Динамические заголовки переопределяют любые статические `headers` с тем же именем

Помощник запускается заново при каждом подключении (при запуске сеанса и при переподключении). Кэширования нет, поэтому ваш скрипт отвечает за любое повторное использование токена.

Claude Code устанавливает эти переменные окружения при выполнении помощника:

| Переменная                    | Значение       |
| :---------------------------- | :------------- |
| `CLAUDE_CODE_MCP_SERVER_NAME` | имя MCP server |
| `CLAUDE_CODE_MCP_SERVER_URL`  | URL MCP server |

Используйте их для написания одного скрипта помощника, который служит нескольким MCP servers.

<Note>
  `headersHelper` выполняет произвольные команды оболочки. Когда определено в области проекта или локальной области, он запускается только после того, как вы примете диалог доверия рабочей области.
</Note>

## Добавьте MCP servers из конфигурации JSON

Если у вас есть конфигурация JSON для MCP server, вы можете добавить ее напрямую:

<Steps>
  <Step title="Добавьте MCP server из JSON">
    ```bash theme={null}
    # Базовый синтаксис
    claude mcp add-json <name> '<json>'

    # Пример: добавление HTTP server с конфигурацией JSON
    claude mcp add-json weather-api '{"type":"http","url":"https://api.weather.com/mcp","headers":{"Authorization":"Bearer token"}}'

    # Пример: добавление stdio server с конфигурацией JSON
    claude mcp add-json local-weather '{"type":"stdio","command":"/path/to/weather-cli","args":["--api-key","abc123"],"env":{"CACHE_DIR":"/tmp"}}'

    # Пример: добавление HTTP server с предварительно настроенными учетными данными OAuth
    claude mcp add-json my-server '{"type":"http","url":"https://mcp.example.com/mcp","oauth":{"clientId":"your-client-id","callbackPort":8080}}' --client-secret
    ```
  </Step>

  <Step title="Проверьте, что server был добавлен">
    ```bash theme={null}
    claude mcp get weather-api
    ```
  </Step>
</Steps>

<Tip>
  Советы:

  * Убедитесь, что JSON правильно экранирован в вашей оболочке
  * JSON должен соответствовать схеме конфигурации MCP server
  * Вы можете использовать `--scope user` для добавления server в вашу конфигурацию пользователя вместо конфигурации, специфичной для проекта
</Tip>

## Импортируйте MCP servers из Claude Desktop

Если вы уже настроили MCP servers в Claude Desktop, вы можете их импортировать:

<Steps>
  <Step title="Импортируйте servers из Claude Desktop">
    ```bash theme={null}
    # Базовый синтаксис 
    claude mcp add-from-claude-desktop 
    ```
  </Step>

  <Step title="Выберите, какие servers импортировать">
    После запуска команды вы увидите интерактивный диалог, который позволяет вам выбрать, какие servers вы хотите импортировать.
  </Step>

  <Step title="Проверьте, что servers были импортированы">
    ```bash theme={null}
    claude mcp list 
    ```
  </Step>
</Steps>

<Tip>
  Советы:

  * Эта функция работает только на macOS и Windows Subsystem for Linux (WSL)
  * Она читает файл конфигурации Claude Desktop из его стандартного расположения на этих платформах
  * Используйте флаг `--scope user` для добавления servers в вашу конфигурацию пользователя
  * Импортированные servers будут иметь те же имена, что и в Claude Desktop
  * Если servers с одинаковыми именами уже существуют, они получат числовой суффикс (например, `server_1`)
</Tip>

## Используйте MCP servers из Claude.ai

Если вы вошли в Claude Code с учетной записью [Claude.ai](https://claude.ai), MCP servers, которые вы добавили в Claude.ai, автоматически доступны в Claude Code:

<Steps>
  <Step title="Настройте MCP servers в Claude.ai">
    Добавьте servers на [claude.ai/settings/connectors](https://claude.ai/settings/connectors). В планах Team и Enterprise только администраторы могут добавлять servers.
  </Step>

  <Step title="Аутентифицируйте MCP server">
    Завершите все необходимые шаги аутентификации в Claude.ai.
  </Step>

  <Step title="Просмотрите и управляйте servers в Claude Code">
    В Claude Code используйте команду:

    ```text theme={null}
    /mcp
    ```

    Claude.ai servers отображаются в списке с индикаторами, показывающими, что они поступают из Claude.ai.
  </Step>
</Steps>

Чтобы отключить MCP servers claude.ai в Claude Code, установите переменную окружения `ENABLE_CLAUDEAI_MCP_SERVERS` на `false`:

```bash theme={null}
ENABLE_CLAUDEAI_MCP_SERVERS=false claude
```

## Используйте Claude Code как MCP server

Вы можете использовать сам Claude Code как MCP server, к которому могут подключаться другие приложения:

```bash theme={null}
# Запустите Claude как stdio MCP server
claude mcp serve
```

Вы можете использовать это в Claude Desktop, добавив эту конфигурацию в claude\_desktop\_config.json:

```json theme={null}
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

<Warning>
  **Настройка пути к исполняемому файлу**: поле `command` должно ссылаться на исполняемый файл Claude Code. Если команда `claude` не находится в PATH вашей системы, вам нужно указать полный путь к исполняемому файлу.

  Чтобы найти полный путь:

  ```bash theme={null}
  which claude
  ```

  Затем используйте полный путь в вашей конфигурации:

  ```json theme={null}
  {
    "mcpServers": {
      "claude-code": {
        "type": "stdio",
        "command": "/full/path/to/claude",
        "args": ["mcp", "serve"],
        "env": {}
      }
    }
  }
  ```

  Без правильного пути к исполняемому файлу вы столкнетесь с ошибками типа `spawn claude ENOENT`.
</Warning>

<Tip>
  Советы:

  * Server предоставляет доступ к инструментам Claude, таким как View, Edit, LS и т. д.
  * В Claude Desktop попробуйте попросить Claude прочитать файлы в каталоге, внести изменения и многое другое.
  * Обратите внимание, что этот MCP server только предоставляет инструменты Claude Code вашему MCP клиенту, поэтому ваш собственный клиент отвечает за реализацию подтверждения пользователя для отдельных вызовов инструментов.
</Tip>

## Лимиты выхода MCP и предупреждения

Когда инструменты MCP производят большие выходы, Claude Code помогает управлять использованием токенов, чтобы предотвратить перегрузку контекста вашего разговора:

* **Порог предупреждения выхода**: Claude Code отображает предупреждение, когда выход любого инструмента MCP превышает 10 000 токенов
* **Настраиваемый лимит**: вы можете отрегулировать максимальное количество разрешенных токенов выхода MCP, используя переменную окружения `MAX_MCP_OUTPUT_TOKENS`
* **Лимит по умолчанию**: максимум по умолчанию составляет 25 000 токенов

Чтобы увеличить лимит для инструментов, которые производят большие выходы:

```bash theme={null}
# Установите более высокий лимит для выходов инструментов MCP
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

Это особенно полезно при работе с MCP servers, которые:

* запрашивают большие наборы данных или базы данных
* генерируют подробные отчеты или документацию
* обрабатывают обширные файлы журналов или информацию отладки

<Warning>
  Если вы часто сталкиваетесь с предупреждениями выхода с конкретными MCP servers, рассмотрите возможность увеличения лимита или настройки server для разбиения на страницы или фильтрации его ответов.
</Warning>

## Ответьте на запросы MCP elicitation

MCP servers могут запрашивать структурированный ввод от вас во время выполнения задачи, используя elicitation. Когда server нуждается в информации, которую он не может получить самостоятельно, Claude Code отображает интерактивный диалог и передает ваш ответ обратно server. На вашей стороне не требуется никакой конфигурации: диалоги elicitation появляются автоматически, когда server их запрашивает.

Servers могут запрашивать ввод двумя способами:

* **Режим формы**: Claude Code показывает диалог с полями формы, определенными server (например, приглашение имени пользователя и пароля). Заполните поля и отправьте.
* **Режим URL**: Claude Code открывает URL браузера для аутентификации или одобрения. Завершите процесс в браузере, затем подтвердите в CLI.

Чтобы автоматически ответить на запросы elicitation без отображения диалога, используйте [`Elicitation` hook](/ru/hooks#Elicitation).

Если вы создаете MCP server, который использует elicitation, см. [спецификацию MCP elicitation](https://modelcontextprotocol.io/docs/learn/client-concepts#elicitation) для деталей протокола и примеров схемы.

## Используйте MCP ресурсы

MCP servers могут предоставлять ресурсы, на которые вы можете ссылаться, используя упоминания @, аналогично тому, как вы ссылаетесь на файлы.

### Ссылка на MCP ресурсы

<Steps>
  <Step title="Список доступных ресурсов">
    Введите `@` в вашу подсказку, чтобы увидеть доступные ресурсы от всех подключенных MCP servers. Ресурсы отображаются рядом с файлами в меню автодополнения.
  </Step>

  <Step title="Ссылка на конкретный ресурс">
    Используйте формат `@server:protocol://resource/path` для ссылки на ресурс:

    ```text theme={null}
    Можете ли вы проанализировать @github:issue://123 и предложить исправление?
    ```

    ```text theme={null}
    Пожалуйста, проверьте документацию API на @docs:file://api/authentication
    ```
  </Step>

  <Step title="Несколько ссылок на ресурсы">
    Вы можете ссылаться на несколько ресурсов в одной подсказке:

    ```text theme={null}
    Сравните @postgres:schema://users с @docs:file://database/user-model
    ```
  </Step>
</Steps>

<Tip>
  Советы:

  * Ресурсы автоматически получаются и включаются как вложения при ссылке
  * Пути ресурсов поддерживают нечеткий поиск в автодополнении упоминания @
  * Claude Code автоматически предоставляет инструменты для списка и чтения MCP ресурсов, когда servers их поддерживают
  * Ресурсы могут содержать любой тип контента, который предоставляет MCP server (текст, JSON, структурированные данные и т. д.)
</Tip>

## Масштабирование с помощью MCP Tool Search

Tool search сохраняет использование контекста MCP низким, откладывая определения инструментов до тех пор, пока Claude их не потребует. Только имена инструментов загружаются при запуске сеанса, поэтому добавление большего количества MCP servers имеет минимальное влияние на ваше окно контекста.

### Как это работает

Tool search включен по умолчанию. Инструменты MCP откладываются, а не загружаются в контекст заранее, и Claude использует инструмент поиска для обнаружения релевантных инструментов, когда задача их требует. Только инструменты, которые Claude действительно использует, входят в контекст. С вашей точки зрения инструменты MCP работают точно так же, как раньше.

Если вы предпочитаете загрузку на основе порога, установите `ENABLE_TOOL_SEARCH=auto` для загрузки схем заранее, когда они подходят в пределах 10% окна контекста, и откладывайте только переполнение. См. [Настройте tool search](#configure-tool-search) для всех опций.

### Для авторов MCP server

Если вы создаете MCP server, поле инструкций server становится более полезным с включенным Tool Search. Инструкции server помогают Claude понять, когда искать ваши инструменты, аналогично тому, как работают [skills](/ru/skills).

Добавьте четкие, описательные инструкции server, которые объясняют:

* какую категорию задач обрабатывают ваши инструменты
* когда Claude должен искать ваши инструменты
* ключевые возможности, которые предоставляет ваш server

Claude Code усекает описания инструментов и инструкции server на 2KB каждое. Держите их краткими, чтобы избежать усечения, и поместите критические детали в начало.

### Настройте tool search

Tool search включен по умолчанию: инструменты MCP откладываются и обнаруживаются по требованию. Когда `ANTHROPIC_BASE_URL` указывает на хост, не являющийся первой стороной, tool search отключен по умолчанию, потому что большинство прокси не пересылают блоки `tool_reference`. Установите `ENABLE_TOOL_SEARCH` явно, если ваш прокси это делает. Эта функция требует моделей, которые поддерживают блоки `tool_reference`: Sonnet 4 и позже, или Opus 4 и позже. Модели Haiku не поддерживают tool search.

Управляйте поведением tool search с помощью переменной окружения `ENABLE_TOOL_SEARCH`:

| Значение         | Поведение                                                                                                                                                                 |
| :--------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| (не установлено) | Все инструменты MCP откладываются и загружаются по требованию. Возвращается к загрузке заранее, когда `ANTHROPIC_BASE_URL` является хостом, не являющимся первой стороной |
| `true`           | Все инструменты MCP откладываются, включая для `ANTHROPIC_BASE_URL`, не являющегося первой стороной                                                                       |
| `auto`           | Режим порога: инструменты загружаются заранее, если они подходят в пределах 10% окна контекста, откладываются иначе                                                       |
| `auto:<N>`       | Режим порога с пользовательским процентом, где `<N>` — это 0-100 (например, `auto:5` для 5%)                                                                              |
| `false`          | Все инструменты MCP загружаются заранее, без откладывания                                                                                                                 |

```bash theme={null}
# Используйте пользовательский порог 5%
ENABLE_TOOL_SEARCH=auto:5 claude

# Полностью отключите tool search
ENABLE_TOOL_SEARCH=false claude
```

Или установите значение в поле `env` вашего [settings.json](/ru/settings#available-settings).

Вы также можете отключить инструмент ToolSearch специально:

```json theme={null}
{
  "permissions": {
    "deny": ["ToolSearch"]
  }
}
```

## Используйте MCP подсказки как команды

MCP servers могут предоставлять подсказки, которые становятся доступными как команды в Claude Code.

### Выполните MCP подсказки

<Steps>
  <Step title="Откройте доступные подсказки">
    Введите `/` для просмотра всех доступных команд, включая те из MCP servers. MCP подсказки отображаются в формате `/mcp__servername__promptname`.
  </Step>

  <Step title="Выполните подсказку без аргументов">
    ```text theme={null}
    /mcp__github__list_prs
    ```
  </Step>

  <Step title="Выполните подсказку с аргументами">
    Многие подсказки принимают аргументы. Передайте их через пробел после команды:

    ```text theme={null}
    /mcp__github__pr_review 456
    ```

    ```text theme={null}
    /mcp__jira__create_issue "Bug in login flow" high
    ```
  </Step>
</Steps>

<Tip>
  Советы:

  * MCP подсказки динамически обнаруживаются из подключенных servers
  * Аргументы анализируются на основе определенных параметров подсказки
  * Результаты подсказки вводятся непосредственно в разговор
  * Имена server и подсказки нормализуются (пробелы становятся подчеркиваниями)
</Tip>

## Управляемая конфигурация MCP

Для организаций, которым требуется централизованный контроль над MCP servers, Claude Code поддерживает две опции конфигурации:

1. **Исключительный контроль с `managed-mcp.json`**: развертывание фиксированного набора MCP servers, которые пользователи не могут изменять или расширять
2. **Контроль на основе политики с allowlists/denylists**: позволить пользователям добавлять свои собственные servers, но ограничить, какие из них разрешены

Эти опции позволяют IT администраторам:

* **Контролировать, какие MCP servers могут использовать сотрудники**: развертывание стандартизированного набора одобренных MCP servers по всей организации
* **Предотвратить несанкционированные MCP servers**: ограничить пользователей от добавления неодобренных MCP servers
* **Полностью отключить MCP**: удалить функциональность MCP, если это необходимо

### Вариант 1: исключительный контроль с managed-mcp.json

Когда вы развертываете файл `managed-mcp.json`, он берет **исключительный контроль** над всеми MCP servers. Пользователи не могут добавлять, изменять или использовать какие-либо MCP servers, кроме определенных в этом файле. Это самый простой подход для организаций, которые хотят полный контроль.

Системные администраторы развертывают файл конфигурации в системный каталог:

* macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
* Linux и WSL: `/etc/claude-code/managed-mcp.json`
* Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

<Note>
  Это системные пути (не домашние каталоги пользователей, такие как `~/Library/...`), которые требуют привилегий администратора. Они предназначены для развертывания IT администраторами.
</Note>

Файл `managed-mcp.json` использует тот же формат, что и стандартный файл `.mcp.json`:

```json theme={null}
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "sentry": {
      "type": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "company-internal": {
      "type": "stdio",
      "command": "/usr/local/bin/company-mcp-server",
      "args": ["--config", "/etc/company/mcp-config.json"],
      "env": {
        "COMPANY_API_URL": "https://internal.company.com"
      }
    }
  }
}
```

### Вариант 2: контроль на основе политики с allowlists и denylists

Вместо того чтобы брать исключительный контроль, администраторы могут позволить пользователям настраивать свои собственные MCP servers, одновременно применяя ограничения на то, какие servers разрешены. Этот подход использует `allowedMcpServers` и `deniedMcpServers` в [файле управляемых параметров](/ru/settings#settings-files).

<Note>
  **Выбор между вариантами**: используйте вариант 1 (`managed-mcp.json`), когда вы хотите развернуть фиксированный набор servers без настройки пользователем. Используйте вариант 2 (allowlists/denylists), когда вы хотите позволить пользователям добавлять свои собственные servers в рамках ограничений политики.
</Note>

#### Опции ограничения

Каждая запись в allowlist или denylist может ограничивать servers тремя способами:

1. **По имени server** (`serverName`): соответствует настроенному имени server
2. **По команде** (`serverCommand`): соответствует точной команде и аргументам, используемым для запуска stdio servers
3. **По шаблону URL** (`serverUrl`): соответствует URL-адресам удаленных servers с поддержкой подстановочных символов

**Важно**: каждая запись должна иметь ровно одно из `serverName`, `serverCommand` или `serverUrl`.

#### Пример конфигурации

```json theme={null}
{
  "allowedMcpServers": [
    // Разрешить по имени server
    { "serverName": "github" },
    { "serverName": "sentry" },

    // Разрешить по точной команде (для stdio servers)
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] },
    { "serverCommand": ["python", "/usr/local/bin/approved-server.py"] },

    // Разрешить по шаблону URL (для удаленных servers)
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverUrl": "https://*.internal.corp/*" }
  ],
  "deniedMcpServers": [
    // Заблокировать по имени server
    { "serverName": "dangerous-server" },

    // Заблокировать по точной команде (для stdio servers)
    { "serverCommand": ["npx", "-y", "unapproved-package"] },

    // Заблокировать по шаблону URL (для удаленных servers)
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

#### Как работают ограничения на основе команд

**Точное совпадение**:

* Массивы команд должны совпадать **точно** — как команда, так и все аргументы в правильном порядке
* Пример: `["npx", "-y", "server"]` НЕ будет совпадать с `["npx", "server"]` или `["npx", "-y", "server", "--flag"]`

**Поведение stdio server**:

* Когда allowlist содержит **любые** записи `serverCommand`, stdio servers **должны** совпадать с одной из этих команд
* Stdio servers не могут пройти только по имени, когда присутствуют ограничения команд
* Это гарантирует, что администраторы могут применять, какие команды разрешены для запуска

**Поведение удаленного server**:

* Удаленные servers (HTTP, SSE, WebSocket) используют сопоставление на основе URL, когда в allowlist существуют записи `serverUrl`
* Если записей URL не существует, удаленные servers возвращаются к сопоставлению на основе имени
* Ограничения команд не применяются к удаленным servers

#### Как работают ограничения на основе URL

Шаблоны URL поддерживают подстановочные символы, используя `*` для совпадения с любой последовательностью символов. Это полезно для разрешения целых доменов или поддоменов.

**Примеры подстановочных символов**:

* `https://mcp.company.com/*` - разрешить все пути на конкретном домене
* `https://*.example.com/*` - разрешить любой поддомен example.com
* `http://localhost:*/*` - разрешить любой порт на localhost

**Поведение удаленного server**:

* Когда allowlist содержит **любые** записи `serverUrl`, удаленные servers **должны** совпадать с одним из этих шаблонов URL
* Удаленные servers не могут пройти только по имени, когда присутствуют ограничения URL
* Это гарантирует, что администраторы могут применять, какие удаленные конечные точки разрешены

<Accordion title="Пример: allowlist только для URL">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverUrl": "https://mcp.company.com/*" },
      { "serverUrl": "https://*.internal.corp/*" }
    ]
  }
  ```

  **Результат**:

  * HTTP server на `https://mcp.company.com/api`: ✅ разрешено (совпадает с шаблоном URL)
  * HTTP server на `https://api.internal.corp/mcp`: ✅ разрешено (совпадает с подстановочным поддоменом)
  * HTTP server на `https://external.com/mcp`: ❌ заблокировано (не совпадает ни с одним шаблоном URL)
  * Stdio server с любой командой: ❌ заблокировано (нет записей имени или команды для совпадения)
</Accordion>

<Accordion title="Пример: allowlist только для команд">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverCommand": ["npx", "-y", "approved-package"] }
    ]
  }
  ```

  **Результат**:

  * Stdio server с `["npx", "-y", "approved-package"]`: ✅ разрешено (совпадает с командой)
  * Stdio server с `["node", "server.js"]`: ❌ заблокировано (не совпадает с командой)
  * HTTP server с именем "my-api": ❌ заблокировано (нет записей имени для совпадения)
</Accordion>

<Accordion title="Пример: смешанный allowlist имени и команды">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverName": "github" },
      { "serverCommand": ["npx", "-y", "approved-package"] }
    ]
  }
  ```

  **Результат**:

  * Stdio server с именем "local-tool" и `["npx", "-y", "approved-package"]`: ✅ разрешено (совпадает с командой)
  * Stdio server с именем "local-tool" и `["node", "server.js"]`: ❌ заблокировано (записи команд существуют, но не совпадают)
  * Stdio server с именем "github" и `["node", "server.js"]`: ❌ заблокировано (stdio servers должны совпадать с командами, когда существуют записи команд)
  * HTTP server с именем "github": ✅ разрешено (совпадает с именем)
  * HTTP server с именем "other-api": ❌ заблокировано (имя не совпадает)
</Accordion>

<Accordion title="Пример: allowlist только для имени">
  ```json theme={null}
  {
    "allowedMcpServers": [
      { "serverName": "github" },
      { "serverName": "internal-tool" }
    ]
  }
  ```

  **Результат**:

  * Stdio server с именем "github" и любой командой: ✅ разрешено (нет ограничений команд)
  * Stdio server с именем "internal-tool" и любой командой: ✅ разрешено (нет ограничений команд)
  * HTTP server с именем "github": ✅ разрешено (совпадает с именем)
  * Любой server с именем "other": ❌ заблокировано (имя не совпадает)
</Accordion>

#### Поведение allowlist (`allowedMcpServers`)

* `undefined` (по умолчанию): нет ограничений - пользователи могут настроить любой MCP server
* Пустой массив `[]`: полная блокировка - пользователи не могут настроить какие-либо MCP servers
* Список записей: пользователи могут настроить только servers, которые совпадают по имени, команде или шаблону URL

#### Поведение denylist (`deniedMcpServers`)

* `undefined` (по умолчанию): никакие servers не блокируются
* Пустой массив `[]`: никакие servers не блокируются
* Список записей: указанные servers явно блокируются во всех областях

#### Важные примечания

* **Вариант 1 и вариант 2 можно комбинировать**: если существует `managed-mcp.json`, он имеет исключительный контроль и пользователи не могут добавлять servers. Allowlists/denylists все еще применяются к самим управляемым servers.
* **Denylist имеет абсолютный приоритет**: если server совпадает с записью denylist (по имени, команде или URL), он будет заблокирован, даже если он находится в allowlist
* Ограничения на основе имени, команды и URL работают вместе: server проходит, если он совпадает с **либо** записью имени, записью команды, либо шаблоном URL (если не заблокирован denylist)

<Note>
  **При использовании `managed-mcp.json`**: пользователи не могут добавлять MCP servers через `claude mcp add` или файлы конфигурации. Параметры `allowedMcpServers` и `deniedMcpServers` все еще применяются для фильтрации, какие управляемые servers фактически загружаются.
</Note>
