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
  Claude Code determina qué características habilitar en función del formato de API. Al usar el formato Anthropic Messages con Bedrock o Vertex, es posible que necesites establecer la variable de entorno `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`.
</Note>

## Configuración

### Selección de modelo

Por defecto, Claude Code utilizará nombres de modelo estándar para el formato de API seleccionado.

Si has configurado nombres de modelo personalizados en tu puerta de enlace, utiliza las variables de entorno documentadas en [Configuración de modelo](/es/model-config) para que coincidan con tus nombres personalizados.

## Configuración de LiteLLM

<Note>
  LiteLLM es un servicio proxy de terceros. Anthropic no respalda, mantiene ni audita la seguridad o funcionalidad de LiteLLM. Esta guía se proporciona con fines informativos y puede quedar obsoleta. Úsala bajo tu propio criterio.
</Note>

### Requisitos previos

* Claude Code actualizado a la última versión
* Servidor Proxy de LiteLLM implementado y accesible
* Acceso a modelos Claude a través de tu proveedor elegido

### Configuración básica de LiteLLM

**Configura Claude Code**:

#### Métodos de autenticación

##### Clave API estática

Método más simple usando una clave API fija:

```bash  theme={null}
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

```bash  theme={null}
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

```json  theme={null}
{
  "apiKeyHelper": "~/bin/get-litellm-key.sh"
}
```

3. Establece el intervalo de actualización de token:

```bash  theme={null}
# Actualizar cada hora (3600000 ms)
export CLAUDE_CODE_API_KEY_HELPER_TTL_MS=3600000
```

Este valor se enviará como encabezados `Authorization` y `X-Api-Key`. El `apiKeyHelper` tiene menor precedencia que `ANTHROPIC_AUTH_TOKEN` o `ANTHROPIC_API_KEY`.

#### Punto final unificado (recomendado)

Usando el [punto final de formato Anthropic](https://docs.litellm.ai/docs/anthropic_unified) de LiteLLM:

```bash  theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000
```

**Beneficios del punto final unificado sobre puntos finales de paso directo:**

* Equilibrio de carga
* Alternativas
* Soporte consistente para seguimiento de costos y seguimiento de usuario final

#### Puntos finales de paso directo específicos del proveedor (alternativa)

##### API de Claude a través de LiteLLM

Usando [punto final de paso directo](https://docs.litellm.ai/docs/pass_through/anthropic_completion):

```bash  theme={null}
export ANTHROPIC_BASE_URL=https://litellm-server:4000/anthropic
```

##### Amazon Bedrock a través de LiteLLM

Usando [punto final de paso directo](https://docs.litellm.ai/docs/pass_through/bedrock):

```bash  theme={null}
export ANTHROPIC_BEDROCK_BASE_URL=https://litellm-server:4000/bedrock
export CLAUDE_CODE_SKIP_BEDROCK_AUTH=1
export CLAUDE_CODE_USE_BEDROCK=1
```

##### Google Vertex AI a través de LiteLLM

Usando [punto final de paso directo](https://docs.litellm.ai/docs/pass_through/vertex_ai):

```bash  theme={null}
export ANTHROPIC_VERTEX_BASE_URL=https://litellm-server:4000/vertex_ai/v1
export ANTHROPIC_VERTEX_PROJECT_ID=your-gcp-project-id
export CLAUDE_CODE_SKIP_VERTEX_AUTH=1
export CLAUDE_CODE_USE_VERTEX=1
export CLOUD_ML_REGION=us-east5
```

Para obtener información más detallada, consulta la [documentación de LiteLLM](https://docs.litellm.ai/).

## Recursos adicionales

* [Documentación de LiteLLM](https://docs.litellm.ai/)
* [Configuración de Claude Code](/es/settings)
* [Configuración de red empresarial](/es/network-config)
* [Descripción general de integraciones de terceros](/es/third-party-integrations)
