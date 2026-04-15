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

## Certificados CA personalizados

Si su entorno empresarial utiliza CA personalizadas para conexiones HTTPS (ya sea a través de un proxy o acceso directo a la API), configure Claude Code para confiar en ellas:

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

Claude Code requiere acceso a las siguientes URL:

* `api.anthropic.com`: Puntos finales de la API de Claude
* `claude.ai`: autenticación para cuentas de claude.ai
* `platform.claude.com`: autenticación para cuentas de Anthropic Console

Asegúrese de que estas URL estén en la lista blanca en su configuración de proxy y reglas de firewall. Esto es especialmente importante cuando se utiliza Claude Code en entornos de red restringidos o en contenedores.

El instalador nativo y las comprobaciones de actualización también requieren las siguientes URL. Agregue ambas a la lista blanca, ya que el instalador y el actualizador automático descargan desde `storage.googleapis.com` mientras que las descargas de plugins utilizan `downloads.claude.ai`. Si instala Claude Code a través de npm o administra su propia distribución binaria, es posible que los usuarios finales no necesiten acceso:

* `storage.googleapis.com`: depósito de descarga para el binario de Claude Code y el actualizador automático
* `downloads.claude.ai`: CDN que aloja el script de instalación, punteros de versión, manifiestos, claves de firma y ejecutables de plugins

[Claude Code en la web](/es/claude-code-on-the-web) y [Code Review](/es/code-review) se conectan a sus repositorios desde infraestructura administrada por Anthropic. Si su organización de GitHub Enterprise Cloud restringe el acceso por dirección IP, habilite [herencia de lista de permitidos de IP para aplicaciones de GitHub instaladas](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps). La aplicación de GitHub de Claude registra sus rangos de IP, por lo que habilitar esta configuración permite el acceso sin configuración manual. Para [agregar los rangos a su lista de permitidos manualmente](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address) en su lugar, o para configurar otros firewalls, consulte [direcciones IP de la API de Anthropic](https://platform.claude.com/docs/en/api/ip-addresses).

Para instancias de [GitHub Enterprise Server](/es/github-enterprise-server) autohospedadas detrás de un firewall, agregue a la lista blanca las mismas [direcciones IP de la API de Anthropic](https://platform.claude.com/docs/en/api/ip-addresses) para que la infraestructura de Anthropic pueda acceder a su host GHES para clonar repositorios y publicar comentarios de revisión.

## Recursos adicionales

* [Configuración de Claude Code](/es/settings)
* [Referencia de variables de entorno](/es/env-vars)
* [Guía de solución de problemas](/es/troubleshooting)
