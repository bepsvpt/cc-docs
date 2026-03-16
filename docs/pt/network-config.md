> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuração de rede empresarial

> Configure Claude Code para ambientes empresariais com servidores proxy, Autoridades de Certificação (CA) personalizadas e autenticação mútua de Transport Layer Security (mTLS).

Claude Code suporta várias configurações de rede e segurança empresariais através de variáveis de ambiente. Isso inclui rotear o tráfego através de servidores proxy corporativos, confiar em Autoridades de Certificação (CA) personalizadas e autenticar com certificados de Transport Layer Security (mTLS) mútuo para segurança aprimorada.

<Note>
  Todas as variáveis de ambiente mostradas nesta página também podem ser configuradas em [`settings.json`](/pt/settings).
</Note>

## Configuração de proxy

### Variáveis de ambiente

Claude Code respeita variáveis de ambiente de proxy padrão:

```bash  theme={null}
# Proxy HTTPS (recomendado)
export HTTPS_PROXY=https://proxy.example.com:8080

# Proxy HTTP (se HTTPS não estiver disponível)
export HTTP_PROXY=http://proxy.example.com:8080

# Ignorar proxy para solicitações específicas - formato separado por espaço
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# Ignorar proxy para solicitações específicas - formato separado por vírgula
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# Ignorar proxy para todas as solicitações
export NO_PROXY="*"
```

<Note>
  Claude Code não suporta proxies SOCKS.
</Note>

### Autenticação básica

Se seu proxy exigir autenticação básica, inclua credenciais na URL do proxy:

```bash  theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  Evite codificar senhas em scripts. Use variáveis de ambiente ou armazenamento seguro de credenciais.
</Warning>

<Tip>
  Para proxies que exigem autenticação avançada (NTLM, Kerberos, etc.), considere usar um serviço LLM Gateway que suporte seu método de autenticação.
</Tip>

## Certificados CA personalizados

Se seu ambiente empresarial usa CAs personalizadas para conexões HTTPS (seja através de um proxy ou acesso direto à API), configure Claude Code para confiar neles:

```bash  theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## Autenticação mTLS

Para ambientes empresariais que exigem autenticação de certificado de cliente:

```bash  theme={null}
# Certificado de cliente para autenticação
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Chave privada do cliente
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Opcional: Frase de acesso para chave privada criptografada
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## Requisitos de acesso à rede

Claude Code requer acesso aos seguintes URLs:

* `api.anthropic.com`: Endpoints da API Claude
* `claude.ai`: autenticação para contas claude.ai
* `platform.claude.com`: autenticação para contas do Anthropic Console

Certifique-se de que esses URLs estão na lista de permissão em sua configuração de proxy e regras de firewall. Isso é especialmente importante ao usar Claude Code em ambientes de rede containerizados ou restritos.

## Recursos adicionais

* [Configurações do Claude Code](/pt/settings)
* [Referência de variáveis de ambiente](/pt/settings#environment-variables)
* [Guia de solução de problemas](/pt/troubleshooting)
