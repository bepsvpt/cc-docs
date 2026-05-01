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

```bash theme={null}
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

```bash theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  Evite codificar senhas em scripts. Use variáveis de ambiente ou armazenamento seguro de credenciais.
</Warning>

<Tip>
  Para proxies que exigem autenticação avançada (NTLM, Kerberos, etc.), considere usar um serviço LLM Gateway que suporte seu método de autenticação.
</Tip>

## Armazenamento de certificados CA

Por padrão, Claude Code confia tanto em seus certificados CA Mozilla agrupados quanto no armazenamento de certificados do seu sistema operacional. Proxies de inspeção TLS empresariais, como CrowdStrike Falcon e Zscaler, funcionam sem configuração adicional quando seu certificado raiz é instalado no armazenamento de confiança do SO.

<Note>
  A integração do armazenamento de CA do sistema requer a distribuição binária nativa do Claude Code. Ao executar no tempo de execução Node.js, o armazenamento de CA do sistema não é mesclado automaticamente. Nesse caso, defina `NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem` para confiar em uma CA raiz empresarial.
</Note>

`CLAUDE_CODE_CERT_STORE` aceita uma lista separada por vírgulas de fontes. Os valores reconhecidos são `bundled` para o conjunto de CA Mozilla enviado com Claude Code e `system` para o armazenamento de confiança do sistema operacional. O padrão é `bundled,system`.

Para confiar apenas no conjunto de CA Mozilla agrupado:

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=bundled
```

Para confiar apenas no armazenamento de certificados do SO:

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=system
```

<Note>
  `CLAUDE_CODE_CERT_STORE` não possui uma chave de esquema dedicada em `settings.json`. Defina-a através do bloco `env` em `~/.claude/settings.json` ou diretamente no ambiente do processo.
</Note>

## Certificados CA personalizados

Se seu ambiente empresarial usa uma CA personalizada, configure Claude Code para confiar nela diretamente:

```bash theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## Autenticação mTLS

Para ambientes empresariais que exigem autenticação de certificado de cliente:

```bash theme={null}
# Certificado de cliente para autenticação
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Chave privada do cliente
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Opcional: Frase de acesso para chave privada criptografada
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## Requisitos de acesso à rede

Claude Code requer acesso aos seguintes URLs. Coloque esses URLs na lista de permissões em sua configuração de proxy e regras de firewall, especialmente em ambientes de rede containerizados ou restritos.

| URL                            | Necessário para                                                                                               |
| ------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| `api.anthropic.com`            | Solicitações da API Claude                                                                                    |
| `claude.ai`                    | Autenticação de conta claude.ai                                                                               |
| `platform.claude.com`          | Autenticação de conta do Anthropic Console                                                                    |
| `downloads.claude.ai`          | Downloads de executáveis de plugins; instalador nativo e atualizador automático nativo                        |
| `storage.googleapis.com`       | {/* max-version: 2.1.115 */}Instalador nativo e atualizador automático nativo em versões anteriores a 2.1.116 |
| `bridge.claudeusercontent.com` | Ponte WebSocket da extensão [Claude no Chrome](/pt/chrome)                                                    |

Se você instalar Claude Code através do npm ou gerenciar sua própria distribuição binária, os usuários finais podem não precisar de acesso a `downloads.claude.ai` ou `storage.googleapis.com`.

Claude Code também envia telemetria operacional opcional por padrão, que você pode desabilitar com variáveis de ambiente. Consulte [Serviços de telemetria](/pt/data-usage#telemetry-services) para saber como desabilitá-la antes de finalizar sua lista de permissões.

Ao usar [Amazon Bedrock](/pt/amazon-bedrock), [Google Vertex AI](/pt/google-vertex-ai) ou [Microsoft Foundry](/pt/microsoft-foundry), o tráfego de modelo e autenticação vão para seu provedor em vez de `api.anthropic.com`, `claude.ai` ou `platform.claude.com`. A ferramenta WebFetch ainda chama `api.anthropic.com` para sua [verificação de segurança de domínio](/pt/data-usage#webfetch-domain-safety-check) a menos que você defina `skipWebFetchPreflight: true` em [configurações](/pt/settings).

[Claude Code na web](/pt/claude-code-on-the-web) e [Code Review](/pt/code-review) se conectam aos seus repositórios a partir da infraestrutura gerenciada pela Anthropic. Se sua organização GitHub Enterprise Cloud restringe o acesso por endereço IP, ative [herança de lista de permissão de IP para GitHub Apps instalados](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps). O Claude GitHub App registra seus intervalos de IP, portanto, ativar essa configuração permite acesso sem configuração manual. Para [adicionar os intervalos à sua lista de permissões manualmente](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address) em vez disso, ou para configurar outros firewalls, consulte [Endereços IP da API Anthropic](https://platform.claude.com/docs/en/api/ip-addresses).

Para instâncias [GitHub Enterprise Server](/pt/github-enterprise-server) auto-hospedadas atrás de um firewall, coloque na lista de permissões os mesmos [Endereços IP da API Anthropic](https://platform.claude.com/docs/en/api/ip-addresses) para que a infraestrutura Anthropic possa alcançar seu host GHES para clonar repositórios e postar comentários de revisão.

## Recursos adicionais

* [Configurações de Claude Code](/pt/settings)
* [Referência de variáveis de ambiente](/pt/env-vars)
* [Guia de solução de problemas](/pt/troubleshooting)
