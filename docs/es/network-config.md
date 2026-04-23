> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuración de red empresarial

> Configure Claude Code para entornos empresariales con servidores proxy, Autoridades de Certificación (CA) personalizadas y autenticación mutua de Seguridad de la Capa de Transporte (mTLS).

Claude Code admite varias configuraciones de red y seguridad empresarial a través de variables de entorno. Esto incluye enrutar el tráfico a través de servidores proxy corporativos, confiar en Autoridades de Certificación (CA) personalizadas y autenticarse con certificados de Seguridad de la Capa de Transporte mutua (mTLS) para mayor seguridad.

<Note>
  Todas las variables de entorno que se muestran en esta página también se pueden configurar en [`settings.json`](/es/settings).
</Note>

## Configuración de proxy

### Variables de entorno

Claude Code respeta las variables de entorno de proxy estándar:

```bash theme={null}
# Proxy HTTPS (recomendado)
export HTTPS_PROXY=https://proxy.example.com:8080

# Proxy HTTP (si HTTPS no está disponible)
export HTTP_PROXY=http://proxy.example.com:8080

# Omitir proxy para solicitudes específicas - formato separado por espacios
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# Omitir proxy para solicitudes específicas - formato separado por comas
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# Omitir proxy para todas las solicitudes
export NO_PROXY="*"
```

<Note>
  Claude Code no admite proxies SOCKS.
</Note>

### Autenticación básica

Si su proxy requiere autenticación básica, incluya las credenciales en la URL del proxy:

```bash theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  Evite codificar contraseñas en scripts. Utilice variables de entorno o almacenamiento seguro de credenciales en su lugar.
</Warning>

<Tip>
  Para proxies que requieren autenticación avanzada (NTLM, Kerberos, etc.), considere utilizar un servicio LLM Gateway que admita su método de autenticación.
</Tip>

## Almacén de certificados CA

De forma predeterminada, Claude Code confía tanto en sus certificados CA de Mozilla incluidos como en el almacén de certificados de su sistema operativo. Los proxies de inspección TLS empresariales como CrowdStrike Falcon y Zscaler funcionan sin configuración adicional cuando su certificado raíz se instala en el almacén de confianza del sistema operativo.

<Note>
  La integración del almacén CA del sistema requiere la distribución binaria nativa de Claude Code. Cuando se ejecuta en el runtime de Node.js, el almacén CA del sistema no se fusiona automáticamente. En ese caso, establezca `NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem` para confiar en una CA raíz empresarial.
</Note>

`CLAUDE_CODE_CERT_STORE` acepta una lista separada por comas de fuentes. Los valores reconocidos son `bundled` para el conjunto de CA de Mozilla incluido con Claude Code y `system` para el almacén de confianza del sistema operativo. El valor predeterminado es `bundled,system`.

Para confiar solo en el conjunto de CA de Mozilla incluido:

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=bundled
```

Para confiar solo en el almacén de certificados del sistema operativo:

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=system
```

<Note>
  `CLAUDE_CODE_CERT_STORE` no tiene una clave de esquema dedicada en `settings.json`. Establézcalo a través del bloque `env` en `~/.claude/settings.json` o directamente en el entorno del proceso.
</Note>

## Certificados CA personalizados

Si su entorno empresarial utiliza una CA personalizada, configure Claude Code para confiar en ella directamente:

```bash theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

## Autenticación mTLS

Para entornos empresariales que requieren autenticación de certificado de cliente:

```bash theme={null}
# Certificado de cliente para autenticación
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# Clave privada del cliente
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# Opcional: Frase de contraseña para clave privada cifrada
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

## Requisitos de acceso a la red

Claude Code requiere acceso a las siguientes URL. Agregue estas a la lista blanca en su configuración de proxy y reglas de firewall, especialmente en entornos de red en contenedores o restringidos.

| URL                            | Requerido para                                                                                                   |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------- |
| `api.anthropic.com`            | Solicitudes de API de Claude                                                                                     |
| `claude.ai`                    | Autenticación de cuenta de claude.ai                                                                             |
| `platform.claude.com`          | Autenticación de cuenta de Anthropic Console                                                                     |
| `downloads.claude.ai`          | Descargas de ejecutables de plugins; instalador nativo y actualizador automático nativo                          |
| `storage.googleapis.com`       | {/* max-version: 2.1.115 */}Instalador nativo y actualizador automático nativo en versiones anteriores a 2.1.116 |
| `bridge.claudeusercontent.com` | Puente WebSocket de la extensión [Claude en Chrome](/es/chrome)                                                  |

Si instala Claude Code a través de npm o administra su propia distribución binaria, es posible que los usuarios finales no necesiten acceso a `downloads.claude.ai` o `storage.googleapis.com`.

Cuando utiliza [Amazon Bedrock](/es/amazon-bedrock), [Google Vertex AI](/es/google-vertex-ai) o [Microsoft Foundry](/es/microsoft-foundry), el tráfico del modelo y la autenticación van a su proveedor en lugar de `api.anthropic.com`, `claude.ai` o `platform.claude.com`. La herramienta WebFetch aún llama a `api.anthropic.com` para su [verificación de seguridad de dominio](/es/data-usage#webfetch-domain-safety-check) a menos que establezca `skipWebFetchPreflight: true` en [configuración](/es/settings).

[Claude Code en la web](/es/claude-code-on-the-web) y [Code Review](/es/code-review) se conectan a sus repositorios desde infraestructura administrada por Anthropic. Si su organización de GitHub Enterprise Cloud restringe el acceso por dirección IP, habilite [herencia de lista de permitidos de IP para aplicaciones de GitHub instaladas](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps). La aplicación de GitHub de Claude registra sus rangos de IP, por lo que habilitar esta configuración permite el acceso sin configuración manual. Para [agregar los rangos a su lista de permitidos manualmente](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address) en su lugar, o para configurar otros firewalls, consulte [direcciones IP de la API de Anthropic](https://platform.claude.com/docs/en/api/ip-addresses).

Para instancias de [GitHub Enterprise Server](/es/github-enterprise-server) autohospedadas detrás de un firewall, agregue a la lista blanca las mismas [direcciones IP de la API de Anthropic](https://platform.claude.com/docs/en/api/ip-addresses) para que la infraestructura de Anthropic pueda acceder a su host GHES para clonar repositorios y publicar comentarios de revisión.

## Recursos adicionales

* [Configuración de Claude Code](/es/settings)
* [Referencia de variables de entorno](/es/env-vars)
* [Guía de solución de problemas](/es/troubleshooting)
