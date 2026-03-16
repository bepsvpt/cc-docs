> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Конфигурация сети для предприятия

> Настройте Claude Code для корпоративных сред с прокси-серверами, пользовательскими центрами сертификации (CA) и взаимной аутентификацией Transport Layer Security (mTLS).

Claude Code поддерживает различные конфигурации сети и безопасности предприятия через переменные окружения. Это включает маршрутизацию трафика через корпоративные прокси-серверы, доверие пользовательским центрам сертификации (CA) и аутентификацию с использованием сертификатов взаимного Transport Layer Security (mTLS) для повышенной безопасности.

<Note>
  Все переменные окружения, показанные на этой странице, также можно настроить в [`settings.json`](/ru/settings).
</Note>

## Конфигурация прокси

### Переменные окружения

Claude Code соответствует стандартным переменным окружения прокси:

```bash  theme={null}
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

```bash  theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  Избегайте жесткого кодирования паролей в скриптах. Используйте переменные окружения или безопасное хранилище учетных данных вместо этого.
</Warning>

<Tip>
  Для прокси, требующих расширенную аутентификацию (NTLM, Kerberos и т. д.), рассмотрите использование сервиса LLM Gateway, который поддерживает ваш метод аутентификации.
</Tip>

## Пользовательские сертификаты CA

Если ваша корпоративная среда использует пользовательские центры сертификации для HTTPS-соединений (через прокси или прямой доступ к API), настройте Claude Code для доверия им:

```bash  theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## Аутентификация mTLS

Для корпоративных сред, требующих аутентификацию с использованием сертификата клиента:

```bash  theme={null}
# Сертификат клиента для аутентификации
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Приватный ключ клиента
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Опционально: Парольная фраза для зашифрованного приватного ключа
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## Требования к доступу в сети

Claude Code требует доступ к следующим URL-адресам:

* `api.anthropic.com`: конечные точки Claude API
* `claude.ai`: аутентификация для учетных записей claude.ai
* `platform.claude.com`: аутентификация для учетных записей Anthropic Console

Убедитесь, что эти URL-адреса добавлены в белый список в конфигурации прокси и правилах брандмауэра. Это особенно важно при использовании Claude Code в контейнеризованных или ограниченных сетевых средах.

## Дополнительные ресурсы

* [Параметры Claude Code](/ru/settings)
* [Справочник переменных окружения](/ru/settings#environment-variables)
* [Руководство по устранению неполадок](/ru/troubleshooting)
