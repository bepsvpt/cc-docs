> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Конфигурация сети для предприятия

> Настройте Claude Code для корпоративных сред с прокси-серверами, пользовательскими центрами сертификации (CA) и взаимной аутентификацией Transport Layer Security (mTLS).

Claude Code поддерживает различные конфигурации сети и безопасности предприятия через переменные окружения. Это включает маршрутизацию трафика через корпоративные прокси-серверы, доверие пользовательским центрам сертификации (CA) и аутентификацию с помощью сертификатов взаимного Transport Layer Security (mTLS) для повышенной безопасности.

<Note>
  Все переменные окружения, показанные на этой странице, также можно настроить в [`settings.json`](/ru/settings).
</Note>

## Конфигурация прокси

### Переменные окружения

Claude Code соответствует стандартным переменным окружения прокси:

```bash theme={null}
# HTTPS прокси (рекомендуется)
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP прокси (если HTTPS недоступен)
export HTTP_PROXY=http://proxy.example.com:8080

# Обход прокси для конкретных запросов - формат с разделением пробелом
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# Обход прокси для конкретных запросов - формат с разделением запятой
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# Обход прокси для всех запросов
export NO_PROXY="*"
```

<Note>
  Claude Code не поддерживает SOCKS прокси.
</Note>

### Базовая аутентификация

Если ваш прокси требует базовую аутентификацию, включите учетные данные в URL прокси:

```bash theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  Избегайте жесткого кодирования паролей в скриптах. Используйте переменные окружения или безопасное хранилище учетных данных вместо этого.
</Warning>

<Tip>
  Для прокси, требующих расширенную аутентификацию (NTLM, Kerberos и т. д.), рассмотрите использование сервиса LLM Gateway, который поддерживает ваш метод аутентификации.
</Tip>

## Хранилище сертификатов CA

По умолчанию Claude Code доверяет как своему встроенному набору сертификатов Mozilla CA, так и хранилищу сертификатов вашей операционной системы. Корпоративные прокси с TLS-инспекцией, такие как CrowdStrike Falcon и Zscaler, работают без дополнительной конфигурации, когда их корневой сертификат установлен в хранилище доверия ОС.

<Note>
  Интеграция системного хранилища CA требует собственного двоичного распределения Claude Code. При запуске на среде выполнения Node.js системное хранилище CA не объединяется автоматически. В этом случае установите `NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem` для доверия корневому CA предприятия.
</Note>

`CLAUDE_CODE_CERT_STORE` принимает список источников, разделенный запятыми. Признанные значения: `bundled` для набора Mozilla CA, поставляемого с Claude Code, и `system` для хранилища доверия операционной системы. По умолчанию используется `bundled,system`.

Для доверия только встроенному набору Mozilla CA:

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=bundled
```

Для доверия только хранилищу сертификатов ОС:

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=system
```

<Note>
  `CLAUDE_CODE_CERT_STORE` не имеет выделенного ключа схемы `settings.json`. Установите его через блок `env` в `~/.claude/settings.json` или непосредственно в окружении процесса.
</Note>

## Пользовательские сертификаты CA

Если ваша корпоративная среда использует пользовательский CA, настройте Claude Code для доверия ему напрямую:

```bash theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## Аутентификация mTLS

Для корпоративных сред, требующих аутентификацию с помощью сертификата клиента:

```bash theme={null}
# Сертификат клиента для аутентификации
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Приватный ключ клиента
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Опционально: Парольная фраза для зашифрованного приватного ключа
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## Требования к доступу в сети

Claude Code требует доступ к следующим URL. Добавьте их в белый список в конфигурации прокси и правилах брандмауэра, особенно в контейнеризованных или ограниченных сетевых средах.

| URL                            | Требуется для                                                                                                 |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| `api.anthropic.com`            | Запросы Claude API                                                                                            |
| `claude.ai`                    | Аутентификация учетной записи claude.ai                                                                       |
| `platform.claude.com`          | Аутентификация учетной записи Anthropic Console                                                               |
| `downloads.claude.ai`          | Загрузки исполняемых файлов плагинов; встроенный установщик и встроенное автоматическое обновление            |
| `storage.googleapis.com`       | {/* max-version: 2.1.115 */}Встроенный установщик и встроенное автоматическое обновление в версиях до 2.1.116 |
| `bridge.claudeusercontent.com` | Мост WebSocket расширения [Claude в Chrome](/ru/chrome)                                                       |

Если вы устанавливаете Claude Code через npm или управляете собственным распределением бинарных файлов, конечным пользователям может не потребоваться доступ к `downloads.claude.ai` или `storage.googleapis.com`.

При использовании [Amazon Bedrock](/ru/amazon-bedrock), [Google Vertex AI](/ru/google-vertex-ai) или [Microsoft Foundry](/ru/microsoft-foundry) трафик модели и аутентификация идут к вашему поставщику вместо `api.anthropic.com`, `claude.ai` или `platform.claude.com`. Инструмент WebFetch по-прежнему вызывает `api.anthropic.com` для своей [проверки безопасности домена](/ru/data-usage#webfetch-domain-safety-check), если вы не установите `skipWebFetchPreflight: true` в [параметрах](/ru/settings).

[Claude Code в веб-версии](/ru/claude-code-on-the-web) и [Code Review](/ru/code-review) подключаются к вашим репозиториям из управляемой Anthropic инфраструктуры. Если ваша организация GitHub Enterprise Cloud ограничивает доступ по IP-адресу, включите [наследование списка разрешенных IP для установленных GitHub Apps](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps). GitHub App Claude регистрирует свои диапазоны IP, поэтому включение этого параметра позволяет получить доступ без ручной конфигурации. Чтобы [добавить диапазоны в список разрешенных вручную](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address) вместо этого, или для настройки других брандмауэров, см. [IP-адреса Anthropic API](https://platform.claude.com/docs/en/api/ip-addresses).

Для самостоятельно размещаемых экземпляров [GitHub Enterprise Server](/ru/github-enterprise-server) за брандмауэром добавьте в белый список те же [IP-адреса Anthropic API](https://platform.claude.com/docs/en/api/ip-addresses), чтобы инфраструктура Anthropic могла достичь вашего хоста GHES для клонирования репозиториев и публикации комментариев к рецензиям.

## Дополнительные ресурсы

* [Параметры Claude Code](/ru/settings)
* [Справочник переменных окружения](/ru/env-vars)
* [Руководство по устранению неполадок](/ru/troubleshooting)
