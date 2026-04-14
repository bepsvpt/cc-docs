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

Certifique-se de que esses URLs estão na lista de permissões em sua configuração de proxy e regras de firewall. Isso é especialmente importante ao usar Claude Code em ambientes de rede containerizados ou restritos.

O instalador nativo e as verificações de atualização também exigem os seguintes URLs. Coloque ambos na lista de permissões, pois o instalador e o atualizador automático buscam de `storage.googleapis.com` enquanto os downloads de plugins usam `downloads.claude.ai`. Se você instalar Claude Code através do npm ou gerenciar sua própria distribuição binária, os usuários finais podem não precisar de acesso:

* `storage.googleapis.com`: bucket de download para o binário Claude Code e atualizador automático
* `downloads.claude.ai`: CDN hospedando o script de instalação, ponteiros de versão, manifestos, chaves de assinatura e executáveis de plugins

[Claude Code na web](/pt/claude-code-on-the-web) e [Code Review](/pt/code-review) se conectam aos seus repositórios a partir da infraestrutura gerenciada pela Anthropic. Se sua organização GitHub Enterprise Cloud restringe o acesso por endereço IP, ative [herança de lista de permissão de IP para GitHub Apps instalados](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps). O Claude GitHub App registra seus intervalos de IP, portanto, ativar essa configuração permite acesso sem configuração manual. Para [adicionar os intervalos à sua lista de permissões manualmente](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address) em vez disso, ou para configurar outros firewalls, consulte [Endereços IP da API Anthropic](https://platform.claude.com/docs/en/api/ip-addresses).

Para instâncias [GitHub Enterprise Server](/pt/github-enterprise-server) auto-hospedadas atrás de um firewall, coloque na lista de permissões os mesmos [Endereços IP da API Anthropic](https://platform.claude.com/docs/en/api/ip-addresses) para que a infraestrutura Anthropic possa alcançar seu host GHES para clonar repositórios e postar comentários de revisão.

## Recursos adicionais

* [Configurações de Claude Code](/pt/settings)
* [Referência de variáveis de ambiente](/pt/env-vars)
* [Guia de solução de problemas](/pt/troubleshooting)
