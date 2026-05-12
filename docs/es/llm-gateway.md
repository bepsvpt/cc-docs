> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Configuración de la puerta de enlace LLM

> Aprende cómo configurar Claude Code para trabajar con soluciones de puerta de enlace LLM. Cubre requisitos de puerta de enlace, configuración de autenticación, selección de modelos y configuración de puntos finales específicos del proveedor.

Las puertas de enlace LLM proporcionan una capa proxy centralizada entre Claude Code y los proveedores de modelos, a menudo proporcionando:

* **Autenticación centralizada** - Punto único para la gestión de claves API
* **Seguimiento de uso** - Monitorea el uso en equipos y proyectos
* **Controles de costos** - Implementa presupuestos y límites de velocidad
* **Registro de auditoría** - Rastrea todas las interacciones del modelo para cumplimiento normativo
* **Enrutamiento de modelos** - Cambia entre proveedores sin cambios de código

## Requisitos de la puerta de enlace

Para que una puerta de enlace LLM funcione con Claude Code, debe cumplir con los siguientes requisitos:

**Formato de API**

La puerta de enlace debe exponer a los clientes al menos uno de los siguientes formatos de API:

1. **Anthropic Messages**: `/v1/messages`, `/v1/messages/count_tokens`
   * Debe reenviar encabezados de solicitud: `anthropic-beta`, `anthropic-version`

2. **Bedrock InvokeModel**: `/invoke`, `/invoke-with-response-stream`
   * Debe preservar campos del cuerpo de la solicitud: `anthropic_beta`, `anthropic_version`

3. **Vertex rawPredict**: `:rawPredict`, `:streamRawPredict`, `/count-tokens:rawPredict`
   * Debe reenviar encabezados de solicitud: `anthropic-beta`, `anthropic-version`

El incumplimiento de reenvío de encabezados o la preservación de campos del cuerpo puede resultar en funcionalidad reducida o incapacidad de usar características de Claude Code.

<Note>
  Claude Code determina qué características habilitar en función del formato de API. Al usar el formato Anthropic Messages con Bedrock o Vertex, es posible que necesite establecer la variable de entorno `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`.
</Note>

**Encabezados de solicitud**

Claude Code incluye los siguientes encabezados en solicitudes de API:

| Encabezado                      | Descripción                                                                                                                                                                                                                                                                                                                      |
| :------------------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `X-Claude-Code-Session-Id`      | Un identificador único para la sesión actual de Claude Code. Los proxies pueden usar esto para agregar todas las solicitudes de API de una sola sesión sin analizar el cuerpo de la solicitud.                                                                                                                                   |
| `X-Claude-Code-Agent-Id`        | Identificador del subagente o compañero de equipo que emitió la solicitud. Su proxy puede usar esto para atribuir el costo de API a subagentes paralelos individuales dentro de una sesión, sin analizar el cuerpo de la solicitud. Presente solo para solicitudes realizadas por un subagente o compañero de equipo en proceso. |
| `X-Claude-Code-Parent-Agent-Id` | Identificador del agente que generó el agente que realiza la solicitud. Use esto con `X-Claude-Code-Agent-Id` para atribuir costos de API en agentes anidados en su proxy. Presente solo cuando el agente solicitante fue generado por otro agente.                                                                              |

Ambos encabezados de ID de agente son identificadores efímeros por generación, no identificadores persistentes de usuario o dispositivo.

Claude Code también antepone un bloque de atribución corto al mensaje del sistema que contiene la versión del cliente y una huella digital derivada de la conversación. La API de Anthropic elimina este bloque antes de procesarlo, por lo que no afecta el almacenamiento en caché de solicitudes de primer nivel. Si su puerta de enlace implementa su propio caché de solicitudes con clave en el cuerpo de la solicitud completa, establezca [`CLAUDE_CODE_ATTRIBUTION_HEADER=0`](/es/env-vars) para omitirlo.

## Configuración

### Selección de modelo

Por defecto, Claude Code utiliza nombres de modelo estándar para el formato de API seleccionado.

Cuando `ANTHROPIC_BASE_URL` apunta a una puerta de enlace que expone el formato de Mensajes de Anthropic, Claude Code puede consultar el punto final `/v1/models` de la puerta de enlace al inicio y añadir los modelos devueltos al selector `/model`. Establezca `CLAUDE_CODE_ENABLE_GATEWAY_MODEL_DISCOVERY=1` para habilitar esto. El descubrimiento está desactivado por defecto para que las puertas de enlace respaldadas por una clave de API compartida no expongan todos los modelos a los que la clave puede acceder a cada usuario. Cada entrada descubierta se etiqueta como "Desde puerta de enlace" y utiliza el campo `display_name` de la respuesta cuando se proporciona uno. Esto requiere Claude Code v2.1.129 o posterior.

El descubrimiento se aplica solo al formato de Mensajes de Anthropic. No se ejecuta para puntos finales de paso a través de Bedrock o Vertex, y no se ejecuta cuando `ANTHROPIC_BASE_URL` no está configurado o apunta a `api.anthropic.com`.

La solicitud de descubrimiento se autentica de la misma manera que las solicitudes de inferencia: envía `ANTHROPIC_AUTH_TOKEN` como un token portador, o `ANTHROPIC_API_KEY` como el encabezado `x-api-key` cuando no hay un token de autenticación configurado, junto con cualquier encabezado de `ANTHROPIC_CUSTOM_HEADERS`. Solo se añaden al selector los modelos cuyo ID comienza con `claude` o `anthropic`. Los resultados se almacenan en caché en `~/.claude/cache/gateway-models.json` y se actualizan en cada inicio. Si la solicitud falla o la puerta de enlace no implementa `/v1/models`, el selector vuelve a la lista en caché del inicio anterior o a la lista de modelos integrada.

Si su puerta de enlace utiliza nombres de modelo que no coinciden con el filtro de descubrimiento, utilice las variables de entorno documentadas en [Configuración de modelo](/es/model-config) para añadirlos manualmente.

## Configuración de LiteLLM

<Warning>
  Las versiones 1.82.7 y 1.82.8 de LiteLLM PyPI fueron comprometidas con malware que roba credenciales. No instales estas versiones. Si ya las has instalado:

  * Elimina el paquete
  * Rota todas las credenciales en los sistemas afectados
  * Sigue los pasos de remediación en [BerriAI/litellm#24518](https://github.com/BerriAI/litellm/issues/24518)

  LiteLLM es un servicio proxy de terceros. Anthropic no respalda, mantiene ni audita la seguridad o funcionalidad de LiteLLM. Esta guía se proporciona con fines informativos y puede quedar obsoleta. Úsala bajo tu propio criterio.
</Warning>

### Requisitos previos

* Claude Code actualizado a la última versión
* Servidor Proxy de LiteLLM implementado y accesible
* Acceso a modelos Claude a través de tu proveedor elegido

### Configuración básica de LiteLLM

**Configura Claude Code**:

#### Métodos de autenticación

##### Clave API estática

Método más simple usando una clave API fija:

```bash theme={null}
# Establecer en el entorno
export ANTHROPIC_AUTH_TOKEN=sk-litellm-static-key

# O en la configuración de Claude Code
{
  "env": {
    "ANTHROPIC_AUTH_TOKEN": "sk-litellm-static-key"
  }
}
```

Este valor se enviará como encabezado `Authorization`.

##### Clave API dinámica con ayudante

Para claves rotativas o autenticación por usuario:

1. Crea un script ayudante de clave API:

```bash theme={null}
#!/bin/bash
# ~/bin/get-litellm-key.sh

# Ejemplo: Obtener clave del almacén
vault kv get -field=api_key secret/litellm/claude-code

# Ejemplo: Generar token JWT
jwt encode \
  --secret="${JWT_SECRET}" \
  --exp="+1h" \
  '{"user":"'${USER}'","team":"engineering"}'
```

2. Configura la configuración de Claude Code para usar el ayudante:

```json theme={null}
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. Establece el intervalo de actualización de token:

```bash theme={null}
# Actualizar cada hora (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

Este valor se enviará como encabezados `Authorization` y `X-Api-Key`. El `apiKeyHelper` tiene menor precedencia que `ANTHROPIC_AUTH_TOKEN` o `ANTHROPIC_API_KEY`.

#### Punto final unificado (recomendado)

Usando el [punto final de formato Anthropic](https://docs.litellm.ai/docs/anthropic_unified) de LiteLLM:

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**Beneficios del punto final unificado sobre puntos finales de paso directo:**

* Equilibrio de carga
* Alternativas
* Soporte consistente para seguimiento de costos y seguimiento de usuario final

#### Puntos finales de paso directo específicos del proveedor (alternativa)

##### API de Claude a través de LiteLLM

Usando [punto final de paso directo](https://docs.litellm.ai/docs/pass_through/anthropic_completion):

```bash theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### Amazon Bedrock a través de LiteLLM

Usando [punto final de paso directo](https://docs.litellm.ai/docs/pass_through/bedrock):

```bash theme={null}
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### Google Vertex AI a través de LiteLLM

Usando [punto final de paso directo](https://docs.litellm.ai/docs/pass_through/vertex_ai):

```bash theme={null}
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

##### Plataforma Claude en AWS a través de una puerta de enlace

Enruta a una puerta de enlace que reenvía al punto final de [Plataforma Claude en AWS](/es/claude-platform-on-aws):

```bash theme={null}
export ANTHROPIC_AWS_BASE_URL=https://litellm-server:4000/anthropic-aws
export ANTHROPIC_AWS_WORKSPACE_ID=wrkspc_01ABCDEFGHIJKLMN
export CLAUDE_CODE_SKIP_ANTHROPIC_AWS_AUTH=1
export CLAUDE_CODE_USE_ANTHROPIC_AWS=1
```

Para obtener información más detallada, consulta la [documentación de LiteLLM](https://docs.litellm.ai/).

## Recursos adicionales

* [Documentación de LiteLLM](https://docs.litellm.ai/)
* [Configuración de Claude Code](/es/settings)
* [Configuración de red empresarial](/es/network-config)
* [Descripción general de integraciones de terceros](/es/third-party-integrations)
